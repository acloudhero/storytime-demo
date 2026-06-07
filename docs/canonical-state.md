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

# Canonical State — Locked-Decision Mirror

> Append-only. This file **mirrors** decisions locked in RoundTable canonical
> state (Round 7 prerequisite correction 9). RoundTable remains the source of
> truth; this is a repo-local, append-only copy for implementers. Never edit or
> delete an existing entry — only append.

## Locked hard decisions (Phase 1 Architecture Baseline, Round 5)

1. `pipeline_run_id` (a ULID) is the durable correlation key, not `trace_id`.
2. `adapters/telemetry` is the only module that may import OpenTelemetry.
3. Stages communicate through artifacts, not shared mutable memory.
4. Artifact envelopes carry the W3C `traceparent` where applicable.
5. Linked traces are used across approval gates.
6. Approval is a persisted pipeline stage.
7. TTS adapters emit WAV only; MP3 encoding lives in assemble/package.
8. MockTTS and ManualImportTTS work before Piper; Piper is stubbed.
9. Internal events are data-only; there is no event bus in Phase 1/2.
10. The source manifest is constrained to CC0 + US public domain via a closed
    schema (`additionalProperties: false`).
11. Import direction is mechanically enforceable (import-linter).

## Locked DTO / context model (Rounds 3 & 5)

- No mutable god-object `PipelineContext`.
- Stages take a serializable `StageInput` DTO plus a minimal frozen
  `RunnerContext`.
- Stages return a `StageResult` that bundles a `StateUpdate` (clarification A2).
- `RunnerContext` carries only stable orchestration services: config, clock,
  state store, telemetry adapter, storage adapter.
- Clarification A1: stage-specific adapters (e.g. TTS) are constructor-injected
  into stages, not placed in the global `RunnerContext`.

## Locked Phase 2 prerequisite corrections (Round 7)

1. `event_log` is an append-only SQLite table, not JSONL.
2. Events and state updates are persisted in the same SQLite transaction where
   practical.
3. `event_log` is forensic/audit-only in Phase 2, not replayable event sourcing.
4. `ARCH-LOCK` annotations are required around load-bearing boundaries; missing
   ones are a scaffold rejection condition.
5. ffmpeg is not required for Phase 2 or its tests; a doctor/check mechanism
   reports its availability and the Phase 3 fail-fast path.
6. uv is the package manager; dependency versions are pinned and reported.
7. The prior external scaffold is non-canonical reference only.

## Phase 2 scaffold decisions (Round 8 — this round)

- **Package manager:** uv 0.11.7. `uv.lock` pins exact versions; commit it.
- **Python floor:** `requires-python = ">=3.11"`; developed and tested on 3.12.
  3.11 provides stdlib `tomllib`, `datetime.UTC`, and exception groups; nothing
  in Phase 2 needs a 3.12-only feature, so 3.11 maximises contributor reach.
- **CLI framework:** Typer (built on Click) — typed command signatures match the
  project's strict-typing posture.
- **RSS:** built with the standard library `xml.etree`; no XML dependency added.
- **HTTP:** Phase 2 uses the standard library `http.server`; the load-bearing
  `validate_bind_host` is a pure, tested function. A range-capable server is a
  Phase 3 item.
- **OTel transport:** OTLP over HTTP (`opentelemetry-exporter-otlp-proto-http`),
  lighter than the gRPC exporter for a local scaffold.
- **Import boundary:** the OpenTelemetry `forbidden` contract uses
  `allow_indirect_imports` so it flags *direct* imports only; the telemetry
  factory legitimately reaches the OTel adapter transitively.

## Phase 6S decisions (Round 13 — serving + multi-item feed)

Reclassified as **Phase 6S** — see `docs/phase-history.md`, section "Phase 6S
provenance". Phase 6S was an out-of-band execution: it implemented OI-7
(range-capable serving) and OI-11 (multi-item RSS feed) rather than the
intended observability work.

**Status:** reviewed post-implementation by GPT-5.5 and Gemini 3 Thinking,
sanitized of local runtime DB artifacts, and accepted by the user as a valid
reclassified phase — **not** architectural drift. Lock-ready. RoundTable
remains the source of truth.

(This section originally carried the provisional status line "Implementation
output, not yet phase-locked." That line was stale once Phase 6S was reviewed
and accepted; the Phase 6A docs-cleanup round corrected the heading and this
status paragraph. The decision bullets below — the actual decision record —
are unchanged, preserving the append-only intent of this mirror.)

- **OI-7 — range-capable HTTP server.** Audio is served by `RangeFileHandler`,
  which resolves the byte range with the pre-existing pure `parse_byte_range`
  and emits `200` / `206 Partial Content` / `416 Range Not Satisfiable`
  accordingly. `Accept-Ranges: bytes` is always sent. `feed.xml` is served as
  `application/rss+xml`, `*.mp3` as `audio/mpeg`. The stdlib
  `SimpleHTTPRequestHandler` is no longer used for serving (it mishandles
  ranges — Architecture Baseline section 15); an ARCH-LOCK on
  `http/server.py` records this. The handler is loopback-only via the
  unchanged `validate_bind_host`, and a request whose resolved path escapes the
  feed root is a `404` — traversal cannot read outside `feed/`.
- **HTTP version.** The server speaks HTTP/1.0: one request per connection,
  Content-Length-delimited bodies, no chunked encoding. Sufficient and correct
  for a local podcast client; HTTP/1.1 keep-alive is a non-blocking future
  option.
- **`storytime serve`.** The canonical command (Architecture Baseline section
  4) is implemented: it binds the configured loopback host/port (or `--port`)
  and serves `feed/` with `ThreadingHTTPServer` so a slow audio download does
  not block other local requests.
- **OI-11 — multi-item RSS feed.** `publish` re-renders the whole feed on every
  publish: the new episode is prepended to all prior episodes. Prior episodes
  come from an injected, read-only `EpisodeCatalog` Protocol; the concrete
  `StateEpisodeCatalog` lives in the composition root, so `PublishStage` never
  imports `storytime.state` — the publish-stage boundary and clarification A1
  (constructor-injected stage dependencies) are preserved.
- **Migration 0004.** `published_episode.description` is added (additive,
  `DEFAULT ''`) so a regenerated multi-item feed keeps each prior `<item>`'s
  own description rather than an empty placeholder. `SCHEMA_VERSION` → 4. Every
  pre-Phase-6 row remains valid.
- **`feed_version`.** Now the real monotonic feed-regeneration counter the
  publish stage computes (`len(prior episodes) + 1`), carried on
  `PublishedEpisodeIntent` and persisted by the runner — no longer a hardcoded
  `1`.
- **Atomic feed publish.** `StorageAdapter` gains `write_text_atomic` (temp
  file + `os.replace`). `publish` now builds the feed, runs `validate_feed`,
  and only then atomically replaces `feed.xml` — closing the Architecture
  Baseline section 14 "validate before the atomic replace" requirement, which
  the prior single-item plain write did not honour.

## Phase 6A decisions (Round 13 — observability infrastructure, dashboards, demo harness)

Implementation output. **Pending final user lock** until the Phase 6A
docs-cleanup round is approved. Recorded here per the append-only mirror
convention; RoundTable remains the source of truth.

Phase 6A is the originally intended Round 13 work (observability dashboards and
demo harness); it was implemented after Phase 6S, on the accepted Phase 6S
codebase, so the deliverable stays cumulative.

- **OI-16 — collector had no metrics pipeline.** Before Phase 6A the
  OpenTelemetry Collector config had only a `traces` pipeline, so the Phase 5
  metric instruments were emitted but landed nowhere. `config/otel-collector.yaml`
  gains a `metrics` pipeline with a `prometheus` exporter.
- **Metric-name preservation.** The `prometheus` exporter sets
  `add_metric_suffixes: false`, so Prometheus stores the eight Phase 5 metric
  series under their exact declared names (no `_total_total`).
- **Local stack.** `docker-compose.observability.yml` adds a Prometheus (scrapes
  the collector) and a Grafana (provisioned datasources + dashboards). All host
  ports remain loopback-bound; the test suite never requires the stack.
- **Dashboards-as-code.** Six Grafana dashboards in `config/grafana/dashboards/`
  are provisioned by file (zero UI configuration) and chart only the eight real
  Phase 5 metrics. No TTS/RSS dashboards — no Phase 5 metric supports them, and
  Phase 6A does not invent metrics.
- **Demo harness.** `python -m storytime.demo` (package `storytime.demo`) drives
  real pipeline scenarios so the dashboards have genuine telemetry. It generates
  telemetry only by running the real pipeline; it never fabricates spans or
  metrics, imports no `opentelemetry`, and is bounded to one workspace directory.
- **Metric honesty is enforced.** `tests/test_dashboards.py` fails the build if
  any dashboard expression references a token that is not a real Phase 5 metric.
- **No new dependency in runtime code.** `pyyaml` was added to the *dev* extra
  only, for the YAML-provisioning tests; no runtime module imports it.
- **Phase 5 telemetry architecture unchanged.** `NoopTelemetry` remains the
  default; OpenTelemetry imports remain confined to one adapter module.

## Phase 7A decisions (Round 15 — blue/green deployment, Option A)

Implementation output. **Pending review and final user lock.** Recorded here
per the append-only mirror convention; RoundTable remains the source of truth.

Phase 7A is the first blue/green-capable deployment path, deliberately scoped
to the lean **Option A**: honest blue/green designation, environment
separation, state boundaries, and telemetry attribution — and nothing more.

- **Deployment unit decision.** The Option A deployment unit is an
  uncontainerized per-slot `storytime` process — not a container, not a pod.
  Containerizing the application would contradict the Architecture Baseline
  §16 ARCH-LOCK (Docker is for the observability stack only); Phase 7A honours
  it. Whether Option B ships a versioned app image is an explicit, deferred
  open question, not decided here.
- **Slot-scoped state roots.** `deployment_slot`, when set, scopes the default
  state and feed roots to `runs/<slot>` and `feed/<slot>`, so blue and green
  get independent SQLite databases and feeds. An explicit `STORYTIME_RUNS_DIR`
  / `STORYTIME_FEED_DIR` still overrides — a shared layout remains possible but
  is never the silent default. This satisfies the hard requirement that blue
  and green not accidentally share mutable runtime state.
- **Slot is a validated path segment.** Because the slot now influences
  filesystem paths, `load_config` rejects any slot value that is not a short
  lowercase `[a-z0-9][a-z0-9._-]*` identifier — no slashes, no traversal —
  fail-fast at startup.
- **Telemetry resource attribution.** `deployment.environment` and
  `deployment.slot` (Phase 5 fields) are now driven by a real per-slot
  deployment and reach the OTel `Resource`. They remain resource attributes,
  never per-span/per-metric labels — no added cardinality.
- **Operator visibility.** `storytime doctor` prints a deployment-identity
  banner (environment, slot, state/feed roots). No new CLI command was added;
  the canonical command surface is unchanged.
- **Lean deployment artifacts.** `config/deploy/blue.env` + `green.env`
  (per-slot env files, no secrets) and `scripts/run-slot.sh` (a thin launcher)
  make the two slots runnable side by side on different loopback ports.
- **No overbuild.** No Kubernetes, no Terraform, no Dockerfile for the app, no
  reverse proxy, no automated traffic cutover, no production auth, no
  multi-tenant behaviour, no active alerting, no vendor fan-out. Switching
  between slots is an honest operator step; the enterprise mechanics are
  deferred to Option B / Phase 7B.
- **Constraints preserved.** Local-first behaviour (no slot required;
  `runs/` / `feed/` unchanged when no slot is set), `NoopTelemetry` as default,
  `OTelTelemetry` opt-in, the one-module OpenTelemetry import boundary,
  SQLite/`event_log`/artifacts as source of truth, `pipeline_run_id` as the
  durable correlation key, and the Phase 6 dashboards/harness/feed format — all
  unchanged. The test suite still needs no Docker and no cloud.

## Phase 7B decisions (Round 18 — blue/green Option B, front door / active-slot switching)

Phase 7B implementation output. Per the Phase Closure Protocol this is not
phase completion: Phase 7B closes only after GPT review, Gemini critique, any
cleanup, a next-phase routing recommendation, and explicit user approval.

- **Option B1 implemented.** A higher-assurance blue/green path over the
  Phase 7A slots: a stable local front door plus an explicit, persisted
  active-slot switch/rollback. Options B2 (app container), B3 (docs-only), and
  B4 (Kubernetes/Terraform) were rejected or deferred in Round 16-17 planning.
- **Front-door mechanism: native Python reverse proxy.** The front door
  (`storytime.frontdoor`) is a standard-library-only, loopback-only reverse
  proxy — deliberately *not* an external Caddy/nginx binary. This preserves
  StoryTime's local-first, zero-external-dependency property, keeps the front
  door fully covered by the normal test suite (no skip-by-default smoke
  tests), and keeps it under the same ruff/mypy/import-linter discipline. This
  is a documented divergence from the Phase 7B brief's "Caddy preferred" hint
  (the brief explicitly sanctioned a native Python front door as an
  alternative); it is flagged for mediator review.
- **Active-slot pointer is the single source of truth.**
  `config/deploy/active-slot` is a one-token text file (`blue`/`green`). The
  front door reads it on every request, so a switch takes effect with no proxy
  reload or restart. Only safe slot names are accepted or written — the same
  `[a-z0-9][a-z0-9._-]*` rule as Phase 7A (`is_valid_slot_name`, now a public
  function shared by `load_config` and the front door); traversal-like or
  shell-unsafe values are rejected. Writes are atomic.
- **Switch and rollback.** `switch_active_slot` validates the target, confirms
  it is a configured slot with a plausible endpoint, and writes *only* the
  pointer. Rollback is the identical mechanism targeting the previous slot.
  The switch never reads, writes, or migrates anything under `runs/` or
  `feed/` — Phase 7A state/feed separation is preserved exactly, and the
  inactive slot is a pristine rollback target.
- **Telemetry attribution unchanged.** The front door fronts feed-serving
  traffic only; pipeline spans/metrics are emitted by each slot's pipeline
  process and carry that slot's `deployment.slot`/`deployment.environment` on
  the OTel `Resource`. Routing or switching does not change any attribution.
  The front door imports no `opentelemetry` — the import-linter
  OpenTelemetry-confinement contract was extended to cover `storytime.frontdoor`.
- **App remains uncontainerized.** Architecture Baseline §16 is **not**
  amended. A documentation note was added to §16 recording that future
  application containerization would require an explicit, user-approved
  amendment — recording the standing rule is not amending it.
- **No overbuild.** No app Dockerfile, no Docker Compose app containers, no
  Kubernetes, no Terraform, no managed cloud, no Envoy/Kong, no automated /
  health-gated promotion, no production auth, no multi-tenant behaviour, no
  active alerting, no CI/CD, no vendor telemetry fan-out. The launcher scripts
  install and download nothing. The switch is scripted but operator-initiated.
- **Constraints preserved.** Local-first behaviour (no slot and no front door
  required), `NoopTelemetry` default, `OTelTelemetry` opt-in, the one-module
  OpenTelemetry import boundary, SQLite/`event_log`/artifacts as source of
  truth, `pipeline_run_id` as the durable correlation key, and the Phase 6/7A
  dashboards/harness/feed format — all unchanged. The test suite still needs
  no Docker, no cloud, and no external proxy binary.

## Phase 7C / 7C.1 decisions (Architecture Baseline amendment + app-containerization implementation)

Phase 7C authored an Architecture Baseline amendment candidate; Gemini
reviewed it (SAFE WITH EDITS), Phase 7C.1 applied the four required edits, and
the amendment was **locked** with user approval. The implementation round
(also referred to as Phase 7D) then delivered the optional containerization
layer. Implementation output is not phase completion — Phase 7C.1
implementation closes only after review/critique and explicit user approval.

- **Architecture Baseline §16 amended (locked).** Optional, local,
  single-host, demo-grade application containerization of the existing
  blue/green slots is now permitted. A documentation note in §16 records the
  locked amendment. Nothing further is authorized: no cloud deployment, no
  image-registry publishing, no Kubernetes, no Terraform, no production
  HA/auth, no multi-tenancy, no vendor telemetry fan-out.
- **Bare-metal stays the default.** Bare-metal local Python remains the
  default supported mode; Docker is optional and is never required. The six
  quality gates (`uv sync`, `pytest`, `ruff`, `mypy`, `lint-imports`,
  `storytime doctor`) all pass with no Docker installed.
- **Containerization layer delivered.** An application `Dockerfile` (pinned
  base, non-root user, installs the frozen `uv.lock` set, includes `ffmpeg`),
  a `.dockerignore` (excludes `runs/`, `feed/`, `.env`, secret patterns,
  caches), and an optional `docker-compose.app.yml` defining the blue and
  green app-slot containers from one image.
- **SQLite safety.** Each slot's SQLite state and feed live on per-slot
  **named Docker volumes**; host bind mounts of the state DB are prohibited
  (virtiofs/FUSE locking hazard). Durable data outlives containers. Blue and
  green keep strictly isolated state — no shared DB, no two writers.
- **Loopback-only.** The app compose uses `network_mode: host` so each slot
  binds `127.0.0.1` itself (Architecture Baseline §15 `validate_bind_host`
  unchanged — the app binds `0.0.0.0` nowhere). No broad port publishing.
- **Stable telemetry identity.** `service.instance.id` is pinned to a stable,
  slot-derived value (`storytime-blue` / `storytime-green`), derived only from
  the deployment slot so it is identical bare-metal and containerized; it is
  never a container ID/PID/hostname. No OpenTelemetry Docker/host/process
  resource detector is used or added; the explicitly-constructed resource is
  authoritative. App owns telemetry identity; the Collector owns routing.
- **Front door unchanged.** The Phase 7B native Python front door stays a host
  process; the active-slot pointer stays a host file; switch/rollback remain
  pointer-based and operator-initiated.
- **Blue/green state divergence accepted and documented** — switching changes
  which isolated timeline is served; it never merges or migrates state.
- **Phase 8 recorded, not implemented.** Vendor telemetry fan-out is deferred:
  local stack OTel Collector + Prometheus + Loki + Jaeger + Grafana; vendor
  priority Dynatrace (primary), New Relic (secondary), Datadog (deferred);
  optional, disabled by default, Collector-owned, no vendor SDK in app code.

## Phase 7 completion (Phase 7D / 7D.1 locked — Phase 8 planning next)

Recorded as a locked-state update. Phase 7 of StoryTime is **complete**.

- **Phase 7D — Optional Local App Containerization — locked.** The Phase 7C.1
  amendment's implementation (Dockerfile, `.dockerignore`, optional
  `docker-compose.app.yml`, per-slot named volumes, loopback-only
  `network_mode: host`, stable slot-derived `service.instance.id`) was
  reviewed, live Docker smoke-tested, and locked with user approval.
- **Phase 7D.1 — Operational Cleanup: Compose Build Race Fix — locked.** The
  fix that makes one service the sole image builder and has the other consume
  the shared image with `pull_policy: never` was reviewed and **live Docker
  smoke-tested on Windows Docker Desktop / WSL2** — `docker compose config`,
  `docker compose build` (no same-tag BuildKit export race), `up -d`, and the
  empty-cache `up -d` rebuild all passed; blue and green both served from
  `StoryTimeFeed Python/3.12.3` on `127.0.0.1:8000` / `:8001`. Locked with
  user approval. Closes OI-20.
- **Phase 7 is complete.** Locked Phase 7 set: 7A, 7B, 7C / 7C.1, 7D, 7D.1.
- **Phase 8 — Multi-Backend Telemetry Fan-Out — is the next planned phase.**
  Planning has not started. Direction remains as recorded above (local stack
  first; vendor priority Dynatrace > New Relic > Datadog; optional,
  Collector-owned, no vendor SDK in app code).
- **State Preservation Bundle is required while RoundTable is unstable.**
  RoundTable prompt/state generation was contaminated during the Phase 7
  sequence. Until RoundTable is restored, the repository State Preservation
  Bundle — `LLM_DIRECTOR.md` plus the `docs/` state files — is the portable
  project memory and the authoritative recovery checkpoint. See
  `LLM_DIRECTOR.md` and `docs/roundtable-import-bridge.md`.

## Phase 8A — Architecture Baseline Amendment (candidate — authored, pending lock)

Amendment-authoring round output. **This is not a locked decision.** Recorded
here, clearly labeled as a pending-lock candidate, following the same
append-only-mirror convention used for the Phase 7A and 7B "implementation
output, pending lock" entries above. RoundTable remains the source of truth.

Phase 8A authored an Architecture Baseline amendment **candidate** —
`docs/architecture-baseline.md` Section 23, "Collector-Owned Multi-Backend
Telemetry Fan-Out". It is architecture/documentation only and authorizes no
implementation. Per the Phase Closure Protocol and the precedent of the locked
Phase 7C / 7C.1 §16 amendment, Section 23 becomes a locked decision only after
GPT-5.5 review, Gemini critique, any required revision, and explicit user
approval. Until then no Phase 8 implementation may depend on it.

The candidate establishes, for the future Phase 8 fan-out work:

- **Collector-owned fan-out.** Multi-backend telemetry fan-out is owned only
  by the OpenTelemetry Collector. Application services emit telemetry solely
  to the configured local Collector endpoint; the app never sends telemetry
  directly to Dynatrace, New Relic, Datadog, Honeycomb, Grafana Cloud, or any
  other vendor endpoint.
- **No vendor SDKs in application code.** No vendor-specific Python SDK,
  agent, or telemetry package may enter StoryTime application code or the
  `pyproject.toml` runtime dependencies. Generic OpenTelemetry SDK usage stays
  exactly as established by Phase 5, confined to the one telemetry adapter
  module behind the import-linter contract.
- **Standard OTLP only.** Vendor fan-out uses `otlp` / `otlphttp` exporter
  families from the Collector. Proprietary vendor exporters, the Datadog
  exporter, vendor agents, sidecar/host agents, and proprietary protocol
  bridges are forbidden unless a future explicit amendment approves them. A
  vendor that cannot accept standard OTLP / OTLP-HTTP is deferred.
- **Narrow outbound-network exception.** The only authorized outbound network
  exception is explicitly enabled telemetry export from the Collector. The
  core app must still run with no internet access; the whole test suite must
  still run with no internet and no Docker; vendor credentials are never
  required for local development, tests, demos, or default operation.
- **Disabled-by-default vendor profiles.** `STORYTIME_TELEMETRY=noop` remains
  the default. Local-only Collector routing must work with no vendor
  credentials; vendor fan-out requires explicit additional environment
  configuration. No committed file may contain a real secret, token, tenant
  ID, API key, or user-specific vendor endpoint.
- **Environment-only secret handling.** All vendor endpoints and tokens are
  injected via environment variables; no secret may be hardcoded in source,
  Compose files, Collector config, docs, tests, dashboards, scripts, or
  Makefile targets. `.env` stays git-ignored; `.env.example` uses fake
  placeholders only.
- **Strengthened telemetry data hygiene.** Telemetry stays control-plane
  metadata only — never raw story text, source/narration text, full RSS XML,
  source payloads, secrets, large blobs, or high-cardinality arbitrary text.
  This strengthens, never weakens, the Phase 5 hygiene rule.
- **Phase 8B log routing.** Logs route to Loki via stdout / Docker log
  collection / Collector-supported local routing. StoryTime's Python logging
  is not rewritten around direct OTLP log export in Phase 8.
- **Collector resiliency.** Future Phase 8B / 8C Collector configs must use
  batching, memory limiting, sending queues, retry-on-failure, graceful
  disablement of empty vendor profiles, and no app dependency on vendor
  exporter health — a vendor endpoint failure must never break the app.
- **Backend priority.** Dynatrace (primary), New Relic (secondary), Datadog
  (deferred unless clean standard OTLP support is possible).
- **Phase 8B local stack.** OpenTelemetry Collector + Prometheus + Loki +
  Jaeger + Grafana.
- **Phase 8 split.** Phase 8A (this amendment), Phase 8B (local multi-backend
  stack expansion), Phase 8C (optional vendor export profiles).

No application code, telemetry code, Docker artifact, configuration, test, or
dependency was changed by Phase 8A. The local-first baseline, the
SQLite/artifact source-of-truth semantics, the optional-telemetry invariant,
and the one-module OpenTelemetry import boundary are all unchanged. When the
user locks Section 23, this section should be re-recorded (append-only) as a
locked decision.

## Phase 8A — Architecture Baseline Amendment — LOCKED

Locked-decision record. The Phase 8A amendment candidate recorded in the
section above completed the Phase Closure Protocol review sequence — Claude
Opus 4.7 authored it; GPT-5.5 reviewed the archive (clean); Gemini reviewed
the Phase 8A review bundle and returned `SAFE TO LOCK`; the user approved the
lock (2026-05-24). **`docs/architecture-baseline.md` Section 23 — "Collector-
Owned Multi-Backend Telemetry Fan-Out" — is now a locked, canonical part of
the Architecture Baseline.** Per the append-only convention this entry records
the lock; the candidate section above is preserved unchanged as history.

The locked amendment authorizes, for Phase 8 multi-backend telemetry fan-out:

- **Collector-owned fan-out.** Only the OpenTelemetry Collector performs
  multi-backend fan-out; application services emit telemetry solely to the
  configured local Collector endpoint — never directly to Dynatrace, New
  Relic, Datadog, Honeycomb, Grafana Cloud, or any other vendor endpoint.
- **No vendor SDKs in application code.** No vendor-specific Python SDK,
  agent, or telemetry package in StoryTime application code or in the
  `pyproject.toml` runtime dependencies. Generic OpenTelemetry SDK usage stays
  exactly as established by Phase 5, confined to the one telemetry adapter
  module behind the import-linter contract.
- **Standard OTLP only.** Vendor fan-out uses the `otlp` / `otlphttp`
  exporter families from the Collector. Proprietary vendor exporters, the
  Datadog exporter, vendor agents, sidecar/host agents, and proprietary
  protocol bridges are forbidden unless a future explicit amendment approves
  them; a vendor lacking clean standard OTLP support is deferred.
- **Narrow outbound-network exception.** The only authorized outbound network
  exception is explicitly enabled telemetry export from the Collector. The
  core app must still run with no internet access; the whole test suite must
  still run with no internet and no Docker; vendor credentials are never
  required for local development, tests, demos, or default operation.
- **Disabled-by-default vendor profiles.** `STORYTIME_TELEMETRY=noop` remains
  the default; local-only Collector routing must work with no vendor
  credentials; vendor fan-out requires explicit additional environment
  configuration; no committed file may contain a real secret, token, tenant
  ID, API key, or user-specific vendor endpoint.
- **Environment-only secret handling.** All vendor endpoints and tokens are
  injected via environment variables; no secret hardcoded in source, Compose
  files, Collector config, docs, tests, dashboards, scripts, or Makefile
  targets. `.env` stays git-ignored; `.env.example` uses fake placeholders.
- **Strengthened telemetry data hygiene.** Telemetry stays control-plane
  metadata only — never raw story text, source/narration text, full RSS XML,
  source payloads, secrets, large blobs, or high-cardinality arbitrary text.
- **Phase 8B log routing.** Logs route to Loki via stdout / Docker log
  collection / Collector-supported local routing; StoryTime's Python logging
  is not rewritten around direct OTLP log export in Phase 8.
- **Collector resiliency.** Future Phase 8B / 8C Collector configs must use
  batching, memory limiting, sending queues, retry-on-failure, graceful
  disablement of empty vendor profiles, and no app dependency on vendor
  exporter health.
- **Backend priority.** Dynatrace (primary), New Relic (secondary), Datadog
  (deferred unless clean standard OTLP support is possible).
- **Phase 8B local stack.** OpenTelemetry Collector + Prometheus + Loki +
  Jaeger + Grafana.
- **Phase 8 split.** Phase 8A (this amendment, locked), Phase 8B (local
  multi-backend stack expansion), Phase 8C (optional vendor export profiles).

The lock closure is documentation-only: no application code, telemetry code,
Docker artifact, Collector configuration, test, or dependency changed. The
local-first baseline, the SQLite/artifact source-of-truth semantics, the
optional-telemetry invariant, and the one-module OpenTelemetry import boundary
are all unchanged. The next phase is **Phase 8B — Local Multi-Backend Stack
Expansion**.

---

## Phase 8B — Local Multi-Backend Stack Expansion (LOCKED — 2026-05-24)

> **Lock status:** Phase 8B, together with the Phase 8B.1 operational cleanup
> below, is **locked** (2026-05-24) — implemented by Opus, reviewed by GPT-5.5
> and independently critiqued by Gemini (`SAFE WITH MINOR CLEANUP`), the
> cleanup applied in Phase 8B.1, and locked with explicit user approval
> conveyed by the go-ahead to begin Phase 8C (which is gated on the Phase 8B
> lock). The section text below was authored as the implementation-output
> record and is retained verbatim as history; the decision it describes is now
> locked and canonical.

