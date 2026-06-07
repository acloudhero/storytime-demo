# Action Execution Boundary (Phase 13F — architecture baseline, not implemented)

> **Status:** Architecture / contract baseline only. Phase 13F is an
> implementation candidate, pending review, **not locked**. **Phase 13F
> executes no operator action and implements no DTO in runtime code.** This
> document defines the boundary between a Demo-mode action *preview* (shipped,
> locked in Phase 13E) and a future Local-mode action *execution*.

## 1. Action preview is not execution

Phase 13E shipped Demo-mode action previews: data-driven descriptions of what
an operator action would do, why it is blocked in Demo mode, what preconditions
apply, and what a future request shape might look like. A preview never
executes. This document describes what *would* turn a preview into a real,
gated Local-mode execution — under a future phase.

## 2. Future Local action request lifecycle (deferred)

```text
preview (Demo mode, shipped)
   ↓ operator chooses to act (future Local mode)
action request DTO constructed (frontend)
   ↓ sent to local bridge (loopback only)
validation boundary (bridge): schema + allowlist + preconditions
   ↓ pass
confirmation boundary (operator confirms consequential action)
   ↓ confirmed
dispatch to exactly one pre-approved operation (command-pattern router)
   ↓ (long-running → async, 202 Accepted + actionRequestId/jobId)
durable action result written to workspace
   ↓
audit record written to workspace
   ↓
deterministic export refresh (after durable write)
   ↓
frontend reads refreshed read model (acceptance ≠ success)
```

## 3. Action request DTO concept (deferred)

See `docs/local-action-dto-spec.md`. The request is a versioned, typed DTO
naming an allowlisted action plus validated parameters. There is no
free-form command field, ever.

## 4. Validation boundary (deferred)

The future bridge validates, before any dispatch:

- `schemaVersion` present and supported,
- `action` is on the allowlist,
- `target` is well-formed and refers to an object in the active workspace,
- `workspace` / `storageTarget` are present and valid,
- `idempotencyKey` present for retry / rerun,
- preconditions are evaluable.

Validation failure → reject before dispatch; no side effects.

## 5. Allowlist (deferred)

Initial allowlist: `retry_failed_stage`, `inspect_trust_envelope`,
`refresh_export`. Everything else is rejected. See
`docs/local-action-dto-spec.md` §"Allowlisted initial actions".

## 6. Confirmation boundary (deferred)

Consequential actions (anything that mutates durable state) require explicit
operator confirmation (`requiresConfirmation: true`). Validation-only or
read-only actions may skip confirmation if clearly safe.

## 7. Audit record expectation (deferred)

Every accepted consequential action produces a durable audit record (see
`docs/local-action-audit-spec.md`). Rejected and failed actions are auditable
where appropriate. **Phase 13F generates no audit record** — nothing executes.

## 8. Idempotency expectation (deferred)

Retry / rerun actions carry an `idempotencyKey`. The future bridge must
deduplicate by idempotency key so a double-submit does not double-execute a
pipeline run. Acceptance of a duplicate key returns the original action's
status, not a new execution.

## 9. Failure-state handling (deferred)

Execution failures produce a durable failure result and audit record, surfaced
through the existing Failure / Recovery read model. The bridge fails closed.

## 10. Rollback / compensation expectations (deferred, where applicable)

Some actions are naturally idempotent or re-runnable (retry a failed stage).
Others would need compensation if partially applied. The implementing phase
must define, per action, whether it is safely re-runnable, requires
compensation, or must be all-or-nothing. Phase 13F flags this as a per-action
design obligation rather than prescribing a single mechanism.

## 11. Refreshed-export expectation (deferred)

After a durable action-result write, the future bridge regenerates the
deterministic export / read model. The frontend reads the refreshed model;
acceptance is never treated as success. See the execution-timing policy in
`docs/local-bridge-architecture.md` §15.

## 12. Async execution expectation for long-running actions (deferred)

Long-running actions (full pipeline run, TTS render) are asynchronous: the
bridge returns `202 Accepted` with an `actionRequestId` / `jobId`, and the
frontend learns status from explicit action-result state or the refreshed
export. The browser never blocks on a long-running operation. The async queue
that backs this must be observable (see
`docs/local-action-queue-observability.md`).

## 13. First likely action candidate

**`retry_failed_stage` / rerun a failed stage** — the safest first real action:
it maps to an existing governed operation, is naturally re-runnable, and has a
clear precondition (a failed / blocked stage on an eligible run).

## 14. Explicitly deferred higher-risk actions

- **approve / reject governance decisions** — highest-risk; changes the Trust
  Envelope and gates downstream actions; needs the strongest audit + identity
  guarantees.
- **destructive cleanup** — deletes durable artifacts; needs compensation /
  confirmation design.
- **provider sync** — touches credentials + network + external mutation.
- **publishing actions** — externally visible side effects.
- **credential-bearing actions** — require a credential model the current
  architecture deliberately excludes from the browser.

Each deferred action requires its own gated phase and review.

## 15. What Phase 13F does NOT do

No DTO is implemented in runtime code, no action executes, no audit record is
generated, no bridge validates anything at runtime. This is the boundary
contract a future phase must implement against.
