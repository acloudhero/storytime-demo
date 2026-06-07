"""The canonical CLI command surface is present, visible, and honest.

Phase 4 makes the per-stage commands real (docs/open-issues.md, OI-12). They
remain discoverable in `--help`; invoking one now does genuine work, pauses
cleanly at the approval gate, or fails with a clear message — it no longer
reports a Phase 3 deferral. The Phase 3 form of this test asserted the
interim exit-code-2 deferral; that behaviour is exactly what OI-12 charters
Phase 4 to replace, so the assertions are updated to the Phase 4 contract.
"""

from __future__ import annotations

from typer.testing import CliRunner

from storytime.cli.app import app

runner = CliRunner()

_CANONICAL_STAGE_COMMANDS = ("ingest", "approve", "synthesize", "assemble", "publish")
# Stage commands that take a pipeline_run_id and rehydrate the run from SQLite.
_RESUME_STAGE_COMMANDS = ("synthesize", "assemble", "publish")


def test_help_lists_run_and_every_canonical_stage_command() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    for command in ("run", "status", *_CANONICAL_STAGE_COMMANDS):
        assert command in result.output, command


def test_no_stage_command_reports_a_phase4_deferral() -> None:
    # The Phase 3 interim deferral language is gone: the commands are real.
    for command in _RESUME_STAGE_COMMANDS:
        result = runner.invoke(app, [command, "01BOGUSRUNID0000000000000X"])
        assert "DEFERRED" not in result.output, command


def test_resume_stage_commands_do_real_work_and_fail_clearly() -> None:
    # Invoked against an unknown run id, a resume stage command does real
    # rehydration and fails with a clear error (exit 1) — not a silent no-op
    # and not the old exit-code-2 deferral.
    for command in _RESUME_STAGE_COMMANDS:
        result = runner.invoke(app, [command, "01BOGUSRUNID0000000000000X"])
        assert result.exit_code == 1, command
        assert "no pipeline run found" in result.output, command


def test_run_command_is_not_removed() -> None:
    result = runner.invoke(app, ["run", "--help"])
    assert result.exit_code == 0
    assert "--manifest" in result.output
    # Phase 4 added resume and the approval-gate flags to the same command.
    assert "--resume" in result.output
    assert "--require-approval" in result.output


def test_run_requires_either_manifest_or_resume() -> None:
    result = runner.invoke(app, ["run"])
    assert result.exit_code == 1
    assert "--manifest" in result.output and "--resume" in result.output


def test_stage_commands_appear_in_help_text() -> None:
    # The per-stage commands carry a docstring summary so `--help` is honest.
    result = runner.invoke(app, ["ingest", "--help"])
    assert result.exit_code == 0
    assert "canonical stage 1" in result.output
    approve_help = runner.invoke(app, ["approve", "--help"])
    assert approve_help.exit_code == 0
    assert "canonical stage 2" in approve_help.output


def test_serve_command_is_present_and_documents_loopback_and_ranges() -> None:
    # `storytime serve` is part of the canonical command surface (Architecture
    # Baseline section 4). Its help must be honest about the two guarantees
    # that matter: a loopback-only bind and HTTP range support (OI-7).
    listing = runner.invoke(app, ["--help"])
    assert listing.exit_code == 0
    assert "serve" in listing.output

    serve_help = runner.invoke(app, ["serve", "--help"])
    assert serve_help.exit_code == 0
    assert "--port" in serve_help.output
    lowered = serve_help.output.lower()
    assert "range" in lowered
    assert "127.0.0.1" in serve_help.output
