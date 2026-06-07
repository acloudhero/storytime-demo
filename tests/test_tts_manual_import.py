"""ManualImportTTS must validate and import an operator-supplied WAV."""

from __future__ import annotations

from pathlib import Path

import pytest

from storytime.adapters.tts import ManualImportTTS, MockTTS, TTSUnavailableError


def test_manual_import_copies_a_valid_wav(tmp_path: Path) -> None:
    source = tmp_path / "operator.wav"
    MockTTS().synthesize("operator supplied audio", out_path=source)

    out = tmp_path / "imported.wav"
    result = ManualImportTTS(source).synthesize("ignored", out_path=out)

    assert out.is_file()
    assert result.audio_bytes == source.stat().st_size
    assert result.channels == 1
    assert result.duration_seconds > 0


def test_manual_import_missing_source_raises(tmp_path: Path) -> None:
    """Negative case: a missing source WAV is an unavailable-provider error."""
    adapter = ManualImportTTS(tmp_path / "nonexistent.wav")
    with pytest.raises(TTSUnavailableError):
        adapter.synthesize("text", out_path=tmp_path / "out.wav")


def test_manual_import_non_wav_source_raises(tmp_path: Path) -> None:
    """Negative case: a non-WAV file must be rejected, not blindly copied."""
    bogus = tmp_path / "not_audio.wav"
    bogus.write_text("this is plainly not a RIFF/WAVE file", encoding="utf-8")
    adapter = ManualImportTTS(bogus)
    with pytest.raises(TTSUnavailableError):
        adapter.synthesize("text", out_path=tmp_path / "out.wav")
