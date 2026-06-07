/**
 * StoryTime — Governance view-model adapter (Phase 13D).
 *
 * This module is the "frontend understanding" layer for the Governance / Safety
 * view. It consumes the raw deterministic static export from
 * `src/data/adapter.ts` and projects UI-ready governance data, without
 * fetching, mutating, or assuming anything beyond the documented export
 * contract.
 *
 * "Backend owns truth, frontend owns understanding": all per-run governance
 * facts come from the backend export's per-run `governance` block, observed
 * `stages` (the governance gate stage is part of the run's ordered stages),
 * and `disabledActions`. This adapter only re-projects them — it does not
 * invent governance content.
 *
 * No network, no mutation, no backend assumption beyond the Phase 13C
 * `StaticDemoExport` contract documented in
 * `docs/frontend-static-export-contract.md`.
 */

import { DEMO_RUN_DETAILS } from "./adapter";
import type {
  DisabledFutureAction,
  EvidenceLink,
  GovernanceDecision,
  GovernanceDecisionStatus,
  PipelineRunDetail,
  PipelineStage,
  PipelineStageStatus,
} from "../types/storytime";

/**
 * One row in the Governance / Safety decisions table — a per-run projection
 * of the run's governance decision, the governance-gate stage result, and the
 * governance-related disabled future actions.
 */
export interface GovernanceRunRow {
  /** The owning run's id, for the "inspect this run" callback. */
  runId: string;
  /** The owning run's display label. */
  runLabel: string;
  /** The governance decision as exported by the backend. */
  decision: GovernanceDecision;
  /** The governance gate stage, if the run records one. */
  governanceGate: PipelineStage | undefined;
  /**
   * The subset of the run's disabled future actions that read as
   * governance-related (review workflow, retry after review). Phase 13D shows
   * these as visibly-disabled affordances so the intended workflow shape is
   * legible, never as invokable controls.
   */
  governanceDisabledActions: DisabledFutureAction[];
  /**
   * The non-dashboard observability evidence links for the run (the trace
   * link is the strongest piece of governance evidence we can surface today).
   */
  evidenceLinks: EvidenceLink[];
}

/**
 * Headline counts of governance decisions across the demo runs. This is a
 * trivial derivation, kept here so the view file stays declarative.
 */
export interface GovernanceCounts {
  total: number;
  allowed: number;
  reviewRequired: number;
  blocked: number;
}

/**
 * A short, display-safe "what we intentionally hide" note. This is portfolio
 * content, but it is co-located with the governance adapter so the view file
 * does not have to know the Architecture Baseline section 25 display
 * discipline by heart.
 */
export interface SafetyDisplayRule {
  title: string;
  body: string;
}

/**
 * The honest list of things the Governance / Safety view intentionally does
 * **not** show — the Architecture Baseline section 25 display-discipline
 * rules, re-framed for a reviewer. These rules apply to the whole frontend;
 * surfacing them here is portfolio-grade honesty.
 */
export const GOVERNANCE_SAFETY_DISPLAY_RULES: readonly SafetyDisplayRule[] = [
  {
    title: "No raw blocked-reason text",
    body:
      "When a run is held by the governance gate, the export carries a stable error-kind code and operator-safe guidance — never the raw, free-form blocked-reason text. The UI shows the structured fields only.",
  },
  {
    title: "No source content, no transcripts",
    body:
      "Source text, narration scripts, and intermediate transcripts never appear in the export or this view. Artifacts are references, not embedded payloads.",
  },
  {
    title: "No secrets or local paths",
    body:
      "No credentials, tokens, environment variables, or absolute local filesystem paths are exposed. Repository-relative or artifact-scoped references only.",
  },
  {
    title: "No legal or compliance overclaiming",
    body:
      "Governance records a human operator's authorization decision. It is not a certification of copyright safety, and this view never describes it as one.",
  },
];

/**
 * Words used by the heuristic that picks out governance-related disabled
 * actions. The match is intentionally narrow — we look for review and retry
 * vocabulary that has unambiguous governance meaning in this codebase.
 */
const GOVERNANCE_ACTION_KEYWORDS = ["review", "retry after"];

function isGovernanceRelatedAction(action: DisabledFutureAction): boolean {
  const haystack = `${action.label} ${action.disabledReason}`.toLowerCase();
  return GOVERNANCE_ACTION_KEYWORDS.some((needle) => haystack.includes(needle));
}

function findGovernanceGate(run: PipelineRunDetail): PipelineStage | undefined {
  return run.stages.find((stage) =>
    stage.name.toLowerCase().includes("governance"),
  );
}

function projectRun(run: PipelineRunDetail): GovernanceRunRow {
  return {
    runId: run.id,
    runLabel: run.label,
    decision: run.governance,
    governanceGate: findGovernanceGate(run),
    governanceDisabledActions: run.disabledActions.filter(
      isGovernanceRelatedAction,
    ),
    evidenceLinks: run.observability.links.filter(
      (link) => link.kind === "trace",
    ),
  };
}

