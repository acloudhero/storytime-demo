/**
 * Status presentation helpers — map the contract's status unions to the
 * stylesheet's semantic chip classes, and a small <StatusChip> component.
 *
 * Centralising this keeps status colours consistent across the run detail
 * view and the stage timeline, and keeps the mapping exhaustive (the switch
 * statements have no default, so a new status value is a TypeScript error).
 */

import type {
  GovernanceDecisionStatus,
  PipelineRunStatus,
  PipelineStageStatus,
} from "../types/storytime";

type Tone = "ok" | "run" | "warn" | "stop" | "idle";

interface ChipSpec {
  tone: Tone;
  label: string;
}

export function runChip(status: PipelineRunStatus): ChipSpec {
  switch (status) {
    case "succeeded":
      return { tone: "ok", label: "succeeded" };
    case "recovered":
      return { tone: "ok", label: "recovered" };
    case "running":
      return { tone: "run", label: "running" };
    case "queued":
      return { tone: "idle", label: "queued" };
    case "failed":
      return { tone: "stop", label: "failed" };
    case "blocked":
      return { tone: "stop", label: "blocked" };
  }
}

export function stageChip(status: PipelineStageStatus): ChipSpec {
  switch (status) {
    case "succeeded":
      return { tone: "ok", label: "succeeded" };
    case "running":
      return { tone: "run", label: "running" };
    case "failed":
      return { tone: "stop", label: "failed" };
    case "blocked":
      return { tone: "stop", label: "blocked" };
    case "skipped":
      return { tone: "idle", label: "skipped" };
    case "not_started":
      return { tone: "idle", label: "not started" };
  }
}

export function governanceChip(status: GovernanceDecisionStatus): ChipSpec {
  switch (status) {
    case "allowed":
      return { tone: "ok", label: "allowed" };
    case "review_required":
      return { tone: "warn", label: "review required" };
    case "blocked":
      return { tone: "stop", label: "blocked" };
  }
}

/** The CSS modifier suffix the timeline rail uses for a stage status. */
export function stageRailModifier(status: PipelineStageStatus): string {
  switch (status) {
    case "succeeded":
      return "ok";
    case "running":
      return "run";
    case "failed":
    case "blocked":
      return "blocked";
    case "skipped":
      return "skip";
    case "not_started":
      return "idle";
  }
}

export function StatusChip({ spec }: { spec: ChipSpec }): JSX.Element {
  return (
    <span className={`chip chip--${spec.tone}`}>
      <span className="chip__dot" aria-hidden="true" />
      {spec.label}
    </span>
  );
}
