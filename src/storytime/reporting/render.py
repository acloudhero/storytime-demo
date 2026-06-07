"""Render the operator-report model to static, air-gapped HTML.

ARCH-LOCK: Static, air-gapped, read-only report rendering
DO NOT REFACTOR: This module renders the locked §25 operator report. It uses
only the Python standard library (``html.escape`` for escaping) — no Jinja2,
no template dependency, no frontend framework, no build step (§25.15). The
generated HTML is fully self-contained: embedded ``<style>`` plus a local
``style.css`` are the only styling; there are no external CDN links, fonts,
scripts, icons, or remote favicons (air-gapped constraint). The report renders
correctly with zero network access.

Rendering is pure and deterministic: every function is a pure transform of the
report model plus an injected ``generated_at`` string, so identical input
yields byte-for-byte identical output. There is no JavaScript, no form, no
button, and no state-changing link — the report is strictly read-only (§25.10,
§25.17). All dynamic text is HTML-escaped.

Phase 10E adds: executive status summary, rerun eligibility section, command
reference section, richer status badges, improved governance warning block,
and improved CSS.  All new sections are read-only and contain no JavaScript.
"""

from __future__ import annotations

from html import escape

from storytime.reporting.model import (
    OperatorReport,
    RunDetail,
    RunSummary,
)

# Number of most-recent runs shown in the latest-runs summary on index.html.
_LATEST_RUNS_ON_INDEX = 10

# The §25.5 governance disclaimer.  Neutral wording: records that the report
# reflects human operator decisions and pipeline state, and is explicitly not
# legal advice.  Contains none of the §24.14 forbidden overclaiming terms.
_DISCLAIMER = (
    "StoryTime records human operator decisions and pipeline state. "
    "This report is not legal advice or certification of copyright safety."
)

# Short, neutral explanation shown on every page.
_READ_ONLY_NOTE = (
    "This report is read-only and was generated locally from the StoryTime "
    "SQLite state database and on-disk artifacts, which remain the source of "
    "truth. It changes nothing and contains no controls that change state."
)

