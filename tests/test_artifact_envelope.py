"""Artifact envelope serialization and version-compatibility enforcement."""

from __future__ import annotations

import json

import pytest

from storytime.artifacts import (
    ARTIFACT_VERSION,
    ArtifactDependency,
    ArtifactEnvelope,
    ArtifactEnvelopeError,
    PayloadKind,
    TraceContext,
    UnsupportedArtifactVersionError,
    from_json,
    to_json,
)


def _envelope() -> ArtifactEnvelope:
    return ArtifactEnvelope(
        artifact_version=ARTIFACT_VERSION,
        pipeline_run_id="01JABCDEF0123456789ABCDEFG",
        stage="synthesize",
        produced_at="2026-01-01T00:00:00+00:00",
        payload_kind=PayloadKind.AUDIO_WAV,
        payload_path="runs/r1/audio/episode.wav",
        payload_sha256="c" * 64,
        payload_bytes=44100,
        depends_on=(ArtifactDependency(stage="ingest", payload_sha256="d" * 64),),
        trace_context=TraceContext(traceparent="00-" + "0" * 32 + "-" + "0" * 16 + "-01"),
        producer={"adapter": "mock", "version": "0.2.0"},
    )


def test_round_trip_preserves_all_fields() -> None:
    original = _envelope()
    restored = from_json(to_json(original))
    assert restored == original


def test_unsupported_version_is_rejected() -> None:
    """Negative case: a future artifact_version must fail loudly."""
    payload = json.loads(to_json(_envelope()))
    payload["artifact_version"] = 999
    with pytest.raises(UnsupportedArtifactVersionError):
        from_json(json.dumps(payload))


def test_missing_artifact_version_is_rejected() -> None:
    payload = json.loads(to_json(_envelope()))
    del payload["artifact_version"]
    with pytest.raises(ArtifactEnvelopeError):
        from_json(json.dumps(payload))


def test_non_integer_version_is_rejected() -> None:
    payload = json.loads(to_json(_envelope()))
    payload["artifact_version"] = "1"
    with pytest.raises(ArtifactEnvelopeError):
        from_json(json.dumps(payload))


def test_missing_required_field_is_rejected() -> None:
    payload = json.loads(to_json(_envelope()))
    del payload["payload_sha256"]
    with pytest.raises(ArtifactEnvelopeError):
        from_json(json.dumps(payload))


def test_unknown_payload_kind_is_rejected() -> None:
    payload = json.loads(to_json(_envelope()))
    payload["payload_kind"] = "audio.flac"
    with pytest.raises(ArtifactEnvelopeError):
        from_json(json.dumps(payload))


def test_malformed_json_is_rejected() -> None:
    with pytest.raises(ArtifactEnvelopeError):
        from_json("{not json")


def test_non_object_json_is_rejected() -> None:
    with pytest.raises(ArtifactEnvelopeError):
        from_json("[1, 2, 3]")
