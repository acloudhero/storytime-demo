/**
 * PipelineRunDetailPage — the one operator-focused view built in Phase 13B.
 *
 * It makes a single pipeline run legible: a run picker over the two demo runs,
 * a run summary, the visual Stage Timeline (the primary element), the
 * governance decision, a structured failure summary when present, artifact and
 * observability references, and the operator actions — the non-mutating ones
 * shown live, the mutating ones shown visibly disabled with the phase that
 * would enable them.
 *
 * It is read-only and backed entirely by static demo data.
 */

import { useState } from "react";
import {
  DEMO_RUN_SUMMARIES,
  findRunDetail,
} from "../data/adapter";
import type {
  AllowedOperatorAction,
  DisabledFutureAction,
  EpisodeArtifact,
  EvidenceLink,
} from "../types/storytime";
import { StageTimeline } from "./StageTimeline";
import { governanceChip, runChip, StatusChip } from "./status";

function formatTimestamp(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) {
    return iso;
  }
  return date.toISOString().replace("T", " ").replace(".000Z", " UTC");
}

function ArtifactRow({ artifact }: { artifact: EpisodeArtifact }): JSX.Element {
  const bits: string[] = [artifact.kind];
  if (artifact.durationSeconds !== undefined) {
    bits.push(`${artifact.durationSeconds}s`);
  }
  if (artifact.sizeBytes !== undefined) {
    bits.push(`${Math.round(artifact.sizeBytes / 1024)} KiB`);
  }
  return (
    <div className="action">
      <div className="action__head">
        <span className="action__label">{artifact.label}</span>
        <span className="tag-disabled">{bits.join(" · ")}</span>
      </div>
      <code className="action__payload">{artifact.reference}</code>
    </div>
  );
}

function EvidenceRow({ link }: { link: EvidenceLink }): JSX.Element {
  return (
    <div className="action">
      <div className="action__head">
        <span className="action__label">{link.label}</span>
        <span className="tag-disabled">{link.kind}</span>
      </div>
      {link.note ? <p className="action__desc">{link.note}</p> : null}
      <code className="action__payload">{link.reference}</code>
    </div>
  );
}

function AllowedActionRow({
  action,
}: {
  action: AllowedOperatorAction;
}): JSX.Element {
  return (
    <div className="action">
      <div className="action__head">
        <span className="action__label">{action.label}</span>
        <span className="tag-disabled">
          {action.kind === "copy_command" ? "command" : "reference"}
        </span>
      </div>
      <p className="action__desc">{action.description}</p>
      <code className="action__payload">{action.payload}</code>
    </div>
  );
}

function DisabledActionRow({
  action,
}: {
  action: DisabledFutureAction;
}): JSX.Element {
  return (
    <div className="action action--disabled">
      <div className="action__head">
        <span className="action__label">{action.label}</span>
        <span className="tag-disabled">disabled</span>
        {action.isMutation ? (
          <span className="tag-mutation">mutation</span>
        ) : null}
        <span className="note-muted">enabled by {action.enabledByPhase}</span>
      </div>
      <p className="action__desc">{action.disabledReason}</p>
    </div>
  );
}

