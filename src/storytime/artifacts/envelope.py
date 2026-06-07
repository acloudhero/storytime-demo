"""Inter-stage artifact envelope model.

ARCH-LOCK: Artifact Envelope Contract
DO NOT REFACTOR: The envelope is the inter-stage contract. Do not pass stage
outputs as bare dicts or in-memory objects between stages. Do not change the
envelope's shape without bumping ARTIFACT_VERSION and extending the
compatibility reader in storytime.artifacts.io.
Rationale: Hard decisions 3 and 4 of the Architecture Baseline. Stages
communicate only through hashed, versioned artifacts on disk; the envelope
carries the W3C traceparent so trace context survives process boundaries.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum

# ARCH-LOCK: Artifact Version
# DO NOT REFACTOR: Increment, never repurpose. Every envelope records the
# version it was written with so old artifacts remain readable.
ARTIFACT_VERSION = 1


class PayloadKind(StrEnum):
    """The kinds of payload an artifact envelope may describe."""

    TEXT_PLAIN = "text.plain"
    AUDIO_WAV = "audio.wav"
    AUDIO_MP3 = "audio.mp3"
    EPISODE_METADATA = "episode.metadata"


@dataclass(frozen=True, slots=True)
class TraceContext:
    """W3C trace context carried across a stage boundary.

    traceparent may be None when telemetry is disabled (NoopTelemetry); the
    pipeline still works because pipeline_run_id is the durable correlation key.
    """

    traceparent: str | None = None
    tracestate: str = ""


@dataclass(frozen=True, slots=True)
class ArtifactDependency:
    """A reference to an upstream artifact this one was derived from."""

    stage: str
    payload_sha256: str


@dataclass(frozen=True, slots=True)
class ArtifactEnvelope:
    """Describes one stage output: its payload, integrity, and provenance."""

    artifact_version: int
    pipeline_run_id: str
    stage: str
    produced_at: str
    payload_kind: PayloadKind
    payload_path: str
    payload_sha256: str
    payload_bytes: int
    depends_on: tuple[ArtifactDependency, ...] = ()
    trace_context: TraceContext = field(default_factory=TraceContext)
    producer: Mapping[str, str] = field(default_factory=dict)
