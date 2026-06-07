/**
 * localBridgeClient — Phase 13H read-only, loopback-only local-bridge client.
 *
 * This is the FIRST frontend network boundary in StoryTime, and it is
 * deliberately constrained:
 *
 *  - **Read-only.** Every call is an HTTP GET. There is no submission helper of
 *    any kind here; the single controlled submission path lives separately in
 *    ``localBridgeActions.ts`` (added in the locked Phase 13H.1), keeping this
 *    read-only surface provably mutation-free.
 *  - **Loopback-only.** A configured base URL is refused unless it is a
 *    loopback origin (``127.0.0.1`` / ``localhost`` / ``[::1]``). Non-loopback,
 *    LAN, public, or non-plain-HTTP URLs are blocked before any request is made.
 *  - **Native ``fetch`` only.** No third-party HTTP client and no
 *    streaming-socket APIs.
 *  - **Bounded.** Each request has a short abort deadline; there is no retry
 *    loop and no background polling. Callers drive every probe explicitly.
 *  - **Non-durable.** Nothing is persisted to browser storage; the base URL
 *    lives only in transient React state.
 *
 * Failures are returned as a safe, typed {@link BridgeResult}, never thrown to
 * the render tree, so the static demo degrades gracefully when no bridge is
 * running.
 */

import type {
  ActionLifecycleState,
  BridgeActionStatus,
  BridgeErrorKind,
  BridgeHealth,
  BridgeQueueSnapshot,
  BridgeReady,
  BridgeResult,
} from "./localBridgeTypes";

/** The bridge's loopback default (matches the Phase 13G CLI default port). */
export const DEFAULT_BRIDGE_BASE_URL = "http://127.0.0.1:8765";

/** Default bounded request deadline, in milliseconds. */
const DEFAULT_TIMEOUT_MS = 2500;

/** Hostnames that resolve to the local loopback interface only. */
const LOOPBACK_HOSTS: ReadonlySet<string> = new Set([
  "127.0.0.1",
  "localhost",
  "::1",
  "[::1]",
]);

/**
 * Return true only if ``raw`` is an ``http`` loopback origin. Everything else —
 * non-loopback, LAN ranges, public hosts, remote/cloud/provider URLs, and any
 * non-plain-HTTP scheme — is rejected. (We intentionally require plain ``http``
 * because the loopback bridge does not terminate TLS.)
 */
export function isLoopbackBridgeUrl(raw: string): boolean {
  let parsed: URL;
  try {
    parsed = new URL(raw);
  } catch {
    return false;
  }
  if (parsed.protocol !== "http:") {
    return false;
  }
  const host = parsed.hostname.toLowerCase();
  return LOOPBACK_HOSTS.has(host) || LOOPBACK_HOSTS.has(`[${host}]`);
}

/** Build a safe error result. */
function err<T>(kind: BridgeErrorKind, status?: number): BridgeResult<T> {
  return status === undefined ? { ok: false, kind } : { ok: false, kind, status };
}

/**
 * Perform one bounded, read-only GET and validate the JSON body via ``adapt``.
 * Never throws: connection failures, timeouts, 403s, non-OK statuses, invalid
 * JSON, and unexpected schemas all map to a typed {@link BridgeResult} error.
 */
