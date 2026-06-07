"""Phase 13I — the governed local TTS boundary.

This module is the Phase 13I proof: it takes a tiny approved text fixture and
drives it through a governed, observable, auditable boundary to a local audio
artifact, using the existing deterministic :class:`MockTTS` adapter. The chain
is::

    approved fixture
      -> governance / cost guard
      -> deterministic mock TTS provider
      -> atomic local audio artifact
      -> manifest beside the artifact
      -> structured audit/event records
      -> observability-safe metadata

The whole proof stands with **no provider credentials and no network access**:
the default provider is the in-process mock, and a non-mock ("real") provider
fails closed unless an explicit enable flag is set — and no real adapter is
bundled in this phase, so a real selection still fails closed with a typed
reason. Generation is invokable only from the backend/CLI; it adds no local
bridge action and never touches the browser.

Safety properties enforced here:

* guard rejection happens *before* any provider call and is audited;
* replacement-free, all-or-nothing artifact writing: synthesis goes to a temp
  file, the output-byte cap is enforced, and only then is the file atomically
  renamed into place — a failure leaves no partial artifact;
* the artifact path is validated against traversal, absolute-path, and symlink
  escape, and must resolve within the controlled artifact directory;
* audit records and telemetry-safe metadata carry a text *hash* and length,
  never the raw fixture text, never credentials, never verbatim provider
  errors.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

from storytime.adapters.tts.base import TTSAdapter
from storytime.adapters.tts.mock import MockTTS
from storytime.tts_proof.config import DEFAULT_PROVIDER, TtsProofConfig
from storytime.tts_proof.events import (
    TtsFailureReason,
    TtsProofEvent,
    TtsProofEventType,
)
from storytime.tts_proof.manifest import (
    TTS_MANIFEST_SCHEMA_VERSION,
    TtsManifest,
    write_manifest,
)
from storytime.util.clock import Clock, SystemClock
from storytime.util.hashing import sha256_text

PHASE_LABEL = "13I"

AUDIO_FILENAME = "audio.wav"
MANIFEST_FILENAME = "manifest.json"
AUDIT_FILENAME = "audit.jsonl"
_TEMP_SUFFIX = ".partial"

# The single approved fixture allowlist: id -> filename under fixtures/.
_FIXTURES_DIR = Path(__file__).parent / "fixtures"
_FIXTURE_ALLOWLIST: dict[str, str] = {
    "approved-proof-fixture": "approved_proof_fixture.txt",
}
DEFAULT_FIXTURE_ID = "approved-proof-fixture"

# Real provider adapters bundled in this phase. Intentionally empty: the proof
# is mock-only, so any non-mock selection fails closed even when enabled.
_BUNDLED_REAL_PROVIDERS: frozenset[str] = frozenset()


class ProviderUnavailableError(RuntimeError):
    """Raised when a requested provider has no bundled adapter."""


# ── result type ──────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class TtsProofResult:
    """The outcome of one governed TTS proof invocation."""

    ok: bool
    proof_run_id: str
    provider: str
    provider_mode: str
    events: tuple[TtsProofEvent, ...]
    # Present on success:
    artifact_path: Path | None = None
    manifest_path: Path | None = None
    audio_sha256: str | None = None
    character_count: int | None = None
    output_bytes: int | None = None
    duration_seconds: float | None = None
    cost: Mapping[str, object] = field(default_factory=dict)
    # Present on failure:
    failure_reason: TtsFailureReason | None = None
    message: str | None = None


# ── fixture allowlist ─────────────────────────────────────────────────────────


def is_fixture_allowlisted(fixture_id: str) -> bool:
    """True if *fixture_id* names an approved, allowlisted fixture."""
    return fixture_id in _FIXTURE_ALLOWLIST


def load_fixture_text(fixture_id: str) -> str | None:
    """Return the approved fixture text, or ``None`` if not allowlisted."""
    filename = _FIXTURE_ALLOWLIST.get(fixture_id)
    if filename is None:
        return None
    return (_FIXTURES_DIR / filename).read_text(encoding="utf-8")


# ── path safety ────────────────────────────────────────────────────────────────


def is_safe_segment(name: str) -> bool:
    """True if *name* is a single safe path segment (no traversal/separators)."""
    if name in ("", ".", ".."):
        return False
    if "/" in name or "\\" in name or "\x00" in name:
        return False
    if name.startswith("."):
        return False
    return not os.path.isabs(name)


def resolve_within(base: Path, candidate: Path) -> Path | None:
    """Resolve *candidate* and return it only if it is within *base*.

    ``resolve()`` collapses ``..`` and symlinks, so a symlink that escapes the
    controlled directory is caught here and rejected.
    """
    base_resolved = base.resolve()
    candidate_resolved = candidate.resolve()
    try:
        candidate_resolved.relative_to(base_resolved)
    except ValueError:
        return None
    return candidate_resolved


def validate_artifact_target(
    artifact_dir: Path, run_id: str, filename: str
) -> Path | None:
    """Validate and resolve ``artifact_dir/run_id/filename`` within the dir.

    Returns the resolved absolute path, or ``None`` if the run id or filename
    is unsafe or the resolved path escapes the controlled artifact directory.
    """
    if not (is_safe_segment(run_id) and is_safe_segment(filename)):
        return None
    return resolve_within(artifact_dir, artifact_dir / run_id / filename)


# ── cost accounting (shared by every provider path) ─────────────────────────────


def estimate_cost(
    character_count: int,
    config: TtsProofConfig,
    *,
    provider: str,
    provider_mode: str,
    voice: str | None,
    model: str | None,
) -> dict[str, object]:
    """Return a labeled cost *estimate* record.

    This is the single accounting code path used regardless of provider, so the
    mock exercises exactly the accounting any real provider would. The rate is
    a configurable estimate (zero by default) and is never authoritative
    provider pricing.
    """
    rate = config.cost_rate
    if config.cost_unit == "usd_per_million_chars":
        amount = (character_count / 1_000_000) * rate
    else:
        # Unknown unit: record the rate but do not invent an amount.
        amount = 0.0
    return {
        "is_estimate": True,
        "provider": provider,
        "provider_mode": provider_mode,
        "voice": voice,
        "model": model,
        "character_count": character_count,
        "unit": config.cost_unit,
        "rate": rate,
        "amount": round(amount, 6),
    }


# ── provider resolution ──────────────────────────────────────────────────────


def resolve_adapter(provider: str, *, real_provider_enabled: bool) -> TTSAdapter:
    """Resolve a provider name to a TTS adapter.

    Only the mock is bundled in this phase. A non-mock provider raises
    :class:`ProviderUnavailableError`; the boundary's guard rejects non-mock
    selections before this is ever reached in normal operation.
    """
    if provider == DEFAULT_PROVIDER:
        return MockTTS()
    raise ProviderUnavailableError(
        f"no bundled adapter for provider {provider!r} in this phase"
    )


def _classify_execution_error(error: Exception) -> TtsFailureReason:
    """Map an execution exception to a typed, safe failure reason."""
    if isinstance(error, OSError):
        return TtsFailureReason.WRITE_FAILED
    if isinstance(error, ProviderUnavailableError):
        return TtsFailureReason.PROVIDER_DISABLED
    return TtsFailureReason.PROVIDER_ERROR


# ── audit sink ─────────────────────────────────────────────────────────────────


def write_audit(run_dir: Path, events: tuple[TtsProofEvent, ...]) -> None:
    """Write the event records as JSONL into the run directory (best-effort).

    Audit persistence never raises into the caller: the structured events are
    always returned in the result regardless of whether the file could be
    written (e.g. when the failure *is* an invalid artifact path).
    """
    try:
        run_dir.mkdir(parents=True, exist_ok=True)
        lines = "".join(event.to_json_line() + "\n" for event in events)
        (run_dir / AUDIT_FILENAME).write_text(lines, encoding="utf-8")
    except OSError:
        return


# ── the governed boundary ──────────────────────────────────────────────────────


def run_tts_proof(
    config: TtsProofConfig,
    *,
    fixture_id: str = DEFAULT_FIXTURE_ID,
    clock: Clock | None = None,
    adapter_override: TTSAdapter | None = None,
) -> TtsProofResult:
    """Run one governed TTS proof and return a typed result.

    Invoked only from the backend/CLI. ``adapter_override`` exists for tests
    (e.g. to inject a deliberately failing provider); production resolves the
    adapter from the validated provider name.
    """
    the_clock = clock if clock is not None else SystemClock()
    from storytime.util.ids import new_ulid

    proof_run_id = new_ulid()
    provider = config.provider
    mode = config.provider_mode
    events: list[TtsProofEvent] = []

    def emit(event_type: TtsProofEventType, payload: dict[str, object]) -> None:
        events.append(
            TtsProofEvent(
                event_type=event_type,
                proof_run_id=proof_run_id,
                occurred_at=the_clock.now(),
                payload=payload,
            )
        )

    run_dir = config.artifact_dir / proof_run_id

    def guard_reject(reason: TtsFailureReason, message: str) -> TtsProofResult:
        emit(
            TtsProofEventType.GUARD_REJECTED,
            {"provider": provider, "provider_mode": mode, "reason": str(reason)},
        )
        write_audit(run_dir, tuple(events))
        return TtsProofResult(
            ok=False,
            proof_run_id=proof_run_id,
            provider=provider,
            provider_mode=mode,
            events=tuple(events),
            failure_reason=reason,
            message=message,
        )

    def fail(reason: TtsFailureReason, message: str) -> TtsProofResult:
        emit(
            TtsProofEventType.FAILED,
            {"provider": provider, "provider_mode": mode, "reason": str(reason)},
        )
        write_audit(run_dir, tuple(events))
        return TtsProofResult(
            ok=False,
            proof_run_id=proof_run_id,
            provider=provider,
            provider_mode=mode,
            events=tuple(events),
            failure_reason=reason,
            message=message,
        )

    emit(
        TtsProofEventType.REQUESTED,
        {"provider": provider, "provider_mode": mode, "fixture_id": fixture_id},
    )

    # ── guard: provider / real-provider enablement ──────────────────────────
    if mode == "real" and not config.real_provider_enabled:
        return guard_reject(
            TtsFailureReason.PROVIDER_DISABLED,
            "real provider is disabled; set STORYTIME_TTS_REAL_PROVIDER_ENABLED",
        )
    if mode == "real" and provider not in _BUNDLED_REAL_PROVIDERS:
        return guard_reject(
            TtsFailureReason.PROVIDER_DISABLED,
            "no real provider adapter is bundled in this phase",
        )

    # ── guard: fixture allowlist ─────────────────────────────────────────────
    if not is_fixture_allowlisted(fixture_id):
        return guard_reject(
            TtsFailureReason.FIXTURE_NOT_ALLOWLISTED,
            f"fixture {fixture_id!r} is not allowlisted",
        )
    text = load_fixture_text(fixture_id)
    if text is None:  # pragma: no cover - allowlist guarantees text
        return guard_reject(
            TtsFailureReason.FIXTURE_NOT_ALLOWLISTED,
            f"fixture {fixture_id!r} could not be loaded",
        )
    character_count = len(text)
    text_hash = sha256_text(text)

    # ── guard: character cap (before any provider execution) ─────────────────
    if character_count > config.max_chars_per_run:
        return guard_reject(
            TtsFailureReason.CHARACTER_LIMIT_EXCEEDED,
            f"input {character_count} chars exceeds cap {config.max_chars_per_run}",
        )

    # ── guard: artifact path within the controlled directory ─────────────────
    final_path = validate_artifact_target(
        config.artifact_dir, proof_run_id, AUDIO_FILENAME
    )
    if final_path is None:
        return guard_reject(
            TtsFailureReason.PATH_INVALID,
            "artifact path does not resolve within the controlled directory",
        )

    # ── cost estimate (recorded regardless of provider) ──────────────────────
    adapter = adapter_override or resolve_adapter(
        provider, real_provider_enabled=config.real_provider_enabled
    )
    voice: str | None = None
    model = f"{adapter.name}:{adapter.version}"
    cost = estimate_cost(
        character_count,
        config,
        provider=provider,
        provider_mode=mode,
        voice=voice,
        model=model,
    )

    emit(
        TtsProofEventType.EXECUTING,
        {
            "provider": provider,
            "provider_mode": mode,
            "model": model,
            "character_count": character_count,
            "text_sha256": text_hash,
            "cost": cost,
        },
    )

    # ── execute: synthesize to a temp path, never directly to the final ──────
    run_dir.mkdir(parents=True, exist_ok=True)
    temp_path = final_path.with_name(AUDIO_FILENAME + _TEMP_SUFFIX)
    try:
        synth = adapter.synthesize(text, out_path=temp_path, voice=voice)
    except Exception as error:  # noqa: BLE001 - mapped to a typed, redacted reason
        temp_path.unlink(missing_ok=True)
        reason = _classify_execution_error(error)
        # Redacted: the verbatim error text is never logged or returned.
        return fail(reason, "provider execution failed (details redacted)")

    # ── output-size cap (post-synthesis, pre-rename) ─────────────────────────
    output_bytes = temp_path.stat().st_size
    if output_bytes > config.max_output_bytes:
        temp_path.unlink(missing_ok=True)
        return fail(
            TtsFailureReason.OUTPUT_LIMIT_EXCEEDED,
            f"output {output_bytes} bytes exceeds cap {config.max_output_bytes}",
        )

    # ── atomic publish: temp -> final ────────────────────────────────────────
    try:
        os.replace(temp_path, final_path)
    except OSError:
        temp_path.unlink(missing_ok=True)
        return fail(TtsFailureReason.WRITE_FAILED, "artifact rename failed")

    # ── manifest beside the artifact ─────────────────────────────────────────
    manifest = TtsManifest(
        schema_version=TTS_MANIFEST_SCHEMA_VERSION,
        phase=PHASE_LABEL,
        proof_run_id=proof_run_id,
        provider=provider,
        provider_mode=mode,
        voice=voice,
        model=model,
        source_fixture_id=fixture_id,
        text_sha256=text_hash,
        character_count=character_count,
        audio_filename=AUDIO_FILENAME,
        audio_format=synth.audio_format,
        audio_sha256=synth.audio_sha256,
        output_bytes=output_bytes,
        sample_rate_hz=synth.sample_rate_hz,
        channels=synth.channels,
        duration_seconds=synth.duration_seconds,
        generated_at=the_clock.now().isoformat(),
        cost=cost,
    )
    manifest_path = run_dir / MANIFEST_FILENAME
    write_manifest(manifest, manifest_path)

    emit(
        TtsProofEventType.COMPLETED,
        {
            "provider": provider,
            "provider_mode": mode,
            "voice": voice,
            "model": model,
            "character_count": character_count,
            "text_sha256": text_hash,
            "audio_sha256": synth.audio_sha256,
            "output_bytes": output_bytes,
            "duration_seconds": synth.duration_seconds,
            "cost": cost,
            "artifact_filename": AUDIO_FILENAME,
            "manifest_filename": MANIFEST_FILENAME,
            "result": "completed",
        },
    )
    write_audit(run_dir, tuple(events))

    return TtsProofResult(
        ok=True,
        proof_run_id=proof_run_id,
        provider=provider,
        provider_mode=mode,
        events=tuple(events),
        artifact_path=final_path,
        manifest_path=manifest_path,
        audio_sha256=synth.audio_sha256,
        character_count=character_count,
        output_bytes=output_bytes,
        duration_seconds=synth.duration_seconds,
        cost=cost,
    )
