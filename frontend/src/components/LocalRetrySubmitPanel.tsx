/**
 * LocalRetrySubmitPanel — Phase 13H.1 controlled local retry request.
 *
 * The single, deliberately constrained browser-initiated mutation affordance.
 * It collects a constrained operator intent (run id, failed stage id, reason),
 * requires an explicit confirmation, and submits exactly one
 * ``retry_failed_stage`` action to the loopback bridge — only when the bridge
 * has reported it as executable. Submission is triggered strictly by the
 * button's ``onClick`` (never a render-driven effect), so React Strict Mode
 * cannot double-submit.
 *
 * It deliberately does NOT: expose an arbitrary action type, expose a
 * command / SQL / path field, refresh the static export, replace the read
 * model, or persist anything. Acceptance is not success.
 */

import type { RetryFailedStageIntent } from "../data/localBridgeActions";
import styles from "./LocalBridgeView.module.css";

/** Transient submit state held by the orchestrator (in-memory only). */
export type RetrySubmitView =
  | { readonly phase: "idle" }
  | { readonly phase: "submitting" }
  | {
      readonly phase: "accepted";
      readonly actionRequestId: string;
      readonly jobId: string;
      readonly status: string;
      readonly deduplicated: boolean;
    }
  | {
      readonly phase: "error";
      readonly kind: string;
      readonly status?: number;
      readonly detail?: string;
    };

export interface LocalRetrySubmitPanelProps {
  intent: RetryFailedStageIntent;
  onIntentChange: (intent: RetryFailedStageIntent) => void;
  confirmed: boolean;
  onConfirmedChange: (value: boolean) => void;
  /** True only when a loopback bridge reported retry_failed_stage executable. */
  retrySupported: boolean;
  submit: RetrySubmitView;
  onSubmit: () => void;
}

function retrySubmitErrorLabel(kind: string, status?: number): string {
  switch (kind) {
    case "blockedNonLoopback":
      return "Refused: submission targets the loopback bridge only.";
    case "unavailable":
      return "No local bridge detected. The static demo remains usable.";
    case "timeout":
      return "The local bridge did not respond before the deadline.";
    case "originRejected":
      return "The local bridge rejected this origin (403). CORS is unchanged.";
    case "rejected":
      return "The local bridge rejected the request (422 validation).";
    case "queueFull":
      return "The local bridge queue is full (429). Try again shortly.";
    case "notAccepted":
      return "The bridge did not return an accepted async handle.";
    case "malformed":
      return "The local bridge response was not valid JSON.";
    case "unexpectedSchema":
      return "The local bridge response did not match the expected schema.";
    default:
      return `The submission failed (${status ?? "?"}).`;
  }
}

export function LocalRetrySubmitPanel(
  props: LocalRetrySubmitPanelProps,
): JSX.Element {
  const {
    intent,
    onIntentChange,
    confirmed,
    onConfirmedChange,
    retrySupported,
    submit,
    onSubmit,
  } = props;

  const fieldsValid =
    intent.runId.trim().length > 0 && intent.stageId.trim().length > 0;
  const submitting = submit.phase === "submitting";
  const canSubmit = retrySupported && fieldsValid && confirmed && !submitting;

  return (
    <section className={styles.panel} aria-label="Controlled local retry request">
      <h2>Controlled local retry request</h2>
      <p className={styles.panelNote}>
        An intentional action request. Only <span className={styles.mono}>retry_failed_stage</span>{" "}
        is supported; the request goes to the loopback local bridge. Acceptance
        is not success, and the static export is not automatically refreshed.
      </p>

      <div className={styles.field}>
        <label className={styles.fieldLabel} htmlFor="retry-run-id">
          Pipeline run id (target.runId)
        </label>
        <input
          id="retry-run-id"
          className={styles.urlInput}
          type="text"
          spellCheck={false}
          placeholder="run-2026-0520-review"
          value={intent.runId}
          onChange={(e) => onIntentChange({ ...intent, runId: e.target.value })}
        />
      </div>

      <div className={styles.field}>
        <label className={styles.fieldLabel} htmlFor="retry-stage-id">
          Failed stage id (target.stageId)
        </label>
        <input
          id="retry-stage-id"
          className={styles.urlInput}
          type="text"
          spellCheck={false}
          placeholder="run-2026-0520-review:governance-gate"
          value={intent.stageId}
          onChange={(e) => onIntentChange({ ...intent, stageId: e.target.value })}
        />
      </div>

      <div className={styles.field}>
        <label className={styles.fieldLabel} htmlFor="retry-intent">
          Operator intent / reason
        </label>
        <textarea
          id="retry-intent"
          className={styles.textarea}
          placeholder="Why this stage is safe to retry now…"
          value={intent.operatorIntent}
          onChange={(e) =>
            onIntentChange({ ...intent, operatorIntent: e.target.value })
          }
        />
      </div>

      <label className={styles.checkboxRow}>
        <input
          type="checkbox"
          checked={confirmed}
          onChange={(e) => onConfirmedChange(e.target.checked)}
        />
        <span>I understand this requests a local retry on the running bridge.</span>
      </label>

      {!retrySupported ? (
        <p className={styles.panelNote}>
          Submission is available only when a loopback bridge reports{" "}
          <span className={styles.mono}>retry_failed_stage</span> as executable.
          Check the local bridge status above first.
        </p>
      ) : null}

      <button
        type="button"
        className={styles.button}
        onClick={onSubmit}
        disabled={!canSubmit}
      >
        {submitting ? "Submitting…" : "Request local retry"}
      </button>

      {submit.phase === "accepted" ? (
        <div className={styles.warn} style={{ marginTop: "0.75rem" }}>
          <strong>Accepted by local bridge — acceptance is not success.</strong>
          <p style={{ margin: "0.4rem 0 0" }}>
            The bridge {submit.deduplicated ? "de-duplicated this request and " : ""}
            returned status <span className={styles.mono}>{submit.status}</span>.
            actionRequestId <span className={styles.mono}>{submit.actionRequestId}</span>
            {submit.jobId ? (
              <>
                {" "}· jobId <span className={styles.mono}>{submit.jobId}</span>
              </>
            ) : null}
            . This id has been placed in the lifecycle panel below so you can
            observe its status. A completed job is not a refreshed UI; static
            export refresh remains deferred and the visible demo data may be
            unchanged.
          </p>
        </div>
      ) : submit.phase === "error" ? (
        <p className={styles.stateLine} style={{ marginTop: "0.5rem" }}>
          <span className={`${styles.badge} ${styles.badgeError}`}>not accepted</span>{" "}
          {retrySubmitErrorLabel(submit.kind, submit.status)}
          {submit.detail ? <> {submit.detail}</> : null}
        </p>
      ) : null}
    </section>
  );
}
