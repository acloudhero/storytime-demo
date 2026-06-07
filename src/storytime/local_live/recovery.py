"""Durable recovery control-plane boundary (Phase 14C.5.1).

The smallest durable, backend-owned recovery control plane that lets a *failed*
local proof execution be safely, durably, and explainably linked to a bounded
*recovery* execution. It is the SOURCE OF TRUTH for recovery lineage (the
``recovery_action`` table); Phase 14C.4 observer events remain explanatory only
and never become the lineage database.

Scope is deliberately local and minimal. There is no cloud retry orchestration,
no distributed worker, no external broker (Redis/NATS/SQS/Temporal/Celery), no
dead-letter queue, no automatic retries, no exponential backoff, and no
scheduler. Eligibility is decided by the backend; the frontend can never decide
it.

The pieces:

- :func:`evaluate_recovery_eligibility` — a small, explicit, testable policy
  that answers whether a failed execution may be recovered.
- :func:`request_recovery` — records durable recovery lineage, enforces
  duplicate-prevention and a bounded attempt limit, and (when eligible) reserves
  and enqueues a new recovery execution linked back to the original.
"""

from __future__ import annotations

import secrets
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from storytime.local_live.proof_run import reserve_proof_run
from storytime.local_live.queue import SqliteWorkQueue
from storytime.state.store import RecoveryActionRecord, StateStore

# A conservative local default: at most one recovery attempt per original failed
# work item (an active or completed recovery blocks a further request).
DEFAULT_MAX_RECOVERY_ATTEMPTS = 1

_WORK_ID_PREFIX = "work-"

# Bounded eligibility decision vocabulary.
RETRY_ELIGIBLE = "retry_eligible"
NOT_FAILED = "not_failed"
UNKNOWN_ORIGINAL = "unknown_original"
DUPLICATE_RECOVERY = "duplicate_recovery"
MAX_ATTEMPTS_REACHED = "max_attempts_reached"
BLOCKED_BY_GOVERNANCE = "blocked_by_governance"
IN_PROGRESS = "in_progress"
TERMINAL_FAILURE = "terminal_failure"

RECOVERY_DECISIONS: frozenset[str] = frozenset(
    {
        RETRY_ELIGIBLE,
        NOT_FAILED,
        UNKNOWN_ORIGINAL,
        DUPLICATE_RECOVERY,
        MAX_ATTEMPTS_REACHED,
        BLOCKED_BY_GOVERNANCE,
        IN_PROGRESS,
        TERMINAL_FAILURE,
    }
)

# Recovery-action status vocabulary (durable).
STATUS_REQUESTED = "requested"
STATUS_CREATED = "created"
STATUS_REJECTED = "rejected"
STATUS_FAILED = "failed"


def _now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(frozen=True, slots=True)
class RecoveryEligibility:
    """The bounded, explainable result of a recovery-eligibility evaluation."""

    eligible: bool
    decision: str
    reason: str


def _failed_at_governance(store: StateStore, run_id: str) -> bool:
    """True if the run's failure was a governance block (terminal, not retryable).

    Uses durable stage_execution rows: a failed stage named ``governance`` is the
    architecture's signal that the failure was a governance decision rather than
    a transient/assembly error.
    """
    for stage in store.list_stage_executions(run_id):
        if stage.stage_name == "governance" and stage.status == "failed":
            return True
    return False


def evaluate_recovery_eligibility(
    store: StateStore,
    original_run_id: str,
    *,
    max_attempts: int = DEFAULT_MAX_RECOVERY_ATTEMPTS,
) -> RecoveryEligibility:
    """Decide whether ``original_run_id`` may be recovered. Backend-owned."""
    run = store.get_run(original_run_id)
    if run is None:
        return RecoveryEligibility(
            False, UNKNOWN_ORIGINAL, "original run does not exist"
        )
    work = store.get_work_item_for_run(original_run_id)
    if work is None:
        return RecoveryEligibility(
            False,
            UNKNOWN_ORIGINAL,
            "original run has no queued work item to recover",
        )
    if run.status == "completed":
        return RecoveryEligibility(
            False, NOT_FAILED, "original run completed; nothing to recover"
        )
    if run.status != "failed":
        return RecoveryEligibility(
            False,
            IN_PROGRESS,
            f"original run is still in progress (status {run.status!r})",
        )
    if _failed_at_governance(store, original_run_id):
        return RecoveryEligibility(
            False,
            BLOCKED_BY_GOVERNANCE,
            "original run failed governance review; recovery is blocked",
        )
    if store.active_recovery_action_for(work.work_id) is not None:
        return RecoveryEligibility(
            False,
            DUPLICATE_RECOVERY,
            "an active recovery action already exists for this work item",
        )
    if store.count_recovery_attempts_for(work.work_id) >= max_attempts:
        return RecoveryEligibility(
            False,
            MAX_ATTEMPTS_REACHED,
            f"recovery attempt limit reached (max {max_attempts})",
        )
    return RecoveryEligibility(True, RETRY_ELIGIBLE, "failed run is recoverable")


