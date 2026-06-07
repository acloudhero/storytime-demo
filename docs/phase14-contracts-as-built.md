# Phase 14C.2 — Contracts as Built (Cloud / Distributed Seam Baseline)

> **Current state:** Phase 14C.1, 14C.2, 14C.3, 14C.4, **14C.5.1, and 14D are
> LOCKED**. Phase 14D — Cloud / Distributed Architecture Baseline from Proven
> Local Contracts — was the current implementation candidate, was pending
> review, and is now **LOCKED** (locked using
> `storytime-phase14d-cloud-distributed-architecture-baseline.tar.gz`, SHA-256
> `a4ccc8aa59beaf6365081973d1c3d78235df028ef0f3214979e9d3b98f4dcce6`); it is the last locked phase. Phase 14C.5.1 — Durable Recovery
> Control Plane Boundary — was locked using
> `storytime-phase14c5-1-durable-recovery-control-plane-boundary.tar.gz`, SHA-256
> `73a9ee1bdcbca295037f4852375d3f6b1ff155c3a0ea9d1b0fe498de3862e604`. Phase 14D
> mapped these proven local contracts to their future cloud / distributed
> equivalents on paper and implemented no cloud behavior. Phase 14E and Phase 15
> are **NOT STARTED** and are **not locked** (Phase 14C.5 through 14C.10 were
> absorbed into Phase 14C.5.1 and are historical planning labels only). Phase 14
> is STARTED and not closed. Section K records the artifact-store contract (14C.3); Section L
> records the minimal queue/worker observability boundary (14C.4); Section M
> records the durable recovery control-plane boundary as built in the now-locked
> Phase 14C.5.1. The Phase 14C.4 observer events are explanatory only and are NOT
> the durable recovery-lineage source of truth.

This document records the contracts **as actually built**, so a future
cold-session reader can understand what exists, which seams are stable, and what
remains unimplemented. It is descriptive, not aspirational: every abstract
snippet below mirrors code that exists today. It documents future seams
**without implementing them** — there is no cloud adapter, no external broker,
no distributed worker pool, no cloud object store, no auth, no provider TTS, no
audio, and no RSS in the codebase.

A note on honesty used throughout: the system provides **local
no-double-execution under the tested SQLite/local-worker model**. It does not
provide exactly-once semantics across a distributed system, and nothing here
should be read as such.

---

### A. Request Acceptance Contract

`POST /api/proof-runs` is the only mutation the browser can trigger. The request
path (`src/storytime/local_live/server.py`, `LocalLiveService.create_proof_run`):

- validates that the requested scenario is in the allowlist
  (`success`, `governance_failure`, `artifact_validation_failure`);
- reserves durable run + read-model state via `reserve_proof_run`
  (`src/storytime/local_live/proof_run.py`), creating the `pipeline_run` row in
  the `queued` state and recording a `RunCreated` event;
- enqueues a durable work item via the queue port;
- returns accepted/queued state (HTTP `202`) with `runId`, `workId`, `status`,
  and `queueState`;
- **does not** execute the proof run inline — execution is performed later by a
  local worker.

Browser authority is constrained. The browser **may supply** only the currently
allowed scenario/request fields (an optional allowlisted `scenario`, and a
`fixtureId`/`fixture` alias resolved against the fixture allowlist).

The browser **may not supply**: arbitrary story text, arbitrary file paths,
arbitrary URLs, provider names, credentials, stage mutations, worker IDs, lease
tokens, database internals, queue state overrides, storage keys, auth claims,
retry lineage mutations, or observability labels. Unknown fields are rejected.

---

### B. Queue Port Contract

The queue is a replaceable **port** (`WorkQueue`,
`src/storytime/local_live/queue.py`) with a SQLite adapter as the first local
implementation. Its purpose is to separate request acceptance from execution by
durably holding one work item per accepted proof-run request.

- **enqueue:** durably insert a new item in the `queued` state.
- **claim:** atomically claim the oldest `queued` item for an owner, taking a
  lease; returns `None` if the queue is empty.
- **lifecycle states:** `queued → claimed → running → completed | failed`.
- **lease / stale-claim semantics:** a claimed/running item carries a lease;
  `recover_stale` requeues or fails items whose lease has expired.
- **completion / failure:** owner-guarded transitions to `completed` / `failed`.
- **recovery:** `recover_stale` is the requeue/fail path for expired leases.
- **read-model visibility:** item lifecycle is exposed through safe DTOs; the
  claim owner and lease expiry are adapter-internal and never exposed.

