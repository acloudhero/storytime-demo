"""Mock TTS adapter.

ARCH-LOCK: MockTTS is a real generator, not a no-op
DO NOT REFACTOR: MockTTS MUST write a valid, playable WAV file to disk so the
artifact-envelope contract, hashing, file-size recording, and downstream tests
all operate against a genuine audio artifact.
Rationale: Hard decision 8 of the Architecture Baseline plus the Round 8
Mock Audio Rule. A no-op mock would let envelope/hash code go untested.
"""

from __future__ import annotations

import array
import math
import sys
import wave
from pathlib import Path

from storytime.adapters.tts.base import TTSResult
from storytime.util.hashing import sha256_file

# Synthesised audio length scales with text length, bounded for test speed.
_SECONDS_PER_WORD = 0.06
_MIN_SECONDS = 1.0
_MAX_SECONDS = 30.0
_TONE_HZ = 220.0
_AMPLITUDE = 1200  # low amplitude: audible but quiet


class MockTTS:
    """Generates a deterministic low-tone WAV. Used in CI and the scaffold."""

    name = "mock"
    version = "0.2.0"

    def synthesize(
        self,
        text: str,
        *,
        out_path: Path,
        voice: str | None = None,
        sample_rate_hz: int = 22050,
    ) -> TTSResult:
        """Write a real mono 16-bit WAV whose duration scales with *text*."""
        word_count = max(1, len(text.split()))
        duration_seconds = min(_MAX_SECONDS, max(_MIN_SECONDS, word_count * _SECONDS_PER_WORD))
        frame_count = int(duration_seconds * sample_rate_hz)

        samples = array.array(
            "h",
            (
                int(_AMPLITUDE * math.sin(2 * math.pi * _TONE_HZ * (i / sample_rate_hz)))
                for i in range(frame_count)
            ),
        )
        # WAV PCM is little-endian; correct on big-endian hosts.
        if sys.byteorder == "big":
            samples.byteswap()

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with wave.open(str(out_path), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate_hz)
            wav.writeframes(samples.tobytes())

        return TTSResult(
            audio_path=out_path,
            audio_format="wav",
            sample_rate_hz=sample_rate_hz,
            channels=1,
            duration_seconds=frame_count / sample_rate_hz,
            audio_bytes=out_path.stat().st_size,
            audio_sha256=sha256_file(out_path),
        )
