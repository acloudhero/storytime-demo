"""Assemble stage — packages the WAV into podcast-ready MP3 + episode metadata.

ARCH-LOCK: Stage Boundary + ffmpeg fail-fast
DO NOT REFACTOR: This stage owns MP3 encoding (hard decision 7). When ffmpeg
is unavailable it returns an explicit FAILED result with actionable guidance;
it must never degrade silently to a non-MP3 output. The Mp3Encoder is a
constructor-injected dependency (Round 5 clarification A1).
Rationale: Hard decision 7 and Round 7 prerequisite correction 5.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from storytime.adapters.telemetry.attributes import (
    ATTR_ARTIFACT_KIND,
    ATTR_AUDIO_FORMAT,
)
from storytime.artifacts import (
    ARTIFACT_VERSION,
    ArtifactDependency,
    ArtifactEnvelope,
    ArtifactEnvelopeError,
    PayloadKind,
    TraceContext,
    from_json,
    to_json,
)
from storytime.dto import StageInput, StageResult, StateUpdate
from storytime.events import EventType, PipelineEvent
from storytime.stages.encode import (
    FFMPEG_GUIDANCE,
    FfmpegUnavailableError,
    Mp3EncodeError,
    Mp3Encoder,
)
from storytime.util.hashing import sha256_text
from storytime.util.ids import new_ulid

if TYPE_CHECKING:
    from datetime import datetime

    from storytime.runner.context import RunnerContext


class AssembleStage:
    """Encodes the WAV to MP3 and writes the episode.metadata artifact."""

    name = "assemble"

    def __init__(
        self, encoder: Mp3Encoder, *, episode_title: str, episode_description: str
    ) -> None:
        # ARCH-LOCK A1: the MP3 encoder is injected into the stage.
        self._encoder = encoder
        self._episode_title = episode_title
        self._episode_description = episode_description

    def run(self, ctx: RunnerContext, stage_input: StageInput) -> StageResult:
        """Encode the upstream WAV to MP3 and emit MP3 + metadata artifacts."""
        run_id = stage_input.pipeline_run_id
        now = ctx.clock.now()

        if not stage_input.input_artifacts:
            return self._fail(
                run_id, now, "MissingInputArtifact",
                "assemble requires the audio.wav artifact from synthesize",
            )

        try:
            wav_envelope = from_json(
                ctx.storage.read_text(stage_input.input_artifacts[0])
            )
        except (ArtifactEnvelopeError, FileNotFoundError, OSError) as exc:
            return self._fail(
                run_id, now, "ArtifactUnreadable",
                f"cannot read upstream WAV artifact: {exc}",
            )

        # ARCH-LOCK: ffmpeg fail-fast. Absence is an explicit, non-silent error.
        if not self._encoder.is_available():
            return self._fail(
                run_id, now, "FfmpegUnavailable", FFMPEG_GUIDANCE,
                reason="ffmpeg_unavailable",
            )

        wav_path = ctx.storage.resolve(wav_envelope.payload_path)
        mp3_key = f"{stage_input.run_dir}/artifacts/assemble/episode.mp3"
        try:
            encode_result = self._encoder.encode(wav_path, ctx.storage.resolve(mp3_key))
        except FfmpegUnavailableError as exc:
            return self._fail(
                run_id, now, "FfmpegUnavailable", str(exc),
                reason="ffmpeg_unavailable",
            )
        except Mp3EncodeError as exc:
            return self._fail(
                run_id, now, "Mp3EncodeFailed", str(exc), reason="encode_failed",
            )

        duration_seconds = float(wav_envelope.producer.get("duration_seconds", "0") or 0)
        episode_guid = new_ulid()

        mp3_envelope_key = f"{mp3_key}.json"
        mp3_envelope = ArtifactEnvelope(
            artifact_version=ARTIFACT_VERSION,
            pipeline_run_id=run_id,
            stage=self.name,
            produced_at=now.isoformat(),
            payload_kind=PayloadKind.AUDIO_MP3,
            payload_path=mp3_key,
            payload_sha256=encode_result.mp3_sha256,
            payload_bytes=encode_result.mp3_bytes,
            depends_on=(
                ArtifactDependency(
                    stage="synthesize", payload_sha256=wav_envelope.payload_sha256
                ),
            ),
            trace_context=TraceContext(traceparent=stage_input.inbound_traceparent),
            producer={
                "encoder": self._encoder.name,
                "episode_guid": episode_guid,
                "duration_seconds": f"{duration_seconds:.3f}",
            },
        )
        ctx.storage.write_text(mp3_envelope_key, to_json(mp3_envelope))

        metadata = {
            "episode_guid": episode_guid,
            "title": self._episode_title,
            "description": self._episode_description,
            "duration_seconds": round(duration_seconds, 3),
            "audio_payload_path": mp3_key,
            "audio_sha256": encode_result.mp3_sha256,
            "audio_bytes": encode_result.mp3_bytes,
        }
        metadata_text = json.dumps(metadata, sort_keys=True, indent=2)
        metadata_key = f"{stage_input.run_dir}/artifacts/assemble/episode.metadata.json"
        ctx.storage.write_text(metadata_key, metadata_text)

        metadata_envelope_key = (
            f"{stage_input.run_dir}/artifacts/assemble/episode.metadata.envelope.json"
        )
        metadata_envelope = ArtifactEnvelope(
            artifact_version=ARTIFACT_VERSION,
            pipeline_run_id=run_id,
            stage=self.name,
            produced_at=now.isoformat(),
            payload_kind=PayloadKind.EPISODE_METADATA,
            payload_path=metadata_key,
            payload_sha256=sha256_text(metadata_text),
            payload_bytes=len(metadata_text.encode("utf-8")),
            depends_on=(
                ArtifactDependency(
                    stage="assemble", payload_sha256=encode_result.mp3_sha256
                ),
            ),
            trace_context=TraceContext(traceparent=stage_input.inbound_traceparent),
            producer={"episode_guid": episode_guid},
        )
        ctx.storage.write_text(metadata_envelope_key, to_json(metadata_envelope))

        completed = PipelineEvent(
            event_type=EventType.ASSEMBLY_COMPLETED,
            pipeline_run_id=run_id,
            occurred_at=now,
            stage_name=self.name,
            payload={
                "episode_guid": episode_guid,
                "audio_sha256": encode_result.mp3_sha256,
                "audio_bytes": encode_result.mp3_bytes,
                "duration_seconds": round(duration_seconds, 3),
            },
        )
        return StageResult.succeeded(
            StateUpdate(run_status="running", current_stage=self.name),
            events=(completed,),
            output_artifacts=(mp3_envelope_key, metadata_envelope_key),
            span_attributes={
                ATTR_ARTIFACT_KIND: str(PayloadKind.AUDIO_MP3),
                ATTR_AUDIO_FORMAT: "mp3",
            },
        )

    def _fail(
        self,
        run_id: str,
        occurred_at: datetime,
        kind: str,
        message: str,
        *,
        reason: str | None = None,
    ) -> StageResult:
        """Build a FAILED result with a RUN_FAILED forensic event."""
        payload: dict[str, object] = {"error_kind": kind, "stage": self.name}
        if reason is not None:
            payload["reason"] = reason
        event = PipelineEvent(
            event_type=EventType.RUN_FAILED,
            pipeline_run_id=run_id,
            occurred_at=occurred_at,
            stage_name=self.name,
            payload=payload,
        )
        return StageResult.failed(
            kind,
            message,
            events=(event,),
            state_update=StateUpdate(run_status="failed", current_stage=self.name),
        )
