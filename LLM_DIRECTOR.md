> **Phase 15C note — Minimal Cloud Demo Deployment / Portfolio Readiness (current implementation candidate; pending review; NOT locked).**
>
> **State:** Phase 15A — Cloud Runtime Skeleton — is LOCKED, and Phase 15B — Cloud Boundary Readiness — is LOCKED (the last locked phase and the baseline for this round). Phase 14D remains LOCKED. Phase 15 — Cloud / Distributed Runtime — remains STARTED, and **Phase 15C — Minimal Cloud Demo Deployment / Portfolio Readiness — has now STARTED as the current implementation candidate (pending review, NOT locked).**
> **What Phase 15C adds:** a public, cloud-hosted *static* operator demo of the local-first, observability-native pipeline and its cloud-readiness seams. It adds one static deployment path (a GitHub Pages workflow that builds the existing frontend and publishes `frontend/dist`), narrow display-only frontend safety changes (a verbatim demo disclaimer banner, a `STATIC_DEMO_MODE` flag, and a local-only notice that gates the two backend-dependent views so the public demo makes no network call), demo docs (`docs/phase15c-minimal-cloud-demo.md`, `DEMO.md`) with a two-minute talk track, and a static overclaim guard (`tests/test_phase15c_static_demo_claims.py`).
> **What Phase 15C does not do:** it adds no backend execution, no serverless function, no public mutation endpoint, no external broker, no object-storage backend, no authentication, no provider telemetry export, no provider TTS, no RSS, and no dependency. Nothing is deployed to the cloud except static files; no backend is running behind the demo, and no distributed worker is running. It is the first phase to touch the frontend, and the change is deliberately copy/display-only and static-demo-safe.
> **Reserved future (NOT STARTED):** Phase 14E — Local Release Candidate / Full Local Mode Closure — remains NOT STARTED and was not opened (intentionally bypassed). Phase 15D — Cloud Backend Runtime Skeleton, Phase 15E — External Queue / Object Store Proof, and Phase 15F — Cloud Observability Export Proof remain NOT STARTED.
> **Validation:** the locked backend gate (`uv run pytest` / `ruff check .` / `mypy src` / `lint-imports` / `storytime doctor`) plus the frontend build (`npm ci` / `npm run typecheck` / `npm run build`) are expected green in the canonical POSIX/Linux environment; operator validation and GPT/Gemini review are the gates before any Phase 15C lock.

> **Phase 15B note — Cloud Boundary Readiness (LOCKED).**
>
> **Lock lineage:** Phase 12 is CLOSED; Phase 13 is CLOSED; Phase 14 remains STARTED (not closed); Phase 14A.1, Phase 14B.1, Phase 14C.1, Phase 14C.2, Phase 14C.3, Phase 14C.4, Phase 14C.5.1, and Phase 14D are LOCKED. Phase 15 — Cloud / Distributed Runtime — remains STARTED; Phase 15A — Cloud Runtime Skeleton — is LOCKED, and **Phase 15B — Cloud Boundary Readiness — is now LOCKED** as its second round and is the last locked phase.
> **Locked artifact:** `storytime-phase15b-cloud-boundary-readiness.tar.gz`, SHA-256 `80dbdb8331dc55f8704f1a4d28364e9b954bbaec7a6d07d6456d9c1efd46723e` — immutable and not rebuilt or altered by this lock record.
> **Lock basis:** GPT preliminary review PASS (ready for Gemini review); Gemini implementation review SAFE TO LOCK, with no critical findings, no non-blocking findings, and no required edits. Canonical POSIX/Linux validation: 1199 passed, with ruff clean, mypy clean across 112 files, import-linter 2 kept / 0 broken, and doctor healthy. Windows/operator validation was recorded honestly with the known native-Windows POSIX-sensitive baseline caveats; Gemini accepted that validation profile as sufficient for lock.
> **What Phase 15B locked:** one pure-data, provider-neutral `storytime.runtime.boundary_readiness` module modelling four cloud-growth seams — queue/worker, artifact/storage, observability/export, and recovery/idempotency — as a `BoundaryReadinessSnapshot`, plus its design doc, deferred-work register, guard tests, and state records. It added no dependency, no environment variable, and no CLI command, and changed no existing behaviour.
> **Reserved future (NOT STARTED):** Phase 14E — Local Release Candidate / Full Local Mode Closure — remains NOT STARTED and was not opened (intentionally bypassed). Phase 15C, Phase 15D, and Phase 15E remain NOT STARTED. Phase 15C is the likely first cloud infrastructure skeleton candidate, but it is not started here.
> **Boundaries preserved (unchanged):** the locked readiness model is descriptive pure data; it wraps, proxies, or adapts none of the WorkQueue, ArtifactStore, StateStore, recovery, or observer contracts, expands no observer schema, and binds no socket.
> **Honest framing:** Phase 15B implements no cloud behaviour; it is not a distributed system, does not run in the cloud, and adds no external broker, no distributed worker, no object storage, no authentication, no telemetry export, no dashboards, no distributed locks, no scheduler, no provider TTS, no audio, and no RSS.

> **Phase 15B note — Cloud Boundary Readiness (current implementation candidate; pending review; NOT locked).**
>
> **State:** Phase 15A — Cloud Runtime Skeleton — is LOCKED (the last locked phase and the baseline for this round). Phase 14D remains LOCKED. Phase 15 — Cloud / Distributed Runtime — remains STARTED, and **Phase 15B — Cloud Boundary Readiness — has now STARTED as the current implementation candidate (pending review, NOT locked).**
> **What Phase 15B adds:** one pure-data `storytime.runtime.boundary_readiness` module modelling four cloud-growth seams — queue/worker, artifact/storage, observability/export, and recovery/idempotency — as a `BoundaryReadinessSnapshot` of four boundary summaries (active local backend, source of truth, current guarantees, required-before-cloud invariants, deferred capabilities, explicit non-goals), plus a design doc (`docs/phase15b-cloud-boundary-readiness.md`), a deferred-work register (`docs/phase15b-deferred-cloud-work-register.md`), guard tests (`tests/test_cloud_boundary_readiness.py`), and state records. It combines the previously planned 15B–15D seams into one disciplined boundary-readiness phase.
> **What Phase 15B does not do:** it adds no new dependency, no new environment variable (it reads only the existing `STORYTIME_RUNTIME_ROLE`), and no CLI command; it changes no WorkQueue, ArtifactStore, StateStore, recovery, or observer semantics, and wraps, proxies, or adapts none of them. It implements no external broker, no distributed worker, no object storage, no authentication, no telemetry export, no collector, no dashboards, no distributed locks, no retry engine, no scheduler, and no provider TTS or RSS. It is not a distributed system and does not run in the cloud.
> **Reserved future (NOT STARTED):** Phase 14E — Local Release Candidate / Full Local Mode Closure — remains NOT STARTED and was not opened (intentionally bypassed). Phase 15C, Phase 15D, and Phase 15E remain NOT STARTED. Phase 15C is the likely first cloud infrastructure skeleton candidate, but it is not started here.
> **Validation:** the locked gate (`uv run pytest` / `ruff check .` / `mypy src` / `lint-imports` / `storytime doctor`) is expected green in the canonical POSIX/Linux environment; operator validation and GPT/Gemini review are the gates before any Phase 15B lock.

> **Phase 15A note — Cloud Runtime Skeleton (LOCKED).**
>
> **Lock lineage:** Phase 12 is CLOSED; Phase 13 is CLOSED; Phase 14 remains STARTED (not closed); Phase 14A.1, Phase 14B.1, Phase 14C.1, Phase 14C.2, Phase 14C.3, Phase 14C.4, Phase 14C.5.1, and Phase 14D are LOCKED. Phase 15 — Cloud / Distributed Runtime — remains STARTED, and **Phase 15A — Cloud Runtime Skeleton — is now LOCKED** as its first round and is the last locked phase.
> **Locked artifact:** `storytime-phase15a-cloud-runtime-skeleton.tar.gz`, SHA-256 `ee256221abb7393fc0dde07365bca9647b1ba2d0420c64b434e6c67b9bcf871f` — immutable and not rebuilt or altered by this lock record.
> **Lock basis:** GPT preliminary review PASS (ready for Gemini review); Gemini implementation review SAFE TO LOCK, with no critical findings, no non-blocking findings, and no required edits. Canonical POSIX/Linux validation: 1160 passed. Windows/operator validation: 1118 passed, 14 known POSIX-sensitive failures, 28 skipped — with the Phase 15A runtime tests passing 28 of 28 on Windows and ruff, mypy, import-linter, and doctor all passing; Gemini accepted that validation record as sufficient for lock.
> **What Phase 15A locked:** a pure-data `storytime.runtime` package — runtime ROLE separation (`api` / `worker` / `combined`, default `combined`), a configuration-derived health / readiness model, and a runtime config boundary reading only `STORYTIME_RUNTIME_ROLE` — plus its design doc, guard tests, and state records. It adds no new dependency and changes no existing behaviour.
> **Reserved future (NOT STARTED):** Phase 14E — Local Release Candidate / Full Local Mode Closure — remains NOT STARTED and was not opened (intentionally bypassed). Phase 15B, Phase 15C, Phase 15D, and Phase 15E remain NOT STARTED.
> **Runtime role boundary (unchanged):** the locked role model is descriptive pure data; it binds no socket, opens no database, drains no queue, and wraps none of the existing WorkQueue, ArtifactStore, recovery, or observer contracts.
> **Honest framing:** Phase 15A implements no cloud behaviour; it is not a distributed system, does not run in the cloud, does not import OpenTelemetry, and adds no external broker, no distributed worker, no object storage, no authentication, no public ingress, no provider TTS, no audio, and no RSS.

> **Phase 15A note — Cloud Runtime Skeleton (current implementation candidate; pending review; NOT locked).**
>
> **Lock lineage:** Phase 13A–13L LOCKED (Phase 13 Closure / Demo-Local Completion Lock) · **14A.1 LOCKED** · **14B.1 LOCKED** · **14C.1 LOCKED** · **14C.2 LOCKED** · **14C.3 LOCKED** · **14C.4 LOCKED** · **14C.5.1 LOCKED** · **14D LOCKED** (Cloud / Distributed Architecture Baseline from Proven Local Contracts, locked using `storytime-phase14d-cloud-distributed-architecture-baseline.tar.gz`, SHA-256 `a4ccc8aa59beaf6365081973d1c3d78235df028ef0f3214979e9d3b98f4dcce6`). **Phase 13 is CLOSED**, **Phase 12 remains CLOSED**. **Phase 14D remains the last locked phase**; Phase 15A is the current implementation candidate and is **NOT locked**. The Phase 14C.5.1 durable `recovery_action` lineage table remains the backend-owned recovery source of truth, unchanged by this phase.
> **Current phase:** **Phase 15 — Cloud / Distributed Runtime — is STARTED.** Phase 15A — Cloud Runtime Skeleton — is the current implementation candidate (pending review; **NOT locked**). Phase 14E — Local Release Candidate / Full Local Mode Closure — remains **NOT STARTED**; it was intentionally bypassed for this transition to Phase 15A. Phase 15A adds the smallest local-first, cloud-shaped runtime skeleton on top of the proven, LOCKED Phase 14D local contracts: a runtime ROLE separation (`api` / `worker` / `combined`), a configuration-derived health and readiness model, and a runtime configuration boundary that reads only the new `STORYTIME_RUNTIME_ROLE` variable and otherwise derives everything from the immutable `StoryTimeConfig`. The default role is `combined`, which preserves the proven local single-process behaviour exactly.
> **What Phase 15A does NOT do:** it does not implement an external broker (no Redis, NATS, SQS, Temporal, Celery, Kafka, or RabbitMQ), no distributed worker, no object storage, no S3 or MinIO, no signed URLs, no authentication, no API keys, no public ingress, no Kubernetes, Terraform, or Helm, no provider TTS, no audio, no RSS, no dashboards, no SLOs, no alerting, no distributed tracing, no collector, and no new dependency. It is not a distributed system and does not run in the cloud. It does not import OpenTelemetry, and it changes no backend, frontend, bridge, queue/worker, recovery, artifact-store, or observation behaviour; it adds a pure-data `storytime.runtime` package, documentation, state records, and guard tests only.
> **Accepted roadmap (mutable):** 14C.1 Local Durable Queue / Worker Shape Proof (LOCKED) · 14C.2 Contracts-as-Built / Cloud-Distributed Seam Baseline (LOCKED) · 14C.3 Object Storage Boundary / Artifact Store Adapter (LOCKED) · 14C.4 Minimal Observability Boundary for Queue/Worker (LOCKED) · 14C.5.1 Durable Recovery Control Plane Boundary (LOCKED) · 14D Cloud / Distributed Architecture Baseline from Proven Local Contracts (LOCKED) · 14E Local Release Candidate / Full Local Mode Closure (future; not started; intentionally bypassed for now) · 15 Cloud / Distributed Runtime (STARTED) · 15A Cloud Runtime Skeleton (current candidate; pending review; not locked). The recommended later decomposition (a queue-worker adapter, an artifact-store adapter, an observability export, and a recovery-lineage proof) is recorded in the Phase 14D baseline document.
> **Reserved future (NOT STARTED):** Phase 15B, Phase 15C, Phase 15D, and Phase 15E remain **NOT STARTED**; they are reserved labels for the later cloud decomposition and nothing in them is built. No external broker, no cloud queue, no Kubernetes, no Terraform, no object storage, no distributed worker, no authentication, no provider TTS, no audio, and no RSS exists yet — all remain deferred future work. Phase 14C.5 through Phase 14C.10 were absorbed into Phase 14C.5.1 and are historical planning labels only.
> **Runtime role boundary:** the three runtime roles describe how a single LOCAL process is shaped, not where it runs. `api` serves the loopback operator read-model only and does not drain the local work queue by default; `worker` drains the existing local durable work queue and executes the proven pipeline and serves no public API; `combined` does both and is the proven local default. The API role reuses the LOCKED loopback bind guard (`validate_bind_host`) and binds no public interface; the health model is pure data derived from configuration and the role — it instantiates no worker, queue, or artifact store, binds no socket, opens no database, and wraps nothing.
> **Configuration boundary:** Phase 15A reads exactly one new environment variable, `STORYTIME_RUNTIME_ROLE` (`api` / `worker` / `combined`, default `combined`); an unrecognised value fails fast. The deployment dimension is fixed to `local`; `STORYTIME_DEPLOYMENT` is documented as DEFERRED and is NOT read as active configuration in this phase. The health summary exposes no secrets, credentials, or filesystem paths.
> **Honest framing (unchanged):** proof runs are deterministic, local, mock fixture runs — not real provider audio; durable state and artifacts are backend-owned, not the browser; execution is queued then drained by a local worker, not run inline on the request and not a cloud / distributed system; recovery is a durable, bounded, backend-decided local action, not automated retry; observation is in-process and ephemeral; the frontend performs one bounded post-run refresh plus manual refresh — not a live sync, and it does not poll. Phase 15A names a local-first runtime shape and describes readiness from configuration; it makes none of these pieces cloud, distributed, or networked, and it changes none of their behaviour.

