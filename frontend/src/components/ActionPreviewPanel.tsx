/**
 * ActionPreviewPanel — Phase 13E Demo-mode Action Preview presentation.
 *
 * Phase 13E turns the existing visibly-disabled future-action affordances
 * into explainable, **non-executing** action previews. This component is
 * the presentation shell. All long-form preview content lives in
 * `frontend/src/data/actionPreviewAdapter.ts`; the panel maps over that
 * data and renders the selected preview.
 *
 * Strict Phase 13E preview-state boundary:
 *
 *  - The selected preview is held in **local, transient React state**
 *    via `useState<ActionPreviewId | null>`. No router. No Context. No
 *    persistence. No URL hash. No URL params. No browser History API
 *    manipulation. No `localStorage` / `sessionStorage`. No global
 *    preview / action state. No new Context providers.
 *  - The panel renders no fake loading spinner, no `setTimeout`-based
 *    fake workflow, no mock success state, no progress bar, and no
 *    "Submitted" / "Succeeded" / "Audit created" rendering. The user
 *    journey ends at an explicitly disabled execution boundary
 *    surfaced as a "Disabled in Demo mode" callout.
 *  - The "Preview action plan" buttons are real `<button>` elements (no
 *    `disabled`) — they open the inline preview panel. They are
 *    labelled as preview / intent inspection, NEVER as execution. They
 *    have NO ARIA labels claiming "Run" or "Execute".
 *  - The existing visibly-disabled action affordances
 *    (`DisabledFutureActionCard` / `DisabledFutureActionList`) are NOT
 *    modified by this component and remain real `<button disabled={true}>`
 *    elements with no `onClick`. The Phase 13E prompt is explicit: do
 *    not turn disabled buttons into active buttons.
 *
 * The "future Local-mode request shape" displayed for each preview is
 * a structured pseudo-DTO labelled "Future request shape — illustrative
 * only, not executable in Demo mode." Never executable code. Never a
 * shell command.
 */

import { useState } from "react";

import {
  ACTION_PREVIEW_PANEL_HEADER,
  ACTION_PREVIEWS,
  MODE_VS_SNAPSHOT_NOTE,
  OPERATING_MODES,
  SAFETY_LABELS,
  SYSTEM_CONSTRAINT_NOTICE,
  findActionPreview,
  type ActionPreview,
  type ActionPreviewContext,
  type ActionPreviewId,
} from "../data/actionPreviewAdapter";

import styles from "./ActionPreviewPanel.module.css";

/* ───────────────────────── component props ──────────────────────────── */

export interface ActionPreviewPanelProps {
  /** Which previews the host view should expose. Order is preserved. */
  readonly availablePreviews: readonly ActionPreviewId[];
  /** The host view context — descriptive only, no routing. */
  readonly view: ActionPreviewContext;
}

/* ───────────────────────── component itself ─────────────────────────── */

/**
 * Render the Demo-mode action-preview affordance for a host view. The
 * panel always renders its header (eyebrow, title, lede, safety pills,
 * the verbatim system constraint notice, and the operating-mode-vs-
 * snapshot framing) so a reviewer who has not opened any preview still
 * sees the boundary in plain English.
 */
export function ActionPreviewPanel({
  availablePreviews,
  view,
}: ActionPreviewPanelProps): JSX.Element {
  const [selected, setSelected] = useState<ActionPreviewId | null>(null);

  // Resolve the previews this host view actually exposes, preserving the
  // order the host view requested. Silently drop ids that aren't in the
  // canonical adapter list — that signals a definition error, not a
  // user-visible one.
  const previews: readonly ActionPreview[] = availablePreviews
    .map((id) => ACTION_PREVIEWS.find((p) => p.id === id))
    .filter((p): p is ActionPreview => p !== undefined);

  const selectedPreview = findActionPreview(selected);

  return (
    <section
      className={styles.section}
      aria-labelledby={`action-preview-${view.replace(/[^a-z]/gi, "-")}`}
    >
      <p className={styles.eyebrow}>{ACTION_PREVIEW_PANEL_HEADER.eyebrow}</p>
      <h3
        id={`action-preview-${view.replace(/[^a-z]/gi, "-")}`}
        className={styles.title}
      >
        {ACTION_PREVIEW_PANEL_HEADER.title}
      </h3>
      <p className={styles.lede}>{ACTION_PREVIEW_PANEL_HEADER.lede}</p>

      <ul className={styles.safetyPills} aria-label="Safety labels">
        {SAFETY_LABELS.map((label) => (
          <li key={label} className={styles.safetyPill}>
            {label}
          </li>
        ))}
      </ul>

      <p className={styles.constraintNotice}>{SYSTEM_CONSTRAINT_NOTICE}</p>
      <p className={styles.modeNote}>{MODE_VS_SNAPSHOT_NOTE}</p>

      {previews.length === 0 ? (
        <p className={styles.lede}>
          No action previews are surfaced in this view at this time.
        </p>
      ) : (
        <ul className={styles.previewList}>
          {previews.map((preview) => {
            const isSelected = selected === preview.id;
            return (
              <li
                key={preview.id}
                className={
                  isSelected
                    ? `${styles.previewItem} ${styles.previewItemSelected}`
                    : styles.previewItem
                }
              >
                <button
                  type="button"
                  className={styles.previewButton}
                  onClick={() => setSelected(isSelected ? null : preview.id)}
                  aria-expanded={isSelected}
                  aria-controls={`preview-detail-${preview.id}`}
                >
                  {isSelected ? "Close preview" : "Preview action plan"}
                </button>
                <span className={styles.previewLabel}>{preview.label}</span>
                <span className={styles.previewCategory}>
                  {preview.category}
                </span>
                {isSelected ? (
                  <button
                    type="button"
                    className={styles.closeButton}
                    onClick={() => setSelected(null)}
                    aria-label="Close action preview"
                  >
                    Close
                  </button>
                ) : null}
              </li>
            );
          })}
        </ul>
      )}

      {selectedPreview ? <PreviewDetail preview={selectedPreview} /> : null}

      <p className={styles.modeFooter}>
        Operating mode model:{" "}
        {OPERATING_MODES.map((mode, i) => (
          <span key={mode.id}>
            <strong>{mode.label}</strong> — {mode.status}
            {i < OPERATING_MODES.length - 1 ? " · " : ""}
          </span>
        ))}
      </p>
    </section>
  );
}

