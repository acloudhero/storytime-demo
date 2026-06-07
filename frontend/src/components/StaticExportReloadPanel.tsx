/**
 * StaticExportReloadPanel — Phase 13H.3 manual static export reload /
 * read-model replacement panel.
 *
 * This panel proves the browser can MANUALLY replace its visible read model
 * from an authoritative static export snapshot while staying non-durable. It
 * owns a narrow, transient in-memory read model (seeded from the bundled static
 * import) and a single operator-triggered reload affordance. There is no
 * automatic reload on mount, no effect-driven reload, no polling, no interval,
 * no live socket, and no server-sent-events stream — the reload runs only from
 * the button's ``onClick``.
 *
 * Replacement is all-or-nothing and is delegated to the separate
 * {@link reloadStaticExport} adapter (``../data/staticExportReload``): on a
 * valid fetched export the held snapshot is replaced wholesale; on any
 * failure the previous snapshot is retained and a typed error is shown. The
 * snapshot lives only in React state — nothing is written to any browser
 * durable store (no web storage, client-side database, cookies, or
 * URL-history state). A page reload returns to the bundled snapshot unless the
 * served static file itself changed.
 *
 * It is deliberately decoupled from the local bridge: manual export reload and
 * the Phase 13H.1 controlled retry submission are separate operator actions.
 * Reloading the snapshot does not prove a retry succeeded, and a completed job
 * does not automatically update this snapshot.
 */

import { useState } from "react";
import {
  DEMO_FAILURE_QUEUE,
  DEMO_PROJECT,
  DEMO_RUN_DETAILS,
  EXPORT_META,
} from "../data/adapter";
import {
  reloadStaticExport,
  type ExportSnapshotReadModel,
} from "../data/staticExportReload";
import styles from "./LocalBridgeView.module.css";

/** Where the currently-held in-memory snapshot came from. */
type SnapshotSource = "bundled" | "reloaded" | "retained-after-failure";

/** The reload lifecycle status. */
type ReloadStatus = "idle" | "loading" | "loaded" | "failed";

/**
 * The initial in-memory read model, seeded from the bundled static import. This
 * is the build-time snapshot the static demo already ships with; a manual
 * reload may later replace it with a freshly fetched snapshot.
 */
const BUNDLED_READ_MODEL: ExportSnapshotReadModel = {
  schemaVersion: EXPORT_META.schemaVersion,
  generatedBy: EXPORT_META.generatedBy,
  exportKind: EXPORT_META.exportKind,
  projectName: DEMO_PROJECT.name,
  projectTagline: DEMO_PROJECT.tagline ?? null,
  currentPhase: DEMO_PROJECT.currentPhase ?? null,
  runCount: DEMO_RUN_DETAILS.length,
  failureQueueCount: DEMO_FAILURE_QUEUE.length,
  runLabels: DEMO_RUN_DETAILS.map((run) => run.label),
};

function sourceLabel(source: SnapshotSource): string {
  switch (source) {
    case "bundled":
      return "Bundled / static import";
    case "reloaded":
      return "Manually reloaded static export";
    case "retained-after-failure":
      return "Reload failed — previous snapshot retained";
  }
}

function statusBadgeClass(status: ReloadStatus): string {
  if (status === "failed") return styles.badgeError ?? "";
  if (status === "loaded") return styles.badgeReady ?? "";
  return styles.badgeIdle ?? "";
}

