"""Inter-stage artifact envelope: model and versioned (de)serialization."""

from storytime.artifacts.envelope import (
    ARTIFACT_VERSION,
    ArtifactDependency,
    ArtifactEnvelope,
    PayloadKind,
    TraceContext,
)
from storytime.artifacts.io import (
    SUPPORTED_ARTIFACT_VERSIONS,
    ArtifactEnvelopeError,
    UnsupportedArtifactVersionError,
    from_json,
    read_envelope,
    to_json,
    write_envelope,
)

__all__ = [
    "ARTIFACT_VERSION",
    "SUPPORTED_ARTIFACT_VERSIONS",
    "ArtifactDependency",
    "ArtifactEnvelope",
    "ArtifactEnvelopeError",
    "PayloadKind",
    "TraceContext",
    "UnsupportedArtifactVersionError",
    "from_json",
    "read_envelope",
    "to_json",
    "write_envelope",
]
