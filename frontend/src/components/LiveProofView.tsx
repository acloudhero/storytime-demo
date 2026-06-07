/**
 * LiveProofView — Phase 14B.1 hardened "Live Proof Loop" surface.
 *
 * Builds on the Phase 14A.1 live surface. It now lets the operator run
 * allowlisted scenarios (a success and two controlled, deterministic failure
 * scenarios), renders failure evidence clearly, and shows richer backend-owned
 * evidence labels. After a proof run it performs exactly ONE bounded, delayed
 * refresh of that run's detail (a single timeout) — there is no polling, no
 * interval, and no streaming socket transport. If that delayed refresh fails,
 * the run id stays visible and the operator is told to refresh manually.
 *
 * Discipline preserved from Phase 13/14A.1: the backend owns truth and durable
 * state; the browser only requests; loopback-only client; no browser durable
 * storage; static demo data is never presented as live.
 */

import { useCallback, useEffect, useRef, useState } from "react";
import {
  DEFAULT_LIVE_BASE_URL,
  fetchHealth,
  fetchRunDetail,
  fetchRuns,
  isLoopbackUrl,
  runProofFixture,
  type LiveHealth,
  type LiveResult,
  type LiveRunDetail,
  type LiveRunSummary,
} from "../data/liveProofClient";
import styles from "./LiveProofView.module.css";

type Connection =
  | { state: "idle" }
  | { state: "checking" }
  | { state: "connected"; health: LiveHealth }
  | { state: "unavailable"; reason: string };

interface ScenarioButton {
  id: string;
  label: string;
  kind: "success" | "failure";
}

// Fixed, safe allowlist of scenarios the UI may trigger. These ids are the
// only values ever sent to the backend; there is no free-form input.
const SCENARIOS: readonly ScenarioButton[] = [
  { id: "success", label: "Run success scenario", kind: "success" },
  { id: "governance_failure", label: "Run governance-failure scenario", kind: "failure" },
  {
    id: "artifact_validation_failure",
    label: "Run artifact-validation-failure scenario",
    kind: "failure",
  },
];

const REFRESH_DELAY_MS = 900;

function reasonFor(result: { kind: string; status?: number }): string {
  switch (result.kind) {
    case "blockedNonLoopback":
      return "base URL is not a loopback address";
    case "timeout":
      return "the backend did not respond in time";
    case "forbidden":
      return "the backend refused this origin (check the allowlist)";
    case "badStatus":
      return `the backend returned HTTP ${result.status ?? "?"}`;
    case "invalidBody":
      return "the backend returned an unexpected body";
    default:
      return "no local-live backend is reachable";
  }
}

