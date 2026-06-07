"""Phase 13I — governed local TTS proof behavioral tests.

These prove the governed boundary end to end with the deterministic mock
provider: no credentials, no network. They exercise the happy path (artifact +
manifest + audit events + cost), every guard rejection, fail-closed real
provider handling, no-partial-artifact on execution failure, path-traversal /
symlink rejection, the output-size cap, observability-safe metadata (text hash,
never raw text), deterministic mock output, and fail-fast config parsing.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from storytime.adapters.tts.base import TTSResult
from storytime.tts_proof import (
    DEFAULT_FIXTURE_ID,
    TtsProofConfig,
    load_tts_proof_config,
    run_tts_proof,
)
from storytime.tts_proof.boundary import (
    AUDIO_FILENAME,
    MANIFEST_FILENAME,
    load_fixture_text,
    validate_artifact_target,
)
from storytime.tts_proof.events import TtsFailureReason, TtsProofEventType
from storytime.util.clock import FixedClock

_FIXED = FixedClock(datetime(2026, 5, 28, 12, 0, 0, tzinfo=UTC))
# A distinctive substring of the approved fixture, used to prove raw text never
# leaks into events, audit, or manifest.
_RAW_TEXT_MARKER = "approved fixture for the deterministic mock"


def _cfg(tmp_path: Path, **overrides: object) -> TtsProofConfig:
    base: dict[str, object] = {"artifact_dir": tmp_path / "tts"}
    base.update(overrides)
    return TtsProofConfig(**base)  # type: ignore[arg-type]


def _event_types(result_events: tuple[object, ...]) -> list[str]:
    return [str(e.event_type) for e in result_events]  # type: ignore[attr-defined]


# ── mock is the default ───────────────────────────────────────────────────────


def test_mock_is_the_default_provider() -> None:
    config = load_tts_proof_config({})
    assert config.provider == "mock"
    assert config.provider_mode == "mock"
    assert config.real_provider_enabled is False


# ── happy path ────────────────────────────────────────────────────────────────


def test_governed_mock_generation_produces_artifact_manifest_events_cost(
    tmp_path: Path,
) -> None:
    result = run_tts_proof(_cfg(tmp_path), clock=_FIXED)
    assert result.ok
    assert result.provider == "mock" and result.provider_mode == "mock"
    assert result.artifact_path is not None and result.artifact_path.is_file()
    assert result.manifest_path is not None and result.manifest_path.is_file()
    # Audit log written beside the artifact.
    audit = result.artifact_path.parent / "audit.jsonl"
    assert audit.is_file()
    # Lifecycle: requested -> executing -> completed.
    assert _event_types(result.events) == [
        TtsProofEventType.REQUESTED,
        TtsProofEventType.EXECUTING,
        TtsProofEventType.COMPLETED,
    ]
    # Cost metadata present and labeled an estimate.
    assert result.cost["is_estimate"] is True
    assert result.cost["character_count"] == result.character_count
    # Manifest marks the mock provider explicitly.
    manifest = json.loads(result.manifest_path.read_text())
    assert manifest["provider"] == "mock"
    assert manifest["provider_mode"] == "mock"
    assert manifest["phase"] == "13I"
    assert manifest["audio_sha256"] == result.audio_sha256


def test_success_leaves_exactly_the_expected_files(tmp_path: Path) -> None:
    result = run_tts_proof(_cfg(tmp_path), clock=_FIXED)
    assert result.artifact_path is not None
    run_dir = result.artifact_path.parent
    names = sorted(p.name for p in run_dir.iterdir())
    assert names == sorted([AUDIO_FILENAME, MANIFEST_FILENAME, "audit.jsonl"])
    # No leftover temp/partial file.
    assert not any(p.name.endswith(".partial") for p in run_dir.iterdir())


# ── guard rejections ─────────────────────────────────────────────────────────


def test_over_character_limit_rejected_before_execution(tmp_path: Path) -> None:
    result = run_tts_proof(_cfg(tmp_path, max_chars_per_run=5), clock=_FIXED)
    assert not result.ok
    assert result.failure_reason == TtsFailureReason.CHARACTER_LIMIT_EXCEEDED
    # Rejected before any provider execution: the lifecycle never reaches
    # EXECUTING — only REQUESTED then GUARD_REJECTED.
    assert _event_types(result.events) == [
        TtsProofEventType.REQUESTED,
        TtsProofEventType.GUARD_REJECTED,
    ]
    assert TtsProofEventType.EXECUTING not in _event_types(result.events)
    # No artifact produced.
    assert not list((tmp_path / "tts").rglob(AUDIO_FILENAME))


def test_non_allowlisted_fixture_rejected(tmp_path: Path) -> None:
    result = run_tts_proof(_cfg(tmp_path), fixture_id="not-approved", clock=_FIXED)
    assert not result.ok
    assert result.failure_reason == TtsFailureReason.FIXTURE_NOT_ALLOWLISTED


def test_real_provider_disabled_fails_closed_and_is_audited(tmp_path: Path) -> None:
    result = run_tts_proof(
        _cfg(tmp_path, provider="elevenlabs", real_provider_enabled=False),
        clock=_FIXED,
    )
    assert not result.ok
    assert result.provider_mode == "real"
    assert result.failure_reason == TtsFailureReason.PROVIDER_DISABLED
    assert _event_types(result.events) == [
        TtsProofEventType.REQUESTED,
        TtsProofEventType.GUARD_REJECTED,
    ]
    # The rejection was audited to disk.
    run_dir = tmp_path / "tts" / result.proof_run_id
    audit = run_dir / "audit.jsonl"
    assert audit.is_file()
    assert "guard_rejected" in audit.read_text()


def test_real_provider_enabled_but_unbundled_still_fails_closed(tmp_path: Path) -> None:
    result = run_tts_proof(
        _cfg(tmp_path, provider="elevenlabs", real_provider_enabled=True),
        clock=_FIXED,
    )
    assert not result.ok
    assert result.failure_reason == TtsFailureReason.PROVIDER_DISABLED


# ── execution failure: no partial artifact, typed failed event ───────────────


class _FailingAdapter:
    """A TTS adapter that always raises — and whose error echoes the text, to
    prove the boundary redacts it."""

    name = "failing"
    version = "0.0.0"

    def synthesize(
        self, text: str, *, out_path: Path, voice: str | None = None,
        sample_rate_hz: int = 22050,
    ) -> TTSResult:
        raise RuntimeError(f"provider blew up and leaked: {text}")


def test_simulated_provider_failure_leaves_no_partial_artifact(tmp_path: Path) -> None:
    result = run_tts_proof(
        _cfg(tmp_path), clock=_FIXED, adapter_override=_FailingAdapter()
    )
    assert not result.ok
    assert result.failure_reason == TtsFailureReason.PROVIDER_ERROR
    assert _event_types(result.events) == [
        TtsProofEventType.REQUESTED,
        TtsProofEventType.EXECUTING,
        TtsProofEventType.FAILED,
    ]
    # No audio artifact, no manifest, no partial temp file.
    run_dir = tmp_path / "tts" / result.proof_run_id
    assert not (run_dir / AUDIO_FILENAME).exists()
    assert not (run_dir / MANIFEST_FILENAME).exists()
    assert not any(p.name.endswith(".partial") for p in run_dir.iterdir())
    # The verbatim provider error (which echoed the text) is redacted.
    assert result.message is not None
    assert "blew up" not in result.message
    assert _RAW_TEXT_MARKER not in result.message


# ── path traversal / symlink escape ──────────────────────────────────────────


def test_path_traversal_and_absolute_paths_rejected(tmp_path: Path) -> None:
    base = tmp_path / "tts"
    assert validate_artifact_target(base, "run1", "../escape.wav") is None
    assert validate_artifact_target(base, "..", "audio.wav") is None
    assert validate_artifact_target(base, "run1", "/etc/passwd") is None
    assert validate_artifact_target(base, "a/b", "audio.wav") is None
    # A safe target resolves within the controlled directory.
    assert validate_artifact_target(base, "run1", "audio.wav") is not None


def test_symlink_escape_rejected(tmp_path: Path) -> None:
    base = tmp_path / "tts"
    base.mkdir(parents=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    link = base / "runlink"
    link.symlink_to(outside, target_is_directory=True)
    # The run dir is a symlink pointing outside the controlled directory.
    assert validate_artifact_target(base, "runlink", "audio.wav") is None


# ── output-size cap ───────────────────────────────────────────────────────────


def test_output_size_cap_enforced(tmp_path: Path) -> None:
    result = run_tts_proof(_cfg(tmp_path, max_output_bytes=100), clock=_FIXED)
    assert not result.ok
    assert result.failure_reason == TtsFailureReason.OUTPUT_LIMIT_EXCEEDED
    assert _event_types(result.events) == [
        TtsProofEventType.REQUESTED,
        TtsProofEventType.EXECUTING,
        TtsProofEventType.FAILED,
    ]
    run_dir = tmp_path / "tts" / result.proof_run_id
    assert not (run_dir / AUDIO_FILENAME).exists()
    assert not any(p.name.endswith(".partial") for p in run_dir.iterdir())


# ── observability-safe metadata ──────────────────────────────────────────────


def test_events_audit_and_manifest_carry_text_hash_not_raw_text(
    tmp_path: Path,
) -> None:
    result = run_tts_proof(_cfg(tmp_path), clock=_FIXED)
    assert result.ok and result.artifact_path is not None
    run_dir = result.artifact_path.parent
    # Confirm the marker is actually in the fixture (guards the test itself).
    assert _RAW_TEXT_MARKER in (load_fixture_text(DEFAULT_FIXTURE_ID) or "")
    text_hash = json.loads(result.manifest_path.read_text())["text_sha256"]  # type: ignore[union-attr]
    # Raw text must not appear in any event payload, the audit log, or manifest.
    for event in result.events:
        assert _RAW_TEXT_MARKER not in event.to_json_line()
        assert text_hash in event.to_json_line() or event.event_type in (
            TtsProofEventType.REQUESTED,
        )
    audit_text = (run_dir / "audit.jsonl").read_text()
    assert _RAW_TEXT_MARKER not in audit_text
    assert text_hash in audit_text
    manifest_text = (run_dir / MANIFEST_FILENAME).read_text()
    assert _RAW_TEXT_MARKER not in manifest_text
    assert text_hash in manifest_text


# ── deterministic mock output ─────────────────────────────────────────────────


def test_mock_output_is_deterministic(tmp_path: Path) -> None:
    first = run_tts_proof(_cfg(tmp_path / "a"), clock=_FIXED)
    second = run_tts_proof(_cfg(tmp_path / "b"), clock=_FIXED)
    assert first.ok and second.ok
    assert first.audio_sha256 == second.audio_sha256
    assert first.output_bytes == second.output_bytes


# ── cost accounting shared + labeled estimate ────────────────────────────────


def test_cost_is_labeled_estimate_and_uses_configured_rate(tmp_path: Path) -> None:
    result = run_tts_proof(
        _cfg(tmp_path, cost_rate=4.0, cost_unit="usd_per_million_chars"),
        clock=_FIXED,
    )
    assert result.ok and result.character_count is not None
    cost = dict(result.cost)
    assert cost["is_estimate"] is True
    assert cost["unit"] == "usd_per_million_chars"
    assert cost["rate"] == 4.0
    expected = round((result.character_count / 1_000_000) * 4.0, 6)
    assert cost["amount"] == expected


# ── fail-fast config ──────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "env",
    [
        {"STORYTIME_TTS_REAL_PROVIDER_ENABLED": "maybe"},
        {"STORYTIME_TTS_MAX_CHARS_PER_RUN": "-5"},
        {"STORYTIME_TTS_MAX_CHARS_PER_RUN": "notanint"},
        {"STORYTIME_TTS_MAX_OUTPUT_BYTES": "0"},
        {"STORYTIME_TTS_COST_RATE": "free"},
    ],
)
def test_config_fails_fast_on_bad_env(env: dict[str, str]) -> None:
    with pytest.raises(ValueError):
        load_tts_proof_config(env)