Supporting code: `src/storytime/local_live/queue.py`,
`src/storytime/state/store.py` (`work_queue` table + queue methods).

Abstract boundary (as built):

```python
from typing import Protocol

# WorkItemRecord is the persisted row shape (work_id, pipeline_run_id, scenario,
# fixture_id, state, owner, lease_expires_at, attempts, enqueued_at, updated_at,
# failure_reason). owner and lease_expires_at are adapter-internal.

class WorkQueue(Protocol):
    """Local durable work-queue port. Replaceable; SQLite is the first adapter.

    No cloud, broker, SDK, credential, or provider concepts appear in this
    contract — it is deliberately queue-shaped, not adapter-shaped.
    """

    def enqueue(
        self, *, work_id: str, pipeline_run_id: str, scenario: str, fixture_id: str
    ) -> "WorkItemRecord": ...

    def claim(
        self, *, owner: str, lease_seconds: int = ...
    ) -> "WorkItemRecord | None": ...

    def mark_running(self, *, work_id: str, owner: str) -> bool: ...

    def mark_completed(self, *, work_id: str, owner: str) -> bool: ...

    def mark_failed(self, *, work_id: str, owner: str, reason: str) -> bool: ...

    def recover_stale(
        self, *, max_attempts: int = ...
    ) -> "tuple[WorkItemRecord, ...]": ...

    def get(self, work_id: str) -> "WorkItemRecord | None": ...

    def list_items(self) -> "tuple[WorkItemRecord, ...]": ...
```

---

### C. SQLite Adapter Contract

`SqliteWorkQueue` (`src/storytime/local_live/queue.py`) is the **first local
adapter** implementing `WorkQueue`, delegating to `StateStore`
(`src/storytime/state/store.py`).

- SQLite is the current local durable adapter.
- Schema **version 6** added the `work_queue` table (additive, idempotent
  migration).
- Local claim uses SQLite transaction semantics: `BEGIN IMMEDIATE` plus a
  conditional update guarded on `state='queued'`, so concurrent claimers
  serialise and only one wins a given item.
- Local queue semantics are suitable for **local proof**, not production
  distributed execution.
- SQLite single-writer concurrency limits remain a known **local constraint**.
- This is **not** an external broker.
- This is **not** a cloud queue.

> SQLite is an adapter, not the architecture.

A future hosted/distributed adapter could implement the same `WorkQueue` port
without changing callers; no such adapter exists yet.

---

### D. Worker Execution Contract

A single bounded local worker (`LocalWorker`,
`src/storytime/local_live/worker.py`) drains the queue and performs
backend-owned execution via `execute_proof_run`
(`src/storytime/local_live/proof_run.py`).

- **role:** claim a queued item, run it, reconcile the work item to the run's
  durable terminal state.
- **claim/drain:** `run_once` processes one item; `drain` processes until the
  queue is empty or a bound is reached, recovering stale claims first.
- **transitions:** `queued → claimed → running → completed | failed`.
- **scenario execution:** the locked Phase 14B.1 scenarios (`success`,
  `governance_failure`, `artifact_validation_failure`) execute through the
  worker with unchanged durable end states.
- **ownership:** execution is worker-owned and backend-owned. The browser does
  not run workers and does not own execution.
- **bounds:** there is **no** production worker pool and **no** distributed
  worker implementation. The running server attaches one local background
  thread; tests drive the worker synchronously.

Abstract boundary (as built):

```python
from typing import Protocol

class WorkerExecution(Protocol):
    """Local bounded worker execution boundary (as built)."""

    def run_once(self) -> "WorkItemRecord | None":
        """Claim + execute one item; reconcile queue state to the run's
        terminal state. Returns None if the queue is empty."""
        ...

    def drain(self, *, max_items: int = 64) -> int:
        """Recover stale claims, then process queued items; return the count."""
        ...

    def recover_stale(self, *, max_attempts: int = ...) -> int:
        """Requeue/fail expired-lease claims; return the count recovered."""
        ...


# Backend-owned execution of a reserved run (worker calls this; the request
# path never does):
def execute_proof_run(
    store, run_id, *, runs_dir, fixture_id=None, scenario=None, fixtures_dir=None
) -> str: ...
```

---

### E. Stale Claim Recovery Contract

