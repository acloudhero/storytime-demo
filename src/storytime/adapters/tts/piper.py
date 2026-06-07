"""Piper TTS adapter — STUB ONLY.

ARCH-LOCK: Piper is stubbed in Phase 2
DO NOT REFACTOR: Do not implement real Piper synthesis here during the scaffold
phase. Phase 2 must not depend on Piper, and Phase 2 tests must not require it.
Rationale: Hard decision 8 of the Architecture Baseline and the Round 8 task
constraints. MockTTS and ManualImportTTS must work before Piper is introduced.
"""

from __future__ import annotations

from pathlib import Path

from storytime.adapters.tts.base import TTSResult, TTSUnavailableError


class PiperTTS:
    """Placeholder for the future Piper-backed adapter. Not yet available."""

    name = "piper"
    version = "0.0.0-stub"

    def synthesize(
        self,
        text: str,
        *,
        out_path: Path,
        voice: str | None = None,
        sample_rate_hz: int = 22050,
    ) -> TTSResult:
        """Always raises: Piper is a stub in Phase 2."""
        raise TTSUnavailableError(
            "PiperTTS is a Phase 2 stub and is not available. "
            "Use the 'mock' or 'manual_import' TTS adapter until Phase 3."
        )
