"""MockTTS must produce a real, playable WAV file."""

from __future__ import annotations

import wave
from pathlib import Path

from storytime.adapters.tts import MockTTS
from storytime.util.hashing import sha256_file


def test_mock_tts_writes_a_real_wav(tmp_path: Path) -> None:
    out = tmp_path / "episode.wav"
    result = MockTTS().synthesize("hello there listener", out_path=out)

    assert out.is_file()
    assert result.audio_format == "wav"
    assert result.audio_bytes == out.stat().st_size
    assert result.audio_bytes > 0
    assert result.audio_sha256 == sha256_file(out)


def test_mock_tts_output_is_a_parseable_wav(tmp_path: Path) -> None:
    out = tmp_path / "episode.wav"
    result = MockTTS().synthesize("one two three four five", out_path=out)

    with wave.open(str(out), "rb") as wav:
        assert wav.getnchannels() == 1
        assert wav.getsampwidth() == 2
        assert wav.getframerate() == result.sample_rate_hz
        assert wav.getnframes() > 0


def test_longer_text_yields_longer_audio(tmp_path: Path) -> None:
    """Relational assertion: the mock is not a fixed-length no-op."""
    short = MockTTS().synthesize("word", out_path=tmp_path / "s.wav")
    long_text = " ".join(["word"] * 200)
    long = MockTTS().synthesize(long_text, out_path=tmp_path / "l.wav")
    assert long.duration_seconds > short.duration_seconds
    assert long.audio_bytes > short.audio_bytes
