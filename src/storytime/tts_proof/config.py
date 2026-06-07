"""Phase 13I — governed local TTS proof configuration.

This is a self-contained configuration object for the Phase 13I governed TTS
proof. It is deliberately separate from the ARCH-LOCKed
:class:`storytime.config.StoryTimeConfig` (which is immutable and documented as
making no authenticated API calls): the TTS proof reads its own
``STORYTIME_TTS_*`` environment with safe defaults so it can be exercised, and
reasoned about, in isolation.

Defaults are chosen so the proof is safe and archive-clean out of the box:

* the provider is the deterministic ``mock`` (no network, no credentials);
* the real provider is disabled and requires an explicit enable flag;
* the artifact directory defaults under ``runs/`` — already git-ignored and
  already excluded by the canonical artifact builder — so generated audio,
  manifests, and audit logs can never leak into the locked archive;
* cost is a *labeled estimate* with a zero default rate, never authoritative
  provider pricing.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

# The deterministic, network-free default provider. The proof's whole claim
# stands on this provider alone.
DEFAULT_PROVIDER = "mock"

# Defaults. The artifact directory lives under runs/ on purpose: runs/ is
# git-ignored and excluded by scripts/build-artifact.sh, so runtime audio /
# manifest / audit output is archive-clean by construction.
DEFAULT_ARTIFACT_DIR = Path("runs") / "tts-proof"
DEFAULT_MAX_CHARS_PER_RUN = 1000
DEFAULT_MAX_OUTPUT_BYTES = 1_048_576  # 1 MiB
DEFAULT_COST_UNIT = "usd_per_million_chars"
DEFAULT_COST_RATE = 0.0  # labeled estimate; never authoritative provider pricing

_TRUE_TOKENS = frozenset({"1", "true", "yes", "on"})
_FALSE_TOKENS = frozenset({"0", "false", "no", "off", ""})


@dataclass(frozen=True, slots=True)
class TtsProofConfig:
    """Immutable configuration for one governed TTS proof invocation."""

    provider: str = DEFAULT_PROVIDER
    real_provider_enabled: bool = False
    max_chars_per_run: int = DEFAULT_MAX_CHARS_PER_RUN
    max_output_bytes: int = DEFAULT_MAX_OUTPUT_BYTES
    artifact_dir: Path = DEFAULT_ARTIFACT_DIR
    cost_unit: str = DEFAULT_COST_UNIT
    cost_rate: float = DEFAULT_COST_RATE

    @property
    def provider_mode(self) -> str:
        """``"mock"`` for the mock provider, ``"real"`` for anything else."""
        return "mock" if self.provider == DEFAULT_PROVIDER else "real"


def _parse_bool(value: str, *, name: str) -> bool:
    token = value.strip().lower()
    if token in _TRUE_TOKENS:
        return True
    if token in _FALSE_TOKENS:
        return False
    raise ValueError(
        f"{name} must be a boolean (true/false), got {value!r}"
    )


def _parse_positive_int(value: str, *, name: str) -> int:
    try:
        parsed = int(value.strip())
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer, got {value!r}") from exc
    if parsed <= 0:
        raise ValueError(f"{name} must be a positive integer, got {parsed}")
    return parsed


def _parse_non_negative_float(value: str, *, name: str) -> float:
    try:
        parsed = float(value.strip())
    except ValueError as exc:
        raise ValueError(f"{name} must be a number, got {value!r}") from exc
    if parsed < 0:
        raise ValueError(f"{name} must be non-negative, got {parsed}")
    return parsed


def load_tts_proof_config(
    environ: dict[str, str] | None = None,
) -> TtsProofConfig:
    """Build a :class:`TtsProofConfig` from *environ* (defaults to os.environ).

    Misconfiguration fails fast with ``ValueError`` rather than surfacing
    mid-generation. The mock provider and a disabled real provider are the
    defaults, so a bare environment yields a safe, network-free configuration.
    """
    env = dict(os.environ) if environ is None else environ

    provider = env.get("STORYTIME_TTS_PROVIDER", DEFAULT_PROVIDER).strip() or DEFAULT_PROVIDER
    real_provider_enabled = _parse_bool(
        env.get("STORYTIME_TTS_REAL_PROVIDER_ENABLED", "false"),
        name="STORYTIME_TTS_REAL_PROVIDER_ENABLED",
    )
    max_chars_per_run = _parse_positive_int(
        env.get("STORYTIME_TTS_MAX_CHARS_PER_RUN", str(DEFAULT_MAX_CHARS_PER_RUN)),
        name="STORYTIME_TTS_MAX_CHARS_PER_RUN",
    )
    max_output_bytes = _parse_positive_int(
        env.get("STORYTIME_TTS_MAX_OUTPUT_BYTES", str(DEFAULT_MAX_OUTPUT_BYTES)),
        name="STORYTIME_TTS_MAX_OUTPUT_BYTES",
    )
    artifact_dir = Path(
        env.get("STORYTIME_TTS_ARTIFACT_DIR", str(DEFAULT_ARTIFACT_DIR))
    )
    cost_unit = (
        env.get("STORYTIME_TTS_COST_UNIT", DEFAULT_COST_UNIT).strip()
        or DEFAULT_COST_UNIT
    )
    cost_rate = _parse_non_negative_float(
        env.get("STORYTIME_TTS_COST_RATE", str(DEFAULT_COST_RATE)),
        name="STORYTIME_TTS_COST_RATE",
    )

    return TtsProofConfig(
        provider=provider,
        real_provider_enabled=real_provider_enabled,
        max_chars_per_run=max_chars_per_run,
        max_output_bytes=max_output_bytes,
        artifact_dir=artifact_dir,
        cost_unit=cost_unit,
        cost_rate=cost_rate,
    )