export function LiveProofView(): JSX.Element {
  const [baseUrl, setBaseUrl] = useState(DEFAULT_LIVE_BASE_URL);
  const [conn, setConn] = useState<Connection>({ state: "idle" });
  const [runs, setRuns] = useState<LiveRunSummary[]>([]);
  const [selected, setSelected] = useState<LiveRunDetail | null>(null);
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);
  const [lastRefreshed, setLastRefreshed] = useState<string | null>(null);
  const refreshTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Clear any pending one-shot refresh timer on unmount.
  useEffect(() => {
    return () => {
      if (refreshTimer.current !== null) clearTimeout(refreshTimer.current);
    };
  }, []);

  const urlValid = isLoopbackUrl(baseUrl);

  const openRun = useCallback(
    async (runId: string): Promise<boolean> => {
      const detail: LiveResult<LiveRunDetail> = await fetchRunDetail(baseUrl, runId);
      if (detail.ok) {
        setSelected(detail.value);
        setLastRefreshed(new Date().toLocaleTimeString());
        return true;
      }
      return false;
    },
    [baseUrl],
  );

  const refresh = useCallback(async () => {
    if (!isLoopbackUrl(baseUrl)) {
      setConn({ state: "unavailable", reason: "base URL is not loopback" });
      return;
    }
    setConn({ state: "checking" });
    setNotice(null);
    const health = await fetchHealth(baseUrl);
    if (!health.ok) {
      setConn({ state: "unavailable", reason: reasonFor(health) });
      setRuns([]);
      setSelected(null);
      return;
    }
    setConn({ state: "connected", health: health.value });
    const list = await fetchRuns(baseUrl);
    setRuns(list.ok ? list.value : []);
    setLastRefreshed(new Date().toLocaleTimeString());
  }, [baseUrl]);

  const runScenario = useCallback(
    async (scenario: string) => {
      setBusy(true);
      setNotice(null);
      const result = await runProofFixture(baseUrl, scenario);
      setBusy(false);
      if (!result.ok) {
        setNotice(`Proof run rejected: ${reasonFor(result)}`);
        return;
      }
      const runId = result.value.runId;
      setNotice(
        `Backend accepted ${result.value.scenario} run ${runId} ` +
          `(${result.value.status}); a local worker will execute it.`,
      );
      await refresh();
      await openRun(runId);
      // Exactly one bounded, delayed refresh of this run — no polling. By the
      // time it fires the local worker has typically drained the queued item;
      // if the run is still queued/running, tell the operator to refresh.
      if (refreshTimer.current !== null) clearTimeout(refreshTimer.current);
      refreshTimer.current = setTimeout(() => {
        void fetchRunDetail(baseUrl, runId).then((detail) => {
          if (detail.ok) {
            setSelected(detail.value);
            setLastRefreshed(new Date().toLocaleTimeString());
            const st = detail.value.status;
            if (st === "queued" || st === "running") {
              setNotice(
                `Run ${runId} is ${st}; the local worker is draining it — ` +
                  `use Refresh to see the final state.`,
              );
            }
          } else {
            setNotice(
              `Run ${runId} is recorded; the delayed refresh failed — use Refresh to reload it.`,
            );
          }
        });
      }, REFRESH_DELAY_MS);
    },
    [baseUrl, refresh, openRun],
  );

  const connected = conn.state === "connected";

  return (
    <section className={styles.wrap} aria-labelledby="liveproof-title">
      <header className={styles.head}>
        <p className={styles.eyebrow}>Operator console · Phase 14B.1 · local live</p>
        <h1 id="liveproof-title" className={styles.title}>
          Live Proof Loop
        </h1>
        <p className={styles.lede}>
          This surface is not a static claim. It connects to a loopback backend,
          shows backend-owned durable state, and can trigger real, approved
          proof runs — including controlled, deterministic failure scenarios — so
          you can see not only that StoryTime succeeds, but that it produces
          intelligible, durable failure evidence. The browser only requests; the
          backend owns truth.
        </p>
      </header>

      {/* Connection / mode banner */}
      <div
        className={`${styles.modeBar} ${connected ? styles.modeLive : styles.modeStatic}`}
        role="status"
      >
        <span className={styles.modeDot} aria-hidden="true" />
        <span className={styles.modeLabel}>
          {connected
            ? "Local Live Connected — data below is backend-owned durable state"
            : conn.state === "checking"
              ? "Checking Local Live Backend…"
              : conn.state === "unavailable"
                ? "Backend Unavailable — no live data; the rest of the console is a Static Demo Snapshot"
                : "Static Demo Snapshot — connect to the local-live backend to see live data"}
        </span>
      </div>

      {/* Connection controls */}
      <div className={styles.controls}>
        <label className={styles.field}>
          <span className={styles.fieldLabel}>Local API base URL (loopback)</span>
          <input
            className={styles.input}
            value={baseUrl}
            spellCheck={false}
            onChange={(e) => setBaseUrl(e.target.value)}
            aria-invalid={!urlValid}
          />
        </label>
        <div className={styles.btnRow}>
          <button
            type="button"
            className={styles.btn}
            onClick={refresh}
            disabled={!urlValid || conn.state === "checking"}
          >
            {connected ? "Refresh" : "Connect"}
          </button>
          {SCENARIOS.map((s) => (
            <button
              key={s.id}
              type="button"
              className={s.kind === "failure" ? styles.btnWarn : styles.btnPrimary}
              onClick={() => runScenario(s.id)}
              disabled={!connected || busy}
              title="Runs an approved, local-only, deterministic scenario. No provider, no audio, no network."
            >
              {busy ? "Running…" : s.label}
            </button>
          ))}
        </div>
        {!urlValid && (
          <p className={styles.warn}>
            Base URL must be an http loopback origin (127.0.0.1 / localhost).
          </p>
        )}
        <p className={styles.refreshNote}>
          Last refreshed: {lastRefreshed ?? "—"} · manual refresh only (one bounded
          post-run refresh; no auto-polling).
        </p>
        {notice && <p className={styles.notice}>{notice}</p>}
      </div>

      {/* Health evidence */}
      {connected && (
        <dl className={styles.evidence}>
          <Evidence k="Backend status" v={conn.health.status} />
          <Evidence k="Mode" v={conn.health.mode} />
          <Evidence k="State owner" v={conn.health.stateOwner} />
          <Evidence k="Browser authority" v={conn.health.browserAuthority} />
          <Evidence k="Persistence" v={conn.health.persistence} />
          <Evidence k="Durable runs" v={String(conn.health.runCount)} />
        </dl>
      )}

      {/* Runs + detail */}
      {connected && (
        <div className={styles.grid}>
          <div className={styles.panel}>
            <h2 className={styles.h2}>Durable runs</h2>
            {runs.length === 0 ? (
              <p className={styles.muted}>
                No runs yet. Run a scenario above — the backend will persist it.
              </p>
            ) : (
              <ul className={styles.runList}>
                {runs.map((r) => (
                  <li key={r.runId}>
                    <button
                      type="button"
                      className={`${styles.runItem} ${
                        selected?.runId === r.runId ? styles.runItemActive : ""
                      }`}
                      onClick={() => openRun(r.runId)}
                    >
                      <code className={styles.mono}>{r.runId}</code>
                      <span className={statusClass(r.status, styles)}>{r.status}</span>
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className={styles.panel}>
            <h2 className={styles.h2}>Run detail</h2>
            {selected ? (
              <RunDetail detail={selected} lastRefreshed={lastRefreshed} />
            ) : (
              <p className={styles.muted}>Select a run to inspect its evidence.</p>
            )}
          </div>
        </div>
      )}

      <footer className={styles.why}>
        <h2 className={styles.h2}>Why this is not just a static page</h2>
        <ul className={styles.whyList}>
          <li>The run id, scenario, stages, artifacts, and events are created and persisted by the backend, not hardcoded in the browser.</li>
          <li>Requests are accepted then <strong>queued durably</strong> and drained by a <strong>local worker</strong> — execution is separated from the request and survives a server restart, but stays strictly local (not a cloud queue or distributed system).</li>
          <li>Failure scenarios produce a durable failed run with an intelligible, backend-recorded failure reason — not a frontend illusion.</li>
          <li>State is owned by the backend SQLite database; restart the local server and the run history (success and failure) is still here.</li>
          <li>The browser cannot submit arbitrary text, paths, providers, credentials, or failure messages; only allowlisted scenarios can be triggered.</li>
        </ul>
        <p className={styles.deferred}>
          Deferred (Phase 14C.2+ / 14D / 14E, NOT STARTED): contracts-as-built
          cloud/distributed seam baseline, object-storage adapter, durable
          retry/recovery, deeper observability, an auth boundary, and the
          provider-TTS / audio / RSS content arc.
        </p>
      </footer>
    </section>
  );
}

function Evidence({ k, v }: { k: string; v: string }): JSX.Element {
  return (
    <div className={styles.evRow}>
      <dt className={styles.evKey}>{k}</dt>
      <dd className={styles.evVal}>{v}</dd>
    </div>
  );
}

function statusClass(status: string, s: Record<string, string>): string {
  const base = s.pill ?? "";
  if (status === "completed") return `${base} ${s.pillOk}`;
  if (status === "failed") return `${base} ${s.pillFail}`;
  return `${base} ${s.pillNeutral}`;
}

function RunDetail({
  detail,
  lastRefreshed,
}: {
  detail: LiveRunDetail;
  lastRefreshed: string | null;
}): JSX.Element {
  const scenarioEvent = detail.events.find((e) => "scenario" in e.payload);
  const scenario =
    scenarioEvent && typeof scenarioEvent.payload.scenario === "string"
      ? scenarioEvent.payload.scenario
      : "—";
  const firstArtifact = detail.artifacts[0];
  return (
    <div className={styles.detail}>
      <dl className={styles.evidence}>
        <Evidence k="Run ID" v={detail.runId} />
        <Evidence k="Scenario" v={scenario} />
        <Evidence k="Status" v={detail.status} />
        <Evidence k="Execution" v="queued → local worker" />
        {detail.queue && (
          <Evidence
            k="Queue state"
            v={`${detail.queue.state} (attempt ${detail.queue.attempts})`}
          />
        )}
        <Evidence k="State owner" v="backend SQLite" />
        <Evidence k="Current stage" v={detail.currentStage} />
        <Evidence k="Event count" v={String(detail.events.length)} />
        <Evidence k="Persistence" v="survives server restart" />
        <Evidence k="Last refreshed" v={lastRefreshed ?? "—"} />
        {firstArtifact && (
          <>
            <Evidence k="Artifact key" v={firstArtifact.key} />
            <Evidence
              k="Artifact SHA-256"
              v={firstArtifact.sha256 ? `${firstArtifact.sha256.slice(0, 16)}…` : "—"}
            />
          </>
        )}
      </dl>

      {detail.failureReason && (
        <div className={styles.failurePanel} role="alert">
          <span className={styles.failureTitle}>Failure reason</span>
          <p className={styles.failureBody}>{detail.failureReason}</p>
        </div>
      )}

      <h3 className={styles.h3}>Stage timeline ({detail.stages.length})</h3>
      <ol className={styles.stageList}>
        {detail.stages.map((st, i) => (
          <li
            key={`${st.stageName}-${i}`}
            className={`${styles.stageItem} ${st.status === "failed" ? styles.stageFailed : ""}`}
          >
            <span className={styles.mono}>{st.stageName}</span>
            <span className={styles.stageStatus}>{st.status}</span>
          </li>
        ))}
      </ol>

      <h3 className={styles.h3}>Artifact evidence ({detail.artifacts.length})</h3>
      {detail.artifacts.length === 0 ? (
        <p className={styles.muted}>No artifacts recorded.</p>
      ) : (
        <ul className={styles.artifactList}>
          {detail.artifacts.map((a) => (
            <li key={a.key} className={styles.artifactItem}>
              <code className={styles.mono}>{a.name}</code>
              <span className={styles.artifactMeta}>
                {a.bytes !== null ? `${a.bytes} B` : "—"} ·{" "}
                {a.sha256 ? `sha256 ${a.sha256.slice(0, 12)}…` : "unhashed"}
              </span>
            </li>
          ))}
        </ul>
      )}

      <h3 className={styles.h3}>Audit events ({detail.events.length})</h3>
      <ul className={styles.eventList}>
        {detail.events.map((e, i) => (
          <li key={`${e.eventType}-${i}`} className={styles.eventItem}>
            <span className={styles.mono}>{e.eventType}</span>
            <span className={styles.eventTime}>{e.occurredAt}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
