/**
 * actionPreviewAdapter — Phase 13E static view-model for the Demo-mode
 * Action Preview / Operator Intent Boundary system.
 *
 * Phase 13E turns the existing visibly-disabled future-action affordances
 * into explainable, **non-executing** action previews. The right framing
 * is: *demo mode may preview serious operator intent — demo mode must
 * not create consequential changes.* The frontend can explain what an
 * operator action would target, why it is blocked in Demo mode, what
 * preconditions would be required, what evidence to inspect first, what
 * a future Local-mode request shape might look like, what audit
 * expectations would apply, and why execution is deferred to a future
 * Local or Cloud/Distributed operating mode — all without ever calling
 * out, fetching, executing a CLI, opening a local bridge, generating an
 * audit record, or pretending anything happened.
 *
 * All long-form preview content lives in this adapter, not in
 * `ActionPreviewPanel.tsx`. The panel is a presentation shell that maps
 * over the adapter data. This separation is an explicit Phase 13E prompt
 * requirement so that the preview definitions stay reviewable as data
 * rather than buried in JSX.
 *
 * The adapter is intentionally static. It imports nothing at runtime; it
 * has no `fetch`, `axios`, `XMLHttpRequest`, `WebSocket`, `localStorage`,
 * `sessionStorage`, router, Context, or global state. Run-id and stage-id
 * references reuse the stable ids already present in the locked Phase 13C
 * static export (`frontend/src/data/storytime-demo-export.json`) and the
 * Phase 13D.2 walkthrough adapter — specifically `GOLDEN_RUN_ID`
 * (`run-2026-0518-golden`) and `REVIEW_RUN_ID` (`run-2026-0520-review`) —
 * so a small Python data-integrity test
 * (`tests/test_action_preview_data_integrity.py`) can assert that every
 * id referenced here exists in the committed export.
 *
 * The future-request shape rendered inside every preview is an
 * **illustrative pseudo-DTO**, not executable code. It is labelled
 * "Future request shape — illustrative only, not executable in Demo
 * mode." No shell commands, no CLI invocations, no API calls.
 */

import { GOLDEN_RUN_ID, REVIEW_RUN_ID } from "./demoWalkthroughAdapter";

/* ───────────────────────── stable target ids ────────────────────────── */

/**
 * Stable target ids used by Phase 13E action previews. These are
 * references to objects that live in the locked Phase 13C static export
 * — every id here must exist in `frontend/src/data/storytime-demo-export.json`
 * (the data-integrity test enforces this). The previews never execute
 * against these ids; they only describe what a future Local-mode action
 * would target.
 */
export const PREVIEW_TARGETS = {
  /** The blocked governance gate stage on the review-required run. */
  REVIEW_GOVERNANCE_GATE_STAGE_ID: `${REVIEW_RUN_ID}:governance-gate`,
  /** The visibly-disabled "open review workflow" action on the review run. */
  REVIEW_OPEN_REVIEW_ACTION_ID: `${REVIEW_RUN_ID}:open-review`,
  /** The visibly-disabled "retry after review" action on the review run. */
  REVIEW_RETRY_ACTION_ID: `${REVIEW_RUN_ID}:retry`,
  /** The committed static export — the artifact a "refresh export" preview would describe. */
  STATIC_EXPORT_PATH: "frontend/src/data/storytime-demo-export.json",
} as const;

/* ───────────────────────── operating mode model ─────────────────────── */

/**
 * The eventual operating-mode model. Phase 13E introduces or clarifies
 * this taxonomy: Demo mode is curated, safe, non-consequential, and
 * portfolio-ready (the only mode implemented). Local mode would be future
 * real local operator workflows. Cloud / Distributed mode would be future
 * hosted/distributed execution. Phase 13E does NOT implement Local mode
 * or Cloud / Distributed mode.
 *
 * Crucial naming note: Demo / Local / Cloud-Distributed are
 * **operating-mode** labels. The existing Demo / Active / Candidate
 * framing (Phase 13D.1's Evidence / Validation view) is a separate axis:
 * those are **data-snapshot** labels. The two axes do not collapse.
 */
