/**
 * staticExportReload — Phase 13H.3 manual static export reload / read-model
 * replacement boundary.
 *
 * This module is the single, deliberately narrow runtime read-model reload
 * path. It performs ONE GET of the committed authoritative static export from
 * its own build-emitted asset URL, validates the fetched JSON all-or-nothing,
 * and returns a typed result carrying a compact, displayable read-model
 * snapshot derived from the validated export.
 *
 * Boundaries (Phase 13H.3):
 *  - It is NOT the local bridge. It never imports or calls the read-only bridge
 *    client or the controlled submission module, and it submits no action.
 *    Manual export reload and retry submission are separate operator actions:
 *    reloading the export does not imply a retry succeeded, and submitting a
 *    retry does not reload the export.
 *  - The fetch target is fixed at build time (the committed
 *    ``storytime-demo-export.json`` asset, resolved via
 *    ``new URL(..., import.meta.url)`` so Vite rewrites it to the emitted
 *    asset URL). The operator never supplies or edits a URL, so no arbitrary
 *    URL can be fetched. A cache-busting query parameter is applied to THIS
 *    fetch only.
 *  - Replacement is all-or-nothing: an invalid / partial / empty /
 *    schema-incompatible response is rejected as a typed error and the caller
 *    keeps its previous in-memory snapshot. There is no partial merge and no
 *    optimistic mutation.
 *  - The result is transient, in-memory data only. This module writes nothing
 *    to any browser durable store (no web storage, no client-side database, no
 *    cookies, no URL-history state) and uses no browser or worker cache APIs
 *    and no filesystem. The browser stays non-durable: a page reload returns to
 *    the bundled initial snapshot unless the served static export file itself
 *    changed.
 *  - There is no polling, no background schedule, no interval, no live socket,
 *    and no server-sent-events stream. The only timer is a single bounded abort
 *    deadline for the one fetch, cleared as soon as the fetch settles.
 */

/** Bounded deadline for the single static-export fetch, in milliseconds. */
const RELOAD_TIMEOUT_MS = 8000;

/**
 * The build-time asset URL of the committed static export. Vite statically
 * rewrites this ``new URL(<literal>, import.meta.url)`` to the emitted asset
 * URL; the operator never supplies or edits it, so no arbitrary URL can be
 * fetched here.
 */
export const STATIC_EXPORT_ASSET_URL = new URL(
  "./storytime-demo-export.json",
  import.meta.url,
).href;

/** A compact, displayable read model derived from a validated export snapshot. */
export interface ExportSnapshotReadModel {
  readonly schemaVersion: string;
  readonly generatedBy: string;
  readonly exportKind: string;
  readonly projectName: string;
  readonly projectTagline: string | null;
  readonly currentPhase: string | null;
  readonly runCount: number;
  readonly failureQueueCount: number;
  /** Run labels, for visible proof of which snapshot is currently held. */
  readonly runLabels: readonly string[];
}

/** Why a reload was rejected. Drives a safe, typed operator-facing message. */
export type ReloadErrorKind =
  | "network"
  | "timeout"
  | "http"
  | "parse"
  | "empty"
  | "schema";

/**
 * Result of a manual reload. ``ok: true`` carries a fully-validated read model
 * that the caller may use to replace its in-memory snapshot wholesale;
 * ``ok: false`` carries a typed reason and the caller retains its previous
 * snapshot. There is never a partial result.
 */
export type ExportReloadResult =
  | { readonly ok: true; readonly readModel: ExportSnapshotReadModel }
  | {
      readonly ok: false;
      readonly kind: ReloadErrorKind;
      readonly message: string;
    };

// ── all-or-nothing validation ───────────────────────────────────────────────

function isObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isNonEmptyString(value: unknown): value is string {
  return typeof value === "string" && value.length > 0;
}

function optionalString(value: unknown): string | null {
  return isNonEmptyString(value) ? value : null;
}