# ---------------------------------------------------------------------------
# Stylesheet — embedded in every page via <style> for offline resilience, and
# also written as style.css for the external <link> fallback.  Minimal by
# design (§25 styling ceiling): readable layout, semantic status colours, and
# simple command-block presentation.  No animation, no design system, no
# framework, no external font.
# ---------------------------------------------------------------------------
STYLE_CSS = """\
/* StoryTime operator report — Phase 10E minimal stylesheet.
   Self-contained, no external assets, no network fonts. */

/* ── reset / base ─────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
body {
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 0.95rem;
  line-height: 1.55;
  max-width: 62rem;
  margin: 1.5rem auto;
  padding: 0 1rem;
  color: #1a1a1a;
  background: #ffffff;
}
a { color: #14506e; }
a:hover { text-decoration: underline; }

/* ── headings ──────────────────────────────────────────────────────── */
h1, h2, h3 { line-height: 1.25; margin-top: 1.5rem; }
h1 { font-size: 1.35rem; margin-top: 0.5rem; }
h2 { font-size: 1.1rem; border-bottom: 1px solid #ddd; padding-bottom: 0.25rem; }
h3 { font-size: 1rem; margin-top: 1rem; }

/* ── tables ────────────────────────────────────────────────────────── */
table { border-collapse: collapse; width: 100%; margin: 0.5rem 0 1rem; }
th, td {
  border: 1px solid #d0d0d0;
  padding: 0.4rem 0.6rem;
  text-align: left;
  vertical-align: top;
}
th { background: #f2f2f2; font-weight: 600; white-space: nowrap; }
tr:hover { background: #fafafa; }

/* ── inline code / pre ─────────────────────────────────────────────── */
code { background: #f0f0f0; padding: 0.1rem 0.3rem; border-radius: 3px;
       font-family: monospace; font-size: 0.88em; }
pre.command-block {
  background: #1e1e2e;
  color: #cdd6f4;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 0.75rem 1rem;
  font-family: monospace;
  font-size: 0.875rem;
  line-height: 1.6;
  white-space: pre;
  overflow-x: auto;
  margin: 0.5rem 0;
}

/* ── notice boxes ──────────────────────────────────────────────────── */
.governance-warning {
  border: 2px solid #b87000;
  background: #fff8e6;
  border-radius: 4px;
  padding: 0.6rem 0.9rem;
  margin: 0.75rem 0 1rem;
  font-size: 0.9rem;
}
.governance-warning strong { color: #7a4b00; }

.attention-box {
  border-left: 4px solid #c0392b;
  background: #fdf3f3;
  padding: 0.6rem 0.9rem;
  margin: 0.75rem 0;
  border-radius: 0 4px 4px 0;
}
.rerun-eligible-box {
  border-left: 4px solid #27ae60;
  background: #f0faf4;
  padding: 0.6rem 0.9rem;
  margin: 0.75rem 0;
  border-radius: 0 4px 4px 0;
}
.rerun-blocked-box {
  border-left: 4px solid #e67e22;
  background: #fdf6ec;
  padding: 0.6rem 0.9rem;
  margin: 0.75rem 0;
  border-radius: 0 4px 4px 0;
}
.info-box {
  border: 1px solid #b0c4d8;
  background: #f0f6fc;
  border-radius: 4px;
  padding: 0.6rem 0.9rem;
  margin: 0.75rem 0;
}

/* ── status badges ─────────────────────────────────────────────────── */
.badge {
  display: inline-block;
  padding: 0.15rem 0.5rem;
  border-radius: 3px;
  font-size: 0.82rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  vertical-align: middle;
}
.badge-completed  { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
.badge-failed     { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
.badge-running    { background: #cce5ff; color: #004085; border: 1px solid #b8daff; }
.badge-blocked    { background: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
.badge-approved   { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
.badge-rejected   { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
.badge-needs-review { background: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
.badge-unknown    { background: #e2e3e5; color: #383d41; border: 1px solid #d6d8db; }
.badge-eligible   { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
.badge-ineligible { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }

/* ── summary grid (executive summary) ─────────────────────────────── */
.summary-grid {
  display: grid;
  grid-template-columns: max-content 1fr;
  gap: 0.3rem 0.75rem;
  margin: 0.5rem 0 1rem;
}
.summary-grid dt {
  font-weight: 600;
  color: #444;
  white-space: nowrap;
}
.summary-grid dd { margin: 0; }

/* ── navigation / footer ───────────────────────────────────────────── */
.breadcrumb { margin-bottom: 0.75rem; color: #555; font-size: 0.9rem; }
footer {
  margin-top: 2.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid #e0e0e0;
  color: #666;
  font-size: 0.85rem;
}

/* ── helpers ───────────────────────────────────────────────────────── */
.note  { color: #555; font-size: 0.9rem; }
.empty { color: #777; font-style: italic; }
.section-intro { margin: 0.25rem 0 0.6rem; color: #444; font-size: 0.9rem; }

/* ── responsive (narrow screens) ──────────────────────────────────── */
@media (max-width: 480px) {
  body { margin: 0.75rem auto; }
  h1 { font-size: 1.15rem; }
  .summary-grid { grid-template-columns: 1fr; }
  pre.command-block { font-size: 0.8rem; }
}
"""


def run_detail_filename(run_id: str) -> str:
    """Return the detail-page filename for a run (``run-<run_id>.html``)."""
    return f"run-{run_id}.html"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _status_badge(status: str) -> str:
    """Render a semantic status badge for *status*."""
    s = status.lower()
    if s in ("completed", "succeeded", "published"):
        cls = "badge-completed"
    elif s == "failed":
        cls = "badge-failed"
    elif s in ("running", "resuming"):
        cls = "badge-running"
    elif s in ("blocked", "needs_review", "awaiting_approval"):
        cls = "badge-blocked"
    elif s == "approved":
        cls = "badge-approved"
    elif s in ("rejected",):
        cls = "badge-rejected"
    else:
        cls = "badge-unknown"
    return f'<span class="badge {cls}">{escape(status)}</span>'


