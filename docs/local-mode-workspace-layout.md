# Local Mode Workspace Layout (Phase 13F — proposed future layout, not implemented)

> **Status:** Architecture / contract baseline only. Phase 13F is an
> implementation candidate, pending review, **not locked**. **No workspace is
> created. No directories are made. No runtime code creates anything.** This
> document proposes the future workspace layout so a later Local-mode phase has
> a fixed target.

## 1. Proposed layout

```text
storytime-workspace/
  manifest.json        # workspace identity, schema version, slot, created/updated
  config/              # local configuration (non-secret); never provider credentials
  runs/                # durable pipeline-run state
  action-requests/     # durable inbound action-request DTOs (future bridge writes here)
  action-results/      # durable action-result records (future bridge writes here)
  exports/             # deterministic export / read model the frontend consumes
  reports/             # generated operator reports
  audio/               # generated audio artifacts
  logs/                # bridge / operation logs
  audit/               # durable audit records (append-only)
  tmp/                 # scratch; safe to delete; never the source of truth
```

## 2. Folder responsibilities

| Folder | Responsibility | Durable? | Generated? | Audit-bearing? | Human-inspectable? | Safe to delete? |
|---|---|---|---|---|---|---|
| `manifest.json` | Workspace identity, schema version, active slot | Yes | No | No | Yes | No |
| `config/` | Local non-secret configuration | Yes | No | No | Yes | No (back up first) |
| `runs/` | Durable pipeline-run state | Yes | Partly | No | Yes | No |
| `action-requests/` | Inbound action-request DTOs | Yes | Yes (by bridge) | Indirectly | Yes | No (audit lineage) |
| `action-results/` | Durable action results | Yes | Yes (by bridge) | Indirectly | Yes | No (audit lineage) |
| `exports/` | Deterministic export / read model | Derived | Yes | No | Yes | Yes (rebuildable) |
| `reports/` | Generated operator reports | Yes | Yes | No | Yes | Yes (regenerable) |
| `audio/` | Generated audio artifacts | Yes | Yes | No | Partly (binary) | Yes (regenerable, costly) |
| `logs/` | Operation / bridge logs | Yes | Yes | Supporting | Yes | Yes (rotate) |
| `audit/` | Append-only audit records | Yes | Yes | **Yes** | Yes | **No** |
| `tmp/` | Scratch | No | Yes | No | Maybe | **Yes** |

Notes:

- `exports/` is **derived**: it can always be regenerated from durable state,
  so it is safe to delete and rebuild. It is never the source of truth.
- `audit/` is **append-only** and must not be deleted; it is the accountability
  record for future executed actions.
- `audio/` is regenerable but expensive (TTS cost / time); deletion is allowed
  but discouraged without a reason.

## 3. Backup / restore expectations

- A workspace is a directory tree; backup is a copy / archive of that tree.
- Restore is unpacking the tree to a path and pointing the CLI / future bridge
  at it.
- `tmp/` may be excluded from backups.
- `audit/` must always be included in backups.
- A restored workspace must be functional without the browser; the browser is
  rebuilt from the workspace, never the other way round.

## 4. RAM workspace vs disk workspace

- A **disk workspace** is a normal directory on persistent storage; it survives
  reboots and is the default for durable work.
- A **RAM / temp workspace** is a workspace rooted at a tmpfs / temp path. It is
  fast and ephemeral: it is **lost on reboot** and must be treated as
  non-durable unless explicitly exported to disk. A RAM workspace is suitable
  for throwaway experiments, never for durable project state.

## 5. USB / removable workspace

A USB / removable-drive workspace is **just a path-backed local workspace**
whose path happens to be removable media. It carries removable-media risks:

- the path can disappear mid-operation (drive unplugged),
- writes may be buffered by the OS and not yet flushed,
- the future bridge must fail closed if the workspace path becomes
  unavailable, and must never silently switch to a different workspace.

## 6. Blue/green / slot-isolated roots

The layout must support slot isolation so an operator can keep an active and an
inactive workspace without cross-contamination:

- the **active slot / workspace must be explicit** (named in `manifest.json`
  and/or selected by the operator),
- **inactive slots must not be mutated accidentally** — the future bridge only
  ever writes to the targeted workspace / slot,
- **bridge actions must target a specific workspace / slot** (the action
  request carries `workspace` and, where relevant, `slot`),
- **export refresh must target the correct workspace / slot** (the read model
  carries the workspace + slot identity it was generated from),
- future Cloud / Distributed mode may map this slot concept to an
  environment / workspace identity.

## 7. What Phase 13F does NOT do

No directory is created, no manifest is written, no slot is selected, and no
runtime code touches a filesystem. This is a proposal for a later phase.
