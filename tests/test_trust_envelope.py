"""Trust Envelope: model, closed-schema validation, and versioned IO.

These cover Architecture Baseline §24.8 — a well-formed Trust Envelope
validates and round-trips; a malformed one is rejected; an unsupported schema
version fails closed.
"""

from __future__ import annotations

import json

import pytest

from storytime.governance import (
    TRUST_ENVELOPE_SCHEMA_VERSION,
    GovernanceDecision,
    LicenseType,
    TrustEnvelope,
    TrustEnvelopeError,
    UnsupportedTrustEnvelopeVersionError,
    from_json,
    to_dict,
    to_json,
    trust_envelope_key,
    validate_trust_envelope,
)


def _approved_envelope() -> TrustEnvelope:
    """A fully-populated, schema-valid APPROVED Trust Envelope."""
    return TrustEnvelope(
        schema_version=TRUST_ENVELOPE_SCHEMA_VERSION,
        source_ref="the-raven",
        license_type=LicenseType.US_PUBLIC_DOMAIN,
        decision=GovernanceDecision.APPROVED,
        decision_timestamp="2026-01-16T09:30:00Z",
        approver_id="operator",
        source_url="https://example.org/the-raven.txt",
        source_title="The Raven",
        source_author="Edgar Allan Poe",
        review_context_summary="Verified public-domain text via reference.",
        artifact_hash_refs=("a" * 64,),
    )


def test_roundtrip_preserves_every_field() -> None:
    envelope = _approved_envelope()
    restored = from_json(to_json(envelope))
    assert restored == envelope
    assert restored.is_approved


def test_to_dict_has_every_canonical_field() -> None:
    data = to_dict(_approved_envelope())
    # All 18 §24.8 fields are present.
    expected = {
        "schema_version", "source_ref", "source_url", "source_title",
        "source_author", "license_type", "license_url", "license_evidence_ref",
        "decision", "decision_timestamp", "approver_id", "allowed_use",
        "attribution_required", "commercial_use_allowed", "blocked_reason",
        "governance_notes", "review_context_summary", "artifact_hash_refs",
    }
    assert set(data) == expected


def test_is_approved_only_for_approved_decision() -> None:
    for decision in GovernanceDecision:
        envelope = TrustEnvelope(
            schema_version=TRUST_ENVELOPE_SCHEMA_VERSION,
            source_ref="s",
            license_type=LicenseType.CC0,
            decision=decision,
            decision_timestamp="2026-01-01T00:00:00Z",
            approver_id="operator",
        )
        assert envelope.is_approved is (decision is GovernanceDecision.APPROVED)


def test_validate_rejects_unknown_field() -> None:
    data = to_dict(_approved_envelope())
    data["surprise"] = "not allowed"
    with pytest.raises(TrustEnvelopeError):
        validate_trust_envelope(data)


def test_validate_rejects_missing_required_field() -> None:
    data = to_dict(_approved_envelope())
    del data["approver_id"]
    with pytest.raises(TrustEnvelopeError):
        validate_trust_envelope(data)


def test_validate_rejects_unknown_enum_value() -> None:
    data = to_dict(_approved_envelope())
    data["decision"] = "MAYBE"
    with pytest.raises(TrustEnvelopeError):
        validate_trust_envelope(data)


def test_from_json_rejects_invalid_json() -> None:
    with pytest.raises(TrustEnvelopeError):
        from_json("{not json")


def test_from_json_rejects_non_object() -> None:
    with pytest.raises(TrustEnvelopeError):
        from_json("[1, 2, 3]")


def test_from_json_rejects_missing_schema_version() -> None:
    data = to_dict(_approved_envelope())
    del data["schema_version"]
    with pytest.raises(TrustEnvelopeError):
        from_json(json.dumps(data))


def test_from_json_rejects_unsupported_schema_version() -> None:
    data = to_dict(_approved_envelope())
    data["schema_version"] = "999"
    with pytest.raises(UnsupportedTrustEnvelopeVersionError):
        from_json(json.dumps(data))


def test_trust_envelope_key_is_a_relative_run_path() -> None:
    key = trust_envelope_key("01TESTRUN0000000000000001")
    assert key == "01TESTRUN0000000000000001/governance/trust-envelope.json"
    assert not key.startswith("/")
