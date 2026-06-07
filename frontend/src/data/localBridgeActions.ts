/**
 * localBridgeActions — Phase 13H.1 controlled retry submission (the ONE POST).
 *
 * This module is the single, deliberately narrow frontend mutation path. It can
 * submit exactly one action type — ``retry_failed_stage`` — to the loopback
 * local bridge via ``POST /actions``, using the locked Phase 13F / 13G action
 * request DTO. It is kept separate from the GET-only read-only observability
 * client (``localBridgeClient.ts``) so the read-only surface stays provably
 * mutation-free.
 *
 * Hard boundaries:
 *  - **One action only.** ``RETRY_FAILED_STAGE`` is a hardcoded constant; there
 *    is no generic action runner, no arbitrary ``action`` input, and no
 *    free-form command / SQL / shell / filesystem-path field.
 *  - **Loopback only.** The same loopback URL guard as the read-only client.
 *  - **Acceptance is not success.** A ``202 Accepted`` is reported as accepted /
 *    queued with an ``actionRequestId`` to observe — never as a completed retry.
 *  - **Non-durable.** Nothing is persisted; the caller holds the returned id in
 *    transient React state only.
 *  - **No export refresh.** This module never touches the static export.
 */

import { isLoopbackBridgeUrl } from "./localBridgeClient";

/** The single action type this phase can submit. */
export const RETRY_FAILED_STAGE = "retry_failed_stage";

/** Bounded request deadline for the submit (ms). */
const SUBMIT_TIMEOUT_MS = 4000;

/** Demo-safe, workspace-relative defaults for the request envelope. */
const DEFAULT_WORKSPACE = {
  id: "ws-demo-0001",
  root: "storytime-workspace",
  slot: "active",
} as const;

/** The constrained operator intent the UI collects. */
export interface RetryFailedStageIntent {
  /** Pipeline run id of the failed run (contract field: target.runId). */
  readonly runId: string;
  /** Failed stage id (contract field: target.stageId). */
  readonly stageId: string;
  /** Human operator intent prose (contract field: operatorIntent). */
  readonly operatorIntent: string;
}

/** A validation error echoed by the bridge on a 422 rejection. */
export interface BridgeRejectionError {
  readonly code: string;
  readonly message: string;
  readonly field?: string;
}

export type RetrySubmitErrorKind =
  | "blockedNonLoopback"
  | "unavailable"
  | "timeout"
  | "originRejected"
  | "rejected"
  | "queueFull"
  | "httpError"
  | "malformed"
  | "unexpectedSchema"
  | "notAccepted";

/**
 * The result of a controlled submit. ``ok: true`` means the bridge ACCEPTED the
 * request (HTTP 202) — it does not mean the retry succeeded. The caller must
 * observe lifecycle status via ``GET /actions/{actionRequestId}``.
 */
export type RetrySubmitResult =
  | {
      readonly ok: true;
      readonly actionRequestId: string;
      readonly jobId: string;
      readonly status: string;
      readonly warnings: readonly string[];
      readonly exportRefreshRequired: boolean;
      readonly deduplicated: boolean;
    }
  | {
      readonly ok: false;
      readonly kind: RetrySubmitErrorKind;
      readonly status?: number;
      readonly errors?: readonly BridgeRejectionError[];
    };

let requestSeq = 0;

function slug(value: string): string {
  return value
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
}

/**
 * Build the typed, contract-shaped request body for ``retry_failed_stage``.
 * The ``action`` is fixed; ``idempotencyKey`` is derived deterministically from
 * the target so a double-click is de-duplicated by the bridge rather than
 * enqueuing a second execution.
 */
export function buildRetryFailedStageRequest(
  intent: RetryFailedStageIntent,
): Record<string, unknown> {
  requestSeq += 1;
  const runId = intent.runId.trim();
  const stageId = intent.stageId.trim();
  return {
    schemaVersion: "1.0",
    requestId: `req-ui-${Date.now()}-${requestSeq}`,
    mode: "local",
    action: RETRY_FAILED_STAGE,
    target: { runId, stageId },
    workspace: { ...DEFAULT_WORKSPACE },
    storageTarget: { type: "local-disk" },
    dryRun: false,
    requiresConfirmation: true,
    requestedAt: new Date().toISOString(),
    operatorIntent: intent.operatorIntent.trim(),
    preconditions: [],
    evidenceRefs: [],
    idempotencyKey: `idem-${slug(runId)}-${slug(stageId)}`,
    executionTiming: "async-long-running",
  };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

/**
 * Submit exactly one ``retry_failed_stage`` request to the loopback bridge.
 * Never throws: every failure maps to a typed {@link RetrySubmitResult} error
 * so the static demo never crashes. Must be invoked from an explicit user
 * event handler — never from a render-driven effect.
 */
export async function submitRetryFailedStage(
  baseUrl: string,
  intent: RetryFailedStageIntent,
): Promise<RetrySubmitResult> {
  if (!isLoopbackBridgeUrl(baseUrl)) {
    return { ok: false, kind: "blockedNonLoopback" };
  }

  const body = JSON.stringify(buildRetryFailedStageRequest(intent));
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), SUBMIT_TIMEOUT_MS);
  let response: Response;
  try {
    response = await fetch(`${baseUrl}/actions`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body,
      signal: controller.signal,
      mode: "cors",
      cache: "no-store",
    });
  } catch (cause) {
    clearTimeout(timer);
    if (cause instanceof DOMException && cause.name === "AbortError") {
      return { ok: false, kind: "timeout" };
    }
    return { ok: false, kind: "unavailable" };
  }
  clearTimeout(timer);

  if (response.status === 403) {
    return { ok: false, kind: "originRejected", status: 403 };
  }
  if (response.status === 429) {
    return { ok: false, kind: "queueFull", status: 429 };
  }

  let parsed: unknown;
  try {
    parsed = await response.json();
  } catch {
    return { ok: false, kind: "malformed" };
  }

  if (response.status === 422) {
    const errors =
      isRecord(parsed) && Array.isArray(parsed.errors)
        ? (parsed.errors.filter(isRecord) as unknown as BridgeRejectionError[])
        : [];
    return { ok: false, kind: "rejected", status: 422, errors };
  }
  if (!response.ok) {
    return { ok: false, kind: "httpError", status: response.status };
  }

  // 2xx. Only a 202-style accepted async response (with a handle) counts.
  if (!isRecord(parsed)) {
    return { ok: false, kind: "unexpectedSchema" };
  }
  const accepted = parsed.accepted === true;
  const actionRequestId =
    typeof parsed.actionRequestId === "string" ? parsed.actionRequestId : "";
  const jobId = typeof parsed.jobId === "string" ? parsed.jobId : "";
  const status = typeof parsed.status === "string" ? parsed.status : "";
  if (!accepted || actionRequestId.length === 0 || status === "rejected") {
    // e.g. a sync validated / not_implemented response: not an accepted retry.
    return { ok: false, kind: "notAccepted", status: response.status };
  }
  const warnings = Array.isArray(parsed.warnings)
    ? parsed.warnings.filter((w): w is string => typeof w === "string")
    : [];
  return {
    ok: true,
    actionRequestId,
    jobId,
    status,
    warnings,
    exportRefreshRequired: parsed.exportRefreshRequired === true,
    deduplicated: warnings.some((w) => w.toLowerCase().includes("duplicate")),
  };
}
