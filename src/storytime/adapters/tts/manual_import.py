"""Manual-import TTS adapter.

Imports a WAV file the operator produced externally. The source WAV path is
constructor-injected (Round 5 clarification A1: stage-specific adapters are
constructor-injected, not placed in global RunnerContext).
"""

from __future__ import annotations

import shutil
import wave
from pathlib import Path

from storytime.adapters.tts.base import TTSResult, TTSUnavailableError
from storytime.util.hashing import sha256_file


class ManualImportTTS:
    """Validates and imports an operator-supplied WAV as the synthesis output."""

    name = "manual_import"
    version = "0.2.0"

    def __init__(self, source_wav: Path) -> None:
        self._source_wav = source_wav

    def synthesize(
        self,
        text: str,
        *,
        out_path: Path,
        voice: str | None = None,
        sample_rate_hz: int = 22050,
    ) -> TTSResult:
        """Validate the source WAV and copy it to *out_path*.

        *text* is part of the shared TTSAdapter contract but is unused here:
        manual import does not synthesise, it ingests. Raises TTSUnavailableError
        if the source file is missing or is not a readable WAV.
        """
        if not self._source_wav.is_file():
            raise TTSUnavailableError(
                f"manual import source WAV not found: {self._source_wav}"
            )
        try:
            with wave.open(str(self._source_wav), "rb") as wav:
                channels = wav.getnchannels()
                rate = wav.getframerate()
                frames = wav.getnframes()
        except (wave.Error, EOFError) as exc:
            raise TTSUnavailableError(
                f"manual import source is not a valid WAV: {self._source_wav} ({exc})"
            ) from exc

        out_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(self._source_wav, out_path)

        duration = frames / rate if rate else 0.0
        return TTSResult(
            audio_path=out_path,
            audio_format="wav",
            sample_rate_hz=rate,
            channels=channels,
            duration_seconds=duration,
            audio_bytes=out_path.stat().st_size,
            audio_sha256=sha256_file(out_path),
        )