When a worker claims an item and is then lost **before** executing stages, the
lease expires and `recover_stale` (queue port) makes the item claimable again:

- an expired lease in `claimed`/`running` is **requeued** to `queued`
  (owner/lease cleared);
- if the item has already used up `max_attempts`, it is **failed** instead so a
  poison item cannot loop forever;
- recovery runs under a write transaction so recovery and claiming cannot race.

What is safe to claim: **local restart resilience** — a recovered item is
re-claimable, and execution remains single per run.

> Correct framing: local no-double-execution behaviour under the tested
> SQLite/local-worker model.

This is **not** exactly-once execution across a distributed system.

---

### F. Stale Partial Execution Recovery Contract

Phase 14C.1.1 added clean handling of a worker lost **after** committing one or
more stage executions but before terminal completion. When a recovered/redelivered
work item is processed for a run that already has stage executions
(`execute_proof_run` guard):

- if the run is already `completed` → **no-op** (idempotent return);
- if the run is already `failed` → **no-op** (idempotent return);
- if the run is **non-terminal** (e.g. `queued`/`running`) with existing
  stages → the run is **failed cleanly without re-executing any stage**, and a
  `RunFailed` event is appended (`lifecycle: stale-partial-recovery`);
- no new stage rows are created (no double execution);
- the read model surfaces a coherent failure reason (the failure-reason
  derivation falls back to the `RunFailed` event when there is no failed stage).

The durable reason string is exactly:

```text
local worker recovered a stale partial execution; run failed without re-executing completed stages
```

Resumable partial-stage continuation does **not** exist and is not implied by
this contract.

---

### G. Read-Model / DTO Safety Contract

The read model (`src/storytime/local_live/read_model.py`) exposes only safe
lifecycle evidence to the frontend.

Safe, browser-visible concepts: run ID, work ID, status, queue state, scenario,
stage status, failure reason, timestamps, and attempts (`LiveWorkItem` exposes
`work_id`, `state`, `scenario`, `attempts`, `enqueued_at`, `updated_at`).

Forbidden browser exposure (deliberately never serialised): absolute filesystem
paths, SQLite internals, lease tokens, claim owner secrets, worker secrets,
credentials, raw database implementation details, unsafe local paths, cloud
credentials, provider credentials, storage credentials, auth tokens,
object-store bucket names as implementation truth, database offsets, internal
worker leases, and retry mutation internals.

The claim owner and lease expiry exist only in the persistence layer; the safe
DTOs omit them by construction.

---

### H. Frontend Boundary Contract

The frontend (`frontend/src/components/LiveProofView.tsx`,
`frontend/src/data/liveProofClient.ts`):

- displays lifecycle evidence from the backend read model;
- does **not** own queue state;
- does **not** run workers;
- does **not** poll continuously — it performs one bounded post-run refresh plus
  manual refresh;
- uses **no** WebSockets;
- uses **no** EventSource;
- uses **no** browser durable storage (no localStorage/sessionStorage/IndexedDB/
  cookies);
- has **no** generic mutation/action framework — only the allowlisted
  scenario trigger;
- implies **no** cloud/distributed capability in the UI.

---

### I. Cloud/Distributed Seam Baseline

These are the seams a future hosted/distributed system could replace or extend.
They are named here as a baseline; none is implemented.

- **queue adapter seam** — `WorkQueue` port; a future hosted adapter could
  implement it. Currently only `SqliteWorkQueue` exists.
- **worker execution seam** — the local bounded worker; a future model could
  change how work is distributed.
- **artifact storage seam** — where run artifacts live; currently local files.
- **auth-capable API seam** — where an auth boundary would attach; currently
  loopback-only with an origin allowlist.
- **observability seam** — where richer queue/worker telemetry would attach.
- **hosted durable-state seam** — where durable state would move off local
  SQLite.

Explicit current truth:

- **no** cloud adapter exists yet;
- **no** external broker exists yet;
- **no** distributed worker pool exists yet;
- **no** auth exists yet;
- **no** cloud object-storage adapter, external object store, public
  artifact-serving adapter, signed-URL mechanism, S3 adapter, or MinIO adapter
  exists yet (the **local** `ArtifactStore` port + `LocalFilesystemArtifactStore`
  adapter added in the Phase 14C.3 candidate are documented in Section K);
- **no** hosted durable store exists yet;
- **no** provider TTS exists yet;
- **no** RSS publishing exists yet.

---

