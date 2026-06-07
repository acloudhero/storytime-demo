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
**Round type:** Phase 13F — Local Bridge Architecture & Contract Baseline — a documentation-and-static-fixture architecture-baseline sub-round over the locked Phase 13E operator GUI. Like Phase 13A, it is architecture / contract only — no runtime code.
**Status:** Phase 13F is an **implementation candidate / pending review — NOT locked.**
**Last locked phase:** Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary.
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13F.
**Next action:** Submit the Phase 13F artifact for GPT-5.5 review, then Gemini critique, then an explicit user decision — before locking Phase 13F or starting Phase 13G.

**Phase 13E lock (recorded honestly).** Phase 13E — Demo-Mode Action
Preview / Operator Intent Boundary — completed its Phase Closure
Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini
returned SAFE TO LOCK with no required edits, and the user, as final
decision-maker, locked Phase 13E. **Phase 13E is LOCKED; it is the
last locked phase.** Locked artifact
`storytime-phase13e-demo-mode-action-preview-operator-intent-boundary.tar.gz`,
SHA-256 `a997f2ca9d213e28e140f47c63336367c8feda46ed994b41300f86b99f8d8164`.
Phase 13 — Portfolio Website / Operator GUI — remains STARTED and is
not closed.

Phase 13F is a documentation-and-static-fixture architecture /
contract baseline — the architectural lock before any Python
local-bridge implementation is allowed (it is to the Local Bridge
what Phase 13A was to the operator GUI). It adds eleven new
architecture / contract docs (`docs/local-bridge-architecture.md`,
`docs/externalized-state-architecture.md`,
`docs/browser-storage-policy.md`,
`docs/local-mode-workspace-layout.md`,
`docs/storage-targets-architecture.md`,
`docs/action-execution-boundary.md`,
`docs/local-action-dto-spec.md`,
`docs/local-action-audit-spec.md`,
`docs/local-mode-storage-contract.md`,
`docs/local-action-queue-observability.md`, and
`docs/phase13f-local-bridge-contract-readiness.md`); a small set of
non-runtime JSON example fixtures under `docs/examples/`
(local-action-requests, local-action-responses,
local-action-audit-records); and one new Python test
(`tests/test_local_mode_contract_examples.py`) that validates those
fixtures are well-formed and contain the required fields using plain
Python (no JSON-schema dependency).

The central architecture principle Phase 13F establishes: **the
frontend is an operator surface, not the durable storage layer.**
Durable state must live outside the browser, in an explicit external
workspace / storage target with clear export, reset, backup, and
recovery semantics — so StoryTime never repeats the RoundTable
browser-storage failure mode where project state accretes in the
browser until it is unrecoverable. The browser may hold temporary UI
state only; `localStorage` / `sessionStorage` / `IndexedDB` remain
forbidden. The docs also settle the Hybrid Option C decisions Gemini
required: an execution-timing policy (long-running actions are
asynchronous, the future bridge returns `202 Accepted` with an
`actionRequestId` / `jobId`, acceptance is not success, export
refresh happens after a durable write, refresh races are avoided
with atomic writes + identity-tagged read models); a loopback-only /
strict-origin / no-arbitrary-command / command-pattern-router
security boundary; a future action allowlist (`retry_failed_stage`,
`inspect_trust_envelope`, `refresh_export`) with higher-risk actions
(`record_review_decision`, `regenerate_operator_report`,
`publish_episode`, `delete_artifact`, provider sync) explicitly
deferred; and a queue-observability model (depth, in-flight,
completed / failed / rejected / dead-letter counts, oldest-queued and
longest-in-flight ages, retry count, capacity, saturation, export
freshness) plus a conservative local load-limit policy and a
distributed/cloud carry-forward.

Phase 13F implements **NO** runtime code: no local bridge, no server,
no socket, no subprocess, no async queue, no queue workers, no queue
metrics / exporters, no OpenTelemetry instrumentation, no storage
providers, no provider integrations, no runtime schema validation, no
router / history, no browser storage, no real Local mode, no
Cloud/Distributed mode, and no mutation / action execution. The
browser remains non-durable. The example fixtures are documentation
artifacts only — never imported by runtime code, never generated by a
running system, and they never claim Phase 13F executed anything.
Phase 13F does **not** modify `src/`, `frontend/src/`,
`frontend/package.json`, `frontend/package-lock.json`,
`pyproject.toml`, `uv.lock`, or
`frontend/src/data/storytime-demo-export.json`; all are byte-identical
to the locked Phase 13E source. The only allowed code changes are the
narrow, explicitly-authorized mechanical advance of the
state-discipline guard `tests/test_failure_mode_regression.py` to the
Phase 13F current-state expectations, and the new
`tests/test_local_mode_contract_examples.py`.

Per the Phase Closure Protocol, Phase 13F is an implementation
candidate, pending review, **not locked**; it does not lock Phase
13F, does not close Phase 13, and does not start Phase 13G. Phase 13G
and every later Phase 13 subphase have **not** started — they are
future, planned work, decomposed in `docs/phase13-roadmap.md` and
recommended in `docs/phase13f-local-bridge-contract-readiness.md`.
Phase 9C remains optional and not scheduled.

*(Every Phase 13E-era and earlier note below is a historical record.
Phase 13E is LOCKED; Phase 13F is the current implementation
candidate. The "# Handoff State" dashboard further down is the
authoritative current-status snapshot.)*

---
# Phase 13E implementation-candidate note — Demo-Mode Action Preview / Operator Intent Boundary (historical record — Phase 13E is LOCKED; see the Phase 13F note above)

**Date:** 2026-05-27
**Round type:** Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary — a static, demo-mode, non-consequential sub-round over the locked Phase 13D.2 operator GUI.
**Status:** Historical record. This note described Phase 13E while it was an implementation candidate. Phase 13E has since been **LOCKED** and is the last locked phase before Phase 13F; Phase 13F is now the current implementation candidate — see the Phase 13F note above and the "# Handoff State" dashboard further down.
**Last locked phase:** Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path.
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13E.
**Next action:** Submit the Phase 13E artifact for GPT-5.5 review, then Gemini critique, then an explicit user decision — before locking Phase 13E or starting Phase 13F.

**Phase 13D.2 lock (recorded honestly).** Phase 13D.2 — Static Demo
Walkthrough / Reviewer Story Path — completed its Phase Closure
Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini
returned SAFE TO LOCK with no required edits, and the user, as final
decision-maker, locked Phase 13D.2. **Phase 13D.2 is LOCKED; it is the
last locked phase.** Phase 13 — Portfolio Website / Operator GUI —
remains STARTED and is not closed.

Phase 13E is the first sub-round that explicitly models operator
intent rather than only displaying read-only state — but it is
deliberately a **Demo-mode** sub-round and remains non-consequential:
demo-mode action previews may model what the operator is trying to
accomplish, why it is blocked in Demo mode, what preconditions would
be required, what evidence to inspect, what a future Local-mode
request shape might look like, and what audit expectations would
apply, but Phase 13E **does not execute any operator action**. It
introduces or clarifies the eventual mode model — **Demo mode**
(curated, safe, non-consequential, portfolio-ready; the only mode
implemented), **Local mode** (future, real local operator workflows;
not implemented in Phase 13E), and **Cloud / Distributed mode**
(future, hosted/distributed execution; not implemented in Phase 13E)
— and clarifies that Demo / Active / Candidate are **data-snapshot**
labels while Demo / Local / Cloud-Distributed are **operating-mode**
labels.

Concretely Phase 13E adds a static, demo-mode Action Preview system
— `frontend/src/data/actionPreviewAdapter.ts` plus
`frontend/src/components/ActionPreviewPanel.tsx` and its CSS Module —
implementing a small initial set of action previews (retry-failed-stage,
inspect-trust-envelope, record-review-decision, regenerate-operator-report,
refresh-export). Each preview is data-driven: stable action id, action
label and category, current mode (Demo), execution status (Preview
only / non-consequential), target object (run id / stage id /
governance decision id / failure queue item / evidence artifact as
applicable), what the operator is trying to accomplish, why it is
blocked in Demo mode, a precondition checklist, the evidence to
inspect first, a risk level and explanation, an illustrative future
Local-mode request shape (a structured pseudo-DTO labelled "Future
request shape — illustrative only, not executable in Demo mode"),
Cloud/Distributed considerations, audit expectations, failure
behaviour expectation, what remains disabled, and the related view
to inspect. The panel is integrated into Failure / Recovery,
Governance / Safety, and Evidence / Validation **alongside** the
existing `DisabledFutureActionCard` — the disabled future-action
buttons remain disabled (real `<button disabled={true}>` with no
`onClick`). A separate, clearly-labelled "Preview action plan"
control opens an inline preview panel; the preview never looks like
execution, there is no fake loading spinner, no simulated success
state, no `setTimeout` workflow, and no "Submitted" / "Succeeded" /
"Audit created" rendering anywhere.

Phase 13E is static and Demo-mode-only. It adds no server, no live
API, no `fetch`/`axios`/`localhost`/network call, no
`localStorage`/`sessionStorage`, no router / hash routing / browser
History API, no Context provider, no global preview/action state, no
mutation handler, no authentication, no cloud deployment, no
production hosting, no dynamic file loading, no Demo / Active /
Candidate snapshot switching, no actual retry / rerun / approval /
report regeneration / export refresh, no audit-record generation
(nothing executed), and no fake-execution surface. It does **not**
modify the backend export generator (`src/storytime/operator_export.py`),
the committed static export JSON
(`frontend/src/data/storytime-demo-export.json`), the `storytime
export-demo-ui` CLI contract, or `src/storytime/cli/app.py`; all four
protected files / contracts are byte-identical to the Phase 13D.2
source. No `src/`, `pyproject.toml`, `uv.lock`,
`frontend/package.json`, `frontend/package-lock.json`, or root
dependency changed. The `tests/` changes are the narrow, explicitly
authorized mechanical advance of the state-discipline guard to the
Phase 13E current-state expectations, and one new data-integrity
test that asserts every run id referenced by the action-preview
adapter exists in the committed static export.

Per the Phase Closure Protocol, Phase 13E is an implementation
candidate, pending review, **not locked**; it does not lock Phase
13E, does not close Phase 13, and does not start Phase 13F. Phase
13F and every later Phase 13 subphase have **not** started — they
are future, planned work, decomposed in `docs/phase13-roadmap.md`.
Phase 9C remains optional and not scheduled.

*(Every Phase 13D.2-era and earlier note below is a historical
record. Phase 13D.2 is LOCKED; Phase 13E is the current
implementation candidate. The "# Handoff State" dashboard further
down is the authoritative current-status snapshot.)*

---
# Phase 13D.2 implementation-candidate note — Static Demo Walkthrough / Reviewer Story Path (historical record — Phase 13D.2 is LOCKED; see the Phase 13E note above)

**Date:** 2026-05-27
**Round type:** Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path — a frontend-only, static / read-only demo-readiness sub-round over the locked Phase 13D.1 operator GUI.
**Status:** Historical record. This note described Phase 13D.2 while it was an implementation candidate. Phase 13D.2 has since been **LOCKED** and is the last locked phase before Phase 13E; Phase 13E is now the current implementation candidate — see the Phase 13E note above and the "# Handoff State" dashboard further down.
**Last locked phase:** Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline.
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13D.2.
**Next action:** Submit the Phase 13D.2 artifact for GPT-5.5 review, then Gemini critique, then an explicit user decision — before locking Phase 13D.2 or starting Phase 13E.

**Phase 13D.1 lock (recorded honestly).** Phase 13D.1 — Static Operator
GUI Refinement / Evidence & Disabled Action Discipline — completed its
Phase Closure Protocol: implementation, GPT-5.5 review, and Gemini
critique. Gemini returned SAFE TO LOCK with no required edits, and the
user, as final decision-maker, locked Phase 13D.1. **Phase 13D.1 is
LOCKED; it is the last locked phase.** Phase 13 — Portfolio Website /
Operator GUI — remains STARTED and is not closed.

Phase 13D.2 is the static / read-only demo-readiness sub-round of Phase
13D.1. It turns the existing operator GUI views into a coherent guided
reviewer / demo path so a hiring manager, Solutions Engineer leader,
technical reviewer, or self-guided portfolio visitor can answer "what
should I click first?", "what does this prove?", "what do I say about
this in an interview?", "where is the architecture boundary?", "how is
this local-first and safe?", "why is the frontend read-only?", and
"what is next, and why is it not live yet?". Concretely it replaces
the honest Demo Walkthrough placeholder with a real read-only view
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
identify it by stable id (`run-2026-0518-golden` for the golden-path
run; `run-2026-0520-review` for the review-required run). The view
also includes architecture-checkpoint cards covering local-first
design, deterministic static export, backend-owns-truth /
frontend-owns-understanding, read-only operator surface, static
evidence boundary, disabled-action boundary, Demo / Active /
Candidate as **data snapshots, not deployment environments**, and
why Phase 13E must be explicitly gated before any action becomes
real. The view also includes a deliberate "what is intentionally
deferred" section and interview / SE talking-point callout cards.
Phase 13D.2 absorbs ~80–90% of an Architecture Story narrative via
these embedded checkpoints but does NOT implement a full standalone
Architecture Story page — that stays deferred and is recorded as a
new item in `docs/frontend-gui-deferred-work-register.md`.

Phase 13D.2 is static, read-only, and export-backed. It adds no
server, no live API, no `fetch`/`axios`/`localhost`/network call, no
watcher, no mutation, no authentication, no cloud deployment, no
production hosting, no dynamic file loading, and no Demo / Active /
Candidate switching; the visibly-disabled review and recovery
affordances continue to be visibly disabled and carry no mutation
handlers. It does **not** modify the backend export generator
(`src/storytime/operator_export.py`), the committed static export
JSON (`frontend/src/data/storytime-demo-export.json`), the `storytime
export-demo-ui` CLI contract, or `src/storytime/cli/app.py`; all four
protected files / contracts are byte-identical to the Phase 13D.1
source. No `src/`, `pyproject.toml`, `uv.lock`,
`frontend/package.json`, `frontend/package-lock.json`, or root
dependency changed. The only `tests/` change is the narrow,
explicitly authorized mechanical advance of the state-discipline
guard `tests/test_failure_mode_regression.py` to the Phase 13D.2
current-state expectations.

Per the Phase Closure Protocol, Phase 13D.2 is an implementation
candidate, pending review, **not locked**; it does not lock Phase
13D.2, does not close Phase 13, and does not start Phase 13E. Phase
13E and every later Phase 13 subphase have **not** started — they
are future, planned work, decomposed in `docs/phase13-roadmap.md`.
Phase 9C remains optional and not scheduled.

*(Every Phase 13D.1-era and earlier note below is a historical
record. Phase 13D.1 is LOCKED; Phase 13D.2 is the current
implementation candidate. The "# Handoff State" dashboard further
down is the authoritative current-status snapshot.)*

---
# Phase 13D.1 implementation-candidate note — Static Operator GUI Refinement / Evidence & Disabled Action Discipline (historical record — Phase 13D.1 is LOCKED; see the Phase 13D.2 note above)

**Date:** 2026-05-27
**Round type:** Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline — a frontend-only, static / read-only refinement sub-round over the locked Phase 13D operator GUI.
**Status:** Historical record. This note described Phase 13D.1 while it was an implementation candidate. Phase 13D.1 has since been **LOCKED** and is the last locked phase; Phase 13D.2 is now the current implementation candidate — see the Phase 13D.2 note above and the "# Handoff State" dashboard further down.
**Last locked phase:** Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery).
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13D.1.
**Next action:** Submit the Phase 13D.1 artifact for GPT-5.5 review, then Gemini critique, then an explicit user decision — before locking Phase 13D.1 or starting Phase 13E.

