"""Shared pytest fixtures for the StoryTime tests."""

from __future__ import annotations

import copy
import itertools
import json
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

from storytime.adapters.storage import LocalFilesystemStorage
from storytime.adapters.telemetry import NoopTelemetry
from storytime.config import load_config
from storytime.runner import RunnerContext
from storytime.state import RunRecord, StateStore
from storytime.util.clock import FixedClock
from storytime.util.hashing import sha256_text

# A source manifest that is valid against the closed schema. Tests mutate
# copies of this to build negative cases.
_VALID_MANIFEST: dict[str, Any] = {
    "manifest_version": 1,
    "source_id": "the-raven",
    "title": "The Raven",
    "author": "Edgar Allan Poe",
    "source_url": "https://example.org/the-raven.txt",
    "retrieval_date": "2026-01-15",
    "jurisdiction": "US",
    "license": "PD-US",
    "text_sha256": "a" * 64,
    "text_encoding": "utf-8",
    "text_path": "source/the-raven.txt",
    "language": "en",
    "approval": {
        "approved_by": "operator",
        "approved_at": "2026-01-16T09:30:00Z",
        "review_notes": "Public domain confirmed.",
    },
}

# A short public-domain text used by the vertical-slice workspace fixtures.
_SLICE_TEXT = (
    "The Raven\n\n"
    "Once upon a midnight dreary, while I pondered, weak and weary,\n"
    "Over many a quaint and curious volume of forgotten lore.\n"
)


@pytest.fixture()
def valid_manifest() -> dict[str, Any]:
    """A deep copy of a schema-valid source manifest."""
    return copy.deepcopy(_VALID_MANIFEST)


@pytest.fixture()
def fixed_clock() -> FixedClock:
    """A deterministic clock fixed at 2026-01-01T00:00:00Z."""
    return FixedClock(datetime(2026, 1, 1, tzinfo=UTC))


@pytest.fixture()
def state_store(tmp_path: Path) -> Iterator[StateStore]:
    """An initialised StateStore backed by a temp-dir SQLite database."""
    with StateStore.open(tmp_path / "state.db") as store:
        yield store


@pytest.fixture()
def sample_run() -> RunRecord:
    """A pipeline_run row for tests that need an existing run."""
    return RunRecord(
        pipeline_run_id="01JABCDEF0123456789ABCDEFG",
        created_at="2026-01-01T00:00:00+00:00",
        updated_at="2026-01-01T00:00:00+00:00",
        current_stage="ingest",
        status="running",
        source_manifest_hash="b" * 64,
        run_dir="runs/01JABCDEF0123456789ABCDEFG",
    )


@dataclass(frozen=True)
class SliceWorkspace:
    """An on-disk manifest + text file pair for vertical-slice tests."""

    manifest_path: Path
    text_path: Path
    text: str
    text_sha256: str


# A factory that builds a SliceWorkspace, optionally with negative-case tweaks.
WorkspaceFactory = Callable[..., SliceWorkspace]


@pytest.fixture()
def make_workspace(
    tmp_path: Path, valid_manifest: dict[str, Any]
) -> WorkspaceFactory:
    """Return a factory that writes a manifest + matching text file to disk.

    By default the manifest's text_sha256 is the real digest of the written
    text, so a full ingest passes its integrity check. Negative cases:
      * text_sha256=...  -> declare a digest that will not match.
      * text_path=...    -> point the manifest at a file that is not written.
      * mutate=callable  -> arbitrarily edit the manifest dict before writing.
      * <field>=value    -> any other keyword overrides that manifest field
                            directly (e.g. source_id=..., license=...).
    Each call gets its own sub-directory, so a test may build several.
    """
    counter = itertools.count()

    def _make(
        *,
        text_sha256: str | None = None,
        text_path: str | None = None,
        mutate: Callable[[dict[str, Any]], None] | None = None,
        **overrides: Any,
    ) -> SliceWorkspace:
        slot = tmp_path / f"ws{next(counter)}"
        source_dir = slot / "source"
        source_dir.mkdir(parents=True)
        real_text_file = source_dir / "the-raven.txt"
        real_text_file.write_text(_SLICE_TEXT, encoding="utf-8")

        manifest = copy.deepcopy(valid_manifest)
        manifest["text_sha256"] = text_sha256 or sha256_text(_SLICE_TEXT)
        if text_path is not None:
            manifest["text_path"] = text_path
        manifest.update(overrides)
        if mutate is not None:
            mutate(manifest)

        manifest_path = slot / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return SliceWorkspace(
            manifest_path=manifest_path,
            text_path=real_text_file,
            text=_SLICE_TEXT,
            text_sha256=str(manifest["text_sha256"]),
        )

    return _make


@pytest.fixture()
def slice_workspace(make_workspace: WorkspaceFactory) -> SliceWorkspace:
    """A schema-valid, hash-correct manifest + text workspace on disk."""
    return make_workspace()


@pytest.fixture()
def runtime_context(
    tmp_path: Path, fixed_clock: FixedClock, state_store: StateStore
) -> RunnerContext:
    """A RunnerContext wired with NoopTelemetry and temp-dir storage.

    Storage is rooted at <tmp>/runs; tests inspect stage output through
    runtime_context.storage.resolve(key) / .read_text(key).
    """
    config = load_config(
        {
            "STORYTIME_RUNS_DIR": str(tmp_path / "runs"),
            "STORYTIME_FEED_DIR": str(tmp_path / "feed"),
            "STORYTIME_TELEMETRY": "noop",
        }
    )
    return RunnerContext(
        config=config,
        clock=fixed_clock,
        state=state_store,
        telemetry=NoopTelemetry(),
        storage=LocalFilesystemStorage(config.runs_dir),
    )
