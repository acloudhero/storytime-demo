"""Text-to-speech adapters: mock (real WAV), manual import, and Piper stub."""

from storytime.adapters.tts.base import TTSAdapter, TTSResult, TTSUnavailableError
from storytime.adapters.tts.manual_import import ManualImportTTS
from storytime.adapters.tts.mock import MockTTS
from storytime.adapters.tts.piper import PiperTTS

__all__ = [
    "ManualImportTTS",
    "MockTTS",
    "PiperTTS",
    "TTSAdapter",
    "TTSResult",
    "TTSUnavailableError",
]
