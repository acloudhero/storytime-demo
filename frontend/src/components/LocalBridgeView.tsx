/**
 * LocalBridgeView — local-bridge view: read-only observability plus the single
 * controlled retry submission.
 *
 * The one nav-level container for the local bridge. It owns only transient,
 * in-memory React state — the loopback base URL, an existing action id to
 * observe, the four {@link BridgeProbe} results, and the constrained retry
 * intent / confirmation / submit view — and drives every probe and the one
 * submission from an explicit operator action. There is no background polling,
 * no retry loop, and no timer owned by this component (the read-only client and
 * the actions module each apply their own bounded abort deadline). Nothing is
 * persisted: a page reload resets the transient state, which is acceptable.
 *
 * Responsibilities are split across small panels so the boundary stays obvious:
 *  - {@link LocalBridgeStatusPanel} — read-only health / readiness status,
 *  - {@link LocalQueueStatusPanel} — read-only queue snapshot,
 *  - {@link LocalRetrySubmitPanel} — the ONLY submission affordance; it submits
 *    exactly one action (`retry_failed_stage`) via the controlled mutation
 *    module {@link submitRetryFailedStage} (`../data/localBridgeActions`),
 *  - {@link LocalActionLifecyclePanel} — read-only observation of an existing
 *    action's lifecycle; it never creates or submits an action,
 *  - {@link StaticExportReloadPanel} — Phase 13H.3 manual read-model reload; it
 *    owns its own transient snapshot and the only static-export fetch, kept
 *    separate from the bridge client and actions module.
 *
 * Read-only bridge observability uses the GET-only `../data/localBridgeClient`;
 * the single controlled mutation lives only in `../data/localBridgeActions`. As
 * of the locked Phase 13H.1, controlled retry submission is active. Acceptance
 * is not success and a completed job is not a refreshed UI: the visible
 * snapshot updates only when the operator manually reloads the static export
 * via the Phase 13H.3 {@link StaticExportReloadPanel} (the static-export fetch
 * lives in `../data/staticExportReload`, never in the bridge modules). The
 * browser stays non-durable.
 */

import { useEffect, useRef, useState } from "react";
import {
  DEFAULT_BRIDGE_BASE_URL,
  fetchActionStatus,
  fetchHealth,
  fetchQueue,
  fetchReady,
} from "../data/localBridgeClient";
import {
  RETRY_FAILED_STAGE,
  type RetryFailedStageIntent,
  submitRetryFailedStage,
} from "../data/localBridgeActions";
import type {
  BridgeActionStatus,
  BridgeHealth,
  BridgeProbe,
  BridgeQueueSnapshot,
  BridgeReady,
  BridgeResult,
} from "../data/localBridgeTypes";
import { LocalActionLifecyclePanel } from "./LocalActionLifecyclePanel";
import { LocalBridgeStatusPanel } from "./LocalBridgeStatusPanel";
import { LocalQueueStatusPanel } from "./LocalQueueStatusPanel";
import {
  LocalRetrySubmitPanel,
  type RetrySubmitView,
} from "./LocalRetrySubmitPanel";
import { StaticExportReloadPanel } from "./StaticExportReloadPanel";
import { OperatorWorkflow } from "./OperatorWorkflow";
import { TTSProofSummary } from "./TTSProofSummary";
import styles from "./LocalBridgeView.module.css";

const IDLE = { phase: "idle" } as const;

/** Map a {@link BridgeResult} into a renderable {@link BridgeProbe}. */
function toProbe<T>(result: BridgeResult<T>): BridgeProbe<T> {
  if (result.ok) {
    return { phase: "ok", data: result.data };
  }
  return result.status === undefined
    ? { phase: "error", kind: result.kind }
    : { phase: "error", kind: result.kind, status: result.status };
}