def _new_recovery_action_id(original_run_id: str) -> str:
    return f"recovery-{original_run_id}-{secrets.token_hex(3)}"


def request_recovery(
    store: StateStore,
    original_run_id: str,
    *,
    requested_by: str,
    reason: str,
    runs_dir: Path,
    fixtures_dir: Path | None = None,
    max_attempts: int = DEFAULT_MAX_RECOVERY_ATTEMPTS,
) -> RecoveryActionRecord:
    """Request recovery for a failed run; return the durable recovery action.

    On rejection, a durably-visible recovery action is recorded with the bounded
    decision and reason (status ``rejected``). When eligible, an active recovery
    slot is reserved atomically (duplicate-prevention under local SQLite), a new
    recovery execution is reserved and enqueued, and the action is linked to the
    new recovery identity (status ``created``). Eligibility is decided here, in
    the backend — never by a caller/frontend.
    """
    eligibility = evaluate_recovery_eligibility(
        store, original_run_id, max_attempts=max_attempts
    )
    now = _now()
    action_id = _new_recovery_action_id(original_run_id)
    work = store.get_work_item_for_run(original_run_id)
    original_work_item_id = work.work_id if work is not None else "(unknown)"

    if not eligibility.eligible:
        rejected = RecoveryActionRecord(
            recovery_action_id=action_id,
            original_run_id=original_run_id,
            original_work_item_id=original_work_item_id,
            recovery_run_id=None,
            recovery_work_item_id=None,
            recovery_reason=reason,
            requested_by=requested_by,
            requested_at=now,
            status=STATUS_REJECTED,
            decision=eligibility.decision,
            rejection_reason=eligibility.reason,
            attempt_number=store.count_recovery_attempts_for(original_work_item_id)
            + 1,
            updated_at=now,
        )
        store.insert_recovery_action(rejected)
        return rejected

    # Eligible: reserve the active recovery slot atomically first so two
    # concurrent requests cannot both create an active recovery action.
    assert work is not None  # guaranteed by eligibility (would be UNKNOWN_ORIGINAL)
    attempt_number = store.count_recovery_attempts_for(work.work_id) + 1
    requested = RecoveryActionRecord(
        recovery_action_id=action_id,
        original_run_id=original_run_id,
        original_work_item_id=work.work_id,
        recovery_run_id=None,
        recovery_work_item_id=None,
        recovery_reason=reason,
        requested_by=requested_by,
        requested_at=now,
        status=STATUS_REQUESTED,
        decision=RETRY_ELIGIBLE,
        rejection_reason=None,
        attempt_number=attempt_number,
        updated_at=now,
    )
    created = store.atomically_create_recovery_action(
        requested, max_attempts=max_attempts
    )
    if not created:
        # Lost the race to a concurrent request that took the active slot.
        rejected = RecoveryActionRecord(
            recovery_action_id=action_id,
            original_run_id=original_run_id,
            original_work_item_id=work.work_id,
            recovery_run_id=None,
            recovery_work_item_id=None,
            recovery_reason=reason,
            requested_by=requested_by,
            requested_at=now,
            status=STATUS_REJECTED,
            decision=DUPLICATE_RECOVERY,
            rejection_reason="an active recovery action already exists for this "
            "work item",
            attempt_number=attempt_number,
            updated_at=now,
        )
        store.insert_recovery_action(rejected)
        return rejected

    # Materialize the recovery execution and link it back to the original.
    try:
        recovery_run_id = reserve_proof_run(
            store,
            runs_dir=runs_dir,
            fixture_id=work.fixture_id,
            scenario=work.scenario,
            fixtures_dir=fixtures_dir,
        )
        recovery_work_id = f"{_WORK_ID_PREFIX}{recovery_run_id}"
        SqliteWorkQueue(store).enqueue(
            work_id=recovery_work_id,
            pipeline_run_id=recovery_run_id,
            scenario=work.scenario,
            fixture_id=work.fixture_id,
        )
        store._conn.commit()  # noqa: SLF001 - persist recovery enqueue durably
    except BaseException:
        store.update_recovery_action(
            action_id, status=STATUS_FAILED, updated_at=_now()
        )
        raise

    store.update_recovery_action(
        action_id,
        status=STATUS_CREATED,
        recovery_run_id=recovery_run_id,
        recovery_work_item_id=recovery_work_id,
        updated_at=_now(),
    )
    result = store.get_recovery_action(action_id)
    assert result is not None  # just written
    return result
