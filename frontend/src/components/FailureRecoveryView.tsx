/**
 * FailureRecoveryView — the Phase 13D Failure / Recovery operator view.
 *
 * Surfaces the runs that need operator attention from the deterministic
 * Phase 13C static export: the failure / review queue, the affected stage,
 * the structured failure summary (no raw error text), the related
 * governance decision, evidence references, the operator's "inspect next"
 * guidance, and the recovery affordances — which remain visibly disabled
 * here because mutation is Phase 13E, not 13D.
 *
 * Drill-down: each row exposes an "Open in Pipeline Run Detail" button
 * that calls back into the App-level run-selection state, the same simple
 * callback pattern Phase 13B/13C already uses. No router is introduced.
 *
 * The component reads from `failureAdapter`. It does not perform retry,
 * re-run, review-decision recording, or any backend call.
 */

import {
  FAILURE_COUNTS,
  FAILURE_RECOVERY_ROWS,
  FAILURE_TALKING_POINTS,
  FAILURE_TOTAL_RUNS_IN_SCOPE,
  failureReasonLabel,
  failureReasonTone,
  type FailureRecoveryRow,
} from "../data/failureAdapter";
import { governanceDecisionTone } from "../data/governanceAdapter";
import type {
  EvidenceLink,
  GovernanceDecision,
  PipelineStage,
} from "../types/storytime";
import { ActionPreviewPanel } from "./ActionPreviewPanel";
import { DisabledFutureActionList } from "./DisabledFutureActionCard";
import styles from "./FailureRecoveryView.module.css";

interface FailureRecoveryViewProps {
  /** Open the matching run in the Pipeline Run Detail view. */
  onInspectRun: (runId: string) => void;
}

function reasonChipClass(tone: "warn" | "stop" | "run"): string {
  switch (tone) {
    case "warn":
      return "chip chip--warn";
    case "stop":
      return "chip chip--stop";
    case "run":
      return "chip chip--run";
  }
}

function governanceChipClass(tone: "ok" | "warn" | "stop"): string {
  switch (tone) {
    case "ok":
      return "chip chip--ok";
    case "warn":
      return "chip chip--warn";
    case "stop":
      return "chip chip--stop";
  }
}

function StagePill({ stage }: { stage: PipelineStage }): JSX.Element {
  return (
    <div className={styles.stagePill}>
      <span className={styles.stagePillName}>{stage.name}</span>
      <span className={styles.stagePillStatus}>
        {stage.status.replace(/_/g, " ")}
      </span>
      {stage.note ? <p className={styles.stagePillNote}>{stage.note}</p> : null}
    </div>
  );
}

function GovernanceLink({
  governance,
}: {
  governance: GovernanceDecision;
}): JSX.Element {
  const tone = governanceDecisionTone(governance.status);
  return (
    <div className={styles.governance}>
      <div className={styles.governanceHead}>
        <span className={styles.governanceTitle}>
          Related governance decision
        </span>
        <span className={governanceChipClass(tone)}>
          <span className="chip__dot" aria-hidden="true" />
          {governance.status.replace(/_/g, " ")}
        </span>
      </div>
      <dl className={styles.governanceKv}>
        <dt>Source category</dt>
        <dd className="mono">{governance.sourceCategory}</dd>
        <dt>Context</dt>
        <dd>{governance.contextSummary}</dd>
      </dl>
    </div>
  );
}

function EvidenceRow({ link }: { link: EvidenceLink }): JSX.Element {
  return (
    <div className={styles.evidence}>
      <div className={styles.evidenceHead}>
        <span className={styles.evidenceLabel}>{link.label}</span>
        <span className="tag-disabled">{link.kind}</span>
      </div>
      {link.note ? <p className={styles.evidenceNote}>{link.note}</p> : null}
      <code className={styles.evidenceRef}>{link.reference}</code>
    </div>
  );
}

