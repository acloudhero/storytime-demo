"""Trust Envelope JSON Schema.

ARCH-LOCK: Trust Envelope Closed Schema
DO NOT REFACTOR: ``additionalProperties`` MUST stay false. The licence-type and
decision enums are the canonical Architecture Baseline §24.8 value sets — do
not silently drop a value, and do not relax them to free-form strings. Adding a
value is a schema change governed by TRUST_ENVELOPE_SCHEMA_VERSION.
Rationale: §24.8 defines this schema as canonical architecture law. A closed
schema is how StoryTime keeps the governance record honest and parseable for
the Phase 10 UI (§24.15).

The schema mirrors the closed-schema discipline of the source manifest
(``storytime.manifest.schema``) and is validated with the same jsonschema
Draft 2020-12 validator already in the dependency set.
"""

from __future__ import annotations

from typing import Any

from storytime.governance.trust_envelope import GovernanceDecision, LicenseType

_LICENSE_TYPE_VALUES: list[str] = [member.value for member in LicenseType]
_DECISION_VALUES: list[str] = [member.value for member in GovernanceDecision]

# A nullable string property: present, but either a string or JSON null.
_NULLABLE_STRING: dict[str, Any] = {"type": ["string", "null"]}
_NULLABLE_BOOL: dict[str, Any] = {"type": ["boolean", "null"]}

# Draft 2020-12 closed schema for the §24.8 Trust Envelope.
TRUST_ENVELOPE_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "StoryTimeTrustEnvelope",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema_version",
        "source_ref",
        "source_url",
        "source_title",
        "source_author",
        "license_type",
        "license_url",
        "license_evidence_ref",
        "decision",
        "decision_timestamp",
        "approver_id",
        "allowed_use",
        "attribution_required",
        "commercial_use_allowed",
        "blocked_reason",
        "governance_notes",
        "review_context_summary",
        "artifact_hash_refs",
    ],
    "properties": {
        "schema_version": {"type": "string", "minLength": 1},
        "source_ref": {"type": "string", "minLength": 1},
        "source_url": _NULLABLE_STRING,
        "source_title": _NULLABLE_STRING,
        "source_author": _NULLABLE_STRING,
        "license_type": {"enum": _LICENSE_TYPE_VALUES},
        "license_url": _NULLABLE_STRING,
        "license_evidence_ref": _NULLABLE_STRING,
        "decision": {"enum": _DECISION_VALUES},
        "decision_timestamp": {"type": "string", "minLength": 1},
        "approver_id": {"type": "string", "minLength": 1},
        "allowed_use": _NULLABLE_STRING,
        "attribution_required": _NULLABLE_BOOL,
        "commercial_use_allowed": _NULLABLE_BOOL,
        "blocked_reason": _NULLABLE_STRING,
        "governance_notes": _NULLABLE_STRING,
        "review_context_summary": _NULLABLE_STRING,
        "artifact_hash_refs": {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
        },
    },
}
