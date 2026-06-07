/**
 * StoryTime — Failure / Recovery view-model adapter (Phase 13D).
 *
 * This module is the "frontend understanding" layer for the Failure /
 * Recovery view. It consumes the raw deterministic static export from
 * `src/data/adapter.ts` and projects UI-ready queue items, joining each
 * failure-queue entry with the corresponding run-detail record so the view
 * can render structured failure / hold reasoning, the affected stage, the
 * related governance decision, evidence references, and visibly-disabled
 * future recovery actions.
 *
 * "Backend owns truth, frontend owns understanding": all facts come from
 * the backend's `failureQueue` projection and the per-run `failure`,
 * `governance`, `stages`, `observability`, and `disabledActions` blocks.
 * The adapter does not invent failure content and never reads raw error
 * text — failures arrive as a structured `errorKind` and operator-safe
 * `operatorGuidance`, consistent with the Architecture Baseline section
 * 25 display discipline.
 *
 * No network, no mutation. No retry / re-run / review-decision is performed
 * here; recovery actions are surfaced only as visibly-disabled affordances,
 * with the Phase that would enable them.
 */

import {
  DEMO_FAILURE_QUEUE,
  DEMO_RUN_DETAILS,
  findRunDetail,
} from "./adapter";
import type {
  DisabledFutureAction,
  EvidenceLink,
  FailureQueueItem,
  GovernanceDecision,
  PipelineRunDetail,
  PipelineStage,
} from "../types/storytime";

/**
 * One row in the Failure / Recovery view — a failure-queue entry joined to
 * the matching run-detail record. Everything the view needs to render the
 * row sits inside one of these objects, so the component file stays
 * declarative.
 */
export interface FailureRecoveryRow {
  /** Stable id of the row — the underlying run id. */
  runId: string;
  /** Display label for the row. */
  runLabel: string;
  /** Structured reason this run needs attention. */
  reason: FailureQueueItem["reason"];
  /** Bounded, display-safe one-liner explaining the reason. */
  summary: string;
  /** What the operator should inspect next, as written by the backend. */
  inspectNext: string;
  /**
   * The structured failure record, if the run carries one. We treat absent
   * failure records as a legitimate "the queue says this run needs review,
   * the run's structured failure block has no further information" — the
   * view falls back on the queue summary in that case.
   */
  failure: PipelineRunDetail["failure"];
  /** The stage where the run stopped or is being held, if discoverable. */
  affectedStage: PipelineStage | undefined;
  /** The governance decision for the run — context for recovery. */
  governance: GovernanceDecision;
  /** Whether the underlying run is actually present in the export. */
  runFound: boolean;
  /**
   * The recovery-related disabled future actions for this run (retry,
   * review-workflow openers). These remain visibly disabled here; Phase 13D
   * does not enable any of them.
   */
  recoveryDisabledActions: DisabledFutureAction[];
  /** Observability evidence links for the run (trace / dashboard). */
  evidenceLinks: EvidenceLink[];
}

/**
 * Words used by the heuristic that selects recovery-related disabled
 * actions. We deliberately match a wider set than the governance adapter
 * because "recovery" includes both governance-decision openers and retry /
 * re-run / regenerate affordances.
 */
const RECOVERY_ACTION_KEYWORDS = [
  "retry",
  "re-run",
  "rerun",
  "review",
  "regenerate",
];

function isRecoveryRelatedAction(action: DisabledFutureAction): boolean {
  const haystack = `${action.label} ${action.disabledReason}`.toLowerCase();
  return RECOVERY_ACTION_KEYWORDS.some((needle) => haystack.includes(needle));
}

/**
 * Pick the stage that best represents "where the run stopped". Preference:
 * an explicitly failed or blocked stage; otherwise the last stage that
 * actually started (the run's progress front); otherwise the first stage.
 */
function findAffectedStage(
  run: PipelineRunDetail,
): PipelineStage | undefined {
  const ordered = [...run.stages].sort((a, b) => a.order - b.order);
  const halted = ordered.find(
    (stage) => stage.status === "failed" || stage.status === "blocked",
  );
  if (halted) {
    return halted;
  }
  const started = [...ordered]
    .reverse()
    .find((stage) => stage.startedAt !== undefined);
  if (started) {
    return started;
  }
  return ordered[0];
}

