/**
 * GovernanceSafetyView — the Phase 13D Governance / Safety operator view.
 *
 * Makes StoryTime's governance posture legible: the per-run Trust Envelope
 * decisions, the source authorization categories observed, the governance
 * gate result per run, the honest "what we intentionally do not show"
 * display-discipline note, evidence references, and the visibly-disabled
 * future review actions. Everything renders from the deterministic Phase
 * 13C static export through the `governanceAdapter` — no network call, no
 * mutation, no live integration.
 *
 * Drill-down: the per-run rows expose a callback into the existing
 * Pipeline Run Detail view, so a reviewer can move from "what is the
 * governance decision" to "what did the full run look like" without a
 * router. The callback is passed in from `App.tsx`, following the same
 * pattern Phase 13B/13C uses for run selection.
 */

import {
  GOVERNANCE_COUNTS,
  GOVERNANCE_DOC_REFERENCES,
  GOVERNANCE_RUN_ROWS,
  GOVERNANCE_SAFETY_DISPLAY_RULES,
  GOVERNANCE_STANDING_DISCLAIMER,
  GOVERNANCE_TALKING_POINTS,
  governanceDecisionTone,
  governanceGateTone,
  type GovernanceRunRow,
} from "../data/governanceAdapter";
import type { EvidenceLink, PipelineStage } from "../types/storytime";
import { ActionPreviewPanel } from "./ActionPreviewPanel";
import { DisabledFutureActionList } from "./DisabledFutureActionCard";
import styles from "./GovernanceSafetyView.module.css";

interface GovernanceSafetyViewProps {
  /** Open the matching run in the Pipeline Run Detail view. */
  onInspectRun: (runId: string) => void;
}

function decisionChipClass(
  tone: "ok" | "warn" | "stop",
): string {
  switch (tone) {
    case "ok":
      return "chip chip--ok";
    case "warn":
      return "chip chip--warn";
    case "stop":
      return "chip chip--stop";
  }
}

function gateChipClass(
  tone: "ok" | "warn" | "stop" | "idle",
): string {
  switch (tone) {
    case "ok":
      return "chip chip--ok";
    case "warn":
      return "chip chip--warn";
    case "stop":
      return "chip chip--stop";
    case "idle":
      return "chip chip--idle";
  }
}