> **Phase 14D note — Cloud / Distributed Architecture Baseline from Proven Local Contracts (LOCKED).**
>
> **Lock lineage:** Phase 13A–13L LOCKED (Phase 13 Closure / Demo-Local Completion Lock) · **14A.1 LOCKED** · **14B.1 LOCKED** · **14C.1 LOCKED** · **14C.2 LOCKED** · **14C.3 LOCKED** · **14C.4 LOCKED** · **14C.5.1 LOCKED** (Durable Recovery Control Plane Boundary, locked using `storytime-phase14c5-1-durable-recovery-control-plane-boundary.tar.gz`, SHA-256 `73a9ee1bdcbca295037f4852375d3f6b1ff155c3a0ea9d1b0fe498de3862e604`) · **14D LOCKED** (Cloud / Distributed Architecture Baseline from Proven Local Contracts, locked using `storytime-phase14d-cloud-distributed-architecture-baseline.tar.gz`, SHA-256 `a4ccc8aa59beaf6365081973d1c3d78235df028ef0f3214979e9d3b98f4dcce6`). **Phase 13 is CLOSED**, **Phase 12 remains CLOSED**. With Phase 14D locked, **Phase 14D is the last locked phase**; the Phase 14C.5.1 durable `recovery_action` lineage table remains the backend-owned recovery source of truth.
> **Current phase:** **Phase 14 — Live System / Cloud-Distributed — is STARTED.** Phase 14D — Cloud / Distributed Architecture Baseline from Proven Local Contracts — is **LOCKED** (locked using `storytime-phase14d-cloud-distributed-architecture-baseline.tar.gz`, SHA-256 `a4ccc8aa59beaf6365081973d1c3d78235df028ef0f3214979e9d3b98f4dcce6`). Phase 14D is a documentation-and-mapping round only: it takes the proven, LOCKED local contracts — request acceptance, the durable work-queue port, the local worker, the artifact store, the durable recovery control plane, in-process observation, and the operator read-model — and writes down the shape each would take in a future cloud / distributed deployment, as the readiness basis for a possible later Phase 15. It implements no cloud behavior of any kind: no external broker, no Redis/NATS/SQS/Temporal/Celery, no Kubernetes, no Terraform, no object storage, no S3/MinIO, no distributed worker, no authentication, no provider TTS, no audio, no RSS, and no new dependency. It changes no backend, frontend, bridge, queue/worker, recovery, artifact-store, or observation behavior; it adds documentation, state records, and guard tests only.
> **Accepted roadmap (mutable):** 14C.1 Local Durable Queue / Worker Shape Proof (LOCKED) · 14C.2 Contracts-as-Built / Cloud-Distributed Seam Baseline (LOCKED) · 14C.3 Object Storage Boundary / Artifact Store Adapter (LOCKED) · 14C.4 Minimal Observability Boundary for Queue/Worker (LOCKED) · 14C.5.1 Durable Recovery Control Plane Boundary (LOCKED) · 14D Cloud / Distributed Architecture Baseline from Proven Local Contracts (LOCKED) · 14E Local Release Candidate / Full Local Mode Closure (future; not started) · 15 Cloud / Distributed Runtime (future; not started; recommended decomposition recorded in the Phase 14D baseline document). The previously sketched provider-TTS / frontend-audio / RSS content-production items (formerly the 14D.1–14D.4 labels) are **deferred future work**, not part of Phase 14D and not started.
> **Reserved future (NOT STARTED):** Phase 14E — Local Release Candidate / Full Local Mode Closure — is **not started**. Phase 15 — the Cloud / Distributed Runtime that would implement the mappings recorded in this phase — is **not started**; the Phase 14D baseline document only recommends how Phase 15 could later be decomposed (for example a cloud runtime skeleton, a queue-worker adapter, an artifact-store adapter, an observability export, and a recovery-lineage proof), and recommends nothing be built yet. No external broker, no cloud queue, no Kubernetes, no Terraform, no object storage, no distributed worker, no authentication, no provider TTS, no audio, and no RSS exists yet — all remain deferred future work. Phase 14C.5 through Phase 14C.10 were absorbed into Phase 14C.5.1 and are historical planning labels only.
> **Cloud / distributed mapping boundary:** this phase records, on paper only, how each proven local seam would map to a cloud / distributed runtime: the local request path → a stateless API service; the SQLite-backed `WorkQueue` port → a managed queue or broker behind the same port; the in-process `LocalWorker` → one or more horizontally scaled worker processes; the `LocalFilesystemArtifactStore` → an object store behind the same `ArtifactStore` port; the durable `recovery_action` control plane → the same backend-owned eligibility policy over a shared database; in-process observation → an exported telemetry stream; and the operator read-model → the same read API. Every mapping is a written target, not a running component; nothing in this list is built, wired, or deployed in this phase.
> **Scope boundary:** Phase 14D is an as-built mapping and documentation round — not a cloud adapter, not a distributed system, not a deployment. It adds three documentation artifacts (a cloud / distributed architecture baseline, a deferred cloud-work register, and supporting state and changelog records) plus pure-text guard tests, and nothing else. No external queue, no Redis/NATS/SQS/Temporal/Celery, no dead-letter queue, no automatic retries, no backoff, no scheduler, no cloud leases, no distributed locks, no Kubernetes, no Terraform, no cloud or object storage, no S3/MinIO, no signed URLs, no distributed worker, no provider TTS, no audio, no RSS, no authentication, no polling, no WebSockets/EventSource, and no new dependency are introduced. It does not change the Phase 14C.5.1 recovery control plane, the Phase 14C.4 observation boundary, or any queue/worker, artifact-store, backend, bridge, or frontend behavior.
> **Honest framing (unchanged):** proof runs are deterministic, local, mock fixture runs — not real provider audio; durable state and artifacts are backend-owned, not the browser; execution is queued then drained by a local worker, not run inline on the request and not a cloud / distributed system; recovery is a durable, bounded, backend-decided local action, not automated retry; observation is in-process and ephemeral; the frontend performs one bounded post-run refresh plus manual refresh — not a live sync, and it does not poll. Phase 14D writes down how these proven local pieces would map to the cloud; it does not make any of them cloud, distributed, or networked, and it changes none of their behavior.

> **Phase 14C.5.1 note — Durable Recovery Control Plane Boundary (historical — now LOCKED; superseded by Phase 14D).**
>
> **Lock lineage:** Phase 13A–13L LOCKED (Phase 13 Closure / Demo-Local Completion Lock) · **14A.1 LOCKED** · **14B.1 LOCKED** · **14C.1 LOCKED** · **14C.2 LOCKED** · **14C.3 LOCKED** · **14C.4 LOCKED** (Minimal Observability Boundary for Queue/Worker, locked using `storytime-phase14c4-minimal-observability-boundary-queue-worker.tar.gz`, SHA-256 `12b951e0a9b6b17f5c73aacf0d055b257bd4a715908f7f5078d401eae2a66d3b`). **Phase 13 is CLOSED**, **Phase 12 remains CLOSED**. With Phase 14C.4 locked, **Phase 14C.4 is the last locked phase**, and its observer (`QueueWorkerEvent`) events are **explanatory only — not the durable retry/recovery lineage source of truth.**
> **Current phase:** **Phase 14 — Live System / Cloud-Distributed — is STARTED.** Phase 14C.5.1 — Durable Recovery Control Plane Boundary — was the implementation candidate and is now **LOCKED** (locked using `storytime-phase14c5-1-durable-recovery-control-plane-boundary.tar.gz`, SHA-256 `73a9ee1bdcbca295037f4852375d3f6b1ff155c3a0ea9d1b0fe498de3862e604`). Phase 14C.5.1 adds the smallest durable, backend-owned recovery control plane: a durable `recovery_action` lineage table (source of truth) linking an original failed execution to a bounded recovery execution, a backend-owned recovery **eligibility policy**, **duplicate-prevention** and a **bounded attempt limit**, a recovery **read-model** projection, local SQLite **concurrency guardrails**, and a cloud-queue **mapping CONTRACT** document. It does not expand the Phase 14C.4 observer event schema, and changes no queue/worker or ArtifactStore execution semantics.
> **Accepted roadmap (mutable):** 14C.1 Local Durable Queue / Worker Shape Proof (LOCKED) · 14C.2 Contracts-as-Built / Cloud-Distributed Seam Baseline (LOCKED) · 14C.3 Object Storage Boundary / Artifact Store Adapter (LOCKED) · 14C.4 Minimal Observability Boundary for Queue/Worker (LOCKED) · 14C.5.1 Durable Recovery Control Plane Boundary (current) · 14D.1 Provider TTS Boundary, Mock-First · 14D.2 Frontend Audio Understanding, Not Playback Yet · 14D.3 RSS Publishing Boundary / Preview · 14D.4 Local Content Production Closure · 14E Local Release Candidate / Full Local Mode Closure. Phase 14C.5.1 **absorbs** the previously planned local recovery-control-plane scope from **Phase 14C.5 through Phase 14C.10**; those numbers are historical planning labels only and are NOT separate active phases.
> **Reserved future (NOT STARTED):** Phase 14D (the provider-TTS / frontend-audio / RSS content-production arc) is **not started**; Phase 14E (local release candidate / full local mode closure) is **not started**. Phase 14C.5 through Phase 14C.10 were absorbed into Phase 14C.5.1 and are not separate active phases. No cloud queue, external broker, dead-letter queue, automatic retries, exponential backoff, retry scheduler, distributed worker, cloud lease, distributed lock, cloud object store, provider TTS, audio, or RSS exists yet — all remain deferred future work.
> **Recovery control-plane boundary:** the durable `recovery_action` table is the **source of truth** for recovery lineage; observer events remain explanatory only. Eligibility is decided in the **backend** (a caller/frontend can request recovery but can never decide whether it is allowed) and yields a bounded decision (`retry_eligible`, `not_failed`, `unknown_original`, `duplicate_recovery`, `max_attempts_reached`, `blocked_by_governance`, `in_progress`, `terminal_failure`) with a durable reason. Duplicate active recovery is prevented under local SQLite via an atomic `requested` slot (`BEGIN IMMEDIATE`); attempts are bounded by a small fixed default. Rejected requests are **durably visible** with their decision/reason. There is **no** cloud retry orchestration, **no** distributed worker, **no** external broker, **no** dead-letter queue, **no** backoff, and **no** scheduler.
> **Scope boundary:** Phase 14C.5.1 is a minimal local recovery control plane — not a workflow engine, not a distributed retry system, not a cloud queue adapter. No external queue, no Redis/NATS/SQS/Temporal/Celery, no dead-letter queue, no automatic retries, no backoff, no scheduler, no cloud leases, no distributed locks, no cloud object storage, no provider TTS, no audio, no RSS, no auth, no broad frontend retry console, and no dependency. It does **not** expand the Phase 14C.4 observer event schema for retry correlation. The browser only requests and may trigger only allowlisted scenarios; the backend owns truth, durable state, artifact storage, observation, and recovery eligibility; the local-live API binds loopback-only with a strict origin allowlist (no wildcard CORS).
> **Honest framing (unchanged):** proof runs are deterministic, local, mock fixture runs — not real provider audio; durable state and artifacts are backend-owned, not the browser; execution is queued then drained by a local worker, not run inline on the request and not a cloud/distributed system; recovery is a durable, bounded, backend-decided local action, not automated retry; observation is in-process/ephemeral and safe; the frontend performs one bounded post-run refresh plus manual refresh — not a live sync, and it does not poll.

> **Phase 14C.4 note — Minimal Observability Boundary for Queue/Worker (historical — now LOCKED; superseded by Phase 14C.5.1).**
>
> **Lock lineage:** Phase 13A–13L LOCKED (Phase 13 Closure / Demo-Local Completion Lock) · **14A.1 LOCKED** · **14B.1 LOCKED** · **14C.1 LOCKED** · **14C.2 LOCKED** · **14C.3 LOCKED** (Object Storage Boundary / Artifact Store Adapter, locked using `storytime-phase14c3-1-contracts-doc-state-wording-cleanup.tar.gz`). **Phase 13 — Portfolio Website / Operator GUI — is CLOSED**, and **Phase 12 — Portfolio / SE Demo Packaging — remains CLOSED**. With Phase 14C.3 locked, **Phase 14C.3 is the last locked phase.**
> **Current phase:** **Phase 14 — Live System / Cloud-Distributed — is STARTED.** Phase 14C.4 — Minimal Observability Boundary for Queue/Worker — was the implementation candidate and is now **LOCKED** (`storytime-phase14c4-minimal-observability-boundary-queue-worker.tar.gz`, SHA-256 `12b951e0a9b6b17f5c73aacf0d055b257bd4a715908f7f5078d401eae2a66d3b`). Phase 14C.4 added a small backend-owned, **in-process** observation boundary for the local queue/worker lifecycle: safe, vendor-neutral event names (`work.enqueued/claimed/started`, `stage.started/completed`, `artifact.recorded`, `work.completed/failed`) and safe fields (existing local identifiers, timestamps, status), emitted fail-soft at the existing lifecycle points. It changes no queue/worker or ArtifactStore execution semantics and adds no dependency.
> **Accepted roadmap (mutable):** 14C.1 Local Durable Queue / Worker Shape Proof (LOCKED) · 14C.2 Contracts-as-Built / Cloud-Distributed Seam Baseline (LOCKED) · 14C.3 Object Storage Boundary / Artifact Store Adapter (LOCKED) · 14C.4 Minimal Observability Boundary for Queue/Worker (current) · 14C.5 Durable Retry / Recovery Lineage · 14C.6 Full Local Observability Deepening · 14C.7 Auth-Capable API Boundary · 14D.1 Provider TTS Boundary, Mock-First · 14D.2 Frontend Audio Understanding, Not Playback Yet · 14D.3 RSS Publishing Boundary / Preview · 14D.4 Local Content Production Closure · 14E Local Release Candidate / Full Local Mode Closure.
> **Reserved future (NOT STARTED):** Phase 14C.5 (durable retry / recovery lineage) is the next reserved sub-phase and has **not started**; Phase 14D (the provider-TTS / frontend-audio / RSS content-production arc) is **not started**; Phase 14E (local release candidate / full local mode closure) is **not started**. No collector, exporters, Prometheus endpoint, Grafana dashboards, alerting, SLOs, sampling, distributed tracing, cloud telemetry, retry/recovery lineage, cloud object store, provider TTS, audio, or RSS exists yet — all remain deferred future work.
> **Observability boundary:** Phase 14C.4 defines a minimal internal queue/worker observation boundary. It keeps a future single-collector / vendor fan-out possible by using vendor-neutral, schema-stable event names and safe fields. It does **not** implement the collector, exporters, dashboards, alerting/SLOs, sampling, distributed tracing, retry/recovery lineage, or cloud/distributed execution. Observation is **in-process and ephemeral by default** (no new database table, broker, or stream) and **fail-soft** (a sink error never breaks the proof loop). It exposes nothing new to the browser.
> **Scope boundary:** Phase 14C.4 is a minimal local observability boundary — not a telemetry platform. No OpenTelemetry SDK, no collector config, no Prometheus/Grafana/Tempo/Loki, no vendor integrations, no alerting, no SLOs, no sampling, no distributed tracing, no cloud telemetry, no retry/recovery lineage, no frontend dashboard, no polling, no WebSockets/EventSource, and no dependency. The browser only requests and may trigger only allowlisted scenarios; the backend owns truth, durable state, artifact storage, and observation; the local-live API binds loopback-only with a strict origin allowlist (no wildcard CORS).
> **Honest framing (unchanged):** proof runs are deterministic, local, mock fixture runs — not real provider audio; durable state and artifacts are backend-owned, not the browser; execution is queued then drained by a local worker, not run inline on the request and not a cloud/distributed system; observation is in-process/ephemeral and safe; the frontend performs one bounded post-run refresh plus manual refresh — not a live sync, and it does not poll.

> **Phase 14C.3 note — Object Storage Boundary / Artifact Store Adapter (historical — Phase 14C.3 is now LOCKED; see the Phase 14C.4 note above for current state).**
>
> **This sub-phase (now locked):** Phase 14C.3 — Object Storage Boundary / Artifact Store Adapter — was the implementation candidate when this note was written and has since been **LOCKED**. It put artifact handling behind a backend-owned `ArtifactStore` port with a single LOCAL filesystem adapter (logical key validation; absolute-path / `..` traversal / backslash / symlink-escape rejection; atomic writes; hash/size/media metadata; deterministic missing behavior; safe evidence), and routed the proof-run evidence write through it. It added no new dependency.
> **Honest framing (unchanged):** proof runs are deterministic, local, mock fixture runs — not real provider audio; durable state is backend-owned in SQLite, not the browser; the frontend refresh is bounded/manual, not a live sync.

> **Phase 14C.2 note — Contracts-as-Built / Cloud-Distributed Seam Baseline (historical — Phase 14C.2 is now LOCKED; see the Phase 14C.3 note above for current state).**
>
> **This sub-phase (now locked):** Phase 14C.2 — Contracts-as-Built / Cloud-Distributed Seam Baseline — was the implementation candidate when this note was written and has since been **LOCKED**. It added `docs/phase14-contracts-as-built.md` (the A–J contracts-as-built sections with abstract `Protocol` snippets for the queue port and worker execution) and guardrail tests, with no runtime `src/` changes. It added no new dependency.
> **Honest framing (unchanged):** proof runs are deterministic, local, mock fixture runs — not real provider audio; durable state is backend-owned in SQLite, not the browser; the frontend refresh is bounded/manual, not a live sync.

> **Phase 14C.1 note — Local Durable Queue / Worker Shape Proof (historical — Phase 14C.1 is now LOCKED; see the Phase 14C.2 note above for current state).**
>
> **This sub-phase (now locked):** Phase 14C.1 — Local Durable Queue / Worker Shape Proof — was the implementation candidate when this note was written and has since been **LOCKED**. It added the local durable work-queue port with a SQLite adapter, a single bounded local worker, a request path that enqueues a durable work item instead of executing inline, atomic claiming, lease-based stale-claim recovery, stale-partial recovery, and a safe read-model lifecycle. It added no new dependency.
> **Honest framing (unchanged):** proof runs are deterministic, local, mock fixture runs — not real provider audio; durable state is backend-owned in SQLite, not the browser; the frontend refresh is bounded/manual, not a live sync.

