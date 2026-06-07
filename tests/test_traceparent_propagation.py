"""W3C traceparent helpers and artifact-envelope trace-context round-trip.

These tests cover the OTel-free propagation layer
(storytime.adapters.telemetry.propagation) and confirm that an
ArtifactEnvelope carries a traceparent across a JSON serialisation boundary --
the mechanism by which a resumed run recovers the trace context of the run
that produced the artifacts it builds on.
"""

from __future__ import annotations

import pytest

from storytime.adapters.telemetry.propagation import (
    format_traceparent,
    is_valid_traceparent,
    parse_traceparent,
    trace_id_of,
)
from storytime.artifacts import (
    ARTIFACT_VERSION,
    ArtifactEnvelope,
    PayloadKind,
    TraceContext,
    from_json,
    to_json,
)

_TRACE_ID = "0af7651916cd43dd8448eb211c80319c"
_SPAN_ID = "b7ad6b7169203331"


def test_format_traceparent_builds_a_valid_w3c_string() -> None:
    traceparent = format_traceparent(_TRACE_ID, _SPAN_ID, sampled=True)
    assert traceparent == f"00-{_TRACE_ID}-{_SPAN_ID}-01"
    assert is_valid_traceparent(traceparent)


def test_format_then_parse_is_a_round_trip() -> None:
    traceparent = format_traceparent(_TRACE_ID, _SPAN_ID)
    parsed = parse_traceparent(traceparent)
    assert parsed is not None
    assert parsed.trace_id == _TRACE_ID
    assert parsed.span_id == _SPAN_ID
    assert parsed.sampled is True


def test_format_traceparent_rejects_all_zero_and_malformed_ids() -> None:
    with pytest.raises(ValueError):
        format_traceparent("0" * 32, _SPAN_ID)
    with pytest.raises(ValueError):
        format_traceparent(_TRACE_ID, "0" * 16)
    with pytest.raises(ValueError):
        format_traceparent("xyz", _SPAN_ID)


def test_parse_traceparent_treats_absent_and_invalid_uniformly() -> None:
    assert parse_traceparent(None) is None
    assert parse_traceparent("") is None
    assert parse_traceparent("not-a-traceparent") is None
    # All-zero trace id is structurally well-formed but not usable.
    assert parse_traceparent(f"00-{'0' * 32}-{_SPAN_ID}-01") is None


def test_trace_id_of_extracts_the_trace_id_or_none() -> None:
    assert trace_id_of(format_traceparent(_TRACE_ID, _SPAN_ID)) == _TRACE_ID
    assert trace_id_of(None) is None
    assert trace_id_of("garbage") is None


def _envelope(trace_context: TraceContext) -> ArtifactEnvelope:
    return ArtifactEnvelope(
        artifact_version=ARTIFACT_VERSION,
        pipeline_run_id="01JABCDEF0123456789ABCDEFG",
        stage="ingest",
        produced_at="2026-01-01T00:00:00+00:00",
        payload_kind=PayloadKind.TEXT_PLAIN,
        payload_path="run/artifacts/ingest/text.txt",
        payload_sha256="a" * 64,
        payload_bytes=12,
        trace_context=trace_context,
    )


def test_envelope_round_trips_a_traceparent_through_json() -> None:
    traceparent = format_traceparent(_TRACE_ID, _SPAN_ID)
    envelope = _envelope(TraceContext(traceparent=traceparent))
    restored = from_json(to_json(envelope))
    assert restored.trace_context.traceparent == traceparent
    assert trace_id_of(restored.trace_context.traceparent) == _TRACE_ID


def test_envelope_round_trips_an_absent_traceparent_as_none() -> None:
    """Under NoopTelemetry the envelope simply carries no trace context."""
    envelope = _envelope(TraceContext(traceparent=None))
    restored = from_json(to_json(envelope))
    assert restored.trace_context.traceparent is None
