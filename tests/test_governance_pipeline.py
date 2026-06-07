"""End-to-end governance wiring through the pipeline (Architecture Baseline §24.6).

These exercise the fail-closed gate where it is wired:

* ingest derives the Trust Envelope and checks it early — a blocked source
  never proceeds;
* synthesize hard-blocks before TTS;
* publish hard-blocks before RSS;

and confirm that an approved source proceeds and is recorded in both the
durable artifact and the SQLite projection.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

import pytest

from storytime.adapters.storage import LocalFilesystemStorage
from storytime.adapters.telemetry import NoopTelemetry
from storytime.adapters.tts import MockTTS
from storytime.config import load_config
from storytime.dto import StageInput, StageStatus
from storytime.governance import (
    GovernanceDecision,
    LicenseType,
    TrustEnvelope,
    read_trust_envelope,
    to_json,
    trust_envelope_key,
)
from storytime.pipeline import run_vertical_slice
from storytime.runner import RunnerContext
from storytime.stages import AssembleStage, IngestStage, PublishStage, SynthesizeStage
from storytime.stages.encode import FfmpegMp3Encoder
from storytime.util.clock import FixedClock

_HAS_FFMPEG = shutil.which("ffmpeg") is not None
RUN_ID = "01TESTGOVERNANCE0000000001"


# -- approved source proceeds ------------------------------------------------

def test_approved_source_completes_and_is_recorded(
    runtime_context: RunnerContext, slice_workspace: Any
) -> None:
    outcome = run_vertical_slice(runtime_context, slice_workspace.manifest_path)
    assert outcome.status == "completed"
    run_id = outcome.pipeline_run_id
    assert run_id is not None

    # The SQLite projection records the APPROVED decision.
    projection = runtime_context.state.latest_trust_envelope(run_id)
    assert projection is not None
    assert projection.decision == str(GovernanceDecision.APPROVED)
    assert projection.license_type == str(LicenseType.US_PUBLIC_DOMAIN)

    # The durable Trust Envelope artifact is the governance source of truth.
    durable = read_trust_envelope(runtime_context.storage, run_id)
    assert durable.is_approved
    assert durable.source_ref == projection.source_ref


# -- blocked source is stopped early at ingest -------------------------------

def _context_with_blocklist(
    tmp_path: Path, fixed_clock: FixedClock, state_store: Any, blocklist_body: str
) -> RunnerContext:
    """Build a RunnerContext whose blocked-source config is *blocklist_body*."""
    blocklist = tmp_path / "blocked-sources.yaml"
    blocklist.write_text(blocklist_body, encoding="utf-8")
    config = load_config(
        {
            "STORYTIME_RUNS_DIR": str(tmp_path / "runs"),
            "STORYTIME_FEED_DIR": str(tmp_path / "feed"),
            "STORYTIME_TELEMETRY": "noop",
            "STORYTIME_BLOCKED_SOURCES": str(blocklist),
        }
    )
    return RunnerContext(
        config=config,
        clock=fixed_clock,
        state=state_store,
        telemetry=NoopTelemetry(),
        storage=LocalFilesystemStorage(config.runs_dir),
    )


def test_blocked_source_fails_closed_at_ingest(
    tmp_path: Path,
    fixed_clock: FixedClock,
    state_store: Any,
    make_workspace: Any,
) -> None:
    # The demo manifest's source_url is https://example.org/... — block it.
    ctx = _context_with_blocklist(
        tmp_path,
        fixed_clock,
        state_store,
        'blocked_sources:\n'
        '  - pattern: "example.org"\n'
        '    reason: "operator-blocked test domain"\n',
    )
    workspace = make_workspace()
    outcome = run_vertical_slice(ctx, workspace.manifest_path)

    # The run fails — and fails at ingest, before synthesis/TTS ever runs.
    assert outcome.status == "failed"
    assert outcome.failed_stage == "ingest"
    assert outcome.error_kind == "SourceNotApproved"

    # The blocking decision is still durably recorded for the audit trail.
    run_id = outcome.pipeline_run_id
    assert run_id is not None
    projection = ctx.state.latest_trust_envelope(run_id)
    assert projection is not None
    assert projection.decision == str(GovernanceDecision.BLOCKED)


# -- synthesize hard-blocks before TTS ---------------------------------------

def _ingest(ctx: RunnerContext, manifest_path: str) -> tuple[str, ...]:
    """Run ingest for RUN_ID and return its output artifacts."""
    result = IngestStage().run(
        ctx,
        StageInput(
            pipeline_run_id=RUN_ID,
            stage_name="ingest",
            run_dir=RUN_ID,
            params={"manifest_path": manifest_path},
        ),
    )
    assert result.status is StageStatus.SUCCEEDED
    return result.output_artifacts


def _synthesize(ctx: RunnerContext, artifacts: tuple[str, ...]) -> Any:
    return SynthesizeStage(MockTTS()).run(
        ctx,
        StageInput(
            pipeline_run_id=RUN_ID,
            stage_name="synthesize",
            run_dir=RUN_ID,
            input_artifacts=artifacts,
        ),
    )


def _overwrite_envelope(ctx: RunnerContext, decision: GovernanceDecision) -> None:
    """Replace RUN_ID's durable Trust Envelope with one carrying *decision*."""
    tampered = TrustEnvelope(
        schema_version="1",
        source_ref="the-raven",
        license_type=LicenseType.US_PUBLIC_DOMAIN,
        decision=decision,
        decision_timestamp="2026-01-16T09:30:00Z",
        approver_id="operator",
    )
    ctx.storage.write_text(trust_envelope_key(RUN_ID), to_json(tampered))