export type OperatingModeId = "demo" | "local" | "cloud-distributed";

export interface OperatingMode {
  readonly id: OperatingModeId;
  readonly label: string;
  readonly summary: string;
  readonly status:
    | "Implemented (Phase 13E)"
    | "Future / not implemented"
    | "Future / not implemented";
  readonly includes: readonly string[];
}

export const OPERATING_MODES: readonly OperatingMode[] = [
  {
    id: "demo",
    label: "Demo mode",
    summary:
      "Curated, safe, non-consequential, portfolio-ready. The only " +
      "operating mode implemented today. Renders previews of operator " +
      "intent — never executes them.",
    status: "Implemented (Phase 13E)",
    includes: [
      "Guided walkthrough (Phase 13D.2).",
      "Static demo data, committed via the Phase 13C static export.",
      "Action previews (this Phase 13E system).",
      "Command/request previews — labelled illustrative only.",
      "Precondition checklists.",
      '"What would happen" explanations.',
      "Evidence links into existing read-only views.",
      "No local writes.",
      "No backend execution.",
      "No actual retry, rerun, approval, or review action.",
    ],
  },
  {
    id: "local",
    label: "Local mode",
    summary:
      "Future real local operator workflows. Not implemented in Phase " +
      "13E. Would let an operator load a refreshed local export, issue " +
      "controlled local actions via the CLI, and write local audit " +
      "records — all behind an explicit, gated safety boundary.",
    status: "Future / not implemented",
    includes: [
      "Loaded local exports.",
      "Local pipeline state.",
      "CLI-mediated actions.",
      "Local action requests with confirmation.",
      "Controlled local mutations.",
      "Local audit records.",
      "Refreshed exports after action completion.",
    ],
  },
  {
    id: "cloud-distributed",
    label: "Cloud / Distributed mode",
    summary:
      "Future distributed/cloud execution architecture. Not implemented " +
      "in Phase 13E. Would be a separate, much later subphase entirely; " +
      "the current local-first design does not depend on it.",
    status: "Future / not implemented",
    includes: [
      "Hosted APIs.",
      "Durable workers.",
      "Cloud storage.",
      "Auth.",
      "Distributed orchestration.",
      "Cloud observability.",
      "Production-like governance and action execution.",
    ],
  },
];

/**
 * Explicit explanation of the relationship between the two label axes
 * (operating mode vs data snapshot), rendered into the panel header so
 * a reviewer never has to guess.
 */
export const MODE_VS_SNAPSHOT_NOTE: string =
  "Demo / Active / Candidate are data-snapshot labels (introduced in " +
  "Phase 13D.1 — the data behind the GUI). Demo / Local / " +
  "Cloud-Distributed are operating-mode labels (how the GUI is " +
  "executing — only Demo mode is implemented). The two axes do not " +
  "collapse: a Demo data snapshot in Demo mode is what you see today; " +
  "an Active data snapshot in a future Local mode would be a different " +
  "combination, gated behind a separate phase.";

/* ───────────────────────── safety / honesty labels ──────────────────── */

/**
 * The required safety / honesty labels rendered in the panel header for
 * every preview. These are the literal phrases the Phase 13E prompt
 * mandates — they make the demo / preview-only boundary unambiguous.
 */
export const SAFETY_LABELS: readonly string[] = [
  "Demo mode",
  "Preview only",
  "No state changed",
  "Action plan, not action result",
  "Execution requires future Local mode",
  "Cloud/Distributed execution is not implemented",
  "No audit record generated because nothing executed",
  "No local bridge is running",
  "No backend command was called",
];

/**
 * The enterprise-governance constraint sentence rendered at the top of
 * every preview. Verbatim from the Phase 13E prompt's suggested
 * enterprise wording.
 */
export const SYSTEM_CONSTRAINT_NOTICE: string =
  "System constraint: Action execution requires future Local or " +
  "Cloud/Distributed mode. Current operating mode is Static Demo. " +
  "This is an action plan preview only; no state changed and no " +
  "audit record was generated.";

