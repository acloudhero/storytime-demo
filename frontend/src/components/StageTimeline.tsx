/**
 * StageTimeline — the primary visual element of the Pipeline Run Detail view.
 *
 * Renders a run's ordered stages as a vertical timeline built from plain
 * HTML + CSS (flexbox/grid). No charting library, no React Flow, no D3 — per
 * the Phase 13B scope. It is read-only: it visualises stage status, order,
 * gates, durations, and notes, and nothing more.
 */

import type { PipelineStage } from "../types/storytime";
import { stageChip, stageRailModifier, StatusChip } from "./status";

function formatDuration(seconds: number | undefined): string | null {
  if (seconds === undefined) {
    return null;
  }
  if (seconds < 60) {
    return `${seconds}s`;
  }
  const minutes = Math.floor(seconds / 60);
  const rest = seconds % 60;
  return rest === 0 ? `${minutes}m` : `${minutes}m ${rest}s`;
}

function nodeGlyph(status: PipelineStage["status"]): string {
  switch (status) {
    case "succeeded":
      return "✓";
    case "failed":
      return "✕";
    case "blocked":
      return "!";
    case "running":
      return "•";
    case "skipped":
      return "–";
    case "not_started":
      return "·";
  }
}

export function StageTimeline({
  stages,
}: {
  stages: PipelineStage[];
}): JSX.Element {
  const ordered = [...stages].sort((a, b) => a.order - b.order);

  return (
    <ol className="timeline" aria-label="Pipeline stage timeline">
      {ordered.map((stage) => {
        const duration = formatDuration(stage.durationSeconds);
        return (
          <li
            key={stage.id}
            className={`stage stage--${stageRailModifier(stage.status)}`}
          >
            <div className="stage__rail" aria-hidden="true">
              <span
                className={
                  stage.isApprovalGate
                    ? "stage__node stage__node--gate"
                    : "stage__node"
                }
              >
                <span>{nodeGlyph(stage.status)}</span>
              </span>
              <span className="stage__connector" />
            </div>
            <div className="stage__body">
              <div className="stage__head">
                <span className="stage__name">{stage.name}</span>
                {stage.isApprovalGate ? (
                  <span className="stage__gatetag">approval gate</span>
                ) : null}
                <StatusChip spec={stageChip(stage.status)} />
                {duration ? (
                  <span className="stage__time">{duration}</span>
                ) : null}
              </div>
              {stage.note ? <p className="stage__note">{stage.note}</p> : null}
            </div>
          </li>
        );
      })}
    </ol>
  );
}
