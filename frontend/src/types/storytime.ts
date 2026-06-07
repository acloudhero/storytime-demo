/**
 * StoryTime — Frontend read-model contract (Phase 13B).
 *
 * These are the TypeScript types the StoryTime frontend consumes. They are the
 * concrete, code-level expression of the read-model categories specified in
 * `docs/frontend-backend-contract.md` ("backend owns truth, frontend owns
 * understanding").
 *
 * Scope and rules (from the Phase 13A contract):
 *  - These are FRONTEND READ MODELS only. They are not the backend's internal
 *    Python/SQLite/Trust-Envelope models. A later subphase (13C) maps backend
 *    data into these shapes; the frontend never depends on backend internals.
 *  - IDs are strings. Timestamps are ISO-8601 strings, aliased as IsoTimestamp.
 *  - Statuses are explicit string unions, never free-form strings.
 *  - Evidence links and artifact links are typed objects, never loose strings.
 *  - Disabled future actions carry typed metadata explaining why they are
 *    disabled and which later phase would enable them.
 *  - Shapes are kept flat and serialization-friendly so Phase 13C can map
 *    Python/SQLite/Trust-Envelope data into them without painful nesting.
 *
 * In Phase 13B the only data conforming to these types is the static demo
 * dataset in `src/data/storytime-demo-data.ts`. No backend, no network, no live
 * data is involved.
 */

/* ────────────────────────────────────────────────────────────────────────
 * Shared primitive aliases
 * ──────────────────────────────────────────────────────────────────────── */

/** An ISO-8601 timestamp string, e.g. "2026-05-20T14:03:11Z". */
export type IsoTimestamp = string;

/** A stable, opaque identifier string (run id, stage id, project id, …). */
export type StoryTimeId = string;

/* ────────────────────────────────────────────────────────────────────────
 * Status unions
 * ──────────────────────────────────────────────────────────────────────── */

/** Lifecycle status of a whole pipeline run. */
export type PipelineRunStatus =
  | "queued"
  | "running"
  | "succeeded"
  | "failed"
  | "blocked"
  | "recovered";

/** Lifecycle status of a single stage within a run. */
export type PipelineStageStatus =
  | "not_started"
  | "running"
  | "succeeded"
  | "failed"
  | "blocked"
  | "skipped";

/**
 * Governance decision status. This is the frontend-facing projection of the
 * backend Trust Envelope decision enum; it is intentionally a small, stable
 * set and carries no legal/compliance overclaiming vocabulary.
 */
export type GovernanceDecisionStatus =
  | "allowed"
  | "review_required"
  | "blocked";

/** Result of a project validation / quality gate. */
export type ValidationGateStatus = "passed" | "warning" | "failed" | "not_run";

/* ────────────────────────────────────────────────────────────────────────
 * Portfolio content model
 * (data about the StoryTime PROJECT — portfolio-facing, run-data-light)
 * ──────────────────────────────────────────────────────────────────────── */

/**
 * A tiered reviewer path: a suggested route through the portfolio for a
 * particular kind of reviewer (5-minute, technical, deep-architecture).
 */
export interface ReviewerPath {
  id: StoryTimeId;
  /** Short audience label, e.g. "5-minute reviewer". */
  audience: string;
  /** One-line description of what this path is for. */
  summary: string;
  /** Ordered, human-readable steps for this reviewer path. */
  steps: string[];
  /** Rough time budget, e.g. "~5 min". */
  timeBudget: string;
}

/**
 * A small, mostly static description of the StoryTime project itself. This is
 * the data behind the portfolio homepage. It is portfolio-facing and
 * deliberately run-data-light.
 */
export interface StoryTimeProjectSummary {
  name: string;
  /** One-sentence description of what StoryTime is. */
  tagline: string;
  /** A short paragraph: what it is and why it exists. */
  description: string;
  /** The current phase label, e.g. "Phase 13B". */
  currentPhase: string;
  /** Plain-language current phase status. */
  currentPhaseStatus: string;
  /** What the project demonstrates (portfolio talking points). */
  demonstrates: string[];
  /** The honest list of things this project is deliberately NOT. */
  notClaims: string[];
  /** Tiered reviewer paths through the portfolio. */
  reviewerPaths: ReviewerPath[];
}