def _governance_badge(decision: str | None) -> str:
    """Render a governance decision badge."""
    if decision is None:
        return '<span class="badge badge-unknown">not recorded</span>'
    d = decision.upper()
    if d == "APPROVED":
        cls = "badge-approved"
    elif d in ("BLOCKED", "REJECTED"):
        cls = "badge-rejected"
    elif d == "NEEDS_REVIEW":
        cls = "badge-needs-review"
    else:
        cls = "badge-unknown"
    return f'<span class="badge {cls}">{escape(decision)}</span>'


def _page(title: str, body: str, generated_at: str) -> str:
    """Wrap *body* in the shared, air-gapped HTML page shell.

    The ``<style>`` block is embedded directly in every page so the report
    renders correctly even when opened as a standalone file without style.css.
    The ``<link>`` to ``style.css`` is kept as a fallback for browsers that
    prefer an external sheet.  There are no external links of any kind.
    ``generated_at`` is the injected timestamp, shown in the footer.
    """
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{escape(title)}</title>\n"
        '<link rel="stylesheet" href="style.css">\n'
        f"<style>\n{STYLE_CSS}</style>\n"
        "</head>\n"
        "<body>\n"
        f"{body}"
        '<footer>Generated at '
        f"{escape(generated_at)} &middot; StoryTime operator report "
        "(read-only, generated locally, no external assets).</footer>\n"
        "</body>\n"
        "</html>\n"
    )


def _disclaimer_block() -> str:
    """Return the standing governance disclaimer block (§25.5).

    The governance warning must remain visually distinct and near the top of
    every page (Phase 10E structural guardrail).
    """
    return (
        '<div class="governance-warning">\n'
        f'<strong>Governance notice:</strong> {escape(_DISCLAIMER)}\n'
        "</div>\n"
    )


def _governance_cell(decision: str | None) -> str:
    """Render a run's governance decision for a table cell."""
    return _governance_badge(decision)


def _run_row(summary: RunSummary) -> str:
    """Render one run as a table row linking to its detail page."""
    href = escape(run_detail_filename(summary.run_id), quote=True)
    return (
        "<tr>"
        f'<td><a href="{href}"><code>{escape(summary.run_id)}</code></a></td>'
        f"<td>{_status_badge(summary.status)}</td>"
        f"<td>{escape(summary.current_stage)}</td>"
        f"<td>{escape(summary.created_at)}</td>"
        f"<td>{escape(summary.updated_at)}</td>"
        f"<td>{_governance_cell(summary.governance_decision)}</td>"
        "</tr>\n"
    )


def _runs_table(runs: tuple[RunSummary, ...]) -> str:
    """Render the run list as an HTML table, or an empty-state message."""
    if not runs:
        return '<p class="empty">No pipeline runs have been recorded yet.</p>\n'
    rows = "".join(_run_row(run) for run in runs)
    return (
        "<table>\n"
        "<thead><tr>"
        "<th>Run ID</th><th>Status</th><th>Current stage</th>"
        "<th>Created</th><th>Updated</th><th>Governance decision</th>"
        "</tr></thead>\n"
        f"<tbody>\n{rows}</tbody>\n"
        "</table>\n"
    )


# ---------------------------------------------------------------------------
# Run-detail sections
# ---------------------------------------------------------------------------

