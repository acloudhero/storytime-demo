"""Operator-report data model — the Phase 10B deterministic report shape.

ARCH-LOCK: Report model is a projection, never a source of truth
DO NOT REFACTOR: This module is the concrete §25.11 report data model of the
locked Architecture Baseline Section 25 (the Phase 10A Operator Experience
Baseline amendment). Every field here is a *bounded projection* of existing
authoritative state — the SQLite run/stage/Trust-Envelope projections and the
durable artifact references. SQLite and the on-disk artifact envelopes remain
the source of truth (§25.4); a generated report is a view, never authoritative.

This module is pure data. It imports nothing from StoryTime and holds no raw
story text, narration, transcripts, secrets, or unbounded free text — the
§25.12 report field blacklist. The collector (``reporting.collect``) is the
only thing that fills these dataclasses, and it fills them only from existing
projections.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# The locked §25.13 maximum displayed length for ``review_context_summary``.
# Phase 10A fixed this bound at 500 characters; the rendered report never shows
# more than this many characters of the operator's governance rationale, and a
# longer summary is safely truncated with a visible indicator. The privacy
# guarantee — no raw content, no unbounded text reaches the report — is the
# binding rule; this number is the testable guardrail that enforces it.
REVIEW_CONTEXT_SUMMARY_MAX_CHARS = 500


@dataclass(frozen=True, slots=True)
class StageView:
    """One pipeline stage's status, as shown on a run-detail page.

    ``error_kind`` is the structured failure *category* (e.g. ``"TtsError"``)
    when a stage failed — never an unbounded stack trace or exception text
    (§25.12). It is ``None`` for a stage that did not fail.
    """

    name: str
    status: str
    error_kind: str | None = None


@dataclass(frozen=True, slots=True)
class ArtifactRef:
    """A read-only reference to a local artifact produced by a run.

    ``key`` is the artifact's relative storage key — a local, relative path,
    never an absolute host path (§25.16, determinism). The report links to it
    as a reference; it never embeds the artifact's contents.
    """

    label: str
    key: str


@dataclass(frozen=True, slots=True)
class ObservabilityLink:
    """An optional reference link to a configured observability dashboard.

    Per §25.14 this is a *link only*: it embeds no dashboard data and no
    credentials, and it carries no token or secret in the URL. If no
    observability backend is configured the report simply has none of these,
    and it remains complete (§25.14).
    """

    label: str
    url: str


@dataclass(frozen=True, slots=True)
class GovernanceView:
    """A run's governance status, projected from the Trust Envelope (§25.5).

    Every field is transcribed from the locked Trust Envelope projection and
    durable artifact (§24.8). ``decision`` is the stable, UI-safe enum
    (``APPROVED`` / ``REJECTED`` / ``BLOCKED`` / ``NEEDS_REVIEW``). The report
    presents this as a record of a human operator's decision — never as a
    legal certification (§25.5).

    ``review_context_summary`` is the operator's short governance rationale,
    already bounded to ``REVIEW_CONTEXT_SUMMARY_MAX_CHARS`` by the collector
    (§25.13). It is ``None`` when the durable artifact has no summary or could
    not be read; the report shows a safe placeholder in that case.
    """

    decision: str
    license_type: str
    approver_id: str
    decision_timestamp: str
    blocked_reason: str | None = None
    review_context_summary: str | None = None
    trust_envelope_key: str | None = None


@dataclass(frozen=True, slots=True)
class RunSummary:
    """A single run as shown in the run list (``runs.html``).

    A compact, bounded projection of the SQLite ``pipeline_run`` row plus the
    run's governance decision, used for the run list and the latest-runs
    summary on ``index.html``.
    """

    run_id: str
    status: str
    current_stage: str
    created_at: str
    updated_at: str
    governance_decision: str | None = None


@dataclass(frozen=True, slots=True)
class RerunView:
    """A bounded, safe projection of Phase 10D rerun eligibility for the report.

    All fields are stable decision codes and short operator-facing messages —
    never raw exception text, raw blocked reasons, or sensitive governance
    internals (§25.12). ``next_command`` is a plain-text suggestion only; it is
    never a clickable control and never executes anything.
    """

    eligible: bool
    code: str
    message: str
    from_stage: str | None = None
    governance_status: str | None = None
    next_command: str | None = None


@dataclass(frozen=True, slots=True)
class RunDetail:
    """A single run in full detail (``run-<run_id>.html``).

    Aggregates the bounded projections for one run: its lifecycle fields, the
    per-stage statuses, the governance view, read-only artifact references,
    optional observability links, a structured failure category when the run
    failed, and a Phase 10D rerun eligibility view. No raw content, no secrets,
    no unbounded text (§25.12).
    """

    run_id: str
    status: str
    current_stage: str
    created_at: str
    updated_at: str
    gates: tuple[str, ...] = ()
    stages: tuple[StageView, ...] = ()
    governance: GovernanceView | None = None
    artifacts: tuple[ArtifactRef, ...] = ()
    observability_links: tuple[ObservabilityLink, ...] = ()
    failure_stage: str | None = None
    failure_category: str | None = None
    rerun: RerunView | None = None


@dataclass(frozen=True, slots=True)
class OperatorReport:
    """The whole operator report — the deterministic input to rendering.

    ``generated_at`` is supplied by an injectable clock (§ deterministic-clock
    constraint): given identical state and an identical ``generated_at`` the
    rendered HTML is byte-for-byte identical. ``runs`` is newest-first for the
    list and latest-runs summary; ``details`` carries one ``RunDetail`` per
    run, in the same order.
    """

    generated_at: str
    runs: tuple[RunSummary, ...] = field(default_factory=tuple)
    details: tuple[RunDetail, ...] = field(default_factory=tuple)
