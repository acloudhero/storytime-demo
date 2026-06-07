"""Phase 13G — local-bridge DTO validation & fixture-synchronization tests.

These tests are the hard gate the Phase 13G prompt requires: the runtime Python
DTO validators in ``storytime.local_bridge.dto`` must stay synchronized with the
Phase 13F documentation example fixtures under ``docs/examples/``. Every request
/ response / audit fixture is loaded and pushed through the runtime validators,
and the dynamically-generated bridge responses are checked against the same
response contract — so the runtime code and the locked Phase 13F contract cannot
silently drift apart.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from storytime.local_bridge.dto import (
    ALLOWLISTED_ACTIONS,
    SCHEMA_VERSION,
    ValidationError,
    validate_audit_shape,
    validate_request,
    validate_response_shape,
)
from storytime.local_bridge.responses import (
    build_accepted_response,
    build_rejected_response,
    build_validated_response,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_EXAMPLES = _REPO_ROOT / "docs" / "examples"
_REQUESTS = sorted((_EXAMPLES / "local-action-requests").glob("*.json"))
_RESPONSES = sorted((_EXAMPLES / "local-action-responses").glob("*.json"))
_AUDITS = sorted((_EXAMPLES / "local-action-audit-records").glob("*.json"))


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


# ── fixture synchronization: requests ────────────────────────────────────


def test_request_fixtures_exist() -> None:
    assert _REQUESTS, "no Phase 13F request fixtures found"


@pytest.mark.parametrize("path", _REQUESTS, ids=lambda p: p.name)
def test_request_fixture_validates(path: Path) -> None:
    """Every Phase 13F request fixture passes the runtime request validator."""
    request, errors = validate_request(_load(path))
    assert request is not None, f"{path.name} failed runtime validation: {errors}"
    assert request.action in ALLOWLISTED_ACTIONS
    assert request.schema_version == SCHEMA_VERSION


@pytest.mark.parametrize("path", _RESPONSES, ids=lambda p: p.name)
def test_response_fixture_validates(path: Path) -> None:
    """Every Phase 13F response fixture passes the runtime response validator."""
    errors = validate_response_shape(_load(path))
    assert errors == [], f"{path.name} failed response validation: {errors}"


@pytest.mark.parametrize("path", _AUDITS, ids=lambda p: p.name)
def test_audit_fixture_validates(path: Path) -> None:
    """Every Phase 13F audit fixture passes the runtime audit validator."""
    errors = validate_audit_shape(_load(path))
    assert errors == [], f"{path.name} failed audit validation: {errors}"


# ── acceptance semantics ─────────────────────────────────────────────────


@pytest.mark.parametrize("path", _RESPONSES, ids=lambda p: p.name)
def test_accepted_response_has_handle_and_is_not_success(path: Path) -> None:
    data = _load(path)
    if data.get("accepted") is True and str(data.get("status")) == "accepted":
        assert data.get("actionRequestId") or data.get("jobId"), (
            f"{path.name} accepted async response missing handle"
        )
        assert str(data.get("status")).lower() not in {
            "completed",
            "succeeded",
            "success",
        }


def test_retry_request_requires_idempotency_key() -> None:
    base = _load(_EXAMPLES / "local-action-requests" / "retry-failed-stage.request.example.json")
    base.pop("idempotencyKey", None)
    request, errors = validate_request(base)
    assert request is None
    assert any(e.code == "missing_idempotency_key" for e in errors)


# ── rejection semantics ──────────────────────────────────────────────────


def _valid_retry() -> dict[str, object]:
    return _load(
        _EXAMPLES / "local-action-requests" / "retry-failed-stage.request.example.json"
    )


def test_unknown_action_is_rejected() -> None:
    payload = _valid_retry()
    payload["action"] = "definitely_not_a_real_action"
    request, errors = validate_request(payload)
    assert request is None
    assert any(e.code == "unknown_action" for e in errors)


def test_deferred_action_is_rejected() -> None:
    payload = _valid_retry()
    payload["action"] = "publish_episode"
    request, errors = validate_request(payload)
    assert request is None
    assert any(e.code == "deferred_action" for e in errors)


def test_missing_required_field_is_rejected() -> None:
    payload = _valid_retry()
    del payload["workspace"]
    request, errors = validate_request(payload)
    assert request is None
    assert any(e.code == "missing_field" and e.field == "workspace" for e in errors)


def test_schema_version_mismatch_is_rejected() -> None:
    payload = _valid_retry()
    payload["schemaVersion"] = "9.9"
    request, errors = validate_request(payload)
    assert request is None
    assert any(e.code == "schema_version_mismatch" for e in errors)


@pytest.mark.parametrize(
    "mutation",
    [
        {"command": "rm -rf /"},
        {"shell": "/bin/sh"},
        {"subprocess": True},
        {"sql": "select * from runs"},
    ],
)
def test_smuggled_command_or_sql_field_is_rejected(mutation: dict[str, object]) -> None:
    payload = _valid_retry()
    payload.update(mutation)
    request, errors = validate_request(payload)
    assert request is None
    assert any(e.code in {"unsafe_field", "unsafe_value"} for e in errors)


def test_injection_value_is_rejected() -> None:
    payload = _valid_retry()
    payload["operatorIntent"] = "do the thing && rm -rf /tmp/x"
    request, errors = validate_request(payload)
    assert request is None
    assert any(e.code == "unsafe_value" for e in errors)


@pytest.mark.parametrize(
    "bad_root",
    ["/home/victim/.ssh", "../../etc/passwd", "/etc/shadow", "C:\\Windows"],
)
def test_unsafe_workspace_path_is_rejected(bad_root: str) -> None:
    payload = _valid_retry()
    workspace = dict(payload["workspace"])  # type: ignore[arg-type]
    workspace["root"] = bad_root
    payload["workspace"] = workspace
    request, errors = validate_request(payload)
    assert request is None
    assert any(e.code == "unsafe_path" for e in errors)


# ── dynamic response-shape validation ────────────────────────────────────


def test_dynamic_accepted_response_matches_contract() -> None:
    resp = build_accepted_response(
        "req-x",
        action_request_id="act-x",
        job_id="job-x",
        export_refresh_required=True,
        warnings=["acceptance is not success"],
    )
    assert validate_response_shape(resp) == []
    assert resp["accepted"] is True
    assert resp["status"] == "accepted"
    assert resp["result"] is None


def test_dynamic_rejected_response_has_structured_errors() -> None:
    resp = build_rejected_response(
        "req-x",
        [ValidationError(code="unknown_action", message="nope", field="action")],
    )
    assert validate_response_shape(resp) == []
    assert resp["accepted"] is False
    assert resp["status"] == "rejected"
    assert isinstance(resp["errors"], list) and resp["errors"]
    first = resp["errors"][0]
    assert first["code"] == "unknown_action" and first["field"] == "action"


def test_dynamic_validation_only_response_is_not_success() -> None:
    resp = build_validated_response("req-x", not_implemented=True)
    assert validate_response_shape(resp) == []
    assert resp["status"] == "not_implemented"
    assert str(resp["status"]).lower() not in {"completed", "succeeded", "success"}


# ── fixtures carry no forbidden content (re-asserted at runtime layer) ────


@pytest.mark.parametrize("path", _REQUESTS + _RESPONSES + _AUDITS, ids=lambda p: p.name)
def test_fixture_has_no_secret_or_command_content(path: Path) -> None:
    raw = path.read_text(encoding="utf-8").lower()
    for needle in ("password", "secret", "api_key", "subprocess", "/bin/sh", "drop table"):
        assert needle not in raw, f"{path.name} leaks forbidden content: {needle!r}"
