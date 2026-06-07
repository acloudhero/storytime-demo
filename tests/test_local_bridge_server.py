"""Phase 13G — local-bridge HTTP server & controlled-execution tests.

These start a real loopback bridge bound to an OS-selected port (``port=0``) and
exercise it over HTTP: binding safety, strict origin policy, the endpoint set,
method/path/JSON rejection, allowlist enforcement, the ``202 Accepted`` async
path, and the one controlled real action (``retry_failed_stage``) running to
honest completion inside an isolated temporary workspace. No browser, no
frontend dev server, no network beyond loopback, and no real user workspace.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

from storytime.http import UnsafeBindError
from storytime.local_bridge.dto import validate_response_shape
from storytime.local_bridge.server import LocalBridgeServer
from storytime.state import RunRecord, StateStore
from storytime.util.clock import FixedClock

_WORKSPACE_ID = "ws-demo-0001"
_ELIGIBLE_RUN = "01RUNELIGIBLE00000000000000"


def _seed_eligible_workspace(root: Path) -> None:
    """Create a state.db with a failed-but-retry-eligible, governance-approved run."""
    with StateStore.open(root / "state.db") as store, store.transaction():
        store.create_run(
            RunRecord(
                pipeline_run_id=_ELIGIBLE_RUN,
                created_at="2026-05-25T10:00:00+00:00",
                updated_at="2026-05-25T10:01:00+00:00",
                current_stage="synthesize",
                status="failed",
                source_manifest_hash="a" * 64,
                run_dir=_ELIGIBLE_RUN,
            )
        )
        store.record_stage_execution(
            pipeline_run_id=_ELIGIBLE_RUN,
            stage_name="ingest",
            started_at="2026-05-25T10:00:00+00:00",
            ended_at="2026-05-25T10:00:30+00:00",
            status="succeeded",
        )
        store.record_stage_execution(
            pipeline_run_id=_ELIGIBLE_RUN,
            stage_name="synthesize",
            started_at="2026-05-25T10:00:30+00:00",
            ended_at="2026-05-25T10:01:00+00:00",
            status="failed",
            error_kind="TtsError",
        )
        store.record_trust_envelope(
            pipeline_run_id=_ELIGIBLE_RUN,
            source_ref="src-eligible",
            schema_version="1",
            license_type="US_PUBLIC_DOMAIN",
            decision="APPROVED",
            decision_timestamp="2026-05-25T09:55:00+00:00",
            approver_id="operator",
            blocked_reason=None,
            envelope_key=f"{_ELIGIBLE_RUN}/governance/trust-envelope.json",
            recorded_at="2026-05-25T10:00:30+00:00",
        )


@pytest.fixture()
def bridge_server(tmp_path: Path) -> Iterator[LocalBridgeServer]:
    _seed_eligible_workspace(tmp_path)
    server = LocalBridgeServer(
        host="127.0.0.1",
        port=0,
        workspace_id=_WORKSPACE_ID,
        workspace_root=tmp_path,
        clock=FixedClock(datetime(2026, 5, 28, tzinfo=UTC)),
        capacity=4,
    )
    server.serve_forever_in_thread()
    try:
        yield server
    finally:
        server.shutdown()


def _get(url: str, *, headers: dict[str, str] | None = None) -> tuple[int, dict[str, Any]]:
    req = urllib.request.Request(url, headers=headers or {}, method="GET")
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read())


def _post(
    url: str, body: Any, *, headers: dict[str, str] | None = None
) -> tuple[int, dict[str, Any]]:
    data = json.dumps(body).encode("utf-8") if body is not None else b""
    hdrs = {"Content-Type": "application/json"}
    hdrs.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=hdrs, method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read())


def _retry_request() -> dict[str, Any]:
    return {
        "schemaVersion": "1.0",
        "requestId": "req-retry-1",
        "mode": "local",
        "action": "retry_failed_stage",
        "target": {"runId": _ELIGIBLE_RUN, "stageId": f"{_ELIGIBLE_RUN}:synthesize"},
        "workspace": {"id": _WORKSPACE_ID, "root": "storytime-workspace", "slot": "active"},
        "storageTarget": {"type": "local-disk"},
        "dryRun": False,
        "requiresConfirmation": True,
        "requestedAt": "2026-05-27T12:00:00Z",
        "operatorIntent": "Resume the failed run from the failed stage.",
        "preconditions": ["Blocked stage is retry-eligible."],
        "evidenceRefs": ["Pipeline Run Detail"],
        "idempotencyKey": "idem-retry-eligible-0001",
        "executionTiming": "async-long-running",
    }


def _await_status(server: LocalBridgeServer, action_request_id: str) -> dict[str, Any]:
    url = f"{server.url}/actions/{action_request_id}"
    for _ in range(100):
        status, body = _get(url)
        if body.get("status") in ("completed", "failed"):
            return body
        time.sleep(0.02)
    raise AssertionError("action did not reach a terminal state in time")


# ── binding safety ───────────────────────────────────────────────────────


def test_construction_rejects_all_interfaces_bind(tmp_path: Path) -> None:
    with pytest.raises(UnsafeBindError):
        LocalBridgeServer(
            host="0.0.0.0",
            port=0,
            workspace_id=_WORKSPACE_ID,
            workspace_root=tmp_path,
        )


def test_construction_rejects_public_host(tmp_path: Path) -> None:
    with pytest.raises(UnsafeBindError):
        LocalBridgeServer(
            host="192.168.1.10",
            port=0,
            workspace_id=_WORKSPACE_ID,
            workspace_root=tmp_path,
        )


def test_server_binds_loopback_only(bridge_server: LocalBridgeServer) -> None:
    assert bridge_server.bind_host == "127.0.0.1"
    assert bridge_server.url.startswith("http://127.0.0.1:")


# ── endpoints ──────────────────────────────────────────────────────────────


def test_health_endpoint(bridge_server: LocalBridgeServer) -> None:
    status, body = _get(f"{bridge_server.url}/health")
    assert status == 200
    assert body["status"] == "ok"


def test_ready_endpoint_reports_security_posture(bridge_server: LocalBridgeServer) -> None:
    status, body = _get(f"{bridge_server.url}/ready")
    assert status == 200
    assert body["loopbackOnly"] is True
    assert body["wildcardOriginAllowed"] is False
    assert body["maxConcurrency"] == 1
    assert body["workspaceConfigured"] is True
    assert body["executableActions"] == ["retry_failed_stage"]
    assert body["queueImplemented"] is True


def test_queue_endpoint_shape(bridge_server: LocalBridgeServer) -> None:
    status, body = _get(f"{bridge_server.url}/queue")
    assert status == 200
    for key in (
        "queueDepth",
        "inFlightCount",
        "completedCount",
        "failedCount",
        "rejectedCount",
        "deadLetterCount",
        "capacity",
        "saturationRatio",
        "maxConcurrency",
    ):
        assert key in body


def test_action_status_unknown_id_is_404(bridge_server: LocalBridgeServer) -> None:
    status, body = _get(f"{bridge_server.url}/actions/act-does-not-exist")
    assert status == 404
    assert body["status"] == "rejected"


# ── origin / CORS policy ───────────────────────────────────────────────────


def test_mismatched_origin_is_forbidden(bridge_server: LocalBridgeServer) -> None:
    status, body = _get(
        f"{bridge_server.url}/health",
        headers={"Origin": "https://evil.example.com"},
    )
    assert status == 403
    assert body["errors"][0]["code"] == "origin_forbidden"


def test_matching_origin_is_allowed_and_echoed_exactly(
    bridge_server: LocalBridgeServer,
) -> None:
    origin = sorted(bridge_server.allowed_origins)[0]
    req = urllib.request.Request(
        f"{bridge_server.url}/health", headers={"Origin": origin}, method="GET"
    )
    resp = urllib.request.urlopen(req, timeout=5)
    echoed = resp.headers.get("Access-Control-Allow-Origin")
    assert echoed == origin
    assert echoed != "*"


def test_no_wildcard_origin_is_ever_emitted(bridge_server: LocalBridgeServer) -> None:
    # No Origin header → no ACAO header at all (and certainly not a wildcard).
    req = urllib.request.Request(f"{bridge_server.url}/health", method="GET")
    resp = urllib.request.urlopen(req, timeout=5)
    assert resp.headers.get("Access-Control-Allow-Origin") != "*"


def test_preflight_rejects_unknown_origin(bridge_server: LocalBridgeServer) -> None:
    req = urllib.request.Request(
        f"{bridge_server.url}/actions",
        headers={"Origin": "https://evil.example.com"},
        method="OPTIONS",
    )
    with pytest.raises(urllib.error.HTTPError) as exc:
        urllib.request.urlopen(req, timeout=5)
    assert exc.value.code == 403


# ── method / path / body rejection ─────────────────────────────────────────


def test_unsupported_method_is_405(bridge_server: LocalBridgeServer) -> None:
    req = urllib.request.Request(f"{bridge_server.url}/actions", method="DELETE")
    with pytest.raises(urllib.error.HTTPError) as exc:
        urllib.request.urlopen(req, timeout=5)
    assert exc.value.code == 405


def test_unknown_path_is_404(bridge_server: LocalBridgeServer) -> None:
    status, _ = _get(f"{bridge_server.url}/nope")
    assert status == 404


def test_malformed_json_is_rejected(bridge_server: LocalBridgeServer) -> None:
    req = urllib.request.Request(
        f"{bridge_server.url}/actions",
        data=b"{not json",
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with pytest.raises(urllib.error.HTTPError) as exc:
        urllib.request.urlopen(req, timeout=5)
    assert exc.value.code == 400
    body = json.loads(exc.value.read())
    assert body["errors"][0]["code"] == "malformed_json"


def test_non_json_content_type_is_rejected(bridge_server: LocalBridgeServer) -> None:
    req = urllib.request.Request(
        f"{bridge_server.url}/actions",
        data=b"hello",
        headers={"Content-Type": "text/plain"},
        method="POST",
    )
    with pytest.raises(urllib.error.HTTPError) as exc:
        urllib.request.urlopen(req, timeout=5)
    assert exc.value.code == 415


# ── allowlist / unsafe-field rejection over HTTP ───────────────────────────


def test_unknown_action_rejected_over_http(bridge_server: LocalBridgeServer) -> None:
    payload = _retry_request()
    payload["action"] = "totally_unknown"
    status, body = _post(f"{bridge_server.url}/actions", payload)
    assert status == 422
    assert body["status"] == "rejected"
    assert any(e["code"] == "unknown_action" for e in body["errors"])


def test_smuggled_command_rejected_over_http(bridge_server: LocalBridgeServer) -> None:
    payload = _retry_request()
    payload["command"] = "rm -rf /"
    status, body = _post(f"{bridge_server.url}/actions", payload)
    assert status == 422
    assert any(e["code"] in {"unsafe_field", "unsafe_value"} for e in body["errors"])


# ── controlled async retry execution ───────────────────────────────────────


def test_retry_returns_202_accepted_with_handle(bridge_server: LocalBridgeServer) -> None:
    status, body = _post(f"{bridge_server.url}/actions", _retry_request())
    assert status == 202
    assert body["accepted"] is True
    assert body["status"] == "accepted"
    assert body["actionRequestId"] and body["jobId"]
    assert validate_response_shape(body) == []


def test_retry_completes_in_temp_workspace(
    bridge_server: LocalBridgeServer, tmp_path: Path
) -> None:
    status, body = _post(f"{bridge_server.url}/actions", _retry_request())
    assert status == 202
    final = _await_status(bridge_server, body["actionRequestId"])
    assert final["status"] == "completed"
    assert final["result"]["performed"] is True
    assert final["result"]["previousStatus"] == "failed"
    assert final["result"]["newStatus"] == "running"
    # The bounded mutation actually happened in the temp workspace state.db.
    with StateStore.open(tmp_path / "state.db") as store:
        run = store.get_run(_ELIGIBLE_RUN)
        assert run is not None and run.status == "running"


def test_retry_of_ineligible_run_fails_honestly(
    bridge_server: LocalBridgeServer,
) -> None:
    payload = _retry_request()
    payload["target"] = {"runId": "01NONEXISTENTRUN0000000000", "stageId": "x"}
    payload["idempotencyKey"] = "idem-missing-run"
    status, body = _post(f"{bridge_server.url}/actions", payload)
    assert status == 202  # accepted asynchronously
    final = _await_status(bridge_server, body["actionRequestId"])
    assert final["status"] == "failed"
    assert final["result"]["performed"] is False
    assert final["result"]["code"] == "run_not_found"


def test_duplicate_idempotency_key_over_http_does_not_duplicate(
    bridge_server: LocalBridgeServer, tmp_path: Path
) -> None:
    first_status, first = _post(f"{bridge_server.url}/actions", _retry_request())
    assert first_status == 202
    _await_status(bridge_server, first["actionRequestId"])
    # Re-submit the same idempotency key.
    second_status, second = _post(f"{bridge_server.url}/actions", _retry_request())
    assert second_status == 202
    assert second["actionRequestId"] == first["actionRequestId"]
    assert any("duplicate" in w.lower() for w in second["warnings"])


# ── other allowlisted actions are validation-only / not-implemented ─────────


def test_inspect_trust_envelope_is_validation_only(
    bridge_server: LocalBridgeServer,
) -> None:
    payload = _retry_request()
    payload["action"] = "inspect_trust_envelope"
    payload["executionTiming"] = "sync-validation-only"
    payload["target"] = {"runId": _ELIGIBLE_RUN}
    payload.pop("idempotencyKey", None)
    status, body = _post(f"{bridge_server.url}/actions", payload)
    assert status == 200
    assert body["status"] == "validated"


def test_refresh_export_is_not_implemented(bridge_server: LocalBridgeServer) -> None:
    payload = _retry_request()
    payload["action"] = "refresh_export"
    payload["target"] = {"exportPath": "exports/storytime-demo-export.json"}
    payload.pop("idempotencyKey", None)
    status, body = _post(f"{bridge_server.url}/actions", payload)
    assert status == 200
    assert body["status"] == "not_implemented"
    assert str(body["status"]).lower() not in {"completed", "succeeded", "success"}
