"""Tests for the Phase 6A observability demo harness.

The harness drives real StoryTime scenarios. These tests run it with telemetry
disabled ("noop") so they need no Docker and no collector — Phase 6A acceptance
criterion 11 (Docker unavailability must not fail tests). They verify the
scenarios actually execute and reach their expected pipeline states, and that
the harness stays bounded to its workspace directory.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from storytime.demo import run_demo
from storytime.demo.harness import SCENARIO_NAMES

_HAS_FFMPEG = shutil.which("ffmpeg") is not None


def test_bad_manifest_scenario_needs_no_ffmpeg(tmp_path: Path) -> None:
    """The bad-manifest scenario is rejected at pre-flight, before assembly."""
    result = run_demo(
        workspace=tmp_path / "ws",
        telemetry="noop",
        scenarios=("bad_manifest",),
    )
    assert result.ok
    (scenario,) = result.scenarios
    assert scenario.name == "bad_manifest"
    assert scenario.actual == "rejected"


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_full_demo_runs_every_scenario_to_its_expected_state(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "demo"
    result = run_demo(workspace=workspace, telemetry="noop")

    # Every scenario is present, in the documented order, and met expectation.
    assert tuple(s.name for s in result.scenarios) == SCENARIO_NAMES
    assert result.ok, [
        (s.name, s.detail) for s in result.scenarios if not s.ok
    ]

    by_name = {s.name: s for s in result.scenarios}
    assert by_name["success"].actual == "completed"
    assert by_name["text_approval"].actual == "completed"
    assert by_name["audio_approval"].actual == "completed"
    assert by_name["text_rejection"].actual == "failed"
    assert by_name["audio_rejection"].actual == "failed"
    assert by_name["bad_manifest"].actual == "rejected"
    # The artifact-validation scenario corrupts a payload; resume must refuse.
    assert by_name["artifact_validation_failure"].actual == "rehydration_error"
    # ffmpeg-missing is an honest, deliberate skip.
    assert by_name["ffmpeg_missing"].actual == "skipped"


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_harness_is_bounded_to_its_workspace(tmp_path: Path) -> None:
    """The harness must only ever write inside the workspace it was given."""
    workspace = tmp_path / "boxed"
    sibling = tmp_path / "untouched"
    sibling.mkdir()

    result = run_demo(
        workspace=workspace, telemetry="noop", scenarios=("success",)
    )

    assert result.workspace == workspace.resolve()
    # Real run artefacts landed under the workspace.
    assert (workspace / "runs").is_dir()
    assert (workspace / "sources").is_dir()
    # Nothing leaked into the sibling directory.
    assert list(sibling.iterdir()) == []


def test_scenario_subset_selection(tmp_path: Path) -> None:
    """Only the requested scenarios run when a subset is given."""
    result = run_demo(
        workspace=tmp_path / "ws",
        telemetry="noop",
        scenarios=("ffmpeg_missing",),
    )
    assert tuple(s.name for s in result.scenarios) == ("ffmpeg_missing",)
    assert result.scenarios[0].actual == "skipped"
