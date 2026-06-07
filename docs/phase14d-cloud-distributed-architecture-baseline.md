> **Phase 14D — Cloud / Distributed Architecture Baseline from Proven Local Contracts (LOCKED).** Phase 13 is CLOSED; **Phase 14A.1, 14B.1, 14C.1, 14C.2, 14C.3, 14C.4, 14C.5.1, and 14D are LOCKED** (Phase 14D is the last locked phase; the Phase 14C sequence is locked / complete through 14C.5.1; Phase 14D locked via `storytime-phase14d-cloud-distributed-architecture-baseline.tar.gz`, SHA-256 `a4ccc8aa59beaf6365081973d1c3d78235df028ef0f3214979e9d3b98f4dcce6`; Phase 14C.5.1 locked via `storytime-phase14c5-1-durable-recovery-control-plane-boundary.tar.gz`, SHA-256 `73a9ee1bdcbca295037f4852375d3f6b1ff155c3a0ea9d1b0fe498de3862e604`). Phase 14 — Live System / Cloud-Distributed — is STARTED. **Phase 14D is an as-built architecture *mapping* phase: it maps the locked local contracts into a future cloud/distributed architecture baseline and implements no cloud/distributed behavior.** Phase 14D adds no dependency. Provider TTS, frontend audio understanding, RSS publishing, and local content-production closure are deferred future work and are **not** the active Phase 14D scope. Phase 14E remains **NOT STARTED**. Phase 15 remains **NOT STARTED**.

# Phase 14D — Cloud / Distributed Architecture Baseline from Proven Local Contracts

This is the grounded cloud/distributed architecture baseline for StoryTime. It is
derived from the local contracts proven through Phase 14C.5.1, not from a
greenfield cloud design. It exists to make Phase 15 narrower, safer, and more
obvious — not to make Phase 15 unnecessary, and not to build the cloud.

The discipline is:

```text
Build local behavior before mapping cloud architecture.
Map cloud architecture before building cloud behavior.
```

It builds on two earlier documents and broadens them to the full proven surface:

- `docs/phase14-cloud-queue-mapping.md` — the Phase 14C.5.1 cloud-queue / recovery
  mapping *contract* (queue, recovery lineage, eligibility, artifact key, observer).
- `docs/phase14-cloud-distributed-roadmap.md` — earlier future-boundary roadmap
  notes (local-live first; future service boundaries; invariants carried forward).

The deferred cloud/distributed work is tracked in
`docs/phase14d-deferred-cloud-work-register.md`.

---

## 1. Purpose

Phase 14D answers, from real implementation evidence rather than imagination:

- What does each proven local contract become in a future cloud/distributed deployment?
- What stays adapter-shaped (a port whose local adapter is swapped, not redesigned)?
- What must become a separate deployable service?
- What local assumptions break in a distributed system?
- What must remain backend-owned?
- What must never move into frontend/browser state?
- What future infrastructure choices remain deferred?
- What evidence must Phase 15 provide before cloud behavior is trusted?

The winning outcome is a baseline that states honestly: here is what StoryTime has
proven locally; here is what each proven local contract becomes in cloud; here is
what stays backend-owned; here is what must not move into the browser; here is what
infrastructure is deferred; here is what Phase 15 must prove first.

---

## 2. Non-goals

Phase 14D does **not** implement cloud/distributed behavior. Concretely, this phase
does not add, and this document does not describe as existing:

- No external broker (no Redis, NATS, SQS, Temporal, Celery, RabbitMQ, Kafka).
- No distributed worker runtime, worker pool, process supervisor, or orchestrator.
- No cloud object storage (no S3, no MinIO, no GCS/Azure Blob), no signed URLs, no
  public artifact serving.
- No auth / OAuth / JWT / user accounts / API keys / session boundary.
- No public ingress, no networked operator API, no cloud API runtime.
- No cloud recovery orchestration, no automatic retries, no exponential backoff, no
  retry scheduler, no dead-letter queue, no distributed lock, no cloud lease.
- No OpenTelemetry exporter wiring beyond what already exists in the repo, no
  collector configuration, no Prometheus/Grafana/Tempo/Loki/Dynatrace/Datadog/New
  Relic integration, no dashboards, no alerting, no SLOs.
- No provider-backed TTS, no real provider credentials, no audio playback/serving,
  no RSS publishing, no local content-production closure.
- No cloud mode toggle, no browser-controlled deployment selection, no mode switching.
- No polling, no WebSockets, no EventSource, no browser durable storage, no general
  frontend control plane.
- No expansion of the Phase 14C.4 observer event schema.
- No new runtime or dev dependency; no edit to `pyproject.toml`, `uv.lock`,
  `package.json`, or `package-lock.json` to add a dependency.