export function PipelineRunDetailPage({
  selectedRunId,
  onSelectRun,
}: {
  selectedRunId: string | null;
  onSelectRun: (id: string) => void;
}): JSX.Element {
  const fallbackId = DEMO_RUN_SUMMARIES[0]?.id ?? "";
  const [localId, setLocalId] = useState<string>(selectedRunId ?? fallbackId);

  const activeId = selectedRunId ?? localId;
  const run = findRunDetail(activeId) ?? findRunDetail(fallbackId);

  function pick(id: string): void {
    setLocalId(id);
    onSelectRun(id);
  }

  if (!run) {
    return (
      <div className="placeholder">
        <p>No demo runs are available.</p>
      </div>
    );
  }

  return (
    <div className="stack">
      <header className="reveal reveal--1">
        <p className="eyebrow">Operator GUI · read-only</p>
        <h1 className="page-title">Pipeline Run Detail</h1>
        <p className="lede">
          One run, made legible. The stage timeline is the core of this view:
          it shows what happened, where the run progressed or stopped, and what
          is blocked or review-required. All data here is static demo data.
        </p>
      </header>

      <div
        className="run-picker reveal reveal--2"
        role="group"
        aria-label="Select a demo run"
      >
        {DEMO_RUN_SUMMARIES.map((summary) => (
          <button
            key={summary.id}
            type="button"
            className="run-tab"
            aria-pressed={summary.id === run.id}
            onClick={() => pick(summary.id)}
          >
            <span className="run-tab__label">{summary.label}</span>
            <span className="run-tab__meta">
              {summary.id} · {summary.status}
              {summary.needsAttention ? " · needs attention" : ""}
            </span>
          </button>
        ))}
      </div>

      <section className="panel reveal reveal--2">
        <div className="row-between">
          <h2 className="sub-title" style={{ margin: 0 }}>
            Run summary
          </h2>
          <StatusChip spec={runChip(run.status)} />
        </div>
        <dl className="kv" style={{ marginTop: "12px" }}>
          <dt>Run id</dt>
          <dd className="mono">{run.id}</dd>
          <dt>Label</dt>
          <dd>{run.label}</dd>
          <dt>Created</dt>
          <dd className="mono">{formatTimestamp(run.createdAt)}</dd>
          <dt>Updated</dt>
          <dd className="mono">{formatTimestamp(run.updatedAt)}</dd>
        </dl>
        <div className="callout" style={{ marginTop: "14px" }}>
          {run.stateExplanation}
        </div>
      </section>

      <section className="reveal reveal--3">
        <h2 className="section-title">Stage timeline</h2>
        <StageTimeline stages={run.stages} />
      </section>

      <section className="reveal reveal--3">
        <h2 className="section-title">Governance decision</h2>
        <div className="panel">
          <div className="row-between">
            <span className="id">source category · {run.governance.sourceCategory}</span>
            <StatusChip spec={governanceChip(run.governance.status)} />
          </div>
          <p style={{ marginTop: "12px" }}>{run.governance.contextSummary}</p>
          <p className="note-muted">{run.governance.disclaimer}</p>
        </div>
      </section>

      {run.failure ? (
        <section className="reveal reveal--3">
          <h2 className="section-title">Failure / hold summary</h2>
          <div className="panel">
            <dl className="kv">
              <dt>Error kind</dt>
              <dd className="mono">{run.failure.errorKind}</dd>
              <dt>Operator guidance</dt>
              <dd>{run.failure.operatorGuidance}</dd>
            </dl>
            <p className="note-muted" style={{ marginTop: "10px" }}>
              Structured error code only — StoryTime never displays a raw error
              message or raw blocked-reason text.
            </p>
          </div>
        </section>
      ) : null}

      <section className="reveal reveal--4">
        <h2 className="section-title">Episode artifacts</h2>
        {run.artifacts.length > 0 ? (
          <div className="actions">
            {run.artifacts.map((artifact) => (
              <ArtifactRow key={artifact.id} artifact={artifact} />
            ))}
          </div>
        ) : (
          <p className="note-muted">
            This run produced no artifacts — it was held before any output
            stage ran.
          </p>
        )}
      </section>

      <section className="reveal reveal--4">
        <h2 className="section-title">Observability evidence</h2>
        <div className="panel">
          <dl className="kv">
            <dt>Correlation key</dt>
            <dd className="mono">{run.observability.correlationKey}</dd>
            {run.observability.traceId ? (
              <>
                <dt>Trace id</dt>
                <dd className="mono">{run.observability.traceId}</dd>
              </>
            ) : null}
          </dl>
        </div>
        <div className="actions" style={{ marginTop: "12px" }}>
          {run.observability.links.map((link) => (
            <EvidenceRow key={link.id} link={link} />
          ))}
        </div>
      </section>

      <section className="reveal reveal--4">
        <h2 className="section-title">Operator actions</h2>
        <h3 className="sub-title">Available now (non-mutating)</h3>
        {run.allowedActions.length > 0 ? (
          <div className="actions">
            {run.allowedActions.map((action) => (
              <AllowedActionRow key={action.id} action={action} />
            ))}
          </div>
        ) : (
          <p className="note-muted">No non-mutating actions for this run.</p>
        )}
        <h3 className="sub-title">Visible but disabled (future phases)</h3>
        {run.disabledActions.length > 0 ? (
          <div className="actions">
            {run.disabledActions.map((action) => (
              <DisabledActionRow key={action.id} action={action} />
            ))}
          </div>
        ) : (
          <p className="note-muted">No disabled future actions for this run.</p>
        )}
        <p className="note-muted" style={{ marginTop: "12px" }}>
          Phase 13C is read-only. Mutating actions (retry, review decisions,
          report regeneration) are shown as disabled affordances so the
          intended operator workflow is visible; they are implemented only in
          the explicitly gated Phase 13E.
        </p>
      </section>
    </div>
  );
}
