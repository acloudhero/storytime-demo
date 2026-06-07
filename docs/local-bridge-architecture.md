# Local Bridge Architecture (Phase 13F — architecture baseline, not implemented)

> **Status:** Architecture / contract baseline only. Phase 13F — Local Bridge
> Architecture & Contract Baseline — is an implementation candidate, pending
> review, **not locked**. **Phase 13F does not implement a local bridge.** No
> server, no socket, no subprocess, no async queue, no worker, no metrics
> exporter, and no runtime code of any kind is added by Phase 13F. This
> document defines the *future* shape so that a later phase (Phase 13G or
> later) can implement a Python-owned local bridge without re-litigating the
> architecture. It is the architectural lock that must be in place before any
> bridge code is written.

## 1. Why a browser cannot execute local CLI commands directly

The StoryTime operator GUI is a static, read-only frontend (Phase 13B–13E). A
browser page cannot — and for safety must not — execute local processes:

- Browsers deliberately sandbox page JavaScript away from the host OS. There
  is no portable, safe API for a web page to spawn `storytime` CLI processes,
  read arbitrary local files, or write to a local workspace.
- Even where a browser extension or experimental API could approximate this,
  granting a web origin host-process authority is a severe security
  regression. StoryTime will not do it.
- The Demo-mode action previews shipped in the locked Phase 13E describe
  operator intent; they never execute. The gap between "preview" and
  "execute" is exactly the gap a local bridge would close — under explicit,
  gated, local-only control.

## 2. Why a local bridge is required for real Local mode

Real Local mode (future) needs a trusted local process that:

- owns writes to the durable workspace (see
  `docs/externalized-state-architecture.md`),
- maps a small allowlist of operator actions to pre-approved StoryTime
  operations,
- runs the existing governed pipeline / CLI operations rather than
  redefining them,
- regenerates the deterministic static export after a durable action result
  is written,
- emits durable audit records.

The browser would send a typed action **request** to this local process and
later read **results** from a refreshed export / read model. The browser
never gains host authority; the bridge holds it, narrowly.

## 3. Why Phase 13F does not implement the bridge

Phase 13F is the architecture lock. Implementing the bridge before the
architecture, DTO contract, storage model, execution-timing policy, queue
observability model, and security boundary are settled would risk exactly the
drift this baseline exists to prevent (RoundTable browser-storage trap,
synchronous-blocking trap, split-brain state, RCE-by-arbitrary-command, and
premature provider-credential ownership). Phase 13F writes the contract;
a later phase implements against it.

## 4. Future local bridge shape (deferred)

A minimal, Python-owned local process. **Do not prescribe a heavy framework.**
The recommendation for the later implementing phase is a small, dependency-
light Python HTTP listener (or equivalent local IPC) that:

- binds loopback-only,
- accepts a narrow, versioned action-request DTO,
- routes each DTO action to exactly one pre-approved Python operation,
- returns a versioned action-response DTO,
- writes durable action results and audit records into the workspace,
- triggers a deterministic export refresh after a durable write.

The bridge is owned by the existing Python package, not by a new service
tier, and not by the browser.

## 5. Future localhost-only binding requirement (deferred)

When the bridge is eventually implemented it MUST:

- bind only to `127.0.0.1` and/or `::1` (loopback),
- reject any request whose connection is not from loopback,
- **never** bind to `0.0.0.0`,
- **never** expose LAN access by default,
- treat any future non-loopback exposure as a separate, explicitly gated
  phase with its own security review.

## 6. Future CORS / origin policy (deferred)

- The bridge must enforce a strict origin allowlist (the local operator GUI
  origin only).
- No wildcard CORS (`Access-Control-Allow-Origin: *`).
- Credentials, if ever introduced, are never echoed to arbitrary origins.
- Preflight handling must default closed (reject unknown origins).

## 7. Future strict DTO request boundary (deferred)

- The bridge accepts only a versioned request DTO (see
  `docs/local-action-dto-spec.md`).
- Unknown fields are rejected or ignored per an explicit, documented policy
  (default: reject unknown top-level action names; ignore unknown optional
  annotations only if a forward-compatibility policy is later defined).
- `schemaVersion` is mandatory; mismatches are rejected with a clear error.

## 8. Future no-arbitrary-command-execution rule (deferred)

This is the central RCE-avoidance rule Gemini flagged:

- The bridge must **never** accept an arbitrary shell command, script, SQL
  string, or file path to execute.
- There is no "run this command" endpoint, ever.
- The only thing the bridge accepts is a DTO naming an **allowlisted action**
  plus typed, validated parameters.

## 9. Future action allowlist (deferred)

The first allowlisted actions (see `docs/local-action-dto-spec.md`):

- `retry_failed_stage`
- `inspect_trust_envelope`
- `refresh_export`

Explicitly deferred / not initially allowlisted (higher risk):

- `record_review_decision`
- `regenerate_operator_report`
- `publish_episode`
- `delete_artifact`
- any provider-sync action.

## 10. Future command-pattern router (deferred)

The bridge maps actions with a command-pattern router:

- each DTO `action` maps to **exactly one** pre-approved Python operation,
- **no** generic shell execution,
- **no** arbitrary SQL,
- **no** arbitrary file-path writes outside the active workspace,
- the router validates the action against the allowlist **before** any
  operation is dispatched,
- unknown or deferred actions are rejected with a typed error, never routed.

## 11. Future response structure (deferred)

See `docs/local-action-dto-spec.md` for the full response DTO. In summary the
bridge returns a versioned response carrying: `accepted`, `status`, optional
`result`, `errors`, `warnings`, `exportRefreshRequired`, `auditRecordRef`, and
— for asynchronous accepted actions — an `actionRequestId` / `jobId`.

