# Browser Storage Policy (Phase 13F — enforceable policy baseline)

> **Status:** Policy baseline. Phase 13F is an implementation candidate,
> pending review, **not locked**. This policy is enforceable today by the
> existing no-storage greps and the state-discipline guard. It restates and
> hardens the rule the frontend has followed since Phase 13B.

## 1. Principle

> **The frontend is an operator surface, not the durable storage layer.**

The browser may hold temporary UI state only. Durable state lives in an
external workspace / storage target (see
`docs/externalized-state-architecture.md`).

## 2. Policy table

| Concern | Status now | Notes |
|---|---|---|
| React component state | **Allowed** | Transient, in-memory only. |
| Selected tab / view | **Allowed** | Transient UI state. |
| Selected action preview | **Allowed** | Phase 13E `useState<ActionPreviewId \| null>`. |
| Selected run | **Allowed** | Transient UI state. |
| Transient error / loading state | **Allowed** | Transient UI state. |
| Durable project state | **Forbidden** | Lives in the workspace. |
| Pipeline-run history | **Forbidden** | Lives in the workspace. |
| Audio / generated artifacts | **Forbidden** | Lives in the workspace. |
| Action history | **Forbidden** | Lives in the workspace. |
| Audit log | **Forbidden** | Lives in the workspace. |
| Exported read model as browser-owned source of truth | **Forbidden** | The export is a derived read model, not a browser-owned database. |
| Local workspace config | **Forbidden** | Lives in the workspace. |
| Provider credentials | **Forbidden** | Never browser-owned (see `docs/storage-targets-architecture.md`). |
| Provider sync metadata | **Forbidden** | Lives in the workspace / future bridge. |
| Secrets | **Forbidden** | Never in the browser. |
| Large blobs | **Forbidden** | Lives in the workspace. |
| Unbounded caches | **Forbidden** | No accreting browser cache. |
| `localStorage` | **Forbidden** | No durable browser key-value store. |
| `sessionStorage` | **Forbidden** | No durable browser key-value store. |
| `IndexedDB` | **Forbidden** | No browser database. |

## 3. Why (RoundTable failure-mode avoidance)

Browser storage such as `localStorage`, `sessionStorage`, and `IndexedDB`
remains forbidden because allowing durable project state to accrete in the
browser is exactly how RoundTable became unrecoverable: state grew until the
browser was the database, with no clean export, reset, backup, or recovery
path. StoryTime forbids that class of growth at the policy level.

## 4. Gate for any future browser persistence

If a future phase ever wants browser persistence (even for a small, bounded
purpose), it must FIRST establish, under an explicit phase gate:

- a **size limit**,
- a **clear / reset control** the operator can use,
- an **export path** (the data can be exported out of the browser),
- a **recovery path** (the data can be rebuilt from the workspace, so the
  browser copy is never the only copy),
- a **privacy / security review**,
- a **visible storage status** (the operator can see what is stored and how
  much).

Absent all of the above, browser persistence stays forbidden.

## 5. Enforcement

- The repository no-storage grep
  (`grep -rn "localStorage\|sessionStorage\|IndexedDB" frontend/src`) must find
  only negation / disclaimer context, never a real call.
- The state-discipline guard forbids any current-state doc from claiming
  Phase 13F implements browser storage, `localStorage`, `sessionStorage`, or
  `IndexedDB`.
- Phase 13F adds no browser storage and no runtime code; this policy is the
  contract a future phase must honour.
