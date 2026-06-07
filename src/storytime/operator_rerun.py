"""Operator pipeline re-run — the Phase 10D governed mutation surface.

ARCH-LOCK: Re-run is a governed, bounded, audited state reset — not an engine
DO NOT REFACTOR: This module implements Phase 10D, StoryTime's first operator
*mutation* surface. It does exactly one thing: when, and only when, a failed
run is provably safe to retry, it resets that run's persisted ``status`` from
``failed`` back to the existing ``running`` state so the existing
``storytime run --resume`` path can re-execute it from the failed stage. That
single ``pipeline_run.status`` update is the whole mutation.

It is deliberately NOT a workflow engine. There is no broker, no background
worker, no daemon, no scheduler, no job queue, no new lifecycle state, and no
new database column. ``rerun`` itself runs no pipeline work — it resets state
and tells the operator the existing command to run next. Every actual mutation
is recorded as an audit event in the existing append-only ``event_log`` (the
``RUN_RERUN_REQUESTED`` event type). Eligibility is evaluated by a small,
pure-ish decision function that defaults to rejection whenever safety cannot
be proven, and a re-run never bypasses an unresolved Trust Envelope governance
decision.

This module reads SQLite, reads the Trust Envelope projection, and on an
eligible non-dry-run request performs the single bounded status reset plus the
audit event. It imports no OpenTelemetry and no web/template code.
"""

from __future__ import annotations

from dataclasses import dataclass

from storytime.events import EventType, PipelineEvent
from storytime.state import StateStore
from storytime.util.clock import Clock
from storytime.util.ids import new_ulid

# The pipeline work stages an operator may name with ``--from-stage``. The
# approval-gate stages (``approve_text`` / ``approve_audio``) are operator
# decision points, not re-run entry points, and are deliberately excluded.
CANONICAL_RERUN_STAGES: tuple[str, ...] = (
    "ingest",
    "synthesize",
    "assemble",
    "publish",
)

# Stage-execution statuses that count as a successful (non-failing) stage.
_SUCCESS_STAGE_STATUSES = frozenset({"SUCCEEDED", "succeeded"})

# The resumable run status a re-run resets a failed run to. This is an
# EXISTING lifecycle state — Phase 10D introduces no new run status.
_RESUMABLE_STATUS = "running"

# --- stable eligibility decision codes -------------------------------------
CODE_ELIGIBLE = "eligible"
CODE_RUN_NOT_FOUND = "run_not_found"
CODE_NOT_RETRYABLE_STATUS = "not_retryable_status"
CODE_OPERATOR_REJECTED = "operator_rejected"
CODE_STAGE_UNKNOWN = "stage_unknown"
CODE_STAGE_MISMATCH = "stage_mismatch"
CODE_GOVERNANCE_BLOCKED = "governance_blocked"
CODE_TRUST_ENVELOPE_MISSING = "trust_envelope_missing"
CODE_TRUST_ENVELOPE_DENIED = "trust_envelope_denied"
CODE_UNSAFE_UNKNOWN_STATE = "unsafe_unknown_state"


@dataclass(frozen=True, slots=True)
class RerunDecision:
    """A structured, bounded re-run eligibility decision.

    Pure data — the result of :func:`evaluate_rerun_eligibility`. ``code`` is a
    stable, testable string from the ``CODE_*`` set; ``message`` is a short,
    safe operator-facing summary that never contains raw story text, raw
    exception text, or sensitive governance internals.
    """

    eligible: bool
    code: str
    message: str
    run_id: str
    from_stage: str | None = None
    current_status: str | None = None
    governance_status: str | None = None
    source_id: str | None = None


@dataclass(frozen=True, slots=True)
class RerunResult:
    """The outcome of a re-run request: the decision plus any mutation.

    ``performed`` is True only when an actual state mutation occurred — never
    for a dry run and never for a rejected request. ``mutation_id`` and
    ``timestamp`` are populated only for a performed mutation; they identify
    the audit event written to the append-only event log.
    """

    decision: RerunDecision
    dry_run: bool
    performed: bool
    mutation_id: str | None = None
    timestamp: str | None = None
    previous_status: str | None = None
    new_status: str | None = None