**Phase 13D lock (recorded honestly).** Phase 13D — Operator Workflow View
Expansion (Governance / Safety, Failure / Recovery) — completed its Phase
Closure Protocol: implementation, GPT-5.5 review, and Gemini critique.
Gemini returned SAFE TO LOCK with no required edits, and the user, as
final decision-maker, locked Phase 13D. **Phase 13D is LOCKED; it is the
last locked phase.** Phase 13 — Portfolio Website / Operator GUI — remains
STARTED and is not closed.

Phase 13D.1 is the static / read-only refinement sub-round of Phase 13D.
It strengthens the operator GUI and portfolio / reviewer flow before
StoryTime crosses into any controlled local action or mutation-boundary
work. Concretely it standardizes the disabled future-action display
across views into a reusable typed component
(`frontend/src/components/DisabledFutureActionCard.tsx` plus its CSS
Module) backed by real `<button disabled={true}>` elements with no
`onClick` handlers and no fake mutation props; replaces the honest
Evidence / Validation placeholder with a real read-only **Evidence /
Validation** view (`frontend/src/components/EvidenceValidationView.tsx`
plus its CSS Module) that carries the mandatory **STATIC PORTFOLIO DATA
— NOT A LIVE CI/CD DASHBOARD** disclaimer, points to repository-relative
evidence (`docs/verification-log.md`,
`docs/frontend-static-export-contract.md`,
`docs/frontend-gui-deferred-work-register.md`, `docs/phase-history.md`,
`docs/artifact-manifest.md`, `tests/test_failure_mode_regression.py`,
`tests/test_operator_export.py`), and does not fabricate runtime CI
status; adds a small read-only **Data Source / Demo Snapshot** framing
(a Demo / Active / Candidate explanatory block inside the new Evidence
view, plus the existing header chip) clarifying that Active and
Candidate are **data snapshots, not deployment environments**, and that
no switching is implemented; extracts navigation / view-key metadata
from `App.tsx` into a small typed `frontend/src/navigation.ts` helper to
keep `App.tsx` readable while preserving plain `useState` navigation and
the `inspectRun(runId)` prop-drilled drill-down (no router); and
synchronizes the State Preservation Bundle including the deferred-work
register.

Phase 13D.1 is static, read-only, and export-backed. It adds no server,
no live API, no `fetch`/`axios`/`localhost`/network call, no watcher, no
mutation, no authentication, no cloud deployment, and no production
hosting; the recovery / review affordances continue to be visibly
disabled with no mutation handlers. It does **not** modify the backend
export generator (`src/storytime/operator_export.py`), the committed
static export JSON (`frontend/src/data/storytime-demo-export.json`), the
`storytime export-demo-ui` CLI contract, or `src/storytime/cli/app.py`;
all four protected files / contracts are byte-identical to the Phase 13D
source. No `src/`, `pyproject.toml`, `uv.lock`, or root dependency
changed. The only `tests/` change is the narrow, explicitly authorized
mechanical advance of the state-discipline guard
`tests/test_failure_mode_regression.py` to the Phase 13D.1 current-state
expectations.

Per the Phase Closure Protocol, Phase 13D.1 is an implementation
candidate, pending review, **not locked**; it does not lock Phase 13D.1,
does not close Phase 13, and does not start Phase 13E. Phase 13E and
every later Phase 13 subphase have **not** started — they are future,
planned work, decomposed in `docs/phase13-roadmap.md`. Phase 9C remains
optional and not scheduled.

*(Every Phase 13D-era and earlier note below is a historical record.
Phase 13D is LOCKED; Phase 13D.1 is the current implementation
candidate. The "# Handoff State" dashboard further down is the
authoritative current-status snapshot.)*

---
# Phase 13D implementation-candidate note — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) (historical record — Phase 13D is LOCKED; see the Phase 13D.1 note above)

**Date:** 2026-05-27
**Round type:** Phase 13D — Operator Workflow View Expansion — a frontend-only round expanding two placeholder operator views against the locked Phase 13C deterministic static export.
**Status:** Historical record. This note described Phase 13D while it was an implementation candidate. Phase 13D has since been **LOCKED** and is the last locked phase; Phase 13D.1 is now the current implementation candidate — see the Phase 13D.1 note above and the "# Handoff State" dashboard further down.
**Last locked phase:** Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment.
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13D.
**Next action:** Submit the Phase 13D artifact for GPT-5.5 review, then Gemini critique, then an explicit user decision — before locking Phase 13D or starting Phase 13E.

**Phase 13C lock (recorded honestly).** Phase 13C — Deterministic Read-Only
Static Export / Frontend Data Alignment — completed its Phase Closure
Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini
returned SAFE TO LOCK with no required edits, and the user, as final
decision-maker, locked Phase 13C. **Phase 13C is LOCKED; it is the last
locked phase.** Phase 13 — Portfolio Website / Operator GUI — remains
STARTED and is not closed.

Phase 13D is the fourth subphase of Phase 13. It expands two of the honest
Phase 13B/13C placeholder views into real read-only operator views —
**Governance / Safety** and **Failure / Recovery** — against the locked
Phase 13C deterministic static export contract. Following Gemini's
suggestion, Phase 13D introduces **CSS Modules for the two new components
only** as the scoped styling strategy; the existing global
`frontend/src/styles.css` continues to back the Phase 13B/13C shell and is
not migrated. The view scope and ordering follow the Phase 13C
deferred-work register's view-expansion recommendation: these two views
reuse data already in the export (per-run `governance` blocks and the
`failureQueue`) and are the strongest architectural proofs of StoryTime's
governance and operational maturity.

Phase 13D adds two new view components and their CSS Modules
(`frontend/src/components/GovernanceSafetyView.tsx` /
`GovernanceSafetyView.module.css` and
`frontend/src/components/FailureRecoveryView.tsx` /
`FailureRecoveryView.module.css`), two domain-specific view-model adapters
(`frontend/src/data/governanceAdapter.ts` and
`frontend/src/data/failureAdapter.ts`) that project the locked export, an
ambient CSS-Modules TypeScript declaration
(`frontend/src/types/css-modules.d.ts`), App-level navigation rewiring with
a read-only "Data source · Demo Snapshot" header chip backed by the
existing `EXPORT_META` adapter export and an inspect-this-run drill-down
callback into the existing Pipeline Run Detail view (plain prop drilling,
no router), and the documentation updates including a deferred-register
entry for the future **Demo / Blue / Green Data Snapshot Switcher**. It
synchronizes the State Preservation Bundle.

Phase 13D is a static, read-only, export-backed frontend round. It does
**not** modify the backend export generator
(`src/storytime/operator_export.py`), the committed static export JSON
(`frontend/src/data/storytime-demo-export.json`), or the `storytime
export-demo-ui` contract; both protected files are byte-identical to the
Phase 13C source. Phase 13D adds no server, no live API, no `fetch`/`axios`,
no watcher, no mutation, no authentication, no cloud deployment, and no
production hosting; the recovery / review affordances are surfaced as
visibly-disabled future actions labelled with the phase that would enable
them (Phase 13E). No `src/`, `pyproject.toml`, `uv.lock`, or root
dependency changed. The only `tests/` change is the narrow, explicitly
authorized mechanical advance of the state-discipline guard
`tests/test_failure_mode_regression.py` to the Phase 13D current-state
expectations.

Per the Phase Closure Protocol, Phase 13D is an implementation candidate,
pending review, **not locked**; it does not lock Phase 13D, does not close
Phase 13, and does not start Phase 13E. Phase 13E and every later Phase 13
subphase have **not** started — they are future, planned work, decomposed
in `docs/phase13-roadmap.md`. Phase 9C remains optional and not scheduled.

*(Every Phase 13C-era and earlier note below is a historical record. Phase
13C is LOCKED; Phase 13D is the current implementation candidate. The "#
Handoff State" dashboard further down is the authoritative current-status
snapshot.)*

---
# Phase 13C implementation-candidate note — Deterministic Read-Only Static Export / Frontend Data Alignment (historical record — Phase 13C is LOCKED; see the Phase 13D note above)

**Date:** 2026-05-27
**Round type:** Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment — a read-only static data-boundary round.
**Status:** Historical record. This note described Phase 13C while it was an implementation candidate. Phase 13C has since been **LOCKED** and is the last locked phase; Phase 13D is now the current implementation candidate — see the Phase 13D note above and the "# Handoff State" dashboard further down.
**Last locked phase:** Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold.
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13C.
**Next action:** Submit the Phase 13C artifact for GPT-5.5 review, then Gemini critique, then an explicit user decision — before locking Phase 13C or starting Phase 13D.

**Phase 13B lock (recorded honestly).** Phase 13B — Typed Static Portfolio
Shell / Minimal Visual Pipeline Scaffold — completed its Phase Closure
Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini returned
SAFE TO LOCK with no required edits, and the user, as final decision-maker,
locked Phase 13B. **Phase 13B is LOCKED; it is the last locked phase.** Phase
13 — Portfolio Website / Operator GUI — remains STARTED and is not closed.

Phase 13C is the third subphase of Phase 13. It establishes a truthful,
reproducible, read-only data boundary between backend truth and the Phase 13B
frontend. It adds a small, read-only backend export module
(`src/storytime/operator_export.py`) and a `storytime export-demo-ui` CLI
command that produce a deterministic static JSON export
(`frontend/src/data/storytime-demo-export.json`, carrying a top-level
`schemaVersion`); the export contract document
`docs/frontend-static-export-contract.md`; the frontend deferred-work register
`docs/frontend-gui-deferred-work-register.md`; a frontend adapter
(`frontend/src/data/adapter.ts`) and a `StaticDemoExport` type; backend
contract tests (`tests/test_operator_export.py`); and it rewires the Phase 13B
homepage and Pipeline Run Detail / Stage Timeline to consume the export through
the adapter. It synchronizes the State Preservation Bundle.

Phase 13C is a static, read-only data-boundary round. The export is
deterministic — built from fixed demo data, with no `datetime.now()`, no
`uuid`, and no randomness; generating it twice yields byte-identical JSON.
Phase 13C does not make the frontend live: it adds no server, no live API, no
`fetch`/`axios`, no watcher, no mutation, no authentication, no cloud
deployment, and no production hosting. The small backend code it adds is
read-only and deterministic and changes no core pipeline runtime behaviour, no
governance, no telemetry, no CLI behaviour beyond the new read-only command,
and no root dependency. Its `tests/` changes are the new
`tests/test_operator_export.py` and the narrow, explicitly authorized
mechanical advance of the state-discipline guard
`tests/test_failure_mode_regression.py`.

Per the Phase Closure Protocol, Phase 13C is an implementation candidate,
pending review, **not locked**; it does not lock Phase 13C, does not close
Phase 13, and does not start Phase 13D. Phase 13D and every later Phase 13
subphase have **not** started — they are future, planned work, decomposed in
`docs/phase13-roadmap.md`. Phase 9C remains optional and not scheduled.

