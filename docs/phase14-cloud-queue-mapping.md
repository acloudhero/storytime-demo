# Phase 14 — Cloud Queue / Recovery Mapping (future contract, not implemented)

> **Phase 14D — Cloud / Distributed Architecture Baseline from Proven Local Contracts (LOCKED).** Phase 14D is now **LOCKED** (locked using `storytime-phase14d-cloud-distributed-architecture-baseline.tar.gz`, SHA-256 `a4ccc8aa59beaf6365081973d1c3d78235df028ef0f3214979e9d3b98f4dcce6`) and is the last locked phase; Phase 14C.5.1 — Durable Recovery Control Plane Boundary — is also **LOCKED**. This document is a **contract/mapping only**. **No cloud queue, external broker, object-storage cloud adapter, distributed worker, or retry scheduler is implemented.** StoryTime remains a local-first SQLite proof; Phase 14D records cloud/distributed targets on paper and implements no cloud behavior.

## Purpose

Phase 14C.5.1 makes the local proof "distributed-system-shaped" without becoming
distributed: it adds a durable, backend-owned recovery control plane (recovery
lineage, eligibility policy, duplicate-prevention / attempt limits, recovery
read-model) on top of the locked local durable queue/worker. This document maps
those local concepts to the future cloud/distributed architecture so Phase 14D
can start from clean contracts rather than guesswork.

## Local → future cloud mapping

| Local (implemented, Phase 14C.1–14C.5.1) | Future cloud/distributed (NOT implemented) |
| --- | --- |
| Local SQLite `work_queue` | a managed broker queue (the queue itself, not its internals) |
| `work_item_id` | a cloud message / job identity |
| `claim` / `owner` / `lease_expires_at` | a lease / visibility-timeout on a message |
| stale-claim recovery (`recover_stale_work`) | lease expiration / message redelivery / reclaim |
| `recovery_action_id` | a durable recovery / audit identity |
| `original_run_id` / `original_work_item_id` | the failed execution identity |
| `recovery_run_id` / `recovery_work_item_id` | the replacement execution identity |
| `artifact_key` (logical, via `ArtifactStore`) | an object-storage pointer (still logical, never a path/URL) |
| `QueueWorkerEvent` (observer) | a telemetry export mapping — **explanatory only, never source of truth** |
| `recovery_action` table (RecoveryLineage) | a durable workflow / audit table |
| `RecoveryEligibilityPolicy` (backend-owned) | a backend-owned admission/eligibility check (never client-decided) |

## Explicit non-implementation statement

Phase 14C.5.1 implements **none** of the following; they remain deferred future
work:

- **No cloud queue is implemented in Phase 14C.5.1.**
- **No external broker is implemented in Phase 14C.5.1.** (No Redis, NATS, SQS, Kafka, Temporal, or Celery.)
- **No object-storage cloud adapter is implemented in Phase 14C.5.1.** (No S3, MinIO, signed URLs, or public artifact serving.)
- **No distributed worker is implemented in Phase 14C.5.1.**
- **No retry scheduler is implemented in Phase 14C.5.1.** (No automatic retries, exponential backoff, retry-after timers, cron-like behavior, or dead-letter queue.)
- No distributed lock manager, cloud lease, provider TTS, audio playback, RSS publishing, auth, or new dependency is introduced.

## Source-of-truth discipline (carried forward)

- The durable queue/run/stage/artifact/recovery-lineage state is the source of
  truth for recovery. Observer (`QueueWorkerEvent`) events explain lifecycle
  behavior and must never become the lineage database (Phase 14C.4 boundary).
- `ArtifactStore` remains the artifact boundary (Phase 14C.3): logical keys
  only, validated and kept under a configured root, safe evidence only — never a
  path, root, bucket, signed URL, or credential.
- Eligibility is decided in the backend; a frontend/caller can request recovery
  but can never decide whether it is allowed.
