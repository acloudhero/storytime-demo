> **Phase 15C — Minimal Cloud Demo Deployment / Portfolio Readiness (current implementation candidate; pending review; NOT locked).** New deployment config: `.github/workflows/pages.yml` (builds `frontend/` and publishes `frontend/dist` to GitHub Pages; no secret, no function, no backend). New frontend files: `frontend/src/data/demoMode.ts` and `frontend/src/components/StaticDemoNotice.tsx`. Edited frontend: `frontend/src/App.tsx` (verbatim disclaimer banner; gates the Local Bridge and Live Proof Loop views to a local-only notice under `STATIC_DEMO_MODE`). New docs: `docs/phase15c-minimal-cloud-demo.md`, `DEMO.md`. New tests: `tests/test_phase15c_static_demo_claims.py`. Edited: `tests/test_failure_mode_regression.py` (narrow state-discipline update), `README.md`, and the living state docs. No backend dependency change and no frontend dependency change (`pyproject.toml`, `uv.lock`, `frontend/package.json`, `frontend/package-lock.json` unchanged). Phase 15A and 15B remain LOCKED; Phase 15C is the current candidate (NOT locked); Phase 14E remains NOT STARTED and was not opened; Phase 15D, Phase 15E, and Phase 15F remain NOT STARTED.

> **Phase 15B — Cloud Boundary Readiness (LOCKED).** Phase 15B — Cloud Boundary Readiness — is now LOCKED and is the last locked phase. **Locked artifact:** `storytime-phase15b-cloud-boundary-readiness.tar.gz`, SHA-256 `80dbdb8331dc55f8704f1a4d28364e9b954bbaec7a6d07d6456d9c1efd46723e` — immutable and not rebuilt or altered by this lock; the post-lock ledger state is packaged separately as `storytime-phase15b-lock-record.tar.gz`. Phase 12 is CLOSED; Phase 13 is CLOSED; Phase 14 remains STARTED (not closed); Phase 14A.1, 14B.1, 14C.1, 14C.2, 14C.3, 14C.4, 14C.5.1, and 14D are LOCKED; Phase 15A is LOCKED. Phase 14E remains NOT STARTED and was not opened (intentionally bypassed). Phase 15 remains STARTED. Phase 15C, Phase 15D, and Phase 15E remain NOT STARTED. The locked round added one pure-data `storytime.runtime.boundary_readiness` module plus its design doc, deferred-work register, and guard tests; it added no dependency, no environment variable, no CLI command, and no change to `pyproject.toml`, `uv.lock`, or the frontend, and it is not a distributed system and does not run in the cloud.

> **Phase 15B — Cloud Boundary Readiness: operator-validated candidate (pending review; NOT locked).** Artifact `storytime-phase15b-cloud-boundary-readiness.tar.gz` rebuilt after recording operator validation; the validation record and its caveats are in `docs/verification-log.md`. Windows/operator validation is confirmed and is caveated by the known, pre-existing native-Windows POSIX-sensitive failures (unrelated to Phase 15B); the canonical POSIX/Linux reference run is a clean full pass (pytest 1199 passed, with ruff, mypy, lint-imports, and doctor all green). Archive hygiene: deterministic tar (numeric owner 0/0, top-level `storytime/`), excluding all caches, `.venv`, `runs`, `feed`, and `node_modules`; only the Phase 15B changed/new files differ from the Phase 15A lock-record baseline, and the dependency manifests and frontend are byte-identical. Phase 15A remains LOCKED; Phase 15B is the current candidate (NOT locked); Phase 14E remains NOT STARTED and was not opened; Phase 15C, Phase 15D, and Phase 15E remain NOT STARTED.

> **Phase 15B — Cloud Boundary Readiness (current implementation candidate; pending review; NOT locked).** New module: `src/storytime/runtime/boundary_readiness.py` (pure-data readiness model for the queue/worker, artifact/storage, observability/export, and recovery/idempotency seams). New docs: `docs/phase15b-cloud-boundary-readiness.md` and `docs/phase15b-deferred-cloud-work-register.md`. New tests: `tests/test_cloud_boundary_readiness.py`. Edited: `src/storytime/runtime/__init__.py` (additive re-export), `tests/test_imports.py` (new module entry), `tests/test_failure_mode_regression.py` (narrow state-discipline update), and the living state docs. No new dependency, no new environment variable, no CLI command, and no change to `pyproject.toml`, `uv.lock`, or the frontend. Phase 15A remains LOCKED; Phase 15B is the current candidate (pending review, NOT locked); Phase 14E remains NOT STARTED and was not opened; Phase 15C, Phase 15D, and Phase 15E remain NOT STARTED.

> **Phase 15A — Cloud Runtime Skeleton (LOCKED).** Phase 15A — Cloud Runtime Skeleton — is now LOCKED and is the last locked phase. **Locked artifact:** `storytime-phase15a-cloud-runtime-skeleton.tar.gz`, SHA-256 `ee256221abb7393fc0dde07365bca9647b1ba2d0420c64b434e6c67b9bcf871f` — immutable and not rebuilt or altered by this lock; the post-lock ledger state is packaged separately as `storytime-phase15a-lock-record.tar.gz`. Phase 12 is CLOSED; Phase 13 is CLOSED; Phase 14 remains STARTED (not closed); Phase 14A.1, 14B.1, 14C.1, 14C.2, 14C.3, 14C.4, 14C.5.1, and 14D are LOCKED. Phase 14E remains NOT STARTED and was not opened (intentionally bypassed). Phase 15 remains STARTED. Phase 15B, Phase 15C, Phase 15D, and Phase 15E remain NOT STARTED. The locked round added a pure-data `storytime.runtime` package (the `api` / `worker` / `combined` role vocabulary, a configuration-derived health/readiness model, and a `STORYTIME_RUNTIME_ROLE` boundary); it adds no new dependency, implements no cloud behaviour, is not a distributed system, does not run in the cloud, and does not import OpenTelemetry.

> **Phase 15A — Validation status (2026-05-31; current implementation candidate; pending review; NOT locked).** Operator validation is recorded in `docs/verification-log.md`: the full locked gate is green in the canonical POSIX (Linux) environment (`pytest` 1160 passed; ruff, mypy across 111 source files, and import-linter all clean; doctor healthy), and a native-Windows operator run passed sync, ruff, mypy, and import-linter with `pytest` at 1118 passed / 14 failed / 28 skipped — the 14 failures being the known POSIX-sensitive baseline families (NTFS executable bit, bash-backed script tests, `os.uname`, CRLF hash behaviour, symlink privilege), not Phase 15A regressions; the Phase 15A-owned `tests/test_runtime_roles.py` passed 28/28 on Windows. This artifact is the Phase 15A implementation candidate and is NOT locked. Phase 14D remains the last locked phase; Phase 14E remains NOT STARTED (intentionally bypassed); Phase 15B, Phase 15C, Phase 15D, and Phase 15E remain NOT STARTED.

> **Phase 15A — Cloud Runtime Skeleton (current implementation candidate; pending review; NOT locked).** Phase 14D remains the last locked phase (locked via `storytime-phase14d-cloud-distributed-architecture-baseline.tar.gz`, SHA-256 `a4ccc8aa59beaf6365081973d1c3d78235df028ef0f3214979e9d3b98f4dcce6`); Phase 15 — Cloud / Distributed Runtime — is STARTED, with Phase 15A as the current candidate on top of the LOCKED Phase 14D local contracts. Phase 14E — Local Release Candidate / Full Local Mode Closure — remains NOT STARTED; it was intentionally bypassed for this transition. New in this candidate: a pure-data `storytime.runtime` package — `src/storytime/runtime/__init__.py`, `roles.py` (the `RuntimeRole` vocabulary `api` / `worker` / `combined`, default `combined`), `config.py` (a `RuntimeConfig` reading only `STORYTIME_RUNTIME_ROLE`), and `health.py` (a configuration-derived `RuntimeHealth` / readiness model) — plus a new design doc `docs/phase15a-cloud-runtime-skeleton.md`, a new guard test `tests/test_runtime_roles.py`, prepended state-doc notes, and a one-line extension of the import-linter OpenTelemetry contract in `pyproject.toml` (no dependency added). It does not implement an external broker, no distributed worker, no object storage, no authentication, no public ingress, no provider TTS, no audio, and no RSS; it is not a distributed system, does not run in the cloud, does not import OpenTelemetry, and changes no existing backend, frontend, queue/worker, recovery, artifact-store, or observation behaviour. Phase 15B, Phase 15C, Phase 15D, and Phase 15E remain NOT STARTED.

> **Phase 14D — Cloud / Distributed Architecture Baseline from Proven Local Contracts (LOCKED).** Phase 13 is CLOSED; **Phase 14A.1, 14B.1, 14C.1, 14C.2, 14C.3, 14C.4, 14C.5.1, and 14D are LOCKED** (14D is the last locked phase; 14D locked via `storytime-phase14d-cloud-distributed-architecture-baseline.tar.gz`, SHA-256 `a4ccc8aa59beaf6365081973d1c3d78235df028ef0f3214979e9d3b98f4dcce6`; 14C.5.1 locked via `storytime-phase14c5-1-durable-recovery-control-plane-boundary.tar.gz`, SHA-256 `73a9ee1bdcbca295037f4852375d3f6b1ff155c3a0ea9d1b0fe498de3862e604`). Phase 14 — Live System / Cloud-Distributed — is STARTED. Phase 14D is a documentation-and-mapping round only: it takes the proven, LOCKED local contracts (request acceptance, the durable `WorkQueue` port, the `LocalWorker`, the `ArtifactStore` port, the durable `recovery_action` control plane, in-process observation, and the operator read-model) and records, on paper, the shape each would take in a future cloud / distributed deployment, as the readiness basis for a possible later Phase 15. It implements no cloud behavior of any kind: no external broker, no Redis/NATS/SQS/Temporal/Celery, no Kubernetes, no Terraform, no object storage, no S3/MinIO, no signed URLs, no distributed worker, no authentication, no provider TTS, no audio, no RSS, and no new dependency; it changes no backend, frontend, bridge, queue/worker, recovery, artifact-store, or observation behavior. The previously sketched provider-TTS / frontend-audio / RSS content-production items (formerly the 14D.1–14D.4 labels) are now **deferred future work**, not part of Phase 14D. Phase 14E (Local Release Candidate / Full Local Mode Closure) and Phase 15 (Cloud / Distributed Runtime) remain **NOT STARTED**.

> **Phase 14C.5.1 — Durable Recovery Control Plane Boundary (historical — now LOCKED; see the Phase 14D banner above for current state).** Phase 13 is CLOSED; **Phase 14A.1, 14B.1, 14C.1, 14C.2, 14C.3, and 14C.4 are LOCKED** (14C.4 is the last locked phase; locked via `storytime-phase14c4-minimal-observability-boundary-queue-worker.tar.gz`, SHA-256 `12b951e0a9b6b17f5c73aacf0d055b257bd4a715908f7f5078d401eae2a66d3b`). Phase 14 — Live System / Cloud-Distributed — is STARTED. Phase 14C.5.1 adds the smallest durable, backend-owned recovery control plane: a durable `recovery_action` lineage table (source of truth) linking an original failed execution to a bounded recovery execution, a backend-owned recovery eligibility policy, duplicate-prevention and a bounded attempt limit, a recovery read-model projection, local SQLite concurrency guardrails, and a cloud-queue mapping CONTRACT document. The Phase 14C.4 observer events are explanatory only and are NOT the recovery-lineage source of truth. It does not expand the Phase 14C.4 observer event schema and changes no queue/worker or ArtifactStore semantics. It absorbs the previously planned Phase 14C.5 through Phase 14C.10 local recovery-control-plane scope (historical labels only). No cloud queue, external broker, dead-letter queue, automatic retries, exponential backoff, retry scheduler, distributed worker, cloud lease, distributed lock, cloud object store, provider TTS, audio, RSS, or auth exists yet. Phase 14D / 14E remain **NOT STARTED**.

> **Phase 14C.4 — Minimal Observability Boundary for Queue/Worker (historical — now LOCKED; see the Phase 14C.5.1 banner above for current state).** Phase 13 is CLOSED; **Phase 14A.1, 14B.1, 14C.1, 14C.2, and 14C.3 are LOCKED** (14C.3 is the last locked phase). Phase 14 — Live System / Cloud-Distributed — is STARTED. Phase 14C.4 adds a small backend-owned, in-process observation boundary for the local queue/worker lifecycle: safe, vendor-neutral event names (`work.enqueued/claimed/started`, `stage.started/completed`, `artifact.recorded`, `work.completed/failed`) and safe fields (existing local identifiers, timestamps, status), emitted fail-soft at the existing lifecycle points. It changes no queue/worker or ArtifactStore semantics and adds no dependency. It is **not** a telemetry platform: no OpenTelemetry SDK, no collector, no Prometheus endpoint, no Grafana dashboards, no vendor exporters, no alerting, no SLOs, no sampling, no distributed tracing, no cloud telemetry, and no retry/recovery lineage. Phase 14C.5 / 14D / 14E remain **NOT STARTED**.

> **Phase 14C.3 — Object Storage Boundary / Artifact Store Adapter (historical — now LOCKED; see the Phase 14C.4 banner above for current state).** Phase 13 is CLOSED; **Phase 14A.1, 14B.1, 14C.1, and 14C.2 are LOCKED** (14C.2 is the last locked phase). Phase 14 — Live System / Cloud-Distributed — is STARTED. Phase 14C.3 puts artifact handling behind a backend-owned `ArtifactStore` port with a single LOCAL filesystem adapter (`LocalFilesystemArtifactStore`): it validates logical keys (rejecting absolute paths, `..` traversal, backslash separators, and symlink escapes), keeps artifacts under a configured root, and returns safe artifact evidence only, so the browser never learns filesystem paths or storage credentials. It changes no queue/worker semantics and adds no dependency. It is **not** cloud storage, **not** S3, **not** MinIO, and **not** public artifact serving; no cloud adapter, external object store, signed URLs, auth, retry/recovery lineage, or observability deepening exists yet. Phase 14C.4 / 14D / 14E remain **NOT STARTED**.

> **Phase 14C.2 — Contracts-as-Built / Cloud-Distributed Seam Baseline (historical — now LOCKED; see the Phase 14C.3 banner above for current state).** Phase 13 is CLOSED; **Phase 14A.1, 14B.1, and 14C.1 are LOCKED** (14C.1 is the last locked phase). Phase 14 — Live System / Cloud-Distributed — is STARTED. Phase 14C.2 is a documentation / contracts / guardrail round: it documents the seams Phase 14C.1 actually built (request acceptance, the queue port, the SQLite adapter, worker execution, stale-claim and stale-partial recovery, read-model/DTO safety, the frontend boundary) in `docs/phase14-contracts-as-built.md`, and defines the cloud/distributed seam baseline for future phases. It changes no runtime behavior and adds no dependency. It is **not** cloud/distributed implementation: not a cloud queue, not an external broker, not object storage, not an auth boundary, not a retry/recovery lineage, and it describes local no-double-execution under the tested SQLite/local-worker model rather than exactly-once semantics across a distributed system. Phase 14C.3 / 14D / 14E remain **NOT STARTED**.

> **Phase 14C.1 — Local Durable Queue / Worker Shape Proof (historical — now LOCKED; see the Phase 14C.2 banner above for current state).** Phase 13 is CLOSED; **Phase 14A.1 and 14B.1 are LOCKED** (14B.1 is the last locked phase). Phase 14 — Live System / Cloud-Distributed — is STARTED. Phase 14C.1 builds on the locked Phase 14B.1 proof loop and proves the local durable execution spine: a proof-run request reserves a run and enqueues a durable work item (a local work-queue port with a SQLite adapter), and a single bounded local worker claims and executes it — separating request acceptance from execution, with atomic claiming, lease-based stale-claim recovery, and no double execution. It adds no new dependency. It is a LOCAL queue/worker shape proof: not a cloud queue, not a distributed system, no external broker; and adds no provider TTS, audio playback, RSS publishing, authentication, or cloud deployment. Phase 14C.2 / 14D / 14E remain **NOT STARTED**.

> **Phase 14B.1 — Live Proof Loop Hardening / Operator Trust (historical — now LOCKED; see the Phase 14C.1 banner above for current state).** Phase 13 is CLOSED and **Phase 14A.1 is LOCKED** (the last locked phase). Phase 14 — Live System / Cloud-Distributed — is STARTED. Phase 14B.1 builds on the locked Phase 14A.1 proof loop: it adds controlled, deterministic, durable failure/recovery proof scenarios (`governance_failure`, `artifact_validation_failure`) alongside `success`, operator-UX and read-model/DTO hardening, Windows operator docs, and cloud-ready boundary docs. It adds no new dependency and implements no cloud/distributed mode, provider-backed TTS, frontend audio/TTS, audio playback, RSS publishing, authentication, or cloud deployment — all reserved for the not-yet-started **Phase 14C.1+**.

> **Phase 14A.1 — Local Live Proof Loop Before Cloud (historical — now LOCKED; see the Phase 14B.1 banner above for current state).** Phase 13L is LOCKED and Phase 13 is now CLOSED; Phase 13L is the last locked phase. Phase 14 — Live System / Cloud-Distributed — is STARTED. Phase 14A.1 adds a loopback-only local-live backend API (`src/storytime/local_live/`), a durable proof-run harness, a `storytime local-live` command, and a frontend "Live Proof Loop" surface; it adds no cloud/distributed mode, no provider-backed TTS, no frontend audio/TTS generation, no audio playback, and no RSS publishing — those remain reserved for Phase 14C.1+ (NOT STARTED). See the Phase 14A.1 note above for current state; the text below is preserved as historical record.

> **Phase 13L note — Phase 13 Closure / Demo-Local Completion Lock (current sub-phase).**
>
> **Lock lineage:** Phase 13A–13F LOCKED · Phase 13D.1 / 13D.2 LOCKED · Phase 13G LOCKED · Phase 13G.1 LOCKED · Phase 13H LOCKED · Phase 13H.1 LOCKED · Phase 13H.2 LOCKED · Phase 13H.3 LOCKED · Phase 13I LOCKED · Phase 13J LOCKED · Phase 13K LOCKED (Demo Walkthrough Refresh / Governed Local Chain Story Path). Phase 13K is the last locked phase.
> **This sub-phase:** Phase 13L — Phase 13 Closure / Demo-Local Completion Lock — implementation candidate; pending review; NOT locked. It is a closure / documentation round: it records Phase 13K as locked, prepares the Phase 13 closure as a candidate, summarizes the Demo + Local proof track, preserves `docs/demo-walkthrough.md` as the canonical reviewer path, and writes an architecture-first readiness handoff for the next, not-yet-started Phase 14 (`docs/phase14-readiness-handoff.md`). It adds no runtime capability and changes no source, frontend, or dependency.
> **Closure framing:** Like the Phase 12D closure round before it, Phase 13L only *prepares* the Phase 13 closure. Phase 13 closure is a candidate that is not yet externally locked; Phase 13 will be formally closed only after Phase 13L review/lock. Until then Phase 13 remains STARTED and is not closed.
> **Phase 14 (next, not started):** Phase 14 — Cloud/Distributed — has not started. Phase 14A — Cloud/Distributed Architecture Baseline — is the next proposed architecture baseline and is NOT STARTED; Phase 13L does not implement, start, or design it in detail.
> **Invariants:** docs and tests only. No new backend behavior, no new local bridge action, no generate_tts, no frontend TTS generation, no audio playback, no provider integration, no browser durable storage, no polling / live sync, no cloud / distributed / full Local mode, no RSS publishing, no authentication, and no cloud deployment. The read-only bridge client stays GET-only; retry_failed_stage stays the only submittable action; the backend bridge (`src/storytime/local_bridge/`), the `src/storytime/tts_proof/` package, the committed static export contract, and the locked Phase 13J / 13K surfaces are untouched.
> **Honest framing (unchanged):** an accepted retry is shown as accepted, not succeeded; a manual reload is a read-model refresh, not a live sync; the browser is not durable; mock output is labeled mock, not real provider audio; the real provider stays deferred / disabled; full Local mode and Cloud/Distributed mode do not exist.
> **Deferred to future (Phase 14) work:** frontend TTS generation, a real provider adapter, audio playback, batch generation, RSS publishing, authentication, and cloud/distributed mode all remain deferred.

# Phase 14C.3.1 cleanup note — Contracts Doc State Wording Cleanup

**Date:** 2026-05-29. Documentation-only cleanup sub-round within the Phase 14C.3 lock lineage. It fixes stale wording in `docs/phase14-contracts-as-built.md` (Section J NOT-STARTED line; Section I object-storage future-state bullet) and preserves Section K and the 14C.3 implementation. No runtime/source/dependency/frontend changes.

**Source (candidate being cleaned):** `storytime-phase14c3-object-storage-boundary-artifact-store-adapter.tar.gz`, SHA-256 `493ea3764b23daffd72c5e1e2e81dc4137305021474e6f04ce1a224770958042` (verified on extraction).

**Superseding artifact (final 14C.3 lock candidate):** `storytime-phase14c3-1-contracts-doc-state-wording-cleanup.tar.gz`; SHA-256 reported on delivery. This artifact supersedes the initial 14C.3 artifact for lock-review purposes; the Phase 14C.3 implementation lineage is unchanged and remains candidate / pending review / NOT locked.

# Phase 14C.4 implementation-candidate note — Minimal Observability Boundary for Queue/Worker

**Date:** 2026-05-29
**Round type:** Phase 14C.4 — Minimal Observability Boundary for Queue/Worker — a disciplined, minimal observability-boundary round on top of the **locked** Phase 14C.3. It defines a small backend-owned, in-process observation boundary for the local queue/worker lifecycle; it is not a telemetry stack.
**Status:** Phase 14C.4 is an **implementation candidate / pending review — NOT locked.**
**Last locked phase:** Phase 14C.3 — Object Storage Boundary / Artifact Store Adapter (LOCKED), over the earlier-locked Phase 13A–13L, 14A.1, 14B.1, 14C.1, and 14C.2.
**Current phase:** Phase 14 — Live System / Cloud-Distributed — STARTED. **Current subphase** — Phase 14C.4 (implementation candidate, pending review). Phase 14C.5 / 14D / 14E are NOT STARTED.

**What Phase 14C.4 does.** (1) Adds `src/storytime/local_live/observability.py`: `QueueWorkerEvent` (safe immutable record), `QueueWorkerEventSink` `Protocol`, `NullQueueWorkerObserver` (default no-op), `InMemoryQueueWorkerObserver` (ephemeral recorder), and a fail-soft `emit(...)` helper. (2) Defines a vendor-neutral, schema-stable event vocabulary (`work.enqueued/claimed/started`, `stage.started/completed`, `artifact.recorded`, `work.completed/failed`) with safe fields only. (3) Wires synchronous, inline, fail-soft emission at the existing enqueue/claim/start/stage/artifact/complete/fail points. (4) Adds `tests/test_queue_worker_observability.py` and advances the state-discipline guard (Phase 14C.3 LOCKED; Phase 14C.4 candidate; OpenTelemetry/collector/Prometheus/Grafana/dashboard/exporter/SLO/alerting/sampling/distributed-tracing/cloud-telemetry overclaim bars).

**What Phase 14C.4 deliberately does NOT do.** No OpenTelemetry SDK instrumentation, collector config, Prometheus endpoint, Grafana/Tempo/Loki, Datadog/New Relic/Honeycomb, alerting, SLOs, sampling, distributed tracing, cloud telemetry, external broker/Kafka/Redis/NATS, retry/recovery lineage, cloud object storage, S3, MinIO, signed URLs, public artifact serving, provider TTS, audio, RSS, auth, frontend dashboard, polling, WebSockets, or EventSource. No queue/worker or ArtifactStore semantics change. No new dependency. `pyproject.toml`, `uv.lock`, `frontend/package.json`, `frontend/package-lock.json`, and `frontend/src/data/storytime-demo-export.json` are byte-identical to the locked Phase 14C.3 source.

**Source (locked).** `storytime-phase14c3-1-contracts-doc-state-wording-cleanup.tar.gz`, SHA-256 `121f27cb5cd9decf9909afd48be1f1af257b3408c2e3d9d0a669342320af8b80` (verified on extraction).

**Artifact.** `storytime-phase14c4-minimal-observability-boundary-queue-worker.tar.gz`; SHA-256 reported on delivery.

**Current phase ledger.** Phase 12 CLOSED · Phase 13 CLOSED · Phase 14 STARTED · Phase 13A–13L LOCKED · Phase 14A.1 LOCKED · Phase 14B.1 LOCKED · Phase 14C.1 LOCKED · Phase 14C.2 LOCKED · Phase 14C.3 LOCKED (last locked phase) · Phase 14C.4 implementation candidate / pending review / NOT locked · Phase 14C.5 / 14D / 14E NOT STARTED.

# Phase 14C.3 implementation-candidate note — Object Storage Boundary / Artifact Store Adapter

**Date:** 2026-05-29
**Round type:** Phase 14C.3 — Object Storage Boundary / Artifact Store Adapter — a backend artifact-boundary round on top of the **locked** Phase 14C.2. It puts artifact handling behind a backend-owned storage seam with a single LOCAL filesystem adapter; it is not cloud storage, S3, MinIO, or public artifact serving.
**Status:** Phase 14C.3 is an **implementation candidate / pending review — NOT locked.**
**Last locked phase:** Phase 14C.2 — Contracts-as-Built / Cloud-Distributed Seam Baseline (LOCKED), over the earlier-locked Phase 13A–13L, 14A.1, 14B.1, and 14C.1.
**Current phase:** Phase 14 — Live System / Cloud-Distributed — STARTED. **Current subphase** — Phase 14C.3 (implementation candidate, pending review). Phase 14C.4 / 14D / 14E are NOT STARTED.

**What Phase 14C.3 does.** (1) Adds `src/storytime/local_live/artifact_store.py`: the `ArtifactStore` `Protocol` (neutral terms only) plus the single `LocalFilesystemArtifactStore` adapter (owns a root, validates/normalizes logical keys, rejects absolute paths / `..` traversal / backslash separators / symlink escapes, atomic writes, hash/size/media metadata, deterministic missing behavior, safe evidence only). (2) Routes the proof-run evidence write through the store (logical key `{runId}/proof/evidence.json`). (3) Keeps browser-visible artifact evidence to a relative logical key + content hash/size — no path, root, bucket, signed URL, or credential. (4) Adds `tests/test_artifact_store.py` and advances the state-discipline guard (Phase 14C.2 LOCKED; Phase 14C.3 candidate; S3/MinIO/cloud-storage/signed-URL/public-serving overclaim bars).

**What Phase 14C.3 deliberately does NOT do.** No S3, MinIO, cloud SDKs, signed URLs, public artifact serving, CDN, browser upload/download/file-picker, provider TTS, audio playback, RSS, auth, retry/recovery lineage, observability deepening, or cloud deployment. No queue/worker semantics change. No new dependency. `pyproject.toml`, `uv.lock`, `frontend/package.json`, `frontend/package-lock.json`, and `frontend/src/data/storytime-demo-export.json` are byte-identical to the locked Phase 14C.2 source.

**Source (locked).** `storytime-phase14c2-contracts-as-built-cloud-distributed-seam-baseline.tar.gz`, SHA-256 `930a339fff100eddd37f5c8b98739bcced4107a01e1959307750a2f0a48b64ff` (verified on extraction).

**Artifact.** `storytime-phase14c3-object-storage-boundary-artifact-store-adapter.tar.gz`; SHA-256 reported on delivery in the round report.

**Current phase ledger.** Phase 12 CLOSED · Phase 13 CLOSED · Phase 14 STARTED · Phase 13A–13L LOCKED · Phase 14A.1 LOCKED · Phase 14B.1 LOCKED · Phase 14C.1 LOCKED · Phase 14C.2 LOCKED (last locked phase) · Phase 14C.3 implementation candidate / pending review / NOT locked · Phase 14C.4 / 14D / 14E NOT STARTED.

# Phase 14C.2 implementation-candidate note — Contracts-as-Built / Cloud-Distributed Seam Baseline

**Date:** 2026-05-29
**Round type:** Phase 14C.2 — Contracts-as-Built / Cloud-Distributed Seam Baseline — a disciplined documentation / contract-baseline / guardrail round on top of the **locked** Phase 14C.1. It documents the seams Phase 14C.1 actually built and defines the future cloud/distributed seam baseline without implementing any of it. No runtime behavior change.
**Status:** Phase 14C.2 is an **implementation candidate / pending review — NOT locked.**
**Last locked phase:** Phase 14C.1 — Local Durable Queue / Worker Shape Proof (LOCKED), over the earlier-locked Phase 13A–13L, 14A.1, and 14B.1.
**Current phase:** Phase 14 — Live System / Cloud-Distributed — STARTED. **Current subphase** — Phase 14C.2 (implementation candidate, pending review). Phase 14C.3 / 14D / 14E are NOT STARTED.

**What Phase 14C.2 does.** (1) Adds `docs/phase14-contracts-as-built.md` — the contracts-as-built baseline with concrete abstract Python `Protocol`/ABC snippets under fixed headers A–J (Request Acceptance, Queue Port, SQLite Adapter, Worker Execution, Stale Claim Recovery, Stale Partial Execution Recovery, Read-Model/DTO Safety, Frontend Boundary, Cloud/Distributed Seam Baseline, Future Phase Dependency Map). (2) Records the formal Phase 14C.1 lock and the Phase 14C.2 candidate state across the living docs. (3) Adds `tests/test_contracts_as_built_doc.py` and advances the state-discipline guard (Phase 14C.1 LOCKED; Phase 14C.2 candidate; Phase 14C.3+/14D/14E NOT STARTED).

**What Phase 14C.2 deliberately does NOT do.** No cloud/distributed implementation, no cloud queue, no external broker, no distributed worker pool, no object storage / artifact store adapter, no auth boundary, no retry/recovery lineage action, no observability deepening, no provider TTS, no audio playback, no RSS. No runtime behavior change to the queue/worker model. No new dependency. `pyproject.toml`, `uv.lock`, `frontend/package.json`, `frontend/package-lock.json`, and `frontend/src/data/storytime-demo-export.json` are byte-identical to the locked Phase 14C.1 source.

**Source (locked).** `storytime-phase14c1-stale-partial-recovery-cleanup.tar.gz`, SHA-256 `47e676c356ecd63a7bcebc2e7da2240c03bdf4f0efb41930d4831eda0d13a6e5` (verified on extraction).

**Artifact.** `storytime-phase14c2-contracts-as-built-cloud-distributed-seam-baseline.tar.gz`; SHA-256 reported on delivery in the round report (the manifest cannot contain its own archive hash).

**Current phase ledger.** Phase 12 CLOSED · Phase 13 CLOSED · Phase 14 STARTED · Phase 13A–13L LOCKED · Phase 14A.1 LOCKED · Phase 14B.1 LOCKED · Phase 14C.1 LOCKED (last locked phase) · Phase 14C.2 implementation candidate / pending review / NOT locked · Phase 14C.3 / 14D / 14E NOT STARTED.

# Phase 14C.1 implementation-candidate note — Local Durable Queue / Worker Shape Proof

**Date:** 2026-05-29
**Round type:** Phase 14C.1 — Local Durable Queue / Worker Shape Proof — a bounded implementation round on top of the **locked** Phase 14B.1 proof loop. It proves the local durable execution spine; it is not a cloud/distributed implementation.
**Status:** Phase 14C.1 is an **implementation candidate / pending review — NOT locked.**
**Last locked phase:** Phase 14B.1 — Live Proof Loop Hardening / Operator Trust (LOCKED), over the earlier-locked Phase 13A–13L and Phase 14A.1.
**Current phase:** Phase 14 — Live System / Cloud-Distributed — STARTED. **Current subphase** — Phase 14C.1 (implementation candidate, pending review). Phase 14C.2 / 14D / 14E are NOT STARTED.

**What Phase 14C.1 does.** (1) Adds a local durable work-queue **port** (`WorkQueue` Protocol) with a **SQLite adapter** (`SqliteWorkQueue`) backed by a new `work_queue` table (schema migration 6, additive/idempotent). (2) Changes the proof-run request path to **reserve + enqueue** (HTTP 202, status `queued`) instead of executing inline. (3) Adds a single bounded **local worker** (`LocalWorker`) that claims, runs, and reconciles work items; the running server attaches one background worker thread. (4) Atomic claiming (`BEGIN IMMEDIATE` + conditional update), lease-based stale-claim recovery, and per-run idempotent execution prevent double execution. (5) Exposes a safe queue lifecycle through the read model (no owner/lease internals). Existing `success` / `governance_failure` / `artifact_validation_failure` scenarios run unchanged through the queue/worker path.

**What Phase 14C.1 deliberately does NOT do.** It is a LOCAL queue/worker shape proof: not a cloud queue, not a distributed system, no external broker, no hosted execution. It adds no provider-backed TTS, no frontend audio/TTS generation, no audio playback, no RSS publishing, no authentication, and no cloud deployment; no retry/recovery *action* (that is Phase 14C.5); no new dependency. `pyproject.toml`, `uv.lock`, `frontend/package.json`, `frontend/package-lock.json`, and the committed `frontend/src/data/storytime-demo-export.json` are byte-identical to the locked Phase 14B.1 source. Honest framing is unchanged.

**Source.** Locked Phase 14B.1 artifact `storytime-phase14b1-live-proof-loop-hardening-operator-trust.tar.gz`, SHA-256 `7576408fc2aef04b40bd6dff236a4d8eccc15f5dd30c7a81eceb0c347f488276` (verified on extraction).