Implementation output for **Phase 8B — Local Multi-Backend Stack Expansion**.
This section records implementation output only; per the Phase Closure
Protocol Phase 8B is **not** a locked decision until GPT review, Gemini
critique, and explicit user approval are complete. It is recorded here, as a
clearly-labeled pending-lock entry, following the precedent of earlier
implementation phases.

Phase 8B implements the local-only observability topology promised by the
locked Phase 8A amendment — the five-service local stack OpenTelemetry
Collector + Prometheus + Loki + Jaeger + Grafana — by adding Loki and a local
log-routing path. It introduces no vendor behavior; Phase 8C remains the
optional-vendor-profiles phase.

Implementation output (pending lock):

- **Loki local logs backend.** `docker-compose.observability.yml` adds a
  `loki` service (`grafana/loki:3.3.2`, host port bound to `127.0.0.1:3100`)
  configured by a new minimal `config/loki.yaml` (single-binary, filesystem
  storage, auth disabled, 72h retention). Loki 3.x ingests OTLP natively.
- **Collector logs pipeline.** `config/otel-collector.yaml` gains a `filelog`
  receiver (tails the read-only-mounted `./logs` directory), a `logs` pipeline,
  and an `otlphttp` exporter targeting Loki's native OTLP endpoint. The
  exporter is the **standard `otlphttp` exporter** — not a proprietary `loki`
  exporter, not a vendor exporter (Architecture Baseline §23.4).
- **Collector resiliency (§23.10).** A `memory_limiter` processor runs first
  in every pipeline; the Jaeger and Loki exporters carry `retry_on_failure`
  and a `sending_queue`. Behavior under a backend outage is drop-not-crash.
  The traces and metrics pipelines are otherwise unchanged — the Phase 6A
  metric-honesty configuration (`add_metric_suffixes: false`) is preserved.
- **Grafana Loki datasource.** `config/grafana/provisioning/datasources/`
  provisions a third datasource (Loki) as code. The six metric dashboards are
  untouched; logs are explored via Grafana Explore, so no logs dashboard is
  added and the Phase 6A metric-honesty dashboard guarantee is unaffected.
- **Log source — demo harness only.** The observability demo harness writes a
  structured JSON-lines log file (new module `storytime.demo.logsink`;
  `run_demo(..., log_dir=...)`; `python -m storytime.demo --log-dir <dir>`).
  This is plain structured *file* logging: it imports no `opentelemetry`,
  opens no socket, and performs no Python OTLP log export (§23.9, §23.13).
  Log records are control-plane metadata only — scenario name, pipeline run
  id, status — never story text, narration, or RSS payloads (§23.8). With no
  `--log-dir` no log file is written; default behavior is unchanged. The
  **StoryTime application core gains no parallel logging system** — the runner,
  stages, and adapters still emit only events (durable) and spans (the view).

Invariants preserved: local-first; `STORYTIME_TELEMETRY=noop` default; core
app and the full test suite run with no Docker, no internet, and no vendor
credentials; the one-module OpenTelemetry import boundary (the new log sink is
OTel-free); blue/green slot identity and the stable slot-derived
`service.instance.id` (Phase 7C / 7C.1, Phase 7D); SQLite + artifact envelopes
as source of truth. No vendor SDK, agent, exporter, endpoint, or secret was
added. Six quality gates pass — 332 tests (18 new), ruff/mypy/import-linter
clean, `storytime doctor` healthy. The Loki image tag and `config/loki.yaml`
are unverified in the Docker-less build environment — open issue **OI-21**.

### Phase 8B.1 — Operational cleanup: logs-directory preflight (2026-05-24)

Appended to the Phase 8B pending-lock record above. After GPT-5.5 review and
Gemini critique returned `SAFE WITH MINOR CLEANUP` for Phase 8B, Phase 8B.1
applied that narrow operational cleanup: the `./logs` directory (bind-mounted
into the Collector's `filelog` receiver) is now created — owned by the
invoking user — before `docker compose up` or the demo depend on it. The
Makefile gained a `logs-dir` preflight target plus `observability-up`,
`observability-down`, and `demo` convenience targets; `docs/observability-demo.md`,
`docs/runbook.md`, and `README.md` document the `mkdir -p logs` preflight for
manual users; two regression tests lock the preflight contract. No application
code, telemetry, Collector/Loki config, compose service, or dependency
changed. Phase 8B.1 folds into the eventual Phase 8B lock; it is implementation
output, pending review/lock, recorded here as a clearly-labeled pending-lock
entry. Six gates green — 334 tests.


---

## Phase 8C — Optional Vendor Export Profiles (implementation output produced, pending review/lock — 2026-05-24)

Implementation output for **Phase 8C — Optional Vendor Export Profiles**, the
third and final Phase 8 sub-phase. Per the Phase Closure Protocol Phase 8C is
**not** a locked decision until GPT review, Gemini critique, and explicit user
approval; it is recorded here as a clearly-labeled pending-lock entry.

Phase 8C is a configuration/documentation phase governed entirely by the locked
Architecture Baseline Section 23. It adds optional, disabled-by-default vendor
telemetry export profiles (Dynatrace, New Relic) through the OpenTelemetry
Collector. It changes **no StoryTime application behaviour** — no `src/` file,
no `pyproject.toml` dependency, and no application test changed. It adds no
vendor SDK or agent and no cloud deployment.

Implementation output (pending lock):

- **Option B — explicit opt-in.** A new override compose file
  `docker-compose.vendor.yml` plus a new vendor collector example config
  `config/otel-collector-vendor.yaml`. The default
  `docker compose -f docker-compose.observability.yml up -d` is unchanged and
  routes locally only — `config/otel-collector.yaml` has no vendor exporter.
  Vendor egress requires the explicit extra file `-f docker-compose.vendor.yml`
  (Section 23.6).
- **Standard OTLP/HTTP only (23.4).** Both profiles — `otlphttp/dynatrace`
  (`Authorization: Api-Token` header) and `otlphttp/newrelic` (`api-key`
  header) — use the generic `otlphttp` exporter. No proprietary exporter. No
  Datadog exporter; Datadog remains deferred (23.11).
- **Secrets are environment-only (23.6, 23.7).** Vendor endpoints and tokens
  are injected via `${env:...}` from a git-ignored `config/vendor.secret.env`
  (the `*.secret.env` pattern). The committed `config/vendor.secret.env.example`
  carries only obvious `REPLACE-WITH-YOUR-...` placeholders on `.invalid` hosts.
  No real endpoint, token, tenant ID, or account ID is committed anywhere.
- **Collector resiliency (23.10).** Each vendor exporter has a bounded
  `retry_on_failure` (`max_elapsed_time: 60s`) and a `sending_queue`;
  `memory_limiter` runs first in every pipeline. Vendor exporters are
  independent siblings of the local exporters — a vendor outage drops only that
  leg and never affects the local Jaeger/Prometheus/Loki stack or the app.
  Drop-not-crash.
- **Tests.** New `tests/test_vendor_export_profiles.py` (12 static governance
  tests). The Phase 7C.1 test that enforced the Section 16 note's blanket "no
  vendor telemetry fan-out" was updated to the post-Section-23 contract (vendor
  config confined to the Phase 8C opt-in files; default path local-only;
  Datadog absent) — the Section 16 note's statement was narrowly superseded by
  the locked Section 23.14.
- **Docs.** New `docs/vendor-export-profiles.md`; `docs/telemetry-map.md`,
  `docs/observability-demo.md`, `docs/runbook.md`, and `.env.example` updated.

Invariants preserved: local-first; `STORYTIME_TELEMETRY=noop` default; the core
app and the full test suite run with no Docker, no internet, and no vendor
credentials; the one-module OpenTelemetry import boundary; no new runtime
dependency; SQLite + artifact envelopes as source of truth. Six quality gates
pass — 346 tests (12 new; one Phase 7 test renamed/updated),
ruff/mypy/import-linter clean, `storytime doctor` healthy. The override compose
merge and live vendor export are unverified in the Docker-less build
environment — open issue **OI-22**.

---

## Phase 8C.1 — Vendor Profile Separation Cleanup (implementation output, pending review/lock — 2026-05-24)

Targeted cleanup of the Phase 8C implementation output, applied **before** the
Phase 8C lock. Like the Phase 8C entry above, Phase 8C.1 is **not** a locked
decision: it is implementation output recorded here as a clearly-labeled
pending-lock entry, and it locks together with Phase 8C on GPT review, Gemini
critique, and explicit user approval. This entry supersedes the override
*mechanism* described in the Phase 8C entry above; every Section 23 invariant
in that entry is unchanged.

Reason for the cleanup: the Phase 8C implementation used a single combined
override (`docker-compose.vendor.yml` + `config/otel-collector-vendor.yaml`)
that activated Dynatrace and New Relic together. Independent review found this
weaker than independently activatable profiles — a user may hold credentials
for only one vendor, or wish to demo one backend at a time, and disabling a
vendor required editing the Collector config. Phase 8C.1 makes the two vendors
independently activatable.

Implementation output (pending lock):

- **Split into two independent, mutually exclusive profiles.** The combined
  `docker-compose.vendor.yml` and `config/otel-collector-vendor.yaml` were
  removed and replaced by: `docker-compose.vendor.dynatrace.yml` +
  `config/vendor/otel-collector.dynatrace.example.yaml` (local config plus the
  single `otlphttp/dynatrace` profile), and `docker-compose.vendor.newrelic.yml`
  + `config/vendor/otel-collector.newrelic.example.yaml` (local config plus the
  single `otlphttp/newrelic` profile). Each override is activated on its own;
  neither profile depends on the other, and disabling a vendor needs no file
  editing — it is simply the absence of that override.
- **Mutual exclusivity is a documented constraint.** A single Collector process
  reads one resolved config and Compose's `command:` is replaced (last `-f`
  wins), so the two overrides cannot be stacked to produce a two-vendor
  pipeline. The override files, the vendor configs, and
  `docs/vendor-export-profiles.md` all state this explicitly; bring the stack
  up with at most one vendor override. Simultaneous dual-vendor export is
  intentionally outside the Phase 8C profile set.
- **No Section 23 invariant changed.** Both profiles still use the standard
  `otlphttp` exporter only (23.4); no proprietary or Datadog exporter (23.4,
  23.11); secrets remain environment-only via `${env:...}` from the git-ignored
  `config/vendor.secret.env` (23.6, 23.7); each vendor exporter keeps its
  bounded `retry_on_failure` (`max_elapsed_time: 60s`) and `sending_queue` with
  `memory_limiter` first in every pipeline (23.10); the default
  `docker-compose.observability.yml` path is untouched and local-only (23.6).
  The shared `config/vendor.secret.env.example` is unchanged in content (one
  template, both vendor sections; unused placeholders are simply never read).
- **Tests.** `tests/test_vendor_export_profiles.py` was rewritten for the split
  shape — parametrized per vendor, asserting each config wires exactly its own
  profile and not the other, and that the two overrides target distinct configs
  and distinct container paths. `tests/test_containerization.py`'s Phase 8C
  opt-in file set was updated to the four split files. No `src/` file,
  `pyproject.toml` dependency, or application test changed.
- **Docs.** `docs/vendor-export-profiles.md` rewritten for the split;
  `docs/telemetry-map.md`, `docs/observability-demo.md`, `docs/runbook.md`,
  `.env.example`, `.dockerignore`, `README.md`, `LLM_DIRECTOR.md`, and
  `docs/open-issues.md` (OI-22) updated to the per-vendor override names.

State-doc cleanup folded into this round: the `docs/handoff-state.md`
"State-source note" — which carried ambiguous "if that inference is wrong,
revert" self-doubt about the Phase 8B / 8B.1 lock — was removed and replaced
with a clean statement that Phase 8B / 8B.1 are locked on the user's explicit
go-ahead and are not under review. The factual provenance of that lock remains
recorded, append-only, in `docs/phase-history.md`.

Invariants preserved: local-first; `STORYTIME_TELEMETRY=noop` default; the core
app and the full test suite run with no Docker, no internet, and no vendor
credentials; no new runtime dependency; SQLite + artifact envelopes as source
of truth. The override compose merges and live vendor export remain unverified
in the Docker-less build environment — open issue **OI-22**.

---

## Phase 8C / 8C.1 — Optional Vendor Export Profiles — LOCKED (2026-05-24)

Locked-decision record. **Phase 8C — Optional Vendor Export Profiles**,
together with the **Phase 8C.1 — Vendor Profile Separation Cleanup**, completed
the Phase Closure Protocol review sequence:

- Claude Opus 4.7 implemented Phase 8C (the optional, disabled-by-default
  Dynatrace / New Relic vendor export profiles, governed by the locked
  Architecture Baseline Section 23).
- GPT-5.5 reviewed the Phase 8C archive and identified a required cleanup:
  split the single combined vendor activation into independently activatable
  per-vendor profiles, and clear ambiguous state-doc language about the
  Phase 8B / 8B.1 lock status.
- Opus implemented Phase 8C.1: removed the combined `docker-compose.vendor.yml`
  and `config/otel-collector-vendor.yaml`; added the two independent,
  mutually exclusive per-vendor profiles
  (`docker-compose.vendor.dynatrace.yml` + `config/vendor/otel-collector.dynatrace.example.yaml`,
  `docker-compose.vendor.newrelic.yml` + `config/vendor/otel-collector.newrelic.example.yaml`);
  rewrote the vendor tests; and removed the ambiguous "if that inference is
  wrong, revert" state-doc language.
- GPT-5.5 reviewed the Phase 8C.1 archive and found it ready for independent
  review — no `src/storytime/**` change, no vendor SDK or agent, no proprietary
  or Datadog exporter, no app-to-vendor call, no dependency change; both vendor
  Collector configs and both override compose files parse; vendor tests
  `24 passed`.
- Gemini independently reviewed the Phase 8C.1 implementation packet and
  returned **`SAFE TO LOCK`**, accepting collector-owned vendor export,
  local-first preservation, disabled-by-default behaviour, standard
  OTLP/HTTP-only export, the Dynatrace and New Relic profiles, the Datadog
  deferral, secret hygiene, state preservation, and the mutually exclusive
  per-vendor profile design as acceptable for Phase 8C.

Phase 8C is **locked with explicit user approval (2026-05-24)**. The Phase 8C.1
cleanup is **accepted as part of the Phase 8C lock** — it is not a separately
locked phase; it is the in-scope cleanup of the Phase 8C output and locks with
it. The locked authoritative archive is
`storytime-phase8c1-vendor-profile-split.tar.gz`
(sha256 `b93cc84a473fe71df2ef2f00862c9ab2a7cce019c11da83ec5e738c0818c7f40`).

What is now canonical:

- Optional vendor telemetry export exists as **two independent, mutually
  exclusive per-vendor profiles** — Dynatrace and New Relic — each a Compose
  override (`docker-compose.vendor.<vendor>.yml`) plus a single-vendor
  Collector example config under `config/vendor/`. Each is activated on its
  own; the default `docker-compose.observability.yml` path is unchanged and
  local-only.
- All Section 23 invariants hold: collector-owned fan-out; no vendor SDK or
  agent; standard `otlphttp` only, no proprietary or Datadog exporter (Datadog
  remains deferred); environment-only secrets; disabled-by-default; bounded
  retry + sending queue with `memory_limiter` first; drop-not-crash;
  local-first preserved; `STORYTIME_TELEMETRY=noop` default; the full test
  suite runs with no Docker, no internet, and no vendor credentials.
- No StoryTime application code, `pyproject.toml` dependency, or application
  test changed across Phase 8C or 8C.1.

**Phase 8 — Multi-Backend Telemetry Fan-Out — is complete.** Its three
sub-phases — 8A (Architecture Baseline Section 23 amendment), 8B / 8B.1 (local
multi-backend stack expansion + logs preflight cleanup), and 8C / 8C.1
(optional vendor export profiles) — are all locked. There is no Phase 8D.

Gate evidence at lock: the six Docker-free quality gates were re-run on the
locked archive — `uv sync --frozen --extra dev` OK; `uv run pytest -q`
**358 passed**; ruff, mypy (71 source files), and import-linter (2 contracts
kept) clean; `storytime doctor` healthy. The only carried caveat is **OI-22** —
the per-vendor Compose override merges and live vendor export are unverified in
the Docker-less build environment; this blocks no phase gate and is not a lock
prerequisite (the full suite is offline).

The next phase is **Phase 9A — Governance Baseline Amendment** (Security,
Licensing, and Governance planning). Phase 9 has not started.

## Phase 9A — Governance Baseline Amendment (candidate — authored, pending lock)

Amendment-authoring round output. **This is not a locked decision.** Recorded
here, clearly labeled as a pending-lock candidate, following the same
append-only-mirror convention used for the Phase 8A "amendment candidate"
entry above. RoundTable remains the source of truth.

Phase 9A authored an Architecture Baseline amendment **candidate** —
`docs/architecture-baseline.md` Section 24, "Governance Baseline (Trust
Envelope, Licensing, Fail-Closed Gating)". It is architecture/documentation
only and authorizes no implementation. Per the Phase Closure Protocol and the
precedent of the locked Phase 7C / 7C.1 §16 and Phase 8A §23 amendments,
Section 24 becomes a locked decision only after GPT-5.5 review, Gemini
critique, any required revision, and explicit user approval. Until then no
Phase 9B implementation may depend on it.

The candidate establishes, for the future Phase 9 governance work:

- **Not a legal rights-clearance engine.** StoryTime is a local-first
  portfolio/demo pipeline; it must never claim that it or any AI has *legally
  determined* copyright/public-domain status. The human operator is the
  source of truth for licensing decisions; the system records, preserves, and
  later enforces those decisions and does not replace legal judgment.
- **No legal automation / no legal hallucination.** Forbidden concepts —
  `legal_verified_by_llm`, `copyright_cleared_by_ai`, `compliance_score`,
  `rights_confidence_score`, `copyright_safe_score`, and any AI-generated
  legal assertion or model-inferred legal determination. No AI copyright
  classifier and no compliance scoring may be added.
- **Allowed source categories.** `CC0`, `US_PUBLIC_DOMAIN`,
  `EXPLICIT_PERMISSION`, `LOCAL_TEST_FIXTURE`. There is deliberately no
  `AMBIGUOUS` category — ambiguous material must resolve into an explicit
  decision state.
- **Disallowed/blocked source categories.** Copyrighted-without-permission,
  paywalled, private/personal, ambiguous-license (unless manually approved
  with notes), arbitrary scraping, and blocked-source-config matches.
  Ambiguous content fails closed unless explicitly operator-approved.
- **Fail-closed governance gate.** Phase 9B must verify an `APPROVED` Trust
  Envelope before TTS/audio synthesis or RSS publish; `BLOCKED`, `REJECTED`,
  `NEEDS_REVIEW`, `UNKNOWN`, missing, malformed, or unverifiable all fail
  closed before TTS and must not publish to RSS.
- **Trust Envelope.** A durable governance/audit record — not a legal
  opinion — represented in both the durable artifact envelope (the governance
  source of truth for portability/recovery) and a rebuildable SQLite
  projection for operational queries.
- **Canonical Trust Envelope schema.** The minimum Phase 9B schema is defined
  in `docs/architecture-baseline.md` §24.8 as canonical architecture law,
  including the `review_context_summary` field, the `license_type` value set
  (`CC0`, `US_PUBLIC_DOMAIN`, `EXPLICIT_PERMISSION`, `LOCAL_TEST_FIXTURE`,
  `BLOCKED`, `UNKNOWN`), and the `decision` value set (`APPROVED`, `REJECTED`,
  `BLOCKED`, `NEEDS_REVIEW`). Phase 9B may refine field names only for repo
  consistency and must preserve the semantics and enum sets.
- **Blocked-source policy.** Phase 9B implements a local, explicit,
  inspectable blocked-source config (expected `config/governance/
  blocked-sources.yaml`) — no cloud service, no remote blocklists, no
  scraping or auto-classification.
- **Secrets policy.** Reinforced — no real secrets committed; `.env` ignored;
  placeholders only in examples; environment-only credentials; no credentials
  in SQLite or artifact envelopes; no production secrets manager or CI/CD
  secrets in Phase 9.
- **Deletion/retention posture.** Honest local-first — deletion is a
  host-level filesystem operation; no cloud soft delete, no compliance
  shredder, no GDPR/CCPA compliance claim.
- **Telemetry/privacy carryover.** Phase 8 hygiene carried forward unchanged;
  any future governance telemetry may carry only bounded status metadata, not
  raw text, notes, review summaries, or secrets.
- **Public/demo disclaimers.** StoryTime is a local-first portfolio/demo
  project, not legal advice, not a production rights-clearance platform; the
  operator remains responsible; the demo uses CC0 / public-domain /
  explicit-permission / local-test-fixture content only.
- **Future legal-hallucination grep/regex gate.** Phase 9B should add a static
  grep/regex gate barring forbidden legal-certification language from docs,
  config, and implementation; governance docs that define the vocabulary are
  allowlisted.
- **Phase 10 dependency.** Phase 9B must deliver a parseable Trust Envelope, a
  stable UI-safe status enum (`APPROVED` / `REJECTED` / `BLOCKED` /
  `NEEDS_REVIEW`), and a rejected/blocked reason — with no legal overclaiming.
- **Phase 9 split.** Phase 9A (this amendment), Phase 9B (Minimal Trust
  Envelope Implementation), Phase 9C (Docs / Audit Polish if needed).

No application code, database schema, artifact envelope code, telemetry code,
configuration behaviour, test, or dependency was changed by Phase 9A. The
local-first baseline, the SQLite/artifact source-of-truth semantics, the
closed source-manifest schema (§6), the optional-telemetry invariant, and the
Phase 8 telemetry/privacy rules are all unchanged; §24 strengthens, never
weakens, them. When the user locks Section 24, this section should be
re-recorded (append-only) as a locked decision.

## Phase 9A — Governance Baseline Amendment — LOCKED (2026-05-24)

Locked-decision record. The Phase 9A Architecture Baseline amendment candidate
(`docs/architecture-baseline.md` Section 24 — Governance Baseline: Trust
Envelope, Licensing, Fail-Closed Gating) completed the Phase Closure Protocol
review sequence:

- Claude Opus 4.7 authored the candidate (the Phase 9A round above).
- GPT-5.5 reviewed the Phase 9A archive and found it docs-only and
  review-ready.
- Gemini reviewed the candidate and returned `SAFE WITH EDITS`. Most requested
  edits were already satisfied in the candidate archive (`review_context_
  summary` present; the Trust Envelope schema already in §24.8; the future
  grep/regex gate already in §24.14; the fail-closed-before-TTS/RSS rule
  already in §24.6). Two clarifications remained.
- The **Phase 9A.1 cleanup** folded the two clarifications into Section 24
  before lock: (1) the source-authorization-not-viewpoint rule (§24.5) —
  StoryTime governs source authorization, not viewpoint acceptability, and is
  not a content-moderation system; (2) the early fail-closed clarification
  (§24.6) — Phase 9B should check governance as early as practical while the
  hard before-TTS/audio/RSS block is unchanged.
- Phase 9A was **locked with explicit user approval (2026-05-24)**.

**Section 24 is now locked and canonical.** Phase 9B implementation may depend
on it. The governance rules, the canonical Trust Envelope schema (§24.8), and
the Phase 9A / 9B / 9C split are unchanged from the reviewed candidate apart
from the two folded-in Phase 9A.1 clarifications; only Section 24's status
block, the §24.16 closing precondition, and the §24.17 closing clause changed
from "candidate / pending lock" to "locked / accepted".

What is now canonical (Architecture Baseline Section 24):

- **StoryTime is not a legal rights-clearance engine.** The human operator is
  the source of truth for licensing decisions; the system records, preserves,
  and later enforces those decisions and never infers, computes, or certifies
  legal status. No legal automation, no legal-hallucination vocabulary, no AI
  copyright classifier, no compliance scoring.
- **Governance is source authorization, not viewpoint acceptability.**
  Sources are blocked or rejected for *how they were obtained or licensed*,
  never for *what they say*. StoryTime governance is not a content-moderation
  system — no topic-policy categories, no viewpoint screening, no content
  safety classification.
- **Allowed / disallowed source categories.** Allowed: `CC0`,
  `US_PUBLIC_DOMAIN`, `EXPLICIT_PERMISSION`, `LOCAL_TEST_FIXTURE` (no
  `AMBIGUOUS` category). Disallowed unless explicitly operator-approved:
  unlicensed copyright, paywalled, private/personal, ambiguous-license,
  arbitrary scraping, blocked-source-config matches.
- **Fail-closed governance gate.** Phase 9B must check governance as early as
  practical and must hard-block before TTS, audio processing, or RSS publish
  unless an `APPROVED` Trust Envelope exists; `BLOCKED`, `REJECTED`,
  `NEEDS_REVIEW`, `UNKNOWN`, missing, malformed, or unverifiable all fail
  closed.
- **Trust Envelope.** A durable governance/audit record — not a legal opinion.
  The durable artifact envelope is the governance source of truth; a
  rebuildable SQLite projection serves operational queries. The canonical
  minimum schema (§24.8) includes `review_context_summary` and
  `artifact_hash_refs`, with the `license_type` and `decision` enum value
  sets.
- **Blocked-source policy, secrets policy, deletion/retention posture,
  telemetry/privacy carryover, public/demo disclaimers, the future
  legal-hallucination grep/regex gate, and the Phase 10 dependency contract**
  are all canonical as recorded in §24.9–§24.15.

No application code, database schema, artifact envelope code, telemetry code,
configuration behaviour, test, or dependency was changed by Phase 9A or the
Phase 9A.1 cleanup. The local-first baseline, the SQLite/artifact
source-of-truth semantics, the closed source-manifest schema (§6), the
optional-telemetry invariant, and the Phase 8 telemetry/privacy rules are all
unchanged; §24 strengthens, never weakens, them.

**Phase 9A is complete and locked.** **Phase 9B — Minimal Trust Envelope
Implementation** has been implemented and delivered as a candidate (2026-05-24):
it implements the Section 24 governance law as the concrete `storytime.governance`
package, the durable Trust Envelope artifact, the `trust_envelope` SQLite
projection (schema v5), the fail-closed gate wired into `ingest` / `synthesize`
/ `publish`, the `config/governance/blocked-sources.yaml` deny-list, and the
static legal-hallucination gate. The **Phase 9B.1 cleanup** (2026-05-24)
hardened that static legal/compliance forbidden-term scanner — per Gemini's
`SAFE WITH MINOR CLEANUP` review — so it cannot crash on binary or generated
files or descend into virtualenv/cache/`runs`/`feed`/build directories; it
changed only the scanner, its test, and the State Preservation Bundle docs.
**Phase 9B is NOT yet locked** — per the Phase Closure Protocol it awaits
GPT-5.5 review, Gemini confirmation if needed, cleanup acceptance, and explicit
user approval before it can be recorded here as a locked phase. Until then this
section's last *locked* phase remains Phase 9A. Phase 9C — Docs / Audit Polish
— has not started.

## Phase 9B — Minimal Trust Envelope Implementation — LOCKED (2026-05-24)

**Phase 9B — Minimal Trust Envelope Implementation is locked.** It is the
implementation phase that turned the locked Architecture Baseline Section 24
governance law into working code. Phase 9B completed the Phase Closure
Protocol: implemented by Claude Opus 4.7; reviewed by GPT-5.5 (found ready for
Gemini review); critiqued by Gemini, which returned `SAFE WITH MINOR CLEANUP`
with one required item; the **Phase 9B.1 cleanup** applied that item and is
folded into this lock (see below); **locked with explicit user approval
(2026-05-24)**.

Locked Phase 9B decisions, now canonical:

- **The `storytime.governance` package** is the concrete artifact of Section
  24. It provides the Trust Envelope model and the canonical §24.8 closed JSON
  Schema, the durable Trust Envelope artifact, the local blocked-source
  configuration loader, the fail-closed governance gate, and the static
  legal-hallucination scanner.
- **The durable Trust Envelope artifact** (`governance/trust-envelope.json` in
  each run directory) is the governance source of truth for portability and
  recovery (§24.7). It is a separate durable JSON file linked from the run —
  deliberately not embedded in the ARCH-LOCKed `ArtifactEnvelope` shape.
- **The SQLite `trust_envelope` table** (schema migration `0005`, schema
  version 5) is a rebuildable projection of the durable artifact, carrying only
  bounded status fields. It is never the source of truth.
- **The fail-closed gate** is wired at three honest points: `ingest` derives
  the Trust Envelope from the human-written source manifest plus the local
  blocked-source list and checks it early; `synthesize` hard-blocks before TTS;
  `publish` hard-blocks before RSS. Only an explicit `APPROVED` Trust Envelope
  passes; `BLOCKED`, `REJECTED`, `NEEDS_REVIEW`, `UNKNOWN`, and a missing,
  malformed, or unverifiable envelope all fail closed (§24.6).
- **The Trust Envelope records a human decision.** It is derived by
  transcribing the operator's manifest-recorded licensing decision plus a
  deterministic local blocked-source lookup — never legal automation or model
  inference (§24.2 / §24.3).
- **The local blocked-source config** (`config/governance/blocked-sources.yaml`)
  is a committed, inspectable, human-curated deny-list (§24.9).
