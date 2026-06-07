"""SynthesizeStage: real WAV synthesis via the injected TTS adapter."""

from __future__ import annotations

import wave

from storytime.adapters.tts import MockTTS, PiperTTS
from storytime.artifacts import PayloadKind, from_json
from storytime.dto import StageInput, StageStatus
from storytime.events import EventType
from storytime.runner import RunnerContext
from storytime.stages import IngestStage, SynthesizeStage

RUN_ID = "01TESTSYNTH000000000000001"


def _ingest_artifact(ctx: RunnerContext, manifest_path: str) -> str:
    """Run ingest and return the text.plain artifact key."""
    result = IngestStage().run(
        ctx,
        StageInput(
            pipeline_run_id=RUN_ID,
            stage_name="ingest",
            run_dir=RUN_ID,
            params={"manifest_path": manifest_path},
        ),
    )
    assert result.status is StageStatus.SUCCEEDED
    return result.output_artifacts[0]


def _synthesize_input(text_artifact: str) -> StageInput:
    return StageInput(
        pipeline_run_id=RUN_ID,
        stage_name="synthesize",
        run_dir=RUN_ID,
        input_artifacts=(text_artifact,),
    )


def test_synthesize_produces_a_real_wav(
    runtime_context: RunnerContext, slice_workspace
) -> None:
    text_artifact = _ingest_artifact(
        runtime_context, str(slice_workspace.manifest_path)
    )
    result = SynthesizeStage(MockTTS()).run(
        runtime_context, _synthesize_input(text_artifact)
    )

    assert result.status is StageStatus.SUCCEEDED
    envelope = from_json(
        runtime_context.storage.read_text(result.output_artifacts[0])
    )
    assert envelope.payload_kind is PayloadKind.AUDIO_WAV
    assert envelope.depends_on[0].stage == "ingest"

    # The payload is a genuine, readable WAV file on disk.
    wav_path = runtime_context.storage.resolve(envelope.payload_path)
    assert wav_path.is_file()
    with wave.open(str(wav_path), "rb") as handle:
        assert handle.getnframes() > 0
        assert handle.getnchannels() == 1

    event_types = {event.event_type for event in result.events}
    assert {EventType.SYNTHESIS_STARTED, EventType.SYNTHESIS_COMPLETED} <= event_types


def test_synthesize_without_input_artifact_fails(
    runtime_context: RunnerContext,
) -> None:
    result = SynthesizeStage(MockTTS()).run(
        runtime_context,
        StageInput(
            pipeline_run_id=RUN_ID, stage_name="synthesize", run_dir=RUN_ID
        ),
    )
    assert result.status is StageStatus.FAILED
    assert result.error_kind == "MissingInputArtifact"


def test_synthesize_with_stub_tts_fails_cleanly(
    runtime_context: RunnerContext, slice_workspace
) -> None:
    text_artifact = _ingest_artifact(
        runtime_context, str(slice_workspace.manifest_path)
    )
    result = SynthesizeStage(PiperTTS()).run(
        runtime_context, _synthesize_input(text_artifact)
    )

    assert result.status is StageStatus.FAILED
    assert result.error_kind == "TTSUnavailable"
    assert any(
        e.event_type is EventType.SYNTHESIS_FAILED for e in result.events
    )
