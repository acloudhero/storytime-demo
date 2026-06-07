"""Phase 13G.1 — archive-hygiene guard.

The Phase 13G deliverable accidentally packaged the runtime SQLite database
``runs/state.db`` (created by ``storytime doctor`` / pipeline tests in the
working tree). These tests are the programmatic guard that prevents that class
of leak from recurring:

1. The canonical packaging script ``scripts/build-artifact.sh`` exists, is
   executable, and excludes every forbidden runtime / cache / archive pattern.
2. Running that script on the real tree — even with a runtime database, a tool
   cache, and a stray nested archive present — produces an archive with NO
   runtime database / journal artifact, no tool cache, no virtualenv, no
   node_modules, no frontend build output, and no nested archive. This is the
   end-to-end proof that the exact Phase 13G leak cannot recur.
3. ``.gitignore`` covers the runtime working-state directory and database
   artifacts.

These tests read the repository tree and build a throwaway archive into a temp
path; they need no network, no live database, and no committed artifact.
"""

from __future__ import annotations

import re
import subprocess
import tarfile
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]
_BUILD_SCRIPT = _REPO_ROOT / "scripts" / "build-artifact.sh"

# Patterns that must NOT appear in any packaged member name. Mirrors the
# Phase 13G.1 prompt's required archive-hygiene patterns (the final artifact
# itself is a .tar.gz, but no nested archive may appear inside it).
_FORBIDDEN_MEMBER_PATTERNS: tuple[str, ...] = (
    r"(^|/)runs/.*\.db$",
    r"(^|/)runs/.*\.sqlite$",
    r"(^|/)runs/.*\.sqlite3$",
    r"(^|/)runs/.*\.db-wal$",
    r"(^|/)runs/.*\.db-shm$",
    r"\.db$",
    r"\.sqlite$",
    r"\.sqlite3$",
    r"\.db-wal$",
    r"\.db-shm$",
    r"__pycache__",
    r"\.pyc$",
    r"\.pyo$",
    r"\.venv",
    r"node_modules",
    r"frontend/dist",
    r"\.pytest_cache",
    r"\.ruff_cache",
    r"\.mypy_cache",
    r"\.import_linter_cache",
    r"\.tar\.gz$",
    r"\.zip$",
)

# Exclude patterns the packaging script MUST carry.
_REQUIRED_EXCLUDES: tuple[str, ...] = (
    "*.db",
    "*.sqlite",
    "*.sqlite3",
    "*.db-wal",
    "*.db-shm",
    "__pycache__",
    "*.pyc",
    "*.pyo",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    ".import_linter_cache",
    ".venv",
    "node_modules",
    "frontend/dist",
    "*.tar.gz",
    "*.zip",
    "runs",
)


def test_build_script_exists_and_is_executable() -> None:
    assert _BUILD_SCRIPT.is_file(), "scripts/build-artifact.sh is missing"
    assert _BUILD_SCRIPT.stat().st_mode & 0o111, (
        "scripts/build-artifact.sh is not executable"
    )


@pytest.mark.parametrize("pattern", _REQUIRED_EXCLUDES)
def test_build_script_excludes_pattern(pattern: str) -> None:
    """The packaging script excludes every forbidden runtime / cache pattern."""
    text = _BUILD_SCRIPT.read_text(encoding="utf-8")
    assert pattern in text, (
        f"scripts/build-artifact.sh does not exclude {pattern!r}; the archive "
        "could leak it again"
    )


def test_packaging_script_produces_clean_archive(tmp_path: Path) -> None:
    """Building via the script yields an archive free of forbidden artifacts.

    A runtime database, a journal sibling, and a stray nested archive are
    planted in the tree first (in already-ignored locations) to prove the
    script excludes them rather than relying on the tree happening to be clean.
    """
    planted: list[Path] = []
    runs_db = _REPO_ROOT / "runs" / "state.db"
    runs_wal = _REPO_ROOT / "runs" / "state.db-wal"
    nested = _REPO_ROOT / "review-bundle.tar.gz"
    try:
        runs_db.parent.mkdir(parents=True, exist_ok=True)
        runs_db.write_bytes(b"SQLite format 3\x00planted")
        runs_wal.write_bytes(b"planted-wal")
        nested.write_bytes(b"planted-nested-archive")
        planted += [runs_db, runs_wal, nested]

        output = tmp_path / "hygiene-probe.tar.gz"
        result = subprocess.run(  # noqa: S603 - fixed, trusted local script
            ["bash", str(_BUILD_SCRIPT), str(output)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, f"packaging script failed: {result.stderr}"
        assert output.is_file(), "packaging script did not produce an archive"

        with tarfile.open(output, "r:gz") as tar:
            members = tar.getnames()

        for pattern in _FORBIDDEN_MEMBER_PATTERNS:
            rx = re.compile(pattern)
            hits = [m for m in members if rx.search(m)]
            assert not hits, (
                f"archive contains members matching forbidden pattern "
                f"{pattern!r}: {hits[:5]}"
            )
        assert not any(m.endswith("runs/state.db") for m in members), (
            "archive still contains runs/state.db"
        )
        assert any(
            m.endswith("src/storytime/local_bridge/server.py") for m in members
        ), "archive unexpectedly missing local_bridge source"
    finally:
        for path in planted:
            path.unlink(missing_ok=True)
        runs_dir = _REPO_ROOT / "runs"
        if runs_dir.is_dir() and not any(runs_dir.iterdir()):
            runs_dir.rmdir()


def test_gitignore_covers_runtime_state() -> None:
    """`.gitignore` covers the runtime working-state directory and DB artifacts."""
    gitignore = (_REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    for needle in ("runs/", "*.db", "*.db-wal", "*.db-shm"):
        assert needle in gitignore, f".gitignore lacks coverage for {needle!r}"