- **The static legal-hallucination gate** (`storytime.governance.legal_terms`)
  bars the §24.14 forbidden legal-certification vocabulary from code, config,
  and non-governance docs, allowlisting the governance documents that define
  that vocabulary.
- Phase 9B changed no ARCH-LOCKed contract — the `ArtifactEnvelope` shape,
  `BASE_STAGE_ORDER`, the stage and DTO boundaries, and the append-only
  `event_log` model are all unchanged. It added no legal automation, AI
  copyright classifier, compliance scoring, authentication, scraping, or hosted
  service. `pyyaml` was promoted to a runtime dependency because the §24.9
  config is YAML.

**The Phase 9B.1 cleanup is folded into this lock.** Phase 9B.1 was the
targeted cleanup applying Gemini's single `SAFE WITH MINOR CLEANUP` item: it
hardened the static legal/compliance forbidden-term scanner so it cannot crash
on binary or generated files (SQLite databases, audio, images, archives,
compiled caches) or descend into virtualenv/cache/`runs`/`feed`/build
directories. The hardened scanner walks the tree deterministically with an
explicit ignored-directory prune set, reads only an allowlist of text
extensions, and reads with `errors="replace"` so invalid UTF-8 can never raise.
Phase 9B.1 changed only the scanner, its test, and the State Preservation
Bundle docs; it touched no Trust Envelope architecture, no SQLite schema, no
pipeline gate semantics, and not `docs/architecture-baseline.md`. It is
accepted as part of the Phase 9B lock.

Phase 9B did not amend the Architecture Baseline — Section 24 was already
locked law and Phase 9B implements it exactly. The full test suite is **418
passing** and all six Docker-free quality gates pass.

**Phase 9B is locked. The next phase is Phase 10 — Product UI / Operator
Experience (§24.15).** Phase 10 has not started. Phase 9C — Docs / Audit
Polish — was an optional follow-up and is not scheduled; the lock closure
supersedes it as the next step.

## Phase 10A — Operator Experience Baseline Amendment (candidate — authored, pending lock)

Amendment-authoring round output. **This is not a locked decision.** Recorded
here, clearly labeled as a pending-lock candidate, following the same
append-only-mirror convention used for the Phase 8A and Phase 9A "amendment
candidate" entries above. RoundTable remains the source of truth.

Phase 10A authored an Architecture Baseline amendment **candidate** —
`docs/architecture-baseline.md` Section 25, "Operator Experience Baseline". It
is architecture/documentation only and authorizes no implementation. Per the
Phase Closure Protocol and the precedent of the locked Phase 7C / 7C.1 §16,
Phase 8A §23, and Phase 9A §24 amendments, Section 25 becomes a locked decision
only after GPT-5.5 review, Gemini critique, any required revision, and explicit
user approval. This candidate state was superseded by the Phase 10A lock; Phase 10B may now be scoped under locked Section 25.

The candidate establishes, for the future Phase 10 operator-experience work:

- **Operator experience goal.** Phase 10 makes StoryTime understandable,
  operable, and demoable by a single local human operator — without turning it
  into a premature SaaS product. There is one operator role, on one host; no
  multi-user, account, or tenant personas.
- **Read-only-first rule.** Phase 10 begins with read-only (or at most
  mostly-read-only) visibility into existing state. State mutation remains
  CLI/pipeline-controlled. The operator surface shows what happened before it
  may ever change what happens.
- **Source-of-truth rule.** SQLite and the on-disk artifact files remain the
  source of truth; the durable Trust Envelope artifact remains governance
  truth (§24.7). Operator reports/UI read from them and are never themselves
  authoritative; observability dashboards are links/views, not truth.
- **Governance display rule.** Phase 10 surfaces may display bounded
  governance fields (source/run IDs, pipeline status, the §24.8 governance
  `decision` and `license_type` enums, approver, approval timestamp, a bounded
  `review_context_summary`, Trust Envelope and artifact paths, a structured
  blocked/rejected reason, observability links). They must not display
  legal/compliance overclaiming language (extending the §24.3 / §24.14
  forbidden vocabulary), and every governance surface carries a standing
  "record of a human operator decision and pipeline state, not legal advice or
  certification of copyright safety" disclaimer.
- **Viewpoint neutrality carryover.** The locked §24.5 rule is preserved:
  StoryTime governs source authorization, not viewpoint acceptability. Phase 10
  surfaces add no topic categories, viewpoint screening, or content-moderation
  labels.
- **Phase 10B target.** The recommended and accepted first Phase 10
  implementation phase is Phase 10B — a generated, static, local, read-only
  HTML operator report built from existing SQLite state and artifact
  envelopes.
- **Phase 10B hard floor.** At minimum a generated report directory
  (`operator-report/index.html`, `runs.html`, `run-<run_id>.html`) with a
  latest-runs summary, a run list, and a single-run detail page covering
  stages, governance detail, artifact paths, failure status, and observability
  links.
- **Phase 10B hard ceiling.** No interactive mutation, forms, state-changing
  buttons, approval/retry/delete workflow, server process, live telemetry
  polling, websockets, frontend framework, asset build pipeline, auth/login,
  cloud/hosted service, responsive design system, theme system, animations,
  dashboard recreation, embedded telemetry charts, or full visual-polish pass.
  Skeleton HTML plus minimal static CSS only.
- **Report data model + field allowlist/blacklist.** A deterministic report
  data model with explicit field sources is defined; a field-level allowlist
  (bounded status fields) and blacklist (raw story/narration text,
  transcripts, secrets, long free-text notes, raw telemetry, embedded
  dashboard data, unbounded exception text) bound report output.
- **Bounded `review_context_summary`.** Displayed only as a short governance
  rationale, capped (Phase 10B bound: 500 characters, testable and refinable
  only if the privacy guarantee is preserved), with a safe placeholder when
  absent and safe truncation when over the bound.
- **Observability link rule.** Observability links are optional references
  only — no embedded dashboard data, no credentials, no secrets/tokens in
  URLs, not a source of truth; the report is complete without them.
- **Determinism / snapshot tests.** Phase 10B must be deterministic enough to
  test — identical/normalized-identical output for identical fixture input,
  with snapshot/golden-output tests or an equivalent strategy.
- **Privacy / no-raw-content tests + governance-copy linting.** Phase 10B must
  prove, by test, that the report contains no raw story text, narration,
  transcripts, secrets, long free-text notes, or forbidden legal/compliance
  overclaiming phrases, and must apply the §24.14 static scanner (or an
  equivalent) to its templates and generated copy.
- **No auth / cloud / server, mutation gate, stop/revert criterion.** Phase
  10B introduces no auth/users/roles, no login/sessions, no hosted backend or
  cloud, no server-side report runtime; it displays past decisions and creates
  none. Any mutation UI is a separate future gated phase. If Phase 10B
  introduces auth, cloud, hosted services, a server runtime, a mutation UI,
  raw-content display, or legal/compliance overclaiming, it must stop and
  return for re-scoping before lock.
- **Phase 10 split.** Phase 10A (this amendment), Phase 10B (Generated Local
  HTML Operator Report — first likely build), Phase 10C (Operator CLI Helpers
  / Failure Queue — future, only if needed), Phase 10D (Optional Local Web
  Dashboard — future, only if still justified). 10C and 10D are not authorized
  by this amendment.

No application code, database schema, artifact envelope code, Trust Envelope
semantics, governance gate behaviour, telemetry behaviour, configuration
behaviour, test, or dependency was changed by Phase 10A. The local-first
baseline, the SQLite/artifact source-of-truth semantics, the §24 governance
law, and the Phase 8 telemetry/privacy rules are all unchanged; §25 builds on
them and strengthens, never weakens, the §24.15 Phase 10 dependency contract.
When the user locks Section 25, this section should be re-recorded
(append-only) as a locked decision.


## Phase 10A — Operator Experience Baseline Amendment locked (2026-05-24)

Locked-decision record. Phase 10A — Operator Experience Baseline Amendment is now **locked / accepted / canonical** with explicit user approval.

The locked architecture law is `docs/architecture-baseline.md` Section 25, "Phase 10A Amendment — Operator Experience Baseline". It defines the operator-experience goal, read-only-first rule, source-of-truth rule, governance display rule, viewpoint-neutrality carryover, report field allowlist/blacklist, bounded `review_context_summary` rule, observability-link rule, static-only/no-server rule, no-auth/cloud/SaaS rule, mutation gate, Phase 10B hard floor and hard ceiling, report data model/schema, determinism/snapshot-test rule, privacy/no-raw-content test requirements, governance-copy linting, performance/size guardrail, Phase 10B handoff, and stop/revert criterion.

Lock basis:

- Claude Opus 4.7 authored the Phase 10A candidate as documentation-only.
- GPT-5.5 verified the candidate archive against the Phase 9B locked bundle: no code, schema, configuration, dependency, template, CLI, report-generator, HTML, CSS, or UI implementation delta; Phase 10B remained not started.
- Gemini 3.1 Pro reviewed the candidate and returned **SAFE TO LOCK (PENDING VERIFICATION)**.
- GPT-5.5 satisfied Gemini's pending-verification condition.
- The user explicitly approved the Phase 10A lock.

Gemini's mention of possible lightweight local-web-server alternatives was treated as general commentary, not accepted as Phase 10B authorization. The locked Phase 10B target remains **Generated Local HTML Operator Report**: static, local-file based, read-only, no server runtime, no auth, no cloud, no frontend framework, no mutation UI.

**Current state after this lock:** Phase 10A is locked. Phase 10B — Generated Local HTML Operator Report — is next and has not started. Phase 10C and Phase 10D remain future, conditional, and not started. Phase 9C remains optional/not scheduled.

## Phase 10B — Generated Local HTML Operator Report (implementation output produced; superseded by lock record — 2026-05-24)

Implementation output for **Phase 10B — Generated Local HTML Operator Report**,
the first implementation phase of Phase 10. Per the Phase Closure Protocol
Historical implementation-candidate record. This entry was superseded by the Phase 10B lock record below after GPT-5.5 verification, Gemini critique, and explicit user approval.

Phase 10B implements the locked Architecture Baseline Section 25
operator-experience law as a generated, static, local, read-only HTML operator
report. It changes no governance, telemetry, or pipeline behaviour, adds no
dependency, and makes no database schema change.

Implementation output (pending lock):

- **New `storytime.reporting` package.** Five modules: `model.py` (the
  deterministic §25.11 report data model — frozen dataclasses, pure data, no
  raw-content fields); `collect.py` (builds the model from existing state
  only — the SQLite `pipeline_run` / `stage_execution` / `stage_artifact` /
  `trust_envelope` / `published_episode` projections plus the durable Trust
  Envelope artifact); `render.py` (pure standard-library HTML rendering — no
  Jinja2, no template dependency); `generate.py` (collect → render → write
  static files); `__init__.py`.
- **`storytime report generate` CLI command.** A new Typer sub-app (`report`)
  with one command, `generate`, accepting `--output` (default
  `operator-report/`). It reads the SQLite state database and on-disk
  artifacts and writes `index.html`, `runs.html`, one `run-<run_id>.html` per
  run, and a single local `style.css`. It starts no server and mutates no
  state.
- **Read-only, static, air-gapped report.** The generated report is viewable
  directly from local files with no web server. It has no JavaScript, no
  form, no button, and no state-changing control (§25.10 / §25.17). All
  styling is one small local `style.css`; there are no external CDN links,
  fonts, scripts, icons, or remote favicons — the report renders with no
  network connection.
- **Bounded governance display.** The report shows the §25.12 allowed fields
  only — `run_id`, run/stage statuses, the §24.8 governance `decision` and
  `license_type` enums, approver, timestamps, a structured blocked/rejected
  reason, artifact path references, and optional observability links. The
  Trust Envelope's `review_context_summary` is displayed bounded to 500
  characters (the §25.13 locked length), safely truncated with a visible
  indicator; the free-text `governance_notes` field is never projected. Every
  governance page carries the §25.5 disclaimer; no legal/compliance
  overclaiming vocabulary appears.
- **Observability links are optional references only.** A Jaeger trace link is
  built only when `STORYTIME_JAEGER_BASE_URL` is configured and a run has a
  recorded trace id; the link embeds no dashboard data and no secret. With
  nothing configured the report is still complete. No observability backend
  is queried.
- **Deterministic.** Report generation takes an injected timestamp; given
  identical state and an identical timestamp the generated HTML is
  byte-for-byte identical. The CLI supplies the real time; tests supply a
  fixed timestamp.
- **Tests.** New `tests/test_operator_report.py` — 19 tests: the three run
  shapes (completed, governance-blocked, failed) generate; no raw story text,
  narration, transcripts, secrets, or long free-text governance notes reach
  the HTML; no forbidden legal/compliance phrases appear (reusing the locked
  `FORBIDDEN_LEGAL_TERMS` set); byte-for-byte determinism; optional sanitized
  observability links; no external CDN/fonts/scripts/assets; no mutation of
  state; the CLI command writes the report and is discoverable.
- **Import boundary.** `storytime.reporting` was added to both import-linter
  contracts — the OpenTelemetry-confinement contract and the events-leaf
  contract — strengthening, never weakening, them.

Invariants preserved: local-first; SQLite + the on-disk artifact envelopes (and
the durable Trust Envelope) remain the source of truth — the generated report
is a view, never authoritative; `STORYTIME_TELEMETRY=noop` default; no
ARCH-LOCKed contract changed; no database schema change; no new dependency; no
auth, cloud, server runtime, persistent backend, frontend framework, build
pipeline, or mutation UI. Six Docker-free quality gates pass — 437 tests (19
new), ruff / mypy (83 source files, strict) / import-linter (2 contracts kept)
clean, `storytime doctor` healthy; the legal-hallucination scanner returns zero
violations. One documented limitation: the SQLite projections record the
published audio path per episode but not a per-run RSS feed path (the feed is
the shared `feed/feed.xml`); the report surfaces the audio path and references
the shared feed for a run that published — closing that gap would need a schema
change, which Phase 10B deliberately does not make.

*(Historical candidate status — superseded by the Phase 10B lock record below.)*


## Phase 10B — Generated Local HTML Operator Report locked (2026-05-24)

Locked-decision record. Phase 10B — Generated Local HTML Operator Report is now **locked / accepted / canonical** with explicit user approval.

Phase 10B implements the locked Architecture Baseline Section 25 operator-experience law as a generated, static, local, read-only operator report. The implementation adds:

- `storytime.reporting` data/model/collection/rendering/generation modules.
- `storytime report generate` CLI command.
- Static report output: `index.html`, `runs.html`, per-run `run-<run_id>.html`, and local `style.css`.
- Air-gapped HTML constraints: no CDN, no external fonts, no external scripts, no tracking, no remote assets.
- Deterministic timestamp/clock override for byte-for-byte stable tests.
- Reporting import-boundary guard so the reporting layer does not import OpenTelemetry.
- Phase 10B tests covering completed, governance-blocked, failed, privacy, legal-copy, external-asset, determinism, observability-link, and no-mutation constraints.

Lock basis:

- Claude Opus 4.7 implemented the Phase 10B candidate from `storytime-phase10a-locked-state-bundle.tar.gz`.
- GPT-5.5 verified the implementation archive and generated a Gemini review package.
- Gemini 3.1 Pro reviewed the Phase 10B implementation evidence packet and returned **SAFE TO LOCK**.
- The user explicitly approved the Phase 10B lock.

Confirmed constraints:

- No server runtime.
- No auth, users, roles, sessions, or SaaS surface.
- No cloud/hosted dependency.
- No frontend framework or asset build pipeline.
- No mutation UI.
- No raw story text, narration text, transcripts, secrets, or long governance notes in the report.
- No legal/compliance overclaiming.
- Observability links are optional references only, not source of truth.
- SQLite and artifact files remain authoritative; generated HTML is a view only.

**Current state after this lock:** Phase 10B is locked. Phase 10C — Operator CLI Helpers / Failure Queue — is optional and not started. Phase 10D — Optional Local Web Dashboard — is future/conditional and not started. Phase 9C remains optional/not scheduled.

Dependency accuracy note: Gemini's review message accidentally referred to a Jinja2 dependency. The locked record corrects that fact: Phase 10B added **no Jinja2** and **no new dependency**; HTML rendering uses the Python standard library and `html.escape`, and `uv.lock` remained byte-identical to Phase 10A.

## Phase 10C — Operator CLI Helpers / Failure Queue (historical implementation-candidate entry; superseded by lock record below — 2026-05-25)

Implementation output for **Phase 10C — Operator CLI Helpers / Failure Queue**.
Per the Phase Closure Protocol Phase 10C is **not** a locked decision until
GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval; it is
recorded here as a clearly-labeled pending-lock entry, following the precedent
of earlier implementation phases.

Phase 10C implements the locked Architecture Baseline Section 25
operator-experience law as a read-only command-line failure / review queue. It
changes no governance, telemetry, or pipeline behaviour, makes no database
schema change, and adds no dependency.

Implementation output (pending lock):

- **New `storytime.operator_queue` module.** A single standard-library module:
  the `QueueItem` bounded projection dataclass; `collect_queue` (a deterministic
  semantic query over the existing SQLite `pipeline_run` / `stage_execution` /
  `trust_envelope` state); `render_table` (plain-text terminal output) and
  `render_json` (deterministic, allowlisted JSON).
- **`storytime queue` CLI command.** A new read-only command with `--status`,
  `--run-id`, `--limit`, and `--json` flags. It surfaces the runs that need
  operator attention — failed, blocked by governance, marked needs-review, or
  awaiting an operator approval decision — with, for each run, why it needs
  attention and which existing command, report, or artifact to inspect next.
- **Queue is a view, not a broker.** The "queue" is an operator-facing filtered
  view of existing run state — a dead-letter / review-queue view. It adds no
  message broker, no background worker, no new queue storage, no new run state,
  and no `pop` / `dequeue` / `claim` / `ack` behaviour. It is read-only: it
  mutates nothing and runs no other command.
- **Bounded, deterministic.** `--limit` defaults to 20 (there is no unlimited
  option); results are sorted most-recently-updated-first with the run id as a
  stable tie-breaker; the output carries no generation timestamp, so human and
  JSON output are byte-for-byte deterministic for identical state.
- **Bounded fields only.** The queue surfaces only structured fields — run and
  stage identifiers and statuses, the §24.8 governance decision enum, the
  structured stage `error_kind` code, a coarse failure category, timestamps,
  the deterministic Phase 10B report-detail-page path, and the Trust Envelope
  artifact path. It never surfaces raw story text, narration, transcripts,
  secrets, long free-text governance notes, unbounded `error_message` text,
  or raw telemetry; for a failed stage it shows the structured `error_kind`
  only, and for a governance decision the decision enum only — never the
  free-text `blocked_reason`. JSON uses an explicit 11-field allowlist. No
  legal/compliance overclaiming vocabulary appears; the `next_hint` is always
  a cautious suggestion pointing at an existing command.
- **Tests.** New `tests/test_operator_queue.py` — 29 tests: queue membership
  across five run shapes; the empty state; `--status` / `--run-id` filtering;
  the bounded default limit and a rejected non-positive limit; deterministic
  most-recently-updated-first sorting; deterministic allowlisted JSON; no raw
  story text, narration, secret, or free-text-reason leakage; no forbidden
  legal/compliance phrase (reusing the locked `FORBIDDEN_LEGAL_TERMS` set);
  the non-mutating `next_hint`; and that the command neither mutates state nor
  requires report generation.
- **Import boundary.** `storytime.operator_queue` was added to both
  import-linter contracts — the OpenTelemetry-confinement contract and the
  events-leaf contract — strengthening, never weakening, them.

Invariants preserved: local-first; SQLite plus the on-disk artifact envelopes
(and the durable Trust Envelope) remain the source of truth — the queue is a
view, never authoritative; no ARCH-LOCKed contract changed; no database schema
change; no new dependency; no web server, dashboard, frontend framework, auth,
cloud, persistent backend, message broker, background worker, terminal-UI
dependency, or mutation workflow. Six Docker-free quality gates pass — 466
tests (29 new), ruff / mypy (84 source files, strict) / import-linter (2
contracts kept) clean, `storytime doctor` healthy; the legal-hallucination
scanner returns zero violations.

*(Historical status — superseded by the Phase 10C lock record below.)*

## Phase 10C — Operator CLI Helpers / Failure Queue locked (2026-05-25)

Locked-decision record. Phase 10C — Operator CLI Helpers / Failure Queue is now **locked / accepted / canonical** with explicit user approval.

Phase 10C implements the locked Architecture Baseline Section 25 operator-experience law as a read-only command-line failure / review queue. The implementation adds:

- `storytime.operator_queue` module — the `QueueItem` bounded projection, `collect_queue` semantic query, `render_table` and `render_json` output.
- `storytime queue` read-only CLI command — `--status`, `--run-id`, `--limit`, `--json` flags.
- 29 tests in `tests/test_operator_queue.py`.
- `docs/operator-queue.md` operator guide.

The queue is a semantic projection over existing SQLite and Trust Envelope state. It adds no broker, background worker, new queue storage, new lifecycle state, pop/dequeue/claim/ack behaviour, mutation API, or unsafe operator action.

Lock basis:

- Claude Opus 4.7 implemented the Phase 10C candidate.
- GPT-5.5 Thinking review: PASS with minor state-hygiene observation.
- Gemini/Flash Light independent critique: SAFE TO LOCK.
- User explicitly approved the Phase 10C lock.

