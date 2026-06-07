"""Phase 13F validation for the Local-mode contract example fixtures.

Phase 13F — Local Bridge Architecture & Contract Baseline — ships a small set
of **documentation example fixtures** under ``docs/examples/`` describing the
*future* Local-mode action request / response / audit DTOs. They are NOT
runtime artifacts: no runtime code imports them, nothing generates them, and
they must never claim Phase 13F executed anything.

This test validates that those fixtures are well-formed and obey the contract
written in ``docs/local-action-dto-spec.md`` and ``docs/local-action-audit-spec.md``.
It uses **plain Python only** — no JSON-schema dependency — consistent with the
Phase 13F "no new dependency" rule.

What this guards against:

- malformed example JSON,
- request examples naming a non-allowlisted or explicitly-deferred action,
- request examples missing the workspace / storage-target objects,
- retry / rerun request examples missing the idempotency key,
- response examples that equate "accepted" with "succeeded",
- async accepted response examples missing an ``actionRequestId`` / ``jobId``,
- audit examples missing the request id or (for retry) the idempotency key,
- any example leaking a credential, shell command, arbitrary SQL, or an
  absolute private user path.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]
_EXAMPLES_ROOT = _REPO_ROOT / "docs" / "examples"
_REQUESTS_DIR = _EXAMPLES_ROOT / "local-action-requests"
_RESPONSES_DIR = _EXAMPLES_ROOT / "local-action-responses"
_AUDIT_DIR = _EXAMPLES_ROOT / "local-action-audit-records"

# The allowlisted initial actions (docs/local-action-dto-spec.md §3).
_ALLOWLISTED_ACTIONS: frozenset[str] = frozenset(
    {"retry_failed_stage", "inspect_trust_envelope", "refresh_export"}
)

# Actions explicitly kept deferred / off the initial allowlist (§3.1). A
# request example must never name one of these.
_DEFERRED_ACTIONS: frozenset[str] = frozenset(
    {
        "record_review_decision",
        "regenerate_operator_report",
        "publish_episode",
        "delete_artifact",
        "provider_sync",
        "sync_provider",
    }
)

# Actions for which an idempotency key is mandatory in a request example.
_IDEMPOTENCY_REQUIRED_ACTIONS: frozenset[str] = frozenset(
    {"retry_failed_stage", "rerun_failed_stage"}
)

# Required top-level fields per file type.
_REQUEST_REQUIRED_FIELDS: tuple[str, ...] = (
    "schemaVersion",
    "requestId",
    "mode",
    "action",
    "target",
    "workspace",
    "storageTarget",
    "dryRun",
    "requiresConfirmation",
    "requestedAt",
    "operatorIntent",
    "preconditions",
    "evidenceRefs",
    "executionTiming",
)
_RESPONSE_REQUIRED_FIELDS: tuple[str, ...] = (
    "schemaVersion",
    "requestId",
    "accepted",
    "status",
    "result",
    "errors",
    "warnings",
    "exportRefreshRequired",
)
_AUDIT_REQUIRED_FIELDS: tuple[str, ...] = (
    "schemaVersion",
    "auditId",
    "requestId",
    "action",
    "target",
    "workspace",
    "storageTarget",
    "preconditionsEvaluated",
    "decision",
    "result",
    "createdAt",
    "completedAt",
    "evidenceRefs",
    "notes",
)

# Status values that would falsely equate acceptance with success.
_SUCCESS_STATUSES: frozenset[str] = frozenset({"succeeded", "completed", "success"})

# Substrings that must never appear in an example fixture (case-insensitive).
# These catch credentials, shell commands, arbitrary SQL, and absolute
# private user paths. The example fixtures use only workspace-relative /
# demo-safe references, so none of these should appear.
_FORBIDDEN_SUBSTRINGS: tuple[str, ...] = (
    # credentials / secrets
    "password",
    "secret",
    "apikey",
    "api_key",
    "access_key",
    "accesskey",
    "access-token",
    "accesstoken",
    "bearer ",
    "credential",
    "private_key",
    "privatekey",
    "client_secret",
    "aws_secret",
    # the bare word "token" as a value-ish token (guarded with word edges below)
    # shell / command execution
    "subprocess",
    "/bin/sh",
    "/bin/bash",
    "sh -c",
    "bash -c",
    "rm -rf",
    "&&",
    "$(",
    "`",
    # arbitrary SQL
    "select * from",
    "insert into",
    "delete from",
    "drop table",
    "update set",
    "; --",
    # absolute private user paths
    "/home/",
    "/users/",
    "/root/",
    "c:\\",
    "/mnt/",
    "/private/var/",
)


def _all_example_files() -> list[Path]:
    files: list[Path] = []
    for d in (_REQUESTS_DIR, _RESPONSES_DIR, _AUDIT_DIR):
        files.extend(sorted(d.glob("*.json")))
    return files


def _load(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, dict), f"{path.name} is not a JSON object"
    return data


# ── existence / well-formedness ──────────────────────────────────────────


def test_example_directories_exist() -> None:
    """The three example directories exist."""
    assert _REQUESTS_DIR.is_dir(), "missing local-action-requests dir"
    assert _RESPONSES_DIR.is_dir(), "missing local-action-responses dir"
    assert _AUDIT_DIR.is_dir(), "missing local-action-audit-records dir"


def test_at_least_the_required_examples_exist() -> None:
    """The required example fixtures named by the Phase 13F prompt are present."""
    required = [
        _REQUESTS_DIR / "retry-failed-stage.request.example.json",
        _REQUESTS_DIR / "inspect-trust-envelope.request.example.json",
        _REQUESTS_DIR / "refresh-export.request.example.json",
        _RESPONSES_DIR / "retry-failed-stage.accepted.example.json",
        _RESPONSES_DIR / "refresh-export.accepted.example.json",
        _AUDIT_DIR / "retry-failed-stage.audit.example.json",
    ]
    missing = [p.name for p in required if not p.is_file()]
    assert not missing, f"missing required example fixtures: {missing}"


@pytest.mark.parametrize(
    "path", _all_example_files(), ids=lambda p: p.name
)
def test_example_is_valid_json(path: Path) -> None:
    """Every example file is syntactically valid JSON object."""
    data = _load(path)
    assert data, f"{path.name} deserialized to an empty object"


# ── required fields by type ──────────────────────────────────────────────


@pytest.mark.parametrize(
    "path", sorted(_REQUESTS_DIR.glob("*.json")), ids=lambda p: p.name
)
def test_request_has_required_fields(path: Path) -> None:
    data = _load(path)
    missing = [f for f in _REQUEST_REQUIRED_FIELDS if f not in data]
    assert not missing, f"{path.name} missing request fields: {missing}"


@pytest.mark.parametrize(
    "path", sorted(_RESPONSES_DIR.glob("*.json")), ids=lambda p: p.name
)
def test_response_has_required_fields(path: Path) -> None:
    data = _load(path)
    missing = [f for f in _RESPONSE_REQUIRED_FIELDS if f not in data]
    assert not missing, f"{path.name} missing response fields: {missing}"


@pytest.mark.parametrize(
    "path", sorted(_AUDIT_DIR.glob("*.json")), ids=lambda p: p.name
)
def test_audit_has_required_fields(path: Path) -> None:
    data = _load(path)
    missing = [f for f in _AUDIT_REQUIRED_FIELDS if f not in data]
    assert not missing, f"{path.name} missing audit fields: {missing}"


# ── request semantics ────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "path", sorted(_REQUESTS_DIR.glob("*.json")), ids=lambda p: p.name
)
def test_request_uses_allowlisted_action(path: Path) -> None:
    data = _load(path)
    action = data.get("action")
    assert action in _ALLOWLISTED_ACTIONS, (
        f"{path.name} uses non-allowlisted action {action!r}; "
        f"allowed: {sorted(_ALLOWLISTED_ACTIONS)}"
    )


@pytest.mark.parametrize(
    "path", sorted(_REQUESTS_DIR.glob("*.json")), ids=lambda p: p.name
)
def test_request_does_not_use_deferred_action(path: Path) -> None:
    data = _load(path)
    action = data.get("action")
    assert action not in _DEFERRED_ACTIONS, (
        f"{path.name} uses an explicitly-deferred action {action!r}"
    )


@pytest.mark.parametrize(
    "path", sorted(_REQUESTS_DIR.glob("*.json")), ids=lambda p: p.name
)
def test_request_has_workspace_and_storage_target_objects(path: Path) -> None:
    data = _load(path)
    workspace = data.get("workspace")
    storage = data.get("storageTarget")
    assert isinstance(workspace, dict), f"{path.name} workspace is not an object"
    assert "id" in workspace and "root" in workspace, (
        f"{path.name} workspace missing id/root"
    )
    assert isinstance(storage, dict), f"{path.name} storageTarget is not an object"
    assert "type" in storage, f"{path.name} storageTarget missing type"


@pytest.mark.parametrize(
    "path", sorted(_REQUESTS_DIR.glob("*.json")), ids=lambda p: p.name
)
def test_retry_request_has_idempotency_key(path: Path) -> None:
    data = _load(path)
    action = data.get("action")
    if action in _IDEMPOTENCY_REQUIRED_ACTIONS:
        key = data.get("idempotencyKey")
        assert isinstance(key, str) and key.strip(), (
            f"{path.name} action {action!r} requires a non-empty idempotencyKey"
        )


# ── response semantics ───────────────────────────────────────────────────


@pytest.mark.parametrize(
    "path", sorted(_RESPONSES_DIR.glob("*.json")), ids=lambda p: p.name
)
def test_response_does_not_equate_accepted_with_succeeded(path: Path) -> None:
    data = _load(path)
    status = str(data.get("status", "")).lower()
    assert status not in _SUCCESS_STATUSES, (
        f"{path.name} status {status!r} equates acceptance with success; "
        f"acceptance is not success"
    )


@pytest.mark.parametrize(
    "path", sorted(_RESPONSES_DIR.glob("*.json")), ids=lambda p: p.name
)
def test_async_accepted_response_has_request_or_job_id(path: Path) -> None:
    data = _load(path)
    # An accepted (async) response must carry a handle the frontend can use to
    # learn status later.
    if data.get("accepted") is True and str(data.get("status", "")).lower() == (
        "accepted"
    ):
        has_handle = bool(data.get("actionRequestId")) or bool(data.get("jobId"))
        assert has_handle, (
            f"{path.name} is accepted/async but has no actionRequestId or jobId"
        )


# ── audit semantics ──────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "path", sorted(_AUDIT_DIR.glob("*.json")), ids=lambda p: p.name
)
def test_audit_has_request_id(path: Path) -> None:
    data = _load(path)
    rid = data.get("requestId")
    assert isinstance(rid, str) and rid.strip(), (
        f"{path.name} audit record missing requestId"
    )


@pytest.mark.parametrize(
    "path", sorted(_AUDIT_DIR.glob("*.json")), ids=lambda p: p.name
)
def test_retry_audit_has_idempotency_key(path: Path) -> None:
    data = _load(path)
    if data.get("action") in _IDEMPOTENCY_REQUIRED_ACTIONS:
        key = data.get("idempotencyKey")
        assert isinstance(key, str) and key.strip(), (
            f"{path.name} retry audit record requires a non-empty idempotencyKey"
        )


@pytest.mark.parametrize(
    "path", sorted(_AUDIT_DIR.glob("*.json")), ids=lambda p: p.name
)
def test_audit_acceptance_is_not_success(path: Path) -> None:
    """An audit record with decision 'accepted' and result null is pending,
    not succeeded — guard against a fixture that marks a merely-accepted
    action as completed."""
    data = _load(path)
    if str(data.get("decision", "")).lower() == "accepted" and data.get(
        "result"
    ) is None:
        assert data.get("completedAt") is None, (
            f"{path.name} has decision 'accepted' + result null but a non-null "
            f"completedAt; acceptance is not success"
        )


# ── safety: no secrets / shell / SQL / private paths ─────────────────────


@pytest.mark.parametrize(
    "path", _all_example_files(), ids=lambda p: p.name
)
def test_example_has_no_forbidden_content(path: Path) -> None:
    raw = path.read_text(encoding="utf-8").lower()
    hits = [s for s in _FORBIDDEN_SUBSTRINGS if s in raw]
    assert not hits, (
        f"{path.name} contains forbidden content (credential / shell / SQL / "
        f"private path): {hits}"
    )


@pytest.mark.parametrize(
    "path", _all_example_files(), ids=lambda p: p.name
)
def test_example_has_no_bare_token_field(path: Path) -> None:
    """Guard the bare word 'token' as a key/value, while allowing benign
    compound identifiers. The example fixtures should carry no token at all."""
    data = _load(path)
    flat = json.dumps(data).lower()
    # Allow nothing token-ish: the fixtures simply do not use tokens.
    assert '"token"' not in flat and "token=" not in flat, (
        f"{path.name} appears to contain a token field"
    )