**Artifact.** `storytime-phase14c1-local-durable-queue-worker-shape-proof.tar.gz`; SHA-256 reported on delivery in the round report (the manifest cannot contain its own archive hash).

**Current phase ledger.** Phase 12 CLOSED · Phase 13 CLOSED · Phase 14 STARTED · Phase 13A–13L LOCKED · Phase 14A.1 LOCKED · Phase 14B.1 LOCKED (last locked phase) · Phase 14C.1 implementation candidate / pending review / NOT locked · Phase 14C.2 / 14D / 14E NOT STARTED.

# Phase 14B.1 implementation-candidate note — Live Proof Loop Hardening / Operator Trust

**Date:** 2026-05-29
**Round type:** Phase 14B.1 — Live Proof Loop Hardening / Operator Trust / Cloud-Ready Boundary Preparation — a hardening round on top of the **locked** Phase 14A.1 local-live proof loop. It deepens the proof rather than expanding the architecture.
**Status:** Phase 14B.1 is an **implementation candidate / pending review — NOT locked.**
**Last locked phase:** Phase 14A.1 — Local Live Proof Loop Before Cloud (LOCKED), over the earlier-locked Phase 13A–13L sequence.
**Current phase:** Phase 14 — Live System / Cloud-Distributed — STARTED. **Current subphase** — Phase 14B.1 (implementation candidate, pending review). Phase 14C.1+ (cloud/distributed bundle) has NOT STARTED.

**What Phase 14B.1 does.** (1) Adds a controlled, deterministic failure/recovery proof path: the proof-run action accepts an allowlisted `scenario` (`success`, `governance_failure`, `artifact_validation_failure`); the two failure scenarios produce durable **failed** runs with a failed `stage_execution`, a `RunFailed` event carrying the failed stage and reason, an evidence artifact, and a failure reason exposed through the read model. (2) Hardens operator UX: scenario buttons, a failure-reason panel, a marked failed stage, richer evidence labels, and exactly one bounded post-run refresh (no polling/interval/socket). (3) Hardens the read model / DTOs: typed proof-run request/response/error shapes, a health DTO with no absolute path (basename + scenario list), no raw story text, no absolute paths. (4) Adds Windows operator docs and (5) cloud-ready boundary docs (mapping the local contracts to a future hosted API/auth/managed DB/object storage/queue/worker/OpenTelemetry/provider adapter).

**What Phase 14B.1 deliberately does NOT do.** No cloud/distributed mode, no provider-backed TTS, no frontend audio/TTS generation, no audio playback, no RSS publishing, no authentication, and no cloud deployment; no retry/recovery action (failure *proof* only); no new dependency. `pyproject.toml`, `uv.lock`, `frontend/package.json`, `frontend/package-lock.json`, and the committed `frontend/src/data/storytime-demo-export.json` are byte-identical to the locked Phase 14A.1 source. Honest framing is unchanged: a failure scenario is an intentional controlled proof, not a real provider/ffmpeg error; mock is labelled mock; the frontend refresh is bounded/manual, not a live sync; durable state is backend-owned, not the browser's.

**Source.** Locked Phase 14A.1 artifact `storytime-phase14a1-local-live-proof-loop-before-cloud.tar.gz`, SHA-256 `398837defa9436e8c298f8bf0ece0814d55f533cb15cb582afd33e7af8d02077` (verified on extraction).

**Artifact.** `storytime-phase14b1-live-proof-loop-hardening-operator-trust.tar.gz`; SHA-256 reported on delivery in the round report (the manifest cannot contain its own archive hash).

**Current phase ledger.** Phase 12 CLOSED · Phase 13 CLOSED · Phase 14 STARTED · Phase 13A–13L LOCKED · Phase 14A.1 LOCKED (last locked phase) · Phase 14B.1 implementation candidate / pending review / NOT locked · Phase 14C.1+ NOT STARTED.

# Phase 13L implementation-candidate note — Phase 13 Closure / Demo-Local Completion Lock

**Date:** 2026-05-28
**Round type:** Phase 13L — Phase 13 Closure / Demo-Local Completion Lock — a closure / documentation round over the locked Phase 13K. It records Phase 13K as locked, prepares the Phase 13 closure as a candidate, summarizes the Demo + Local proof track, preserves the canonical demo walkthrough as the reviewer path, and writes an architecture-first readiness handoff for the next, not-yet-started Phase 14. It changes no backend behavior, adds no dependency, and adds no execution path.
**Status:** Phase 13L is an **implementation candidate / pending review — NOT locked.**
**Last locked phase:** Phase 13K — Demo Walkthrough Refresh / Governed Local Chain Story Path (LOCKED), over the earlier-locked Phase 13A–13F / 13D.1 / 13D.2 / 13G / 13G.1 / 13H / 13H.1 / 13H.2 / 13H.3 / 13I / 13J.
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13L (implementation candidate, pending review). Phase 13L prepares the Phase 13 closure; Phase 13 will be formally closed only after Phase 13L review/lock, so Phase 13 is not yet closed.

**What Phase 13L does.** It records the Phase 13K lock in every living state document, then prepares a clean, honest closure of Phase 13. It adds two concise documents: `docs/phase13-closure.md` (the Phase 13 closure summary, the final locked sub-phase sequence, the Demo + Local proof accomplishments, the canonical reviewer surface, the local-bridge / browser-authority / governed-TTS boundaries, the deferred-capability register, a Phase 14 readiness pointer, the validation/lock evidence summary, and the final current-state declaration) and `docs/phase14-readiness-handoff.md` (an architecture-first, implementation-free handoff that frames the next, not-yet-started Phase 14A — Cloud/Distributed Architecture Baseline). It advances the state-discipline guard to record Phase 13K locked, Phase 13L as a pending-review candidate, the Phase 13 closure as prepared-but-not-locked, and the next Phase 14 as not started. It points reviewers at `docs/demo-walkthrough.md` as the single canonical reviewer/demo path rather than duplicating it.

**What Phase 13L deliberately does NOT do.** It adds NO runtime capability and changes no source, frontend, or dependency: no new backend behavior, no new local bridge action, no generate_tts, no frontend TTS generation, no audio playback, no provider integration, no browser durable storage, no polling / live sync, no cloud / distributed / full Local mode, no RSS publishing, no authentication, and no cloud deployment. It does not implement, start, or design in detail the next Phase 14 — it only writes an architecture-first readiness handoff for it. `pyproject.toml`, `uv.lock`, `src/`, `frontend/src/`, `frontend/package.json`, `frontend/package-lock.json`, `frontend/vite.config.ts`, `frontend/tsconfig.json`, the committed static export, and `frontend/src/data/adapter.ts` are byte-identical to the locked Phase 13K source. The honest framing is unchanged: an accepted retry is shown as accepted, not succeeded; a manual reload is a read-model refresh, not a live sync; mock output is labeled mock, not real provider audio; the real provider stays deferred; and neither full Local mode nor Cloud/Distributed mode is presented as existing.

**Source.** Locked Phase 13K artifact `storytime-phase13k-demo-walkthrough-refresh-governed-local-chain-story-path.tar.gz`, SHA-256 `bf3bcc87cd147205558eddd16b53c5a09e91af1bfa6269d10a8de153a7e6f10a`. Phase 13K was locked by the user as final decision-maker (GPT preliminary verification PASS, Gemini implementation review SAFE TO LOCK, no required edits, protected surfaces byte-identical, archive hygiene clean) — the same narrow mechanical exception used at every prior phase transition.

**Current phase ledger.** Phase 12 CLOSED · Phase 13 STARTED · Phase 13A–13F LOCKED · 13D.1 / 13D.2 LOCKED · Phase 13G LOCKED · Phase 13G.1 LOCKED · Phase 13H LOCKED · Phase 13H.1 LOCKED · Phase 13H.2 LOCKED · Phase 13H.3 LOCKED · Phase 13I LOCKED · Phase 13J LOCKED · Phase 13K LOCKED · Phase 13L implementation candidate / pending review / NOT locked. Phase 13L prepares the Phase 13 closure (a candidate, not yet externally locked); Phase 13 remains STARTED until Phase 13L locks. Phase 14 — Cloud/Distributed — has not started; Phase 14A is the next proposed architecture baseline.

_The Phase 13K note below is retained as historical context; Phase 13K is now LOCKED and is the last locked phase. (That historical note states "there is no Phase 13L"; that was accurate when Phase 13K was authored — Phase 13L now exists as this Phase 13 closure round.)_

---

> **Phase 13K note — Demo Walkthrough Refresh / Governed Local Chain Story Path (historical record — Phase 13K is now LOCKED; see the Phase 13L note above).**
>
> **Lock lineage:** Phase 13G LOCKED · Phase 13G.1 LOCKED · Phase 13H LOCKED · Phase 13H.1 LOCKED · Phase 13H.2 LOCKED · Phase 13H.3 LOCKED · Phase 13I LOCKED · Phase 13J LOCKED (Operator GUI Polish / Demo-Local Alignment). Phase 13J is the last locked phase.
> **This sub-phase (historical):** Phase 13K — now LOCKED (it was an implementation candidate, pending review, when this note was written). It is a demo / walkthrough / reviewer-story-path refresh: it designates one canonical walkthrough (`docs/demo-walkthrough.md`), refreshes the stale in-app Demo Walkthrough view and adapter to tell the true governed local-chain story with an evidence map, and reconciles the pre-existing stale demo/portfolio docs to point at the canonical walkthrough. It adds no runtime capability.
> **Terminal implementation sub-phase (historical):** Phase 13K was the terminal planned *implementation* sub-phase. Phase 13L now exists as the Phase 13 closure round (see the note above); it prepares closure and is itself an implementation candidate, not yet locked. Phase 13 remains STARTED and is not closed until Phase 13L locks.
> **Invariants:** docs / narrative / read-only presentation only. No new backend behavior, no new local bridge action, no generate_tts, no frontend TTS generation, no Generate-audio button, no audio player, no file / directory / URL / credential inputs, and no provider-selection control that changes runtime behavior. No browser durable storage (no localStorage / sessionStorage / IndexedDB / cookies); no automatic reload, polling, WebSocket, or EventSource; the read-only bridge client stays GET-only and retry_failed_stage stays the only submittable action; the backend bridge (`src/storytime/local_bridge/`), the `src/storytime/tts_proof/` package, the committed static export contract, and the locked Phase 13J polish components are untouched.
> **Honest framing:** an accepted retry is shown as accepted, not succeeded; a manual reload is a read-model refresh, not a live sync; the browser is not durable; mock output is labeled mock, not real provider audio; the real provider stays deferred / disabled (not bundled); full Local mode and Cloud/Distributed mode do not exist.
> **No unsafe demo guidance:** the canonical demo is mock-first and local-safe — it does not tell a reviewer to enable a real provider, set provider credentials, bind the bridge beyond loopback, or disable origin/CORS protections.
> **Provenance:** the committed static export may carry an older baked phase value; the walkthrough frames that as snapshot provenance ("snapshot generated by"), not the current system phase.
> **Deferred:** frontend TTS generation, a real provider adapter, audio playback, batch generation, RSS publishing, cloud/distributed mode, and full Local mode all remain deferred.

# Phase 13K implementation-candidate note — Demo Walkthrough Refresh / Governed Local Chain Story Path

**Date:** 2026-05-28
**Round type:** Phase 13K — Demo Walkthrough Refresh / Governed Local Chain Story Path — a demo / walkthrough / reviewer-story-path refresh over the locked Phase 13J. It designates one canonical walkthrough, refreshes the in-app walkthrough to the true governed local-chain story with an evidence map, reconciles stale demo/portfolio docs, and adds truthfulness / evidence guards. It changes no backend behavior, adds no dependency, and adds no execution path.
**Status (historical):** Phase 13K is now **LOCKED** and is the last locked phase (it was an implementation candidate, pending review, when this note was written).
**Last locked phase:** Phase 13J — Operator GUI Polish / Demo-Local Alignment (LOCKED), over the earlier-locked Phase 13G / 13G.1 / 13H / 13H.1 / 13H.2 / 13H.3 / 13I.
**Current phase (at time of writing):** Phase 13 — Portfolio Website / Operator GUI — STARTED; Phase 13K was then the current subphase (implementation candidate, pending review). Phase 13K is now LOCKED and Phase 13L is the current closure round (see the note above). Phase 13 remains STARTED and is not yet closed.

**What Phase 13K does.** It makes StoryTime's reviewer/demo path tell the true governed local-chain story. It adds one canonical walkthrough — `docs/demo-walkthrough.md` — layered for a 30-second glance, a 5–7 minute guided demo, a ~15-minute technical appendix, a deferred-capability register, and a structured evidence map of real repository paths, plus machine-checkable truth labels. It refreshes the stale in-app Demo Walkthrough view and `demoWalkthroughAdapter.ts` (which predated the local bridge, controlled retry, manual reload, and governed TTS proof) so the modes, the loopback bridge, the one controlled retry, the manual snapshot reload, and the governed mock-first TTS proof are described truthfully and point at the existing Phase 13J surfaces — without adding any route, view, execution control, or duplicated source of truth. It reconciles the pre-existing demo / portfolio / narrative cluster so those documents point at the canonical walkthrough rather than competing with it, and it adds tests that verify the evidence-map paths exist, that the walkthrough's truth labels are present and active overclaims are absent (negation-aware), and that exactly one canonical walkthrough exists.

**What Phase 13K deliberately does NOT do.** It adds NO runtime capability: no new backend behavior, no new local bridge action, no `generate_tts`, no frontend TTS generation, no Generate-audio button, no audio player, no file / directory / URL / credential inputs, and no provider-selection control that changes runtime behavior. It introduces NO browser durable storage and NO automatic reload, polling, WebSocket, or EventSource. The read-only bridge client stays GET-only and `retry_failed_stage` stays the only submittable action; the backend bridge, the `src/storytime/tts_proof/` package, the committed static export contract, and the locked Phase 13J polish components (`operatorConsole.ts`, `ModeOverview.tsx`, `BoundaryLegend.tsx`, `OperatorWorkflow.tsx`, `TTSProofSummary.tsx`, `consolePolish.module.css`) are untouched. The walkthrough keeps the honest boundaries: an accepted retry is shown as accepted, not succeeded; a manual reload is a read-model refresh, not a live sync; mock output is labeled mock, not real provider audio; the real provider stays deferred; and neither full Local mode nor Cloud/Distributed mode is presented as existing. The canonical demo is mock-first and local-safe and gives no instruction to enable a real provider, set credentials, or expose the bridge beyond loopback. Where the committed export carries an older baked phase value, the walkthrough frames it as snapshot provenance, not the current system phase.

**Source.** Locked Phase 13J artifact `storytime-phase13j-operator-gui-polish-demo-local-alignment.tar.gz`, SHA-256 `7fdfcc4dbb23a99cd569310f77e2a6d958df6d88f435cd575556df01f070f589`. Phase 13J was locked out-of-band by the user as final decision-maker (GPT preliminary verification PASS, Gemini implementation review SAFE TO LOCK, 955 tests passing, frontend typecheck/build clean, protected surfaces byte-identical, archive hygiene clean, no required edits) — the same narrow mechanical exception used at every prior phase transition; the source artifact internally recorded Phase 13J as the then-current candidate, as expected for a prior-phase source. Protected surfaces — `pyproject.toml`, `uv.lock`, `src/storytime/local_bridge/`, `src/storytime/tts_proof/`, `src/storytime/operator_export.py`, `frontend/package.json`, `frontend/package-lock.json`, `frontend/vite.config.ts`, `frontend/tsconfig.json`, `frontend/src/data/storytime-demo-export.json`, `frontend/src/data/adapter.ts`, and the locked Phase 13J polish components — are byte-identical.

**Current phase ledger.** Phase 12 CLOSED · Phase 13 STARTED · Phase 13A–13F LOCKED · 13D.1 / 13D.2 LOCKED · Phase 13G LOCKED · Phase 13G.1 LOCKED · Phase 13H LOCKED · Phase 13H.1 LOCKED · Phase 13H.2 LOCKED · Phase 13H.3 LOCKED · Phase 13I LOCKED · Phase 13J LOCKED · Phase 13K implementation candidate / pending review / NOT locked. Phase 13K is the terminal planned sub-phase; Phase 13 remains STARTED and is not closed (closure is a separate later decision).

_The Phase 13J implementation-candidate note below is retained as historical context; Phase 13J is now LOCKED and is the last locked phase._

---

# Phase 13J implementation-candidate note — Operator GUI Polish / Demo-Local Alignment

**Date:** 2026-05-28
**Round type:** Phase 13J — Operator GUI Polish / Demo-Local Alignment — a frontend/operator-GUI polish round over the locked Phase 13I. It refines presentation, information architecture, and reviewer-facing copy and adds READ-ONLY GUI understanding of the governed TTS proof. It changes no backend behavior, adds no dependency, and adds no execution path.
**Status:** Phase 13J is an **implementation candidate / pending review — NOT locked.**
**Last locked phase:** Phase 13I — Governed Local TTS Proof / Audio Artifact Boundary (LOCKED), over the earlier-locked Phase 13G / 13G.1 / 13H / 13H.1 / 13H.2 / 13H.3.
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13J (implementation candidate, pending review).

**What Phase 13J does.** It makes the existing StoryTime frontend feel like a credible, polished operator console rather than a stack of phase artifacts. It improves the at-a-glance orientation (a mode overview and a boundary legend distinguishing Demo Mode, Local Bridge, the Governed Local TTS Proof, and Manual Snapshot Reload), gives the Local Bridge page an explicit operator workflow so the page sequence reads in order, tightens dense copy into scannable badges / callouts, and adds a READ-ONLY TTS proof summary that explains the Phase 13I governed chain (provider mode mock, real provider deferred/disabled, approved-fixture and text-hash concepts, character count, artifact/manifest/audit lifecycle, and a labeled cost estimate) sourced from a frontend-owned presentation adapter — not from any live artifact read and not by changing the export contract. Accessibility is treated as part of the polish (semantic headings, focus states, status communicated by text and shape rather than color alone).

**What Phase 13J deliberately does NOT do.** It adds NO backend behavior, NO new local bridge action, and NO `generate_tts` action; it adds NO frontend TTS generation, NO Generate-audio button, and NO audio player. It adds NO file / directory / URL / credential inputs and NO provider-selection control that changes runtime behavior. It introduces NO browser durable storage (no localStorage / sessionStorage / IndexedDB / cookies) and NO automatic reload, polling, WebSocket, or EventSource. The read-only bridge client stays GET-only and `retry_failed_stage` stays the only submittable action; the backend bridge and the `src/storytime/tts_proof/` package are untouched. The committed static export contract is unchanged — derived display data comes from a frontend presentation adapter over the existing export shape. The UI never blurs these honest boundaries: an accepted retry is shown as accepted, not succeeded; a manual reload is shown as a manual read-model refresh, not a live sync; the browser is shown as non-durable; mock output is labeled mock, not real provider audio; and neither full Local mode nor Cloud/Distributed mode is presented as existing. TTS appears only as read-only understanding / status / evidence; generation remains backend/CLI-owned and the browser cannot trigger it.

**Source.** Locked Phase 13I artifact `storytime-phase13i-governed-local-tts-proof-audio-artifact-boundary.tar.gz`, SHA-256 `dcb57853c046d44f459af32bb59964502b016eb8620d66258af763c740dd244a`. Phase 13I was locked out-of-band by the user as final decision-maker (GPT preliminary verification PASS, Gemini implementation review SAFE TO LOCK, 932 tests passing, protected surfaces byte-identical, archive hygiene clean, no required edits) — the same narrow mechanical exception used at every prior phase transition; the source artifact internally recorded Phase 13I as the then-current candidate, as expected for a prior-phase source. Protected surfaces — `pyproject.toml`, `uv.lock`, `src/storytime/local_bridge/`, `src/storytime/tts_proof/`, `src/storytime/operator_export.py`, `frontend/package.json`, `frontend/package-lock.json`, `frontend/vite.config.ts`, `frontend/tsconfig.json`, `frontend/src/data/storytime-demo-export.json`, and `frontend/src/data/adapter.ts` — are byte-identical.

**Current phase ledger.** Phase 12 CLOSED · Phase 13 STARTED · Phase 13A–13F LOCKED · 13D.1 / 13D.2 LOCKED · Phase 13G LOCKED · Phase 13G.1 LOCKED · Phase 13H LOCKED · Phase 13H.1 LOCKED · Phase 13H.2 LOCKED · Phase 13H.3 LOCKED · Phase 13I LOCKED · Phase 13J implementation candidate / pending review / NOT locked · Phase 13K (Demo Walkthrough Refresh / Governed Local Chain Story Path) NOT STARTED. Phase 13 remains STARTED and is not closed.

_The Phase 13I implementation-candidate note below is retained as historical context; Phase 13I is now LOCKED and is the last locked phase._

---

# Phase 13I implementation-candidate note — Governed Local TTS Proof / Audio Artifact Boundary

**Date:** 2026-05-28
**Round type:** Phase 13I — Governed Local TTS Proof / Audio Artifact Boundary — a narrow backend/local-chain round over the locked Phase 13H.3. It adds a self-contained `storytime.tts_proof` subpackage and one backend-only CLI command; it changes no frontend behavior and adds no dependency.
**Status:** Phase 13I is an **implementation candidate / pending review — NOT locked.**
**Last locked phase:** Phase 13H.3 — Manual Static Export Reload / Read-Model Replacement Boundary (LOCKED), over the earlier-locked Phase 13G / 13G.1 / 13H / 13H.1 / 13H.2.
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13I (implementation candidate, pending review).

**Forward roadmap re-sequencing.** This round intentionally re-sequences the forward roadmap: Phase 13I is now Governed Local TTS Proof, Phase 13J is Operator GUI Polish / Demo-Local Alignment, and Phase 13K is Demo Walkthrough Refresh / Governed Local Chain Story Path. This is a forward-looking plan change, not a rewrite of append-only history; the earlier notes describing 13I as Operator GUI Polish remain historical below. Phase 13’s charter is widened narrowly and honestly to “the Operator GUI and the governed local generation chain the GUI explains.” Phase 13 is NOT a full audio-production epoch.

**What Phase 13I does.** It proves that StoryTime can produce a local audio artifact through a governed, observable, auditable boundary, without browser execution authority, credential exposure, cost-control bypass, or archive contamination. A self-contained `storytime.tts_proof` subpackage drives one tiny **approved, allowlisted** text fixture through a governance/cost guard and the existing deterministic `MockTTS` adapter to an atomic local WAV artifact, writes a manifest beside it, and emits structured audit/event records (`tts.requested` → `tts.executing` → `tts.completed`, with `tts.guard_rejected` / `tts.failed` and a typed failure taxonomy). The guard checks provider/flag, fixture allowlist, a character cap (before any provider call), and that the artifact path resolves within the controlled directory, and it records a labeled cost **estimate** (the same accounting code path every provider would use). A new backend-only `storytime tts-proof` CLI command invokes it. The whole proof passes with **no credentials and no network**.

**What Phase 13I deliberately does NOT do.** The mock is the default and the only bundled provider; a non-mock (“real”) provider is disabled by default, requires an explicit enable flag, is non-load-bearing, is never exercised by tests, and fails closed with a typed reason (no real adapter is bundled, so even an enabled real selection fails closed). It adds NO frontend TTS button and NO browser-triggered generation; it adds NO new local bridge action, NO POST /tts or POST /generate endpoint, NO `generate_tts` action, and serves NO audio over the bridge — generation is backend/CLI-only and the backend bridge (`src/storytime/local_bridge/`) and browser surface are untouched. It does NOT ingest arbitrary text, arbitrary files, or arbitrary URLs; the input is the one allowlisted fixture. It performs no automatic or SDK-level retries, no batch generation, no audio post-processing, no playback UI, no RSS publishing, no cloud/distributed mode, and no full Local mode. Artifact writes are atomic (temp → rename) with an output-byte cap and leave no partial artifact on failure; the path is validated against traversal, absolute, and symlink escape. Telemetry/logs/audit carry a text hash and length — never raw fixture text, credentials, or verbatim provider errors. Generated audio, manifests, and audit logs are runtime output under `runs/` and are excluded from version control and from the locked archive.

**Source.** Locked Phase 13H.3 artifact `storytime-phase13h3-manual-static-export-reload-read-model-replacement-boundary.tar.gz`, SHA-256 `ae12c88f65755cc1bac0ca5cb323b59a0e94538bd29d6a813c6dcf16d7a03a6c`. Phase 13H.3 was locked out-of-band by the user as final decision-maker (GPT preliminary verification PASS, Gemini implementation review SAFE TO LOCK, 902 tests passing, protected surfaces byte-identical, archive hygiene clean, no required edits) — the same narrow mechanical exception used at every prior phase transition; the source artifact internally recorded Phase 13H.3 as the then-current candidate, as expected for a prior-phase source. Protected surfaces — `frontend/package.json`, `frontend/package-lock.json`, `frontend/vite.config.ts`, `frontend/tsconfig.json`, `frontend/src/data/storytime-demo-export.json`, `frontend/src/data/adapter.ts`, and `src/storytime/local_bridge/` — are byte-identical.

**Current phase ledger.** Phase 12 CLOSED · Phase 13 STARTED · Phase 13A–13F LOCKED · 13D.1 / 13D.2 LOCKED · Phase 13G LOCKED · Phase 13G.1 LOCKED · Phase 13H LOCKED · Phase 13H.1 LOCKED · Phase 13H.2 LOCKED · Phase 13H.3 LOCKED · Phase 13I implementation candidate / pending review / NOT locked · Phase 13J (Operator GUI Polish / Demo-Local Alignment) NOT STARTED · Phase 13K (Demo Walkthrough Refresh / Governed Local Chain Story Path) NOT STARTED. Phase 13 remains STARTED and is not closed.

_The Phase 13H.3 implementation-candidate note below is retained as historical context; Phase 13H.3 is now LOCKED and is the last locked phase._

---

# Phase 13H.3 implementation-candidate note — Manual Static Export Reload / Read-Model Replacement Boundary

**Date:** 2026-05-28
**Round type:** Phase 13H.3 — Manual Static Export Reload / Read-Model Replacement Boundary — a frontend-only round over the locked Phase 13H.2. It adds one narrow feature and changes no backend behavior; no dependency change, no archive-hygiene regression.
**Status:** Phase 13H.3 is an **implementation candidate / pending review — NOT locked.**
**Last locked phase:** Phase 13H.2 — Frontend Boundary Cleanup / Local Bridge Component Hardening (LOCKED), over the earlier-locked Phase 13G / 13G.1 / 13H / 13H.1.
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13H.3 (implementation candidate, pending review).

**What Phase 13H.3 does.** It proves the browser can MANUALLY replace its visible read model from an authoritative static export snapshot while staying non-durable. A new, self-contained module (`frontend/src/data/staticExportReload.ts`) performs exactly one GET of the committed static export asset (resolved at build time via `new URL("./storytime-demo-export.json", import.meta.url)`, with a `?reload=<timestamp>` cache-bust applied only to that one fetch), validates the fetched JSON all-or-nothing, and returns a typed read-model snapshot. A new panel (`frontend/src/components/StaticExportReloadPanel.tsx`), wired into `LocalBridgeView`, owns a narrow, transient in-memory read model (seeded from the bundled static import) and a single operator-triggered "Reload static export snapshot" button; on a valid fetch it replaces the held snapshot wholesale and shows the source, status, reloaded-at time, and snapshot metadata (schema version, export kind, generated-by, run count, failure-queue count, project).

**What Phase 13H.3 deliberately does NOT do.** It does not add automatic sync, polling, background refresh, a live socket, or server-sent events — the reload runs only from the button's onClick, never on mount or from an effect. It adds no backend or bridge endpoint and never reloads the read model from the bridge; the reload fetches only the committed static export asset, and the operator cannot enter an arbitrary URL. It adds no new action type and no generic action runner; the only browser-initiated submission is still the single controlled retry path that landed in locked Phase 13H.1 (one POST /actions for the allowlisted action retry_failed_stage), and the read-only client stays GET-only. Replacement is all-or-nothing: an invalid / partial / empty / schema-incompatible export is rejected and the previous snapshot is retained — there is no partial merge and no optimistic update. The snapshot lives only in transient React state — no `localStorage` / `sessionStorage` / `IndexedDB` / cookies / URL-history persistence — so a page reload returns to the bundled snapshot unless the served static file itself changed. Acceptance is still not success, and a manual reload does not prove a retry succeeded. Full Local mode remains deferred. Cloud/Distributed mode remains deferred.

**Source.** Locked Phase 13H.2 artifact `storytime-phase13h2-frontend-boundary-cleanup-local-bridge-component-hardening.tar.gz`, SHA-256 `833c223bafaa82c7680c33d61e2ababc6a9aa011f98dabf95dd00ba1ea250522`. Phase 13H.2 was locked out-of-band by the user as final decision-maker, per this prompt's required-state and roadmap context — the same narrow mechanical exception used at every prior phase transition; the source artifact internally recorded Phase 13H.2 as the then-current candidate, as expected for a prior-phase source. Protected surfaces — `pyproject.toml`, `uv.lock`, `frontend/package.json`, `frontend/package-lock.json`, `frontend/src/data/storytime-demo-export.json`, and `src/storytime/local_bridge/` — are byte-identical.

**Current phase ledger.** Phase 12 CLOSED · Phase 13 STARTED · Phase 13A–13F LOCKED · 13D.1 / 13D.2 LOCKED · Phase 13G LOCKED · Phase 13G.1 LOCKED · Phase 13H LOCKED · Phase 13H.1 LOCKED · Phase 13H.2 LOCKED · Phase 13H.3 implementation candidate / pending review / NOT locked · Phase 13I (Operator GUI Polish / Demo-Local Alignment) NOT STARTED · Phase 13J (Demo Walkthrough Refresh / Local Bridge Story Path) NOT STARTED. Phase 13 remains STARTED and is not closed.

---

# Phase 13H.2 implementation-candidate note — Frontend Boundary Cleanup / Local Bridge Component Hardening

**Date:** 2026-05-28
**Round type:** Phase 13H.2 — Frontend Boundary Cleanup / Local Bridge Component Hardening — a BORING frontend-only cleanup / hardening round over the locked Phase 13H.1. It corrects stale comments / docstrings and clarifies the local-bridge component boundary; it adds NO new runtime feature. The backend bridge is untouched; no dependency change, no archive-hygiene regression.
**Status:** Phase 13H.2 is an **implementation candidate / pending review — NOT locked.**
**Last locked phase:** Phase 13H.1 — Controlled Retry Submission from Frontend (LOCKED), over the earlier-locked Phase 13G / 13G.1 / 13H.
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13H.2 (implementation candidate, pending review).

**What Phase 13H.2 does.** It makes the frontend local-bridge boundary safe to extend before the deferred Phase 13H.3. It rewrites stale Phase 13H.1-era comments and module docstrings in the read-only surface (`LocalBridgeView.tsx`, `LocalActionLifecyclePanel.tsx`, `LocalBridgeStatusPanel.tsx`, `localBridgeClient.ts`, `localBridgeTypes.ts`) so they describe the boundary as it actually is today: a GET-only observability client, with the single controlled submission path living separately in `localBridgeActions.ts` (added in locked Phase 13H.1). Panel copy is made honest and panel-scoped — each read-only panel states it submits nothing and points to the one Controlled local retry request panel as the only browser-initiated submission. No component signature, exported type, or network method changes.

**What Phase 13H.2 deliberately does NOT do.** It adds no new action type and no generic action runner; the only browser-initiated submission is still the single controlled retry path that already landed in locked Phase 13H.1 (one POST /actions for the allowlisted action retry_failed_stage to the loopback bridge). It does not implement export refresh or reload, and it never touches the static export; the manual static export reload / read-model replacement remains deferred to the not-started Phase 13H.3. Acceptance is still not success. Full Local mode remains deferred. Cloud/Distributed mode remains deferred. Browser durable storage remains forbidden — no `localStorage` / `sessionStorage` / `IndexedDB` / cookies; the only state is transient, in-memory React state that a page reload may discard. The backend Origin/CORS logic, the read model, and the exported signatures of `localBridgeClient.ts` and `localBridgeActions.ts` are unchanged.

**Source.** Locked Phase 13H.1 artifact `storytime-phase13h1-controlled-retry-submission-from-frontend.tar.gz`, SHA-256 `84d678052e6d50631e4485b973d5af42586fbf4e38e5a59c0d481d56a97af0f1`. Protected surfaces — `pyproject.toml`, `uv.lock`, `frontend/package.json`, `frontend/package-lock.json`, `frontend/src/data/storytime-demo-export.json`, and `src/storytime/local_bridge/` — are byte-identical.

**Current phase ledger.** Phase 12 CLOSED · Phase 13 STARTED · Phase 13A–13F LOCKED · 13D.1 / 13D.2 LOCKED · Phase 13G LOCKED · Phase 13G.1 LOCKED · Phase 13H LOCKED · Phase 13H.1 LOCKED · Phase 13H.2 implementation candidate / pending review / NOT locked · Phase 13H.3+ NOT STARTED (Phase 13H.3 — manual static export reload / read-model replacement — is the next, future, not-started subphase). Phase 13 remains STARTED and is not closed.

---

# Phase 13H implementation-candidate note — Frontend Bridge Observability & Action Lifecycle Readiness

**Date:** 2026-05-28
**Round type:** Phase 13H — Frontend Bridge Observability & Action Lifecycle Readiness — a frontend-only round. The backend bridge is untouched; no dependency, no archive-hygiene regression.
**Status:** Phase 13H is an **implementation candidate / pending review — NOT locked.**
**Last locked phase:** Phase 13G — Local Bridge Contract Synchronization & Controlled Async Retry (LOCKED), including the Phase 13G.1 archive-hygiene cleanup (LOCKED).
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13H (implementation candidate, pending review).

