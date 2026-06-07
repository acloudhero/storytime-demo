"""Synthesize stage — turns the ingested text into a WAV audio artifact.

ARCH-LOCK: Stage Boundary + TTS adapter is constructor-injected
DO NOT REFACTOR: The TTS adapter is a constructor dependency of this stage
(Round 5 clarification A1), never a field of RunnerContext. The stage emits
WAV only; MP3 encoding belongs to the assemble stage (hard decision 7).
Rationale: Architecture Baseline sections 8-9, 13 and hard decisions 7-8.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from storytime.adapters.telemetry.attributes import (
    ATTR_ARTIFACT_KIND,
    ATTR_AUDIO_FORMAT,
    ATTR_TTS_ADAPTER,
)
from storytime.adapters.tts import TTSAdapter, TTSUnavailableError
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
from storytime.governance import require_approved_envelope
from storytime.util.hashing import sha256_text

if TYPE_CHECKING:
    from datetime import datetime

    from storytime.runner.context import RunnerContext


class SynthesizeStage:
    """Synthesizes a WAV from the upstream text.plain artifact."""

    name = "synthesize"

    def __init__(self, tts: TTSAdapter) -> None:
        # ARCH-LOCK A1: the chosen TTS engine is injected into the stage.
        self._tts = tts

    def run(self, ctx: RunnerContext, stage_input: StageInput) -> StageResult:
        """Read the text artifact, synthesize a WAV, and emit a WAV artifact."""
        run_id = stage_input.pipeline_run_id
        now = ctx.clock.now()

        if not stage_input.input_artifacts:
            return self._fail(
                run_id, now, "MissingInputArtifact",
                "synthesize requires the text.plain artifact from ingest",
            )

        text_envelope_key = stage_input.input_artifacts[0]
        try:
            text_envelope = from_json(ctx.storage.read_text(text_envelope_key))
        except (ArtifactEnvelopeError, FileNotFoundError, OSError) as exc:
            return self._fail(
                run_id, now, "ArtifactUnreadable",
                f"cannot read upstream text artifact {text_envelope_key}: {exc}",
            )

        text = ctx.storage.read_text(text_envelope.payload_path)
        if sha256_text(text) != text_envelope.payload_sha256:
            return self._fail(
                run_id, now, "ArtifactIntegrityError",
                "text payload digest does not match its envelope payload_sha256",
            )

        # Phase 9B (Architecture Baseline §24.6): the fail-closed governance
        # gate, hard-blocking BEFORE any TTS. Synthesis is the first
        # externally-sensitive stage; the durable Trust Envelope must say
        # APPROVED. A BLOCKED / REJECTED / NEEDS_REVIEW / UNKNOWN decision, or
        # a missing, malformed, or unverifiable envelope, fails closed here —
        # an APPROVED check earlier (at ingest) never licenses skipping this.
        gate = require_approved_envelope(ctx.storage, stage_input.run_dir)
        if not gate.passed:
            return self._fail(
                run_id, now, "GovernanceGateBlocked",
                f"governance gate blocked synthesis before TTS: {gate.reason}",
            )

        wav_key = f"{stage_input.run_dir}/artifacts/synthesize/audio.wav"
        wav_path = ctx.storage.resolve(wav_key)

        started = PipelineEvent(
            event_type=EventType.SYNTHESIS_STARTED,
            pipeline_run_id=run_id,
            occurred_at=now,
            stage_name=self.name,
            payload={"tts_name": self._tts.name, "tts_version": self._tts.version},
        )

        try:
            tts_result = self._tts.synthesize(text, out_path=wav_path)
        except TTSUnavailableError as exc:
            failed_event = PipelineEvent(
                event_type=EventType.SYNTHESIS_FAILED,
                pipeline_run_id=run_id,
                occurred_at=now,
                stage_name=self.name,
                payload={"error": str(exc), "tts_name": self._tts.name},
            )
            return StageResult.failed(
                "TTSUnavailable",
                str(exc),
                events=(started, failed_event),
                state_update=StateUpdate(run_status="failed", current_stage=self.name),
            )

        envelope_key = f"{stage_input.run_dir}/artifacts/synthesize/audio.wav.json"
        envelope = ArtifactEnvelope(
            artifact_version=ARTIFACT_VERSION,
            pipeline_run_id=run_id,
            stage=self.name,
            produced_at=now.isoformat(),
            payload_kind=PayloadKind.AUDIO_WAV,
            payload_path=wav_key,
            payload_sha256=tts_result.audio_sha256,
            payload_bytes=tts_result.audio_bytes,
            depends_on=(
                ArtifactDependency(
                    stage="ingest", payload_sha256=text_envelope.payload_sha256
                ),
            ),
            trace_context=TraceContext(traceparent=stage_input.inbound_traceparent),
            producer={
                "tts_name": self._tts.name,
                "tts_version": self._tts.version,
                "sample_rate_hz": str(tts_result.sample_rate_hz),
                "channels": str(tts_result.channels),
                "duration_seconds": f"{tts_result.duration_seconds:.3f}",
                "title": text_envelope.producer.get("title", ""),
                "author": text_envelope.producer.get("author", ""),
            },
        )
        ctx.storage.write_text(envelope_key, to_json(envelope))

        completed = PipelineEvent(
            event_type=EventType.SYNTHESIS_COMPLETED,
            pipeline_run_id=run_id,
            occurred_at=now,
            stage_name=self.name,
            payload={
                "audio_sha256": tts_result.audio_sha256,
                "audio_bytes": tts_result.audio_bytes,
                "duration_seconds": round(tts_result.duration_seconds, 3),
            },
        )
        return StageResult.succeeded(
            StateUpdate(run_status="running", current_stage=self.name),
            events=(started, completed),
            output_artifacts=(envelope_key,),
            span_attributes={
                ATTR_ARTIFACT_KIND: str(PayloadKind.AUDIO_WAV),
                ATTR_AUDIO_FORMAT: "wav",
                ATTR_TTS_ADAPTER: self._tts.name,
            },
        )

    def _fail(
        self, run_id: str, occurred_at: datetime, kind: str, message: str
    ) -> StageResult:
        """Build a FAILED result with a RUN_FAILED forensic event."""
        event = PipelineEvent(
            event_type=EventType.RUN_FAILED,
            pipeline_run_id=run_id,
            occurred_at=occurred_at,
            stage_name=self.name,
            payload={"error_kind": kind, "stage": self.name},
        )
        return StageResult.failed(
            kind,
            message,
            events=(event,),
            state_update=StateUpdate(run_status="failed", current_stage=self.name),
        )