/* ───────────────────────── action preview model ─────────────────────── */

/** Stable ids for the first set of Phase 13E action previews. */
export type ActionPreviewId =
  | "preview-retry-failed-stage"
  | "preview-inspect-trust-envelope"
  | "preview-record-review-decision"
  | "preview-regenerate-operator-report"
  | "preview-refresh-export";

/**
 * The view context in which an action preview is most relevant. This is
 * descriptive metadata, not a routing hint — the panel is rendered
 * inline inside the host view, never via a router.
 */
export type ActionPreviewContext =
  | "Failure / Recovery"
  | "Governance / Safety"
  | "Evidence / Validation";

/**
 * The category of an action preview. Categories are informational
 * groupings used by the panel to label what kind of operator workflow
 * the preview belongs to.
 */
export type ActionPreviewCategory =
  | "Failure recovery"
  | "Governance review"
  | "Evidence inspection"
  | "Report regeneration"
  | "Export refresh";

/** Risk-level summary for an action preview. */
export type ActionPreviewRiskLevel = "Low" | "Medium" | "High";

/**
 * The current operating mode at the time the preview is rendered. Phase
 * 13E hardcodes `"demo"` for every preview — the GUI only operates in
 * Demo mode. Kept as a field for future clarity so a future Local-mode
 * implementation could reuse the same data shape.
 */
export type CurrentMode = "demo";

/**
 * The execution status of a preview. Phase 13E hardcodes
 * `"preview-only"` for every preview — nothing executes.
 */
export type ExecutionStatus = "preview-only";

/**
 * References to the target object of an action preview. Every reference
 * is by stable id (never by a transient runtime object). The
 * `targetContextLabel` is the short, plain-English name the panel
 * renders next to the ids.
 */
export interface ActionPreviewTarget {
  /** The pipeline run id the action would target, if applicable. */
  readonly runId?: string;
  /** The stage id the action would target, if applicable. */
  readonly stageId?: string;
  /** The governance decision id the action would target, if applicable. */
  readonly governanceDecisionId?: string;
  /** The failure queue item runId the action would target, if applicable. */
  readonly failureQueueRunId?: string;
  /** The evidence artifact path the action would target, if applicable. */
  readonly evidenceArtifactPath?: string;
  /** The visibly-disabled action this preview corresponds to, if any. */
  readonly relatedDisabledActionId?: string;
  /** Short plain-English label for the target ("Stage X on Run Y"). */
  readonly targetContextLabel: string;
}

/**
 * One concrete action preview. This is the unit the panel renders. Every
 * field is required (except the target references inside
 * `target`, which are optional individually but at least one must be
 * present). No methods, no callbacks — the panel never invokes anything
 * through a preview object.
 */
export interface ActionPreview {
  readonly id: ActionPreviewId;
  readonly label: string;
  readonly category: ActionPreviewCategory;
  readonly currentMode: CurrentMode;
  readonly executionStatus: ExecutionStatus;
  readonly target: ActionPreviewTarget;
  /** What the operator would be trying to accomplish. */
  readonly operatorIntent: string;
  /** Why this action is blocked in Demo mode (Phase 13E framing). */
  readonly whyBlockedInDemo: string;
  /** Checklist of preconditions that future Local-mode execution would require. */
  readonly preconditionChecklist: readonly string[];
  /** Evidence the operator should inspect first, framed read-only. */
  readonly evidenceToInspect: readonly string[];
  /** Risk-level summary. */
  readonly riskLevel: ActionPreviewRiskLevel;
  /** A short explanation of the risk-level assessment. */
  readonly riskExplanation: string;
  /**
   * The illustrative future Local-mode request shape — a structured
   * pseudo-DTO. NEVER executable code. The panel renders this as a
   * `<pre>` block under the label "Future request shape — illustrative
   * only, not executable in Demo mode."
   */
  readonly futureLocalRequestShape: Record<string, unknown>;
  /** What Cloud/Distributed considerations would apply (still future, not implemented). */
  readonly cloudDistributedConsiderations: string;
  /** What audit expectations would apply once a real action eventually executes. */
  readonly auditExpectations: string;
  /** What the failure behaviour of a future Local-mode execution would be. */
  readonly failureBehaviorExpectation: string;
  /** What remains explicitly disabled in Demo mode for this action. */
  readonly whatRemainsDisabled: string;
  /** The host view the preview is rendered inside. */
  readonly relatedView: ActionPreviewContext;
  /** Optional related run id (for cross-reference). */
  readonly relatedRunId?: string;
  /** A short "what this preview proves" sentence for the host view header. */
  readonly headlineSummary: string;
}

