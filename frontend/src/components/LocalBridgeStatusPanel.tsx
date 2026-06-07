/**
 * LocalBridgeStatusPanel — Phase 13H read-only bridge health/readiness panel.
 *
 * Presentational only: it renders a transient {@link BridgeProbe} for the
 * bridge's health and readiness, plus a manual "Check" control and a
 * loopback-only base-URL field (transient, never persisted). It performs no
 * fetch itself and exposes no submission affordance — the single controlled
 * retry submission lives in {@link LocalRetrySubmitPanel} and
 * ``localBridgeActions.ts``, not here.
 */

import type {
  BridgeErrorKind,
  BridgeHealth,
  BridgeProbe,
  BridgeReady,
} from "../data/localBridgeTypes";
import styles from "./LocalBridgeView.module.css";

/** Human-readable, safe label for each bridge error outcome. */
export function bridgeErrorLabel(kind: BridgeErrorKind, status?: number): string {
  switch (kind) {
    case "blockedNonLoopback":
      return (
        "Refused: the configured URL is not loopback. The frontend only " +
        "contacts 127.0.0.1 / localhost."
      );
    case "unavailable":
      return "No local bridge detected. This is expected in the static demo.";
    case "timeout":
      return "The local bridge did not respond before the deadline.";
    case "originRejected":
      return (
        "The local bridge rejected this origin (403). Strict Origin policy is " +
        "working as designed; this read-only panel does not change CORS."
      );
    case "httpError":
      return `The local bridge returned an unexpected HTTP status (${status ?? "?"}).`;
    case "malformed":
      return "The local bridge response was not valid JSON.";
    case "unexpectedSchema":
      return "The local bridge response did not match the expected schema.";
    default:
      return "Unknown bridge state.";
  }
}

export interface LocalBridgeStatusPanelProps {
  baseUrl: string;
  onBaseUrlChange: (value: string) => void;
  healthProbe: BridgeProbe<BridgeHealth>;
  readyProbe: BridgeProbe<BridgeReady>;
  probing: boolean;
  onCheck: () => void;
}

function renderReady(ready: BridgeReady): JSX.Element {
  return (
    <div>
      <p className={styles.stateLine}>
        <span className={`${styles.badge} ${styles.badgeReady}`}>bridge ready</span>
      </p>
      <p className={styles.stateLine}>
        Runtime mode <span className={styles.mono}>{ready.runtimeMode || "—"}</span>,
        schema <span className={styles.mono}>{ready.schemaVersion}</span>, bridge
        version <span className={styles.mono}>{ready.bridgeVersion || "—"}</span>.
      </p>
      <p className={styles.stateLine}>
        Loopback-only: {ready.loopbackOnly ? "yes" : "no"} · wildcard origin
        allowed: {ready.wildcardOriginAllowed ? "yes" : "no"} · workspace
        configured: {ready.workspaceConfigured ? "yes" : "no"} · max concurrency:{" "}
        {ready.maxConcurrency} · queue capacity: {ready.queueCapacity}.
      </p>
      <p className={styles.stateLine}>
        Backend executable actions:{" "}
        <span className={styles.mono}>
          {ready.executableActions.length > 0
            ? ready.executableActions.join(", ")
            : "—"}
        </span>
        . The backend bridge supports controlled retry; the browser submits it
        only through the Controlled local retry request panel below.
      </p>
    </div>
  );
}

function renderProbe<T>(
  probe: BridgeProbe<T>,
  renderOk: (data: T) => JSX.Element,
  okFallbackLabel: string,
): JSX.Element {
  switch (probe.phase) {
    case "idle":
      return (
        <p className={styles.stateLine}>
          <span className={`${styles.badge} ${styles.badgeIdle}`}>not checked</span>{" "}
          The static demo contacts no backend. Press “Check local bridge” to probe
          the optional loopback bridge.
        </p>
      );
    case "probing":
      return (
        <p className={styles.stateLine}>
          <span className={`${styles.badge} ${styles.badgeIdle}`}>checking…</span>
        </p>
      );
    case "ok":
      return renderOk(probe.data) ?? <p>{okFallbackLabel}</p>;
    case "error":
      return (
        <p className={styles.stateLine}>
          <span className={`${styles.badge} ${styles.badgeError}`}>
            bridge unavailable / degraded
          </span>{" "}
          {bridgeErrorLabel(probe.kind, probe.status)}
        </p>
      );
    default:
      return <p>{okFallbackLabel}</p>;
  }
}

export function LocalBridgeStatusPanel(
  props: LocalBridgeStatusPanelProps,
): JSX.Element {
  const { baseUrl, onBaseUrlChange, healthProbe, readyProbe, probing, onCheck } =
    props;
  return (
    <section className={styles.panel} aria-label="Local bridge status">
      <h2>Local bridge status</h2>
      <p className={styles.panelNote}>
        Read-only local bridge observability over loopback. This status panel
        submits nothing; the only browser-initiated submission is the Controlled
        local retry request panel below.
      </p>

      <div className={styles.controls}>
        <input
          className={styles.urlInput}
          type="text"
          inputMode="url"
          aria-label="Local bridge loopback URL (transient, not stored)"
          value={baseUrl}
          onChange={(e) => onBaseUrlChange(e.target.value)}
          spellCheck={false}
        />
        <button
          type="button"
          className={styles.button}
          onClick={onCheck}
          disabled={probing}
        >
          {probing ? "Checking…" : "Check local bridge"}
        </button>
      </div>
      <p className={styles.panelNote}>
        Loopback only (127.0.0.1 / localhost). The URL is transient session
        state and is never stored in the browser.
      </p>

      <div>
        <strong>Health</strong>
        {renderProbe(
          healthProbe,
          (h: BridgeHealth) => (
            <p className={styles.stateLine}>
              <span className={`${styles.badge} ${styles.badgeReady}`}>
                bridge detected
              </span>{" "}
              health <span className={styles.mono}>{h.status}</span>, schema{" "}
              <span className={styles.mono}>{h.schemaVersion}</span>.
            </p>
          ),
          "Health unavailable.",
        )}
      </div>

      <div>
        <strong>Readiness</strong>
        {renderProbe(readyProbe, renderReady, "Readiness unavailable.")}
      </div>
    </section>
  );
}
