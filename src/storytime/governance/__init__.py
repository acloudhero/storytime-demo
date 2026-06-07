"""StoryTime governance — the Phase 9B Minimal Trust Envelope implementation.

This package is the concrete artifact and projection of the locked Architecture
Baseline Section 24 (the Phase 9A Governance Baseline amendment). It provides:

* the Trust Envelope model and its canonical §24.8 closed schema;
* serialization of the durable Trust Envelope artifact (the governance source
  of truth — §24.7);
* the local, inspectable blocked-source configuration (§24.9);
* the fail-closed governance gate (§24.6) — only an explicit APPROVED Trust
  Envelope lets a source past the gate before TTS / audio / RSS publishing;
* the static legal-hallucination verification gate (§24.14).

The package performs no legal determination and no model inference: a Trust
Envelope records a human operator's decision, transcribed from the source
manifest (§24.2 / §24.3).
"""

from storytime.governance.blocked_sources import (
    BlockedSource,
    BlockedSourceConfigError,
    load_blocked_sources,
    match_blocked_source,
)
from storytime.governance.gate import (
    GovernanceGateResult,
    evaluate_envelope,
    require_approved_envelope,
    trust_envelope_from_manifest,
)
from storytime.governance.io import (
    SUPPORTED_TRUST_ENVELOPE_VERSIONS,
    TRUST_ENVELOPE_FILENAME,
    TrustEnvelopeError,
    UnsupportedTrustEnvelopeVersionError,
    from_json,
    read_trust_envelope,
    to_dict,
    to_json,
    trust_envelope_key,
    validate_trust_envelope,
    write_trust_envelope,
)
from storytime.governance.legal_terms import (
    FORBIDDEN_LEGAL_TERMS,
    GOVERNANCE_DOC_ALLOWLIST,
    LegalTermViolation,
    scan_for_forbidden_terms,
)
from storytime.governance.trust_envelope import (
    TRUST_ENVELOPE_SCHEMA_VERSION,
    GovernanceDecision,
    LicenseType,
    TrustEnvelope,
)

__all__ = [
    "FORBIDDEN_LEGAL_TERMS",
    "GOVERNANCE_DOC_ALLOWLIST",
    "SUPPORTED_TRUST_ENVELOPE_VERSIONS",
    "TRUST_ENVELOPE_FILENAME",
    "TRUST_ENVELOPE_SCHEMA_VERSION",
    "BlockedSource",
    "BlockedSourceConfigError",
    "GovernanceDecision",
    "GovernanceGateResult",
    "LegalTermViolation",
    "LicenseType",
    "TrustEnvelope",
    "TrustEnvelopeError",
    "UnsupportedTrustEnvelopeVersionError",
    "evaluate_envelope",
    "from_json",
    "load_blocked_sources",
    "match_blocked_source",
    "read_trust_envelope",
    "require_approved_envelope",
    "scan_for_forbidden_terms",
    "to_dict",
    "to_json",
    "trust_envelope_from_manifest",
    "trust_envelope_key",
    "validate_trust_envelope",
    "write_trust_envelope",
]
