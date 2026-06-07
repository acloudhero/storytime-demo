"""End-to-end CLI flows for the approval gate and resume (Phase 4)."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

import pytest
from typer.testing import CliRunner

from storytime.cli.app import app

runner = CliRunner()
_HAS_FFMPEG = shutil.which("ffmpeg") is not None
_RUN_ID = re.compile(r"run ([0-9A-HJKMNP-TV-Z]{26})")


def _env(tmp_path: Path) -> dict[str, str]:
    return {
        "STORYTIME_RUNS_DIR": str(tmp_path / "runs"),
        "STORYTIME_FEED_DIR": str(tmp_path / "feed"),
        "STORYTIME_TELEMETRY": "noop",
    }


def _run_id(output: str) -> str:
    match = _RUN_ID.search(output)
    assert match is not None, f"no run id in CLI output:\n{output}"
    return match.group(1)


def test_run_without_flags_still_runs_the_phase3_slice(
    tmp_path: Path, slice_workspace
) -> None:
    # Phase 3 compatibility: a plain `run` needs no approval and either
    # completes (ffmpeg present) or fails at assemble (ffmpeg absent) — it
    # must never pause at a gate.
    result = runner.invoke(
        app,
        ["run", "--manifest", str(slice_workspace.manifest_path)],
        env=_env(tmp_path),
    )
    assert "AWAITING APPROVAL" not in result.output
    if _HAS_FFMPEG:
        assert result.exit_code == 0
        assert "COMPLETED" in result.output


def test_run_with_require_approval_pauses_at_the_gate(
    tmp_path: Path, slice_workspace
) -> None:
    result = runner.invoke(
        app,
        ["run", "--manifest", str(slice_workspace.manifest_path), "--require-approval"],
        env=_env(tmp_path),
    )
    # Pausing at a gate is a clean exit, not a failure.
    assert result.exit_code == 0
    assert "AWAITING APPROVAL" in result.output
    assert "storytime approve" in result.output


def test_status_reports_the_awaiting_gate(
    tmp_path: Path, slice_workspace
) -> None:
    env = _env(tmp_path)
    parked = runner.invoke(
        app, ["ingest", "--manifest", str(slice_workspace.manifest_path)], env=env
    )
    run_id = _run_id(parked.output)

    status = runner.invoke(app, ["status", run_id], env=env)
    assert status.exit_code == 0
    assert "awaiting_approval" in status.output
    assert "awaiting an operator decision" in status.output


def test_approve_unknown_run_fails_clearly(tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        ["approve", "01NOSUCHRUN0000000000000001", "--decision", "approve"],
        env=_env(tmp_path),
    )
    assert result.exit_code == 1
    assert "no pipeline run found" in result.output


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_full_ingest_approve_resume_cli_flow(
    tmp_path: Path, slice_workspace
) -> None:
    env = _env(tmp_path)

    parked = runner.invoke(
        app, ["ingest", "--manifest", str(slice_workspace.manifest_path)], env=env
    )
    assert parked.exit_code == 0
    assert "AWAITING APPROVAL" in parked.output
    run_id = _run_id(parked.output)

    approved = runner.invoke(
        app, ["approve", run_id, "--decision", "approve", "--operator", "ada"], env=env
    )
    assert approved.exit_code == 0
    assert "APPROVED" in approved.output

    resumed = runner.invoke(app, ["run", "--resume", run_id], env=env)
    assert resumed.exit_code == 0
    assert "COMPLETED" in resumed.output

    status = runner.invoke(app, ["status", run_id], env=env)
    assert "completed" in status.output
    assert "approved by ada" in status.output


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_auto_approve_completes_and_persists_a_real_decision(
    tmp_path: Path, slice_workspace
) -> None:
    env = _env(tmp_path)
    result = runner.invoke(
        app,
        ["run", "--manifest", str(slice_workspace.manifest_path), "--auto-approve"],
        env=env,
    )
    assert result.exit_code == 0
    assert "COMPLETED" in result.output
    run_id = _run_id(result.output)

    # --auto-approve still persists a genuine approval decision and event.
    status = runner.invoke(app, ["status", run_id], env=env)
    assert "approved by auto-approve" in status.output
    assert "TextApproved" in status.output


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_granular_per_stage_cli_walk(tmp_path: Path, slice_workspace) -> None:
    env = _env(tmp_path)
    parked = runner.invoke(
        app, ["ingest", "--manifest", str(slice_workspace.manifest_path)], env=env
    )
    run_id = _run_id(parked.output)
    runner.invoke(app, ["approve", run_id, "--decision", "approve"], env=env)

    synth = runner.invoke(app, ["synthesize", run_id], env=env)
    assert synth.exit_code == 0
    assert "STAGE COMPLETE" in synth.output

    asm = runner.invoke(app, ["assemble", run_id], env=env)
    assert asm.exit_code == 0
    assert "STAGE COMPLETE" in asm.output

    pub = runner.invoke(app, ["publish", run_id], env=env)
    assert pub.exit_code == 0
    assert "COMPLETED" in pub.output


def test_rejected_run_cli_flow_blocks_resume(
    tmp_path: Path, slice_workspace
) -> None:
    env = _env(tmp_path)
    parked = runner.invoke(
        app, ["ingest", "--manifest", str(slice_workspace.manifest_path)], env=env
    )
    run_id = _run_id(parked.output)

    rejected = runner.invoke(
        app, ["approve", run_id, "--decision", "reject"], env=env
    )
    assert rejected.exit_code == 0
    assert "REJECTED" in rejected.output

    # A rejected run cannot be resumed.
    resumed = runner.invoke(app, ["run", "--resume", run_id], env=env)
    assert resumed.exit_code == 1
    assert "failed/rejected" in resumed.output


# -- Phase 4.1: audio approval gate CLI flows --------------------------------

def test_approve_rejects_an_unknown_stage(tmp_path: Path, slice_workspace) -> None:
    env = _env(tmp_path)
    parked = runner.invoke(
        app, ["ingest", "--manifest", str(slice_workspace.manifest_path)], env=env
    )
    run_id = _run_id(parked.output)
    bad = runner.invoke(
        app, ["approve", run_id, "--stage", "bogus", "--decision", "approve"], env=env
    )
    assert bad.exit_code == 1
    assert "must be 'text' or 'audio'" in bad.output


def test_cli_audio_gated_run_pauses_after_synthesis(
    tmp_path: Path, slice_workspace
) -> None:
    # Synthesis uses MockTTS, so this clean pause needs no ffmpeg.
    result = runner.invoke(
        app,
        [
            "run",
            "--manifest",
            str(slice_workspace.manifest_path),
            "--require-audio-approval",
        ],
        env=_env(tmp_path),
    )
    assert result.exit_code == 0
    assert "AWAITING APPROVAL" in result.output
    assert "audio approval gate" in result.output


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_cli_audio_gate_full_flow(tmp_path: Path, slice_workspace) -> None:
    env = _env(tmp_path)

    # ingest with both gates: the run pauses first at the text gate.
    parked = runner.invoke(
        app,
        [
            "ingest",
            "--manifest",
            str(slice_workspace.manifest_path),
            "--require-audio-approval",
        ],
        env=env,
    )
    assert parked.exit_code == 0
    run_id = _run_id(parked.output)

    text_ok = runner.invoke(
        app, ["approve", run_id, "--decision", "approve"], env=env
    )
    assert text_ok.exit_code == 0

    # Resuming runs synthesize and then pauses at the audio gate.
    at_audio = runner.invoke(app, ["run", "--resume", run_id], env=env)
    assert at_audio.exit_code == 0
    assert "audio approval gate" in at_audio.output

    audio_ok = runner.invoke(
        app,
        ["approve", run_id, "--stage", "audio", "--decision", "approve",
         "--operator", "grace"],
        env=env,
    )
    assert audio_ok.exit_code == 0
    assert "audio gate approved by grace" in audio_ok.output

    done = runner.invoke(app, ["run", "--resume", run_id], env=env)
    assert done.exit_code == 0
    assert "COMPLETED" in done.output

    status = runner.invoke(app, ["status", run_id], env=env)
    assert "audio gate:" in status.output
    assert "approved by grace" in status.output


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_cli_audio_rejection_blocks_the_run(tmp_path: Path, slice_workspace) -> None:
    env = _env(tmp_path)
    result = runner.invoke(
        app,
        [
            "run",
            "--manifest",
            str(slice_workspace.manifest_path),
            "--require-audio-approval",
        ],
        env=env,
    )
    run_id = _run_id(result.output)

    rejected = runner.invoke(
        app, ["approve", run_id, "--stage", "audio", "--decision", "reject"], env=env
    )
    assert rejected.exit_code == 0
    assert "REJECTED" in rejected.output

    blocked = runner.invoke(app, ["run", "--resume", run_id], env=env)
    assert blocked.exit_code == 1
    assert "failed/rejected" in blocked.output