function GateRow({ stage }: { stage: PipelineStage }): JSX.Element {
  const tone = governanceGateTone(stage.status);
  return (
    <div className={styles.gate}>
      <span className={styles.gateLabel}>Governance gate</span>
      <span className={gateChipClass(tone)}>
        <span className="chip__dot" aria-hidden="true" />
        {stage.status.replace(/_/g, " ")}
      </span>
      {stage.note ? <p className={styles.gateNote}>{stage.note}</p> : null}
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

function RunRow({
  row,
  onInspectRun,
}: {
  row: GovernanceRunRow;
  onInspectRun: (runId: string) => void;
}): JSX.Element {
  const tone = governanceDecisionTone(row.decision.status);
  return (
    <article className={styles.row}>
      <header className={styles.rowHead}>
        <div className={styles.rowIdent}>
          <span className={styles.rowLabel}>{row.runLabel}</span>
          <span className={styles.rowId}>{row.runId}</span>
        </div>
        <span className={decisionChipClass(tone)}>
          <span className="chip__dot" aria-hidden="true" />
          {row.decision.status.replace(/_/g, " ")}
        </span>
      </header>

      <dl className={styles.rowKv}>
        <dt>Source category</dt>
        <dd className="mono">{row.decision.sourceCategory}</dd>
        <dt>Decision context</dt>
        <dd>{row.decision.contextSummary}</dd>
      </dl>

      {row.governanceGate ? <GateRow stage={row.governanceGate} /> : null}

      {row.evidenceLinks.length > 0 ? (
        <div className={styles.evidenceBlock}>
          <h4 className={styles.subHead}>Evidence</h4>
          <div className={styles.evidenceList}>
            {row.evidenceLinks.map((link) => (
              <EvidenceRow key={link.id} link={link} />
            ))}
          </div>
        </div>
      ) : null}

      {row.governanceDisabledActions.length > 0 ? (
        <div className={styles.actionsBlock}>
          <h4 className={styles.subHead}>
            Review actions · visibly disabled
          </h4>
          <DisabledFutureActionList
            actions={row.governanceDisabledActions}
          />
        </div>
      ) : null}

      <p className={`note-muted ${styles.rowDisclaimer}`}>
        {row.decision.disclaimer}
      </p>

      <div className={styles.rowFooter}>
        <button
          type="button"
          className={styles.inspectBtn}
          onClick={() => onInspectRun(row.runId)}
        >
          Inspect this run in Pipeline Run Detail →
        </button>
      </div>
    </article>
  );
}

export function GovernanceSafetyView({
  onInspectRun,
}: GovernanceSafetyViewProps): JSX.Element {
  return (
    <div className="stack">
      <header className="reveal reveal--1">
        <p className="eyebrow">Operator GUI · read-only</p>
        <h1 className="page-title">Governance / Safety</h1>
        <p className="lede">
          How StoryTime authorizes a source, where the fail-closed gate runs,
          and what the operator sees when a run is held. All data here is the
          deterministic Phase 13C static export; this view contacts no backend
          and changes no state.
        </p>
      </header>

      <section className="panel reveal reveal--2">
        <h2 className={styles.sectionTitle}>Trust Envelope posture</h2>
        <p className={styles.posture}>
          Every pipeline run carries a per-source Trust Envelope: a stable
          decision status, a structured source-authorization category, and a
          bounded context summary. The governance gate enforces the envelope
          fail-closed — before any expensive stage runs. The frontend shows
          only the projection the backend exports; it cannot change a decision
          and has no path to do so.
        </p>
        <p className={`note-muted ${styles.disclaimer}`}>
          {GOVERNANCE_STANDING_DISCLAIMER}
        </p>
      </section>

      <section className="reveal reveal--2">
        <h2 className={styles.sectionTitle}>Decision summary</h2>
        <div className={styles.counts} role="list">
          <div className={styles.countCard} role="listitem">
            <span className={styles.countValue}>
              {GOVERNANCE_COUNTS.total}
            </span>
            <span className={styles.countLabel}>runs in scope</span>
          </div>
          <div className={styles.countCard} role="listitem">
            <span className={styles.countValue}>
              {GOVERNANCE_COUNTS.allowed}
            </span>
            <span className={styles.countLabel}>allowed</span>
          </div>
          <div className={styles.countCard} role="listitem">
            <span className={styles.countValue}>
              {GOVERNANCE_COUNTS.reviewRequired}
            </span>
            <span className={styles.countLabel}>review required</span>
          </div>
          <div className={styles.countCard} role="listitem">
            <span className={styles.countValue}>
              {GOVERNANCE_COUNTS.blocked}
            </span>
            <span className={styles.countLabel}>blocked</span>
          </div>
        </div>
      </section>

      <section className="reveal reveal--3">
        <h2 className={styles.sectionTitle}>Per-run decisions</h2>
        {GOVERNANCE_RUN_ROWS.length > 0 ? (
          <div className={styles.rows}>
            {GOVERNANCE_RUN_ROWS.map((row) => (
              <RunRow
                key={row.runId}
                row={row}
                onInspectRun={onInspectRun}
              />
            ))}
          </div>
        ) : (
          <p className="note-muted">
            No runs are present in the static export.
          </p>
        )}
      </section>

      <section className="reveal reveal--4">
        <h2 className={styles.sectionTitle}>
          What this view intentionally hides
        </h2>
        <p className={styles.honestyIntro}>
          Display discipline is part of governance. The Architecture Baseline
          section 25 rules below apply across the frontend and are enforced at
          the export — this view never bypasses them.
        </p>
        <ul className={styles.honesty}>
          {GOVERNANCE_SAFETY_DISPLAY_RULES.map((rule) => (
            <li key={rule.title} className={styles.honestyItem}>
              <span className={styles.honestyTitle}>{rule.title}</span>
              <p className={styles.honestyBody}>{rule.body}</p>
            </li>
          ))}
        </ul>
      </section>

      <section className="reveal reveal--4">
        <h2 className={styles.sectionTitle}>Why governance matters here</h2>
        <div className={styles.talkingGrid}>
          {GOVERNANCE_TALKING_POINTS.map((point) => (
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
            "preview-inspect-trust-envelope",
            "preview-record-review-decision",
          ]}
          view="Governance / Safety"
        />
      </section>

      <section className="reveal reveal--4">
        <h2 className={styles.sectionTitle}>Reference documents</h2>
        <div className={styles.evidenceList}>
          {GOVERNANCE_DOC_REFERENCES.map((link) => (
            <EvidenceRow key={link.id} link={link} />
          ))}
        </div>
        <p className="note-muted" style={{ marginTop: "12px" }}>
          References are shown as repository-relative paths. The static shell
          does not fetch them; open them in the repository.
        </p>
      </section>
    </div>
  );
}