/* ───────────────────────── the previews themselves ──────────────────── */

const previewRetryFailedStage: ActionPreview = {
  id: "preview-retry-failed-stage",
  label: "Retry failed stage (preview)",
  category: "Failure recovery",
  currentMode: "demo",
  executionStatus: "preview-only",
  target: {
    runId: REVIEW_RUN_ID,
    stageId: PREVIEW_TARGETS.REVIEW_GOVERNANCE_GATE_STAGE_ID,
    failureQueueRunId: REVIEW_RUN_ID,
    relatedDisabledActionId: PREVIEW_TARGETS.REVIEW_RETRY_ACTION_ID,
    targetContextLabel:
      "Governance Gate stage on the review-required run (failure queue entry)",
  },
  operatorIntent:
    "Resume the pipeline from the blocked Governance Gate stage on the " +
    "review-required run once the governance review has been recorded " +
    "out-of-band. Goal: get a needs-review run back into motion without " +
    "rebuilding earlier stages.",
  whyBlockedInDemo:
    "Phase 13E is Demo mode. The GUI cannot start a real retry, cannot " +
    "call the `storytime` CLI, cannot mutate the pipeline DB, and cannot " +
    "open a local bridge. The visibly-disabled retry affordance on the " +
    "run remains visibly disabled and unhandled — this preview only " +
    "describes what a future Local-mode retry would look like.",
  preconditionChecklist: [
    "Governance review for the run has been recorded out-of-band (CLI).",
    "The Trust Envelope source-authorization status is no longer 'review-required'.",
    "The blocked stage is in a state the underlying governed retry operation accepts.",
    "Operator has explicit local-mode execution authority (future).",
    "A fresh local export will be regenerated after a real retry completes.",
  ],
  evidenceToInspect: [
    "Pipeline Run Detail → Governance Gate stage status and timing.",
    "Governance / Safety view → the review decision for this run, once recorded.",
    "Failure / Recovery view → the failure queue entry and its reason.",
    "`docs/frontend-static-export-contract.md` → the static-data boundary.",
  ],
  riskLevel: "Medium",
  riskExplanation:
    "A real retry would re-enter the governed stage pipeline. The Trust " +
    "Envelope and fail-closed gate still apply. The action does not " +
    "delete or alter prior artifacts — but it does change pipeline state.",
  futureLocalRequestShape: {
    mode: "local",
    action: "retry_failed_stage",
    runId: REVIEW_RUN_ID,
    stageId: PREVIEW_TARGETS.REVIEW_GOVERNANCE_GATE_STAGE_ID,
    dryRun: false,
    requiresConfirmation: true,
    auditTagsRequired: ["operatorId", "reviewDecisionId"],
  },
  cloudDistributedConsiderations:
    "In a future Cloud/Distributed mode this would be a hosted, audited " +
    "API call routed through the same governance gate. Phase 13E does " +
    "not implement that path.",
  auditExpectations:
    "Once Local mode (and later, Cloud/Distributed mode) exists, a real " +
    "retry would emit an audit record tying the operator id, the " +
    "associated review decision id, the run id, and the stage id, with a " +
    "before/after status snapshot. Phase 13E does not generate any audit " +
    "record because nothing executed.",
  failureBehaviorExpectation:
    "If a future Local-mode retry fails, the governed pipeline reports " +
    "the failure through the same Failure / Recovery surface the GUI " +
    "already shows. No silent retries; no automatic re-runs.",
  whatRemainsDisabled:
    "The 'Retry after review' button on the run detail page is and " +
    "remains a visibly-disabled `<button disabled={true}>` with no " +
    "`onClick`. This preview adds no execution affordance to it.",
  relatedView: "Failure / Recovery",
  relatedRunId: REVIEW_RUN_ID,
  headlineSummary:
    "Preview of the safest future local action candidate: resuming a " +
    "blocked stage on a needs-review run, once review is recorded.",
};