Confirmed gate results: 466 tests passing, ruff clean, mypy clean (84 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy, legal scanner 0 violations.

Confirmed constraints: no broker; no background worker; no new queue storage; no new lifecycle state; no server; no dashboard; no frontend framework; no auth; no cloud; no mutation API; no raw content display; no legal overclaiming; no new dependency; no database schema change; no ARCH-LOCKed contract change. SQLite and artifact files remain authoritative; the queue is a read-only view.

**Current state after this lock:** Phase 10A, Phase 10B, and Phase 10C are all locked. Phase 10D — Pipeline Re-Run / Mutation Actions — has not started. Phase 9C remains optional/not scheduled. *(Historical status before Phase 10D implementation; superseded by Phase 10D implementation candidate entry below.)*

## Phase 10D — Pipeline Re-Run / Mutation Actions (locked — 2026-05-25)

Implementation round. Phase 10D implements StoryTime's first operator *mutation* surface under the locked Architecture Baseline Section 25 operator-experience law. Per the Phase Closure Protocol this is implementation output — a candidate, **not** a locked phase. GPT-5.5 and Gemini/Flash Light each reviewed the Phase 10D implementation artifact and returned **SAFE WITH EDITS** — implementation safe, docs/state-preservation cleanup required before lock. The required edit is docs/state-preservation cleanup only (Phase 10D.1); the Phase 10D code and mutation implementation should not change.

Phase 10D adds the `storytime rerun` command: a governed, bounded, audited re-run of a failed pipeline run. The implementation adds:

- `storytime.operator_rerun` module — the `RerunDecision` / `RerunResult` bounded dataclasses, `evaluate_rerun_eligibility` (a pure-ish decision function over the existing SQLite run / stage / Trust Envelope state), `perform_rerun` (the single bounded mutation plus audit event), and `render_rerun_text` / `render_rerun_json` output.
- `storytime rerun` CLI command — `--from-stage`, `--dry-run`, `--json` flags.
- `EventType.RUN_RERUN_REQUESTED` — the audit event written to the existing append-only `event_log` for every actual re-run mutation. The `event_log` table stores `event_type` as a string; adding the enum value is not a database schema change.
- 27 tests in `tests/test_operator_rerun.py`.
- `docs/operator-rerun.md` operator guide.

Mutation semantics: when a re-run proceeds, the entire mutation is a single bounded status reset — a failed run's `pipeline_run.status` is reset from `failed` to the existing resumable `running` state, so the existing `storytime run --resume` path can re-execute it from the failed stage. The `rerun` command runs no pipeline work itself. No new run lifecycle state and no new database column are introduced.

Eligibility / safety model: a re-run proceeds only when the run exists, is `failed` because of a genuine pipeline-stage failure (not an operator approval-gate rejection), and carries an `APPROVED` Trust Envelope. A missing Trust Envelope, a `BLOCKED` / `REJECTED` / `NEEDS_REVIEW` decision, an operator gate rejection, an unknown `--from-stage`, a `--from-stage` that is not the failed stage, or an unclassifiable state all yield a rejection with a stable decision code. The decision defaults to rejection whenever safety cannot be proven, and a re-run never bypasses governance.

Audit: every actual mutation is recorded as a `RunRerunRequested` event in the append-only `event_log`, with a bounded payload (mutation id, from-stage, previous/new status, governance decision, dry-run flag) — no raw content. A dry run and a rejected attempt write no event.

Confirmed gate results: 493 tests passing (27 new), ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy, legal scanner 0 violations.

Confirmed constraints: no message broker; no background worker; no daemon; no scheduler; no long-running process; no server; no dashboard; no frontend framework; no authentication; no cloud dependency; no new queue storage; no new run lifecycle state; no new database column; no database schema change; no ARCH-LOCKed contract change; no new dependency. The Phase 10C read-only queue is unchanged. SQLite and artifact files remain authoritative.

**Current state after this round (Phase 10C.1 / Phase 10D.1):** Phase 10A, Phase 10B, Phase 10C, Phase 10C.1, Phase 10D, and Phase 10D.1 are all locked. Phase 10E — Static HTML Operator Report Refinement — is an implementation candidate, pending review, **not locked**. Phase 10F has not started. Phase 9C remains optional/not scheduled.

*(The 'Phase 10D not locked' status in the line immediately above was superseded when Phase 10D and Phase 10D.1 were locked; see the Phase 10E implementation candidate entry below.)*

## Phase 10E — Static HTML Operator Report Refinement (implementation candidate, reviewed SAFE WITH EDITS — Phase 10E.1 cleanup required — not locked — 2026-05-25)

Implementation round. Phase 10E refines the existing generated static HTML operator report under the locked Architecture Baseline Section 25 operator-experience law. GPT-5.5 and Gemini/Flash Light each reviewed the Phase 10E implementation artifact and returned **SAFE WITH EDITS** — implementation safe; three cleanup items required before lock. Phase 10E.1 addressed: (1) blocked_reason redaction (partial — full-phrase fix in v2), (2) archive pollution, (3) state-preservation sync. Phase 10E.2 final cleanup (v2) completes the full-phrase render fix.

Phase 10E adds: executive status summary, Phase 10D rerun eligibility / action guidance, bounded failure summary, command reference section, semantic status badges, improved governance warning block, embedded `<style>` per page, improved responsive CSS. No JavaScript. No external assets. No browser-side mutation controls. No backend mutation behavior changed. No database schema changed. No new dependencies. 18 new report-safety tests; all six Docker-free gates pass.

**Current state after this round (Phase 10E):** Phase 10A, Phase 10B, Phase 10C, Phase 10C.1, Phase 10D, and Phase 10D.1 are all locked. Phase 10E — Static HTML Operator Report Refinement — is an implementation candidate, reviewed SAFE WITH EDITS, Phase 10E.1 cleanup required, **not locked**. Phase 10F has not started. Phase 9C remains optional/not scheduled.

*(Phase 10E.1 — Redaction, Artifact Hygiene, and State Preservation Cleanup — produced as cleanup artifact; see Phase 10E.1 entry below.)*

## Phase 10E.1 — Redaction, Artifact Hygiene, and State Preservation Cleanup (cleanup output — pending review — not a feature phase) — 2026-05-25

Cleanup pass. Addresses the three lock-blocking issues found by GPT-5.5 and Gemini/Flash Light reviews:
(1) raw governance `blocked_reason` text was rendered in the static HTML report — replaced with required safe wording ("Decision detail: blocked by governance policy; inspect Trust Envelope locally if authorized.");
(2) `.mypy_cache`, `.ruff_cache`, and `runs/state.db` runtime/cache artifacts were present in the source archive — excluded from output archive;
(3) state-preservation documentation was partially desynchronized — first-read docs now consistently reflect Phase 10E candidate status with Phase 10E.1 cleanup in progress.

No application mutation behavior changed. No JavaScript added. No external assets added. No database schema changed. No new dependencies. All six Docker-free gates pass.

**Current state after this round:** Phase 10A, Phase 10B, Phase 10C, Phase 10C.1, Phase 10D, and Phase 10D.1 are all locked. Phase 10E — Static HTML Operator Report Refinement — is an implementation candidate, Phase 10E.1 cleanup produced, pending Phase 10E lock review. Phase 10F has not started. Phase 9C remains optional/not scheduled.

## Phase 10E.2 — Final Cleanup v2 (render.py full-phrase fix + state-preservation sync — pending Phase 10E lock review) — 2026-05-25

Surgical cleanup. Two fixes: (1) render.py governance section now renders the exact required full phrase "Decision detail: blocked by governance policy; inspect Trust Envelope locally if authorized." as a single value string in the "Governance detail" table row — the full phrase appears as one report-visible string, not split across a header and a partial value; (2) state-preservation docs updated to reference Phase 10E.2 artifact. No application code changed beyond render.py. No JavaScript. No external assets. No mutation behavior changed. 512 tests pass; ruff clean.

**Current state after this round:** Phase 10A, Phase 10B, Phase 10C, Phase 10C.1, Phase 10D, and Phase 10D.1 are all locked. Phase 10E — Static HTML Operator Report Refinement — is an implementation candidate, Phase 10E.2 final cleanup produced, pending Phase 10E lock review. Phase 10F has not started. Phase 9C remains optional/not scheduled.

## Phase 10E — Static HTML Operator Report Refinement (LOCKED / ACCEPTED / CANONICAL — 2026-05-25)

Lock closure. Phase 10E — Static HTML Operator Report Refinement — is locked, accepted, and canonical, with the Phase 10E.1 / 10E.2 cleanup sequence accepted and the Phase 10E.2 normalized cleanup as the canonical state. Lock archive: `storytime-phase10e2-final-cleanup-v2-normalized.tar.gz`, SHA-256 `87fad92b2e0a919a81588f4c628ccfdf08860571fdc778c527d8fe93c30b7dec`.

Phase 10E refined the existing generated static HTML operator report under the locked Architecture Baseline Section 25 operator-experience law: an executive status summary, Phase 10D rerun eligibility / action guidance, a bounded failure summary, a contextual command reference section, semantic status badges, an improved governance warning block, and improved embedded CSS. The report remains a local, static, read-only artifact — no JavaScript, no external assets, no browser-side mutation controls, no backend behavior change, no database schema change, no new dependency. The Phase 10E.1 / 10E.2 cleanup sequence addressed the review findings: raw `blocked_reason` redaction (the report shows the required safe wording "Decision detail: blocked by governance policy; inspect Trust Envelope locally if authorized."), archive hygiene, and state-preservation synchronization. Phase 10E was reviewed and locked with explicit user approval.

**Current state after this round:** Phase 10A, Phase 10B, Phase 10C, Phase 10C.1, Phase 10D, Phase 10D.1, and Phase 10E (with the 10E.1 / 10E.2 cleanup sequence) are all locked. Phase 10F has not started before the Phase 10F implementation round below. Phase 9C remains optional/not scheduled.

## Phase 10F — Demo Seed Data / Golden Path Fixtures (implementation candidate — pending review — not locked — 2026-05-25)

Implementation round. Phase 10F is demo-readiness / fixture-design work under the locked Architecture Baseline Section 25 operator-experience law. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 10F awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval.

Phase 10F adds the `demo/` directory: four original CC0 demo seed texts with schema-valid source manifests (`demo/seed/`), a demo-only blocked-source deny-list (`demo/governance/demo-blocked-sources.yaml`), and six fixture definitions plus an index (`demo/fixtures/`) — scenarios STF-10F-01 through STF-10F-06: successful golden path, retryable technical failure, governance-blocked source, needs-review / approval-gate run, rerun-requested run, and completed-after-rerun run. It adds the `docs/demo.md` operator demo runbook and `tests/test_demo_fixtures.py`.

Every fixture exercises the real existing system. The governance-blocked scenario supplies a demo-only deny-list for one run through the existing `STORYTIME_BLOCKED_SOURCES` mechanism (Architecture Baseline §24.9); it changes no enforcement code and no committed configuration — `config/governance/blocked-sources.yaml` stays empty. The re-run fixtures reference the existing Phase 10D `storytime rerun` semantics unchanged. A governance `NEEDS_REVIEW` decision is not reachable through the normal local manifest path (the closed manifest licence enum maps only to `APPROVED`); the needs-review fixture uses the operator text approval gate and documents that limitation rather than inventing a workflow.

Confirmed constraints: no new product feature; no UI; no server; no dashboard; no browser mutation control; no JavaScript; no external assets; no CDN; no generated audio committed; no large binary artifact; no runtime database or cache artifact packaged; no message broker; no background worker; no new dependency; no database schema change; no change to pipeline behaviour, `storytime rerun` behaviour, or Trust Envelope enforcement; no ARCH-LOCKed contract change. The demo seed texts are original CC0 fixture content.

Confirmed gate results: 549 tests passing (37 new), ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy, legal-hallucination scanner 0 violations.

**Current state after this round (Phase 10F):** Phase 10A, Phase 10B, Phase 10C, Phase 10C.1, Phase 10D, Phase 10D.1, and Phase 10E (with the 10E.1 / 10E.2 cleanup sequence) are all locked. Phase 10F — Demo Seed Data / Golden Path Fixtures — is an implementation candidate, pending review, **not locked**. Phase 10G has not started. Phase 9C remains optional/not scheduled.

## Phase 10F — Demo Seed Data / Golden Path Fixtures (LOCKED / ACCEPTED / CANONICAL — 2026-05-25)

Lock closure. Phase 10F — Demo Seed Data / Golden Path Fixtures — is locked, accepted, and canonical with explicit user approval. Lock archive: `storytime-phase10f-demo-seed-data-golden-path-fixtures.tar.gz`, SHA-256 `e060570a94fb19f790c539542b3ef7445111430bc308668675548f66fa48df55`.

Phase 10F was demo-readiness / fixture-design work under the locked Architecture Baseline Section 25 operator-experience law. It added the `demo/` directory — four original CC0 demo seed texts with schema-valid source manifests (`demo/seed/`), a demo-only blocked-source deny-list (`demo/governance/demo-blocked-sources.yaml`), and six fixture definitions plus an index (`demo/fixtures/`, scenarios STF-10F-01 through STF-10F-06: successful golden path, retryable technical failure, governance-blocked source, needs-review / approval-gate run, rerun-requested run, completed-after-rerun run) — together with the `docs/demo.md` operator demo runbook and `tests/test_demo_fixtures.py`. Every fixture exercises the real existing system; the governance-blocked scenario supplies a demo-only deny-list for one run through the existing `STORYTIME_BLOCKED_SOURCES` mechanism (§24.9), changing no enforcement code and no committed configuration. Phase 10F added no product feature, no UI, no server, no dashboard, no browser mutation control, no JavaScript, no external assets, no generated audio, no new dependency, no database schema change, and no change to pipeline / `storytime rerun` / Trust Envelope enforcement behaviour. Phase 10F completed the Phase Closure Protocol — implementation, GPT-5.5 review, Gemini critique, and explicit user approval.

**Current state after this round:** Phase 10A, Phase 10B, Phase 10C, Phase 10C.1, Phase 10D, Phase 10D.1, Phase 10E (with the 10E.1 / 10E.2 cleanup sequence), and Phase 10F are all locked. Phase 10G has not started before the Phase 10G implementation round below. Phase 9C remains optional/not scheduled.

## Phase 10G — Portfolio Narrative / Phase 10 Closure (implementation candidate — pending review — not locked — 2026-05-25)

Implementation round. Phase 10G is a documentation, portfolio-narrative, demo-explanation, and Phase 10 closure round under the locked Architecture Baseline Section 25 operator-experience law. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 10G awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 10 itself is **not** marked closed by this round — Phase 10 is closed only after the Phase 10G review completes and the user locks it.

Phase 10G turns the completed Phase 10 operator-experience layer into a clear, honest, professional demo/portfolio story and formally prepares Phase 10 for closure. It adds eight Phase 10 portfolio/closure documents: `docs/portfolio-narrative.md` (what StoryTime is, why it matters, and what the Phase 10 work demonstrates), `docs/demo-script.md` (a step-by-step presentation demo script using only real existing commands), `docs/operator-experience-walkthrough.md` (how the report, queue, and rerun surfaces compose), `docs/command-reference.md` (the operator CLI with explicit read-only vs. mutating boundaries), `docs/known-limitations.md` (honest boundaries and non-goals), `docs/observability-governance-talking-points.md` (the technical story in interview/portfolio language), `docs/phase10-acceptance-checklist.md` (the Phase 10 closure checklist), and `docs/screenshot-instructions.md` (a manual evidence-capture checklist; no images are generated or committed). It also synchronizes the State Preservation Bundle so the artifact is cold-session safe.

The portfolio narrative is honest: it does not claim a production SaaS dashboard, a multi-user management system, a cloud-hosted product, a fully automated content platform, a legal-advice engine, a production-grade rights-clearing system, or a commercial TTS platform. The demo script uses only commands that exist in the current CLI. The known-limitations document frames boundaries as deliberate architecture choices where appropriate.

Confirmed constraints: no new product feature; no UI; no server; no dashboard; no browser mutation control; no JavaScript; no external assets; no CDN; no generated audio; no screenshots, images, or binary portfolio assets; no PowerPoint/PDF/slide deck; no new dependency; no database schema change; no change to pipeline behaviour, `storytime rerun` behaviour, or Trust Envelope enforcement; no ARCH-LOCKed contract change. Phase 10G is documentation-first; no application code was changed.

Confirmed gate results: 549 tests passing, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy, legal-hallucination scanner 0 violations.

**Current state after this round (Phase 10G):** Phase 10A, Phase 10B, Phase 10C, Phase 10C.1, Phase 10D, Phase 10D.1, Phase 10E (with the 10E.1 / 10E.2 cleanup sequence), and Phase 10F are all locked. Phase 10G — Portfolio Narrative / Phase 10 Closure — is an implementation candidate, pending review, **not locked**. Phase 10 is not yet marked closed. Phase 11 has not started. Phase 9C remains optional/not scheduled.

## Phase 10G — Portfolio Narrative / Phase 10 Closure (LOCKED / ACCEPTED / CANONICAL — Phase 10 CLOSED — 2026-05-25)

Lock closure. Phase 10G — Portfolio Narrative / Phase 10 Closure — is locked, accepted, and canonical with explicit user approval. **With Phase 10G locked, Phase 10 — Product UI / Operator Experience — is formally CLOSED.** Locked artifact: `storytime-phase10g1-uvlock-reversion-cleanup.tar.gz`, SHA-256 `8a0cc9a5b6426a291bec3a793e41501c7d3492187dd48b4f7729ea95e501a0c1`.

Phase 10G was a documentation, portfolio-narrative, demo-explanation, and Phase 10 closure round under the locked Architecture Baseline Section 25 operator-experience law. It added eight Phase 10 portfolio/closure documents under `docs/` — `portfolio-narrative.md`, `demo-script.md`, `operator-experience-walkthrough.md`, `command-reference.md`, `known-limitations.md`, `observability-governance-talking-points.md`, `phase10-acceptance-checklist.md`, and `screenshot-instructions.md` — and synchronized the State Preservation Bundle. It added no product feature, no UI, no server, no JavaScript, no generated audio, no screenshots/binary assets, and no new dependency; it changed no pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, or the database schema.

Phase 10G completed the Phase Closure Protocol: GPT-5.5 Phase 10G review PASS; Gemini Phase 10G review SAFE WITH EDITS, with one required cleanup — verify/revert `uv.lock` to the exact Phase 10F state. The Phase 10G.1 cleanup completed that requirement; the suspected `uv.lock` drift was a false positive — `uv.lock` was byte-for-byte identical across Phase 10F, Phase 10G, and Phase 10G.1, and Phase 10G.1 explicitly copied the Phase 10F `uv.lock` into the tree to guarantee identity (only `docs/artifact-manifest.md` and `docs/verification-log.md` cleanup bookkeeping changed from Phase 10G to Phase 10G.1). GPT-5.5 Phase 10G.1 verification PASS; Gemini Phase 10G.1 final verification SAFE TO LOCK. The user then locked Phase 10G with explicit approval.

Validation basis at lock: 549 tests passing, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 contracts kept, `storytime doctor` healthy.

This lock/closure was recorded into the State Preservation Bundle by the Post-Phase-10 Closure State Synchronization task (a governance/state-document synchronization, not a feature phase): it updated the first-read current-state docs — `LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, `docs/roadmap.md`, this `docs/canonical-state.md`, `docs/phase-history.md`, `docs/artifact-manifest.md`, `docs/verification-log.md`, `docs/roundtable-import-bridge.md`, and `docs/open-issues.md` — to record the already-approved Phase 10G lock and Phase 10 closure. It changed no `pyproject.toml`, `uv.lock`, `src/`, or `tests/` content and added no product behaviour.

**Current state after this round (Phase 10G lock / Phase 10 closure):** Phase 10A, Phase 10B, Phase 10C, Phase 10C.1, Phase 10D, Phase 10D.1, Phase 10E (with the 10E.1 / 10E.2 cleanup sequence), Phase 10F, and Phase 10G are all locked. **Phase 10 — Product UI / Operator Experience — is formally CLOSED.** The next phase is **Phase 11 — Release Candidate Hardening**, which has **not started**. Phase 9C remains optional/not scheduled.

## Post-Phase-10 Historical State Reconciliation (locked work item — documentation/state-history checkpoint — 2026-05-25)

Recorded for log continuity. The Post-Phase-10 Historical State Reconciliation was a documentation/state-history reconciliation checkpoint between Phase 10 closure and Phase 11 start — **not a new phase** (not Phase 10G.2, not Phase 11.0); it did not reopen Phase 10 or start Phase 11. It integrated early RoundTable lineage (Phases 0–7) into the historical living docs: `docs/phase-history.md` gained a quarantined "Appendix — Historical RoundTable Lineage, Phases 0–7" section, `docs/roundtable-import-bridge.md` gained a "Historical RoundTable export" section, and `docs/artifact-manifest.md` / `docs/verification-log.md` recorded the artifact and its verification. All RoundTable-export-derived material is explicitly labeled historical/superseded; the current state was unchanged. It changed no `pyproject.toml`, `uv.lock`, `src/`, or `tests/` content and added no product behaviour. Locked artifact: `storytime-post-phase10-roundtable-historical-backfill.tar.gz`, SHA-256 `367e647c46aa6e4fd039369da30859b11ca783249569df291343db133ef4cfdd`. It is the last locked work item before Phase 11.

## Phase 11A — Release Candidate Hardening Baseline (implementation candidate — pending review — not locked — 2026-05-25)

Implementation round. Phase 11A is the first subphase of Phase 11 — Release Candidate Hardening. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 11A awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 11A does **not** mark Phase 11 complete and does **not** start Phase 11B, 11C, 11D, or Phase 12.

Phase 11A is a documentation-first release-candidate hardening round. It audits and documents the repository's non-feature surfaces so the later Phase 11 subphases can proceed from a stable, understandable base: fresh-clone readiness, the canonical validation-command baseline, artifact hygiene, the local-first security/secrets posture, demo reproducibility, the known-limitations posture, and the Phase 11 decomposition. It adds seven `docs/` hardening documents — `release-candidate-hardening.md` (the hardening baseline overview), `phase11-plan.md` (the Phase 11A–11D decomposition), `local-setup-runbook.md`, `fresh-clone-checklist.md`, `rc-validation-checklist.md`, `security-secrets-checklist.md`, and `demo-reproducibility-checklist.md` — and synchronizes the State Preservation Bundle.

Confirmed constraints: no new product feature; no UI; no server; no dashboard; no browser mutation control; no JavaScript; no external assets; no CDN; no generated audio; no screenshots/images/PDF/PowerPoint/binary assets; no new dependency; no database schema change; no change to pipeline behaviour, `storytime rerun` behaviour, or Trust Envelope enforcement; no ARCH-LOCKed contract change. `pyproject.toml`, `uv.lock`, the `src/` tree, and the `tests/` tree are byte-for-byte unchanged from the source artifact. Phase 11A is documentation-first; no application code was changed. `docs/known-limitations.md` is intentionally left unchanged — it is a locked Phase 10G deliverable whose phase-status section is self-scoped and already defers to `docs/handoff-state.md`.

Confirmed gate results: 549 tests passing, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy; the legal-hallucination scanner (run inside the pytest suite) returns zero violations.

**Current state after this round (Phase 11A):** Phase 10A, Phase 10B, Phase 10C, Phase 10C.1, Phase 10D, Phase 10D.1, Phase 10E (with the 10E.1 / 10E.2 cleanup sequence), Phase 10F, and Phase 10G are all locked; **Phase 10 is CLOSED**; the Post-Phase-10 Historical State Reconciliation is the last locked work item. Phase 11 — Release Candidate Hardening — is in progress; Phase 11A — Release Candidate Hardening Baseline — is an implementation candidate, pending review, **not locked**. Phase 11B, 11C, 11D, and Phase 12 have not started. Phase 9C remains optional/not scheduled.

## Phase 11A — Release Candidate Hardening Baseline (LOCKED / ACCEPTED / CANONICAL — 2026-05-25)

Lock closure. Phase 11A — Release Candidate Hardening Baseline — is locked, accepted, and canonical. It is the last locked phase. Locked artifact: `storytime-phase11a-release-candidate-hardening-baseline.tar.gz`, SHA-256 `664f8ba4ae90cf6a98ccc7d20369e690eac74497ab78f2b7067f0aac2079a7aa`.

Phase 11A was the first subphase of Phase 11 — Release Candidate Hardening — a documentation-first hardening round that audited and documented the repository's non-feature surfaces and added seven `docs/` hardening documents (`release-candidate-hardening.md`, `phase11-plan.md`, `local-setup-runbook.md`, `fresh-clone-checklist.md`, `rc-validation-checklist.md`, `security-secrets-checklist.md`, `demo-reproducibility-checklist.md`). It added no product feature, no UI, no server, no JavaScript, no generated audio, no screenshots/binary assets, no new dependency, and no database schema change; it changed no pipeline behaviour, `storytime rerun`, or Trust Envelope enforcement, and changed no `pyproject.toml`, `uv.lock`, `src/`, or `tests/` content. Phase 11A completed the Phase Closure Protocol and was locked with explicit user approval.

This lock is recorded into the State Preservation Bundle by the Phase 11B round as part of its state synchronization — the same after-the-fact lock-recording pattern used for the Post-Phase-10 Closure State Synchronization. The Phase 11A "implementation candidate" entry earlier in this append-only file is preserved as written and is superseded for status purposes by this lock-closure entry.

**Current state after this lock (Phase 11A):** Phase 10A–10G all locked; **Phase 10 CLOSED**; the Post-Phase-10 Historical State Reconciliation was the last locked work item before Phase 11; Phase 11 — Release Candidate Hardening — in progress; **Phase 11A — Release Candidate Hardening Baseline — locked (the last locked phase)**. Phase 11B has not started before the Phase 11B round below. Phase 9C remains optional/not scheduled.

## Phase 11B — Fresh Clone / Operator Reproducibility (implementation candidate — pending review — not locked — 2026-05-25)

Implementation round. Phase 11B is the second subphase of Phase 11 — Release Candidate Hardening. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 11B awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 11B does **not** mark Phase 11 complete and does **not** start Phase 11C, 11D, or Phase 12.

Phase 11B is a fresh-clone / operator reproducibility verification round. It took the locked Phase 11A documentation as a specification and verified it against reality: it extracted the locked Phase 11A artifact (`storytime-phase11a-release-candidate-hardening-baseline.tar.gz`, SHA-256 `664f8ba4ae90cf6a98ccc7d20369e690eac74497ab78f2b7067f0aac2079a7aa`) into a clean tree, walked the documented setup, validation, and demo paths exactly as written, and confirmed they reproduce the Phase 11A baseline. The six Docker-free quality gates were re-run from the clean extraction and passed (549 tests, ruff clean, mypy clean over 85 source files strict, import-linter 2/2 kept, `storytime doctor` healthy); the documented operator commands (`version`, `--help`, `validate-manifest`, the golden-path `run --auto-approve`, `status`, `report generate`, the demo-fixture integrity tests) ran as documented.

Phase 11B added two reproducibility documents — `docs/operator-reproducibility-checklist.md` (the step-by-step verification path, paired with the observed reference results) and `docs/fresh-clone-troubleshooting.md` (common fresh-clone setup failures and their safe responses) — refined the Phase 11A reproducibility documents (`phase11-plan.md`, `fresh-clone-checklist.md`, `local-setup-runbook.md`, `rc-validation-checklist.md`, `demo-reproducibility-checklist.md`, `release-candidate-hardening.md`), aligned the `README.md` setup command with the canonical `uv sync --frozen --extra dev` form used by every release-candidate validation document (a documentation-consistency fix; no behaviour change), and synchronized the State Preservation Bundle.

Confirmed constraints: no new product feature; no UI; no server; no dashboard; no browser mutation control; no JavaScript; no external assets; no CDN; no generated audio; no screenshots/images/PDF/PowerPoint/binary assets; no new dependency; no database schema change; no change to pipeline behaviour, `storytime rerun` behaviour, or Trust Envelope enforcement; no ARCH-LOCKed contract change; no helper scripts added (documentation-first removed the ambiguity — the existing `make` targets and the explicit `uv run` gate commands already cover verification). `pyproject.toml`, `uv.lock`, the `src/` tree, and the `tests/` tree are byte-for-byte unchanged from the source artifact. Phase 11B is documentation-first; no application code was changed.

Confirmed gate results: 549 tests passing, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy; the legal-hallucination scanner (run inside the pytest suite, covering the two new documents and the updated docs) returns zero violations.

**Current state after this round (Phase 11B):** Phase 10A–10G all locked; **Phase 10 CLOSED**; the Post-Phase-10 Historical State Reconciliation was the last locked work item before Phase 11; **Phase 11A — Release Candidate Hardening Baseline — locked (the last locked phase)**; Phase 11 — Release Candidate Hardening — in progress; Phase 11B — Fresh Clone / Operator Reproducibility — is an implementation candidate, pending review, **not locked**. Phase 11C, 11D, and Phase 12 have not started. Phase 9C remains optional/not scheduled.

## Phase 11B — Fresh Clone / Operator Reproducibility (LOCKED / ACCEPTED / CANONICAL — 2026-05-25)

Lock closure. Phase 11B — Fresh Clone / Operator Reproducibility — is locked, accepted, and canonical. It is the last locked phase. Locked artifact: `storytime-phase11b-fresh-clone-operator-reproducibility.tar.gz`, SHA-256 `08b72f2833da9adf3b8acc1f3170334eb7c5f998e19263838efbce2f571cc73f`.

Phase 11B was the second subphase of Phase 11 — Release Candidate Hardening — a fresh-clone / operator reproducibility verification round that extracted the locked Phase 11A artifact into a clean tree, confirmed the documented setup, validation, and demo paths reproduce the Phase 11A baseline, added two reproducibility documents (`docs/operator-reproducibility-checklist.md`, `docs/fresh-clone-troubleshooting.md`), refined the Phase 11A reproducibility documents, and aligned the `README.md` setup command with the canonical `uv sync --frozen --extra dev` form. It added no product feature, no UI, no server, no JavaScript, no generated audio, no screenshots/binary assets, no new dependency, and no database schema change; it changed no pipeline behaviour, `storytime rerun`, or Trust Envelope enforcement, and changed no `pyproject.toml`, `uv.lock`, `src/`, or `tests/` content. Phase 11B completed the Phase Closure Protocol and was locked with explicit user approval.

This lock is recorded into the State Preservation Bundle by the Phase 11C round as part of its state synchronization — the same after-the-fact lock-recording pattern used for Phase 11A and for the Post-Phase-10 Closure State Synchronization. The Phase 11B "implementation candidate" entry earlier in this append-only file is preserved as written and is superseded for status purposes by this lock-closure entry.

**Current state after this lock (Phase 11B):** Phase 10A–10G all locked; **Phase 10 CLOSED**; the Post-Phase-10 Historical State Reconciliation was the last locked work item before Phase 11; Phase 11 — Release Candidate Hardening — in progress; Phase 11A locked; **Phase 11B — Fresh Clone / Operator Reproducibility — locked (the last locked phase)**. Phase 11C has not started before the Phase 11C round below. Phase 9C remains optional/not scheduled.

## Phase 11C — Failure-Mode / Regression Hardening (implementation candidate — pending review — not locked — 2026-05-25)

Implementation round. Phase 11C is the third subphase of Phase 11 — Release Candidate Hardening. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 11C awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 11C does **not** mark Phase 11 complete and does **not** start Phase 11D or Phase 12.

Phase 11C is a failure-mode and regression-hardening round. It answers the release-candidate question "what breaks, how do we know, and can we prove the system fails safely?" by inventorying the highest-risk failure and regression paths that already exist in StoryTime — the operator failure / review queue, retry / re-run behaviour, governance-blocked content, static HTML report safety, demo fixture invariants, the static legal-hallucination gate, operator-safe failure messages, state preservation around failed runs, and traceability of blocked / failed / retried stages — recording for each one which tests and validation gates protect it, and documenting how a local operator should respond to a failure without bypassing governance or deleting state.

Phase 11C added four `docs/` documents — `failure-mode-regression-hardening.md` (the Phase 11C overview), `regression-risk-register.md` (the risk inventory R1–R9, each with a coverage status), `failure-mode-test-matrix.md` (the regression coverage map from each risky path to the tests and gates that protect it), and `operator-failure-response.md` (the operator failure-response playbook) — and one focused regression test module, `tests/test_failure_mode_regression.py`. That module is genuine new coverage: it converts the project's state-documentation discipline rule into an executable guard, asserting that the State Preservation Bundle keeps Phase 11C marked a pending-review implementation candidate, keeps Phase 11B as the last locked phase, never claims Phase 11D or Phase 12 has started or locked, and still retains the append-only historical lock records. Phase 11C synchronized the State Preservation Bundle.

Confirmed constraints: no new product feature; no UI; no server; no dashboard; no browser mutation control; no JavaScript; no external assets; no CDN; no generated audio; no screenshots/images/PDF/PowerPoint/binary assets; no new dependency; no database schema change; no change to pipeline behaviour, `storytime rerun` behaviour, or Trust Envelope enforcement; no ARCH-LOCKed contract change; no source change. `pyproject.toml`, `uv.lock`, and the `src/` tree are byte-for-byte unchanged from the source artifact. The only `tests/` change is the added regression module `tests/test_failure_mode_regression.py`; no existing test was modified. `docs/known-limitations.md` is intentionally left unchanged — it is a locked Phase 10G deliverable whose phase-status section is self-scoped and already defers to `docs/handoff-state.md`.

Confirmed gate results: 580 tests passing, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy; the legal-hallucination scanner (run inside the pytest suite, covering the four new documents and the new test module) returns zero violations.

**Current state after this round (Phase 11C):** Phase 10A–10G all locked; **Phase 10 CLOSED**; the Post-Phase-10 Historical State Reconciliation was the last locked work item before Phase 11; Phase 11A locked; **Phase 11B — Fresh Clone / Operator Reproducibility — locked (the last locked phase)**; Phase 11 — Release Candidate Hardening — in progress; Phase 11C — Failure-Mode / Regression Hardening — is an implementation candidate, pending review, **not locked**. Phase 11D and Phase 12 have not started. Phase 9C remains optional/not scheduled.

## Phase 11C — Failure-Mode / Regression Hardening (LOCKED / ACCEPTED / CANONICAL — 2026-05-25)

Lock closure. Phase 11C — Failure-Mode / Regression Hardening — is locked, accepted, and canonical. It is the last locked phase. Locked artifact: `storytime-phase11c-failure-mode-regression-hardening.tar.gz`, SHA-256 `2dd31442e62c13241a64d10c2d117aefedc3b9c633ad5ea5d1fa94cfaad7d57b`.

Phase 11C was the third subphase of Phase 11 — Release Candidate Hardening — a failure-mode and regression-hardening round that inventoried the highest-risk failure and regression paths that already exist in StoryTime (operator failure / review queue, retry / re-run behaviour, governance-blocked content, static HTML report safety, demo fixture invariants, the static legal-hallucination gate, operator-safe failure messages, state preservation around failed runs), recorded which tests and validation gates protect each one, documented operator failure-response, added four `docs/` documents (`failure-mode-regression-hardening.md`, `regression-risk-register.md`, `failure-mode-test-matrix.md`, `operator-failure-response.md`), and added one focused regression test module (`tests/test_failure_mode_regression.py`, the state-documentation discipline guard). It added no product feature, no UI, no server, no JavaScript, no generated audio, no screenshots/binary assets, no new dependency, and no database schema change; it changed no pipeline behaviour, `storytime rerun`, or Trust Envelope enforcement, and changed no `pyproject.toml`, `uv.lock`, or `src/` content; the only `tests/` change was the new regression module. Phase 11C completed the Phase Closure Protocol and was locked with explicit user approval.

This lock is recorded into the State Preservation Bundle by the Phase 11D round as part of its state synchronization — the same after-the-fact lock-recording pattern used for Phase 11A, Phase 11B, and the Post-Phase-10 Closure State Synchronization. The Phase 11C "implementation candidate" entry earlier in this append-only file is preserved as written and is superseded for status purposes by this lock-closure entry.

**Current state after this lock (Phase 11C):** Phase 10A–10G all locked; **Phase 10 CLOSED**; the Post-Phase-10 Historical State Reconciliation was the last locked work item before Phase 11; Phase 11A locked; Phase 11B locked; **Phase 11C — Failure-Mode / Regression Hardening — locked (the last locked phase)**. Phase 11D has not started before the Phase 11D round below. Phase 9C remains optional/not scheduled.

## Phase 11D — Release Candidate Evidence Pack (implementation candidate — pending review — not locked — 2026-05-25)

Implementation round. Phase 11D is the fourth and final planned subphase of Phase 11 — Release Candidate Hardening. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 11D awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 11D does **not** mark Phase 11 complete and does **not** start Phase 12.

Phase 11D is an evidence, closure-readiness, and proof-consolidation round. It answers the release-candidate question "can we prove this release candidate is ready to show, explain, hand off, and package?" by consolidating the release-candidate evidence produced by Phases 11A, 11B, and 11C into a reviewer-facing index, recording the canonical validation results, preparing a Phase 11 closure checklist, and writing a Phase 12 readiness handoff. It is not product development.

Phase 11D took the locked Phase 11C artifact (`storytime-phase11c-failure-mode-regression-hardening.tar.gz`, SHA-256 `2dd31442e62c13241a64d10c2d117aefedc3b9c633ad5ea5d1fa94cfaad7d57b`, verified on extraction) as its source. It added four `docs/` documents — `release-candidate-evidence-pack.md` (the Phase 11D overview and the release-candidate evidence index), `final-validation-summary.md` (the canonical validation results), `phase11-closure-checklist.md` (what each Phase 11 subphase contributed and the conditions for an explicit Phase 11 closure decision), and `phase12-readiness-handoff.md` (what Phase 12 may safely do) — and synchronized the State Preservation Bundle. It re-ran the six Docker-free validation gates against the Phase 11C artifact with no source, dependency, or test change applied, and recorded the results.

Confirmed constraints: no new product feature; no UI; no server; no dashboard; no browser mutation control; no JavaScript; no external assets; no CDN; no generated audio; no screenshots/images/PDF/PowerPoint/binary assets; no new dependency; no database schema change; no change to pipeline behaviour, `storytime rerun` behaviour, or Trust Envelope enforcement; no ARCH-LOCKed contract change; no source change; no test change. `pyproject.toml`, `uv.lock`, the `src/` tree, and the `tests/` tree are byte-for-byte unchanged from the source artifact. Phase 11D is documentation/evidence consolidation only. `docs/known-limitations.md` is intentionally left unchanged — it is a locked Phase 10G deliverable whose phase-status section is self-scoped and already defers to `docs/handoff-state.md`, the same decision Phase 11C recorded.

Confirmed gate results: 580 tests passing, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy; the legal-hallucination scanner (run inside the pytest suite, covering the four new documents) returns zero violations.

**Current state after this round (Phase 11D):** Phase 10A–10G all locked; **Phase 10 CLOSED**; the Post-Phase-10 Historical State Reconciliation was the last locked work item before Phase 11; Phase 11A locked; Phase 11B locked; **Phase 11C — Failure-Mode / Regression Hardening — locked (the last locked phase)**; Phase 11 — Release Candidate Hardening — is in progress; Phase 11D — Release Candidate Evidence Pack — is an implementation candidate, pending review, **not locked**. Phase 12 has not started. Phase 9C remains optional/not scheduled.

## Phase 11D — Release Candidate Evidence Pack (LOCKED / ACCEPTED / CANONICAL — Phase 11 CLOSED — 2026-05-26)

Lock closure recorded out-of-band. Phase 11D — Release Candidate Evidence Pack — the fourth and final planned subphase of Phase 11 — Release Candidate Hardening — is locked, accepted, and canonical with explicit user approval. **With Phase 11D locked, Phase 11 — Release Candidate Hardening — is formally CLOSED.** Locked artifact: `storytime-phase11d-release-candidate-evidence-pack.tar.gz`, SHA-256 `07a3973e3dbb69d760ff2c330418f85101c2afa1464fc0eed752fc7053894d94`.

Phase 11D was an evidence, closure-readiness, and proof-consolidation round. It consolidated the release-candidate evidence produced by Phases 11A, 11B, and 11C into a reviewer-facing index, recorded the canonical validation results, prepared a Phase 11 closure checklist, and wrote a Phase 12 readiness handoff. It added four `docs/` documents — `release-candidate-evidence-pack.md`, `final-validation-summary.md`, `phase11-closure-checklist.md`, and `phase12-readiness-handoff.md` — and synchronized the State Preservation Bundle. It added no product feature, no UI, no server, no JavaScript, no generated audio, no screenshots/binary assets, and no new dependency; it changed no pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, or the database schema, and changed no `pyproject.toml`, `uv.lock`, `src/`, or `tests/` content.

Phase 11D completed the Phase Closure Protocol out-of-band, in the GPT/Gemini review workflow: GPT-5.5 Phase 11D review PASS; Gemini Phase 11D review SAFE TO LOCK; no required edits. The user, as final decision-maker, then locked Phase 11D and made the explicit Phase 11 closure decision. This out-of-band closure was a user/mediator decision supplied to the Phase 12A round; it was not contained in the Phase 11D archive itself, which captured the pre-lock implementation-candidate state. The Phase 12A round records this lock and closure into the append-only canonical state; it did not re-perform the GPT-5.5 / Gemini reviews. Validation basis at lock: 580 tests passing, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 contracts kept, `storytime doctor` healthy, legal-hallucination scanner zero violations.

This lock/closure is recorded into the State Preservation Bundle by the Phase 12A — Portfolio / SE Demo Packaging Baseline — round as part of its state synchronization, the same after-the-fact lock-recording pattern used for Phase 11A, Phase 11B, Phase 11C, and the Post-Phase-10 Closure State Synchronization. The Phase 11D "implementation candidate" entry earlier in this append-only file is preserved as written and is superseded for status purposes by this lock-closure entry.

**Current state after this lock (Phase 11D / Phase 11 closure):** Phase 10A–10G all locked; **Phase 10 CLOSED**; the Post-Phase-10 Historical State Reconciliation was the last locked work item before Phase 11; Phase 11A, Phase 11B, Phase 11C, and **Phase 11D — Release Candidate Evidence Pack** are all locked; **Phase 11 — Release Candidate Hardening — is formally CLOSED**; Phase 11D is the last locked phase. The next phase is **Phase 12 — Portfolio / SE Demo Packaging**, started below. Phase 9C remains optional/not scheduled.

## Phase 12 — Portfolio / SE Demo Packaging (STARTED) / Phase 12A — Portfolio / SE Demo Packaging Baseline (implementation candidate — pending review — not locked — 2026-05-26)

Phase start and implementation round. With Phase 11 — Release Candidate Hardening — closed, the user authorized **Phase 12 — Portfolio / SE Demo Packaging**, and Phase 12 is **STARTED**. Phase 12A — Portfolio / SE Demo Packaging Baseline — is the first subphase of Phase 12. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 12A awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 12A does **not** lock Phase 12A, does **not** close Phase 12, and does **not** start Phase 12B or any later Phase 12 subphase.

Phase 12A is a documentation and portfolio-packaging round under no new architecture amendment — it builds on, and explains, the already-locked Phases 0–11. It makes StoryTime explainable as a Solutions Engineer / observability / OpenTelemetry portfolio project. It added four `docs/` documents — `portfolio-overview.md` (the plain-English portfolio overview and entry point), `solutions-engineer-narrative.md` (30-second / 2-minute / deep pitches plus business, observability, OpenTelemetry, and governance framings), `portfolio-demo-script.md` (a narrated, reviewer-facing demo walkthrough that defers to `docs/demo.md` for authoritative commands), and `interview-talking-points.md` (concise, study-friendly talking points) — refined `README.md` with a portfolio-facing "For reviewers" section and an updated phase table, and synchronized the State Preservation Bundle.

The portfolio documents are honest about scope. They do not claim a production SaaS deployment, users, an SLA, cloud hosting, active alerting, an error-budget policy, integration with any named commercial observability vendor, a legal determination, or a rights-clearance capability. They state that StoryTime emits standard OpenTelemetry to a local Collector and that the Collector pattern is what would make vendor fan-out a configuration change — without claiming any such vendor integration exists.

Confirmed constraints: no new product feature; no UI; no server; no dashboard; no browser mutation control; no JavaScript; no external assets; no CDN; no generated audio; no screenshots/images/PDF/PowerPoint/binary assets; no new dependency; no database schema change; no change to pipeline behaviour, `storytime rerun` behaviour, or Trust Envelope enforcement; no ARCH-LOCKed contract change; no source change. `pyproject.toml`, `uv.lock`, and the `src/` tree are byte-for-byte unchanged from the source artifact. The only `tests/` change is a narrow, explicitly authorized advance of the state-discipline guard `tests/test_failure_mode_regression.py` (the Phase 11C state-documentation discipline module) so it tracks the Phase 12A current-state expectations: it now guards against a premature Phase 12A lock, a premature Phase 12 closure, and a premature Phase 12B-or-later start, and it strengthens — does not weaken — the historical lock-record coverage. This test update was explicitly authorized because the test was intentionally phase-specific and otherwise blocks the approved phase transition.

Confirmed gate results: 585 tests passing (580 from the closed Phase 11 baseline, plus 5 net from the authorized advance of the state-discipline guard), ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy; the legal-hallucination scanner (run inside the pytest suite, covering the four new documents) returns zero violations.

**Current state after this round (Phase 12 start / Phase 12A):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 11D — Release Candidate Evidence Pack — is the last locked phase; **Phase 12 — Portfolio / SE Demo Packaging — is STARTED**; Phase 12A — Portfolio / SE Demo Packaging Baseline — is an implementation candidate, pending review, **not locked**. Phase 12B and later subphases of Phase 12 have not started. Phase 9C remains optional/not scheduled.

## Phase 12A — Portfolio / SE Demo Packaging Baseline (LOCKED / ACCEPTED / CANONICAL — 2026-05-26)

Lock closure. Phase 12A — Portfolio / SE Demo Packaging Baseline — the first subphase of Phase 12 — Portfolio / SE Demo Packaging — is locked, accepted, and canonical with explicit user approval. Locked artifact lineage: `storytime-phase12a-portfolio-se-demo-packaging-baseline.tar.gz`, with the accepted Phase 12A.1 state-hygiene cleanup (`storytime-phase12a1-state-hygiene-cleanup.tar.gz`, SHA-256 `5f9eca1cc8c2efb55d57f87becdc53cd0d8e514221947e445965232f608b621a`) folded into the Phase 12A lock lineage.

Phase 12A was a documentation and portfolio-packaging round: it added four portfolio `docs/` documents (`portfolio-overview.md`, `solutions-engineer-narrative.md`, `portfolio-demo-script.md`, `interview-talking-points.md`), refined `README.md` with a portfolio-facing "For reviewers" section, advanced the state-discipline guard `tests/test_failure_mode_regression.py` under explicit authorization to the Phase 12A current-state expectations, and synchronized the State Preservation Bundle. It added no product feature and changed no `pyproject.toml`, `uv.lock`, or `src/` content.

Phase 12A.1 — Portfolio / SE Demo Packaging Baseline state-hygiene cleanup — was a bounded, documentation-only cleanup sub-round of the Phase 12A round: a pre-lock review found stale present-tense phrasing in the historical notes of the living documents, and Phase 12A.1 revised those notes to read as superseded point-in-time records. Phase 12A.1 changed no `src/`, `tests/`, `pyproject.toml`, `uv.lock`, dependency, or product behaviour. Phase 12A.1 is an accepted cleanup sub-round folded into the Phase 12A lock lineage — it is not an independently locked phase.

Phase 12A completed the Phase Closure Protocol — implementation, GPT-5.5 review, Gemini critique, the accepted Phase 12A.1 state-hygiene cleanup sub-round, and an explicit user lock decision. The Phase 12A "implementation candidate" entry earlier in this append-only file is preserved as written and is superseded for status purposes by this lock-closure entry.

**Current state after this lock (Phase 12A):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; **Phase 12A — Portfolio / SE Demo Packaging Baseline — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — is STARTED** and not closed. Phase 12B has not started before the Phase 12B round below. Phase 9C remains optional/not scheduled.

## Phase 12B — Portfolio Evidence Pack / Reviewer Assets (implementation candidate — pending review — not locked — 2026-05-26)

Implementation round. Phase 12B is the second subphase of Phase 12 — Portfolio / SE Demo Packaging. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 12B awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 12B does **not** lock Phase 12B, does **not** close Phase 12, and does **not** start Phase 12C or any later Phase 12 subphase.

Phase 12B is a reviewer / evidence packaging round under no new architecture amendment — it builds on, and makes independently verifiable, the already-locked Phases 0–12A. It took the locked Phase 12A lineage artifact `storytime-phase12a1-state-hygiene-cleanup.tar.gz` (SHA-256 `5f9eca1cc8c2efb55d57f87becdc53cd0d8e514221947e445965232f608b621a`, verified on extraction) as its source. It added four `docs/` documents — `portfolio-evidence-index.md` (a claim-to-evidence index mapping each portfolio claim to a test, config file, source module, or document), `se-interview-evidence-matrix.md` (a Solutions-Engineer competency-to-evidence matrix with an honesty checklist), `demo-reviewer-checklist.md` (a reviewer wrapper over `docs/demo.md` — a pre-flight and what-to-look-for index, explicitly not a duplicate command script), and `portfolio-public-copy.md` (disciplined, non-hype public-facing copy with an honest "what it is not" scope statement) — lightly updated `README.md` to point reviewers to the new evidence documents, and synchronized the State Preservation Bundle.

The new documents are honest about scope. They do not claim a production SaaS deployment, users, an SLA, cloud hosting, active alerting, an error-budget policy, integration with any named commercial observability vendor, a legal determination, or a rights-clearance capability. Every claim in the evidence index points at a real repository artifact.

Confirmed constraints: no new product feature; no UI; no server; no dashboard; no browser mutation control; no JavaScript; no external assets; no CDN; no generated audio; no screenshots/images/PDF/PowerPoint/binary assets; no new dependency; no database schema change; no change to pipeline behaviour, `storytime rerun` behaviour, or Trust Envelope enforcement; no ARCH-LOCKed contract change; no source change. `pyproject.toml`, `uv.lock`, and the `src/` tree are byte-for-byte unchanged from the source artifact. The only `tests/` change is the narrow, explicitly authorized §5 mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 12B current-state expectations: `_CURRENT_PHASE` advanced to "phase 12b", `_LAST_LOCKED_PHASE` advanced to "phase 12a", and `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 12B lock, a premature Phase 12 closure, and a premature Phase 12C-or-later start. The guard is strengthened, not weakened — it additionally requires the Phase 12A lock record in the append-only history. This test update was explicitly authorized under the Phase 12B §5 mechanical exception because the test is intentionally phase-specific and otherwise blocks the approved phase transition.

Confirmed gate results: 588 tests passing (585 from the Phase 12A baseline, plus 3 net from the strengthened state-discipline guard), ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy; the legal-hallucination scanner (run inside the pytest suite, covering the four new documents) returns zero violations.

**Current state after this round (Phase 12B):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; **Phase 12A — Portfolio / SE Demo Packaging Baseline — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — is STARTED**; Phase 12B — Portfolio Evidence Pack / Reviewer Assets — is an implementation candidate, pending review, **not locked**. Phase 12C and later subphases of Phase 12 have not started. Phase 9C remains optional/not scheduled.

## Phase 12B — Portfolio Evidence Pack / Reviewer Assets (LOCKED / ACCEPTED / CANONICAL — 2026-05-26)

Lock closure recorded out-of-band. Phase 12B — Portfolio Evidence Pack / Reviewer Assets — the second subphase of Phase 12 — Portfolio / SE Demo Packaging — is locked, accepted, and canonical with explicit user approval. Locked artifact lineage: `storytime-phase12b-portfolio-evidence-pack-reviewer-assets.tar.gz`, with the accepted Phase 12B.1 state-hygiene cleanup, Phase 12B.2 roadmap-preservation cleanup, and Phase 12B.3 residual living-doc state-wording cleanup folded into the Phase 12B lock lineage. The folded cleanup lineage artifact is `storytime-phase12b3-residual-state-wording-cleanup.tar.gz`, SHA-256 `ce0fb2d1bea4eaa636be7796613f9a9aa56cba4b8bf34c0ae5440c3509de4a45`.

Phase 12B was a reviewer / evidence packaging round: it added four reviewer/evidence `docs/` documents (`portfolio-evidence-index.md`, `se-interview-evidence-matrix.md`, `demo-reviewer-checklist.md`, `portfolio-public-copy.md`), lightly updated `README.md` to point reviewers to them, advanced the state-discipline guard `tests/test_failure_mode_regression.py` under the explicitly authorized §5 mechanical exception, and synchronized the State Preservation Bundle. It added no product feature, no UI, no server, no JavaScript, no generated audio, no screenshots/binary assets, and no new dependency; it changed no pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, or the database schema, and changed no `pyproject.toml`, `uv.lock`, or `src/` content; the only `tests/` change was the authorized state-discipline guard advance.

Phase 12B.1 — Portfolio Evidence Pack / Reviewer Assets state-hygiene cleanup — was a bounded, documentation-only cleanup sub-round of the Phase 12B round: a pre-Gemini-review check found stale Phase 12A.1-era present-tense phrasing in the historical notes of the living documents, and Phase 12B.1 revised those notes to read as superseded point-in-time records. Phase 12B.2 — Phase 13 GUI roadmap preservation — was a bounded roadmap-preservation cleanup sub-round that added `docs/GUI_vision.md` and a Phase 13 — Operator GUI / Decoupled Frontend Vision — roadmap note (future work, not started). Phase 12B.3 — residual living-doc state-wording cleanup — was a bounded cleanup sub-round removing remaining stale present-tense historical wording. Phase 12B.1, Phase 12B.2, and Phase 12B.3 each changed no `src/`, `tests/`, `pyproject.toml`, `uv.lock`, dependency, or product behaviour; they are accepted cleanup sub-rounds folded into the Phase 12B lock lineage — they are not independently locked phases.

Phase 12B completed the Phase Closure Protocol — implementation, GPT-5.5 review, the accepted Phase 12B.1 / 12B.2 / 12B.3 cleanup sub-rounds, Gemini critique of the combined Phase 12B sequence (SAFE TO LOCK, no required edits), and an explicit user lock decision. This out-of-band closure was a user/mediator decision supplied to the Phase 12C round; it was not contained in the Phase 12B sequence archive itself, which captured the pre-lock implementation-candidate/cleanup-lineage state. The Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — round records this lock into the append-only canonical state as part of its state synchronization; it did not re-perform the GPT-5.5 / Gemini reviews. This is the same after-the-fact lock-recording pattern used for Phase 11D and the Phase 12A lock. The Phase 12B "implementation candidate" entry earlier in this append-only file is preserved as written and is superseded for status purposes by this lock-closure entry. Validation basis at lock: 588 tests passing, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 contracts kept, `storytime doctor` healthy, legal-hallucination scanner zero violations.

**Current state after this lock (Phase 12B):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A locked; **Phase 12B — Portfolio Evidence Pack / Reviewer Assets — locked (the last locked phase)** (the accepted Phase 12B.1 / 12B.2 / 12B.3 cleanup sub-rounds folded into its lock lineage); **Phase 12 — Portfolio / SE Demo Packaging — is STARTED** and not closed. Phase 12C has not started before the Phase 12C round below. Phase 13 — Operator GUI / Decoupled Frontend Vision — is roadmap-preserved only and has not started. Phase 9C remains optional/not scheduled.

## Phase 12C — Portfolio Demo Narrative / Public Presentation Kit (implementation candidate — pending review — not locked — 2026-05-26)

Implementation round. Phase 12C is the third subphase of Phase 12 — Portfolio / SE Demo Packaging. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 12C awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 12C does **not** lock Phase 12C, does **not** close Phase 12, and does **not** start Phase 12D or any later Phase 12 subphase.

Phase 12C is a documentation-first portfolio-packaging round under no new architecture amendment — it builds on, and converts into public-presentation form, the already-locked Phases 0–12B. It took the locked Phase 12B sequence lineage artifact `storytime-phase12b3-residual-state-wording-cleanup.tar.gz` (SHA-256 `ce0fb2d1bea4eaa636be7796613f9a9aa56cba4b8bf34c0ae5440c3509de4a45`, verified on extraction) as its source. It added four `docs/` documents — `portfolio-demo-narrative.md` (a concise demo narrative covering the business problem, technical architecture, observability value, governance posture, what the operator sees, what the reviewer should notice, the SE/Dynatrace-style credibility mapping, and the intentional out-of-scope boundaries), `demo-talk-track.md` (a spoken walkthrough script at 5-minute, 10-minute, and 20-minute lengths, with interviewer Q&A pivots and a "what to say if the demo cannot be run live" fallback), `interview-story-bank.md` (reusable Solutions-Engineer / observability interview answer frames for the seven standard project-interview questions, each with an honesty checklist), and `public-repository-readiness.md` (a checklist and guardrails for preparing the repository for public viewing — public-safe README check, secrets/config check, demo-data check, screenshot-placeholder check, known-limitations check, and "do not publish until verified" hard gates) — lightly updated `README.md` to point reviewers to the new presentation documents, and synchronized the State Preservation Bundle.

Confirmed constraints: documentation-first portfolio packaging only. No new product feature, UI, server, dashboard, browser mutation control, JavaScript, frontend directory, React/Vite/TypeScript file, external asset, CDN, generated audio, screenshot/image/PDF/PowerPoint/binary asset, demo video, new dependency, or database schema change; no change to pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, API, CLI, or telemetry behaviour; no ARCH-LOCKed contract change; no source change; no Phase 13 GUI implementation. `pyproject.toml`, `uv.lock`, and the `src/` tree are byte-for-byte unchanged from the source artifact. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 12C current-state expectations: `_CURRENT_PHASE` advanced to "phase 12c", `_LAST_LOCKED_PHASE` advanced to "phase 12b", and `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 12C lock, a premature Phase 12 closure, and a premature Phase 12D-or-later start. The guard is strengthened, not weakened — the append-only lock-record checks now additionally require the Phase 12B lock record. This test update was explicitly authorized because the test is intentionally phase-specific and otherwise blocks the approved phase transition. The append-only locked-decision documents `docs/canonical-state.md` and the round log in `docs/phase-history.md` were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

Confirmed gate results: 590 tests passing (588 from the Phase 12B baseline, plus 2 net from the strengthened state-discipline guard — the advance adds two parametrized append-only lock-record cases requiring the Phase 12B record), ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy; the legal-hallucination scanner (run inside the pytest suite, covering the four new documents) returns zero violations.

**Current state after this round (Phase 12C):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A locked; **Phase 12B — Portfolio Evidence Pack / Reviewer Assets — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — is STARTED**; Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — is an implementation candidate, pending review, **not locked**. Phase 12D and later subphases of Phase 12 have not started. Phase 13 — Operator GUI / Decoupled Frontend Vision — is roadmap-preserved only and has not started. Phase 9C remains optional/not scheduled.

## Phase 12C — Portfolio Demo Narrative / Public Presentation Kit (LOCKED / ACCEPTED / CANONICAL — 2026-05-26)

Lock closure recorded. Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — the third subphase of Phase 12 — Portfolio / SE Demo Packaging — is locked, accepted, and canonical with explicit user approval. Locked artifact lineage: `storytime-phase12c-portfolio-demo-narrative-public-presentation-kit.tar.gz`, SHA-256 `4c98a25d6bb0ae751b4ba33851bc60e7d7805d4fd31ebcfc45c2d30a659301da`.

Phase 12C was a documentation-first portfolio-packaging round: it added four public-presentation `docs/` documents (`portfolio-demo-narrative.md`, `demo-talk-track.md`, `interview-story-bank.md`, `public-repository-readiness.md`), lightly updated `README.md` to point reviewers to them, advanced the state-discipline guard `tests/test_failure_mode_regression.py` under the explicitly authorized §5 mechanical exception, and synchronized the State Preservation Bundle. It added no product feature, no UI, no server, no JavaScript, no frontend directory, no generated audio, no screenshots/binary assets, no demo video, and no new dependency; it changed no pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, API, CLI, telemetry, or the database schema, and changed no `pyproject.toml`, `uv.lock`, or `src/` content; the only `tests/` change was the authorized state-discipline guard advance.

Phase 12C completed the Phase Closure Protocol — implementation, GPT-5.5 review, and Gemini critique. Gemini returned **SAFE TO LOCK** for Phase 12C with no critical findings, no non-blocking findings, and no required edits; state discipline, scope/code/dependency assessment, and validation assessment all passed. The user then locked Phase 12C. This out-of-band closure was a user/mediator decision supplied to the Phase 12D round; it was not contained in the Phase 12C artifact itself, which captured the pre-lock implementation-candidate state. The Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — round records this lock into the append-only canonical state as part of its state synchronization; it did not re-perform the GPT-5.5 / Gemini reviews. This is the same after-the-fact lock-recording pattern used for Phase 11D, Phase 12A, and Phase 12B. The Phase 12C "implementation candidate" entry earlier in this append-only file is preserved as written and is superseded for status purposes by this lock-closure entry. Validation basis at lock: 590 tests passing, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 contracts kept, `storytime doctor` healthy, legal-hallucination scanner zero violations.

**Current state after this lock (Phase 12C):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A locked; Phase 12B locked; **Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — is STARTED** and not closed. Phase 12D has not started before the Phase 12D round below. Phase 13 — Operator GUI / Decoupled Frontend Vision — is roadmap-preserved only and has not started. Phase 9C remains optional/not scheduled.

## Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition (implementation candidate — pending review — not locked — 2026-05-26)

Implementation round. Phase 12D is the fourth subphase of Phase 12 — Portfolio / SE Demo Packaging. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 12D awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 12D does **not** lock Phase 12D, does **not** close Phase 12, and does **not** start Phase 12E or any later Phase 12 subphase.

Phase 12D is a documentation-only closure-definition round. It does not itself close Phase 12 — it prepares the Phase 12 closure decision. It took the locked Phase 12C artifact `storytime-phase12c-portfolio-demo-narrative-public-presentation-kit.tar.gz` (SHA-256 `4c98a25d6bb0ae751b4ba33851bc60e7d7805d4fd31ebcfc45c2d30a659301da`, verified on extraction) as its source. It added three `docs/` documents — `phase12-closure-plan.md` (the Phase 12 closure criteria, the completed Phase 12A–12C asset inventory, the closure-readiness checklist, the remaining-gaps / no-go criteria, the close-after-12D vs bounded-cleanup vs separate-12E recommendation, and the Phase 13 boundary statement), `final-portfolio-handoff.md` (a cold-reader handoff: current-state snapshot, 5-minute / 15-minute / deep-architecture reviewer paths, a suggested demo flow, an evidence map, explicit limitations, and the next-phase boundary), and `phase12-final-review-checklist.md` (the checklist a reviewer uses to decide whether Phase 12D can lock and whether Phase 12 can close) — and synchronized the State Preservation Bundle.

Confirmed constraints: documentation-only closure-definition round. No new product feature, UI, server, dashboard, browser mutation control, JavaScript, frontend directory, React/Vite/TypeScript file, external asset, CDN, generated audio, screenshot/image/PDF/PowerPoint/binary asset, demo video, new dependency, or database schema change; no change to pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, API, CLI, or telemetry behaviour; no ARCH-LOCKed contract change; no source change; no Phase 13 GUI implementation. `pyproject.toml`, `uv.lock`, and the `src/` tree are byte-for-byte unchanged from the source artifact. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 12D current-state expectations: `_CURRENT_PHASE` advanced to "phase 12d", `_LAST_LOCKED_PHASE` advanced to "phase 12c", and `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 12D lock, a premature Phase 12 closure, and a premature Phase 12E-or-later start. The guard is strengthened, not weakened — the append-only lock-record checks now additionally require the Phase 12C lock record. This test update was explicitly authorized because the test is intentionally phase-specific and otherwise blocks the approved phase transition. The append-only locked-decision documents `docs/canonical-state.md` and the round log in `docs/phase-history.md` were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

Confirmed gate results: 592 tests passing (590 from the Phase 12C baseline, plus 2 net from the strengthened state-discipline guard — the advance adds two parametrized append-only lock-record cases requiring the Phase 12C record), ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy; the legal-hallucination scanner (run inside the pytest suite, covering the three new documents) returns zero violations.

**Current state after this round (Phase 12D):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A locked; Phase 12B locked; **Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — is STARTED**; Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — is an implementation candidate, pending review, **not locked**. Phase 12 is not closed. Phase 12E is optional, future, contingency-only work and has not started. Phase 13 — Operator GUI / Decoupled Frontend Vision — is roadmap-preserved only and has not started. Phase 9C remains optional/not scheduled.

## Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition (LOCKED / ACCEPTED / CANONICAL — Phase 12 CLOSED — 2026-05-27)

Lock closure recorded. Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — the fourth subphase of Phase 12 — Portfolio / SE Demo Packaging — is locked, accepted, and canonical with explicit user approval. Locked artifact lineage: `storytime-phase12d-phase12-closure-plan-final-portfolio-handoff.tar.gz`, SHA-256 `64ad09e875f0653608e0deb756f11ee5adc0d2ff1265e2039cbc51491f286cf8`.

Phase 12D was a documentation-only closure-definition round: it added three closure-definition `docs/` documents (`phase12-closure-plan.md`, `final-portfolio-handoff.md`, `phase12-final-review-checklist.md`), lightly updated `README.md`, advanced the state-discipline guard `tests/test_failure_mode_regression.py` under the explicitly authorized §5 mechanical exception, and synchronized the State Preservation Bundle. It added no product feature, no UI, no server, no JavaScript, no frontend directory, no generated audio, no screenshots/binary assets, no demo video, and no new dependency; it changed no pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, API, CLI, telemetry, or the database schema, and changed no `pyproject.toml`, `uv.lock`, or `src/` content; the only `tests/` change was the authorized state-discipline guard advance.

Phase 12D completed the Phase Closure Protocol — implementation, GPT-5.5 review, and Gemini critique. The Gemini review returned the verdict to lock Phase 12D and close Phase 12, with no critical findings, no non-blocking findings, and no required edits; state discipline, scope/code/dependency assessment, and validation assessment all passed. The user, as final decision-maker, then locked Phase 12D and formally closed Phase 12 — Portfolio / SE Demo Packaging. This out-of-band closure was a user/mediator decision supplied to the Phase 13A round; it was not contained in the Phase 12D artifact itself, which captured the pre-lock implementation-candidate state. The Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — round records this lock and closure into the append-only canonical state as part of its state synchronization; it did not re-perform the GPT-5.5 / Gemini reviews. This is the same after-the-fact lock-recording pattern used for Phase 11D, Phase 12A, Phase 12B, and Phase 12C. The Phase 12D "implementation candidate" entry earlier in this append-only file is preserved as written and is superseded for status purposes by this lock-closure entry. Validation basis at lock: 592 tests passing, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 contracts kept, `storytime doctor` healthy, legal-hallucination scanner zero violations.

**Phase 12 — Portfolio / SE Demo Packaging — is CLOSED.** All four of its subphases — Phase 12A (Portfolio / SE Demo Packaging Baseline), Phase 12B (Portfolio Evidence Pack / Reviewer Assets), Phase 12C (Portfolio Demo Narrative / Public Presentation Kit), and Phase 12D (Phase 12 Closure Plan / Final Portfolio Handoff Definition) — are locked. Phase 12A.1 is folded into the Phase 12A lock lineage, and Phase 12B.1 / 12B.2 / 12B.3 are folded into the Phase 12B lock lineage, as accepted cleanup sub-rounds — not independently locked phases. Phase 12E was optional, contingency-only work that would have existed only if the Phase 12D review had found a substantive packaging gap; the review found none, so Phase 12E was not needed and never started.

**Current state after this lock (Phase 12D / Phase 12 closure):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — is the last locked phase**; **Phase 12 — Portfolio / SE Demo Packaging — is CLOSED**. Phase 13 — Portfolio Website / Operator GUI — is STARTED before the Phase 13A round below. Phase 9C remains optional/not scheduled.

## Phase 13A — Portfolio Website / Operator GUI Architecture Baseline (implementation candidate — pending review — not locked — 2026-05-27)

Implementation round. Phase 13A is the first subphase of Phase 13 — Portfolio Website / Operator GUI — the phase that follows the closed Phase 12. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 13A awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 13A does **not** lock Phase 13A, does **not** close Phase 13, and does **not** start Phase 13B or any later Phase 13 subphase.

Phase 13A is a documentation-only architecture-baseline round under no new architecture amendment — it designs the portfolio website and the decoupled operator GUI on paper and refines the earlier `docs/GUI_vision.md` sketch into an authoritative Phase 13 plan, without building any of it. It took the locked Phase 12D artifact `storytime-phase12d-phase12-closure-plan-final-portfolio-handoff.tar.gz` (SHA-256 `64ad09e875f0653608e0deb756f11ee5adc0d2ff1265e2039cbc51491f286cf8`, verified on extraction) as its source. It added five `docs/` documents — `phase13-portfolio-website-architecture.md` (the Phase 13 purpose, the end-state website and operator-GUI vision, audiences and review paths, the website and operator information architectures, the local-first and future-cloud compatibility rules, and the Phase 13 success criteria), `frontend-backend-contract.md` (the "backend owns truth, frontend owns understanding" data contract — read-model categories, future action categories, the actions deliberately disabled for this round, and candidate data-source options), `phase13-roadmap.md` (the Phase 13A–13G subphase decomposition, with each subphase's objective, allowed and forbidden scope, acceptance criteria, and review gate), `portfolio-website-content-model.md` (the website section inventory mapped to existing repository source documents, with a content-honesty checklist), and `operator-gui-view-model.md` (the operator-GUI view inventory, the disabled and future actions, the empty / error / loading states, and the accessibility and readability requirements) — lightly updated `README.md`, and synchronized the State Preservation Bundle.

Confirmed constraints: documentation-only architecture-baseline round. Phase 13A is a planning round; it does not implement the portfolio website and does not implement the operator GUI. No React, Vite, TypeScript, JavaScript, CSS, or HTML application code; no `frontend/` / `web/` / `app/` directory; no `package.json` or `vite.config`; no new product feature, UI, server, dashboard, browser mutation control, external asset, CDN, generated audio, screenshot/image/PDF/PowerPoint/binary asset, demo video, new dependency, or database schema change; no change to pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, API, CLI, or telemetry behaviour; no ARCH-LOCKed contract change; no source change. `pyproject.toml`, `uv.lock`, and the `src/` tree are byte-for-byte unchanged from the source artifact. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 13A current-state expectations: `_CURRENT_PHASE` advanced to "phase 13a", `_LAST_LOCKED_PHASE` advanced to "phase 12d", `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 13A lock, a premature Phase 13 closure, and a premature Phase 13B-or-later start, and a new `_FORBIDDEN_FRONTEND_CLAIMS` list with a parametrized `test_no_frontend_implementation_claimed` check guarding against a false claim that Phase 13A built the frontend, the portfolio website, or the operator GUI. The guard is strengthened, not weakened — the append-only lock-record checks now additionally require the Phase 12D lock record. This test update was explicitly authorized because the test is intentionally phase-specific and otherwise blocks the approved phase transition. The append-only locked-decision documents `docs/canonical-state.md` and the round log in `docs/phase-history.md` were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

**Current state after this round (Phase 13A):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; **Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**; Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — is an implementation candidate, pending review, **not locked**. Phase 13B and every later Phase 13 subphase have not started; Phase 13 is not closed. Phase 9C remains optional/not scheduled.

## Phase 13A — Portfolio Website / Operator GUI Architecture Baseline (LOCKED / ACCEPTED / CANONICAL — 2026-05-27)

Lock closure recorded. Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — the first subphase of Phase 13 — Portfolio Website / Operator GUI — is locked, accepted, and canonical with explicit user approval. Locked artifact lineage: `storytime-phase13a-portfolio-website-operator-gui-architecture-baseline.tar.gz`, SHA-256 `100098aa6280b740a6eeb862c1e1923d2e031bd02a06786b7a8b8ec07facf1c0`.

Phase 13A was a documentation-only architecture-baseline round: it added five architecture-baseline `docs/` documents (`phase13-portfolio-website-architecture.md`, `frontend-backend-contract.md`, `phase13-roadmap.md`, `portfolio-website-content-model.md`, `operator-gui-view-model.md`), lightly updated `README.md`, advanced the state-discipline guard `tests/test_failure_mode_regression.py` under the explicitly authorized §5 mechanical exception, and synchronized the State Preservation Bundle. It added no frontend application code, no `frontend/` directory, no `package.json` or `vite.config`, no React / Vite / TypeScript / CSS / HTML application code, no product feature, UI, server, generated audio, screenshots/binary assets, or new dependency, and changed no pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, API, CLI, telemetry, the database schema, `pyproject.toml`, `uv.lock`, or `src/` content.

Phase 13A completed the Phase Closure Protocol — implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no critical findings, no non-blocking findings, and no required edits; the user, as final decision-maker, then locked Phase 13A. This out-of-band lock was a user/mediator decision supplied to the Phase 13B round; the Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — round records this lock into the append-only canonical state as part of its state synchronization and did not re-perform the reviews. This is the same after-the-fact lock-recording pattern used for Phase 11D and the Phase 12 subphases. The Phase 13A "implementation candidate" entry earlier in this append-only file is preserved as written and is superseded for status purposes by this lock-closure entry.

**Current state after this lock (Phase 13A):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 CLOSED**; Phase 12A–12D all locked; **Phase 12 CLOSED**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**; **Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — is the last locked phase**. Phase 13B is the implementation candidate in the round below. Phase 9C remains optional/not scheduled.

## Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold (implementation candidate — pending review — not locked — 2026-05-27)

Implementation round. Phase 13B is the second subphase of Phase 13 — Portfolio Website / Operator GUI — and the first round of Phase 13 in which frontend code is written. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 13B awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 13B does **not** lock Phase 13B, does **not** close Phase 13, and does **not** start Phase 13C or any later Phase 13 subphase.

Phase 13B took the locked Phase 13A artifact `storytime-phase13a-portfolio-website-operator-gui-architecture-baseline.tar.gz` (SHA-256 `100098aa6280b740a6eeb862c1e1923d2e031bd02a06786b7a8b8ec07facf1c0`, verified on extraction) as its source. Against the locked Phase 13A contract it implements a deliberately bounded frontend: it adds a new top-level `frontend/` directory — a React + TypeScript (strict) + Vite project, standard CSS, and no external UI / component / state / charting library — containing the frontend read-model contract (`frontend/src/types/storytime.ts`), a static demo dataset of exactly two mock pipeline runs (one golden-path successful run, one governance review-required run, in `frontend/src/data/storytime-demo-data.ts`), the portfolio homepage, one Pipeline Run Detail view with a visual Stage Timeline, honest placeholder components for the future portfolio sections and operator views, the frontend scaffold files (`package.json`, `package-lock.json`, `tsconfig.json`, `vite.config.ts`, `index.html`), and a frontend README. It lightly updated `README.md` and synchronized the State Preservation Bundle.

Confirmed constraints: Phase 13B introduces a static, read-only, demo-data-backed frontend shell. It is not backend-connected, uses no live or runtime data, implements no mutations (retry, re-run, and review-decision actions appear only as visibly-disabled affordances), and is not production-hosted or cloud-deployed; it contacts no backend — there is no `fetch()`, no `axios`, and no network call. No backend integration, live data, mutation behaviour, cloud deployment, or Phase 13C+ work exists. No change to pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, API, CLI, telemetry, Docker behaviour, or the database schema; no ARCH-LOCKed contract change. `pyproject.toml`, `uv.lock`, and the `src/` tree are byte-for-byte unchanged from the source artifact. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 13B current-state expectations: `_CURRENT_PHASE` advanced to "phase 13b", `_LAST_LOCKED_PHASE` advanced to "phase 13a", `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 13B lock, a premature Phase 13 closure, and a premature Phase 13C-or-later start, and the Phase 13A `_FORBIDDEN_FRONTEND_CLAIMS` list replaced by a `_FORBIDDEN_OVERCLAIM_CLAIMS` list with a parametrized `test_no_overclaim` check — since Phase 13B legitimately builds a frontend, the guard no longer forbids building one but instead forbids overclaiming it as backend-connected, live-data-powered, mutation-capable, or production / cloud hosted. The guard is strengthened, not weakened — the append-only lock-record checks now additionally require the Phase 13A lock record. This test update was explicitly authorized because the test is intentionally phase-specific and otherwise blocks the approved phase transition. The append-only locked-decision documents `docs/canonical-state.md` and the round log in `docs/phase-history.md` were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

**Current state after this round (Phase 13B):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; Phase 13A locked; **Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**; Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — is an implementation candidate, pending review, **not locked**. Phase 13C and every later Phase 13 subphase have not started; Phase 13 is not closed. Phase 9C remains optional/not scheduled.

## Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold (LOCKED / ACCEPTED / CANONICAL — 2026-05-27)

Lock closure recorded. Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — the second subphase of Phase 13 — Portfolio Website / Operator GUI — is locked, accepted, and canonical with explicit user approval. Locked artifact lineage: `storytime-phase13b-typed-static-portfolio-shell-minimal-visual-pipeline-scaffold.tar.gz`, SHA-256 `9319ece26f5b457ddbbefaab346aba61cb61f65a6b7b729b5acaa12f30df3f24`.

Phase 13B was the first frontend implementation round of Phase 13: it added a new top-level `frontend/` directory — a React + TypeScript (strict) + Vite project, standard CSS, no external UI / component / state / charting library — containing the frontend read-model contract, a static demo dataset of exactly two mock pipeline runs, the portfolio homepage, one Pipeline Run Detail view with a visual Stage Timeline, honest placeholders for the future views, the scaffold files, and a frontend README; it lightly updated `README.md`, advanced the state-discipline guard `tests/test_failure_mode_regression.py` under the explicitly authorized §5 mechanical exception, and synchronized the State Preservation Bundle. Phase 13B is a static, read-only, demo-data-backed shell — not backend-connected, no live data, no mutations, not production-hosted; it contacts no backend (no `fetch()`, no `axios`, no network call). It changed no pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, API, CLI, telemetry, the database schema, `pyproject.toml`, `uv.lock`, or `src/` content.

Phase 13B completed the Phase Closure Protocol — implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no required edits; the user, as final decision-maker, then locked Phase 13B. This out-of-band lock was a user/mediator decision supplied to the Phase 13C round; the Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment — round records this lock into the append-only canonical state as part of its state synchronization and did not re-perform the reviews. This is the same after-the-fact lock-recording pattern used for Phase 11D and the Phase 12 subphases. The Phase 13B "implementation candidate" entry earlier in this append-only file is preserved as written and is superseded for status purposes by this lock-closure entry.

**Current state after this lock (Phase 13B):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 CLOSED**; Phase 12A–12D all locked; **Phase 12 CLOSED**; Phase 13A locked; Phase 13B locked; **Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**. Phase 13C is the implementation candidate in the round below. Phase 9C remains optional/not scheduled.

## Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment (implementation candidate — pending review — not locked — 2026-05-27)

Implementation round. Phase 13C is the third subphase of Phase 13 — Portfolio Website / Operator GUI. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 13C awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 13C does **not** lock Phase 13C, does **not** close Phase 13, and does **not** start Phase 13D or any later Phase 13 subphase.

Phase 13C took the locked Phase 13B artifact `storytime-phase13b-typed-static-portfolio-shell-minimal-visual-pipeline-scaffold.tar.gz` (SHA-256 `9319ece26f5b457ddbbefaab346aba61cb61f65a6b7b729b5acaa12f30df3f24`, verified on extraction) as its source. It establishes a truthful, reproducible, read-only data boundary between backend truth and the Phase 13B frontend, realizing the "backend owns truth, frontend owns understanding" contract: the backend defines the export shape and the frontend mirrors it. Phase 13C adds a small read-only backend export module `src/storytime/operator_export.py` and a `storytime export-demo-ui` CLI command that together produce a deterministic static JSON export, committed at `frontend/src/data/storytime-demo-export.json` and carrying a top-level `schemaVersion` (`"1.0"`); the export contract document `docs/frontend-static-export-contract.md`; the frontend / GUI deferred-work register `docs/frontend-gui-deferred-work-register.md`; a frontend adapter `frontend/src/data/adapter.ts` and a `StaticDemoExport` envelope type appended to `frontend/src/types/storytime.ts`; backend contract tests `tests/test_operator_export.py`; and it rewires the Phase 13B homepage and Pipeline Run Detail / Stage Timeline to consume the export through the adapter (the hand-authored `frontend/src/data/storytime-demo-data.ts` is removed and superseded by the generated export plus the adapter). It updated user-visible Phase 13B → 13C wording in the frontend, lightly updated `README.md`, and synchronized the State Preservation Bundle.

Confirmed constraints: Phase 13C is a static, read-only data-boundary round. The export is deterministic — it is built entirely from fixed demo data with no `datetime.now()`, no `uuid`, no randomness, and no environment-dependent value, and it is serialized with sorted keys and a stable format, so generating it twice yields byte-identical JSON (proven: SHA-256 `0b2989554a1f9fae1c5963527d3f59f882381f253aced2582087c233d42d6156`). Phase 13C does not make the frontend live: it adds no server, no live API, no `fetch`/`axios`, no watcher, no backend-to-frontend runtime coupling, no mutation, no authentication, no cloud deployment, and no production hosting. Unlike Phase 13B, Phase 13C adds small backend code — but it is read-only and deterministic and changes no core pipeline runtime behaviour, no governance, no telemetry, no CLI behaviour beyond the new read-only `export-demo-ui` command, no database schema, and no ARCH-LOCKed contract. `uv.lock` and root dependencies are unchanged; the only `src/` changes are the new `src/storytime/operator_export.py` module and the addition of the `export-demo-ui` command and its import to `src/storytime/cli/app.py`, and `pyproject.toml` changes only by adding `storytime.operator_export` to the two import-linter contract module lists. The `tests/` changes are the new `tests/test_operator_export.py` and the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 13C current-state expectations: `_CURRENT_PHASE` advanced to "phase 13c", `_LAST_LOCKED_PHASE` advanced to "phase 13b", `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 13C lock, a premature Phase 13 closure, and a premature Phase 13D-or-later start, and the `_FORBIDDEN_OVERCLAIM_CLAIMS` list re-anchored to Phase 13C. The guard is strengthened, not weakened — the append-only lock-record checks now additionally require the Phase 13B lock record. This test update was explicitly authorized because the test is intentionally phase-specific and otherwise blocks the approved phase transition. The append-only locked-decision documents `docs/canonical-state.md` and the round log in `docs/phase-history.md` were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

**Current state after this round (Phase 13C):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; Phase 13A locked; Phase 13B locked; **Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**; Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment — is an implementation candidate, pending review, **not locked**. Phase 13D and every later Phase 13 subphase have not started; Phase 13 is not closed. Phase 9C remains optional/not scheduled.

## Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment (LOCKED / ACCEPTED / CANONICAL — 2026-05-27)

Lock closure recorded. Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment — the third subphase of Phase 13 — Portfolio Website / Operator GUI — is locked, accepted, and canonical with explicit user approval. Locked artifact lineage: `storytime-phase13c-deterministic-read-only-static-export-frontend-data-alignment.tar.gz`, SHA-256 `1c24cf03283590d7f095d3805bc8f5d560e3583131c04e5be0359e0053145507`.

Phase 13C established the deterministic, read-only data boundary between backend truth and the Phase 13B frontend. It added a small read-only backend export module `src/storytime/operator_export.py` and a `storytime export-demo-ui` CLI command that together produce a deterministic static JSON export, committed at `frontend/src/data/storytime-demo-export.json` and carrying a top-level `schemaVersion` `"1.0"`; the export contract document `docs/frontend-static-export-contract.md`; the frontend / GUI deferred-work register `docs/frontend-gui-deferred-work-register.md`; a frontend adapter `frontend/src/data/adapter.ts` and a `StaticDemoExport` envelope type; backend contract tests `tests/test_operator_export.py`; and it rewired the homepage and Pipeline Run Detail / Stage Timeline to consume the export through the adapter. The export is deterministic — no `datetime.now()`, no `uuid`, no randomness — and generating it twice yields byte-identical JSON. Phase 13C added no server, no live API, no `fetch`/`axios`, no mutation, no authentication, no cloud deployment, and no production hosting; the small backend code it added changed no core pipeline runtime behaviour and no root dependency.

Phase 13C completed the Phase Closure Protocol — implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no required edits; the user, as final decision-maker, then locked Phase 13C. This out-of-band lock was a user/mediator decision supplied to the Phase 13D round; the Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) — round records this lock into the append-only canonical state as part of its state synchronization and did not re-perform the reviews. This is the same after-the-fact lock-recording pattern used for Phase 11D, the Phase 12 subphases, and Phase 13B. The Phase 13C "implementation candidate" entry earlier in this append-only file is preserved as written and is superseded for status purposes by this lock-closure entry.

**Current state after this lock (Phase 13C):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 CLOSED**; Phase 12A–12D all locked; **Phase 12 CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; **Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**. Phase 13D is the implementation candidate in the round below. Phase 9C remains optional/not scheduled.

## Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) (implementation candidate — pending review — not locked — 2026-05-27)

Implementation round. Phase 13D is the fourth subphase of Phase 13 — Portfolio Website / Operator GUI. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 13D awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 13D does **not** lock Phase 13D, does **not** close Phase 13, and does **not** start Phase 13E or any later Phase 13 subphase.

Phase 13D took the locked Phase 13C artifact `storytime-phase13c-deterministic-read-only-static-export-frontend-data-alignment.tar.gz` (SHA-256 `1c24cf03283590d7f095d3805bc8f5d560e3583131c04e5be0359e0053145507`, verified on extraction) as its source. It is a frontend-only round that expands two of the honest Phase 13B/13C placeholder views into real read-only operator views: **Governance / Safety** (per-run Trust Envelope decisions, source authorization categories, the governance-gate result per run, the display-discipline honesty list, evidence references, and the visibly-disabled future review actions) and **Failure / Recovery** (the failure / review queue joined to per-run failure summaries, affected stage, related governance decision, evidence links, the operator inspect-next guidance, and visibly-disabled recovery actions, with an inspect-this-run drill-down callback into the existing Pipeline Run Detail view). The view choice and ordering followed the Phase 13C deferred-work register's view-expansion recommendation. Phase 13D added two new view components and their CSS Modules (`frontend/src/components/GovernanceSafetyView.tsx` / `GovernanceSafetyView.module.css` and `frontend/src/components/FailureRecoveryView.tsx` / `FailureRecoveryView.module.css`), two domain-specific view-model adapters (`frontend/src/data/governanceAdapter.ts` and `frontend/src/data/failureAdapter.ts`) projecting the locked Phase 13C export, an ambient CSS-Modules TypeScript declaration (`frontend/src/types/css-modules.d.ts`) to enable CSS Modules under strict mode, App-level navigation rewiring with a read-only "Data source · Demo Snapshot" header chip backed by the existing `EXPORT_META` adapter export and an inspect-this-run drill-down callback (plain prop drilling, no router), a tiny `.data-chip` rule in the shared global stylesheet for the header chip (the only global addition; the existing global `src/styles.css` is not migrated), and the documentation updates including a deferred-register entry for the future **Demo / Blue / Green Data Snapshot Switcher**. It synchronized the State Preservation Bundle.

Confirmed constraints: Phase 13D is a static, read-only, export-backed frontend round. It did **not** modify the backend export generator (`src/storytime/operator_export.py`), the committed static export JSON (`frontend/src/data/storytime-demo-export.json`), or the `storytime export-demo-ui` CLI contract; both protected files are byte-identical to the Phase 13C source (verified by `diff -q`). Phase 13D added no server, no live API, no `fetch`/`axios`, no watcher, no backend-to-frontend runtime coupling, no mutation, no authentication, no cloud deployment, and no production hosting; the recovery / review affordances are surfaced as visibly-disabled future actions labelled with the phase that would enable them (Phase 13E). No `src/`, `pyproject.toml`, `uv.lock`, or root dependency changed. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 13D current-state expectations: `_CURRENT_PHASE` advanced to "phase 13d", `_LAST_LOCKED_PHASE` advanced to "phase 13c", `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 13D lock, a premature Phase 13 closure, and a premature Phase 13E-or-later start, and the `_FORBIDDEN_OVERCLAIM_CLAIMS` list re-anchored to Phase 13D. The guard is strengthened, not weakened — the append-only lock-record checks now additionally require the Phase 13C lock record, and a new `test_handoff_state_records_phase_13c_locked` check was added. This test update was explicitly authorized because the test is intentionally phase-specific and otherwise blocks the approved phase transition. The append-only locked-decision documents `docs/canonical-state.md` and the round log in `docs/phase-history.md` were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

**Current state after this round (Phase 13D):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; **Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**; Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) — is an implementation candidate, pending review, **not locked**. Phase 13E and every later Phase 13 subphase have not started; Phase 13 is not closed. Phase 9C remains optional/not scheduled.

## Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) (LOCKED / ACCEPTED / CANONICAL — 2026-05-27)

Lock closure recorded. Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) — the fourth subphase of Phase 13 — Portfolio Website / Operator GUI — is locked, accepted, and canonical with explicit user approval. Locked artifact lineage: `storytime-phase13d-operator-workflow-view-expansion-governance-failure.tar.gz`, SHA-256 `5ec0b1edaaedfed2f3ae9b3e221e6a9089c52b8df152c4824503e7ca796894f3`.

