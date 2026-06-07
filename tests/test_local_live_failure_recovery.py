"""Phase 14B.1 — tests for the controlled failure/recovery proof path and the
hardened local-live read model.

These build on the Phase 14A.1 suite (which is preserved unchanged) and cover
the new deterministic failure scenarios, durable failure evidence, the safe
read-model contract (no raw story text, no absolute paths), and the controlled
action validation for scenarios.
"""

from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from storytime.local_live.proof_run import (
    APPROVED_SCENARIOS,
    ProofRunError,
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
# A distinctive phrase from the fixture's story *body* (not its title). It must
# never appear in any read-model output — only bounded metadata is exposed.
_STORY_BODY_PHRASE = "walked the quiet street"

_FAILURE_SCENARIOS = ("governance_failure", "artifact_validation_failure")


@pytest.fixture()
def service(tmp_path: Path) -> LocalLiveService:
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    return LocalLiveService(
        db_path=runs_dir / "state.db",
        runs_dir=runs_dir,
        fixtures_dir=_FIXTURES_DIR,
    )


def _iter_strings(value: Any) -> Iterator[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from _iter_strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from _iter_strings(v)


def _enqueue_and_drain(
    service: LocalLiveService, payload: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Post a proof-run request (which enqueues), drain the worker, return
    (post_body, run_detail).

    Phase 14C.1 separates acceptance from execution: the request enqueues a
    durable work item (HTTP 202, status ``queued``) and a local worker executes
    it. These helpers drive the worker synchronously so the end-state assertions
    are deterministic.
    """
    status, body = service.create_proof_run(payload)
    assert status == 202, f"expected 202 accepted, got {status}: {body}"
    assert body["status"] == "queued"
    assert body["queueState"] == "queued"
    service.drain_queue()
    _, detail = service.run_detail(body["runId"])
    return body, detail


# -- success regression (must not be weakened) ----------------------------


def test_success_scenario_still_completes(service: LocalLiveService) -> None:
    body, detail = _enqueue_and_drain(service, {"scenario": "success"})
    assert body["scenario"] == "success"
    assert detail["status"] == "completed"
    assert detail["failureReason"] is None
    assert len(detail["stages"]) == 4


def test_default_scenario_is_success(service: LocalLiveService) -> None:
    status, body = service.create_proof_run({})
    assert status == 202
    assert body["scenario"] == "success"


# -- controlled failure scenarios -----------------------------------------


@pytest.mark.parametrize("scenario", _FAILURE_SCENARIOS)
def test_failure_scenario_persists_failed_run(
    service: LocalLiveService, scenario: str
) -> None:
    body, _ = _enqueue_and_drain(service, {"scenario": scenario})
    run_id = body["runId"]
    # Read back through a fresh connection: the failed run is durable.
    with StateStore.open(service.db_path) as store:
        run = store.get_run(run_id)
        assert run is not None
        assert run.status == "failed"
        stages = store.list_stage_executions(run_id)
        assert any(s.status == "failed" for s in stages)


@pytest.mark.parametrize("scenario", _FAILURE_SCENARIOS)
def test_failure_scenario_exposes_deterministic_reason(
    service: LocalLiveService, scenario: str
) -> None:
    _, detail = _enqueue_and_drain(service, {"scenario": scenario})
    assert detail["failureReason"], "no failure reason exposed"
    # Deterministic: a second run yields the same reason.
    _, detail2 = _enqueue_and_drain(service, {"scenario": scenario})
    assert detail["failureReason"] == detail2["failureReason"]


@pytest.mark.parametrize("scenario", _FAILURE_SCENARIOS)
def test_failure_event_log_includes_failure_evidence(
    service: LocalLiveService, scenario: str
) -> None:
    _, detail = _enqueue_and_drain(service, {"scenario": scenario})
    event_types = [e["eventType"] for e in detail["events"]]
    assert "RunFailed" in event_types
    run_failed = next(e for e in detail["events"] if e["eventType"] == "RunFailed")
    assert run_failed["payload"].get("failedStage")
    assert run_failed["payload"].get("reason")


def test_failure_scenario_produces_artifact_evidence(
    service: LocalLiveService,
) -> None:
    _, detail = _enqueue_and_drain(service, {"scenario": "governance_failure"})
    assert len(detail["artifacts"]) == 1
    art = detail["artifacts"][0]
    assert art["sha256"]
    assert art["bytes"] > 0


def test_server_survives_repeated_failures(service: LocalLiveService) -> None:
    for _ in range(3):
        status, _ = service.create_proof_run({"scenario": "governance_failure"})
        assert status == 202  # the service does not crash on failure scenarios
    # the worker drains all of them into durable failed state without crashing
    service.drain_queue()
    _, runs_body = service.list_runs()
    assert all(r["status"] == "failed" for r in runs_body["runs"])


# -- read-model safety -----------------------------------------------------


def test_read_model_does_not_expose_raw_story_text(
    service: LocalLiveService,
) -> None:
    body, detail = _enqueue_and_drain(service, {"scenario": "success"})
    blob = json.dumps(detail)
    assert _STORY_BODY_PHRASE not in blob
    # The evidence artifact on disk also must not contain the body text.
    evidence = service.runs_dir / body["runId"] / "proof" / "evidence.json"
    assert _STORY_BODY_PHRASE not in evidence.read_text()


def test_read_model_does_not_expose_absolute_paths(
    service: LocalLiveService,
) -> None:
    service.create_proof_run({"scenario": "success"})
    _, runs_body = service.list_runs()
    run_id = runs_body["runs"][0]["runId"]
    _, detail = service.run_detail(run_id)
    _, health = service.health()
    for payload in (detail, health, runs_body):
        for s in _iter_strings(payload):
            assert not s.startswith("/"), f"absolute POSIX path leaked: {s!r}"
            assert not (len(s) > 2 and s[1] == ":" and s[2] == "\\"), (
                f"absolute Windows path leaked: {s!r}"
            )


def test_health_exposes_scenarios_and_no_db_path(
    service: LocalLiveService,
) -> None:
    _, health = service.health()
    assert "dbPath" not in health
    assert set(health["scenarios"]) == set(APPROVED_SCENARIOS)


# -- controlled action validation -----------------------------------------


def test_unknown_scenario_rejected(service: LocalLiveService) -> None:
    status, body = service.create_proof_run({"scenario": "demo_error"})
    assert status == 400
    assert "allowedScenarios" in body


def test_arbitrary_fields_rejected(service: LocalLiveService) -> None:
    for bad in (
        {"text": "once upon a time"},
        {"path": "/etc/passwd"},
        {"url": "http://example.com"},
        {"provider": "openai"},
        {"scenario": "success", "command": "rm -rf /"},
    ):
        status, _ = service.create_proof_run(bad)
        assert status == 400, f"expected rejection for {bad}"


def test_fixture_id_alias_accepted(service: LocalLiveService) -> None:
    # Both the new fixtureId and the back-compat fixture alias work.
    assert service.create_proof_run({"fixtureId": "golden-path"})[0] == 202
    assert service.create_proof_run({"fixture": "golden-path"})[0] == 202


def test_harness_rejects_unknown_scenario_directly(
    service: LocalLiveService,
) -> None:
    with StateStore.open(service.db_path) as store, pytest.raises(ProofRunError):
        run_proof_fixture(
            store,
            runs_dir=service.runs_dir,
            scenario="not-a-scenario",
            fixtures_dir=_FIXTURES_DIR,
        )


# -- HTTP loopback / origin / error shape ----------------------------------


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


def _post(
    url: str, raw_body: bytes, *, origin: str | None = None
) -> tuple[int, str | None, dict]:
    req = urllib.request.Request(url, data=raw_body, method="POST")
    req.add_header("Content-Type", "application/json")
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


def test_http_invalid_json_rejected_as_json(live_base_url: str) -> None:
    status, _, body = _post(
        f"{live_base_url}/api/proof-runs", b"{not json", origin="http://localhost:5173"
    )
    assert status == 400
    assert body["error"]  # a deterministic JSON error, not an HTML page


def test_http_failure_scenario_over_http(
    live_base_url: str, service: LocalLiveService
) -> None:
    status, acao, body = _post(
        f"{live_base_url}/api/proof-runs",
        json.dumps({"scenario": "governance_failure"}).encode(),
        origin="http://localhost:5173",
    )
    # Acceptance enqueues (202); CORS stays allowlisted, never wildcard.
    assert status == 202
    assert body["queueState"] == "queued"
    assert acao == "http://localhost:5173"
    assert acao != "*"
    # The local worker drains the queued item into durable failed state.
    service.drain_queue()
    _, detail = service.run_detail(body["runId"])
    assert detail["status"] == "failed"
    assert detail["failureReason"]