function projectQueueItem(item: FailureQueueItem): FailureRecoveryRow {
  const run = findRunDetail(item.runId);
  if (!run) {
    // The failure queue refers to a run id that is not present in the
    // export. The export contract makes this very unlikely (the queue is
    // generated from the same run set), but we keep the frontend honest
    // and surface a safe, empty-ish row rather than crashing.
    return {
      runId: item.runId,
      runLabel: item.runLabel,
      reason: item.reason,
      summary: item.summary,
      inspectNext: item.inspectNext,
      failure: undefined,
      affectedStage: undefined,
      governance: {
        status: "review_required",
        contextSummary:
          "This queue entry refers to a run that is not present in the static export.",
        sourceCategory: "UNKNOWN",
        disclaimer:
          "This is a record of a human operator's authorization decision. It is not legal advice and not a certification of copyright safety.",
      },
      runFound: false,
      recoveryDisabledActions: [],
      evidenceLinks: [],
    };
  }

  return {
    runId: item.runId,
    runLabel: item.runLabel,
    reason: item.reason,
    summary: item.summary,
    inspectNext: item.inspectNext,
    failure: run.failure,
    affectedStage: findAffectedStage(run),
    governance: run.governance,
    runFound: true,
    recoveryDisabledActions: run.disabledActions.filter(
      isRecoveryRelatedAction,
    ),
    evidenceLinks: run.observability.links,
  };
}

/** The Failure / Recovery rows, in export order. */
export const FAILURE_RECOVERY_ROWS: readonly FailureRecoveryRow[] =
  DEMO_FAILURE_QUEUE.map(projectQueueItem);

/** Counts of failure / review-queue items by structured reason. */
export interface FailureCounts {
  total: number;
  failed: number;
  blocked: number;
  needsReview: number;
  awaitingApproval: number;
}

function countByReason(
  rows: readonly FailureRecoveryRow[],
): FailureCounts {
  const counts: FailureCounts = {
    total: rows.length,
    failed: 0,
    blocked: 0,
    needsReview: 0,
    awaitingApproval: 0,
  };
  for (const row of rows) {
    switch (row.reason) {
      case "failed":
        counts.failed += 1;
        break;
      case "blocked":
        counts.blocked += 1;
        break;
      case "needs_review":
        counts.needsReview += 1;
        break;
      case "awaiting_approval":
        counts.awaitingApproval += 1;
        break;
    }
  }
  return counts;
}

export const FAILURE_COUNTS: FailureCounts =
  countByReason(FAILURE_RECOVERY_ROWS);

/**
 * Total run count from the export — used by the view to render a stable
 * "N runs in scope" pointer that contextualises the queue size.
 */
export const FAILURE_TOTAL_RUNS_IN_SCOPE: number = DEMO_RUN_DETAILS.length;

/** Display label for a structured queue reason. */
export function failureReasonLabel(
  reason: FailureQueueItem["reason"],
): string {
  switch (reason) {
    case "failed":
      return "failed";
    case "blocked":
      return "blocked";
    case "needs_review":
      return "needs review";
    case "awaiting_approval":
      return "awaiting approval";
  }
}

/** Chip tone for a structured queue reason. */
export function failureReasonTone(
  reason: FailureQueueItem["reason"],
): "warn" | "stop" | "run" {
  switch (reason) {
    case "failed":
    case "blocked":
      return "stop";
    case "needs_review":
      return "warn";
    case "awaiting_approval":
      return "run";
  }
}

/**
 * One bullet on the "why failure visibility matters" panel. Kept here so
 * the view file remains declarative.
 */
export interface FailureTalkingPoint {
  heading: string;
  body: string;
}

export const FAILURE_TALKING_POINTS: readonly FailureTalkingPoint[] = [
  {
    heading: "A run that holds is not a run that hides",
    body:
      "When the governance gate or a pipeline stage holds a run, the operator sees a structured reason, the affected stage, and a guided next step — not a quiet failure and not a raw stack trace.",
  },
  {
    heading: "Failures carry structure, not free text",
    body:
      "Each held or failed run carries a stable error-kind code and operator-safe guidance. Raw error messages and raw blocked-reason text never reach the operator UI; the display discipline is enforced at the export.",
  },
  {
    heading: "Recovery is visibly disabled, not invisibly absent",
    body:
      "Retry and review-workflow affordances are present in the UI but visibly disabled, labelled with the phase that would enable them. The intended operator workflow is legible long before any action becomes invokable.",
  },
  {
    heading: "Evidence stays one click away",
    body:
      "Each row links to its run-detail view so the operator can read the full stage timeline, the governance decision, and the trace reference for the run — without leaving the read-only shell.",
  },
];
