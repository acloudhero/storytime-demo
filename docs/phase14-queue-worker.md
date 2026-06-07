# Phase 14C.1 — Local Durable Queue / Worker Shape

> **Current state:** Phase 14C.1, 14C.2, 14C.3, 14C.4, 14C.5.1, and 14D are
> **LOCKED** (14D is the last locked phase; 14D locked using
> `storytime-phase14d-cloud-distributed-architecture-baseline.tar.gz`, SHA-256
> `a4ccc8aa59beaf6365081973d1c3d78235df028ef0f3214979e9d3b98f4dcce6`). Phase 14D — Cloud / Distributed
> Architecture Baseline from Proven Local Contracts — was the documentation-and-mapping
> round and is now **LOCKED**. With Phase
> 14C.5.1 locked, a failed run can be durably and explainably linked to a bounded
> recovery execution via the backend-owned `recovery_action` lineage table,
> eligibility policy, duplicate-prevention/attempt limits, and recovery
> read-model (see `docs/phase14-contracts-as-built.md` Section M and
> `docs/phase14-cloud-queue-mapping.md`). The Phase 14C.4 observer events remain
> explanatory only and are not the recovery-lineage source of truth. This
> document remains the architectural overview of the locked 14C.1 queue/worker
> spine.


Phase 14C.1 separates request **acceptance** from **execution** in the local-live
proof loop. It is a LOCAL durable queue/worker shape proof — not a cloud queue,
a distributed system, or an external broker.

## 1. The shift

```text
Before (14A.1/14B.1):
  POST /api/proof-runs  →  execute proof run inline  →  return terminal result

After (14C.1):
  POST /api/proof-runs  →  reserve run + enqueue durable work item  →  202 queued
  local worker          →  claim → running → execute → completed | failed
  read model            →  exposes the durable lifecycle
```

The honest claim: *StoryTime now has a local durable queue and local worker
execution shape that separates request acceptance from execution and preserves
backend-owned, restart-durable proof-run state.* It is **not** cloud execution
and **not** a distributed system.

## 2. Queue port + SQLite adapter

The queue is a replaceable **port** (`storytime.local_live.queue.WorkQueue`, a
`typing.Protocol`) with a **SQLite adapter** (`SqliteWorkQueue`) as the first
local implementation. The port is queue-shaped, not SQLite-shaped: a future
hosted/distributed adapter could implement the same contract without changing
callers. The adapter delegates to the existing `StateStore`, so the queue uses
the same durable SQLite source-of-truth, WAL journalling, and migration
discipline as the rest of the system (new `work_queue` table, schema migration
6, additive and idempotent).

Contract: `enqueue`, `claim`, `mark_running`, `mark_completed`, `mark_failed`,
`recover_stale`, `get`, `list_items`. Lifecycle:

```text
queued → claimed → running → completed
queued → claimed → running → failed
```

## 3. Local worker

`storytime.local_live.worker.LocalWorker` is a single bounded worker:
`run_once()` claims one item, marks it running, executes the existing
backend-owned proof logic (`execute_proof_run`), and reconciles the work item to
the run's durable terminal state; `drain()` processes the queue until empty. The
running `storytime local-live` server attaches **one** `BackgroundWorker`
daemon thread that drains on a bounded interval so the operator gets results
without the browser polling. Tests drive `LocalWorker` synchronously for
determinism. There is no worker pool, process supervisor, or external broker.

## 4. Atomic claim, lease recovery, no double execution

- **Atomic claim:** `claim_next_work` runs under `BEGIN IMMEDIATE` and updates a
  row conditionally on `state='queued'`, so concurrent claimers serialise and
  only one wins an item — no double-claim.
- **Lease / stale-claim recovery:** a claimed/running item carries a lease
  expiry. If a worker is lost (crash/interruption) the lease expires;
  `recover_stale` requeues the item (or fails it after `max_attempts`) so
  another worker can pick it up.
- **No double execution:** `execute_proof_run` is idempotent per run — if stage
  executions already exist for the run, it returns without re-running. So a
  recovered or redelivered work item never causes the run to execute twice.

This is local durable claim/recovery behaviour with no duplicate execution under
the tested local worker model — deliberately **not** advertised as full
distributed exactly-once execution.

## 5. Safe read model

The read model exposes the lifecycle the operator needs — `queued`, `running`,
`completed`, `failed`, scenario, attempts, work id, timestamps — and the run's
own status reflects the same lifecycle. The claim/lease mechanics (owner, lease
expiry) are adapter-internal and are **never** exposed: no lease tokens, no
owners, no database internals, no absolute paths. Health reports
`execution: queued-then-local-worker` plus per-state queue counts.

## 6. Boundaries (unchanged from 14A.1/14B.1)

The browser only requests and may trigger only allowlisted scenarios (no
arbitrary text, paths, URLs, providers, credentials, failure messages, or stage
mutation). The local-live API binds loopback-only with a strict origin allowlist
(no wildcard CORS). No browser durable storage; no WebSocket/EventSource; the
frontend uses one bounded post-run refresh plus manual refresh, not polling.

## 7. Where this sits on the cloud path

Phase 14A.1 proved local execution; 14B.1 hardened operator trust; **14C.1
proves the local durable queue/worker execution shape**. The contracts this
round establishes (a queue port, durable lifecycle, worker reconciliation) are
the seams a future hosted/distributed system would implement — but that
documentation-of-contracts-as-built is **Phase 14C.2**, object storage is
**14C.3**, and actual cloud/distributed work is later still. Nothing cloud,
distributed, provider, audio, RSS, or auth is implemented here.