Phase 13D expanded two of the honest Phase 13B/13C placeholder views into real read-only operator views against the locked Phase 13C deterministic static export contract: Governance / Safety and Failure / Recovery, each with per-run drill-down to the existing Pipeline Run Detail view. It added two new view components and their CSS Modules, two domain-specific view-model adapters projecting the locked Phase 13C export, an ambient CSS-Modules TypeScript declaration, App-level navigation rewiring with a read-only "Data source · Demo Snapshot" header chip and an inspect-this-run drill-down (plain prop drilling, no router), and a tiny `.data-chip` rule in the shared global stylesheet for the header chip (the only global addition). The protected Phase 13C boundary held: `src/storytime/operator_export.py`, the committed `frontend/src/data/storytime-demo-export.json`, and the `storytime export-demo-ui` CLI contract were byte-identical to the Phase 13C source. No server, no live API, no `fetch`/`axios`, no mutation, no authentication, no cloud deployment, and no production hosting were introduced; the recovery / review affordances are surfaced as visibly-disabled future actions labelled with Phase 13E. No `src/`, `pyproject.toml`, `uv.lock`, or root dependency changed.

Phase 13D completed the Phase Closure Protocol — implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no required edits; the user, as final decision-maker, then locked Phase 13D. This out-of-band lock was a user/mediator decision supplied to the Phase 13D.1 round; the Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline — round records this lock into the append-only canonical state as part of its state synchronization and did not re-perform the reviews. This is the same after-the-fact lock-recording pattern used for Phase 11D, the Phase 12 subphases, Phase 13B, and Phase 13C. The Phase 13D "implementation candidate" entry earlier in this append-only file is preserved as written and is superseded for status purposes by this lock-closure entry.

