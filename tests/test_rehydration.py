"""Resume / rehydration of a paused or partial run from SQLite + artifacts."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from storytime.approval import apply_approval_decision
from storytime.config import load_config
from storytime.pipeline import build_runtime_context, resume_run, run_vertical_slice
from storytime.runner import RunnerContext
from storytime.runner.rehydrate import RehydrationError, validate_artifact

_HAS_FFMPEG = shutil.which("ffmpeg") is not None


def _config(root: Path):
    """A config with every storage root under *root* (so a run is relocatable)."""
    return load_config(
        {
            "STORYTIME_RUNS_DIR": str(root / "runs"),
            "STORYTIME_FEED_DIR": str(root / "feed"),
            "STORYTIME_TELEMETRY": "noop",
        }
    )


def _park_and_approve(ctx: RunnerContext, make_workspace) -> str:
    """Create a gated run, pause at the gate, then record an approval."""
    workspace = make_workspace()
    parked = run_vertical_slice(ctx, workspace.manifest_path, require_approval=True)
    assert parked.status == "awaiting_approval"
    run_id = parked.pipeline_run_id
    assert run_id is not None
    apply_approval_decision(
        ctx,
        pipeline_run_id=run_id,
        gate="text",
        decision="approved",
        operator="reviewer",
    )
    return run_id


# -- validate_artifact: integrity is enforced before reuse --------------------

def test_validate_artifact_accepts_a_sound_envelope(
    runtime_context: RunnerContext, make_workspace
) -> None:
    run_id = _park_and_approve(runtime_context, make_workspace)
    key = f"{run_id}/artifacts/ingest/text.plain.json"
    envelope = validate_artifact(runtime_context, key)
    assert envelope.pipeline_run_id == run_id
    assert len(envelope.payload_sha256) == 64


def test_validate_artifact_rejects_a_missing_envelope(
    runtime_context: RunnerContext,
) -> None:
    with pytest.raises(RehydrationError, match="missing or unreadable"):
        validate_artifact(runtime_context, "nope/artifacts/ingest/text.plain.json")


def test_validate_artifact_rejects_an_absolute_key(
    runtime_context: RunnerContext,
) -> None:
    with pytest.raises(RehydrationError, match="not a portable relative path"):
        validate_artifact(runtime_context, "/etc/passwd")


def test_validate_artifact_rejects_a_payload_hash_mismatch(
    runtime_context: RunnerContext, make_workspace
) -> None:
    run_id = _park_and_approve(runtime_context, make_workspace)
    # Corrupt the ingested text payload on disk; its envelope digest no longer
    # matches, so rehydration must refuse to build on it.
    payload_key = f"{run_id}/artifacts/ingest/text.txt"
    runtime_context.storage.write_text(payload_key, "tampered text payload")
    key = f"{run_id}/artifacts/ingest/text.plain.json"
    with pytest.raises(RehydrationError, match="hash mismatch"):
        validate_artifact(runtime_context, key)


# -- build_resume_plan / resume_run guard rails -------------------------------

def test_resume_unknown_run_fails_clearly(runtime_context: RunnerContext) -> None:
    with pytest.raises(RehydrationError, match="no pipeline run found"):
        resume_run(runtime_context, "01NOSUCHRUN0000000000000001")


def test_resume_refuses_a_rejected_run(
    runtime_context: RunnerContext, make_workspace
) -> None:
    workspace = make_workspace()
    parked = run_vertical_slice(
        runtime_context, workspace.manifest_path, require_approval=True
    )
    run_id = parked.pipeline_run_id
    assert run_id is not None
    apply_approval_decision(
        runtime_context,
        pipeline_run_id=run_id,
        gate="text",
        decision="rejected",
        operator="reviewer",
    )
    # A rejected run is failed; it cannot be resumed.
    with pytest.raises(RehydrationError, match="failed/rejected"):
        resume_run(runtime_context, run_id)


# -- resume mechanics that do not require ffmpeg (stop at synthesize) ---------

def test_resume_runs_the_gate_then_synthesize_without_reingesting(
    runtime_context: RunnerContext, make_workspace
) -> None:
    run_id = _park_and_approve(runtime_context, make_workspace)
    state = runtime_context.state

    ingest_runs_before = [
        e for e in state.list_stage_executions(run_id) if e.stage_name == "ingest"
    ]
    assert len(ingest_runs_before) == 1

    outcome = resume_run(runtime_context, run_id, stop_after="synthesize")
    assert outcome.status == "stage_completed"
    assert outcome.last_stage == "synthesize"

    executions = state.list_stage_executions(run_id)
    # ingest is NOT re-executed on resume — still exactly one ingest row.
    assert len([e for e in executions if e.stage_name == "ingest"]) == 1
    # the gate and synthesize did run.
    succeeded = {e.stage_name for e in executions if e.status == "succeeded"}
    assert {"ingest", "approve_text", "synthesize"} <= succeeded
    # TextIngested is emitted exactly once across the whole run.
    assert state.event_types(run_id).count("TextIngested") == 1


def test_pipeline_run_id_is_stable_across_stop_approve_resume(
    runtime_context: RunnerContext, make_workspace
) -> None:
    run_id = _park_and_approve(runtime_context, make_workspace)
    outcome = resume_run(runtime_context, run_id, stop_after="synthesize")
    assert outcome.pipeline_run_id == run_id

    state = runtime_context.state
    run = state.get_run(run_id)
    assert run is not None and run.pipeline_run_id == run_id
    assert all(
        e.pipeline_run_id == run_id for e in state.list_stage_executions(run_id)
    )
    assert all(
        a.pipeline_run_id == run_id for a in state.list_stage_artifacts(run_id)
    )


# -- full-slice resume (needs ffmpeg for the assemble stage) ------------------

@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_resume_completes_a_paused_run(
    runtime_context: RunnerContext, make_workspace
) -> None:
    run_id = _park_and_approve(runtime_context, make_workspace)
    outcome = resume_run(runtime_context, run_id)

    assert outcome.status == "completed"
    assert outcome.pipeline_run_id == run_id
    run = runtime_context.state.get_run(run_id)
    assert run is not None and run.status == "completed"


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_resuming_a_completed_run_is_a_safe_clear_error(
    runtime_context: RunnerContext, make_workspace
) -> None:
    run_id = _park_and_approve(runtime_context, make_workspace)
    resume_run(runtime_context, run_id)  # completes the run

    events_after_first = runtime_context.state.count_events(run_id)
    # A second resume must not re-run anything or duplicate events.
    with pytest.raises(RehydrationError, match="already completed"):
        resume_run(runtime_context, run_id)
    assert runtime_context.state.count_events(run_id) == events_after_first


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_persisted_artifact_paths_are_relative(
    runtime_context: RunnerContext, make_workspace
) -> None:
    run_id = _park_and_approve(runtime_context, make_workspace)
    outcome = resume_run(runtime_context, run_id)
    assert outcome.status == "completed"

    state = runtime_context.state
    # No stage_artifact key is an absolute path.
    for row in state.list_stage_artifacts(run_id):
        assert not Path(row.artifact_key).is_absolute(), row.artifact_key
        assert not row.artifact_key.startswith("/"), row.artifact_key
    # The published episode's audio path is relative to the feed root.
    assert outcome.episode_guid is not None
    episode = state.get_published_episode(outcome.episode_guid)
    assert episode is not None
    assert not Path(episode.audio_path).is_absolute()


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_run_survives_workspace_relocation(
    tmp_path: Path, make_workspace
) -> None:
    # Park + approve a run under one workspace root.
    origin = tmp_path / "origin"
    ctx_a = build_runtime_context(_config(origin))
    try:
        run_id = _park_and_approve(ctx_a, make_workspace)
    finally:
        ctx_a.state.close()

    # Move the entire workspace (state.db + artifacts) to a new location.
    moved = tmp_path / "relocated"
    shutil.copytree(origin, moved)
    shutil.rmtree(origin)

    # Resume from the relocated workspace: relative keys make this work.
    ctx_b = build_runtime_context(_config(moved))
    try:
        outcome = resume_run(ctx_b, run_id)
    finally:
        ctx_b.state.close()
    assert outcome.status == "completed"
    assert outcome.pipeline_run_id == run_id