/**
 * Validate that a fetched value has the static-export top-level shape and the
 * specific fields the read model surfaces, then derive the compact read model.
 *
 * Returns ``null`` if anything required is missing or the wrong type — the
 * caller then rejects the reload and keeps the previous snapshot. This function
 * never returns a partially-populated model: it either validates the whole
 * shape it needs and returns a complete read model, or returns ``null``.
 */
export function deriveValidatedReadModel(
  value: unknown,
): ExportSnapshotReadModel | null {
  if (!isObject(value)) return null;
  if (!isNonEmptyString(value.schemaVersion)) return null;
  if (!isNonEmptyString(value.generatedBy)) return null;
  if (!isNonEmptyString(value.exportKind)) return null;
  if (!isObject(value.project)) return null;
  const project = value.project;
  if (!isNonEmptyString(project.name)) return null;
  if (!Array.isArray(value.runs)) return null;
  if (!Array.isArray(value.failureQueue)) return null;

  // Each run must carry the fields the read model surfaces.
  const runLabels: string[] = [];
  for (const run of value.runs) {
    if (!isObject(run)) return null;
    if (!isNonEmptyString(run.id)) return null;
    if (!isNonEmptyString(run.status)) return null;
    if (!isNonEmptyString(run.label)) return null;
    runLabels.push(run.label);
  }
  for (const item of value.failureQueue) {
    if (!isObject(item)) return null;
  }

  return {
    schemaVersion: value.schemaVersion,
    generatedBy: value.generatedBy,
    exportKind: value.exportKind,
    projectName: project.name,
    projectTagline: optionalString(project.tagline),
    currentPhase: optionalString(project.currentPhase),
    runCount: value.runs.length,
    failureQueueCount: value.failureQueue.length,
    runLabels,
  };
}

// ── the single manual reload fetch ──────────────────────────────────────────

/**
 * Fetch the committed static export once, validate it, and return a typed
 * result. Triggered only by an explicit operator action (a button onClick in
 * {@link StaticExportReloadPanel}) — never from module load, an effect
 * dependency, an interval, or a socket. The optional ``signal`` lets a caller
 * abort; an internal bounded deadline also aborts a stuck fetch.
 */
export async function reloadStaticExport(
  options?: { readonly signal?: AbortSignal },
): Promise<ExportReloadResult> {
  // Cache-busting is scoped to THIS static-export fetch only.
  const url = `${STATIC_EXPORT_ASSET_URL}?reload=${Date.now()}`;

  const controller = new AbortController();
  const onAbort = (): void => controller.abort();
  if (options?.signal) {
    if (options.signal.aborted) controller.abort();
    else options.signal.addEventListener("abort", onAbort, { once: true });
  }
  const timer = setTimeout(() => controller.abort(), RELOAD_TIMEOUT_MS);

  let response: Response;
  try {
    response = await fetch(url, {
      method: "GET",
      headers: { Accept: "application/json" },
      cache: "no-store",
      signal: controller.signal,
    });
  } catch (error) {
    clearTimeout(timer);
    options?.signal?.removeEventListener("abort", onAbort);
    const aborted =
      error instanceof DOMException && error.name === "AbortError";
    return aborted
      ? { ok: false, kind: "timeout", message: "Reload timed out; previous snapshot retained." }
      : { ok: false, kind: "network", message: "Could not reach the static export; previous snapshot retained." };
  }
  clearTimeout(timer);
  options?.signal?.removeEventListener("abort", onAbort);

  if (!response.ok) {
    return {
      ok: false,
      kind: "http",
      message: `Static export returned HTTP ${response.status}; previous snapshot retained.`,
    };
  }

  let parsed: unknown;
  try {
    parsed = await response.json();
  } catch {
    return {
      ok: false,
      kind: "parse",
      message: "Static export was not valid JSON; previous snapshot retained.",
    };
  }

  if (parsed === null || parsed === undefined) {
    return {
      ok: false,
      kind: "empty",
      message: "Static export response was empty; previous snapshot retained.",
    };
  }

  const readModel = deriveValidatedReadModel(parsed);
  if (readModel === null) {
    return {
      ok: false,
      kind: "schema",
      message:
        "Static export did not match the expected shape; previous snapshot retained.",
    };
  }

  return { ok: true, readModel };
}