**Current state after this lock (Phase 13D):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 CLOSED**; Phase 12A–12D all locked; **Phase 12 CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; Phase 13D locked; **Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**. Phase 13D.1 is the implementation candidate in the round below. Phase 9C remains optional/not scheduled.

## Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline (implementation candidate — pending review — not locked — 2026-05-27)

Implementation round. Phase 13D.1 is a static / read-only refinement sub-round of the locked Phase 13D, intended to strengthen the operator GUI and portfolio / reviewer flow before any future controlled local action or mutation-boundary work. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 13D.1 awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 13D.1 does **not** lock Phase 13D.1, does **not** close Phase 13, and does **not** start Phase 13E or any later Phase 13 subphase.

Phase 13D.1 took the locked Phase 13D artifact `storytime-phase13d-operator-workflow-view-expansion-governance-failure.tar.gz` (SHA-256 `5ec0b1edaaedfed2f3ae9b3e221e6a9089c52b8df152c4824503e7ca796894f3`, verified on extraction) as its source. It is frontend-only and static / read-only. It standardizes the disabled future-action display across views into a reusable typed component (`frontend/src/components/DisabledFutureActionCard.tsx` plus its CSS Module) backed by real `<button disabled={true}>` elements with no `onClick` handlers and no fake mutation props — Governance / Safety and Failure / Recovery were refactored to consume it; replaces the honest Evidence / Validation placeholder with a real read-only view (`frontend/src/components/EvidenceValidationView.tsx` plus its CSS Module) that carries the mandatory **STATIC PORTFOLIO DATA — NOT A LIVE CI/CD DASHBOARD** disclaimer and points to repository-relative evidence (`docs/verification-log.md`, `docs/frontend-static-export-contract.md`, `docs/frontend-gui-deferred-work-register.md`, `docs/phase-history.md`, `docs/artifact-manifest.md`, `tests/test_failure_mode_regression.py`, `tests/test_operator_export.py`) without fabricating runtime CI status; adds an evidence view-model helper (`frontend/src/data/evidenceAdapter.ts`) organising the static evidence categories and the Demo / Active / Candidate Data Source framing — clarifying that Active and Candidate are **data snapshots, not deployment environments**, and that no switching is implemented; and extracts navigation / view-key metadata from `App.tsx` into a small typed `frontend/src/navigation.ts` helper to keep `App.tsx` readable while preserving plain `useState` navigation and the `inspectRun(runId)` prop-drilled drill-down (no router). It synchronizes the State Preservation Bundle including the deferred-work register.

