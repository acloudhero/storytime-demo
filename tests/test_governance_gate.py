"""The fail-closed governance gate and manifest-to-Trust-Envelope derivation.

Covers Architecture Baseline §24.6 — only an explicit APPROVED Trust Envelope
passes the gate; every other decision, and a missing / malformed envelope,
fails closed — and §24.2/§24.3: the derivation transcribes the human
operator's manifest-recorded decision, never an inferred legal conclusion.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from storytime.adapters.storage import LocalFilesystemStorage
from storytime.governance import (
    BlockedSource,
    GovernanceDecision,
    LicenseType,
    TrustEnvelope,
    evaluate_envelope,
    require_approved_envelope,
    to_json,
    trust_envelope_from_manifest,
    trust_envelope_key,
    write_trust_envelope,
)
from storytime.manifest import parse_manifest

_TS = "2026-01-16T09:30:00Z"


def _envelope(decision: GovernanceDecision) -> TrustEnvelope:
    return TrustEnvelope(
        schema_version="1",
        source_ref="s",
        license_type=LicenseType.CC0,
        decision=decision,
        decision_timestamp=_TS,
        approver_id="operator",
    )


# -- evaluate_envelope ------------------------------------------------------

def test_approved_envelope_passes_the_gate() -> None:
    result = evaluate_envelope(_envelope(GovernanceDecision.APPROVED))
    assert result.passed
    assert result.decision is GovernanceDecision.APPROVED


@pytest.mark.parametrize(
    "decision",
    [
        GovernanceDecision.REJECTED,
        GovernanceDecision.BLOCKED,
        GovernanceDecision.NEEDS_REVIEW,
    ],
)
def test_non_approved_decisions_fail_closed(decision: GovernanceDecision) -> None:
    result = evaluate_envelope(_envelope(decision))
    assert not result.passed
    assert result.decision is decision


def test_absent_envelope_fails_closed() -> None:
    result = evaluate_envelope(None)
    assert not result.passed
    assert result.decision is None


def test_absent_envelope_carries_the_error_reason() -> None:
    result = evaluate_envelope(None, error="trust envelope artifact is missing")
    assert not result.passed
    assert "missing" in result.reason


# -- require_approved_envelope (durable artifact) ---------------------------

def test_require_passes_for_an_approved_durable_envelope(tmp_path: Path) -> None:
    storage = LocalFilesystemStorage(tmp_path)
    write_trust_envelope(storage, "run1", _envelope(GovernanceDecision.APPROVED))
    assert require_approved_envelope(storage, "run1").passed


def test_require_fails_closed_when_envelope_missing(tmp_path: Path) -> None:
    storage = LocalFilesystemStorage(tmp_path)
    # Nothing was written for this run.
    assert not require_approved_envelope(storage, "ghost-run").passed


def test_require_fails_closed_for_a_blocked_durable_envelope(tmp_path: Path) -> None:
    storage = LocalFilesystemStorage(tmp_path)
    write_trust_envelope(storage, "run2", _envelope(GovernanceDecision.BLOCKED))
    assert not require_approved_envelope(storage, "run2").passed


def test_require_fails_closed_for_a_malformed_durable_envelope(
    tmp_path: Path,
) -> None:
    storage = LocalFilesystemStorage(tmp_path)
    storage.write_text(trust_envelope_key("run3"), "{ this is not valid json")
    result = require_approved_envelope(storage, "run3")
    assert not result.passed


# -- trust_envelope_from_manifest -------------------------------------------

def _manifest(valid_manifest: dict[str, Any], **overrides: Any) -> Any:
    data = dict(valid_manifest)
    data.update(overrides)
    return parse_manifest(data)


def test_pd_us_manifest_derives_an_approved_envelope(
    valid_manifest: dict[str, Any],
) -> None:
    manifest = _manifest(valid_manifest, license="PD-US")
    envelope = trust_envelope_from_manifest(manifest)
    assert envelope.decision is GovernanceDecision.APPROVED
    assert envelope.license_type is LicenseType.US_PUBLIC_DOMAIN
    # The decision identity/time is the HUMAN operator's, from the manifest.
    assert envelope.approver_id == manifest.approval.approved_by
    assert envelope.decision_timestamp == manifest.approval.approved_at


def test_cc0_manifest_derives_cc0_license_type(
    valid_manifest: dict[str, Any],
) -> None:
    manifest = _manifest(valid_manifest, license="CC0-1.0")
    envelope = trust_envelope_from_manifest(manifest)
    assert envelope.license_type is LicenseType.CC0
    assert envelope.decision is GovernanceDecision.APPROVED


def test_blocked_source_derives_a_blocked_envelope(
    valid_manifest: dict[str, Any],
) -> None:
    manifest = _manifest(valid_manifest)
    blocked = (BlockedSource(pattern="example.org", reason="operator-blocked"),)
    envelope = trust_envelope_from_manifest(manifest, blocked_sources=blocked)
    assert envelope.decision is GovernanceDecision.BLOCKED
    assert envelope.blocked_reason is not None
    assert "operator-blocked" in envelope.blocked_reason


def test_artifact_hash_refs_are_carried(valid_manifest: dict[str, Any]) -> None:
    manifest = _manifest(valid_manifest)
    envelope = trust_envelope_from_manifest(
        manifest, artifact_hash_refs=("d" * 64,)
    )
    assert envelope.artifact_hash_refs == ("d" * 64,)


def test_review_summary_is_bounded(valid_manifest: dict[str, Any]) -> None:
    # review_context_summary is a short rationale, never a content store
    # (§24.8): a very long manifest note is truncated.
    manifest = _manifest(
        valid_manifest,
        approval={
            "approved_by": "operator",
            "approved_at": _TS,
            "review_notes": "x" * 5000,
        },
    )
    envelope = trust_envelope_from_manifest(manifest)
    assert envelope.review_context_summary is not None
    assert len(envelope.review_context_summary) <= 500


def test_derived_envelope_serializes_and_validates(
    valid_manifest: dict[str, Any],
) -> None:
    # A derived envelope must satisfy its own closed schema.
    envelope = trust_envelope_from_manifest(_manifest(valid_manifest))
    # to_json -> from_json round-trips without raising.
    from storytime.governance import from_json

    assert from_json(to_json(envelope)) == envelope
