"""Fail-closed governance gate (Architecture Baseline §24.6).

ARCH-LOCK: Fail-closed before TTS / audio / RSS
DO NOT REFACTOR: ``evaluate_envelope`` and ``require_approved_envelope`` are
the load-bearing fail-closed invariant. ONLY an explicit ``APPROVED`` Trust
Envelope passes the gate. A ``BLOCKED`` / ``REJECTED`` / ``NEEDS_REVIEW`` /
``UNKNOWN`` decision, and a missing, malformed, or unverifiable envelope, MUST
fail closed. The gate never "fails open" on absence or error.
Rationale: §24.6 — the pipeline must hard-block before TTS, audio processing,
or RSS publishing unless an APPROVED Trust Envelope exists.

``trust_envelope_from_manifest`` derives a Trust Envelope from a *human-written*
source manifest plus the operator's local blocked-source list. This is honest
transcription of a decision the operator already made (the manifest's licence
field and approval block) plus a deterministic local lookup — it is NOT legal
automation, model inference, or an AI rights determination (§24.2 / §24.3).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from storytime.governance.blocked_sources import BlockedSource, match_blocked_source
from storytime.governance.io import TrustEnvelopeError, read_trust_envelope
from storytime.governance.trust_envelope import (
    TRUST_ENVELOPE_SCHEMA_VERSION,
    GovernanceDecision,
    LicenseType,
    TrustEnvelope,
)

if TYPE_CHECKING:
    from storytime.adapters.storage import StorageAdapter
    from storytime.manifest import SourceManifest

# review_context_summary is a short rationale, never a content store (§24.8).
# The manifest review_notes field is operator-written, but cap it defensively
# so a long note can never turn the rationale into bulk text.
_REVIEW_SUMMARY_MAX_CHARS = 500

# Map the manifest's closed licence enum (CC0-1.0 / PD-US — see the source
# manifest schema) to the Trust Envelope licence-type enum. A manifest licence
# StoryTime does not recognise maps to UNKNOWN, which fails the gate closed.
_MANIFEST_LICENSE_TO_TYPE: dict[str, LicenseType] = {
    "CC0-1.0": LicenseType.CC0,
    "PD-US": LicenseType.US_PUBLIC_DOMAIN,
}


@dataclass(frozen=True, slots=True)
class GovernanceGateResult:
    """The outcome of evaluating the fail-closed governance gate.

    ``passed`` is True only for an explicit APPROVED envelope. ``decision`` is
    the recorded decision when an envelope was read (``None`` when none could
    be read at all). ``reason`` is a short, operator-facing explanation safe to
    surface in a stage failure message and an event payload — it carries no
    raw source text, notes, or review summary (§24.12).
    """

    passed: bool
    decision: GovernanceDecision | None
    reason: str


def evaluate_envelope(
    envelope: TrustEnvelope | None, *, error: str | None = None
) -> GovernanceGateResult:
    """Evaluate a (possibly absent) Trust Envelope against the §24.6 gate.

    *envelope* is the parsed Trust Envelope, or ``None`` when none could be
    obtained; *error* carries the reason it could not be obtained (missing,
    malformed, unverifiable). Only an explicit APPROVED envelope passes; every
    other state fails closed.
    """
    if envelope is None:
        return GovernanceGateResult(
            passed=False,
            decision=None,
            reason=error or "no trust envelope is present for this source",
        )
    if envelope.is_approved:
        return GovernanceGateResult(
            passed=True,
            decision=envelope.decision,
            reason="source has an APPROVED trust envelope",
        )
    detail = f" ({envelope.blocked_reason})" if envelope.blocked_reason else ""
    return GovernanceGateResult(
        passed=False,
        decision=envelope.decision,
        reason=(
            f"trust envelope decision is {envelope.decision} (not APPROVED); "
            f"the pipeline fails closed{detail}"
        ),
    )


def require_approved_envelope(
    storage: StorageAdapter, run_dir: str
) -> GovernanceGateResult:
    """Load a run's durable Trust Envelope and evaluate the fail-closed gate.

    This is the hard block the TTS (synthesize) and RSS (publish) stages call
    before doing externally sensitive work. A missing, malformed, or
    unverifiable durable envelope is caught here and fails closed — the durable
    artifact is the governance source of truth (§24.7), so if it cannot be read
    and verified, the source is not approved.
    """
    try:
        envelope = read_trust_envelope(storage, run_dir)
    except TrustEnvelopeError as exc:
        return evaluate_envelope(None, error=str(exc))
    return evaluate_envelope(envelope)


def _bounded(text: str) -> str:
    """Return *text* trimmed to the review-summary cap, with an ellipsis if cut."""
    text = text.strip()
    if len(text) <= _REVIEW_SUMMARY_MAX_CHARS:
        return text
    return text[: _REVIEW_SUMMARY_MAX_CHARS - 1].rstrip() + "\u2026"


def trust_envelope_from_manifest(
    manifest: SourceManifest,
    *,
    blocked_sources: tuple[BlockedSource, ...] = (),
    artifact_hash_refs: tuple[str, ...] = (),
) -> TrustEnvelope:
    """Derive a Trust Envelope from a validated source manifest.

    The manifest's ``license`` field and ``approval`` block are a *human
    operator's* recorded decision (the schema requires a named approver, an
    approval timestamp, and review notes). This function transcribes that
    recorded human decision into the §24.8 Trust Envelope and applies the
    operator's local blocked-source list. It performs no legal determination
    and no model inference (§24.2 / §24.3):

    * a source matched by the operator's blocked-source list resolves to a
      BLOCKED decision (§24.5 / §24.9);
    * otherwise the manifest-recorded approval is transcribed to an APPROVED
      decision under the manifest's declared, recognised licence;
    * a manifest licence StoryTime does not recognise yields an UNKNOWN
      licence type and a NEEDS_REVIEW decision — it fails the gate closed
      rather than being guessed at.

    ``decision_timestamp`` and ``approver_id`` come straight from the
    manifest's approval block — the time and identity of the *human* decision.
    """
    blocker = match_blocked_source(blocked_sources, manifest.source_url, manifest.source_id)
    license_type = _MANIFEST_LICENSE_TO_TYPE.get(manifest.license, LicenseType.UNKNOWN)
    review_summary = _bounded(manifest.approval.review_notes)

    if blocker is not None:
        return TrustEnvelope(
            schema_version=TRUST_ENVELOPE_SCHEMA_VERSION,
            source_ref=manifest.source_id,
            license_type=license_type,
            decision=GovernanceDecision.BLOCKED,
            decision_timestamp=manifest.approval.approved_at,
            approver_id=manifest.approval.approved_by,
            source_url=manifest.source_url,
            source_title=manifest.title,
            source_author=manifest.author,
            blocked_reason=(
                f"matched blocked-source pattern {blocker.pattern!r}: "
                f"{blocker.reason}"
            ),
            review_context_summary=review_summary or None,
            artifact_hash_refs=artifact_hash_refs,
        )

    if license_type is LicenseType.UNKNOWN:
        return TrustEnvelope(
            schema_version=TRUST_ENVELOPE_SCHEMA_VERSION,
            source_ref=manifest.source_id,
            license_type=LicenseType.UNKNOWN,
            decision=GovernanceDecision.NEEDS_REVIEW,
            decision_timestamp=manifest.approval.approved_at,
            approver_id=manifest.approval.approved_by,
            source_url=manifest.source_url,
            source_title=manifest.title,
            source_author=manifest.author,
            blocked_reason=(
                f"manifest declares licence {manifest.license!r}, which StoryTime "
                "does not recognise as an approved category; a human operator "
                "must review it"
            ),
            review_context_summary=review_summary or None,
            artifact_hash_refs=artifact_hash_refs,
        )

    return TrustEnvelope(
        schema_version=TRUST_ENVELOPE_SCHEMA_VERSION,
        source_ref=manifest.source_id,
        license_type=license_type,
        decision=GovernanceDecision.APPROVED,
        decision_timestamp=manifest.approval.approved_at,
        approver_id=manifest.approval.approved_by,
        source_url=manifest.source_url,
        source_title=manifest.title,
        source_author=manifest.author,
        review_context_summary=review_summary or None,
        artifact_hash_refs=artifact_hash_refs,
    )