Where earlier roadmap intent (the provider-TTS / frontend-audio / RSS
content-production arc) differs from the locked implementation, the locked
implementation is preserved and the delta is recorded: that arc is **deferred
future work**, not the active Phase 14D scope, and was previously mis-labelled as
"Phase 14D.1–14D.4" in stale roadmap language now corrected.

---

## 3. As-built mapping principle

This is an **as-built mapping**, not an idealized architecture. Every row starts
from a proven local implementation surface and maps it forward using one frame:

```text
Local proven contract -> future cloud/distributed equivalent -> assumptions -> risks -> deferred implementation
```

Two rules keep it honest:

1. **Do not design from imagination.** If a concept is not already proven in the
   locked local code, it is described as a *future* concern and listed in the
   deferred register, not asserted as designed.
2. **Preserve the port shape.** Several local surfaces are already replaceable
   ports (`WorkQueue`, `ArtifactStore`, `StorageAdapter`, `QueueWorkerEventSink`).
   The cloud equivalent is a *new adapter behind the same port*, not a rewrite.
   What is genuinely new in cloud (a networked API, auth, distributed claim
   safety) is called out explicitly as new, with its risks.

The architecture must remain minimal. No service is introduced merely because cloud
diagrams usually have one.

---

## 4. Locked local contract inventory

The proven surfaces this baseline maps (all locked through Phase 14C.5.1):

| Local surface | Source (as-built) | Shape | What it proves locally |
| --- | --- | --- | --- |
| Local bridge / local-live API | `src/storytime/local_bridge/`, `src/storytime/local_live/server.py` | loopback-only HTTP, versioned allowlisted action DTO, command-router, 202-accepted | request acceptance is separate from execution; the backend validates; the browser never sends free-form commands |
| WorkQueue (port) + `SqliteWorkQueue` (adapter) | `src/storytime/local_live/queue.py` | `enqueue/claim/mark_*/recover_stale`; states `queued → claimed → running → completed/failed`; `owner`+lease | durable work identity, claim/lease semantics, stale-claim recovery, no-double-execution under the local worker |
| Local worker | `src/storytime/local_live/worker.py` | single in-process worker; optional single daemon-thread drain loop | claim → run → reconcile to the run's durable terminal state |
| ArtifactStore (port) + `LocalFilesystemArtifactStore` (adapter) | `src/storytime/local_live/artifact_store.py` | logical `artifact_key`; safe `ArtifactEvidence`; key validation | artifacts are backend-owned behind a storage-neutral contract; the browser never learns paths or credentials |
| Pipeline `StorageAdapter` (port) | `src/storytime/adapters/storage/base.py` | key-addressed read/write; atomic `write_text_atomic` | the feed/artifact write seam is already object-store-shaped (Architecture Baseline §19) |
| Recovery control plane | `src/storytime/local_live/recovery.py` | durable `recovery_action` table; backend eligibility policy; duplicate-prevention; bounded attempts | recovery lineage is durable backend state and decided in the backend, never the browser |
| Observability boundary | `src/storytime/local_live/observability.py`, `src/storytime/events/model.py` | `QueueWorkerEvent` + sink ports; vendor-neutral names; fail-soft `emit` | a queue/worker lifecycle is explainable from explanatory-only events that are never the source of truth |
| Read model / operator visibility | `src/storytime/local_live/read_model.py` | read-only DTO projection of SQLite; bounded metadata only | the operator surface is a projection of backend truth, never the source of truth, and never raw text |

Two invariants hold across every row and are repeated throughout this document:

- **SQLite (durable backend state) is the source of truth.** Read models and
  observer events are derived views; neither is authoritative.
- **The backend owns truth, durable state, artifact storage, observation, and
  recovery eligibility.** The browser may request and may trigger only allowlisted
  scenarios; it decides nothing consequential.

---

## 5. Future deployable service shape

The minimal future shape — described, not built. For each component: responsibilities,
owned data, what it does not own, local equivalent, future adapter/interface, known
risks, and the deferred phase that would implement it.

### 5.1 API service

- **Responsibilities:** terminate ingress; authenticate and authorize the operator;
  validate the versioned action DTO; route allowlisted actions to handlers; return
  `202 Accepted` with an action/job identity; serve bounded read projections.
- **Owns:** request validation and admission. **Does not own:** the work queue,
  artifact bytes, recovery eligibility *truth* (it calls the backend policy), or the
  durable state.
- **Local equivalent:** the loopback-only local bridge / `local_live` server
  (`http.server`, strict origin policy, no wildcard CORS, single submittable action
  `retry_failed_stage`).