def _executive_summary_section(detail: RunDetail) -> str:
    """Render the executive status summary — the first section on a detail page.

    Shows run status, governance decision, rerun eligibility, and the
    recommended next operator action in a compact, scannable layout.
    All fields are safe bounded projections.
    """
    gov_decision = (
        detail.governance.decision if detail.governance else None
    )
    rerun = detail.rerun

    # Determine attention status
    if detail.status == "failed":
        if rerun is not None and rerun.eligible:
            attention = "Failed — rerun eligible"
            attention_cls = "rerun-eligible-box"
        else:
            attention = "Failed — requires operator attention"
            attention_cls = "attention-box"
    elif detail.status in ("blocked",):
        attention = "Blocked by governance"
        attention_cls = "rerun-blocked-box"
    elif detail.status == "completed":
        attention = "Completed successfully"
        attention_cls = "info-box"
    else:
        attention = escape(detail.status)
        attention_cls = "info-box"

    # Next recommended action
    if rerun is not None and rerun.eligible:
        next_action = (
            f"Preview rerun: <code>storytime rerun {escape(detail.run_id)} --dry-run</code>"
        )
    elif detail.status == "failed":
        next_action = "Inspect the failure and governance sections below."
    elif detail.status in ("blocked",):
        next_action = "Inspect the governance section; resolve the block before retrying."
    elif detail.status == "completed":
        next_action = "No action required."
    else:
        next_action = "Review the stages and governance sections below."

    return (
        "<h2>Executive Summary</h2>\n"
        f'<div class="{attention_cls}">\n'
        '<dl class="summary-grid">\n'
        f"<dt>Run ID</dt><dd><code>{escape(detail.run_id)}</code></dd>\n"
        f"<dt>Status</dt><dd>{_status_badge(detail.status)}</dd>\n"
        f"<dt>Stage</dt><dd><code>{escape(detail.current_stage)}</code></dd>\n"
        f"<dt>Attention</dt><dd>{escape(attention)}</dd>\n"
        f"<dt>Governance</dt><dd>{_governance_badge(gov_decision)}</dd>\n"
    ) + (
        (
            "<dt>Rerun eligible</dt>"
            '<dd><span class="badge badge-eligible">YES</span></dd>\n'
        )
        if rerun is not None and rerun.eligible
        else (
            "<dt>Rerun eligible</dt>"
            '<dd><span class="badge badge-ineligible">NO</span></dd>\n'
        )
        if rerun is not None
        else ""
    ) + (
        f"<dt>Next action</dt><dd>{next_action}</dd>\n"
        "</dl>\n"
        "</div>\n"
    )


def _failure_section(detail: RunDetail) -> str:
    """Render the structured failure summary, when the run failed."""
    if detail.failure_stage is None and detail.failure_category is None:
        return ""
    stage = detail.failure_stage or "unknown"
    category = detail.failure_category or "unknown"

    # Classify failure type for operator guidance
    if category.endswith("Rejected"):
        failure_type = "Operator rejection at approval gate"
        guidance = (
            "This run was rejected by an operator at an approval gate. "
            "A rerun cannot override an operator rejection. "
            "Start a new run if the source should be reconsidered."
        )
    elif "Governance" in category or "Trust" in category:
        failure_type = "Governance / Trust Envelope failure"
        guidance = (
            "This run failed due to a governance or Trust Envelope issue. "
            "Review the Governance section below and resolve before retrying."
        )
    else:
        failure_type = "Pipeline stage failure"
        guidance = (
            "This is a technical pipeline failure. If the source is approved, "
            "use the rerun commands below to retry from the failed stage."
        )

    return (
        "<h2>Failure Summary</h2>\n"
        '<div class="attention-box">\n'
        '<dl class="summary-grid">\n'
        f"<dt>Failed stage</dt><dd><code>{escape(stage)}</code></dd>\n"
        f"<dt>Failure category</dt><dd><code>{escape(category)}</code></dd>\n"
        f"<dt>Failure type</dt><dd>{escape(failure_type)}</dd>\n"
        f"<dt>Guidance</dt><dd>{escape(guidance)}</dd>\n"
        "</dl>\n"
        "</div>\n"
    )


