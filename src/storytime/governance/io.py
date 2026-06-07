"""Trust Envelope serialization, deserialization, and compatibility reading.

ARCH-LOCK: Trust Envelope Compatibility Reader
DO NOT REFACTOR: ``from_json`` must validate against the closed §24.8 schema
and reject any ``schema_version`` it does not explicitly support. Do not
"best effort" parse an unknown or malformed envelope — the fail-closed gate
(§24.6) depends on a malformed or unverifiable envelope failing loudly.
Rationale: Architecture Baseline §24.7/§24.8. The durable Trust Envelope
artifact is the governance source of truth; it is only safe if a bad envelope
fails closed instead of being silently misread.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from jsonschema import Draft202012Validator

from storytime.governance.schema import TRUST_ENVELOPE_SCHEMA
from storytime.governance.trust_envelope import (
    TRUST_ENVELOPE_SCHEMA_VERSION,
    GovernanceDecision,
    LicenseType,
    TrustEnvelope,
)

if TYPE_CHECKING:
    from storytime.adapters.storage import StorageAdapter

# The set of Trust Envelope schema versions this build can read. A version
# outside this set fails closed rather than being parsed.
SUPPORTED_TRUST_ENVELOPE_VERSIONS: frozenset[str] = frozenset(
    {TRUST_ENVELOPE_SCHEMA_VERSION}
)

# The durable Trust Envelope artifact's storage key, relative to a run_dir.
# It is a separate durable artifact, deliberately NOT embedded in the
# ArtifactEnvelope (whose shape is ARCH-LOCKed): §24.7 permits the Trust
# Envelope to be "embedded in OR linked from" the artifact-envelope format,
# and a sibling durable file is the minimal, non-invasive linkage.
TRUST_ENVELOPE_FILENAME = "trust-envelope.json"

_VALIDATOR = Draft202012Validator(TRUST_ENVELOPE_SCHEMA)


class TrustEnvelopeError(ValueError):
    """Raised when a Trust Envelope is structurally invalid or unverifiable."""


class UnsupportedTrustEnvelopeVersionError(TrustEnvelopeError):
    """Raised when an envelope declares a schema_version this build cannot read."""


def trust_envelope_key(run_dir: str) -> str:
    """Return the relative storage key of a run's durable Trust Envelope.

    *run_dir* is the run's relative directory (the value threaded through
    ``StageInput.run_dir``). The key is POSIX-relative so a run survives its
    workspace being relocated, exactly like the artifact-envelope keys.
    """
    return f"{run_dir}/governance/{TRUST_ENVELOPE_FILENAME}"


def to_dict(envelope: TrustEnvelope) -> dict[str, Any]:
    """Render *envelope* as a plain JSON-ready dictionary (every §24.8 field)."""
    return {
        "schema_version": envelope.schema_version,
        "source_ref": envelope.source_ref,
        "source_url": envelope.source_url,
        "source_title": envelope.source_title,
        "source_author": envelope.source_author,
        "license_type": str(envelope.license_type),
        "license_url": envelope.license_url,
        "license_evidence_ref": envelope.license_evidence_ref,
        "decision": str(envelope.decision),
        "decision_timestamp": envelope.decision_timestamp,
        "approver_id": envelope.approver_id,
        "allowed_use": envelope.allowed_use,
        "attribution_required": envelope.attribution_required,
        "commercial_use_allowed": envelope.commercial_use_allowed,
        "blocked_reason": envelope.blocked_reason,
        "governance_notes": envelope.governance_notes,
        "review_context_summary": envelope.review_context_summary,
        "artifact_hash_refs": list(envelope.artifact_hash_refs),
    }


def to_json(envelope: TrustEnvelope) -> str:
    """Serialize *envelope* to an indented, sorted JSON string."""
    return json.dumps(to_dict(envelope), indent=2, sort_keys=True)


def validate_trust_envelope(data: dict[str, Any]) -> None:
    """Validate *data* against the closed §24.8 schema.

    Raises TrustEnvelopeError listing every problem. Because the schema sets
    ``additionalProperties: false``, any unknown field is an error.
    """
    errors = sorted(_VALIDATOR.iter_errors(data), key=lambda e: list(e.absolute_path))
    if errors:
        messages = [
            f"{'/'.join(str(p) for p in err.absolute_path) or '<root>'}: {err.message}"
            for err in errors
        ]
        raise TrustEnvelopeError(
            "trust envelope failed schema validation: " + "; ".join(messages)
        )


def from_json(text: str) -> TrustEnvelope:
    """Parse and fully validate a Trust Envelope from JSON.

    Enforces, in order: valid JSON; a JSON object; a supported
    ``schema_version``; the closed §24.8 schema. Any failure raises
    TrustEnvelopeError (or UnsupportedTrustEnvelopeVersionError) so a malformed
    or unverifiable envelope fails closed.
    """
    try:
        raw: Any = json.loads(text)
    except json.JSONDecodeError as exc:
        raise TrustEnvelopeError(f"trust envelope is not valid JSON: {exc}") from exc

    if not isinstance(raw, dict):
        raise TrustEnvelopeError("trust envelope must be a JSON object")

    version = raw.get("schema_version")
    if not isinstance(version, str) or not version:
        raise TrustEnvelopeError(
            "trust envelope is missing a non-empty string schema_version"
        )
    if version not in SUPPORTED_TRUST_ENVELOPE_VERSIONS:
        raise UnsupportedTrustEnvelopeVersionError(
            f"trust envelope schema_version {version!r} is not supported by this "
            f"build (supported: {sorted(SUPPORTED_TRUST_ENVELOPE_VERSIONS)})"
        )

    validate_trust_envelope(raw)

    refs_raw = raw["artifact_hash_refs"]
    artifact_hash_refs = tuple(str(ref) for ref in refs_raw)

    return TrustEnvelope(
        schema_version=raw["schema_version"],
        source_ref=raw["source_ref"],
        source_url=raw["source_url"],
        source_title=raw["source_title"],
        source_author=raw["source_author"],
        license_type=LicenseType(raw["license_type"]),
        license_url=raw["license_url"],
        license_evidence_ref=raw["license_evidence_ref"],
        decision=GovernanceDecision(raw["decision"]),
        decision_timestamp=raw["decision_timestamp"],
        approver_id=raw["approver_id"],
        allowed_use=raw["allowed_use"],
        attribution_required=raw["attribution_required"],
        commercial_use_allowed=raw["commercial_use_allowed"],
        blocked_reason=raw["blocked_reason"],
        governance_notes=raw["governance_notes"],
        review_context_summary=raw["review_context_summary"],
        artifact_hash_refs=artifact_hash_refs,
    )


def write_trust_envelope(
    storage: StorageAdapter, run_dir: str, envelope: TrustEnvelope
) -> str:
    """Write *envelope* as the run's durable Trust Envelope artifact.

    Returns the relative storage key written. The durable artifact is the
    governance source of truth (§24.7); the SQLite projection is rebuilt from
    it and never overrides it.
    """
    key = trust_envelope_key(run_dir)
    storage.write_text(key, to_json(envelope))
    return key


def read_trust_envelope(storage: StorageAdapter, run_dir: str) -> TrustEnvelope:
    """Read and validate a run's durable Trust Envelope artifact.

    Raises TrustEnvelopeError if the artifact is missing, unreadable, or
    invalid — the caller (the fail-closed gate) treats every such failure as a
    governance failure.
    """
    key = trust_envelope_key(run_dir)
    try:
        text = storage.read_text(key)
    except (FileNotFoundError, OSError) as exc:
        raise TrustEnvelopeError(
            f"trust envelope artifact is missing or unreadable: {key!r} ({exc})"
        ) from exc
    return from_json(text)
