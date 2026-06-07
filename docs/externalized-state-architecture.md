# Externalized State Architecture (Phase 13F — architecture baseline, not implemented)

> **Status:** Architecture / contract baseline only. Phase 13F is an
> implementation candidate, pending review, **not locked**. Phase 13F adds no
> runtime code, no workspace, and no bridge. This document defines where
> durable state must live so a future Local mode never repeats the RoundTable
> browser-storage failure mode.

## 1. Core principle

> **The frontend is an operator surface, not the durable storage layer.**

Durable state lives **outside** the browser. The browser holds temporary UI
state only. The durable source of truth lives in an explicit external
workspace / storage target with clear export, reset, backup, and recovery
semantics.

## 2. Why (the RoundTable failure mode)

StoryTime must not repeat the RoundTable browser-storage failure mode, where
project state accreted in `localStorage` / `IndexedDB` until the browser
became the de-facto database — unrecoverable, hard to reset, and difficult to
export. The browser must never become the durable state container for
StoryTime. See `docs/browser-storage-policy.md` for the enforceable policy.

## 3. Durable state lives outside the browser

The durable state root is a **workspace** (see
`docs/local-mode-workspace-layout.md`). Everything durable lives there:

- project state,
- pipeline runs,
- generated artifacts (audio, reports),
- action requests and results,
- audit records,
- exports,
- local configuration,
- workspace manifest.

## 4. Ownership split

- **Workspace (durable):** owns truth. Files on disk (or a path-backed storage
  target), human-inspectable, exportable, backup-able, recoverable.
- **CLI / future local bridge (writer):** the only writer to durable state.
  Runs the existing governed operations; regenerates the deterministic export
  after a durable write.
- **Deterministic export / read model:** a derived, read-only projection of
  durable state, committed/produced for the frontend to consume.
- **Frontend (reader):** consumes the read model. Owns transient UI state
  only. Never the durable writer, never the durable owner.

## 5. High-level data flow

```text
Storage target / workspace
        ↓
StoryTime CLI / local bridge
        ↓
deterministic export / read model
        ↓
frontend operator surface
```

(No images, no external-asset diagrams. The flow is one-directional for reads;
writes flow only through the CLI / future bridge into the workspace.)

## 6. Specific guarantees

- **Generated artifacts** (audio, reports) live in workspace storage, never in
  the browser.
- **Audit records** live in workspace storage (see
  `docs/local-action-audit-spec.md`).
- **Action requests and results** live in workspace storage (see
  `docs/local-mode-storage-contract.md`).
- **Browser reset must not destroy project state.** Clearing the browser,
  closing the tab, or wiping site data must leave the workspace untouched. The
  workspace is the recovery point.
- **Workspace export / backup / recovery** are first-class: a workspace can be
  copied, archived, restored, and inspected with ordinary file tools.

## 7. What must be human-inspectable

A reviewer or operator must be able to open and read, with ordinary tools:

- the workspace manifest,
- action requests and results,
- audit records,
- the deterministic export / read model,
- logs.

Opaque, browser-locked, or binary-only durable state is forbidden by this
architecture.

## 8. Split-brain avoidance (Gemini risk #3)

There is exactly one source of truth: the workspace. The frontend never holds
a competing durable copy. The read model is derived, not authoritative. The
export-refresh loop (see `docs/local-bridge-architecture.md` §14–15) keeps the
read model behind the durable write, never ahead of it, and carries identity
so the frontend can detect a stale or mid-flight refresh.

## 9. What Phase 13F does NOT do

No workspace is created. No directories are made. No state is externalized at
runtime (there is no runtime). This is the architecture a future Local mode
must follow; Phase 13F only writes it down.