def _rerun_section(detail: RunDetail) -> str:
    """Render the Phase 10D rerun eligibility and action guidance section.

    Shows whether the run is eligible for rerun, the stable decision code,
    a safe operator-facing message, and — when eligible — the plain-text
    commands the operator should run next.  Commands are plain text only;
    they are never clickable mutation controls.
    """
    rerun = detail.rerun
    if rerun is None:
        # No rerun projection available (run not failed, or projection failed).
        if detail.status != "failed":
            return (
                "<h2>Rerun Eligibility</h2>\n"
                '<p class="empty">Rerun is not applicable for this run '
                f"(status: <code>{escape(detail.status)}</code>).</p>\n"
            )
        return (
            "<h2>Rerun Eligibility</h2>\n"
            '<p class="empty">Rerun eligibility could not be determined.</p>\n'
        )

    if rerun.eligible:
        commands = rerun.next_command or (
            f"storytime rerun {escape(detail.run_id)} --dry-run\n"
            f"storytime rerun {escape(detail.run_id)}\n"
            f"storytime run --resume {escape(detail.run_id)}"
        )
        return (
            "<h2>Rerun Eligibility</h2>\n"
            '<div class="rerun-eligible-box">\n'
            f'<p><span class="badge badge-eligible">ELIGIBLE</span> '
            f"&nbsp;{escape(rerun.message)}</p>\n"
            '<dl class="summary-grid">\n'
            f"<dt>Decision code</dt><dd><code>{escape(rerun.code)}</code></dd>\n"
            f"<dt>From stage</dt><dd><code>{escape(rerun.from_stage or '-')}</code></dd>\n"
            f"<dt>Governance</dt><dd>{_governance_badge(rerun.governance_status)}</dd>\n"
            "</dl>\n"
            "</div>\n"
            "<h3>Commands</h3>\n"
            '<p class="section-intro">These are plain-text commands only — '
            "copy and run in your terminal. The report contains no buttons "
            "or controls that execute commands.</p>\n"
            f'<pre class="command-block">{escape(commands)}</pre>\n'
        )
    else:
        return (
            "<h2>Rerun Eligibility</h2>\n"
            '<div class="rerun-blocked-box">\n'
            f'<p><span class="badge badge-ineligible">NOT ELIGIBLE</span> '
            f"&nbsp;{escape(rerun.message)}</p>\n"
            '<dl class="summary-grid">\n'
            f"<dt>Decision code</dt><dd><code>{escape(rerun.code)}</code></dd>\n"
        ) + (
            f"<dt>From stage</dt><dd><code>{escape(rerun.from_stage)}</code></dd>\n"
            if rerun.from_stage else ""
        ) + (
            f"<dt>Governance</dt><dd>{_governance_badge(rerun.governance_status)}</dd>\n"
            if rerun.governance_status else ""
        ) + (
            "</dl>\n"
            "</div>\n"
        )


def _stages_section(detail: RunDetail) -> str:
    """Render the per-stage status table for a run-detail page."""
    if not detail.stages:
        return (
            "<h2>Stages</h2>\n"
            '<p class="empty">No stage executions recorded for this run.</p>\n'
        )
    def _error_cell(error_kind: str | None) -> str:
        if error_kind is None:
            return '<span class="empty">—</span>'
        return "<code>" + escape(error_kind) + "</code>"

    rows = "".join(
        "<tr>"
        f"<td><code>{escape(stage.name)}</code></td>"
        f"<td>{_status_badge(stage.status)}</td>"
        f"<td>{_error_cell(stage.error_kind)}</td>"
        "</tr>\n"
        for stage in detail.stages
    )
    return (
        "<h2>Stages</h2>\n"
        "<table>\n"
        "<thead><tr><th>Stage</th><th>Status</th><th>Failure category</th>"
        "</tr></thead>\n"
        f"<tbody>\n{rows}</tbody>\n"
        "</table>\n"
    )


