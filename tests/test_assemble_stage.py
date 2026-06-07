"""AssembleStage: MP3 packaging with explicit ffmpeg fail-fast."""

from __future__ import annotations

import json
import shutil

import pytest

from storytime.adapters.tts import MockTTS
from storytime.artifacts import PayloadKind, from_json
from storytime.dto import StageInput, StageStatus
from storytime.events import EventType
from storytime.runner import RunnerContext
from storytime.stages import AssembleStage, IngestStage, SynthesizeStage
from storytime.stages.encode import FfmpegMp3Encoder

_HAS_FFMPEG = shutil.which("ffmpeg") is not None
RUN_ID = "01TESTASSEMBLE000000000001"


def _wav_artifact(ctx: RunnerContext, manifest_path: str) -> str:
    """Run ingest + synthesize and return the audio.wav artifact key."""
    ingest = IngestStage().run(
        ctx,
        StageInput(
            pipeline_run_id=RUN_ID,
            stage_name="ingest",
            run_dir=RUN_ID,
            params={"manifest_path": manifest_path},
        ),
    )
    assert ingest.status is StageStatus.SUCCEEDED
    synth = SynthesizeStage(MockTTS()).run(
        ctx,
        StageInput(
            pipeline_run_id=RUN_ID,
            stage_name="synthesize",
            run_dir=RUN_ID,
            input_artifacts=ingest.output_artifacts,
        ),
    )
    assert synth.status is StageStatus.SUCCEEDED
    return synth.output_artifacts[0]


def _assemble_input(wav_artifact: str) -> StageInput:
    return StageInput(
        pipeline_run_id=RUN_ID,
        stage_name="assemble",
        run_dir=RUN_ID,
        input_artifacts=(wav_artifact,),
    )


def test_assemble_fails_fast_when_ffmpeg_absent(
    runtime_context: RunnerContext, slice_workspace
) -> None:
    wav_artifact = _wav_artifact(
        runtime_context, str(slice_workspace.manifest_path)
    )
    # An encoder with no ffmpeg path: deterministically unavailable.
    stage = AssembleStage(
        FfmpegMp3Encoder(None),
        episode_title="The Raven",
        episode_description="A public-domain reading.",
    )
    result = stage.run(runtime_context, _assemble_input(wav_artifact))

    assert result.status is StageStatus.FAILED
    assert result.error_kind == "FfmpegUnavailable"
    assert "ffmpeg" in (result.error_message or "").lower()
    assert "install" in (result.error_message or "").lower()
    assert result.state_update.run_status == "failed"

    run_failed = [
        e for e in result.events if e.event_type is EventType.RUN_FAILED
    ]
    assert run_failed, "an absent ffmpeg must emit an explicit RUN_FAILED event"
    assert run_failed[0].payload.get("reason") == "ffmpeg_unavailable"


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_assemble_produces_mp3_and_metadata(
    runtime_context: RunnerContext, slice_workspace
) -> None:
    wav_artifact = _wav_artifact(
        runtime_context, str(slice_workspace.manifest_path)
    )
    stage = AssembleStage(
        FfmpegMp3Encoder.autodetect(),
        episode_title="The Raven",
        episode_description="A public-domain reading.",
    )
    result = stage.run(runtime_context, _assemble_input(wav_artifact))

    assert result.status is StageStatus.SUCCEEDED
    assert len(result.output_artifacts) == 2

    mp3_envelope = from_json(
        runtime_context.storage.read_text(result.output_artifacts[0])
    )
    metadata_envelope = from_json(
        runtime_context.storage.read_text(result.output_artifacts[1])
    )
    assert mp3_envelope.payload_kind is PayloadKind.AUDIO_MP3
    assert metadata_envelope.payload_kind is PayloadKind.EPISODE_METADATA

    # The MP3 payload is a real, non-empty file.
    mp3_path = runtime_context.storage.resolve(mp3_envelope.payload_path)
    assert mp3_path.is_file()
    assert mp3_path.stat().st_size > 0

    metadata = json.loads(
        runtime_context.storage.read_text(metadata_envelope.payload_path)
    )
    assert metadata["episode_guid"]
    assert metadata["title"] == "The Raven"

    assert any(
        e.event_type is EventType.ASSEMBLY_COMPLETED for e in result.events
    )