**What Phase 13H introduces read-only frontend bridge observability and action lifecycle readiness.** It teaches the frontend to *understand* the locked Phase 13G local bridge before the frontend is ever allowed to *command* it. The browser can now optionally observe a locally-running bridge over loopback only — health, readiness/security posture, the queue snapshot, and an existing action's lifecycle state — through native-`fetch` read-only GET calls to `/health`, `/ready`, `/queue`, and `/actions/{actionRequestId}`. Three small read-only panels (status, queue snapshot, action lifecycle) render distinct safe states for unavailable / origin-rejected (403) / timeout / malformed / unexpected-schema / ready / degraded. The static Demo remains first-class and fully usable with no bridge running; disabled future actions remain disabled.

**What Phase 13H deliberately does NOT do.** No action is submitted from the browser. Browser action submission is deferred to Phase 13H.1. Acceptance is not success; a completed job is not a refreshed UI; export refresh is deferred. Full Local mode is deferred. Cloud/Distributed mode is deferred. Browser durable storage remains forbidden — no `localStorage` / `sessionStorage` / `IndexedDB`; the only state is transient, in-memory React state that a page reload may discard. The backend Origin/CORS logic and the read model are unchanged and are neither replaced nor mutated.

**Source.** Locked Phase 13G.1 cleanup artifact `storytime-phase13g1-archive-hygiene-cleanup.tar.gz`, SHA-256 `44c16e7d44a09f7a417e07a30501222acd50100fbb896404e1d1d4317430a014`. Protected surfaces — `pyproject.toml`, `uv.lock`, `frontend/package.json`, `frontend/package-lock.json`, `frontend/src/data/storytime-demo-export.json`, and `src/storytime/local_bridge/` — are byte-identical.

**Current phase ledger.** Phase 12 CLOSED · Phase 13 STARTED · Phase 13A–13F LOCKED · 13D.1 / 13D.2 LOCKED · Phase 13G LOCKED · Phase 13G.1 LOCKED · Phase 13H implementation candidate / pending review / NOT locked · Phase 13H.1+ NOT STARTED (Phase 13H.1 is the next, future, not-started subphase). Phase 13 remains STARTED and is not closed.

---

# Phase 13G.1 cleanup-candidate note — Archive Hygiene Cleanup

**Date:** 2026-05-28
**Round type:** Phase 13G.1 — Archive Hygiene Cleanup — a narrow, scalpel cleanup sub-round of Phase 13G. No bridge, DTO, queue, retry, frontend, CLI, or dependency behavior changes.
**Status:** Phase 13G.1 is an **archive-hygiene cleanup candidate / pending review — NOT locked.**
**Last locked phase:** Phase 13F — Local Bridge Architecture & Contract Baseline (LOCKED).
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13G (with cleanup sub-round Phase 13G.1).

**Why this cleanup exists.** GPT-5.5 found a blocking archive-hygiene issue in the Phase 13G deliverable before lock: the runtime SQLite database `runs/state.db` was packaged inside the artifact (it was created by `storytime doctor` in the working tree during Phase 13G validation and slipped past the manual junk check). Gemini agreed this is an absolute blocker and recommended expanding the cleanup to SQLite journal siblings and mechanical archive-hygiene hardening.

**What Phase 13G.1 removes leaked runtime database artifacts from the Phase 13G deliverable and tightens archive hygiene.** Specifically it: removes the leaked `runs/` runtime working-state directory (which restored parity with the locked Phase 13F baseline, which had no `runs/`); confirms no SQLite database / journal siblings (`*.db`, `*.sqlite`, `*.sqlite3`, `*.db-wal`, `*.db-shm`) remain anywhere in the tree; adds a canonical deterministic packaging script `scripts/build-artifact.sh` whose `--exclude` patterns make it impossible to package these runtime / cache / nested-archive artifacts again; adds a programmatic archive-hygiene guard `tests/test_archive_hygiene.py`; and hardens `.gitignore` with explicit database / journal / `node_modules` / `*.tsbuildinfo` patterns (defense-in-depth — `runs/` was already ignored).

**Source.** Phase 13G implementation artifact `storytime-phase13g-local-bridge-contract-sync-controlled-async-retry.tar.gz`, SHA-256 `7be82d98b80eaf86080b96e885c7c76a5d38210aa88f025cd994b16b401f696b`. All Phase 13G runtime source (`src/storytime/local_bridge/`) and the protected frontend / packaging surfaces are byte-identical; this cleanup changes only packaging, one hygiene test, `.gitignore`, and state docs.

**Current phase ledger.** Phase 12 CLOSED · Phase 13 STARTED · Phase 13A–13E LOCKED · 13D.1 / 13D.2 LOCKED · Phase 13F LOCKED · Phase 13G implementation candidate / pending review / NOT locked · Phase 13G.1 archive-hygiene cleanup candidate / pending review / NOT locked · Phase 13H and later are NOT STARTED (Phase 13H is the next, future, not-started subphase). Phase 13 remains STARTED and is not closed.

---

# Phase 13G implementation-candidate note — Local Bridge Contract Synchronization & Controlled Async Retry

**Date:** 2026-05-28
**Round type:** Phase 13G — Local Bridge Contract Synchronization & Controlled Async Retry — the first *runtime* local-bridge sub-round over the locked Phase 13F architecture / contract baseline. It is a minimal, gated, safety-first bridge implementation.
**Status:** Phase 13G is an **implementation candidate / pending review — NOT locked.**
**Last locked phase:** Phase 13F — Local Bridge Architecture & Contract Baseline (LOCKED).
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13G.
**Next action:** Submit the Phase 13G artifact for GPT-5.5 review, then Gemini critique, then an explicit user decision — before locking Phase 13G or starting Phase 13H.

**Phase 13F lock (recorded honestly).** Phase 13F — Local Bridge Architecture & Contract Baseline — was reviewed by GPT-5.5 and Gemini; Gemini returned SAFE TO LOCK with no required edits, and the user, as final decision-maker, locked Phase 13F. **Phase 13F is LOCKED; it is the last locked phase.** Locked artifact `storytime-phase13f-local-bridge-architecture-contract-baseline.tar.gz`, SHA-256 `9d3286633e10a0ea3ec32f25ac90ae1369c4bc5bc871a17978bb41de861c9d2d`. Phase 13 — Portfolio Website / Operator GUI — remains STARTED and is not closed.

**What Phase 13G delivers (runtime, gated).** Phase 13G adds a new Python package `src/storytime/local_bridge/` implementing, against the locked Phase 13F contract:

- a loopback-only standard-library HTTP server (binds `127.0.0.1` only; every all-interfaces / non-loopback host is refused by the project's audited `validate_bind_host`);
- a strict origin policy — a request whose `Origin` header is present and does not exactly match the allowed loopback origin set is answered `403 Forbidden`; no wildcard `Access-Control-Allow-Origin` is ever emitted;
- the minimal endpoint set `GET /health`, `GET /ready`, `GET /queue`, `POST /actions`, `GET /actions/{actionRequestId}`;
- runtime DTO parsing / validation using plain dataclasses and dictionaries (no Pydantic, no jsonschema), synchronized against the Phase 13F example fixtures by a hard-gate test;
- a command-pattern router mapping each allowlisted action (`retry_failed_stage`, `inspect_trust_envelope`, `refresh_export`) to exactly one pre-approved handler — there is no free-form command / shell / SQL / file-path field, ever;
- a single-concurrency observable in-memory queue / worker (at most one in-flight long-running worker), with finite capacity, explicit backpressure, idempotency-key deduplication, and a queue snapshot exposing the Phase 13F observability concepts;
- exactly one controlled real action, `retry_failed_stage`, which maps to the existing locked Phase 10D governed re-run abstraction and runs only against an explicitly-configured (in tests, temporary) workspace, returning `202 Accepted` first and reporting honest completion / failure later. Acceptance is not success.

**What Phase 13G does NOT do (explicit scope boundary).** Phase 13G does not implement full Local mode; does not implement Cloud/Distributed mode; does not implement provider integrations, provider sync, or storage providers; does not wire the frontend, does not connect the browser to the bridge, and does not add any frontend bridge call; does not implement browser durable storage and forbids `localStorage` / `sessionStorage` / `IndexedDB`; does not implement a persistent or external queue (no Redis, no Celery, no cloud queue); does not implement a multi-worker, worker-fleet, or autoscaling executor; does not execute against a real user workspace; does not generate audio; and does not publish episodes. The frontend remains static / read-only and the browser remains non-durable.

**Current phase ledger.** Phase 12 CLOSED · Phase 13 STARTED · Phase 13A LOCKED · Phase 13B LOCKED · Phase 13C LOCKED · Phase 13D LOCKED · Phase 13D.1 LOCKED · Phase 13D.2 LOCKED · Phase 13E LOCKED · Phase 13F LOCKED · Phase 13G implementation candidate / pending review / NOT locked · Phase 13H and later are NOT STARTED (Phase 13H is the next, future, not-started subphase).

---

# Artifact Manifest Entry — Phase 13F Local Bridge Architecture & Contract Baseline — 2026-05-27

- Artifact: `storytime-phase13f-local-bridge-architecture-contract-baseline.tar.gz`
- Phase: Phase 13F — Local Bridge Architecture & Contract Baseline — a documentation-and-static-fixture architecture / contract baseline sub-round of the locked Phase 13E (the architectural lock before any Python local-bridge implementation is allowed; to the Local Bridge what Phase 13A was to the operator GUI). **Implementation candidate; pending review; not locked.** Per the Phase Closure Protocol, Phase 13F is implementation output until GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval complete. It does not lock Phase 13F, does not close Phase 13, and does not start Phase 13G.
- Source / base artifact: `storytime-phase13e-demo-mode-action-preview-operator-intent-boundary.tar.gz` (SHA-256 `a997f2ca9d213e28e140f47c63336367c8feda46ed994b41300f86b99f8d8164`, the locked Phase 13E lineage; SHA-256 verified on extraction).
- sha256: reported on delivery.
- Scope: documentation-and-static-fixture round; no runtime code. Phase 13F adds eleven new architecture / contract docs — `docs/local-bridge-architecture.md` (why a browser cannot execute local commands; why a local bridge is required for real Local mode; why Phase 13F does not implement it; the future bridge shape; loopback-only binding to `127.0.0.1`/`::1` with non-loopback rejection and never `0.0.0.0`; CORS/origin allowlist; strict DTO boundary; the no-arbitrary-command rule; the action allowlist; the command-pattern router mapping one DTO action to one pre-approved Python operation with no shell/SQL/arbitrary-path writes; the response/error/shutdown model; the action-completion→export-refresh update loop; the §15 execution-timing policy — long-running actions asynchronous, `202 Accepted` + `actionRequestId`/`jobId`, acceptance ≠ success, export refresh after a durable write, §15.3 rehydration-race avoidance via atomic write + identity-tagged read model; and the §16 risk table mapping the five Gemini risks), `docs/externalized-state-architecture.md`, `docs/browser-storage-policy.md`, `docs/local-mode-workspace-layout.md`, `docs/storage-targets-architecture.md`, `docs/action-execution-boundary.md`, `docs/local-action-dto-spec.md`, `docs/local-action-audit-spec.md`, `docs/local-mode-storage-contract.md`, `docs/local-action-queue-observability.md` (13 required gauges, 11 events, 14 attributes, local load-limiting / backpressure, stuck-action detection, distributed/cloud carry-forward — all defined, none implemented), and `docs/phase13f-local-bridge-contract-readiness.md` (a readiness checklist + recommended next phases). It adds a set of non-runtime JSON example fixtures under `docs/examples/` — `local-action-requests/` (retry-failed-stage, inspect-trust-envelope, refresh-export), `local-action-responses/` (retry-failed-stage.accepted, refresh-export.accepted), `local-action-audit-records/` (retry-failed-stage.audit) — each labelled future / documentation-only, using stable demo-safe ids and workspace-relative references, containing no secrets / shell / SQL / private paths. It adds one new Python test `tests/test_local_mode_contract_examples.py` validating those fixtures with plain Python (no JSON-schema dependency): required fields by type, allowlisted-action use, deferred-action absence, workspace + storageTarget presence, idempotency key for retry, accepted ≠ succeeded, async accepted → actionRequestId/jobId, audit → requestId/idempotencyKey, and no forbidden content. It advances the state-discipline guard `tests/test_failure_mode_regression.py` (the narrow, explicitly authorized mechanical change). It updates `frontend/README.md` and `README.md`, and synchronizes the State Preservation Bundle (`LLM_DIRECTOR.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/canonical-state.md` (append-only Phase 13E lock entry + Phase 13F entry), `docs/phase-history.md` (append-only Phase 13E lock entry + Phase 13F round), this `docs/artifact-manifest.md`, `docs/verification-log.md`, `docs/open-issues.md`, `docs/roundtable-import-bridge.md`, `docs/phase13-roadmap.md`, and `docs/frontend-gui-deferred-work-register.md`).
- Known constraints: Phase 13F implements **no** runtime code. It adds no local bridge, no server, no socket, no subprocess, no async queue, no queue workers, no queue metrics / exporters, no OpenTelemetry instrumentation, no storage providers, no provider integrations, no runtime schema validation, no router / history, no browser storage, no real Local mode, no Cloud/Distributed mode, and no mutation / action execution; the browser remains non-durable and the example fixtures are documentation artifacts only (never imported by runtime code, never generated by a running system, never claiming Phase 13F executed anything). **Protected boundary: `src/`, `frontend/src/` (including `frontend/src/data/storytime-demo-export.json`), `frontend/package.json`, `frontend/package-lock.json`, `pyproject.toml`, and `uv.lock` are byte-identical to the locked Phase 13E source — verified with `diff -q` against the Phase 13E source bundle.** No dependency was added. The `tests/` changes are the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` to the Phase 13F current-state expectations (current-phase / last-locked / forbidden-future / no-overclaim re-anchored to Phase 13F; new `test_handoff_state_records_phase_13e_locked` check; prior 13F-explicit framing check renamed to `test_handoff_state_addresses_phase_13g_explicitly`; future-phase fragment scan advanced to `13g`/`13h`; the append-only lock-record checks now also require the Phase 13E lock record), and the new `tests/test_local_mode_contract_examples.py`. Coverage is strengthened, not weakened.
- Tests: see `docs/verification-log.md` for the recorded gate results from this round.
- Archive hygiene: no `.mypy_cache`, `.ruff_cache`, `.pytest_cache`, `.import_linter_cache`, `.venv`, `runs/`, `feed/`, `logs/`, `operator-report/`, `__pycache__`, `*.pyc`, generated DB, generated audio, `.wav`/`.mp3`, screenshots/images, PDF/PowerPoint, frontend `node_modules`, frontend `dist/`, frontend build caches, nested `*.tar.gz`, or large binary artifacts in the output archive. The eleven new docs, the `docs/examples/` fixtures, the new test, the advanced guard, and the synchronized State Preservation Bundle are included. Built from a clean staging copy with only the Phase 13F docs, fixtures, and authorized test edits applied.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; Phase 13D locked; Phase 13D.1 locked; Phase 13D.2 locked; Phase 13E locked; **Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — STARTED**; Phase 13F — Local Bridge Architecture & Contract Baseline — implementation candidate, pending review, not locked. Phase 13G and every later Phase 13 subphase have not started; Phase 13 is not closed.

---

# Artifact Manifest Entry — Phase 13E Demo-Mode Action Preview / Operator Intent Boundary (LOCKED) — 2026-05-27

- Artifact: `storytime-phase13e-demo-mode-action-preview-operator-intent-boundary.tar.gz`
- Phase: Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary — the seventh subphase of Phase 13 (a sub-round of Phase 13D.2). **LOCKED / ACCEPTED / CANONICAL — it is the last locked phase before Phase 13F.** Phase 13E completed the Phase Closure Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no required edits; the user, as final decision-maker, then locked Phase 13E. This lock is recorded into the manifest by the Phase 13F round as part of its state synchronization — the same after-the-fact lock-recording pattern used for earlier subphases. The Phase 13E implementation-candidate manifest entry below is preserved as written and is superseded for status purposes by this lock entry.
- sha256: `a997f2ca9d213e28e140f47c63336367c8feda46ed994b41300f86b99f8d8164` (the locked Phase 13E lineage; it is the source/base artifact for Phase 13F).
- Scope at lock: frontend-only Demo-mode Action Preview round over the locked Phase 13D.2 operator GUI — a static view-model adapter (`frontend/src/data/actionPreviewAdapter.ts`) and a presentation panel (`frontend/src/components/ActionPreviewPanel.tsx` plus `ActionPreviewPanel.module.css`) integrated into Failure / Recovery, Governance / Safety, and Evidence / Validation **alongside** the unchanged `DisabledFutureActionCard`, opened by a separate "Preview action plan" control; the Demo / Local / Cloud-Distributed operating-mode model clarified (distinct from the Demo / Active / Candidate data-snapshot model); a `tests/test_action_preview_data_integrity.py` asserting adapter-referenced run/stage ids exist in the committed export. No live integration; no mutation; no audit records (nothing executed); no production hosting; no `src/`, no `pyproject.toml`, no `uv.lock`, no `frontend/package.json`, no `frontend/package-lock.json`, no root dependency change; `src/storytime/operator_export.py`, `frontend/src/data/storytime-demo-export.json`, the `storytime export-demo-ui` CLI contract, and `src/storytime/cli/app.py` were byte-identical to the Phase 13D.2 source, and `DisabledFutureActionCard` remained byte-identical and truly disabled.

---

# Artifact Manifest Entry — Phase 13E Demo-Mode Action Preview / Operator Intent Boundary (historical implementation-candidate record — see the LOCKED entry above) — 2026-05-27

- Artifact: `storytime-phase13e-demo-mode-action-preview-operator-intent-boundary.tar.gz`
- Phase: Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary — a static, **Demo-mode-only**, **non-consequential** sub-round of the locked Phase 13D.2. **Implementation candidate; pending review; not locked.** Per the Phase Closure Protocol, Phase 13E is implementation output until GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval complete. It does not lock Phase 13E, does not close Phase 13, and does not start Phase 13F.
- Source / base artifact: `storytime-phase13d2-static-demo-walkthrough-reviewer-story-path.tar.gz` (SHA-256 `cd553679ce109483b69e99f51fceab34af216c9b1ce7dfe859fc7b78c13cd429`, the locked Phase 13D.2 lineage; SHA-256 verified on extraction).
- sha256: reported on delivery.
- Scope: frontend-only Demo-mode Action Preview round. Phase 13E adds a static view-model adapter `frontend/src/data/actionPreviewAdapter.ts` (typed action-preview definitions — stable id, label, category, current mode (Demo), execution status (Preview only / non-consequential), target object references for run id / stage id / governance decision id / failure queue item / evidence artifact, target context label, what the operator is trying to accomplish, why blocked in Demo mode, precondition checklist, evidence to inspect first, risk level and explanation, illustrative future Local-mode request shape labelled "Future request shape — illustrative only, not executable in Demo mode", Cloud/Distributed considerations, audit expectations, failure behaviour expectation, what remains disabled, related view, optional related run id; plus operating-mode model constants for Demo / Local / Cloud-Distributed); adds a presentation component `frontend/src/components/ActionPreviewPanel.tsx` plus `ActionPreviewPanel.module.css` (a presentation shell that maps over adapter data and renders the selected preview with safety / honesty labels — "Demo mode", "Preview only", "No state changed", "Action plan, not action result", "Execution requires future Local mode", "Cloud/Distributed execution is not implemented", "No audit record generated because nothing executed", "No local bridge is running", "No backend command was called"); integrates the panel into Failure / Recovery, Governance / Safety, and Evidence / Validation **alongside** the existing `DisabledFutureActionCard` / `DisabledFutureActionList` (which remains unchanged: real `<button disabled={true}>` with no `onClick`) via a separate, clearly-labelled "Preview action plan" affordance — the inline preview panel opens via local `useState<ActionPreviewId | null>` only (no router, no Context, no persistence, no URL params, no `localStorage`/`sessionStorage`); implements the first five action previews — retry-failed-stage (target run `run-2026-0520-review`, stage `run-2026-0520-review:governance-gate`, related disabled action `run-2026-0520-review:retry`), inspect-trust-envelope (target run `run-2026-0520-review`, non-mutating inspection), record-review-decision (target run `run-2026-0520-review`, related disabled action `run-2026-0520-review:open-review`), regenerate-operator-report (target evidence/report surface), refresh-export (target static export `frontend/src/data/storytime-demo-export.json`); advances the state-discipline guard `tests/test_failure_mode_regression.py` (the narrow, explicitly authorized mechanical change); adds a new `tests/test_action_preview_data_integrity.py` that opens both `frontend/src/data/storytime-demo-export.json` and `frontend/src/data/actionPreviewAdapter.ts` (as text), extracts run-id and stage-id targets referenced by the adapter, and asserts each exists in the committed static export (no new test framework dependency); updates `frontend/README.md`, lightly updates `README.md`; and synchronizes the State Preservation Bundle (`LLM_DIRECTOR.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/canonical-state.md` (append-only Phase 13D.2 lock entry + Phase 13E entry), `docs/phase-history.md` (append-only Phase 13D.2 lock entry + Phase 13E round), this `docs/artifact-manifest.md`, `docs/verification-log.md`, `docs/open-issues.md`, `docs/roundtable-import-bridge.md`, `docs/phase13-roadmap.md`, and `docs/frontend-gui-deferred-work-register.md` (new §15 records Demo-mode action previews implemented; existing deferred items refreshed to note that real Local mode, actual local bridge, actual local server, CLI-mediated action execution, refreshed export update loop, hash routing / browser history, Cloud/Distributed mode, and actual retry/rerun/approval/report-regeneration execution remain deferred, with the note that "Phase 13E models operator intent in Demo mode. It does not execute actions.")).
- Known constraints: Phase 13E is a static, Demo-mode-only, export-backed frontend round. It adds no server, no live API, no `fetch`/`axios`/`localhost`/network call, no `localStorage`/`sessionStorage`, no router/hash routing/browser History API, no Context provider, no global preview/action state, no watcher, no backend-to-frontend runtime coupling, no actual retry/rerun/approval/report regeneration/export refresh, no authentication, no Local mode, no Cloud/Distributed mode, no audit-record generation (nothing executed), no production hosting, no cloud deployment, no fake-execution surface, no Demo/Active/Candidate snapshot switching, and no dynamic file loading. The visibly-disabled review and recovery affordances continue to be visibly disabled and carry no mutation handlers — the Phase 13D.1 `DisabledFutureActionCard` is not modified; no `onClick` is added to the disabled button. **Protected boundary: `src/storytime/operator_export.py`, `frontend/src/data/storytime-demo-export.json`, the `storytime export-demo-ui` CLI contract, and `src/storytime/cli/app.py` are byte-identical to the locked Phase 13D.2 source — verified with `diff -q` against the Phase 13D.2 source bundle.** No `src/`, `pyproject.toml`, `uv.lock`, `frontend/package.json`, `frontend/package-lock.json`, or root dependency changed. The frontend adds no global CSS selector (every new style lives in the new CSS Module); the existing global `.data-chip` rule is reused as-is. No CSS art, SVG, image, diagram, animation library, charting library, router, state library, UI library, or schema-validation dependency was added. The `tests/` changes are the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` to the Phase 13E current-state expectations (current-phase / last-locked / forbidden-future / no-overclaim re-anchored to Phase 13E; new `test_handoff_state_records_phase_13d2_locked` check; prior 13E-explicit framing check renamed to `test_handoff_state_addresses_phase_13f_explicitly`; future-phase fragment scan advanced to `13f`/`13g`; the append-only lock-record checks now also require the Phase 13D.2 lock record; the `_FORBIDDEN_OVERCLAIM_CLAIMS` list re-anchored to Phase 13E with new entries forbidding overclaims of real action execution, real retry/rerun/approval/report regeneration, Local mode, Cloud/Distributed mode, local bridge/local server, audit-record generation, persisted action state, backend connection, live data, snapshot switching, and production/cloud hosting), and one new `tests/test_action_preview_data_integrity.py` data-integrity test. Coverage is strengthened, not weakened. `docs/known-limitations.md`, `docs/architecture-baseline.md`, `docs/GUI_vision.md`, and `docs/frontend-static-export-contract.md` are intentionally unchanged.
- Tests: see `docs/verification-log.md` for the recorded gate results from this round.
- Archive hygiene: no `.mypy_cache`, `.ruff_cache`, `.pytest_cache`, `.import_linter_cache`, `.venv`, `runs/`, `feed/`, `logs/`, `operator-report/`, `__pycache__`, `*.pyc`, generated DB, generated audio, `.wav`/`.mp3`, screenshots/images, PDF/PowerPoint, frontend `node_modules`, frontend `dist/`, frontend build caches, nested `*.tar.gz`, or large binary artifacts in the output archive. The frontend source (incl. the new `ActionPreviewPanel.tsx`, `ActionPreviewPanel.module.css`, `actionPreviewAdapter.ts`, and the lightly updated `FailureRecoveryView.tsx`, `GovernanceSafetyView.tsx`, `EvidenceValidationView.tsx`), `frontend/package.json`, `frontend/package-lock.json`, the frontend TypeScript config, the frontend README, and the committed `frontend/src/data/storytime-demo-export.json` are included. Built from a clean staging copy with only the Phase 13E frontend, docs, state, and authorized test edits applied.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; Phase 13D locked; Phase 13D.1 locked; Phase 13D.2 locked; **Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — STARTED**; Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary — implementation candidate, pending review, not locked. Phase 13F and every later Phase 13 subphase have not started; Phase 13 is not closed.

---

# Artifact Manifest Entry — Phase 13D.2 Static Demo Walkthrough / Reviewer Story Path (LOCKED) — 2026-05-27

- Artifact: `storytime-phase13d2-static-demo-walkthrough-reviewer-story-path.tar.gz`
- Phase: Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path — the sixth subphase of Phase 13 (a sub-round of Phase 13D.1). **LOCKED / ACCEPTED / CANONICAL — it is the last locked phase before Phase 13E.** Phase 13D.2 completed the Phase Closure Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no required edits; the user, as final decision-maker, then locked Phase 13D.2. This lock is recorded into the manifest by the Phase 13E round as part of its state synchronization — the same after-the-fact lock-recording pattern used for earlier subphases. The Phase 13D.2 implementation-candidate manifest entry below is preserved as written and is superseded for status purposes by this lock entry.
- sha256: `cd553679ce109483b69e99f51fceab34af216c9b1ce7dfe859fc7b78c13cd429` (the locked Phase 13D.2 lineage; it is the source/base artifact for Phase 13E).
- Scope at lock: frontend-only static demo-readiness round over the locked Phase 13D.1 operator GUI — the real read-only Demo Walkthrough view (`frontend/src/components/DemoWalkthroughView.tsx` plus its CSS Module) replacing the Phase 13D.1 placeholder, the static `demoWalkthroughAdapter.ts` view-model holding the long-form route content, four reviewer routes (5-minute scan, 10-minute SE-style demo, technical deep-dive, self-guided reviewer) switched by a simple segmented control with local `useState<RouteId>`, eight embedded architecture-checkpoint cards absorbing ~80–90% of an Architecture Story narrative, a "what is intentionally deferred" section, interview / SE talking-point callout cards, and `frontend/src/navigation.ts` + `App.tsx` updated to promote Demo Walkthrough to a real view. No live integration; no mutation; no production hosting; no `src/`, no `pyproject.toml`, no `uv.lock`, no `frontend/package.json`, no `frontend/package-lock.json`, no root dependency change; `src/storytime/operator_export.py`, `frontend/src/data/storytime-demo-export.json`, the `storytime export-demo-ui` CLI contract, and `src/storytime/cli/app.py` were byte-identical to the Phase 13D.1 source.

---

# Artifact Manifest Entry — Phase 13D.2 Static Demo Walkthrough / Reviewer Story Path (historical implementation-candidate record — see the LOCKED entry above) — 2026-05-27

- Artifact: `storytime-phase13d2-static-demo-walkthrough-reviewer-story-path.tar.gz`
- Phase: Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path — a static / read-only demo-readiness sub-round of the locked Phase 13D.1. **Implementation candidate; pending review; not locked.** Per the Phase Closure Protocol, Phase 13D.2 is implementation output until GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval complete. It does not lock Phase 13D.2, does not close Phase 13, and does not start Phase 13E.
- Source / base artifact: `storytime-phase13d1-static-operator-gui-refinement-evidence-disabled-actions.tar.gz` (SHA-256 `812841381075e0e7839266512eb6d7f41bf2d890ee4c82b91627ce824f5b1eae`, the locked Phase 13D.1 lineage; SHA-256 verified on extraction).
- sha256: reported on delivery.
- Scope: frontend-only static demo-readiness round. Phase 13D.2 adds a real read-only Demo Walkthrough / Reviewer Story Path view (`frontend/src/components/DemoWalkthroughView.tsx` + `DemoWalkthroughView.module.css`) replacing the Phase 13D.1 placeholder; adds a static view-model adapter (`frontend/src/data/demoWalkthroughAdapter.ts`) holding the long-form route content (route definitions, step definitions, architecture checkpoints, deferred-work explanations, interview / SE talking points, repository references, stable run-id constants `GOLDEN_RUN_ID` and `REVIEW_RUN_ID`); offers four reviewer routes (5-minute scan, 10-minute SE-style demo, technical deep-dive, self-guided reviewer) switched by a local `useState<RouteId>` segmented control (no router, no Context, no persistence); each step carries title, target view, what to inspect, what it proves, talking points, and an in-line navigation affordance into the relevant existing view; steps pointing to a specific run identify it by stable id (`run-2026-0518-golden` for the golden-path run; `run-2026-0520-review` for the review-required run); embeds eight architecture-checkpoint cards (local-first design, deterministic static export, backend owns truth / frontend owns understanding, read-only operator surface, static evidence boundary, disabled-action boundary, Demo / Active / Candidate as data snapshots not deployment environments, why Phase 13E must be explicitly gated); includes a "what is intentionally deferred" section and interview / SE talking-point callout cards; absorbs ~80–90% of an Architecture Story narrative as embedded checkpoints; updates `frontend/src/navigation.ts` so the Demo Walkthrough nav entry is `soon: false` and sits in the real-views group (the `PLACEHOLDERS` map no longer includes `demo`; Architecture Story / Roadmap / Settings still point to Phase 13E or later, with the Architecture Story placeholder copy refreshed to note Phase 13D.2's embedded-checkpoint coverage); updates `frontend/src/App.tsx` to render `<DemoWalkthroughView onNavigate={setView} onInspectRun={inspectRun} />` for case `"demo"` and advances the brand tag and footer copy to Phase 13D.2; advances the state-discipline guard `tests/test_failure_mode_regression.py` (the narrow, explicitly authorized mechanical change); updates `frontend/README.md` and lightly updates `README.md`; and synchronizes the State Preservation Bundle (`LLM_DIRECTOR.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/canonical-state.md` (append-only Phase 13D.1 lock entry + Phase 13D.2 entry), `docs/phase-history.md` (append-only Phase 13D.1 lock entry + Phase 13D.2 round), this `docs/artifact-manifest.md`, `docs/verification-log.md`, `docs/open-issues.md`, `docs/roundtable-import-bridge.md`, `docs/phase13-roadmap.md`, and `docs/frontend-gui-deferred-work-register.md` (Demo Walkthrough now marked implemented; new §13 records the Demo Walkthrough implementation; new §14 records the deferred "Standalone Architecture Story / System Boundary Reference" item)).
- Known constraints: Phase 13D.2 is a static, read-only, export-backed frontend round. It adds no server, no live API, no `fetch`/`axios`/`localhost`/network call, no watcher, no backend-to-frontend runtime coupling, no mutation, no authentication, no cloud deployment, no production hosting, no dynamic file loading, and no Demo / Active / Candidate switching; the visibly-disabled review and recovery affordances continue to be visibly disabled and carry no mutation handlers. **Protected boundary: `src/storytime/operator_export.py`, `frontend/src/data/storytime-demo-export.json`, the `storytime export-demo-ui` CLI contract, and `src/storytime/cli/app.py` are byte-identical to the locked Phase 13D.1 source — verified with `diff -q` against the Phase 13D.1 source bundle.** No `src/`, `pyproject.toml`, `uv.lock`, `frontend/package.json`, `frontend/package-lock.json`, or root dependency changed. The frontend adds no global CSS selector (every new style lives in the new CSS Module); the existing global `.data-chip` rule from Phase 13D is reused as-is. No CSS art, SVG, image, diagram, animation library, charting library, or router was added. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` to the Phase 13D.2 current-state expectations: `_CURRENT_PHASE` advanced to "phase 13d.2", `_LAST_LOCKED_PHASE` advanced to "phase 13d.1", `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 13D.2 lock, premature Phase 13 closure, and a premature Phase 13E-or-later start (while allowing the now-legitimate "phase 13d.1 is locked" claims), `_FORBIDDEN_OVERCLAIM_CLAIMS` re-anchored to Phase 13D.2 with new entries forbidding live-CI / live-telemetry, snapshot-switching, dynamic-loading, and standalone-architecture-story overclaims, a new `test_handoff_state_records_phase_13d1_locked` check added, the append-only lock-record checks now additionally require the Phase 13D.1 lock record, and the "current phase not claimed locked" check continues to use a direct substring scan (the period inside "Phase 13D.2" is itself a fragment-split character). Coverage is strengthened, not weakened. `docs/known-limitations.md`, `docs/architecture-baseline.md`, `docs/GUI_vision.md`, and `docs/frontend-static-export-contract.md` are intentionally unchanged.
- Tests: see `docs/verification-log.md` for the recorded gate results from this round.
- Archive hygiene: no `.mypy_cache`, `.ruff_cache`, `.pytest_cache`, `.import_linter_cache`, `.venv`, `runs/`, `feed/`, `logs/`, `operator-report/`, `__pycache__`, `*.pyc`, generated DB, generated audio, `.wav`/`.mp3`, screenshots/images, PDF/PowerPoint, frontend `node_modules`, frontend `dist/`, frontend build caches, nested `*.tar.gz`, or large binary artifacts in the output archive. The frontend source (incl. the new `DemoWalkthroughView.tsx`, `DemoWalkthroughView.module.css`, `demoWalkthroughAdapter.ts`, and the updated `navigation.ts` / `App.tsx`), `frontend/package.json`, `frontend/package-lock.json`, the frontend TypeScript config, the frontend README, and the committed `frontend/src/data/storytime-demo-export.json` are included. Built from a clean staging copy with only the Phase 13D.2 frontend, docs, state, and authorized test edits applied.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; Phase 13D locked; Phase 13D.1 locked; **Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — STARTED**; Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path — implementation candidate, pending review, not locked. Phase 13E and every later Phase 13 subphase have not started; Phase 13 is not closed.

---

# Artifact Manifest Entry — Phase 13D.1 Static Operator GUI Refinement / Evidence & Disabled Action Discipline (LOCKED) — 2026-05-27

- Artifact: `storytime-phase13d1-static-operator-gui-refinement-evidence-disabled-actions.tar.gz`
- Phase: Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline — the fifth subphase of Phase 13 (a sub-round of Phase 13D). **LOCKED / ACCEPTED / CANONICAL — it is the last locked phase.** Phase 13D.1 completed the Phase Closure Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no required edits; the user, as final decision-maker, then locked Phase 13D.1. This lock is recorded into the manifest by the Phase 13D.2 round as part of its state synchronization — the same after-the-fact lock-recording pattern used for earlier subphases. The Phase 13D.1 implementation-candidate manifest entry below is preserved as written and is superseded for status purposes by this lock entry.
- sha256: `812841381075e0e7839266512eb6d7f41bf2d890ee4c82b91627ce824f5b1eae` (the locked Phase 13D.1 lineage; it is the source/base artifact for Phase 13D.2).
- Scope at lock: frontend-only static refinement over the locked Phase 13D operator GUI — the reusable `DisabledFutureActionCard` / `DisabledFutureActionList` component pair, the refactored Governance / Safety and Failure / Recovery views, the real Evidence / Validation view with mandatory STATIC PORTFOLIO DATA disclaimer and repository-relative evidence references, the evidence adapter with the Demo / Active / Candidate Data Source framing, and the `frontend/src/navigation.ts` extraction (App.tsx 228 → 136 lines). No live integration; no mutation; no production hosting; no `src/`, no `pyproject.toml`, no `uv.lock`, no `frontend/package.json`, no `frontend/package-lock.json`, no root dependency change; `src/storytime/operator_export.py`, `frontend/src/data/storytime-demo-export.json`, the `storytime export-demo-ui` CLI contract, and `src/storytime/cli/app.py` were byte-identical to the Phase 13D source.

---

# Artifact Manifest Entry — Phase 13D.1 Static Operator GUI Refinement / Evidence & Disabled Action Discipline (historical implementation-candidate record — see the LOCKED entry above) — 2026-05-27

- Artifact: `storytime-phase13d1-static-operator-gui-refinement-evidence-disabled-actions.tar.gz`
- Phase: Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline — a static / read-only refinement sub-round of the locked Phase 13D. **Implementation candidate; pending review; not locked.** Per the Phase Closure Protocol, Phase 13D.1 is implementation output until GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval complete. It does not lock Phase 13D.1, does not close Phase 13, and does not start Phase 13E.
- Source / base artifact: `storytime-phase13d-operator-workflow-view-expansion-governance-failure.tar.gz` (SHA-256 `5ec0b1edaaedfed2f3ae9b3e221e6a9089c52b8df152c4824503e7ca796894f3`, the locked Phase 13D lineage; SHA-256 verified on extraction).
- sha256: reported on delivery.
- Scope: frontend-only static refinement. Phase 13D.1 adds a reusable disabled-future-action display component (`frontend/src/components/DisabledFutureActionCard.tsx` + `DisabledFutureActionCard.module.css`) backed by real `<button disabled={true}>` elements with no `onClick` handlers and no fake mutation props; refactors the locked Governance / Safety and Failure / Recovery views to consume the new component (removing their local `DisabledActionRow` functions); replaces the Evidence / Validation placeholder with a real read-only view (`frontend/src/components/EvidenceValidationView.tsx` + `EvidenceValidationView.module.css`) that renders the mandatory **STATIC PORTFOLIO DATA — NOT A LIVE CI/CD DASHBOARD** disclaimer, a scope strip of static facts from the locked Phase 13C export (schemaVersion, generatedBy, run / failure-queue / governance-row counts), a claims-vs-proof category grid, a Data Source / Demo Snapshot framing card (Demo current; Active / Candidate as future **data snapshots, not deployment environments**), a repository-references list, and a talking-points block; adds an evidence view-model helper (`frontend/src/data/evidenceAdapter.ts`) organising the static categories, Data Source snapshots, and disclaimer constant; extracts nav metadata from `App.tsx` into `frontend/src/navigation.ts` (View type, NAV array, PLACEHOLDERS map) so `App.tsx` drops from 228 → 136 lines while preserving plain `useState` navigation, the `inspectRun(runId)` prop-drilled drill-down, and no router; promotes Evidence / Validation in `App.tsx` from a placeholder to a real view; advances the brand tag and footer copy to Phase 13D.1; advances the state-discipline guard `tests/test_failure_mode_regression.py` (the narrow, explicitly authorized mechanical change); updates `frontend/README.md` and lightly updates `README.md`; and synchronizes the State Preservation Bundle (`LLM_DIRECTOR.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/canonical-state.md` (append-only Phase 13D lock entry + Phase 13D.1 entry), `docs/phase-history.md` (append-only Phase 13D lock entry + Phase 13D.1 round), this `docs/artifact-manifest.md`, `docs/verification-log.md`, `docs/open-issues.md`, `docs/roundtable-import-bridge.md`, `docs/phase13-roadmap.md`, and `docs/frontend-gui-deferred-work-register.md` (the prior Phase 13D "Demo / Blue / Green" §8 is renamed to "Demo / Active / Candidate" to remove blue/green deployment ambiguity, and new §10–§12 record the implemented disabled-action component, the Evidence / Validation view, and the navigation extraction)).
- Known constraints: Phase 13D.1 is a static, read-only, export-backed frontend round. It adds no server, no live API, no `fetch`/`axios`/`localhost`/network call, no watcher, no backend-to-frontend runtime coupling, no mutation, no authentication, no cloud deployment, and no production hosting; the visibly-disabled review and recovery affordances continue to be visibly disabled and carry no mutation handlers. **Protected boundary: `src/storytime/operator_export.py`, `frontend/src/data/storytime-demo-export.json`, the `storytime export-demo-ui` CLI contract, and `src/storytime/cli/app.py` are byte-identical to the locked Phase 13D source — verified with `diff -q` against the Phase 13D source bundle.** No `src/`, `pyproject.toml`, `uv.lock`, or root dependency changed. The frontend adds no global CSS selector (every new style lives in the new CSS Modules); the existing global `.data-chip` rule from Phase 13D is reused as-is. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` to the Phase 13D.1 current-state expectations: `_CURRENT_PHASE` advanced to "phase 13d.1", `_LAST_LOCKED_PHASE` advanced to "phase 13d", `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 13D.1 lock, premature Phase 13 closure, and a premature Phase 13E-or-later start (while allowing the now-legitimate "phase 13d is locked" claims), `_FORBIDDEN_OVERCLAIM_CLAIMS` re-anchored to Phase 13D.1 with new entries forbidding live-CI, snapshot-switching, and promotion overclaims, a new `test_handoff_state_records_phase_13d_locked` check added, the append-only lock-record checks now additionally require the Phase 13D lock record, and the "current phase not claimed locked" check rewritten to do a direct substring scan rather than fragment-splitting (the period inside "Phase 13D.1" is itself a fragment-split character). Coverage is strengthened, not weakened. `docs/known-limitations.md`, `docs/architecture-baseline.md`, `docs/GUI_vision.md`, and `docs/frontend-static-export-contract.md` are intentionally unchanged.
- Tests: see `docs/verification-log.md` for the recorded gate results from this round.
- Archive hygiene: no `.mypy_cache`, `.ruff_cache`, `.pytest_cache`, `.import_linter_cache`, `.venv`, `runs/`, `feed/`, `logs/`, `operator-report/`, `__pycache__`, `*.pyc`, generated DB, generated audio, `.wav`/`.mp3`, screenshots/images, PDF/PowerPoint, frontend `node_modules`, frontend `dist/`, frontend build caches, nested `*.tar.gz`, or large binary artifacts in the output archive. The frontend source (incl. the new CSS Modules and the new `navigation.ts`, `DisabledFutureActionCard.tsx`, `EvidenceValidationView.tsx`, `evidenceAdapter.ts`), `frontend/package.json`, `frontend/package-lock.json`, the frontend TypeScript config, the frontend README, and the committed `frontend/src/data/storytime-demo-export.json` are included. Built from a clean staging copy with only the Phase 13D.1 frontend, docs, state, and authorized test edits applied.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; Phase 13D locked; **Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — STARTED**; Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline — implementation candidate, pending review, not locked. Phase 13E and every later Phase 13 subphase have not started; Phase 13 is not closed.

---

# Artifact Manifest Entry — Phase 13D Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) (LOCKED) — 2026-05-27

- Artifact: `storytime-phase13d-operator-workflow-view-expansion-governance-failure.tar.gz`
- Phase: Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) — the fourth subphase of Phase 13 — Portfolio Website / Operator GUI. **LOCKED / ACCEPTED / CANONICAL — it is the last locked phase.** Phase 13D completed the Phase Closure Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no required edits; the user, as final decision-maker, then locked Phase 13D. This lock is recorded into the manifest by the Phase 13D.1 round as part of its state synchronization — the same after-the-fact lock-recording pattern used for earlier subphases. The Phase 13D implementation-candidate manifest entry below is preserved as written and is superseded for status purposes by this lock entry.
- sha256: `5ec0b1edaaedfed2f3ae9b3e221e6a9089c52b8df152c4824503e7ca796894f3` (the locked Phase 13D lineage; it is the source/base artifact for Phase 13D.1).
- Scope at lock: frontend-only operator workflow view expansion — two new real read-only operator views (Governance / Safety, Failure / Recovery) and their CSS Modules; two domain-specific view-model adapters projecting the locked Phase 13C export; an ambient CSS-Modules TypeScript declaration; App-level navigation rewiring with the read-only "Data source · Demo Snapshot" header chip and inspect-this-run drill-down; one small `.data-chip` rule added to the global stylesheet (the only global addition). No live integration; no mutation; no production hosting; no `src/`, no `pyproject.toml`, no `uv.lock`, no root dependency change; the protected Phase 13C backend export generator and JSON were byte-identical to the Phase 13C source.
- Current state after lock: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 CLOSED**; Phase 12A–12D all locked; **Phase 12 CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; Phase 13D locked; **Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — STARTED**; Phase 13D.1 is the current implementation candidate (recorded in the Phase 13D.1 entry above).

---

# Artifact Manifest Entry — Phase 13D Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) — 2026-05-27

- Artifact: `storytime-phase13d-operator-workflow-view-expansion-governance-failure.tar.gz`
- Phase: Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) — the fourth subphase of Phase 13 — Portfolio Website / Operator GUI. **Implementation candidate; pending review; not locked.** Per the Phase Closure Protocol, Phase 13D is implementation output until GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval complete. It does not lock Phase 13D, does not close Phase 13, and does not start Phase 13E.
- Source / base artifact: `storytime-phase13c-deterministic-read-only-static-export-frontend-data-alignment.tar.gz` (SHA-256 `1c24cf03283590d7f095d3805bc8f5d560e3583131c04e5be0359e0053145507`, the locked Phase 13C lineage; SHA-256 verified on extraction).
- sha256: reported on delivery.
- Scope: frontend-only operator workflow view expansion. Phase 13D expands two of the honest Phase 13B/13C placeholder views into real read-only operator views against the locked Phase 13C deterministic static export contract: **Governance / Safety** (per-run Trust Envelope decisions, source authorization categories, governance-gate result per run, display-discipline honesty list, evidence references, visibly-disabled review actions, drill-down) and **Failure / Recovery** (failure / review queue with per-row affected stage, structured failure summary, related governance decision, evidence, inspect-next guidance, visibly-disabled recovery actions, drill-down). It adds two new view components and their CSS Modules (`frontend/src/components/GovernanceSafetyView.tsx` / `GovernanceSafetyView.module.css` and `frontend/src/components/FailureRecoveryView.tsx` / `FailureRecoveryView.module.css`), two domain-specific view-model adapters (`frontend/src/data/governanceAdapter.ts` and `frontend/src/data/failureAdapter.ts`) projecting the locked Phase 13C export, an ambient CSS-Modules TypeScript declaration (`frontend/src/types/css-modules.d.ts`), App-level navigation rewiring (`frontend/src/App.tsx`) with a read-only "Data source · Demo Snapshot" header chip backed by the existing `EXPORT_META` adapter export and an inspect-this-run drill-down callback into the existing Pipeline Run Detail view (plain prop drilling, no router), and a tiny `.data-chip` rule added to the shared global stylesheet (`frontend/src/styles.css`) for the header chip — the only global addition. It advances the state-discipline guard `tests/test_failure_mode_regression.py` (the narrow, explicitly authorized mechanical change), updates `frontend/README.md` and lightly updates `README.md`, and synchronizes the State Preservation Bundle (`LLM_DIRECTOR.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/canonical-state.md` (append-only Phase 13C lock entry + Phase 13D entry), `docs/phase-history.md` (append-only Phase 13C lock entry + Phase 13D round), this `docs/artifact-manifest.md`, `docs/verification-log.md`, `docs/open-issues.md`, `docs/roundtable-import-bridge.md`, `docs/phase13-roadmap.md`, and `docs/frontend-gui-deferred-work-register.md`).
- Known constraints: Phase 13D is a static, read-only, export-backed frontend round. It adds no server, no live API, no `fetch`/`axios`/`localhost`/network call, no watcher, no backend-to-frontend runtime coupling, no mutation, no authentication, no cloud deployment, and no production hosting; recovery / review affordances are surfaced as visibly-disabled future actions labelled with the phase that would enable them (Phase 13E). **Protected boundary: `src/storytime/operator_export.py`, `frontend/src/data/storytime-demo-export.json`, and the `storytime export-demo-ui` CLI contract are byte-identical to the locked Phase 13C source — verified with `diff -q` against the Phase 13C source bundle.** No `src/`, `pyproject.toml`, `uv.lock`, or root dependency changed. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` to the Phase 13D current-state expectations: `_CURRENT_PHASE` advanced to "phase 13d", `_LAST_LOCKED_PHASE` advanced to "phase 13c", `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 13D lock, a premature Phase 13 closure, and a premature Phase 13E-or-later start, `_FORBIDDEN_OVERCLAIM_CLAIMS` re-anchored to Phase 13D, a new `test_handoff_state_records_phase_13c_locked` check added, and the append-only lock-record checks now additionally require the Phase 13C lock record. Coverage is strengthened, not weakened. `docs/known-limitations.md`, `docs/architecture-baseline.md`, `docs/GUI_vision.md`, and `docs/frontend-static-export-contract.md` are intentionally unchanged.
- Tests: see `docs/verification-log.md` for the recorded gate results from this round.
- Archive hygiene: no `.mypy_cache`, `.ruff_cache`, `.pytest_cache`, `.import_linter_cache`, `.venv`, `runs/`, `feed/`, `logs/`, `operator-report/`, `__pycache__`, `*.pyc`, generated DB, generated audio, `.wav`/`.mp3`, screenshots/images, PDF/PowerPoint, frontend `node_modules`, frontend `dist/`, frontend build caches, nested `*.tar.gz`, or large binary artifacts in the output archive. The frontend source (incl. the new CSS Modules), `frontend/package.json`, `frontend/package-lock.json`, the frontend TypeScript config, the frontend README, and the committed `frontend/src/data/storytime-demo-export.json` are included. Built from a clean staging copy with only the Phase 13D frontend, docs, state, and authorized test edits applied.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; **Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — STARTED**; Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) — implementation candidate, pending review, not locked. Phase 13E and every later Phase 13 subphase have not started; Phase 13 is not closed.