const previewInspectTrustEnvelope: ActionPreview = {
  id: "preview-inspect-trust-envelope",
  label: "Inspect Trust Envelope (preview)",
  category: "Evidence inspection",
  currentMode: "demo",
  executionStatus: "preview-only",
  target: {
    runId: REVIEW_RUN_ID,
    targetContextLabel:
      "Trust Envelope governance context for the review-required run",
  },
  operatorIntent:
    "Open a non-mutating inspection of the Trust Envelope for the " +
    "review-required run: source category, source authorization status, " +
    "policy outcomes, and the gate decision summary. Goal: understand " +
    "why the run was held without making any change.",
  whyBlockedInDemo:
    "Inspection is non-mutating, but in Phase 13E the inspection workflow " +
    "is presented as a preview because the eventual Local-mode flow may " +
    "wire it to a richer audited view (e.g. recording who inspected what " +
    "and when). Phase 13E only shows what the inspection would surface " +
    "and pointers into the existing read-only Governance / Safety view.",
  preconditionChecklist: [
    "Run is identifiable by its stable id.",
    "Governance / Safety view is reachable from the current view.",
    "Operator has read access to the static export (always true in Demo mode).",
  ],
  evidenceToInspect: [
    "Governance / Safety view → contextSummary, sourceCategory, status, disclaimer.",
    "Pipeline Run Detail → stage notes and governance gate status.",
    "`docs/architecture-baseline.md` §24 (governance) for the policy model.",
  ],
  riskLevel: "Low",
  riskExplanation:
    "Inspection is non-mutating by design. The risk in a future Local " +
    "mode is principally about audit-trail completeness (recording who " +
    "inspected what), not about altering pipeline state.",
  futureLocalRequestShape: {
    mode: "local",
    action: "inspect_trust_envelope",
    runId: REVIEW_RUN_ID,
    dryRun: false,
    requiresConfirmation: false,
    auditTagsRequired: ["operatorId"],
  },
  cloudDistributedConsiderations:
    "Cloud/Distributed mode would expose the same inspection as an " +
    "audited, hosted, governed read endpoint with operator identity " +
    "tracking. Phase 13E does not implement any hosted endpoint.",
  auditExpectations:
    "In Local mode (and later Cloud/Distributed mode), inspection would " +
    "be logged with operator id and timestamp. Phase 13E does not " +
    "generate any audit record because nothing executed.",
  failureBehaviorExpectation:
    "A future inspection has no failure path beyond 'evidence not found' " +
    "— the existing Governance / Safety view already handles that case " +
    "by surfacing the policy status.",
  whatRemainsDisabled:
    "No execution affordance exists. The disabled 'Open review workflow' " +
    "button on this run is still a `<button disabled={true}>` and is " +
    "covered by a separate preview (record-review-decision).",
  relatedView: "Governance / Safety",
  relatedRunId: REVIEW_RUN_ID,
  headlineSummary:
    "Preview of the evidence-first operator workflow: inspect the Trust " +
    "Envelope of a held run before any decision is recorded.",
};

