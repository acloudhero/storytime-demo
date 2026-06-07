"""Text-to-speech adapter interface.

ARCH-LOCK: TTS Adapter Contract
DO NOT REFACTOR: TTS adapters emit WAV only. MP3 encoding belongs in the
assemble/package layer (Phase 3), never here. Do not add MP3 output to an
adapter.
Rationale: Hard decision 7 of the Architecture Baseline. Keeping adapters
WAV-only means swapping the TTS engine never perturbs the publish pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, runtime_checkable


class TTSUnavailableError(NotImplementedError):
    """Raised by a TTS adapter that is a stub / not available in this phase."""


@dataclass(frozen=True, slots=True)
class TTSResult:
    """The result of a synthesis call. The payload is always a WAV file."""

    audio_path: Path
    audio_format: str  # always "wav" in Phase 2
    sample_rate_hz: int
    channels: int
    duration_seconds: float
    audio_bytes: int
    audio_sha256: str


@runtime_checkable
class TTSAdapter(Protocol):
    """Converts text into a WAV audio file on disk."""

    name: str
    version: str

    def synthesize(
        self,
        text: str,
        *,
        out_path: Path,
        voice: str | None = None,
        sample_rate_hz: int = 22050,
    ) -> TTSResult: ...