- **Future adapter/interface:** a networked HTTP API in front of the same handlers;
  an auth boundary; a network boundary; a request-validation boundary; a deployment
  ingress.
- **Known risks:** exposing the loopback assumption to the network without auth;
  wildcard CORS; letting the API become a second source of truth.
- **Deferred phase:** Phase 15A (runtime skeleton) and a later auth boundary.
- **Must state:** Phase 14D does not implement auth; does not implement public
  ingress; does not expose the local bridge to the network; does not implement a
  cloud API runtime.

### 5.2 Worker service

- **Responsibilities:** claim work; execute the pipeline; reconcile work-item state
  to the run's durable terminal state; emit explanatory lifecycle events.
- **Owns:** execution. **Does not own:** work identity issuance (the queue does),
  artifact authority (the store does), or recovery decisions (the backend policy does).
- **Local equivalent:** the single in-process `local_live` worker (synchronous in
  tests; one daemon thread under the running server).
- **Future adapter/interface:** a separately deployable worker process, replica-safe,
  with idempotent stage execution and clean shutdown/restart.
- **Known risks:** duplicate execution across replicas; non-idempotent stages;
  partial-execution on crash; clock skew between workers.
- **Deferred phase:** Phase 15B.

### 5.3 Durable database

- **Responsibilities:** be the single source of truth for runs, stage executions,
  events, artifact metadata, work-item lifecycle, and recovery lineage.
- **Owns:** all durable domain state. **Does not own:** artifact bytes (it holds
  metadata/keys, not blobs) or telemetry.
- **Local equivalent:** SQLite via `StateStore` (WAL, schema-versioned migrations,
  `BEGIN IMMEDIATE` for the atomic recovery slot).
- **Future adapter/interface:** a managed relational database behind the same
  `StateStore`-shaped contract; migrations promoted to a disciplined migration tool.
- **Known risks:** SQLite single-writer locking assumptions do not hold under many
  concurrent writers; reconstructing lineage from telemetry instead of the database.
- **Deferred phase:** Phase 15A/15E.

### 5.4 Queue / broker

- **Responsibilities:** hold durable work identity; hand a claim/lease to one worker;
  support ack/fail/redelivery.
- **Owns:** in-flight work identity and lease state. **Does not own:** run truth
  (the database does) or recovery eligibility.
- **Local equivalent:** `SqliteWorkQueue` behind the `WorkQueue` port.
- **Future adapter/interface:** a managed broker queue implementing the same
  `WorkQueue` port (the queue itself, not its internals leaking outward).
- **Known risks:** at-least-once delivery causing duplicate execution; visibility
  timeouts shorter than stage runtime; broker semantics leaking into the domain.
- **Deferred phase:** Phase 15B.

### 5.5 Artifact / object storage

- **Responsibilities:** store artifact bytes; return safe, non-sensitive evidence.
- **Owns:** artifact bytes. **Does not own:** artifact *metadata of record* (the
  database does) or key authority (the backend mints logical keys).
- **Local equivalent:** `LocalFilesystemArtifactStore` behind `ArtifactStore`, and
  the pipeline `StorageAdapter`.
- **Future adapter/interface:** an object-storage adapter implementing the same
  port; an artifact-metadata table of record; server-side artifact authority.
- **Known risks:** URL/key leakage; the browser becoming the key authority; the
  browser writing directly to storage; signed URLs without server-side control.
- **Deferred phase:** Phase 15C.
- **Must state:** Browser/frontend must not become the authority for artifact keys;
  must not write directly to artifact storage in the initial cloud proof. Phase 14D
  does not implement S3, MinIO, signed URLs, or cloud object storage.

### 5.6 Observability collector / export path

- **Responsibilities:** receive explanatory lifecycle events; export to a
  vendor-neutral collector and onward to a vendor.
- **Owns:** telemetry. **Does not own:** any domain truth — telemetry is a view over
  the event_log and lifecycle, never its source.
- **Local equivalent:** `QueueWorkerEvent` + `QueueWorkerEventSink`
  (`NullQueueWorkerObserver` default; `InMemoryQueueWorkerObserver` for tests);
  fail-soft `emit`.
- **Future adapter/interface:** a sink adapter that maps StoryTime-native events to
  OpenTelemetry traces/spans/logs/metrics, a collector, and an exporter; resource
  attribution per environment.
- **Known risks:** vendor semantic conventions back-propagating into the domain
  model; treating telemetry as the retry/recovery source of truth.
- **Deferred phase:** Phase 15D.

### 5.7 Operator frontend / static console

- **Responsibilities:** render bounded backend-owned read projections; offer the
  allowlisted actions; show failure and recovery state.
