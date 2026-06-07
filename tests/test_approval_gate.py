"""The persisted interactive approval gate: the gate stage and approve service."""

from __future__ import annotations

import shutil

import pytest

from storytime.approval import ApprovalError, apply_approval_decision
from storytime.dto import StageInput, StageStatus
from storytime.events import EventType
from storytime.pipeline import run_vertical_slice
from storytime.runner import RunnerContext
from storytime.stages.approve import text_approval_gate

_HAS_FFMPEG = shutil.which("ffmpeg") is not None


# -- the gate stage is a pure function of StageInput.params -------------------

def _gate_input(params: dict[str, object]) -> StageInput:
    return StageInput(
        pipeline_run_id="01GATETEST0000000000000001",
        stage_name="approve_text",
        run_dir="01GATETEST0000000000000001",
        input_artifacts=("01GATETEST0000000000000001/artifacts/ingest/text.plain.json",),
        params=params,
    )


def test_gate_with_no_decision_pauses_and_requests_approval(
    runtime_context: RunnerContext,
) -> None:
    result = text_approval_gate().run(runtime_context, _gate_input({}))

    assert result.status is StageStatus.AWAITING_APPROVAL
    assert result.state_update.run_status == "awaiting_approval"
    # A fresh gate emits exactly one TextApprovalRequested event.
    assert [e.event_type for e in result.events] == [
        EventType.TEXT_APPROVAL_REQUESTED
    ]


def test_gate_does_not_re_request_when_already_requested(
    runtime_context: RunnerContext,
) -> None:
    # On a resumed run the request event already exists; do not duplicate it.
    result = text_approval_gate().run(
        runtime_context, _gate_input({"approval_already_requested": True})
    )
    assert result.status is StageStatus.AWAITING_APPROVAL
    assert result.events == ()


def test_gate_with_approved_decision_passes_artifacts_through(
    runtime_context: RunnerContext,
) -> None:
    stage_input = _gate_input({"approval_decision": "approved"})
    result = text_approval_gate().run(runtime_context, stage_input)

    assert result.status is StageStatus.SUCCEEDED
    assert result.state_update.run_status == "running"
    # The upstream text artifact is threaded through to synthesize unchanged.
    assert result.output_artifacts == stage_input.input_artifacts
    # The TextApproved event is the approve service's job, not the gate's.
    assert result.events == ()


def test_gate_with_rejected_decision_fails_and_blocks_downstream(
    runtime_context: RunnerContext,
) -> None:
    result = text_approval_gate().run(
        runtime_context, _gate_input({"approval_decision": "rejected"})
    )
    assert result.status is StageStatus.FAILED
    assert result.error_kind == "TextRejected"
    assert result.state_update.run_status == "failed"
    # A FAILED gate result stops run_sequence — downstream stages never run.
    assert result.output_artifacts == ()


# -- the approve service records a persisted operator decision ----------------

def _parked_run(ctx: RunnerContext, make_workspace) -> str:
    """Create a run that is paused at the text approval gate."""
    workspace = make_workspace()
    outcome = run_vertical_slice(ctx, workspace.manifest_path, require_approval=True)
    assert outcome.status == "awaiting_approval"
    assert outcome.pipeline_run_id is not None
    return outcome.pipeline_run_id


def test_approve_records_a_persisted_decision_and_event(
    runtime_context: RunnerContext, make_workspace
) -> None:
    run_id = _parked_run(runtime_context, make_workspace)

    outcome = apply_approval_decision(
        runtime_context,
        pipeline_run_id=run_id,
        gate="text",
        decision="approved",
        operator="reviewer",
    )
    assert outcome.decision == "approved"

    state = runtime_context.state
    decision = state.latest_approval(run_id, "approve_text")
    assert decision is not None
    assert decision.decision == "approved"
    assert decision.operator == "reviewer"
    # The TextApproved event is appended to the event_log.
    assert "TextApproved" in state.event_types(run_id)


def test_reject_moves_the_run_to_a_failed_state(
    runtime_context: RunnerContext, make_workspace
) -> None:
    run_id = _parked_run(runtime_context, make_workspace)

    outcome = apply_approval_decision(
        runtime_context,
        pipeline_run_id=run_id,
        gate="text",
        decision="rejected",
        operator="reviewer",
    )
    assert outcome.run_status == "failed"

    run = runtime_context.state.get_run(run_id)
    assert run is not None and run.status == "failed"
    decision = runtime_context.state.latest_approval(run_id, "approve_text")
    assert decision is not None and decision.decision == "rejected"
    assert "TextRejected" in runtime_context.state.event_types(run_id)


def test_duplicate_approval_is_rejected(
    runtime_context: RunnerContext, make_workspace
) -> None:
    run_id = _parked_run(runtime_context, make_workspace)
    apply_approval_decision(
        runtime_context,
        pipeline_run_id=run_id,
        gate="text",
        decision="approved",
        operator="reviewer",
    )
    with pytest.raises(ApprovalError, match="duplicate approval"):
        apply_approval_decision(
            runtime_context,
            pipeline_run_id=run_id,
            gate="text",
            decision="approved",
            operator="reviewer",
        )


def test_approving_an_unknown_run_fails_clearly(
    runtime_context: RunnerContext,
) -> None:
    with pytest.raises(ApprovalError, match="no pipeline run found"):
        apply_approval_decision(
            runtime_context,
            pipeline_run_id="01NOSUCHRUN0000000000000001",
            gate="text",
            decision="approved",
            operator="reviewer",
        )


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_approving_a_run_not_awaiting_approval_fails_clearly(
    runtime_context: RunnerContext, slice_workspace
) -> None:
    # A plain Phase 3 run completes without ever pausing at a gate.
    outcome = run_vertical_slice(runtime_context, slice_workspace.manifest_path)
    assert outcome.status == "completed"
    assert outcome.pipeline_run_id is not None
    with pytest.raises(ApprovalError, match="not awaiting approval"):
        apply_approval_decision(
            runtime_context,
            pipeline_run_id=outcome.pipeline_run_id,
            gate="text",
            decision="approved",
            operator="reviewer",
        )


def test_invalid_decision_value_is_rejected(
    runtime_context: RunnerContext, make_workspace
) -> None:
    run_id = _parked_run(runtime_context, make_workspace)
    with pytest.raises(ApprovalError, match="invalid decision"):
        apply_approval_decision(
            runtime_context,
            pipeline_run_id=run_id,
            gate="text",
            decision="maybe",
            operator="reviewer",
        )