/* ───────────────────────── inline preview detail ────────────────────── */

interface PreviewDetailProps {
  readonly preview: ActionPreview;
}

/**
 * Render every field of an `ActionPreview` as a labelled field-row. No
 * tabs, no modals, no progressive disclosure beyond the
 * already-decided open/closed state — the reviewer reads the preview
 * top-to-bottom as a static dossier page.
 */
function PreviewDetail({ preview }: PreviewDetailProps): JSX.Element {
  const riskClass =
    preview.riskLevel === "High"
      ? styles.riskHigh
      : preview.riskLevel === "Medium"
        ? styles.riskMedium
        : styles.riskLow;

  return (
    <article
      id={`preview-detail-${preview.id}`}
      className={styles.detail}
      aria-label={`Action preview detail: ${preview.label}`}
    >
      <header className={styles.detailHeader}>
        <h4 className={styles.detailTitle}>{preview.label}</h4>
        <span className={styles.detailMeta}>
          Mode: {preview.currentMode} · Status: {preview.executionStatus} ·
          Category: {preview.category}
        </span>
      </header>

      <p className={styles.headline}>{preview.headlineSummary}</p>

      <Field label="Target">
        <p>{preview.target.targetContextLabel}</p>
        <ul>
          {preview.target.runId ? (
            <li>
              Run id: <code>{preview.target.runId}</code>
            </li>
          ) : null}
          {preview.target.stageId ? (
            <li>
              Stage id: <code>{preview.target.stageId}</code>
            </li>
          ) : null}
          {preview.target.governanceDecisionId ? (
            <li>
              Governance decision id:{" "}
              <code>{preview.target.governanceDecisionId}</code>
            </li>
          ) : null}
          {preview.target.failureQueueRunId ? (
            <li>
              Failure queue run id:{" "}
              <code>{preview.target.failureQueueRunId}</code>
            </li>
          ) : null}
          {preview.target.evidenceArtifactPath ? (
            <li>
              Evidence artifact path:{" "}
              <code>{preview.target.evidenceArtifactPath}</code>
            </li>
          ) : null}
          {preview.target.relatedDisabledActionId ? (
            <li>
              Related disabled action id:{" "}
              <code>{preview.target.relatedDisabledActionId}</code> (stays
              disabled in Demo mode)
            </li>
          ) : null}
        </ul>
      </Field>

      <Field label="Operator intent">
        <p>{preview.operatorIntent}</p>
      </Field>

      <Field label="Why blocked in Demo mode">
        <p>{preview.whyBlockedInDemo}</p>
      </Field>

      <Field label="Precondition checklist">
        <ul>
          {preview.preconditionChecklist.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </Field>

      <Field label="Evidence to inspect first">
        <ul>
          {preview.evidenceToInspect.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </Field>

      <Field label="Risk">
        <p>
          <span className={`${styles.riskBadge} ${riskClass}`}>
            {preview.riskLevel} risk
          </span>
          {preview.riskExplanation}
        </p>
      </Field>

      <Field label="Future Local-mode request shape">
        <p className={styles.requestShapeLabel}>
          Future request shape — illustrative only, not executable in Demo
          mode.
        </p>
        <pre className={styles.requestShape}>
          {JSON.stringify(preview.futureLocalRequestShape, null, 2)}
        </pre>
      </Field>

      <Field label="Cloud / Distributed considerations">
        <p>{preview.cloudDistributedConsiderations}</p>
      </Field>

      <Field label="Audit expectations">
        <p>{preview.auditExpectations}</p>
      </Field>

      <Field label="Failure behaviour expectation">
        <p>{preview.failureBehaviorExpectation}</p>
      </Field>

      <Field label="What remains disabled in Demo mode">
        <p className={styles.boundaryCallout}>{preview.whatRemainsDisabled}</p>
      </Field>

      <Field label="Related view">
        <p>
          {preview.relatedView}
          {preview.relatedRunId ? (
            <>
              {" "}
              · Related run id: <code>{preview.relatedRunId}</code>
            </>
          ) : null}
        </p>
      </Field>
    </article>
  );
}

/* ───────────────────────── small field-row helper ───────────────────── */

interface FieldProps {
  readonly label: string;
  readonly children: React.ReactNode;
}

function Field({ label, children }: FieldProps): JSX.Element {
  return (
    <div className={styles.fieldRow}>
      <div className={styles.fieldLabel}>{label}</div>
      <div className={styles.fieldValue}>{children}</div>
    </div>
  );
}
