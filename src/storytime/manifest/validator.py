"""Source manifest validation and loading.

A manifest is validated against the closed schema before its text is trusted.
Validation failure is a hard stop: StoryTime never ingests an unvalidated or
partially valid manifest.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from storytime.manifest.schema import SOURCE_MANIFEST_SCHEMA

_VALIDATOR = Draft202012Validator(SOURCE_MANIFEST_SCHEMA)


class ManifestValidationError(ValueError):
    """Raised when a source manifest fails closed-schema validation."""

    def __init__(self, messages: list[str]) -> None:
        self.messages = messages
        super().__init__("; ".join(messages))


@dataclass(frozen=True, slots=True)
class ManifestApproval:
    """The approval block of a source manifest."""

    approved_by: str
    approved_at: str
    review_notes: str


@dataclass(frozen=True, slots=True)
class SourceManifest:
    """A validated source manifest."""

    manifest_version: int
    source_id: str
    title: str
    author: str
    source_url: str
    retrieval_date: str
    jurisdiction: str
    license: str
    text_sha256: str
    text_encoding: str
    text_path: str
    language: str
    approval: ManifestApproval


def validate_manifest(data: dict[str, Any]) -> None:
    """Validate *data* against the closed schema.

    Raises ManifestValidationError listing every problem found. Because the
    schema sets additionalProperties:false, any unknown field is an error.
    """
    errors = sorted(_VALIDATOR.iter_errors(data), key=lambda e: list(e.absolute_path))
    if errors:
        messages = [
            f"{'/'.join(str(p) for p in err.absolute_path) or '<root>'}: {err.message}"
            for err in errors
        ]
        raise ManifestValidationError(messages)


def parse_manifest(data: dict[str, Any]) -> SourceManifest:
    """Validate *data* and build a SourceManifest from it."""
    validate_manifest(data)
    approval_raw = data["approval"]
    return SourceManifest(
        manifest_version=data["manifest_version"],
        source_id=data["source_id"],
        title=data["title"],
        author=data["author"],
        source_url=data["source_url"],
        retrieval_date=data["retrieval_date"],
        jurisdiction=data["jurisdiction"],
        license=data["license"],
        text_sha256=data["text_sha256"],
        text_encoding=data["text_encoding"],
        text_path=data["text_path"],
        language=data["language"],
        approval=ManifestApproval(
            approved_by=approval_raw["approved_by"],
            approved_at=approval_raw["approved_at"],
            review_notes=approval_raw["review_notes"],
        ),
    )


def load_manifest(path: Path) -> SourceManifest:
    """Read, validate, and parse a source manifest from *path*."""
    try:
        raw: Any = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ManifestValidationError([f"manifest is not valid JSON: {exc}"]) from exc
    if not isinstance(raw, dict):
        raise ManifestValidationError(["manifest must be a JSON object"])
    return parse_manifest(raw)