---

# Artifact Manifest Entry — Phase 13C Deterministic Read-Only Static Export / Frontend Data Alignment (LOCKED) — 2026-05-27

- Artifact: `storytime-phase13c-deterministic-read-only-static-export-frontend-data-alignment.tar.gz`
- Phase: Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment — the third subphase of Phase 13 — Portfolio Website / Operator GUI. **LOCKED / ACCEPTED / CANONICAL — it is the last locked phase.** Phase 13C completed the Phase Closure Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no required edits; the user, as final decision-maker, then locked Phase 13C. This lock is recorded into the manifest by the Phase 13D round as part of its state synchronization — the same after-the-fact lock-recording pattern used for earlier subphases. The Phase 13C implementation-candidate manifest entry below is preserved as written and is superseded for status purposes by this lock entry.
- sha256: `1c24cf03283590d7f095d3805bc8f5d560e3583131c04e5be0359e0053145507` (the locked Phase 13C lineage; it is the source/base artifact for Phase 13D).
- Scope at lock: deterministic, read-only data-boundary round — a small read-only backend export module (`src/storytime/operator_export.py`), a `storytime export-demo-ui` CLI command, the committed deterministic static JSON export (`frontend/src/data/storytime-demo-export.json` with `schemaVersion` `"1.0"`), the export contract document, the frontend / GUI deferred-work register, a frontend adapter and `StaticDemoExport` type, backend contract tests, and the rewired homepage and Pipeline Run Detail / Stage Timeline. No live integration; no mutation; no production hosting; no root dependency or `uv.lock` change.
- Current state after lock: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 CLOSED**; Phase 12A–12D all locked; **Phase 12 CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; **Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — STARTED**; Phase 13D is the current implementation candidate (recorded in the Phase 13D entry above).

---

# Artifact Manifest Entry — Phase 13C Deterministic Read-Only Static Export / Frontend Data Alignment — 2026-05-27

