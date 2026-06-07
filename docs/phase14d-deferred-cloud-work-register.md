> **Phase 14D — Cloud / Distributed Architecture Baseline from Proven Local Contracts (current sub-phase; implementation candidate; pending review; NOT locked).** Phase 14A.1, 14B.1, 14C.1, 14C.2, 14C.3, 14C.4, and **14C.5.1 are LOCKED** (Phase 14C.5.1 is the last locked phase; the Phase 14C sequence is locked / complete through 14C.5.1). This register tracks cloud/distributed work that Phase 14D **defers**. Phase 14D records these items as future work and implements **none** of them; it adds no dependency. Phase 14E and Phase 15 are **NOT STARTED**.

# Phase 14D — Deferred Cloud / Distributed Work Register

This register lists the cloud/distributed work that the Phase 14D as-built mapping
(`docs/phase14d-cloud-distributed-architecture-baseline.md`) has identified but
deliberately **defers**. Nothing here is implemented in Phase 14D. Each entry records
its description, why it is deferred, what it depends on, the risk of implementing it
too early, and the expected future phase.

The recommended (not active) future sequencing referenced below — Phase 15A Cloud
Runtime Skeleton, 15B Cloud Queue / Worker Adapter, 15C Cloud Artifact Store Adapter,
15D Cloud Observability Export, 15E Cloud Recovery Lineage Proof — is defined in
§11 of the architecture baseline. Phase 15 remains NOT STARTED; these labels are
planning targets only.

---

## How to read this register

For every item:

- **Description** — what the cloud/distributed work would be.
- **Why deferred** — why Phase 14D does not build it now.
- **Depends on** — the local contract or prior deferred item it builds on.
- **Risk if implemented too early** — what breaks or is locked in prematurely.
- **Expected future phase** — the recommended (not active) phase that would own it.

A standing rule across every item: the backend remains the source of truth, the
browser/frontend never becomes authoritative for queue, recovery, artifact, or
observability state, and recovery lineage is read from durable backend state rather
than reconstructed from telemetry.

---

## 1. External broker adapter

- **Description:** a managed broker / job queue (for example Redis, NATS, SQS,
  Temporal, Celery, RabbitMQ, or Kafka) implementing the existing `WorkQueue` port in
  place of `SqliteWorkQueue`.
- **Why deferred:** the local `SqliteWorkQueue` already proves durable work identity
  and claim/lease semantics behind a stable port; a broker is a new adapter, not a new
  contract, and is not needed to prove the local loop.
- **Depends on:** the `WorkQueue` port (`src/storytime/local_live/queue.py`) and the
  cloud-queue mapping contract (`docs/phase14-cloud-queue-mapping.md`).
- **Risk if implemented too early:** at-least-once delivery causing duplicate
  execution before idempotent stages exist; broker semantics leaking into the domain
  model; visibility timeouts mismatched to real stage runtimes.
- **Expected future phase:** Phase 15B.

## 2. Distributed worker runtime

- **Description:** a separately deployable, replica-safe worker service replacing the
  single in-process `local_live` worker.
- **Why deferred:** local "no double execution" holds today only because there is one
  worker and SQLite arbitration; replica safety depends on the broker lease and
  idempotent stages, which do not exist yet.
- **Depends on:** the worker boundary (`src/storytime/local_live/worker.py`) and item 1
  (external broker adapter).
- **Risk if implemented too early:** duplicate execution, non-idempotent side effects,
  partial-execution on crash across machines, and clock skew between workers.
- **Expected future phase:** Phase 15B.

## 3. Object storage adapter

- **Description:** an object-storage adapter (for example S3, MinIO, GCS, or Azure
  Blob) implementing the existing `ArtifactStore` port, plus an artifact-metadata table
  of record.
- **Why deferred:** `LocalFilesystemArtifactStore` already proves backend-owned,
  storage-neutral artifact handling with logical keys and safe evidence behind a stable
  port.
- **Depends on:** the `ArtifactStore` port and `normalize_artifact_key`
  (`src/storytime/local_live/artifact_store.py`); the pipeline `StorageAdapter`
  (`src/storytime/adapters/storage/base.py`).
- **Risk if implemented too early:** URL/key leakage; the browser becoming the key
  authority or writing directly to storage; signed URLs without server-side control.
- **Expected future phase:** Phase 15C.

## 4. Auth / secrets boundary

- **Description:** an authentication/authorization boundary for a networked operator
  API and a secrets manager for per-environment credentials.
- **Why deferred:** the local bridge is loopback-only and reachable only by local
  processes, so no auth is needed to prove the local loop; introducing auth before a
  networked API exists would be speculative.
- **Depends on:** the local API / bridge boundary (`src/storytime/local_bridge/`,
  `src/storytime/local_live/server.py`) and the configuration layer
  (`src/storytime/config.py`).
- **Risk if implemented too early:** exposing the loopback assumption to the network
  without a hardened boundary; secrets leaking into logs, telemetry, or artifact
  evidence.
- **Expected future phase:** a later auth/secrets boundary after Phase 15A.

## 5. Cloud observability export

- **Description:** a sink adapter mapping the StoryTime-native `QueueWorkerEvent`
  vocabulary onto OpenTelemetry traces/spans/logs/metrics, plus a collector and
  exporter with per-environment resource attribution.
- **Why deferred:** Phase 14C.4 already proves a vendor-neutral, fail-soft,
  explanatory-only observability boundary; the export path is additive and must not
  change the domain model.
