"""The doctor reports environment status; ffmpeg absence is non-fatal."""

from __future__ import annotations

from storytime.doctor import run_doctor


def test_doctor_runs_all_checks() -> None:
    report = run_doctor()
    names = {check.name for check in report.checks}
    assert names == {"python", "sqlite3", "opentelemetry", "ffmpeg"}


def test_required_checks_pass_in_this_environment() -> None:
    report = run_doctor()
    required = {c.name: c for c in report.checks if c.required}
    assert required["python"].ok
    assert required["sqlite3"].ok


def test_ffmpeg_check_is_not_required() -> None:
    """ffmpeg must be a non-required check so its absence never fails Phase 2."""
    report = run_doctor()
    ffmpeg = next(c for c in report.checks if c.name == "ffmpeg")
    assert ffmpeg.required is False
    # Whether ffmpeg is present or not, the environment stays 'healthy'
    # as long as the required checks pass.
    assert report.healthy is True


def test_healthy_ignores_optional_failures() -> None:
    """healthy depends only on required checks, never on optional ones."""
    report = run_doctor()
    optional_failed = any(not c.ok for c in report.checks if not c.required)
    required_passed = all(c.ok for c in report.checks if c.required)
    assert report.healthy == required_passed
    # The property holds even when an optional check is failing.
    if optional_failed:
        assert report.healthy is True
