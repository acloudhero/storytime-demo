"""Phase 13I — governed local TTS proof audit / event model.

These are the structured audit records the governed boundary emits for one
proof invocation. They are deliberately a *separate, self-contained* model and
NOT additions to :class:`storytime.events.model.EventType`, which is an
ARCH-LOCKed closed enum for the main pipeline ("do not introduce an event bus,
do not let events import other storytime modules"). The TTS proof is a narrow
local-chain proof with its own lifecycle, so it carries its own record type.

Discipline mirrored from the pipeline event model: every payload is small and
JSON-serializable (paths, hashes, counts, durations, typed reasons) and MUST
NOT contain raw fixture text, credentials, provider request/response bodies, or
verbatim provider error strings.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

# The stage label all TTS proof events carry, for observability correlation.
TTS_STAGE = "tts"


class TtsProofEventType(StrEnum):
    """The closed lifecycle of one governed TTS proof invocation."""

    REQUESTED = "tts.requested"
    GUARD_REJECTED = "tts.guard_rejected"
    EXECUTING = "tts.executing"
    COMPLETED = "tts.completed"
    FAILED = "tts.failed"


class TtsFailureReason(StrEnum):
    """Typed, safe failure taxonomy. A reason is recorded; never a raw error."""

    GUARD_REJECTED = "guard_rejected"
    PROVIDER_DISABLED = "provider_disabled"
    FIXTURE_NOT_ALLOWLISTED = "fixture_not_allowlisted"
    CHARACTER_LIMIT_EXCEEDED = "character_limit_exceeded"
    OUTPUT_LIMIT_EXCEEDED = "output_limit_exceeded"
    PATH_INVALID = "path_invalid"
    PROVIDER_ERROR = "provider_error"
    QUOTA_OR_RATE_LIMIT = "quota_or_rate_limit"
    NETWORK_ERROR = "network_error"
    TIMEOUT = "timeout"
    WRITE_FAILED = "write_failed"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class TtsProofEvent:
    """A single immutable governed-TTS audit record.

    ``payload`` must be small and JSON-serializable: provider/mode/voice,
    character count, text hash, audio hash, byte size, durations, cost
    estimate, artifact filename, result, typed failure reason. Raw fixture
    text, credentials, and verbatim provider errors must never appear here.
    """

    event_type: TtsProofEventType
    proof_run_id: str
    occurred_at: datetime
    payload: Mapping[str, object]
    stage: str = TTS_STAGE

    def to_record(self) -> dict[str, object]:
        """Render this event as a JSON-ready audit record dictionary."""
        return {
            "event_type": str(self.event_type),
            "proof_run_id": self.proof_run_id,
            "occurred_at": self.occurred_at.isoformat(),
            "stage": self.stage,
            "payload": dict(self.payload),
        }

    def to_json_line(self) -> str:
        """Return a compact, sorted single-line JSON record for the audit log.

        Raises ``TypeError`` if the payload is not JSON-serializable, which
        keeps the "small, serializable payload" rule enforced at write time.
        """
        return json.dumps(self.to_record(), sort_keys=True, separators=(",", ":"))