def _governance_section(detail: RunDetail) -> str:
    """Render the governance / Trust Envelope summary (§25.5).

    The governance warning must remain visually distinct and prominent.
    No raw blocked-reason text or sensitive internals are shown.
    """
    governance = detail.governance
    if governance is None:
        return (
            "<h2>Governance / Trust Envelope</h2>\n"
            '<p class="empty">No Trust Envelope recorded for this run.</p>\n'
        )

    summary = governance.review_context_summary
    summary_html = (
        escape(summary)
        if summary
        else '<span class="empty">no rationale recorded</span>'
    )

    decision_badge = _governance_badge(governance.decision)
    rows = [
        ("Governance decision", decision_badge),
        ("License type", f"<code>{escape(governance.license_type)}</code>"),
        ("Approved by operator", escape(governance.approver_id)),
        ("Decision timestamp", escape(governance.decision_timestamp)),
    ]
    if governance.blocked_reason:
        # The raw blocked_reason is never rendered (§25.12 redaction rule).
        # The full required phrase appears as one rendered value string.
        rows.append(
            (
                "Governance detail",
                "Decision detail: blocked by governance policy;"
                " inspect Trust Envelope locally if authorized.",
            )
        )
    rows.append(("Review context summary", summary_html))
    if governance.trust_envelope_key:
        rows.append(
            (
                "Trust Envelope artifact",
                f"<code>{escape(governance.trust_envelope_key)}</code>",
            )
        )

    body = "".join(
        f"<tr><th>{label}</th><td>{value}</td></tr>\n" for label, value in rows
    )
    return (
        "<h2>Governance / Trust Envelope</h2>\n"
        '<p class="section-intro">Governance decisions are recorded by the '
        "local human operator and reflected here as a bounded projection. "
        "No raw story content, source text, or sensitive internals are shown.</p>\n"
        f"<table>\n<tbody>\n{body}</tbody>\n</table>\n"
    )


def _artifacts_section(detail: RunDetail) -> str:
    """Render a run's read-only artifact references as text paths.

    Artifact paths are shown as code text, not as clickable links: they are
    relative storage keys under the runs / feed directories, which are
    separate roots from the report directory, so a relative hyperlink would
    not resolve. Showing them as text references is honest and keeps the
    output deterministic and free of absolute host paths (§25.12, §25.16).
    """
    if not detail.artifacts:
        return (
            "<h2>Artifacts</h2>\n"
            '<p class="empty">No artifact references recorded for this run.</p>\n'
        )
    rows = "".join(
        f"<tr><td>{escape(ref.label)}</td>"
        f"<td><code>{escape(ref.key)}</code></td></tr>\n"
        for ref in detail.artifacts
    )
    return (
        "<h2>Artifacts</h2>\n"
        "<table>\n"
        "<thead><tr><th>Artifact</th><th>Path (local reference)</th></tr></thead>\n"
        f"<tbody>\n{rows}</tbody>\n"
        "</table>\n"
    )


def _observability_section(detail: RunDetail) -> str:
    """Render a run's optional observability links (§25.14).

    Observability links are optional references only. When none are configured
    the section says so and the report remains complete.
    """
    if not detail.observability_links:
        return (
            "<h2>Observability</h2>\n"
            '<p class="empty">No observability links configured. '
            "Observability dashboards are optional references; the report is "
            "complete without them.</p>\n"
        )
    rows = "".join(
        f"<tr><td>{escape(link.label)}</td>"
        f'<td><a href="{escape(link.url, quote=True)}">{escape(link.url)}</a></td></tr>\n'
        for link in detail.observability_links
    )
    return (
        "<h2>Observability</h2>\n"
        '<p class="note">Optional references to configured dashboards. '
        "The report does not embed dashboard data.</p>\n"
        "<table>\n"
        "<thead><tr><th>Link</th><th>URL</th></tr></thead>\n"
        f"<tbody>\n{rows}</tbody>\n"
        "</table>\n"
    )


def _command_reference_section(detail: RunDetail) -> str:
    """Render a short contextual command reference section.

    Shows the relevant local commands as plain text only.  This section is
    a read-only reference; it contains no buttons, forms, or mutation controls.
    """
    run_id = escape(detail.run_id)
    commands = (
        f"# Inspect the failure queue\n"
        f"storytime queue\n\n"
        f"# Preview a rerun (dry run — no state change)\n"
        f"storytime rerun {run_id} --dry-run\n\n"
        f"# Request a rerun (resets status to allow resume)\n"
        f"storytime rerun {run_id}\n\n"
        f"# Re-execute after a rerun reset\n"
        f"storytime run --resume {run_id}\n\n"
        f"# Regenerate this report\n"
        f"storytime report generate"
    )
    return (
        "<h2>Command Reference</h2>\n"
        '<p class="section-intro">Local CLI commands for this run. '
        "These are plain-text references only — copy and run in your terminal. "
        "This report contains no controls that execute commands or change state.</p>\n"
        f'<pre class="command-block">{commands}</pre>\n'
    )