*(Every Phase 13B-era and earlier note below is a historical record. Phase 13B
is LOCKED; Phase 13C is the current implementation candidate. The "# Handoff
State" dashboard further down is the authoritative current-status snapshot.)*

---
# Phase 13B implementation-candidate note — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold (historical record — Phase 13B is LOCKED; see the Phase 13C note above)

**Date:** 2026-05-27
**Round type:** Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — first frontend implementation round of Phase 13.
**Status:** Historical record. This note described Phase 13B while it was an implementation candidate. Phase 13B has since been **LOCKED** and is the last locked phase; Phase 13C is now the current implementation candidate — see the Phase 13C note above and the "# Handoff State" dashboard below.
**Last locked phase:** Phase 13A — Portfolio Website / Operator GUI Architecture Baseline.
**Current phase:** Phase 13 — Portfolio Website / Operator GUI — STARTED. **Current subphase** — Phase 13B.
**Next action:** Submit the Phase 13B artifact for GPT-5.5 review, then Gemini critique, then an explicit user decision — before locking Phase 13B or starting Phase 13C.

**Phase 13A lock (recorded honestly).** Phase 13A — Portfolio Website /
Operator GUI Architecture Baseline — completed its Phase Closure Protocol:
implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO
LOCK with no required edits, and the user, as final decision-maker, locked
Phase 13A. **Phase 13A is LOCKED; it is the last locked phase.** Phase 13 —
Portfolio Website / Operator GUI — remains STARTED and is not closed.

Phase 13B is the second subphase of Phase 13 and the first round that writes
frontend code. Against the locked Phase 13A contract it implements a
deliberately bounded frontend: a typed static portfolio shell plus one visual
operator view. It adds a new top-level `frontend/` directory — a React +
TypeScript (strict) + Vite project, standard CSS, no external UI / component /
state / charting library — containing the frontend read-model contract
(`frontend/src/types/storytime.ts`), a static demo dataset of exactly two mock
pipeline runs (`frontend/src/data/storytime-demo-data.ts`), the portfolio
homepage, one Pipeline Run Detail view with a visual Stage Timeline, honest
placeholders for the future portfolio sections and operator views, and a
frontend README. It lightly updates `README.md` and synchronizes the State
Preservation Bundle.

Phase 13B is a static, read-only, demo-data-backed shell. It is **not**
backend-connected, does **not** use live or runtime data, does **not**
implement mutations (retry, re-run, and review-decision actions appear only as
visibly-disabled affordances), and is **not** production-hosted or
cloud-deployed. It contacts no backend — there is no `fetch()`, no `axios`, and
no network call. It changed no pipeline behaviour, `storytime rerun`, Trust
Envelope enforcement, API, CLI, telemetry, Docker behaviour, `pyproject.toml`,
`uv.lock`, or `src/` content; the backend is untouched. Its only `tests/`
change is the narrow, explicitly authorized mechanical advance of the
state-discipline guard `tests/test_failure_mode_regression.py` to the
Phase 13B current-state expectations.

Per the Phase Closure Protocol, Phase 13B is an implementation candidate,
pending review, **not locked**; it does not lock Phase 13B, does not close
Phase 13, and does not start Phase 13C. Phase 13C and every later Phase 13
subphase have **not** started — they are future, planned work only, decomposed
in `docs/phase13-roadmap.md`. Phase 9C remains optional and not scheduled.

*(Every Phase 13A-era, Phase 12D-era, and earlier note below is a historical
record. Phase 13A is LOCKED; Phase 13B is the current implementation
candidate. The "# Handoff State" dashboard further down is the authoritative
current-status snapshot.)*

---
# Phase 13A implementation-candidate note — Portfolio Website / Operator GUI Architecture Baseline (historical record — Phase 13A is LOCKED; see the Phase 13B note above)

**Date:** 2026-05-27
**Round type:** Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — documentation-only architecture-baseline round (documentation only).
**Status:** Historical record. This note described Phase 13A while it was an implementation candidate. Phase 13A has since been **LOCKED** and is the last locked phase; Phase 13B is now the current implementation candidate — see the Phase 13B note above and the "# Handoff State" dashboard below.

Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — is now
**LOCKED** and is the last locked phase, and **Phase 12 — Portfolio / SE Demo
Packaging — is CLOSED** (Phase 12A through 12D all locked). Phase 12D completed
its Phase Closure Protocol out-of-band: Gemini returned the verdict to lock
Phase 12D and close Phase 12, with no critical findings, no non-blocking
findings, and no required edits; the user then locked Phase 12D and formally
closed Phase 12. **Phase 13 — Portfolio Website / Operator GUI — is STARTED.**
Phase 12E was optional, contingency-only work; the Phase 12D review found no
substantive gap, so Phase 12E was not needed and never started. Phase 13B and
every later Phase 13 subphase have **not** started — they are future, planned
work only.

Phase 13A is the first subphase of Phase 13 — Portfolio Website / Operator
GUI — the phase that follows the closed Phase 12. Phase 13A is a
documentation-only architecture-baseline round: it designs the portfolio
website and the decoupled operator GUI on paper and refines the earlier
`docs/GUI_vision.md` sketch into an authoritative Phase 13 plan, without
building any of it. It adds five `docs/` documents —
`phase13-portfolio-website-architecture.md` (the Phase 13 purpose, the
end-state website and operator-GUI vision, audiences and review paths, the
website and operator information architectures, the local-first and
future-cloud compatibility rules, and the Phase 13 success criteria),
`frontend-backend-contract.md` (the "backend owns truth, frontend owns
understanding" data contract — read-model categories, future action
categories, the actions disabled in Phase 13A, and candidate data-source
options), `phase13-roadmap.md` (the Phase 13A–13G subphase decomposition),
`portfolio-website-content-model.md` (the website section inventory mapped to
existing repository source documents, with a content-honesty checklist), and
`operator-gui-view-model.md` (the operator-GUI view inventory, disabled and
future actions, empty / error / loading states, and accessibility
requirements) — and synchronizes the State Preservation Bundle.

Phase 13A is a planning round and does **not** implement the portfolio website
and does **not** implement the operator GUI: it adds no React, Vite,
TypeScript, JavaScript, CSS, HTML application code, no `frontend/` / `web/` /
`app/` directory, no `package.json` or `vite.config`, no UI, no server, and no
new dependency, and changed no `src/`, `pyproject.toml`, `uv.lock`,
dependency, or runtime / product / API / CLI / telemetry behaviour. Its only
`tests/` change is the narrow, explicitly authorized mechanical advance of the
state-discipline guard `tests/test_failure_mode_regression.py` to the Phase
13A current-state expectations. Per the Phase Closure Protocol, Phase 13A is an
implementation candidate, pending review, **not locked**.

*(The Handoff State dashboard further down is the authoritative current-status
snapshot and has been updated to the Phase 13A state. The Phase 12D-era and
Phase 12C-era notes below — and the Phase 12B-era, Phase 12A.1, Phase 12A, and
Phase 11x notes further below — are historical records.)*

---
# Phase 12D implementation-candidate note — Phase 12 Closure Plan / Final Portfolio Handoff Definition (historical record — Phase 12D is LOCKED and Phase 12 is CLOSED; see the Phase 13A note above)

**Date:** 2026-05-26
**Round type:** Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — documentation-only closure-definition round (documentation only).
**Status:** Historical record. This note described Phase 12D while it was an implementation candidate. Phase 12D has since been **LOCKED** and is the last locked phase, **Phase 12 — Portfolio / SE Demo Packaging — has been CLOSED**, and Phase 13 is now STARTED with Phase 13A the current implementation candidate — see the Phase 13A note above and the Handoff State dashboard below.

Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — is now
**LOCKED** and is the last locked phase. Gemini reviewed Phase 12C and returned
SAFE TO LOCK with no critical findings, no non-blocking findings, and no
required edits; the user then locked Phase 12C. **Phase 12 — Portfolio / SE
Demo Packaging — is STARTED and is not closed.** Phase 12E is optional, future,
contingency-only work — it exists only if the Phase 12D review finds a
substantive gap — and has **not** started. Phase 13 — Operator GUI / Decoupled
Frontend Vision — is roadmap-preserved only (`docs/GUI_vision.md` and the
`docs/roadmap.md` Phase 13 note) and has **not** started.

Phase 12D is the fourth subphase of Phase 12. It is a documentation-only
closure-definition round: it defines what it means to close Phase 12, records
the final Phase 12A–12C portfolio asset inventory, and prepares the Phase 12
closure decision — it does **not** itself close Phase 12. It adds three `docs/`
documents — `phase12-closure-plan.md` (Phase 12 closure criteria, the asset
inventory, the closure-readiness checklist, the remaining-gaps / no-go
criteria, the close-after-12D vs bounded-cleanup vs separate-12E recommendation,
and the Phase 13 boundary statement), `final-portfolio-handoff.md` (a
cold-reader handoff with current-state snapshot, tiered reviewer paths, a
suggested demo flow, an evidence map, explicit limitations, and the next-phase
boundary), and `phase12-final-review-checklist.md` (the checklist a reviewer
uses at the Phase 12D / Phase 12 closure gate) — and synchronizes the State
Preservation Bundle. It changed no `src/`, `pyproject.toml`, `uv.lock`,
dependency, or runtime/product/API/CLI/telemetry behaviour, and adds no Phase
13 GUI implementation; its only `tests/` change is the narrow, explicitly
authorized mechanical advance of the state-discipline guard
`tests/test_failure_mode_regression.py` to the Phase 12D current-state
expectations. Per the Phase Closure Protocol, Phase 12D is an implementation
candidate, pending review, **not locked**.

*(The Handoff State dashboard further down is the authoritative current-status
snapshot and has been updated to the Phase 13A state. The Phase 12C-era and
Phase 12B-era notes below — and the Phase 12A.1, Phase 12A, and Phase 11x notes
further below — are historical records.)*

---

# Phase 12C implementation-candidate note — Portfolio Demo Narrative / Public Presentation Kit (historical record — Phase 12C is LOCKED; see the Phase 12D note above)

**Date:** 2026-05-26
**Round type:** Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — documentation-first portfolio packaging (documentation only).
**Status:** Historical record. This note described Phase 12C while it was an implementation candidate. Phase 12C has since been **LOCKED** and is the last locked phase; Phase 12D is now the current implementation candidate — see the Phase 12D note above and the Handoff State dashboard below.

Phase 12B — Portfolio Evidence Pack / Reviewer Assets — is now **LOCKED** and is
the last locked phase; the accepted Phase 12B.1 state-hygiene cleanup, Phase
12B.2 Phase 13 GUI roadmap-preservation cleanup, and Phase 12B.3 residual
living-doc state-wording cleanup sub-rounds are folded into the Phase 12B lock
lineage and are not independently locked phases. Gemini reviewed the combined
Phase 12B sequence and returned SAFE TO LOCK with no required edits; the user
then locked Phase 12B. **Phase 12 — Portfolio / SE Demo Packaging — is STARTED
and is not closed.** Phase 12D and every later Phase 12 subphase have **not**
started. Phase 13 — Operator GUI / Decoupled Frontend Vision — is
roadmap-preserved only (`docs/GUI_vision.md` and the `docs/roadmap.md` Phase 13
note) and has **not** started.

Phase 12C is the third subphase of Phase 12. It is a documentation-first
portfolio-packaging round: it converts the project's existing technical
evidence into polished, reusable public-presentation assets. It adds four
`docs/` documents — `portfolio-demo-narrative.md` (a concise demo narrative),
`demo-talk-track.md` (a 5/10/20-minute spoken walkthrough),
`interview-story-bank.md` (reusable interview answer frames), and
`public-repository-readiness.md` (a public-viewing readiness checklist) —
lightly updates `README.md` to point reviewers to them, and synchronizes the
State Preservation Bundle. It changed no `src/`, `pyproject.toml`, `uv.lock`,
dependency, or runtime/product/API/CLI/telemetry behaviour, and adds no Phase
13 GUI implementation; its only `tests/` change is the narrow, explicitly
authorized mechanical advance of the state-discipline guard
`tests/test_failure_mode_regression.py` to the Phase 12C current-state
expectations. Per the Phase Closure Protocol, Phase 12C is an implementation
candidate, pending review, **not locked**.

*(The Handoff State dashboard further down is the authoritative current-status
snapshot and has been updated to the Phase 12C state. The Phase 12B-era notes
below — the Phase 12B.3, 12B.2, 12B.1, and Phase 12B notes — and the Phase
12A.1, Phase 12A, and Phase 11x notes further below, are historical records.)*

---

# Phase 12B.3 residual living-doc state-wording cleanup note — Portfolio Evidence Pack / Reviewer Assets (bounded cleanup, NOT A LOCK — historical record)

**Round type:** residual state-hygiene cleanup of living/cold-session documents after Phase 12B.2.
**Status:** Historical record. This was a documentation-only cleanup sub-round of the Phase 12B round; it is **not a lock**. Phase 12B has since been **LOCKED** (with Phase 12B.1 / 12B.2 / 12B.3 folded into its lock lineage), and Phase 12C is now the current implementation candidate — see the Phase 12C note above and the Handoff State dashboard below.

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
**Round type:** Phase 12B — Portfolio Evidence Pack / Reviewer Assets — reviewer/evidence documentation packaging (documentation only).
**Status:** Phase 12B — Portfolio Evidence Pack / Reviewer Assets is an **implementation candidate / pending review — NOT locked.**

Phase 12A — Portfolio / SE Demo Packaging Baseline — is now **LOCKED** and is
the last locked phase; the accepted Phase 12A.1 state-hygiene cleanup sub-round
is folded into the Phase 12A lock lineage and is not an independently locked
phase. **Phase 12 — Portfolio / SE Demo Packaging — is STARTED and is not
closed.** Phase 12C and every later Phase 12 subphase have **not** started —
Phase 12C is planned, future work only and has not begun.

Phase 12B is the second subphase of Phase 12. It adds four reviewer/evidence
`docs/` documents — `portfolio-evidence-index.md`, `se-interview-evidence-matrix.md`,
`demo-reviewer-checklist.md`, and `portfolio-public-copy.md` — lightly updates
`README.md` to point reviewers to them, and synchronizes the State Preservation
Bundle. It changed no `src/`, `pyproject.toml`, `uv.lock`, dependency, or
runtime/product behaviour; its only `tests/` change is the narrow, explicitly
authorized §5 mechanical advance of the state-discipline guard
`tests/test_failure_mode_regression.py` to the Phase 12B current-state
expectations. Per the Phase Closure Protocol, Phase 12B is an implementation
candidate, pending review, **not locked**.

*(The Phase 12A.1 and Phase 12A notes below are historical records — Phase 12A
is locked. The "Handoff State" dashboard further down is the authoritative
current-status snapshot and has been updated to the Phase 12B state.)*

---

# Phase 12A.1 state-hygiene cleanup note — Portfolio / SE Demo Packaging Baseline (folded into the Phase 12A lock — historical record)

**Date:** 2026-05-26
**Round type:** bounded state-hygiene cleanup of the Phase 12A round (documentation only).
**Status:** Historical record. Phase 12A has since been **LOCKED**; the Phase 12A.1 cleanup is folded into the Phase 12A lock lineage as an accepted sub-round. Current status is in the Phase 12B note above and the Handoff State dashboard below.

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

# Phase 12A note — Portfolio / SE Demo Packaging Baseline (locked — historical record)

**Date:** 2026-05-26
**Candidate artifact:** `storytime-phase12a-portfolio-se-demo-packaging-baseline.tar.gz` (SHA-256 reported on delivery).
**Source artifact:** `storytime-phase11d-release-candidate-evidence-pack.tar.gz` (SHA-256 `07a3973e3dbb69d760ff2c330418f85101c2afa1464fc0eed752fc7053894d94`).
**Status:** Phase 12A — Portfolio / SE Demo Packaging Baseline is **LOCKED / ACCEPTED / CANONICAL** (locked after the accepted Phase 12A.1 state-hygiene cleanup sub-round). *(Historical record — current status is in the Phase 12B note above and the Handoff State dashboard below.)*
**Last locked phase:** Phase 12A — Portfolio / SE Demo Packaging Baseline (this phase).
**Current phase:** *(superseded — see the Phase 12B note above.)*
**Next review gate:** *(superseded — Phase 12A is locked.)*

Phase 11 — Release Candidate Hardening — is **CLOSED**. Phase 11D — Release
Candidate Evidence Pack — completed its Phase Closure Protocol out-of-band
(GPT-5.5 review PASS; Gemini review SAFE TO LOCK; no required edits); the user,
as final decision-maker, then locked Phase 11D, formally closed Phase 11, and
authorized Phase 12. That out-of-band closure was a user/mediator decision
supplied to the Phase 12A round and recorded — not re-reviewed — by it. The
locked Phase 11D artifact is
`storytime-phase11d-release-candidate-evidence-pack.tar.gz` (SHA-256
`07a3973e3dbb69d760ff2c330418f85101c2afa1464fc0eed752fc7053894d94`).

Phase 12A is the first subphase of Phase 12 — Portfolio / SE Demo Packaging. It
is a documentation and portfolio-packaging round: it makes StoryTime
explainable as a Solutions Engineer / observability / OpenTelemetry portfolio
project without adding any product feature or changing any runtime behaviour.
It added four `docs/` documents — `portfolio-overview.md`,
`solutions-engineer-narrative.md`, `portfolio-demo-script.md`, and
`interview-talking-points.md` — refined `README.md` for a portfolio-facing
reviewer, and synchronized the State Preservation Bundle. It added no product
feature, no UI, no server, no JavaScript, no generated audio, no
screenshots/binary assets, and no new dependency; it changed no pipeline
behaviour, `storytime rerun`, or Trust Envelope enforcement, and changed no
`pyproject.toml`, `uv.lock`, or `src/` content. The only `tests/` change is a
narrow, explicitly authorized advance of the state-discipline guard
`tests/test_failure_mode_regression.py` to the Phase 12A current-state
expectations.

Per the Phase Closure Protocol, Phase 12A is implementation output and is
**not** a locked phase: it is not lock-ready until GPT-5.5 review, Gemini
critique, any cleanup, and explicit user approval complete. Phase 12A does not
lock Phase 12A, does not close Phase 12, and does not start Phase 12B.
**Phase 12B — and every later Phase 12 subphase — has not started**; Phase 12B
is future, planned work only.

*(This Phase 12A note records the current implementation candidate. The
Phase 11D note below — now a historical record, since Phase 11D is locked and
Phase 11 is closed — and the Phase 11C, Phase 11B, Phase 11A, and Phase 10G
notes further below are historical records.)*

---

# Phase 11D note — Release Candidate Evidence Pack (locked — historical record)

**Date:** 2026-05-25
**Candidate artifact:** `storytime-phase11d-release-candidate-evidence-pack.tar.gz` (SHA-256 `07a3973e3dbb69d760ff2c330418f85101c2afa1464fc0eed752fc7053894d94`).
**Source artifact:** `storytime-phase11c-failure-mode-regression-hardening.tar.gz` (SHA-256 `2dd31442e62c13241a64d10c2d117aefedc3b9c633ad5ea5d1fa94cfaad7d57b`).
**Status:** Phase 11D — Release Candidate Evidence Pack is **LOCKED / ACCEPTED / CANONICAL**; with Phase 11D locked, **Phase 11 — Release Candidate Hardening — is CLOSED**. *(This note was written when Phase 11D was an implementation candidate; it was subsequently locked out-of-band and Phase 11 was closed. Current status is in the Phase 12B note above.)*
**Previous locked phase** — Phase 11C — Failure-Mode / Regression Hardening.
**Current phase** — *(superseded — see the Phase 12B note above.)*
**Next review gate:** *(superseded — see the Phase 12B note above.)*

Phase 11D is the fourth and final planned Release Candidate Hardening subphase.
It is an evidence, closure-readiness, and proof-consolidation round: it
consolidates the release-candidate evidence produced by Phases 11A, 11B, and
11C into a reviewer-facing index, records the canonical validation results,
prepares a Phase 11 closure checklist, and writes a Phase 12 readiness handoff.
It added four `docs/` documents — `release-candidate-evidence-pack.md` (the
overview and the release-candidate evidence index),
`final-validation-summary.md` (the canonical validation results),
`phase11-closure-checklist.md` (what each Phase 11 subphase contributed and the
conditions for an explicit Phase 11 closure decision), and
`phase12-readiness-handoff.md` (what Phase 12 may safely do) — refreshed the
status notes in `docs/phase11-plan.md`, `docs/release-candidate-hardening.md`,
and `docs/rc-validation-checklist.md`, and synchronized the State Preservation
Bundle. It added no product feature, no UI, no server, no JavaScript, no
generated audio, no screenshots/binary assets, no new dependency, and no schema
change; it changed no pipeline behaviour, `storytime rerun`, or Trust Envelope
enforcement, and changed no `pyproject.toml`, `uv.lock`, `src/`, or `tests/`
content — it is documentation/evidence consolidation only and added no test.
Phase 11D subsequently completed its Phase Closure Protocol out-of-band
(GPT-5.5 review PASS; Gemini review SAFE TO LOCK; no required edits) and was
locked by explicit user decision; with Phase 11D locked, **Phase 11 — Release
Candidate Hardening — is CLOSED**, and Phase 12 was authorized.

*(This Phase 11D note is a historical record — Phase 11D is locked and Phase 11 is closed. Current state is recorded in the active Phase 12B / Phase 12B.2 notes at the top of this file; the Phase 12A, Phase 11C, Phase 11B, Phase 11A, and Phase 10G notes below are historical records.)*

---

# Phase 11C note — Failure-Mode / Regression Hardening (locked — historical record)

**Date:** 2026-05-25
**Locked artifact:** `storytime-phase11c-failure-mode-regression-hardening.tar.gz` (SHA-256 `2dd31442e62c13241a64d10c2d117aefedc3b9c633ad5ea5d1fa94cfaad7d57b`).
**Source artifact:** `storytime-phase11b-fresh-clone-operator-reproducibility.tar.gz` (SHA-256 `08b72f2833da9adf3b8acc1f3170334eb7c5f998e19263838efbce2f571cc73f`).
**Status:** Phase 11C — Failure-Mode / Regression Hardening is **LOCKED / ACCEPTED / CANONICAL** — it was the last locked phase at that point in the project history. *(This is a superseded point-in-time record, originally written when Phase 11C was an implementation candidate; it was subsequently locked under the Phase Closure Protocol, and is the source/base artifact for Phase 11D. Current status is in the Phase 12B note above.)*
**Previous locked phase:** Phase 11B — Fresh Clone / Operator Reproducibility.
**Next review gate:** *(superseded — see the Phase 12B note above.)*

Phase 11C is the third Release Candidate Hardening subphase. It is a
failure-mode and regression-hardening round: it inventories the highest-risk
failure and regression paths that already exist in StoryTime, records which
tests and gates protect each one, and documents how a local operator should
respond to a failure without bypassing governance or deleting state. It added
four `docs/` documents — `failure-mode-regression-hardening.md` (the overview),
`regression-risk-register.md` (the risk inventory),
`failure-mode-test-matrix.md` (the regression coverage map), and
`operator-failure-response.md` (the operator playbook) — and one focused
regression test module, `tests/test_failure_mode_regression.py`, which converts
the project's state-documentation discipline rule into an executable guard. It
synchronized the State Preservation Bundle. It added no product feature, no UI,
no server, no JavaScript, no generated audio, no screenshots/binary assets, no
new dependency, and no schema change; it changed no pipeline behaviour,
`storytime rerun`, or Trust Envelope enforcement, and changed no
`pyproject.toml`, `uv.lock`, or `src/` content. The only `tests/` change is the
new regression module. Phase 11C — Failure-Mode / Regression Hardening —
completed the Phase Closure Protocol and has since been locked; it was the last locked phase at that point in the project history, and is the source/base artifact for Phase 11D.

*(This Phase 11C note is a superseded point-in-time record. Current state is recorded in the active Phase 12B / Phase 12B.2 notes at the top of this file; the Phase 12A, Phase 11B, Phase 11A, and Phase 10G notes below are historical records.)*

---

# Phase 11B note — Fresh Clone / Operator Reproducibility (locked — historical record)

**Date:** 2026-05-25
**Locked artifact:** `storytime-phase11b-fresh-clone-operator-reproducibility.tar.gz` (SHA-256 `08b72f2833da9adf3b8acc1f3170334eb7c5f998e19263838efbce2f571cc73f`).
**Status:** Phase 11B — Fresh Clone / Operator Reproducibility is **LOCKED / ACCEPTED / CANONICAL** — it was the last locked phase at that point in the project history. *(This is a superseded point-in-time record, originally written when Phase 11B was an implementation candidate; Phase 11B was subsequently locked under the Phase Closure Protocol, and is the source/base artifact for Phase 11C. Current status is in the Phase 12B note above.)*
**Last locked phase before Phase 11B:** Phase 11A — Release Candidate Hardening Baseline.
**Next review gate:** *(superseded — see the Phase 12B note above.)*

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
Phase 10G lock closure note further below is a historical record; Phase 10 and
Phase 11 are both CLOSED; Phase 12A is locked, and Phase 12B is the current
implementation candidate — see the Phase 12B note at the top of this file.)*

