"""Environment diagnostics.

ARCH-LOCK: ffmpeg is a deferred (non-fatal in Phase 2) dependency
DO NOT REFACTOR: Phase 2 must not require ffmpeg, and the test suite must not
require it. The doctor reports ffmpeg as a non-required check so its absence is
visible but never fails the scaffold. The fail-fast point arrives in Phase 3,
when the assemble/package stage needs MP3 encoding.
Rationale: Round 7 prerequisite correction 7.

This module deliberately does NOT import opentelemetry. It probes importability
with importlib.util.find_spec so the telemetry import boundary stays intact.
"""

from __future__ import annotations

import importlib.util
import shutil
import sqlite3
import sys
from dataclasses import dataclass

_MIN_PYTHON = (3, 11)


@dataclass(frozen=True, slots=True)
class DoctorCheck:
    """The result of one environment check."""

    name: str
    ok: bool
    required: bool
    detail: str


@dataclass(frozen=True, slots=True)
class DoctorReport:
    """The collected results of all environment checks."""

    checks: tuple[DoctorCheck, ...]

    @property
    def healthy(self) -> bool:
        """True if every *required* check passed. Optional checks never fail this."""
        return all(check.ok for check in self.checks if check.required)


def _check_python() -> DoctorCheck:
    version = sys.version_info[:3]
    ok = version >= _MIN_PYTHON
    return DoctorCheck(
        name="python",
        ok=ok,
        required=True,
        detail=(
            f"running {'.'.join(map(str, version))}; "
            f"minimum is {'.'.join(map(str, _MIN_PYTHON))}"
        ),
    )


def _check_sqlite() -> DoctorCheck:
    return DoctorCheck(
        name="sqlite3",
        ok=True,
        required=True,
        detail=f"SQLite {sqlite3.sqlite_version}; WAL journal mode is used by the state store",
    )


def _check_opentelemetry() -> DoctorCheck:
    available = importlib.util.find_spec("opentelemetry") is not None
    return DoctorCheck(
        name="opentelemetry",
        ok=available,
        required=False,
        detail=(
            "available; required only when STORYTIME_TELEMETRY=otel"
            if available
            else "not installed; NoopTelemetry will be used"
        ),
    )


def _check_ffmpeg() -> DoctorCheck:
    path = shutil.which("ffmpeg")
    return DoctorCheck(
        name="ffmpeg",
        ok=path is not None,
        required=False,  # ARCH-LOCK: non-fatal in Phase 2.
        detail=(
            f"found at {path}"
            if path is not None
            else "NOT found; Phase 2 does not need it, but Phase 3 MP3 "
            "assembly will fail-fast until ffmpeg is installed"
        ),
    )


def run_doctor() -> DoctorReport:
    """Run every environment check and return a DoctorReport."""
    return DoctorReport(
        checks=(
            _check_python(),
            _check_sqlite(),
            _check_opentelemetry(),
            _check_ffmpeg(),
        )
    )