> **Phase 14B.1 note — Live Proof Loop Hardening / Operator Trust / Cloud-Ready Boundary Preparation (historical — Phase 14B.1 is now LOCKED; see the Phase 14C.1 note above for current state).**
>
> **This sub-phase (now locked):** Phase 14B.1 — Live Proof Loop Hardening / Operator Trust — was the implementation candidate when this note was written and has since been **LOCKED**. It added controlled, deterministic, durable failure/recovery proof scenarios (`governance_failure`, `artifact_validation_failure`) alongside `success`, operator-UX and read-model/DTO hardening, Windows operator docs, and cloud-readiness docs. It added no new dependency.
> **Honest framing (unchanged):** proof runs are deterministic, local, mock fixture runs — not real provider audio; durable state is backend-owned in SQLite, not the browser; the frontend refresh is bounded/manual, not a live sync.

> **Phase 14A.1 note — Local Live Proof Loop Before Cloud (historical — Phase 14A.1 is now LOCKED; see the Phase 14B.1 note above for current state).**
>
> **Lock lineage (at the time):** Phase 13A–13F LOCKED · 13G–13L LOCKED (Phase 13 Closure / Demo-Local Completion Lock). With Phase 13L locked, **Phase 13 — Portfolio Website / Operator GUI — is now formally CLOSED**.
> **This sub-phase (now locked):** Phase 14A.1 — Local Live Proof Loop Before Cloud — was the implementation candidate when this note was written and has since been **LOCKED**. It added a loopback-only local-live HTTP API (`src/storytime/local_live/`), a durable backend-owned proof-run harness that persists real run / stage / event / artifact state to SQLite (and survives a local-live server restart), a `storytime local-live` command, and a frontend "Live Proof Loop" surface.
> **Reserved future (now Phase 14C.1+, NOT STARTED):** the combined cloud / distributed, provider-backed TTS, frontend audio, audio playback, and RSS work is reserved as Phase 14C.1+ and has **not started**. (Earlier notes called this reserved bundle "Phase 14B.1"; that label now denotes the current hardening round, and the reserved future bundle is the not-yet-started Phase 14C.1+.)
> **Honest framing (unchanged):** the proof run is a deterministic, local, mock fixture run — not real provider audio; durable state is backend-owned in SQLite, not the browser; the frontend refresh is manual, not a live sync.

> **Phase 13L note — Phase 13 Closure / Demo-Local Completion Lock (historical — Phase 13L is now LOCKED and Phase 13 is now CLOSED; see the Phase 14A.1 note above for current state).**
>
> **Lock lineage:** Phase 13A–13F LOCKED · Phase 13D.1 / 13D.2 LOCKED · Phase 13G LOCKED · Phase 13G.1 LOCKED · Phase 13H LOCKED · Phase 13H.1 LOCKED · Phase 13H.2 LOCKED · Phase 13H.3 LOCKED · Phase 13I LOCKED · Phase 13J LOCKED · Phase 13K LOCKED (Demo Walkthrough Refresh / Governed Local Chain Story Path). Phase 13K was the last locked phase when this Phase 13L note was written; Phase 13L has since locked, so Phase 13L is now the last locked phase.
> **This sub-phase:** Phase 13L — Phase 13 Closure / Demo-Local Completion Lock — implementation candidate; pending review; NOT locked. It is a closure / documentation round: it records Phase 13K as locked, prepares the Phase 13 closure as a candidate, summarizes the Demo + Local proof track, preserves `docs/demo-walkthrough.md` as the canonical reviewer path, and writes an architecture-first readiness handoff for the next, not-yet-started Phase 14 (`docs/phase14-readiness-handoff.md`). It adds no runtime capability and changes no source, frontend, or dependency.
> **Closure framing:** Like the Phase 12D closure round before it, Phase 13L only *prepares* the Phase 13 closure. Phase 13 closure is a candidate that is not yet externally locked; Phase 13 will be formally closed only after Phase 13L review/lock. Until then Phase 13 remains STARTED and is not closed.
> **Phase 14 (historical note):** When this Phase 13L note was written, Phase 14 had not yet started. Phase 14 has since STARTED; Phase 14A.1 — Local Live Proof Loop Before Cloud — is the current implementation candidate (see the Phase 14A.1 note above). The reserved future combined bundle is now named Phase 14C.1+ and is NOT STARTED.
> **Invariants:** docs and tests only. No new backend behavior, no new local bridge action, no generate_tts, no frontend TTS generation, no audio playback, no provider integration, no browser durable storage, no polling / live sync, no cloud / distributed / full Local mode, no RSS publishing, no authentication, and no cloud deployment. The read-only bridge client stays GET-only; retry_failed_stage stays the only submittable action; the backend bridge (`src/storytime/local_bridge/`), the `src/storytime/tts_proof/` package, the committed static export contract, and the locked Phase 13J / 13K surfaces are untouched.
> **Honest framing (unchanged):** an accepted retry is shown as accepted, not succeeded; a manual reload is a read-model refresh, not a live sync; the browser is not durable; mock output is labeled mock, not real provider audio; the real provider stays deferred / disabled; full Local mode and Cloud/Distributed mode do not exist.
> **Deferred to future (Phase 14) work:** frontend TTS generation, a real provider adapter, audio playback, batch generation, RSS publishing, authentication, and cloud/distributed mode all remain deferred.

# Phase 13L implementation-candidate note — Phase 13 Closure / Demo-Local Completion Lock

> **Superseded by the Phase 14A.1 round:** Phase 13L has since been LOCKED and, with it, Phase 13 is now CLOSED; Phase 14 is STARTED with Phase 14A.1 — Local Live Proof Loop Before Cloud — the current implementation candidate (pending review, NOT locked). The dated text below is preserved verbatim as the historical Phase 13L-round record.

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

# Phase 13F implementation-candidate note — Local Bridge Architecture & Contract Baseline

**Date:** 2026-05-27
**Round type:** Phase 13F — Local Bridge Architecture & Contract Baseline — a documentation-and-static-fixture architecture / contract baseline over the locked Phase 13E operator GUI (the architectural lock before any Python local-bridge implementation). No runtime code.
**Status:** Phase 13F is an **implementation candidate / pending review — NOT locked.**
**Last locked phase:** Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary (locked; SHA-256 `a997f2ca9d213e28e140f47c63336367c8feda46ed994b41300f86b99f8d8164`).

Phase 13F establishes the central principle that **the frontend is an operator surface, not the durable storage layer** — durable state must live outside the browser in an explicit workspace / storage target, so StoryTime never repeats the RoundTable browser-storage failure mode (`localStorage`/`sessionStorage`/`IndexedDB` stay forbidden). It adds eleven new architecture / contract docs, a set of non-runtime JSON example fixtures under `docs/examples/`, and one new Python contract-examples test (plain Python, no JSON-schema dependency). It settles the future local-bridge execution-timing policy (async long-running actions; `202 Accepted` + `actionRequestId`/`jobId`; acceptance is not success; export refresh after a durable write; refresh-race avoidance), the loopback-only / strict-origin / no-arbitrary-command / command-pattern-router security boundary, the action allowlist (`retry_failed_stage`, `inspect_trust_envelope`, `refresh_export`) with higher-risk actions deferred, and the queue-observability model. Phase 13F implements **NO** runtime code (no local bridge, no server, no async queue, no workers, no metrics exporters, no OpenTelemetry, no storage providers, no real Local mode, no Cloud/Distributed mode, no mutation execution); the browser remains non-durable. It does **not** modify `src/`, `frontend/src/`, `frontend/package.json`, `frontend/package-lock.json`, `pyproject.toml`, `uv.lock`, or `frontend/src/data/storytime-demo-export.json`. Per the Phase Closure Protocol, Phase 13F awaits review and an explicit user lock decision; it does not lock Phase 13F, does not close Phase 13, and does not start Phase 13G. Phase 13G+ have not started.

---

# Phase 13E implementation-candidate note — Demo-Mode Action Preview / Operator Intent Boundary (historical — Phase 13E is LOCKED; see the Phase 13F note above)

**Date:** 2026-05-27
**Round type:** Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary — a static, demo-mode, non-consequential sub-round over the locked Phase 13D.2 operator GUI.
**Status:** Historical record. Phase 13E has since been **LOCKED** and is the last locked phase; Phase 13F is the current implementation candidate (see above).
**Last locked phase:** Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path.
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13E.
**Next action:** Submit the Phase 13E artifact for GPT-5.5 review, then Gemini critique, then an explicit user decision — before locking Phase 13E or starting Phase 13F.

**Phase 13D.2 lock (recorded honestly).** Phase 13D.2 — Static Demo
Walkthrough / Reviewer Story Path — completed its Phase Closure
Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini
returned SAFE TO LOCK with no required edits, and the user, as final
decision-maker, locked Phase 13D.2. **Phase 13D.2 is LOCKED; it is
the last locked phase.** Phase 13 — Portfolio Website / Operator GUI
— remains STARTED and is not closed.

Phase 13E is the first sub-round that explicitly models operator
intent rather than only displaying read-only state — but it is
deliberately a **Demo-mode** sub-round and remains non-consequential.
The right framing is: *demo mode may preview serious operator intent
— demo mode must not create consequential changes.* Phase 13E adds a
static Demo-mode Action Preview system
(`frontend/src/data/actionPreviewAdapter.ts` plus
`frontend/src/components/ActionPreviewPanel.tsx` and its CSS Module)
that turns the existing visibly-disabled future-action affordances
into explainable, non-executing action previews. A "Preview action
plan" control opens an inline preview panel; the existing
`DisabledFutureActionCard` is unchanged (still a real
`<button disabled={true}>` with no `onClick`). The first set of
previews covers retry-failed-stage, inspect-trust-envelope,
record-review-decision, regenerate-operator-report, and
refresh-export. Each preview is data-driven (stable action id, label
and category, current mode (Demo), execution status (Preview only /
non-consequential), target object references, what the operator is
trying to accomplish, why it is blocked in Demo mode, precondition
checklist, evidence to inspect, risk level and explanation,
illustrative future Local-mode request shape labelled "Future
request shape — illustrative only, not executable in Demo mode",
Cloud/Distributed considerations, audit expectations, failure
behaviour expectation, what remains disabled, related view).

Phase 13E introduces or clarifies the eventual operating-mode model:
**Demo mode** (curated, safe, non-consequential, portfolio-ready;
the only mode implemented), **Local mode** (future real local
operator workflows; not implemented), and **Cloud / Distributed
mode** (future hosted/distributed execution; not implemented). Demo
/ Active / Candidate remain **data-snapshot** labels, distinct from
Demo / Local / Cloud-Distributed which are **operating-mode**
labels. The previews never look like execution — there is no fake
loading spinner, no simulated success state, no `setTimeout`
workflow, and no "Submitted" / "Succeeded" / "Audit created"
rendering. The user journey ends at an explicitly disabled
execution boundary.

Phase 13E is static, Demo-mode-only, and export-backed. It adds no
server, no live API, no `fetch`/`axios`/`localhost`/network call, no
`localStorage` / `sessionStorage`, no router / hash routing /
browser History API, no Context provider, no global preview/action
state, no actual retry / rerun / approval / report regeneration /
export refresh, no authentication, no Local mode, no
Cloud/Distributed mode, no audit-record generation (nothing
executed), no production hosting, and no fake-execution surface. It
does **not** modify the backend export generator
(`src/storytime/operator_export.py`), the committed static export
JSON (`frontend/src/data/storytime-demo-export.json`), the
`storytime export-demo-ui` CLI contract, or
`src/storytime/cli/app.py`; all four protected files / contracts are
byte-identical to the Phase 13D.2 source. No `src/`,
`pyproject.toml`, `uv.lock`, `frontend/package.json`,
`frontend/package-lock.json`, or root dependency changed. The
`tests/` changes are the narrow, explicitly authorized mechanical
advance of the state-discipline guard
`tests/test_failure_mode_regression.py` to the Phase 13E
current-state expectations, and one new
`tests/test_action_preview_data_integrity.py` that asserts the
run-id and other target ids referenced by the action-preview
adapter exist in the committed static export.

Per the Phase Closure Protocol, Phase 13E is an implementation
candidate, pending review, **not locked**; it does not lock Phase
13E, does not close Phase 13, and does not start Phase 13F. Phase
13F and every later Phase 13 subphase have **not** started — they
are future, planned work, decomposed in `docs/phase13-roadmap.md`.
Phase 9C remains optional and not scheduled.

*(Every Phase 13D.2-era and earlier note below is a historical
record. Phase 13D.2 is LOCKED; Phase 13E is the current
implementation candidate. The "Current state (checkpoint)" section
at the end of this file is the authoritative current-status
snapshot.)*

---
# Phase 13D.2 implementation-candidate note — Static Demo Walkthrough / Reviewer Story Path (historical record — Phase 13D.2 is LOCKED; see the Phase 13E note above)

**Date:** 2026-05-27
**Round type:** Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path — a frontend-only static / read-only demo-readiness sub-round of the locked Phase 13D.1, turning the existing operator GUI views into a coherent guided reviewer / demo path that absorbs ~80–90% of an Architecture Story narrative as embedded checkpoints.
**Status:** Historical record. This note described Phase 13D.2 while it was an implementation candidate. Phase 13D.2 has since been **LOCKED** and is the last locked phase; Phase 13E is now the current implementation candidate — see the Phase 13E note above and the "Current state (checkpoint)" section at the end of this file.
**Last locked phase:** Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline.
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path.
**Next action:** Submit the Phase 13D.2 artifact for GPT-5.5 review, then Gemini critique, then an explicit user decision — before locking Phase 13D.2 or starting Phase 13E.

**Phase 13D.1 lock (recorded honestly).** Phase 13D.1 — Static Operator
GUI Refinement / Evidence & Disabled Action Discipline — completed its
Phase Closure Protocol: implementation, GPT-5.5 review, and Gemini
critique. Gemini returned SAFE TO LOCK with no required edits, and the
user, as final decision-maker, locked Phase 13D.1. **Phase 13D.1 is
LOCKED; it is the last locked phase.** Phase 13 — Portfolio Website /
Operator GUI — remains STARTED and is not closed.

Phase 13D.2 is a static / read-only demo-readiness sub-round of Phase
13D.1. It takes the locked operator GUI and turns it into a coherent
guided reviewer / demo path before any future controlled local action
or mutation-boundary work — answering the reviewer questions "what
should I click first?", "what does this prove?", "what do I say about
this in an interview?", "where is the architecture boundary?", "how is
this local-first and safe?", "why is the frontend read-only?", and
"what is next, and why is it not live yet?". Phase 13D.2 replaces the
honest Demo Walkthrough placeholder with a real read-only view
(`frontend/src/components/DemoWalkthroughView.tsx` plus its CSS
Module) backed by a static view-model adapter
(`frontend/src/data/demoWalkthroughAdapter.ts`) that holds the
long-form route content. The view offers four reviewer routes — a
5-minute scan, a 10-minute SE-style demo, a technical deep-dive, and
a self-guided reviewer path — switched by a simple segmented control
backed by local `useState<RouteId>` (no router, no Context, no
persistence). Each step carries title, target view, what to inspect,
what it proves, talking points, and an in-line navigation affordance
into the relevant existing view; steps that point to a specific run
identify it by stable id (`run-2026-0518-golden` or
`run-2026-0520-review`) so the reviewer is never asked to guess. The
view also includes architecture-checkpoint cards (local-first design,
deterministic static export, backend-owns-truth /
frontend-owns-understanding, read-only operator surface, static
evidence boundary, disabled-action boundary, Demo / Active /
Candidate as data snapshots — not deployment environments —, and why
Phase 13E must be explicitly gated), a deliberate "what is
intentionally deferred" section, and interview / SE talking-point
callout cards. The view does not introduce a router, URL routing,
Context, global state, persistence, a guided-tour sidebar, or any
diagram/SVG/image; it stays a focused presentation shell driven by
adapter data.

Phase 13D.2 is static, read-only, and export-backed. It adds no
server, no live API, no `fetch`/`axios`/`localhost`/network call, no
watcher, no mutation, no authentication, no cloud deployment, no
production hosting, no dynamic file loading, and no Demo / Active /
Candidate switching. It does **not** modify the backend export
generator (`src/storytime/operator_export.py`), the committed static
export JSON (`frontend/src/data/storytime-demo-export.json`), the
`storytime export-demo-ui` CLI contract, or `src/storytime/cli/app.py`;
all four protected files / contracts are byte-identical to the Phase
13D.1 source. The visibly-disabled review and recovery affordances
continue to be visibly disabled; no mutation handler appears anywhere.
No `src/`, `pyproject.toml`, `uv.lock`, `frontend/package.json`,
`frontend/package-lock.json`, or root dependency changed. Phase 13D.2
absorbs ~80–90% of an Architecture Story narrative via embedded
checkpoints in the walkthrough, but it does **not** implement a full
standalone Architecture Story page — that stays deferred and is
recorded as a new item in `docs/frontend-gui-deferred-work-register.md`
("Standalone Architecture Story / System Boundary Reference"). Its
only `tests/` change is the narrow, explicitly authorized mechanical
advance of the state-discipline guard `tests/test_failure_mode_regression.py`
to the Phase 13D.2 current-state expectations.

