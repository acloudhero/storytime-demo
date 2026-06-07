"""Phase 14A.1 — tests for the local-live proof loop.

Covers the durable proof-run harness, the read model, the controlled action
validation, durability across a simulated server restart, and the loopback /
strict-origin HTTP policy.
"""

from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from collections.abc import Iterator
from pathlib import Path

import pytest

from storytime.local_live.proof_run import (
    APPROVED_FIXTURES,
    ProofRunError,
    default_fixtures_dir,
    run_proof_fixture,
)
from storytime.local_live.server import (
    LocalLiveService,
    default_allowed_origins,
    make_server,
)
from storytime.state import StateStore

_REPO_ROOT = Path(__file__).resolve().parents[1]
_FIXTURES_DIR = _REPO_ROOT / "demo" / "seed"


@pytest.fixture()
def service(tmp_path: Path) -> LocalLiveService:
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    return LocalLiveService(
        db_path=runs_dir / "state.db",
        runs_dir=runs_dir,
        fixtures_dir=_FIXTURES_DIR,
    )


# -- proof-run harness + durability ---------------------------------------


def test_proof_run_persists_real_durable_state(service: LocalLiveService) -> None:
    with StateStore.open(service.db_path) as store:
        run_id = run_proof_fixture(
            store, runs_dir=service.runs_dir, fixtures_dir=_FIXTURES_DIR
        )
    # A fresh connection (simulating a server restart) must still see the run.
    with StateStore.open(service.db_path) as store2:
        run = store2.get_run(run_id)
        assert run is not None
        assert run.status == "completed"
        stages = store2.list_stage_executions(run_id)
        artifacts = store2.list_stage_artifacts(run_id)
        assert len(stages) == 4
        assert len(artifacts) == 1
        assert store2.count_events(run_id) == 6


def test_proof_run_writes_real_evidence_artifact(service: LocalLiveService) -> None:
    with StateStore.open(service.db_path) as store:
        run_id = run_proof_fixture(
            store, runs_dir=service.runs_dir, fixtures_dir=_FIXTURES_DIR
        )
    evidence = service.runs_dir / run_id / "proof" / "evidence.json"
    assert evidence.is_file()
    data = json.loads(evidence.read_text())
    assert data["mode"] == "proof"
    assert data["mock"] is True
    assert data["fixture"]["license"]  # bounded fixture metadata present
    # The raw story text is never written into the evidence artifact.
    assert "text" not in data["fixture"]


def test_proof_run_rejects_unknown_fixture(service: LocalLiveService) -> None:
    with StateStore.open(service.db_path) as store, pytest.raises(ProofRunError):
        run_proof_fixture(
            store,
            runs_dir=service.runs_dir,
            fixture_id="../etc/passwd",
            fixtures_dir=_FIXTURES_DIR,
        )


def test_restart_survives_across_multiple_runs(service: LocalLiveService) -> None:
    ids = []
    for _ in range(3):
        with StateStore.open(service.db_path) as store:
            ids.append(
                run_proof_fixture(
                    store, runs_dir=service.runs_dir, fixtures_dir=_FIXTURES_DIR
                )
            )
    status, body = service.list_runs()
    assert status == 200
    assert {r["runId"] for r in body["runs"]} == set(ids)


# -- read model + service endpoints ---------------------------------------


def test_health_reports_backend_owned_state(service: LocalLiveService) -> None:
    status, body = service.health()
    assert status == 200
    assert body["loopbackOnly"] is True
    assert body["wildcardOriginAllowed"] is False
    assert body["stateOwner"] == "backend-sqlite"
    assert body["browserAuthority"] == "request-only"


def test_list_runs_empty_before_any_run(service: LocalLiveService) -> None:
    status, body = service.list_runs()
    assert status == 200
    assert body["runs"] == []


