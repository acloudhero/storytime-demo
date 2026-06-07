"""Generate the static operator report — collect, render, and write files.

This module is the Phase 10B orchestration seam: it collects the report model
from existing state (``reporting.collect``), renders it to air-gapped HTML
(``reporting.render``), and writes the static files into a local output
directory. It starts no server, opens no socket, and runs no persistent
process (§25.15) — it writes inert files and returns.

Output files written into the report directory:

* ``index.html``        — landing page + latest-runs summary
* ``runs.html``         — the full run list
* ``run-<run_id>.html`` — one single-run detail page per run
* ``style.css``         — the single, local, minimal stylesheet

Generation is read-only with respect to StoryTime state: it never writes to
SQLite, never touches run artifacts, and never mutates anything (§25.17).
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from storytime.adapters.storage import StorageAdapter
from storytime.reporting.collect import collect_report
from storytime.reporting.model import OperatorReport
from storytime.reporting.render import (
    STYLE_CSS,
    render_index,
    render_run_detail,
    render_runs,
    run_detail_filename,
)
from storytime.state import StateStore

INDEX_FILENAME = "index.html"
RUNS_FILENAME = "runs.html"
STYLE_FILENAME = "style.css"


@dataclass(frozen=True, slots=True)
class GeneratedReport:
    """The result of a report generation: the output directory and its files.

    ``index_path`` is the report entry point; ``files`` lists every file
    written, ``index.html`` first. ``run_count`` is the number of runs the
    report covers — purely informational for the CLI.
    """

    output_dir: Path
    index_path: Path
    files: tuple[Path, ...]
    run_count: int


def _write(path: Path, text: str) -> None:
    """Write *text* to *path* as UTF-8, creating parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def render_report(report: OperatorReport) -> dict[str, str]:
    """Render an in-memory report model to a {filename: html/css} mapping.

    Pure: no filesystem access. Given an identical *report* (identical state
    and identical ``generated_at``) the returned mapping is identical, so the
    written report is byte-for-byte deterministic.
    """
    files: dict[str, str] = {
        INDEX_FILENAME: render_index(report),
        RUNS_FILENAME: render_runs(report),
        STYLE_FILENAME: STYLE_CSS,
    }
    for detail in report.details:
        files[run_detail_filename(detail.run_id)] = render_run_detail(
            detail, report.generated_at
        )
    return files


def generate_report(
    store: StateStore,
    storage: StorageAdapter,
    output_dir: Path,
    *,
    generated_at: str,
    feed_reference: str | None = None,
    observability: Mapping[str, str] | None = None,
) -> GeneratedReport:
    """Collect, render, and write the static operator report to *output_dir*.

    *generated_at* is an injected timestamp string: with identical state and
    an identical *generated_at*, the generated files are byte-for-byte
    identical. The CLI passes the real current time; tests pass a fixed value.

    Returns a :class:`GeneratedReport` describing what was written. This
    function reads StoryTime state and writes only into *output_dir*; it
    mutates no StoryTime state.
    """
    report = collect_report(
        store,
        storage,
        generated_at=generated_at,
        feed_reference=feed_reference,
        observability=observability,
    )
    rendered = render_report(report)

    output_dir.mkdir(parents=True, exist_ok=True)
    # Deterministic write order: index, runs, style, then run pages sorted by
    # filename. The mapping itself is already deterministic; sorting the paths
    # keeps the returned tuple stable too.
    ordered = [INDEX_FILENAME, RUNS_FILENAME, STYLE_FILENAME]
    ordered += sorted(name for name in rendered if name not in ordered)

    written: list[Path] = []
    for name in ordered:
        path = output_dir / name
        _write(path, rendered[name])
        written.append(path)

    return GeneratedReport(
        output_dir=output_dir,
        index_path=output_dir / INDEX_FILENAME,
        files=tuple(written),
        run_count=len(report.runs),
    )