Per the Phase Closure Protocol, Phase 13D.2 is an implementation
candidate, pending review, **not locked**; it does not lock Phase
13D.2, does not close Phase 13, and does not start Phase 13E. Phase
13E and every later Phase 13 subphase have **not** started — they are
future, planned work, decomposed in `docs/phase13-roadmap.md`. Phase
9C remains optional and not scheduled.

*(Every Phase 13D.1-era and earlier note below is a historical record.
Phase 13D.1 is LOCKED; Phase 13D.2 is the current implementation
candidate. The "Current state (checkpoint)" section at the end of
this file is the authoritative current-status snapshot.)*

---
# Phase 13D.1 implementation-candidate note — Static Operator GUI Refinement / Evidence & Disabled Action Discipline (historical record — Phase 13D.1 is LOCKED; see the Phase 13D.2 note above)

**Date:** 2026-05-27
**Round type:** Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline — a frontend-only refinement sub-round of the locked Phase 13D, expanding read-only operator GUI clarity before any controlled local action or mutation-boundary work.
**Status:** Historical record. This note described Phase 13D.1 while it was an implementation candidate. Phase 13D.1 has since been **LOCKED** and is the last locked phase; Phase 13D.2 is now the current implementation candidate — see the Phase 13D.2 note above and the "Current state (checkpoint)" section at the end of this file.
**Last locked phase:** Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery).
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline.
**Next action:** Submit the Phase 13D.1 artifact for GPT-5.5 review, then Gemini critique, then an explicit user decision — before locking Phase 13D.1 or starting Phase 13E.

**Phase 13D lock (recorded honestly).** Phase 13D — Operator Workflow View
Expansion (Governance / Safety, Failure / Recovery) — completed its Phase
Closure Protocol: implementation, GPT-5.5 review, and Gemini critique.
Gemini returned SAFE TO LOCK with no required edits, and the user, as final
decision-maker, locked Phase 13D. **Phase 13D is LOCKED; it is the last
locked phase.** Phase 13 — Portfolio Website / Operator GUI — remains
STARTED and is not closed.

Phase 13D.1 is the static / read-only refinement sub-round of Phase 13D. It
takes the locked Phase 13D operator GUI and strengthens it before any future
mutation-boundary work, so a reviewer can see clearly what the system
shows, what remains intentionally disabled, what evidence supports the
artifact, why the GUI is static, and what must precede any future mutation
behaviour. It standardizes the disabled future-action display across views
into a reusable typed component (`DisabledFutureActionCard` /
`DisabledFutureActionList`) that uses real `<button disabled={true}>`
elements with no `onClick` handlers and no fake mutation props; replaces
the honest Evidence / Validation placeholder with a real read-only
**Evidence / Validation** view (`EvidenceValidationView.tsx` plus its CSS
Module) that carries the mandatory **STATIC PORTFOLIO DATA — NOT A LIVE
CI/CD DASHBOARD** disclaimer, points to repository-relative evidence, and
does not fabricate runtime CI status; adds a small read-only **Data Source
/ Demo Snapshot** framing (a Demo / Active / Candidate explanatory block
inside the new Evidence view plus the existing header chip) clarifying
that Active and Candidate are **data snapshots, not deployment
environments**, and that no switching is implemented; extracts the
navigation/view-key metadata from `App.tsx` into a small typed
`frontend/src/navigation.ts` helper to keep `App.tsx` readable while
preserving plain `useState` navigation and the `inspectRun(runId)` prop-
drilled drill-down; and updates the State Preservation Bundle and the
deferred-work register.

Phase 13D.1 is static, read-only, and export-backed. It adds no server, no
live API, no `fetch`/`axios`/`localhost`/network call, no watcher, no
mutation, no authentication, no cloud deployment, and no production
hosting. It does **not** modify the backend export generator
(`src/storytime/operator_export.py`), the committed static export JSON
(`frontend/src/data/storytime-demo-export.json`), the `storytime
export-demo-ui` CLI contract, or `src/storytime/cli/app.py`; all four
protected files / contracts are byte-identical to the Phase 13D source.
The visibly-disabled review and recovery affordances continue to be
visibly disabled; no mutation handler appears anywhere. No `src/`,
`pyproject.toml`, `uv.lock`, or root dependency changed. Its only
`tests/` change is the narrow, explicitly authorized mechanical advance
of the state-discipline guard `tests/test_failure_mode_regression.py`
to the Phase 13D.1 current-state expectations.

Per the Phase Closure Protocol, Phase 13D.1 is an implementation
candidate, pending review, **not locked**; it does not lock Phase 13D.1,
does not close Phase 13, and does not start Phase 13E. Phase 13E and
every later Phase 13 subphase have **not** started — they are future,
planned work, decomposed in `docs/phase13-roadmap.md`. Phase 9C remains
optional and not scheduled.

*(Every Phase 13D-era and earlier note below is a historical record.
Phase 13D is LOCKED; Phase 13D.1 is the current implementation
candidate. The "Current state (checkpoint)" section at the end of this
file is the authoritative current-status snapshot.)*

---
# Phase 13D implementation-candidate note — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) (historical record — Phase 13D is LOCKED; see the Phase 13D.1 note above)

**Date:** 2026-05-27
**Round type:** Phase 13D — Operator Workflow View Expansion — a frontend-only round expanding two placeholder operator views against the locked Phase 13C deterministic static export.
**Status:** Historical record. This note described Phase 13D while it was an implementation candidate. Phase 13D has since been **LOCKED** and is the last locked phase; Phase 13D.1 is now the current implementation candidate — see the Phase 13D.1 note above and the "Current state (checkpoint)" section at the end of this file.
**Last locked phase:** Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment.
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13D — Operator Workflow View Expansion.
**Next action:** Submit the Phase 13D artifact for GPT-5.5 review, then Gemini critique, then an explicit user decision — before locking Phase 13D or starting Phase 13E.

**Phase 13C lock (recorded honestly).** Phase 13C — Deterministic Read-Only
Static Export / Frontend Data Alignment — completed its Phase Closure
Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini returned
SAFE TO LOCK with no required edits, and the user, as final decision-maker,
locked Phase 13C. **Phase 13C is LOCKED; it is the last locked phase.** Phase
13 — Portfolio Website / Operator GUI — remains STARTED and is not closed.

Phase 13D is the fourth subphase of Phase 13. It is a frontend-only round
that takes the locked Phase 13C deterministic static export contract and
expands two of the honest placeholder views into real read-only operator
views: **Governance / Safety** and **Failure / Recovery**. The choice and
ordering follow the Phase 13C deferred-work register's
view-expansion recommendation — these two reuse data already present in the
Phase 13C export (per-run `governance` blocks and the `failureQueue`) and
give the strongest single proof to a Solutions Engineer or hiring manager
that StoryTime is a governed, observability-native pipeline. The view-count
growth motivates Gemini's recommendation to introduce scoped styling — Phase
13D introduces **CSS Modules for the two new components only**; the existing
global `src/styles.css` continues to back the Phase 13B/13C shell.

Phase 13D adds the two new view components and their CSS Modules
(`frontend/src/components/GovernanceSafetyView.tsx` /
`GovernanceSafetyView.module.css` and
`frontend/src/components/FailureRecoveryView.tsx` /
`FailureRecoveryView.module.css`), two domain-specific view-model adapters
(`frontend/src/data/governanceAdapter.ts` and
`frontend/src/data/failureAdapter.ts`) projecting the locked export, a small
ambient TypeScript declaration enabling CSS Modules under strict mode
(`frontend/src/types/css-modules.d.ts`), App-level navigation rewiring and a
read-only "Data source · Demo Snapshot" header chip backed by the existing
`EXPORT_META` adapter export, an inspect-this-run drill-down callback into
the existing Pipeline Run Detail view (plain prop drilling, no router), and
documentation updates including the deferred-work register entry for the
future **Demo / Blue / Green Data Snapshot Switcher** concept. It
synchronizes the State Preservation Bundle.

Phase 13D is static, read-only, and export-backed. It adds no server, no
live API, no `fetch`/`axios`, no watcher, no mutation, no authentication,
no cloud deployment, and no production hosting. It does **not** modify the
backend export generator (`src/storytime/operator_export.py`), the committed
static export JSON (`frontend/src/data/storytime-demo-export.json`), or the
`storytime export-demo-ui` contract; both protected files are byte-identical
to the Phase 13C source. The recovery / review affordances are surfaced as
visibly-disabled future actions, labelled with the phase that would enable
them (Phase 13E). Its only `tests/` change is the narrow, explicitly
authorized mechanical advance of the state-discipline guard
`tests/test_failure_mode_regression.py` to the Phase 13D current-state
expectations.

Per the Phase Closure Protocol, Phase 13D is an implementation candidate,
pending review, **not locked**; it does not lock Phase 13D, does not close
Phase 13, and does not start Phase 13E. Phase 13E and every later Phase 13
subphase have **not** started — they are future, planned work, decomposed in
`docs/phase13-roadmap.md`. Phase 9C remains optional and not scheduled.

*(Every Phase 13C-era and earlier note below is a historical record. Phase
13C is LOCKED; Phase 13D is the current implementation candidate. The
"Current state (checkpoint)" section at the end of this file is the
authoritative current-status snapshot.)*

---
# Phase 13C implementation-candidate note — Deterministic Read-Only Static Export / Frontend Data Alignment (historical record — Phase 13C is LOCKED; see the Phase 13D note above)

**Date:** 2026-05-27
**Round type:** Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment — a read-only static data-boundary round.
**Status:** Historical record. This note described Phase 13C while it was an implementation candidate. Phase 13C has since been **LOCKED** and is the last locked phase; Phase 13D is now the current implementation candidate — see the Phase 13D note above and the "Current state (checkpoint)" section at the end of this file.
**Last locked phase:** Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold.
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment.
**Next action:** Submit the Phase 13C artifact for GPT-5.5 review, then Gemini critique, then an explicit user decision — before locking Phase 13C or starting Phase 13D.

**Phase 13B lock (recorded honestly).** Phase 13B — Typed Static Portfolio
Shell / Minimal Visual Pipeline Scaffold — completed its Phase Closure
Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini returned
SAFE TO LOCK with no required edits, and the user, as final decision-maker,
locked Phase 13B. **Phase 13B is LOCKED; it is the last locked phase.** Phase
13 — Portfolio Website / Operator GUI — remains STARTED and is not closed.

Phase 13C is the third subphase of Phase 13. It establishes a truthful,
reproducible data boundary between the backend and the Phase 13B frontend,
realizing the "backend owns truth, frontend owns understanding" contract: the
backend defines the export shape; the frontend mirrors it. Phase 13C adds a
small, read-only backend export module `src/storytime/operator_export.py` and a
`storytime export-demo-ui` CLI command that together produce a deterministic
static JSON export (`frontend/src/data/storytime-demo-export.json`, carrying a
top-level `schemaVersion`); it adds the contract document
`docs/frontend-static-export-contract.md`, the frontend deferred-work register
`docs/frontend-gui-deferred-work-register.md`, a frontend adapter
(`frontend/src/data/adapter.ts`), and a `StaticDemoExport` type; it adds
backend contract tests `tests/test_operator_export.py`; and it rewires the
Phase 13B homepage and Pipeline Run Detail / Stage Timeline to consume the
export through the adapter. It synchronizes the State Preservation Bundle.

Phase 13C is a static, read-only data-boundary round. The export is
deterministic — built from fixed demo data with no `datetime.now()`, no `uuid`,
no randomness; generating it twice yields byte-identical JSON. Phase 13C does
**not** make the frontend live: it adds no server, no live API, no
`fetch`/`axios`, no watcher, no backend-to-frontend runtime coupling, no
mutation, no authentication, no cloud deployment, and no production hosting.
The small backend code it adds is read-only and deterministic and changes no
core pipeline runtime behaviour, no governance, no telemetry, no CLI behaviour
beyond the new read-only command, and no root dependency. Its `tests/` changes
are the new `tests/test_operator_export.py` and the narrow, explicitly
authorized mechanical advance of the state-discipline guard
`tests/test_failure_mode_regression.py` to the Phase 13C current-state
expectations.

Per the Phase Closure Protocol, Phase 13C is an implementation candidate,
pending review, **not locked**; it does not lock Phase 13C, does not close
Phase 13, and does not start Phase 13D. Phase 13D and every later Phase 13
subphase have **not** started — they are future, planned work, decomposed in
`docs/phase13-roadmap.md`. Phase 9C remains optional and not scheduled.

*(Every Phase 13B-era, Phase 13A-era, and earlier note below is a historical
record. Phase 13B is LOCKED; Phase 13C is the current implementation
candidate. The "Current state (checkpoint)" section at the end of this file is
the authoritative current-status snapshot.)*

---
# Phase 13B implementation-candidate note — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold (historical record — Phase 13B is LOCKED; see the Phase 13C note above)

**Date:** 2026-05-27
**Round type:** Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — first frontend implementation round of Phase 13 (a bounded frontend scaffold).
**Status:** Historical record. This note described Phase 13B while it was an implementation candidate. Phase 13B has since been **LOCKED** and is the last locked phase; Phase 13C is now the current implementation candidate — see the Phase 13C note above and the "Current state (checkpoint)" section at the end of this file.
**Last locked phase:** Phase 13A — Portfolio Website / Operator GUI Architecture Baseline.
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold.
**Next action:** Submit the Phase 13B artifact for GPT-5.5 review, then Gemini critique, then an explicit user decision — before locking Phase 13B or starting Phase 13C.

**Phase 13A lock (recorded honestly).** Phase 13A — Portfolio Website /
Operator GUI Architecture Baseline — completed its Phase Closure Protocol:
implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO
LOCK with no required edits, and the user, as final decision-maker, locked
Phase 13A. **Phase 13A is LOCKED; it is the last locked phase.** Its five
architecture documents are now the authoritative Phase 13 plan. Phase 13 —
Portfolio Website / Operator GUI — remains STARTED and is not closed.

Phase 13B is the second subphase of Phase 13 and the first round in which
frontend code is written. It implements, against the Phase 13A contract, a
deliberately bounded frontend: a typed static portfolio shell plus one
visual operator view. It adds a new top-level `frontend/` directory — a React
+ TypeScript + Vite project (strict TypeScript; standard CSS; no external UI,
component, state, or charting library) — containing the frontend read-model
contract (`frontend/src/types/storytime.ts`), a static demo dataset of exactly
two mock pipeline runs (`frontend/src/data/storytime-demo-data.ts`), the
portfolio homepage, one Pipeline Run Detail view with a visual Stage Timeline,
honest placeholders for the future portfolio sections and operator views, and
a frontend README. It lightly updates `README.md` and synchronizes the State
Preservation Bundle.

Phase 13B is a static, read-only, demo-data-backed shell. It is **not**
backend-connected, does **not** use live or runtime data, does **not**
implement mutations (retry, re-run, and review-decision actions appear only as
visibly-disabled affordances), and is **not** production-hosted or
cloud-deployed. It contacts no backend: there is no `fetch()`, no `axios`, and
no network call — every screen is backed by the static demo dataset. It
changed no pipeline behaviour, `storytime rerun`, Trust Envelope enforcement,
API, CLI, telemetry, Docker behaviour, `pyproject.toml`, `uv.lock`, or `src/`
content; the backend is untouched. Its only `tests/` change is the narrow,
explicitly authorized mechanical advance of the state-discipline guard
`tests/test_failure_mode_regression.py` to the Phase 13B current-state
expectations (it now tracks Phase 13B as the current implementation candidate,
with Phase 13A recorded as the last locked phase; it guards against a premature
Phase 13B lock, a premature Phase 13 closure, and a premature Phase 13C start;
its append-only lock-record checks now also require the Phase 13A record; and
its frontend-claim guard is replaced by a no-overclaim guard, since Phase 13B
legitimately builds a frontend but must not be described as backend-connected,
live-data-powered, mutation-capable, or production / cloud hosted).

Per the Phase Closure Protocol, Phase 13B is an implementation candidate,
pending review, **not locked**; it does not lock Phase 13B, does not close
Phase 13, and does not start Phase 13C. Phase 13C and every later Phase 13
subphase have **not** started — they are future, planned work only, decomposed
in `docs/phase13-roadmap.md`. Phase 9C remains optional and not scheduled.