- Artifact: `storytime-phase13c-deterministic-read-only-static-export-frontend-data-alignment.tar.gz`
- Phase: Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment — the third subphase of Phase 13 — Portfolio Website / Operator GUI. **Implementation candidate; pending review; not locked.** Per the Phase Closure Protocol, Phase 13C is implementation output until GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval complete. It does not lock Phase 13C, does not close Phase 13, and does not start Phase 13D.
- Source / base artifact: `storytime-phase13b-typed-static-portfolio-shell-minimal-visual-pipeline-scaffold.tar.gz` (SHA-256 `9319ece26f5b457ddbbefaab346aba61cb61f65a6b7b729b5acaa12f30df3f24`, the locked Phase 13B lineage; SHA-256 verified on extraction).
- sha256: reported on delivery.
- Scope: read-only static data-boundary round. Phase 13C establishes a truthful, reproducible, deterministic data boundary between backend truth and the Phase 13B frontend ("backend owns truth, frontend owns understanding"). It adds: a small read-only backend export module (`src/storytime/operator_export.py`) and a `storytime export-demo-ui` CLI command (in `src/storytime/cli/app.py`) that together produce a deterministic static JSON export; the committed export artifact `frontend/src/data/storytime-demo-export.json` (carrying a top-level `schemaVersion` of `"1.0"`); the export contract document `docs/frontend-static-export-contract.md`; the frontend / GUI deferred-work register `docs/frontend-gui-deferred-work-register.md`; a frontend adapter `frontend/src/data/adapter.ts` and a `StaticDemoExport` envelope type appended to `frontend/src/types/storytime.ts`; and backend contract tests `tests/test_operator_export.py`. It rewires the Phase 13B homepage (`frontend/src/components/HomePage.tsx`) and Pipeline Run Detail / Stage Timeline view (`frontend/src/components/PipelineRunDetailPage.tsx`) to consume the export through the adapter; removes the hand-authored `frontend/src/data/storytime-demo-data.ts` (superseded by the generated export plus the adapter); updates user-visible Phase 13B → 13C wording across the frontend (`App.tsx`, `HomePage.tsx`, `PipelineRunDetailPage.tsx`, `Placeholder.tsx`); lightly updates `README.md` and `frontend/README.md`; advances the state-discipline guard `tests/test_failure_mode_regression.py` (the narrow, explicitly authorized mechanical change); and synchronizes the State Preservation Bundle (`LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/canonical-state.md` (append-only Phase 13B lock entry + Phase 13C entry), `docs/phase-history.md` (append-only Phase 13B lock entry + Phase 13C round), this `docs/artifact-manifest.md`, `docs/verification-log.md`, `docs/open-issues.md`, `docs/roundtable-import-bridge.md`, and `docs/phase13-roadmap.md`).
- Determinism: the export is built entirely from fixed demo data — no `datetime.now()`, no `uuid`, no randomness, no environment-dependent value — and serialized with sorted keys and a stable format. Running `storytime export-demo-ui` twice produces byte-identical JSON; the committed `frontend/src/data/storytime-demo-export.json` has SHA-256 `0b2989554a1f9fae1c5963527d3f59f882381f253aced2582087c233d42d6156`, and a contract test asserts the committed file equals a fresh render.
- Known constraints: Phase 13C is a static, read-only data-boundary round. It adds no server, no live API, no `fetch`/`axios`/`localhost`/network call, no watcher, no backend-to-frontend runtime coupling, no mutation, no authentication, no cloud deployment, and no production hosting. Unlike Phase 13B it adds small backend code, but that code is read-only and deterministic and changes no core pipeline runtime behaviour, `storytime rerun`, Trust Envelope enforcement, governance, telemetry, Docker behaviour, or the database schema; no ARCH-LOCKed contract change. `uv.lock` and root dependencies are unchanged. The `src/` changes are limited to the new `src/storytime/operator_export.py` and the `export-demo-ui` command plus its import added to `src/storytime/cli/app.py`; `pyproject.toml` changes only by adding `storytime.operator_export` to the two import-linter contract module lists. The `tests/` changes are the new `tests/test_operator_export.py` and the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` to the Phase 13C current-state expectations — it now guards against a premature Phase 13C lock, a premature Phase 13 closure, and a premature Phase 13D-or-later start, additionally requires the Phase 13B lock record, and re-anchors the no-overclaim guard to Phase 13C; coverage is strengthened, not weakened. `docs/known-limitations.md`, `docs/architecture-baseline.md`, and `docs/GUI_vision.md` are intentionally unchanged.
- Tests: see `docs/verification-log.md` for the recorded gate results from this round (backend gates and frontend gates).
- Archive hygiene: no `.mypy_cache`, `.ruff_cache`, `.pytest_cache`, `.import_linter_cache`, `.venv`, `runs/`, `feed/`, `logs/`, `operator-report/`, `__pycache__`, `*.pyc`, generated DB, generated audio, `.wav`/`.mp3`, screenshots/images, PDF/PowerPoint, frontend `node_modules`, frontend `dist/`, frontend build caches, nested `*.tar.gz`, or large binary artifacts in the output archive. The frontend source, `frontend/package.json`, `frontend/package-lock.json`, the frontend TypeScript config, the frontend README, and the committed `frontend/src/data/storytime-demo-export.json` are included. Built from a clean staging copy with only the Phase 13C backend export code, frontend, docs, state, and authorized test edits applied.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; Phase 13A locked; Phase 13B locked; **Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — STARTED**; Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment — implementation candidate, pending review, not locked. Phase 13D and every later Phase 13 subphase have not started; Phase 13 is not closed.

---

# Artifact Manifest Entry — Phase 13B Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold (LOCKED) — 2026-05-27

- Artifact: `storytime-phase13b-typed-static-portfolio-shell-minimal-visual-pipeline-scaffold.tar.gz`
- Phase: Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — the second subphase of Phase 13 — Portfolio Website / Operator GUI. **LOCKED / ACCEPTED / CANONICAL — it is the last locked phase.** Phase 13B completed the Phase Closure Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no required edits; the user, as final decision-maker, then locked Phase 13B. This lock is recorded into the manifest by the Phase 13C round as part of its state synchronization — the same after-the-fact lock-recording pattern used for earlier subphases. The Phase 13B implementation-candidate manifest entry below is preserved as written and is superseded for status purposes by this lock entry.
- sha256: `9319ece26f5b457ddbbefaab346aba61cb61f65a6b7b729b5acaa12f30df3f24` (the locked Phase 13B lineage; it is the source/base artifact for Phase 13C).
- Scope at lock: first frontend implementation round — a new top-level `frontend/` directory (React + TypeScript + Vite) with the frontend read-model contract, a two-run static demo dataset, the portfolio homepage, one Pipeline Run Detail view with a visual Stage Timeline, honest placeholders, and a frontend README. No `pyproject.toml`, `uv.lock`, or `src/` change.
- Current state after lock: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 CLOSED**; Phase 12A–12D all locked; **Phase 12 CLOSED**; Phase 13A locked; Phase 13B locked; **Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — STARTED**; Phase 13C is the current implementation candidate (recorded in the Phase 13C entry above).

---

# Artifact Manifest Entry — Phase 13B Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — 2026-05-27

- Artifact: `storytime-phase13b-typed-static-portfolio-shell-minimal-visual-pipeline-scaffold.tar.gz`
- Phase: Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — the second subphase of Phase 13 — Portfolio Website / Operator GUI, and the first frontend implementation round of Phase 13. **Implementation candidate; pending review; not locked.** Per the Phase Closure Protocol, Phase 13B is implementation output until GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval complete. It does not lock Phase 13B, does not close Phase 13, and does not start Phase 13C.
- Source / base artifact: `storytime-phase13a-portfolio-website-operator-gui-architecture-baseline.tar.gz` (SHA-256 `100098aa6280b740a6eeb862c1e1923d2e031bd02a06786b7a8b8ec07facf1c0`, the locked Phase 13A lineage; SHA-256 verified on extraction).
- sha256: reported on delivery.
- Scope: first frontend implementation round. Against the locked Phase 13A contract, Phase 13B adds a new top-level `frontend/` directory — a React 18 + TypeScript (strict) + Vite 5 project, standard CSS, and no external UI / component / state / charting library. It contains: the frontend read-model contract (`frontend/src/types/storytime.ts`); a static demo dataset of exactly two mock pipeline runs — one golden-path successful run, one governance review-required run (`frontend/src/data/storytime-demo-data.ts`); the portfolio homepage (`frontend/src/components/HomePage.tsx`); one Pipeline Run Detail view with a visual Stage Timeline (`frontend/src/components/PipelineRunDetailPage.tsx`, `frontend/src/components/StageTimeline.tsx`, `frontend/src/components/status.tsx`); honest placeholder components for the future portfolio sections and operator views (`frontend/src/components/Placeholder.tsx`); the app shell with state-based navigation (`frontend/src/App.tsx`, `frontend/src/main.tsx`, `frontend/src/styles.css`); the scaffold files (`frontend/package.json`, `frontend/package-lock.json`, `frontend/tsconfig.json`, `frontend/vite.config.ts`, `frontend/index.html`, `frontend/.gitignore`); and a frontend README (`frontend/README.md`). It lightly updates `README.md`, advances the state-discipline guard `tests/test_failure_mode_regression.py` (the narrow, explicitly authorized mechanical change), and synchronizes the State Preservation Bundle (`LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/canonical-state.md` (append-only Phase 13A lock entry + Phase 13B entry), `docs/phase-history.md` (append-only Phase 13A lock entry + Phase 13B round), this `docs/artifact-manifest.md`, `docs/verification-log.md`, `docs/open-issues.md`, `docs/roundtable-import-bridge.md`, and `docs/phase13-roadmap.md`).
- Known constraints: Phase 13B introduces a static, read-only, demo-data-backed frontend shell. It is not backend-connected, uses no live or runtime data, implements no mutations (retry, re-run, and review-decision actions appear only as visibly-disabled affordances), and is not production-hosted or cloud-deployed; it contacts no backend — no `fetch()`, no `axios`, no `localhost`, no network call. No `pyproject.toml`, `uv.lock`, or `src/` change (all byte-for-byte identical to the source artifact); no backend dependency change; no change to pipeline / `storytime rerun` / Trust Envelope enforcement / API / CLI / telemetry / Docker behaviour; no database schema change; no ARCH-LOCKed contract change; no Phase 13C+ work. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 13B current-state expectations — it now guards against a premature Phase 13B lock, a premature Phase 13 closure, and a premature Phase 13C-or-later start, additionally requires the Phase 13A lock record, and replaces the Phase 13A frontend-claim guard with a no-overclaim guard; coverage is strengthened, not weakened. `docs/known-limitations.md`, `docs/architecture-baseline.md`, and `docs/GUI_vision.md` are intentionally unchanged.
- Tests: see `docs/verification-log.md` for the recorded gate results from this round (backend gates and frontend gates).
- Archive hygiene: no `.mypy_cache`, `.ruff_cache`, `.pytest_cache`, `.import_linter_cache`, `.venv`, `runs/`, `feed/`, `logs/`, `operator-report/`, `__pycache__`, `*.pyc`, generated DB, generated audio, `.wav`/`.mp3`, screenshots/images, PDF/PowerPoint, frontend `node_modules`, frontend `dist/`, frontend build caches, nested `*.tar.gz`, or large binary artifacts in the output archive. The frontend source, `frontend/package.json`, `frontend/package-lock.json`, the frontend TypeScript config, and the frontend README are included. Built from a clean staging copy with only the Phase 13B frontend, README, state, and authorized test edits applied.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; **Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — STARTED**; Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — implementation candidate, pending review, not locked. Phase 13C and every later Phase 13 subphase have not started; Phase 13 is not closed.

---

# Artifact Manifest Entry — Phase 13A Portfolio Website / Operator GUI Architecture Baseline (LOCKED) — 2026-05-27

- Artifact: `storytime-phase13a-portfolio-website-operator-gui-architecture-baseline.tar.gz`
- Phase: Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — the first subphase of Phase 13 — Portfolio Website / Operator GUI. **LOCKED / ACCEPTED / CANONICAL — it is the last locked phase.** Phase 13A completed the Phase Closure Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no required edits; the user, as final decision-maker, then locked Phase 13A. This lock is recorded into the manifest by the Phase 13B round as part of its state synchronization — the same after-the-fact lock-recording pattern used for earlier subphases. The Phase 13A implementation-candidate manifest entry below is preserved as written and is superseded for status purposes by this lock entry.
- sha256: `100098aa6280b740a6eeb862c1e1923d2e031bd02a06786b7a8b8ec07facf1c0` (the locked Phase 13A lineage; it is the source/base artifact for Phase 13B).
- Scope at lock: documentation-only architecture-baseline round — five architecture-baseline `docs/` documents, no frontend application code, no `pyproject.toml` / `uv.lock` / `src/` change.
- Current state after lock: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 CLOSED**; Phase 12A–12D all locked; **Phase 12 CLOSED**; **Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — locked (the last locked phase)**; **Phase 13 — Portfolio Website / Operator GUI — STARTED**; Phase 13B is the current implementation candidate (recorded in the Phase 13B entry above).

---

# Artifact Manifest Entry — Phase 13A Portfolio Website / Operator GUI Architecture Baseline — 2026-05-27

- Artifact: `storytime-phase13a-portfolio-website-operator-gui-architecture-baseline.tar.gz`
- Phase: Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — the first subphase of Phase 13 — Portfolio Website / Operator GUI. **Implementation candidate; pending review; not locked.** Per the Phase Closure Protocol, Phase 13A is implementation output until GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval complete. It does not lock Phase 13A, does not close Phase 13, and does not start Phase 13B.
- Source / base artifact: `storytime-phase12d-phase12-closure-plan-final-portfolio-handoff.tar.gz` (SHA-256 `64ad09e875f0653608e0deb756f11ee5adc0d2ff1265e2039cbc51491f286cf8`, the locked Phase 12D lineage and final Phase 12 artifact; SHA-256 verified on extraction).
- sha256: reported on delivery.
- Scope: documentation-only architecture-baseline round. Phase 13A designs the portfolio website and the decoupled operator GUI on paper; it does not build either of them. Adds five `docs/` documents — `phase13-portfolio-website-architecture.md` (the Phase 13 purpose, the end-state website and operator-GUI vision, audiences and review paths, the website and operator information architectures, the local-first and future-cloud compatibility rules, and the Phase 13 success criteria), `frontend-backend-contract.md` (the "backend owns truth, frontend owns understanding" data contract — read-model categories, future action categories, the actions deliberately disabled for this round, and candidate data-source options), `phase13-roadmap.md` (the Phase 13A–13G subphase decomposition, with each subphase's objective, allowed and forbidden scope, acceptance criteria, and review gate), `portfolio-website-content-model.md` (the website section inventory mapped to existing repository source documents, with a content-honesty checklist), and `operator-gui-view-model.md` (the operator-GUI view inventory, the disabled and future actions, the empty / error / loading states, and the accessibility and readability requirements) — refines the earlier `docs/GUI_vision.md` sketch into an authoritative Phase 13 plan (the sketch file itself is left unchanged), lightly updates `README.md`, advances the state-discipline guard `tests/test_failure_mode_regression.py` (the narrow, explicitly authorized mechanical change), and synchronizes the State Preservation Bundle (`LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/canonical-state.md` (append-only Phase 12D lock entry + Phase 13A entry), `docs/phase-history.md` (append-only Phase 12D lock entry + Phase 13A round), this `docs/artifact-manifest.md`, `docs/verification-log.md`, `docs/open-issues.md`, and `docs/roundtable-import-bridge.md`).
- Known constraints: documentation and state changes only. Phase 13A is a planning round; it does not implement the portfolio website and does not implement the operator GUI. No React, Vite, TypeScript, JavaScript, CSS, or HTML application code; no `frontend/` / `web/` / `app/` directory; no `package.json` or `vite.config`; no `pyproject.toml`, `uv.lock`, or `src/` change (all byte-for-byte identical to the source artifact); no dependency change; no new product feature, UI, server, dashboard, browser mutation control, external asset, CDN, generated audio, screenshot/image/PDF/PowerPoint/binary asset, demo video, or runtime/cache artifact; no database schema change; no change to pipeline / `storytime rerun` / Trust Envelope enforcement / API / CLI / telemetry behaviour; no ARCH-LOCKed contract change. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 13A current-state expectations — it now guards against a premature Phase 13A lock, a premature Phase 13 closure, and a premature Phase 13B-or-later start, additionally requires the Phase 12D lock record, and adds a new check that no current-state doc falsely claims Phase 13A built the frontend, the portfolio website, or the operator GUI; coverage is strengthened, not weakened. `docs/known-limitations.md`, `docs/architecture-baseline.md`, and `docs/GUI_vision.md` are intentionally unchanged.
- Tests: see `docs/verification-log.md` for the recorded gate results from this round.
- Archive hygiene: no `.mypy_cache`, `.ruff_cache`, `.pytest_cache`, `.import_linter_cache`, `.venv`, `runs/`, `feed/`, `logs/`, `operator-report/`, `__pycache__`, `*.pyc`, generated DB, generated audio, `.wav`/`.mp3`, screenshots/images, PDF/PowerPoint, `node_modules`, nested `*.tar.gz`, or large binary artifacts in the output archive. Built from a clean extraction with only the Phase 13A documentation, README, state, and authorized test edits applied.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; **Phase 12D is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — STARTED**; Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — implementation candidate, pending review, not locked. Phase 13B and every later Phase 13 subphase have not started; Phase 13 is not closed.

# Artifact Manifest Entry — Phase 12D Phase 12 Closure Plan / Final Portfolio Handoff Definition (LOCKED — Phase 12 CLOSED) — 2026-05-27

- Artifact: `storytime-phase12d-phase12-closure-plan-final-portfolio-handoff.tar.gz`
- Phase: Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — the fourth subphase of Phase 12 — Portfolio / SE Demo Packaging. **LOCKED / ACCEPTED / CANONICAL — it is the last locked phase.** Phase 12D completed the Phase Closure Protocol: implementation, GPT-5.5 review, and Gemini critique. The Gemini review returned the verdict to lock Phase 12D and close Phase 12, with no critical findings, no non-blocking findings, and no required edits; the user, as final decision-maker, then locked Phase 12D and formally closed Phase 12. This lock and closure is recorded into the manifest by the Phase 13A round as part of its state synchronization — the same after-the-fact lock-recording pattern used for earlier subphases. The Phase 12D implementation-candidate manifest entry below is preserved as written and is superseded for status purposes by this lock entry.
- sha256: `64ad09e875f0653608e0deb756f11ee5adc0d2ff1265e2039cbc51491f286cf8` (the locked Phase 12D lineage; it is the source/base artifact for Phase 13A and the final Phase 12 artifact).
- Scope: documentation-only closure-definition round — three closure-definition `docs/` documents (`phase12-closure-plan.md`, `final-portfolio-handoff.md`, `phase12-final-review-checklist.md`), a light README reviewer-pointer refinement, the authorized advance of the state-discipline guard, and the synchronized State Preservation Bundle. No `pyproject.toml`, `uv.lock`, or `src/` change; no dependency change; no product behaviour change.
- Phase 12 closure: with Phase 12D locked, **Phase 12 — Portfolio / SE Demo Packaging — is CLOSED**. All four subphases (12A–12D) are locked; Phase 12A.1 and Phase 12B.1 / 12B.2 / 12B.3 are folded into their parent lock lineages as accepted cleanup sub-rounds. Phase 12E was optional, contingency-only work; the Phase 12D review found no substantive gap, so Phase 12E was not needed and never started.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — CLOSED**; Phase 12A–12D all locked; **Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**. Phase 13 — Portfolio Website / Operator GUI — is STARTED; Phase 13A is the current implementation candidate (recorded in the Phase 13A entry above).

# Artifact Manifest Entry — Phase 12D Phase 12 Closure Plan / Final Portfolio Handoff Definition — 2026-05-26

*Supersession note (added by Phase 13A): this is a historical point-in-time entry from the Phase 12D implementation round. Phase 12D is now LOCKED and is the last locked phase, and Phase 12 — Portfolio / SE Demo Packaging — is CLOSED; Phase 13A is the current implementation candidate (pending review, not locked). See the Phase 13A and Phase 12D (LOCKED) entries at the top of this file for current state.*

- Artifact: `storytime-phase12d-phase12-closure-plan-final-portfolio-handoff.tar.gz`
- Phase: Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — the fourth subphase of Phase 12 — Portfolio / SE Demo Packaging. **Implementation candidate; pending review; not locked.** Per the Phase Closure Protocol, Phase 12D is implementation output until GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval complete. It does not lock Phase 12D, does not close Phase 12, and does not start Phase 12E.
- Source / base artifact: `storytime-phase12c-portfolio-demo-narrative-public-presentation-kit.tar.gz` (SHA-256 `4c98a25d6bb0ae751b4ba33851bc60e7d7805d4fd31ebcfc45c2d30a659301da`, the locked Phase 12C lineage; SHA-256 verified on extraction).
- sha256: reported on delivery.
- Scope: documentation-only closure-definition round. It prepares the Phase 12 closure decision; it does not itself close Phase 12. Adds three `docs/` documents — `phase12-closure-plan.md` (Phase 12 closure criteria, the completed Phase 12A–12C asset inventory, the closure-readiness checklist, the remaining-gaps / no-go criteria, the close-after-12D vs bounded-cleanup vs separate-12E recommendation, and the Phase 13 boundary statement), `final-portfolio-handoff.md` (a cold-reader handoff: current-state snapshot, 5-minute / 15-minute / deep-architecture reviewer paths, a suggested demo flow, an evidence map, explicit limitations, and the next-phase boundary), and `phase12-final-review-checklist.md` (the checklist a reviewer uses to decide whether Phase 12D can lock and whether Phase 12 can close) — advances the state-discipline guard `tests/test_failure_mode_regression.py` (the narrow, explicitly authorized mechanical change), and synchronizes the State Preservation Bundle (`LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/canonical-state.md` (append-only Phase 12C lock entry + Phase 12D entry), `docs/phase-history.md` (append-only Phase 12C lock entry + Phase 12D round), this `docs/artifact-manifest.md`, `docs/verification-log.md`, `docs/open-issues.md`, and `docs/roundtable-import-bridge.md`).
- Known constraints: documentation and state changes only. No `pyproject.toml`, `uv.lock`, or `src/` change (all byte-for-byte identical to the source artifact); no dependency change; no new product feature, UI, server, dashboard, browser mutation control, JavaScript, frontend directory, React/Vite/TypeScript file, external asset, CDN, generated audio, screenshot/image/PDF/PowerPoint/binary asset, demo video, or runtime/cache artifact; no database schema change; no change to pipeline / `storytime rerun` / Trust Envelope enforcement / API / CLI / telemetry behaviour; no ARCH-LOCKed contract change; no Phase 13 GUI implementation. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 12D current-state expectations — it now guards against a premature Phase 12D lock, a premature Phase 12 closure, and a premature Phase 12E-or-later start, and additionally requires the Phase 12C lock record; coverage is strengthened, not weakened. `docs/known-limitations.md` and `docs/architecture-baseline.md` are intentionally unchanged.
- Tests: 592 passed (590 from the Phase 12C baseline plus 2 net from the strengthened state-discipline guard); ruff clean; mypy clean (85 source files, strict); lint-imports 2/2 kept; `storytime doctor` healthy; legal-hallucination scanner 0 violations (run inside the pytest suite, covering the three new documents).
- Archive hygiene: no `.mypy_cache`, `.ruff_cache`, `.pytest_cache`, `.import_linter_cache`, `.venv`, `runs/`, `feed/`, `logs/`, `operator-report/`, `__pycache__`, `*.pyc`, generated DB, generated audio, `.wav`/`.mp3`, screenshots/images, PDF/PowerPoint, `node_modules`, nested `*.tar.gz`, or large binary artifacts in the output archive. Built from a clean extraction with only the Phase 12D documentation, state, and authorized test edits applied.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A locked; Phase 12B locked; **Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — STARTED** and not closed; Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — implementation candidate, pending review, not locked. Phase 12E is optional, future, contingency-only work and has not started. Phase 13 — Operator GUI / Decoupled Frontend Vision — roadmap-preserved only, not started.

# Artifact Manifest Entry — Phase 12C Portfolio Demo Narrative / Public Presentation Kit (LOCKED) — 2026-05-26

- Artifact: `storytime-phase12c-portfolio-demo-narrative-public-presentation-kit.tar.gz`
- Phase: Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — the third subphase of Phase 12 — Portfolio / SE Demo Packaging. **LOCKED / ACCEPTED / CANONICAL — it is the last locked phase.** Phase 12C completed the Phase Closure Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini returned **SAFE TO LOCK** with no critical findings, no non-blocking findings, and no required edits; the user then locked Phase 12C. This lock is recorded into the manifest by the Phase 12D round as part of its state synchronization — the same after-the-fact lock-recording pattern used for earlier subphases. The Phase 12C implementation-candidate manifest entry below is preserved as written and is superseded for status purposes by this lock entry.
- sha256: `4c98a25d6bb0ae751b4ba33851bc60e7d7805d4fd31ebcfc45c2d30a659301da` (the locked Phase 12C lineage; it is the source/base artifact for Phase 12D).
- Scope: documentation-first portfolio packaging — four public-presentation `docs/` documents (`portfolio-demo-narrative.md`, `demo-talk-track.md`, `interview-story-bank.md`, `public-repository-readiness.md`), a light README reviewer-pointer refinement, the authorized advance of the state-discipline guard, and the synchronized State Preservation Bundle. No `pyproject.toml`, `uv.lock`, or `src/` change; no dependency change; no product behaviour change.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — CLOSED**; Phase 12A locked; Phase 12B locked; **Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — STARTED** and not closed. Phase 12D is the current implementation candidate (recorded in the Phase 12D entry above); Phase 12E is optional/future/not started. Phase 13 — Operator GUI / Decoupled Frontend Vision — roadmap-preserved only, not started.

# Artifact Manifest Entry — Phase 12C Portfolio Demo Narrative / Public Presentation Kit — 2026-05-26

*Supersession note (added by Phase 12D): this is a historical point-in-time entry from the Phase 12C implementation round. Phase 12C is now LOCKED and is the last locked phase; Phase 12D is the current implementation candidate (pending review, not locked). See the Phase 12D and Phase 12C (LOCKED) entries at the top of this file for current state.*

- Artifact: `storytime-phase12c-portfolio-demo-narrative-public-presentation-kit.tar.gz`
- Phase: Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — the third subphase of Phase 12 — Portfolio / SE Demo Packaging. **Implementation candidate; pending review; not locked.** Per the Phase Closure Protocol, Phase 12C is implementation output until GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval complete. It does not lock Phase 12C, does not close Phase 12, and does not start Phase 12D.
- Source / base artifact: `storytime-phase12b3-residual-state-wording-cleanup.tar.gz` (SHA-256 `ce0fb2d1bea4eaa636be7796613f9a9aa56cba4b8bf34c0ae5440c3509de4a45`, the locked Phase 12B sequence lineage — Phase 12B with the accepted Phase 12B.1 / 12B.2 / 12B.3 cleanup sub-rounds folded in; SHA-256 verified on extraction).
- sha256: reported on delivery.
- Scope: documentation-first portfolio packaging. Converts the project's existing technical evidence into polished, reusable public-presentation assets. Adds four `docs/` documents — `portfolio-demo-narrative.md` (a concise demo narrative covering the business problem, technical architecture, observability value, governance posture, what the operator sees, what the reviewer should notice, the SE / Dynatrace-style credibility mapping, and the intentional out-of-scope boundaries), `demo-talk-track.md` (a spoken walkthrough at 5-minute / 10-minute / 20-minute lengths, with interviewer Q&A pivots and a "what to say if the demo cannot be run live" fallback), `interview-story-bank.md` (reusable Solutions-Engineer / observability interview answer frames for the seven standard project-interview questions, with a cross-cutting honesty checklist), and `public-repository-readiness.md` (a public-viewing readiness checklist — public-safe README check, secrets/config check, demo-data check, screenshot-placeholder check, known-limitations check, and "do not publish until verified" hard gates) — lightly updates `README.md` to point reviewers to the new presentation documents, advances the state-discipline guard `tests/test_failure_mode_regression.py` (the narrow, explicitly authorized mechanical change), and synchronizes the State Preservation Bundle (`LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/canonical-state.md` (append-only Phase 12B lock entry + Phase 12C entry), `docs/phase-history.md` (append-only Phase 12B.2 / 12B.3 / Phase 12B lock entries + Phase 12C round), this `docs/artifact-manifest.md`, `docs/verification-log.md`, `docs/open-issues.md`, and `docs/roundtable-import-bridge.md`).
- Known constraints: documentation, public-presentation packaging, and state changes only. No `pyproject.toml`, `uv.lock`, or `src/` change (all byte-for-byte identical to the source artifact); no dependency change; no new product feature, UI, server, dashboard, browser mutation control, JavaScript, frontend directory, React/Vite/TypeScript file, external asset, CDN, generated audio, screenshot/image/PDF/PowerPoint/binary asset, demo video, or runtime/cache artifact; no database schema change; no change to pipeline / `storytime rerun` / Trust Envelope enforcement / API / CLI / telemetry behaviour; no ARCH-LOCKed contract change; no Phase 13 GUI implementation. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 12C current-state expectations — it now guards against a premature Phase 12C lock, a premature Phase 12 closure, and a premature Phase 12D-or-later start, and additionally requires the Phase 12B lock record; coverage is strengthened, not weakened. `docs/known-limitations.md` and `docs/architecture-baseline.md` are intentionally unchanged.
- Tests: 590 passed (588 from the Phase 12B baseline plus 2 net from the strengthened state-discipline guard); ruff clean; mypy clean (85 source files, strict); lint-imports 2/2 kept; `storytime doctor` healthy; legal-hallucination scanner 0 violations (run inside the pytest suite, covering the four new documents).
- Archive hygiene: no `.mypy_cache`, `.ruff_cache`, `.pytest_cache`, `.import_linter_cache`, `.venv`, `runs/`, `feed/`, `logs/`, `operator-report/`, `__pycache__`, `*.pyc`, generated DB, generated audio, `.wav`/`.mp3`, screenshots/images, PDF/PowerPoint, `node_modules`, nested `*.tar.gz`, or large binary artifacts in the output archive. Built from a clean extraction with only the Phase 12C documentation, README, state, and authorized test edits applied.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A locked; **Phase 12B — Portfolio Evidence Pack / Reviewer Assets — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — STARTED** and not closed; Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — implementation candidate, pending review, not locked. Phase 12D and later subphases have not started. Phase 13 — Operator GUI / Decoupled Frontend Vision — roadmap-preserved only, not started.

# Artifact Manifest Entry — Phase 12B Portfolio Evidence Pack / Reviewer Assets (LOCKED) — 2026-05-26

- Artifact: `storytime-phase12b-portfolio-evidence-pack-reviewer-assets.tar.gz` (Phase 12B lineage; the accepted Phase 12B.1 state-hygiene cleanup, Phase 12B.2 Phase 13 GUI roadmap-preservation cleanup, and Phase 12B.3 residual living-doc state-wording cleanup are folded into this lock — the folded lineage artifact is `storytime-phase12b3-residual-state-wording-cleanup.tar.gz`).
- Phase: Phase 12B — Portfolio Evidence Pack / Reviewer Assets — the second subphase of Phase 12 — Portfolio / SE Demo Packaging. **LOCKED / ACCEPTED / CANONICAL — it is the last locked phase.** Phase 12B completed the Phase Closure Protocol: implementation, GPT-5.5 review, the accepted Phase 12B.1 / 12B.2 / 12B.3 cleanup sub-rounds, Gemini critique of the combined Phase 12B sequence (SAFE TO LOCK, no required edits), and an explicit user lock decision. This lock is recorded into the manifest by the Phase 12C round as part of its state synchronization — the same after-the-fact lock-recording pattern used for earlier subphases. The Phase 12B.1 and Phase 12B implementation-candidate manifest entries below are preserved as written and are superseded for status purposes by this lock entry.
- sha256: `ce0fb2d1bea4eaa636be7796613f9a9aa56cba4b8bf34c0ae5440c3509de4a45` (the `storytime-phase12b3-residual-state-wording-cleanup.tar.gz` cleanup-lineage artifact folded into the locked Phase 12B lineage; it is the source/base artifact for Phase 12C).
- Scope: reviewer / evidence packaging — four reviewer/evidence `docs/` documents (`portfolio-evidence-index.md`, `se-interview-evidence-matrix.md`, `demo-reviewer-checklist.md`, `portfolio-public-copy.md`), a light README reviewer-pointer refinement, the authorized advance of the state-discipline guard, the synchronized State Preservation Bundle, and the accepted Phase 12B.1 / 12B.2 / 12B.3 documentation-only cleanup sub-rounds. Phase 12B.2 added `docs/GUI_vision.md` and a Phase 13 — Operator GUI / Decoupled Frontend Vision — roadmap note (future work, not started). No `pyproject.toml`, `uv.lock`, or `src/` change; no dependency change; no product behaviour change.
- Phase 12B.1 / 12B.2 / 12B.3 note: each is an accepted documentation-only cleanup sub-round folded into the Phase 12B lock lineage — none is an independently locked phase.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — CLOSED**; Phase 12A locked; **Phase 12B — Portfolio Evidence Pack / Reviewer Assets — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — STARTED** and not closed. Phase 12C is the current implementation candidate (recorded in the Phase 12C entry above); Phase 12D and later subphases have not started. Phase 13 — Operator GUI / Decoupled Frontend Vision — roadmap-preserved only, not started.

# Artifact Manifest Entry — Phase 12B.1 State-Hygiene Cleanup — 2026-05-26

*Supersession note (added by Phase 12C): this is a historical point-in-time entry. Phase 12B — with the accepted Phase 12B.1 / 12B.2 / 12B.3 cleanup sub-rounds folded into its lock lineage — is now LOCKED and is the last locked phase; Phase 12C is the current implementation candidate (pending review, not locked). See the Phase 12C and Phase 12B (LOCKED) entries at the top of this file for current state.*

- Artifact: `storytime-phase12b1-state-hygiene-cleanup.tar.gz`
- Phase: Phase 12B.1 — State-Hygiene Cleanup — a bounded, documentation-only cleanup of the Phase 12B — Portfolio Evidence Pack / Reviewer Assets round. **Not a new phase and not a lock.** Phase 12B remains the current implementation candidate, pending review, not locked; per the Phase Closure Protocol it still awaits Gemini critique and explicit user approval.
- Source / base artifact: `storytime-phase12b-portfolio-evidence-pack-reviewer-assets.tar.gz` (SHA-256 `dc7c0013a240e648f5a94f04871b86f45af3e152c923b949aad36beb7e6da8e5`, the Phase 12B implementation-candidate artifact; SHA-256 verified on extraction).
- sha256: reported on delivery.
- Scope: state-hygiene cleanup. A pre-Gemini-review check found stale Phase 12A.1-era present-tense phrasing inside historical notes in the living / current-state documents (Phase 12A described as "remains an implementation candidate", Phase 11D as "remains the last locked phase", parentheticals calling Phase 12A "the current implementation candidate"). Phase 12B.1 revised the historical-note wording in `LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, and `docs/roadmap.md` so those notes read as superseded point-in-time records, prepended a concise Phase 12B.1 cleanup note to each of those four files, added concise supersession notes to the affected historical entries in this `docs/artifact-manifest.md` and `docs/verification-log.md` (rather than rewriting those append-only-style entries), fixed one stale parenthetical in `docs/open-issues.md`, appended a round record to `docs/phase-history.md`, and prepended entries to `docs/verification-log.md` and this `docs/artifact-manifest.md`.
- Known constraints: documentation / state-hygiene wording only. No `src/`, `tests/`, `pyproject.toml`, or `uv.lock` change (all byte-for-byte identical to the Phase 12B source artifact); no dependency change; no new product feature, UI, server, dashboard, JavaScript, external assets, generated audio, screenshot/image/PDF/PowerPoint, or runtime/cache artifact; no database schema change; no change to pipeline / `storytime rerun` / Trust Envelope enforcement behaviour; no ARCH-LOCKed contract change. `docs/canonical-state.md` was intentionally not changed — Phase 12B.1 locks nothing. Historical chronology is preserved; the append-only round log was only appended to, never rewritten.
- Tests: 588 passed (unchanged from the Phase 12B baseline — Phase 12B.1 adds and modifies no test); ruff clean; mypy clean (85 source files, strict); lint-imports 2/2 kept; `storytime doctor` healthy; legal-hallucination scanner 0 violations. The state-discipline regression guard (39 tests) passes against the cleaned-up documents with no `tests/` change.
- Archive hygiene: no `.mypy_cache`, `.ruff_cache`, `.pytest_cache`, `.import_linter_cache`, `.venv`, `runs/`, `feed/`, `logs/`, `operator-report/`, `__pycache__`, `*.pyc`, generated DB, generated audio, `.wav`/`.mp3`, screenshots/images, PDF/PowerPoint, `node_modules`, nested `*.tar.gz`, or large binary artifacts in the output archive. Built from a clean extraction with only the Phase 12B.1 documentation edits applied.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; **Phase 12A — Portfolio / SE Demo Packaging Baseline — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — STARTED** and not closed; Phase 12B — Portfolio Evidence Pack / Reviewer Assets — implementation candidate, pending review, not locked, with the Phase 12B.1 state-hygiene cleanup applied. Phase 12C and later subphases have not started.

# Artifact Manifest Entry — Phase 12B Portfolio Evidence Pack / Reviewer Assets — 2026-05-26

- Artifact: `storytime-phase12b-portfolio-evidence-pack-reviewer-assets.tar.gz`
- Phase: Phase 12B — Portfolio Evidence Pack / Reviewer Assets — the second subphase of Phase 12 — Portfolio / SE Demo Packaging. **Implementation candidate; pending review; not locked.** Per the Phase Closure Protocol, Phase 12B is implementation output until GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval complete. It does not lock Phase 12B, does not close Phase 12, and does not start Phase 12C.
- Source / base artifact: `storytime-phase12a1-state-hygiene-cleanup.tar.gz` (SHA-256 `5f9eca1cc8c2efb55d57f87becdc53cd0d8e514221947e445965232f608b621a`, the accepted Phase 12A.1 state-hygiene cleanup folded into the locked Phase 12A — Portfolio / SE Demo Packaging Baseline lineage; SHA-256 verified on extraction).
- sha256: reported on delivery.
- Scope: reviewer / evidence packaging. Makes StoryTime's portfolio claims independently verifiable. Adds four `docs/` documents — `portfolio-evidence-index.md` (a claim-to-evidence index mapping each portfolio claim to a test, config file, source module, or document), `se-interview-evidence-matrix.md` (a Solutions-Engineer competency-to-evidence matrix with an honesty checklist), `demo-reviewer-checklist.md` (a reviewer wrapper over `docs/demo.md` — a pre-flight and what-to-look-for index, explicitly not a duplicate command script), and `portfolio-public-copy.md` (disciplined, non-hype public-facing copy with an honest "what it is not" scope statement) — lightly updates `README.md` to point reviewers to the new evidence documents, advances the state-discipline guard `tests/test_failure_mode_regression.py` (the narrow, explicitly authorized §5 mechanical change), and synchronizes the State Preservation Bundle (`LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/canonical-state.md` (append-only Phase 12A lock entry + Phase 12B entry), `docs/phase-history.md` (append-only Phase 12A lock entry + Phase 12B round), this `docs/artifact-manifest.md`, `docs/verification-log.md`, `docs/open-issues.md`, and `docs/roundtable-import-bridge.md`).
- Known constraints: documentation, reviewer-asset packaging, and state changes only. No `pyproject.toml`, `uv.lock`, or `src/` change (all byte-for-byte identical to the source artifact); no dependency change; no new product feature, UI, server, dashboard, browser mutation control, JavaScript, external assets, generated audio, screenshot/image/PDF/PowerPoint, or runtime/cache artifact; no database schema change; no change to pipeline / `storytime rerun` / Trust Envelope enforcement behaviour; no ARCH-LOCKed contract change. The only `tests/` change is the narrow, explicitly authorized §5 mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 12B current-state expectations — it now guards against a premature Phase 12B lock, a premature Phase 12 closure, and a premature Phase 12C-or-later start, and additionally requires the Phase 12A lock record; coverage is strengthened, not weakened. `docs/known-limitations.md` and `docs/architecture-baseline.md` are intentionally unchanged.
- Tests: 588 passed (585 from the Phase 12A baseline plus 3 net from the strengthened state-discipline guard); ruff clean; mypy clean (85 source files, strict); lint-imports 2/2 kept; `storytime doctor` healthy; legal-hallucination scanner 0 violations (run inside the pytest suite, covering the four new documents).
- Archive hygiene: no `.mypy_cache`, `.ruff_cache`, `.pytest_cache`, `.import_linter_cache`, `.venv`, `runs/`, `feed/`, `logs/`, `operator-report/`, `__pycache__`, `*.pyc`, generated DB, generated audio, `.wav`/`.mp3`, screenshots/images, PDF/PowerPoint, `node_modules`, nested `*.tar.gz`, or large binary artifacts in the output archive. Built from a clean extraction with only the Phase 12B documentation, README, state, and authorized test edits applied.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; **Phase 12A — Portfolio / SE Demo Packaging Baseline — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — STARTED**; Phase 12B — Portfolio Evidence Pack / Reviewer Assets — implementation candidate, pending review, not locked. Phase 12C and later subphases have not started.

# Artifact Manifest Entry — Phase 12A Portfolio / SE Demo Packaging Baseline (LOCKED) — 2026-05-26

- Artifact: `storytime-phase12a-portfolio-se-demo-packaging-baseline.tar.gz` (Phase 12A lineage; the accepted Phase 12A.1 state-hygiene cleanup `storytime-phase12a1-state-hygiene-cleanup.tar.gz` is folded into this lock).
- Phase: Phase 12A — Portfolio / SE Demo Packaging Baseline — the first subphase of Phase 12 — Portfolio / SE Demo Packaging. **LOCKED / ACCEPTED / CANONICAL — it is the last locked phase.** Phase 12A completed the Phase Closure Protocol: implementation, GPT-5.5 review, Gemini critique, the accepted Phase 12A.1 state-hygiene cleanup sub-round, and an explicit user lock decision. This lock is recorded into the manifest by the Phase 12B round as part of its state synchronization (the same after-the-fact lock-recording pattern used for earlier subphases). The Phase 12A.1 and Phase 12A implementation-candidate manifest entries below are preserved as written and are superseded for status purposes by this lock entry.
- sha256: `5f9eca1cc8c2efb55d57f87becdc53cd0d8e514221947e445965232f608b621a` (the Phase 12A.1 state-hygiene cleanup artifact folded into the locked Phase 12A lineage; it is the source/base artifact for Phase 12B).
- Scope: Portfolio / SE demo packaging — four portfolio `docs/` documents (`portfolio-overview.md`, `solutions-engineer-narrative.md`, `portfolio-demo-script.md`, `interview-talking-points.md`), a portfolio-facing `README.md` refinement, the authorized advance of the state-discipline guard, and the synchronized State Preservation Bundle, plus the accepted Phase 12A.1 documentation-only state-hygiene cleanup sub-round. No `pyproject.toml`, `uv.lock`, or `src/` change; no dependency change; no product behaviour change.
- Phase 12A.1 note: Phase 12A.1 is an accepted documentation-only cleanup sub-round folded into the Phase 12A lock lineage — it is not an independently locked phase.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — CLOSED**; **Phase 12A — Portfolio / SE Demo Packaging Baseline — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — STARTED** and not closed. Phase 12B is the current implementation candidate (recorded in the Phase 12B entry above); Phase 12C and later subphases have not started.

# Artifact Manifest Entry — Phase 12A.1 State-Hygiene Cleanup — 2026-05-26

*Supersession note (added by Phase 12B.1): this is a historical point-in-time entry. Phase 12A — with the accepted Phase 12A.1 cleanup sub-round folded into its lock lineage — is now LOCKED and is the last locked phase; Phase 12B is the current implementation candidate (pending review, not locked). Present-tense wording below describes the Phase 12A.1 round at the time it ran. See the Phase 12B and Phase 12A (LOCKED) entries at the top of this file for current state.*