def _failing_stage(store: StateStore, run_id: str) -> tuple[str | None, str | None]:
    """Return the (stage_name, error_kind) of a run's last failing stage.

    Only the structured ``error_kind`` code is returned — never the unbounded
    ``error_message`` text. ``(None, None)`` when no failed stage execution is
    recorded.
    """
    stage: str | None = None
    error_kind: str | None = None
    for execution in store.list_stage_executions(run_id):
        if execution.status not in _SUCCESS_STAGE_STATUSES:
            stage = execution.stage_name
            error_kind = execution.error_kind
    return stage, error_kind


def evaluate_rerun_eligibility(
    store: StateStore,
    run_id: str,
    *,
    requested_from_stage: str | None = None,
) -> RerunDecision:
    """Decide whether *run_id* may be safely re-run. Defaults to rejection.

    A re-run is eligible only when the run exists, is in the ``failed`` state
    because of a genuine stage failure (not an operator approval-gate
    rejection), and carries an ``APPROVED`` Trust Envelope governance
    decision. Any unresolved governance decision, a missing Trust Envelope, an
    unknown ``--from-stage``, or an unclassifiable state yields a rejection
    with a stable ``code``. This function only reads state; it mutates nothing.
    """
    run = store.get_run(run_id)
    if run is None:
        return RerunDecision(
            eligible=False,
            code=CODE_RUN_NOT_FOUND,
            message=f"No pipeline run found with run_id={run_id}.",
            run_id=run_id,
        )

    # A supplied --from-stage must name a known pipeline work stage.
    if requested_from_stage is not None and (
        requested_from_stage not in CANONICAL_RERUN_STAGES
    ):
        return RerunDecision(
            eligible=False,
            code=CODE_STAGE_UNKNOWN,
            message=(
                f"Unknown stage {requested_from_stage!r}; expected one of: "
                f"{', '.join(CANONICAL_RERUN_STAGES)}."
            ),
            run_id=run_id,
            current_status=run.status,
        )

    # Only a failed run is a re-run target. A completed, running,
    # awaiting-approval, or stage-completed run is not re-runnable here.
    if run.status != "failed":
        return RerunDecision(
            eligible=False,
            code=CODE_NOT_RETRYABLE_STATUS,
            message=(
                f"Run status is {run.status!r}; only a failed run can be "
                "re-run. Nothing to do."
            ),
            run_id=run_id,
            current_status=run.status,
        )

    failing_stage, error_kind = _failing_stage(store, run_id)
    if failing_stage is None:
        # A failed run with no failed stage execution is internally
        # inconsistent — refuse rather than guess.
        return RerunDecision(
            eligible=False,
            code=CODE_UNSAFE_UNKNOWN_STATE,
            message=(
                "Run is marked failed but no failing stage was recorded; its "
                "state cannot be classified safely."
            ),
            run_id=run_id,
            current_status=run.status,
        )

    # An operator approval-gate rejection must not be overridden by a re-run.
    if error_kind is not None and error_kind.endswith("Rejected"):
        return RerunDecision(
            eligible=False,
            code=CODE_OPERATOR_REJECTED,
            message=(
                "Run was rejected by an operator at an approval gate; a "
                "re-run cannot override that decision. Start a new run."
            ),
            run_id=run_id,
            from_stage=failing_stage,
            current_status=run.status,
        )

    # Governance: the Trust Envelope decision must be APPROVED. A missing or
    # non-approved envelope fails closed.
    envelope = store.latest_trust_envelope(run_id)
    if envelope is None:
        return RerunDecision(
            eligible=False,
            code=CODE_TRUST_ENVELOPE_MISSING,
            message=(
                "No Trust Envelope governance record exists for this run; a "
                "re-run cannot proceed without one."
            ),
            run_id=run_id,
            from_stage=failing_stage,
            current_status=run.status,
        )
    governance = envelope.decision
    source_id = envelope.source_ref
    if governance == "BLOCKED":
        return RerunDecision(
            eligible=False,
            code=CODE_GOVERNANCE_BLOCKED,
            message=(
                "Run is blocked by governance; a re-run cannot bypass a "
                "governance block."
            ),
            run_id=run_id,
            from_stage=failing_stage,
            current_status=run.status,
            governance_status=governance,
            source_id=source_id,
        )
    if governance != "APPROVED":
        return RerunDecision(
            eligible=False,
            code=CODE_TRUST_ENVELOPE_DENIED,
            message=(
                f"Trust Envelope governance decision is {governance!r}; only "
                "an approved source may be re-run."
            ),
            run_id=run_id,
            from_stage=failing_stage,
            current_status=run.status,
            governance_status=governance,
            source_id=source_id,
        )

    # Phase 10D re-runs from the stage the run failed at. A supplied
    # --from-stage must match that stage; re-running from an earlier stage is
    # deliberately out of scope for Phase 10D.
    if requested_from_stage is not None and requested_from_stage != failing_stage:
        return RerunDecision(
            eligible=False,
            code=CODE_STAGE_MISMATCH,
            message=(
                f"Run failed at stage {failing_stage!r}; Phase 10D re-runs "
                f"from the failed stage. Requested {requested_from_stage!r} "
                "does not match. Omit --from-stage, or pass the failed stage."
            ),
            run_id=run_id,
            from_stage=failing_stage,
            current_status=run.status,
            governance_status=governance,
            source_id=source_id,
        )

    return RerunDecision(
        eligible=True,
        code=CODE_ELIGIBLE,
        message=(
            f"Run is eligible for re-run from stage {failing_stage!r}; "
            "governance is approved."
        ),
        run_id=run_id,
        from_stage=failing_stage,
        current_status=run.status,
        governance_status=governance,
        source_id=source_id,
    )


