"""Trust Envelope model — the durable governance record for a source.

ARCH-LOCK: Trust Envelope is governance law, not a legal opinion
DO NOT REFACTOR: The Trust Envelope is the concrete artifact of the locked
Architecture Baseline Section 24 (Phase 9A governance amendment). It records a
*human operator's* licensing decision — "operator X decided Y about source Z,
for reason R, at time T". It is an audit artifact. It does NOT assert legal
truth, and StoryTime never infers, computes, or certifies legal status from it
(Section 24.2 / 24.3). The field set and the two enum value sets below are the
canonical §24.8 minimum schema; widening either requires a new
TRUST_ENVELOPE_SCHEMA_VERSION and a documented amendment.

This module is pure data. It imports nothing from StoryTime; the licensing
*decision* is made by a human and merely transcribed here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

# The Trust Envelope schema version. Bump (never repurpose) when the field set
# or an enum value set changes; the compatibility reader in governance.io
# refuses a version it does not recognise rather than silently misreading.
TRUST_ENVELOPE_SCHEMA_VERSION = "1"


class LicenseType(StrEnum):
    """The licence categories StoryTime recognises (Architecture Baseline §24.4/§24.8).

    These describe the operator's recorded understanding of a source's
    licence. ``BLOCKED`` and ``UNKNOWN`` are explicit states, not licences:
    there is deliberately no ``AMBIGUOUS`` value — ambiguity must resolve into
    an explicit decision (§24.4).
    """

    CC0 = "CC0"
    US_PUBLIC_DOMAIN = "US_PUBLIC_DOMAIN"
    EXPLICIT_PERMISSION = "EXPLICIT_PERMISSION"
    LOCAL_TEST_FIXTURE = "LOCAL_TEST_FIXTURE"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class GovernanceDecision(StrEnum):
    """The operator's decision about a source (Architecture Baseline §24.8/§24.15).

    This is the stable, UI-safe status enum Phase 10 builds on. Only
    ``APPROVED`` lets a source past the fail-closed gate (§24.6); every other
    value — and a missing, malformed, or unverifiable envelope — fails closed.
    """

    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    BLOCKED = "BLOCKED"
    NEEDS_REVIEW = "NEEDS_REVIEW"


@dataclass(frozen=True, slots=True)
class TrustEnvelope:
    """A durable governance/audit record for one source's licensing decision.

    The field set is the canonical Architecture Baseline §24.8 minimum schema.
    Required fields have no default; the §24.8 nullable fields default to
    ``None`` and ``artifact_hash_refs`` defaults to the empty tuple.

    ``review_context_summary`` is a short, human-readable justification for the
    operator's decision (e.g. "Verified public-domain text via Project
    Gutenberg reference."). It MUST NOT contain raw story text, full source
    text, narration, or other private content — it is a rationale, not a
    content store (§24.8).
    """

    schema_version: str
    source_ref: str
    license_type: LicenseType
    decision: GovernanceDecision
    decision_timestamp: str
    approver_id: str
    source_url: str | None = None
    source_title: str | None = None
    source_author: str | None = None
    license_url: str | None = None
    license_evidence_ref: str | None = None
    allowed_use: str | None = None
    attribution_required: bool | None = None
    commercial_use_allowed: bool | None = None
    blocked_reason: str | None = None
    governance_notes: str | None = None
    review_context_summary: str | None = None
    artifact_hash_refs: tuple[str, ...] = field(default_factory=tuple)

    @property
    def is_approved(self) -> bool:
        """True only when the operator's decision is APPROVED.

        This is the single predicate the fail-closed gate (§24.6) consults;
        nothing weaker than an explicit APPROVED decision satisfies it.
        """
        return self.decision is GovernanceDecision.APPROVED