*(Every Phase 13A-era, Phase 12D-era, and Phase 12C-era note below — and the
Phase 12B-era, Phase 12A.1, Phase 12A, Phase 11x, and Phase 10x notes further
below — are historical records. Phase 13A is LOCKED; Phase 13B is the current
implementation candidate. The "Current state (checkpoint)" section at the end
of this file is the authoritative current-status snapshot.)*

---
# Phase 13A implementation-candidate note — Portfolio Website / Operator GUI Architecture Baseline (historical record — Phase 13A is LOCKED; see the Phase 13B note above)

**Date:** 2026-05-27
**Round type:** Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — documentation-only architecture-baseline round (documentation only).
**Status:** Historical record. This note described Phase 13A while it was an implementation candidate. Phase 13A has since been **LOCKED** and is the last locked phase; Phase 13B is now the current implementation candidate — see the Phase 13B note above and the "Current state (checkpoint)" section at the end of this file.
**Last locked phase:** Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition.
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13A — Portfolio Website / Operator GUI Architecture Baseline.
**Next action:** Submit the Phase 13A artifact for GPT-5.5 review, then Gemini critique, then an explicit user decision — before locking Phase 13A or starting Phase 13B.

**Phase 12D lock and Phase 12 closure (recorded honestly).** Phase 12D — Phase
12 Closure Plan / Final Portfolio Handoff Definition — completed its Phase
Closure Protocol out-of-band: implementation, GPT-5.5 review, and Gemini
critique. Gemini returned the verdict to lock Phase 12D and close Phase 12,
with no critical findings, no non-blocking findings, and no required edits;
the user, as final decision-maker, then locked Phase 12D and formally closed
Phase 12. That out-of-band lock-and-closure was a user/mediator decision
supplied to the Phase 13A round and recorded — not re-reviewed — by it.
**Phase 12D is LOCKED; it is the last locked phase. Phase 12 — Portfolio / SE
Demo Packaging — is CLOSED** (Phase 12A through 12D all locked). The locked
Phase 12D artifact is
`storytime-phase12d-phase12-closure-plan-final-portfolio-handoff.tar.gz`
(SHA-256 `64ad09e875f0653608e0deb756f11ee5adc0d2ff1265e2039cbc51491f286cf8`).
Phase 12E was optional, contingency-only work that existed only if the Phase
12D review found a substantive gap; the review found none, so Phase 12E was
not needed and never started.

Phase 13 — Portfolio Website / Operator GUI — is the phase that follows the
closed Phase 12. It is the project track that designs, and in later subphases
will build, a portfolio-facing website and a decoupled operator GUI. **Phase
13 is STARTED.** Phase 13A is its first subphase: a documentation-only
architecture-baseline round. Phase 13A refines, supersedes, and makes
authoritative the earlier sketch in `docs/GUI_vision.md` (which named a Phase
13 "Operator GUI / Decoupled Frontend Vision" with a planned 13A–13F
decomposition); `docs/GUI_vision.md` is left unchanged as the original
verbatim vision capture, and the Phase 13 documents added by this round are
now authoritative for the Phase 13 plan.

Phase 13A adds five `docs/` documents and changes nothing else of substance:
`phase13-portfolio-website-architecture.md` (the Phase 13 purpose, the
end-state website and operator-GUI vision, audiences and review paths, the
website and operator information architectures, the local-first and
future-cloud compatibility rules, and the Phase 13 success criteria),
`frontend-backend-contract.md` (the "backend owns truth, frontend owns
understanding" data contract — the read-model categories, the future action
categories, the actions explicitly disabled in Phase 13A, and the candidate
data-source options), `phase13-roadmap.md` (the Phase 13A–13G subphase
decomposition, each subphase's objective, allowed scope, forbidden scope,
acceptance criteria, and review gate), `portfolio-website-content-model.md`
(the website section inventory, each section mapped to existing repository
source documents, and a content-honesty checklist), and
`operator-gui-view-model.md` (the operator-GUI view inventory, the disabled
and future actions, the empty / error / loading states, and the accessibility
and readability requirements). It also synchronizes the State Preservation
Bundle.

Phase 13A is a planning and architecture-definition round only. It does **not**
implement the portfolio website and does **not** implement the operator GUI:
it adds no React, Vite, TypeScript, JavaScript, CSS, HTML application code, no
`frontend/`, `web/`, or `app/` directory, no `package.json` or `vite.config`,
no UI, no server, no generated audio, no screenshots or binary assets, and no
new dependency, and it changed no pipeline behaviour, `storytime rerun`, Trust
Envelope enforcement, API, CLI, telemetry, `pyproject.toml`, `uv.lock`, or
`src/` content. Its only `tests/` change is the narrow, explicitly authorized
mechanical advance of the state-discipline guard
`tests/test_failure_mode_regression.py` to the Phase 13A current-state
expectations (it now tracks Phase 13A as the current implementation candidate,
with Phase 12D recorded as the last locked phase; it guards against a
premature Phase 13A lock, a premature Phase 13 closure, and a premature Phase
13B start, and adds a new frontend-claim guard that the current-state docs do
not assert that the frontend or the operator GUI was implemented in Phase
13A).

Per the Phase Closure Protocol, Phase 13A is an implementation candidate,
pending review, **not locked**; it does not lock Phase 13A, does not close
Phase 13, and does not start Phase 13B. Phase 13B and every later Phase 13
subphase have **not** started — they are future, planned work only, decomposed
in `docs/phase13-roadmap.md`. Phase 9C remains optional and not scheduled.

*(Every Phase 12D-era and Phase 12C-era note below — and the Phase 12B-era,
Phase 12A.1, Phase 12A, Phase 11x, and Phase 10x notes further below — are
historical records. Phase 12D is LOCKED and Phase 12 is CLOSED; Phase 13A is
the current implementation candidate. The "Current state (checkpoint)" section
at the end of this file is the authoritative current-status snapshot.)*

---
# Phase 12D implementation-candidate note — Phase 12 Closure Plan / Final Portfolio Handoff Definition (historical record — Phase 12D is LOCKED and Phase 12 is CLOSED; see the Phase 13A note above)

**Date:** 2026-05-26
**Round type:** Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — documentation-only closure-definition round (documentation only).
**Status:** Historical record. This note described Phase 12D while it was an implementation candidate. Phase 12D has since been **LOCKED** and is the last locked phase, and **Phase 12 — Portfolio / SE Demo Packaging — has been CLOSED**; Phase 13 is now STARTED and Phase 13A is the current implementation candidate — see the Phase 13A note above and the "Current state (checkpoint)" section at the end of this file.
**Last locked phase:** Phase 12C — Portfolio Demo Narrative / Public Presentation Kit.
**Current phase:** Phase 12 — Portfolio / SE Demo Packaging — STARTED. **Current subphase** — Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition.
**Next action:** Submit the Phase 12D artifact for GPT-5.5 review, then Gemini critique, then an explicit user decision — before locking Phase 12D or closing Phase 12.

**Phase 12C lock (recorded honestly).** Phase 12C — Portfolio Demo Narrative /
Public Presentation Kit — completed its Phase Closure Protocol: implementation,
GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no
critical findings, no non-blocking findings, and no required edits, and the
user, as final decision-maker, locked Phase 12C. **Phase 12C is LOCKED; it is
the last locked phase.** Phase 12 — Portfolio / SE Demo Packaging — remains
STARTED and is not closed.

Phase 12D is the fourth subphase of Phase 12 — Portfolio / SE Demo Packaging. It
is a documentation-only closure-definition round: it defines what it means to
close Phase 12, records the final portfolio asset inventory, and prepares the
Phase 12 closure decision — it does **not** itself close Phase 12. It adds three
`docs/` documents — `phase12-closure-plan.md` (the Phase 12 closure criteria,
the Phase 12A–12C asset inventory, the closure-readiness checklist, the
remaining-gaps / no-go criteria, the close-after-12D vs bounded-cleanup vs
separate-12E recommendation, and the Phase 13 boundary statement),
`final-portfolio-handoff.md` (a cold-reader handoff with current-state
snapshot, tiered reviewer paths, a suggested demo flow, an evidence map,
explicit limitations, and the next-phase boundary), and
`phase12-final-review-checklist.md` (the checklist a reviewer uses at the
Phase 12D / Phase 12 closure gate) — and synchronizes the State Preservation
Bundle. Phase 12D added no product feature, UI, server, JavaScript, frontend
directory, generated audio, screenshots/binary assets, demo video, or new
dependency, and changed no pipeline behaviour, `storytime rerun`, Trust
Envelope enforcement, API, CLI, telemetry, or `pyproject.toml` / `uv.lock` /
`src/` content; its only `tests/` change is the narrow, explicitly authorized
mechanical advance of the state-discipline guard
`tests/test_failure_mode_regression.py` to the Phase 12D current-state
expectations (it now guards against a premature Phase 12D lock, a premature
Phase 12 closure, and a premature Phase 12E-or-later start, and additionally
requires the Phase 12C lock record). Per the Phase Closure Protocol, Phase 12D
is an implementation candidate, pending review, **not locked**; it does not
lock Phase 12D, does not close Phase 12, and does not start Phase 12E. Phase 12E
is optional, future, contingency-only work — it exists only if the Phase 12D
review finds a substantive gap — and has **not** started. Phase 13 — Operator
GUI / Decoupled Frontend Vision — is roadmap-preserved only (see
`docs/GUI_vision.md` and the `docs/roadmap.md` Phase 13 note) and has **not**
started.

*(Every Phase 12C-era and Phase 12B-era note below — and the Phase 12A.1,
Phase 12A, Phase 11x, and Phase 10x notes further below — are historical
records. Phase 12D is LOCKED and Phase 12 is CLOSED; Phase 13A is the current
implementation candidate. The "Current state (checkpoint)" section at the end
of this file is the authoritative current-status snapshot.)*

---

# Phase 12C implementation-candidate note — Portfolio Demo Narrative / Public Presentation Kit (historical record — Phase 12C is LOCKED; see the Phase 12D note above)

**Date:** 2026-05-26
**Round type:** Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — documentation-first portfolio packaging (documentation only).
**Status:** Historical record. This note described Phase 12C while it was an implementation candidate. Phase 12C has since been **LOCKED** and is the last locked phase; Phase 12D is now the current implementation candidate — see the Phase 12D note above and the "Current state (checkpoint)" section at the end of this file.
**Last locked phase:** Phase 12B — Portfolio Evidence Pack / Reviewer Assets.
**Current phase:** Phase 12 — Portfolio / SE Demo Packaging — STARTED. **Current subphase** — Phase 12C — Portfolio Demo Narrative / Public Presentation Kit.
**Next action:** Submit the Phase 12C artifact for GPT-5.5 review, then Gemini critique, then explicit user lock — before locking Phase 12C or starting Phase 12D.

**Phase 12B lock (recorded honestly).** Phase 12B — Portfolio Evidence Pack /
Reviewer Assets — completed its Phase Closure Protocol: after the Phase 12B.1
state-hygiene cleanup, the Phase 12B.2 Phase 13 GUI roadmap-preservation
cleanup, and the Phase 12B.3 residual living-doc state-wording cleanup
sub-rounds, Gemini reviewed the combined Phase 12B sequence and returned SAFE
TO LOCK with no required edits, and the user, as final decision-maker, locked
Phase 12B. Phase 12B.1 / 12B.2 / 12B.3 are folded into the Phase 12B lock
lineage as accepted cleanup sub-rounds — they are not independently locked
phases. **Phase 12B is LOCKED; it is the last locked phase.** Phase 12 —
Portfolio / SE Demo Packaging — remains STARTED and is not closed.

Phase 12C is the third subphase of Phase 12 — Portfolio / SE Demo Packaging. It
is a documentation-first portfolio-packaging round: it converts the project's
existing technical evidence into polished, reusable public-presentation
assets. It adds four `docs/` documents — `portfolio-demo-narrative.md` (a
concise demo narrative), `demo-talk-track.md` (a 5/10/20-minute spoken
walkthrough), `interview-story-bank.md` (reusable interview answer frames),
and `public-repository-readiness.md` (a public-viewing readiness checklist) —
lightly updates `README.md` to point reviewers to them, and synchronizes the
State Preservation Bundle. Phase 12C added no product feature, UI, server,
JavaScript, frontend directory, generated audio, screenshots/binary assets,
demo video, or new dependency, and changed no pipeline behaviour,
`storytime rerun`, Trust Envelope enforcement, API, CLI, telemetry, or
`pyproject.toml` / `uv.lock` / `src/` content; its only `tests/` change is the
narrow, explicitly authorized mechanical advance of the state-discipline guard
`tests/test_failure_mode_regression.py` to the Phase 12C current-state
expectations (it now guards against a premature Phase 12C lock, a premature
Phase 12 closure, and a premature Phase 12D-or-later start, and additionally
requires the Phase 12B lock record). Per the Phase Closure Protocol, Phase 12C
is an implementation candidate, pending review, **not locked**; it does not
lock Phase 12C, does not close Phase 12, and does not start Phase 12D. Phase 12D
and later subphases have not started. Phase 13 — Operator GUI / Decoupled
Frontend Vision — is roadmap-preserved only (see `docs/GUI_vision.md` and the
`docs/roadmap.md` Phase 13 note) and has **not** started.

*(Every Phase 12B-era note below — the Phase 12B.3, 12B.2, 12B.1, and Phase 12B
notes — and the Phase 12A.1, Phase 12A, Phase 11x, and Phase 10x notes further
below, are historical records. Phase 12B is LOCKED; Phase 12C is the current
implementation candidate. The "Current state (checkpoint)" section at the end
of this file is the authoritative current-status snapshot.)*

---

# Phase 12B.3 residual living-doc state-wording cleanup note — Portfolio Evidence Pack / Reviewer Assets (bounded cleanup, NOT A LOCK — historical record)

**Round type:** residual state-hygiene cleanup of living/cold-session documents after Phase 12B.2.
**Status:** Historical record. This was a documentation-only cleanup sub-round of the Phase 12B round; it is **not a lock**. Phase 12B has since been **LOCKED** (with Phase 12B.1 / 12B.2 / 12B.3 folded into its lock lineage), and Phase 12C is now the current implementation candidate — see the Phase 12C note above.

Phase 12B.3 removes remaining stale present-tense historical wording that described Phase 12A as the current implementation candidate inside older Phase 11 notes. Those passages now explicitly point readers to the active Phase 12B / Phase 12B.2 current-state notes at the top of each living document. This preserves historical records without allowing cold sessions to misread superseded Phase 11-era notes as current state.

No product behavior, source code, tests, dependencies, lockfiles, frontend implementation, GUI implementation, runtime assets, generated audio, server/UI behavior, or Phase 13 implementation is authorized or changed by this cleanup.

Current state remains: **Phase 12A is LOCKED**; **Phase 12B, Phase 12B.1, Phase 12B.2, and Phase 12B.3 are cleanup/implementation-candidate lineage pending Gemini review and formal user lock**; **Phase 12C and later are NOT STARTED**; **Phase 13 is roadmap-preserved only and NOT STARTED**.

# Phase 12B.2 roadmap-preservation cleanup note — Portfolio Evidence Pack / Reviewer Assets (historical record — Phase 12B is LOCKED; see the Phase 12C note above)

**Date:** 2026-05-26
**Round type:** bounded roadmap-preservation cleanup of the Phase 12B round (documentation only).
**Status:** Phase 12B — Portfolio Evidence Pack / Reviewer Assets — **remains the current implementation candidate: pending review, NOT locked.** Phase 12B.2 changes no phase status.

Phase 12B.2 is a narrow roadmap-preservation cleanup. It preserves a future
Operator GUI / Decoupled Frontend vision inside the repository so a cold LLM
session can see it, without starting that work and without changing Phase
12B's implementation-candidate status. It adds one new documentation file,
`docs/GUI_vision.md`, recording the user's GUI requirement and the
architecture interpretation; adds a Phase 13 roadmap note to the body of
`docs/roadmap.md` describing a future Phase 13 — Operator GUI / Decoupled
Frontend Vision — and its planned 13A–13F decomposition; and adds this
current-state round note to the top of `LLM_DIRECTOR.md`,
`docs/handoff-state.md`, and `docs/roadmap.md`.

Phase 13 is roadmap-preserved as a future GUI track only. **Phase 13 has NOT
started.** No GUI is implemented; this round adds no React, Vite, TypeScript,
frontend directory, dependency, package file, or UI code, and this note does
not authorize Phase 13 implementation. Phase 12B.2 changed no `src/`, no
`tests/`, no `pyproject.toml`, no `uv.lock`, no dependency, no product or
runtime behaviour, and no append-only locked decision; it preserves all
historical chronology.

