/**
 * DisabledFutureActionCard — the Phase 13D.1 reusable disabled-action display.
 *
 * StoryTime's operator GUI surfaces future operator actions (retry, re-run,
 * review-decision recording, etc.) as **visibly-disabled** affordances. They
 * exist so a reviewer can see the intended workflow shape, but they cannot
 * be invoked: this is a static / read-only frontend, and no mutation handler
 * exists anywhere. Before Phase 13D.1 each consuming view rendered its own
 * near-identical disabled-action `<div>`, leading to duplication and risk of
 * drift (one view could accidentally make an action look enabled).
 *
 * This component standardizes that rendering across views:
 *
 *  - The action is rendered as a **real** `<button disabled={true}>` element.
 *    No `onClick` handler is attached — not even a no-op or `console.log`.
 *    The browser disables the button natively; the DOM tells assistive
 *    technology the control is unavailable. No `aria-disabled` lie, no
 *    `cursor: pointer`, no hover style that suggests it could be clicked.
 *  - The `label`, `disabledReason`, `enabledByPhase`, optional `safetyNote`,
 *    and (when relevant) the "mutation" pill are rendered as subtext adjacent
 *    to the disabled button — not as fake active controls.
 *  - The component never accepts an action-execution callback. It is a pure
 *    presentational primitive. When Phase 13E (or later) eventually introduces
 *    real action handlers behind an explicit safety gate, those will live in
 *    a separate component or a deliberately wrapping component — not by
 *    silently passing handlers through this one.
 *
 * Harmless navigation / inspection affordances (e.g. "Inspect this run in
 * Pipeline Run Detail →") live in the consuming view directly, NOT in this
 * component. Mixing the two would obscure the static / no-mutation boundary.
 */

import type { DisabledFutureAction } from "../types/storytime";
import styles from "./DisabledFutureActionCard.module.css";

/**
 * Derive a short, conservative safety note from a disabled action. The Phase
 * 13C/13D data model does not carry a per-action `safetyNote`, so we surface
 * a stable string keyed off the `isMutation` flag. This is descriptive copy,
 * not a behavioural claim — and it remains an honest read-only fallback.
 */
function deriveSafetyNote(action: DisabledFutureAction): string {
  if (action.isMutation) {
    return (
      "Backend mutation — held behind an explicit safety review until " +
      action.enabledByPhase +
      "."
    );
  }
  return (
    "Operator review affordance — surfaced read-only until " +
    action.enabledByPhase +
    " gates the action behind explicit review."
  );
}

/* ─────────────────── single-card component ─────────────────── */

export interface DisabledFutureActionCardProps {
  action: DisabledFutureAction;
  /** Optional explicit safety note; defaults to the derived note. */
  safetyNote?: string;
}

/**
 * Render a single disabled future action as a real `<button disabled={true}>`
 * with adjacent metadata. This component never accepts an `onClick` or any
 * other action-execution prop.
 */
export function DisabledFutureActionCard({
  action,
  safetyNote,
}: DisabledFutureActionCardProps): JSX.Element {
  const note = safetyNote ?? deriveSafetyNote(action);
  return (
    <article className={styles.card}>
      <div className={styles.head}>
        {/*
          Intentionally no onClick. The button is disabled at the DOM level so
          the browser refuses to activate it. There is no "click is a no-op"
          path here, because no click path exists at all.
        */}
        <button
          type="button"
          className={styles.button}
          disabled={true}
        >
          {action.label}
        </button>
        <span className={`${styles.pill} ${styles.pillDisabled}`}>
          disabled
        </span>
        {action.isMutation ? (
          <span className={`${styles.pill} ${styles.pillMutation}`}>
            mutation
          </span>
        ) : null}
        <span className={styles.enabledBy}>
          enabled by {action.enabledByPhase}
        </span>
      </div>
      <p className={styles.reason}>{action.disabledReason}</p>
      <p className={styles.safety}>{note}</p>
    </article>
  );
}

/* ─────────────────── list wrapper component ─────────────────── */

export interface DisabledFutureActionListProps {
  actions: readonly DisabledFutureAction[];
  /**
   * Optional heading rendered above the list. Pass `undefined` to let the
   * consuming view render its own heading (the existing Phase 13D Governance /
   * Safety and Failure / Recovery views do this).
   */
  heading?: string;
  /**
   * Optional preface rendered above the list. Useful for views that want a
   * single explanatory paragraph (e.g. the Evidence / Validation view).
   */
  preface?: string;
  /** Optional safety-note overrides keyed by action id. */
  safetyNotesById?: Record<string, string>;
  /**
   * Optional empty-state message shown when `actions` is empty. If omitted,
   * the list renders nothing in that case.
   */
  emptyMessage?: string;
}

export function DisabledFutureActionList({
  actions,
  heading,
  preface,
  safetyNotesById,
  emptyMessage,
}: DisabledFutureActionListProps): JSX.Element | null {
  if (actions.length === 0) {
    if (!emptyMessage) {
      return null;
    }
    return (
      <div className={styles.empty}>
        <p>{emptyMessage}</p>
      </div>
    );
  }
  return (
    <div className={styles.list}>
      {heading ? <h4 className={styles.heading}>{heading}</h4> : null}
      {preface ? <p className={styles.preface}>{preface}</p> : null}
      <div className={styles.cards}>
        {actions.map((action) => (
          <DisabledFutureActionCard
            key={action.id}
            action={action}
            safetyNote={safetyNotesById?.[action.id]}
          />
        ))}
      </div>
    </div>
  );
}