# ---------------------------------------------------------------------------
# Page renderers
# ---------------------------------------------------------------------------

def render_index(report: OperatorReport) -> str:
    """Render ``index.html`` — the landing page and latest-runs summary."""
    latest = report.runs[:_LATEST_RUNS_ON_INDEX]

    # Build a quick attention summary
    total = len(report.runs)
    failed = sum(1 for r in report.runs if r.status == "failed")
    blocked = sum(1 for r in report.runs if r.status == "blocked")
    needs_attention = failed + blocked

    attention_note = ""
    if needs_attention > 0:
        attention_note = (
            f'<div class="attention-box">'
            f"<strong>{needs_attention} run(s) need attention</strong>"
            f" &mdash; {failed} failed, {blocked} blocked."
            "</div>\n"
        )
    elif total > 0:
        attention_note = (
            '<div class="info-box">'
            "No runs currently need operator attention."
            "</div>\n"
        )

    body = (
        "<h1>StoryTime operator report</h1>\n"
        f'<p class="note">{escape(_READ_ONLY_NOTE)}</p>\n'
        f"{_disclaimer_block()}"
        f"{attention_note}"
        f'<p><a href="runs.html">View the full run list &rarr;</a></p>\n'
        f"<h2>Latest runs ({len(latest)} of {total})</h2>\n"
        f"{_runs_table(latest)}"
    )
    return _page("StoryTime operator report", body, report.generated_at)


def render_runs(report: OperatorReport) -> str:
    """Render ``runs.html`` — the full run list."""
    body = (
        "<h1>All pipeline runs</h1>\n"
        '<p class="breadcrumb"><a href="index.html">&larr; Back to summary</a></p>\n'
        f"{_disclaimer_block()}"
        f"<h2>Runs ({len(report.runs)})</h2>\n"
        f"{_runs_table(report.runs)}"
    )
    return _page("StoryTime runs", body, report.generated_at)


def render_run_detail(detail: RunDetail, generated_at: str) -> str:
    """Render ``run-<run_id>.html`` — the single-run detail page.

    Section order (Phase 10E):
    1. Governance warning (§25.5 — always near the top)
    2. Executive status summary
    3. Failure summary (when failed)
    4. Rerun eligibility / action guidance (when status is failed)
    5. Stages
    6. Governance / Trust Envelope detail
    7. Artifacts
    8. Observability
    9. Command reference
    """
    gates = ", ".join(detail.gates) if detail.gates else "none"
    body = (
        f"<h1>Run <code>{escape(detail.run_id)}</code></h1>\n"
        '<p class="breadcrumb">'
        '<a href="runs.html">&larr; Back to run list</a> &middot; '
        '<a href="index.html">Summary</a></p>\n'
        f"{_disclaimer_block()}"
        f"{_executive_summary_section(detail)}"
        "<h2>Overview</h2>\n"
        "<table>\n<tbody>\n"
        f"<tr><th>Run ID</th><td><code>{escape(detail.run_id)}</code></td></tr>\n"
        f"<tr><th>Status</th><td>{_status_badge(detail.status)}</td></tr>\n"
        f"<tr><th>Current stage</th><td><code>{escape(detail.current_stage)}</code></td></tr>\n"
        f"<tr><th>Created</th><td>{escape(detail.created_at)}</td></tr>\n"
        f"<tr><th>Updated</th><td>{escape(detail.updated_at)}</td></tr>\n"
        f"<tr><th>Approval gates</th><td>{escape(gates)}</td></tr>\n"
        "</tbody>\n</table>\n"
        f"{_failure_section(detail)}"
        f"{_rerun_section(detail)}"
        f"{_stages_section(detail)}"
        f"{_governance_section(detail)}"
        f"{_artifacts_section(detail)}"
        f"{_observability_section(detail)}"
        f"{_command_reference_section(detail)}"
    )
    return _page(f"Run {detail.run_id}", body, generated_at)
