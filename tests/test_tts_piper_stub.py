"""PiperTTS is a Phase 2 stub and must fail clearly."""

from __future__ import annotations

from pathlib import Path

import pytest

from storytime.adapters.tts import PiperTTS, TTSUnavailableError


def test_piper_synthesize_raises_unavailable(tmp_path: Path) -> None:
    with pytest.raises(TTSUnavailableError):
        PiperTTS().synthesize("anything", out_path=tmp_path / "out.wav")


def test_piper_error_is_a_notimplementederror(tmp_path: Path) -> None:
    """TTSUnavailableError is a NotImplementedError, per the Round 8 rule."""
    with pytest.raises(NotImplementedError):
        PiperTTS().synthesize("anything", out_path=tmp_path / "out.wav")


def test_piper_writes_no_file(tmp_path: Path) -> None:
    """Negative case: a stub must not leave a partial artifact behind."""
    out = tmp_path / "out.wav"
    with pytest.raises(TTSUnavailableError):
        PiperTTS().synthesize("anything", out_path=out)
    assert not out.exists()
