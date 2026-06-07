"""MP3 encoder: ffmpeg fail-fast guidance and real encoding."""

from __future__ import annotations

import shutil
import wave
from pathlib import Path

import pytest

from storytime.stages.encode import (
    EncodeResult,
    FfmpegMp3Encoder,
    FfmpegUnavailableError,
    Mp3EncodeError,
)

_HAS_FFMPEG = shutil.which("ffmpeg") is not None


def _write_wav(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(22050)
        handle.writeframes(b"\x00\x01" * 22050)


def test_encoder_with_no_ffmpeg_reports_unavailable() -> None:
    assert FfmpegMp3Encoder(None).is_available() is False


def test_encode_without_ffmpeg_fails_fast_with_guidance(tmp_path: Path) -> None:
    encoder = FfmpegMp3Encoder(None)
    with pytest.raises(FfmpegUnavailableError) as exc:
        encoder.encode(tmp_path / "in.wav", tmp_path / "out.mp3")
    message = str(exc.value).lower()
    assert "ffmpeg" in message
    assert "install" in message
    # The failure is explicit: no MP3 is silently produced.
    assert not (tmp_path / "out.mp3").exists()


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_autodetect_finds_ffmpeg() -> None:
    assert FfmpegMp3Encoder.autodetect().is_available() is True


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_encode_produces_real_mp3(tmp_path: Path) -> None:
    wav = tmp_path / "in.wav"
    _write_wav(wav)
    result = FfmpegMp3Encoder.autodetect().encode(wav, tmp_path / "out.mp3")
    assert isinstance(result, EncodeResult)
    assert result.mp3_path.is_file()
    assert result.mp3_bytes > 0
    assert len(result.mp3_sha256) == 64
    # An MP3 begins with an ID3 tag or an MPEG frame sync byte.
    head = result.mp3_path.read_bytes()[:3]
    assert head == b"ID3" or head[0] == 0xFF


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_encode_missing_input_raises(tmp_path: Path) -> None:
    with pytest.raises(Mp3EncodeError):
        FfmpegMp3Encoder.autodetect().encode(
            tmp_path / "does-not-exist.wav", tmp_path / "out.mp3"
        )
