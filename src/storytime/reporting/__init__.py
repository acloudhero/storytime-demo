"""StoryTime operator reporting — the Phase 10B generated local report.

This package is the concrete implementation of the locked Architecture
Baseline Section 25 (the Phase 10A Operator Experience Baseline amendment). It
generates a static, local, read-only HTML operator report from existing
authoritative state — the SQLite run/stage/Trust-Envelope projections and the
on-disk artifact references — so a local operator can see what each run did
and what governance recorded.

The report is a *view*, never a source of truth (§25.4): SQLite and the
on-disk artifact envelopes remain authoritative. The package starts no server,
adds no dependency, opens no socket, queries no observability backend, and
contains no control that changes state — it is read-only-first by
construction (§25.3, §25.15, §25.17).
"""

from storytime.reporting.collect import collect_report
from storytime.reporting.generate import (
    GeneratedReport,
    generate_report,
    render_report,
)
from storytime.reporting.model import (
    REVIEW_CONTEXT_SUMMARY_MAX_CHARS,
    ArtifactRef,
    GovernanceView,
    ObservabilityLink,
    OperatorReport,
    RerunView,
    RunDetail,
    RunSummary,
    StageView,
)
from storytime.reporting.render import (
    render_index,
    render_run_detail,
    render_runs,
    run_detail_filename,
)

__all__ = [
    "REVIEW_CONTEXT_SUMMARY_MAX_CHARS",
    "ArtifactRef",
    "GeneratedReport",
    "GovernanceView",
    "ObservabilityLink",
    "OperatorReport",
    "RunDetail",
    "RunSummary",
    "RerunView",
    "StageView",
    "collect_report",
    "generate_report",
    "render_index",
    "render_report",
    "render_run_detail",
    "render_runs",
    "run_detail_filename",
]
