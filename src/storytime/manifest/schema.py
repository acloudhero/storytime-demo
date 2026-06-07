"""Source manifest JSON Schema.

ARCH-LOCK: Manifest Closed Schema
DO NOT REFACTOR: additionalProperties MUST stay false at every object level.
Do not relax license/jurisdiction/language to free-form strings.
Rationale: Hard decision 10 of the Architecture Baseline. A closed schema is
how StoryTime keeps source material constrained to CC0 / US public domain and
catches typos and undeclared scope creep at ingest time.
"""

from __future__ import annotations

from typing import Any

# Draft 2020-12 schema. `pattern` does the deterministic enforcement; `format`
# annotations are documentation and are harmless without a format checker.
SOURCE_MANIFEST_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "StoryTimeSourceManifest",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "manifest_version",
        "source_id",
        "title",
        "author",
        "source_url",
        "retrieval_date",
        "jurisdiction",
        "license",
        "text_sha256",
        "text_encoding",
        "text_path",
        "language",
        "approval",
    ],
    "properties": {
        "manifest_version": {"const": 1},
        "source_id": {"type": "string", "pattern": "^[a-z0-9-]{3,64}$"},
        "title": {"type": "string", "minLength": 1},
        "author": {"type": "string", "minLength": 1},
        "source_url": {"type": "string", "minLength": 1, "format": "uri"},
        "retrieval_date": {
            "type": "string",
            "pattern": r"^\d{4}-\d{2}-\d{2}$",
            "format": "date",
        },
        "jurisdiction": {"const": "US"},
        "license": {"enum": ["CC0-1.0", "PD-US"]},
        "text_sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "text_encoding": {"const": "utf-8"},
        "text_path": {"type": "string", "minLength": 1},
        "language": {"const": "en"},
        "approval": {
            "type": "object",
            "additionalProperties": False,
            "required": ["approved_by", "approved_at", "review_notes"],
            "properties": {
                "approved_by": {"type": "string", "minLength": 1},
                "approved_at": {
                    "type": "string",
                    "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",
                    "format": "date-time",
                },
                "review_notes": {"type": "string"},
            },
        },
    },
}