async function getJson<T>(
  baseUrl: string,
  path: string,
  adapt: (raw: unknown) => T | null,
  timeoutMs: number = DEFAULT_TIMEOUT_MS,
): Promise<BridgeResult<T>> {
  if (!isLoopbackBridgeUrl(baseUrl)) {
    return err<T>("blockedNonLoopback");
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  let response: Response;
  try {
    response = await fetch(`${baseUrl}${path}`, {
      method: "GET",
      headers: { Accept: "application/json" },
      signal: controller.signal,
      // Cross-origin reads are subject to the bridge's strict Origin policy;
      // a rejected origin surfaces as a 403 handled below.
      mode: "cors",
      cache: "no-store",
    });
  } catch (cause) {
    clearTimeout(timer);
    if (cause instanceof DOMException && cause.name === "AbortError") {
      return err<T>("timeout");
    }
    return err<T>("unavailable");
  }
  clearTimeout(timer);

  if (response.status === 403) {
    return err<T>("originRejected", 403);
  }
  if (!response.ok) {
    return err<T>("httpError", response.status);
  }

  let body: unknown;
  try {
    body = await response.json();
  } catch {
    return err<T>("malformed");
  }

  const data = adapt(body);
  if (data === null) {
    return err<T>("unexpectedSchema");
  }
  return { ok: true, data };
}

/* ─────────────────── shape guards / adapters ─────────────────── */

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function isNumber(value: unknown): value is number {
  return typeof value === "number" && Number.isFinite(value);
}

function adaptHealth(raw: unknown): BridgeHealth | null {
  if (!isRecord(raw)) return null;
  if (typeof raw.status !== "string" || typeof raw.schemaVersion !== "string") {
    return null;
  }
  return { status: raw.status, schemaVersion: raw.schemaVersion };
}

function adaptReady(raw: unknown): BridgeReady | null {
  if (!isRecord(raw)) return null;
  if (
    typeof raw.status !== "string" ||
    typeof raw.schemaVersion !== "string" ||
    typeof raw.loopbackOnly !== "boolean"
  ) {
    return null;
  }
  const executable = Array.isArray(raw.executableActions)
    ? raw.executableActions.filter((a): a is string => typeof a === "string")
    : [];
  return {
    status: raw.status,
    schemaVersion: raw.schemaVersion,
    bridgeVersion: typeof raw.bridgeVersion === "string" ? raw.bridgeVersion : "",
    runtimeMode: typeof raw.runtimeMode === "string" ? raw.runtimeMode : "",
    loopbackOnly: raw.loopbackOnly,
    wildcardOriginAllowed: raw.wildcardOriginAllowed === true,
    workspaceConfigured: raw.workspaceConfigured === true,
    maxConcurrency: isNumber(raw.maxConcurrency) ? raw.maxConcurrency : 1,
    queueCapacity: isNumber(raw.queueCapacity) ? raw.queueCapacity : 0,
    executableActions: executable,
  };
}

/** The required numeric gauges that make a queue snapshot meaningful. */
const REQUIRED_QUEUE_FIELDS = [
  "queueDepth",
  "inFlightCount",
  "completedCount",
  "failedCount",
  "rejectedCount",
  "deadLetterCount",
  "oldestQueuedAgeSeconds",
  "longestInFlightAgeSeconds",
  "capacity",
  "saturationRatio",
  "maxConcurrency",
] as const;

export function adaptQueueSnapshot(raw: unknown): BridgeQueueSnapshot | null {
  if (!isRecord(raw)) return null;
  for (const field of REQUIRED_QUEUE_FIELDS) {
    if (!isNumber(raw[field])) return null;
  }
  return {
    queueDepth: raw.queueDepth as number,
    inFlightCount: raw.inFlightCount as number,
    completedCount: raw.completedCount as number,
    failedCount: raw.failedCount as number,
    rejectedCount: raw.rejectedCount as number,
    deadLetterCount: raw.deadLetterCount as number,
    oldestQueuedAgeSeconds: raw.oldestQueuedAgeSeconds as number,
    longestInFlightAgeSeconds: raw.longestInFlightAgeSeconds as number,
    capacity: raw.capacity as number,
    saturationRatio: raw.saturationRatio as number,
    maxConcurrency: raw.maxConcurrency as number,
  };
}

const KNOWN_LIFECYCLE_STATES: ReadonlySet<string> = new Set([
  "accepted",
  "queued",
  "running",
  "completed",
  "failed",
  "rejected",
  "not_implemented",
]);

/** Normalise any status string to a known lifecycle state or ``unknown``. */
export function normalizeLifecycleState(raw: unknown): ActionLifecycleState {
  if (typeof raw === "string" && KNOWN_LIFECYCLE_STATES.has(raw)) {
    return raw as ActionLifecycleState;
  }
  return "unknown";
}

export function adaptActionStatus(raw: unknown): BridgeActionStatus | null {
  if (!isRecord(raw)) return null;
  if (typeof raw.actionRequestId !== "string") return null;
  return {
    actionRequestId: raw.actionRequestId,
    jobId: typeof raw.jobId === "string" ? raw.jobId : "",
    requestId: typeof raw.requestId === "string" ? raw.requestId : "",
    action: typeof raw.action === "string" ? raw.action : "",
    status: normalizeLifecycleState(raw.status),
    error: typeof raw.error === "string" ? raw.error : null,
  };
}

/* ─────────────────── public read-only endpoints ─────────────────── */

export function fetchHealth(baseUrl: string): Promise<BridgeResult<BridgeHealth>> {
  return getJson(baseUrl, "/health", adaptHealth);
}

export function fetchReady(baseUrl: string): Promise<BridgeResult<BridgeReady>> {
  return getJson(baseUrl, "/ready", adaptReady);
}

export function fetchQueue(
  baseUrl: string,
): Promise<BridgeResult<BridgeQueueSnapshot>> {
  return getJson(baseUrl, "/queue", adaptQueueSnapshot);
}

/**
 * Read the lifecycle state of an EXISTING action id. The id must already exist
 * (operator-provided or a fixture) — this client never creates an id and never
 * submits an action.
 */
export function fetchActionStatus(
  baseUrl: string,
  actionRequestId: string,
): Promise<BridgeResult<BridgeActionStatus>> {
  const safeId = encodeURIComponent(actionRequestId);
  return getJson(baseUrl, `/actions/${safeId}`, adaptActionStatus);
}