function QueueRow({
  row,
  onInspectRun,
}: {
  row: FailureRecoveryRow;
  onInspectRun: (runId: string) => void;
}): JSX.Element {
  const tone = failureReasonTone(row.reason);
  return (
    <article className={styles.row}>
      <header className={styles.rowHead}>
        <div className={styles.rowIdent}>
          <span className={styles.rowLabel}>{row.runLabel}</span>
          <span className={styles.rowId}>{row.runId}</span>
        </div>
        <span className={reasonChipClass(tone)}>
          <span className="chip__dot" aria-hidden="true" />
          {failureReasonLabel(row.reason)}
        </span>
      </header>

      <p className={styles.summary}>{row.summary}</p>

      {!row.runFound ? (
        <p className={`note-muted ${styles.warning}`}>
          The static export does not contain a run with this id; only the
          queue summary is available.
        </p>
      ) : null}

      {row.affectedStage ? (
        <div className={styles.section}>
          <h4 className={styles.subHead}>Where it stopped</h4>
          <StagePill stage={row.affectedStage} />
        </div>
      ) : null}

      {row.failure ? (
        <div className={styles.section}>
          <h4 className={styles.subHead}>Failure / hold summary</h4>
          <div className={styles.failure}>
            <dl className={styles.failureKv}>
              <dt>Error kind</dt>
              <dd className="mono">{row.failure.errorKind}</dd>
              <dt>Operator guidance</dt>
              <dd>{row.failure.operatorGuidance}</dd>
            </dl>
            <p className="note-muted" style={{ marginTop: "8px" }}>
              Structured error code only — no raw error message and no raw
              blocked-reason text reaches the operator UI.
            </p>
          </div>
        </div>
      ) : null}

      <div className={styles.section}>
        <GovernanceLink governance={row.governance} />
      </div>

      <div className={styles.section}>
        <h4 className={styles.subHead}>Inspect next</h4>
        <p className={styles.inspectNote}>{row.inspectNext}</p>
      </div>

      {row.evidenceLinks.length > 0 ? (
        <div className={styles.section}>
          <h4 className={styles.subHead}>Evidence</h4>
          <div className={styles.evidenceList}>
            {row.evidenceLinks.map((link) => (
              <EvidenceRow key={link.id} link={link} />
            ))}
          </div>
        </div>
      ) : null}

      {row.recoveryDisabledActions.length > 0 ? (
        <div className={styles.section}>
          <h4 className={styles.subHead}>Recovery actions · visibly disabled</h4>
          <DisabledFutureActionList
            actions={row.recoveryDisabledActions}
          />
        </div>
      ) : null}

      <div className={styles.rowFooter}>
        <button
          type="button"
          className={styles.inspectBtn}
          onClick={() => onInspectRun(row.runId)}
          disabled={!row.runFound}
        >
          Open in Pipeline Run Detail →
        </button>
      </div>
    </article>
  );
}

export function FailureRecoveryView({
  onInspectRun,
}: FailureRecoveryViewProps): JSX.Element {
  const hasQueue = FAILURE_RECOVERY_ROWS.length > 0;

  return (
    <div className="stack">
      <header className="reveal reveal--1">
        <p className="eyebrow">Operator GUI · read-only</p>
        <h1 className="page-title">Failure / Recovery</h1>
        <p className="lede">
          The runs that need attention, what stopped them, what evidence to
          read, and what the operator should inspect next. Read-only and
          backed by the deterministic Phase 13C static export — no backend
          call, no retry, no re-run from this view.
        </p>
      </header>

      <section className="reveal reveal--2">
        <h2 className={styles.sectionTitle}>Queue summary</h2>
        <div className={styles.counts} role="list">
          <div className={styles.countCard} role="listitem">
            <span className={styles.countValue}>
              {FAILURE_COUNTS.total}
            </span>
            <span className={styles.countLabel}>
              in queue / {FAILURE_TOTAL_RUNS_IN_SCOPE} runs in scope
            </span>
          </div>
          <div className={styles.countCard} role="listitem">
            <span className={styles.countValue}>
              {FAILURE_COUNTS.failed}
            </span>
            <span className={styles.countLabel}>failed</span>
          </div>
          <div className={styles.countCard} role="listitem">
            <span className={styles.countValue}>
              {FAILURE_COUNTS.blocked}
            </span>
            <span className={styles.countLabel}>blocked</span>
          </div>
          <div className={styles.countCard} role="listitem">
            <span className={styles.countValue}>
              {FAILURE_COUNTS.needsReview}
            </span>
            <span className={styles.countLabel}>needs review</span>
          </div>
          <div className={styles.countCard} role="listitem">
            <span className={styles.countValue}>
              {FAILURE_COUNTS.awaitingApproval}
            </span>
            <span className={styles.countLabel}>awaiting approval</span>
          </div>
        </div>
      </section>

      <section className="reveal reveal--3">
        <h2 className={styles.sectionTitle}>Queue</h2>
        {hasQueue ? (
          <div className={styles.rows}>
            {FAILURE_RECOVERY_ROWS.map((row) => (
              <QueueRow
                key={row.runId}
                row={row}
                onInspectRun={onInspectRun}
              />
            ))}
          </div>
        ) : (
          <div className={`panel ${styles.empty}`}>
            <p>
              The static demo export currently shows no runs needing
              attention. A held or failed run would appear here with a
              structured reason, the affected stage, the related governance
              decision, and a guided next step.
            </p>
          </div>
        )}
      </section>

      <section className="reveal reveal--4">
        <h2 className={styles.sectionTitle}>
          Why failure visibility matters
        </h2>
        <div className={styles.talkingGrid}>
          {FAILURE_TALKING_POINTS.map((point) => (
            <article key={point.heading} className={styles.talking}>
              <h3 className={styles.talkingHead}>{point.heading}</h3>
              <p className={styles.talkingBody}>{point.body}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="reveal reveal--4">
        <ActionPreviewPanel
          availablePreviews={[
            "preview-retry-failed-stage",
            "preview-regenerate-operator-report",
          ]}
          view="Failure / Recovery"
        />
      </section>

      <section className="reveal reveal--4">
        <p className="note-muted">
          This view is read-only. Retry, re-run, report regeneration, and
          review-decision recording are not implemented as executing
          actions: the disabled affordances above remain visibly
          disabled, and the Demo-mode action-preview panel renders an
          inline preview of operator intent without ever executing
          anything (Phase 13E). Real execution is deferred to a future
          Local mode or Cloud / Distributed mode.
        </p>
      </section>
    </div>
  );
}