/** The Governance / Safety decisions table, in export order. */
export const GOVERNANCE_RUN_ROWS: readonly GovernanceRunRow[] =
  DEMO_RUN_DETAILS.map(projectRun);

/** Decision-status counts across the demo runs. */
export const GOVERNANCE_COUNTS: GovernanceCounts = countDecisions(
  GOVERNANCE_RUN_ROWS,
);

function countDecisions(
  rows: readonly GovernanceRunRow[],
): GovernanceCounts {
  const counts: GovernanceCounts = {
    total: rows.length,
    allowed: 0,
    reviewRequired: 0,
    blocked: 0,
  };
  for (const row of rows) {
    switch (row.decision.status) {
      case "allowed":
        counts.allowed += 1;
        break;
      case "review_required":
        counts.reviewRequired += 1;
        break;
      case "blocked":
        counts.blocked += 1;
        break;
    }
  }
  return counts;
}

/**
 * One bullet on the "why governance matters" panel. Short, display-safe,
 * never claims live governance integration.
 */
export interface GovernanceTalkingPoint {
  heading: string;
  body: string;
}

export const GOVERNANCE_TALKING_POINTS: readonly GovernanceTalkingPoint[] = [
  {
    heading: "A human decision, durably recorded",
    body:
      "Every source is authorized — or held — by a named human decision before any expensive stage runs. The decision is captured in the per-run Trust Envelope; the export surfaces it as a stable status, a structured source category, and a bounded context summary.",
  },
  {
    heading: "Fail-closed before expensive stages",
    body:
      "The governance gate runs between Ingest and Synthesize. If a source has no clear authorization, the gate holds the run — it does not allow it to proceed and quietly succeed. The held run in this demo shows that path.",
  },
  {
    heading: "Honest about what it is not",
    body:
      "Governance records a human decision. It is not legal automation, not a copyright-clearance engine, and not a compliance certification. The standing disclaimer on each decision says that plainly.",
  },
  {
    heading: "Evidence over assertion",
    body:
      "Each decision is linked to a pipeline trace and to the run's stage timeline, so a reviewer can see where the decision was applied — not just that it was applied.",
  },
];

/**
 * The single canonical disclaimer used across governance decisions. The
 * export attaches an equivalent disclaimer to each per-run decision; this
 * constant is the bare text used in the view header so the page reads
 * coherently without repeating the same string twice in the same render.
 */
export const GOVERNANCE_STANDING_DISCLAIMER: string =
  "Governance decisions are records of a human operator's authorization. They are not legal advice and not a certification of copyright safety.";

/**
 * Stable evidence pointers for the Governance / Safety view: references the
 * reviewer can open in the repo. These are not fetched — they are displayed
 * as references, consistent with the rest of the Phase 13C/13D shell.
 */
export const GOVERNANCE_DOC_REFERENCES: readonly EvidenceLink[] = [
  {
    id: "gov-doc-architecture-baseline-25",
    label: "Architecture Baseline — Section 25 (Operator Experience)",
    kind: "doc",
    reference: "docs/architecture-baseline.md",
    note:
      "The locked operator-experience law: display discipline, disabled actions, and the mutation boundary.",
  },
  {
    id: "gov-doc-architecture-baseline-24",
    label: "Architecture Baseline — Section 24 (Governance Baseline)",
    kind: "doc",
    reference: "docs/architecture-baseline.md",
    note: "The Trust Envelope, source authorization, and the fail-closed gate.",
  },
  {
    id: "gov-doc-frontend-static-export-contract",
    label: "Frontend Static Export Contract",
    kind: "doc",
    reference: "docs/frontend-static-export-contract.md",
    note:
      "The deterministic, read-only export shape that backs this view's data.",
  },
];

/**
 * Helper: chip-tone for a governance stage outcome on the gate stage. The
 * regular stage status union is wider than the visual semantics we need
 * here (we collapse `not_started` and `skipped` into an idle tone for the
 * gate-result row).
 */
export function governanceGateTone(
  status: PipelineStageStatus,
): "ok" | "warn" | "stop" | "idle" {
  switch (status) {
    case "succeeded":
      return "ok";
    case "running":
      return "warn";
    case "failed":
    case "blocked":
      return "stop";
    case "skipped":
    case "not_started":
      return "idle";
  }
}

/**
 * Helper: chip-tone for a decision status — re-exported so the view file
 * does not have to know the mapping. Mirrors `governanceChip` semantics.
 */
export function governanceDecisionTone(
  status: GovernanceDecisionStatus,
): "ok" | "warn" | "stop" {
  switch (status) {
    case "allowed":
      return "ok";
    case "review_required":
      return "warn";
    case "blocked":
      return "stop";
  }
}