/* ────────────────────────────────────────────────────────────────────────
 * Evidence / readiness model
 * ──────────────────────────────────────────────────────────────────────── */

/**
 * A typed link to a piece of evidence (a document, a report, a dashboard
 * reference). Evidence links are typed objects, never loose strings.
 */
export interface EvidenceLink {
  id: StoryTimeId;
  label: string;
  /**
   * Where the evidence lives. `kind` describes the reference so the UI can
   * present it honestly without assuming it is a live, clickable URL.
   */
  kind: "doc" | "report" | "dashboard" | "trace" | "artifact" | "external";
  /**
   * A reference string — a repository-relative path, an artifact reference, or
   * (rarely) an external URL. In the Phase 13B static shell these are shown as
   * references; they are not fetched.
   */
  reference: string;
  /** Optional short note about what the evidence shows. */
  note?: string;
}

/**
 * A reference to an observability surface for a run: a trace id/link, a
 * dashboard reference, and the correlation key. Links and references only —
 * the contract never embeds telemetry payloads or secrets.
 */
export interface ObservabilityEvidence {
  /** The correlation key shared across telemetry — the pipeline run id. */
  correlationKey: StoryTimeId;
  /** The trace identifier, if a trace was recorded. */
  traceId?: StoryTimeId;
  /** Typed links into traces and dashboards. */
  links: EvidenceLink[];
}

/* ────────────────────────────────────────────────────────────────────────
 * Future action model
 * (operator actions are READ-ONLY-first; nothing here is wired in Phase 13B)
 * ──────────────────────────────────────────────────────────────────────── */

/**
 * An operator action that is allowed to be VISIBLE in the current phase. In
 * Phase 13B even "allowed" actions are non-mutating affordances only (for
 * example, surfacing a CLI command to copy). No action performs a mutation in
 * Phase 13B.
 */
export interface AllowedOperatorAction {
  id: StoryTimeId;
  label: string;
  /**
   * The kind of affordance. `copy_command` surfaces a CLI command;
   * `open_reference` opens/navigates to an artifact or report reference.
   * Neither mutates anything.
   */
  kind: "copy_command" | "open_reference";
  /** Plain description of what the action does. */
  description: string;
  /**
   * The payload the affordance exposes — a CLI command string for
   * `copy_command`, or a reference string for `open_reference`.
   */
  payload: string;
}

/**
 * An operator action that is intentionally DISABLED in the current phase, with
 * typed metadata explaining why and which later phase would enable it. Disabled
 * future actions are shown in the UI as visibly-present, visibly-disabled
 * affordances so the operator can see the intended workflow shape.
 */
export interface DisabledFutureAction {
  id: StoryTimeId;
  label: string;
  /** Why this action is disabled right now. */
  disabledReason: string;
  /** The Phase 13 subphase that would enable this action, e.g. "Phase 13E". */
  enabledByPhase: string;
  /**
   * Whether this action, once enabled, would be a true backend mutation. The
   * UI uses this to label genuinely state-changing actions distinctly.
   */
  isMutation: boolean;
}

/* ────────────────────────────────────────────────────────────────────────
 * Operator read model
 * (data about pipeline RUNS — the backbone of the operator GUI)
 * ──────────────────────────────────────────────────────────────────────── */

/**
 * The Trust Envelope governance decision for a run, projected for display.
 * Carries the stable decision status, a bounded context summary, the source
 * category, and the standing non-legal-advice disclaimer. No raw
 * `blocked_reason` free text; no legal/compliance overclaiming.
 */
export interface GovernanceDecision {
  status: GovernanceDecisionStatus;
  /** Bounded, display-safe summary of the review context. */
  contextSummary: string;
  /** The source authorization category, e.g. "CC0", "US_PUBLIC_DOMAIN". */
  sourceCategory: string;
  /** Standing disclaimer: a record of a human decision, not legal advice. */
  disclaimer: string;
}

/** A typed reference to an episode artifact a run produced. */
export interface EpisodeArtifact {
  id: StoryTimeId;
  label: string;
  /** The kind of artifact this reference points at. */
  kind: "audio" | "feed" | "episode_metadata" | "report";
  /** A reference string (repository-relative path or artifact reference). */
  reference: string;
  /** Optional duration in seconds, for audio artifacts. */
  durationSeconds?: number;
  /** Optional size in bytes. */
  sizeBytes?: number;
}