- Artifact: `storytime-phase12a1-state-hygiene-cleanup.tar.gz`
- Phase: Phase 12A.1 — State-Hygiene Cleanup — a bounded, documentation-only cleanup of the Phase 12A — Portfolio / SE Demo Packaging Baseline round. **Not a new phase and not a lock.** Phase 12A remains the current implementation candidate, pending review, not locked; per the Phase Closure Protocol it still awaits GPT-5.5 review, Gemini critique, and explicit user approval.
- Source / base artifact: `storytime-phase12a-portfolio-se-demo-packaging-baseline.tar.gz` (SHA-256 `54909ee9da9ea20c0a416de733e2a7d1e1b4722ef3799e21c374698be778ffaa`, the Phase 12A implementation-candidate artifact; SHA-256 verified).
- sha256: reported on delivery.
- Scope: state-hygiene cleanup. A pre-lock review found stale present-tense phrasing inside historical notes in the living / current-state documents (Phase 11A / 11B / 11C described as "the last locked phase"; stale "Phase 11x note above" pointers). Phase 12A.1 revised the historical-note wording in `LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, and `docs/roadmap.md` so those notes read as superseded point-in-time records ("was the last locked phase at that point in the project history"; pointers redirected to the Phase 12A current-state note), prepended a concise Phase 12A.1 cleanup note to each of those four files, appended a round record to `docs/phase-history.md`, prepended entries to `docs/verification-log.md` and this `docs/artifact-manifest.md`, and updated `docs/handoff-state.md` artifact lineage.
- Known constraints: documentation / state-hygiene wording only. No `src/`, `tests/`, `pyproject.toml`, or `uv.lock` change (all byte-for-byte identical to the Phase 12A source artifact); no dependency change; no new product feature, UI, server, dashboard, JavaScript, external assets, generated audio, screenshot/image/PDF/PowerPoint, or runtime/cache artifact; no database schema change; no change to pipeline / `storytime rerun` / Trust Envelope enforcement behaviour; no ARCH-LOCKed contract change. `docs/canonical-state.md` was intentionally not changed — Phase 12A.1 locks nothing. Historical chronology is preserved; the append-only round log was only appended to, never rewritten.
- Tests: 585 passed (unchanged from the Phase 12A baseline — Phase 12A.1 adds and modifies no test); ruff clean; mypy clean (85 source files, strict); lint-imports 2/2 kept; `storytime doctor` healthy; legal-hallucination scanner 0 violations. The state-discipline regression test (36 tests) and the legal-hallucination gate (11 tests) were also confirmed in isolation.
- Archive hygiene: no `.mypy_cache`, `.ruff_cache`, `.pytest_cache`, `.import_linter_cache`, `.venv`, `runs/`, `feed/`, `logs/`, `operator-report/`, `__pycache__`, `*.pyc`, generated DB, generated audio, `.wav`/`.mp3`, screenshots/images, PDF/PowerPoint, `node_modules`, nested `*.tar.gz`, or large binary artifacts in the output archive. Built from a clean extraction with only the Phase 12A.1 documentation edits applied.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 11D is the last locked phase; **Phase 12 — Portfolio / SE Demo Packaging — STARTED**; Phase 12A — Portfolio / SE Demo Packaging Baseline — implementation candidate, pending review, not locked, with the Phase 12A.1 state-hygiene cleanup applied. Phase 12B and later subphases have not started.

# Artifact Manifest Entry — Phase 12A Portfolio / SE Demo Packaging Baseline — 2026-05-26

*Supersession note (added by Phase 12B.1): this is a historical point-in-time entry recording the Phase 12A implementation-candidate artifact. Phase 12A has since been LOCKED (see the Phase 12A (LOCKED) entry at the top of this file), and Phase 12B is the current implementation candidate. Present-tense "implementation candidate / not locked" wording below describes Phase 12A at the time this entry was written.*

- Artifact: `storytime-phase12a-portfolio-se-demo-packaging-baseline.tar.gz`
- Phase: Phase 12A — Portfolio / SE Demo Packaging Baseline — the first subphase of Phase 12 — Portfolio / SE Demo Packaging. **Implementation candidate; pending review; not locked.** Per the Phase Closure Protocol, Phase 12A is implementation output until GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval complete. It does not lock Phase 12A, does not close Phase 12, and does not start Phase 12B.
- Source / base artifact: `storytime-phase11d-release-candidate-evidence-pack.tar.gz` (SHA-256 `07a3973e3dbb69d760ff2c330418f85101c2afa1464fc0eed752fc7053894d94`, the locked Phase 11D — Release Candidate Evidence Pack artifact and the last locked phase; SHA-256 verified on extraction).
- sha256: reported on delivery.
- Scope: Portfolio / SE demo packaging. Makes StoryTime explainable as a Solutions Engineer / observability / OpenTelemetry portfolio project. Adds four `docs/` documents — `portfolio-overview.md` (the plain-English portfolio overview and reviewer entry point), `solutions-engineer-narrative.md` (30-second / 2-minute / deep pitches plus business, observability, OpenTelemetry, governance, and failure-mode framings), `portfolio-demo-script.md` (a narrated, reviewer-facing demo walkthrough that defers to `docs/demo.md` for authoritative commands), and `interview-talking-points.md` (concise study points) — refines `README.md` with a portfolio-facing "For reviewers" section and an updated phase table, advances the state-discipline guard `tests/test_failure_mode_regression.py` (a narrow, explicitly authorized change), and synchronizes the State Preservation Bundle (`LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/canonical-state.md` (append-only Phase 11D lock-closure entry + Phase 12 start / Phase 12A entry), `docs/phase-history.md` (append-only Phase 11D lock-closure entry + Phase 12A round), this `docs/artifact-manifest.md`, `docs/verification-log.md`, `docs/open-issues.md`, and `docs/roundtable-import-bridge.md`).
- Known constraints: documentation, portfolio-packaging, and state changes only. No `pyproject.toml`, `uv.lock`, or `src/` change (all byte-for-byte identical to the source artifact); no dependency change; no new product feature, UI, server, dashboard, browser mutation control, JavaScript, external assets, generated audio, screenshot/image/PDF/PowerPoint, or runtime/cache artifact; no database schema change; no change to pipeline / `storytime rerun` / Trust Envelope enforcement behaviour; no ARCH-LOCKed contract change. The only `tests/` change is a narrow, explicitly authorized advance of the state-discipline guard `tests/test_failure_mode_regression.py` (the Phase 11C state-documentation discipline module) so it tracks the Phase 12A current-state expectations — it now guards against a premature Phase 12A lock, a premature Phase 12 closure, and a premature Phase 12B-or-later start; coverage is strengthened, not weakened. `docs/known-limitations.md` is intentionally unchanged (locked Phase 10G deliverable; self-scoped status section deferring to `docs/handoff-state.md`).
- Tests: 585 passed (580 from the closed Phase 11 baseline plus 5 net from the authorized advance of the state-discipline guard); ruff clean; mypy clean (85 source files, strict); lint-imports 2/2 kept; `storytime doctor` healthy; legal-hallucination scanner 0 violations (run inside the pytest suite, covering the four new documents).
- Archive hygiene: no `.mypy_cache`, `.ruff_cache`, `.pytest_cache`, `.import_linter_cache`, `.venv`, `runs/`, `feed/`, `logs/`, `operator-report/`, `__pycache__`, `*.pyc`, generated DB, generated audio, `.wav`/`.mp3`, screenshots/images, PDF/PowerPoint, `node_modules`, nested `*.tar.gz`, or large binary artifacts in the output archive. Built from a clean extraction with only the Phase 12A documentation, README, state, and authorized test edits applied.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 11D — Release Candidate Evidence Pack — is the last locked phase; **Phase 12 — Portfolio / SE Demo Packaging — STARTED**; Phase 12A — Portfolio / SE Demo Packaging Baseline — implementation candidate, pending review, not locked. Phase 12B and later subphases have not started. This entry records the Phase 12A candidate artifact without marking Phase 12A locked.

# Artifact Manifest Entry — Phase 11D Release Candidate Evidence Pack (LOCKED — Phase 11 CLOSED) — 2026-05-26

*Supersession note (added by Phase 12B.1): this entry's lock record for Phase 11D remains accurate. Its closing line describing Phase 12A as "the current implementation candidate" is a historical point-in-time statement — Phase 12A is now LOCKED and Phase 12B is the current implementation candidate. See the entries at the top of this file for current state.*

- Artifact: `storytime-phase11d-release-candidate-evidence-pack.tar.gz`
- Phase: Phase 11D — Release Candidate Evidence Pack — the fourth and final subphase of Phase 11 — Release Candidate Hardening. **LOCKED / ACCEPTED / CANONICAL — it is the last locked phase.** With Phase 11D locked, **Phase 11 — Release Candidate Hardening — is formally CLOSED.** Phase 11D completed the Phase Closure Protocol out-of-band in the GPT/Gemini review workflow (GPT-5.5 review PASS; Gemini review SAFE TO LOCK; no required edits); the user, as final decision-maker, then locked Phase 11D and made the explicit Phase 11 closure decision, and authorized Phase 12. This out-of-band lock and closure are recorded into the manifest by the Phase 12A round as part of its state synchronization (the same after-the-fact lock-recording pattern used for Phase 11A, Phase 11B, Phase 11C, and the Post-Phase-10 Closure State Synchronization). The Phase 11D implementation-candidate manifest entry further below is preserved as written and is superseded for status purposes by this lock entry.
- sha256: `07a3973e3dbb69d760ff2c330418f85101c2afa1464fc0eed752fc7053894d94` (the locked Phase 11D artifact; it is the source/base artifact for Phase 12A).
- Scope: release-candidate evidence packaging — four `docs/` documents added (`release-candidate-evidence-pack.md`, `final-validation-summary.md`, `phase11-closure-checklist.md`, `phase12-readiness-handoff.md`) and the synchronized State Preservation Bundle. No `pyproject.toml`, `uv.lock`, `src/`, or `tests/` change; no dependency change; no product behaviour change.
- Validation basis at lock: 580 tests passing, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 contracts kept, `storytime doctor` healthy, legal-hallucination scanner zero violations.
- Current state after lock: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; **Phase 11D locked (the last locked phase)**; Phase 12 — Portfolio / SE Demo Packaging — STARTED; Phase 12A is the current implementation candidate (see the Phase 12A entry above).

# Artifact Manifest Entry — Phase 11D Release Candidate Evidence Pack — 2026-05-25

- Artifact: `storytime-phase11d-release-candidate-evidence-pack.tar.gz`
- Phase: Phase 11D — Release Candidate Evidence Pack — the fourth and final planned subphase of Phase 11 — Release Candidate Hardening. **Implementation candidate; pending review; not locked.** Per the Phase Closure Protocol, Phase 11D is implementation output until GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval complete. It does not mark Phase 11 complete and does not start Phase 12.
- Source / base artifact: `storytime-phase11c-failure-mode-regression-hardening.tar.gz` (SHA-256 `2dd31442e62c13241a64d10c2d117aefedc3b9c633ad5ea5d1fa94cfaad7d57b`, the locked Phase 11C — Failure-Mode / Regression Hardening artifact and the last locked phase; SHA-256 verified on extraction).
- sha256: reported on delivery.
- Scope: Release-candidate evidence packaging. Consolidates the release-candidate evidence produced by Phases 11A, 11B, and 11C into a reviewer-facing index. Adds four `docs/` documents — `release-candidate-evidence-pack.md` (the Phase 11D overview and the release-candidate evidence index), `final-validation-summary.md` (the canonical validation results), `phase11-closure-checklist.md` (what each Phase 11 subphase contributed and the conditions for an explicit Phase 11 closure decision), and `phase12-readiness-handoff.md` (what Phase 12 may safely do) — refreshes the status notes in `docs/phase11-plan.md`, `docs/release-candidate-hardening.md`, and `docs/rc-validation-checklist.md`, and synchronizes the State Preservation Bundle (`LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/canonical-state.md` (append-only Phase 11C lock-closure entry + Phase 11D entry), `docs/phase-history.md` (append-only Phase 11C lock-closure entry + Phase 11D round), this `docs/artifact-manifest.md`, and `docs/verification-log.md`).
- Known constraints: documentation/evidence and state changes only. No `pyproject.toml`, `uv.lock`, `src/`, or `tests/` change (all byte-for-byte identical to the source artifact); no dependency change; no new product feature, UI, server, dashboard, browser mutation control, JavaScript, external assets, generated audio, screenshot/image/PDF/PowerPoint, or runtime/cache artifact; no database schema change; no change to pipeline / `storytime rerun` / Trust Envelope enforcement behaviour; no ARCH-LOCKed contract change; no helper scripts added. `docs/known-limitations.md` is intentionally unchanged (locked Phase 10G deliverable; self-scoped status section deferring to `docs/handoff-state.md`).
- Tests: 580 passed (unchanged from the locked Phase 11C baseline; Phase 11D adds no test); ruff clean; mypy clean (85 source files, strict); lint-imports 2/2 kept; `storytime doctor` healthy; legal-hallucination scanner 0 violations (run inside the pytest suite, covering the four new documents). The six Docker-free gates were re-run from a clean extraction of the locked Phase 11C artifact with no source/dependency/test change applied.
- Archive hygiene: no `.mypy_cache`, `.ruff_cache`, `.pytest_cache`, `.import_linter_cache`, `.venv`, `runs/`, `feed/`, `logs/`, `operator-report/`, `__pycache__`, `*.pyc`, generated DB, generated audio, `.wav`/`.mp3`, screenshots/images, PDF/PowerPoint, `node_modules`, nested `*.tar.gz`, or large binary artifacts in the output archive. Built from a clean extraction with only the Phase 11D documentation and state edits applied.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; the Post-Phase-10 Historical State Reconciliation was the last locked work item before Phase 11; Phase 11A locked; Phase 11B locked; **Phase 11C — Failure-Mode / Regression Hardening — locked (the last locked phase)**; Phase 11 — Release Candidate Hardening — in progress; Phase 11D — Release Candidate Evidence Pack — implementation candidate, pending review, not locked. This entry records the Phase 11D candidate artifact without marking Phase 11D locked.

# Artifact Manifest Entry — Phase 11C Failure-Mode / Regression Hardening (LOCKED) — 2026-05-25

- Artifact: `storytime-phase11c-failure-mode-regression-hardening.tar.gz`
- Phase: Phase 11C — Failure-Mode / Regression Hardening — the third subphase of Phase 11 — Release Candidate Hardening. **LOCKED / ACCEPTED / CANONICAL — it is the last locked phase.** Phase 11C completed the Phase Closure Protocol and was locked with explicit user approval; this lock is recorded into the manifest by the Phase 11D round as part of its state synchronization (the same after-the-fact lock-recording pattern used for Phase 11A, Phase 11B, and the Post-Phase-10 Closure State Synchronization). The Phase 11C implementation-candidate manifest entry further below is preserved as written and is superseded for status purposes by this lock entry.
- sha256: `2dd31442e62c13241a64d10c2d117aefedc3b9c633ad5ea5d1fa94cfaad7d57b` (the locked Phase 11C artifact; it is the source/base artifact for Phase 11D).
- Scope: failure-mode / regression hardening — four `docs/` documents added, one regression test module added (`tests/test_failure_mode_regression.py`, the state-documentation discipline guard), and the synchronized State Preservation Bundle. No `pyproject.toml`, `uv.lock`, or `src/` change; no dependency change; no product behaviour change; the only `tests/` change was the new regression module.
- Current state after lock: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11 — Release Candidate Hardening — in progress; Phase 11A locked; Phase 11B locked; **Phase 11C locked (the last locked phase)**; Phase 11D is the current implementation candidate (see the Phase 11D entry above).

# Artifact Manifest Entry — Phase 11C Failure-Mode / Regression Hardening — 2026-05-25

- Artifact: `storytime-phase11c-failure-mode-regression-hardening.tar.gz`
- Phase: Phase 11C — Failure-Mode / Regression Hardening — the third subphase of Phase 11 — Release Candidate Hardening. **Implementation candidate; pending review; not locked.** Per the Phase Closure Protocol, Phase 11C is implementation output until GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval complete. It does not mark Phase 11 complete and does not start Phase 11D or Phase 12.
- Source / base artifact: `storytime-phase11b-fresh-clone-operator-reproducibility.tar.gz` (SHA-256 `08b72f2833da9adf3b8acc1f3170334eb7c5f998e19263838efbce2f571cc73f`, the locked Phase 11B — Fresh Clone / Operator Reproducibility artifact and the last locked phase; SHA-256 verified on extraction).
- sha256: reported on delivery.
- Scope: Failure-mode / regression hardening. Inventories the highest-risk failure and regression paths that already exist in StoryTime — the operator failure / review queue, retry / re-run behaviour, governance-blocked content, static HTML report safety, demo fixture invariants, the static legal-hallucination gate, operator-safe failure messages, state preservation around failed runs, and traceability of blocked / failed / retried stages — records for each one which tests and validation gates protect it, and documents operator failure-response. Adds four `docs/` documents — `failure-mode-regression-hardening.md` (the Phase 11C overview), `regression-risk-register.md` (the risk inventory R1–R9 with coverage status), `failure-mode-test-matrix.md` (the regression coverage map), and `operator-failure-response.md` (the operator failure-response playbook) — and one focused regression test module, `tests/test_failure_mode_regression.py` (31 tests; the state-documentation discipline guard). Synchronizes the State Preservation Bundle (`LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/open-issues.md`, `docs/canonical-state.md` (append-only Phase 11B lock-closure entry + Phase 11C entry), `docs/phase-history.md` (append-only Phase 11B lock-closure entry + Phase 11C round), this `docs/artifact-manifest.md`, `docs/verification-log.md`, and `docs/roundtable-import-bridge.md`).
- Known constraints: documentation and test additions only. No `pyproject.toml`, `uv.lock`, or `src/` change (all byte-for-byte identical to the source artifact); no dependency change; no new product feature, UI, server, dashboard, browser mutation control, JavaScript, external assets, generated audio, screenshot/image/PDF/PowerPoint, or runtime/cache artifact; no database schema change; no change to pipeline / `storytime rerun` / Trust Envelope enforcement behaviour; no ARCH-LOCKed contract change. The only `tests/` change is the added regression module `tests/test_failure_mode_regression.py`; no existing test was modified. `docs/known-limitations.md` is intentionally unchanged (locked Phase 10G deliverable; self-scoped status section deferring to `docs/handoff-state.md`).
- Tests: 580 passed (549 baseline + 31 new in `tests/test_failure_mode_regression.py`); ruff clean; mypy clean (85 source files, strict); lint-imports 2/2 kept; `storytime doctor` healthy; legal-hallucination scanner 0 violations (run inside the pytest suite, covering the four new documents and the new test module).
- Archive hygiene: no `.mypy_cache`, `.ruff_cache`, `.pytest_cache`, `.import_linter_cache`, `.venv`, `runs/`, `feed/`, `logs/`, `operator-report/`, `__pycache__`, `*.pyc`, generated DB, generated audio, `.wav`/`.mp3`, screenshots/images, PDF/PowerPoint, `node_modules`, nested `*.tar.gz`, or large binary artifacts in the output archive. Built from a clean extraction with only the Phase 11C documentation and test additions applied.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; the Post-Phase-10 Historical State Reconciliation was the last locked work item before Phase 11; Phase 11A locked; **Phase 11B — Fresh Clone / Operator Reproducibility — locked (the last locked phase)**; Phase 11 — Release Candidate Hardening — in progress; Phase 11C — Failure-Mode / Regression Hardening — implementation candidate, pending review, not locked. This entry records the Phase 11C candidate artifact without marking Phase 11C locked.

# Artifact Manifest Entry — Phase 11B Fresh Clone / Operator Reproducibility (LOCKED) — 2026-05-25

- Artifact: `storytime-phase11b-fresh-clone-operator-reproducibility.tar.gz`
- Phase: Phase 11B — Fresh Clone / Operator Reproducibility — the second subphase of Phase 11 — Release Candidate Hardening. **LOCKED / ACCEPTED / CANONICAL — it is the last locked phase.** Phase 11B completed the Phase Closure Protocol and was locked with explicit user approval; this lock is recorded into the manifest by the Phase 11C round as part of its state synchronization (the same after-the-fact lock-recording pattern used for Phase 11A and the Post-Phase-10 Closure State Synchronization). The Phase 11B implementation-candidate manifest entry further below is preserved as written and is superseded for status purposes by this lock entry.
- sha256: `08b72f2833da9adf3b8acc1f3170334eb7c5f998e19263838efbce2f571cc73f` (the locked Phase 11B artifact; it is the source/base artifact for Phase 11C).
- Scope: fresh-clone / operator reproducibility verification — two `docs/` reproducibility documents added, the Phase 11A reproducibility documents refined, the `README.md` Setup command aligned with the canonical `uv sync --frozen --extra dev` form, and the synchronized State Preservation Bundle. No `pyproject.toml`, `uv.lock`, `src/`, or `tests/` change; no dependency change; no product behaviour change.
- Current state after lock: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11 — Release Candidate Hardening — in progress; Phase 11A locked; **Phase 11B locked (the last locked phase)**; Phase 11C is the current implementation candidate (see the Phase 11C entry above).

# Artifact Manifest Entry — Phase 11B Fresh Clone / Operator Reproducibility — 2026-05-25

- Artifact: `storytime-phase11b-fresh-clone-operator-reproducibility.tar.gz`
- Phase: Phase 11B — Fresh Clone / Operator Reproducibility — the second subphase of Phase 11 — Release Candidate Hardening. **Implementation candidate; pending review; not locked.** Per the Phase Closure Protocol, Phase 11B is implementation output until GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval complete. It does not mark Phase 11 complete and does not start Phase 11C, 11D, or Phase 12.
- Source / base artifact: `storytime-phase11a-release-candidate-hardening-baseline.tar.gz` (SHA-256 `664f8ba4ae90cf6a98ccc7d20369e690eac74497ab78f2b7067f0aac2079a7aa`, the locked Phase 11A — Release Candidate Hardening Baseline artifact and the last locked phase; SHA-256 verified on extraction).
- sha256: reported on delivery.
- Scope: Fresh-clone / operator reproducibility verification. Takes the locked Phase 11A documentation as a specification and verifies it against reality: extracts the locked Phase 11A artifact into a clean tree, walks the documented setup, validation, and demo paths exactly as written, and confirms they reproduce the Phase 11A baseline. Adds two `docs/` reproducibility documents — `operator-reproducibility-checklist.md` (the step-by-step verification path, paired with the observed reference results) and `fresh-clone-troubleshooting.md` (common fresh-clone setup failures and their safe responses) — refines the Phase 11A reproducibility documents (`phase11-plan.md`, `fresh-clone-checklist.md`, `local-setup-runbook.md`, `rc-validation-checklist.md`, `demo-reproducibility-checklist.md`, `release-candidate-hardening.md`), aligns the `README.md` Setup command with the canonical `uv sync --frozen --extra dev` form used by every release-candidate validation document, adds a `README.md` index of the release-candidate hardening / reproducibility documents, and synchronizes the State Preservation Bundle (`LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/open-issues.md`, `docs/canonical-state.md` (append-only Phase 11A lock-closure entry + Phase 11B entry), `docs/phase-history.md` (append-only Phase 11A lock-closure entry + Phase 11B round), this `docs/artifact-manifest.md`, `docs/verification-log.md`, and `docs/roundtable-import-bridge.md`).
- Known constraints: documentation/state changes only. No `pyproject.toml`, `uv.lock`, `src/`, or `tests/` change (all byte-for-byte identical to the source artifact); no dependency change; no new product feature, UI, server, dashboard, browser mutation control, JavaScript, external assets, generated audio, screenshot/image/PDF/PowerPoint, or runtime/cache artifact; no database schema change; no change to pipeline / `storytime rerun` / Trust Envelope enforcement behaviour; no ARCH-LOCKed contract change; no helper scripts added (documentation-first removed the ambiguity — the existing `make` targets and explicit `uv run` gate commands already cover verification). The `README.md` Setup-command alignment is a documentation-consistency fix and introduces no behaviour change.
- Tests: 549 passed; ruff clean; mypy clean (85 source files, strict); lint-imports 2/2 kept; `storytime doctor` healthy; legal-hallucination scanner 0 violations (run inside the pytest suite, covering the two new documents). The six Docker-free gates were re-run from a clean extraction; the documented operator commands (`version`, `--help`, `validate-manifest`, the golden-path `run --auto-approve`, `status`, `report generate`, the demo-fixture integrity tests) ran as documented.
- Archive hygiene: no `.mypy_cache`, `.ruff_cache`, `.pytest_cache`, `.import_linter_cache`, `.venv`, `runs/`, `feed/`, `logs/`, `operator-report/`, `__pycache__`, `*.pyc`, generated DB, generated audio, `.wav`/`.mp3`, screenshots/images, PDF/PowerPoint, `node_modules`, nested `*.tar.gz`, or large binary artifacts in the output archive. Built from a clean extraction with only the Phase 11B documentation edits applied.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; the Post-Phase-10 Historical State Reconciliation was the last locked work item before Phase 11; **Phase 11A — Release Candidate Hardening Baseline — locked (the last locked phase)**; Phase 11 — Release Candidate Hardening — in progress; Phase 11B — Fresh Clone / Operator Reproducibility — implementation candidate, pending review, not locked. This entry records the Phase 11B candidate artifact without marking Phase 11B locked.

# Artifact Manifest Entry — Phase 11A Release Candidate Hardening Baseline (LOCKED) — 2026-05-25

- Artifact: `storytime-phase11a-release-candidate-hardening-baseline.tar.gz`
- Phase: Phase 11A — Release Candidate Hardening Baseline — the first subphase of Phase 11 — Release Candidate Hardening. **LOCKED / ACCEPTED / CANONICAL — it is the last locked phase.** Phase 11A completed the Phase Closure Protocol and was locked with explicit user approval; this lock is recorded into the manifest by the Phase 11B round as part of its state synchronization (the same after-the-fact lock-recording pattern used for the Post-Phase-10 Closure State Synchronization). The Phase 11A implementation-candidate manifest entry further below is preserved as written and is superseded for status purposes by this lock entry.
- sha256: `664f8ba4ae90cf6a98ccc7d20369e690eac74497ab78f2b7067f0aac2079a7aa` (the locked Phase 11A artifact; it is the source/base artifact for Phase 11B).
- Scope: documentation-first release-candidate hardening — seven `docs/` hardening documents and the synchronized State Preservation Bundle. No `pyproject.toml`, `uv.lock`, `src/`, or `tests/` change; no dependency change; no product behaviour change.
- Current state after lock: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11 — Release Candidate Hardening — in progress; **Phase 11A locked (the last locked phase)**; Phase 11B is the current implementation candidate (see the Phase 11B entry above).

# Artifact Manifest Entry — Phase 11A Release Candidate Hardening Baseline — 2026-05-25

- Artifact: `storytime-phase11a-release-candidate-hardening-baseline.tar.gz`
- Phase: Phase 11A — Release Candidate Hardening Baseline — the first subphase of Phase 11 — Release Candidate Hardening. **Implementation candidate; pending review; not locked.** Per the Phase Closure Protocol, Phase 11A is implementation output until GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval complete. It does not mark Phase 11 complete and does not start Phase 11B, 11C, 11D, or Phase 12.
- Source / base artifact: `storytime-post-phase10-roundtable-historical-backfill.tar.gz` (SHA-256 `367e647c46aa6e4fd039369da30859b11ca783249569df291343db133ef4cfdd`, the locked Post-Phase-10 Historical State Reconciliation artifact — the last locked work item before Phase 11).
- sha256: reported on delivery.
- Scope: Documentation-first release-candidate hardening. Audits and documents the repository's non-feature surfaces so the later Phase 11 subphases can proceed from a stable, understandable base. Adds seven `docs/` hardening documents — `release-candidate-hardening.md`, `phase11-plan.md`, `local-setup-runbook.md`, `fresh-clone-checklist.md`, `rc-validation-checklist.md`, `security-secrets-checklist.md`, and `demo-reproducibility-checklist.md` — and synchronizes the State Preservation Bundle (`LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/canonical-state.md` (append-only entry), `docs/phase-history.md` (append-only round), this `docs/artifact-manifest.md`, `docs/verification-log.md`, `docs/open-issues.md`, and `docs/roundtable-import-bridge.md`).
- Known constraints: documentation/state changes only. No `pyproject.toml`, `uv.lock`, `src/`, or `tests/` change (all byte-for-byte identical to the source artifact); no dependency change; no new product feature, UI, server, dashboard, browser mutation control, JavaScript, external assets, generated audio, screenshot/image/PDF/PowerPoint, or runtime/cache artifact; no database schema change; no change to pipeline / `storytime rerun` / Trust Envelope enforcement behaviour; no ARCH-LOCKed contract change; no helper scripts added. `docs/known-limitations.md` is intentionally unchanged (locked Phase 10G deliverable; self-scoped status section deferring to `docs/handoff-state.md`).
- Tests: 549 passed; ruff clean; mypy clean (85 source files, strict); lint-imports 2/2 kept; `storytime doctor` healthy; legal-hallucination scanner 0 violations (run inside the pytest suite, covering the seven new documents).
- Archive hygiene: no `.mypy_cache`, `.ruff_cache`, `.pytest_cache`, `.import_linter_cache`, `.venv`, `runs/`, `feed/`, `logs/`, `operator-report/`, `__pycache__`, `*.pyc`, generated DB, generated audio, `.wav`/`.mp3`, screenshots/images, PDF/PowerPoint, `node_modules`, nested `*.tar.gz`, or large binary artifacts in the output archive.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; the Post-Phase-10 Historical State Reconciliation is the last locked work item; Phase 11 — Release Candidate Hardening — in progress; Phase 11A — Release Candidate Hardening Baseline — implementation candidate, pending review, not locked. This entry records the Phase 11A candidate artifact without marking Phase 11A locked.

# Artifact Manifest Entry — Post-Phase-10 Historical State Reconciliation — 2026-05-25

- Artifact: `storytime-post-phase10-roundtable-historical-backfill.tar.gz`
- Job: Post-Phase-10 Historical State Reconciliation — a documentation/state-history reconciliation checkpoint between Phase 10 closure and Phase 11 start. **Not a new phase** (not Phase 10G.2, not Phase 11.0); it does not reopen Phase 10 or start Phase 11.
- Source / base artifact: `storytime-post-phase10-closure-state-sync.tar.gz` (SHA-256 `5b309bb171ceea9380367c346945d20c67b242f42547902d9619668a27a804c1`, the verified Post-Phase-10 Closure State Synchronization artifact).
- Historical input: `ROUNDTABLE_PROJECT_StoryTime__formerly_podcast_pipeline__2026-05-24.json` (SHA-256 `8b6a089f5e5a4bc58b2387b0fc3f8b90e548a9d9237423ba88d0dd64dcddfdb4`; RoundTable full-project export, schema 0.11.0, exported 2026-05-24) — historical recovery input only, not current-state authority.
- sha256: reported on delivery.
- Scope: enriches the historical living docs with early RoundTable lineage (Phases 0–7) without changing current state. `docs/phase-history.md` gains a quarantined "Appendix — Historical RoundTable Lineage, Phases 0–7" section; `docs/roundtable-import-bridge.md` gains a "Historical RoundTable export — 2026-05-24 (how to interpret it)" section; this `docs/artifact-manifest.md` records the reconciliation artifact; `docs/verification-log.md` records its verification. All RoundTable-export-derived material is explicitly labeled historical/superseded. The current state is unchanged and remains **Phase 10G locked, Phase 10 CLOSED, Phase 11 — Release Candidate Hardening — not started**.
- Known constraints: documentation/state-history changes only. `docs/canonical-state.md`, `docs/handoff-state.md`, and `docs/roadmap.md` were **not** modified (no historical narrative added to them). No `pyproject.toml`, `uv.lock`, `src/`, or `tests/` change; no dependency change; no new product feature, UI, JavaScript, server, generated audio, screenshot/image/PDF/PowerPoint, or runtime/cache artifact; no RoundTable demo-app project state imported; no Phase 11 work.
- Historical lineage note: the RoundTable export records two early Phase 7 implementation artifacts by name — `storytime-phase7a-bluegreen-option-a.tar.gz` (Phase 7A) and `storytime-phase7b-bluegreen-frontdoor-switching.tar.gz` (Phase 7B implementation output) — and a Round 20 desync/recovery checkpoint. These are historical references; the authoritative artifact lineage remains the entries in this file.
- Tests: 549 passed; ruff clean; mypy clean (85 source files, strict); lint-imports 2/2 kept; `storytime doctor` healthy.
- Current state after archive: Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11 — Release Candidate Hardening — not started. This entry records the reconciliation artifact without overriding the Phase 10G closure record.

# Artifact Manifest Entry — Post-Phase-10 Closure State Synchronization — 2026-05-25

- Artifact: `storytime-post-phase10-closure-state-sync.tar.gz`
- Job: Post-Phase-10 Closure State Synchronization — a governance/state-document synchronization checkpoint. **Not a new phase** (not Phase 10G.2, not Phase 11); it records an already-approved lock/closure decision into the State Preservation Bundle.
- Source / base artifact: `storytime-phase10g1-uvlock-reversion-cleanup.tar.gz` (SHA-256 `8a0cc9a5b6426a291bec3a793e41501c7d3492187dd48b4f7729ea95e501a0c1`, the locked Phase 10G artifact).
- sha256: reported on delivery.
- Scope: synchronizes the first-read current-state documents with the already-approved Phase 10G lock and Phase 10 closure. **Phase 10G — Portfolio Narrative / Phase 10 Closure is LOCKED / ACCEPTED / CANONICAL; Phase 10 — Product UI / Operator Experience — is formally CLOSED; the next phase is Phase 11 — Release Candidate Hardening, not started.** Updated docs: `LLM_DIRECTOR.md`, `README.md`, `docs/canonical-state.md` (append-only entry), `docs/handoff-state.md`, `docs/roadmap.md`, `docs/phase-history.md` (append-only entry), this `docs/artifact-manifest.md`, `docs/verification-log.md`, `docs/roundtable-import-bridge.md`, and `docs/open-issues.md`.
- Known constraints: documentation/state-wording changes only. No `pyproject.toml`, `uv.lock`, `src/`, or `tests/` change; no dependency change; no new product feature, UI, server, JavaScript, browser mutation control, generated audio, screenshot/image/PDF/PowerPoint, or runtime/cache artifact; no RoundTable JSON historical backfill (that is a separate task); no Phase 11 work. The Phase 10G content documents (`docs/portfolio-narrative.md`, `docs/demo-script.md`, `docs/operator-experience-walkthrough.md`, `docs/command-reference.md`, `docs/known-limitations.md`, `docs/observability-governance-talking-points.md`, `docs/phase10-acceptance-checklist.md`, `docs/screenshot-instructions.md`) are unchanged — their internal self-scoped "at the time this document was written" wording is preserved as locked Phase 10G deliverable content.
- Tests: 549 passed; ruff clean; mypy clean (85 source files, strict); lint-imports 2/2 kept; `storytime doctor` healthy.
- Current state after archive: Phase 10A, 10B, 10C, 10C.1, 10D, 10D.1, 10E (with the 10E.1 / 10E.2 cleanup sequence), 10F, and 10G are all locked; **Phase 10 is CLOSED**; Phase 11 — Release Candidate Hardening — not started.

# Artifact Manifest Entry — Phase 10G.1 uv.lock Reversion Cleanup — 2026-05-25

- Artifact: `storytime-phase10g1-uvlock-reversion-cleanup.tar.gz`
- Phase: Phase 10G.1 — uv.lock Reversion Cleanup (documentation-phase artifact hygiene). **This artifact is the locked Phase 10G artifact** — SHA-256 `8a0cc9a5b6426a291bec3a793e41501c7d3492187dd48b4f7729ea95e501a0c1`; Phase 10G was locked on this artifact and Phase 10 is closed. *(At the time of this entry's original writing, Phase 10G.1 was a cleanup pending final review; it has since been verified — GPT-5.5 PASS, Gemini SAFE TO LOCK — and locked as the Phase 10G artifact. See the Post-Phase-10 Closure State Synchronization entry above.)* This was a sub-cleanup of the Phase 10G candidate, not a new feature phase.
- Source / base artifacts: `storytime-phase10g-portfolio-narrative-phase10-closure.tar.gz` (SHA-256 `f3c21b9e21ee22e263d61ffad04642e9e9a604e1508aa1cbd54fc6781cb245fe`, the Phase 10G implementation candidate) and `storytime-phase10f-demo-seed-data-golden-path-fixtures.tar.gz` (SHA-256 `e060570a94fb19f790c539542b3ef7445111430bc308668675548f66fa48df55`, locked Phase 10F — the authoritative source for the correct `uv.lock`).
- sha256: reported on delivery.
- Scope: Gemini reviewed Phase 10G and returned **SAFE WITH EDITS**, with one required edit — revert `uv.lock` to its exact Phase 10F state. On comparison the Phase 10G candidate's `uv.lock` was already byte-for-byte identical to the Phase 10F `uv.lock` (both 172248 bytes, both SHA-256 `c06b1a4fc58843463eedda66a36aa394df6e7765986b5b69c1b7819fc2fa90a1`); the `--frozen` flag used in the Phase 10G round had left the lockfile unmodified. The Phase 10F `uv.lock` was nonetheless copied explicitly over the Phase 10G `uv.lock` so the reversion procedure is executed in full; the result is unchanged. All eight Phase 10G documentation deliverables are preserved.
- Known constraints: no application/source code change (the `src/` and `tests/` trees and `pyproject.toml` are byte-for-byte identical to Phase 10F and to the Phase 10G candidate); no dependency added or changed; no lockfile regeneration; no new product feature, UI, server, dashboard, browser mutation control, JavaScript, external asset, generated audio, screenshot/image/PDF/PowerPoint, or runtime/cache artifact. The only documentation content changed versus the Phase 10G candidate is this manifest entry and the corresponding `docs/verification-log.md` Phase 10G.1 entry — artifact name / SHA / lineage bookkeeping for the cleanup.
- Tests: 549 passed; ruff clean; mypy clean (85 source files, strict); lint-imports 2/2 kept; `storytime doctor` healthy.
- Current state after archive: Phase 10A, 10B, 10C, 10C.1, 10D, 10D.1, 10E (with the 10E.1 / 10E.2 cleanup sequence), and 10F are all locked; Phase 10G implementation candidate, Phase 10G.1 cleanup applied, pending final review, not locked; Phase 10 not yet marked closed; Phase 11 not started.

# Artifact Manifest Entry — Phase 10G Portfolio Narrative / Phase 10 Closure — 2026-05-25

- Artifact: `storytime-phase10g-portfolio-narrative-phase10-closure.tar.gz`
- Phase: Phase 10G — Portfolio Narrative / Phase 10 Closure — **implementation candidate; pending review; not locked**.
- Source / base artifact: `storytime-phase10f-demo-seed-data-golden-path-fixtures.tar.gz` (SHA-256 `e060570a94fb19f790c539542b3ef7445111430bc308668675548f66fa48df55`).
- sha256: reported on delivery.
- Scope: Documentation, portfolio-narrative, demo-explanation, and Phase 10 closure work. Adds eight Phase 10 portfolio/closure documents under `docs/` — `portfolio-narrative.md`, `demo-script.md`, `operator-experience-walkthrough.md`, `command-reference.md`, `known-limitations.md`, `observability-governance-talking-points.md`, `phase10-acceptance-checklist.md`, and `screenshot-instructions.md` — and synchronizes the State Preservation Bundle (`LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/canonical-state.md`, `docs/phase-history.md`, `docs/open-issues.md`, `docs/verification-log.md`, this `docs/artifact-manifest.md`, and `docs/roundtable-import-bridge.md`). Documentation-first: no application code changed.
- Known constraints: no new product feature, no UI, no server, no dashboard, no browser mutation control, no JavaScript, no external assets, no CDN, no generated audio, no screenshots/images/binary portfolio assets, no PowerPoint/PDF/slide deck, no large binary artifact, no runtime database or cache artifact packaged, no new dependency, no database schema change, and no change to pipeline / `storytime rerun` / Trust Envelope enforcement behaviour.
- Tests: 549 passed; ruff clean; mypy clean (85 source files, strict); lint-imports 2/2 kept; `storytime doctor` healthy; legal-hallucination scanner 0 violations (all repository `.md` files, including the eight new Phase 10G documents).
- Current state after archive: Phase 10A, 10B, 10C, 10C.1, 10D, 10D.1, 10E (with the 10E.1 / 10E.2 cleanup sequence), and 10F are all locked; Phase 10G implementation candidate, pending review, not locked; Phase 10 not yet marked closed; Phase 11 not started.

# Artifact Manifest Entry — Phase 10F Demo Seed Data / Golden Path Fixtures — 2026-05-25

- Artifact: `storytime-phase10f-demo-seed-data-golden-path-fixtures.tar.gz`
- Phase: Phase 10F — Demo Seed Data / Golden Path Fixtures — **LOCKED / ACCEPTED / CANONICAL** (locked 2026-05-25).
- Source / base artifact: `storytime-phase10e2-final-cleanup-v2-normalized.tar.gz` (SHA-256 `87fad92b2e0a919a81588f4c628ccfdf08860571fdc778c527d8fe93c30b7dec`).
- sha256: `e060570a94fb19f790c539542b3ef7445111430bc308668675548f66fa48df55`.
- Scope: Demo-readiness / fixture-design work. Adds the `demo/` directory (`demo/seed/` — four original CC0 seed texts plus schema-valid source manifests; `demo/governance/demo-blocked-sources.yaml` — a demo-only blocked-source deny-list; `demo/fixtures/` — an index plus six fixture definitions, scenarios STF-10F-01 .. STF-10F-06), the `docs/demo.md` operator demo runbook, `tests/test_demo_fixtures.py`, and a `demo/` entry in `.dockerignore`.
- Known constraints: no new product feature, no UI, no server, no dashboard, no browser mutation control, no JavaScript, no external assets, no CDN, no generated audio committed, no large binary artifact, no runtime database or cache artifact packaged, no message broker, no background worker, no new dependency, no database schema change, and no change to pipeline / `storytime rerun` / Trust Envelope enforcement behaviour.
- Tests: 549 passed (37 new in `tests/test_demo_fixtures.py`); ruff clean; mypy clean (85 source files, strict); lint-imports 2/2 kept; `storytime doctor` healthy; legal-hallucination scanner 0 violations.
- Current state after archive: Phase 10A, 10B, 10C, 10C.1, 10D, 10D.1, 10E (with the 10E.1 / 10E.2 cleanup sequence), and 10F are all locked; Phase 10G is the next phase. *(Status updated by the Phase 10G round: Phase 10F is now locked; the original Phase 10F entry recorded it as an implementation candidate pending review.)*

# Artifact Manifest Entry — Phase 10E.2 Final Cleanup v2 Normalized — 2026-05-25

- Artifact: `storytime-phase10e2-final-cleanup-v2-normalized.tar.gz`
- Phase: Phase 10E.2 — Final Cleanup v2 Normalized — *(historical — Phase 10E is now locked; this was the pre-lock cleanup candidate. Lock recorded under the Phase 10F entry above.)*
- Source / base artifact: `storytime-phase10e2-final-cleanup-v2.tar.gz`
- Scope: Docs/state wording normalization only after GPT review confirmed the code-level Phase 10E.2 fixes. Updated first-read notes to reference the Phase 10E.2 final-cleanup-v2 artifact rather than stale Phase 10E.1 review language. No application code changed, no tests changed, no JavaScript, no external assets, no mutation behavior changed, no database schema changed, no new dependencies.
- Current state after archive: *(historical — superseded by the Phase 10F entry above)* Phase 10A, 10B, 10C, 10C.1, 10D, 10D.1 locked; Phase 10E implementation candidate with Phase 10E.2 final-cleanup-v2 complete, pending Phase 10E lock review; Phase 10F not started.

# Artifact Manifest

### storytime-phase10e2-final-cleanup-v2.tar.gz

- Created: 2026-05-25
- Phase: Phase 10E.2 — Final Cleanup (render.py redaction fix + state-preservation sync) — **cleanup candidate; pending Phase 10E lock review**.
- Source / base artifact: `storytime-phase10e2-final-cleanup.tar.gz` (Phase 10E.2 v1)
- sha256: reported on delivery.
- Scope: Two surgical fixes — (1) render.py: "Governance detail" row value is now the exact full phrase "Decision detail: blocked by governance policy; inspect Trust Envelope locally if authorized." as one rendered string; (2) state-preservation docs fully synchronized (handoff-state.md, roundtable-import-bridge.md, and this manifest). No JavaScript, no external assets, no mutation behavior changed, no database schema changed, no new dependencies.
- Tests: 512 passed; ruff clean; raw blocked_reason confirmed absent; full phrase confirmed present in rendered HTML.
- Current state after archive: Phase 10A, 10B, 10C, 10C.1, 10D, 10D.1 locked; Phase 10E implementation candidate (Phase 10E.2 final cleanup produced), pending Phase 10E lock review; Phase 10F not started. *(Historical record — Phase 10E is now locked; current state is in the Phase 10F entry at the top of this file.)*

### storytime-phase10e1-cleanup.tar.gz

- Created: 2026-05-25
- Phase: Phase 10E.1 — Redaction, Artifact Hygiene, and State Preservation Cleanup — *(superseded by Phase 10E.2 final-cleanup-v2; see entry above)*.
- Source / base artifact: `storytime-phase10e-static-html-operator-report-refinement.tar.gz`
- Source SHA-256: `ceb3e9d08057a1c7ff2e83ea7ef0520ff80f9258bac84d33f7ec42fdf75e05b6`
- sha256: reported on delivery.
- Scope: Three cleanup items only — (1) raw blocked_reason replaced with safe wording in render.py; (2) .mypy_cache, .ruff_cache, runs/state.db excluded from archive; (3) state-preservation docs synchronized. No JavaScript, no external assets, no mutation behavior changed, no database schema changed, no new dependencies.
- Tests: 512 passed; ruff clean; mypy 85 source files (1 pre-existing stubs error, unchanged); archive pollution confirmed absent.
- Current state after archive: Phase 10A, 10B, 10C, 10C.1, 10D, 10D.1 locked; Phase 10E implementation candidate (Phase 10E.1 cleanup produced), pending Phase 10E lock review; Phase 10F not started. *(Historical record — Phase 10E is now locked; current state is in the Phase 10F entry at the top of this file.)*

### storytime-phase10e-static-html-operator-report-refinement.tar.gz

- Created: 2026-05-25
- Phase: Phase 10E — Static HTML Operator Report Refinement — **implementation candidate; reviewed SAFE WITH EDITS (Phase 10E.2 final-cleanup-v2 review pending); pending Phase 10E.2 final-cleanup-v2 review and lock**.
- Source / base artifact: `storytime-phase10d1-llm-director-hardened.tar.gz`
- sha256: reported on delivery (a file cannot contain its own hash).
- Scope: Operator report refinement only. Adds executive status summary, rerun eligibility / action guidance, failure summary, command reference section, semantic status badges, improved governance warning block, embedded CSS per page, improved responsive layout. No JavaScript, no external assets, no browser-side mutation controls, no backend behavior changed, no database schema changed, no new dependencies.
- Tests: 511 passed (18 new Phase 10E report-safety tests); ruff clean; mypy 85 source files (1 pre-existing stubs error, unchanged from baseline); lint-imports 2/2 kept; storytime doctor healthy.
- Current state after archive: Phase 10A, 10B, 10C, 10C.1, 10D, 10D.1 locked; Phase 10E implementation candidate, pending review; Phase 10F not started. *(Historical record — Phase 10E is now locked; current state is in the Phase 10F entry at the top of this file.)*

### storytime-phase10d1-state-preservation-cleanup.tar.gz

- Created: 2026-05-25
- Phase: Phase 10D.1 — State Preservation Cleanup + LLM Director Hardening — **locked / accepted / canonical**.
- Source / base artifact: `storytime-phase10d-pipeline-rerun-mutation-actions.tar.gz`
- Source SHA-256: `479ce122992efe05ed8494619a60f7464952f744e0b351164b54208042a21a16`
- sha256: reported on delivery (a file cannot contain its own hash).
- Scope: Docs/state-preservation cleanup only. Updates first-read and current-state documentation to reflect that Phase 10D reviews returned SAFE WITH EDITS (docs/state cleanup required before lock). No application code, tests, mutation semantics, audit behavior, Trust Envelope logic, or database schema changed. Phase 10D remains not locked; Phase 10E remains not started.
- Verification status: all six Docker-free quality gates pass — pytest 493 passed, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy, legal scanner 0 violations.
- Current state after archive: Phase 10A, 10B, 10C, 10C.1, 10D, 10D.1 locked; Phase 10E implementation candidate, pending review; Phase 10F not started. *(Historical — superseded by Phase 10E entry above.)*

### storytime-phase10d-pipeline-rerun-mutation-actions.tar.gz

- Created: 2026-05-25
- sha256: `479ce122992efe05ed8494619a60f7464952f744e0b351164b54208042a21a16`

- Created: 2026-05-25
- Phase: Phase 10D — Pipeline Re-Run / Mutation Actions — **implementation candidate, pending review, not locked**.
- Source / base artifact: `storytime-phase10c1-state-preservation-sync.tar.gz`
- Source SHA-256: `ac2f56ed6ba22f0f00aee8f0caaaac0154ac02eef16b20d08b9d4e2addb67c9a`
- sha256: reported on delivery (a file cannot contain its own hash).
- Scope: StoryTime's first operator *mutation* surface. Adds the new `storytime.operator_rerun` module, the governed `storytime rerun` CLI command, the `EventType.RUN_RERUN_REQUESTED` audit event type, `tests/test_operator_rerun.py` (27 tests), and `docs/operator-rerun.md`; updates `src/storytime/cli/app.py`, `src/storytime/events/model.py`, `pyproject.toml` (import-linter contracts), and the State Preservation Bundle.
- Mutation semantics: a re-run resets a failed run's `pipeline_run.status` from `failed` to the existing resumable `running` state — one bounded status update — so the existing `storytime run --resume` path re-executes it from the failed stage. The `rerun` command runs no pipeline work itself.
- Verification status: the six Docker-free quality gates pass — pytest 493 passed (27 new), ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy, legal scanner 0 violations.
- Known constraints: no database schema change, no new run lifecycle state, no new database column, no new dependency, no broker/worker/daemon/scheduler/server/dashboard/auth/cloud. The Phase 10C read-only queue is unaffected. Phase 10D is locked; Phase 10D.1 is locked. Phase 10E — Static HTML Operator Report Refinement — is the current implementation candidate. *(Historical candidate constraints note — superseded by Phase 10E implementation candidate entry above.)*
- Current state after archive: Phase 10A, 10B, 10C, 10C.1 locked; Phase 10D implementation candidate, pending review, not locked.


### storytime-phase10b-locked-state-bundle.tar.gz

- Created: 2026-05-24
- Phase: Phase 10B — Generated Local HTML Operator Report locked-state bundle.
- Source / base artifact: `storytime-phase10b-generated-local-operator-report.tar.gz`
- Source SHA-256: `128d9697185d0ea44431041f0db05d64fba3c763c561aae6d701a9ba8dddca89`
- Status: **Phase 10B locked / accepted / canonical.**
- Review basis: GPT-5.5 verified the Phase 10B implementation; Gemini 3.1 Pro returned **SAFE TO LOCK**; user approved the lock.
- Scope: Documentation-only lock closure. No application/report code, database schema, governance behavior, telemetry behavior, tests, dependencies, or config behavior changed in this lock pass.
- **Jinja2 correction:** The Gemini review text mistakenly mentioned Jinja2. The locked implementation has no Jinja2 and no dependency change; rendering is pure standard library with `html.escape`.
- Current state after archive: Phase 10B locked; Phase 10C locked (2026-05-25); Phase 10D — Pipeline Re-Run / Mutation Actions — not started.
- Notes: Confirms the static local report, no external assets/CDNs/fonts/scripts, deterministic timestamp support, no server/auth/cloud/framework, no mutation UI, no raw-content display, and no legal overclaiming.



### storytime-phase10a-locked-state-bundle.tar.gz

- Created: 2026-05-24
- Phase: Phase 10A — Operator Experience Baseline Amendment locked-state bundle.
- Source / base artifact: `storytime-phase10a-operator-experience-baseline-amendment.tar.gz`
- Source SHA-256: `ec0ff3393252392ae6bbf6ca61c90860c43d5debe95b9cc1e9f3c2d94e481ad5`
- Status: **Phase 10A locked / accepted / canonical.**
- Review basis: Gemini 3.1 Pro returned **SAFE TO LOCK (PENDING VERIFICATION)**; GPT-5.5 satisfied the pending verification by confirming docs-only scope, no implementation delta, and Phase 10B not started; user approved the lock.
- Scope: Documentation-only lock closure. No Phase 10B implementation. No code, schema, config-behavior, dependency, HTML, CSS, template, CLI, report-generator, or UI change intended.
- Current state after archive: Phase 10A locked; Phase 10B next and not started; Phase 10C/10D future and not started.
- Note: Gemini's local-web-server aside was not accepted as Phase 10B authorization. Locked Phase 10B target remains generated static local HTML with no server runtime.



Lineage of StoryTime repository archives. Each `.tar.gz` is a full repository
snapshot built on the previous archive — the lineage is cumulative, never
forked. sha256 values are of the `.tar.gz` files as delivered. Verification
evidence per archive is in `docs/verification-log.md`.

## Archives (newest first)

### storytime-phase10f-demo-seed-data-golden-path-fixtures.tar.gz

- Phase: Phase 10F — Demo Seed Data / Golden Path Fixtures — implementation candidate, pending review, not locked.
- sha256: reported on delivery.
- Source / base artifact: `storytime-phase10e2-final-cleanup-v2-normalized.tar.gz`
  (sha256 `87fad92b2e0a919a81588f4c628ccfdf08860571fdc778c527d8fe93c30b7dec`).
- Round type: implementation round. Adds curated demo seed data and golden-path fixtures, the operator demo runbook, and fixture shape / safety tests. Exercises the real existing system; no product feature, UI, server, generated audio, JavaScript, new dependency, or schema / mutation-behaviour change.
- Files added: `demo/README.md`, `demo/seed/*` (4 texts + 4 manifests), `demo/governance/demo-blocked-sources.yaml`, `demo/fixtures/index.yaml`, `demo/fixtures/01-..06-*.yaml`, `docs/demo.md`, `tests/test_demo_fixtures.py`.
- Files modified: `.dockerignore`, `LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/canonical-state.md`, `docs/phase-history.md`, `docs/verification-log.md`, `docs/artifact-manifest.md`, `docs/open-issues.md`, `docs/roundtable-import-bridge.md`, `docs/operator-rerun.md`, `docs/operator-report.md`, `docs/operator-queue.md`.

### storytime-phase10c1-state-preservation-sync.tar.gz

- Phase: Phase 10C.1 — State Preservation Synchronization Cleanup (docs-only; no application code changed).
- sha256: reported on delivery.
- Source / base artifact: `storytime-phase10c-operator-cli-helpers-failure-queue.tar.gz`
  (sha256 `e30aaa57f900756e62347ddaac2df658d96065c9e1061679adb31594c73e2543`).
- Round type: docs/state-preservation cleanup only. Updates first-read documents to reflect Phase 10C locked status and Phase 10D as next/not-started. No application code, tests, or dependency changes.
- Files modified: `LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/open-issues.md`, `docs/roundtable-import-bridge.md`, `docs/canonical-state.md`, `docs/phase-history.md`, `docs/verification-log.md`, `docs/artifact-manifest.md`.

### storytime-phase10c-operator-cli-helpers-failure-queue.tar.gz

- Phase: Phase 10C — Operator CLI Helpers / Failure Queue — **locked / accepted / canonical (2026-05-25)**.
- sha256: `e30aaa57f900756e62347ddaac2df658d96065c9e1061679adb31594c73e2543`.
- Source / base artifact: `storytime-phase10b-locked-state-bundle-corrected.tar.gz`
  (sha256 `00e6d543ce334fb8be83448f3397510761568af7d4318ab8df4b9bc6ca0e0c59`).
- Round type: implementation round — adds a new module, a CLI command, tests,
  and docs. No database schema migration, no ARCH-LOCKed contract change, no
  new dependency, no governance/telemetry/pipeline behaviour change.
- Files added:
  - **`src/storytime/operator_queue.py`** — the read-only failure / review
    queue: the `QueueItem` bounded projection dataclass, `collect_queue` (a
    deterministic semantic query over the existing SQLite run/stage/
    Trust-Envelope state), and `render_table` / `render_json` output.
  - **`tests/test_operator_queue.py`** — 29 Phase 10C tests.
  - **`docs/operator-queue.md`** — the operator-queue guide.
- Files modified:
  - **`src/storytime/cli/app.py`** — a new read-only `queue` command
    (`storytime queue` with `--status`, `--run-id`, `--limit`, `--json`);
    imports for the queue module.
  - **`pyproject.toml`** — `storytime.operator_queue` added to both
    import-linter contracts (the OpenTelemetry-confinement contract and the
    events-leaf contract). No dependency change.
  - **State Preservation Bundle docs** — `docs/canonical-state.md` and
    `docs/phase-history.md` (append-only — Phase 10C implementation-output
    entry); `docs/handoff-state.md`, `docs/roadmap.md`, `docs/open-issues.md`,
    `docs/verification-log.md`, this manifest, `docs/roundtable-import-bridge.md`,
    `LLM_DIRECTOR.md`, and `README.md` — all updated to record Phase 10C
    implemented as a candidate. *(These documents were later updated by the
    Phase 10C.1 cleanup to reflect the Phase 10C lock.)*
- Verification status: the six Docker-free quality gates pass — **pytest 466 passed** (29 new), ruff clean, mypy clean (84 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy, legal scanner 0 violations. Review: GPT-5.5 Thinking PASS; Gemini/Flash Light SAFE TO LOCK. **LOCKED.**
- Architecture: the queue is a read-only view over existing state: no message broker, background worker, new queue storage, new run state, or `pop`/`dequeue`/`claim`/`ack` behaviour. Phase 10D — Pipeline Re-Run / Mutation Actions — has not started.
- State Preservation Bundle inclusion: complete — all Bundle files present,
  including `LLM_DIRECTOR.md`.

### storytime-phase10b-generated-local-operator-report.tar.gz

- Phase: Phase 10B — Generated Local HTML Operator Report (implementation candidate; superseded by lock bundle above). The first implementation phase of Phase 10.
- sha256: reported on delivery (a file cannot contain its own hash).
- Source / base artifact: `storytime-phase10a-locked-state-bundle.tar.gz`
  (sha256 `d9e6ce79a8bc12b26b48bfc032355b17d1acf46cc610a407cf0f65be3babf8f9`).
- Round type: implementation round — adds a new package, a CLI command, tests,
  and docs. No database schema migration, no ARCH-LOCKed contract change, no
  new dependency, no governance/telemetry/pipeline behaviour change.
- Files added:
  - **`src/storytime/reporting/`** — new package: `model.py` (the deterministic
    §25.11 report data model), `collect.py` (builds the model from existing
    SQLite projections plus the durable Trust Envelope artifact), `render.py`
    (pure standard-library HTML rendering — no Jinja2, no template
    dependency), `generate.py` (collect → render → write static files),
    `__init__.py`.
  - **`tests/test_operator_report.py`** — 19 Phase 10B tests.
  - **`docs/operator-report.md`** — the operator-report guide.
- Files modified:
  - **`src/storytime/cli/app.py`** — a new `report` Typer sub-app with the
    `generate` command (`storytime report generate [--output …]`); imports for
    the report path.
  - **`pyproject.toml`** — `storytime.reporting` added to both import-linter
    contracts (the OpenTelemetry-confinement contract and the events-leaf
    contract). No dependency change.
  - **`.gitignore`, `.dockerignore`** — `operator-report/` excluded as
    generated runtime output.
  - **State Preservation Bundle docs** — `docs/canonical-state.md` and
    `docs/phase-history.md` (append-only — Phase 10B implementation-output
    entry); `docs/handoff-state.md`, `docs/roadmap.md`, `docs/open-issues.md`,
    `docs/verification-log.md`, this manifest, `docs/roundtable-import-bridge.md`,
    `LLM_DIRECTOR.md`, and `README.md` — all updated to record the Phase 10B implementation candidate; superseded by the Phase 10B lock bundle above.
- Verification status: the six Docker-free quality gates pass — `uv sync
  --frozen`, **pytest 437 passed** (19 new), ruff clean, mypy clean (83 source
  files, strict), import-linter 2/2 kept, `storytime doctor` healthy; the
  legal-hallucination scanner returns zero violations. The `storytime report
  generate` command was run end to end. Per the Phase Closure Protocol this was implementation output before lock; superseded by the Phase 10B lock bundle above.
- Known caveats: implementation candidate — Phase 10B awaits GPT-5.5 review,
  Gemini critique, any cleanup, and explicit user approval. One documented,
  non-blocking limitation: the projections record a per-episode audio path but
  not a per-run RSS feed path (the feed is the shared `feed/feed.xml`); the
  report surfaces the audio path and references the shared feed for a run that
  published. Phase 10C and Phase 10D have not started.
- State Preservation Bundle inclusion: complete — all Bundle files present,
  including `LLM_DIRECTOR.md`.

### storytime-phase10a-operator-experience-baseline-amendment.tar.gz

- Phase: Phase 10A — Operator Experience Baseline Amendment (candidate; pending
  review/lock). Architecture/documentation only.
- sha256: reported on delivery (a file cannot contain its own hash).
- Source / base artifact: `storytime-phase9b-locked-state-bundle.tar.gz`
  (sha256 `f7d205959986907a80b101602b6f4a58032a61e0b03ab23256d9b2dc45039a4f`).
- Round type: architecture/documentation amendment-authoring round. No
  application code, database schema, artifact envelope code, Trust Envelope
  semantics, governance gate behaviour, telemetry behaviour, configuration
  behaviour, test, or dependency changed — only Markdown living-doc files. The
  contents are byte-identical to the base archive except for the documents
  listed below.
- Files modified:
  - **`docs/architecture-baseline.md`** — added **Section 25**, "Operator
    Experience Baseline" — the Phase 10A Architecture Baseline amendment
    **candidate**. Defines the operator-experience goal, the read-only-first
    rule, the source-of-truth rule, the governance display rule (allowed vs
    forbidden vocabulary), the viewpoint-neutrality carryover, the Phase 10B
    target / hard floor / hard ceiling, the report data model and field
    allowlist/blacklist, the bounded `review_context_summary` rule, the
    observability-link rule, the static-only / no-server / no-auth / no-cloud /
    mutation-gate rules, the determinism / privacy / governance-copy-linting
    test requirements, the performance guardrail, the Phase 10B handoff
    section, the stop/revert criterion, and the Phase 10A / 10B / 10C / 10D
    split. Earlier sections (1–24) are unchanged.
  - **State Preservation Bundle docs** — `docs/canonical-state.md` and
    `docs/phase-history.md` (append-only — Phase 10A candidate round and
    candidate decision-mirror entry); `docs/handoff-state.md`,
    `docs/roadmap.md`, `docs/open-issues.md`, `docs/verification-log.md`, this
    manifest, `docs/roundtable-import-bridge.md`, `LLM_DIRECTOR.md`, and
    `README.md` — all updated to record: Phase 10A authored as a candidate (`docs/architecture-baseline.md` Section 25); superseded by the lock bundle above; Phase 10B not started.
- Verification status: lightweight verification — the six Docker-free quality
  gates were run on the delivered state as a regression check (`uv run pytest
  -q` **418 passed**, ruff / mypy (78 source files) / import-linter (2
  contracts) clean, `storytime doctor` healthy); the static legal/compliance
  scan returns zero violations. A diff against the base archive confirms only
  `.md` living-doc files changed. Per the Phase Closure Protocol this is
  amendment-authoring output; superseded by the Phase 10A locked-state bundle above.
- Known caveats: superseded by `storytime-phase10a-locked-state-bundle.tar.gz`, which records Section 25 as locked / accepted / canonical. Phase 10B has not started.
- State Preservation Bundle inclusion: complete — all Bundle files present,
  including `LLM_DIRECTOR.md`.

### storytime-phase9b-locked-state-bundle.tar.gz

- Phase: Phase 9B — Minimal Trust Envelope Implementation **lock closure**
  (with the Phase 9B.1 forbidden-term-scanner hardening cleanup folded into the
  lock). **Phase 9B locked (2026-05-24).** Documentation-only.
- sha256: `f7d205959986907a80b101602b6f4a58032a61e0b03ab23256d9b2dc45039a4f`.
- Source / base artifact: `storytime-phase9b1-forbidden-scanner-hardening.tar.gz`
  (sha256 `f6fd02bb780521e3bc9d9d64fc7c7a9392aa532b41d9e1cc5d27e66e5dd67608`).
- Round type: lock-closure round — no application code, governance code,
  database schema, artifact envelope code, configuration behaviour, test, or
  dependency changed; only State Preservation Bundle Markdown docs were edited.
  `docs/architecture-baseline.md` was not touched.
- Files modified:
  - **State Preservation Bundle docs** — `docs/canonical-state.md` (new
    Phase 9B LOCKED section), `docs/phase-history.md` (Phase 9B lock entry),
    `docs/handoff-state.md` (Current phase rewritten to Phase 9B locked /
    Phase 10 next), `docs/roadmap.md` (Phase 9B → locked, Phase 9C → not
    scheduled, new Phase 10 section), `docs/open-issues.md`,
    `docs/verification-log.md`, `docs/artifact-manifest.md`,
    `docs/roundtable-import-bridge.md`, `LLM_DIRECTOR.md`, `README.md`.
- Verification status: all six Docker-free gates were re-run as a regression
  check and pass — `uv sync --frozen`, **pytest 418 passed**, ruff clean, mypy
  clean (78 files, strict), import-linter 2/2 kept, `doctor` healthy; the
  hardened forbidden-term scan returns zero violations. **Phase 9B locked;
  Phase 9B.1 folded in.**
- Known caveats: none new. State Preservation Bundle inclusion: full Bundle
  included in the archive.

### storytime-phase9b1-forbidden-scanner-hardening.tar.gz

- Phase: Phase 9B.1 — Forbidden-Term Scanner Hardening Cleanup. A targeted
  cleanup applying Gemini's single `SAFE WITH MINOR CLEANUP` item from the
  Phase 9B review. **Phase 9B remains implemented and delivered as a candidate;
  not yet locked.**
- sha256: reported on delivery (a file cannot contain its own hash).
- Source / base artifact: `storytime-phase9b-minimal-trust-envelope-implementation.tar.gz`
  (sha256 `162ad0f49a7ee7e4c21035f4f9f562962a28f407d9887bf8d14110100d3b2a3c`).
- Round type: targeted cleanup round — scanner hardening only.
- Files modified:
  - **`src/storytime/governance/legal_terms.py`** — the static
    legal/compliance forbidden-term scanner rewritten to a deterministic,
    cross-platform `os.walk` traversal with an explicit ignored-directory prune
    set, a text-extension allowlist (so binary/generated files are never
    opened), and `errors="replace"` reads (so invalid UTF-8 can never raise).
  - **`tests/test_legal_hallucination_gate.py`** — seven hardening tests added.
  - **State Preservation Bundle docs** — minimal Phase 9B.1 records.
- Files unchanged: the Trust Envelope model/schema/IO, the blocked-source
  config, the SQLite schema, the pipeline gates, `pyproject.toml` / `uv.lock`,
  and `docs/architecture-baseline.md`.
- Verification status: all six Docker-free gates pass — `uv sync --frozen`,
  **pytest 418 passed**, ruff clean, mypy clean (78 files, strict),
  import-linter 2/2 kept, `doctor` healthy; the hardened forbidden-term scan
  returns zero violations. Not yet locked.
- Known caveats: none new. State Preservation Bundle inclusion: full Bundle
  included in the archive.

### storytime-phase9b-minimal-trust-envelope-implementation.tar.gz

- Phase: Phase 9B — Minimal Trust Envelope Implementation. The implementation
  of the locked Architecture Baseline Section 24 governance law. **Implemented
  and delivered as a candidate; not yet locked** — pending GPT-5.5 review,
  Gemini critique, and explicit user approval.
- sha256: reported on delivery (a file cannot contain its own hash).
- Source / base artifact: `storytime-phase9a-locked-state-bundle.tar.gz`
  (sha256 `1a67e2d0936376f6ea00cd7a9b1a16e57bd388fc3404fc0b41be5f6b0fffff21`).
- Round type: implementation round — the first Phase 9 round to change
  application code, database schema, and dependencies.
- Files added:
  - **`src/storytime/governance/`** — new package: `trust_envelope.py` (model
    + enums), `schema.py` (canonical §24.8 closed JSON Schema), `io.py`
    (serialization + versioned compatibility reader), `blocked_sources.py`
    (§24.9 deny-list loader/matcher), `gate.py` (fail-closed gate + manifest
    derivation), `legal_terms.py` (§24.14 static scanner), `__init__.py`.
  - **`config/governance/blocked-sources.yaml`** — committed empty deny-list
    with a documented schema header.
  - **Tests** — `test_trust_envelope.py`, `test_blocked_sources.py`,
    `test_governance_gate.py`, `test_governance_pipeline.py`,
    `test_legal_hallucination_gate.py` (53 tests).
- Files modified:
  - **`src/storytime/state/schema.py`** — migration `0005` adds the
    `trust_envelope` projection table; SCHEMA_VERSION 4 -> 5.
  - **`src/storytime/state/store.py`**, **`state/__init__.py`** —
    `TrustEnvelopeRecord` and projection write/read methods.
  - **`src/storytime/dto/stage_io.py`**, **`dto/__init__.py`** —
    `TrustEnvelopeIntent`; `StateUpdate.trust_envelope`.
  - **`src/storytime/events/model.py`** — `GOVERNANCE_EVALUATED` event type.
  - **`src/storytime/runner/runner.py`** — translates the trust-envelope
    intent into the projection inside the single transaction.
  - **`src/storytime/stages/ingest.py`** — derives the Trust Envelope, writes
    the durable artifact, projects it, emits `GovernanceEvaluated`, and applies
    the early fail-closed check.
  - **`src/storytime/stages/synthesize.py`** — hard governance gate before TTS.
  - **`src/storytime/stages/publish.py`** — hard governance gate before RSS.
  - **`src/storytime/config.py`** — `governance_blocked_sources_path` + the
    `STORYTIME_BLOCKED_SOURCES` override.
  - **`src/storytime/cli/app.py`** — `storytime status` governance line.
  - **`pyproject.toml`** — `pyyaml` promoted to a runtime dependency,
    `types-pyyaml` added for dev, import-linter no-OpenTelemetry contract
    extended to `storytime.governance`; **`uv.lock`** re-locked.
  - **`tests/test_vertical_slice.py`** — `GovernanceEvaluated` added to the
    expected event sequence.
  - **State Preservation Bundle docs** plus `docs/runbook.md` and
    `docs/telemetry-map.md`.
- Verification status: all six Docker-free gates pass — `uv sync --frozen`,
  **pytest 411 passed**, ruff clean, mypy clean (78 files, strict),
  import-linter 2/2 kept, `doctor` healthy. Not yet locked.
- Known caveats: none new. State Preservation Bundle inclusion: full Bundle
  included in the archive.

### storytime-phase9a-locked-state-bundle.tar.gz

- Phase: Phase 9A — Governance Baseline Amendment **lock closure** (with the
  Phase 9A.1 governance-baseline cleanup folded in). Phase 9A **locked**.
  Architecture/documentation only.
- sha256: reported on delivery (a file cannot contain its own hash).
- Source / base artifact: `storytime-phase9a-governance-baseline-amendment.tar.gz`
  (sha256 `bc35f7a1af6764f70b788515bdc842fad5c55a4d9a7ad7f75917a5d23e64fac6`).
- Round type: bounded compound round — the Phase 9A.1 cleanup, the Phase 9A
  lock closure, and the drafting of the Phase 9B implementation prompt. No
  application code, database schema, artifact envelope code, telemetry code,
  configuration behaviour, test, or dependency changed — only Markdown
  living-doc files, plus one new draft-prompt Markdown file.
- Files modified:
  - **`docs/architecture-baseline.md`** — Section 24 cleanup + lock closure.
    Added the source-authorization-not-viewpoint rule (§24.5) and the early
    fail-closed clarification (§24.6); the §24 status block, the §24.16 closing
    precondition, and the §24.17 closing clause changed from "candidate /
    pending lock" to "locked / accepted". The governance rules, the Trust
    Envelope schema, and the Phase 9A / 9B / 9C split are otherwise unchanged.
  - **State Preservation Bundle docs** — `docs/phase-history.md` and
    `docs/canonical-state.md` (append-only — the Phase 9A.1 + LOCKED round and
    the Phase 9A locked-decision record); `docs/handoff-state.md`,
    `docs/roadmap.md`, `docs/open-issues.md`, `docs/verification-log.md`, this
    manifest, `docs/roundtable-import-bridge.md`, `LLM_DIRECTOR.md`, and
    `README.md` — all updated to record Phase 9A locked, Section 24 canonical,
    Phase 9B next and not started.
  - **New** `docs/phase9b-minimal-trust-envelope-implementation-prompt.md`
    — the draft Phase 9B implementation prompt. It is a draft prompt only — not
    implementation, and it authorizes nothing by itself.
- Verification status: lightweight verification — the six Docker-free quality
  gates were run on the delivered state as a regression check (`uv run pytest
  -q` **358 passed**, ruff / mypy (71 source files) / import-linter (2
  contracts) clean, `storytime doctor` healthy). A diff against the base
  archive confirms only `.md` files changed (the existing living docs plus the
  one new draft-prompt file). Per the Phase Closure Protocol Phase 9A is now a
  locked phase.
- Known caveats: architecture/documentation lock-closure round only. Section 24
  is now a locked, canonical part of the Architecture Baseline; Phase 9B may
  depend on it. Phase 9B has not started.
- State Preservation Bundle inclusion: complete — all Bundle files present,
  including `LLM_DIRECTOR.md`.

### storytime-phase9a-governance-baseline-amendment.tar.gz

- Phase: Phase 9A — Governance Baseline Amendment (candidate; pending
  review/lock). Architecture/documentation only.
- sha256: reported on delivery (a file cannot contain its own hash).
- Source / base artifact: `storytime-phase8c-locked-state-bundle.tar.gz`.
- Round type: architecture/documentation amendment-authoring round. No
  application code, database schema, artifact envelope code, telemetry code,
  configuration behaviour, test, or dependency changed — only Markdown
  living-doc files. The contents are byte-identical to the base archive except
  for the documents listed below.
- Files modified:
  - **`docs/architecture-baseline.md`** — added **Section 24**, "Governance
    Baseline (Trust Envelope, Licensing, Fail-Closed Gating)" — the Phase 9A
    Architecture Baseline amendment **candidate**. Defines the governance
    model, the canonical minimum Trust Envelope schema (§24.8), the
    fail-closed gating law (§24.6), the legal-hallucination ban (§24.3), the
    future grep/regex gate requirement (§24.14), and the Phase 10 dependency
    contract (§24.15). Earlier sections are unchanged.
  - **State Preservation Bundle docs** — `docs/phase-history.md` and
    `docs/canonical-state.md` (append-only — Phase 9A candidate round and
    candidate decision-mirror entry); `docs/handoff-state.md`,
    `docs/roadmap.md`, `docs/open-issues.md`, `docs/verification-log.md`, this
    manifest, `docs/roundtable-import-bridge.md`, `LLM_DIRECTOR.md`, and
    `README.md` — all updated to record: Phase 9A authored as a candidate
    (`docs/architecture-baseline.md` Section 24), pending GPT-5.5 review,
    Gemini critique, and explicit user lock; Phase 9B not started.
- Verification status: lightweight verification — the six Docker-free quality
  gates were run on the delivered state as a regression check (`uv run pytest
  -q` **358 passed**, ruff / mypy (71 source files) / import-linter (2
  contracts) clean, `storytime doctor` healthy). A diff against the base
  archive confirms only `.md` living-doc files changed. Per the Phase Closure
  Protocol this is amendment-authoring output, not a locked phase: Section 24
  is a candidate until the user locks it.
- Known caveats: architecture/documentation round only. Section 24 is an
  authored amendment **candidate** — not locked; it awaits GPT-5.5 review,
  Gemini critique, and explicit user approval. No Phase 9B implementation may
  depend on it until then.
- State Preservation Bundle inclusion: complete — all Bundle files present,
  including `LLM_DIRECTOR.md`.

### storytime-phase8c-locked-state-bundle.tar.gz

- Phase: Phase 8C / 8C.1 lock closure — Phase 8C **locked**, Phase 8 complete.
- sha256: reported on delivery (a file cannot contain its own hash).
- Source / base artifact: `storytime-phase8c1-vendor-profile-split.tar.gz`.
- Round type: state/documentation lock-closure only. No application code, no
  vendor configs, no vendor profile behaviour, and no test changed. The
  contents are byte-identical to the 8C.1 archive except for the State
  Preservation Bundle docs, which were updated to record the Phase 8C lock.
- Files modified: `LLM_DIRECTOR.md`, `README.md`, and the State Preservation
  Bundle docs `canonical-state.md`, `handoff-state.md`, `phase-history.md`,
  `roadmap.md`, `roundtable-import-bridge.md`, `artifact-manifest.md`,
  `verification-log.md` — all updated to record: Phase 8C / 8C.1 locked
  (2026-05-24, explicit user approval; Gemini `SAFE TO LOCK`); Phase 8C.1
  accepted as part of the Phase 8C lock; Phase 8 complete; next phase is
  Phase 9A — Governance Baseline Amendment (not started).
- Verification status: the six Docker-free quality gates were re-run on the
  base 8C.1 archive as lock evidence — `uv run pytest -q` **358 passed**, ruff
  / mypy (71 files) / import-linter (2 contracts) clean, `storytime doctor`
  healthy. Per the Phase Closure Protocol Phase 8C is now a locked phase.

### storytime-phase8c1-vendor-profile-split.tar.gz

- Phase: Phase 8C — Optional Vendor Export Profiles, with the Phase 8C.1
  cleanup applied — the reviewed implementation archive that was **locked**
  (the lock is recorded in `storytime-phase8c-locked-state-bundle.tar.gz`).
- sha256: `b93cc84a473fe71df2ef2f00862c9ab2a7cce019c11da83ec5e738c0818c7f40`.
- Source / base artifact: `storytime-phase8c-vendor-export-profiles.tar.gz`.
- Scope: Phase 8C.1 — targeted cleanup of the Phase 8C output before lock. It
  splits the single combined vendor override into two independent, mutually
  exclusive per-vendor profiles. No `src/` file, `pyproject.toml` dependency,
  or application test changed; no Section 23 invariant changed.
- Files added/modified:
  - **New** `config/vendor/otel-collector.dynatrace.example.yaml` — local
    Phase 8B collector config plus the single `otlphttp/dynatrace` profile.
  - **New** `config/vendor/otel-collector.newrelic.example.yaml` — local
    Phase 8B collector config plus the single `otlphttp/newrelic` profile.
  - **New** `docker-compose.vendor.dynatrace.yml` — Dynatrace-only override;
    points the collector at the Dynatrace vendor config.
  - **New** `docker-compose.vendor.newrelic.yml` — New Relic-only override;
    points the collector at the New Relic vendor config.
  - **Removed** `config/otel-collector-vendor.yaml` and
    `docker-compose.vendor.yml` — the combined override, superseded by the
    four split files above.
  - **Modified** `config/vendor.secret.env.example` — header updated for the
    two profiles (content/placeholders unchanged).
  - **Modified** `docs/vendor-export-profiles.md` — rewritten for the split,
    documenting per-vendor activation and the mutual-exclusivity constraint.
  - **Modified** `tests/test_vendor_export_profiles.py` — rewritten for the
    split shape (parametrized per vendor; each config wires exactly its own
    profile; overrides target distinct configs/paths).
  - **Modified** `tests/test_containerization.py` — the Phase 8C opt-in file
    set updated to the four split files.
  - **Modified** `.dockerignore`, `.env.example`, `docs/telemetry-map.md`,
    `docs/observability-demo.md`, `docs/runbook.md`, `README.md`,
    `LLM_DIRECTOR.md`, `docs/open-issues.md` (OI-22) — per-vendor override
    names.
  - **Modified** State Preservation Bundle docs (`phase-history`,
    `canonical-state`, `handoff-state`, `roadmap`, `verification-log`,
    `artifact-manifest`, `roundtable-import-bridge`) — record the Phase 8C.1
    cleanup; the `handoff-state` "if that inference is wrong, revert"
    self-doubt language was removed.
- Verification status: six gates re-run after the cleanup (see
  `docs/verification-log.md`). Per the Phase Closure Protocol this was implementation output before lock; superseded by the Phase 10B lock bundle above.

### storytime-phase8c-vendor-export-profiles.tar.gz

- Phase: Phase 8C — Optional Vendor Export Profiles (implementation output;
  pending review/lock — its lock closes Phase 8).
- sha256: reported on delivery (a file cannot contain its own hash).
- Source / base artifact: `storytime-phase8b1-logs-preflight-cleanup.tar.gz`.
- Files added/modified:
  - **New** `config/otel-collector-vendor.yaml` — the local Phase 8B collector
    config plus disabled-by-default `otlphttp/dynatrace` and `otlphttp/newrelic`
    export profiles (standard OTLP/HTTP only; bounded retry + sending queue).
  - **New** `docker-compose.vendor.yml` — override compose file; swaps the
    collector onto the vendor config and reads credentials from a git-ignored
    `config/vendor.secret.env`. Vendor egress requires this explicit extra `-f`
    file; the default stack is unchanged and local-only.
  - **New** `config/vendor.secret.env.example` — committed placeholder template
    (obvious `REPLACE-WITH-YOUR-...` values on `.invalid` hosts; no real
    secret). The real `config/vendor.secret.env` is git-ignored / docker-ignored.
  - **New** `docs/vendor-export-profiles.md` — the Phase 8C documentation.
  - **New** `tests/test_vendor_export_profiles.py` — 12 static governance tests.
  - **Modified** `tests/test_containerization.py` — the Phase 7C.1 test
    `test_no_vendor_telemetry_fanout_config_is_introduced` renamed and updated
    to `test_vendor_export_config_is_confined_to_the_phase8c_optin_files` (the
    Section 16 note's blanket "no vendor fan-out" was narrowly superseded by the
    locked Section 23.14).
  - **Modified** `.dockerignore`, `.env.example` — vendor opt-in pointers.
  - **Modified** State Preservation Bundle docs (`phase-history`,
    `canonical-state`, `handoff-state`, `roadmap`, `open-issues`,
    `verification-log`, `artifact-manifest`, `roundtable-import-bridge`,
    `telemetry-map`, `observability-demo`, `runbook`, `LLM_DIRECTOR.md`,
    `README.md`) — record the Phase 8B / 8B.1 lock and the Phase 8C
    implementation output.
- Verification status: six gates pass (346 tests). Per the Phase Closure
  Protocol this is implementation output, not a locked phase.
- Known caveats: the override compose merge and live vendor export are
  unverified without Docker — open issue **OI-22**.

### storytime-phase8b1-logs-preflight-cleanup.tar.gz

- Phase: Phase 8B.1 — Operational cleanup: logs-directory preflight
  (implementation output; folds into the Phase 8B lock).
- sha256: reported on delivery (a file cannot contain its own hash).
- Source / base artifact: `storytime-phase8b-local-multi-backend-stack.tar.gz`.
- Files added/modified:
  - `Makefile` — added a `logs-dir` preflight target (`mkdir -p logs`) and
    three convenience targets: `observability-up` (depends on `logs-dir`,
    then `docker compose ... up -d`), `observability-down`, and `demo`
    (depends on `logs-dir`, then `python -m storytime.demo --log-dir logs`).
    `.PHONY` and `make help` updated.
  - `tests/test_observability_stack.py` — two regression tests added asserting
    the `logs-dir` preflight exists and that `observability-up` and `demo`
    depend on it (334 tests total).
  - `docs/observability-demo.md`, `docs/runbook.md`, `README.md` — show
    `mkdir -p logs` before `docker compose up` for manual users, with a short
    rationale, and point at the `make` shortcuts.
  - State Preservation Bundle living docs updated: `docs/phase-history.md`,
    `docs/canonical-state.md`, `docs/handoff-state.md`, `docs/roadmap.md`,
    `docs/open-issues.md`, `docs/verification-log.md`, this manifest,
    `docs/roundtable-import-bridge.md`, `LLM_DIRECTOR.md`.
- Verification status: six Docker-free quality gates pass — 334 tests (2 new),
  ruff/mypy/import-linter clean, `storytime doctor` healthy. The `./logs`
  bind-mount and the Loki path still need live Docker verification — OI-21,
  unchanged by this cleanup.
- Known caveats: narrow operational cleanup only — no application code,
  telemetry, Collector/Loki config, compose service, or dependency changed. It
  resolves the `SAFE WITH MINOR CLEANUP` review feedback on Phase 8B and folds
  into the eventual Phase 8B lock; it is not itself a separate lockable phase.
- State Preservation Bundle inclusion: complete — all Bundle files present,
  including `LLM_DIRECTOR.md`.

### storytime-phase8b-local-multi-backend-stack.tar.gz

- Phase: Phase 8B — Local Multi-Backend Stack Expansion (implementation output;
  pending review/lock).
- sha256: reported on delivery (a file cannot contain its own hash).
- Source / base artifact: `storytime-phase8a-locked-state-bundle.tar.gz`.
- Files added/modified:
  - **New** `config/loki.yaml` — minimal local Loki config (single-binary,
    filesystem storage, auth disabled, 72h retention).
  - **New** `src/storytime/demo/logsink.py` — structured JSON-lines log sink
    for the demo (`write_demo_log`); OTel-free, control-plane metadata only.
  - **New** `tests/test_observability_stack.py` — 18 Phase 8B tests (Loki
    config, collector logs pipeline / `filelog` / resiliency / no-vendor
    governance, compose Loki service + loopback ports + log mount, Grafana
    Loki datasource, log-sink JSON-lines / control-plane / append behavior).
  - `config/otel-collector.yaml` — rewritten: added a `filelog` receiver, a
    `memory_limiter` processor, a `resource/logs` processor, a `logs`
    pipeline, an `otlphttp` exporter to Loki, and `retry_on_failure` +
    `sending_queue` on the Jaeger and Loki exporters. Traces/metrics
    pipelines and the `add_metric_suffixes: false` metric-honesty setting are
    preserved.
  - `docker-compose.observability.yml` — rewritten: added the `loki` service
    (`grafana/loki:3.3.2`, `127.0.0.1:3100`); the collector mounts `./logs`
    read-only; collector and Grafana `depends_on` Loki.
  - `config/grafana/provisioning/datasources/datasources.yaml` — added the
    Loki datasource (provisioned as code).
  - `src/storytime/demo/harness.py` — `run_demo` gained an optional
    `log_dir` parameter; writes the demo log when set (default off).
  - `src/storytime/demo/__main__.py` — added the `--log-dir` flag.
  - `.gitignore`, `.dockerignore` — added `logs/`.
  - Docs: `docs/telemetry-map.md` (Structured logging + Local backend
    sections), `docs/observability-demo.md` (Loki in the stack, logs path,
    new "Interpreting the logs" section), and the State Preservation Bundle
    living docs (`docs/phase-history.md`, `docs/canonical-state.md`,
    `docs/handoff-state.md`, `docs/roadmap.md`, `docs/open-issues.md`,
    `docs/verification-log.md`, this manifest, `docs/roundtable-import-bridge.md`,
    `LLM_DIRECTOR.md`, `README.md`).
- Verification status: six Docker-free quality gates pass — 332 tests (18
  new), ruff/mypy/import-linter clean, `storytime doctor` healthy. **Pending**:
  live Docker verification of the Loki image tag, `config/loki.yaml`, and the
  `filelog` → `otlphttp` → Loki path — open issue **OI-21**.
- Known caveats: implementation output, not a lock. Section 23 compliance
  holds (no vendor SDK/agent/exporter/secret; standard `otlphttp` only;
  `noop` telemetry default; offline test suite; control-plane-only file-routed
  logs). Logs originate from the demo harness only — the StoryTime
  application core gains no parallel logging system.
- State Preservation Bundle inclusion: complete — all Bundle files present,
  including `LLM_DIRECTOR.md`.

### storytime-phase8a-locked-state-bundle.tar.gz

- Phase: Phase 8A — Architecture Baseline Amendment — lock closure.
- sha256: reported on delivery (a file cannot contain its own hash).
- Source / base artifact: `storytime-phase8a-architecture-amendment.tar.gz`.
- Files added/modified: documentation-only lock closure.
  `docs/architecture-baseline.md` — Section 23 status changed from authored
  candidate to **locked / accepted**, with the §16 amendment note and the
  §23.14 closing clause updated for status consistency (the twelve rules and
  the 8A/8B/8C split are unchanged). Appended `docs/phase-history.md` and
  `docs/canonical-state.md` (Phase 8A locked record). Updated
  `docs/handoff-state.md`, `docs/roadmap.md`, `docs/verification-log.md`,
  `docs/roundtable-import-bridge.md`, `LLM_DIRECTOR.md`, and `README.md`. No
  application, telemetry, Docker, Collector-config, test, or dependency change.
- Verification status: six Docker-free quality gates pass (314 tests). No
  runtime/container behavior changed, so no new Docker validation was needed.
- Known caveats: documentation-only lock-closure round. Section 23 is now a
  locked, canonical part of the Architecture Baseline; Phase 8B may depend on
  it.
- State Preservation Bundle inclusion: complete — all Bundle files present,
  including `LLM_DIRECTOR.md`.

### storytime-phase8a-architecture-amendment.tar.gz

- Phase: Phase 8A — Architecture Baseline Amendment (candidate).
- sha256: reported on delivery (a file cannot contain its own hash).
- Source / base artifact: `storytime-state-preservation-bundle-docs.tar.gz`.
- Files added/modified: `docs/architecture-baseline.md` (added Section 23, the
  Phase 8A Collector-owned-fan-out amendment candidate; added a Phase 8A
  candidate cross-reference note to §16); appended `docs/phase-history.md` and
  `docs/canonical-state.md` (Phase 8A candidate, clearly labeled pending lock);
  updated `docs/handoff-state.md`, `docs/roadmap.md`, `docs/open-issues.md`,
  `docs/verification-log.md`, `docs/roundtable-import-bridge.md`,
  `LLM_DIRECTOR.md`, and `README.md`. No application, telemetry, Docker,
  configuration, test, or dependency change.
- Verification status: six Docker-free quality gates pass (314 tests). No
  runtime/container behavior changed, so no new Docker validation was needed.
- Known caveats: architecture/documentation round only. Section 23 is an
  authored amendment **candidate** — not locked; it awaits GPT-5.5 review,
  Gemini critique, and explicit user approval.
- State Preservation Bundle inclusion: complete — all Bundle files present,
  including `LLM_DIRECTOR.md`.

### storytime-state-preservation-bundle-docs.tar.gz

- Phase: Phase 7 complete — State Preservation Bundle director system round.
- sha256: reported on delivery (a file cannot contain its own hash).
- Source / base artifact: `storytime-phase7d1-with-state-bundle.tar.gz`.
- Files added/modified: added `LLM_DIRECTOR.md` at repo root; updated the
  State Preservation Bundle docs (`docs/roadmap.md`, `docs/handoff-state.md`,
  `docs/roundtable-import-bridge.md`, `docs/verification-log.md`,
  `docs/artifact-manifest.md`) to record Phase 7 complete and Phase 8 next;
  appended `docs/canonical-state.md` and `docs/phase-history.md`; updated
  `docs/open-issues.md` and `README.md`. No application, Docker, telemetry,
  test, or dependency change.
- Verification status: six Docker-free quality gates pass (314 tests). No
  runtime/container behavior changed, so no new Docker validation was needed.
- Known caveats: documentation/state-preservation round only.
- State Preservation Bundle inclusion: complete — all 15 Bundle files present,
  including `LLM_DIRECTOR.md`.

### storytime-phase7d1-with-state-bundle.tar.gz

- Phase: Phase 7D.1 + initial State Preservation Bundle.
- sha256: `63cd2e6f352fc7483fadfb81e438666d9f1e1219b42bd55930deb94e83cc9bb6`.
- Source / base artifact: `storytime-phase7d1-compose-build-fix.tar.gz`.
- Files added/modified: added the first State Preservation Bundle docs
  (`roadmap.md`, `handoff-state.md`, `verification-log.md`,
  `artifact-manifest.md`, `roundtable-import-bridge.md`); updated `README.md`
  and `docs/phase-history.md`. No code change.
- Verification status: six gates pass (314 tests).
- Known caveats: superseded by `storytime-state-preservation-bundle-docs.tar.gz`
  (which adds `LLM_DIRECTOR.md` and the Phase 7 completion updates).
- State Preservation Bundle inclusion: partial — 14 of 15 files (no
  `LLM_DIRECTOR.md`).

### storytime-phase7d1-compose-build-fix.tar.gz

- Phase: Phase 7D.1 — Operational Cleanup: Compose Build Race Fix.
- sha256: `b5489f10b02b3fd4ee5690f6f9053038a32c4655cb13ba318a5236145e77ff5b`.
- Source / base artifact: `storytime-phase7c1-app-containerization.tar.gz`.
- Files added/modified: `docker-compose.app.yml` (one builder; consumer uses
  `pull_policy: never`); `tests/test_containerization.py` (5 build-contract
  tests); docs (`deployment-containerized.md`, `README.md`, `runbook.md`,
  `phase-history.md`, `open-issues.md`). No application source change.
- Verification status: six gates pass (314 tests); live Docker smoke test
  passed on Windows Docker Desktop / WSL2 (see `docs/verification-log.md`).
- Known caveats: none outstanding — Phase 7D.1 is locked.
- State Preservation Bundle inclusion: none (predates the Bundle).

### storytime-phase7c1-app-containerization.tar.gz

- Phase: Phase 7D — Optional Local App Containerization (the Phase 7C.1
  amendment's implementation; earlier labeled "Phase 7C.1 / 7D").
- sha256: `9b450cf86aaa39dbec38c138c98e39d55842cda11deb95506ac6644172016fcd`.
- Source / base artifact: `storytime-phase7b-bluegreen-frontdoor-switching.tar.gz`.
- Files added/modified: added `Dockerfile`, `.dockerignore`,
  `docker-compose.app.yml`, `tests/test_containerization.py`,
  `docs/deployment-containerized.md`; stable slot-derived
  `service.instance.id` in config/telemetry; doc updates. 179 entries.
- Verification status: six gates pass (309 tests); live Docker smoke-tested.
- Known caveats: none outstanding — Phase 7D is locked.
- State Preservation Bundle inclusion: none (predates the Bundle).

### storytime-phase7b-bluegreen-frontdoor-switching.tar.gz

- Phase: Phase 7B — Higher-Assurance Front Door / Active-Slot Switching.
- sha256: `f3ca94b0fa2f31efa082622918908f1da15d0b1a6cc60e951473699ad87c504a`.
- Source / base artifact: `storytime-phase7a-bluegreen-option-a.tar.gz`.
- Files added/modified: `storytime.frontdoor` package (native Python
  loopback-only reverse proxy), active-slot pointer, switch/rollback scripts,
  docs. 174 entries.
- Verification status: six gates pass (285 tests). Locked.
- Known caveats: none. State Preservation Bundle inclusion: none.

### storytime-phase7a-bluegreen-option-a.tar.gz

- Phase: Phase 7A — Blue/Green Option A (per-slot processes).
- sha256: `4b4ce674945c497d538c547bda7e5ed514684fd77b454edbe2893b9b1cfa570f`.
- Source / base artifact: prior locked codebase (Phase 6B).
- Files added/modified: slot-scoped state/feed roots, per-slot env files,
  `run-slot.sh`, deployment-identity banner, docs.
- Verification status: six gates clean. Locked.
- Known caveats: none. State Preservation Bundle inclusion: none.

## RoundTable response reports

Companion `RT_RESPONSE_*.md` reports accompany each round (Phase 7A, 7B
planning, 7B implementation, 7C amendment, 7C.1 revised amendment, 7D
containerization, 7D.1 operational cleanup, and this State Preservation Bundle
docs round). They are delivered alongside the archives and are not stored
inside the repository tree (`.dockerignore` / `.gitignore` exclude
`RT_RESPONSE_*`).

## Lineage notes

- Each archive contains the full prior codebase plus that round's changes.
  There is no fork.
- Runtime artifacts (`.venv/`, `runs/`, `feed/`, tool caches) are excluded from
  every archive; the tracked `config/deploy/active-slot` pointer is preserved
  at its default value `blue`.

## Phase 13K — Demo Walkthrough Refresh / Governed Local Chain Story Path — LOCKED (2026-05-28)

- Artifact: `storytime-phase13k-demo-walkthrough-refresh-governed-local-chain-story-path.tar.gz`
- SHA-256: `bf3bcc87cd147205558eddd16b53c5a09e91af1bfa6269d10a8de153a7e6f10a`
- Source / base artifact: locked Phase 13J `storytime-phase13j-operator-gui-polish-demo-local-alignment.tar.gz` (SHA-256 `7fdfcc4dbb23a99cd569310f77e2a6d958df6d88f435cd575556df01f070f589`).
- Contents: canonical `docs/demo-walkthrough.md`, machine-checkable truth labels, tiered reviewer path, technical inspection appendix, deferred-capability register, evidence map, refreshed in-app DemoWalkthroughView / demoWalkthroughAdapter, stale demo/portfolio doc reconciliation via pointers/supersession notes.
- Lock basis: GPT preliminary verification PASS, Gemini implementation review SAFE TO LOCK, no required edits, protected surfaces byte-identical, archive hygiene clean.
- Verification status: six gates clean (970 tests). Locked — last locked phase.
- Known caveats: none.

## Phase 13L — Phase 13 Closure / Demo-Local Completion Lock (implementation candidate — pending review — not locked — 2026-05-28)

- Artifact: `storytime-phase13l-phase13-closure-demo-local-completion-lock.tar.gz`
- SHA-256: recorded in the Phase 13L final report and `docs/verification-log.md` at build time (an artifact cannot embed its own hash).
- Source / base artifact: locked Phase 13K `storytime-phase13k-demo-walkthrough-refresh-governed-local-chain-story-path.tar.gz` (SHA-256 `bf3bcc87cd147205558eddd16b53c5a09e91af1bfa6269d10a8de153a7e6f10a`, verified on extraction).
- Contents (docs + tests only): records Phase 13K as locked across the living state docs; adds `docs/phase13-closure.md` and `docs/phase14-readiness-handoff.md`; advances the state-discipline guard `tests/test_failure_mode_regression.py` to the Phase 13L expectations; appends 13G–13K lock and 13L closure-candidate records to the append-only history docs.
- Protected surfaces: `pyproject.toml`, `uv.lock`, `src/`, `frontend/src/`, `frontend/package.json`, `frontend/package-lock.json`, `frontend/vite.config.ts`, `frontend/tsconfig.json`, the committed static export, and `frontend/src/data/adapter.ts` are byte-identical to the locked Phase 13K source.
- Verification status: implementation candidate, pending review, NOT locked. Prepares the Phase 13 closure as a candidate; Phase 13 is not yet externally closed.
- Known caveats: none. Phase 14 — Cloud/Distributed — has not started; Phase 14A is the next proposed architecture baseline.


---

## Phase 14A.1 — Local Live Proof Loop Before Cloud (implementation candidate; pending review; NOT locked)

**Date:** 2026-05-29
**Source artifact:** `storytime-phase13l-phase13-closure-demo-local-completion-lock.tar.gz`, SHA-256 `acecdf0aac7e6f184be1c368e37f65170bf25365751090adfc394ffdde2e5a53` (verified on extraction).
**New artifact:** `storytime-phase14a1-local-live-proof-loop-before-cloud.tar.gz`. Built with the canonical `scripts/build-artifact.sh` (deterministic, sorted, numeric-owner tar; excludes `node_modules`, `dist`, `runs/`, `feed/`, audio, caches, databases, nested archives, and `.env`). The artifact's own SHA-256 is reported in the producing round's build report and Phase 14A.1 verification entry and will be confirmed at lock (an artifact cannot contain its own hash).
**Protected surfaces unchanged (byte-identical to the Phase 13L source):** `pyproject.toml`, `uv.lock`, `frontend/package.json`, `frontend/package-lock.json`, `frontend/src/data/storytime-demo-export.json`. No dependency was added (standard-library HTTP only).


---

## Phase 14D — Cloud / Distributed Architecture Baseline from Proven Local Contracts (LOCKED)

**Date:** 2026-05-30
**Source artifact:** `storytime-phase14c5-1-durable-recovery-control-plane-boundary.tar.gz`, SHA-256 `73a9ee1bdcbca295037f4852375d3f6b1ff155c3a0ea9d1b0fe498de3862e604` (the locked Phase 14C.5.1 baseline; verified on extraction). The Phase 14C sequence is locked / complete through 14C.5.1; Phase 14C.5.1 is the last locked phase.
**New artifact (LOCKED):** `storytime-phase14d-cloud-distributed-architecture-baseline.tar.gz`, SHA-256 `a4ccc8aa59beaf6365081973d1c3d78235df028ef0f3214979e9d3b98f4dcce6`. Built with the canonical `scripts/build-artifact.sh` (deterministic, sorted, numeric-owner tar; excludes `node_modules`, `dist`, `runs/`, `feed/`, audio, caches, databases, nested archives, and `.env`). This artifact is immutable and is the locked Phase 14D deliverable; internally it self-labels Phase 14D a "candidate / pending review / NOT locked" — the project's standard internal framing for a locked artifact (every locked artifact self-labels as a candidate). The lock itself is recorded in this ledger and the living state, not inside the artifact.
**Contents (docs + tests only):** new `docs/phase14d-cloud-distributed-architecture-baseline.md` (the as-built cloud/distributed mapping deliverable) and `docs/phase14d-deferred-cloud-work-register.md` (deferred cloud/distributed work register); new pure-text guard `tests/test_cloud_distributed_baseline_doc.py`; re-anchored state-discipline guard `tests/test_failure_mode_regression.py` (Phase 14C.5.1 recorded LOCKED / last locked; Phase 14D recorded as the current candidate; 14E/15 future); current-state banners prepended and the prior 14C.5.1 banner demoted to history across the living state docs (`LLM_DIRECTOR.md`, `README.md`, `docs/canonical-state.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/phase-history.md`, `docs/artifact-manifest.md`, `docs/verification-log.md`, `docs/open-issues.md`, `docs/phase14-cloud-distributed-roadmap.md`, `docs/phase14-cloud-queue-mapping.md`, `docs/phase14-queue-worker.md`, `docs/phase14-contracts-as-built.md`); dated 14D records appended to the append-only history docs.
**Protected surfaces unchanged (byte-identical to the locked Phase 14C.5.1 source):** `pyproject.toml`, `uv.lock`, `package.json` / `frontend/package.json`, `package-lock.json` / `frontend/package-lock.json`, the entire `src/` tree, and `frontend/src/`. No dependency was added; no application, frontend, bridge, queue/worker, recovery, ArtifactStore, or observability behavior changed. Phase 14D is documentation, state, and guard work only.
**Verification status: LOCKED.** Lock basis: GPT preliminary review PASS (ready for Gemini review); Gemini implementation review SAFE TO LOCK with no required edits; Gemini accepted the native-Windows validation caveat as non-blocking; the Phase 14D-specific guards passed; no `src/`, `frontend/`, dependency-manifest, runtime, cloud, broker, object-storage, auth, provider-TTS, RSS, polling/WebSocket/EventSource, or observer-schema change. Native-Windows gates recorded in `docs/verification-log.md`: `uv sync --frozen` / `ruff` / `mypy` (108 files) / `lint-imports` (2 kept, 0 broken) / `doctor` (healthy) all PASS; `uv run pytest` reported 1093 passed, 14 failed, 28 skipped. The 14 failures are Windows/POSIX environment-sensitive failures in files byte-identical to the locked 14C.5.1 baseline (no Phase 14D source change); the Phase 14D-owned guards all passed. Full `pytest` is NOT recorded as a clean pass; a clean Linux/WSL `uv run pytest` remains recommended.
**Known caveats:** none. Phase 14D implements no cloud/distributed behavior (no external broker, distributed worker, cloud object storage, signed URLs, auth, cloud recovery orchestration, automatic retries, provider TTS, audio, RSS, or polling/WebSockets/EventSource). Phase 14 remains STARTED; Phase 14E and Phase 15 remain NOT STARTED.