### J. Future Phase Dependency Map

How Phase 14C.2 informs later phases (roadmap is mutable; nothing below is
started):

```text
14C.3 — uses artifact/storage seam baseline
14C.4 — uses queue/worker lifecycle for minimal observability boundary
14C.5 — uses queue/worker lifecycle for retry/recovery lineage
14C.6 — expands observability across full path
14C.7 — defines auth-capable API boundary
14D.1+ — content production arc after local/distributed seams are stable
14E — local release candidate / full local mode closure
```

Phase 14C.3 is the current implementation candidate (pending review, NOT
locked); Phase 14C.4 and every later phase are **NOT STARTED**.

---

### K. Artifact Store Contract (Phase 14C.3)

Phase 14C.3 puts artifact handling behind a backend-owned **port**
(`ArtifactStore`, `src/storytime/local_live/artifact_store.py`) with a single
LOCAL adapter (`LocalFilesystemArtifactStore`). The browser never learns
filesystem paths or storage credentials — it sees only safe artifact evidence
(logical key, content hash, size, media type, timestamps).

- **purpose:** own artifact content behind a neutral, storage-agnostic contract.
- **terms:** `artifact_id`, `artifact_key`, `content`, `content_hash`,
  `media_type`, `size_bytes`, `metadata`, `created_at` — no bucket, region, ACL,
  signed-URL, or credential concepts.
- **key safety (adapter):** logical keys are validated/normalized; absolute
  paths, `..` traversal, backslash separators, and symlink escapes are rejected;
  artifacts stay under a configured root.
- **writes:** atomic (temp file + `os.replace`); returns `ArtifactEvidence`.
- **missing behavior:** deterministic — `read` raises `ArtifactNotFoundError`,
  `exists` returns `False`, `evidence` returns `None`.
- **routing:** the proof-run evidence artifact is written through the store
  under the logical key `{runId}/proof/evidence.json`; queue/worker semantics are
  unchanged.

Abstract boundary (as built):

```python
from typing import Protocol

# ArtifactEvidence carries only safe fields: artifact_id, artifact_key,
# content_hash, size_bytes, media_type, created_at, metadata. Never a path,
# root, bucket, URL, or credential.

class ArtifactStore(Protocol):
    """Backend-owned artifact storage port (storage-neutral terms only)."""

    def write(
        self,
        *,
        artifact_key: str,
        content: bytes,
        media_type: str | None = None,
        metadata: dict[str, str] | None = None,
        created_at: str,
    ) -> "ArtifactEvidence": ...

    def read(self, artifact_key: str) -> bytes: ...

    def exists(self, artifact_key: str) -> bool: ...

    def evidence(self, artifact_key: str) -> "ArtifactEvidence | None": ...

    def validate_key(self, artifact_key: str) -> str: ...
```

`LocalFilesystemArtifactStore` is the only adapter. **No** cloud adapter, **no**
external object store, **no** S3/MinIO adapter, and **no** public artifact
serving exist yet — those remain future work on the artifact-storage seam named
in Section I.


---

### L. Minimal Queue/Worker Observability Boundary (Phase 14C.4)

Phase 14C.4 adds a small backend-owned, **in-process** observation boundary
(`src/storytime/local_live/observability.py`) that makes the local queue/worker
lifecycle explainable. It keeps a future single-collector / vendor fan-out
possible by using vendor-neutral, schema-stable names and safe fields. It does
**not** implement the collector, exporters, dashboards, alerting/SLOs, sampling,
distributed tracing, retry/recovery lineage, or cloud/distributed execution.

- **boundary:** a `QueueWorkerEventSink` `Protocol`, a `QueueWorkerEvent`
  immutable record, a default no-op sink (`NullQueueWorkerObserver`), an
  ephemeral in-memory recorder (`InMemoryQueueWorkerObserver`), and a fail-soft
  `emit(...)` helper.
- **event names:** `work.enqueued`, `work.claimed`, `work.started`,
  `stage.started`, `stage.completed`, `artifact.recorded`, `work.completed`,
  `work.failed`. No retry/recovery, cloud, or distributed names; no
  exactly-once/cross-node claims.
- **safe fields only:** `run_id`, `work_item_id`, `stage_name`, `artifact_key`
  (logical), `status`, `failure_reason`, `worker_id`, `attempt_number`,
  `created_at`. Never a path, root, credential, secret, token, signed URL, or
  raw text.