- **Owns:** display state only. **Does not own:** any backend state — it invents
  nothing and persists nothing operational in the browser.
- **Local equivalent:** the static operator console reading the read model with one
  bounded post-run refresh plus manual refresh (no polling).
- **Future adapter/interface:** a mode-aware console talking to cloud-safe read APIs.
- **Known risks:** the frontend becoming a source of truth; browser durable storage;
  polling/streaming creeping in.
- **Deferred phase:** Phase 15A+ (read APIs), with operator-mode UX later.

### 5.8 Configuration / secrets layer

- **Responsibilities:** supply environment/workspace configuration and (in cloud)
  secrets.
- **Owns:** configuration values and secret material. **Does not own:** domain state.
- **Local equivalent:** `src/storytime/config.py`, `.env.example`, `storytime.toml`,
  `storytime doctor` (which reports the active deployment/slot/state-root and never
  prints secrets).
- **Future adapter/interface:** a secrets manager and per-environment configuration;
  secrets never in the browser, never in telemetry, never in artifact metadata.
- **Known risks:** secrets leaking into logs, telemetry, or artifact evidence;
  configuration drift between blue/green environments.
- **Deferred phase:** a later auth/secrets boundary (post-15A).

---

## 6. Contract-by-contract mapping

Each subsection uses the as-built frame: **local proven contract → future
cloud/distributed equivalent → assumptions → risks → deferred implementation**, and
includes the explicit boundary statements this phase must record.

### 6.A Local API / Bridge boundary

- **Local proven contract:** a loopback-only HTTP bridge (`127.0.0.1`/`::1`,
  refusing all-interfaces and non-loopback binds), a strict origin policy (no
  wildcard `Access-Control-Allow-Origin`; `403` on mismatch), a versioned
  allowlisted action-request DTO (never free-form command / SQL / file path), a
  command-pattern router to exactly one pre-approved handler, and `202 Accepted`
  with an `actionRequestId`/`jobId` executed on a single-concurrency worker —
  acceptance is never success. Backend-owned validation.
- **Future equivalent:** a cloud API service; a controlled, networked operator API;
  an auth boundary; a network boundary; a request-validation boundary; a deployment
  ingress.
- **Assumptions:** request acceptance stays separate from execution; the action
  vocabulary stays allowlisted and versioned; validation stays backend-owned.
- **Risks:** exposing the loopback-only assumption to the network without auth;
  wildcard CORS; free-form commands; acceptance being read as success.
- **Deferred implementation:** the networked API runtime and the auth boundary.
- **Must state:** Phase 14D does not implement auth; does not implement public
  ingress; does not expose the local bridge to the network; does not implement a
  cloud API runtime.

### 6.B WorkQueue boundary

- **Local proven contract:** the `WorkQueue` port with the `SqliteWorkQueue` adapter.
  `enqueue(work_id, pipeline_run_id, scenario, fixture_id)`; `claim(owner,
  lease_seconds)`; `mark_running/mark_completed/mark_failed(work_id, owner, …)`;
  `recover_stale(max_attempts)`; `get`/`list_items`. Lifecycle `queued → claimed →
  running → completed/failed`. `claimed_by`/`owner`, `claimed_at`, and
  `lease_expires_at` are lease mechanics; `owner` is adapter-internal and is **not**
  part of the safe read model. Stale-claim recovery requeues or fails an item whose
  lease expired (`DEFAULT_LEASE_SECONDS = 30`, `DEFAULT_MAX_ATTEMPTS = 5`).
- **Future equivalent:** a broker/job queue; message/job identity; a lease or
  visibility timeout; worker ownership; ack/fail semantics; reclaim behavior;
  idempotency expectations.
- **Assumptions:** durable work identity; claim/lease semantics; retry visibility;
  the queue port is the seam, so a managed broker is a new adapter, not a rewrite.
- **Risks:** duplicate execution under distributed workers (at-least-once delivery);
  visibility timeout shorter than stage runtime; broker internals leaking into the
  domain model.
- **Deferred implementation:** the broker adapter and distributed claim safety.
- **Must state:** Phase 14D does not implement Redis; does not implement NATS; does
  not implement SQS; does not implement Temporal; does not implement Celery; does
  not implement any external broker.

### 6.C Worker boundary

- **Local proven contract:** a single in-process `local_live` worker
  (`DEFAULT_WORKER_OWNER = "local-worker"`) that claims a queued item, marks it
  running, executes the backend-owned proof-run logic, and marks it completed/failed,
  reconciling the work item to the run's durable terminal state. The optional
  background loop is one daemon thread draining on a bounded interval; tests drive it
  synchronously for determinism. It is **not** an external-broker worker, a cloud
  worker, a distributed worker pool, a process supervisor, or a
  Celery/Temporal-style orchestrator.
