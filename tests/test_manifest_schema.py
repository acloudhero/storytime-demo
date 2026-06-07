"""Source manifest closed-schema validation."""

from __future__ import annotations

from typing import Any

import pytest

from storytime.manifest import ManifestValidationError, parse_manifest, validate_manifest


def test_valid_manifest_passes(valid_manifest: dict[str, Any]) -> None:
    validate_manifest(valid_manifest)  # must not raise
    parsed = parse_manifest(valid_manifest)
    assert parsed.source_id == "the-raven"
    assert parsed.license == "PD-US"
    assert parsed.approval.approved_by == "operator"


def test_unknown_top_level_field_is_rejected(valid_manifest: dict[str, Any]) -> None:
    """Negative case: the schema is closed (additionalProperties: false)."""
    valid_manifest["surprise_field"] = "nope"
    with pytest.raises(ManifestValidationError):
        validate_manifest(valid_manifest)


def test_unknown_nested_field_is_rejected(valid_manifest: dict[str, Any]) -> None:
    """Negative case: the approval object is closed too."""
    valid_manifest["approval"]["extra"] = "nope"
    with pytest.raises(ManifestValidationError):
        validate_manifest(valid_manifest)


def test_missing_required_field_is_rejected(valid_manifest: dict[str, Any]) -> None:
    del valid_manifest["text_sha256"]
    with pytest.raises(ManifestValidationError):
        validate_manifest(valid_manifest)


def test_disallowed_license_is_rejected(valid_manifest: dict[str, Any]) -> None:
    valid_manifest["license"] = "All-Rights-Reserved"
    with pytest.raises(ManifestValidationError):
        validate_manifest(valid_manifest)


def test_non_us_jurisdiction_is_rejected(valid_manifest: dict[str, Any]) -> None:
    valid_manifest["jurisdiction"] = "EU"
    with pytest.raises(ManifestValidationError):
        validate_manifest(valid_manifest)


def test_bad_text_sha256_pattern_is_rejected(valid_manifest: dict[str, Any]) -> None:
    valid_manifest["text_sha256"] = "not-a-hash"
    with pytest.raises(ManifestValidationError):
        validate_manifest(valid_manifest)


def test_wrong_manifest_version_is_rejected(valid_manifest: dict[str, Any]) -> None:
    valid_manifest["manifest_version"] = 2
    with pytest.raises(ManifestValidationError):
        validate_manifest(valid_manifest)


def test_error_lists_every_problem(valid_manifest: dict[str, Any]) -> None:
    valid_manifest["license"] = "bad"
    valid_manifest["jurisdiction"] = "bad"
    with pytest.raises(ManifestValidationError) as caught:
        validate_manifest(valid_manifest)
    assert len(caught.value.messages) >= 2
