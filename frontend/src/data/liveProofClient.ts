/**
 * liveProofClient — Phase 14A.1 loopback-only client for the local-live API.
 *
 * This talks to the `storytime local-live` backend service (see
 * `src/storytime/local_live/server.py`). It mirrors the Phase 13H local-bridge
 * client discipline:
 *
 *  - **Loopback-only.** A base URL is refused unless it is an `http` loopback
 *    origin (`127.0.0.1` / `localhost` / `[::1]`). LAN, public, cloud, and
 *    non-plain-HTTP URLs are blocked before any request is made.
 *  - **Native `fetch` only.** No third-party HTTP client and no streaming
 *    socket transports.
 *  - **Bounded.** Each request has a short abort deadline; there is no retry
 *    loop and no background polling. The operator drives every refresh.
 *  - **Non-durable.** Nothing is written to any browser durable-storage API;
 *    the base URL lives only in transient React state.
 *  - Exactly one mutating call exists: `runProofFixture`, which POSTs an empty
 *    or `{fixture}` body to the controlled `/api/proof-runs` endpoint. It never
 *    sends free text, paths, URLs, providers, or credentials.
 *
 * Failures are returned as typed results, never thrown into the render tree.
 */

/** Loopback default; matches the `storytime local-live` CLI default port. */
export const DEFAULT_LIVE_BASE_URL = "http://127.0.0.1:8770";

const DEFAULT_TIMEOUT_MS = 2500;

const LOOPBACK_HOSTS: ReadonlySet<string> = new Set([
  "127.0.0.1",
  "localhost",
  "::1",
  "[::1]",
]);

export interface LiveHealth {
  status: string;
  mode: string;
  loopbackOnly: boolean;
  stateOwner: string;
  dbPresent: boolean;
  runCount: number;
  browserAuthority: string;
  persistence: string;
  scenarios?: string[];
}

export interface LiveStage {
  stageName: string;
  status: string;
  startedAt: string;
  endedAt: string | null;
  errorKind: string | null;
  errorMessage: string | null;
}

export interface LiveArtifact {
  stageName: string;
  key: string;
  name: string;
  recordedAt: string;
  sha256: string | null;
  bytes: number | null;
}

export interface LiveEvent {
  occurredAt: string;
  eventType: string;
  payload: Record<string, unknown>;
}

export interface LiveWorkItem {
  workId: string;
  state: string;
  scenario: string;
  attempts: number;
  enqueuedAt: string;
  updatedAt: string;
}

export interface LiveRunSummary {
  runId: string;
  status: string;
  currentStage: string;
  createdAt: string;
  updatedAt: string;
  stageCount: number;
  artifactCount: number;
  eventCount: number;
  queue?: LiveWorkItem | null;
}

export interface LiveRunDetail extends LiveRunSummary {
  stages: LiveStage[];
  artifacts: LiveArtifact[];
  events: LiveEvent[];
  failureReason: string | null;
}

export type LiveErrorKind =
  | "blockedNonLoopback"
  | "unreachable"
  | "timeout"
  | "forbidden"
  | "badStatus"
  | "invalidBody";

export type LiveResult<T> =
  | { ok: true; value: T }
  | { ok: false; kind: LiveErrorKind; status?: number; message?: string };

export function isLoopbackUrl(raw: string): boolean {
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

function fail<T>(
  kind: LiveErrorKind,
  status?: number,
  message?: string,
): LiveResult<T> {
  return { ok: false, kind, status, message };
}

async function request<T>(
  baseUrl: string,
  path: string,
  init: RequestInit,
  timeoutMs = DEFAULT_TIMEOUT_MS,
): Promise<LiveResult<T>> {
  if (!isLoopbackUrl(baseUrl)) {
    return fail<T>("blockedNonLoopback");
  }
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  let resp: Response;
  try {
    resp = await fetch(`${baseUrl}${path}`, {
      ...init,
      signal: controller.signal,
      // The backend enforces a strict origin allowlist; we never send creds.
      credentials: "omit",
      mode: "cors",
    });
  } catch (e) {
    clearTimeout(timer);
    if (e instanceof DOMException && e.name === "AbortError") {
      return fail<T>("timeout");
    }
    return fail<T>("unreachable");
  }
  clearTimeout(timer);
  if (resp.status === 403) {
    return fail<T>("forbidden", 403);
  }
  let body: unknown;
  try {
    body = await resp.json();
  } catch {
    return fail<T>("invalidBody", resp.status);
  }
  if (!resp.ok) {
    const message =
      typeof body === "object" && body !== null && "message" in body
        ? String((body as Record<string, unknown>).message)
        : undefined;
    return fail<T>("badStatus", resp.status, message);
  }
  return { ok: true, value: body as T };
}

export function fetchHealth(baseUrl: string): Promise<LiveResult<LiveHealth>> {
  return request<LiveHealth>(baseUrl, "/health", { method: "GET" });
}

export async function fetchRuns(
  baseUrl: string,
): Promise<LiveResult<LiveRunSummary[]>> {
  const result = await request<{ runs: LiveRunSummary[] }>(baseUrl, "/api/runs", {
    method: "GET",
  });
  return result.ok ? { ok: true, value: result.value.runs } : result;
}

export function fetchRunDetail(
  baseUrl: string,
  runId: string,
): Promise<LiveResult<LiveRunDetail>> {
  return request<LiveRunDetail>(
    baseUrl,
    `/api/runs/${encodeURIComponent(runId)}`,
    { method: "GET" },
  );
}

/**
 * The single controlled mutating call. POSTs an empty body, or an allowlisted
 * `{scenario}` body. No arbitrary input is ever sent — the scenario id comes
 * only from the backend-provided allowlist surfaced as fixed buttons.
 */
export function runProofFixture(
  baseUrl: string,
  scenario?: string,
): Promise<
  LiveResult<{
    runId: string;
    status: string;
    scenario: string;
    source: string;
    workId?: string;
    queueState?: string;
  }>
> {
  const body = scenario ? JSON.stringify({ scenario }) : "{}";
  return request(
    baseUrl,
    "/api/proof-runs",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body,
    },
    8000,
  );
}
