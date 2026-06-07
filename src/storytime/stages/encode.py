"""WAV-to-MP3 encoding for the assemble stage.

ARCH-LOCK: MP3 encoding is confined to the assemble layer
DO NOT REFACTOR: TTS adapters emit WAV only (hard decision 7). MP3 encoding
lives here and is used by the assemble stage, never by a TTS adapter. ffmpeg
is an external tool; its absence must fail fast with clear, actionable
guidance and must never degrade silently to a non-MP3 fallback.
Rationale: Hard decision 7 and Round 7 prerequisite correction 5 — ffmpeg is
not required for the test suite, but when MP3 assembly is actually requested
its absence is an explicit, non-silent failure.

This module imports no other storytime package beyond util; it is the
assemble stage's injected, swappable dependency (Round 5 clarification A1).
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, runtime_checkable

from storytime.util.hashing import sha256_file

# Actionable operator guidance, surfaced verbatim when ffmpeg is missing.
FFMPEG_GUIDANCE = (
    "ffmpeg was not found on PATH. StoryTime needs ffmpeg to encode "
    "podcast-ready MP3 audio in the assemble stage. Install ffmpeg "
    "(e.g. 'apt install ffmpeg' or 'brew install ffmpeg'), then re-run. "
    "'storytime doctor' reports ffmpeg availability."
)


class FfmpegUnavailableError(RuntimeError):
    """Raised when MP3 assembly is requested but ffmpeg is not available."""


class Mp3EncodeError(RuntimeError):
    """Raised when ffmpeg is available but the encode invocation fails."""


@dataclass(frozen=True, slots=True)
class EncodeResult:
    """The result of encoding a WAV file to MP3."""

    mp3_path: Path
    mp3_bytes: int
    mp3_sha256: str


@runtime_checkable
class Mp3Encoder(Protocol):
    """Encodes a WAV file to MP3. The assemble stage's injected dependency."""

    name: str

    def is_available(self) -> bool: ...

    def encode(self, wav_path: Path, mp3_path: Path) -> EncodeResult: ...


class FfmpegMp3Encoder:
    """An Mp3Encoder backed by the ffmpeg command-line tool.

    The ffmpeg path is resolved once and stored. A None path means ffmpeg is
    not installed; is_available() reports that and encode() fails fast.
    """

    name = "ffmpeg"

    def __init__(self, ffmpeg_path: str | None) -> None:
        self._ffmpeg_path = ffmpeg_path

    @classmethod
    def autodetect(cls) -> FfmpegMp3Encoder:
        """Build an encoder, resolving ffmpeg from PATH (None if absent)."""
        return cls(shutil.which("ffmpeg"))

    def is_available(self) -> bool:
        """True if an ffmpeg executable was resolved."""
        return self._ffmpeg_path is not None

    def encode(self, wav_path: Path, mp3_path: Path) -> EncodeResult:
        """Encode *wav_path* to MP3 at *mp3_path*.

        Raises FfmpegUnavailableError if ffmpeg is not installed, and
        Mp3EncodeError if ffmpeg runs but does not produce a valid MP3.
        """
        if self._ffmpeg_path is None:
            raise FfmpegUnavailableError(FFMPEG_GUIDANCE)
        if not wav_path.is_file():
            raise Mp3EncodeError(f"input WAV does not exist: {wav_path}")
        mp3_path.parent.mkdir(parents=True, exist_ok=True)
        completed = subprocess.run(
            [
                self._ffmpeg_path,
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(wav_path),
                "-codec:a",
                "libmp3lame",
                "-q:a",
                "5",
                str(mp3_path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0 or not mp3_path.is_file():
            raise Mp3EncodeError(
                f"ffmpeg failed to encode MP3 (exit {completed.returncode}): "
                f"{completed.stderr.strip()}"
            )
        return EncodeResult(
            mp3_path=mp3_path,
            mp3_bytes=mp3_path.stat().st_size,
            mp3_sha256=sha256_file(mp3_path),
        )
