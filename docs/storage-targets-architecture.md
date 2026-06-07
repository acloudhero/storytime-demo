# Storage Targets Architecture (Phase 13F — architecture baseline, not implemented)

> **Status:** Architecture / contract baseline only. Phase 13F is an
> implementation candidate, pending review, **not locked**. **Phase 13F
> implements no storage provider and no provider integration.** This document
> categorizes future storage targets so a later phase can implement them under
> the right security model.

## 1. Storage target categories

### 1.1 Now / near-term local targets

- **Local hard drive workspace** — a directory on persistent local storage.
  The default durable target.
- **RAM / temp workspace** — a workspace rooted at a temp / tmpfs path.
  Ephemeral; lost on reboot.
- **USB / removable-drive workspace** — a path-backed local workspace on
  removable media, with removable-media risks (see
  `docs/local-mode-workspace-layout.md` §5).

### 1.2 Future filesystem-backed sync targets

- **Google Drive synced folder**
- **iCloud Drive synced folder**
- **Dropbox synced folder**

These are **path-backed workspaces only when mounted / synced by the OS**. When
the OS presents them as a local path, the future bridge treats them like any
local directory — but sync latency, conflict files, and partial-sync states are
real risks and must be handled by the implementing phase.

### 1.3 Future API / object targets

- **S3-compatible object storage**
- **Direct Google Drive API**
- **Direct Dropbox API**
- **Direct iCloud integration** (if practical)
- **Future cloud / distributed storage**

These require credentials and provider-specific design. They are deferred and
higher risk.

## 2. Hard rules

- **Phase 13F does not implement any provider.**
- **Provider credentials must never be browser-owned** in the current
  architecture (see `docs/browser-storage-policy.md`).
- **Direct provider APIs require later security / auth / provider-specific
  design** — a separate, explicitly gated phase.
- **S3 is object storage, not a normal filesystem** — it has object semantics
  (put / get / list keys), not POSIX path semantics; treating it like a
  directory is a design error.
- **Google Drive / iCloud / Dropbox sync folders may be treated as local paths
  only when mounted by the OS** — never via direct API in the near term.
- **Provider sync actions are deferred and higher risk** — they touch
  credentials, network, and external mutation.

## 3. Capability matrix

| Target | Path semantics | Object semantics | Offline local op | Requires credentials | Suitable for Demo | Suitable for Local | Suitable for Cloud/Dist | Implementation status |
|---|---|---|---|---|---|---|---|---|
| Local hard drive | Yes | No | Yes | No | n/a (Demo uses static export) | Yes | No | Not implemented (future Local) |
| RAM / temp | Yes | No | Yes | No | n/a | Yes (ephemeral) | No | Not implemented (future Local) |
| USB / removable | Yes | No | Yes | No | n/a | Yes (with risks) | No | Not implemented (future Local) |
| Google Drive synced folder | Yes (when mounted) | No | Partly | No (OS handles sync) | n/a | Future | Maybe | Not implemented (deferred) |
| iCloud Drive synced folder | Yes (when mounted) | No | Partly | No (OS handles sync) | n/a | Future | Maybe | Not implemented (deferred) |
| Dropbox synced folder | Yes (when mounted) | No | Partly | No (OS handles sync) | n/a | Future | Maybe | Not implemented (deferred) |
| S3-compatible object storage | No | Yes | No | Yes | No | No (not near-term) | Future | Not implemented (deferred, higher risk) |
| Direct Google Drive API | No | Yes | No | Yes | No | No | Future | Not implemented (deferred, higher risk) |
| Direct Dropbox API | No | Yes | No | Yes | No | No | Future | Not implemented (deferred, higher risk) |
| Direct iCloud integration | No | Maybe | No | Yes | No | No | Future | Not implemented (deferred, higher risk) |
| Cloud / distributed storage | No | Yes | No | Yes | No | No | Future | Not implemented (deferred) |

"Suitable for Demo" is `n/a` / `No` for all targets because Demo mode (the only
implemented mode, locked in Phase 13E) reads a committed static export and does
not touch any storage target.

## 4. What Phase 13F does NOT do

No provider SDK, no credential handling, no network call, no object-store
client, no sync logic. The matrix is a plan, not an implementation.