- **Future equivalent:** a separately deployable worker service; replica-safe
  execution; distributed claim safety; idempotent stage execution; defined
  shutdown/restart behavior.
- **Assumptions still unsafe for distributed execution (must be addressed in
  Phase 15+):**
  - Single-process / single-machine claim safety: today, "no double execution" holds
    because there is one local worker and SQLite arbitration. With multiple replicas
    this depends entirely on the broker lease + idempotent stages, which do not exist
    yet.
  - Stage idempotency is not guaranteed end-to-end for re-execution after a partial
    crash across machines; locally it is bounded by stale-partial recovery on one host.
  - Worker identity (`owner`) is a local string, not an authenticated, unique,
    fenced identity.
  - Lease duration is a fixed local default, not tuned to real stage runtimes.
- **Risks:** duplicate execution; non-idempotent side effects; partial execution on
  crash; clock skew.
- **Deferred implementation:** the distributed worker runtime and idempotency proof.

### 6.D ArtifactStore boundary

- **Local proven contract:** the `ArtifactStore` port with `LocalFilesystemArtifactStore`.
  Storage-neutral terms only — `artifact_key`, `content`, `content_hash`,
  `media_type`, `size_bytes`, `metadata`, `created_at` — and safe `ArtifactEvidence`
  that never carries an absolute path, storage root, credential, bucket, or URL.
  `normalize_artifact_key` enforces relative POSIX keys with no drive letter, no
  leading separator, no backslashes, and no `.`/`..` segments; atomic writes; safe
  evidence; deterministic missing behavior. The pipeline `StorageAdapter` is the same
  shape (key-addressed, atomic feed publish).
- **Future equivalent:** an object-storage adapter; bucket/container identity; object
  key mapping; an artifact-metadata table of record; signed-URL considerations;
  server-side artifact authority.
- **Assumptions:** `artifact_key` remains logical and non-path-authoritative; the
  backend mints keys; evidence stays free of paths/URLs/credentials.
- **Risks:** URL/key leakage; the browser becoming the key authority; the browser
  writing directly to storage.
- **Deferred implementation:** the S3/MinIO/cloud object-storage adapter and any URL
  strategy.
- **Must state:** Browser/frontend must not become the authority for artifact keys;
  must not write directly to artifact storage in the initial cloud proof. Phase 14D
  does not implement S3; does not implement MinIO; does not implement signed URLs;
  does not implement cloud object storage.

### 6.E Recovery control plane boundary (Phase 14C.5.1)

- **Local proven contract:** the durable `recovery_action` table is the **source of
  truth** for recovery lineage. `RecoveryActionRecord` carries `recovery_action_id`,
  `original_run_id`, `original_work_item_id`, `recovery_run_id`,
  `recovery_work_item_id`, `recovery_reason`, `requested_by`, `requested_at`,
  `status`, `decision`, `rejection_reason`, `attempt_number`, `updated_at`.
  `evaluate_recovery_eligibility` is a backend-owned policy returning a bounded
  decision (`retry_eligible`, `not_failed`, `unknown_original`, `duplicate_recovery`,
  `max_attempts_reached`, `blocked_by_governance`, `in_progress`, `terminal_failure`)
  with a durable reason; statuses are `requested`/`created`/`rejected`/`failed`.
  Duplicate active recovery is prevented atomically under SQLite (`BEGIN IMMEDIATE`
  active slot); attempts are bounded (`DEFAULT_MAX_RECOVERY_ATTEMPTS = 1`); a
  governance failure is terminal; rejected requests are durably visible with their
  decision/reason. A caller/frontend can request recovery but can never decide whether
  it is allowed.
- **Future equivalent:** a durable recovery/audit table; distributed retry-request
  identity; operator-action audit; workflow lineage; cloud worker replacement
  execution; a retry-eligibility service or module.
- **Assumptions:** the retry/recovery source of truth stays durable backend state;
  eligibility stays backend-owned.
- **Risks:** reconstructing lineage from telemetry instead of the database; letting a
  client decide eligibility.
- **Deferred implementation:** distributed recovery orchestration.
- **Must state:** Recovery lineage remains durable backend state; must not be
  reconstructed from telemetry. Recovery eligibility remains backend-owned; the
  frontend/browser does not decide retry eligibility. Phase 14D does not implement
  distributed recovery orchestration; does not implement automatic retries; does not
  implement scheduling/backoff/DLQ.

### 6.F Observability boundary (Phase 14C.4)