---

# Phase 11A note — Release Candidate Hardening Baseline (locked — historical record)

**Date:** 2026-05-25
**Locked artifact:** `storytime-phase11a-release-candidate-hardening-baseline.tar.gz` (SHA-256 `664f8ba4ae90cf6a98ccc7d20369e690eac74497ab78f2b7067f0aac2079a7aa`).
**Status:** Phase 11A — Release Candidate Hardening Baseline is **LOCKED / ACCEPTED / CANONICAL**. *(This is a superseded point-in-time record, originally written when Phase 11A was an implementation candidate; Phase 11A was subsequently locked under the Phase Closure Protocol. Phase 11B, Phase 11C, and Phase 11D have since also been locked and Phase 11 — Release Candidate Hardening — is CLOSED; current status is in the Phase 12B note above.)*
**Last locked work item before Phase 11A:** Post-Phase-10 Historical State Reconciliation.
**Next review gate:** *(superseded — see the Phase 12B note above.)*

Phase 11A is the first Release Candidate Hardening subphase. It is
documentation-first: it audits and documents the repository's non-feature
surfaces — fresh-clone readiness, the validation-command baseline, artifact
hygiene, the security/secrets posture, demo reproducibility, known limitations,
and the Phase 11 decomposition. It added seven `docs/` hardening documents
(`release-candidate-hardening.md`, `phase11-plan.md`, `local-setup-runbook.md`,
`fresh-clone-checklist.md`, `rc-validation-checklist.md`,
`security-secrets-checklist.md`, `demo-reproducibility-checklist.md`) and
synchronized the State Preservation Bundle. It added no product feature, no UI,
no server, no JavaScript, no generated audio, no screenshots/binary assets, no
new dependency, and no schema change; it changed no pipeline behaviour,
`storytime rerun`, or Trust Envelope enforcement, and changed no
`pyproject.toml`, `uv.lock`, `src/`, or `tests/` content. The six Docker-free
quality gates pass (549 tests, ruff/mypy/import-linter clean, `storytime
doctor` healthy).

*(The Phase 10G lock closure note below is a historical record. Phase 10 is
CLOSED; the Post-Phase-10 Historical State Reconciliation was the last locked
work item before Phase 11; Phase 11A and Phase 11B are locked; Phase 11C is
the current implementation candidate.)*

---

# Phase 10G lock closure note — Phase 10 CLOSED

**Date:** 2026-05-25
**Locked artifact:** `storytime-phase10g1-uvlock-reversion-cleanup.tar.gz`
**SHA-256:** `8a0cc9a5b6426a291bec3a793e41501c7d3492187dd48b4f7729ea95e501a0c1`
**Status:** Phase 10G — Portfolio Narrative / Phase 10 Closure is **LOCKED / ACCEPTED / CANONICAL**. **Phase 10 is formally CLOSED.**
**Last locked phase:** Phase 10G — Portfolio Narrative / Phase 10 Closure.
**Next phase:** Phase 11 — Release Candidate Hardening *(Phase 11 has since been completed and is CLOSED — Phase 11A through 11D all locked; Phase 12 is now STARTED. See the Phase 12A note at the top of this file for current status)*.
**Next action:** *(superseded — see the Phase 12B note above.)*

Phase 10G — the documentation, portfolio-narrative, demo-explanation, and Phase 10 closure phase — is locked. It added the Phase 10 portfolio/closure documents (`docs/portfolio-narrative.md`, `docs/demo-script.md`, `docs/operator-experience-walkthrough.md`, `docs/command-reference.md`, `docs/known-limitations.md`, `docs/observability-governance-talking-points.md`, `docs/phase10-acceptance-checklist.md`, `docs/screenshot-instructions.md`) and synchronized the State Preservation Bundle. It added no product feature, no UI, no server, no JavaScript, no generated audio, no screenshots/binary assets, and no new dependency; it changed no pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, or the database schema. Phase 10G completed the Phase Closure Protocol — GPT-5.5 review PASS, Gemini review SAFE WITH EDITS, the Phase 10G.1 `uv.lock` cleanup (the suspected drift was a false positive), GPT-5.5 Phase 10G.1 verification PASS, Gemini Phase 10G.1 final verification SAFE TO LOCK, and explicit user lock approval. With Phase 10G locked, **Phase 10 — Product UI / Operator Experience — is formally CLOSED** (Phases 10A–10G all locked). The next phase is **Phase 11 — Release Candidate Hardening**, which has **not started**. This note was synchronized by the Post-Phase-10 Closure State Synchronization task.

*(The Phase 10F lock closure note and the Phase 10E / Phase 10C lock closure notes below are historical records. Phase 10A, 10B, 10C, 10C.1, 10D, 10D.1, 10E — with the 10E.1 / 10E.2 cleanup sequence — 10F, and 10G are all locked; Phase 10 is closed.)*

---

# Phase 10F lock closure note

**Date:** 2026-05-25
**Lock archive:** `storytime-phase10f-demo-seed-data-golden-path-fixtures.tar.gz`
**SHA-256:** `e060570a94fb19f790c539542b3ef7445111430bc308668675548f66fa48df55`
**Status:** Phase 10F — Demo Seed Data / Golden Path Fixtures is **LOCKED / ACCEPTED / CANONICAL**.
**Last locked phase:** Phase 10F.
**Next phase:** Phase 10G — Portfolio Narrative / Phase 10 Closure.

Phase 10F added curated demo seed data and golden-path fixture scenarios — the `demo/` directory (four original CC0 seed texts plus schema-valid manifests, a demo-only blocked-source deny-list, and six fixture definitions), the `docs/demo.md` operator runbook, and `tests/test_demo_fixtures.py`. It was fixture / demo-readiness work that exercises the existing system only: no new product feature, no UI, no server, no generated audio committed, no JavaScript, no new dependency, no change to pipeline, `storytime rerun`, Trust Envelope enforcement, or the database schema. Phase 10F completed the Phase Closure Protocol and was locked with explicit user approval.

*(The Phase 10E lock closure note and the Phase 10C lock closure note below are historical records, superseded by this Phase 10F closure.)*

---

# Phase 10E lock closure note

**Date:** 2026-05-25
**Lock archive:** `storytime-phase10e2-final-cleanup-v2-normalized.tar.gz`
**Status:** Phase 10E — Static HTML Operator Report Refinement is **LOCKED / ACCEPTED / CANONICAL**, with the Phase 10E.1 / 10E.2 cleanup sequence accepted and the normalized cleanup as the canonical state.
**Last locked phase:** Phase 10E / 10E.2 normalized cleanup.
**Next phase:** Phase 10F — Demo Seed Data / Golden Path Fixtures, not started before the Phase 10F implementation above.

Phase 10E refined the existing generated static HTML operator report for clarity, usability, and demo readiness — an executive status summary, rerun eligibility / action guidance, a failure summary, a command reference, semantic status badges, an improved governance warning block, and improved embedded CSS — with the report still a local, static, read-only artifact (no JavaScript, no external assets, no browser-side mutation controls, no backend behavior change). The Phase 10E.1 / 10E.2 cleanup sequence addressed raw `blocked_reason` redaction, archive hygiene, and state-preservation synchronization. Phase 10E was reviewed and locked with explicit user approval.

