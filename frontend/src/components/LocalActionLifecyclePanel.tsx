/**
 * LocalActionLifecyclePanel — read-only action lifecycle panel.
 *
 * This panel teaches the action lifecycle vocabulary and lets an operator
 * OBSERVE the state of an EXISTING action id (via ``GET /actions/{id}``). It is
 * read-only lifecycle observation, deliberately separate from submission:
 * submission is owned by {@link LocalRetrySubmitPanel} and the controlled
 * mutation module ``localBridgeActions.ts``. As of the locked Phase 13H.1 that
 * controlled retry submission is active; this panel still only reads.
 *
 * Hard boundaries:
 *  - it never creates an ``actionRequestId`` and never submits an action,
 *  - it stores nothing durably (the id field is transient session state),
 *  - it never fakes a successful job, never claims an export refresh happened,
 *    and never replaces or mutates the static read model itself (manual
 *    read-model reload is owned by the Phase 13H.3 StaticExportReloadPanel and
 *    its ``staticExportReload.ts`` adapter, never by this read-only panel).
 */

import {
  ACTION_LIFECYCLE_ORDER,
  type BridgeActionStatus,
  type BridgeProbe,
} from "../data/localBridgeTypes";
import { bridgeErrorLabel } from "./LocalBridgeStatusPanel";
import styles from "./LocalBridgeView.module.css";

export interface LocalActionLifecyclePanelProps {
  /** Operator-entered EXISTING action id to observe (transient). */
  actionRequestId: string;
  onActionRequestIdChange: (value: string) => void;
  lifecycleProbe: BridgeProbe<BridgeActionStatus>;
  probing: boolean;
  /** Look up the lifecycle of the already-entered existing id (read-only). */
  onLookup: () => void;
}

export function LocalActionLifecyclePanel(
  props: LocalActionLifecyclePanelProps,
): JSX.Element {
  const {
    actionRequestId,
    onActionRequestIdChange,
    lifecycleProbe,
    probing,
    onLookup,
  } = props;
  const hasId = actionRequestId.trim().length > 0;

  return (
    <section className={styles.panel} aria-label="Action lifecycle (read-only)">
      <h2>Action lifecycle (read-only)</h2>
      <p className={styles.panelNote}>
        The lifecycle states a controlled bridge action moves through. This panel
        observes an existing action id; it does not create or submit one.
      </p>

      <ul className={styles.lifecycleLegend} aria-label="Lifecycle vocabulary">
        {ACTION_LIFECYCLE_ORDER.map((state) => (
          <li key={state}>{state.replace("_", " ")}</li>
        ))}
      </ul>

      <div className={styles.controls}>
        <input
          className={styles.urlInput}
          type="text"
          aria-label="Existing actionRequestId to observe (transient, not stored)"
          placeholder="existing actionRequestId (read-only lookup)"
          value={actionRequestId}
          onChange={(e) => onActionRequestIdChange(e.target.value)}
          spellCheck={false}
        />
        <button
          type="button"
          className={styles.button}
          onClick={onLookup}
          disabled={probing || !hasId}
        >
          {probing ? "Looking up…" : "Look up lifecycle"}
        </button>
      </div>

      {!hasId && lifecycleProbe.phase === "idle" ? (
        <p className={styles.stateLine}>
          <span className={`${styles.badge} ${styles.badgeIdle}`}>read-only</span>{" "}
          No action id yet. Submit a controlled local retry above to populate one,
          or paste an existing actionRequestId to observe its lifecycle. This
          panel only observes — it never creates or submits an action.
        </p>
      ) : lifecycleProbe.phase === "ok" ? (
        renderLifecycle(lifecycleProbe.data)
      ) : lifecycleProbe.phase === "error" ? (
        <p className={styles.stateLine}>
          <span className={`${styles.badge} ${styles.badgeError}`}>
            lookup unavailable
          </span>{" "}
          {bridgeErrorLabel(lifecycleProbe.kind, lifecycleProbe.status)}
        </p>
      ) : lifecycleProbe.phase === "probing" ? (
        <p className={styles.stateLine}>
          <span className={`${styles.badge} ${styles.badgeIdle}`}>checking…</span>
        </p>
      ) : null}

      <div className={styles.deferred}>
        <strong>Lifecycle observation is separate from submission.</strong>
        <p style={{ margin: "0.4rem 0 0" }}>
          The Controlled local retry request panel above submits the action;
          this panel only reads its lifecycle. Acceptance is not success. A
          completed job is not a refreshed UI: the visible snapshot does not
          auto-update — reload it manually via the Static export snapshot panel
          below. Full Local mode and Cloud/Distributed mode are deferred.
        </p>
      </div>
    </section>
  );
}

function renderLifecycle(status: BridgeActionStatus): JSX.Element {
  const isComplete = status.status === "completed";
  return (
    <div>
      <p className={styles.stateLine}>
        Action <span className={styles.mono}>{status.action || "—"}</span> ·{" "}
        <span
          className={`${styles.badge} ${
            status.status === "failed" || status.status === "rejected"
              ? styles.badgeError
              : styles.badgeIdle
          }`}
        >
          {status.status.replace("_", " ")}
        </span>
      </p>
      <p className={styles.stateLine}>
        actionRequestId <span className={styles.mono}>{status.actionRequestId}</span>
        {status.jobId ? (
          <>
            {" "}· jobId <span className={styles.mono}>{status.jobId}</span>
          </>
        ) : null}
        {status.error ? (
          <>
            {" "}· error <span className={styles.mono}>{status.error}</span>
          </>
        ) : null}
      </p>
      {isComplete ? (
        <p className={styles.stateLine}>
          The job reports completed on the bridge. A completed job is not a
          refreshed UI — the static read model is unchanged until you manually
          reload the static export snapshot below.
        </p>
      ) : null}
    </div>
  );
}