export function LocalBridgeView(): JSX.Element {
  const [baseUrl, setBaseUrl] = useState<string>(DEFAULT_BRIDGE_BASE_URL);
  const [actionId, setActionId] = useState<string>("");

  const [healthProbe, setHealthProbe] = useState<BridgeProbe<BridgeHealth>>(IDLE);
  const [readyProbe, setReadyProbe] = useState<BridgeProbe<BridgeReady>>(IDLE);
  const [queueProbe, setQueueProbe] =
    useState<BridgeProbe<BridgeQueueSnapshot>>(IDLE);
  const [lifecycleProbe, setLifecycleProbe] =
    useState<BridgeProbe<BridgeActionStatus>>(IDLE);

  const [statusBusy, setStatusBusy] = useState<boolean>(false);
  const [lifecycleBusy, setLifecycleBusy] = useState<boolean>(false);

  // Controlled retry submission — transient state only.
  const [intent, setIntent] = useState<RetryFailedStageIntent>({
    runId: "",
    stageId: "",
    operatorIntent: "",
  });
  const [confirmed, setConfirmed] = useState<boolean>(false);
  const [submit, setSubmit] = useState<RetrySubmitView>(IDLE);

  // The submit affordance is enabled only when a loopback bridge has reported
  // retry_failed_stage as an executable action.
  const retrySupported =
    readyProbe.phase === "ok" &&
    readyProbe.data.executableActions.includes(RETRY_FAILED_STAGE);

  // Guard against setState after unmount during an in-flight fetch.
  const mounted = useRef(true);
  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
    };
  }, []);

  async function checkBridge(): Promise<void> {
    setStatusBusy(true);
    setHealthProbe({ phase: "probing" });
    setReadyProbe({ phase: "probing" });
    setQueueProbe({ phase: "probing" });
    const [health, ready, queue] = await Promise.all([
      fetchHealth(baseUrl),
      fetchReady(baseUrl),
      fetchQueue(baseUrl),
    ]);
    if (!mounted.current) return;
    setHealthProbe(toProbe(health));
    setReadyProbe(toProbe(ready));
    setQueueProbe(toProbe(queue));
    setStatusBusy(false);
  }

  async function lookupAction(): Promise<void> {
    const id = actionId.trim();
    if (id.length === 0) return;
    setLifecycleBusy(true);
    setLifecycleProbe({ phase: "probing" });
    const result = await fetchActionStatus(baseUrl, id);
    if (!mounted.current) return;
    setLifecycleProbe(toProbe(result));
    setLifecycleBusy(false);
  }

  // Triggered strictly by the submit button's onClick — never an effect.
  async function submitRetry(): Promise<void> {
    if (!retrySupported || !confirmed) return;
    if (intent.runId.trim().length === 0 || intent.stageId.trim().length === 0) {
      return;
    }
    setSubmit({ phase: "submitting" });
    const result = await submitRetryFailedStage(baseUrl, intent);
    if (!mounted.current) return;
    if (result.ok) {
      setSubmit({
        phase: "accepted",
        actionRequestId: result.actionRequestId,
        jobId: result.jobId,
        status: result.status,
        deduplicated: result.deduplicated,
      });
      // Transient hand-off: populate the lifecycle id so the operator can
      // observe status. This is in-memory only; nothing is persisted.
      setActionId(result.actionRequestId);
    } else {
      setSubmit(
        result.status === undefined
          ? { phase: "error", kind: result.kind }
          : { phase: "error", kind: result.kind, status: result.status },
      );
    }
  }

  return (
    <div className={styles.view}>
      <div className={styles.intro}>
        <h1>Local bridge — observability &amp; controlled retry</h1>
        <p>
          The static demo is fully usable with no backend. This view lets the
          operator optionally observe a locally-running bridge over loopback —
          health, readiness, the queue snapshot, and an action’s lifecycle — and
          submit exactly one controlled action: a retry request for a failed
          stage.
        </p>
        <p>
          The Controlled local retry request below can submit only{" "}
          <span className={styles.mono}>retry_failed_stage</span> to the loopback
          bridge. Acceptance is not success, and a completed job is not a
          refreshed UI: the visible snapshot updates only when you manually
          reload the static export in the Static export snapshot panel below.
          The browser stays non-durable.
        </p>
      </div>

      <section className={styles.panel} aria-label="Local operator workflow">
        <h2>Operator workflow</h2>
        <p className={styles.panelNote}>
          The panels below follow this order. Each step is a separate, explicit
          operator action — nothing runs automatically, and the snapshot updates
          only when you manually reload it.
        </p>
        <OperatorWorkflow />
      </section>

      <LocalBridgeStatusPanel
        baseUrl={baseUrl}
        onBaseUrlChange={setBaseUrl}
        healthProbe={healthProbe}
        readyProbe={readyProbe}
        probing={statusBusy}
        onCheck={() => {
          void checkBridge();
        }}
      />

      <LocalQueueStatusPanel queueProbe={queueProbe} />

      <LocalRetrySubmitPanel
        intent={intent}
        onIntentChange={setIntent}
        confirmed={confirmed}
        onConfirmedChange={setConfirmed}
        retrySupported={retrySupported}
        submit={submit}
        onSubmit={() => {
          void submitRetry();
        }}
      />

      <LocalActionLifecyclePanel
        actionRequestId={actionId}
        onActionRequestIdChange={setActionId}
        lifecycleProbe={lifecycleProbe}
        probing={lifecycleBusy}
        onLookup={() => {
          void lookupAction();
        }}
      />

      <StaticExportReloadPanel />

      <TTSProofSummary />
    </div>
  );
}
