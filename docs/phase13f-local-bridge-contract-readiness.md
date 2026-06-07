# Phase 13F — Local Bridge Contract Readiness (summary & checklist)

> **Status:** Architecture / contract baseline only. Phase 13F — Local Bridge
> Architecture & Contract Baseline — is an implementation candidate, pending
> review, **not locked**. Phase 13 remains STARTED and is not closed. Phase 13G
> and later are not started.

## 1. What Phase 13F decided

Phase 13F is the architectural lock before any Python local-bridge
implementation is allowed. It decided, as written contracts:

- **Local bridge architecture** — why the browser cannot execute local
  commands, why a local bridge is required for real Local mode, the future
  loopback-only binding, CORS / origin policy, strict DTO boundary,
  no-arbitrary-command rule, action allowlist, command-pattern router, response
  / error / shutdown model, and the action-completion → export-refresh loop
  (`docs/local-bridge-architecture.md`).
- **Execution timing policy** — long-running actions are asynchronous; the
  bridge returns `202 Accepted` with an `actionRequestId` / `jobId`; acceptance
  is not success; export refresh happens after a durable write; refresh races
  are avoided with atomic writes + identity-tagged read models
  (`docs/local-bridge-architecture.md` §15).
- **Externalized state architecture** — durable state lives outside the
  browser; the workspace is the durable root; the frontend is a reader, the
  CLI / future bridge is the writer (`docs/externalized-state-architecture.md`).
- **Browser storage policy** — an enforceable allowed/forbidden table; no
  `localStorage` / `sessionStorage` / `IndexedDB`; a strict gate for any future
  browser persistence (`docs/browser-storage-policy.md`).
- **Local-mode workspace layout** — a proposed workspace tree with per-folder
  durability / generation / audit / inspectability / deletability semantics,
  RAM vs disk vs USB distinctions, and blue/green slot isolation
  (`docs/local-mode-workspace-layout.md`).
- **Storage-targets architecture** — local / sync-folder / API-object target
  categories, a capability matrix, and the rule that providers and credentials
  are deferred and never browser-owned (`docs/storage-targets-architecture.md`).
- **Action-execution boundary** — preview is not execution; the future request
  lifecycle, validation / allowlist / confirmation / audit / idempotency /
  failure / rollback / export-refresh / async expectations; the first action
  candidate and the deferred higher-risk actions
  (`docs/action-execution-boundary.md`).
- **Local-action DTO spec** — future request / response field contracts; the
  initial allowlist (`retry_failed_stage`, `inspect_trust_envelope`,
  `refresh_export`); the deferred actions and why
  (`docs/local-action-dto-spec.md`).
- **Local-action audit spec** — future audit-record fields; acceptance ≠
  success; rejected / failed actions auditable (`docs/local-action-audit-spec.md`).
- **Local-mode storage contract** — workspace / storage-target references,
  directory contract, slot identity, export-refresh ownership, provider
  credential exclusion (`docs/local-mode-storage-contract.md`).
- **Local action queue observability** — the gauges, events, attributes, load
  limiting, stuck-action detection, and distributed carry-forward a future
  queue must satisfy before it is acceptable
  (`docs/local-action-queue-observability.md`).

## 2. What Phase 13F did NOT implement

- No local bridge, no server, no socket, no subprocess.
- No async queue, no workers, no polling, no job store.
- No queue metrics, no exporters, no OpenTelemetry instrumentation.
- No storage providers, no provider integrations, no provider sync.
- No real Local mode, no Cloud / Distributed mode.
- No mutation execution, no action execution, no audit-record generation.
- No DTO runtime code, no runtime schema validation.
- No router, no browser history, no browser storage.
- No change to `src/`, `frontend/src/`, `frontend/package.json`,
  `frontend/package-lock.json`, `pyproject.toml`, `uv.lock`, or
  `frontend/src/data/storytime-demo-export.json`.

## 3. Why the browser remains non-durable

To avoid the RoundTable browser-storage failure mode (durable state accreting
in the browser until it is unrecoverable). The browser is an operator surface;
durable state lives in the workspace. See
`docs/externalized-state-architecture.md` and `docs/browser-storage-policy.md`.

## 4. Why the local bridge is future work

Implementing the bridge before its architecture, DTO contract, storage model,
execution-timing policy, queue-observability model, and security boundary are
settled would risk the exact drift this baseline prevents. The contract is now
written; implementation is a later phase.

## 5. Readiness checklist — what must be true before Phase 13G (or later) implements bridge code

- [ ] Phase 13F is reviewed (GPT-5.5 + Gemini) and **locked** by explicit user
      decision.
- [ ] The DTO request / response contract is accepted as stable enough to build
      against (`docs/local-action-dto-spec.md`).
- [ ] The audit-record contract is accepted (`docs/local-action-audit-spec.md`).
- [ ] The workspace layout and storage contract are accepted
      (`docs/local-mode-workspace-layout.md`,
      `docs/local-mode-storage-contract.md`).
- [ ] The execution-timing policy (async + `202 Accepted` + acceptance ≠
      success + refresh-after-durable-write) is accepted
      (`docs/local-bridge-architecture.md` §15).
- [ ] The queue-observability model is accepted as the minimum bar a queue must
      meet (`docs/local-action-queue-observability.md`).
- [ ] The security boundary (loopback-only, strict origin, no arbitrary
      command, command-pattern router, allowlist) is accepted
      (`docs/local-bridge-architecture.md` §5–10).
- [ ] The browser-storage policy remains intact and enforced
      (`docs/browser-storage-policy.md`).
- [ ] The implementing phase commits to: no provider credentials in the
      browser; loopback-only binding; allowlist-only actions; idempotency for
      retry / rerun; observable queue from day one.

## 6. Recommended next phases

1. **Phase 13G — Local Bridge Implementation (minimal, gated):** implement the
   smallest possible loopback-only Python bridge that supports exactly the
   initial allowlist (`retry_failed_stage`, `inspect_trust_envelope`,
   `refresh_export`), with the observable queue and the execution-timing policy,
   under its own Phase Closure Protocol review. The most safety-sensitive gate
   in Phase 13.
2. **Alternative — Runtime Contract Hardening:** add lightweight runtime
   validation of the committed export against the frontend types before any
   bridge writes can introduce drift.
3. **Alternative — Portfolio Website Polish / Public Demo Packaging** (the
   roadmap's later Phase 13G/13H content), if portfolio-readiness is the
   priority over Local mode.
4. **Pause Phase 13:** the read-only operator GUI plus the Demo-mode preview
   layer plus this architecture lock is a coherent, demo-credible stopping
   point; pausing here is defensible.

## 7. Current state after Phase 13F

- Phase 12 CLOSED.
- Phase 13 STARTED.
- Phase 13A–13D, 13D.1, 13D.2, 13E all LOCKED; **Phase 13E is the last locked
  phase**.
- Phase 13F — Local Bridge Architecture & Contract Baseline — implementation
  candidate, pending review, **not locked**.
- Phase 13G and later NOT STARTED.
- Phase 13 remains STARTED and not closed.