- **Local proven contract:** `QueueWorkerEvent` with the vendor-neutral lifecycle
  vocabulary `work.enqueued → work.claimed → work.started → stage.started →
  stage.completed → artifact.recorded → work.completed | work.failed` and safe fields
  (`run_id`, `work_item_id`, `stage_name`, `artifact_key`, `status`,
  `failure_reason`, `worker_id`, `attempt_number`) — never raw text, secrets,
  credentials, filesystem paths, artifact roots, or signed URLs. `QueueWorkerEventSink`
  is the port; `NullQueueWorkerObserver` is the default no-op; `InMemoryQueueWorkerObserver`
  is an ephemeral recorder for tests. `emit` is fail-soft (a sink error never breaks
  the proof loop). Internal `PipelineEvent`/`event_log` is persisted before telemetry;
  telemetry is a view over that data, never its source.
- **Future equivalent:** an OpenTelemetry mapping; a collector/exporter path;
  vendor-neutral telemetry; resource attribution; a trace/span/log/metric strategy;
  dashboard/alerting future boundaries.
- **Assumptions:** the internal event vocabulary stays StoryTime-native and
  schema-stable.
- **Risks:** vendor semantic conventions leaking into the domain model; treating
  events as the retry/recovery source of truth.
- **Deferred implementation:** the OpenTelemetry SDK/exporter integration and collector.
- **Must state:** `QueueWorkerEvent` remains explanatory, not authoritative; it is
  not the retry/recovery source of truth. Vendor telemetry semantics must not
  back-propagate into StoryTime's internal domain model. Phase 14D does not add
  OpenTelemetry SDK integration unless it already exists; does not add collector
  configuration; does not add Prometheus/Grafana/Dynatrace/Datadog/New Relic
  integration; does not add dashboards; does not add alerting/SLOs.

> Note (as-built): `opentelemetry-api`/`-sdk`/`-exporter-otlp-proto-http` are already
> locked dependencies (`pyproject.toml`) and a telemetry adapter already exists at
> `src/storytime/adapters/telemetry/`, confined by an import-linter contract. Phase
> 14D neither adds nor expands that integration; it only documents how the
> queue/worker `QueueWorkerEvent` vocabulary would *map* outward in a future phase.

### 6.G Read model / operator visibility boundary

- **Local proven contract:** a read-only, deterministic DTO projection
  (`read_model.py`) of the backend-owned SQLite state (`pipeline_run`,
  `stage_execution`, `event_log`, `stage_artifact`, recovery actions) into a small,
  safe JSON shape. It exposes bounded metadata only — ids, statuses, stage names,
  timestamps, artifact keys/hashes/sizes, small event payloads — and never raw story
  text. It never invents a status (`KNOWN_STATUSES` is bounded; unknown statuses pass
  through verbatim). The operator console performs one bounded post-run refresh plus
  manual refresh — not a live sync — and does not poll.
- **Future equivalent:** a backend-owned query projection; an operator console; a
  mode-aware UI; controlled action visibility; cloud-safe read APIs;
  eventual-consistency considerations.
- **Assumptions:** the read model stays a projection, never the source of truth.
- **Risks:** the frontend inventing backend state; persisting operational state in
  the browser; the frontend becoming the source of truth for recovery/queue/artifact/
  observability data.
- **Deferred implementation:** cloud read APIs and operator mode.
- **Must state:** Frontend must not invent backend state; must not persist
  operational state in browser storage; must not become the source of truth for
  recovery, queue, artifact, or observability data. Phase 14D does not implement a
  cloud operator mode; does not implement polling/WebSockets/EventSource.

---

## 7. Data ownership boundaries

Source of truth, allowed writers/readers, future cloud owner, and what must **never**
own each datum. "Backend" means a backend service/handler/policy, never the browser.