- **emission points (synchronous, inline, fail-soft):** enqueue (request path);
  claim/started/completed/failed (worker); stage.started/completed and
  artifact.recorded (execute). Emission never changes queue/worker or
  ArtifactStore semantics; a sink error is swallowed with a bounded stderr
  diagnostic.
- **durable vs ephemeral:** ephemeral/in-process by default — no new database
  table, broker, or stream, and no schema change (decision per Section I + the
  durable-event discipline). Observation is opt-in by injecting a recorder.
- **read-model/API exposure:** none in this phase; the boundary is backend-owned
  and exposes nothing new to the browser.

Abstract boundary (as built):

```python
from typing import Protocol

# QueueWorkerEvent carries only safe fields: event_name, created_at, run_id,
# work_item_id, stage_name, artifact_key, status, failure_reason, worker_id,
# attempt_number. Optional fields are populated only when materialized.

class QueueWorkerEventSink(Protocol):
    """Backend-owned observation sink port (default no-op; in-memory for tests)."""

    def record(self, event: "QueueWorkerEvent") -> None: ...
```

This is a minimal local signal contract a later collector-oriented phase could
map outward. No collector, exporters, Prometheus endpoint, dashboards, alerting,
SLOs, sampling, distributed tracing, or cloud telemetry exist yet.

### M. Durable Recovery Control Plane Boundary (Phase 14C.5.1)

Phase 14C.5.1 adds the smallest durable, backend-owned recovery control plane on
top of the locked local queue/worker, artifact-store, and observability
boundaries. It makes the local proof "distributed-system-shaped" without becoming
distributed. It does **not** expand the Phase 14C.4 observer event schema; the
`recovery_action` table — not observer events — is the source of truth for
recovery lineage.

**Durable recovery lineage.** Schema **version 7** adds the `recovery_action`
table (additive, idempotent migration). Each row links the original failed
execution identity (`original_run_id`, `original_work_item_id`) to the new
recovery execution identity (`recovery_run_id`, `recovery_work_item_id`), plus
`recovery_reason`, `requested_by`, `requested_at`, `status`
(`requested → created | rejected | failed`), bounded `decision` /
`rejection_reason`, and `attempt_number`. The `RecoveryLineageView` read-model DTO
projects only safe, bounded fields (never a path, storage root, bucket, signed
URL, credential, or raw text) and is reconstructable after restart.

**Backend-owned eligibility policy.** `evaluate_recovery_eligibility(...)` decides,
in the backend, whether a failed run may be recovered, yielding a bounded result
`(eligible, decision, reason)`. Decisions: `retry_eligible`, `not_failed`,
`unknown_original`, `duplicate_recovery`, `max_attempts_reached`,
`blocked_by_governance`, `in_progress`, `terminal_failure`. A governance-failed
run is recognised from its durable failed `governance` stage and is blocked. A
caller/frontend can request recovery but can never decide eligibility.

**Duplicate-prevention / bounded attempts.** Duplicate active recovery is
prevented under local SQLite via an atomic `requested` slot taken with
`BEGIN IMMEDIATE` (`atomically_create_recovery_action`), mirroring the queue's
claim discipline. A small fixed default attempt limit
(`DEFAULT_MAX_RECOVERY_ATTEMPTS`) bounds total recovery actions per original
failed work item; consumed attempts are counted from durable rows. Rejected
requests are **durably visible** with their decision and reason.

**Concurrency guardrails (tested).** Two workers cannot both claim the same work
item; recovery cannot be requested while the original work is still running;
recovery creation is atomic enough to avoid duplicate active recovery under local
SQLite; existing stale-claim / stale-partial recovery remains intact. Tests use
the existing queue claim APIs and deterministic sequential race simulations
rather than introducing WAL/global-database configuration changes.

**Boundary preservation.** `QueueWorkerEvent` remains the exact Phase 14C.4 field
set with no recovery-correlation fields; recovery lineage is never reconstructed
from observer events; the Phase 14C.3 `ArtifactStore` boundary (logical keys,
safe evidence) is unchanged. No cloud queue, external broker
(Redis/NATS/SQS/Temporal/Celery), dead-letter queue, automatic retries,
exponential backoff, retry scheduler, distributed worker, cloud lease,
distributed lock, cloud object store, provider TTS, audio, RSS, or auth exists
yet — all remain deferred future work, mapped (not implemented) in
`docs/phase14-cloud-queue-mapping.md`.