Confirmed constraints: Phase 13D.1 is a static, read-only, export-backed frontend round. It did **not** modify the backend export generator (`src/storytime/operator_export.py`), the committed static export JSON (`frontend/src/data/storytime-demo-export.json`), the `storytime export-demo-ui` CLI contract, or `src/storytime/cli/app.py`; all four protected files / contracts are byte-identical to the Phase 13D source (verified by `diff -q`). Phase 13D.1 added no server, no live API, no `fetch`/`axios`/`localhost`/network call, no watcher, no backend-to-frontend runtime coupling, no mutation, no authentication, no cloud deployment, and no production hosting; the visibly-disabled review and recovery affordances remain visibly disabled and carry no mutation handlers. No `src/`, `pyproject.toml`, `uv.lock`, or root dependency changed. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 13D.1 current-state expectations: `_CURRENT_PHASE` advanced to "phase 13d.1", `_LAST_LOCKED_PHASE` advanced to "phase 13d", `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 13D.1 lock, a premature Phase 13 closure, and a premature Phase 13E-or-later start (and to allow the now-legitimate "phase 13d is locked" claims), the `_FORBIDDEN_OVERCLAIM_CLAIMS` list re-anchored to Phase 13D.1 with new entries forbidding live-CI, snapshot-switching, and promotion overclaims, a new `test_handoff_state_records_phase_13d_locked` check was added, and the append-only lock-record checks now additionally require the Phase 13D lock record. The "current phase not claimed locked" check was rewritten to do a direct substring scan for `"phase 13d.1 is locked"` and its variants rather than relying on fragment splitting (the period inside the "Phase 13D.1" label is itself a fragment-split character). The guard is strengthened, not weakened. This test update was explicitly authorized because the test is intentionally phase-specific and otherwise blocks the approved phase transition. The append-only locked-decision documents `docs/canonical-state.md` and the round log in `docs/phase-history.md` were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

**Current state after this round (Phase 13D.1):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; Phase 13D locked; **Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**; Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline — is an implementation candidate, pending review, **not locked**. Phase 13E and every later Phase 13 subphase have not started; Phase 13 is not closed. Phase 9C remains optional/not scheduled.

## Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline (LOCKED / ACCEPTED / CANONICAL — 2026-05-27)

Lock closure recorded. Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline — a sub-round of Phase 13D — is locked, accepted, and canonical with explicit user approval. Locked artifact lineage: `storytime-phase13d1-static-operator-gui-refinement-evidence-disabled-actions.tar.gz`, SHA-256 `812841381075e0e7839266512eb6d7f41bf2d890ee4c82b91627ce824f5b1eae`.

Phase 13D.1 standardized the disabled future-action display across views into a reusable typed component (`frontend/src/components/DisabledFutureActionCard.tsx` plus its CSS Module) backed by real `<button disabled={true}>` elements with no `onClick` handlers and no fake mutation props; Governance / Safety and Failure / Recovery were refactored to consume it. It replaced the Evidence / Validation placeholder with a real read-only view (`frontend/src/components/EvidenceValidationView.tsx` plus its CSS Module) carrying the mandatory STATIC PORTFOLIO DATA — NOT A LIVE CI/CD DASHBOARD disclaimer and repository-relative evidence references, added an evidence adapter (`frontend/src/data/evidenceAdapter.ts`) organising static evidence categories and the Demo / Active / Candidate Data Source framing (data snapshots, not deployment environments), and extracted navigation / view-key metadata from `App.tsx` into a small typed `frontend/src/navigation.ts` helper (App.tsx slimmed from 228 to 136 lines). The protected Phase 13D boundary held: `src/storytime/operator_export.py`, the committed `frontend/src/data/storytime-demo-export.json`, the `storytime export-demo-ui` CLI contract, and `src/storytime/cli/app.py` were byte-identical to the Phase 13D source. No server, no live API, no `fetch`/`axios`, no mutation, no authentication, no cloud deployment, and no production hosting were introduced; recovery / review affordances remained visibly disabled. No `src/`, `pyproject.toml`, `uv.lock`, `frontend/package.json`, `frontend/package-lock.json`, or root dependency changed.

Phase 13D.1 completed the Phase Closure Protocol — implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no required edits; the user, as final decision-maker, then locked Phase 13D.1. This out-of-band lock was a user/mediator decision supplied to the Phase 13D.2 round; the Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path — round records this lock into the append-only canonical state as part of its state synchronization and did not re-perform the reviews. This is the same after-the-fact lock-recording pattern used for Phase 11D, the Phase 12 subphases, Phase 13B, Phase 13C, and Phase 13D. The Phase 13D.1 "implementation candidate" entry earlier in this append-only file is preserved as written and is superseded for status purposes by this lock-closure entry.

**Current state after this lock (Phase 13D.1):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 CLOSED**; Phase 12A–12D all locked; **Phase 12 CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; Phase 13D locked; Phase 13D.1 locked; **Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**. Phase 13D.2 is the implementation candidate in the round below. Phase 9C remains optional/not scheduled.

## Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path (implementation candidate — pending review — not locked — 2026-05-27)

Implementation round. Phase 13D.2 is a static / read-only demo-readiness sub-round of the locked Phase 13D.1, turning the existing operator GUI views into a coherent guided reviewer / demo path before any future controlled local action or mutation-boundary work. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 13D.2 awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 13D.2 does **not** lock Phase 13D.2, does **not** close Phase 13, and does **not** start Phase 13E or any later Phase 13 subphase.

Phase 13D.2 took the locked Phase 13D.1 artifact `storytime-phase13d1-static-operator-gui-refinement-evidence-disabled-actions.tar.gz` (SHA-256 `812841381075e0e7839266512eb6d7f41bf2d890ee4c82b91627ce824f5b1eae`, verified on extraction) as its source. It is frontend-only and static / read-only. It replaces the honest Demo Walkthrough placeholder with a real read-only view (`frontend/src/components/DemoWalkthroughView.tsx` plus its CSS Module) backed by a static view-model adapter (`frontend/src/data/demoWalkthroughAdapter.ts`) that holds the long-form route content (route definitions, step definitions, architecture checkpoints, deferred-work framing, interview / SE talking points, repository references). The view offers four reviewer routes — a 5-minute scan, a 10-minute SE-style demo, a technical deep-dive, and a self-guided reviewer path — switched by a simple segmented control backed by local `useState<RouteId>` (no router, no Context, no persistence). Each step carries title, target view, what to inspect, what it proves, talking points, and an in-line navigation affordance into the relevant existing view; steps that point to a specific run identify it by stable id (`run-2026-0518-golden` for the golden-path run; `run-2026-0520-review` for the review-required run) so the reviewer is never asked to guess. The view also includes architecture-checkpoint cards (local-first design, deterministic static export, backend owns truth / frontend owns understanding, read-only operator surface, static evidence boundary, disabled-action boundary, Demo / Active / Candidate as **data snapshots, not deployment environments**, and why Phase 13E must be explicitly gated), a deliberate "what is intentionally deferred" section, and interview / SE talking-point callout cards. Phase 13D.2 absorbs ~80–90% of an Architecture Story narrative via these embedded checkpoints but does NOT implement a full standalone Architecture Story page — that stays deferred and is recorded as a new item in `docs/frontend-gui-deferred-work-register.md` ("Standalone Architecture Story / System Boundary Reference"). Navigation: `frontend/src/navigation.ts` was updated so Demo Walkthrough is a real view (the remaining placeholders still point to Phase 13E or later); `frontend/src/App.tsx` was lightly updated to render the new view and pass a navigation callback down; no router, no Context, no global state introduced.

Confirmed constraints: Phase 13D.2 is a static, read-only, export-backed frontend round. It did **not** modify the backend export generator (`src/storytime/operator_export.py`), the committed static export JSON (`frontend/src/data/storytime-demo-export.json`), the `storytime export-demo-ui` CLI contract, or `src/storytime/cli/app.py`; all four protected files / contracts are byte-identical to the Phase 13D.1 source (verified by `diff -q`). Phase 13D.2 added no server, no live API, no `fetch`/`axios`/`localhost`/network call, no watcher, no backend-to-frontend runtime coupling, no mutation, no authentication, no cloud deployment, no production hosting, no dynamic file loading, and no Demo / Active / Candidate switching; the visibly-disabled review and recovery affordances remain visibly disabled and carry no mutation handlers. No `src/`, `pyproject.toml`, `uv.lock`, `frontend/package.json`, `frontend/package-lock.json`, or root dependency changed. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 13D.2 current-state expectations: `_CURRENT_PHASE` advanced to "phase 13d.2", `_LAST_LOCKED_PHASE` advanced to "phase 13d.1", `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 13D.2 lock, a premature Phase 13 closure, and a premature Phase 13E-or-later start (and to allow the now-legitimate "phase 13d.1 is locked" claims), the `_FORBIDDEN_OVERCLAIM_CLAIMS` list re-anchored to Phase 13D.2 with new entries forbidding live-CI / live-telemetry, snapshot-switching, dynamic-loading, and standalone-architecture-story overclaims, a new `test_handoff_state_records_phase_13d1_locked` check was added, and the append-only lock-record checks now additionally require the Phase 13D.1 lock record. The "current phase not claimed locked" check continues to use a direct substring scan (the period inside the "Phase 13D.2" label is itself a fragment-split character). The guard is strengthened, not weakened. This test update was explicitly authorized because the test is intentionally phase-specific and otherwise blocks the approved phase transition. The append-only locked-decision documents `docs/canonical-state.md` and the round log in `docs/phase-history.md` were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

**Current state after this round (Phase 13D.2):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; Phase 13D locked; Phase 13D.1 locked; **Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**; Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path — is an implementation candidate, pending review, **not locked**. Phase 13E and every later Phase 13 subphase have not started; Phase 13 is not closed. Phase 9C remains optional/not scheduled.

## Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path (LOCKED / ACCEPTED / CANONICAL — 2026-05-27)

Lock closure recorded. Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path — a sub-round of Phase 13D.1 — is locked, accepted, and canonical with explicit user approval. Locked artifact lineage: `storytime-phase13d2-static-demo-walkthrough-reviewer-story-path.tar.gz`, SHA-256 `cd553679ce109483b69e99f51fceab34af216c9b1ce7dfe859fc7b78c13cd429`.

Phase 13D.2 replaced the honest Demo Walkthrough placeholder with a real read-only guided reviewer / demo path view (`frontend/src/components/DemoWalkthroughView.tsx` plus its CSS Module) backed by a static view-model adapter (`frontend/src/data/demoWalkthroughAdapter.ts`) holding the long-form route content, offered four reviewer routes (5-minute scan, 10-minute SE-style demo, technical deep-dive, self-guided reviewer) via a simple segmented control backed by `useState<RouteId>` (no router, no Context, no persistence), and embedded eight architecture-checkpoint cards absorbing ~80–90% of an Architecture Story narrative. A standalone Architecture Story page remained deferred and was recorded as a new "Standalone Architecture Story / System Boundary Reference" item in `docs/frontend-gui-deferred-work-register.md`. The protected Phase 13D.1 boundary held: `src/storytime/operator_export.py`, `frontend/src/data/storytime-demo-export.json`, the `storytime export-demo-ui` CLI contract, and `src/storytime/cli/app.py` were byte-identical to the Phase 13D.1 source. No server, no live API, no `fetch`/`axios`, no mutation, no dynamic file loading, no snapshot switching, no router, no Context, no global state, no authentication, no cloud deployment, and no production hosting were introduced; recovery / review affordances remained visibly disabled. No `src/`, `pyproject.toml`, `uv.lock`, `frontend/package.json`, `frontend/package-lock.json`, or root dependency changed.

Phase 13D.2 completed the Phase Closure Protocol — implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no required edits; the user, as final decision-maker, then locked Phase 13D.2. This out-of-band lock was a user/mediator decision supplied to the Phase 13E round; the Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary — round records this lock into the append-only canonical state as part of its state synchronization and did not re-perform the reviews. This is the same after-the-fact lock-recording pattern used for Phase 11D, the Phase 12 subphases, Phase 13B, Phase 13C, Phase 13D, and Phase 13D.1. The Phase 13D.2 "implementation candidate" entry earlier in this append-only file is preserved as written and is superseded for status purposes by this lock-closure entry.

**Current state after this lock (Phase 13D.2):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 CLOSED**; Phase 12A–12D all locked; **Phase 12 CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; Phase 13D locked; Phase 13D.1 locked; Phase 13D.2 locked; **Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**. Phase 13E is the implementation candidate in the round below. Phase 9C remains optional/not scheduled.

## Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary (implementation candidate — pending review — not locked — 2026-05-27)

Implementation round. Phase 13E is a static, **Demo-mode-only**, **non-consequential** sub-round of the locked Phase 13D.2, intended to turn the existing visibly-disabled future-action affordances into explainable, non-executing action previews before any future real local action or mutation work. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 13E awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 13E does **not** lock Phase 13E, does **not** close Phase 13, and does **not** start Phase 13F or any later Phase 13 subphase.