def test_synthesize_proceeds_for_an_approved_run(
    runtime_context: RunnerContext, slice_workspace: Any
) -> None:
    artifacts = _ingest(runtime_context, str(slice_workspace.manifest_path))
    assert _synthesize(runtime_context, artifacts).status is StageStatus.SUCCEEDED


def test_synthesize_fails_closed_when_envelope_missing(
    runtime_context: RunnerContext, slice_workspace: Any
) -> None:
    artifacts = _ingest(runtime_context, str(slice_workspace.manifest_path))
    # Remove the durable Trust Envelope: synthesis must not proceed to TTS.
    runtime_context.storage.resolve(trust_envelope_key(RUN_ID)).unlink()
    result = _synthesize(runtime_context, artifacts)
    assert result.status is StageStatus.FAILED
    assert result.error_kind == "GovernanceGateBlocked"


@pytest.mark.parametrize(
    "decision",
    [
        GovernanceDecision.REJECTED,
        GovernanceDecision.BLOCKED,
        GovernanceDecision.NEEDS_REVIEW,
    ],
)
def test_synthesize_fails_closed_for_non_approved_envelope(
    runtime_context: RunnerContext, slice_workspace: Any, decision: GovernanceDecision
) -> None:
    artifacts = _ingest(runtime_context, str(slice_workspace.manifest_path))
    _overwrite_envelope(runtime_context, decision)
    result = _synthesize(runtime_context, artifacts)
    assert result.status is StageStatus.FAILED
    assert result.error_kind == "GovernanceGateBlocked"


def test_synthesize_fails_closed_for_malformed_envelope(
    runtime_context: RunnerContext, slice_workspace: Any
) -> None:
    artifacts = _ingest(runtime_context, str(slice_workspace.manifest_path))
    runtime_context.storage.write_text(
        trust_envelope_key(RUN_ID), "{ not a valid trust envelope"
    )
    result = _synthesize(runtime_context, artifacts)
    assert result.status is StageStatus.FAILED
    assert result.error_kind == "GovernanceGateBlocked"


# -- publish hard-blocks before RSS ------------------------------------------

@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_publish_fails_closed_when_envelope_blocked_after_synthesis(
    runtime_context: RunnerContext, slice_workspace: Any
) -> None:
    from storytime.rss import EmptyEpisodeCatalog

    ctx = runtime_context
    artifacts = _ingest(ctx, str(slice_workspace.manifest_path))
    synth = _synthesize(ctx, artifacts)
    assert synth.status is StageStatus.SUCCEEDED
    assemble = AssembleStage(
        FfmpegMp3Encoder.autodetect(),
        episode_title="The Raven",
        episode_description="A public-domain reading.",
    ).run(
        ctx,
        StageInput(
            pipeline_run_id=RUN_ID,
            stage_name="assemble",
            run_dir=RUN_ID,
            input_artifacts=synth.output_artifacts,
        ),
    )
    assert assemble.status is StageStatus.SUCCEEDED

    # The durable envelope is changed to BLOCKED after synthesis: publish must
    # still fail closed before writing the RSS feed.
    _overwrite_envelope(ctx, GovernanceDecision.BLOCKED)
    publish = PublishStage(
        LocalFilesystemStorage(ctx.config.feed_dir),
        channel_title="StoryTime",
        channel_link="http://127.0.0.1:8000/feed.xml",
        channel_description="StoryTime test feed.",
        episode_catalog=EmptyEpisodeCatalog(),
    ).run(
        ctx,
        StageInput(
            pipeline_run_id=RUN_ID,
            stage_name="publish",
            run_dir=RUN_ID,
            input_artifacts=assemble.output_artifacts,
        ),
    )
    assert publish.status is StageStatus.FAILED
    assert publish.error_kind == "GovernanceGateBlocked"
    # No feed.xml was written.
    assert not (ctx.config.feed_dir / "feed.xml").exists()