def test_run_detail_exposes_stages_artifacts_events(
    service: LocalLiveService,
) -> None:
    status, created = service.create_proof_run({})
    assert status == 202  # request acceptance enqueues; execution is by a worker
    run_id = created["runId"]
    service.drain_queue()  # local worker claims and executes the queued item
    status, detail = service.run_detail(run_id)
    assert status == 200
    assert detail["status"] == "completed"
    assert len(detail["stages"]) == 4
    assert len(detail["artifacts"]) == 1
    assert detail["artifacts"][0]["sha256"]  # hash computed from the real file
    assert detail["artifacts"][0]["bytes"] > 0
    event_types = [e["eventType"] for e in detail["events"]]
    assert "RunCreated" in event_types
    assert "RunCompleted" in event_types


def test_run_detail_404_for_unknown_run(service: LocalLiveService) -> None:
    assert service.run_detail("does-not-exist")[0] == 404


# -- controlled action validation -----------------------------------------


def test_proof_action_accepts_empty_body(service: LocalLiveService) -> None:
    assert service.create_proof_run({})[0] == 202
    assert service.create_proof_run(None)[0] == 202


def test_proof_action_accepts_allowlisted_fixture(service: LocalLiveService) -> None:
    status, body = service.create_proof_run({"fixture": "golden-path"})
    assert status == 202
    assert body["source"] == "approved-fixture"


def test_proof_action_rejects_extra_fields(service: LocalLiveService) -> None:
    status, body = service.create_proof_run(
        {"fixture": "golden-path", "text": "arbitrary story"}
    )
    assert status == 400
    assert body["error"] == "unexpected_fields"


def test_proof_action_rejects_unknown_fixture(service: LocalLiveService) -> None:
    status, body = service.create_proof_run({"fixture": "evil"})
    assert status == 400
    assert "allowedFixtures" in body


def test_proof_action_rejects_non_object_body(service: LocalLiveService) -> None:
    assert service.create_proof_run(["not", "an", "object"])[0] == 400
    assert service.create_proof_run("just a string")[0] == 400


def test_allowlist_contains_only_golden_path() -> None:
    assert set(APPROVED_FIXTURES) == {"golden-path"}


def test_fixtures_dir_resolves_in_repo() -> None:
    found = default_fixtures_dir(_REPO_ROOT)
    assert (found / "demo-golden-path.json").is_file()


# -- HTTP loopback / origin policy ----------------------------------------


@pytest.fixture()
def live_base_url(service: LocalLiveService) -> Iterator[str]:
    httpd = make_server(
        service,
        host="127.0.0.1",
        port=0,
        allowed_origins=default_allowed_origins(5173),
    )
    host, port = httpd.server_address[0], httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://{host}:{port}"
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=5)


def _get(url: str, *, origin: str | None = None) -> tuple[int, str | None, dict]:
    req = urllib.request.Request(url, method="GET")
    if origin:
        req.add_header("Origin", origin)
    try:
        with urllib.request.urlopen(req) as resp:  # noqa: S310 - loopback test
            return (
                resp.status,
                resp.headers.get("Access-Control-Allow-Origin"),
                json.loads(resp.read()),
            )
    except urllib.error.HTTPError as exc:  # noqa: PERF203
        return (
            exc.code,
            exc.headers.get("Access-Control-Allow-Origin"),
            json.loads(exc.read()),
        )


def test_http_health_ok(live_base_url: str) -> None:
    status, _, body = _get(f"{live_base_url}/health")
    assert status == 200
    assert body["status"] == "ok"


def test_http_allows_vite_origin_without_wildcard(live_base_url: str) -> None:
    status, acao, _ = _get(
        f"{live_base_url}/api/runs", origin="http://localhost:5173"
    )
    assert status == 200
    assert acao == "http://localhost:5173"
    assert acao != "*"


def test_http_rejects_unknown_origin(live_base_url: str) -> None:
    status, acao, body = _get(
        f"{live_base_url}/api/runs", origin="http://evil.example.com"
    )
    assert status == 403
    assert acao is None
    assert body["error"] == "forbidden_origin"


def test_http_unknown_route_404(live_base_url: str) -> None:
    assert _get(f"{live_base_url}/api/nope")[0] == 404