- **Depends on:** the observability boundary
  (`src/storytime/local_live/observability.py`, `src/storytime/events/model.py`) and the
  existing confined telemetry adapter (`src/storytime/adapters/telemetry/`).
- **Risk if implemented too early:** vendor semantic conventions back-propagating into
  the domain model; treating telemetry as the retry/recovery source of truth.
- **Expected future phase:** Phase 15D.

## 6. Blue/green deployment mechanics

- **Description:** the actual mechanics of running adjacent blue and green
  environments (resource naming, slot switching, migration choreography).
- **Why deferred:** Phase 14D only records how the mapping stays blue/green-friendly;
  the mechanics require real cloud resources that do not exist.
- **Depends on:** the blue/green compatibility notes (architecture baseline §10) and the
  existing local slot model (`config/deploy/active-slot`, `blue.env`, `green.env`).
- **Risk if implemented too early:** cross-slot key/queue collisions; blended telemetry;
  configuration drift between environments; coupling the API and worker so a slot cannot
  be swapped cleanly.
- **Expected future phase:** after Phase 15A, alongside the relevant adapter phases.

## 7. Cloud recovery orchestration

- **Description:** distributed recovery/retry orchestration across cloud workers.
- **Why deferred:** Phase 14C.5.1 proves bounded, backend-decided recovery lineage and
  eligibility as durable state; automatic distributed orchestration is a much larger,
  riskier surface that is not needed to prove the local control plane.
- **Depends on:** the recovery control plane
  (`src/storytime/local_live/recovery.py`, the `recovery_action` table) and items 1–2.
- **Risk if implemented too early:** reconstructing lineage from telemetry instead of
  the database; unbounded automatic retries; eligibility decisions drifting out of the
  backend. Phase 14D adds no automatic retries, scheduling, backoff, or dead-letter
  queue.
- **Expected future phase:** Phase 15E.

## 8. Cloud operator API

- **Description:** a networked, controlled operator API serving bounded read
  projections and allowlisted actions over the network.
- **Why deferred:** the operator surface is proven locally as a read-model projection
  with a loopback bridge; networking it requires the auth boundary (item 4) first.
- **Depends on:** the read model (`src/storytime/local_live/read_model.py`) and item 4.
- **Risk if implemented too early:** the API becoming a second source of truth; the
  frontend inventing or persisting backend state; polling/streaming creeping in.
- **Expected future phase:** Phase 15A and later (read APIs first, then operator-mode UX).

## 9. Provider TTS integration

- **Description:** a real text-to-speech provider integration with provider credentials.
- **Why deferred:** this is content-production work unrelated to the cloud/distributed
  architecture mapping; it was previously mis-labelled as the "Phase 14D.1" arc and is
  now corrected to deferred future work.
- **Depends on:** the artifact/storage and configuration/secrets boundaries.
- **Risk if implemented too early:** credentials leaking into logs/telemetry/evidence;
  conflating content production with the architecture baseline.
- **Expected future phase:** a later content-production phase, not Phase 15's
  cloud-runtime sequence.

## 10. RSS publishing

- **Description:** an RSS publishing boundary / feed preview for produced content.
- **Why deferred:** content-distribution work unrelated to the cloud/distributed
  mapping; previously mis-labelled as the "Phase 14D.3" arc and now corrected to
  deferred future work.
- **Depends on:** item 9 (provider TTS) and the artifact/storage boundary.
- **Risk if implemented too early:** publishing surfaces before artifact authority and
  storage are settled in cloud.
- **Expected future phase:** a later content-production phase.

## 11. Audio playback / serving

- **Description:** frontend audio understanding and audio playback/serving of produced
  artifacts.
- **Why deferred:** content/playback work unrelated to the architecture mapping;
  previously mis-labelled as the "Phase 14D.2" arc and now corrected to deferred future
  work.
- **Depends on:** items 9–10 and the artifact URL strategy (item 12).
- **Risk if implemented too early:** the browser becoming an authority over artifact
  access; serving artifacts without server-side mediation.
- **Expected future phase:** a later content-production phase.

## 12. Artifact URL strategy

- **Description:** a server-mediated strategy for referencing artifacts (for example
  short-lived, server-issued references) once artifacts live in object storage.
- **Why deferred:** there is no cloud object storage yet (item 3), so a URL strategy
  would be premature; locally, evidence carries no path, URL, or credential.
- **Depends on:** item 3 (object storage adapter).
- **Risk if implemented too early:** key/URL leakage; the browser learning storage
  paths or credentials; signed URLs without server-side control. Phase 14D implements
  no signed URLs and no public artifact serving.
- **Expected future phase:** Phase 15C and later.

## 13. Dashboard / SLO / alerting

- **Description:** dashboards, service-level objectives, and alerting built on exported
  telemetry.
- **Why deferred:** these sit on top of the observability export (item 5), which does
  not exist yet, and must never become a source of truth for domain state.
- **Depends on:** item 5 (cloud observability export).
- **Risk if implemented too early:** alerting on incomplete telemetry; treating
  dashboards/telemetry as authoritative over backend state.
- **Expected future phase:** after Phase 15D.

---

## Explicit statement

Phase 14D implements **none** of the items in this register. It adds no external
broker, no distributed worker runtime, no object storage adapter, no auth or secrets
system, no cloud observability export, no blue/green mechanics, no cloud recovery
orchestration, no cloud operator API, no provider TTS, no RSS publishing, no audio
playback/serving, no artifact URL strategy, and no dashboards/SLOs/alerting. It adds
no dependency. This register is a map of deferred future work, not a record of
implemented behavior.