const previewRecordReviewDecision: ActionPreview = {
  id: "preview-record-review-decision",
  label: "Record review decision (preview)",
  category: "Governance review",
  currentMode: "demo",
  executionStatus: "preview-only",
  target: {
    runId: REVIEW_RUN_ID,
    governanceDecisionId: `${REVIEW_RUN_ID}:governance-decision`,
    relatedDisabledActionId: PREVIEW_TARGETS.REVIEW_OPEN_REVIEW_ACTION_ID,
    targetContextLabel:
      "Governance review decision for the review-required run",
  },
  operatorIntent:
    "Record an approve/reject governance decision against the " +
    "review-required run with a written rationale. Goal: convert a " +
    "'needs review' run into a state where the pipeline can be retried " +
    "or rejected, with an auditable trail.",
  whyBlockedInDemo:
    "Recording a review decision is a true backend mutation and would " +
    "create an audit record. Phase 13E is Demo mode and creates no " +
    "audit records, makes no backend call, and writes nothing. The " +
    "visibly-disabled 'Open review workflow' button remains visibly " +
    "disabled. This preview only describes what the review-decision " +
    "request would carry.",
  preconditionChecklist: [
    "Trust Envelope has been inspected (see preview-inspect-trust-envelope).",
    "Operator has explicit reviewer authority (future).",
    "Rationale text has been drafted out-of-band.",
    "Decision is one of approve / reject — no third option.",
    "A unique decision id will be assigned by the governed backend operation.",
  ],
  evidenceToInspect: [
    "Governance / Safety view → contextSummary and disclaimer for the run.",
    "Pipeline Run Detail → run-level status and stage timeline.",
    "`docs/architecture-baseline.md` §24 (governance), §25 (operator experience).",
  ],
  riskLevel: "High",
  riskExplanation:
    "Recording a governance decision is consequential: it changes what " +
    "the Trust Envelope says about the run, and it gates downstream " +
    "actions (retry, publish). It is also the most safety-sensitive " +
    "future mutation, which is precisely why Phase 13E only previews it.",
  futureLocalRequestShape: {
    mode: "local",
    action: "record_review_decision",
    runId: REVIEW_RUN_ID,
    decision: "approve | reject",
    rationale: "<operator rationale, required, free text>",
    dryRun: false,
    requiresConfirmation: true,
    auditTagsRequired: ["operatorId", "reviewerRole"],
  },
  cloudDistributedConsiderations:
    "Cloud/Distributed mode would require additional identity and " +
    "non-repudiation guarantees (signed audit records, hosted policy " +
    "enforcement). Phase 13E does not implement any of that.",
  auditExpectations:
    "A real decision would emit an audit record tying operator id, " +
    "reviewer role, decision (approve/reject), rationale, run id, " +
    "governance decision id, and timestamp. The audit record itself " +
    "would be append-only and immutable. Phase 13E does not generate " +
    "any audit record because nothing executed.",
  failureBehaviorExpectation:
    "If recording fails (e.g. duplicate decision id, missing rationale), " +
    "the governed backend operation rejects the request and the GUI " +
    "surfaces the rejection through the existing Failure / Recovery view.",
  whatRemainsDisabled:
    "The 'Open review workflow' button on this run is and remains a " +
    "visibly-disabled `<button disabled={true}>` with no `onClick`. " +
    "This preview adds no execution affordance to it.",
  relatedView: "Governance / Safety",
  relatedRunId: REVIEW_RUN_ID,
  headlineSummary:
    "Preview of the highest-risk future Local-mode action: recording a " +
    "governance review decision. Surfaced read-only in Demo mode.",
};

