/**
 * localBridgeTypes — Phase 13H read-only local-bridge type vocabulary.
 *
 * Phase 13H introduces the FIRST frontend network boundary, and it is
 * deliberately observe-only. These types describe what the frontend may *read*
 * from the locked Phase 13G local bridge over loopback — bridge health,
 * readiness/security posture, the observable queue snapshot, and an existing
 * action's lifecycle state — plus the safe error vocabulary the UI renders when
 * the bridge is absent, rejects the origin, times out, or returns something
 * unexpected.
 *
 * This module holds the read-only response / probe / error shapes only. The
 * request and result types for the single controlled submission live separately
 * in ``localBridgeActions.ts`` (added in the locked Phase 13H.1), so this
 * read-only vocabulary stays free of any mutation shape. The browser remains an
 * operator surface, never durable storage; these are transient, in-memory
 * shapes only.
 */

/* ─────────────────── action lifecycle vocabulary ─────────────────── */

/**
 * The honest lifecycle states a bridge action can be in, mirroring the Phase
 * 13G queue/worker states. ``unknown`` is the safe fallback the adapter uses
 * for any state string it does not recognise — the UI never invents success.
 */
export type ActionLifecycleState =
  | "accepted"
  | "queued"
  | "running"
  | "completed"
  | "failed"
  | "rejected"
  | "not_implemented"
  | "unknown";

/** Ordered lifecycle vocabulary for the read-only lifecycle legend. */
export const ACTION_LIFECYCLE_ORDER: readonly ActionLifecycleState[] = [
  "accepted",
  "queued",
  "running",
  "completed",
  "failed",
  "rejected",
  "not_implemented",
] as const;

/* ─────────────────── read-only response shapes ─────────────────── */

/** Shape of ``GET /health`` (liveness only). */
export interface BridgeHealth {
  readonly status: string;
  readonly schemaVersion: string;
}

/** Shape of ``GET /ready`` (readiness + security posture). */
export interface BridgeReady {
  readonly status: string;
  readonly schemaVersion: string;
  readonly bridgeVersion: string;
  readonly runtimeMode: string;
  readonly loopbackOnly: boolean;
  readonly wildcardOriginAllowed: boolean;
  readonly workspaceConfigured: boolean;
  readonly maxConcurrency: number;
  readonly queueCapacity: number;
  readonly executableActions: readonly string[];
}

/** Shape of ``GET /queue`` (observable snapshot — read-only gauges). */
export interface BridgeQueueSnapshot {
  readonly queueDepth: number;
  readonly inFlightCount: number;
  readonly completedCount: number;
  readonly failedCount: number;
  readonly rejectedCount: number;
  readonly deadLetterCount: number;
  readonly oldestQueuedAgeSeconds: number;
  readonly longestInFlightAgeSeconds: number;
  readonly capacity: number;
  readonly saturationRatio: number;
  readonly maxConcurrency: number;
}

/** Shape of ``GET /actions/{actionRequestId}`` (lifecycle state of one action). */
export interface BridgeActionStatus {
  readonly actionRequestId: string;
  readonly jobId: string;
  readonly requestId: string;
  readonly action: string;
  readonly status: ActionLifecycleState;
  readonly error: string | null;
}

/* ─────────────────── safe error vocabulary ─────────────────── */

/**
 * The distinct, safe outcomes a read-only bridge probe can produce. Each maps
 * to a clearly-worded UI state; none is treated as success.
 *
 *  - ``blockedNonLoopback`` — the configured URL is not loopback; the client
 *    refuses to call it (defence-in-depth; the bridge is loopback-only anyway).
 *  - ``unavailable`` — no bridge is reachable (connection refused / DNS / etc.).
 *  - ``timeout`` — the bounded request deadline elapsed.
 *  - ``originRejected`` — the bridge answered 403 (strict Origin policy).
 *  - ``httpError`` — a non-OK HTTP status other than 403.
 *  - ``malformed`` — the body was not valid JSON.
 *  - ``unexpectedSchema`` — valid JSON, but missing required fields.
 */
export type BridgeErrorKind =
  | "blockedNonLoopback"
  | "unavailable"
  | "timeout"
  | "originRejected"
  | "httpError"
  | "malformed"
  | "unexpectedSchema";

/** A read-only probe result: typed data, or a safe structured error. */
export type BridgeResult<T> =
  | { readonly ok: true; readonly data: T }
  | { readonly ok: false; readonly kind: BridgeErrorKind; readonly status?: number };

/* ─────────────────── transient UI probe state ─────────────────── */

/**
 * The transient (in-memory only) probe state the panels render. ``idle`` means
 * the operator has not yet asked the frontend to look; probing only happens on
 * an explicit manual action, never in a background loop.
 */
export type BridgeProbe<T> =
  | { readonly phase: "idle" }
  | { readonly phase: "probing" }
  | { readonly phase: "ok"; readonly data: T }
  | { readonly phase: "error"; readonly kind: BridgeErrorKind; readonly status?: number };
