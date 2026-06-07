"""Approval decision service — the persistence behind ``storytime approve``.

ARCH-LOCK: Single-transaction persistence
DO NOT REFACTOR: an operator decision writes the approval row, the
TextApproved / TextRejected event, and any run-status transition in ONE
SQLite transaction. Partial persistence would let the event_log and the
approval / run state disagree after a crash.

Recording an operator decision is an operator ACTION, not a pipeline stage, so
it does not flow through StageResult / StateUpdate. It is a small, explicit
state-store service invoked directly by the CLI. The gate stage
(storytime.stages.approve) later consumes the decision recorded here.
"""

from __future__ import annotations

from dataclasses import dataclass

from storytime.adapters.telemetry.attributes import LABEL_DECISION, LABEL_GATE
from storytime.adapters.telemetry.metrics import METRIC_APPROVALS_TOTAL
from storytime.events import EventType, PipelineEvent
from storytime.runner.context import RunnerContext
from storytime.stages.approve import DECISION_APPROVED, DECISION_REJECTED, VALID_DECISIONS


# The operator-facing gate labels and the stage/event identities they map to.
# Phase 4 wires the text gate; the audio gate is built but not yet wired.
@dataclass(frozen=True, slots=True)
class _GateSpec:
    """The stage name and event types of one approval gate."""

    stage_name: str
    approved_event: EventType
    rejected_event: EventType


_GATES: dict[str, _GateSpec] = {
    "text": _GateSpec(
        stage_name="approve_text",
        approved_event=EventType.TEXT_APPROVED,
        rejected_event=EventType.TEXT_REJECTED,
    ),
    "audio": _GateSpec(
        stage_name="approve_audio",
        approved_event=EventType.AUDIO_APPROVED,
        rejected_event=EventType.AUDIO_REJECTED,
    ),
}
VALID_GATES = tuple(_GATES)


class ApprovalError(RuntimeError):
    """Raised when an operator approval decision cannot be applied."""


@dataclass(frozen=True, slots=True)
class ApprovalOutcome:
    """The result of recording an operator approval decision."""

    pipeline_run_id: str
    gate: str
    gate_stage_name: str
    decision: str
    operator: str
    run_status: str


def _latest_stage_trace_id(ctx: RunnerContext, pipeline_run_id: str) -> str | None:
    """Return the most recent stage_execution trace_id for a run, or None.

    Phase 5: the approval gate's *inbound* trace is the trace that produced
    the artifact now awaiting an operator decision -- i.e. the trace of the
    last stage the paused run executed. It is recorded on the approval row as
    a durable view anchor; pipeline_run_id remains the correlation key, and a
    NULL trace_id (telemetry was disabled) is a perfectly valid result.
    """
    for record in reversed(ctx.state.list_stage_executions(pipeline_run_id)):
        if record.trace_id:
            return record.trace_id
    return None


def apply_approval_decision(
    ctx: RunnerContext,
    *,
    pipeline_run_id: str,
    gate: str,
    decision: str,
    operator: str,
    notes: str | None = None,
) -> ApprovalOutcome:
    """Record an operator approval/rejection for a run awaiting approval.

    Fails clearly (ApprovalError) for: an unknown gate, an invalid decision,
    an unknown run id, a run that is not awaiting approval, or a duplicate
    decision for a gate that already has one. On success the approval row and
    its event are persisted in a single transaction; a rejection also
    transitions the run to ``failed`` so the rejected state is explicit.
    """
    if gate not in _GATES:
        raise ApprovalError(
            f"unknown approval gate {gate!r}; valid gates: {', '.join(VALID_GATES)}"
        )
    if decision not in VALID_DECISIONS:
        raise ApprovalError(
            f"invalid decision {decision!r}; expected one of "
            f"{', '.join(VALID_DECISIONS)}"
        )

    gate_spec = _GATES[gate]
    gate_stage_name = gate_spec.stage_name

    run = ctx.state.get_run(pipeline_run_id)
    if run is None:
        raise ApprovalError(
            f"no pipeline run found with pipeline_run_id={pipeline_run_id!r}"
        )
    if run.status != "awaiting_approval":
        raise ApprovalError(
            f"run {pipeline_run_id} is not awaiting approval "
            f"(current status: {run.status}); nothing to approve"
        )

    existing = ctx.state.latest_approval(pipeline_run_id, gate_stage_name)
    if existing is not None:
        raise ApprovalError(
            f"run {pipeline_run_id} already has a {gate} approval decision "
            f"({existing.decision}); duplicate approval rejected"
        )

    now = ctx.clock.now()
    decided_at = now.isoformat()
    approved = decision == DECISION_APPROVED
    event_type = gate_spec.approved_event if approved else gate_spec.rejected_event
    # A rejection ends the run: the locked run-status vocabulary has no
    # distinct "rejected" value, so the run becomes "failed" and the approval
    # row's decision="rejected" is the explicit, queryable rejection record.
    new_status = run.status if approved else "failed"

    # Phase 5: anchor the gate to the trace that produced the artifact under
    # review. Read before the transaction; it is a pure read of view metadata.
    inbound_trace_id = _latest_stage_trace_id(ctx, pipeline_run_id)

    with ctx.state.transaction():
        ctx.state.record_approval(
            pipeline_run_id=pipeline_run_id,
            stage_name=gate_stage_name,
            decision=decision,
            operator=operator,
            decided_at=decided_at,
            notes=notes,
            inbound_trace_id=inbound_trace_id,
        )
        ctx.state.append_event(
            PipelineEvent(
                event_type=event_type,
                pipeline_run_id=pipeline_run_id,
                occurred_at=now,
                stage_name=gate_stage_name,
                payload={"gate": gate, "operator": operator, "decision": decision},
            )
        )
        if new_status != run.status:
            ctx.state.update_run_state(
                pipeline_run_id,
                status=new_status,
                current_stage=run.current_stage,
                updated_at=decided_at,
            )

    # Telemetry is a view, recorded only after the decision is durably
    # persisted -- it must never gate the transaction above. Under
    # NoopTelemetry this is a no-op; pipeline_run_id is deliberately not a
    # label (unbounded), only the low-cardinality gate / decision pair is.
    ctx.telemetry.record_metric(
        METRIC_APPROVALS_TOTAL,
        1,
        attributes={LABEL_GATE: gate, LABEL_DECISION: decision},
    )

    return ApprovalOutcome(
        pipeline_run_id=pipeline_run_id,
        gate=gate,
        gate_stage_name=gate_stage_name,
        decision=decision,
        operator=operator,
        run_status=new_status,
    )


__all__ = [
    "ApprovalError",
    "ApprovalOutcome",
    "DECISION_APPROVED",
    "DECISION_REJECTED",
    "VALID_DECISIONS",
    "VALID_GATES",
    "apply_approval_decision",
]