Current state is unambiguous: **Phase 12A — Portfolio / SE Demo Packaging
Baseline — is LOCKED** (the accepted Phase 12A.1 cleanup sub-round is folded
into its lock lineage; Phase 12A.1 is not an independently locked phase);
**Phase 12B — Portfolio Evidence Pack / Reviewer Assets — is the current
implementation candidate, pending review, NOT locked**; Phase 12B.1 and Phase
12B.2 are bounded documentation cleanup sub-rounds of the Phase 12B round and
are not locks; **Phase 12 — Portfolio / SE Demo Packaging — is STARTED** and
not closed; Phase 12C and later subphases have not started; Phase 13 —
Operator GUI / Decoupled Frontend Vision — is preserved as future work and has
not started.

*(The Phase 12B implementation-candidate note below records the Phase 12B
round in full and remains the current implementation-candidate round. The
Phase 12B.1, Phase 12A.1, and Phase 12A notes, and the notes further below,
are historical records.)*

---

# Phase 12B.1 state-hygiene cleanup note — Portfolio Evidence Pack / Reviewer Assets (historical record — Phase 12B is LOCKED; see the Phase 12C note above)

**Date:** 2026-05-26
**Round type:** bounded state-hygiene cleanup of the Phase 12B round (documentation only).
**Status:** Phase 12B — Portfolio Evidence Pack / Reviewer Assets — **remains the current implementation candidate: pending review, NOT locked.** Phase 12B.1 changes no phase status.

Phase 12B.1 is a narrow state-hygiene cleanup. A pre-Gemini-review check of the
Phase 12B artifact found that some historical notes inside the living /
current-state documents still carried stale Phase 12A.1-era present-tense
wording — for example "Phase 12A remains an implementation candidate pending
review", "Phase 11D remains the last locked phase", "Phase 12B and later
subphases have not started", and parentheticals calling Phase 12A "the current
implementation candidate". The authoritative top-of-file current-state entries
(the Phase 12B notes) were already correct; the stale phrasing sat only inside
older point-in-time notes and could mislead a cold session.

Phase 12B.1 revised those historical notes so they read explicitly as
superseded point-in-time records, and added supersession notes to the
historical entries in `docs/artifact-manifest.md` and `docs/verification-log.md`
rather than rewriting those append-only-style entries. It edited only
historical-note wording in `LLM_DIRECTOR.md`, `README.md`,
`docs/handoff-state.md`, and `docs/roadmap.md`, added supersession notes to
`docs/artifact-manifest.md` and `docs/verification-log.md`, fixed one stale
parenthetical in `docs/open-issues.md`, and appended a round record to
`docs/phase-history.md`, `docs/verification-log.md`, and
`docs/artifact-manifest.md`. It changed no `src/`, no `tests/`, no
`pyproject.toml`, no `uv.lock`, no dependency, no product or runtime behaviour,
and no append-only locked decision; it preserves all historical chronology.

Current state is unambiguous: **Phase 12A — Portfolio / SE Demo Packaging
Baseline — is LOCKED** (the accepted Phase 12A.1 cleanup sub-round is folded
into its lock lineage; Phase 12A.1 is not an independently locked phase);
**Phase 12B — Portfolio Evidence Pack / Reviewer Assets — is the current
implementation candidate, pending review, NOT locked**; **Phase 12 — Portfolio
/ SE Demo Packaging — is STARTED** and not closed; Phase 12C and later
subphases have not started.

*(The Phase 12B implementation-candidate note below records the Phase 12B round
in full and remains the current implementation-candidate round. The Phase
12A.1 and Phase 12A notes, and the notes further below, are historical
records.)*

---

# Phase 12B implementation-candidate note — Portfolio Evidence Pack / Reviewer Assets (historical record — Phase 12B is LOCKED; see the Phase 12C note above)

**Date:** 2026-05-26
**Candidate artifact:** `storytime-phase12b-portfolio-evidence-pack-reviewer-assets.tar.gz` (SHA-256 reported on delivery).
**Source artifact:** `storytime-phase12a1-state-hygiene-cleanup.tar.gz` (SHA-256 `5f9eca1cc8c2efb55d57f87becdc53cd0d8e514221947e445965232f608b621a`).
**Status:** Phase 12B — Portfolio Evidence Pack / Reviewer Assets is an **implementation candidate / pending review — NOT locked**.
**Last locked phase:** Phase 12A — Portfolio / SE Demo Packaging Baseline.
**Current phase:** Phase 12 — Portfolio / SE Demo Packaging — STARTED. **Current subphase** — Phase 12B — Portfolio Evidence Pack / Reviewer Assets.
**Next action:** Submit the Phase 12B artifact for GPT-5.5 review, then Gemini critique, then explicit user lock — before locking Phase 12B or starting Phase 12C.

**Phase 12A lock (recorded honestly).** Phase 12A — Portfolio / SE Demo
Packaging Baseline — completed its Phase Closure Protocol: after the Phase 12A.1
state-hygiene cleanup sub-round was accepted, the user, as final
decision-maker, locked Phase 12A. Phase 12A.1 is folded into the Phase 12A lock
lineage as an accepted cleanup sub-round — not an independently locked phase.
**Phase 12A is LOCKED; it is the last locked phase.** Phase 12 — Portfolio / SE
Demo Packaging — remains STARTED and is not closed.

Phase 12B is the second subphase of Phase 12 — Portfolio / SE Demo Packaging. It
is a reviewer / evidence packaging round: it adds four `docs/` documents that
let a reviewer find and verify the evidence behind StoryTime's portfolio
claims — `portfolio-evidence-index.md` (a claim-to-evidence index),
`se-interview-evidence-matrix.md` (a Solutions-Engineer competency-to-evidence
matrix), `demo-reviewer-checklist.md` (a reviewer wrapper over `docs/demo.md`,
not a duplicate command script), and `portfolio-public-copy.md` (disciplined,
non-hype public-facing copy) — lightly updates `README.md` to point reviewers
to the new evidence documents, and synchronizes the State Preservation Bundle.