def perform_rerun(
    store: StateStore,
    clock: Clock,
    run_id: str,
    *,
    requested_from_stage: str | None = None,
    dry_run: bool = False,
) -> RerunResult:
    """Evaluate and, if eligible and not a dry run, perform the re-run reset.

    On an eligible, non-dry-run request this performs the single bounded
    mutation — resetting the run's ``status`` from ``failed`` to the existing
    resumable ``running`` state — and writes a ``RUN_RERUN_REQUESTED`` audit
    event to the append-only event log, atomically. A dry run and a rejected
    request mutate nothing (including the audit log).
    """
    decision = evaluate_rerun_eligibility(
        store, run_id, requested_from_stage=requested_from_stage
    )
    if not decision.eligible or dry_run:
        return RerunResult(decision=decision, dry_run=dry_run, performed=False)

    run = store.get_run(run_id)
    # evaluate_rerun_eligibility already proved the run exists and is failed;
    # this guard keeps the type-checker honest and fails closed if state
    # changed underneath us.
    if run is None or run.status != "failed":
        return RerunResult(
            decision=RerunDecision(
                eligible=False,
                code=CODE_UNSAFE_UNKNOWN_STATE,
                message="Run state changed before the re-run could be applied.",
                run_id=run_id,
            ),
            dry_run=dry_run,
            performed=False,
        )

    mutation_id = new_ulid()
    now = clock.now()
    previous_status = run.status
    audit_event = PipelineEvent(
        event_type=EventType.RUN_RERUN_REQUESTED,
        pipeline_run_id=run_id,
        occurred_at=now,
        stage_name="rerun",
        payload={
            "mutation_id": mutation_id,
            "from_stage": decision.from_stage,
            "previous_status": previous_status,
            "new_status": _RESUMABLE_STATUS,
            "governance_decision": decision.governance_status,
            "dry_run": False,
        },
    )
    with store.transaction():
        store.update_run_state(
            run_id,
            status=_RESUMABLE_STATUS,
            current_stage=run.current_stage,
            updated_at=now.isoformat(),
        )
        store.append_event(audit_event)

    return RerunResult(
        decision=decision,
        dry_run=False,
        performed=True,
        mutation_id=mutation_id,
        timestamp=now.isoformat(),
        previous_status=previous_status,
        new_status=_RESUMABLE_STATUS,
    )