*(The Phase 10D implementation candidate note and Phase 10C lock closure note below are historical records, superseded by this Phase 10E closure.)*

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

# Handoff State

The current dashboard. Authoritative snapshot of where StoryTime stands right
now, for the next model or session. If another document's status text
disagrees with this file, this file is authoritative for *current status*.
(`docs/canonical-state.md` remains authoritative for the history of *locked
decisions*.) Read `LLM_DIRECTOR.md` first.

## Current phase

**Phase 13 — Portfolio Website / Operator GUI — is STARTED. Phase 13K —
Demo Walkthrough Refresh / Governed Local Chain Story Path — is locked and is
the last locked phase. Phase 13L — Phase 13 Closure / Demo-Local Completion
Lock — is the current subphase: an implementation candidate, pending review,
NOT locked. Phase 13L prepares the Phase 13 closure as a candidate; Phase 13
will be formally closed only after Phase 13L review/lock, so Phase 13 is not yet
closed. Phase 14 — Cloud/Distributed — has not
started, and Phase 14A — Cloud/Distributed Architecture Baseline — is the next
proposed architecture baseline; neither has started.**

Phase 10 — Product UI / Operator Experience — is CLOSED (Phase 10A
through 10G all locked, 2026-05-25). **Phase 11 — Release Candidate
Hardening — is CLOSED** (Phase 11A through 11D all locked). **Phase 12
— Portfolio / SE Demo Packaging — is CLOSED** (Phase 12A through 12D
all locked). The Post-Phase-10 Historical State Reconciliation was the
last locked work item before Phase 11; its locked artifact is
`storytime-post-phase10-roundtable-historical-backfill.tar.gz`
(SHA-256 `367e647c46aa6e4fd039369da30859b11ca783249569df291343db133ef4cfdd`).

Phase 12 closed across four subphases, each locked under the Phase
Closure Protocol: 12A (Portfolio / SE Demo Packaging Baseline), 12B
(Portfolio Evidence Pack / Reviewer Assets), 12C (Portfolio Demo
Narrative / Public Presentation Kit), and 12D (Phase 12 Closure Plan
/ Final Portfolio Handoff Definition). Phase 12A.1 is folded into the
Phase 12A lock lineage, and Phase 12B.1 / 12B.2 / 12B.3 are folded
into the Phase 12B lock lineage, as accepted cleanup sub-rounds —
not independently locked phases. Phase 12D completed its Phase
Closure Protocol out-of-band: Gemini returned the verdict to lock
Phase 12D and close Phase 12, with no critical findings, no
non-blocking findings, and no required edits, and the user then
locked Phase 12D and formally closed Phase 12. The locked Phase 12D
artifact is
`storytime-phase12d-phase12-closure-plan-final-portfolio-handoff.tar.gz`
(SHA-256 `64ad09e875f0653608e0deb756f11ee5adc0d2ff1265e2039cbc51491f286cf8`).
Phase 12E was optional, contingency-only work; the Phase 12D review
found no substantive gap, so Phase 12E was not needed and never
started.

Phase 13 — Portfolio Website / Operator GUI — is the phase that
follows the closed Phase 12. Phase 13A — architecture baseline —,
Phase 13B — typed static portfolio shell —, Phase 13C —
deterministic read-only static export / frontend data alignment —,
Phase 13D — operator workflow view expansion (Governance / Safety,
Failure / Recovery) —, Phase 13D.1 — static operator GUI refinement /
Evidence & disabled action discipline —, Phase 13D.2 — static
demo walkthrough / reviewer story path —, and Phase 13E — Demo-Mode
Action Preview / Operator Intent Boundary — are all locked. Phase 13E
completed its Phase Closure Protocol (GPT-5.5 review, Gemini SAFE TO
LOCK with no required edits) and was locked by explicit user
decision. **Phase 13E is the last locked phase.** Its locked artifact
is
`storytime-phase13e-demo-mode-action-preview-operator-intent-boundary.tar.gz`
(SHA-256 `a997f2ca9d213e28e140f47c63336367c8feda46ed994b41300f86b99f8d8164`).

Phase 13F — Local Bridge Architecture & Contract Baseline — is the
current subphase. It is a documentation-and-static-fixture
architecture / contract baseline over the locked Phase 13E operator
GUI — the architectural lock before any Python local-bridge
implementation is allowed (it is to the Local Bridge what Phase 13A
was to the operator GUI). The central principle it establishes:
**the frontend is an operator surface, not the durable storage
layer.** Durable state must live outside the browser in an explicit
external workspace / storage target with clear export, reset, backup,
and recovery semantics, so StoryTime never repeats the RoundTable
browser-storage failure mode; the browser may hold transient UI state
only, and `localStorage` / `sessionStorage` / `IndexedDB` remain
forbidden.

Concretely Phase 13F adds eleven new architecture / contract docs
(`docs/local-bridge-architecture.md`,
`docs/externalized-state-architecture.md`,
`docs/browser-storage-policy.md`,
`docs/local-mode-workspace-layout.md`,
`docs/storage-targets-architecture.md`,
`docs/action-execution-boundary.md`, `docs/local-action-dto-spec.md`,
`docs/local-action-audit-spec.md`,
`docs/local-mode-storage-contract.md`,
`docs/local-action-queue-observability.md`, and
`docs/phase13f-local-bridge-contract-readiness.md`); a small set of
non-runtime JSON example fixtures under `docs/examples/`
(local-action-requests, local-action-responses,
local-action-audit-records); and one new Python test
(`tests/test_local_mode_contract_examples.py`) validating those
fixtures with plain Python (no JSON-schema dependency). The docs
settle the Hybrid Option C decisions Gemini required: an
execution-timing policy (long-running actions are asynchronous; the
future bridge returns `202 Accepted` with an `actionRequestId` /
`jobId`; acceptance is not success; export refresh happens after a
durable write; refresh races are avoided with atomic writes +
identity-tagged read models); a loopback-only / strict-origin /
no-arbitrary-command / command-pattern-router security boundary; a
future action allowlist (`retry_failed_stage`,
`inspect_trust_envelope`, `refresh_export`) with higher-risk actions
(`record_review_decision`, `regenerate_operator_report`,
`publish_episode`, `delete_artifact`, provider sync) explicitly
deferred; and a queue-observability model (depth, in-flight,
completed / failed / rejected / dead-letter counts, oldest-queued and
longest-in-flight ages, retry count, capacity, saturation, export
freshness) plus a conservative local load-limit policy and a
distributed/cloud carry-forward.

Phase 13F is a documentation-and-static-fixture round. It implements
**NO** runtime code: no local bridge, no server, no socket, no
subprocess, no async queue, no queue workers, no queue metrics /
exporters, no OpenTelemetry instrumentation, no storage providers, no
provider integrations, no runtime schema validation, no router /
history, no browser storage, no real Local mode, no Cloud/Distributed
mode, and no mutation / action execution. The browser remains
non-durable. The example fixtures are documentation artifacts only —
never imported by runtime code, never generated by a running system,
and they never claim Phase 13F executed anything. Phase 13F does
**not** modify `src/`, `frontend/src/`, `frontend/package.json`,
`frontend/package-lock.json`, `pyproject.toml`, `uv.lock`, or
`frontend/src/data/storytime-demo-export.json`; all are byte-identical
to the locked Phase 13E source. The only allowed code changes are the
narrow, explicitly-authorized mechanical advance of the
state-discipline guard `tests/test_failure_mode_regression.py` to the
Phase 13F current-state expectations, and the new
`tests/test_local_mode_contract_examples.py`.

Per the Phase Closure Protocol, Phase 13F is implementation output —
it is **not** a locked phase until GPT-5.5 review, Gemini critique,
any cleanup, and explicit user approval complete. Phase 13F does
**not** lock Phase 13F, does **not** close Phase 13, and does
**not** start Phase 13G. Phase 13 is in progress and not closed.
Phase 13G and every later Phase 13 subphase have **not** started —
they are future, planned work only, decomposed in
`docs/phase13-roadmap.md` and recommended in
`docs/phase13f-local-bridge-contract-readiness.md`.

*(Historical Phase 11, Phase 12, and Phase 10 round details are in
`docs/phase-history.md` and `docs/canonical-state.md`. All Phase 10,
Phase 11, and Phase 12 sub-phases are locked; Phase 10, Phase 11, and
Phase 12 are all closed.)*

## Last locked phase / last locked work item

- **Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary** is the
  **last locked phase** (locked under the Phase Closure Protocol;
  GPT-5.5 review, then Gemini SAFE TO LOCK with no required edits,
  then an explicit user lock decision). Locked artifact
  `storytime-phase13e-demo-mode-action-preview-operator-intent-boundary.tar.gz`,
  SHA-256 `a997f2ca9d213e28e140f47c63336367c8feda46ed994b41300f86b99f8d8164`.
  It is the seventh subphase of Phase 13 (a sub-round of Phase 13D.2) and
  the source/base artifact for Phase 13F. It added a static Demo-mode
  Action Preview system — a view-model adapter
  (`frontend/src/data/actionPreviewAdapter.ts`) and a presentation panel
  (`frontend/src/components/ActionPreviewPanel.tsx` plus its CSS Module)
  wired into the Failure / Recovery, Governance / Safety, and Evidence /
  Validation views — that lets the operator GUI **preview** what a real
  operator action would look like under future Local or Cloud/Distributed
  mode without ever executing one, alongside the unchanged
  `DisabledFutureActionCard`. It clarified the Demo / Local /
  Cloud-Distributed operating-mode model (distinct from the Demo /
  Active / Candidate data-snapshot model) and added a Python data-integrity
  test (`tests/test_action_preview_data_integrity.py`). It changed no
  `src/`, no `pyproject.toml`, no `uv.lock`, no `frontend/package.json`,
  no `frontend/package-lock.json`, and no root dependency; the protected
  backend export generator, the committed static export JSON, the CLI app,
  and the `storytime export-demo-ui` contract were byte-identical to the
  Phase 13D.2 source, and `DisabledFutureActionCard` remained
  byte-identical and truly disabled.
- **Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path** is
  locked (locked under the Phase Closure Protocol;
  GPT-5.5 review, then Gemini SAFE TO LOCK with no required edits,
  then an explicit user lock decision). Locked artifact
  `storytime-phase13d2-static-demo-walkthrough-reviewer-story-path.tar.gz`,
  SHA-256 `cd553679ce109483b69e99f51fceab34af216c9b1ce7dfe859fc7b78c13cd429`.
  It is the sixth subphase of Phase 13 (a sub-round of Phase 13D.1) and
  the source/base artifact for Phase 13E. It replaced the honest Demo
  Walkthrough placeholder with a real read-only guided reviewer / demo
  path view (`frontend/src/components/DemoWalkthroughView.tsx` plus its
  CSS Module) backed by a static view-model adapter
  (`frontend/src/data/demoWalkthroughAdapter.ts`) holding the long-form
  route content, offered four reviewer routes (5-minute scan, 10-minute
  SE-style demo, technical deep-dive, self-guided reviewer) via a
  simple segmented control, embedded eight architecture-checkpoint
  cards absorbing ~80–90% of an Architecture Story narrative, added a
  "what is intentionally deferred" section and interview / SE
  talking-point cards, updated `frontend/src/navigation.ts` to promote
  Demo Walkthrough to a real view, and updated `App.tsx` to render the
  new view with navigation callbacks. It changed no `src/`, no
  `pyproject.toml`, no `uv.lock`, no `frontend/package.json`, no
  `frontend/package-lock.json`, no core pipeline runtime behaviour, and
  no root dependency; the protected backend export generator, JSON, CLI
  app, and `storytime export-demo-ui` contract were byte-identical to
  the Phase 13D.1 source.
- **Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled
  Action Discipline** is locked (locked under the Phase Closure
  Protocol; GPT-5.5 review, then Gemini SAFE TO LOCK with no required
  edits, then an explicit user lock decision). Locked
  artifact
  `storytime-phase13d1-static-operator-gui-refinement-evidence-disabled-actions.tar.gz`,
  SHA-256 `812841381075e0e7839266512eb6d7f41bf2d890ee4c82b91627ce824f5b1eae`.
  It is the fifth subphase of Phase 13 (a sub-round of Phase 13D) and
  the source/base artifact for Phase 13D.2. It added the reusable
  disabled future-action component pair
  (`frontend/src/components/DisabledFutureActionCard.tsx` plus its CSS
  Module — real `<button disabled={true}>` with no `onClick`), refactored
  the Governance / Safety and Failure / Recovery views to consume it,
  replaced the Evidence / Validation placeholder with a real read-only
  view (`frontend/src/components/EvidenceValidationView.tsx` plus its
  CSS Module) carrying the mandatory STATIC PORTFOLIO DATA — NOT A LIVE
  CI/CD DASHBOARD disclaimer and repository-relative evidence
  references, added the evidence adapter
  (`frontend/src/data/evidenceAdapter.ts`) with the Demo / Active /
  Candidate Data Source framing, and extracted navigation metadata from
  `App.tsx` into `frontend/src/navigation.ts` (the View type, NAV array,
  and PLACEHOLDERS map — slimming `App.tsx` from 228 to 136 lines). It
  changed no `src/`, no `pyproject.toml`, no `uv.lock`, no
  `frontend/package.json`, no `frontend/package-lock.json`, no core
  pipeline runtime behaviour, and no root dependency; the protected
  backend export generator, JSON, CLI app, and `storytime export-demo-ui`
  contract were byte-identical to the Phase 13D source.
- **Phase 13D — Operator Workflow View Expansion (Governance / Safety,
  Failure / Recovery)** is locked (locked under the Phase Closure
  Protocol; GPT-5.5 review, then Gemini SAFE TO LOCK with no required
  edits, then an explicit user lock decision). Locked artifact
  `storytime-phase13d-operator-workflow-view-expansion-governance-failure.tar.gz`,
  SHA-256 `5ec0b1edaaedfed2f3ae9b3e221e6a9089c52b8df152c4824503e7ca796894f3`.
  It is the fourth subphase of Phase 13 and the source/base artifact for
  Phase 13D.1. It added two new real read-only operator view components
  (`frontend/src/components/GovernanceSafetyView.tsx` and
  `FailureRecoveryView.tsx`) with co-located CSS Modules, two
  domain-specific view-model adapters
  (`frontend/src/data/governanceAdapter.ts` and `failureAdapter.ts`)
  projecting the locked Phase 13C export, the ambient CSS-Modules
  TypeScript declaration, App-level navigation rewiring with the read-only
  "Data source · Demo Snapshot" header chip and an inspect-this-run
  drill-down into the existing Pipeline Run Detail view, and a small
  `.data-chip` rule in the shared global stylesheet (the only global
  addition). It changed no `src/`, no `pyproject.toml`, no `uv.lock`, no
  core pipeline runtime behaviour, and no root dependency; the protected
  backend export generator and JSON were byte-identical to the Phase 13C
  source.