/** A single stage within a pipeline run. */
export interface PipelineStage {
  id: StoryTimeId;
  /** Human-readable stage name, e.g. "Ingest", "Synthesize". */
  name: string;
  /** Zero-based position of the stage in the run's ordered sequence. */
  order: number;
  status: PipelineStageStatus;
  /** Whether this stage is an operator approval gate rather than a work stage. */
  isApprovalGate: boolean;
  startedAt?: IsoTimestamp;
  endedAt?: IsoTimestamp;
  /** Optional measured duration in seconds, when the backend recorded it. */
  durationSeconds?: number;
  /** Short, display-safe note about this stage's outcome. */
  note?: string;
}

/** A run as it appears in a list of runs (the runs-list read model). */
export interface PipelineRunSummary {
  id: StoryTimeId;
  /** Human-readable label or source title for the run. */
  label: string;
  status: PipelineRunStatus;
  governanceStatus: GovernanceDecisionStatus;
  createdAt: IsoTimestamp;
  updatedAt: IsoTimestamp;
  /** True if this run needs operator attention. */
  needsAttention: boolean;
}

/**
 * Everything the run-detail view needs about a single run. This is the richest
 * read model and the backbone of the operator GUI.
 */
export interface PipelineRunDetail {
  id: StoryTimeId;
  label: string;
  status: PipelineRunStatus;
  createdAt: IsoTimestamp;
  updatedAt: IsoTimestamp;
  /** The ordered stages of the run (also the stage-timeline projection). */
  stages: PipelineStage[];
  governance: GovernanceDecision;
  /**
   * Structured failure summary if the run failed or was blocked. Carries a
   * stable `errorKind` code and operator-safe guidance — never a raw error
   * message or raw `blocked_reason`.
   */
  failure?: {
    errorKind: string;
    operatorGuidance: string;
  };
  /** What the run produced, if anything. */
  artifacts: EpisodeArtifact[];
  /** Observability references for this run. */
  observability: ObservabilityEvidence;
  /** Plain statement of what the run's current state means for the operator. */
  stateExplanation: string;
  /** Visible, non-mutating affordances available now. */
  allowedActions: AllowedOperatorAction[];
  /** Visible-but-disabled affordances reserved for later Phase 13 subphases. */
  disabledActions: DisabledFutureAction[];
}

/**
 * An entry in the failure / review queue: a run that needs operator attention,
 * with the structured reason and a pointer to what to inspect next. This is the
 * read-model shape of the existing `storytime queue` projection.
 */
export interface FailureQueueItem {
  runId: StoryTimeId;
  runLabel: string;
  /** Structured reason this run needs attention. */
  reason: "failed" | "blocked" | "needs_review" | "awaiting_approval";
  /** Display-safe summary of the reason. */
  summary: string;
  /** What the operator should inspect next (a run-detail view, command, …). */
  inspectNext: string;
}

/* ────────────────────────────────────────────────────────────────────────
 * Static export envelope
 * (the top-level shape of the deterministic backend export — Phase 13C)
 * ──────────────────────────────────────────────────────────────────────── */

/**
 * The top-level shape of the deterministic static export produced by the
 * backend (`storytime export-demo-ui`, module `storytime.operator_export`) and
 * committed at `src/data/storytime-demo-export.json`.
 *
 * Phase 13C realizes the "backend owns truth, frontend owns understanding"
 * contract: this envelope mirrors the backend export shape. The frontend reads
 * it through `src/data/adapter.ts`, which derives UI-ready view data (such as
 * the runs-list summaries) without the React components touching raw export
 * details. See `docs/frontend-static-export-contract.md`.
 *
 * This is a static, read-only data boundary: there is no `fetch`, no network,
 * no live backend, and no mutation involved in consuming it.
 */
export interface StaticDemoExport {
  /** Export contract schema version, e.g. "1.0". */
  schemaVersion: string;
  /** Stable identifier of the producing backend module. */
  generatedBy: string;
  /** The kind of export, e.g. "phase13c_static_demo". */
  exportKind: string;
  /** The portfolio project summary (includes the reviewer paths). */
  project: StoryTimeProjectSummary;
  /** Full run-detail records. The runs-list summary is derived in the adapter. */
  runs: PipelineRunDetail[];
  /** The failure / review queue projection. */
  failureQueue: FailureQueueItem[];
}
