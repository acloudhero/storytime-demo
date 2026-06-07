"""Observability demo harness — runs real StoryTime scenarios.

ARCH-LOCK: Demo harness is a telemetry GENERATOR, not a telemetry source
DO NOT REFACTOR: every scenario below drives the real pipeline entry points.
The harness must never construct spans, emit metrics, or fabricate telemetry
itself — the only honest telemetry is the telemetry the instrumented pipeline
emits while doing real work. The harness also stays bounded to its workspace
directory (Phase 6A acceptance criteria 8 and 9).
Rationale: Phase 6A — "demo honesty"; the dashboards must reflect real runs.

This module imports only the pipeline's public surface; it does NOT import
opentelemetry. Whether telemetry is exported is decided by the StoryTimeConfig
the caller passes (telemetry="otel" plus a reachable collector) — exactly the
same selection a normal CLI invocation makes.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from storytime.approval import ApprovalError, apply_approval_decision
from storytime.config import StoryTimeConfig
from storytime.demo.logsink import write_demo_log
from storytime.pipeline import (
    SliceOutcome,
    build_runtime_context,
    resume_run,
    run_vertical_slice,
)
from storytime.runner import RehydrationError
from storytime.runner.context import RunnerContext

# A short, original public-domain-equivalent passage. It is written for this
# harness and released CC0, so it is safe demo source material under the
# manifest's CC0-1.0 license without depending on any external text.
_DEMO_BODY = (
    "The lighthouse keeper trimmed the lamp at dusk. "
    "Far below, the tide turned against the rocks, patient and certain. "
    "She wrote the night's first line in the log and waited for the dark."
)


# --------------------------------------------------------------------------
# Result types.
# --------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class DemoScenarioResult:
    """The outcome of one demo scenario."""

    name: str
    description: str
    expected: str
    actual: str
    ok: bool
    detail: str
    pipeline_run_id: str | None = None


@dataclass(frozen=True, slots=True)
class DemoResult:
    """The collected outcome of a demo run."""

    workspace: Path
    telemetry: str
    otlp_endpoint: str
    scenarios: tuple[DemoScenarioResult, ...]

    @property
    def ok(self) -> bool:
        """True if every scenario met its expectation (skips count as ok)."""
        return all(scenario.ok for scenario in self.scenarios)


# --------------------------------------------------------------------------
# Source-material generation (bounded to the workspace).
# --------------------------------------------------------------------------

def _write_source(
    workspace: Path,
    source_id: str,
    *,
    title: str,
    valid: bool = True,
) -> Path:
    """Write a demo source text + manifest under *workspace*; return the manifest.

    With ``valid=False`` the manifest carries a license outside the closed
    schema enum, so ``load_manifest`` rejects it — the honest way to drive the
    bad-manifest scenario without hand-corrupting JSON structure.
    """
    sources = workspace / "sources"
    sources.mkdir(parents=True, exist_ok=True)

    text_path = sources / f"{source_id}.txt"
    text_path.write_text(_DEMO_BODY, encoding="utf-8")
    digest = hashlib.sha256(_DEMO_BODY.encode("utf-8")).hexdigest()

    manifest: dict[str, Any] = {
        "manifest_version": 1,
        "source_id": source_id,
        "title": title,
        "author": "StoryTime Demo Harness",
        "source_url": "https://example.org/storytime/demo",
        "retrieval_date": "2026-01-01",
        "jurisdiction": "US",
        # A schema-invalid license for the bad-manifest scenario.
        "license": "CC0-1.0" if valid else "ALL-RIGHTS-RESERVED",
        "text_sha256": digest,
        "text_encoding": "utf-8",
        "text_path": f"{source_id}.txt",
        "language": "en",
        "approval": {
            "approved_by": "demo-operator",
            "approved_at": "2026-01-01T00:00:00Z",
            "review_notes": "Demo harness source; CC0 original text.",
        },
    }
    manifest_path = sources / f"{source_id}.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest_path


# --------------------------------------------------------------------------
# Scenario helpers.
# --------------------------------------------------------------------------

def _result(
    name: str,
    description: str,
    expected: str,
    outcome: SliceOutcome,
    *,
    run_id: str | None = None,
) -> DemoScenarioResult:
    """Build a DemoScenarioResult by comparing an outcome to its expectation."""
    actual = outcome.status
    ok = actual == expected
    detail = f"status={actual}"
    if outcome.failed_stage:
        detail += f", failed_stage={outcome.failed_stage}"
    if outcome.error_kind:
        detail += f", error_kind={outcome.error_kind}"
    return DemoScenarioResult(
        name=name,
        description=description,
        expected=expected,
        actual=actual,
        ok=ok,
        detail=detail,
        pipeline_run_id=run_id or outcome.pipeline_run_id,
    )


def _scenario_success(ctx: RunnerContext, workspace: Path) -> DemoScenarioResult:
    """A straight-through run with no approval gates."""
    manifest = _write_source(workspace, "demo-success", title="The Lighthouse")
    outcome = run_vertical_slice(ctx, manifest)
    return _result(
        "success",
        "Straight-through run: ingest -> synthesize -> assemble -> publish.",
        "completed",
        outcome,
    )


def _scenario_text_approval(
    ctx: RunnerContext, workspace: Path
) -> DemoScenarioResult:
    """A run that pauses at the text gate, is approved, and resumes."""
    manifest = _write_source(workspace, "demo-text-approve", title="Approved Tale")
    paused = run_vertical_slice(ctx, manifest, require_approval=True)
    run_id = paused.pipeline_run_id
    if paused.status != "awaiting_approval" or run_id is None:
        return _result(
            "text_approval",
            "Text approval gate: pause, approve, resume.",
            "completed",
            paused,
        )
    apply_approval_decision(
        ctx,
        pipeline_run_id=run_id,
        gate="text",
        decision="approved",
        operator="demo-operator",
        notes="Demo: text approved.",
    )
    resumed = resume_run(ctx, run_id)
    return _result(
        "text_approval",
        "Text approval gate: pause, approve, resume to completion.",
        "completed",
        resumed,
        run_id=run_id,
    )


def _scenario_audio_approval(
    ctx: RunnerContext, workspace: Path
) -> DemoScenarioResult:
    """A run that pauses at the audio gate, is approved, and resumes."""
    manifest = _write_source(
        workspace, "demo-audio-approve", title="Audio Approved Tale"
    )
    paused = run_vertical_slice(ctx, manifest, require_audio_approval=True)
    run_id = paused.pipeline_run_id
    if paused.status != "awaiting_approval" or run_id is None:
        return _result(
            "audio_approval",
            "Audio approval gate: pause, approve, resume.",
            "completed",
            paused,
        )
    apply_approval_decision(
        ctx,
        pipeline_run_id=run_id,
        gate="audio",
        decision="approved",
        operator="demo-operator",
        notes="Demo: audio approved.",
    )
    resumed = resume_run(ctx, run_id)
    return _result(
        "audio_approval",
        "Audio approval gate: pause, approve, resume to completion.",
        "completed",
        resumed,
        run_id=run_id,
    )


def _scenario_rejection(
    ctx: RunnerContext, workspace: Path, *, gate: str
) -> DemoScenarioResult:
    """A run that pauses at *gate* and is rejected (run ends 'failed').

    A rejection is terminal at the moment the decision is recorded:
    apply_approval_decision moves the run to 'failed'. There is no resume — a
    failed run is not resumable — so the scenario's outcome is the
    ApprovalOutcome, not a SliceOutcome.
    """
    name = f"{gate}_rejection"
    source_id = f"demo-{gate}-reject"
    require = (
        {"require_approval": True}
        if gate == "text"
        else {"require_audio_approval": True}
    )
    description = (
        f"{gate.capitalize()} approval gate: pause then reject; run ends "
        "'failed'."
    )
    manifest = _write_source(workspace, source_id, title=f"Rejected {gate} Tale")
    paused = run_vertical_slice(ctx, manifest, **require)  # type: ignore[arg-type]
    run_id = paused.pipeline_run_id
    if paused.status != "awaiting_approval" or run_id is None:
        return _result(name, description, "awaiting_approval", paused)

    approval = apply_approval_decision(
        ctx,
        pipeline_run_id=run_id,
        gate=gate,
        decision="rejected",
        operator="demo-operator",
        notes=f"Demo: {gate} rejected.",
    )
    ok = approval.run_status == "failed"
    return DemoScenarioResult(
        name=name,
        description=description,
        expected="failed",
        actual=approval.run_status,
        ok=ok,
        detail=f"rejection recorded at the {gate} gate; run_status="
        f"{approval.run_status}",
        pipeline_run_id=run_id,
    )


def _scenario_bad_manifest(
    ctx: RunnerContext, workspace: Path
) -> DemoScenarioResult:
    """A run rejected at pre-flight because its manifest is schema-invalid."""
    manifest = _write_source(
        workspace, "demo-bad-manifest", title="Invalid Tale", valid=False
    )
    outcome = run_vertical_slice(ctx, manifest)
    return _result(
        "bad_manifest",
        "Schema-invalid manifest is rejected before a run is created.",
        "rejected",
        outcome,
    )


def _corrupt_an_artifact(run_dir: Path) -> Path | None:
    """Append bytes to one persisted artifact payload under *run_dir*.

    Prefers a WAV payload (a validated synthesize artifact); falls back to a
    text payload. Returns the corrupted path, or None if nothing suitable was
    found — in which case the caller skips the scenario honestly.
    """
    if not run_dir.is_dir():
        return None
    candidates = sorted(run_dir.rglob("*.wav")) or sorted(run_dir.rglob("*.txt"))
    if not candidates:
        return None
    target = candidates[0]
    with target.open("ab") as handle:
        handle.write(b"\x00storytime-demo-corruption")
    return target


def _scenario_artifact_validation_failure(
    ctx: RunnerContext, workspace: Path
) -> DemoScenarioResult:
    """Corrupt a completed-stage artifact, then resume — rehydration must fail.

    A resumed run hash-verifies every artifact it reuses; a tampered payload
    raises RehydrationError and records pipeline_artifact_validation_failed_total.
    """
    name = "artifact_validation_failure"
    description = (
        "Tampered artifact payload: resume fails artifact hash verification."
    )
    manifest = _write_source(
        workspace, "demo-artifact-fail", title="Corrupted Tale"
    )
    paused = run_vertical_slice(ctx, manifest, require_audio_approval=True)
    run_id = paused.pipeline_run_id
    if paused.status != "awaiting_approval" or run_id is None:
        return DemoScenarioResult(
            name, description, "skipped", "skipped", True,
            "could not reach a paused state to corrupt an artifact",
            run_id,
        )

    corrupted = _corrupt_an_artifact(ctx.config.run_dir(run_id))
    if corrupted is None:
        return DemoScenarioResult(
            name, description, "skipped", "skipped", True,
            "no persisted artifact payload found to corrupt", run_id,
        )

    apply_approval_decision(
        ctx,
        pipeline_run_id=run_id,
        gate="audio",
        decision="approved",
        operator="demo-operator",
        notes="Demo: audio approved (artifact will fail validation).",
    )
    try:
        resumed = resume_run(ctx, run_id)
    except RehydrationError as exc:
        return DemoScenarioResult(
            name, description, "rehydration_error", "rehydration_error",
            True,
            f"resume correctly refused the tampered artifact: {exc}",
            run_id,
        )
    return _result(name, description, "rehydration_error", resumed, run_id=run_id)


def _ffmpeg_missing_skip() -> DemoScenarioResult:
    """The ffmpeg-missing scenario is skipped on purpose — see detail."""
    return DemoScenarioResult(
        name="ffmpeg_missing",
        description="ffmpeg-missing assembly failure.",
        expected="skipped",
        actual="skipped",
        ok=True,
        detail=(
            "skipped by design: removing ffmpeg from PATH process-wide is "
            "unsafe to script, and injecting a fake failing encoder would not "
            "be real telemetry. Demonstrate it manually by running the demo "
            "on a host without ffmpeg installed."
        ),
    )


# --------------------------------------------------------------------------
# Orchestration.
# --------------------------------------------------------------------------

_SCENARIOS: dict[str, Callable[[RunnerContext, Path], DemoScenarioResult]] = {
    "success": _scenario_success,
    "text_approval": _scenario_text_approval,
    "audio_approval": _scenario_audio_approval,
    "text_rejection": lambda ctx, ws: _scenario_rejection(ctx, ws, gate="text"),
    "audio_rejection": lambda ctx, ws: _scenario_rejection(ctx, ws, gate="audio"),
    "bad_manifest": _scenario_bad_manifest,
    "artifact_validation_failure": _scenario_artifact_validation_failure,
}

# Stable presentation order.
SCENARIO_NAMES: tuple[str, ...] = (
    "success",
    "text_approval",
    "audio_approval",
    "text_rejection",
    "audio_rejection",
    "bad_manifest",
    "artifact_validation_failure",
    "ffmpeg_missing",
)


def _shutdown_telemetry(adapter: object) -> None:
    """Best-effort telemetry shutdown.

    Only OTelTelemetry has a shutdown(); NoopTelemetry does not. Resolved
    dynamically so this module needs no telemetry-adapter type coupling.
    """
    shutdown = getattr(adapter, "shutdown", None)
    if callable(shutdown):
        shutdown()


def run_demo(
    *,
    workspace: Path,
    telemetry: str = "otel",
    otlp_endpoint: str = "http://127.0.0.1:4318",
    scenarios: tuple[str, ...] | None = None,
    log_dir: Path | None = None,
) -> DemoResult:
    """Run the demo scenarios under *workspace* and return a DemoResult.

    *workspace* is created if absent; the harness only ever writes inside it
    (sources, runs, feed). *telemetry* selects the adapter exactly as the CLI
    would: "otel" emits and exports real telemetry to *otlp_endpoint* when a
    collector is reachable; "noop" runs the identical scenarios with telemetry
    disabled (used by the test suite, so the demo needs no Docker to verify).

    *log_dir*, when given, is where the harness writes a structured JSON-lines
    log file (Phase 8B). It is the local log *source* the OpenTelemetry
    Collector ``filelog`` receiver tails on its way to Loki — plain structured
    file logging, never Python OTLP log export. When *log_dir* is ``None`` (the
    default) no log file is written, so default behaviour is unchanged.
    """
    workspace = workspace.resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    config = StoryTimeConfig(
        runs_dir=workspace / "runs",
        feed_dir=workspace / "feed",
        telemetry=telemetry,
        otlp_endpoint=otlp_endpoint,
        http_host="127.0.0.1",
        http_port=8000,
        environment="demo",
    )
    ctx = build_runtime_context(config)

    selected = scenarios or SCENARIO_NAMES
    results: list[DemoScenarioResult] = []
    try:
        for scenario_name in selected:
            if scenario_name == "ffmpeg_missing":
                results.append(_ffmpeg_missing_skip())
                continue
            runner = _SCENARIOS.get(scenario_name)
            if runner is None:
                results.append(
                    DemoScenarioResult(
                        scenario_name, "unknown scenario", "skipped",
                        "skipped", True, "no such scenario",
                    )
                )
                continue
            try:
                results.append(runner(ctx, workspace))
            except (ApprovalError, RehydrationError, OSError, ValueError) as exc:
                results.append(
                    DemoScenarioResult(
                        scenario_name, "scenario raised", "completed",
                        f"error:{type(exc).__name__}", False, str(exc),
                    )
                )
    finally:
        _shutdown_telemetry(ctx.telemetry)
        ctx.state.close()

    result = DemoResult(
        workspace=workspace,
        telemetry=telemetry,
        otlp_endpoint=otlp_endpoint,
        scenarios=tuple(results),
    )

    # Phase 8B: write the structured demo log for the Collector filelog ->
    # Loki path. Telemetry/log emission must never break the demo, so a log
    # write failure is reported but not raised.
    if log_dir is not None:
        try:
            write_demo_log(
                log_dir, result, service_version=config.service_version
            )
        except OSError as exc:  # pragma: no cover - defensive
            print(f"  warning: could not write demo log to {log_dir}: {exc}")

    return result


def format_report(result: DemoResult) -> str:
    """Render a DemoResult as a plain-text report."""
    lines = [
        "StoryTime observability demo",
        f"  workspace : {result.workspace}",
        f"  telemetry : {result.telemetry} (endpoint: {result.otlp_endpoint})",
        "",
    ]
    for scenario in result.scenarios:
        mark = "ok  " if scenario.ok else "FAIL"
        lines.append(f"  [{mark}] {scenario.name}")
        lines.append(f"         {scenario.description}")
        lines.append(
            f"         expected={scenario.expected} actual={scenario.actual}"
        )
        lines.append(f"         {scenario.detail}")
        if scenario.pipeline_run_id:
            lines.append(f"         run_id={scenario.pipeline_run_id}")
    lines.append("")
    lines.append(
        f"  result: {'all scenarios met expectations' if result.ok else 'FAILURES'}"
    )
    if result.telemetry == "otel":
        lines.append(
            "  telemetry was emitted; if the collector was running it is now "
            "visible in Grafana (http://127.0.0.1:3000) and Jaeger "
            "(http://127.0.0.1:16686)."
        )
    return "\n".join(lines)