export function StaticExportReloadPanel(): JSX.Element {
  // The replaceable read model and its provenance — transient, in-memory only.
  const [readModel, setReadModel] =
    useState<ExportSnapshotReadModel>(BUNDLED_READ_MODEL);
  const [source, setSource] = useState<SnapshotSource>("bundled");
  const [status, setStatus] = useState<ReloadStatus>("idle");
  const [loadedAt, setLoadedAt] = useState<Date | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Triggered strictly by the reload button's onClick — never from an effect,
  // an interval, a socket, or module load.
  async function handleReload(): Promise<void> {
    setStatus("loading");
    setError(null);
    const result = await reloadStaticExport();
    if (result.ok) {
      // All-or-nothing replacement: swap the whole snapshot for the validated
      // one. No partial merge, no optimistic mutation.
      setReadModel(result.readModel);
      setSource("reloaded");
      setStatus("loaded");
      setLoadedAt(new Date());
    } else {
      // Retain the previous snapshot; surface a typed, safe message only.
      setSource("retained-after-failure");
      setStatus("failed");
      setError(result.message);
    }
  }

  const busy = status === "loading";

  return (
    <section
      className={styles.panel}
      aria-label="Static export snapshot (read-model reload)"
    >
      <h2>Static export snapshot</h2>
      <p className={styles.panelNote}>
        The visible data is a read model loaded from the committed static export
        snapshot. A completed bridge job does not automatically update it. You
        can manually reload the latest static export to replace this snapshot —
        validated and all-or-nothing.
      </p>

      <div className={styles.controls}>
        <button
          type="button"
          className={styles.button}
          onClick={() => {
            void handleReload();
          }}
          disabled={busy}
        >
          {busy ? "Reloading…" : "Reload static export snapshot"}
        </button>
        <span className={`${styles.badge} ${statusBadgeClass(status)}`}>
          {status}
        </span>
      </div>

      <p className={styles.stateLine}>
        Source:{" "}
        <span className={styles.mono}>{sourceLabel(source)}</span>
        {loadedAt ? (
          <>
            {" "}
            · reloaded at{" "}
            <span className={styles.mono}>{loadedAt.toLocaleString()}</span>
          </>
        ) : (
          <> · using the snapshot bundled at build time</>
        )}
      </p>

      {status === "failed" && error ? (
        <p className={styles.warn} role="status">
          {error} The previously loaded snapshot is still shown below.
        </p>
      ) : null}

      <ul className={styles.metrics} aria-label="Current snapshot metadata">
        <li>
          <span className={styles.metricLabel}>schema version</span>
          <span className={styles.metricValue}>{readModel.schemaVersion}</span>
        </li>
        <li>
          <span className={styles.metricLabel}>export kind</span>
          <span className={styles.metricValue}>{readModel.exportKind}</span>
        </li>
        <li>
          <span className={styles.metricLabel}>generated by</span>
          <span className={styles.metricValue}>{readModel.generatedBy}</span>
        </li>
        <li>
          <span className={styles.metricLabel}>runs in snapshot</span>
          <span className={styles.metricValue}>{readModel.runCount}</span>
        </li>
        <li>
          <span className={styles.metricLabel}>failure-queue items</span>
          <span className={styles.metricValue}>
            {readModel.failureQueueCount}
          </span>
        </li>
        <li>
          <span className={styles.metricLabel}>project</span>
          <span className={styles.metricValue}>{readModel.projectName}</span>
        </li>
      </ul>

      <p className={styles.stateLine}>
        Current phase in snapshot:{" "}
        <span className={styles.mono}>{readModel.currentPhase ?? "—"}</span>
        {readModel.runLabels.length > 0 ? (
          <>
            {" "}
            · runs:{" "}
            <span className={styles.mono}>
              {readModel.runLabels.join(", ")}
            </span>
          </>
        ) : null}
      </p>

      <div className={styles.deferred}>
        <strong>Manual reload replaces the visible snapshot only.</strong>
        <p style={{ margin: "0.4rem 0 0" }}>
          Reload fetches only the committed static export and replaces this
          in-memory read model after the fetched export validates; an invalid or
          unreachable export is rejected and the previous snapshot is retained.
          This is not a live sync and not a backend refresh: a reload does not
          prove a retry succeeded, and the snapshot is not durable — a page
          reload returns to the bundled snapshot unless the served static file
          changed. Full Local mode and Cloud/Distributed mode remain deferred.
        </p>
      </div>
    </section>
  );
}
