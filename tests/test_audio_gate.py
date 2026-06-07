"""Phase 4.1: the audio approval gate and the event-taxonomy cleanup.

These tests prove the Phase 4.1 acceptance criteria:
  * manifest/provenance approval and operator approval no longer share an
    event name (SourceManifestApproved vs TextApproved);
  * a run can pause at the audio approval gate, be approved/rejected through
    the same persisted approval service the text gate uses, and resume;
  * the text and audio gates are independent — a run may use either or both;
  * a run's gate configuration survives resume even before a gate is reached.
"""

from __future__ import annotations

import shutil

import pytest

from storytime.approval import ApprovalError, apply_approval_decision
from storytime.dto import StageInput, StageStatus
from storytime.events import EventType
from storytime.pipeline import canonical_stage_order, resume_run, run_vertical_slice
from storytime.runner import RunnerContext
from storytime.runner.rehydrate import RehydrationError
from storytime.stages.approve import audio_approval_gate

_HAS_FFMPEG = shutil.which("ffmpeg") is not None


# -- 1. event taxonomy cleanup ------------------------------------------------

def test_ingest_emits_source_manifest_approved_not_text_approved(
    runtime_context: RunnerContext, slice_workspace
) -> None:
    """Provenance approval is SourceManifestApproved, never TextApproved."""
    outcome = run_vertical_slice(
        runtime_context, slice_workspace.manifest_path, require_approval=True
    )
    assert outcome.pipeline_run_id is not None
    events = runtime_context.state.event_types(outcome.pipeline_run_id)

    # Ingest's rights-clearance approval uses the new, unambiguous name.
    assert "SourceManifestApproved" in events
    # The run is parked at the text gate, so no operator TextApproved yet —
    # the two approval concepts no longer collide on one event name.
    assert "TextApproved" not in events


def test_gated_run_event_log_has_no_ambiguous_duplicate(
    runtime_context: RunnerContext, make_workspace
) -> None:
    """After operator approval the two approvals are two distinct events."""
    workspace = make_workspace()
    outcome = run_vertical_slice(
        runtime_context, workspace.manifest_path, require_approval=True
    )
    run_id = outcome.pipeline_run_id
    assert run_id is not None

    apply_approval_decision(
        runtime_context,
        pipeline_run_id=run_id,
        gate="text",
        decision="approved",
        operator="reviewer",
    )
    events = runtime_context.state.event_types(run_id)
    # Exactly one of each: provenance vs operator approval are unambiguous.
    assert events.count("SourceManifestApproved") == 1
    assert events.count("TextApproved") == 1


def test_source_manifest_approved_is_a_distinct_closed_enum_member() -> None:
    """The new event type is a real closed-enum member, not a free string."""
    assert EventType.SOURCE_MANIFEST_APPROVED != EventType.TEXT_APPROVED
    assert EventType.SOURCE_MANIFEST_APPROVED.value == "SourceManifestApproved"


# -- 2. the audio gate stage --------------------------------------------------

def _audio_gate_input(params: dict[str, object]) -> StageInput:
    return StageInput(
        pipeline_run_id="01AUDIOGATE000000000000001",
        stage_name="approve_audio",
        run_dir="01AUDIOGATE000000000000001",
        input_artifacts=("01AUDIOGATE000000000000001/artifacts/synthesize/audio.wav",),
        params=params,
    )


def test_audio_gate_with_no_decision_requests_audio_approval(
    runtime_context: RunnerContext,
) -> None:
    result = audio_approval_gate().run(runtime_context, _audio_gate_input({}))
    assert result.status is StageStatus.AWAITING_APPROVAL
    assert [e.event_type for e in result.events] == [
        EventType.AUDIO_APPROVAL_REQUESTED
    ]


def test_audio_gate_rejection_blocks_downstream(
    runtime_context: RunnerContext,
) -> None:
    result = audio_approval_gate().run(
        runtime_context, _audio_gate_input({"approval_decision": "rejected"})
    )
    assert result.status is StageStatus.FAILED
    assert result.error_kind == "AudioRejected"
    assert result.output_artifacts == ()


# -- 3. the audio gate woven into the pipeline --------------------------------

def test_canonical_order_weaves_the_audio_gate_after_synthesize() -> None:
    assert canonical_stage_order(()) == (
        "ingest",
        "synthesize",
        "assemble",
        "publish",
    )
    assert canonical_stage_order(("audio",)) == (
        "ingest",
        "synthesize",
        "approve_audio",
        "assemble",
        "publish",
    )
    assert canonical_stage_order(("text", "audio")) == (
        "ingest",
        "approve_text",
        "synthesize",
        "approve_audio",
        "assemble",
        "publish",
    )


def test_audio_gated_run_pauses_after_synthesis(
    runtime_context: RunnerContext, slice_workspace
) -> None:
    """An audio-gated run pauses at the audio gate — no ffmpeg needed yet."""
    outcome = run_vertical_slice(
        runtime_context, slice_workspace.manifest_path, require_audio_approval=True
    )
    assert outcome.status == "awaiting_approval"
    assert outcome.awaiting_gate == "audio"

    run_id = outcome.pipeline_run_id
    assert run_id is not None
    # Synthesis ran and completed before the pause; assemble never started.
    executions = {
        e.stage_name: e.status
        for e in runtime_context.state.list_stage_executions(run_id)
    }
    assert executions["synthesize"] == "succeeded"
    assert executions["approve_audio"] == "awaiting_approval"
    assert "assemble" not in executions
    # The gate configuration is persisted on the run row.
    run = runtime_context.state.get_run(run_id)
    assert run is not None and run.gates == ("audio",)