| Datum | Source of truth | Allowed writers | Allowed readers | Future cloud owner | Must NOT be owned by |
| --- | --- | --- | --- | --- | --- |
| Runs (`pipeline_run`) | durable DB (SQLite) | backend proof-run / worker | backend read model / API | managed durable DB | frontend, telemetry, object storage |
| Work items (`work_queue`) | durable DB | backend queue adapter | backend worker / read model | broker + DB | frontend, telemetry |
| Stage executions | durable DB | backend worker / stages | backend read model | managed durable DB | frontend, telemetry |
| Artifacts (bytes) | artifact store | backend `ArtifactStore` adapter | backend (mediated) | object storage | frontend (no direct writes), telemetry |
| Artifact metadata (`artifact_key`, hash, size) | durable DB + safe evidence | backend artifact store / store | backend read model / operator | DB (metadata of record) | frontend as authority, object storage as authority |
| Queue/worker lifecycle state | durable DB (work item) | backend queue/worker | backend read model | broker + DB | frontend, telemetry as source |
| Recovery lineage (`recovery_action`) | durable DB | backend recovery action handler | backend read model / operator API | durable workflow/audit table | frontend, telemetry, object storage |
| Recovery eligibility decisions | backend policy (computed from DB) | backend eligibility policy | backend / operator API | backend admission/eligibility service | frontend/browser, telemetry |
| Operator actions | durable DB / append-only audit | backend action handler | backend read model | DB audit | frontend as authority |
| Observability events (`QueueWorkerEvent`) | ephemeral / explanatory only | backend `emit` → sink | sink / future collector | telemetry backend (view only) | the domain model (never the source of truth) |
| Configuration | config layer | operator/deploy | backend | per-environment config | frontend, telemetry |
| Secrets | secrets layer (future) | deploy/secrets manager | backend only | secrets manager | frontend, telemetry, artifact metadata, logs |
| Frontend display state | the browser (display only) | frontend | frontend | the browser | the backend's source of truth (it is derived, never authoritative) |

---

## 8. Local assumptions that break in cloud

Each assumption is safe locally and classified for cloud: **safe to preserve**,
**must be replaced by adapter**, **must be redesigned**, or **deferred risk**. Phase
14D maps these; it does not solve them.

| Local assumption | Why safe locally | Cloud classification | Note |
| --- | --- | --- | --- |
| Single-process execution | one worker, one host | must be redesigned | distributed claim safety + idempotency required (15B) |
| Single-machine filesystem | artifacts on local disk | must be replaced by adapter | object-storage adapter behind `ArtifactStore` (15C) |
| SQLite single-writer locking | `BEGIN IMMEDIATE` arbitrates one writer | must be redesigned | managed DB concurrency; the atomic recovery slot must keep its guarantee (15A/15E) |
| Loopback-only API, no auth | only local processes reach it | must be redesigned | network boundary + auth (15A + later) |
| In-memory / ephemeral observability | safe, fail-soft, no storage | must be replaced by adapter | export sink adapter; still explanatory-only (15D) |
| Manual / one-shot refresh (no polling) | operator drives reads | safe to preserve (then extend) | cloud read APIs may add eventual-consistency handling; no polling mandated (15A+) |
| Operator identity placeholder (`requested_by`, `owner`) | local strings | must be redesigned | authenticated operator + fenced worker identity |
| Local timestamps / single clock | one host clock | deferred risk | clock skew across services; prefer DB/broker-authoritative ordering |
| Worker crash/restart on one host | stale-partial recovery on the host | must be redesigned | replica-safe restart + idempotent stages |
| Artifact paths under one root | one configured root | must be replaced by adapter | bucket/container namespace; keys stay logical |
| Configuration defaults / `.env` | local file | must be replaced by adapter | per-environment config + secrets manager |

---

## 9. Demo / Local / Cloud mode boundary

StoryTime's operator modes are preserved as a concept. Phase 14D **documents** them;
it does not implement mode switching, add a cloud mode toggle, or add
browser-controlled deployment selection.

### Demo mode
Safe / non-consequential; static or fixture-backed; a guided walkthrough; action
*previews* allowed; no real external side effects.

### Local mode
Real local operator workflows; loopback-only bridge; local durable state; local
artifacts; bounded, controlled actions; no cloud infrastructure.

### Cloud / Distributed mode (future)
A future distributed API/worker/queue/storage architecture; real deployment
boundaries; auth/secrets required; the operator API becomes networked; a cloud
observability path; blue/green compatibility required.

**Must state:** Phase 14D documents these modes but does not implement mode
switching; does not add a cloud mode toggle; does not add browser-controlled
deployment selection.

---

## 10. Blue/green compatibility notes

StoryTime previously chose a staged blue/green path: Option A first for faster
demo/time-to-market, Option B later after learning from Option A (see
`docs/deployment-bluegreen-option-a.md` / `-option-b.md`). The cloud/distributed
baseline must avoid blocking future blue/green. Phase 14D does not implement
blue/green, add cloud resources, or add deployment files (beyond documentation).

How the mapping stays blue/green-friendly:

- **Environment / workspace separation:** every owned datum is scoped to an
  environment; no global singletons in the contracts.
- **Blue vs green resource naming:** broker queues, buckets, databases, and
  telemetry resources carry an environment/slot prefix; the existing
  `config/deploy/active-slot` + front-door slot model is the local analogue.
- **Deployable state boundaries:** API and worker are separately deployable so a slot
  can be swapped without coupling.
