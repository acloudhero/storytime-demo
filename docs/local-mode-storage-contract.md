# Local Mode Storage Contract (Phase 13F — future contract, not implemented)

> **Status:** Architecture / contract baseline only. Phase 13F is an
> implementation candidate, pending review, **not locked**. **Phase 13F does
> not implement the workspace, does not create directories, and adds no runtime
> code.** This document is the storage contract a future Local-mode phase must
> honour.

## 1. Workspace references

A future action request / result / audit record references a workspace by:

- **`workspace.id`** — a stable identifier for the workspace (not a secret, not
  an absolute private user path).
- **`workspace.root`** — the workspace root, expressed as a workspace-relative
  or demo-safe reference in examples (never an absolute private user path in
  documentation fixtures).
- **`workspace.manifest`** — `manifest.json` at the workspace root: identity,
  schema version, active slot, created / updated timestamps.

## 2. Storage target

- **`storageTarget.type`** — one of the categories in
  `docs/storage-targets-architecture.md` (`local-disk`, `ram`, `usb`, future
  sync / API targets). No credentials in the contract, ever.

## 3. Directory contract

| Reference | Directory | Owner (future) | Notes |
|---|---|---|---|
| action request dir | `action-requests/` | bridge writes | durable inbound DTOs |
| action result dir | `action-results/` | bridge writes | durable results |
| audit dir | `audit/` | bridge writes | append-only, never deleted |
| export dir | `exports/` | CLI / bridge writes | derived read model |
| reports dir | `reports/` | operations write | regenerable |
| artifacts (audio) dir | `audio/` | operations write | regenerable, costly |

See `docs/local-mode-workspace-layout.md` for the full layout and durability
table.

## 4. Slot / environment identity

Where blue/green or slot isolation is used:

- the active slot is named in `manifest.json` and/or selected by the operator,
- every action request targets a specific `workspace` (and `slot` where
  relevant),
- export refresh targets the same workspace / slot,
- future Cloud / Distributed mode maps slot identity to environment /
  workspace identity.

## 5. Export refresh ownership

- The **CLI / future local bridge owns export refresh**, not the browser.
- Export refresh happens **after** a durable action-result write.
- The export / read model is derived and rebuildable; it is never the source
  of truth (see `docs/externalized-state-architecture.md`).

## 6. Provider credential exclusion from browser

- **Provider credentials are never browser-owned** (see
  `docs/browser-storage-policy.md` and `docs/storage-targets-architecture.md`).
- The storage contract carries a storage-target **type**, never a credential,
  token, key, or secret.
- Documentation example fixtures must contain no credentials; the test
  `tests/test_local_mode_contract_examples.py` enforces this.

## 7. What Phase 13F does NOT do

No workspace, no directories, no manifest, no runtime code that touches a
filesystem. This is the contract; the implementation is a later phase.
