"""Approval gate stage — a persisted, interactive operator approval gate.

ARCH-LOCK: Stage Boundary (see storytime.stages.base)
DO NOT REFACTOR: ApprovalGateStage takes a RunnerContext + StageInput and
returns a StageResult. It does not write to SQLite directly, does not call
other stages, and does not import OpenTelemetry.

Approval is a real, persisted pipeline stage, not an interrupt (Architecture
Baseline section 9 and hard decision 6). This stage is a PURE function of its
StageInput: the runner / resume engine reads the persisted operator decision
from SQLite and injects it through StageInput.params. The stage performs no
SQLite I/O of its own, which keeps it trivially unit-testable and keeps every
state write flowing through the declarative StateUpdate the runner applies.

StageInput.params consumed by this stage:
  * ``approval_decision``          — ``None`` | ``"approved"`` | ``"rejected"``
  * ``approval_already_requested`` — ``bool``; ``True`` when a
    ``*_APPROVAL_REQUESTED`` event was already persisted on a prior encounter,
    so a re-run during resume does not append a duplicate request event.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from storytime.dto import StageInput, StageResult, StateUpdate
from storytime.events import EventType, PipelineEvent

if TYPE_CHECKING:
    from storytime.runner.context import RunnerContext

# Decision values an operator may record. The manifest-derived ingest approval
# row is recorded under stage_name "ingest"; an operator GATE decision is
# recorded under the gate stage name, so the two are never conflated.
DECISION_APPROVED = "approved"
DECISION_REJECTED = "rejected"
VALID_DECISIONS = (DECISION_APPROVED, DECISION_REJECTED)


class ApprovalGateStage:
    """A persisted operator approval gate between two pipeline stages.

    The stage is generic over which gate it is (text or audio). Phase 4 wires
    the text gate; the audio gate is a documented carryforward (the only extra
    work is one more stage position and its event types).
    """

    def __init__(
        self,
        *,
        name: str,
        gate: str,
        requested_event: EventType,
    ) -> None:
        # ``name`` is the stage/gate name persisted in stage_execution and the
        # approval table (e.g. "approve_text"). ``gate`` is the short operator
        # label used on the CLI and in event payloads (e.g. "text").
        self.name = name
        self._gate = gate
        self._requested_event = requested_event

    def run(self, ctx: RunnerContext, stage_input: StageInput) -> StageResult:
        """Resolve the gate from the injected decision in StageInput.params."""
        run_id = stage_input.pipeline_run_id
        now = ctx.clock.now()

        decision = stage_input.params.get("approval_decision")
        already_requested = bool(
            stage_input.params.get("approval_already_requested", False)
        )

        if decision == DECISION_APPROVED:
            # The operator approved. The TEXT_APPROVED event was already
            # persisted by `storytime approve`, so the gate emits nothing and
            # simply passes the upstream artifacts through to the next stage.
            return StageResult.succeeded(
                StateUpdate(run_status="running", current_stage=self.name),
                output_artifacts=stage_input.input_artifacts,
            )

        if decision == DECISION_REJECTED:
            # Rejection blocks every downstream stage: run_sequence stops on a
            # non-SUCCEEDED result. The TEXT_REJECTED event was already
            # persisted by `storytime approve`; the gate emits nothing.
            return StageResult.failed(
                error_kind=f"{self._gate.title()}Rejected",
                error_message=(
                    f"operator rejected the {self._gate} at the approval gate; "
                    "downstream stages are blocked"
                ),
                state_update=StateUpdate(
                    run_status="failed", current_stage=self.name
                ),
            )

        # No decision yet: pause the run. The process exits cleanly; the run
        # is rehydrated later once `storytime approve` records a decision.
        events: tuple[PipelineEvent, ...] = ()
        if not already_requested:
            events = (
                PipelineEvent(
                    event_type=self._requested_event,
                    pipeline_run_id=run_id,
                    occurred_at=now,
                    stage_name=self.name,
                    payload={"gate": self._gate},
                ),
            )
        return StageResult.awaiting_approval(
            StateUpdate(run_status="awaiting_approval", current_stage=self.name),
            events=events,
        )


def text_approval_gate() -> ApprovalGateStage:
    """The text approval gate: pauses between ingest and synthesize."""
    return ApprovalGateStage(
        name="approve_text",
        gate="text",
        requested_event=EventType.TEXT_APPROVAL_REQUESTED,
    )


def audio_approval_gate() -> ApprovalGateStage:
    """The audio approval gate (built, not wired in Phase 4 — see docs).

    Provided so the audio gate is a one-line wiring change in a later phase;
    the generic ApprovalGateStage already supports it.
    """
    return ApprovalGateStage(
        name="approve_audio",
        gate="audio",
        requested_event=EventType.AUDIO_APPROVAL_REQUESTED,
    )