- **Phase 13C — Deterministic Read-Only Static Export / Frontend Data
  Alignment** is locked (locked under the Phase Closure Protocol;
  GPT-5.5 review, then Gemini SAFE TO LOCK with no required edits, then
  an explicit user lock decision). Locked artifact
  `storytime-phase13c-deterministic-read-only-static-export-frontend-data-alignment.tar.gz`,
  SHA-256 `1c24cf03283590d7f095d3805bc8f5d560e3583131c04e5be0359e0053145507`.
  It is the third subphase of Phase 13 and the source/base artifact for
  Phase 13D. It added a small read-only backend export module
  (`src/storytime/operator_export.py`) and `storytime export-demo-ui` CLI
  command producing the deterministic static JSON export
  (`frontend/src/data/storytime-demo-export.json`, top-level `schemaVersion`
  `"1.0"`), the export contract document, the frontend deferred-work
  register, the frontend adapter and `StaticDemoExport` type, backend
  contract tests, and rewired the homepage and Pipeline Run Detail / Stage
  Timeline onto the adapter. It changed no core pipeline runtime behaviour
  and no root dependency.
- **Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline
  Scaffold** is locked (locked under the Phase Closure Protocol; GPT-5.5
  review, then Gemini SAFE TO LOCK with no required edits, then an explicit
  user lock decision). Locked artifact
  `storytime-phase13b-typed-static-portfolio-shell-minimal-visual-pipeline-scaffold.tar.gz`,
  SHA-256 `9319ece26f5b457ddbbefaab346aba61cb61f65a6b7b729b5acaa12f30df3f24`.
  It is the second subphase of Phase 13 and the source/base artifact for Phase
  13C. It added the bounded React + TypeScript + Vite static frontend shell and
  changed no `pyproject.toml`, `uv.lock`, or `src/`.
- **Phase 13A — Portfolio Website / Operator GUI Architecture Baseline** is
  locked (locked under the Phase Closure Protocol; GPT-5.5 review, then Gemini
  SAFE TO LOCK with no required edits, then an explicit user lock decision).
  Locked artifact
  `storytime-phase13a-portfolio-website-operator-gui-architecture-baseline.tar.gz`,
  SHA-256 `100098aa6280b740a6eeb862c1e1923d2e031bd02a06786b7a8b8ec07facf1c0`.
  It is the first subphase of Phase 13 — Portfolio Website / Operator GUI. It
  was a documentation-only architecture-baseline round and changed no
  `pyproject.toml`, `uv.lock`, or `src/`.
- **Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition** is
  locked (locked out-of-band under the Phase Closure Protocol; the Phase 12D
  review returned the verdict to lock Phase 12D and close Phase 12, with no
  required edits). Locked artifact
  `storytime-phase12d-phase12-closure-plan-final-portfolio-handoff.tar.gz`,
  SHA-256 `64ad09e875f0653608e0deb756f11ee5adc0d2ff1265e2039cbc51491f286cf8`.
  It is the fourth and final subphase of Phase 12 — Portfolio / SE Demo
  Packaging — and, with it locked, **Phase 12 is CLOSED**. It was a
  documentation-only closure-definition round and changed no `pyproject.toml`,
  `uv.lock`, or `src/`.
- **Phase 12C — Portfolio Demo Narrative / Public Presentation Kit** is locked
  under the Phase Closure Protocol. Locked artifact
  `storytime-phase12c-portfolio-demo-narrative-public-presentation-kit.tar.gz`,
  SHA-256 `4c98a25d6bb0ae751b4ba33851bc60e7d7805d4fd31ebcfc45c2d30a659301da`.
  It is the third subphase of Phase 12.
- **Phase 12B — Portfolio Evidence Pack / Reviewer Assets** is locked under the
  Phase Closure Protocol (the accepted Phase 12B.1 / 12B.2 / 12B.3 cleanup
  sub-rounds folded into its lock lineage). It is the second subphase of
  Phase 12.
- **Phase 12A — Portfolio / SE Demo Packaging Baseline** is locked under the
  Phase Closure Protocol (locked after the accepted Phase
  12A.1 state-hygiene cleanup sub-round). Locked artifact
  `storytime-phase12a-portfolio-se-demo-packaging-baseline.tar.gz` (the locked
  Phase 12A lineage; the accepted Phase 12A.1 cleanup
  `storytime-phase12a1-state-hygiene-cleanup.tar.gz`, SHA-256
  `5f9eca1cc8c2efb55d57f87becdc53cd0d8e514221947e445965232f608b621a`, is folded
  into this lock and is the source/base artifact for Phase 12B). Phase 12A is
  the first subphase of Phase 12 — Portfolio / SE Demo Packaging; it was a
  documentation and portfolio-packaging round and changed no `pyproject.toml`,
  `uv.lock`, or `src/`.
- **Phase 11D — Release Candidate Evidence Pack** is locked out-of-band under
  the Phase Closure Protocol. Locked artifact
  `storytime-phase11d-release-candidate-evidence-pack.tar.gz`, SHA-256
  `07a3973e3dbb69d760ff2c330418f85101c2afa1464fc0eed752fc7053894d94`. It is the
  fourth and final subphase of Phase 11 and the source/base artifact for
  Phase 12A. It was an evidence, closure-readiness, and proof-consolidation
  round; it changed no `pyproject.toml`, `uv.lock`, `src/`, or `tests/`. With
  Phase 11D locked, **Phase 11 — Release Candidate Hardening — is CLOSED**.
- **Phase 11C — Failure-Mode / Regression Hardening** is locked under the Phase
  Closure Protocol. Locked artifact
  `storytime-phase11c-failure-mode-regression-hardening.tar.gz`, SHA-256
  `2dd31442e62c13241a64d10c2d117aefedc3b9c633ad5ea5d1fa94cfaad7d57b`. It is the
  third subphase of Phase 11.
- **Phase 11B — Fresh Clone / Operator Reproducibility** is locked under the
  Phase Closure Protocol. Locked artifact
  `storytime-phase11b-fresh-clone-operator-reproducibility.tar.gz`, SHA-256
  `08b72f2833da9adf3b8acc1f3170334eb7c5f998e19263838efbce2f571cc73f`. It is the
  second subphase of Phase 11.
- **Phase 11A — Release Candidate Hardening Baseline** is locked under the
  Phase Closure Protocol. Locked artifact
  `storytime-phase11a-release-candidate-hardening-baseline.tar.gz`, SHA-256
  `664f8ba4ae90cf6a98ccc7d20369e690eac74497ab78f2b7067f0aac2079a7aa`. It is the
  first subphase of Phase 11.
- **Post-Phase-10 Historical State Reconciliation** was the **last locked work
  item before Phase 11** (2026-05-25) — a documentation/state-history
  reconciliation checkpoint, **not a new phase**. Locked artifact
  `storytime-post-phase10-roundtable-historical-backfill.tar.gz`,
  SHA-256 `367e647c46aa6e4fd039369da30859b11ca783249569df291343db133ef4cfdd`.
- **Phase 10G — Portfolio Narrative / Phase 10 Closure** is the locked phase
  that closed Phase 10, locked 2026-05-25. Locked artifact
  `storytime-phase10g1-uvlock-reversion-cleanup.tar.gz`, SHA-256
  `8a0cc9a5b6426a291bec3a793e41501c7d3492187dd48b4f7729ea95e501a0c1`.
  With Phase 10G locked, **Phase 10 is formally CLOSED**.
- **Phase 10F — Demo Seed Data / Golden Path Fixtures** is locked, 2026-05-25.
- **Phase 10E — Static HTML Operator Report Refinement** is locked,
  2026-05-25, with the Phase 10E.1 / 10E.2 cleanup sequence accepted.
- **Phase 10D / 10D.1, 10C / 10C.1, 10B, 10A** — all locked (2026-05-25 and
  earlier); see `docs/canonical-state.md` for the full ledger.
- Phase 9B — Minimal Trust Envelope Implementation remains locked.

**Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary is the
current implementation candidate; it is NOT locked.** Phase 13D.2 —
Static Demo Walkthrough / Reviewer Story Path — is locked and is the
last locked phase; Phase 12 — Portfolio / SE Demo Packaging — is
CLOSED.

## Active next phase

- **Phase 13 — Portfolio Website / Operator GUI — is STARTED.** Phase
  13A (architecture baseline), Phase 13B (typed static portfolio
  shell), Phase 13C (deterministic read-only static export / frontend
  data alignment), Phase 13D (operator workflow view expansion:
  Governance / Safety, Failure / Recovery), Phase 13D.1 (static
  operator GUI refinement / Evidence & Disabled Action Discipline),
  Phase 13D.2 (static demo walkthrough / reviewer story path), and
  Phase 13E (Demo-Mode Action Preview / Operator Intent Boundary) are
  all locked. Phase 13F — Local Bridge Architecture & Contract
  Baseline — is the current implementation candidate, pending review,
  not locked. Phase 13F is a documentation-and-static-fixture
  architecture / contract baseline (no runtime code): eleven new
  architecture docs, a set of non-runtime JSON example fixtures under
  `docs/examples/`, and one new Python contract-examples test. It
  establishes that the frontend is an operator surface — not the
  durable storage layer — and that durable state must live outside
  the browser in an explicit workspace / storage target, so StoryTime
  never repeats the RoundTable browser-storage failure mode; it
  settles the future local-bridge security boundary (loopback-only,
  strict origin, no arbitrary command, command-pattern router,
  action allowlist), the execution-timing policy (async long-running
  actions, `202 Accepted` + `actionRequestId`/`jobId`, acceptance is
  not success, export refresh after a durable write), and the
  queue-observability model. Nothing is implemented: no bridge, no
  server, no async queue, no workers, no metrics exporters, no storage
  providers, no real Local mode, no Cloud/Distributed mode, no
  mutation execution. See `docs/phase13-roadmap.md`,
  `docs/phase13f-local-bridge-contract-readiness.md`, and
  `docs/frontend-gui-deferred-work-register.md`.
- **Phase 13G and every later Phase 13 subphase have not started.**
  They are future, planned work only; the recommended next phase is a
  minimal, gated Local Bridge implementation (Phase 13G) against the
  Phase 13F contract, with Portfolio Website Polish / Public Demo
  Packaging and Deployment / Hosting Readiness as later subphases —
  each after its own review gate. Phase 13G is **not** started. See
  `docs/phase13-roadmap.md` and
  `docs/phase13f-local-bridge-contract-readiness.md`.
- **Phase 12E was not created.** It was optional, contingency-only
  work that would have existed only if the Phase 12D review found a
  substantive packaging gap; the review found none, so Phase 12
  closed after Phase 12D and no Phase 12E exists.
- Do not mark Phase 13F locked, do not mark Phase 13 closed or
  complete, and do not begin Phase 13G or any real bridge / mutation /
  execution work without the Phase Closure Protocol and an explicit
  gate. The immediate next action is the Phase 13F review gate:
  GPT-5.5 review, then Gemini critique, then an explicit user
  decision on whether to lock Phase 13F.

## Current artifact lineage

- Latest archive (implementation candidate — Phase 13F): `storytime-phase13f-local-bridge-architecture-contract-baseline.tar.gz`
  — the Phase 13F — Local Bridge Architecture & Contract Baseline
  candidate: a documentation-and-static-fixture architecture / contract
  baseline (the architectural lock before any Python local-bridge
  implementation is allowed). It adds eleven new architecture / contract
  docs (`docs/local-bridge-architecture.md` including the execution-timing
  policy and risk table, `docs/externalized-state-architecture.md`,
  `docs/browser-storage-policy.md`, `docs/local-mode-workspace-layout.md`,
  `docs/storage-targets-architecture.md`,
  `docs/action-execution-boundary.md`, `docs/local-action-dto-spec.md`,
  `docs/local-action-audit-spec.md`, `docs/local-mode-storage-contract.md`,
  `docs/local-action-queue-observability.md`, and
  `docs/phase13f-local-bridge-contract-readiness.md`); a set of non-runtime
  JSON example fixtures under `docs/examples/` (local-action-requests,
  local-action-responses, local-action-audit-records) labelled as
  future / documentation-only; one new Python test
  (`tests/test_local_mode_contract_examples.py`) validating those fixtures
  with plain Python (no JSON-schema dependency); the state-discipline guard
  advanced under the explicitly authorized mechanical exception; and the
  State Preservation Bundle synchronized. The central principle: the
  frontend is an operator surface, not the durable storage layer — durable
  state lives outside the browser in an explicit workspace / storage
  target, so StoryTime never repeats the RoundTable browser-storage failure
  mode. Nothing is implemented at runtime: no local bridge, no server, no
  async queue, no workers, no queue metrics / exporters, no OpenTelemetry,
  no storage providers, no provider integrations, no runtime schema
  validation, no router / history, no browser storage, no real Local mode,
  no Cloud/Distributed mode, no mutation / action execution; the browser
  remains non-durable. `src/`, `frontend/src/` (including
  `frontend/src/data/storytime-demo-export.json`), `frontend/package.json`,
  `frontend/package-lock.json`, `pyproject.toml`, and `uv.lock` are
  byte-identical to the locked Phase 13E source. Implementation candidate,
  pending review, **not locked**. sha256 reported on delivery.
- Source / base archive (locked — Phase 13E): `storytime-phase13e-demo-mode-action-preview-operator-intent-boundary.tar.gz`
  — the locked Phase 13E — Demo-Mode Action Preview / Operator Intent
  Boundary lineage: a static view-model adapter
  (`frontend/src/data/actionPreviewAdapter.ts`) holding action-preview
  definitions (stable id, label, category, current mode (Demo),
  execution status (Preview only / non-consequential), target object
  references, what the operator is trying to accomplish, why it is
  blocked in Demo mode, precondition checklist, evidence to inspect,
  risk level and explanation, illustrative future Local-mode request
  shape, Cloud/Distributed considerations, audit expectations,
  failure behaviour expectation, what remains disabled, related
  view) and the operating-mode model (Demo / Local / Cloud-Distributed)
  distinct from the Demo / Active / Candidate snapshot framing; a
  presentation panel (`frontend/src/components/ActionPreviewPanel.tsx`
  and its CSS Module) integrated **alongside** the unchanged
  `DisabledFutureActionCard` (a real `<button disabled={true}>` with no
  `onClick`) on the Failure / Recovery, Governance / Safety, and
  Evidence / Validation views via a separate, clearly-labelled "Preview
  action plan" control — the preview never looks like execution and
  renders no fake success state; a `tests/test_action_preview_data_integrity.py`
  asserting the run-id and other target ids referenced by the
  action-preview adapter exist in the committed static export.
  `src/storytime/operator_export.py`, the committed static export
  JSON, the `storytime export-demo-ui` contract, and
  `src/storytime/cli/app.py` were byte-identical to the Phase 13D.2
  source. **Phase 13E is locked**; it is the source/base artifact for
  Phase 13F. sha256
  `a997f2ca9d213e28e140f47c63336367c8feda46ed994b41300f86b99f8d8164`.