- **Database migration discipline:** schema is versioned and migrations are forward-
  compatible so blue and green can run adjacent schema versions during a switch.
- **Artifact storage namespace separation:** logical keys are prefixed per
  environment; no cross-slot key collisions; keys stay non-path-authoritative.
- **Queue namespace separation:** per-environment queue identity so blue work is
  never claimed by a green worker.
- **Telemetry resource attribution:** events carry environment/slot resource
  attributes so dashboards never blend blue and green.
- **Configuration separation:** per-environment config + secrets; no shared mutable
  global config.
- **Operator visibility of active/candidate environment:** the read model / doctor
  surface should report which slot is active vs candidate (the local `storytime
  doctor` already reports deployment/slot).

---

## 11. Phase 15 readiness implications

This turns the 14D mapping into Phase 15 planning constraints. Phase 15 is **not**
designed here; this is **recommended future sequencing, not active implementation**.
Phase 15 remains NOT STARTED.

A narrow recommended sequence:

### Phase 15A — Cloud Runtime Skeleton (recommended, future)
- **Goal:** stand up an API service + worker service + managed DB skeleton that runs
  the *existing* contracts unchanged behind the existing ports.
- **Input contract from 14D:** §5 service shape; §7 ownership; the `WorkQueue`,
  `ArtifactStore`, `StorageAdapter`, `QueueWorkerEventSink` ports.
- **Non-goals:** no broker yet (in-process/DB-backed adapter is fine); no auth
  hardening beyond a minimal boundary; no real object storage.
- **Acceptance evidence:** the locked local proof loop runs in the skeleton with
  SQLite-or-managed-DB truth, no behavior change, all current guards green.

### Phase 15B — Cloud Queue / Worker Adapter (recommended, future)
- **Goal:** a managed broker behind `WorkQueue`, with a replica-safe worker.
- **Input contract from 14D:** §6.B, §6.C; the unsafe-for-distributed assumptions list.
- **Non-goals:** no DLQ, no backoff, no scheduler, no automatic retries.
- **Acceptance evidence:** no-double-execution under ≥2 workers via lease +
  demonstrated idempotent stage execution; reclaim on lease expiry.

### Phase 15C — Cloud Artifact Store Adapter (recommended, future)
- **Goal:** an object-storage adapter behind `ArtifactStore`.
- **Input contract from 14D:** §6.D; the no-browser-authority / no-direct-writes rule.
- **Non-goals:** no public serving; no signed URLs unless server-mediated.
- **Acceptance evidence:** artifacts round-trip with safe evidence only; keys stay
  logical; the browser never learns a path/URL/credential.

### Phase 15D — Cloud Observability Export (recommended, future)
- **Goal:** a sink adapter mapping `QueueWorkerEvent` to OpenTelemetry + a collector.
- **Input contract from 14D:** §6.F; explanatory-only invariant.
- **Non-goals:** events never become the source of truth; no domain back-propagation.
- **Acceptance evidence:** events export without changing the domain model; lineage
  still read from the DB, not telemetry.

### Phase 15E — Cloud Recovery Lineage Proof (recommended, future)
- **Goal:** prove recovery lineage + eligibility on the managed DB with cloud workers.
- **Input contract from 14D:** §6.E; backend-owned eligibility; duplicate-prevention.
- **Non-goals:** no automatic retry orchestration beyond bounded, backend-decided
  recovery.
- **Acceptance evidence:** duplicate-prevention holds under concurrency on the managed
  DB; eligibility stays backend-decided; rejected requests stay durably visible.

Phase 14D does not start Phase 15 and does not mark Phase 15 active.

---

## 12. Deferred cloud work register

The full deferred register (description / why deferred / depends on / risk if
implemented too early / expected future phase) is maintained in
`docs/phase14d-deferred-cloud-work-register.md`. Summary of tracked items: external
broker adapter; distributed worker runtime; object-storage adapter; auth/secrets
boundary; cloud observability export; blue/green deployment mechanics; cloud
recovery orchestration; cloud operator API; provider TTS integration; RSS publishing;
audio playback / serving; artifact URL strategy; dashboard/SLO/alerting.

---

## 13. Explicit statement — no cloud behavior implemented

Phase 14D implements **no** cloud/distributed behavior. No cloud runtime, external
broker, object-storage adapter, distributed worker runtime, auth system, provider
TTS, RSS publishing, polling/WebSockets/EventSource, observer-schema expansion, or
dependency was added. This document is an as-built *mapping* of the locked local
contracts to a future cloud/distributed architecture. The local system remains a
local-first SQLite proof; the cloud/distributed architecture described here is a
plan, and Phase 15 must provide the evidence above before any of it is trusted.