Phase 12B added no product feature, no UI, no server, no JavaScript, no
generated audio, no screenshots/binary assets, and no new dependency; it
changed no pipeline behaviour, `storytime rerun`, or Trust Envelope
enforcement, and changed no `pyproject.toml`, `uv.lock`, or `src/` content. The
only `tests/` change is the narrow, explicitly authorized §5 mechanical advance
of the state-discipline guard `tests/test_failure_mode_regression.py` so it
tracks the Phase 12B current-state expectations: `_CURRENT_PHASE` advanced to
"phase 12b", `_LAST_LOCKED_PHASE` advanced to "phase 12a", and
`_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 12B lock, a
premature Phase 12 closure, and a premature Phase 12C-or-later start. The guard
is strengthened, not weakened — it now also requires the Phase 12A lock record
in the append-only history.

Per the Phase Closure Protocol, Phase 12B is implementation output, **not** a
locked phase: it is not lock-ready until GPT-5.5 review, Gemini critique, any
cleanup, and explicit user approval complete. Phase 12C and later subphases of
Phase 12 have **not** started.

*(This Phase 12B note records the current implementation candidate. The Phase
12A.1 and Phase 12A notes below — now historical records, since Phase 12A is
locked — and the Phase 11D, Phase 11C, Phase 11B, Phase 11A, and Phase 10G
notes further below are historical records. Phase 10 and Phase 11 are CLOSED;
Phase 12A is LOCKED.)*

---

# Phase 12A.1 state-hygiene cleanup note — Portfolio / SE Demo Packaging Baseline (folded into the Phase 12A lock — historical record)

**Date:** 2026-05-26
**Round type:** bounded state-hygiene cleanup of the Phase 12A round (documentation only).
**Status:** Historical record. Phase 12A — Portfolio / SE Demo Packaging Baseline — has since been **LOCKED**; the Phase 12A.1 cleanup is folded into the Phase 12A lock lineage as an accepted sub-round. Current status is in the Phase 12B note above.

Phase 12A.1 is a narrow state-hygiene cleanup. A pre-lock review of the Phase 12A
artifact found that some historical notes inside the living / current-state
documents still carried stale present-tense phrasing — for example describing
Phase 11A, Phase 11B, or Phase 11C as "the last locked phase", or pointing the
reader to a superseded "Phase 11D note above" / "Phase 11C note above" for
current status. The authoritative top-of-file current-state entries were already
correct; the stale phrasing sat only inside older point-in-time notes and could
mislead a cold session.

Phase 12A.1 revises those historical notes so they read explicitly as superseded
point-in-time records: stale "is the last locked phase" wording becomes "was the
last locked phase at that point in the project history", and stale "current
status is in the Phase 11x note above" pointers now point to the Phase 12A
current-state note. It edits only the historical-note wording in `LLM_DIRECTOR.md`,
`README.md`, `docs/handoff-state.md`, and `docs/roadmap.md`, and appends a round
record to `docs/phase-history.md`, `docs/verification-log.md`, and
`docs/artifact-manifest.md`. It changed no `src/`, no `tests/`, no
`pyproject.toml`, no `uv.lock`, no dependency, no product or runtime behaviour,
and no append-only locked decision; it preserves all historical chronology.

At the time of the Phase 12A.1 round, Phase 12A was an implementation candidate
pending review under the Phase Closure Protocol, and Phase 12A.1 was a sub-round
cleanup — not a new phase and not a lock. **That point-in-time status is now
superseded: Phase 12A — with the accepted Phase 12A.1 cleanup sub-round folded
into its lock lineage — is LOCKED, and is the last locked phase.** Phase 11 —
Release Candidate Hardening — is CLOSED and Phase 12 — Portfolio / SE Demo
Packaging — is STARTED; the current implementation candidate is now Phase 12B —
Portfolio Evidence Pack / Reviewer Assets. Current status is in the Phase 12B
note above.

*(This Phase 12A.1 note is a superseded point-in-time record. The Phase 12A
note below is likewise a historical record — Phase 12A is locked — and the
notes further below are historical records. The current implementation
candidate, pending review and not locked, is Phase 12B; see the Phase 12B note
above.)*

---

# Phase 12A note — Portfolio / SE Demo Packaging Baseline (locked — historical record) — Phase 11 CLOSED

**Date:** 2026-05-26
**Candidate artifact:** `storytime-phase12a-portfolio-se-demo-packaging-baseline.tar.gz` (SHA-256 reported on delivery).
**Source artifact:** `storytime-phase11d-release-candidate-evidence-pack.tar.gz` (SHA-256 `07a3973e3dbb69d760ff2c330418f85101c2afa1464fc0eed752fc7053894d94`).
**Status:** Phase 12A — Portfolio / SE Demo Packaging Baseline is **LOCKED / ACCEPTED / CANONICAL** (locked after the accepted Phase 12A.1 state-hygiene cleanup sub-round; Phase 12A.1 is folded into this lock lineage). *(This note was originally written when Phase 12A was an implementation candidate; it has since been locked. Current status is in the Phase 12B note above.)*
**Last locked phase:** Phase 12A — Portfolio / SE Demo Packaging Baseline (this phase).
**Current phase:** *(superseded — see the Phase 12B note above.)*
**Next action:** *(superseded — see the Phase 12B note above.)*

**Out-of-band Phase 11 closure (recorded honestly).** Before Phase 12A, the
Phase 11D — Release Candidate Evidence Pack artifact completed its Phase Closure
Protocol out-of-band in the GPT/Gemini review workflow: GPT-5.5 review PASS;
Gemini review SAFE TO LOCK; no required edits. The user, as final
decision-maker, then (1) locked Phase 11D — Release Candidate Evidence Pack, and
(2) formally closed Phase 11 — Release Candidate Hardening, and (3) authorized
Phase 12 — Portfolio / SE Demo Packaging, with Phase 12A as its first
implementation candidate. **Phase 11D is locked; Phase 11 is CLOSED; Phase 12 is
STARTED.** This closure decision was supplied to the Phase 12A round by the
user/mediator; it was not contained in the uploaded Phase 11D archive, which
captured the pre-lock implementation-candidate state. The Phase 12A round
records that decision into the State Preservation Bundle — it does not
re-perform the review.

Phase 12A is the first subphase of Phase 12 — Portfolio / SE Demo Packaging. It
is documentation and portfolio-packaging only: it makes StoryTime explainable as
a Solutions Engineer / observability / OpenTelemetry portfolio project without
adding any product feature or changing any runtime behaviour. It adds four
`docs/` documents — `portfolio-overview.md` (the plain-English portfolio
overview), `solutions-engineer-narrative.md` (interview / SE framings),
`portfolio-demo-script.md` (a reviewer-facing demo walkthrough), and
`interview-talking-points.md` (concise study points) — refines `README.md` for a
portfolio-facing reviewer, and synchronizes the State Preservation Bundle.

Phase 12A added no product feature, no UI, no server, no JavaScript, no
generated audio, no screenshots/binary assets, and no new dependency; it changed
no pipeline behaviour, `storytime rerun`, or Trust Envelope enforcement, and
changed no `pyproject.toml`, `uv.lock`, or `src/` content. The only `tests/`
change is a narrow, explicitly authorized advance of the state-discipline guard
`tests/test_failure_mode_regression.py` so it tracks the Phase 12A current-state
expectations: the guard now protects against a premature Phase 12A lock, a
premature Phase 12 closure, and a premature Phase 12B-or-later start, and it
strengthens — does not weaken — the historical lock-record coverage.

Per the Phase Closure Protocol, Phase 12A is implementation output, **not** a
locked phase: it is not lock-ready until GPT-5.5 review, Gemini critique, any
cleanup, and explicit user approval complete. Phase 12B and later subphases of
Phase 12 have **not** started.

*(This Phase 12A note records the current implementation candidate. The
Phase 11D note below — now a historical record, since Phase 11D is locked and
Phase 11 is closed — and the Phase 11C, Phase 11B, Phase 11A, and Phase 10G
notes further below are historical records. Phase 10 and Phase 11 are both
CLOSED.)*

---

# Phase 11D note — Release Candidate Evidence Pack (locked — historical record) — Phase 11 CLOSED

**Date:** 2026-05-25
**Candidate artifact:** `storytime-phase11d-release-candidate-evidence-pack.tar.gz` (SHA-256 reported on delivery).
**Source artifact:** `storytime-phase11c-failure-mode-regression-hardening.tar.gz` (SHA-256 `2dd31442e62c13241a64d10c2d117aefedc3b9c633ad5ea5d1fa94cfaad7d57b`).
**Status:** Phase 11D — Release Candidate Evidence Pack is **LOCKED / ACCEPTED / CANONICAL**. With Phase 11D locked, **Phase 11 — Release Candidate Hardening — is CLOSED**. *(This note was originally written when Phase 11D was an implementation candidate; Phase 11D was subsequently locked out-of-band under the Phase Closure Protocol and Phase 11 was formally closed. Current status is in the Phase 12B note above.)*
**Previous locked phase:** Phase 11C — Failure-Mode / Regression Hardening.
**Current phase:** *(superseded — see the Phase 12B note above.)*
**Next action:** *(superseded — see the Phase 12B note above.)*

Phase 11D is the fourth and final planned Release Candidate Hardening subphase.
It is an evidence, closure-readiness, and proof-consolidation round: it answers
the release-candidate question "can we prove this release candidate is ready to
show, explain, hand off, and package?". It consolidates the release-candidate
evidence produced by Phases 11A, 11B, and 11C into a reviewer-facing index,
records the canonical validation results, prepares a Phase 11 closure
checklist, and writes a Phase 12 readiness handoff. It added four `docs/`
documents — `release-candidate-evidence-pack.md` (the overview and the
release-candidate evidence index), `final-validation-summary.md` (the canonical
validation results), `phase11-closure-checklist.md` (what each Phase 11
subphase contributed and the conditions for an explicit Phase 11 closure
decision), and `phase12-readiness-handoff.md` (what Phase 12 may safely do) —
refreshed the status notes in `docs/phase11-plan.md`,
`docs/release-candidate-hardening.md`, and `docs/rc-validation-checklist.md`,
and synchronized the State Preservation Bundle.

Phase 11D added no product feature, no UI, no server, no JavaScript, no
generated audio, no screenshots/binary assets, no new dependency, and no
database schema change; it changed no pipeline behaviour, `storytime rerun`, or
Trust Envelope enforcement, and changed no `pyproject.toml`, `uv.lock`, `src/`,
or `tests/` content. It is documentation/evidence consolidation only — no test
was added and no test was modified.

Per the Phase Closure Protocol, Phase 11D was implementation output until
GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval
completed; it has since been locked out-of-band. With Phase 11D locked,
**Phase 11 — Release Candidate Hardening — is CLOSED**. Phase 11D did not by
itself close Phase 11 or start Phase 12 — the user made the explicit Phase 11
closure decision and authorized Phase 12.

*(This Phase 11D note is a historical record — Phase 11D is locked and Phase 11
is closed. The Phase 12B note above records the current implementation
candidate. The Phase 11C note below is a historical record; Phase 11C is also
locked. The Phase 11A and Phase 10G notes further below are historical records;
Phase 10 is CLOSED.)*

---

# Phase 11C note — Failure-Mode / Regression Hardening (locked — historical record)

**Date:** 2026-05-25
**Candidate artifact:** `storytime-phase11c-failure-mode-regression-hardening.tar.gz` (SHA-256 reported on delivery).
**Source artifact:** `storytime-phase11b-fresh-clone-operator-reproducibility.tar.gz` (SHA-256 `08b72f2833da9adf3b8acc1f3170334eb7c5f998e19263838efbce2f571cc73f`).
**Status:** Phase 11C — Failure-Mode / Regression Hardening is **LOCKED / ACCEPTED / CANONICAL** — it was the last locked phase at that point in the project history. *(This is a superseded point-in-time record, originally written when Phase 11C was an implementation candidate; it was subsequently locked under the Phase Closure Protocol, and is the source/base artifact for Phase 11D. Current status is in the Phase 12B note above.)*
**Previous locked phase:** Phase 11B — Fresh Clone / Operator Reproducibility.
**Next action:** *(superseded — see the Phase 12B note above.)*

Phase 11C is the third Release Candidate Hardening subphase. It is a
failure-mode and regression-hardening round: it answers the release-candidate
question "what breaks, how do we know, and can we prove the system fails
safely?". It inventories the highest-risk failure and regression paths that
already exist in StoryTime — the failure / review queue, retry / re-run
behaviour, governance-blocked content, static HTML report safety, demo fixture
invariants, the legal-hallucination gate, operator-safe failure messages, and
state preservation around failed runs — records which tests and gates protect
each one, and documents how a local operator should respond to a failure
without bypassing governance or deleting state. It added four `docs/`
documents — `failure-mode-regression-hardening.md` (the overview),
`regression-risk-register.md` (the risk inventory), `failure-mode-test-matrix.md`
(the regression coverage map), and `operator-failure-response.md` (the operator
playbook) — and one focused regression test module,
`tests/test_failure_mode_regression.py`, which converts the project's
state-documentation discipline rule into an executable guard. It synchronized
the State Preservation Bundle.

Phase 11C added no product feature, no UI, no server, no JavaScript, no
generated audio, no screenshots/binary assets, no new dependency, and no
database schema change; it changed no pipeline behaviour, `storytime rerun`, or
Trust Envelope enforcement, and changed no `pyproject.toml`, `uv.lock`, or
`src/` content. The only `tests/` change is the new regression module.

Per the Phase Closure Protocol, Phase 11C was implementation output until
GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval
completed; it has since been locked. The artifact locked for this phase is
`storytime-phase11c-failure-mode-regression-hardening.tar.gz` (SHA-256
`2dd31442e62c13241a64d10c2d117aefedc3b9c633ad5ea5d1fa94cfaad7d57b`). Phase 11C
did **not** mark Phase 11 complete and did **not** start Phase 11D or Phase 12.

*(This Phase 11C note is a superseded point-in-time record — it is locked. Current state is recorded in the active Phase 12B / Phase 12B.2 notes at the top of this file; the Phase 12A, Phase 11B, Phase 11A, and Phase 10G notes below are historical records.)*

---

# Phase 11B note — Fresh Clone / Operator Reproducibility (locked — historical record)

**Date:** 2026-05-25
**Locked artifact:** `storytime-phase11b-fresh-clone-operator-reproducibility.tar.gz` (SHA-256 `08b72f2833da9adf3b8acc1f3170334eb7c5f998e19263838efbce2f571cc73f`).
**Status:** Phase 11B — Fresh Clone / Operator Reproducibility is **LOCKED / ACCEPTED / CANONICAL** — it was the last locked phase at that point in the project history. *(This is a superseded point-in-time record, originally written when Phase 11B was an implementation candidate; Phase 11B was subsequently locked under the Phase Closure Protocol, and is the source/base artifact for Phase 11C. Current status is in the Phase 12B note above.)*
**Last locked phase before Phase 11B:** Phase 11A — Release Candidate Hardening Baseline.
**Next action:** *(superseded — see the Phase 12B note above.)*

Phase 11B is the second Release Candidate Hardening subphase. It is a
fresh-clone / operator reproducibility verification round: it took the
Phase 11A documentation as a specification and verified it against reality. It
extracted the locked Phase 11A artifact into a clean tree, walked the
documented setup, validation, and demo paths exactly as written, and confirmed
they reproduce — the six Docker-free quality gates pass (549 tests, ruff/mypy
clean, import-linter 2/2 kept, `storytime doctor` healthy) and the documented
operator commands run as documented. It added two reproducibility documents
(`docs/operator-reproducibility-checklist.md`,
`docs/fresh-clone-troubleshooting.md`), refined the Phase 11A reproducibility
documents, aligned the `README.md` setup command with the canonical
`uv sync --frozen --extra dev` form, and synchronized the State Preservation
Bundle. It added no product feature, no UI, no server, no JavaScript, no
generated audio, no screenshots/binary assets, no new dependency, and no schema
change; it changed no pipeline behaviour, `storytime rerun`, or Trust Envelope
enforcement, and changed no `pyproject.toml`, `uv.lock`, `src/`, or `tests/`
content.

*(The Phase 11A note below is a historical record — Phase 11A is locked. The
Phase 10G lock closure note further below remains the record of the Phase 10
closure; Phase 10 is CLOSED.)*

---

# Phase 11A note — Release Candidate Hardening Baseline (locked — historical record)

**Date:** 2026-05-25
**Locked artifact:** `storytime-phase11a-release-candidate-hardening-baseline.tar.gz` (SHA-256 `664f8ba4ae90cf6a98ccc7d20369e690eac74497ab78f2b7067f0aac2079a7aa`).
**Status:** Phase 11A — Release Candidate Hardening Baseline is **LOCKED / ACCEPTED / CANONICAL**. *(This is a superseded point-in-time record, originally written when Phase 11A was an implementation candidate; Phase 11A was subsequently locked under the Phase Closure Protocol, and is the source/base artifact for Phase 11B. Phase 11B, Phase 11C, and Phase 11D have since also been locked and Phase 11 — Release Candidate Hardening — is CLOSED; current status is in the Phase 12B note above.)*
**Last locked work item before Phase 11A:** Post-Phase-10 Historical State Reconciliation.
**Next action:** *(superseded — see the Phase 12B note above.)*

Phase 11A is the first Release Candidate Hardening subphase. It is
documentation-first: it audits and documents the repository's non-feature
surfaces — fresh-clone readiness, the validation-command baseline, artifact
hygiene, the security/secrets posture, demo reproducibility, known limitations,
and the Phase 11 decomposition — so the later subphases can proceed from a
stable, understandable base. It added seven `docs/` hardening documents
(`release-candidate-hardening.md`, `phase11-plan.md`, `local-setup-runbook.md`,
`fresh-clone-checklist.md`, `rc-validation-checklist.md`,
`security-secrets-checklist.md`, `demo-reproducibility-checklist.md`) and
synchronized the State Preservation Bundle. It added no product feature, no UI,
no server, no JavaScript, no generated audio, no screenshots/binary assets, no
new dependency, and no database schema change; it changed no pipeline
behaviour, `storytime rerun`, or Trust Envelope enforcement, and changed no
`pyproject.toml`, `uv.lock`, `src/`, or `tests/` content. The six Docker-free
quality gates pass (549 tests, ruff/mypy clean, import-linter 2/2 kept,
`storytime doctor` healthy).

*(The Phase 10G lock closure note below remains the record of the Phase 10
closure; Phase 10 is CLOSED, and the Post-Phase-10 Historical State
Reconciliation was the last locked work item before Phase 11. The Phase 10F /
10E / 10C lock closure notes below are historical records.)*

---

# Phase 10G lock closure note — Phase 10 CLOSED

**Date:** 2026-05-25
**Locked artifact:** `storytime-phase10g1-uvlock-reversion-cleanup.tar.gz`
**SHA-256:** `8a0cc9a5b6426a291bec3a793e41501c7d3492187dd48b4f7729ea95e501a0c1`
**Status:** Phase 10G — Portfolio Narrative / Phase 10 Closure is **LOCKED / ACCEPTED / CANONICAL**. **Phase 10 is formally CLOSED.**
**Last locked phase:** Phase 10G — Portfolio Narrative / Phase 10 Closure.
**Next phase:** Phase 11 — Release Candidate Hardening *(Phase 11 has since been completed and is CLOSED — Phase 11A through 11D all locked; Phase 12 — Portfolio / SE Demo Packaging — is now STARTED. See the Phase 12A note at the top of this file for current status)*.
**Next action:** Begin Phase 11 — Release Candidate Hardening — under the Phase Closure Protocol when scheduled.

Phase 10G — the documentation, portfolio-narrative, demo-explanation, and Phase 10 closure phase — is locked. It added the Phase 10 portfolio/closure documents (`docs/portfolio-narrative.md`, `docs/demo-script.md`, `docs/operator-experience-walkthrough.md`, `docs/command-reference.md`, `docs/known-limitations.md`, `docs/observability-governance-talking-points.md`, `docs/phase10-acceptance-checklist.md`, `docs/screenshot-instructions.md`) and synchronized the State Preservation Bundle. It added no product feature, no UI, no server, no JavaScript, no generated audio, no screenshots/binary assets, and no new dependency; it changed no pipeline behaviour, no `storytime rerun` behaviour, no Trust Envelope enforcement, and no database schema.

Review basis: GPT-5.5 Phase 10G review PASS; Gemini Phase 10G review SAFE WITH EDITS (one required cleanup — verify/revert `uv.lock` to the exact Phase 10F state). The Phase 10G.1 cleanup completed that; the suspected `uv.lock` drift was a false positive (`uv.lock` was byte-for-byte identical across Phase 10F, Phase 10G, and Phase 10G.1, and Phase 10G.1 explicitly copied the Phase 10F `uv.lock` into the tree to guarantee identity — only `docs/artifact-manifest.md` and `docs/verification-log.md` cleanup bookkeeping changed from 10G to 10G.1). GPT-5.5 Phase 10G.1 verification PASS; Gemini Phase 10G.1 final verification SAFE TO LOCK. Validation at lock: 549 tests passing, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy.

The authoritative locked artifact for Phase 10G is `storytime-phase10g1-uvlock-reversion-cleanup.tar.gz` (SHA-256 `8a0cc9a5b6426a291bec3a793e41501c7d3492187dd48b4f7729ea95e501a0c1`). With Phase 10G locked, **Phase 10 — Product UI / Operator Experience — is formally CLOSED**: Phases 10A–10G are all locked. The next phase is **Phase 11 — Release Candidate Hardening**, which has **not started**.

*(This Phase 10G lock note records the Post-Phase-10 Closure State Synchronization. The Phase 10F lock closure note and the Phase 10E / Phase 10C lock closure notes below are historical records. Phase 10A, 10B, 10C, 10C.1, 10D, 10D.1, 10E — with the 10E.1 / 10E.2 cleanup sequence — 10F, and 10G are all locked.)*

---

# Phase 10F lock closure note

**Date:** 2026-05-25
**Lock archive:** `storytime-phase10f-demo-seed-data-golden-path-fixtures.tar.gz`
**SHA-256:** `e060570a94fb19f790c539542b3ef7445111430bc308668675548f66fa48df55`
**Status:** Phase 10F — Demo Seed Data / Golden Path Fixtures is **LOCKED / ACCEPTED / CANONICAL**.
**Last locked phase:** Phase 10F.
**Next phase:** Phase 10G — Portfolio Narrative / Phase 10 Closure.

Phase 10F added curated demo seed data and golden-path fixture scenarios so an operator can demonstrate the existing StoryTime pipeline, operator report, failure queue, Trust Envelope governance, and `storytime rerun` command reproducibly from a clean local environment — the `demo/` directory (four original CC0 seed texts plus schema-valid manifests, a demo-only blocked-source deny-list, and six fixture definitions), the `docs/demo.md` operator runbook, and `tests/test_demo_fixtures.py`. It was fixture / demo-readiness work: no new product feature, no UI, no server, no generated audio committed, no JavaScript, no new dependency, and no change to pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, or the database schema. Phase 10F completed the Phase Closure Protocol and was locked with explicit user approval.

*(The Phase 10E lock closure note and the Phase 10C lock closure note below are historical records, superseded by this Phase 10F closure.)*

---

# Phase 10E lock closure note

**Date:** 2026-05-25
**Lock archive:** `storytime-phase10e2-final-cleanup-v2-normalized.tar.gz`
**SHA-256:** `87fad92b2e0a919a81588f4c628ccfdf08860571fdc778c527d8fe93c30b7dec`
**Status:** Phase 10E — Static HTML Operator Report Refinement is **LOCKED / ACCEPTED / CANONICAL**, with the Phase 10E.1 / 10E.2 cleanup sequence accepted and the 10E.2 normalized cleanup as canonical state.
**Last locked phase:** Phase 10E / 10E.2 normalized cleanup.
**Next phase:** Phase 10F — Demo Seed Data / Golden Path Fixtures.

Phase 10E refined the existing generated static HTML operator report (executive status summary, rerun eligibility / action guidance, failure summary, command reference, semantic status badges, improved governance warning block, improved embedded CSS), keeping the report a local, static, read-only artifact with no JavaScript, no external assets, no browser-side mutation controls, and no backend behavior change. The Phase 10E.1 / 10E.2 cleanup sequence addressed raw `blocked_reason` redaction, archive hygiene, and state-preservation synchronization. Phase 10E was reviewed and locked with explicit user approval.

*(The Phase 10C lock closure note below is a historical record, superseded by this Phase 10E closure.)*

---

# Phase 10C lock closure note

**Date:** 2026-05-25
**Lock archive:** `storytime-phase10c-operator-cli-helpers-failure-queue.tar.gz`
**SHA-256:** `e30aaa57f900756e62347ddaac2df658d96065c9e1061679adb31594c73e2543`
**Status:** Phase 10C — Operator CLI Helpers / Failure Queue is **LOCKED / ACCEPTED / CANONICAL**.
**Last locked phase:** Phase 10C.
**Next phase:** Phase 10D — Pipeline Re-Run / Mutation Actions, not started.

Review basis: GPT-5.5 Thinking PASS with minor state-hygiene observation; Gemini/Flash Light SAFE TO LOCK. 466 tests passing, ruff clean, mypy clean, import-linter clean, `storytime doctor` healthy, legal scanner 0 violations.

*(The Phase 10B lock closure note immediately below is a historical record, superseded by this Phase 10C closure.)*

---

*(Historical record — superseded by the Phase 10C lock closure note above.)*

# Phase 10B lock closure note

**Date:** 2026-05-24 4:38 PM CDT  
**Lock archive:** `storytime-phase10b-locked-state-bundle.tar.gz`  
**Status:** Phase 10B — Generated Local HTML Operator Report is **LOCKED / ACCEPTED / CANONICAL**.  
**Last locked phase:** Phase 10B.  
**Next phase:** Phase 10C — Operator CLI Helpers / Failure Queue, optional / not started; Phase 10D future / not started.

Phase 10B was locked with explicit user approval after Claude Opus 4.7 implemented the generated static local operator report, GPT-5.5 verified the archive and gates, and Gemini 3.1 Pro returned `SAFE TO LOCK`.

Gemini confirmed: static local generated HTML, no server runtime, no frontend framework, no CDN/external assets, no mutation UI, no legal overclaiming, no raw-content leakage, deterministic timestamp support, and correct State Preservation Bundle updates.


---

# LLM_DIRECTOR — First-Read Instructions for Any LLM Working on StoryTime

**Read this file first, before doing anything else on StoryTime.**

StoryTime is built by a multi-model "RoundTable" workflow. During the Phase 7
sequence, RoundTable prompt/state generation became contaminated. Until
RoundTable is restored, **this repository — specifically the State Preservation
Bundle — is the portable project memory** passed between GPT-5.5, Claude Opus,
Gemini, and any future model. Trust the Bundle in this repo over any stale
RoundTable round text.

## What StoryTime is

A local-first, CLI-driven, observability-native content-to-audio pipeline. It
converts approved CC0 / US-public-domain text into podcast-ready audio, an RSS
feed, and a traceable record of every run. SQLite plus on-disk artifact
envelopes are the source of truth; OpenTelemetry is an optional view. It is
both a portfolio-grade OpenTelemetry / cloud-native demo and a proving ground
for the Kaname / RoundTable workflow.

## The State Preservation Bundle

These files together are the portable project memory. Keep them current.

- `LLM_DIRECTOR.md` — this file: roles, rules, first-read order.
- `docs/handoff-state.md` — the current dashboard: current phase, next action,
  what not to replay.
- `docs/roadmap.md` — phases, acceptance gates, model routing, amendment rules.
- `docs/canonical-state.md` — append-only mirror of locked decisions.
- `docs/phase-history.md` — append-only round-by-round record.
- `docs/open-issues.md` — the open-issue / carryover register.
- `docs/verification-log.md` — actual verification evidence per phase.
- `docs/artifact-manifest.md` — repository-archive lineage and hashes.
- `docs/roundtable-import-bridge.md` — how to reconstruct RoundTable state from
  this Bundle.
- `docs/architecture-baseline.md` — the locked architecture (Phase 1 plus the
  locked Phase 7C/7C.1 §16, Phase 8A §23, and Phase 9A §24 amendments; §24 is
  the Governance Baseline — Trust Envelope, licensing, fail-closed gating —
  plus the locked Phase 10A §25 Operator Experience Baseline amendment).
- `docs/product-charter.md` — the locked product definition (Phase 0).
- `docs/phase-closure-protocol.md` — how a phase is allowed to lock.

## First-read order

1. `LLM_DIRECTOR.md` (this file)
2. `docs/handoff-state.md`
3. `docs/canonical-state.md`
4. `docs/phase-history.md`
5. `docs/roadmap.md`
6. `docs/open-issues.md`
7. `docs/architecture-baseline.md`
8. `docs/phase-closure-protocol.md`

Read all eight before proposing or implementing anything.

## Model roles

- **GPT-5.5 Thinking** — Mediator / Architect / State Keeper / Prompt Engineer
  / Reviewer.
- **Claude Opus 4.7** — Chief Implementation / Hardening Engineer.
- **Gemini 3 Thinking** — Independent Critic / Architecture Reviewer.
- **Claude Sonnet 4.6** — bounded cleanup only when explicitly directed.

### What GPT-5.5 must do

Hold and update RoundTable state; mediate between models; author the prompts
for each round; route work to the right model; review implementation output;
enforce the Phase Closure Protocol; never let implementation output be treated
as a locked phase without review, critique, and explicit user approval. If
RoundTable state is lost or contaminated, reconstruct it from
`docs/roundtable-import-bridge.md` rather than replaying stale rounds.

### What Claude Opus must do

Implement the locked, scoped task narrowly and harden it. Never expand scope
(no cloud, registry, Kubernetes, Terraform, Helm, CI/CD, vendor fan-out, auth,
or multi-tenancy unless a locked phase explicitly authorizes it). Run the
quality gates and report exactly what passed or failed — never fabricate
commands, tests, or results. Update the living docs the round affects. End
every implementation round with the required final report (see below).

### What Gemini must do

Independently critique the implementation and its architecture. Look for scope
creep, weakened invariants, hidden architectural change, unsafe assumptions,
and gaps between docs and behavior. Never rubber-stamp; a clean review must be
earned. Critique is advisory to the user, who decides.

### What Claude Sonnet may and may not do

May: perform a small, explicitly-directed cleanup (e.g. a doc fix or a bounded
mechanical change) when GPT-5.5 or the user assigns it. May not: expand scope,
make architecture decisions, author amendments, lock a phase, or take on deep
implementation — those route to Opus and the closure protocol.

## Required living docs

Every round keeps the State Preservation Bundle current. At minimum, the round
that changes a thing updates the doc that records that thing:
`handoff-state.md` (always — it is the dashboard), `phase-history.md` (always —
append the round), `verification-log.md` (whenever gates or smoke tests ran),
`canonical-state.md` (whenever a decision locks), `roadmap.md` (whenever phase
status or routing changes), `open-issues.md` (whenever an issue opens/closes),
`artifact-manifest.md` (whenever a new archive is produced).

## Required updates by round type

- **Planning round** — update `roadmap.md`, `open-issues.md`, `handoff-state.md`;
  append `phase-history.md`. Produce a planning artifact, not code.
- **Implementation round** — update `phase-history.md`, `verification-log.md`,
  `artifact-manifest.md`, `handoff-state.md`, and `open-issues.md` as affected;
  update `canonical-state.md` only if a decision is locked this round.
- **Cleanup round** — bounded; update only the docs the cleanup touches; append
  `phase-history.md`; record gates in `verification-log.md`.
- **Review / lock round** — when the user locks a phase, append
  `canonical-state.md` and `phase-history.md`, and update `handoff-state.md`,
  `roadmap.md`, and `verification-log.md` to reflect the lock.


## Mandatory State Preservation Synchronization Gate

This gate is part of the artifact and applies to every future planning,
implementation, cleanup, review, and lock round. A round is not complete, and
an artifact is not review-ready, unless this gate is satisfied.

Updating one obvious living document is not enough. Appending a phase-history
entry is not enough. The model producing the artifact must reconcile the whole
State Preservation Bundle so a cold LLM session cannot resume from stale state.

Before producing the final archive, every implementation or cleanup model must:

1. Inspect the first-read/current-state surfaces:
   - `LLM_DIRECTOR.md`
   - `docs/handoff-state.md`
   - `docs/canonical-state.md`
   - `docs/phase-history.md`
   - `docs/roadmap.md`
   - `docs/open-issues.md`
   - `docs/verification-log.md`
   - `docs/artifact-manifest.md`
   - `docs/roundtable-import-bridge.md`
2. Update whichever of those files are affected by the round.
3. Search for stale current-looking language about the prior phase, current
   phase, next phase, lock status, candidate status, and review status.
4. Correct stale language when it appears as current state.
5. Preserve valid history only when clearly marked as historical, superseded, or
   no longer current.
6. Ensure the current authoritative state appears before older historical notes
   in first-read files.
7. Confirm that Phase N, Phase N.1 cleanup, and Phase N+1 status are not
   contradicted across the Bundle.

The stale-state search must be concrete. It must include terms for at least:

- the last locked phase
- the phase just implemented or cleaned up
- the next phase
- `not started`
- `pending review`
- `pending lock`
- `implementation candidate`
- `SAFE WITH EDITS` / `SAFE TO LOCK` when those review statuses apply
- `Last locked phase:`
- `Next phase:`

The final report for every artifact-producing round must include a dedicated
State Preservation Synchronization section with:

1. Living docs updated.
2. Living docs intentionally unchanged and why.
3. Stale-state search terms used.
4. Stale-state matches remaining.
5. Explanation proving remaining matches are historical/superseded or accurate.
6. Confirmation that no first-read/current-state document contains
   unsuperseded stale phase status.
7. Confirmation that the output archive is cold-session safe.

A phase is not lock-ready merely because code and tests pass. If the State
Preservation Bundle contains current-looking stale phase status, the correct
verdict is **SAFE WITH EDITS** until a docs/state-preservation cleanup fixes it.

## Append-only rule

`docs/canonical-state.md` and the round log in `docs/phase-history.md` are
**append-only**. Never delete or rewrite a prior locked decision or a prior
round entry. If a status line elsewhere is stale, correct it carefully and
label the correction (e.g. "superseded — see ..."); do not erase history.

## Architecture amendment rule

Any change to the locked Architecture Baseline (`docs/architecture-baseline.md`)
requires an **explicit, user-approved amendment** routed through RoundTable —
authored, Gemini-reviewed, revised if needed, then locked — *before* any
implementation depends on it. An amendment is never introduced as an
implementation detail. Precedent: the Phase 7C / 7C.1 amendment to §16 (optional
local app containerization).

## RoundTable recovery rule

If RoundTable state is lost, stale, or contaminated: do **not** replay stale or
superseded rounds. Reconstruct state from `docs/roundtable-import-bridge.md`
and the rest of the State Preservation Bundle. If the Bundle contains a newer
explicit recovery checkpoint than RoundTable, prefer the Bundle. The current
checkpoint is recorded in `docs/handoff-state.md`.

## Required final report from implementation models

Every implementation round must end with a report containing exactly these
sections:

1. Files changed
2. Tests/gates run
3. Living docs updated
4. Living docs unchanged and why
5. Open issues added/closed
6. Artifact produced
7. Confirmation that the State Preservation Bundle is included
8. Lock readiness assessment

## Current state (checkpoint)

**Phase 13 — Portfolio Website / Operator GUI — is STARTED. Phase 13K —
Demo Walkthrough Refresh / Governed Local Chain Story Path — is locked and is
the last locked phase. Phase 13L — Phase 13 Closure / Demo-Local Completion
Lock — is the current subphase: an implementation candidate, pending
review, NOT locked.** Phase 12 — Portfolio / SE Demo Packaging — is CLOSED
(Phase 12A–12D all locked), Phase 10 — Product UI / Operator Experience —
is CLOSED, and **Phase 11 — Release Candidate Hardening — is CLOSED** (all
four subphases 11A–11D locked). Phase 13L prepares the Phase 13 closure as a
candidate; Phase 13 will be formally closed only after Phase 13L review/lock,
so Phase 13 is not yet closed. Phase 13A through 13K are all locked. Phase 14 —
Cloud/Distributed — has not started; Phase 14A is the next proposed
architecture baseline and is NOT STARTED.

Phase 7, Phase 8, Phase 9A, Phase 9B, Phase 10A–10G, Phase 11A–11D,
Phase 12A, Phase 12B, Phase 12C, Phase 12D, Phase 13A, Phase 13B,
Phase 13C, Phase 13D, Phase 13D.1, Phase 13D.2, and Phase 13E are all
locked; Phase 9B.1 is folded into the Phase 9B lock, Phase 12A.1 (an
accepted state-hygiene cleanup sub-round) is folded into the Phase
12A lock lineage, and Phase 12B.1 / 12B.2 / 12B.3 (accepted cleanup
sub-rounds) are folded into the Phase 12B lock lineage.
`docs/architecture-baseline.md` Section 24 is canonical governance
law and Section 25 is canonical operator-experience law. The
**Post-Phase-10 Historical State Reconciliation** was the last
locked work item before Phase 11; its locked artifact is
`storytime-post-phase10-roundtable-historical-backfill.tar.gz`
(SHA-256 `367e647c46aa6e4fd039369da30859b11ca783249569df291343db133ef4cfdd`).

**Phase 11 closure.** Phase 11 — Release Candidate Hardening —
proceeded through four subphases, each locked under the Phase
Closure Protocol: 11A, 11B, 11C, and 11D. Phase 11D completed its
Phase Closure Protocol out-of-band; the user then locked Phase 11D,
formally closed Phase 11, and authorized Phase 12. The locked Phase
11D artifact is
`storytime-phase11d-release-candidate-evidence-pack.tar.gz`
(SHA-256 `07a3973e3dbb69d760ff2c330418f85101c2afa1464fc0eed752fc7053894d94`).

**Phase 12 closure.** Phase 12 — Portfolio / SE Demo Packaging —
proceeded through four subphases, each locked under the Phase Closure
Protocol: 12A (Portfolio / SE Demo Packaging Baseline), 12B (Portfolio
Evidence Pack / Reviewer Assets), 12C (Portfolio Demo Narrative /
Public Presentation Kit), and 12D (Phase 12 Closure Plan / Final
Portfolio Handoff Definition). Phase 12A.1 is folded into the Phase
12A lock lineage and Phase 12B.1 / 12B.2 / 12B.3 are folded into the
Phase 12B lock lineage as accepted cleanup sub-rounds — not
independently locked phases. Phase 12D completed its Phase Closure
Protocol out-of-band: Gemini returned the verdict to lock Phase 12D
and close Phase 12, with no critical findings, no non-blocking
findings, and no required edits, and the user then locked Phase 12D
and formally closed Phase 12. The locked Phase 12D artifact is
`storytime-phase12d-phase12-closure-plan-final-portfolio-handoff.tar.gz`
(SHA-256 `64ad09e875f0653608e0deb756f11ee5adc0d2ff1265e2039cbc51491f286cf8`),
recorded in `docs/canonical-state.md` and `docs/artifact-manifest.md`.
Phase 12E was optional, contingency-only work; the Phase 12D review
found no substantive gap, so Phase 12E was not needed and never
started.

**Phase 13E lock.** Phase 13E — Demo-Mode Action Preview / Operator
Intent Boundary — completed its Phase Closure Protocol (GPT-5.5
review, Gemini SAFE TO LOCK with no required edits) and was locked by
explicit user decision. **Phase 13E is the last locked phase.** Its
locked artifact is
`storytime-phase13e-demo-mode-action-preview-operator-intent-boundary.tar.gz`
(SHA-256 `a997f2ca9d213e28e140f47c63336367c8feda46ed994b41300f86b99f8d8164`).
Phase 13E added a static Demo-mode Action Preview system alongside the
unchanged `DisabledFutureActionCard`, clarified the Demo / Local /
Cloud-Distributed operating-mode model, and added a data-integrity
test — all static and Demo-mode-only, with the protected backend
export generator, the committed export JSON, the CLI app, and the
`storytime export-demo-ui` contract byte-identical to the Phase 13D.2
source.

**Current phase:** Phase 13 — Portfolio Website / Operator GUI — is
STARTED. **Phase 13F — Local Bridge Architecture & Contract Baseline —
is the current subphase:** a documentation-and-static-fixture
architecture / contract baseline over the locked Phase 13E operator
GUI — the architectural lock before any Python local-bridge
implementation is allowed (to the Local Bridge what Phase 13A was to
the operator GUI). The central principle: **the frontend is an
operator surface, not the durable storage layer** — durable state
lives outside the browser in an explicit external workspace / storage
target with clear export, reset, backup, and recovery semantics, so
StoryTime never repeats the RoundTable browser-storage failure mode;
the browser holds transient UI state only and `localStorage` /
`sessionStorage` / `IndexedDB` remain forbidden. Phase 13F adds
eleven new architecture / contract docs
(`docs/local-bridge-architecture.md`,
`docs/externalized-state-architecture.md`,
`docs/browser-storage-policy.md`,
`docs/local-mode-workspace-layout.md`,
`docs/storage-targets-architecture.md`,
`docs/action-execution-boundary.md`, `docs/local-action-dto-spec.md`,
`docs/local-action-audit-spec.md`,
`docs/local-mode-storage-contract.md`,
`docs/local-action-queue-observability.md`,
`docs/phase13f-local-bridge-contract-readiness.md`); a set of
non-runtime JSON example fixtures under `docs/examples/`
(local-action-requests, local-action-responses,
local-action-audit-records) labelled future / documentation-only; and
one new Python test (`tests/test_local_mode_contract_examples.py`)
validating those fixtures with plain Python (no JSON-schema
dependency). It settles the Hybrid Option C decisions: an
execution-timing policy (long-running actions asynchronous; the future
bridge returns `202 Accepted` with an `actionRequestId` / `jobId`;
acceptance is not success; export refresh after a durable write;
refresh-race avoidance via atomic write + identity-tagged read model);
the loopback-only / strict-origin / no-arbitrary-command /
command-pattern-router security boundary; the action allowlist
(`retry_failed_stage`, `inspect_trust_envelope`, `refresh_export`)
with higher-risk actions (`record_review_decision`,
`regenerate_operator_report`, `publish_episode`, `delete_artifact`,
provider sync) deferred; and a queue-observability model (depth,
in-flight, completed / failed / rejected / dead-letter counts,
oldest-queued and longest-in-flight ages, retry count, capacity,
saturation, export freshness) with a conservative local load-limit
policy and a distributed/cloud carry-forward. Phase 13F does **not**
modify `src/`, `frontend/src/`, the committed export JSON
`frontend/src/data/storytime-demo-export.json`, `frontend/package.json`,
`frontend/package-lock.json`, `pyproject.toml`, or `uv.lock`; all are
byte-identical to the locked Phase 13E source. Phase 13F implements
**no** runtime code: no local bridge, no server, no async queue, no
queue workers, no queue metrics / exporters, no OpenTelemetry, no
storage providers, no provider integrations, no runtime schema
validation, no router / history, no browser storage, no real Local
mode, no Cloud/Distributed mode, and no mutation / action execution;
the browser remains non-durable and the example fixtures are
documentation artifacts only that never claim Phase 13F executed
anything. The `tests/` changes are the narrow, explicitly-authorized
mechanical advance of the state-discipline guard
`tests/test_failure_mode_regression.py` to the Phase 13F current-state
expectations, and the new `tests/test_local_mode_contract_examples.py`.
Phase 13F is an implementation candidate, pending review, **not
locked**; it does not lock Phase 13F, does not close Phase 13, and
does not start Phase 13G. Phase 13G and later subphases have not
started. Phase 9C remains optional and not scheduled.

For the authoritative, always-current snapshot see `docs/handoff-state.md`.