Phase 13E took the locked Phase 13D.2 artifact `storytime-phase13d2-static-demo-walkthrough-reviewer-story-path.tar.gz` (SHA-256 `cd553679ce109483b69e99f51fceab34af216c9b1ce7dfe859fc7b78c13cd429`, verified on extraction) as its source. It is frontend-only and static, Demo-mode-only. It adds a static Demo-mode Action Preview system — `frontend/src/data/actionPreviewAdapter.ts` (the typed static view-model holding action-preview definitions: stable action id, label, category, current mode (Demo), execution status (Preview only / non-consequential), target object references for run / stage / governance decision / failure queue / evidence artifact, what the operator is trying to accomplish, why it is blocked in Demo mode, precondition checklist, evidence to inspect, risk level, illustrative future Local-mode request shape labelled "Future request shape — illustrative only, not executable in Demo mode", Cloud/Distributed considerations, audit expectations, failure behaviour expectation, what remains disabled, related view; plus operating-mode model constants for Demo / Local / Cloud-Distributed) and `frontend/src/components/ActionPreviewPanel.tsx` plus its CSS Module (a presentation panel rendering the selected preview). The panel is integrated into Failure / Recovery, Governance / Safety, and Evidence / Validation **alongside** the existing `DisabledFutureActionCard` (unchanged: a real `<button disabled={true}>` with no `onClick`). A separate, clearly-labelled "Preview action plan" control opens the inline preview panel; the preview never looks like execution, there is no fake loading spinner, no simulated success state, no `setTimeout` workflow, and no "Submitted" / "Succeeded" / "Audit created" rendering anywhere. The first set of previews covers retry-failed-stage (target run `run-2026-0520-review`, stage `run-2026-0520-review:governance-gate`), inspect-trust-envelope (target run `run-2026-0520-review`), record-review-decision (target run `run-2026-0520-review`, related disabled action `run-2026-0520-review:open-review`), regenerate-operator-report (target evidence/report surface), and refresh-export (target static export). Phase 13E introduces or clarifies the eventual operating-mode model — **Demo mode** (curated, safe, non-consequential, portfolio-ready; the only mode implemented), **Local mode** (future real local operator workflows; not implemented in Phase 13E), and **Cloud / Distributed mode** (future hosted/distributed execution; not implemented in Phase 13E) — distinct from the existing **Demo / Active / Candidate** data-snapshot labels (which Phase 13D.1's Evidence / Validation view already framed and which Phase 13E does not replace).

Confirmed constraints: Phase 13E is a static, Demo-mode-only, export-backed frontend round. It did **not** modify the backend export generator (`src/storytime/operator_export.py`), the committed static export JSON (`frontend/src/data/storytime-demo-export.json`), the `storytime export-demo-ui` CLI contract, or `src/storytime/cli/app.py`; all four protected files / contracts are byte-identical to the Phase 13D.2 source (verified by `diff -q`). Phase 13E added no server, no live API, no `fetch`/`axios`/`localhost`/network call, no `localStorage`/`sessionStorage`, no router/hash routing/browser History API, no Context provider, no global preview/action state, no actual retry/rerun/approval/report regeneration/export refresh, no authentication, no Local mode, no Cloud/Distributed mode, no audit-record generation (nothing executed), no production hosting, no fake-execution surface, no Demo/Active/Candidate snapshot switching, and no dynamic file loading; the visibly-disabled review and recovery affordances remain visibly disabled and carry no mutation handlers — the Phase 13D.1 `DisabledFutureActionCard` was not modified. No `src/`, `pyproject.toml`, `uv.lock`, `frontend/package.json`, `frontend/package-lock.json`, or root dependency changed. The `tests/` changes are the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 13E current-state expectations (`_CURRENT_PHASE` advanced to "phase 13e", `_LAST_LOCKED_PHASE` advanced to "phase 13d.2", `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 13E lock, a premature Phase 13 closure, and a premature Phase 13F-or-later start — and to allow the now-legitimate "phase 13d.2 is locked" claims; the `_FORBIDDEN_OVERCLAIM_CLAIMS` list re-anchored to Phase 13E with new entries forbidding overclaims of real action execution, real retry/rerun/approval/report regeneration, Local mode, Cloud/Distributed mode, local bridge/local server, audit-record generation, persisted action state, backend connection, live data, snapshot switching, and production/cloud hosting; a new `test_handoff_state_records_phase_13d2_locked` check was added; the prior 13E-explicit framing check was renamed to `test_handoff_state_addresses_phase_13f_explicitly`; the append-only lock-record checks now additionally require the Phase 13D.2 lock record; the future-phase fragment scan advanced to `13f`/`13g`), and one new `tests/test_action_preview_data_integrity.py` that opens both `frontend/src/data/storytime-demo-export.json` and `frontend/src/data/actionPreviewAdapter.ts` (as text), extracts run-id and stage-id patterns referenced by the adapter, and asserts each exists in the committed static export — at minimum asserting `run-2026-0518-golden` and `run-2026-0520-review` are present in both. Coverage is strengthened, not weakened. The append-only locked-decision documents `docs/canonical-state.md` and the round log in `docs/phase-history.md` were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

**Current state after this round (Phase 13E):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; Phase 13D locked; Phase 13D.1 locked; Phase 13D.2 locked; **Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**; Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary — is an implementation candidate, pending review, **not locked**. Phase 13F and every later Phase 13 subphase have not started; Phase 13 is not closed. Phase 9C remains optional/not scheduled.

## Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary (LOCKED / ACCEPTED / CANONICAL — 2026-05-27)

Lock closure recorded. Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary — a sub-round of Phase 13D.2 — is locked, accepted, and canonical with explicit user approval. Locked artifact lineage: `storytime-phase13e-demo-mode-action-preview-operator-intent-boundary.tar.gz`, SHA-256 `a997f2ca9d213e28e140f47c63336367c8feda46ed994b41300f86b99f8d8164`.

Phase 13E added a static Demo-mode Action Preview system — a typed static view-model adapter (`frontend/src/data/actionPreviewAdapter.ts`) and a presentation panel (`frontend/src/components/ActionPreviewPanel.tsx` plus its CSS Module) — letting the operator GUI preview what a real operator action would look like under future Local or Cloud/Distributed mode without ever executing one. The panel was integrated into the Failure / Recovery, Governance / Safety, and Evidence / Validation views alongside the unchanged `DisabledFutureActionCard` (a real `<button disabled={true}>` with no `onClick`), opened by a separate, clearly-labelled "Preview action plan" control; the preview never looks like execution and renders no fake success state. It clarified the Demo / Local / Cloud-Distributed operating-mode model (distinct from the Demo / Active / Candidate data-snapshot model) and added a Python data-integrity test (`tests/test_action_preview_data_integrity.py`) asserting the run-id and other target ids referenced by the adapter exist in the committed static export. The protected Phase 13D.2 boundary held: `src/storytime/operator_export.py`, `frontend/src/data/storytime-demo-export.json`, the `storytime export-demo-ui` CLI contract, and `src/storytime/cli/app.py` were byte-identical to the Phase 13D.2 source, and `DisabledFutureActionCard` remained byte-identical and truly disabled. No server, no live API, no `fetch`/`axios`, no mutation, no Local mode, no Cloud/Distributed mode, no audit records (nothing executed), no `localStorage`/`sessionStorage`, no router/Context/global state, and no production hosting were introduced. No `src/`, `pyproject.toml`, `uv.lock`, `frontend/package.json`, `frontend/package-lock.json`, or root dependency changed.

Phase 13E completed the Phase Closure Protocol — implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no required edits; the user, as final decision-maker, then locked Phase 13E. This out-of-band lock was a user/mediator decision supplied to the Phase 13F round; the Phase 13F — Local Bridge Architecture & Contract Baseline — round records this lock into the append-only canonical state as part of its state synchronization and did not re-perform the reviews. This is the same after-the-fact lock-recording pattern used for Phase 11D, the Phase 12 subphases, Phase 13B, Phase 13C, Phase 13D, Phase 13D.1, and Phase 13D.2. The Phase 13E "implementation candidate" entry earlier in this append-only file is preserved as written and is superseded for status purposes by this lock-closure entry.

**Current state after this lock (Phase 13E):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 CLOSED**; Phase 12A–12D all locked; **Phase 12 CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; Phase 13D locked; Phase 13D.1 locked; Phase 13D.2 locked; Phase 13E locked; **Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**. Phase 13F is the implementation candidate in the round below. Phase 9C remains optional/not scheduled.

## Phase 13F — Local Bridge Architecture & Contract Baseline (implementation candidate — pending review — not locked — 2026-05-27)

Implementation round. Phase 13F is a documentation-and-static-fixture architecture / contract baseline sub-round of the locked Phase 13E — the architectural lock before any Python local-bridge implementation is allowed (it is to the Local Bridge what Phase 13A was to the operator GUI). Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 13F awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 13F does **not** lock Phase 13F, does **not** close Phase 13, and does **not** start Phase 13G or any later Phase 13 subphase.

Phase 13F took the locked Phase 13E artifact `storytime-phase13e-demo-mode-action-preview-operator-intent-boundary.tar.gz` (SHA-256 `a997f2ca9d213e28e140f47c63336367c8feda46ed994b41300f86b99f8d8164`, verified on extraction) as its source. It adds eleven new architecture / contract docs: `docs/local-bridge-architecture.md` (why a browser cannot execute local commands, why a local bridge is required for real Local mode, why Phase 13F does not implement it, the future bridge shape, loopback-only binding (`127.0.0.1`/`::1`, reject non-loopback, never `0.0.0.0`), CORS/origin allowlist, strict DTO boundary, the no-arbitrary-command rule, the action allowlist, the command-pattern router mapping one action to one pre-approved Python operation, the response/error/shutdown model, the action-completion→export-refresh update loop, the §15 execution-timing policy, and a §16 risk table mapping the five Gemini risks); `docs/externalized-state-architecture.md`; `docs/browser-storage-policy.md`; `docs/local-mode-workspace-layout.md`; `docs/storage-targets-architecture.md`; `docs/action-execution-boundary.md`; `docs/local-action-dto-spec.md`; `docs/local-action-audit-spec.md`; `docs/local-mode-storage-contract.md`; `docs/local-action-queue-observability.md`; and `docs/phase13f-local-bridge-contract-readiness.md`. It adds a set of non-runtime JSON example fixtures under `docs/examples/` (local-action-requests: retry-failed-stage, inspect-trust-envelope, refresh-export; local-action-responses: retry-failed-stage.accepted, refresh-export.accepted; local-action-audit-records: retry-failed-stage.audit) labelled as future / documentation-only, carrying no secrets / shell / SQL / private paths, using stable demo-safe ids and workspace-relative references. It adds one new Python test (`tests/test_local_mode_contract_examples.py`) validating those fixtures with plain Python (no JSON-schema dependency): required fields by type, allowlisted-action use, deferred-action absence, workspace + storageTarget presence, idempotency key for retry, accepted≠succeeded, async accepted→actionRequestId/jobId, audit→requestId/idempotencyKey, and no forbidden content. The central principle established: the frontend is an operator surface, not the durable storage layer — durable state must live outside the browser in an explicit workspace / storage target with clear export, reset, backup, and recovery semantics, so StoryTime never repeats the RoundTable browser-storage failure mode; the browser may hold transient UI state only and `localStorage`/`sessionStorage`/`IndexedDB` remain forbidden. The Hybrid Option C decisions are settled: an execution-timing policy (long-running actions asynchronous; the future bridge returns `202 Accepted` with `actionRequestId`/`jobId`; acceptance is not success; export refresh after a durable write; refresh-race avoidance via atomic write + identity-tagged read model); the loopback-only / strict-origin / no-arbitrary-command / command-pattern-router security boundary; the action allowlist (`retry_failed_stage`, `inspect_trust_envelope`, `refresh_export`) with higher-risk actions (`record_review_decision`, `regenerate_operator_report`, `publish_episode`, `delete_artifact`, provider sync) deferred; and a queue-observability model (depth, in-flight, completed/failed/rejected/dead-letter counts, oldest-queued and longest-in-flight ages, retry count, capacity, saturation, export freshness) plus a conservative local load-limit policy and distributed/cloud carry-forward.

Confirmed constraints: Phase 13F is a documentation-and-static-fixture round and implements **no** runtime code. It did **not** modify `src/`, `frontend/src/` (including `frontend/src/data/storytime-demo-export.json`), `frontend/package.json`, `frontend/package-lock.json`, `pyproject.toml`, or `uv.lock`; all are byte-identical to the locked Phase 13E source (verified by `diff -q`). Phase 13F implemented no local bridge, no server, no socket, no subprocess, no async queue, no queue workers, no queue metrics / exporters, no OpenTelemetry instrumentation, no storage providers, no provider integrations, no runtime schema validation, no router / history, no browser storage, no real Local mode, no Cloud/Distributed mode, and no mutation / action execution; the browser remains non-durable and the example fixtures are documentation artifacts only (never imported by runtime code, never generated by a running system, never claiming Phase 13F executed anything). The only `tests/` changes are the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 13F current-state expectations (`_CURRENT_PHASE` advanced to "phase 13f", `_LAST_LOCKED_PHASE` advanced to "phase 13e", `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 13F lock, a premature Phase 13 closure, and a premature Phase 13G/13H start — and to allow the now-legitimate "phase 13e is locked" claims; the `_FORBIDDEN_OVERCLAIM_CLAIMS` list re-anchored to Phase 13F with entries forbidding overclaims of implementing a local bridge, a server, an async queue, queue workers, queue metrics/exporters, OpenTelemetry, storage providers, real Local mode, Cloud/Distributed mode, mutation/action execution, runtime DTOs, runtime schema validation, browser storage, and `localStorage`/`sessionStorage`/`IndexedDB`; a new `test_handoff_state_records_phase_13e_locked` check was added; the prior 13F-explicit framing check was renamed to `test_handoff_state_addresses_phase_13g_explicitly`; the append-only lock-record checks now additionally require the Phase 13E lock record; the future-phase fragment scan advanced to `13g`/`13h`), and the new `tests/test_local_mode_contract_examples.py`. Coverage is strengthened, not weakened. The append-only locked-decision documents `docs/canonical-state.md` and the round log in `docs/phase-history.md` were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

**Current state after this round (Phase 13F):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; Phase 13D locked; Phase 13D.1 locked; Phase 13D.2 locked; Phase 13E locked; **Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**; Phase 13F — Local Bridge Architecture & Contract Baseline — is an implementation candidate, pending review, **not locked**. Phase 13G and every later Phase 13 subphase have not started; Phase 13 is not closed. Phase 9C remains optional/not scheduled.


## Phase 13G – 13K — Demo + Local Proof Track (lock-lineage catch-up record — LOCKED) — 2026-05-28

This append-only record consolidates the lock lineage for Phase 13G through Phase 13K, which were tracked in the prepended current-state note across rounds and are recorded here as a body record at Phase 13 closure. Each was locked by the user as final decision-maker under the Phase Closure Protocol (GPT preliminary verification, Gemini implementation review, any cleanup, explicit approval), with protected surfaces byte-identical and archive hygiene clean at each transition:

- **Phase 13G — Local Bridge Implementation (standard-library loopback bridge) — LOCKED.** The first real local bridge: a loopback-only (`127.0.0.1`/`::1`) standard-library HTTP bridge with a strict DTO boundary, an action allowlist, and a command-pattern router; no arbitrary command execution.
- **Phase 13G.1 — Local Bridge Cleanup — LOCKED.** Bounded hardening/cleanup folded into the Phase 13G lock lineage.
- **Phase 13H — Controlled Async Retry Submission — LOCKED.** Controlled, asynchronous `retry_failed_stage` submission with `202 Accepted` semantics; acceptance is not success.
- **Phase 13H.1 — Controlled Retry Submission from Frontend — LOCKED.**
- **Phase 13H.2 — Frontend Boundary Cleanup / Local Bridge Component Hardening — LOCKED.**
- **Phase 13H.3 — Manual Static Export Reload / Read-Model Replacement Boundary — LOCKED.** A manual reload is a read-model refresh, not a live sync.
- **Phase 13I — Governed Local TTS Proof / Audio Artifact Boundary — LOCKED.** A governed, mock-first TTS proof and audio-artifact boundary; mock output is labeled mock, not real provider audio; the real provider stays deferred.
- **Phase 13J — Operator GUI Polish / Demo-Local Alignment — LOCKED.** Operator-GUI polish aligning the demo and local surfaces.
- **Phase 13K — Demo Walkthrough Refresh / Governed Local Chain Story Path — LOCKED (2026-05-28).** Designated `docs/demo-walkthrough.md` as the single canonical reviewer/demo path, refreshed the in-app Demo Walkthrough view and adapter to tell the true governed local-chain story with an evidence map, and reconciled stale demo/portfolio docs. Locked artifact `storytime-phase13k-demo-walkthrough-refresh-governed-local-chain-story-path.tar.gz`, SHA-256 `bf3bcc87cd147205558eddd16b53c5a09e91af1bfa6269d10a8de153a7e6f10a`. Lock basis: GPT preliminary verification PASS, Gemini implementation review SAFE TO LOCK, no required edits, protected surfaces byte-identical, archive hygiene clean.

**Phase 13K is the last locked phase.** Phase 13 — Portfolio Website / Operator GUI — remains STARTED.

## Phase 13L — Phase 13 Closure / Demo-Local Completion Lock (implementation candidate — pending review — not locked — 2026-05-28)

Phase 13L is a closure / documentation round over the locked Phase 13K. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 13L awaits GPT review, Gemini critique, any cleanup, and explicit user approval. Phase 13L does **not** lock Phase 13L, does **not** itself close Phase 13, and does **not** start or implement Phase 14.

Phase 13L took the locked Phase 13K artifact (SHA-256 `bf3bcc87cd147205558eddd16b53c5a09e91af1bfa6269d10a8de153a7e6f10a`, verified on extraction) as its source. It records the Phase 13K lock in every living state document; advances the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 13L current-state expectations (`_CURRENT_PHASE` advanced to "phase 13l", `_LAST_LOCKED_PHASE` advanced to "phase 13k", the forbidden-future list re-anchored to forbid a premature Phase 13L lock, a premature Phase 13 closure, a phantom Phase 13M, and any claim that Phase 14 / 14A has started, is locked, or is implemented; the overclaim list re-anchored to Phase 13L; new checks requiring Phase 13K recorded as locked and Phase 14 framed as not started; the append-only retention checks now also require the Phase 13K lock record; the future-phase fragment scan advanced to `phase 14`); and adds two concise documents — `docs/phase13-closure.md` (the Phase 13 closure summary, final locked sub-phase sequence, Demo + Local proof accomplishments, canonical reviewer surface, local-bridge / browser-authority / governed-TTS boundaries, deferred-capability register, Phase 14 readiness pointer, validation/lock evidence, and final current-state declaration) and `docs/phase14-readiness-handoff.md` (an architecture-first, implementation-free handoff framing the next, not-yet-started Phase 14A — Cloud/Distributed Architecture Baseline). It preserves `docs/demo-walkthrough.md` as the single canonical reviewer path rather than duplicating it.

Confirmed constraints: Phase 13L is a documentation-and-tests round and implements **no** runtime code. It did **not** modify `pyproject.toml`, `uv.lock`, `src/`, `frontend/src/` (including `frontend/src/data/storytime-demo-export.json` and `frontend/src/data/adapter.ts`), `frontend/package.json`, `frontend/package-lock.json`, `frontend/vite.config.ts`, or `frontend/tsconfig.json`; all are byte-identical to the locked Phase 13K source (verified by `diff -q`). It added no backend behavior, no local bridge action, no frontend TTS generation, no audio playback, no provider integration, no browser storage, no polling / live sync, no cloud / distributed / full Local mode, no RSS publishing, no authentication, and no cloud deployment. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard. The append-only locked-decision documents were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

**Current state after this round (Phase 13L candidate):** Phase 10 CLOSED; Phase 11 CLOSED; Phase 12 CLOSED; Phase 13A–13F locked; Phase 13D.1 / 13D.2 locked; Phase 13G / 13G.1 locked; Phase 13H / 13H.1 / 13H.2 / 13H.3 locked; Phase 13I locked; Phase 13J locked; **Phase 13K locked — the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**; Phase 13L — Phase 13 Closure / Demo-Local Completion Lock — is an implementation candidate, pending review, **not locked**. Phase 13L prepares the Phase 13 closure as a candidate; Phase 13 will be formally closed only after Phase 13L review/lock, so Phase 13 is not yet closed. Phase 14 — Cloud/Distributed — has not started; Phase 14A is the next proposed architecture baseline and is NOT STARTED. Phase 9C remains optional/not scheduled.


---

## Phase 14A.1 — Local Live Proof Loop Before Cloud (implementation candidate; pending review; NOT locked)

**Date:** 2026-05-29

Phase 14A.1 took the locked Phase 13L artifact (SHA-256 `acecdf0aac7e6f184be1c368e37f65170bf25365751090adfc394ffdde2e5a53`, verified on extraction) as its source. With Phase 13L locked, **Phase 13 — Portfolio Website / Operator GUI — is now formally CLOSED**, and Phase 13L is the last locked phase. **Phase 14 — Live System / Cloud-Distributed — is now STARTED**, and Phase 14A.1 — Local Live Proof Loop Before Cloud — is the current implementation candidate (pending review, NOT locked).

Unlike the Phase 13L closure round, Phase 14A.1 is a real implementation round. It adds a new backend package `src/storytime/local_live/` (a loopback-only standard-library HTTP API exposing read-only backend-owned durable run state plus one controlled proof-run action; a typed read model; and a durable proof-run harness), a `storytime local-live` CLI command, a frontend "Live Proof Loop" surface (`frontend/src/components/LiveProofView.tsx` + `frontend/src/data/liveProofClient.ts`, wired into navigation), three architecture docs (`docs/phase14-live-system-architecture.md`, `docs/phase14-proof-loop.md`, `docs/phase14-cloud-distributed-roadmap.md`), and targeted tests (`tests/test_local_live_proof_loop.py`). It advances the state-discipline guard `tests/test_failure_mode_regression.py` to track the Phase 14A.1 current-state expectations (`_CURRENT_PHASE` → "phase 14a.1", `_LAST_LOCKED_PHASE` → "phase 13l"; the forbidden-future list re-anchored to forbid a premature Phase 14A.1 lock, a premature Phase 14 closure, and any claim that the reserved Phase 14B.1+ bundle has started/locked/current; the overclaim list re-anchored to forbid claiming Phase 14A.1 added cloud/distributed mode, provider-backed TTS, frontend audio/TTS generation, audio playback, RSS publishing, authentication, or cloud deployment; new checks requiring Phase 13 recorded as closed, Phase 13L as locked, and Phase 14 as started; the append-only retention checks now also require the Phase 13L lock record; the future-phase fragment scan advanced to `phase 14b`).

The proof run persists real durable state to SQLite through the existing `StateStore` contracts (`pipeline_run`, `stage_execution`, append-only `event_log`, `stage_artifact`) and a real on-disk evidence artifact; the run history survives a local-live server restart (verified by tests). The browser submits no arbitrary text, paths, URLs, providers, or credentials — only an allowlisted approved CC0 fixture can be triggered. The local-live API binds loopback only with a strict origin allowlist (loopback + Vite dev origins) and never emits a wildcard `Access-Control-Allow-Origin`.

Confirmed constraints: Phase 14A.1 did **not** modify `pyproject.toml` or `uv.lock` (no dependency added; standard-library HTTP only), and added no Docker/Kubernetes/Terraform/Helm, no cloud deployment resource, no real provider invocation, no audio playback, and no RSS publishing. Existing source was modified only where the new command was registered (`src/storytime/cli/app.py`) and where a guard's tracked controlled-mutation file set was extended to include the new local-live proof client (`tests/test_frontend_controlled_retry_submission.py`). The append-only locked-decision documents were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

**Current state after this round (Phase 14A.1 candidate):** Phase 10 CLOSED; Phase 11 CLOSED; Phase 12 CLOSED; **Phase 13 — Portfolio Website / Operator GUI — CLOSED**; Phase 13A–13L all locked; **Phase 13L is the last locked phase**; **Phase 14 — Live System / Cloud-Distributed — is STARTED**; Phase 14A.1 — Local Live Proof Loop Before Cloud — is an implementation candidate, pending review, **not locked**. The reserved future combined bundle is named **Phase 14B.1** and is **NOT STARTED**. Phase 9C remains optional/not scheduled.

---

## Phase 14B.1 — Live Proof Loop Hardening / Operator Trust (2026-05-29, implementation candidate; pending review; NOT locked)

Phase 14B.1 builds on the **LOCKED** Phase 14A.1 local-live proof loop. It is a hardening round, not a capability expansion:

- **Controlled failure/recovery proof:** the proof-run action now accepts an allowlisted `scenario` (`success`, `governance_failure`, `artifact_validation_failure`). The two failure scenarios produce deterministic, durable **failed** runs — a failed `stage_execution` with an error kind/message, a `RunFailed` event carrying the failed stage and reason, an evidence artifact, and a failure reason exposed through the read model. No scenario invokes a real provider, ffmpeg, RSS, cloud, or network.
- **Operator UX:** the Live Proof Loop surface adds controlled scenario buttons, a failure-reason panel, a marked failed stage in the timeline, richer evidence labels, and exactly one bounded post-run refresh (a single delayed refresh; no polling, no interval, no socket).
- **Read-model / DTO hardening:** typed proof-run request/response/error shapes; the health DTO no longer exposes an absolute database path (only a basename) and now lists the approved scenarios; the read model still exposes no raw story text and no absolute paths.
- **Docs:** Windows operator setup/troubleshooting and cloud-ready boundary mapping (hosted API, auth, managed database, object storage, queue/worker, OpenTelemetry, provider adapter) — documented only; nothing cloud is implemented.

**State after this candidate:** Phase 12 CLOSED · Phase 13 CLOSED · Phase 14 STARTED · **Phase 14A.1 LOCKED** (last locked phase) · **Phase 14B.1 implementation candidate / pending review / NOT locked** · **Phase 14C.1+ NOT STARTED**. Phase 14B.1 adds no new dependency and implements no cloud/distributed mode, provider-backed TTS, frontend audio/TTS, audio playback, RSS publishing, authentication, or cloud deployment; all of that remains deferred to the not-yet-started Phase 14C.1+.

---

## Phase 14C.1 — Local Durable Queue / Worker Shape Proof (2026-05-29, implementation candidate; pending review; NOT locked)

Phase 14C.1 builds on the **LOCKED** Phase 14B.1 proof loop. It proves the local durable execution spine without any cloud/distributed implementation:

- **Queue port + SQLite adapter:** a `WorkQueue` `Protocol` (port) with a `SqliteWorkQueue` adapter backed by a new durable `work_queue` table (schema migration 6, additive/idempotent). The queue is shaped as a replaceable port — queue-shaped, not SQLite-shaped — so a future hosted adapter could implement the same contract.
- **Request enqueues, does not execute inline:** `POST /api/proof-runs` now reserves a durable run (status `queued`) and enqueues a work item, returning HTTP 202 accepted. Execution no longer happens on the request path.
- **Local worker:** a single bounded `LocalWorker` claims a queued item, transitions it through `claimed → running → completed | failed`, executes the existing backend-owned proof logic, and reconciles the work item to the run's durable terminal state. The running `storytime local-live` server attaches one background worker thread; tests drive the worker synchronously.
- **Atomic claim, lease recovery, no double execution:** claiming uses `BEGIN IMMEDIATE` + a conditional update so only one worker wins an item; an expired lease is recovered (requeued or failed) by stale-claim recovery; `execute_proof_run` is idempotent per run, so a recovered or redelivered item never double-executes.
- **Safe read model:** the lifecycle (`queued/running/completed/failed`, scenario, attempts, work id) is exposed; claim/lease internals (owner, lease expiry) are never exposed. Health reports `execution: queued-then-local-worker` and queue counts.
- **Scenarios preserved:** `success`, `governance_failure`, and `artifact_validation_failure` all run through the queue/worker path with unchanged durable end states.

**State after this candidate:** Phase 12 CLOSED · Phase 13 CLOSED · Phase 14 STARTED · Phase 14A.1 LOCKED · **Phase 14B.1 LOCKED** (last locked phase) · **Phase 14C.1 implementation candidate / pending review / NOT locked** · **Phase 14C.2 / 14D / 14E NOT STARTED**. Phase 14C.1 is a LOCAL durable queue/worker shape proof: it is not a cloud queue, not a distributed system, uses no external broker, and adds no provider TTS, audio playback, RSS publishing, authentication, or cloud deployment — all reserved for later phases.

---

## Phase 14C.2 — Contracts-as-Built / Cloud-Distributed Seam Baseline (2026-05-29, implementation candidate; pending review; NOT locked)

Phase 14C.1 — Local Durable Queue / Worker Shape Proof — is now **LOCKED** (using `storytime-phase14c1-stale-partial-recovery-cleanup.tar.gz`, SHA-256 `47e676c356ecd63a7bcebc2e7da2240c03bdf4f0efb41930d4831eda0d13a6e5`). Phase 14C.2 is a **documentation / contracts / guardrail** round on top of that locked spine. It changes no runtime behavior.

- **Contracts-as-built doc.** Adds `docs/phase14-contracts-as-built.md` describing the seams Phase 14C.1 actually built, with concrete abstract Python `Protocol`/ABC snippets, under fixed headers A–J: Request Acceptance, Queue Port, SQLite Adapter, Worker Execution, Stale Claim Recovery, Stale Partial Execution Recovery, Read-Model/DTO Safety, Frontend Boundary, Cloud/Distributed Seam Baseline, and Future Phase Dependency Map.
- **Seam baseline (documented, not implemented).** Names the future seams a hosted/distributed system could replace — queue adapter, worker execution, artifact storage, auth-capable API, observability, hosted durable state — and states explicitly that none of them exist yet.
- **Guardrail tests.** Adds `tests/test_contracts_as_built_doc.py` (document presence, required headers, required state phrases, key contract terms, forbidden overclaim phrases) and advances the state-discipline guard to record Phase 14C.1 LOCKED and Phase 14C.2 candidate.
- **No drift.** No queue/worker runtime change; protected dependency surfaces byte-identical to the locked 14C.1 source; schema unchanged (version 6).

**State after this candidate:** Phase 12 CLOSED · Phase 13 CLOSED · Phase 14 STARTED · Phase 14A.1 LOCKED · Phase 14B.1 LOCKED · **Phase 14C.1 LOCKED** (last locked phase) · **Phase 14C.2 implementation candidate / pending review / NOT locked** · **Phase 14C.3 / 14D / 14E NOT STARTED**. Phase 14C.2 implements no cloud, distributed, object-storage, external-broker, auth, retry-lineage, provider-TTS, audio, or RSS capability; it documents contracts as built and defines the future seam baseline.

---

## Phase 14C.3 — Object Storage Boundary / Artifact Store Adapter (2026-05-29, implementation candidate; pending review; NOT locked)

Phase 14C.2 — Contracts-as-Built / Cloud-Distributed Seam Baseline — is now **LOCKED** (using `storytime-phase14c2-contracts-as-built-cloud-distributed-seam-baseline.tar.gz`, SHA-256 `930a339fff100eddd37f5c8b98739bcced4107a01e1959307750a2f0a48b64ff`). Phase 14C.3 puts artifact handling behind a backend-owned storage seam:

- **ArtifactStore port.** A backend-owned `typing.Protocol` (`src/storytime/local_live/artifact_store.py`) using only neutral terms (`artifact_id`, `artifact_key`, `content`, `content_hash`, `media_type`, `size_bytes`, `metadata`, `created_at`) — no bucket/region/ACL/signed-URL/credential concepts. Operations: write, read, exists, evidence, validate_key.
- **LocalFilesystemArtifactStore — the only adapter.** Owns an artifact root; normalizes/validates logical keys; rejects absolute paths, `..` traversal, backslash separators, and symlink escapes; keeps artifacts under the root; writes atomically (temp + `os.replace`); computes content hash / size / media type; returns safe evidence only; deterministic missing behavior (`ArtifactNotFoundError` / `exists`=False / `evidence`=None).
- **Routing.** The proof-run evidence write now flows through the store (logical key `{runId}/proof/evidence.json`) instead of a direct filesystem write. Queue/worker execution semantics are unchanged; `success` / `governance_failure` / `artifact_validation_failure` scenarios are intact.
- **Read-model safety.** Browser-visible artifact evidence remains a relative logical key plus content hash / size; no absolute path, storage root, bucket, signed URL, or credential is exposed.
- **Guardrails.** Adds `tests/test_artifact_store.py` (port/adapter, write/read, metadata, traversal/absolute/backslash/symlink rejection, deterministic missing, proof-run routing, scenario integrity, DTO path-leak safety) and advances the state-discipline guard (Phase 14C.2 LOCKED; Phase 14C.3 candidate; overclaim bars for S3/MinIO/cloud-storage/signed-URLs/public-serving).

**State after this candidate:** Phase 12 CLOSED · Phase 13 CLOSED · Phase 14 STARTED · Phase 14A.1 LOCKED · Phase 14B.1 LOCKED · Phase 14C.1 LOCKED · **Phase 14C.2 LOCKED** (last locked phase) · **Phase 14C.3 implementation candidate / pending review / NOT locked** · **Phase 14C.4 / 14D / 14E NOT STARTED**. Phase 14C.3 is local filesystem artifact storage behind a backend-owned seam: no cloud adapter, no S3/MinIO adapter, no external object store, no signed URLs, no public artifact serving, no auth, no retry/recovery lineage, no observability deepening, and no new dependency.


---

## Phase 14C.3.1 — Contracts Doc State Wording Cleanup (2026-05-29, cleanup sub-round within the Phase 14C.3 lock lineage; NOT a new roadmap phase)

A surgical, documentation-only cleanup of the Phase 14C.3 candidate before Gemini review and lock. It fixes stale wording in `docs/phase14-contracts-as-built.md`: Section J no longer claims Phase 14C.3 is NOT STARTED (now: Phase 14C.3 is the current candidate; **Phase 14C.4 and every later phase are NOT STARTED**), and the Section I object-storage bullet now distinguishes the implemented LOCAL artifact-store adapter (Section K) from the still-absent cloud object-storage / external object store / public artifact-serving / signed-URL / S3 / MinIO adapters. Section K and the 14C.3 implementation are preserved.

No runtime source, dependency, or frontend changes; the entire `src/` tree is byte-identical to the 14C.3 source. The superseding cleanup artifact (`storytime-phase14c3-1-contracts-doc-state-wording-cleanup.tar.gz`) becomes the final candidate for the Phase 14C.3 lock decision.

**State (unchanged by this cleanup):** Phase 12 CLOSED · Phase 13 CLOSED · Phase 14 STARTED · Phase 14A.1 / 14B.1 / 14C.1 / 14C.2 LOCKED · **Phase 14C.3 implementation candidate / pending review / NOT locked** · **Phase 14C.4 / 14D / 14E NOT STARTED**. Phase 14C.3.1 is a cleanup sub-round inside the 14C.3 lineage, not a new phase.
---

## Phase 14C.4 — Minimal Observability Boundary for Queue/Worker (2026-05-30, implementation candidate; pending review; NOT locked)

Phase 14C.3 — Object Storage Boundary / Artifact Store Adapter — is now **LOCKED** (using `storytime-phase14c3-1-contracts-doc-state-wording-cleanup.tar.gz`, SHA-256 `121f27cb5cd9decf9909afd48be1f1af257b3408c2e3d9d0a669342320af8b80`; Gemini: SAFE TO LOCK). Phase 14C.4 adds a minimal, backend-owned observability boundary for the local queue/worker lifecycle. It changes no runtime execution semantics.

- **Boundary (stdlib-only).** `src/storytime/local_live/observability.py`: a `QueueWorkerEvent` immutable record (safe fields only), a `QueueWorkerEventSink` `Protocol`, a default `NullQueueWorkerObserver` (no-op), an `InMemoryQueueWorkerObserver` (ephemeral recorder for tests/inspection), and a fail-soft `emit(...)` helper.
- **Event vocabulary (vendor-neutral, schema-stable).** `work.enqueued`, `work.claimed`, `work.started`, `stage.started`, `stage.completed`, `artifact.recorded`, `work.completed`, `work.failed`. No retry/recovery, cloud, or distributed event names; no exactly-once/cross-node claims.
- **Safe fields only.** Existing local identifiers/timestamps/status: `run_id`, `work_item_id`, `stage_name`, `artifact_key` (logical), `status`, `failure_reason`, `worker_id`, `attempt_number`, `created_at`. No paths, roots, credentials, secrets, tokens, signed URLs, or raw text.
- **Emission points (synchronous, inline, fail-soft).** Enqueue (server) → claim/started/completed/failed (worker) → stage.started/completed + artifact.recorded (execute_proof_run). Emission never changes queue claim, worker execution, ArtifactStore, or scenario semantics; a sink error is swallowed with a bounded stderr diagnostic.
- **Durable vs ephemeral.** Deliberately **ephemeral/in-process** — no new database table, broker, stream, or schema change (decision tree in `docs/phase14-contracts-as-built.md` Section L). Default sink is no-op; observation is opt-in by injecting a recorder.
- **Read-model/API exposure.** None added — exposure was not necessary to make the boundary real, so per the minimal mandate it is omitted (no frontend dashboard, polling, WebSockets, or EventSource).
- **Guardrails.** Adds `tests/test_queue_worker_observability.py` (boundary/protocol, safe event shape, deterministic success order, failure-scenario preservation, logical artifact key, leak-prevention, semantics-unchanged, fail-soft) and advances the state-discipline guard (Phase 14C.3 LOCKED; Phase 14C.4 candidate; OpenTelemetry/collector/Prometheus/Grafana/dashboards/exporters/SLOs/alerting/sampling/distributed-tracing/cloud-telemetry overclaim bars).

**State after this candidate:** Phase 12 CLOSED · Phase 13 CLOSED · Phase 14 STARTED · Phase 14A.1 LOCKED · Phase 14B.1 LOCKED · Phase 14C.1 LOCKED · Phase 14C.2 LOCKED · **Phase 14C.3 LOCKED** (last locked phase) · **Phase 14C.4 implementation candidate / pending review / NOT locked** · **Phase 14C.5 / 14D / 14E NOT STARTED**. Phase 14C.4 is a minimal local observability boundary: no OpenTelemetry SDK, collector, Prometheus endpoint, dashboards, vendor exporters, alerting, SLOs, sampling, distributed tracing, cloud telemetry, retry/recovery lineage, or new dependency.

## 2026-05-30 — Phase 14C.4 LOCKED; Phase 14C.5.1 (Durable Recovery Control Plane Boundary) implementation candidate

- **Phase 14C.4 — Minimal Observability Boundary for Queue/Worker — is formally LOCKED.** Locked artifact: `storytime-phase14c4-minimal-observability-boundary-queue-worker.tar.gz`, SHA-256 `12b951e0a9b6b17f5c73aacf0d055b257bd4a715908f7f5078d401eae2a66d3b`. Scope: a minimal backend-owned, in-process queue/worker observability boundary (safe vendor-neutral event names + safe fields, emitted fail-soft). **Phase 14C.4 observer events are explanatory only and are NOT the durable retry/recovery lineage source of truth.** Phase 14C.4 is now the last locked phase.
- **Phase 14C.5.1 — Durable Recovery Control Plane Boundary — is the current implementation candidate (pending review; NOT locked).** It adds a durable, backend-owned `recovery_action` lineage table (SCHEMA_VERSION 6 → 7) that links an original failed execution identity to a bounded recovery execution identity (source of truth), a backend-owned recovery eligibility policy, duplicate-prevention and a bounded attempt limit, a recovery read-model projection, local SQLite concurrency guardrails, and a cloud-queue mapping CONTRACT document (`docs/phase14-cloud-queue-mapping.md`).
- **Phase 14C.5.1 absorbs the previously planned local recovery-control-plane scope from Phase 14C.5 through Phase 14C.10**; those numbers are historical planning labels only and are not separate active phases.
- Phase 14C.5.1 does **not** expand the Phase 14C.4 observability event schema; does **not** implement cloud/distributed retries, external queues, dead-letter queues, backoff, scheduling, distributed workers, cloud leases, distributed locks, cloud object storage, provider TTS, audio playback, RSS publishing, or auth; and adds **no** new dependency (`pyproject.toml`, `uv.lock`, `package.json`, `package-lock.json` unchanged).
- The Phase 14C.3 artifact-store boundary and the Phase 14C.4 observer boundary remain intact. **Phase 14 remains STARTED. Phase 14D and Phase 14E remain NOT STARTED.**

## 2026-05-30 — Phase 14C.5.1 LOCKED; Phase 14D (Cloud / Distributed Architecture Baseline from Proven Local Contracts) implementation candidate

- **Phase 14C.5.1 — Durable Recovery Control Plane Boundary — is formally LOCKED.** Locked artifact: `storytime-phase14c5-1-durable-recovery-control-plane-boundary.tar.gz`, SHA-256 `73a9ee1bdcbca295037f4852375d3f6b1ff155c3a0ea9d1b0fe498de3862e604` (GPT preliminary: PASS; Gemini: SAFE TO LOCK with no required edits; user directive: Phase 14C.5.1 / Phase 14C officially locked). Scope: a durable, backend-owned `recovery_action` lineage table (source of truth) linking an original failed execution to a bounded recovery execution, a backend-owned recovery eligibility policy, duplicate-prevention and a bounded attempt limit, a recovery read-model, local SQLite concurrency guardrails, and a cloud-queue mapping CONTRACT document. The Phase 14C sequence is locked / complete through 14C.5.1. **Phase 14C.5.1 is now the last locked phase.**
- **Phase 14D — Cloud / Distributed Architecture Baseline from Proven Local Contracts — is the current implementation candidate (pending review; NOT locked).** It is an as-built architecture *mapping* round: it maps the locked local contracts (request acceptance, the `WorkQueue` port, the `LocalWorker`, the `ArtifactStore` port, the durable `recovery_action` control plane, in-process observation, and the operator read-model) to their future cloud/distributed equivalents on paper, recommends a narrow future Phase 15A–15E sequence, and tracks deferred work. New docs: `docs/phase14d-cloud-distributed-architecture-baseline.md` (the deliverable) and `docs/phase14d-deferred-cloud-work-register.md` (deferred register); new guard `tests/test_cloud_distributed_baseline_doc.py`.
- **Phase 14D implements no cloud/distributed behavior.** No external broker, distributed worker, cloud object storage, signed URLs, auth, public ingress, cloud recovery orchestration, automatic retries, backoff, dead-letter queue, OpenTelemetry export expansion, dashboards, provider TTS, audio playback, RSS publishing, polling/WebSockets/EventSource, or observer-schema expansion. It adds **no** new dependency (`pyproject.toml`, `uv.lock`, `package.json`, `package-lock.json` unchanged).
- **Stale 14D roadmap language corrected.** The previously sketched provider-TTS / frontend-audio / RSS / local-content-production arc (formerly mislabelled "Phase 14D.1–14D.4") is **deferred future work**, not the active Phase 14D scope.
- **Phase 14 remains STARTED and is not closed. Phase 14E and Phase 15 remain NOT STARTED.**


## 2026-05-30 — Phase 14D LOCKED (Cloud / Distributed Architecture Baseline from Proven Local Contracts)

- **Phase 14D — Cloud / Distributed Architecture Baseline from Proven Local Contracts — is formally LOCKED.** Locked artifact: `storytime-phase14d-cloud-distributed-architecture-baseline.tar.gz`, SHA-256 `a4ccc8aa59beaf6365081973d1c3d78235df028ef0f3214979e9d3b98f4dcce6`. **Phase 14D is now the last locked phase.** The Phase 14C sequence remains locked / complete through 14C.5.1.
- **Lock basis:** GPT preliminary review PASS (ready for Gemini review); Gemini implementation review SAFE TO LOCK with no required edits; Gemini accepted the native-Windows validation caveat as non-blocking; the Phase 14D-specific guards passed; and the lock changed no `src/`, `frontend/`, dependency manifest, runtime, cloud, broker, object-storage, auth, provider-TTS, RSS, polling/WebSocket/EventSource, or observer-schema surface. User directive: Phase 14D officially locked.
- **Validation recorded honestly.** Native-Windows gates: `uv sync --frozen` / `ruff` / `mypy` (108 files) / `lint-imports` (2 kept, 0 broken) / `storytime doctor` (healthy) all PASS; `uv run pytest` reported 1093 passed, 14 failed, 28 skipped. The 14 failures are Windows/POSIX environment-sensitive failures in files byte-identical to the locked 14C.5.1 baseline (no Phase 14D source change), and the Phase 14D-owned guards all passed. Full `pytest` is NOT recorded as a clean pass; a clean Linux/WSL `uv run pytest` remains recommended (see `docs/verification-log.md`).
- **Phase 14D implemented no cloud/distributed behavior** and added **no** new dependency (`pyproject.toml`, `uv.lock`, `package.json`, `package-lock.json` unchanged). The locked deliverable artifact internally labels Phase 14D a "candidate / pending review / NOT locked"; that is the project's standard internal framing for a locked artifact (every locked artifact self-labels as a candidate), and the lock is recorded here in the ledger, not inside the artifact.
- **Phase 12 CLOSED. Phase 13 CLOSED. Phase 14 STARTED (not closed). Phase 14A.1, 14B.1, 14C.1, 14C.2, 14C.3, 14C.4, 14C.5.1, and 14D LOCKED. Phase 14E NOT STARTED. Phase 15 NOT STARTED.**