const previewRegenerateOperatorReport: ActionPreview = {
  id: "preview-regenerate-operator-report",
  label: "Regenerate operator report (preview)",
  category: "Report regeneration",
  currentMode: "demo",
  executionStatus: "preview-only",
  target: {
    runId: GOLDEN_RUN_ID,
    evidenceArtifactPath: "operator-report/run-2026-0518-golden.html",
    targetContextLabel:
      "Operator report artifact for the golden-path run (static export-derived)",
  },
  operatorIntent:
    "Regenerate the operator-facing report artifact for a completed run " +
    "after a content or template change. Goal: refresh the report " +
    "deterministically from the committed pipeline state, without " +
    "re-running the pipeline.",
  whyBlockedInDemo:
    "Report regeneration is a content-producing CLI action that writes " +
    "files. Phase 13E is Demo mode and writes nothing. The existing " +
    "static export already carries the artifact metadata; the GUI does " +
    "not regenerate the artifact in Demo mode.",
  preconditionChecklist: [
    "Run is in a state where regeneration is supported (succeeded or partially complete).",
    "The report template is stable and has been reviewed.",
    "Operator has explicit local-mode execution authority (future).",
    "The destination path is writable (future).",
    "After regeneration, a fresh static export will be produced.",
  ],
  evidenceToInspect: [
    "Pipeline Run Detail → published artifacts list for this run.",
    "Evidence / Validation view → STATIC PORTFOLIO DATA disclaimer and references.",
    "`docs/frontend-static-export-contract.md` → the export contract.",
  ],
  riskLevel: "Low",
  riskExplanation:
    "Report regeneration is content-only and deterministic from " +
    "committed pipeline state. It does not alter the pipeline run.",
  futureLocalRequestShape: {
    mode: "local",
    action: "regenerate_operator_report",
    runId: GOLDEN_RUN_ID,
    outputPath: "operator-report/<runId>.html",
    dryRun: false,
    requiresConfirmation: false,
    auditTagsRequired: ["operatorId"],
  },
  cloudDistributedConsiderations:
    "Cloud/Distributed mode would route this through a hosted report " +
    "service with the same input/output contract. Phase 13E does not " +
    "implement that.",
  auditExpectations:
    "Once Local mode exists, a regeneration would record the operator " +
    "id, run id, output path, and timestamp. Phase 13E does not generate " +
    "any audit record because nothing executed.",
  failureBehaviorExpectation:
    "If the underlying governed regeneration operation fails (template " +
    "error, missing input), the GUI would surface the failure through " +
    "the same Failure / Recovery view.",
  whatRemainsDisabled:
    "No regeneration button exists on the run detail page in Phase 13E. " +
    "This preview describes the intended workflow shape without adding " +
    "any clickable execution affordance.",
  relatedView: "Evidence / Validation",
  relatedRunId: GOLDEN_RUN_ID,
  headlineSummary:
    "Preview of report-generation intent: regenerate the operator " +
    "report deterministically from committed pipeline state.",
};

const previewRefreshExport: ActionPreview = {
  id: "preview-refresh-export",
  label: "Refresh static export (preview)",
  category: "Export refresh",
  currentMode: "demo",
  executionStatus: "preview-only",
  target: {
    evidenceArtifactPath: PREVIEW_TARGETS.STATIC_EXPORT_PATH,
    targetContextLabel:
      "The committed static export the GUI reads at build time",
  },
  operatorIntent:
    "Regenerate the committed static export from current pipeline state " +
    "after a real action (retry, report regeneration, review decision) " +
    "completes, so the GUI can reflect new state. Goal: keep the static " +
    "GUI consistent with the local pipeline.",
  whyBlockedInDemo:
    "Phase 13E is Demo mode. The committed export is byte-identical to " +
    "the locked Phase 13C lineage; nothing on the GUI side regenerates " +
    "it. A real refresh would be CLI-mediated (`storytime export-demo-ui`) " +
    "and rewrite a committed file — a write the GUI does not perform.",
  preconditionChecklist: [
    "Pipeline state has actually changed since the last export (otherwise refresh is a no-op).",
    "Operator has explicit local-mode execution authority (future).",
    "Static export schema version is unchanged or the GUI types have been updated together with it.",
    "After refresh, the GUI must be rebuilt — there is no runtime export reload (deferred).",
  ],
  evidenceToInspect: [
    "Evidence / Validation view → STATIC PORTFOLIO DATA disclaimer and Data Source framing.",
    "`docs/frontend-static-export-contract.md` → schema version and contract.",
    "The export header (`schemaVersion`, `generatedBy`) shown in the chip.",
  ],
  riskLevel: "Low",
  riskExplanation:
    "Export refresh is the same `storytime export-demo-ui` CLI call the " +
    "project already supports; it is deterministic and content-only. The " +
    "principal risk is committing a refreshed export that drifts from " +
    "the frontend's expected schema — a contract concern, not a runtime " +
    "concern.",
  futureLocalRequestShape: {
    mode: "local",
    action: "refresh_static_export",
    cliCommand: "storytime export-demo-ui",
    outputPath: PREVIEW_TARGETS.STATIC_EXPORT_PATH,
    dryRun: false,
    requiresConfirmation: false,
    auditTagsRequired: ["operatorId"],
  },
  cloudDistributedConsiderations:
    "Cloud/Distributed mode would not need a committed static export at " +
    "all — it would read from a hosted store. Phase 13E does not " +
    "implement that path.",
  auditExpectations:
    "Once Local mode exists, refreshing the export would record the " +
    "operator id, the schema version, and the source pipeline-state " +
    "fingerprint. Phase 13E does not generate any audit record because " +
    "nothing executed.",
  failureBehaviorExpectation:
    "If `storytime export-demo-ui` fails, the existing CLI doctor and " +
    "operator runbook already surface the failure; the GUI is decoupled " +
    "and continues to render the previous committed export.",
  whatRemainsDisabled:
    "There is no GUI control that regenerates the export. The Settings " +
    "/ Config placeholder still describes the deferred Demo / Active / " +
    "Candidate snapshot selector — a separate, also-deferred concern.",
  relatedView: "Evidence / Validation",
  headlineSummary:
    "Preview of the export-refresh contract: real Local mode would " +
    "require regenerating the committed export after an action completes.",
};

