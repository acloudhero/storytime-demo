"""Local-bridge DTO parsing / validation (Phase 13G — runtime).

Phase 13F shipped the Local-mode action request / response / audit **contracts**
as documentation plus non-runtime JSON example fixtures (``docs/examples/``).
Phase 13G implements the first runtime validators for those contracts, using
**plain Python dataclasses and dictionaries only** — no Pydantic, no
jsonschema (the Phase 13F "no new dependency" rule still holds).

The validators here are deliberately strict and fail closed:

- a request must carry every required field (``docs/local-action-dto-spec.md`` §1),
- ``schemaVersion`` must match the supported contract version,
- ``action`` must be on the initial allowlist; deferred / unknown actions are
  rejected before any dispatch (``docs/action-execution-boundary.md`` §4-5),
- ``retry_failed_stage`` must carry a non-empty ``idempotencyKey``,
- there is **never** a free-form shell / command / SQL field — such a field is
  an immediate rejection (``docs/local-bridge-architecture.md`` §8),
- path-bearing fields must be workspace-relative; absolute private paths and
  ``..`` traversal are rejected.

The same validators back the fixture-synchronization tests, so the runtime
contract and the Phase 13F documentation fixtures cannot silently drift apart.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# The single supported contract version. A mismatch is rejected (never coerced).
SCHEMA_VERSION = "1.0"

# The initial allowlist (docs/local-action-dto-spec.md §3). Only these three
# action names are accepted; everything else is rejected before dispatch.
ALLOWLISTED_ACTIONS: frozenset[str] = frozenset(
    {"retry_failed_stage", "inspect_trust_envelope", "refresh_export"}
)

# Actions explicitly kept off the initial allowlist (§3.1). Naming one of these
# is rejected with a clear, specific error rather than a generic "unknown".
DEFERRED_ACTIONS: frozenset[str] = frozenset(
    {
        "record_review_decision",
        "regenerate_operator_report",
        "publish_episode",
        "delete_artifact",
        "provider_sync",
        "sync_provider",
    }
)

# Actions for which an idempotency key is mandatory.
IDEMPOTENCY_REQUIRED_ACTIONS: frozenset[str] = frozenset(
    {"retry_failed_stage", "rerun_failed_stage"}
)

# The only two execution-timing values the contract defines.
EXECUTION_TIMINGS: frozenset[str] = frozenset(
    {"sync-validation-only", "async-long-running"}
)

# Required top-level request fields (docs/local-action-dto-spec.md §1.1).
REQUEST_REQUIRED_FIELDS: tuple[str, ...] = (
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

# Required top-level response fields (docs/local-action-dto-spec.md §2.1).
RESPONSE_REQUIRED_FIELDS: tuple[str, ...] = (
    "schemaVersion",
    "requestId",
    "accepted",
    "status",
    "result",
    "errors",
    "warnings",
    "exportRefreshRequired",
)

# Required audit-record fields (docs/local-action-audit-spec.md §1).
AUDIT_REQUIRED_FIELDS: tuple[str, ...] = (
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

# Response / audit status values that would falsely equate acceptance with
# success. A merely-accepted async action must never carry one of these.
SUCCESS_STATUSES: frozenset[str] = frozenset({"succeeded", "completed", "success"})

# Object keys that, if present anywhere in a request, signal an attempt to smuggle
# a free-form command / script / SQL string. There is no "run this" field, ever
# (docs/local-bridge-architecture.md §8); any of these is an instant rejection.
_FORBIDDEN_KEYS: frozenset[str] = frozenset(
    {
        "command",
        "cmd",
        "commandline",
        "command_line",
        "shell",
        "shellcommand",
        "shell_command",
        "sh",
        "bash",
        "powershell",
        "subprocess",
        "exec",
        "execute",
        "eval",
        "script",
        "sql",
        "query",
        "rawsql",
        "raw_sql",
        "statement",
    }
)

# High-signal injection substrings scanned for inside string values. These do
# not appear in the legitimate, demo-safe example fixtures (whose free text is
# ordinary operator prose), so scanning every string value is safe.
_FORBIDDEN_VALUE_SUBSTRINGS: tuple[str, ...] = (
    "/bin/sh",
    "/bin/bash",
    "sh -c",
    "bash -c",
    "rm -rf",
    "&&",
    "$(",
    "`",
    "; --",
    ";--",
    "select * from",
    "insert into",
    "delete from",
    "drop table",
    "update set",
    "truncate table",
)

# Absolute / private path prefixes that must never appear in a path-bearing
# field. The contract is workspace-relative / demo-safe references only
# (docs/local-mode-storage-contract.md §1).
_FORBIDDEN_PATH_PREFIXES: tuple[str, ...] = (
    "/",
    "~",
    "/home/",
    "/users/",
    "/root/",
    "/etc/",
    "/var/",
    "/mnt/",
    "/private/",
    "c:\\",
    "c:/",
    "\\\\",
)

# Fields whose string values are treated as filesystem paths and held to the
# workspace-relative / no-traversal rule.
_PATH_BEARING_FIELDS: frozenset[str] = frozenset({"root", "exportpath", "path"})


@dataclass(frozen=True, slots=True)
class ValidationError:
    """A structured, machine-readable validation error.

    ``code`` is a stable identifier the frontend / tests can switch on;
    ``message`` is a short, safe, human-readable summary; ``field`` names the
    offending field where one applies. These map directly into the response
    DTO's ``errors`` array.
    """

    code: str
    message: str
    field: str | None = None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.field is not None:
            out["field"] = self.field
        return out


@dataclass(frozen=True, slots=True)
class ValidatedRequest:
    """A request that passed structural + semantic validation.

    Only the fields the bridge actually uses are surfaced as typed attributes;
    the untouched original payload is retained in ``raw`` for audit echoing.
    """

    schema_version: str
    request_id: str
    mode: str
    action: str
    target: dict[str, Any]
    workspace: dict[str, Any]
    storage_target: dict[str, Any]
    dry_run: bool
    requires_confirmation: bool
    requested_at: str
    operator_intent: str
    preconditions: list[Any]
    evidence_refs: list[Any]
    execution_timing: str
    idempotency_key: str | None
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def is_async(self) -> bool:
        return self.execution_timing == "async-long-running"


def _iter_keys(value: Any) -> list[str]:
    """Return every object key appearing anywhere in *value* (recursively)."""
    keys: list[str] = []
    if isinstance(value, dict):
        for k, v in value.items():
            keys.append(str(k))
            keys.extend(_iter_keys(v))
    elif isinstance(value, list):
        for item in value:
            keys.extend(_iter_keys(item))
    return keys


def _iter_strings(value: Any) -> list[str]:
    """Return every string value appearing anywhere in *value* (recursively)."""
    strings: list[str] = []
    if isinstance(value, str):
        strings.append(value)
    elif isinstance(value, dict):
        for v in value.values():
            strings.extend(_iter_strings(v))
    elif isinstance(value, list):
        for item in value:
            strings.extend(_iter_strings(item))
    return strings


def _path_is_unsafe(raw_path: str) -> bool:
    """True if *raw_path* is absolute, private, or uses ``..`` traversal."""
    candidate = raw_path.strip().lower()
    if not candidate:
        return False
    if ".." in candidate:
        return True
    return any(candidate.startswith(prefix) for prefix in _FORBIDDEN_PATH_PREFIXES)


def _scan_unsafe(payload: dict[str, Any]) -> list[ValidationError]:
    """Reject smuggled command / SQL fields, injection values, and unsafe paths."""
    errors: list[ValidationError] = []

    for key in _iter_keys(payload):
        if key.strip().lower() in _FORBIDDEN_KEYS:
            errors.append(
                ValidationError(
                    code="unsafe_field",
                    message=(
                        "Request contains a forbidden free-form command / SQL "
                        "field; the bridge accepts only allowlisted actions."
                    ),
                    field=key,
                )
            )

    for text in _iter_strings(payload):
        lowered = text.lower()
        for needle in _FORBIDDEN_VALUE_SUBSTRINGS:
            if needle in lowered:
                errors.append(
                    ValidationError(
                        code="unsafe_value",
                        message=(
                            "Request value contains a forbidden shell / SQL "
                            "fragment; arbitrary commands are never executed."
                        ),
                    )
                )
                break

    # Path-bearing fields must be workspace-relative.
    def _check_paths(value: Any) -> None:
        if isinstance(value, dict):
            for k, v in value.items():
                if (
                    str(k).strip().lower() in _PATH_BEARING_FIELDS
                    and isinstance(v, str)
                    and _path_is_unsafe(v)
                ):
                    errors.append(
                        ValidationError(
                            code="unsafe_path",
                            message=(
                                "Path-bearing field must be workspace-relative; "
                                "absolute, private, or traversal paths are rejected."
                            ),
                            field=str(k),
                        )
                    )
                _check_paths(v)
        elif isinstance(value, list):
            for item in value:
                _check_paths(item)

    _check_paths(payload)
    return errors


def validate_request(payload: Any) -> tuple[ValidatedRequest | None, list[ValidationError]]:
    """Validate a candidate request payload against the Phase 13F contract.

    Returns ``(request, [])`` when valid, or ``(None, errors)`` with a
    non-empty, structured error list otherwise. Never raises on bad input —
    the bridge fails closed by returning a rejection, not by crashing.
    """
    errors: list[ValidationError] = []

    if not isinstance(payload, dict):
        return None, [
            ValidationError(
                code="malformed_request",
                message="Request body must be a JSON object.",
            )
        ]

    # Reject smuggled command / SQL / unsafe-path content first.
    errors.extend(_scan_unsafe(payload))

    # Required top-level fields.
    for required in REQUEST_REQUIRED_FIELDS:
        if required not in payload:
            errors.append(
                ValidationError(
                    code="missing_field",
                    message=f"Required field {required!r} is missing.",
                    field=required,
                )
            )

    # schemaVersion must match.
    schema_version = payload.get("schemaVersion")
    if schema_version is not None and schema_version != SCHEMA_VERSION:
        errors.append(
            ValidationError(
                code="schema_version_mismatch",
                message=(
                    f"Unsupported schemaVersion {schema_version!r}; "
                    f"expected {SCHEMA_VERSION!r}."
                ),
                field="schemaVersion",
            )
        )

    # action must be allowlisted; deferred actions get a specific error.
    action = payload.get("action")
    if action is not None:
        if action in DEFERRED_ACTIONS:
            errors.append(
                ValidationError(
                    code="deferred_action",
                    message=(
                        f"Action {action!r} is explicitly deferred and not on "
                        "the initial allowlist."
                    ),
                    field="action",
                )
            )
        elif action not in ALLOWLISTED_ACTIONS:
            errors.append(
                ValidationError(
                    code="unknown_action",
                    message=(
                        f"Action {action!r} is not allowlisted; allowed: "
                        f"{sorted(ALLOWLISTED_ACTIONS)}."
                    ),
                    field="action",
                )
            )

    # workspace / storageTarget sub-objects.
    workspace = payload.get("workspace")
    if workspace is not None:
        if not isinstance(workspace, dict):
            errors.append(
                ValidationError(
                    code="invalid_field",
                    message="workspace must be an object.",
                    field="workspace",
                )
            )
        else:
            for sub in ("id", "root"):
                if sub not in workspace:
                    errors.append(
                        ValidationError(
                            code="missing_field",
                            message=f"workspace.{sub} is required.",
                            field=f"workspace.{sub}",
                        )
                    )

    storage_target = payload.get("storageTarget")
    if storage_target is not None:
        if not isinstance(storage_target, dict):
            errors.append(
                ValidationError(
                    code="invalid_field",
                    message="storageTarget must be an object.",
                    field="storageTarget",
                )
            )
        elif "type" not in storage_target:
            errors.append(
                ValidationError(
                    code="missing_field",
                    message="storageTarget.type is required.",
                    field="storageTarget.type",
                )
            )

    target = payload.get("target")
    if target is not None and not isinstance(target, dict):
        errors.append(
            ValidationError(
                code="invalid_field",
                message="target must be an object.",
                field="target",
            )
        )

    # executionTiming must be one of the two contract values.
    execution_timing = payload.get("executionTiming")
    if execution_timing is not None and execution_timing not in EXECUTION_TIMINGS:
        errors.append(
            ValidationError(
                code="invalid_field",
                message=(
                    f"executionTiming {execution_timing!r} must be one of "
                    f"{sorted(EXECUTION_TIMINGS)}."
                ),
                field="executionTiming",
            )
        )

    # idempotencyKey required for retry / rerun.
    idempotency_key = payload.get("idempotencyKey")
    if action in IDEMPOTENCY_REQUIRED_ACTIONS and not (
        isinstance(idempotency_key, str) and idempotency_key.strip()
    ):
        errors.append(
            ValidationError(
                code="missing_idempotency_key",
                message=f"Action {action!r} requires a non-empty idempotencyKey.",
                field="idempotencyKey",
            )
        )

    if errors:
        return None, errors

    # All checks passed — construct the typed request. The presence and types
    # of these fields were just validated above.
    return (
        ValidatedRequest(
            schema_version=str(payload["schemaVersion"]),
            request_id=str(payload["requestId"]),
            mode=str(payload["mode"]),
            action=str(payload["action"]),
            target=dict(payload["target"]),
            workspace=dict(payload["workspace"]),
            storage_target=dict(payload["storageTarget"]),
            dry_run=bool(payload["dryRun"]),
            requires_confirmation=bool(payload["requiresConfirmation"]),
            requested_at=str(payload["requestedAt"]),
            operator_intent=str(payload["operatorIntent"]),
            preconditions=list(payload["preconditions"]),
            evidence_refs=list(payload["evidenceRefs"]),
            execution_timing=str(payload["executionTiming"]),
            idempotency_key=(
                str(idempotency_key)
                if isinstance(idempotency_key, str) and idempotency_key.strip()
                else None
            ),
            raw=dict(payload),
        ),
        [],
    )


def validate_response_shape(payload: Any) -> list[ValidationError]:
    """Validate a response payload against the Phase 13F response contract.

    Used both to check the documentation fixtures and to self-check every
    dynamically generated bridge response before it leaves the server.
    """
    errors: list[ValidationError] = []
    if not isinstance(payload, dict):
        return [
            ValidationError(
                code="malformed_response",
                message="Response must be a JSON object.",
            )
        ]
    for required in RESPONSE_REQUIRED_FIELDS:
        if required not in payload:
            errors.append(
                ValidationError(
                    code="missing_field",
                    message=f"Response field {required!r} is missing.",
                    field=required,
                )
            )
    if not isinstance(payload.get("errors"), list):
        errors.append(
            ValidationError(
                code="invalid_field",
                message="Response 'errors' must be an array.",
                field="errors",
            )
        )
    if not isinstance(payload.get("warnings"), list):
        errors.append(
            ValidationError(
                code="invalid_field",
                message="Response 'warnings' must be an array.",
                field="warnings",
            )
        )
    # Acceptance is not success: an accepted async response must carry a handle
    # and must not claim a success status.
    if (
        payload.get("accepted") is True
        and str(payload.get("status", "")).lower() == "accepted"
        and not (payload.get("actionRequestId") or payload.get("jobId"))
    ):
        errors.append(
            ValidationError(
                code="missing_handle",
                message=(
                    "Accepted async response must carry actionRequestId / jobId."
                ),
            )
        )
    if str(payload.get("status", "")).lower() in SUCCESS_STATUSES and (
        payload.get("accepted") is True and payload.get("result") is None
    ):
        errors.append(
            ValidationError(
                code="acceptance_is_not_success",
                message="A merely-accepted action must not claim a success status.",
                field="status",
            )
        )
    return errors


def validate_audit_shape(payload: Any) -> list[ValidationError]:
    """Validate an audit-record payload against the Phase 13F audit contract."""
    errors: list[ValidationError] = []
    if not isinstance(payload, dict):
        return [
            ValidationError(
                code="malformed_audit",
                message="Audit record must be a JSON object.",
            )
        ]
    for required in AUDIT_REQUIRED_FIELDS:
        if required not in payload:
            errors.append(
                ValidationError(
                    code="missing_field",
                    message=f"Audit field {required!r} is missing.",
                    field=required,
                )
            )
    # decision 'accepted' + result null is pending, not complete.
    if str(payload.get("decision", "")).lower() == "accepted" and (
        payload.get("result") is None and payload.get("completedAt") is not None
    ):
        errors.append(
            ValidationError(
                code="acceptance_is_not_success",
                message=(
                    "Audit 'accepted' with null result must have null completedAt."
                ),
                field="completedAt",
            )
        )
    return errors