# The exact, ordered key allowlist for `--json` output. JSON is built from this
# list explicitly — the result dataclasses are never serialised wholesale — so
# no field can leak into JSON by accident.
_JSON_FIELDS: tuple[str, ...] = (
    "run_id",
    "source_id",
    "current_status",
    "requested_action",
    "from_stage",
    "dry_run",
    "eligible",
    "code",
    "message",
    "mutation_id",
    "previous_status",
    "new_status",
    "governance_status",
    "next_action",
)


def _next_action(result: RerunResult) -> str:
    """Return a safe, suggestion-only next operator step for a re-run result."""
    decision = result.decision
    if result.performed:
        return (
            f"Run `storytime run --resume {decision.run_id}` to re-execute the "
            "run from the failed stage."
        )
    if decision.eligible and result.dry_run:
        return (
            f"Dry run only — no state changed. Run `storytime rerun "
            f"{decision.run_id}` without --dry-run to apply the re-run reset."
        )
    if decision.eligible:
        return "Re-run is eligible."
    # Rejected: a neutral, non-mutating hint.
    return (
        "Resolve the cause shown above before retrying; the re-run was not "
        "applied."
    )


def _result_fields(result: RerunResult) -> dict[str, object]:
    """Return the full, allowlisted field mapping for a re-run result."""
    decision = result.decision
    return {
        "run_id": decision.run_id,
        "source_id": decision.source_id,
        "current_status": decision.current_status,
        "requested_action": "rerun",
        "from_stage": decision.from_stage,
        "dry_run": result.dry_run,
        "eligible": decision.eligible,
        "code": decision.code,
        "message": decision.message,
        "mutation_id": result.mutation_id,
        "previous_status": result.previous_status,
        "new_status": result.new_status,
        "governance_status": decision.governance_status,
        "next_action": _next_action(result),
    }


def render_rerun_json(result: RerunResult) -> str:
    """Render a re-run result as deterministic, allowlisted JSON.

    Keys are sorted and restricted to the field allowlist, so the output is
    stable in structure for identical state. (``mutation_id`` and a performed
    re-run's audit timestamp are inherently unique per mutation.)
    """
    import json

    fields = _result_fields(result)
    payload = {key: fields[key] for key in _JSON_FIELDS}
    return json.dumps(payload, indent=2, sort_keys=True)


def render_rerun_text(result: RerunResult) -> str:
    """Render a re-run result as a concise, safe plain-text block.

    Contains only bounded structured fields — no raw story text, no raw
    exception text, no sensitive governance internals.
    """
    f = _result_fields(result)
    verdict = "ELIGIBLE" if f["eligible"] else "REJECTED"
    if result.performed:
        verdict = "RE-RUN APPLIED"
    elif f["eligible"] and result.dry_run:
        verdict = "ELIGIBLE (dry run — not applied)"
    lines = [
        f"rerun {f['run_id']}: {verdict}",
        f"  requested action: {f['requested_action']}"
        f"{' (dry run)' if result.dry_run else ''}",
        f"  current status:   {f['current_status'] or '-'}",
        f"  from stage:       {f['from_stage'] or '-'}",
        f"  governance:       {f['governance_status'] or '-'}",
        f"  source:           {f['source_id'] or '-'}",
        f"  decision code:    {f['code']}",
        f"  detail:           {f['message']}",
    ]
    if result.performed:
        lines.append(f"  previous status:  {f['previous_status']}")
        lines.append(f"  new status:       {f['new_status']}")
        lines.append(f"  mutation id:      {f['mutation_id']}")
    lines.append(f"  next:             {f['next_action']}")
    return "\n".join(lines)
