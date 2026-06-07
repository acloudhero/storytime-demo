"""W3C trace-context helpers — pure string parsing, no OpenTelemetry import.

ARCH-LOCK: Telemetry Import Boundary (see storytime.adapters.telemetry.base)
DO NOT REFACTOR: This module parses and formats the W3C ``traceparent`` header
as plain strings. It deliberately does NOT import opentelemetry, so it is safe
to use anywhere the serializable trace context must be reasoned about (the
artifact envelope, DTOs, the runner) without coupling those modules to the
OpenTelemetry SDK. The SDK-level work — minting span contexts, creating Links —
stays in storytime.adapters.telemetry.otel, the sole OpenTelemetry module.

A ``traceparent`` is the W3C Trace Context version-00 string::

    <version>-<trace-id>-<parent-id>-<trace-flags>
    00       -32 hex     -16 hex     -2 hex

It is the *serializable* shape of trace context. It is a VIEW identifier: the
durable correlation key remains ``pipeline_run_id``. A ``traceparent`` may be
absent (None) whenever telemetry is disabled — the pipeline still works.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# W3C Trace Context, version 00. Only this version is emitted/accepted here.
_TRACEPARENT_VERSION = "00"
_INVALID_TRACE_ID = "0" * 32
_INVALID_SPAN_ID = "0" * 16
_TRACEPARENT_RE = re.compile(
    r"^(?P<version>[0-9a-f]{2})-"
    r"(?P<trace_id>[0-9a-f]{32})-"
    r"(?P<span_id>[0-9a-f]{16})-"
    r"(?P<flags>[0-9a-f]{2})$"
)


@dataclass(frozen=True, slots=True)
class ParsedTraceparent:
    """A W3C traceparent decomposed into its (lower-case hex) fields."""

    version: str
    trace_id: str
    span_id: str
    flags: str

    @property
    def sampled(self) -> bool:
        """True if the trace-flags mark the trace as sampled (bit 0 set)."""
        return (int(self.flags, 16) & 0x01) == 0x01


def format_traceparent(trace_id: str, span_id: str, *, sampled: bool = True) -> str:
    """Build a W3C version-00 traceparent from a *trace_id* and *span_id*.

    *trace_id* must be 32 hex chars; *span_id* 16 hex chars. Raises ValueError
    on a malformed or all-zero identifier so a bad traceparent never silently
    enters an artifact envelope.
    """
    trace_id = trace_id.lower()
    span_id = span_id.lower()
    if len(trace_id) != 32 or not re.fullmatch(r"[0-9a-f]{32}", trace_id):
        raise ValueError(f"trace_id must be 32 hex characters, got {trace_id!r}")
    if len(span_id) != 16 or not re.fullmatch(r"[0-9a-f]{16}", span_id):
        raise ValueError(f"span_id must be 16 hex characters, got {span_id!r}")
    if trace_id == _INVALID_TRACE_ID:
        raise ValueError("trace_id must not be all zeros")
    if span_id == _INVALID_SPAN_ID:
        raise ValueError("span_id must not be all zeros")
    flags = "01" if sampled else "00"
    return f"{_TRACEPARENT_VERSION}-{trace_id}-{span_id}-{flags}"


def parse_traceparent(traceparent: str | None) -> ParsedTraceparent | None:
    """Parse a W3C *traceparent*, returning None when it is absent or invalid.

    Validity follows the W3C rules this project relies on: the string matches
    the version-00 grammar and neither the trace-id nor the span-id is the
    all-zero sentinel. Returning None (rather than raising) lets callers treat
    "no usable parent" uniformly with "telemetry disabled".
    """
    if not traceparent:
        return None
    match = _TRACEPARENT_RE.match(traceparent.strip().lower())
    if match is None:
        return None
    trace_id = match.group("trace_id")
    span_id = match.group("span_id")
    if trace_id == _INVALID_TRACE_ID or span_id == _INVALID_SPAN_ID:
        return None
    return ParsedTraceparent(
        version=match.group("version"),
        trace_id=trace_id,
        span_id=span_id,
        flags=match.group("flags"),
    )


def is_valid_traceparent(traceparent: str | None) -> bool:
    """True if *traceparent* is a usable W3C version-00 traceparent."""
    return parse_traceparent(traceparent) is not None


def trace_id_of(traceparent: str | None) -> str | None:
    """Return the trace-id of *traceparent*, or None if it is absent/invalid."""
    parsed = parse_traceparent(traceparent)
    return parsed.trace_id if parsed is not None else None


__all__ = [
    "ParsedTraceparent",
    "format_traceparent",
    "is_valid_traceparent",
    "parse_traceparent",
    "trace_id_of",
]
