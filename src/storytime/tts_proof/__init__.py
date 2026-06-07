"""Phase 13I — governed local TTS proof / audio artifact boundary.

A narrow backend/local-chain proof that StoryTime can generate a local audio
artifact through a governed, observable, auditable boundary: an approved
fixture → governance/cost guard → deterministic mock TTS provider → atomic
local audio artifact → manifest → audit/event records → observability-safe
metadata. The proof stands with no credentials and no network access, adds no
local bridge action, and never touches the browser.
"""

from storytime.tts_proof.boundary import (
    DEFAULT_FIXTURE_ID,
    TtsProofResult,
    run_tts_proof,
)
from storytime.tts_proof.config import TtsProofConfig, load_tts_proof_config
from storytime.tts_proof.events import (
    TtsFailureReason,
    TtsProofEvent,
    TtsProofEventType,
)

__all__ = [
    "DEFAULT_FIXTURE_ID",
    "TtsFailureReason",
    "TtsProofConfig",
    "TtsProofEvent",
    "TtsProofEventType",
    "TtsProofResult",
    "load_tts_proof_config",
    "run_tts_proof",
]