- Prior archive (locked — Phase 13D.2): `storytime-phase13d2-static-demo-walkthrough-reviewer-story-path.tar.gz`
  — the locked Phase 13D.2 — Static Demo Walkthrough / Reviewer Story
  Path lineage: the real read-only Demo Walkthrough view and its CSS
  Module, the static `demoWalkthroughAdapter.ts` holding the four
  reviewer routes (5-minute scan, 10-minute SE-style demo, technical
  deep-dive, self-guided reviewer), eight embedded
  architecture-checkpoint cards absorbing ~80–90% of an Architecture
  Story narrative, a "what is intentionally deferred" section, and
  interview / SE talking-point callout cards. Promoted Demo
  Walkthrough to a real view in `navigation.ts`; rendered the new
  view in `App.tsx` with navigation callbacks. No `src/`,
  `pyproject.toml`, `uv.lock`, `frontend/package.json`,
  `frontend/package-lock.json`, or root dependency changed;
  `src/storytime/operator_export.py`,
  `frontend/src/data/storytime-demo-export.json`, the `storytime
  export-demo-ui` contract, and `src/storytime/cli/app.py` were
  byte-identical to the Phase 13D.1 source. **Phase 13D.2 is
  locked**; it is the source/base artifact for Phase 13E. sha256
  `cd553679ce109483b69e99f51fceab34af216c9b1ce7dfe859fc7b78c13cd429`.
- Prior archive (locked — Phase 13D.1): `storytime-phase13d1-static-operator-gui-refinement-evidence-disabled-actions.tar.gz`
  — the locked Phase 13D.1 — Static Operator GUI Refinement / Evidence
  & Disabled Action Discipline lineage: the reusable disabled
  future-action component pair, the refactored Governance / Safety and
  Failure / Recovery views, the real Evidence / Validation view
  carrying the mandatory STATIC PORTFOLIO DATA disclaimer and
  repository-relative evidence references, the evidence adapter, and
  the navigation-metadata extraction (`App.tsx` slimmed from 228 to
  136 lines). No `src/`, `pyproject.toml`, `uv.lock`,
  `frontend/package.json`, `frontend/package-lock.json`, or root
  dependency changed; `src/storytime/operator_export.py`,
  `frontend/src/data/storytime-demo-export.json`, the `storytime
  export-demo-ui` contract, and `src/storytime/cli/app.py` were
  byte-identical to the Phase 13D source. **Phase 13D.1 is locked**;
  it is the source/base artifact for Phase 13D.2. sha256
  `812841381075e0e7839266512eb6d7f41bf2d890ee4c82b91627ce824f5b1eae`.
- Prior archive (locked — Phase 13D): `storytime-phase13d-operator-workflow-view-expansion-governance-failure.tar.gz`
  — the locked Phase 13D — Operator Workflow View Expansion (Governance
  / Safety, Failure / Recovery) lineage: two new view components and
  their CSS Modules
  (`frontend/src/components/GovernanceSafetyView.tsx` /
  `GovernanceSafetyView.module.css` and
  `frontend/src/components/FailureRecoveryView.tsx` /
  `FailureRecoveryView.module.css`), two domain-specific view-model
  adapters (`frontend/src/data/governanceAdapter.ts` and
  `frontend/src/data/failureAdapter.ts`) projecting the locked Phase
  13C export, an ambient CSS-Modules TypeScript declaration
  (`frontend/src/types/css-modules.d.ts`), App-level navigation
  rewiring with a "Data source · Demo Snapshot" header chip and an
  inspect-this-run drill-down into the existing Pipeline Run Detail
  view, and a small `.data-chip` rule in the shared global stylesheet
  (the only global addition). No `src/`, `pyproject.toml`, `uv.lock`,
  or root dependency changed; `src/storytime/operator_export.py`,
  `frontend/src/data/storytime-demo-export.json`, and the `storytime
  export-demo-ui` contract were byte-identical to the Phase 13C
  source. **Phase 13D is locked**; it is the source/base artifact for
  Phase 13D.1. sha256
  `5ec0b1edaaedfed2f3ae9b3e221e6a9089c52b8df152c4824503e7ca796894f3`.
- Prior archive (locked — Phase 13C): `storytime-phase13c-deterministic-read-only-static-export-frontend-data-alignment.tar.gz`
  — the locked Phase 13C — Deterministic Read-Only Static Export / Frontend
  Data Alignment lineage: a new read-only backend export module
  (`src/storytime/operator_export.py`) and `storytime export-demo-ui` CLI
  command producing the deterministic static JSON export
  (`frontend/src/data/storytime-demo-export.json`, top-level `schemaVersion`
  `"1.0"`), the export contract document, the frontend deferred-work
  register, the frontend adapter and `StaticDemoExport` type, backend
  contract tests, and the rewired homepage and Pipeline Run Detail / Stage
  Timeline. No core pipeline runtime behaviour and no root dependency
  changed. **Phase 13C is locked**; this is the source/base artifact for
  Phase 13D. sha256
  `1c24cf03283590d7f095d3805bc8f5d560e3583131c04e5be0359e0053145507`.
- Prior archive (locked — Phase 13B): `storytime-phase13b-typed-static-portfolio-shell-minimal-visual-pipeline-scaffold.tar.gz`
  — the locked Phase 13B — Typed Static Portfolio Shell / Minimal Visual
  Pipeline Scaffold lineage: a new top-level `frontend/` directory (a React +
  TypeScript + Vite project — the frontend read-model contract, a static demo
  dataset, the portfolio homepage, one Pipeline Run Detail view with a Stage
  Timeline, placeholders, and a frontend README), the state-discipline guard
  advanced, a light `README.md` update, and the State Preservation Bundle
  synchronized. No backend source code, dependencies, lockfile, or product
  behaviour changed. **Phase 13B is locked**; it was the source/base artifact
  for Phase 13C. sha256
  `9319ece26f5b457ddbbefaab346aba61cb61f65a6b7b729b5acaa12f30df3f24`.
- Prior archive (locked — Phase 13A): `storytime-phase13a-portfolio-website-operator-gui-architecture-baseline.tar.gz`
  — the locked Phase 13A — Portfolio Website / Operator GUI Architecture
  Baseline lineage: five architecture-baseline `docs/` documents added, the
  state-discipline guard advanced, and the State Preservation Bundle
  synchronized. No source code, dependencies, lockfile, frontend / UI code, or
  product behaviour changed. **Phase 13A is locked**. sha256
  `100098aa6280b740a6eeb862c1e1923d2e031bd02a06786b7a8b8ec07facf1c0`.
- Prior archive (locked — Phase 12D): `storytime-phase12d-phase12-closure-plan-final-portfolio-handoff.tar.gz`
  — the locked Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff
  Definition lineage: three closure-definition `docs/` documents added
  (`docs/phase12-closure-plan.md`, `docs/final-portfolio-handoff.md`,
  `docs/phase12-final-review-checklist.md`), the state-discipline guard
  advanced, a light README reviewer-pointer update, and the State Preservation
  Bundle synchronized. No source code, dependencies, lockfile, or product
  behaviour changed. **Phase 12D is locked and Phase 12 is CLOSED**. sha256
  `64ad09e875f0653608e0deb756f11ee5adc0d2ff1265e2039cbc51491f286cf8`.
- Prior archive (locked — Phase 12C): `storytime-phase12c-portfolio-demo-narrative-public-presentation-kit.tar.gz`
  — the locked Phase 12C — Portfolio Demo Narrative / Public Presentation Kit
  lineage: four public-presentation `docs/` documents
  (`docs/portfolio-demo-narrative.md`, `docs/demo-talk-track.md`,
  `docs/interview-story-bank.md`, `docs/public-repository-readiness.md`), a
  light README reviewer-pointer refinement, the authorized state-discipline
  guard advance, and the synchronized State Preservation Bundle. No `src/`,
  `tests/` (beyond the guard), dependency, lockfile, or product behaviour
  change. **Phase 12C is locked**; this is the source/base artifact for
  Phase 12D. sha256 `4c98a25d6bb0ae751b4ba33851bc60e7d7805d4fd31ebcfc45c2d30a659301da`.
- Prior archive (Phase 12B sequence lineage, locked): `storytime-phase12b3-residual-state-wording-cleanup.tar.gz`
  — the locked Phase 12B — Portfolio Evidence Pack / Reviewer Assets lineage,
  with the accepted Phase 12B.1 state-hygiene cleanup, Phase 12B.2 Phase 13 GUI
  roadmap-preservation cleanup, and Phase 12B.3 residual living-doc
  state-wording cleanup sub-rounds folded in. No `src/`, `tests/`, dependency,
  lockfile, or product behaviour change beyond the documentation, README,
  state, and authorized state-discipline guard edits of the Phase 12B sequence.
  **Phase 12B is locked**; it was the source/base artifact for Phase 12C.
  sha256 `ce0fb2d1bea4eaa636be7796613f9a9aa56cba4b8bf34c0ae5440c3509de4a45`.
- Prior archive (Phase 12B implementation candidate, now locked): `storytime-phase12b-portfolio-evidence-pack-reviewer-assets.tar.gz`
  — the Phase 12B — Portfolio Evidence Pack / Reviewer Assets candidate: four
  reviewer/evidence `docs/` documents added (`docs/portfolio-evidence-index.md`,
  `docs/se-interview-evidence-matrix.md`, `docs/demo-reviewer-checklist.md`,
  `docs/portfolio-public-copy.md`), `README.md` lightly updated to point
  reviewers to them, the state-discipline guard
  `tests/test_failure_mode_regression.py` advanced under the explicitly
  authorized §5 mechanical exception to the Phase 12B current-state
  expectations, and the State Preservation Bundle synchronized. No source code,
  dependencies, lockfile, or product behaviour changed. **Phase 12B is now
  locked** (after the accepted Phase 12B.1 / 12B.2 / 12B.3 cleanup sub-rounds);
  superseded as the latest archive by the Phase 12B.3 cleanup lineage above.
  sha256 reported on delivery.

- Source / base archive (locked — Phase 12A lineage): `storytime-phase12a1-state-hygiene-cleanup.tar.gz`
  — the accepted Phase 12A.1 state-hygiene cleanup, folded into the locked
  Phase 12A — Portfolio / SE Demo Packaging Baseline lineage. It was a bounded,
  documentation-only state-hygiene cleanup of the Phase 12A round (stale
  present-tense phrasing in the living documents revised to read as superseded
  point-in-time records). No `src/`, `tests/`, dependency, lockfile, or product
  behaviour change. **Phase 12A is locked**; this is the source/base artifact
  for Phase 12B. sha256 `5f9eca1cc8c2efb55d57f87becdc53cd0d8e514221947e445965232f608b621a`.
- Prior archive (Phase 12A implementation candidate, now locked): `storytime-phase12a-portfolio-se-demo-packaging-baseline.tar.gz`
  — the Phase 12A — Portfolio / SE Demo Packaging Baseline candidate: four
  portfolio `docs/` documents added (`docs/portfolio-overview.md`,
  `docs/solutions-engineer-narrative.md`, `docs/portfolio-demo-script.md`,
  `docs/interview-talking-points.md`), `README.md` refined for a
  portfolio-facing reviewer, the state-discipline guard
  `tests/test_failure_mode_regression.py` advanced under explicit authorization
  to the Phase 12A current-state expectations, and the State Preservation
  Bundle synchronized. No source code, dependencies, lockfile, or product
  behaviour changed. **Phase 12A is now locked** (after the accepted Phase
  12A.1 cleanup);
  superseded as the latest archive by the Phase 12A.1 state-hygiene cleanup
  above. sha256 `54909ee9da9ea20c0a416de733e2a7d1e1b4722ef3799e21c374698be778ffaa`.
- Last locked phase artifact: `storytime-phase11d-release-candidate-evidence-pack.tar.gz`
  — the locked Phase 11D — Release Candidate Evidence Pack artifact: four
  release-candidate evidence `docs/` documents and the synchronized State
  Preservation Bundle. No source code, tests, dependencies, or product
  behaviour changed. It is the source/base artifact for Phase 12A and, with it
  locked, **Phase 11 — Release Candidate Hardening — is CLOSED**. sha256
  `07a3973e3dbb69d760ff2c330418f85101c2afa1464fc0eed752fc7053894d94`.
- Prior archive (locked, Phase 11C): `storytime-phase11c-failure-mode-regression-hardening.tar.gz`
  — the locked Phase 11C — Failure-Mode / Regression Hardening artifact: four
  failure-mode / regression documents added
  (`docs/failure-mode-regression-hardening.md`,
  `docs/regression-risk-register.md`, `docs/failure-mode-test-matrix.md`,
  `docs/operator-failure-response.md`), one focused regression test module
  added (`tests/test_failure_mode_regression.py`, the state-documentation
  discipline guard), and the State Preservation Bundle synchronized. No source
  code, dependencies, or product behaviour changed; the only `tests/` change
  was the new regression module. Locked under the Phase Closure Protocol; it is
  the third subphase of Phase 11. sha256
  `2dd31442e62c13241a64d10c2d117aefedc3b9c633ad5ea5d1fa94cfaad7d57b`.
- Last locked phase artifact: `storytime-phase11b-fresh-clone-operator-reproducibility.tar.gz`
  — the locked Phase 11B — Fresh Clone / Operator Reproducibility artifact: two
  reproducibility documents added and the State Preservation Bundle
  synchronized. No source code, tests, dependencies, or product behaviour
  changed. It is the source/base artifact for Phase 11C. sha256
  `08b72f2833da9adf3b8acc1f3170334eb7c5f998e19263838efbce2f571cc73f`.
- Prior locked phase artifact: `storytime-phase11a-release-candidate-hardening-baseline.tar.gz`
  — the locked Phase 11A — Release Candidate Hardening Baseline artifact: seven
  `docs/` hardening documents added and the State Preservation Bundle
  synchronized. No source code, tests, dependencies, or product behaviour
  changed. sha256
  `664f8ba4ae90cf6a98ccc7d20369e690eac74497ab78f2b7067f0aac2079a7aa`.