/**
 * The complete, ordered list of action previews. The list is the
 * canonical source for the panel and for the data-integrity test.
 */
export const ACTION_PREVIEWS: readonly ActionPreview[] = [
  previewRetryFailedStage,
  previewInspectTrustEnvelope,
  previewRecordReviewDecision,
  previewRegenerateOperatorReport,
  previewRefreshExport,
];

/**
 * Quick lookup helper used by the panel. Returns `undefined` if no
 * preview with the given id exists — callers must handle the
 * possibility (the panel does, since the empty/null state is also the
 * default closed state).
 */
export function findActionPreview(
  id: ActionPreviewId | null,
): ActionPreview | undefined {
  if (id === null) return undefined;
  return ACTION_PREVIEWS.find((p) => p.id === id);
}

/**
 * Convenience: which previews to surface in a given host view. The
 * panel is rendered inline in each host view with this filter applied
 * (in addition to the host view's own `availablePreviews` allow-list,
 * which is the authoritative scoping mechanism).
 */
export function previewsForView(
  view: ActionPreviewContext,
): readonly ActionPreview[] {
  return ACTION_PREVIEWS.filter((p) => p.relatedView === view);
}

/* ───────────────────────── header copy for the panel ────────────────── */

export const ACTION_PREVIEW_PANEL_HEADER = {
  eyebrow: "Demo mode · Action plan preview",
  title: "Operator intent preview",
  lede:
    "Demo mode may preview serious operator intent. Demo mode must not " +
    "create consequential changes. Each preview describes what an action " +
    "would target, why it is blocked in Demo mode, what preconditions " +
    "would apply, what evidence to inspect first, what a future " +
    "Local-mode request shape might look like, and what audit " +
    "expectations would follow — without ever executing anything.",
} as const;

/* ───────────────────────── sanity exports for tests / introspection ── */

/**
 * Every stable run-id, stage-id, and other target-id this adapter
 * references. The Python data-integrity test
 * (`tests/test_action_preview_data_integrity.py`) reads this file as
 * text, extracts the `run-*` patterns it sees, and asserts each
 * exists in the committed static export. The constant is also
 * exposed here so a future TypeScript test could read it directly.
 */
export const REFERENCED_TARGET_IDS: readonly string[] = [
  GOLDEN_RUN_ID,
  REVIEW_RUN_ID,
  PREVIEW_TARGETS.REVIEW_GOVERNANCE_GATE_STAGE_ID,
  PREVIEW_TARGETS.REVIEW_OPEN_REVIEW_ACTION_ID,
  PREVIEW_TARGETS.REVIEW_RETRY_ACTION_ID,
];
