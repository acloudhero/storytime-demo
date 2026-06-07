"""StoryTime — deterministic read-only static UI export (Phase 13C).

This module is the backend-native source of the static data export that the
Phase 13 frontend (the portfolio website and operator GUI shell) consumes. It
is the Phase 13C realization of the "backend owns truth, frontend owns
understanding" contract: the *shape* of the export is defined here, in backend
Python, and the frontend mirrors it — not the other way around.

Scope and guarantees:

* **Read-only.** This module reads nothing mutable and writes only the static
  export file when explicitly asked. It performs no pipeline action, no
  mutation, no network call, and no live backend query. It is safe to run at
  any time.
* **Deterministic.** The export is built entirely from fixed module-level demo
  data — fixed ids, fixed ISO-8601 timestamps, fixed ordering. There is no
  ``datetime.now()``, no ``uuid``, no randomness, and no environment-dependent
  value anywhere in the output. ``render_export_json`` serializes with sorted
  keys and a stable format, so generating the export twice yields byte-
  identical JSON.
* **Demo data, not live data.** The two runs below are a curated, hand-authored
  demo dataset — one golden-path run and one governance review-required run.
  They contain no secrets, no credentials, no personal data, no copyrighted
  source text, and no raw free-text error or ``blocked_reason`` strings. They
  mirror the shape that a future file-backed or local-API adapter (a later
  Phase 13 subphase) would produce from real local StoryTime state.

The export envelope carries a ``schemaVersion`` so the frontend and any future
adapter can detect contract drift. See ``docs/frontend-static-export-contract.md``
for the full contract.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# The export contract schema version. Bump only on a breaking shape change;
# document every bump in docs/frontend-static-export-contract.md.
SCHEMA_VERSION = "1.0"

# Stable identifier of the producer and the kind of export. Fixed strings —
# part of the deterministic output.
GENERATED_BY = "storytime.operator_export"
EXPORT_KIND = "phase13c_static_demo"

# The committed static artifact path, relative to the repository root. The
# frontend imports this file statically (no fetch), so it lives inside the
# frontend source tree.
DEFAULT_EXPORT_RELPATH = "frontend/src/data/storytime-demo-export.json"

# A standing, display-safe governance disclaimer reused across decisions. It is
# deliberately not legal language.
_GOVERNANCE_DISCLAIMER = (
    "This is a record of a human operator's authorization decision. "
    "It is not legal advice and not a certification of copyright safety."
)


def _project_summary() -> dict[str, Any]:
    """Return the portfolio project-summary section of the export."""
    return {
        "name": "StoryTime",
        "tagline": (
            "A local-first, observability-native content-to-audio pipeline "
            "with a human-decided governance layer."
        ),
        "description": (
            "StoryTime turns approved public-domain text into podcast-ready "
            "audio, an RSS feed, and a traceable record of every run. SQLite "
            "and on-disk artifact envelopes are the source of truth; "
            "OpenTelemetry is an optional view. It was built as a "
            "portfolio-grade engineering project to show disciplined, "
            "observable, governed pipeline work — not as a hosted product."
        ),
        "currentPhase": "Phase 13C",
        "currentPhaseStatus": (
            "Implementation candidate, pending review. Phase 13C aligns the "
            "frontend with a deterministic, read-only static export produced "
            "by the backend: the data the portfolio shell shows now comes "
            "from a backend-defined export contract, still static and "
            "demo-data-backed, with no live backend and no mutations."
        ),
        "demonstrates": [
            (
                "An end-to-end pipeline (ingest, synthesize, assemble, "
                "publish) with persisted operator approval gates and resume "
                "from SQLite."
            ),
            (
                "Observability as a first-class concern: OpenTelemetry "
                "instrumentation, dashboards-as-code, and a demo harness."
            ),
            (
                "An honest governance layer: a human-decided, durably "
                "recorded Trust Envelope and a fail-closed gate before the "
                "expensive stages."
            ),
            (
                "A decoupled frontend contract: this site reads a documented, "
                "deterministic backend export — never the backend's internals."
            ),
        ],
        "notClaims": [
            (
                "Not a hosted or production-deployed product — there is no "
                "server, no user accounts, and no SLA."
            ),
            (
                "Not connected to a live backend in Phase 13C — every screen "
                "is backed by a static, deterministic demo export."
            ),
            (
                "Not a legal rights-clearance engine — governance records a "
                "human decision; it does not perform legal automation."
            ),
            (
                "Not a complete portfolio site or a complete operator GUI "
                "yet — later Phase 13 subphases build the rest."
            ),
        ],
        "reviewerPaths": [
            {
                "id": "rp-5min",
                "audience": "5-minute reviewer",
                "summary": (
                    "The fastest honest read of what StoryTime is and shows."
                ),
                "timeBudget": "~5 min",
                "steps": [
                    (
                        "Read the homepage overview and the "
                        "observability/governance points."
                    ),
                    (
                        "Open the Pipeline Run Detail view and read the "
                        "golden-path run."
                    ),
                    (
                        "Switch to the review-required run to see how "
                        "governance is shown."
                    ),
                ],
            },
            {
                "id": "rp-technical",
                "audience": "Technical reviewer",
                "summary": (
                    "For an engineer evaluating the pipeline, observability, "
                    "and the data contract."
                ),
                "timeBudget": "~20 min",
                "steps": [
                    (
                        "Read the homepage, then study both runs in the "
                        "Pipeline Run Detail view."
                    ),
                    (
                        "Note the stage timeline: stage order, status, gates, "
                        "and durations."
                    ),
                    (
                        "Review the static export contract in "
                        "docs/frontend-static-export-contract.md."
                    ),
                    (
                        "Read docs/frontend-backend-contract.md for the "
                        "backend boundary."
                    ),
                ],
            },
            {
                "id": "rp-architecture",
                "audience": "Deep architecture reviewer",
                "summary": (
                    "For a reviewer assessing architecture decisions and "
                    "phase discipline."
                ),
                "timeBudget": "~45 min",
                "steps": [
                    (
                        "Read docs/phase13-portfolio-website-architecture.md "
                        "and the frontend/backend contract."
                    ),
                    (
                        "Read docs/architecture-baseline.md sections 24 and "
                        "25 (governance, operator experience)."
                    ),
                    (
                        "Trace a run through the stage timeline and the "
                        "governance decision."
                    ),
                    (
                        "Read docs/phase13-roadmap.md for the 13A–13G subphase "
                        "decomposition."
                    ),
                ],
            },
        ],
    }


def _run_golden() -> dict[str, Any]:
    """Return the golden-path demo run (run-detail shape)."""
    return {
        "id": "run-2026-0518-golden",
        "label": "Aesop — The Fox and the Grapes (CC0 demo text)",
        "status": "succeeded",
        "createdAt": "2026-05-18T09:12:04Z",
        "updatedAt": "2026-05-18T09:21:47Z",
        "stages": [
            {
                "id": "run-2026-0518-golden:ingest",
                "name": "Ingest",
                "order": 0,
                "status": "succeeded",
                "isApprovalGate": False,
                "startedAt": "2026-05-18T09:12:04Z",
                "endedAt": "2026-05-18T09:12:39Z",
                "durationSeconds": 35,
                "note": (
                    "Source text ingested and normalized; manifest validated."
                ),
            },
            {
                "id": "run-2026-0518-golden:governance-gate",
                "name": "Governance Gate",
                "order": 1,
                "status": "succeeded",
                "isApprovalGate": True,
                "startedAt": "2026-05-18T09:12:39Z",
                "endedAt": "2026-05-18T09:13:10Z",
                "durationSeconds": 31,
                "note": (
                    "Trust Envelope APPROVED for a CC0 source; fail-closed "
                    "gate passed."
                ),
            },
            {
                "id": "run-2026-0518-golden:synthesize",
                "name": "Synthesize",
                "order": 2,
                "status": "succeeded",
                "isApprovalGate": False,
                "startedAt": "2026-05-18T09:13:10Z",
                "endedAt": "2026-05-18T09:18:02Z",
                "durationSeconds": 292,
                "note": "Narration synthesized to audio segments.",
            },
            {
                "id": "run-2026-0518-golden:assemble",
                "name": "Assemble",
                "order": 3,
                "status": "succeeded",
                "isApprovalGate": False,
                "startedAt": "2026-05-18T09:18:02Z",
                "endedAt": "2026-05-18T09:20:15Z",
                "durationSeconds": 133,
                "note": (
                    "Audio segments assembled into a single episode artifact."
                ),
            },
            {
                "id": "run-2026-0518-golden:publish-gate",
                "name": "Publish Approval",
                "order": 4,
                "status": "succeeded",
                "isApprovalGate": True,
                "startedAt": "2026-05-18T09:20:15Z",
                "endedAt": "2026-05-18T09:20:51Z",
                "durationSeconds": 36,
                "note": "Operator approved publication of the assembled episode.",
            },
            {
                "id": "run-2026-0518-golden:publish",
                "name": "Publish",
                "order": 5,
                "status": "succeeded",
                "isApprovalGate": False,
                "startedAt": "2026-05-18T09:20:51Z",
                "endedAt": "2026-05-18T09:21:47Z",
                "durationSeconds": 56,
                "note": "Episode published to the local RSS feed.",
            },
        ],
        "governance": {
            "status": "allowed",
            "contextSummary": (
                "Source authorized as CC0 public-domain text. Operator "
                "confirmed the source category before the run; the "
                "fail-closed gate passed."
            ),
            "sourceCategory": "CC0",
            "disclaimer": _GOVERNANCE_DISCLAIMER,
        },
        "failure": None,
        "artifacts": [
            {
                "id": "run-2026-0518-golden:audio",
                "label": "Assembled episode audio",
                "kind": "audio",
                "reference": "runs/run-2026-0518-golden/episode.wav",
                "durationSeconds": 224,
                "sizeBytes": 7168000,
            },
            {
                "id": "run-2026-0518-golden:feed",
                "label": "Local RSS feed entry",
                "kind": "feed",
                "reference": "feed/index.xml#run-2026-0518-golden",
                "durationSeconds": None,
                "sizeBytes": None,
            },
            {
                "id": "run-2026-0518-golden:report",
                "label": "Static operator report (run page)",
                "kind": "report",
                "reference": "operator-report/run-run-2026-0518-golden.html",
                "durationSeconds": None,
                "sizeBytes": None,
            },
        ],
        "observability": {
            "correlationKey": "run-2026-0518-golden",
            "traceId": "trace-9f3c12ab",
            "links": [
                {
                    "id": "run-2026-0518-golden:trace",
                    "label": "Pipeline trace",
                    "kind": "trace",
                    "reference": "trace://local/trace-9f3c12ab",
                    "note": (
                        "Per-stage spans for the full ingest-to-publish run."
                    ),
                },
                {
                    "id": "run-2026-0518-golden:dashboard",
                    "label": "Pipeline overview dashboard",
                    "kind": "dashboard",
                    "reference": "grafana/dashboards/pipeline-overview.json",
                    "note": "Dashboard-as-code reference; not embedded here.",
                },
            ],
        },
        "stateExplanation": (
            "This run completed end to end. All six stages succeeded, "
            "governance allowed the CC0 source, and the episode was published "
            "to the local feed. No operator action is needed."
        ),
        "allowedActions": [
            {
                "id": "run-2026-0518-golden:copy-report-cmd",
                "label": "Copy: regenerate operator report command",
                "kind": "copy_command",
                "description": (
                    "Surfaces the CLI command an operator would run to "
                    "regenerate the static operator report. The frontend only "
                    "shows the command; it does not run anything."
                ),
                "payload": "uv run storytime report generate",
            },
            {
                "id": "run-2026-0518-golden:open-report",
                "label": "Open static operator report (reference)",
                "kind": "open_reference",
                "description": (
                    "Points at the existing static HTML operator report for "
                    "this run. Shown as a reference in the static shell."
                ),
                "payload": "operator-report/run-run-2026-0518-golden.html",
            },
        ],
        "disabledActions": [
            {
                "id": "run-2026-0518-golden:rerun",
                "label": "Re-run this pipeline run",
                "disabledReason": (
                    "Mutation actions are not implemented in Phase 13C. This "
                    "run also succeeded, so there is nothing to re-run."
                ),
                "enabledByPhase": "Phase 13E",
                "isMutation": True,
            },
        ],
    }


def _run_review() -> dict[str, Any]:
    """Return the governance review-required demo run (run-detail shape)."""
    return {
        "id": "run-2026-0520-review",
        "label": "Untitled community submission (source pending review)",
        "status": "blocked",
        "createdAt": "2026-05-20T13:48:55Z",
        "updatedAt": "2026-05-20T13:51:30Z",
        "stages": [
            {
                "id": "run-2026-0520-review:ingest",
                "name": "Ingest",
                "order": 0,
                "status": "succeeded",
                "isApprovalGate": False,
                "startedAt": "2026-05-20T13:48:55Z",
                "endedAt": "2026-05-20T13:49:33Z",
                "durationSeconds": 38,
                "note": (
                    "Source text ingested and normalized; manifest validated."
                ),
            },
            {
                "id": "run-2026-0520-review:governance-gate",
                "name": "Governance Gate",
                "order": 1,
                "status": "blocked",
                "isApprovalGate": True,
                "startedAt": "2026-05-20T13:49:33Z",
                "endedAt": "2026-05-20T13:51:30Z",
                "durationSeconds": 117,
                "note": (
                    "Fail-closed gate held the run: the source category "
                    "needs an operator review decision before the run may "
                    "continue."
                ),
            },
            {
                "id": "run-2026-0520-review:synthesize",
                "name": "Synthesize",
                "order": 2,
                "status": "not_started",
                "isApprovalGate": False,
                "startedAt": None,
                "endedAt": None,
                "durationSeconds": None,
                "note": "Not started — the run is held at the governance gate.",
            },
            {
                "id": "run-2026-0520-review:assemble",
                "name": "Assemble",
                "order": 3,
                "status": "not_started",
                "isApprovalGate": False,
                "startedAt": None,
                "endedAt": None,
                "durationSeconds": None,
                "note": "Not started — the run is held at the governance gate.",
            },
            {
                "id": "run-2026-0520-review:publish-gate",
                "name": "Publish Approval",
                "order": 4,
                "status": "not_started",
                "isApprovalGate": True,
                "startedAt": None,
                "endedAt": None,
                "durationSeconds": None,
                "note": "Not started — the run is held at the governance gate.",
            },
            {
                "id": "run-2026-0520-review:publish",
                "name": "Publish",
                "order": 5,
                "status": "not_started",
                "isApprovalGate": False,
                "startedAt": None,
                "endedAt": None,
                "durationSeconds": None,
                "note": "Not started — the run is held at the governance gate.",
            },
        ],
        "governance": {
            "status": "review_required",
            "contextSummary": (
                "The submitted source has no confirmed authorization "
                "category yet. The fail-closed gate held the run so an "
                "operator can review the source and record an explicit "
                "decision. No expensive stage ran."
            ),
            "sourceCategory": "PENDING_REVIEW",
            "disclaimer": _GOVERNANCE_DISCLAIMER,
        },
        "failure": {
            "errorKind": "GOVERNANCE_REVIEW_REQUIRED",
            "operatorGuidance": (
                "Review the source and record an authorization decision. If "
                "the source is authorized, the run can be retried; if not, it "
                "stays blocked. This is expected fail-closed behaviour, not a "
                "defect."
            ),
        },
        "artifacts": [],
        "observability": {
            "correlationKey": "run-2026-0520-review",
            "traceId": "trace-2b71d004",
            "links": [
                {
                    "id": "run-2026-0520-review:trace",
                    "label": "Pipeline trace (partial run)",
                    "kind": "trace",
                    "reference": "trace://local/trace-2b71d004",
                    "note": "Spans for ingest and the governance gate only.",
                },
            ],
        },
        "stateExplanation": (
            "This run is held at the governance gate. The fail-closed gate "
            "did its job: it stopped the run before any expensive stage "
            "because the source needs a human authorization decision. The run "
            "is blocked, not failed."
        ),
        "allowedActions": [
            {
                "id": "run-2026-0520-review:copy-queue-cmd",
                "label": "Copy: inspect the review queue command",
                "kind": "copy_command",
                "description": (
                    "Surfaces the CLI command that lists runs needing "
                    "operator attention. The frontend only shows the command; "
                    "it does not run it."
                ),
                "payload": "uv run storytime queue --status needs-review",
            },
        ],
        "disabledActions": [
            {
                "id": "run-2026-0520-review:open-review",
                "label": "Open review workflow",
                "disabledReason": (
                    "Recording a governance review decision is a true "
                    "mutation and is not implemented in Phase 13C. The "
                    "operator GUI is read-only here."
                ),
                "enabledByPhase": "Phase 13E",
                "isMutation": True,
            },
            {
                "id": "run-2026-0520-review:retry",
                "label": "Retry after review",
                "disabledReason": (
                    "Retrying a run is a true mutation and is not implemented "
                    "in Phase 13C. It would also only be eligible once the "
                    "source has an authorization decision."
                ),
                "enabledByPhase": "Phase 13E",
                "isMutation": True,
            },
        ],
    }


def _failure_queue() -> list[dict[str, Any]]:
    """Return the failure / review queue projection for the export."""
    return [
        {
            "runId": "run-2026-0520-review",
            "runLabel": (
                "Untitled community submission (source pending review)"
            ),
            "reason": "needs_review",
            "summary": (
                "Held at the governance gate — the source needs an operator "
                "authorization decision."
            ),
            "inspectNext": (
                "Open this run in the Pipeline Run Detail view and read the "
                "governance section."
            ),
        },
    ]


def _prune(value: Any) -> Any:
    """Recursively drop ``None``-valued mapping keys for a clean, stable JSON.

    Optional fields are represented in the frontend contract as absent keys
    (TypeScript ``?:``), not as ``null``. Dropping ``None`` values here keeps
    the JSON aligned with that contract. Ordering is preserved, so the result
    stays deterministic; ``render_export_json`` additionally sorts keys.
    """
    if isinstance(value, dict):
        return {
            key: _prune(item)
            for key, item in value.items()
            if item is not None
        }
    if isinstance(value, list):
        return [_prune(item) for item in value]
    return value


def build_static_demo_export() -> dict[str, Any]:
    """Build the full static demo export envelope.

    The result is a plain, JSON-serializable mapping built entirely from fixed
    demo data. It is deterministic: calling this function any number of times,
    on any machine, returns equal content.
    """
    envelope: dict[str, Any] = {
        "schemaVersion": SCHEMA_VERSION,
        "generatedBy": GENERATED_BY,
        "exportKind": EXPORT_KIND,
        "project": _project_summary(),
        "runs": [_run_golden(), _run_review()],
        "failureQueue": _failure_queue(),
    }
    pruned: dict[str, Any] = {
        key: _prune(value) for key, value in envelope.items()
    }
    return pruned


def render_export_json(export: dict[str, Any]) -> str:
    """Serialize an export mapping to deterministic, byte-stable JSON text.

    Keys are sorted, indentation is fixed, and a single trailing newline is
    appended. Serializing the same export twice always yields identical text.
    """
    return (
        json.dumps(export, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    )


def write_static_demo_export(path: Path) -> Path:
    """Write the deterministic static demo export to *path*.

    The parent directory must already exist (it is part of the frontend source
    tree). Returns the path written. This is the only function in this module
    that touches the filesystem, and it only writes the one static artifact.
    """
    text = render_export_json(build_static_demo_export())
    path.write_text(text, encoding="utf-8")
    return path