- Last locked work item artifact before Phase 11: `storytime-post-phase10-roundtable-historical-backfill.tar.gz`
  — the Post-Phase-10 Historical State Reconciliation artifact (the RoundTable
  JSON historical backfill into the historical living docs). Documentation/
  state-history only; no current state or product behaviour changed. sha256
  `367e647c46aa6e4fd039369da30859b11ca783249569df291343db133ef4cfdd`.
- Prior archive (state synchronization): `storytime-post-phase10-closure-state-sync.tar.gz`
  — the Post-Phase-10 Closure State Synchronization artifact: the State
  Preservation Bundle first-read docs synchronized to record the already-
  approved Phase 10G lock and Phase 10 closure. No source code, tests,
  dependencies, or product behaviour changed. sha256
  `5b309bb171ceea9380367c346945d20c67b242f42547902d9619668a27a804c1`.
- Prior locked phase artifact: `storytime-phase10g1-uvlock-reversion-cleanup.tar.gz`
  — the locked Phase 10G artifact (the Phase 10G.1 `uv.lock` reversion cleanup
  of the Phase 10G portfolio/closure documentation); with Phase 10G locked,
  Phase 10 is CLOSED. sha256
  `8a0cc9a5b6426a291bec3a793e41501c7d3492187dd48b4f7729ea95e501a0c1`.
- Prior archive (superseded historical): `storytime-phase10g-portfolio-narrative-phase10-closure.tar.gz`
  — the original Phase 10G implementation-candidate archive, superseded by the
  Phase 10G.1 cleanup above. It introduced the Phase 10 portfolio/closure
  documents (`docs/portfolio-narrative.md`, `docs/demo-script.md`,
  `docs/operator-experience-walkthrough.md`, `docs/command-reference.md`,
  `docs/known-limitations.md`,
  `docs/observability-governance-talking-points.md`,
  `docs/phase10-acceptance-checklist.md`, `docs/screenshot-instructions.md`)
  and the synchronized State Preservation Bundle. sha256
  `f3c21b9e21ee22e263d61ffad04642e9e9a604e1508aa1cbd54fc6781cb245fe`.
- Prior archive (locked): `storytime-phase10f-demo-seed-data-golden-path-fixtures.tar.gz`
  — the Phase 10F lock archive: the `demo/` seed data and golden-path
  fixtures, `docs/demo.md`, and `tests/test_demo_fixtures.py`. sha256
  `e060570a94fb19f790c539542b3ef7445111430bc308668675548f66fa48df55`.
- Prior archive (locked): `storytime-phase10e2-final-cleanup-v2-normalized.tar.gz`
  — the Phase 10E lock archive: Phase 10E with the 10E.1 / 10E.2 cleanup
  sequence, normalized cleanup canonical. sha256
  `87fad92b2e0a919a81588f4c628ccfdf08860571fdc778c527d8fe93c30b7dec`.
- Prior archive: `storytime-phase10e2-final-cleanup-v2.tar.gz`
  — the Phase 10E.2 final cleanup: render.py full-phrase redaction fix,
  state-preservation sync. sha256 reported on delivery.
- Prior archive: `storytime-phase10e1-cleanup.tar.gz`
  — the Phase 10E.1 cleanup (superseded by Phase 10E.2). sha256 reported on delivery.
- Prior archive (implementation candidate): `storytime-phase10e-static-html-operator-report-refinement.tar.gz`
  — the Phase 10E implementation candidate: refined static HTML operator report.
  sha256 `ceb3e9d08057a1c7ff2e83ea7ef0520ff80f9258bac84d33f7ec42fdf75e05b6`.
- Prior archive (locked): `storytime-phase10d1-state-preservation-cleanup.tar.gz`
  — the Phase 10D.1 state-preservation cleanup + LLM director hardening. sha256
  `98d0884310281f0ea63a1bc7477ed597587f5bcd975724a62a9e6c4df8748765`.
- Prior archive (locked): `storytime-phase10d-pipeline-rerun-mutation-actions.tar.gz`
  — the Phase 10D implementation candidate: the `storytime.operator_rerun`
  module, the `storytime rerun` CLI command, the `RUN_RERUN_REQUESTED` audit
  event type, `tests/test_operator_rerun.py`, `docs/operator-rerun.md`, and the
  State Preservation Bundle updated to record Phase 10D as a pending-review
  candidate. sha256 `479ce122992efe05ed8494619a60f7464952f744e0b351164b54208042a21a16`.
- Prior archive (locked): `storytime-phase10c1-state-preservation-sync.tar.gz`
  — the Phase 10C.1 state-preservation cleanup. sha256
  `ac2f56ed6ba22f0f00aee8f0caaaac0154ac02eef16b20d08b9d4e2addb67c9a`.
- Prior archive (locked): `storytime-phase10c-operator-cli-helpers-failure-queue.tar.gz`
  — the Phase 10C locked archive: the `storytime.operator_queue` module and
  the read-only `storytime queue` CLI command. sha256
  `e30aaa57f900756e62347ddaac2df658d96065c9e1061679adb31594c73e2543`.
- Prior archive (locked): `storytime-phase10b-locked-state-bundle.tar.gz`
  — the Phase 10B lock-closure archive. sha256
  `00e6d543ce334fb8be83448f3397510761568af7d4318ab8df4b9bc6ca0e0c59`
  (corrected bundle).
- Prior archive (locked): `storytime-phase10a-locked-state-bundle.tar.gz`
  — the Phase 10A locked-state bundle: Architecture Baseline Section 25
  canonical operator-experience law.
- Full lineage and sha256 values: `docs/artifact-manifest.md`.

## Required next action

1. **Phase 13C — Deterministic Read-Only Static Export / Frontend Data
   Alignment — is an implementation candidate.** Submit the Phase 13C artifact
   (`storytime-phase13c-deterministic-read-only-static-export-frontend-data-alignment.tar.gz`)
   for GPT-5.5 review and Gemini critique under the Phase Closure Protocol,
   then an explicit user decision — before locking Phase 13C or starting
   Phase 13D. See `docs/phase13-roadmap.md` for the Phase 13 review gates and
   `docs/frontend-static-export-contract.md` for the export contract under
   review.
2. Do not mark Phase 13C locked, do not mark Phase 13 closed or complete, and
   do not begin Phase 13D (or any later Phase 13 subphase, or any further
   frontend / operator-GUI view expansion) without the Phase Closure Protocol
   and an explicit gate. Phase 13C is a deterministic, read-only static data
   boundary; the frontend remains static, read-only, and demo/export-backed —
   it is not backend-connected, uses no live data, implements no mutations, and
   is not production-hosted. `docs/frontend-static-export-contract.md`,
   `docs/frontend-backend-contract.md`, and `docs/phase13-roadmap.md` are the
   reviewer entry points for Phase 13C.
3. Do not re-open or re-review any locked phase (0–7D.1, 8A, 8B / 8B.1,
   8C / 8C.1, 9A, 9B with 9B.1, 10A–10G, 11A, 11B, 11C, 11D, 12A, 12B, 12C,
   12D, 13A, 13B), and do not re-run the Post-Phase-10 Historical State
   Reconciliation or re-import the RoundTable JSON. Those are closed or locked;
   Phase 10, Phase 11, and Phase 12 are all closed and Phase 12A through 12D
   and Phase 13A and 13B are locked.

## What not to replay

- Do **not** replay stale or superseded RoundTable rounds. RoundTable
  prompt/state generation was contaminated during the Phase 7 sequence.
- RoundTable should resume from **this repository state**, not from stale
  Round 21–23 prompt text.
- Treat phases 0–7D.1 as already locked — do not re-open, re-implement, or
  re-review them. Phase 7 is closed.

## Which docs are canonical

- Locked decisions: `docs/canonical-state.md` (append-only).
- Round history: `docs/phase-history.md` (append-only).
- Current status: this file, `docs/handoff-state.md`.
- Roadmap / routing / gates: `docs/roadmap.md`.
- RoundTable reconstruction: `docs/roundtable-import-bridge.md`.
- Verification evidence: `docs/verification-log.md`.
- Artifact lineage: `docs/artifact-manifest.md`.
- Operator report: `docs/operator-report.md` (how to generate the Phase 10B
  operator report; what it includes and excludes).
- Operator queue: `docs/operator-queue.md` (how to use the Phase 10C
  `storytime queue` failure/review queue; what it surfaces and excludes).
- Operator demo: `docs/demo.md` (the operator demo runbook; how to
  demonstrate the pipeline, report, queue, governance, and re-run with the
  `demo/` seed data and golden-path fixtures) and `docs/demo-script.md` (the
  Phase 10G presentation demo script).
- Portfolio / Phase 10 closure: `docs/portfolio-narrative.md`,
  `docs/operator-experience-walkthrough.md`, `docs/command-reference.md`,
  `docs/known-limitations.md`,
  `docs/observability-governance-talking-points.md`,
  `docs/phase10-acceptance-checklist.md`, and `docs/screenshot-instructions.md`
  (the Phase 10G closure documents).
- Portfolio / SE demo packaging (Phase 12A): `docs/portfolio-overview.md` (the
  plain-English portfolio overview and reviewer entry point),
  `docs/solutions-engineer-narrative.md` (interview and SE framings),
  `docs/portfolio-demo-script.md` (a reviewer-facing demo walkthrough), and
  `docs/interview-talking-points.md` (concise study points).
- Release-candidate hardening (Phase 11A), fresh-clone / operator
  reproducibility (Phase 11B), and failure-mode / regression hardening
  (Phase 11C): `docs/release-candidate-hardening.md`
  (the hardening baseline overview), `docs/phase11-plan.md` (the Phase 11
  subphase decomposition), `docs/local-setup-runbook.md`,
  `docs/fresh-clone-checklist.md`, `docs/operator-reproducibility-checklist.md`
  (the step-by-step verification path), `docs/fresh-clone-troubleshooting.md`
  (common setup failures), `docs/rc-validation-checklist.md`,
  `docs/security-secrets-checklist.md`,
  `docs/demo-reproducibility-checklist.md`,
  `docs/failure-mode-regression-hardening.md` (the Phase 11C overview),
  `docs/regression-risk-register.md` (the failure / regression risk
  inventory), `docs/failure-mode-test-matrix.md` (the regression coverage
  map), and `docs/operator-failure-response.md` (the operator failure-response
  playbook).
- Architecture: `docs/architecture-baseline.md` (Phase 1 + the locked §16,
  §23, §24, and §25 amendments — §24 is the Phase 9A Governance Baseline and
  §25 is the Phase 10A Operator Experience Baseline, both locked and
  canonical).
- Portfolio Website / Operator GUI architecture baseline (Phase 13A):
  `docs/phase13-portfolio-website-architecture.md` (the Phase 13 purpose, the
  end-state website and operator-GUI vision, audiences and review paths, the
  website and operator information architectures, and the Phase 13 success
  criteria), `docs/frontend-backend-contract.md` (the frontend / backend data
  contract — read-model categories, future action categories, the actions
  disabled in Phase 13A, and candidate data-source options),
  `docs/phase13-roadmap.md` (the Phase 13A–13G subphase decomposition),
  `docs/portfolio-website-content-model.md` (the website section inventory
  mapped to existing repository source documents), and
  `docs/operator-gui-view-model.md` (the operator-GUI view inventory and
  states). These five documents are the authoritative Phase 13 plan;
  `docs/GUI_vision.md` remains the original verbatim vision capture and is
  superseded by them for planning purposes.

## Known RoundTable desync / recovery notes

- RoundTable prompt/state generation became contaminated during Phase 7. Until
  RoundTable is restored, the repository State Preservation Bundle is the
  portable project memory.
- If RoundTable state is lost, stale, or contaminated, reconstruct it from
  `docs/roundtable-import-bridge.md`. Prefer this repository's Bundle over
  RoundTable if the Bundle holds a newer explicit recovery checkpoint — and it
  does: this checkpoint records Phase 8A, Phase 8B / 8B.1, Phase 8C / 8C.1,
  Phase 9A, **Phase 9B (with Phase 9B.1 folded in), Phase 10A through 10G,
  Phase 11A through 11D, and Phase 12A through 12D all locked**, with
  **Phase 10 — Product UI / Operator Experience — formally CLOSED**, **Phase 11
  — Release Candidate Hardening — formally CLOSED**, and **Phase 12 —
  Portfolio / SE Demo Packaging — formally CLOSED**, the **Post-Phase-10
  Historical State Reconciliation** as the last locked work item before
  Phase 11 (artifact
  `storytime-post-phase10-roundtable-historical-backfill.tar.gz`, SHA-256
  `367e647c46aa6e4fd039369da30859b11ca783249569df291343db133ef4cfdd`), and
  **Phase 13 — Portfolio Website / Operator GUI — STARTED, with Phase 12D —
  Phase 12 Closure Plan / Final Portfolio Handoff Definition — locked (the last
  locked phase; the accepted Phase 12A.1 and Phase 12B.1 / 12B.2 / 12B.3
  cleanup sub-rounds are folded into the Phase 12A and Phase 12B lock
  lineages), and Phase 13A — Portfolio Website / Operator GUI Architecture
  Baseline — an implementation candidate pending review, not locked**.
  Phase 13 is not closed. Phase 13B and every later Phase 13 subphase have not
  started — they are future, planned work only. Phase 12E was optional,
  contingency-only work that was not needed and never started. The locked
  Phase 12D artifact is
  `storytime-phase12d-phase12-closure-plan-final-portfolio-handoff.tar.gz`
  (SHA-256 `64ad09e875f0653608e0deb756f11ee5adc0d2ff1265e2039cbc51491f286cf8`);
  the locked Phase 11D artifact is
  `storytime-phase11d-release-candidate-evidence-pack.tar.gz`
  (SHA-256 `07a3973e3dbb69d760ff2c330418f85101c2afa1464fc0eed752fc7053894d94`).
  `docs/architecture-baseline.md` Section 24 (governance) and Section 25
  (operator experience) are both locked and canonical.
- The Phase 7D.1 live Docker smoke test (Windows Docker Desktop / WSL2) passed;
  evidence is in `docs/verification-log.md`.

## Standing carryover

- OI-15 — `storytime clean` retention policy — still unimplemented; tracked in
  `docs/open-issues.md`. Independent of the deployment track; not a Phase 8
  prerequisite.

## Environment notes for the next implementer

- Toolchain: `uv` (dependencies pinned in `uv.lock`); Python ≥ 3.11, developed
  and tested on 3.12.
- The six quality gates are Docker-free and must stay Docker-free.
- Docker is NOT available in the Claude Opus implementation environment;
  container builds/runs are validated as data plus user-run live smoke tests.
  Do not claim live Docker validation that was not performed.
- Bare-metal local Python is the default supported mode; Docker is optional.
