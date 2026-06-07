"""Phase 13I — governed local TTS proof manifest.

The manifest is the local provenance record written beside each generated audio
artifact. It records what produced the artifact (provider, mode, voice/model),
its integrity (text hash, audio hash, byte size), timing, the labeled cost
estimate, and phase/source metadata.

It is a *local runtime artifact*: it lives under the controlled artifact
directory (which defaults under ``runs/``) and is excluded from version control
and from the locked archive. It records the source *text hash* and character
count, never the raw fixture text.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

# Increment, never repurpose, if the manifest shape changes.
TTS_MANIFEST_SCHEMA_VERSION = 1


@dataclass(frozen=True, slots=True)
class TtsManifest:
    """Local provenance for one generated audio artifact."""

    schema_version: int
    phase: str
    proof_run_id: str
    provider: str
    provider_mode: str
    voice: str | None
    model: str | None
    source_fixture_id: str
    text_sha256: str
    character_count: int
    audio_filename: str
    audio_format: str
    audio_sha256: str
    output_bytes: int
    sample_rate_hz: int
    channels: int
    duration_seconds: float
    generated_at: str
    cost: Mapping[str, object]

    def to_dict(self) -> dict[str, object]:
        """Render the manifest as a JSON-ready dictionary."""
        return {
            "schema_version": self.schema_version,
            "phase": self.phase,
            "proof_run_id": self.proof_run_id,
            "provider": self.provider,
            "provider_mode": self.provider_mode,
            "voice": self.voice,
            "model": self.model,
            "source_fixture_id": self.source_fixture_id,
            "text_sha256": self.text_sha256,
            "character_count": self.character_count,
            "audio_filename": self.audio_filename,
            "audio_format": self.audio_format,
            "audio_sha256": self.audio_sha256,
            "output_bytes": self.output_bytes,
            "sample_rate_hz": self.sample_rate_hz,
            "channels": self.channels,
            "duration_seconds": self.duration_seconds,
            "generated_at": self.generated_at,
            "cost": dict(self.cost),
        }

    def to_json(self) -> str:
        """Serialize the manifest to an indented, sorted JSON string."""
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)


def write_manifest(manifest: TtsManifest, path: Path) -> None:
    """Write *manifest* to *path* as JSON, creating parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(manifest.to_json(), encoding="utf-8")
