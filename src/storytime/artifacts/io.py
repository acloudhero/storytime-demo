"""Artifact envelope serialization, deserialization, and compatibility reading.

ARCH-LOCK: Artifact Compatibility Reader
DO NOT REFACTOR: from_json must reject any artifact_version it does not
explicitly support. Do not "best effort" parse unknown versions.
Rationale: Architecture Baseline section 7. A versioned envelope is only safe
if unknown versions fail loudly instead of being silently misread.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from storytime.artifacts.envelope import (
    ArtifactDependency,
    ArtifactEnvelope,
    PayloadKind,
    TraceContext,
)

# The set of envelope versions this build of StoryTime can read.
SUPPORTED_ARTIFACT_VERSIONS: frozenset[int] = frozenset({1})


class ArtifactEnvelopeError(ValueError):
    """Raised when an artifact envelope is structurally invalid."""


class UnsupportedArtifactVersionError(ArtifactEnvelopeError):
    """Raised when an envelope declares an artifact_version we cannot read."""


def to_dict(envelope: ArtifactEnvelope) -> dict[str, Any]:
    """Render *envelope* as a plain JSON-ready dictionary."""
    return {
        "artifact_version": envelope.artifact_version,
        "pipeline_run_id": envelope.pipeline_run_id,
        "stage": envelope.stage,
        "produced_at": envelope.produced_at,
        "payload_kind": str(envelope.payload_kind),
        "payload_path": envelope.payload_path,
        "payload_sha256": envelope.payload_sha256,
        "payload_bytes": envelope.payload_bytes,
        "depends_on": [
            {"stage": dep.stage, "payload_sha256": dep.payload_sha256}
            for dep in envelope.depends_on
        ],
        "trace_context": {
            "traceparent": envelope.trace_context.traceparent,
            "tracestate": envelope.trace_context.tracestate,
        },
        "producer": dict(envelope.producer),
    }


def to_json(envelope: ArtifactEnvelope) -> str:
    """Serialize *envelope* to an indented JSON string."""
    return json.dumps(to_dict(envelope), indent=2, sort_keys=True)


def _require(mapping: dict[str, Any], key: str) -> Any:
    if key not in mapping:
        raise ArtifactEnvelopeError(f"artifact envelope missing required key: {key!r}")
    return mapping[key]


def _require_str(mapping: dict[str, Any], key: str) -> str:
    value = _require(mapping, key)
    if not isinstance(value, str):
        raise ArtifactEnvelopeError(f"artifact envelope key {key!r} must be a string")
    return value


def _require_int(mapping: dict[str, Any], key: str) -> int:
    value = _require(mapping, key)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ArtifactEnvelopeError(f"artifact envelope key {key!r} must be an integer")
    return value


def from_json(text: str) -> ArtifactEnvelope:
    """Parse an artifact envelope from JSON, enforcing version compatibility.

    Raises UnsupportedArtifactVersionError if the declared artifact_version is
    not in SUPPORTED_ARTIFACT_VERSIONS, and ArtifactEnvelopeError on any other
    structural problem.
    """
    try:
        raw: Any = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ArtifactEnvelopeError(f"artifact envelope is not valid JSON: {exc}") from exc

    if not isinstance(raw, dict):
        raise ArtifactEnvelopeError("artifact envelope must be a JSON object")

    version = raw.get("artifact_version")
    if not isinstance(version, int) or isinstance(version, bool):
        raise ArtifactEnvelopeError("artifact envelope missing integer artifact_version")
    if version not in SUPPORTED_ARTIFACT_VERSIONS:
        raise UnsupportedArtifactVersionError(
            f"artifact_version {version} is not supported by this build "
            f"(supported: {sorted(SUPPORTED_ARTIFACT_VERSIONS)})"
        )

    kind_raw = _require_str(raw, "payload_kind")
    try:
        payload_kind = PayloadKind(kind_raw)
    except ValueError as exc:
        raise ArtifactEnvelopeError(f"unknown payload_kind: {kind_raw!r}") from exc

    deps_raw = raw.get("depends_on", [])
    if not isinstance(deps_raw, list):
        raise ArtifactEnvelopeError("depends_on must be a list")
    depends_on = tuple(
        ArtifactDependency(
            stage=_require_str(dep, "stage"),
            payload_sha256=_require_str(dep, "payload_sha256"),
        )
        for dep in deps_raw
        if isinstance(dep, dict)
    )

    trace_raw = raw.get("trace_context", {})
    trace_raw = trace_raw if isinstance(trace_raw, dict) else {}
    traceparent = trace_raw.get("traceparent")
    if traceparent is not None and not isinstance(traceparent, str):
        raise ArtifactEnvelopeError("trace_context.traceparent must be a string or null")
    tracestate = trace_raw.get("tracestate", "")
    tracestate = tracestate if isinstance(tracestate, str) else ""

    producer_raw = raw.get("producer", {})
    producer = {
        str(k): str(v) for k, v in producer_raw.items()
    } if isinstance(producer_raw, dict) else {}

    return ArtifactEnvelope(
        artifact_version=version,
        pipeline_run_id=_require_str(raw, "pipeline_run_id"),
        stage=_require_str(raw, "stage"),
        produced_at=_require_str(raw, "produced_at"),
        payload_kind=payload_kind,
        payload_path=_require_str(raw, "payload_path"),
        payload_sha256=_require_str(raw, "payload_sha256"),
        payload_bytes=_require_int(raw, "payload_bytes"),
        depends_on=depends_on,
        trace_context=TraceContext(traceparent=traceparent, tracestate=tracestate),
        producer=producer,
    )


def write_envelope(envelope: ArtifactEnvelope, path: Path) -> None:
    """Write *envelope* to *path* as JSON, creating parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(to_json(envelope), encoding="utf-8")


def read_envelope(path: Path) -> ArtifactEnvelope:
    """Read and parse an artifact envelope from *path*."""
    return from_json(path.read_text(encoding="utf-8"))
