/**
 * LocalQueueStatusPanel — Phase 13H read-only queue snapshot panel.
 *
 * Renders the Phase 13G observable queue gauges from ``GET /queue`` as a plain,
 * dependency-free metric grid. There are no charts and no controls: queue
 * visibility is strictly read-only. When the bridge is absent it degrades to a
 * safe message and never breaks the demo.
 */

import type {
  BridgeProbe,
  BridgeQueueSnapshot,
} from "../data/localBridgeTypes";
import { bridgeErrorLabel } from "./LocalBridgeStatusPanel";
import styles from "./LocalBridgeView.module.css";

export interface LocalQueueStatusPanelProps {
  queueProbe: BridgeProbe<BridgeQueueSnapshot>;
}

interface Metric {
  readonly label: string;
  readonly value: number;
}

function metricsOf(snapshot: BridgeQueueSnapshot): readonly Metric[] {
  return [
    { label: "queue depth", value: snapshot.queueDepth },
    { label: "in flight", value: snapshot.inFlightCount },
    { label: "completed", value: snapshot.completedCount },
    { label: "failed", value: snapshot.failedCount },
    { label: "rejected", value: snapshot.rejectedCount },
    { label: "dead letter", value: snapshot.deadLetterCount },
    { label: "oldest queued (s)", value: snapshot.oldestQueuedAgeSeconds },
    { label: "longest in-flight (s)", value: snapshot.longestInFlightAgeSeconds },
    { label: "capacity", value: snapshot.capacity },
    { label: "saturation ratio", value: snapshot.saturationRatio },
    { label: "max concurrency", value: snapshot.maxConcurrency },
  ];
}

export function LocalQueueStatusPanel(
  props: LocalQueueStatusPanelProps,
): JSX.Element {
  const { queueProbe } = props;
  return (
    <section className={styles.panel} aria-label="Local queue snapshot">
      <h2>Queue snapshot</h2>
      <p className={styles.panelNote}>
        Read-only snapshot of the single-concurrency in-memory queue. Visibility
        only — the browser cannot enqueue, cancel, or drain work.
      </p>
      {queueProbe.phase === "ok" ? (
        <ul className={styles.metrics}>
          {metricsOf(queueProbe.data).map((m) => (
            <li key={m.label}>
              <span className={styles.metricLabel}>{m.label}</span>
              <span className={styles.metricValue}>{m.value}</span>
            </li>
          ))}
        </ul>
      ) : queueProbe.phase === "error" ? (
        <p className={styles.stateLine}>
          <span className={`${styles.badge} ${styles.badgeError}`}>
            queue unavailable
          </span>{" "}
          {bridgeErrorLabel(queueProbe.kind, queueProbe.status)}
        </p>
      ) : queueProbe.phase === "probing" ? (
        <p className={styles.stateLine}>
          <span className={`${styles.badge} ${styles.badgeIdle}`}>checking…</span>
        </p>
      ) : (
        <p className={styles.stateLine}>
          <span className={`${styles.badge} ${styles.badgeIdle}`}>not checked</span>{" "}
          The queue snapshot appears here after you check the local bridge.
        </p>
      )}
    </section>
  );
}
