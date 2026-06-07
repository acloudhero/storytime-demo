"""Local-bridge response / audit-record builders (Phase 13G — runtime).

Every response the bridge emits is built here from explicit fields — the
dataclasses are never serialized wholesale — so no internal field can leak into
a response by accident, and every response conforms to the Phase 13F response
contract (``docs/local-action-dto-spec.md`` §2). The builders enforce the
"acceptance is not success" rule structurally: an accepted async response
carries an ``actionRequestId`` / ``jobId`` and ``status: "accepted"`` with a
null ``result`` — never a success status.
"""

from __future__ import annotations

from typing import Any

from storytime.local_bridge.dto import SCHEMA_VERSION, ValidationError


def build_accepted_response(
    request_id: str,
    *,
    action_request_id: str,
    job_id: str,
    export_refresh_required: bool,
    warnings: list[str] | None = None,
    audit_record_ref: str | None = None,
) -> dict[str, Any]:
    """Build a ``202 Accepted`` async response. Acceptance is not success."""
    return {
        "schemaVersion": SCHEMA_VERSION,
        "requestId": request_id,
        "accepted": True,
        "status": "accepted",
        "result": None,
        "errors": [],
        "warnings": list(warnings or []),
        "exportRefreshRequired": export_refresh_required,
        "auditRecordRef": audit_record_ref,
        "actionRequestId": action_request_id,
        "jobId": job_id,
    }


def build_validated_response(
    request_id: str,
    *,
    warnings: list[str] | None = None,
    not_implemented: bool = False,
) -> dict[str, Any]:
    """Build a synchronous validation-only response (read-only / not-implemented).

    ``status`` is ``"validated"`` (a fast-path validation result) or
    ``"not_implemented"`` for an allowlisted action with no execution behaviour
    in this phase. Neither equates to success.
    """
    return {
        "schemaVersion": SCHEMA_VERSION,
        "requestId": request_id,
        "accepted": True,
        "status": "not_implemented" if not_implemented else "validated",
        "result": None,
        "errors": [],
        "warnings": list(warnings or []),
        "exportRefreshRequired": False,
        "auditRecordRef": None,
        "actionRequestId": None,
        "jobId": None,
    }


def build_rejected_response(
    request_id: str | None,
    errors: list[ValidationError],
    *,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    """Build a rejection response carrying the structured ``errors`` array."""
    return {
        "schemaVersion": SCHEMA_VERSION,
        "requestId": request_id if request_id is not None else "unknown",
        "accepted": False,
        "status": "rejected",
        "result": None,
        "errors": [e.to_dict() for e in errors],
        "warnings": list(warnings or []),
        "exportRefreshRequired": False,
        "auditRecordRef": None,
        "actionRequestId": None,
        "jobId": None,
    }


def build_deduplicated_response(
    request_id: str,
    *,
    action_request_id: str,
    job_id: str,
    export_refresh_required: bool,
) -> dict[str, Any]:
    """Build the response for a duplicate idempotency key.

    Returns the original action's accepted handle rather than enqueuing a new
    execution (``docs/action-execution-boundary.md`` §8). Acceptance — and a
    deduplicated re-acceptance — is still not success.
    """
    return {
        "schemaVersion": SCHEMA_VERSION,
        "requestId": request_id,
        "accepted": True,
        "status": "accepted",
        "result": None,
        "errors": [],
        "warnings": [
            "Duplicate idempotencyKey: returning the original action handle; "
            "no new execution was enqueued."
        ],
        "exportRefreshRequired": export_refresh_required,
        "auditRecordRef": None,
        "actionRequestId": action_request_id,
        "jobId": job_id,
    }


def build_audit_record(
    *,
    audit_id: str,
    request_id: str,
    action: str,
    target: dict[str, Any],
    workspace: dict[str, Any],
    storage_target: dict[str, Any],
    preconditions_evaluated: list[Any],
    decision: str,
    result: str | None,
    created_at: str,
    completed_at: str | None,
    evidence_refs: list[Any],
    idempotency_key: str | None = None,
    notes: str = "",
) -> dict[str, Any]:
    """Build a durable audit record conforming to the Phase 13F audit contract."""
    record: dict[str, Any] = {
        "schemaVersion": SCHEMA_VERSION,
        "auditId": audit_id,
        "requestId": request_id,
        "action": action,
        "target": dict(target),
        "workspace": dict(workspace),
        "storageTarget": dict(storage_target),
        "preconditionsEvaluated": list(preconditions_evaluated),
        "decision": decision,
        "result": result,
        "createdAt": created_at,
        "completedAt": completed_at,
        "evidenceRefs": list(evidence_refs),
        "notes": notes,
    }
    if idempotency_key is not None:
        record["idempotencyKey"] = idempotency_key
    return record