## 12. Future error-handling model (deferred)

- Validation errors → rejected before dispatch, typed error, no side effects.
- Precondition failures → rejected, audited where appropriate, no execution.
- Execution failures (future) → durable failure result + audit record;
  surfaced through the existing Failure / Recovery read model.
- The bridge fails closed: on any ambiguity it rejects rather than guesses.

## 13. Future bridge shutdown / reset expectations (deferred)

- The bridge is a local process the operator starts and stops explicitly.
- Stopping the bridge must never corrupt the workspace; in-flight async work
  must be resumable or cleanly marked interrupted (see
  `docs/local-action-queue-observability.md`).
- A bridge reset must not delete durable workspace state; resetting the
  bridge is not the same as resetting the workspace.

## 14. Future update loop: action completion → refreshed export (deferred)

The canonical loop (architecture only):

```text
operator GUI  --(action request DTO)-->  local bridge
local bridge  --(dispatch)-->            one pre-approved Python operation
operation     --(durable write)-->       workspace (results + audit)
bridge        --(after durable write)--> deterministic export refresh
operator GUI  --(reads refreshed export / read model)--> updated view
```

The frontend learns results by reading the refreshed export / read model —
**not** by treating request acceptance as success. See the execution-timing
policy below.

---

## 15. Execution timing policy (Hybrid Option C)

> Cross-referenced from `docs/action-execution-boundary.md`. This is the
> explicit timing policy Gemini's Hybrid Option C requires. Architecture only —
> Phase 13F implements none of it.

### 15.1 Questions this policy answers

- **Are future long-running actions synchronous or asynchronous?** Long-running
  actions (a full pipeline run, a TTS render) are **asynchronous**. Short
  validation-only actions may return an immediate validation response.
- **How does the bridge avoid browser timeout for long-running operations?** By
  returning promptly with an accepted-but-not-complete response and an
  `actionRequestId` / `jobId`, rather than holding the HTTP connection open for
  the entire operation.
- **What should the first local bridge return when an action is accepted?** For
  long-running actions: `202 Accepted` (or the local-IPC equivalent) with an
  `actionRequestId` / `jobId` and `status: "accepted"`. **Acceptance is not
  success.**
- **How does the frontend learn status later?** By reading explicit
  action-result state and/or the refreshed export / read model — never by
  inferring success from acceptance.
- **How does the export-refresh loop avoid stale read-model refreshes?** Export
  refresh occurs **after** a durable action result is written, and the read
  model carries enough identity (workspace id, slot, action request id, a
  freshness/refresh timestamp) that the frontend can detect a stale or
  mid-flight refresh and avoid a rehydration race.

### 15.2 Recommended policy (deferred)

- Short validation-only actions may return immediate validation responses.
- Long-running actions must use an asynchronous job / action pattern.
- The bridge returns `202 Accepted` with `actionRequestId` / `jobId` for
  long-running operations.
- The browser must not block on a full pipeline run or TTS render.
- Status is read from explicit action-result state or the refreshed export /
  read model.
- Export refresh occurs only after a durable action-result write.
- The frontend must not treat request acceptance as execution success.
- Retry / rerun actions must be idempotency-aware (see `idempotencyKey` in the
  DTO spec) to avoid duplicate execution.
- Any asynchronous action queue must be observable from the start (see
  `docs/local-action-queue-observability.md`).
- Local mode does not need autoscaling, but it still needs queue visibility and
  load limiting.
- Distributed / Cloud mode may later map the same queue concepts to scaling,
  worker pools, and autoscaling signals — see the carry-forward section of the
  queue-observability doc.

### 15.3 State rehydration race avoidance (Gemini risk #2)

To avoid the refresh race Gemini flagged:

- export refresh is written atomically (write-temp-then-rename or equivalent),
- the read model carries a monotonic refresh marker / timestamp and the
  workspace + slot identity it was generated from,
- the frontend treats a refresh whose identity does not match the action it
  issued as not-yet-current and waits for the next refresh rather than
  rendering a half-updated model,
- the frontend never merges its own optimistic guess into the read model.

### 15.4 What Phase 13F does NOT do here

No queue, no workers, no polling loop, no job store, no `202` endpoint, no
timers, no OpenTelemetry instrumentation, and no metrics exporters are
implemented. This section is a contract for a later phase.

---

## 16. Risks this architecture explicitly addresses

| # | Gemini-flagged risk | Where addressed |
|---|---------------------|-----------------|
| 1 | Synchronous blocking for long-running pipeline / TTS actions | §15 execution-timing policy (async + `202 Accepted`) |
| 2 | State rehydration race after refreshed-export writes | §15.3 + `docs/externalized-state-architecture.md` |
| 3 | Browser storage / backend source-of-truth split-brain | `docs/browser-storage-policy.md` + `docs/externalized-state-architecture.md` |
| 4 | RCE if a bridge accepts arbitrary commands | §8 no-arbitrary-command rule + §10 command-pattern router |
| 5 | Premature direct provider-credential ownership by the browser | `docs/storage-targets-architecture.md` + `docs/browser-storage-policy.md` |

## 17. What Phase 13F decided vs deferred

- **Decided (documented contract):** the bridge's binding, origin, DTO, router,
  allowlist, response, error, shutdown, update-loop, and timing model.
- **Deferred (future phase):** every line of bridge runtime code, the async
  queue, workers, metrics exporters, OpenTelemetry instrumentation, storage
  providers, and real Local mode.

See `docs/phase13f-local-bridge-contract-readiness.md` for the readiness
checklist that must be satisfied before any bridge code is written.