def test_audio_approval_persists_and_is_distinct_from_text(
    runtime_context: RunnerContext, make_workspace
) -> None:
    workspace = make_workspace()
    outcome = run_vertical_slice(
        runtime_context, workspace.manifest_path, require_audio_approval=True
    )
    run_id = outcome.pipeline_run_id
    assert run_id is not None

    apply_approval_decision(
        runtime_context,
        pipeline_run_id=run_id,
        gate="audio",
        decision="approved",
        operator="audio-reviewer",
    )
    decision = runtime_context.state.latest_approval(run_id, "approve_audio")
    assert decision is not None
    assert decision.decision == "approved"
    assert decision.operator == "audio-reviewer"
    assert "AudioApproved" in runtime_context.state.event_types(run_id)
    # The audio decision did not write a text-gate row.
    assert runtime_context.state.latest_approval(run_id, "approve_text") is None


def test_duplicate_audio_approval_fails_cleanly(
    runtime_context: RunnerContext, make_workspace
) -> None:
    workspace = make_workspace()
    outcome = run_vertical_slice(
        runtime_context, workspace.manifest_path, require_audio_approval=True
    )
    run_id = outcome.pipeline_run_id
    assert run_id is not None
    apply_approval_decision(
        runtime_context,
        pipeline_run_id=run_id,
        gate="audio",
        decision="approved",
        operator="audio-reviewer",
    )
    with pytest.raises(ApprovalError, match="duplicate approval"):
        apply_approval_decision(
            runtime_context,
            pipeline_run_id=run_id,
            gate="audio",
            decision="approved",
            operator="audio-reviewer",
        )


def test_audio_rejection_blocks_assembly_and_publish(
    runtime_context: RunnerContext, make_workspace
) -> None:
    workspace = make_workspace()
    outcome = run_vertical_slice(
        runtime_context, workspace.manifest_path, require_audio_approval=True
    )
    run_id = outcome.pipeline_run_id
    assert run_id is not None

    apply_approval_decision(
        runtime_context,
        pipeline_run_id=run_id,
        gate="audio",
        decision="rejected",
        operator="audio-reviewer",
    )
    run = runtime_context.state.get_run(run_id)
    assert run is not None and run.status == "failed"

    # A rejected run cannot be resumed: assembly/publish are blocked.
    with pytest.raises(RehydrationError, match="failed/rejected"):
        resume_run(runtime_context, run_id)
    executions = {
        e.stage_name for e in runtime_context.state.list_stage_executions(run_id)
    }
    assert "assemble" not in executions
    assert "publish" not in executions


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_audio_gated_run_resumes_to_completion_after_approval(
    runtime_context: RunnerContext, make_workspace
) -> None:
    workspace = make_workspace()
    outcome = run_vertical_slice(
        runtime_context, workspace.manifest_path, require_audio_approval=True
    )
    run_id = outcome.pipeline_run_id
    assert run_id is not None

    apply_approval_decision(
        runtime_context,
        pipeline_run_id=run_id,
        gate="audio",
        decision="approved",
        operator="audio-reviewer",
    )
    resumed = resume_run(runtime_context, run_id)
    assert resumed.status == "completed"
    # synthesize was completed before the pause and is NOT regenerated.
    synth_runs = [
        e
        for e in runtime_context.state.list_stage_executions(run_id)
        if e.stage_name == "synthesize" and e.status == "succeeded"
    ]
    assert len(synth_runs) == 1


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_both_gates_pause_independently_and_resume_to_completion(
    runtime_context: RunnerContext, make_workspace
) -> None:
    """A run with both gates pauses at text, then at audio, then completes."""
    workspace = make_workspace()
    outcome = run_vertical_slice(
        runtime_context,
        workspace.manifest_path,
        require_approval=True,
        require_audio_approval=True,
    )
    run_id = outcome.pipeline_run_id
    assert run_id is not None
    # First pause: the text gate, before synthesis.
    assert outcome.status == "awaiting_approval"
    assert outcome.awaiting_gate == "text"

    apply_approval_decision(
        runtime_context,
        pipeline_run_id=run_id,
        gate="text",
        decision="approved",
        operator="reviewer",
    )
    # Resuming re-inserts the not-yet-reached audio gate from the run's
    # persisted gate configuration: the run pauses again, this time at audio.
    second = resume_run(runtime_context, run_id)
    assert second.status == "awaiting_approval"
    assert second.awaiting_gate == "audio"

    apply_approval_decision(
        runtime_context,
        pipeline_run_id=run_id,
        gate="audio",
        decision="approved",
        operator="audio-reviewer",
    )
    third = resume_run(runtime_context, run_id)
    assert third.status == "completed"


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_auto_approve_satisfies_both_gates(
    runtime_context: RunnerContext, make_workspace
) -> None:
    """--auto-approve loops over every gate the run pauses at."""
    workspace = make_workspace()
    outcome = run_vertical_slice(
        runtime_context,
        workspace.manifest_path,
        require_audio_approval=True,
        auto_approve=True,
    )
    assert outcome.status == "completed"
    run_id = outcome.pipeline_run_id
    assert run_id is not None
    # Both gates were satisfied by genuine, persisted decisions.
    text = runtime_context.state.latest_approval(run_id, "approve_text")
    audio = runtime_context.state.latest_approval(run_id, "approve_audio")
    assert text is not None and text.decision == "approved"
    assert audio is not None and audio.decision == "approved"
