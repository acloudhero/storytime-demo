"""Stage data-transfer contracts: StageInput, StageResult, StateUpdate.

ARCH-LOCK: DTO Boundary
DO NOT REFACTOR: Do not replace StageInput / StageResult / StateUpdate with
shared dicts or a mutable context object. Do not collapse them "for
convenience". Do not place OTel Span objects or live adapter handles in them.
Rationale: Round 3 / Round 5 locked decision. Serializable DTO contracts keep
stages decoupled, keep them unit-testable, preserve trace persistence, and
make a future worker/queue migration mechanical instead of a rewrite.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum

from storytime.events import PipelineEvent


class StageStatus(StrEnum):
    """The outcome discriminant of a stage execution."""

    SUCCEEDED = "succeeded"
    AWAITING_APPROVAL = "awaiting_approval"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class ApprovalIntent:
    """A stage's declarative request to record an operator approval decision."""

    stage_name: str
    decision: str  # "approved" | "rejected"
    operator: str
    notes: str = ""


@dataclass(frozen=True, slots=True)
class PublishedEpisodeIntent:
    """A stage's declarative request to record a published episode.

    Phase 6 (OI-11): feed_version is the monotonic feed-regeneration counter
    the publish stage assigns — len(prior episodes) + 1. It records which
    multi-item feed build first carried this episode. description is the
    episode-level description text, persisted so a later publish can rebuild
    a faithful multi-item feed. Both default so a first publish, and any
    pre-Phase-6 caller, remains valid.
    """

    episode_guid: str
    title: str
    audio_path: str
    audio_bytes: int
    duration_seconds: float
    feed_version: int = 1
    description: str = ""


@dataclass(frozen=True, slots=True)
class TrustEnvelopeIntent:
    """A stage's declarative request to record the Trust Envelope projection.

    Phase 9B (Architecture Baseline §24.7/§24.8). The ingest stage derives a
    Trust Envelope, writes the durable artifact itself, and returns this intent
    so the runner records the SQLite *projection* in the same transaction as
    the stage's events — exactly as ApprovalIntent / PublishedEpisodeIntent do.
    The fields are primitives (no governance domain types) so the DTO layer
    stays free of higher-level imports. ``envelope_key`` is the relative
    storage key of the durable Trust Envelope artifact, which remains the
    governance source of truth.
    """

    source_ref: str
    schema_version: str
    license_type: str
    decision: str
    decision_timestamp: str
    approver_id: str
    envelope_key: str
    blocked_reason: str | None = None


@dataclass(frozen=True, slots=True)
class StateUpdate:
    """A declarative description of state-store mutations a stage requires.

    The stage does NOT write to SQLite. It returns this intent; the runner
    applies it, together with the stage's events, in a single transaction.
    """

    run_status: str | None = None
    current_stage: str | None = None
    approval: ApprovalIntent | None = None
    published_episode: PublishedEpisodeIntent | None = None
    trust_envelope: TrustEnvelopeIntent | None = None


@dataclass(frozen=True, slots=True)
class StageInput:
    """The serializable input to a single stage execution.

    All fields are JSON-serializable on purpose: a stage invocation can be
    persisted and, in a future cloud phase, relocated to a worker. Paths are
    strings, not Path objects, for the same reason.
    """

    pipeline_run_id: str
    stage_name: str
    run_dir: str
    inbound_traceparent: str | None = None
    input_artifacts: tuple[str, ...] = ()
    params: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class StageResult:
    """The result of a single stage execution.

    Carries the outcome status, the declarative StateUpdate, the internal
    events emitted, references (file paths) to artifact envelopes written, and
    span_attributes -- safe, low-cardinality telemetry facts the stage wishes
    to surface on its span.

    span_attributes is a plain str->str mapping (artifact.kind, tts.adapter,
    audio.format, ...). It is JSON-serializable like the rest of the DTO and
    carries NO live OpenTelemetry object: a stage names a telemetry attribute
    without importing OpenTelemetry. The runner hands it to the telemetry
    adapter, which sanitises and attaches it; under NoopTelemetry it is
    ignored. It must never carry raw text, full payloads, or absolute paths.
    """

    status: StageStatus
    state_update: StateUpdate
    events: tuple[PipelineEvent, ...] = ()
    output_artifacts: tuple[str, ...] = ()
    error_kind: str | None = None
    error_message: str | None = None
    span_attributes: Mapping[str, str] = field(default_factory=dict)

    @classmethod
    def succeeded(
        cls,
        state_update: StateUpdate,
        *,
        events: tuple[PipelineEvent, ...] = (),
        output_artifacts: tuple[str, ...] = (),
        span_attributes: Mapping[str, str] | None = None,
    ) -> StageResult:
        """Build a SUCCEEDED result."""
        return cls(
            status=StageStatus.SUCCEEDED,
            state_update=state_update,
            events=events,
            output_artifacts=output_artifacts,
            span_attributes=dict(span_attributes or {}),
        )

    @classmethod
    def awaiting_approval(
        cls,
        state_update: StateUpdate,
        *,
        events: tuple[PipelineEvent, ...] = (),
        span_attributes: Mapping[str, str] | None = None,
    ) -> StageResult:
        """Build an AWAITING_APPROVAL result (stage paused at an operator gate)."""
        return cls(
            status=StageStatus.AWAITING_APPROVAL,
            state_update=state_update,
            events=events,
            span_attributes=dict(span_attributes or {}),
        )

    @classmethod
    def failed(
        cls,
        error_kind: str,
        error_message: str,
        *,
        events: tuple[PipelineEvent, ...] = (),
        state_update: StateUpdate | None = None,
        span_attributes: Mapping[str, str] | None = None,
    ) -> StageResult:
        """Build a FAILED result."""
        return cls(
            status=StageStatus.FAILED,
            state_update=state_update if state_update is not None else StateUpdate(),
            events=events,
            error_kind=error_kind,
            error_message=error_message,
            span_attributes=dict(span_attributes or {}),
        )
