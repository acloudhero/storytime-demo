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

# Phase History

A short, factual record of how StoryTime reached this scaffold. The detailed
canonical record is RoundTable canonical state.

| Round | Date | Outcome |
|-------|------|---------|
| 1 | 2026-05-21 | Legacy artifacts must be ratified natively through Phase 0/1; RoundTable history becomes the source of truth. |
| 2 | 2026-05-21 | Project renamed StoryTime (from "Podcast Pipeline"). Phase 0/1 native ratification basis accepted; eleven hard decisions stated. |
| 3 | 2026-05-21 | Canonical docs to be generated one at a time, not as one mega-prompt. DTO-vs-context model carried forward. |
| 4 | 2026-05-21 | Phase 0 Product Charter generated, patched (sections 14-15), and **locked**. |
| 5 | 2026-05-22 | Phase 1 Architecture Baseline generated by Claude Opus 4.7, reviewed, and **locked**. Clarifications A1/A2 accepted. |
| 6 | 2026-05-22 | Phase Closure Protocol generated, reviewed, and **locked**. |
| 7 | 2026-05-22 | Phase 2 prerequisites resolved; high-assurance route chosen (Opus 4.7 builds the scaffold). Ten prerequisite corrections accepted. |
| 8 | 2026-05-22 | Phase 2 repository scaffold + local development environment built by Claude Opus 4.7. |
| 9 | 2026-05-22 | Phase 3 thin vertical slice implemented: ingest → synthesize → assemble → publish, persisted to SQLite, with the per-stage CLI commands kept visible but intentionally deferred (OI-12). |
| 10 | 2026-05-22 | Phase 4 deep implementation by Claude Opus 4.7: persisted interactive approval gate (OI-9), resume/rehydration of a paused run from SQLite (OI-10), and real per-stage CLI commands (OI-12). |
| 11 | 2026-05-22 | Phase 4.1 cleanup/hardening by Claude Opus 4.7: event-taxonomy cleanup — ingest now emits `SourceManifestApproved`, distinct from the operator gate's `TextApproved` (OI-14); audio approval gate wired between `synthesize` and `assemble` with `--require-audio-approval` and `approve --stage audio` (OI-13); trace-link attach points preserved and the exact remaining OI-2 work documented (no fake implementation). |
| 12 | 2026-05-23 | Phase 5 OpenTelemetry instrumentation foundation by Claude Opus 4.7: the pipeline is observability-native. One `pipeline.run` span per run with child `pipeline.stage.<name>` spans; each stage's span `traceparent` is stamped into its artifact envelopes; a resumed run is a fresh `pipeline.resume` trace carrying a W3C `Link` to the pre-pause trace; a closed metric set over a `MeterProvider`; a single data-hygiene choke point redacting absolute paths. OI-2 (trace-link propagation) closed with a genuine implementation. OpenTelemetry stays confined to one adapter module; `NoopTelemetry` remains the default and every functional test passes on it. |
| 13 | 2026-05-23 | Phase 6S deep implementation by Claude Opus 4.7 (range-capable serving + multi-item feed): StoryTime can serve real episodes. OI-7 closed — a loopback-only, range-capable HTTP server (`RangeFileHandler` + `storytime serve`) honours HTTP byte ranges through the pure `parse_byte_range`, answering `206`/`416`/`200` correctly and refusing path traversal. OI-11 closed — `publish` builds a multi-item RSS feed by aggregating prior episodes from an injected, read-only `EpisodeCatalog`; migration `0004` adds `published_episode.description` for faithful regeneration; `feed_version` becomes a real monotonic counter; the feed is validated and swapped in atomically. An out-of-band execution (see "Phase 6S provenance" below); reviewed post-implementation by GPT-5.5 and Gemini 3 Thinking and **accepted by the user as Phase 6S**. |
| 13 | 2026-05-23 | Phase 6A deep implementation by Claude Opus 4.7 (Observability Infrastructure, Dashboards-as-Code, Demo Harness): StoryTime's telemetry is now visible. The OpenTelemetry Collector gains a metrics pipeline feeding a Prometheus the `docker-compose.observability.yml` stack now includes alongside a provisioned Grafana; six dashboards-as-code chart only the eight real Phase 5 metrics; a bounded demo harness (`python -m storytime.demo`) drives real pipeline scenarios — success, text/audio approval pause-and-resume, text/audio rejection, bad manifest, artifact-validation failure — to populate that telemetry. No metric is invented; an automated test rejects any dashboard token that is not a real metric. |
| 13 | 2026-05-23 | Phase 6A documentation / source-of-truth cleanup before lock by Claude Opus 4.7: a bounded, docs-only round. `phase-history.md` gains the "Phase 6S provenance" section below; `canonical-state.md` is reclassified (Phase 6 → Phase 6S) and its stale "not yet phase-locked" status corrected; `open-issues.md` OI-7/OI-11 dispositions are relabelled Phase 6S and a post-MVP RSS re-publish-semantics carryover is recorded. No code, dashboards, Grafana JSON, Prometheus config, demo harness, or telemetry architecture were touched. Phase 6S and Phase 6A subsequently **locked**. |
| 14 | 2026-05-23 | Phase 6B documentation by Claude Opus 4.7 (SLO narrative, runbooks, demo walkthrough, documentation polish): a documentation-only phase turning Phase 6A's raw observability infrastructure into a portfolio-grade explanation. New docs: `slo-sli.md` (SLIs derived strictly from the eight real metrics, an illustrative demo-grade SLO model, and an honest account of what cannot be measured), `runbook.md` (operator + investigation procedures), `dashboard-guide.md` (per-panel interpretation), `portfolio-notes.md` (SE talking points). `observability-demo.md` was expanded from the short 6A guide into the full end-to-end walkthrough. No code, configuration, dashboards, telemetry instruments, or harness were changed; no SLO was invented beyond what the metrics support; no production-readiness claim was made. |
| 15 | 2026-05-23 | Phase 7A deep implementation by Claude Opus 4.7 (blue/green deployment, Option A — lean cloud-shaped demo path): the first blue/green-capable deployment path. `deployment_slot` now scopes the default state/feed roots to `runs/<slot>` / `feed/<slot>`, so blue and green get independent SQLite databases and feeds; the slot is validated as a safe path segment; an explicit `STORYTIME_RUNS_DIR`/`STORYTIME_FEED_DIR` override still wins. `config/deploy/blue.env` + `green.env` and `scripts/run-slot.sh` make the two slots runnable side by side on different loopback ports; `storytime doctor` prints a deployment-identity banner; `deployment.environment`/`deployment.slot` reach the OTel `Resource`. The application is deliberately **not** containerized — the Architecture Baseline §16 ARCH-LOCK is honoured; the Option A deployment unit is an uncontainerized per-slot process. No Kubernetes, no Terraform, no automated traffic cutover, no vendor fan-out — switching is an honest operator step, and the enterprise mechanics are deferred to Option B / Phase 7B. OI-17 closed. Local-first behaviour, `NoopTelemetry`-by-default, the OTel import boundary, and Phase 6 dashboards/harness are all unchanged. |
| 16-17 | 2026-05-23 | Phase 7B planning. GPT-5.5 and Gemini 3 Thinking reviewed the Option B planning; Round 17 consolidated it. Outcome: proceed with **Option B1** — keep the app uncontainerized, add a stable local front door and an active-slot switch/rollback around the Phase 7A per-slot processes. No Architecture Baseline amendment; B2 (app container), B3 (docs-only), and B4 (Kubernetes/Terraform) rejected or deferred. |
| 18 | 2026-05-23 | **This round.** Phase 7B deep implementation by Claude Opus 4.7 (blue/green Option B — higher-assurance front door / active-slot switching): a stable local entry point over the Phase 7A slots. A new `storytime.frontdoor` package provides a **native Python, loopback-only reverse proxy** — deliberately chosen over an external Caddy/nginx binary so the front door stays zero-dependency, fully testable in the normal suite, and inside the same ruff/mypy/import-linter discipline. It binds one stable port (default `127.0.0.1:8080`) and, on every request, routes to the slot named by a persisted **active-slot pointer** (`config/deploy/active-slot`); a switch updates that pointer atomically and takes effect with no proxy reload. `switch_active_slot` validates the target, confirms it is configured, writes only the pointer, and never touches `runs/`/`feed/` — rollback is the identical mechanism targeting the previous slot. `scripts/run-frontdoor.sh` + `scripts/switch-slot.sh` are the launchers (no binary install/download); `python -m storytime.frontdoor` exposes `serve`/`switch`/`status`. The front door relays `Range`/`206` faithfully, answers honest `502`/`503`, is outside the pipeline telemetry path, and imports no `opentelemetry` (import-linter contract extended). The app stays uncontainerized — Architecture Baseline §16 unamended, with a doc note that future containerization requires an explicit amendment. OI-18 closed. 42 new tests; all six gates green. Phase 7A slot identity, state/feed separation, `NoopTelemetry`-by-default, the OTel import boundary, and the Phase 6 dashboards/harness are all unchanged. |

## Phase 6S provenance

Phase 6S was an **out-of-band execution** caused by a user prompt-transfer /
copy-paste error during Round 13. The handoff to Claude Opus 4.7 carried the
canonical RoundTable history and the open-issues backlog, but **not** the
intended Phase 6A task block. Working from the backlog it did have, Opus
implemented the two top live carryover items — **OI-7** (range-capable HTTP
serving) and **OI-11** (multi-item RSS feed aggregation).

This was caught immediately after implementation. Phase 6S was then:

- **reviewed post-implementation** by GPT-5.5 and Gemini 3 Thinking;
- **sanitized of local runtime DB artifacts** (a stray `runs/state.db` left by
  the build environment was removed; it is runtime state, not source);
- **accepted by the user as a valid, reclassified phase — "Phase 6S" — not
  architectural drift.** The work is sound, well-tested, and consistent with
  the locked Architecture Baseline; only its *sequencing* was unintended.

**Phase 6A remained the intended Round 13 phase** — observability
infrastructure, dashboards-as-code, and the demo harness — and was implemented
afterward, on the accepted Phase 6S codebase so the deliverable stays
cumulative rather than forking. The numbering reflects this: 6S is the
out-of-band serving work; 6A is the intended observability work; 6B is the
planned SLO/runbook/demo-narrative phase.

This section exists so a future model reading the history understands that the
"6S" label denotes a reclassified out-of-band execution that was reviewed and
accepted — it does **not** denote unreviewed or rejected work, and it does not
denote a deviation from the Architecture Baseline.

## Current position

- Phase 0 — Product Charter: **locked**.
- Phase 1 — Architecture Baseline: **locked**.
- Phase Closure Protocol: **locked**.
- Phase 2 — Repo scaffold: implementation output produced.
- Phase 3 — Thin vertical slice: implementation output produced.
- Phase 4 — Approval gate + resume/rehydration: implementation output
  produced (Round 10).
- Phase 4.1 — Approval / event-taxonomy / trace-prep cleanup: implementation
  output produced (Round 11).
- Phase 5 — OpenTelemetry instrumentation foundation: implementation output
  produced (Round 12).
- Phase 6S — Range-capable serving + multi-item feed aggregation: reviewed,
  accepted as a reclassified phase, and **locked**. See "Phase 6S provenance"
  above.
- Phase 6A — Observability infrastructure, dashboards-as-code, demo harness:
  reviewed, docs-cleaned, and **locked**.
- Phase 6B — SLO narrative, runbooks, demo walkthrough, documentation polish:
  implementation output produced (Round 14, documentation-only).
- Phase 7A — Blue/green deployment, Option A (lean cloud-shaped demo path):
  implementation output produced (Round 15).
- Phase 7B — Blue/green deployment, Option B (higher-assurance front door /
  active-slot switching): **implementation output produced** (this round,
  Round 18). Per the Phase Closure Protocol, implementation output is not
  phase completion: Phase 7B closes only after review/critique and explicit
  user approval. `storytime clean` retention (OI-15) is the standing
  functional carryover, independent of the deployment track.
- Phase 7C / 7C.1 — Architecture Baseline amendment for optional local app
  containerization: Phase 7C authored the amendment candidate; Gemini reviewed
  it (SAFE WITH EDITS); Phase 7C.1 applied the four required edits and the
  amendment was **locked** with user approval.
- Phase 7C.1 / 7D — App containerization implementation: **implementation
  output produced** (this round). Delivered the `Dockerfile`, `.dockerignore`,
  and optional `docker-compose.app.yml`; a stable slot-derived
  `service.instance.id`; per-slot named volumes; loopback-only slot exposure;
  containerization config-as-data tests; and documentation. Bare-metal remains
  the default and the six gates remain Docker-free. Per the Phase Closure
  Protocol, implementation output is not phase completion: it closes only
  after review/critique and explicit user approval. `storytime clean`
  retention (OI-15) remains the standing functional carryover.
- Phase 7D.1 — App containerization operational cleanup: **implementation
  output produced** (this round). A bounded fix for the parallel
  `docker compose build` image-tag race in `docker-compose.app.yml` — both
  slot services had declared `build:` and exported the same `storytime-app:local`
  tag concurrently. The fix makes `storytime-blue` the sole builder and has
  `storytime-green` consume the same image with `pull_policy: never`, so
  `docker compose build` and a fresh-cache `docker compose up -d` both work
  without per-service targeting. No architecture changed: same one image, same
  loopback-only `network_mode: host`, same per-slot ports/volumes, same host
  front door. Five regression tests added. Per the Phase Closure Protocol this
  is implementation output, not phase completion.

## State Preservation Bundle round (2026-05-24)

A bounded, documentation-only round added the **State Preservation Bundle** so
the repository archive is portable project memory until RoundTable is
restored. Created `docs/roadmap.md`, `docs/handoff-state.md`,
`docs/verification-log.md`, `docs/artifact-manifest.md`, and
`docs/roundtable-import-bridge.md`; updated `README.md` (maturity table + a
bundle pointer) and this file. No code, configuration, tests, architecture,
deployment behavior, or telemetry behavior changed.

**Authoritative current status (supersedes stale status text above).** Locked:
phases 0, 1, Phase Closure Protocol, 2, 3, 4 / 4.1, 5, 6S, 6A, 6B, 7A, 7B, and
the Phase 7C / 7C.1 Architecture Baseline §16 amendment. Implementation output,
not yet locked: Phase 7C.1 / 7D (app containerization — live smoke-tested on
Windows Docker Desktop / WSL2) and Phase 7D.1 (compose build-race cleanup).
Next required action: GPT review → Gemini critique → user-run live Docker
validation → user locks 7C.1 / 7D together with 7D.1. See
`docs/handoff-state.md` and `docs/roadmap.md`.

## Phase 7 complete — 7D / 7D.1 locked (2026-05-24)

Recorded as a status update (the round log above is append-only and is not
rewritten). Phase 7D (Optional Local App Containerization) and Phase 7D.1
(Operational Cleanup: Compose Build Race Fix) were reviewed, **live Docker
smoke-tested on Windows Docker Desktop / WSL2**, and **locked** with user
approval. The smoke test confirmed `docker compose config` / `build` (no
same-tag BuildKit export race) / `up -d` / empty-cache `up -d` rebuild, with
blue and green serving from `StoryTimeFeed Python/3.12.3` on `127.0.0.1:8000`
and `:8001`. OI-20 (the compose build race) is closed.

**Phase 7 is complete.** Locked Phase 7 set: 7A, 7B, 7C / 7C.1, 7D, 7D.1. The
next planned phase is **Phase 8 — Multi-Backend Telemetry Fan-Out** (planning
not yet started).

This entry supersedes the earlier "State Preservation Bundle round" status
note, which described 7D / 7D.1 as implementation output pending lock.

## State Preservation Bundle director-system round (2026-05-24)

A bounded documentation round added `LLM_DIRECTOR.md` (repo-root first-read
instructions) and brought the State Preservation Bundle to Phase 7 completion:
`docs/roadmap.md`, `docs/handoff-state.md`, `docs/roundtable-import-bridge.md`,
`docs/verification-log.md`, and `docs/artifact-manifest.md` updated;
`docs/canonical-state.md`, `docs/phase-history.md`, `docs/open-issues.md`, and
`README.md` updated. No code, configuration, Docker, tests, architecture,
deployment behavior, or telemetry behavior changed. Six Docker-free gates pass
(314 tests).

## Phase 8A — Architecture Baseline Amendment (candidate) — 2026-05-24

An architecture/documentation round (Claude Opus 4.7) that **authored the
Phase 8A Architecture Baseline amendment candidate** — it did not implement
anything. Phase 8 (Multi-Backend Telemetry Fan-Out) introduces optional
observability fan-out to external backends, which is an outbound network call
and therefore needs an explicit amendment to the local-first baseline before
any implementation. This round adds `docs/architecture-baseline.md` **Section
23** — "Collector-Owned Multi-Backend Telemetry Fan-Out" — establishing twelve
governing rules: Collector-owned fan-out only; no vendor SDKs in application
code; standard `otlp` / `otlphttp` exporters only; a narrow outbound-network
exception (core app and the whole test suite still run offline); vendor
profiles disabled by default with `STORYTIME_TELEMETRY=noop` unchanged;
environment-only secret injection; strengthened telemetry data hygiene
(control-plane metadata only); stdout/Loki log routing for Phase 8B (no Python
OTLP log rewrite); mandatory Collector resiliency patterns; the recorded
backend priority Dynatrace → New Relic → Datadog-deferred; the Phase 8B local
stack (Collector + Prometheus + Loki + Jaeger + Grafana); and the accepted
Phase 8A / 8B / 8C split. A short candidate cross-reference note was added to
§16. **Section 23 is an authored candidate — not locked.** Per the Phase
Closure Protocol and the precedent of the Phase 7C / 7C.1 §16 amendment, it
locks only after GPT-5.5 review, Gemini critique, any revision, and explicit
user approval; no Phase 8 implementation may depend on it until then. No
application code, telemetry code, Docker, configuration, tests, or
dependencies were changed. Six Docker-free quality gates pass (314 tests).

## Phase 8A — Architecture Baseline Amendment — LOCKED (2026-05-24)

Recorded as a status update (the round log above is append-only and is not
rewritten). The Phase 8A Architecture Baseline amendment candidate
(`docs/architecture-baseline.md` Section 23 — Collector-Owned Multi-Backend
Telemetry Fan-Out) completed the Phase Closure Protocol review sequence:
Claude Opus 4.7 authored the candidate; GPT-5.5 reviewed the archive and found
it clean; Gemini reviewed the self-contained Phase 8A review bundle and
returned `SAFE TO LOCK`; the user approved the lock. **Section 23 is now
locked and canonical.** Its twelve governing rules and the Phase 8A / 8B / 8C
split are unchanged from the locked candidate — only the section's status
text changed from "authored candidate / not yet locked" to "locked /
accepted", with the matching §16 amendment note and §23.14 closing clause
updated for status consistency.

This lock closure is documentation-only: no application code, telemetry code,
Docker artifact, Collector configuration, test, or dependency was changed; no
vendor exporter, vendor SDK, or vendor configuration was added. Six
Docker-free quality gates pass (314 tests).

**Phase 8A is complete.** The next phase is **Phase 8B — Local Multi-Backend
Stack Expansion** (add Loki and local log routing; prove the local topology;
no vendor credentials, no network egress). Phase 8B implementation may now
depend on the locked Section 23.

---

## Phase 8B — Local Multi-Backend Stack Expansion (implementation output produced, pending review/lock)

**Date:** 2026-05-24

Implementation output for **Phase 8B — Local Multi-Backend Stack Expansion**.
Per the Phase Closure Protocol this is implementation output only — Phase 8B
is **not** locked. It locks only after GPT review, Gemini critique, and
explicit user approval.

Phase 8B expands the local observability stack from four services to five by
adding **Loki** and a local **log-routing path**, governed by the now-locked
Architecture Baseline Section 23.

Implemented:

- **Loki** added to `docker-compose.observability.yml` (`grafana/loki:3.3.2`,
  loopback-bound `127.0.0.1:3100`) with a minimal local config `config/loki.yaml`
  (single-binary, filesystem storage, no auth, 72h retention).
- **OpenTelemetry Collector** gained a `logs` pipeline: a `filelog` receiver
  tails a mounted log directory and forwards lines to Loki via the **standard
  `otlphttp` exporter** pointed at Loki's native OTLP endpoint — deliberately
  not a proprietary `loki` exporter and not a vendor exporter (§23.4). The
  collector mounts `./logs` read-only. Resiliency added per §23.10: a
  `memory_limiter` processor first in every pipeline, and `retry_on_failure` +
  `sending_queue` on the Jaeger and Loki exporters. Traces and metrics
  pipelines are otherwise unchanged.
- **Grafana** provisions a third datasource (**Loki**) as code; the six metric
  dashboards are untouched. Logs are explored via Grafana Explore — Phase 8B
  adds no logs dashboard, so the Phase 6A metric-honesty guarantee is intact.
- **Log source:** the observability **demo harness** writes a structured
  JSON-lines log file (`storytime.demo.logsink`) when run with `--log-dir`.
  This is plain structured *file* logging — no `opentelemetry` import, no
  network call, no Python OTLP log export (§23.9, §23.13). Records are
  control-plane metadata only (§23.8). The StoryTime application core gains no
  parallel logging system.

Section 23 compliance: collector owns routing; no vendor SDKs/agents/exporters;
standard `otlphttp` only; `STORYTIME_TELEMETRY=noop` default unchanged; core
app and all tests run offline with no Docker/credentials; no secrets; logs are
control-plane only and file-routed, never Python OTLP log export; collector
config is resilient; observability ports are loopback-bound; blue/green slot
identity and `service.instance.id` (Phase 7D) untouched.

Quality gates: all six green — `uv sync` OK, **332 tests passed** (314 prior +
18 new in `tests/test_observability_stack.py`), ruff clean, mypy clean (71
source files), 2 import contracts kept, `storytime doctor` healthy. Docker was
unavailable in the build environment, so the Loki image tag and `config/loki.yaml`
are unverified there — tracked as **OI-21**, to be verified on a Docker host.

**Next:** GPT review → Gemini critique → user approval → Phase 8B lock. Phase
8C (Optional Vendor Export Profiles) is gated on the Phase 8B lock.

---

## Phase 8B.1 — Operational Cleanup: logs-directory preflight (implementation output produced, pending review/lock)

**Date:** 2026-05-24

Narrow operational cleanup of Phase 8B. GPT-5.5 review and Gemini independent
critique found the Phase 8B implementation architecturally sound and in scope,
returning `SAFE WITH MINOR CLEANUP`. Phase 8B.1 applies that cleanup; it does
not redesign Phase 8B and does not begin Phase 8C.

Cleanup applied — **`./logs` directory preflight.** `docker-compose.observability
.yml` bind-mounts `./logs` into the Collector's `filelog` receiver. If that
directory does not exist when `docker compose up` runs, Docker may create it
root-owned, after which the non-root local demo (`python -m storytime.demo
--log-dir logs`) cannot write `logs/storytime-demo.log` and Loki receives no
demo logs. The fix makes the directory exist, owned by the invoking user,
before anything depends on it:

- **Makefile** — added a `logs-dir` preflight target (`mkdir -p logs`) and
  three convenience targets: `observability-up` (depends on `logs-dir`, then
  `docker compose ... up -d`), `observability-down`, and `demo` (depends on
  `logs-dir`, then `python -m storytime.demo --log-dir logs`). `make help` and
  `.PHONY` updated. The six Docker-free gates are unchanged.
- **Docs** — `docs/observability-demo.md`, `docs/runbook.md`, and `README.md`
  now show `mkdir -p logs` before `docker compose up` for manual users, with a
  short note on why, and point at the `make` shortcuts.
- **Tests** — two regression tests added to `tests/test_observability_stack.py`
  asserting the `logs-dir` preflight exists and that `observability-up` and
  `demo` depend on it.

No application code, telemetry, Collector config, Loki config, compose
service, or dependency changed — this is operational/developer-experience
cleanup only. Quality gates: all six green — **334 tests passed** (332 prior +
2 new), ruff/mypy/import-linter clean, `storytime doctor` healthy.

**Next:** confirm the cleanup resolves the review feedback → Phase 8B (now
including 8B.1) lock on user approval. Phase 8C (Optional Vendor Export
Profiles) remains gated on the Phase 8B lock.


---

## Phase 8B / 8B.1 — LOCKED (2026-05-24)

Phase 8B — Local Multi-Backend Stack Expansion, together with the Phase 8B.1
operational cleanup (the `./logs` directory preflight), completed the Phase
Closure Protocol: implemented by Opus, reviewed by GPT-5.5 and independently
critiqued by Gemini (`SAFE WITH MINOR CLEANUP`), the cleanup applied in Phase
8B.1, and **locked with explicit user approval (2026-05-24)** — the approval
conveyed by the go-ahead to begin Phase 8C, which is gated on the Phase 8B
lock. The five-service local observability stack (OpenTelemetry Collector +
Prometheus + Loki + Jaeger + Grafana) and the local log-routing path are now
canonical; Phase 8C builds on them.

## Phase 8C — Optional Vendor Export Profiles (implementation output produced, pending review/lock)

**Date:** 2026-05-24

Implementation output for **Phase 8C — Optional Vendor Export Profiles**, the
third and final Phase 8 sub-phase. Per the Phase Closure Protocol this is
implementation output only — Phase 8C is **not** locked until GPT review,
Gemini critique, and explicit user approval.

Phase 8C is a configuration/documentation phase. It changes no StoryTime
application behaviour, adds no vendor SDK, and adds no cloud deployment. It is
governed entirely by the locked Architecture Baseline Section 23.

Implemented (Gemini-reviewed direction `SAFE WITH EDITS`, Option B):

- **`config/otel-collector-vendor.yaml`** (new) — the local Phase 8B collector
  config plus two disabled-by-default vendor export profiles: `otlphttp/dynatrace`
  and `otlphttp/newrelic`. Both use the standard `otlphttp` exporter (23.4) —
  no proprietary exporter, no Datadog exporter (Datadog deferred, 23.11).
  Traces, metrics, and logs fan out to both vendors in addition to the local
  Jaeger/Prometheus/Loki legs.
- **`docker-compose.vendor.yml`** (new) — an override compose file. The default
  `docker compose -f docker-compose.observability.yml up -d` is unchanged and
  local-only; vendor egress requires the explicit extra file
  `-f docker-compose.vendor.yml`, which swaps the collector onto the vendor
  config and injects credentials from a git-ignored secrets file.
- **`config/vendor.secret.env.example`** (new) — committed placeholder template
  for the vendor credentials. The real `config/vendor.secret.env` matches the
  `*.secret.env` git-ignore / docker-ignore pattern and is never committed.
  Every value is an obvious `REPLACE-WITH-YOUR-...` placeholder on a `.invalid`
  host — no real endpoint, token, tenant ID, or account ID anywhere (23.6, 23.7).
- **Resiliency (23.10)** — each vendor exporter has a bounded `retry_on_failure`
  (`max_elapsed_time: 60s`) and a `sending_queue`; `memory_limiter` is first in
  every pipeline. Vendor exporters are independent siblings of the local
  exporters: a vendor outage drops only that leg, never the local stack or the
  app. Drop-not-crash.
- **`tests/test_vendor_export_profiles.py`** (new, 12 tests) — static
  governance checks: profiles present, `otlphttp` only, no Datadog/proprietary
  exporter, resiliency, env-injected secrets, the default local-only path
  untouched, and secret-safety of the committed template.
- **`tests/test_containerization.py`** — the Phase 7C.1 test
  `test_no_vendor_telemetry_fanout_config_is_introduced` enforced the Section
  16 note's blanket "no vendor telemetry fan-out", which the locked Section
  23.14 amendment narrowly superseded. It was updated (and renamed
  `test_vendor_export_config_is_confined_to_the_phase8c_optin_files`) to the
  post-Section-23 contract: vendor config is allowed only in the Phase 8C
  opt-in files, the default path stays local-only, and Datadog stays absent.
- **Docs** — new `docs/vendor-export-profiles.md`; `docs/telemetry-map.md`,
  `docs/observability-demo.md`, `docs/runbook.md`, and `.env.example` updated.

Quality gates: all six green — `uv sync` OK, **346 tests passed** (334 prior +
12 new; one Phase 7 test renamed/updated), ruff clean, mypy clean (71 source
files — no application code changed), 2 import contracts kept, `storytime
doctor` healthy. Docker was unavailable in the build environment, so the
override compose merge and live vendor export are unverified there — covered by
OI-22.

**Process notes for the reviewer.** (a) The Phase 8C prompt asserted Phase 8B /
8B.1 were already locked, whereas the prior bundle recorded them as pending
lock; this round treated the Phase 8C go-ahead as the user's lock authorization
for 8B / 8B.1 and flipped their state records from pending to locked. (b) The
Phase 8C prompt was truncated mid goal-diagram (it ended after "optional New
Relic OTLPHTTP export"); the scope above follows the fully-specified Gemini
`SAFE WITH EDITS` direction. (c) The build environment's container filesystem
reset mid-session, so Phase 8C was reconstructed from a clean Phase 8B.1
baseline.

**Next:** GPT review → Gemini critique → user approval → Phase 8C lock, which
closes Phase 8.

## Phase 8C.1 — Vendor Profile Separation Cleanup (implementation output produced, pending review/lock)

**Date:** 2026-05-24. **Round type:** targeted cleanup of the Phase 8C
implementation output, applied before the Phase 8C lock. Not a redesign of
Phase 8C and not Phase 9.

**Why.** Independent review of the Phase 8C archive
(`storytime-phase8c-vendor-export-profiles.tar.gz`, sha256
`c85a664517df4d9aae604ae744a57ee561b412839b931a453df04135fea2d009`) found one
lock-blocking design issue: Phase 8C shipped a single combined override
(`docker-compose.vendor.yml` + `config/otel-collector-vendor.yaml`) that
activated Dynatrace and New Relic together. The prior Gemini Option B
recommendation favoured explicit, deliberate per-vendor opt-in. A combined
override is weaker: a user may hold only one vendor's credentials, may want to
demo one backend at a time, and disabling a vendor meant editing the Collector
config — not ideal for a governed demo workflow.

**Phase-gate verification before changes.** Confirmed from the uploaded bundle:
Phase 8A locked; Phase 8B / 8B.1 locked; Phase 8C implemented but not locked;
the requested task is the Phase 8C.1 cleanup. The Phase 8C archive sha256 was
verified against the value above before any file was touched.

**What changed.**
- **Removed** `docker-compose.vendor.yml` and `config/otel-collector-vendor.yaml`
  (the combined override).
- **Added** `docker-compose.vendor.dynatrace.yml` and
  `config/vendor/otel-collector.dynatrace.example.yaml` — the Dynatrace-only
  profile (local config plus a single `otlphttp/dynatrace` exporter).
- **Added** `docker-compose.vendor.newrelic.yml` and
  `config/vendor/otel-collector.newrelic.example.yaml` — the New Relic-only
  profile (local config plus a single `otlphttp/newrelic` exporter).
- Each override mounts its vendor config at a distinct container path and
  points the Collector `command:` there. The two overrides are **mutually
  exclusive**: a single Collector reads one resolved config and Compose's
  `command:` is last-write-wins, so stacking both does not yield a two-vendor
  pipeline. This is stated explicitly in both override files, both vendor
  configs, and `docs/vendor-export-profiles.md`.
- `config/vendor.secret.env.example` kept as one shared template (its header
  updated to explain the two profiles); each override reads it, and the unused
  vendor's placeholders are simply never referenced.
- **`tests/test_vendor_export_profiles.py`** rewritten for the split shape —
  parametrized per vendor; new assertions that each config wires exactly its
  own profile and not the other, and that the overrides target distinct configs
  and distinct container paths.
- **`tests/test_containerization.py`** — the Phase 8C opt-in file set updated
  from the two combined files to the four split files. No rename, no behaviour
  change.
- **Docs** — `docs/vendor-export-profiles.md` rewritten; `docs/telemetry-map.md`,
  `docs/observability-demo.md`, `docs/runbook.md`, `.env.example`,
  `.dockerignore`, `README.md`, `LLM_DIRECTOR.md`, `docs/open-issues.md`
  (OI-22) updated to the per-vendor override names.

**State-doc cleanup folded in.** The `docs/handoff-state.md` "State-source
note" carried ambiguous self-doubt language ("If that inference is wrong,
revert the Phase 8B / 8B.1 lock-status lines"). Per the secondary review
concern it was removed; handoff-state now states cleanly that Phase 8B / 8B.1
are locked on the user's explicit go-ahead and that only Phase 8C (with 8C.1)
awaits review/lock. The provenance of the 8B / 8B.1 lock remains recorded here
in phase-history (the Phase 8C round's process note (a)) — append-only history
is the right home for it; durable status docs should not carry the doubt.

**No Section 23 invariant changed.** Standard `otlphttp` only (23.4); no
proprietary or Datadog exporter (23.4, 23.11); environment-only secrets via
`${env:...}` from a git-ignored `config/vendor.secret.env` (23.6, 23.7);
bounded `retry_on_failure` + `sending_queue`, `memory_limiter` first (23.10);
default path untouched and local-only (23.6); no `src/` file, `pyproject.toml`
dependency, or application test changed.

**Quality gates.** Re-run after the cleanup — see `docs/verification-log.md`
for the recorded counts. Docker was unavailable in the build environment, so
the per-vendor override compose merges and live vendor export remain unverified
there — covered by OI-22 (scope updated to the two split overrides).

**Scope note for the reviewer.** The Phase 8C.1 task prompt as delivered was
truncated mid-document (it ended inside the Cleanup objective 1 target-shape
block, with no closing sections). The cleanup above follows the two clearly
established objectives — split vendor activation, and remove ambiguous
state-doc language — which the accompanying independent-review brief
independently corroborates. No additional objectives were inferred.

**Next:** GPT review → Gemini critique → user approval → Phase 8C lock (closing
Phase 8); the 8C.1 cleanup locks together with Phase 8C.

## Phase 8C / 8C.1 — LOCKED (2026-05-24)

Phase 8C — Optional Vendor Export Profiles, together with the Phase 8C.1
Vendor Profile Separation Cleanup, completed the Phase Closure Protocol:
implemented by Opus; the Phase 8C archive reviewed by GPT-5.5, which required a
cleanup (split combined vendor activation into independent per-vendor profiles;
clear ambiguous 8B / 8B.1 lock-status wording); the cleanup applied in Phase
8C.1; the Phase 8C.1 archive re-reviewed by GPT-5.5 (clean — no `src/` change,
no vendor SDK/agent, no proprietary or Datadog exporter, no app-to-vendor call,
no dependency change, both vendor configs and both override files parse,
vendor tests `24 passed`); independently critiqued by Gemini, which returned
**`SAFE TO LOCK`**; and **locked with explicit user approval (2026-05-24)**.

The locked authoritative archive is `storytime-phase8c1-vendor-profile-split.tar.gz`
(sha256 `b93cc84a473fe71df2ef2f00862c9ab2a7cce019c11da83ec5e738c0818c7f40`).
Phase 8C.1 is accepted as part of the Phase 8C lock — it is the in-scope
cleanup of the Phase 8C output, not a separately locked phase.

Lock-closure round: state/documentation only. No application code, no vendor
profile behaviour, and no implementation changed during lock closure; the
six Docker-free quality gates were re-run on the locked archive as final lock
evidence — `uv sync --frozen --extra dev` OK, `uv run pytest -q` **358
passed**, ruff / mypy (71 source files) / import-linter (2 contracts kept)
clean, `storytime doctor` healthy.

**Phase 8 — Multi-Backend Telemetry Fan-Out — is complete.** All three
sub-phases are locked: 8A (Architecture Baseline Section 23 amendment), 8B /
8B.1 (local multi-backend stack expansion + `./logs` preflight cleanup), and
8C / 8C.1 (optional vendor export profiles). There is no Phase 8D.

Carried caveat: **OI-22** — the per-vendor Compose override merges and live
vendor export remain unverified in the Docker-less build environment. It blocks
no phase gate and was not a lock prerequisite.

**Next:** Phase 9A — Governance Baseline Amendment (Security, Licensing, and
Governance planning). Phase 9 has not started.

---

## Phase 9A — Governance Baseline Amendment (candidate) — 2026-05-24

An architecture/documentation round (Claude Opus 4.7) that **authored the
Phase 9A Architecture Baseline amendment candidate** — it did not implement
anything. Phase 9 is Security, Licensing, and Governance; the accepted
structure is a hybrid split — Phase 9A (Governance Baseline Amendment), Phase
9B (Minimal Trust Envelope Implementation), Phase 9C (Docs / Audit Polish if
needed). Phase 9A exists to define the governance law before Phase 9B
implements the minimal Trust Envelope.

This round adds `docs/architecture-baseline.md` **Section 24** — "Governance
Baseline (Trust Envelope, Licensing, Fail-Closed Gating)" — establishing the
governance model: StoryTime is **not** a legal rights-clearance engine and the
human operator is the source of truth for licensing decisions (§24.2); a ban
on legal automation / legal hallucination, with a forbidden concept list —
`legal_verified_by_llm`, `copyright_cleared_by_ai`, `compliance_score`,
`rights_confidence_score`, `copyright_safe_score`, and any AI-generated legal
assertion (§24.3); the allowed source categories `CC0`, `US_PUBLIC_DOMAIN`,
`EXPLICIT_PERMISSION`, `LOCAL_TEST_FIXTURE`, with **no** `AMBIGUOUS` category
(§24.4); the disallowed/blocked categories, with ambiguous content failing
closed unless explicitly operator-approved with notes (§24.5); the fail-closed
governance gate — an `APPROVED` Trust Envelope must exist before TTS or RSS
publish, and `BLOCKED` / `REJECTED` / `NEEDS_REVIEW` / `UNKNOWN` / missing /
malformed / unverifiable all fail closed before TTS (§24.6); the Trust Envelope
concept as a durable audit artifact, not a legal opinion, with the durable
artifact envelope as the governance source of truth and a rebuildable SQLite
projection (§24.7); the **canonical minimum Trust Envelope schema** including
`review_context_summary`, with the `license_type` and `decision` enum value
sets (§24.8); the local, inspectable blocked-source config direction —
`config/governance/blocked-sources.yaml`, no cloud, no remote blocklists, no
scraping (§24.9); the reinforced secrets policy — no secrets in SQLite or
artifact envelopes, environment-only credentials (§24.10); the honest
local-first deletion/retention posture — no cloud soft delete, no compliance
shredder, no GDPR/CCPA claim (§24.11); the carried-forward telemetry/privacy
hygiene, with bounded governance status metadata only (§24.12); the public/demo
disclaimers (§24.13); the future static legal-hallucination grep/regex gate
requirement, documented for Phase 9B with a note that governance docs which
define the forbidden vocabulary must be allowlisted (§24.14); the Phase 10
dependency contract — a parseable Trust Envelope and a stable UI-safe status
enum, no legal overclaiming (§24.15); the accepted Phase 9A / 9B / 9C split
(§24.16); and a closing "what this amendment does NOT authorize" clause
(§24.17).

**Section 24 is an authored candidate — not locked.** Per the Phase Closure
Protocol and the precedent of the locked Phase 7C / 7C.1 §16 and Phase 8A §23
amendments, it locks only after GPT-5.5 review, Gemini critique, any revision,
and explicit user approval; no Phase 9B implementation may depend on it until
then. No application code, database schema, artifact envelope code, telemetry
code, configuration behaviour, tests, or dependencies were changed — only
Markdown living-doc files. Lightweight verification was run on the delivered
state; see `docs/verification-log.md`.

**Next:** GPT-5.5 review → Gemini critique → any revision → explicit user
approval → Phase 9A lock. Then Phase 9B — Minimal Trust Envelope
Implementation — is scoped and gated under the Phase Closure Protocol.

## Phase 9A.1 — Governance Baseline Cleanup + Phase 9A LOCKED (2026-05-24)

A bounded compound round (Claude Opus 4.7): the Phase 9A.1 governance-baseline
cleanup, the Phase 9A lock closure, and the drafting of the Phase 9B
implementation prompt. No implementation: no application code, database
schema, artifact envelope code, or configuration behaviour changed — only
Markdown living-doc files, plus one new draft-prompt Markdown file.

**Phase 9A.1 cleanup.** GPT-5.5 reviewed the Phase 9A candidate archive and
found it docs-only and review-ready. Gemini returned `SAFE WITH EDITS`; most
requested edits were already satisfied in the candidate (`review_context_
summary` present; the Trust Envelope schema already in `docs/architecture-
baseline.md` §24.8; the future grep/regex gate already documented in §24.14;
the fail-closed-before-TTS/RSS rule already in §24.6). Two clarifications were
folded into `docs/architecture-baseline.md` Section 24 before lock:

1. **Source authorization, not viewpoint acceptability (§24.5).** Added a rule:
   StoryTime governs source authorization, not viewpoint acceptability;
   controversial, sensitive, political, religious, historical, philosophical,
   or unpopular perspectives are not blocked merely for their viewpoint.
   Governance decisions concern source authorization, licensing provenance,
   privacy, operator approval, blocked-source status, and auditability — never
   the opinions or themes expressed. StoryTime governance is explicitly not a
   content-moderation system: no topic-policy categories, no viewpoint
   screening, no content safety classification, and Phase 9B must add none.
2. **Check early; block hard (§24.6).** Clarified that Phase 9B should check
   governance status as early as practical — ideally before or during
   approval/rehydration — while the hard requirement is unchanged: the
   pipeline must block execution before TTS, audio processing, or RSS
   publishing if no `APPROVED` Trust Envelope exists. Early checking is an
   additional fail-fast safeguard, never a relaxation of, or substitute for,
   the before-TTS/audio/RSS hard block.

These are architecture-law clarifications only; no gate, runner, or stage code
was implemented or changed.

**Phase 9A LOCKED.** With the cleanup folded in, the Phase 9A Architecture
Baseline amendment (`docs/architecture-baseline.md` Section 24 — Governance
Baseline: Trust Envelope, Licensing, Fail-Closed Gating) completed the Phase
Closure Protocol: authored by Opus; reviewed by GPT-5.5 (docs-only,
review-ready); reviewed by Gemini (`SAFE WITH EDITS` — the two edits folded in
by the 9A.1 cleanup); **locked with explicit user approval (2026-05-24)**.
**Section 24 is now locked and canonical.** Phase 9B implementation may depend
on it. Section 24's status block, the §24.16 closing precondition, and the
§24.17 closing clause were updated from "candidate / pending lock" to "locked";
the governance rules, the Trust Envelope schema, and the Phase 9A / 9B / 9C
split are unchanged from the reviewed candidate apart from the two folded-in
clarifications.

**Phase 9B prompt drafted.** A draft implementation prompt for the next round
was written to `docs/phase9b-minimal-trust-envelope-implementation-
prompt.md`. It is a draft prompt only — not implementation, and it authorizes
nothing by itself. It instructs the next Opus session to implement the minimal
Trust Envelope per the locked Section 24: the schema, the durable
artifact-envelope governance truth plus a SQLite projection, the fail-closed
gate, the local blocked-source config, the static legal-hallucination
grep/regex gate, tests, and doc/runbook updates.

This compound round is documentation-only: no application code, telemetry
code, Docker artifact, database schema, artifact envelope code, configuration
behaviour, test, or dependency was changed; no secret was added. The six
Docker-free quality gates were run as a regression check; see
`docs/verification-log.md`.

**Phase 9A is complete and locked. Architecture Baseline Section 24 is
canonical. The next phase is Phase 9B — Minimal Trust Envelope Implementation;
Phase 9B has not started.** Phase 9B must be scoped and gated under the Phase
Closure Protocol (the drafted prompt is the starting point) before any
implementation begins.

## Phase 9B — Minimal Trust Envelope Implementation (implementation output produced, pending review/lock) — 2026-05-24

Phase 9B deep implementation by Claude Opus 4.7: the implementation phase that
turns the locked Architecture Baseline Section 24 governance law into working
code. It implements, minimally and honestly, exactly the eight Section 24
deliverables — no more.

A new `storytime.governance` package provides the **Trust Envelope** model and
its canonical §24.8 closed JSON Schema: the `LicenseType` and
`GovernanceDecision` enums (the exact §24.8 value sets), the `TrustEnvelope`
frozen dataclass (all eighteen §24.8 fields), `TRUST_ENVELOPE_SCHEMA_VERSION =
"1"`, and a versioned compatibility reader that fails closed on a malformed or
unsupported envelope. The **durable Trust Envelope artifact** is a separate
durable JSON file at `governance/trust-envelope.json` in each run directory —
the governance source of truth (§24.7). It is deliberately *linked from* the
run rather than embedded in the ARCH-LOCKed `ArtifactEnvelope` shape, the
minimal non-invasive reading of §24.7's "embedded in or linked from". A
**SQLite projection** — schema migration `0005`, the `trust_envelope` table —
is a rebuildable, queryable projection carrying only bounded status fields; it
is never the source of truth.

The **fail-closed governance gate** (§24.6) is wired at three honest points:
`ingest` derives the Trust Envelope from the human-written source manifest
(its licence field and approval block) plus the operator's local
blocked-source list, writes the durable artifact, records the projection, and
**checks early** — a blocked or unapproved source fails at ingest, before the
run reaches the text gate. `synthesize` **hard-blocks before TTS** and
`publish` **hard-blocks before RSS**, each re-verifying the durable envelope
independently — an early APPROVED check never licenses a later stage to skip
the hard gate. Only an explicit `APPROVED` envelope passes; a `BLOCKED` /
`REJECTED` / `NEEDS_REVIEW` / `UNKNOWN` decision, and a missing, malformed, or
unverifiable envelope, all fail closed. The derivation transcribes a recorded
human decision plus a deterministic local lookup — it is **not** legal
automation or model inference (§24.2 / §24.3).

The **local blocked-source config** (`config/governance/blocked-sources.yaml`,
§24.9) is a committed, human-curated deny-list — local, inspectable, no remote
fetch, no scraping; it ships empty so the CC0 / public-domain demo is never
blocked. The **static legal-hallucination gate** (§24.14) is the
`storytime.governance.legal_terms` scanner plus `test_legal_hallucination_gate.py`,
which scan the repo's code, config, and non-governance docs for the §24.14
forbidden legal-certification vocabulary, allowlisting the governance documents
that legitimately define it. A `GovernanceEvaluated` event records the gate
decision in the durable event_log with only bounded status metadata (§24.12);
`storytime status` shows the governance decision (§24.15 Phase 10 prep).

Five new test files add 53 tests (suite total **411 passing**). `pyyaml` was
promoted from a dev-only to a runtime dependency — the §24.9 config is YAML —
and `uv.lock` was re-locked; the import-linter no-OpenTelemetry contract was
extended to cover `storytime.governance`. No ARCH-LOCKed contract changed: the
`ArtifactEnvelope` shape, `BASE_STAGE_ORDER`, the stage and DTO boundaries, and
the append-only event_log model are all unchanged. No legal/compliance/
clearance claim, AI copyright classifier, compliance score, authentication,
scraping, or hosted service was added. All six Docker-free quality gates pass.

Per the Phase Closure Protocol this implementation output is **not** phase
completion: Phase 9B awaits GPT-5.5 review, Gemini critique, and explicit user
approval before it locks. The authoritative implementation archive is
`storytime-phase9b-minimal-trust-envelope-implementation.tar.gz`.

## Phase 9B.1 — Forbidden-Term Scanner Hardening Cleanup — 2026-05-24

Targeted cleanup round for the Phase 9B implementation. GPT-5.5 reviewed the
Phase 9B candidate archive and passed it to Gemini; Gemini returned `SAFE WITH
MINOR CLEANUP` and explicitly passed Phase 9B scope correctness, locked Section
24 compliance, the Trust Envelope implementation, pipeline integration, the
blocked-source implementation, the fail-closed gate, test/verification
coverage, and the documentation/state-preservation updates. Gemini's single
required cleanup item: harden the static legal/compliance forbidden-term
scanner so it cannot crash on binary or generated files — SQLite databases,
WAV/MP3 audio, images, archives, compiled `.pyc` caches — or on
virtualenv/cache/`runs`/`feed`/build directories.

Phase 9B.1 applied exactly that cleanup, and nothing else. The scanner
(`storytime.governance.legal_terms`) was rewritten to be deterministic,
cross-platform, and independent of any shell: it walks the project tree once
with `os.walk`, pruning an explicit ignored-directory set (`.venv`, `.git`,
`__pycache__`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`,
`.import_linter_cache`, `runs`, `feed`, `dist`, `build`, `node_modules`); it
reads only files whose extension is on a text allowlist (`.py`, `.md`, `.yaml`,
`.yml`, `.json`, `.toml`, `.txt`), so binary/generated extensions are never
opened; and it reads with `errors="replace"` so a stray invalid UTF-8 byte
becomes `U+FFFD` rather than raising `UnicodeDecodeError`. A file that genuinely
cannot be opened is skipped as a controlled, non-fatal event. The scanner
cannot crash on binary, generated, or malformed input.

Seven hardening tests were added to `tests/test_legal_hallucination_gate.py`
proving: binary-extension files are never opened even when their bytes spell a
forbidden term; a real binary blob does not crash the scan; an allowlisted text
file with invalid UTF-8 is read safely and a forbidden term in its valid text
is still detected; forbidden text under `runs/` and `feed/` is ignored;
forbidden text under `.venv/`, `.git/`, and cache directories is ignored; an
ignored directory nested inside a real source tree is pruned; and a forbidden
claim in a non-allowlisted doc is still flagged (detection is not weakened).
The suite is **418 passing** (411 prior + 7 new).

Phase 9B.1 changed only `src/storytime/governance/legal_terms.py`,
`tests/test_legal_hallucination_gate.py`, and the State Preservation Bundle
docs. It did not touch the Trust Envelope schema or architecture, the durable
artifact source-of-truth rule, the SQLite schema, the pipeline gate semantics,
the `APPROVED`/`REJECTED`/`BLOCKED`/`NEEDS_REVIEW`/`UNKNOWN` meanings, or
`docs/architecture-baseline.md`. No legal automation, AI copyright
classification, content/viewpoint filtering, auth, scraping, cloud service, or
secret was added. All six Docker-free quality gates pass; the hardened
forbidden-term scan returns zero violations.

**Phase 9B remains implemented but not locked.** Phase 9B is pending GPT-5.5
review, Gemini confirmation if needed, cleanup acceptance, and explicit user
lock. **Phase 9C has not started.** The authoritative archive is
`storytime-phase9b1-forbidden-scanner-hardening.tar.gz`.

## Phase 9B — Minimal Trust Envelope Implementation — LOCKED (2026-05-24)

Phase 9B lock closure. Phase 9B — the implementation of the locked Architecture
Baseline Section 24 governance law — completed the Phase Closure Protocol and
is **locked with explicit user approval (2026-05-24)**.

Closure path: implemented by Claude Opus 4.7 (the `storytime.governance`
package, the durable Trust Envelope artifact, the `trust_envelope` SQLite
projection at schema migration `0005`, the fail-closed gate wired into
`ingest` / `synthesize` / `publish`, the local blocked-source config, and the
static legal-hallucination grep/regex gate); reviewed by GPT-5.5, which found
it ready for Gemini review; critiqued by Gemini, which returned `SAFE WITH
MINOR CLEANUP` and explicitly passed scope correctness, locked Section 24
compliance, the Trust Envelope implementation, pipeline integration, the
blocked-source implementation, the fail-closed gate, test/verification
coverage, and the documentation updates. The **Phase 9B.1 cleanup** applied
Gemini's one required item — hardening the static forbidden-term scanner
against binary/generated files and cache/virtualenv/`runs`/`feed` directories —
and is **folded into the Phase 9B lock**. The user gave explicit approval to
lock Phase 9B with Phase 9B.1 folded in.

This lock-closure round is documentation-only: no application code, governance
code, telemetry code, database schema, artifact envelope code, configuration
behaviour, test, or dependency changed; `docs/architecture-baseline.md` was not
touched. The six Docker-free quality gates were run as a regression check —
**418 passing**, ruff/mypy/lint-imports clean, `doctor` healthy, and the
hardened forbidden-term scan returns zero violations; see
`docs/verification-log.md`.

**Phase 9B is locked. The next phase is Phase 10 — Product UI / Operator
Experience**, the §24.15 dependency contract's consumer: Phase 10 will
visualize governance status (the stable `APPROVED` / `REJECTED` / `BLOCKED` /
`NEEDS_REVIEW` enum) without overclaiming legal certification. Phase 10 has
**not started**. Phase 9C — Docs / Audit Polish — was an optional follow-up and
is not scheduled. The locked authoritative archive is
`storytime-phase9b-locked-state-bundle.tar.gz`.

## Phase 10A — Operator Experience Baseline Amendment (candidate) — 2026-05-24

Amendment-authoring round. Claude Opus 4.7 authored a Phase 10A Architecture
Baseline amendment **candidate** — `docs/architecture-baseline.md` Section 25,
"Operator Experience Baseline". It is architecture/documentation only and
authorizes no implementation; it is **not locked**. Per the Phase Closure
Protocol and the precedent of the Phase 7C / 7C.1 §16, Phase 8A §23, and Phase
9A §24 amendments, Section 25 becomes a locked decision only after GPT-5.5
review, Gemini critique, any required revision, and explicit user approval.

Phase 10 is **Product UI / Operator Experience** — the consumer of the locked
§24.15 dependency contract. Phase 10A defines what "Operator Experience" means
for a local-first portfolio pipeline **before** any Phase 10 implementation,
so the build is the concrete artifact of an agreed model rather than an
architecture decision smuggled in as implementation. Phase 10A planning was
reviewed by multiple independent reviewers (GPT-5.5 as architect/mediator;
Claude Haiku 3.5, Copilot Think Deeper, GPT-5 mini, Gemini 3.5 Flash Lite
Extended, and Llama 4 Scout as critics); the reviewer consensus — docs-only
Phase 10A, a generated local HTML operator report for Phase 10B, read-only
first, no SaaS rewrite, Phase 9 governance boundaries preserved, hard floor and
hard ceiling fixed before implementation — is codified in Section 25.

Section 25 establishes: the operator-experience goal (a single local operator;
no SaaS personas); the read-only-first rule; the source-of-truth rule (SQLite +
artifact envelopes + the durable Trust Envelope stay authoritative; reports and
observability dashboards are projections/links, never truth); the governance
display rule (allowed bounded fields vs a forbidden legal/compliance
overclaiming vocabulary extending §24.3 / §24.14, plus a standing "record of a
human decision, not legal advice" disclaimer); the viewpoint-neutrality
carryover (§24.5 preserved — no content-moderation labels); the Phase 10B
target (a generated, static, local, read-only HTML operator report); the Phase
10B hard floor (a report directory with a latest-runs summary, a run list, and
a single-run detail page) and hard ceiling (no mutation, forms, server,
framework, build pipeline, auth, cloud, dashboard recreation, or visual-polish
pass — skeleton HTML plus minimal static CSS only); the deterministic report
data model with explicit field sources; the report field allowlist/blacklist
(no raw story/narration text, transcripts, secrets, long notes, raw telemetry,
or embedded dashboard data); the bounded `review_context_summary` rule (a
500-character display cap, testable); the observability-link rule (links only,
no embedded data, no secrets in URLs); the determinism/snapshot-test
requirement; the privacy/no-raw-content test requirement; the governance-copy
linting requirement (apply the §24.14 scanner to templates and generated
copy); a performance/size guardrail; three Phase 10B example run shapes
(completed, governance-blocked, failed); a full Phase 10B handoff section; the
no-auth/no-cloud/no-server and mutation-gate rules; the stop/revert criterion;
and the accepted Phase 10A / 10B / 10C / 10D split (10C and 10D future and
conditional, not authorized here).

This was a documentation-only round. No application code, database schema,
artifact envelope code, Trust Envelope semantics, governance gate behaviour,
telemetry behaviour, configuration behaviour, test, or dependency changed —
only Markdown living-doc files (the new Section 25 in
`docs/architecture-baseline.md` plus the State Preservation Bundle docs). The
six Docker-free quality gates were re-run as a regression check — `uv run
pytest -q` **418 passed**, ruff / mypy (78 source files) / import-linter (2
contracts) clean, `storytime doctor` healthy; the legal-hallucination scanner
returns zero violations (Section 25 quotes the forbidden vocabulary inside the
allowlisted `docs/architecture-baseline.md`, so the gate is unaffected).

**Historical candidate status at time of authoring:** Phase 10A was a candidate pending review/lock and Phase 10B had not started. This was superseded by the Phase 10A lock record below. Phase 10C and Phase 10D remain future, conditional, and not started. The candidate archive was `storytime-phase10a-operator-experience-baseline-amendment.tar.gz`; the authoritative current archive is the Phase 10A locked-state bundle.


## Phase 10A locked — Operator Experience Baseline Amendment (2026-05-24)

Phase 10A — Operator Experience Baseline Amendment is **locked / accepted / canonical** with explicit user approval.

Gemini 3.1 Pro reviewed the candidate and returned **SAFE TO LOCK (PENDING VERIFICATION)**. GPT-5.5 verified the pending condition by confirming the candidate was documentation-only, changed no implementation files, and left Phase 10B not started. The user then approved the lock.

The locked architecture law is `docs/architecture-baseline.md` Section 25. It defines a read-only-first, static-local-report-first operator-experience baseline and fixes the next implementation target as Phase 10B — Generated Local HTML Operator Report.

No implementation was performed by the lock pass. Phase 10B is next and not started. Phase 10C and Phase 10D remain future and conditional. Gemini's local-web-server aside was not accepted as authorization for Phase 10B; no-server static local HTML remains the locked target.

## Phase 10B — Generated Local HTML Operator Report (implementation output produced; superseded by lock record) — 2026-05-24

Implementation round. Claude Opus 4.7 implemented **Phase 10B — Generated Local
HTML Operator Report**, the first implementation phase of Phase 10, under the
locked Architecture Baseline Section 25 (the Phase 10A Operator Experience
Baseline). Historical implementation-candidate record. This entry was superseded by the Phase 10B lock record below after GPT-5.5 verification, Gemini critique, and explicit user approval.

Phase 10B adds a new `storytime.reporting` package and a `storytime report
generate` CLI command that generates a static, local, read-only HTML operator
report from existing authoritative state — the SQLite run/stage/Trust-Envelope
projections and the durable Trust Envelope artifact. The report is four kinds
of file written into `operator-report/`: `index.html` (landing page + the
latest-runs summary), `runs.html` (the full run list), one `run-<run_id>.html`
detail page per run, and a single minimal local `style.css`. The operator opens
`index.html` directly in a browser — there is no web server, no persistent
backend, no frontend framework, no build step, no authentication, and no cloud
dependency. The report renders with zero network access: all styling is the one
local stylesheet and there are no external CDN links, fonts, scripts, icons, or
remote favicons.

The report is strictly read-only and bounded. It shows only the Section 25.12
allowed fields — run and stage identifiers and statuses, the §24.8 governance
`decision` and `license_type` enums, the approver, timestamps, a structured
blocked/rejected reason, artifact path references, and optional observability
links. The Trust Envelope's `review_context_summary` is displayed bounded to
500 characters (the §25.13 locked length) and safely truncated with a visible
indicator; the free-text `governance_notes` field is never projected into the
report. Every governance page carries the §25.5 disclaimer that the report
records a human operator's decision and pipeline state and is not legal advice
or a certification of copyright safety. The report contains no form, no button,
no state-changing link, and no JavaScript — it cannot approve, retry, reject,
rerun, delete, publish, or edit anything (§25.10 / §25.17). Observability links
are optional references only: a Jaeger trace link appears only when
`STORYTIME_JAEGER_BASE_URL` is configured and a run has a recorded trace id, it
embeds no dashboard data or secret, and the report is complete without it. No
observability backend is queried.

Report generation is deterministic — the rendering core takes an injected
timestamp, so identical state plus an identical timestamp yields byte-for-byte
identical HTML; the CLI supplies the real time and the tests supply a fixed
one. Nineteen new tests in `tests/test_operator_report.py` lock the Section 25
guarantees: the completed / governance-blocked / failed run shapes all
generate; no raw story text, narration, transcript, secret, or long free-text
governance note reaches the HTML; no forbidden legal/compliance phrase appears
(the test reuses the locked `FORBIDDEN_LEGAL_TERMS` set rather than re-listing
the phrases); the report is byte-for-byte deterministic; observability links
are optional and sanitized; no external asset is referenced; and neither the
generator nor the CLI command mutates state.

`storytime.reporting` was added to both import-linter contracts (the
OpenTelemetry-confinement contract and the events-leaf contract) — strengthening
them. No ARCH-LOCKed contract changed; no database schema migration; no new
dependency; SQLite plus the on-disk artifact envelopes (and the durable Trust
Envelope) remain the source of truth — the generated report is a view, never
authoritative. The six Docker-free quality gates pass — 437 tests (19 new),
ruff / mypy (83 source files, strict) / import-linter (2 contracts kept) clean,
`storytime doctor` healthy; the legal-hallucination scanner returns zero
violations. One documented limitation is carried: the projections record a
per-episode audio path but not a per-run RSS feed path (the feed is the shared
`feed/feed.xml`), so the report surfaces the audio path and references the
shared feed for a run that published; closing that would need a schema change
Phase 10B deliberately does not make.

*(Historical candidate status — superseded by the Phase 10B lock-closure round.)*


## Phase 10B locked — Generated Local HTML Operator Report (2026-05-24)

Phase 10B — Generated Local HTML Operator Report is **locked / accepted / canonical** with explicit user approval.

Gemini 3.1 Pro reviewed the Phase 10B implementation evidence packet and returned **SAFE TO LOCK**. GPT-5.5 verification found the implementation architecturally clean and lockable, with the only sandbox caveat being old Rich/Typer ANSI help-string tests in full pytest that did not indicate a Phase 10B architecture defect; focused Phase 10B tests, ruff, mypy, import-linter, and doctor passed in GPT's sandbox, and Opus reported the full suite passing in its environment.

The lock confirms that Phase 10B delivered the intended operator-experience surface without violating the locked Section 25 law: static local generated HTML, local CSS only, no external CDNs/fonts/scripts/assets, no server runtime, no auth/cloud, no frontend framework, no mutation UI, no raw-content display, no legal overclaiming, deterministic timestamp support, and read-only views over existing SQLite/artifact/Trust Envelope state.

No implementation was performed by this lock pass. *(Historical status at time of Phase 10B lock: Phase 10C remained optional/not started and Phase 10D future/conditional. Phase 10C has since been locked.)*

## Phase 10C — Operator CLI Helpers / Failure Queue (historical implementation-candidate entry) — 2026-05-25

Implementation round. Claude Opus 4.7 implemented **Phase 10C — Operator CLI
Helpers / Failure Queue** under the locked Architecture Baseline Section 25
operator-experience law. Per the Phase Closure Protocol this is implementation
output, **not** a locked phase: it awaits GPT-5.5 review, Gemini critique, any
cleanup, and explicit user approval.

Phase 10C adds a new `storytime.operator_queue` module and a `storytime queue`
CLI command — a read-only failure / review queue. The command gives the local
operator a quick, terminal-native answer to "which runs need attention, why,
and what should I look at next?" It surfaces the runs that are failed, blocked
by governance, marked needs-review, or awaiting an operator approval decision,
and for each one shows the run id, status, stage, governance decision, a
structured failure code and coarse failure category, timestamps, a relative
path to the run's Phase 10B report detail page, the Trust Envelope artifact
path, and a `next_hint` that suggests which existing command or inspection
step to use next.

The command is a viewer only. The word "queue" means an operator-facing
filtered view of existing run state — conceptually a dead-letter / review
queue — and is a semantic query over the existing SQLite source-of-truth
tables. It adds no message broker, no background worker, no Redis / RabbitMQ /
Celery / Kafka / NATS / SQS, no new queue storage, no new run state, and no
`pop` / `dequeue` / `claim` / `ack` behaviour. It mutates nothing and executes
no other command; the `next_hint` only ever suggests an existing command (for
an awaiting-approval run it points at the existing canonical `storytime
approve`), phrased cautiously, never as an automated action.

The queue is bounded and deterministic. `--limit` defaults to 20 — there is no
unlimited option, so the queue never floods the terminal — and `--status` /
`--run-id` filters narrow the view. Results are sorted most-recently-updated
first with the run id as a stable tie-breaker; the output carries no
generation timestamp, so the human table and the `--json` output are
byte-for-byte deterministic for identical state. JSON is emitted from an
explicit 11-field allowlist. The queue surfaces only bounded, structured
fields: for a failed stage it shows the structured `error_kind` code, never
the unbounded `error_message` text; for a governance decision it shows the
§24.8 decision enum, never the free-text `blocked_reason`. It never displays
raw story text, narration, transcripts, secrets, long governance notes, or raw
telemetry, and it makes no legal/compliance certification claim.

Twenty-nine new tests in `tests/test_operator_queue.py` lock these guarantees
across five run shapes (completed, failed, governance-blocked, needs-review,
awaiting-approval): queue membership and the exclusion of healthy runs; the
empty state; `--status` and `--run-id` filtering; the bounded default limit
and a rejected non-positive limit; deterministic sorting and JSON; the
no-raw-content / no-secret / no-free-text-reason / no-overclaiming guarantees
(the legal-phrase test reuses the locked `FORBIDDEN_LEGAL_TERMS` set); the
non-mutating `next_hint`; and that the command neither mutates state nor
requires report generation.

`storytime.operator_queue` was added to both import-linter contracts. No
ARCH-LOCKed contract changed; no database schema migration; no new dependency;
SQLite plus the on-disk artifact envelopes (and the durable Trust Envelope)
remain the source of truth — the queue is a view. The six Docker-free quality
gates pass — 466 tests (29 new), ruff / mypy (84 source files, strict) /
import-linter (2 contracts kept) clean, `storytime doctor` healthy; the
legal-hallucination scanner returns zero violations.

*(Historical candidate status — superseded by the Phase 10C lock-closure round below.)*

## Phase 10C — Operator CLI Helpers / Failure Queue lock closure — 2026-05-25

Lock-closure round. Phase 10C — Operator CLI Helpers / Failure Queue completed the Phase Closure Protocol and is **locked / accepted / canonical**.

Lock basis: Claude Opus 4.7 implemented the Phase 10C candidate from `storytime-phase10b-locked-state-bundle-corrected.tar.gz`. GPT-5.5 Thinking reviewed the implementation and returned PASS with a minor state-hygiene observation (triggering this Phase 10C.1 cleanup). Gemini/Flash Light reviewed the evidence packet and returned SAFE TO LOCK. The user explicitly approved the Phase 10C lock.

Locked artifact: `storytime-phase10c-operator-cli-helpers-failure-queue.tar.gz` (SHA-256 `e30aaa57f900756e62347ddaac2df658d96065c9e1061679adb31594c73e2543`).

The Phase 10C.1 State Preservation Synchronization Cleanup (this round) brings all first-read / cold-session-entry documents up to date with the Phase 10C lock, without changing any application code.

No implementation was performed by this cleanup pass. Phase 10D — Pipeline Re-Run / Mutation Actions — remains not started. Phase 9C remains optional/not scheduled.

## Phase 10D — Pipeline Re-Run / Mutation Actions (implementation output produced, reviewed SAFE WITH EDITS — pending Phase 10D.1 cleanup and lock) — 2026-05-25

Implementation round. Phase 10D implements StoryTime's first operator *mutation* surface under the locked Architecture Baseline Section 25 operator-experience law. Per the Phase Closure Protocol this is implementation output — a candidate, not a locked phase. GPT-5.5 and Gemini/Flash Light have each reviewed the Phase 10D implementation artifact and returned **SAFE WITH EDITS** — implementation safe, docs/state-preservation cleanup required before lock. The required edit is docs/state-preservation cleanup only (Phase 10D.1); the Phase 10D code and mutation implementation should not change.

Phase 10D adds the `storytime rerun` command — a governed, bounded, audited re-run of a failed pipeline run. Phases 10B and 10C gave operators read-only ways to *see* pipeline state; Phase 10D adds the first governed way to *change* it.

What Phase 10D added:

- a new `storytime.operator_rerun` standard-library module — `RerunDecision` / `RerunResult` bounded dataclasses, `evaluate_rerun_eligibility` (a pure-ish decision function), `perform_rerun` (the single bounded mutation plus audit event), and `render_rerun_text` / `render_rerun_json` output;
- a `storytime rerun` CLI command with `--from-stage`, `--dry-run`, and `--json` flags;
- an `EventType.RUN_RERUN_REQUESTED` event type — the audit record written to the existing append-only `event_log` for every actual re-run mutation;
- 27 tests in `tests/test_operator_rerun.py`;
- the `docs/operator-rerun.md` operator guide.

Mutation semantics: a re-run resets a failed run's `pipeline_run.status` from `failed` to the existing resumable `running` state — one bounded status update — so the existing `storytime run --resume` path can re-execute the run from the failed stage. The `rerun` command runs no pipeline work itself; there is no hidden or long-running work. No new run lifecycle state and no new database column are introduced.

Safety model: a re-run proceeds only for a run that exists, is `failed` from a genuine pipeline-stage failure (not an operator approval-gate rejection), and carries an `APPROVED` Trust Envelope. Any unresolved or missing governance decision, an operator gate rejection, an unknown or mismatched `--from-stage`, or an unclassifiable state yields a rejection with a stable decision code. The decision defaults to rejection whenever safety cannot be proven; a re-run never bypasses governance.

Every actual mutation is recorded as a `RunRerunRequested` audit event with a bounded, no-raw-content payload. A dry run and a rejected attempt mutate nothing.

Phase 10D made no database schema change, changed no ARCH-LOCKed contract, and added no dependency; `storytime.operator_rerun` was added to both import-linter contracts. The six Docker-free gates pass — 493 tests (27 new), ruff/mypy (85 source files, strict)/import-linter (2 contracts kept) clean, `storytime doctor` healthy; the legal-hallucination scanner returns zero violations. Phase 10D added no broker, worker, daemon, scheduler, server, dashboard, authentication, or cloud dependency, and the Phase 10C read-only queue is unaffected.

One documented, non-blocking design boundary (not an open issue): Phase 10D re-runs a failed run from the stage it failed at; re-running from an arbitrary earlier stage is intentionally out of scope, so `--from-stage` accepts only the run's failed stage.

Phase 10D is **locked**. Phase 10D.1 — State Preservation Cleanup + LLM Director Hardening — is **locked**. Phase 10E — Static HTML Operator Report Refinement — is an implementation candidate, pending review, not locked. Phase 9C remains optional/not scheduled.

## Phase 10E — Static HTML Operator Report Refinement (implementation output produced, reviewed SAFE WITH EDITS — Phase 10E.1 cleanup in progress — not locked) — 2026-05-25

Implementation round. Phase 10E refines the existing generated static HTML operator report under the locked Architecture Baseline Section 25 operator-experience law. GPT-5.5 and Gemini/Flash Light each reviewed the Phase 10E implementation artifact and returned **SAFE WITH EDITS** — implementation safe; three cleanup items required before lock (blocked_reason redaction, archive pollution, state-preservation sync). Phase 10E.1 addresses these cleanup items.

Phase 10E adds an executive status summary, Phase 10D rerun eligibility / action guidance, a bounded failure summary with operator guidance, a contextual command reference section, semantic status badges with CSS classes, an improved governance warning block (visually prominent, near the top of every page), embedded `<style>` per page for offline resilience, and improved responsive CSS layout.

Phase 10E made no database schema change, added no dependency, added no JavaScript, added no external CSS or assets, added no browser-side mutation controls, and changed no backend mutation behavior; 18 new report-safety tests and all six Docker-free gates pass. Phase 10E.2 final cleanup adds the full-phrase render fix and state-preservation sync. Phase 10F — Demo Seed Data / Golden Path Fixtures — has not started. Phase 9C remains optional/not scheduled.

## Phase 10E — Static HTML Operator Report Refinement (LOCKED) — 2026-05-25

Lock round. Phase 10E — Static HTML Operator Report Refinement — is locked, accepted, and canonical with explicit user approval, with the Phase 10E.1 / 10E.2 cleanup sequence accepted and the Phase 10E.2 normalized cleanup as canonical state. Lock archive: `storytime-phase10e2-final-cleanup-v2-normalized.tar.gz`, SHA-256 `87fad92b2e0a919a81588f4c628ccfdf08860571fdc778c527d8fe93c30b7dec`.

The Phase 10E.1 / 10E.2 cleanup sequence resolved the three review findings (raw `blocked_reason` redaction to the required safe wording, archive hygiene, and state-preservation synchronization). The refined static operator report remains a local, static, read-only artifact: no JavaScript, no external assets, no browser-side mutation controls, no backend behavior change, no database schema change, no new dependency. Phase 10F — Demo Seed Data / Golden Path Fixtures — has not started before the Phase 10F implementation round below.

## Phase 10F — Demo Seed Data / Golden Path Fixtures (implementation output produced — pending review — not locked) — 2026-05-25

Implementation round. Phase 10F is demo-readiness / fixture-design work under the locked Architecture Baseline Section 25 operator-experience law. Per the Phase Closure Protocol it is implementation output, not a locked phase: it awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval.

Phase 10F adds the `demo/` directory — `demo/seed/` (four original CC0 demo seed texts plus schema-valid source manifests: demo-golden-path, demo-retryable-failure, demo-governance-blocked, demo-needs-review), `demo/governance/demo-blocked-sources.yaml` (a demo-only blocked-source deny-list), and `demo/fixtures/` (an index plus six fixture definitions, scenarios STF-10F-01 through STF-10F-06). It adds the `docs/demo.md` operator demo runbook and `tests/test_demo_fixtures.py` (37 fixture shape / safety / behaviour tests).

The six scenarios cover the successful golden path, a retryable technical failure, a governance-blocked source, a needs-review / approval-gate run, a rerun-requested run, and a completed-after-rerun run. Every fixture drives the real existing pipeline, operator report, failure queue, Trust Envelope governance, and `storytime rerun` command. The governance-blocked scenario uses the existing `STORYTIME_BLOCKED_SOURCES` mechanism (§24.9) to supply a demo-only deny-list for one run, changing no enforcement code and no committed configuration. The needs-review fixture uses the operator text approval gate and documents that a governance `NEEDS_REVIEW` decision is not reachable through the normal local manifest path.

Phase 10F added no product feature, no UI, no server, no dashboard, no browser mutation control, no JavaScript, no external assets, no generated audio, no large binary artifact, no runtime database or cache artifact, no new dependency, no database schema change, and no change to pipeline / `storytime rerun` / Trust Envelope enforcement behaviour. 37 new tests and all six Docker-free quality gates pass — 549 tests, ruff/mypy (85 source files, strict)/import-linter (2 contracts kept) clean, `storytime doctor` healthy; the legal-hallucination scanner returns zero violations. The operator demo runbook is `docs/demo.md`. Phase 10G — Portfolio Narrative / Phase 10 Closure — has not started. Phase 9C remains optional/not scheduled.

## Phase 10F — Demo Seed Data / Golden Path Fixtures (LOCKED) — 2026-05-25

Lock round. Phase 10F — Demo Seed Data / Golden Path Fixtures — is locked, accepted, and canonical with explicit user approval. Lock archive: `storytime-phase10f-demo-seed-data-golden-path-fixtures.tar.gz`, SHA-256 `e060570a94fb19f790c539542b3ef7445111430bc308668675548f66fa48df55`.

Phase 10F added the `demo/` directory — `demo/seed/` (four original CC0 demo seed texts plus schema-valid source manifests), `demo/governance/demo-blocked-sources.yaml` (a demo-only blocked-source deny-list), and `demo/fixtures/` (an index plus six fixture definitions, scenarios STF-10F-01 through STF-10F-06) — together with the `docs/demo.md` operator demo runbook and `tests/test_demo_fixtures.py`. The six scenarios cover the successful golden path, a retryable technical failure, a governance-blocked source, a needs-review / approval-gate run, a rerun-requested run, and a completed-after-rerun run. Every fixture drives the real existing pipeline, operator report, failure queue, Trust Envelope governance, and `storytime rerun` command. Phase 10F added no product feature, no UI, no server, no dashboard, no browser mutation control, no JavaScript, no external assets, no generated audio, no new dependency, no database schema change, and no change to pipeline / `storytime rerun` / Trust Envelope enforcement behaviour. Phase 10F completed the Phase Closure Protocol — implementation, GPT-5.5 review, Gemini critique, and explicit user approval — and was locked. Phase 10G — Portfolio Narrative / Phase 10 Closure — has not started before the Phase 10G implementation round below. Phase 9C remains optional/not scheduled.

## Phase 10G — Portfolio Narrative / Phase 10 Closure (implementation output produced — pending review — not locked) — 2026-05-25

Implementation round. Phase 10G is a documentation, portfolio-narrative, demo-explanation, and Phase 10 closure round under the locked Architecture Baseline Section 25 operator-experience law. Per the Phase Closure Protocol it is implementation output, not a locked phase: it awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 10 is not marked closed by this round — Phase 10 closes only after the Phase 10G review and explicit user approval.

Phase 10G turns the completed Phase 10 operator-experience layer into a clear, honest, professional demo/portfolio story and prepares Phase 10 for closure. It adds eight documents under `docs/`: `portfolio-narrative.md`, `demo-script.md`, `operator-experience-walkthrough.md`, `command-reference.md`, `known-limitations.md`, `observability-governance-talking-points.md`, `phase10-acceptance-checklist.md`, and `screenshot-instructions.md`. The portfolio narrative explains the local-first architecture, the operator-controlled workflow, the Trust Envelope governance posture, the static HTML operator report, the failure queue, the governed rerun command, the demo seed data / golden-path fixtures, observability-native thinking, auditability, and privacy/redaction discipline — and is explicit that StoryTime is not a production SaaS dashboard, a multi-user system, a cloud-hosted product, a fully automated content platform, a legal-advice engine, or a commercial TTS platform. The demo script uses only commands that exist in the current CLI. The command reference labels every command read-only or state-changing and makes the mutation boundary explicit. The Phase 10 acceptance checklist verifies the operator baseline, the refined static report, the failure queue, the governed rerun command, bounded/audited mutation, the safe governance-blocked wording, the demo fixtures and runbook, scope discipline, and state-preservation synchronization.

Phase 10G is documentation-first: no application code changed. It added no product feature, no UI, no server, no dashboard, no browser mutation control, no JavaScript, no external assets, no generated audio, no screenshots/images/binary portfolio assets, no PowerPoint/PDF/slide deck, no new dependency, no database schema change, and no change to pipeline / `storytime rerun` / Trust Envelope enforcement behaviour. The State Preservation Bundle was synchronized — `LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/canonical-state.md`, `docs/phase-history.md`, `docs/open-issues.md`, `docs/verification-log.md`, `docs/artifact-manifest.md`, and `docs/roundtable-import-bridge.md` now record Phase 10F as locked and Phase 10G as an implementation candidate pending review.

All six Docker-free quality gates pass — 549 tests, ruff/mypy (85 source files, strict)/import-linter (2 contracts kept) clean, `storytime doctor` healthy; the legal-hallucination scanner returns zero violations. Phase 11 has not started. Phase 9C remains optional/not scheduled.

## Phase 10G — Portfolio Narrative / Phase 10 Closure (LOCKED — Phase 10 CLOSED) — 2026-05-25

Lock round. Phase 10G — Portfolio Narrative / Phase 10 Closure — is locked, accepted, and canonical with explicit user approval. **With Phase 10G locked, Phase 10 — Product UI / Operator Experience — is formally CLOSED.** Locked artifact: `storytime-phase10g1-uvlock-reversion-cleanup.tar.gz`, SHA-256 `8a0cc9a5b6426a291bec3a793e41501c7d3492187dd48b4f7729ea95e501a0c1`.

Phase 10G was the documentation, portfolio-narrative, demo-explanation, and Phase 10 closure round. It added eight Phase 10 portfolio/closure documents under `docs/` (`portfolio-narrative.md`, `demo-script.md`, `operator-experience-walkthrough.md`, `command-reference.md`, `known-limitations.md`, `observability-governance-talking-points.md`, `phase10-acceptance-checklist.md`, `screenshot-instructions.md`) and synchronized the State Preservation Bundle. It was documentation-first: no application code changed; no product feature, UI, server, JavaScript, generated audio, screenshots/binary assets, new dependency, database schema change, or change to pipeline / `storytime rerun` / Trust Envelope enforcement behaviour.

Phase Closure Protocol record: GPT-5.5 Phase 10G review PASS; Gemini Phase 10G review SAFE WITH EDITS (one required cleanup — verify/revert `uv.lock` to the exact Phase 10F state). The Phase 10G.1 cleanup round completed that cleanup — the suspected `uv.lock` drift proved to be a false positive (`uv.lock` was byte-for-byte identical across Phase 10F, Phase 10G, and Phase 10G.1; Phase 10G.1 explicitly copied the Phase 10F `uv.lock` into the tree to guarantee identity, and only `docs/artifact-manifest.md` and `docs/verification-log.md` bookkeeping changed from 10G to 10G.1). GPT-5.5 Phase 10G.1 verification PASS; Gemini Phase 10G.1 final verification SAFE TO LOCK. The user locked Phase 10G with explicit approval. At lock the six Docker-free gates passed — 549 tests, ruff/mypy (85 source files, strict)/import-linter (2 contracts kept) clean, `storytime doctor` healthy; the legal-hallucination scanner returns zero violations.

The Phase 10G lock and Phase 10 closure were synchronized into the State Preservation Bundle by the Post-Phase-10 Closure State Synchronization round — a governance/state-document synchronization task that updated the first-read current-state docs to record the already-approved lock/closure decision, changing no `pyproject.toml`, `uv.lock`, `src/`, or `tests/` content and adding no product behaviour. That sync produced the artifact `storytime-post-phase10-closure-state-sync.tar.gz`.

With Phase 10G locked, every Phase 10 sub-phase (10A, 10B, 10C, 10C.1, 10D, 10D.1, 10E with the 10E.1 / 10E.2 cleanup sequence, 10F, and 10G) is locked, and **Phase 10 — Product UI / Operator Experience — is formally CLOSED**. The next phase is **Phase 11 — Release Candidate Hardening**, which has **not started**. Phase 9C remains optional/not scheduled.

## Phase 11A — Release Candidate Hardening Baseline (implementation output produced — pending review — not locked) — 2026-05-25

Implementation round. Phase 11A is the first subphase of Phase 11 — Release Candidate Hardening. Per the Phase Closure Protocol it is implementation output, not a locked phase: it awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 11A does not mark Phase 11 complete and does not start Phase 11B, 11C, 11D, or Phase 12.

The round began from `storytime-post-phase10-roundtable-historical-backfill.tar.gz` (SHA-256 `367e647c46aa6e4fd039369da30859b11ca783249569df291343db133ef4cfdd`), the locked Post-Phase-10 Historical State Reconciliation artifact and the last locked work item before Phase 11.

Phase 11A is a documentation-first release-candidate hardening round. It audits and documents the repository's non-feature surfaces so the later Phase 11 subphases can proceed from a stable, understandable base. It adds seven `docs/` hardening documents: `release-candidate-hardening.md` (the release-candidate hardening baseline overview, including the artifact-hygiene and known-limitations baselines and the dependency policy), `phase11-plan.md` (the Phase 11A–11D subphase decomposition), `local-setup-runbook.md` (step-by-step local setup from a fresh clone to a verified environment), `fresh-clone-checklist.md` (the fresh-clone path condensed to a checklist), `rc-validation-checklist.md` (the six canonical Docker-free validation commands and their expected results), `security-secrets-checklist.md` (the local-first security and secrets hygiene baseline), and `demo-reproducibility-checklist.md` (how a reviewer reproduces the Phase 10F / 10G demo fixtures without generated audio or external APIs). It synchronizes the State Preservation Bundle — `LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/canonical-state.md`, this `docs/phase-history.md`, `docs/artifact-manifest.md`, `docs/verification-log.md`, `docs/open-issues.md`, and `docs/roundtable-import-bridge.md` — to record the Post-Phase-10 Historical State Reconciliation as the last locked work item and Phase 11A as the current implementation candidate.

Phase 11A is documentation-first: no application code changed. It added no product feature, no UI, no server, no dashboard, no browser mutation control, no JavaScript, no external assets, no generated audio, no screenshots/images/binary assets, no PowerPoint/PDF/slide deck, no new dependency, no database schema change, and no change to pipeline / `storytime rerun` / Trust Envelope enforcement behaviour. `pyproject.toml`, `uv.lock`, the `src/` tree, and the `tests/` tree are byte-for-byte unchanged from the source artifact. `docs/known-limitations.md` is intentionally left unchanged — it is a locked Phase 10G deliverable whose phase-status section is self-scoped and already defers to `docs/handoff-state.md`.

All six Docker-free quality gates pass — 549 tests, ruff/mypy (85 source files, strict)/import-linter (2 contracts kept) clean, `storytime doctor` healthy; the legal-hallucination scanner (run inside the pytest suite) returns zero violations. Phase 11B, 11C, 11D, and Phase 12 have not started. Phase 9C remains optional/not scheduled.

## Phase 11A — Release Candidate Hardening Baseline (LOCKED / ACCEPTED / CANONICAL — 2026-05-25)

Lock closure. Phase 11A — Release Candidate Hardening Baseline — is locked, accepted, and canonical with explicit user approval. It is the last locked phase. Locked artifact: `storytime-phase11a-release-candidate-hardening-baseline.tar.gz`, SHA-256 `664f8ba4ae90cf6a98ccc7d20369e690eac74497ab78f2b7067f0aac2079a7aa`.

Phase 11A — the first subphase of Phase 11 — Release Candidate Hardening — was a documentation-first hardening round that audited and documented the repository's non-feature surfaces and added seven `docs/` hardening documents (`release-candidate-hardening.md`, `phase11-plan.md`, `local-setup-runbook.md`, `fresh-clone-checklist.md`, `rc-validation-checklist.md`, `security-secrets-checklist.md`, `demo-reproducibility-checklist.md`). It added no product feature, no UI, no server, no JavaScript, no generated audio, no new dependency, and no database schema change, and changed no `pyproject.toml`, `uv.lock`, `src/`, or `tests/` content. Phase 11A completed the Phase Closure Protocol and was locked with explicit user approval. This lock-closure entry is recorded into the append-only round log by the Phase 11B round as part of its state synchronization; the Phase 11A implementation-output entry above is preserved as written.

**Current state after this lock (Phase 11A):** Phase 10A–10G all locked; **Phase 10 CLOSED**; the Post-Phase-10 Historical State Reconciliation was the last locked work item before Phase 11; **Phase 11A — Release Candidate Hardening Baseline — locked (the last locked phase)**. Phase 11B has not started before the Phase 11B round below. Phase 9C remains optional/not scheduled.

## Phase 11B — Fresh Clone / Operator Reproducibility (implementation candidate — pending review — not locked — 2026-05-25)

Implementation round. Phase 11B is the second subphase of Phase 11 — Release Candidate Hardening. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 11B awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 11B does **not** mark Phase 11 complete and does **not** start Phase 11C, 11D, or Phase 12.

Phase 11B is a fresh-clone / operator reproducibility verification round. It took the locked Phase 11A documentation as a specification and verified it against reality. It extracted the locked Phase 11A artifact (SHA-256 `664f8ba4ae90cf6a98ccc7d20369e690eac74497ab78f2b7067f0aac2079a7aa`, verified on extraction) into a clean tree, walked the documented setup, validation, and demo paths exactly as written, and confirmed they reproduce the Phase 11A baseline. The six Docker-free quality gates were re-run from the clean extraction and passed (549 tests, ruff clean, mypy clean over 85 source files strict, import-linter 2/2 kept, `storytime doctor` healthy); the documented operator commands — `storytime version`, `storytime --help`, `storytime validate-manifest`, the golden-path `storytime run --auto-approve`, `storytime status`, `storytime report generate`, and the `tests/test_demo_fixtures.py` integrity tests — all ran as documented.

Phase 11B adds two reproducibility documents: `docs/operator-reproducibility-checklist.md` (the step-by-step verification path from a clean checkout to a verified environment, paired with the reference results Phase 11B observed) and `docs/fresh-clone-troubleshooting.md` (the common fresh-clone setup failures and the safe response to each). It refines the Phase 11A reproducibility documents — `phase11-plan.md` (11A marked locked, 11B marked the current round), `fresh-clone-checklist.md`, `local-setup-runbook.md`, `rc-validation-checklist.md`, `demo-reproducibility-checklist.md`, and `release-candidate-hardening.md` (cross-references and Phase 11B verification notes). It aligns the `README.md` Setup command with the canonical `uv sync --frozen --extra dev` form already used by every release-candidate validation document — a documentation-consistency fix that introduces no behaviour change — and adds a README index of the release-candidate hardening and reproducibility documents. It synchronizes the State Preservation Bundle.

Validation consistency was checked across `README.md`, `docs/local-setup-runbook.md`, `docs/fresh-clone-checklist.md`, `docs/rc-validation-checklist.md`, `docs/command-reference.md`, and `docs/verification-log.md`: the six-gate command list and ordering are consistent; the one divergence found — the `README.md` Setup line previously used `uv sync --extra dev` while every release-candidate validation document uses `uv sync --frozen --extra dev` — was corrected by aligning `README.md` to the `--frozen` form. The documented paths rely on no network access beyond the single `uv sync` package download, require no secrets, and do not imply that generated audio or screenshots exist.

Confirmed constraints: no new product feature; no UI; no server; no dashboard; no browser mutation control; no JavaScript; no external assets; no CDN; no generated audio; no screenshots/images/PDF/PowerPoint/binary assets; no new dependency; no database schema change; no change to pipeline behaviour, `storytime rerun` behaviour, or Trust Envelope enforcement; no ARCH-LOCKed contract change; no helper scripts added (documentation-first removed the ambiguity — the existing `make` targets and the explicit `uv run` gate commands already cover verification). `pyproject.toml`, `uv.lock`, the `src/` tree, and the `tests/` tree are byte-for-byte unchanged from the source artifact. Phase 11B is documentation-first; no application code was changed.

Confirmed gate results: 549 tests passing, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy; the legal-hallucination scanner (run inside the pytest suite, covering the two new documents and the updated docs) returns zero violations.

**Current state after this round (Phase 11B):** Phase 10A–10G all locked; **Phase 10 CLOSED**; the Post-Phase-10 Historical State Reconciliation was the last locked work item before Phase 11; **Phase 11A — Release Candidate Hardening Baseline — locked (the last locked phase)**; Phase 11 — Release Candidate Hardening — is in progress; Phase 11B — Fresh Clone / Operator Reproducibility — is an implementation candidate, pending review, **not locked**. Phase 11C, 11D, and Phase 12 have not started. Phase 9C remains optional/not scheduled.

## Phase 11B — Fresh Clone / Operator Reproducibility (LOCKED / ACCEPTED / CANONICAL — 2026-05-25)

Lock closure. Phase 11B — Fresh Clone / Operator Reproducibility — is locked, accepted, and canonical with explicit user approval. It is the last locked phase. Locked artifact: `storytime-phase11b-fresh-clone-operator-reproducibility.tar.gz`, SHA-256 `08b72f2833da9adf3b8acc1f3170334eb7c5f998e19263838efbce2f571cc73f`.

Phase 11B — the second subphase of Phase 11 — Release Candidate Hardening — was a fresh-clone / operator reproducibility verification round that extracted the locked Phase 11A artifact into a clean tree, confirmed the documented setup, validation, and demo paths reproduce the Phase 11A baseline, added two reproducibility documents (`docs/operator-reproducibility-checklist.md`, `docs/fresh-clone-troubleshooting.md`), refined the Phase 11A reproducibility documents, and aligned the `README.md` setup command with the canonical `uv sync --frozen --extra dev` form. It added no product feature, no UI, no server, no JavaScript, no generated audio, no new dependency, and no database schema change, and changed no `pyproject.toml`, `uv.lock`, `src/`, or `tests/` content. Phase 11B completed the Phase Closure Protocol and was locked with explicit user approval. This lock-closure entry is recorded into the append-only round log by the Phase 11C round as part of its state synchronization; the Phase 11B implementation-output entry above is preserved as written.

**Current state after this lock (Phase 11B):** Phase 10A–10G all locked; **Phase 10 CLOSED**; the Post-Phase-10 Historical State Reconciliation was the last locked work item before Phase 11; Phase 11A locked; **Phase 11B — Fresh Clone / Operator Reproducibility — locked (the last locked phase)**. Phase 11C has not started before the Phase 11C round below. Phase 9C remains optional/not scheduled.

## Phase 11C — Failure-Mode / Regression Hardening (implementation candidate — pending review — not locked — 2026-05-25)

Implementation round. Phase 11C is the third subphase of Phase 11 — Release Candidate Hardening. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 11C awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 11C does **not** mark Phase 11 complete and does **not** start Phase 11D or Phase 12.

Phase 11C is a failure-mode and regression-hardening round. It answers the release-candidate question "what breaks, how do we know, and can we prove the system fails safely?". It inventories the highest-risk failure and regression paths that already exist in StoryTime — the operator failure / review queue, retry / re-run behaviour, governance-blocked content, static HTML report safety, demo fixture invariants, the static legal-hallucination gate, operator-safe failure messages, state preservation around failed runs, and traceability of blocked / failed / retried stages — records for each one which tests and validation gates protect it, and documents how a local operator should respond to a failure without bypassing governance or deleting state.

Phase 11C took the locked Phase 11B artifact (`storytime-phase11b-fresh-clone-operator-reproducibility.tar.gz`, SHA-256 `08b72f2833da9adf3b8acc1f3170334eb7c5f998e19263838efbce2f571cc73f`, verified on extraction) as its source. It added four `docs/` documents — `failure-mode-regression-hardening.md` (the Phase 11C overview), `regression-risk-register.md` (the risk inventory R1–R9, each with a coverage status), `failure-mode-test-matrix.md` (the regression coverage map from each risky path to the tests and gates that protect it), and `operator-failure-response.md` (the operator failure-response playbook). It added one focused regression test module, `tests/test_failure_mode_regression.py` — genuine new coverage that converts the project's state-documentation discipline rule into an executable guard: the module asserts that the State Preservation Bundle keeps Phase 11C marked a pending-review implementation candidate, keeps Phase 11B as the last locked phase, never claims Phase 11D or Phase 12 has started or locked, and still retains the append-only historical lock records. Phase 11C synchronized the State Preservation Bundle.

The existing test suite was confirmed to already cover most failure-mode invariants directly — the raw-`blocked_reason` redaction and the safe governance wording, the air-gapped / non-interactive / no-JavaScript / no-external-asset properties of the static report, the read-only failure queue, the governed re-run rejection codes and bounded audited apply path, the demo-fixture small/text-based/no-secret invariants, and the legal-hallucination scanner — and `failure-mode-test-matrix.md` records exactly which tests protect each path. No source change was required: every risky path either is test-covered or is explicitly documented as documented-only with the reason.

Confirmed constraints: no new product feature; no UI; no server; no dashboard; no browser mutation control; no JavaScript; no external assets; no CDN; no generated audio; no screenshots/images/PDF/PowerPoint/binary assets; no new dependency; no database schema change; no change to pipeline behaviour, `storytime rerun` behaviour, or Trust Envelope enforcement; no ARCH-LOCKed contract change; no source change. `pyproject.toml`, `uv.lock`, and the `src/` tree are byte-for-byte unchanged from the source artifact. The only `tests/` change is the added regression module `tests/test_failure_mode_regression.py`; no existing test was modified. `docs/known-limitations.md` is intentionally left unchanged — it is a locked Phase 10G deliverable whose phase-status section is self-scoped and already defers to `docs/handoff-state.md`.

Confirmed gate results: 580 tests passing, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy; the legal-hallucination scanner (run inside the pytest suite, covering the four new documents and the new test module) returns zero violations.

**Current state after this round (Phase 11C):** Phase 10A–10G all locked; **Phase 10 CLOSED**; the Post-Phase-10 Historical State Reconciliation was the last locked work item before Phase 11; Phase 11A locked; **Phase 11B — Fresh Clone / Operator Reproducibility — locked (the last locked phase)**; Phase 11 — Release Candidate Hardening — is in progress; Phase 11C — Failure-Mode / Regression Hardening — is an implementation candidate, pending review, **not locked**. Phase 11D and Phase 12 have not started. Phase 9C remains optional/not scheduled.

## Phase 11C — Failure-Mode / Regression Hardening (LOCKED / ACCEPTED / CANONICAL — 2026-05-25)

Lock closure. Phase 11C — the third subphase of Phase 11 — Release Candidate Hardening — was a failure-mode and regression-hardening round that inventoried the highest-risk failure and regression paths that already exist in StoryTime, recorded which tests and validation gates protect each one, documented operator failure-response, added four `docs/` documents (`failure-mode-regression-hardening.md`, `regression-risk-register.md`, `failure-mode-test-matrix.md`, `operator-failure-response.md`), and added one focused regression test module (`tests/test_failure_mode_regression.py`, the state-documentation discipline guard). It added no product feature, no UI, no server, no JavaScript, no generated audio, no new dependency, and no database schema change, and changed no `pyproject.toml`, `uv.lock`, or `src/` content; the only `tests/` change was the new regression module. Phase 11C completed the Phase Closure Protocol and was locked with explicit user approval. The locked Phase 11C artifact is `storytime-phase11c-failure-mode-regression-hardening.tar.gz`, SHA-256 `2dd31442e62c13241a64d10c2d117aefedc3b9c633ad5ea5d1fa94cfaad7d57b`. This lock-closure entry is recorded into the append-only round log by the Phase 11D round as part of its state synchronization; the Phase 11C implementation-output entry above is preserved as written.

**Current state after this lock (Phase 11C):** Phase 10A–10G all locked; **Phase 10 CLOSED**; the Post-Phase-10 Historical State Reconciliation was the last locked work item before Phase 11; Phase 11A locked; Phase 11B locked; **Phase 11C — Failure-Mode / Regression Hardening — locked (the last locked phase)**. Phase 11D has not started before the Phase 11D round below. Phase 9C remains optional/not scheduled.

## Phase 11D — Release Candidate Evidence Pack (implementation candidate — pending review — not locked — 2026-05-25)

Implementation round. Phase 11D is the fourth and final planned subphase of Phase 11 — Release Candidate Hardening. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 11D awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 11D does **not** mark Phase 11 complete and does **not** start Phase 12.

Phase 11D is an evidence, closure-readiness, and proof-consolidation round. It answers the release-candidate question "can we prove this release candidate is ready to show, explain, hand off, and package?" by consolidating the release-candidate evidence produced by Phases 11A, 11B, and 11C into a reviewer-facing index. It is not product development.

Phase 11D took the locked Phase 11C artifact (`storytime-phase11c-failure-mode-regression-hardening.tar.gz`, SHA-256 `2dd31442e62c13241a64d10c2d117aefedc3b9c633ad5ea5d1fa94cfaad7d57b`, verified on extraction) as its source. It added four `docs/` documents — `release-candidate-evidence-pack.md` (the Phase 11D overview and the release-candidate evidence index), `final-validation-summary.md` (the canonical validation results), `phase11-closure-checklist.md` (what each Phase 11 subphase contributed and the conditions for an explicit Phase 11 closure decision), and `phase12-readiness-handoff.md` (what Phase 12 may safely do) — refreshed the status notes in `docs/phase11-plan.md`, `docs/release-candidate-hardening.md`, and `docs/rc-validation-checklist.md`, and synchronized the State Preservation Bundle. It re-ran the six Docker-free validation gates against the Phase 11C artifact with no source, dependency, or test change applied, and recorded the results.

The existing test suite was confirmed to already cover the release-candidate invariants the evidence index references; no new test was required and none was added. No source behaviour changed; no dependency or lockfile changed; no generated or runtime artifact was created.

Confirmed constraints: no new product feature; no UI; no server; no dashboard; no browser mutation control; no JavaScript; no external assets; no CDN; no generated audio; no screenshots/images/PDF/PowerPoint/binary assets; no new dependency; no database schema change; no change to pipeline behaviour, `storytime rerun` behaviour, or Trust Envelope enforcement; no ARCH-LOCKed contract change; no source change; no test change. `pyproject.toml`, `uv.lock`, the `src/` tree, and the `tests/` tree are byte-for-byte unchanged from the source artifact. Phase 11D is documentation/evidence consolidation only. `docs/known-limitations.md` is intentionally left unchanged — it is a locked Phase 10G deliverable whose phase-status section is self-scoped and already defers to `docs/handoff-state.md`, the same decision Phase 11C recorded.

Confirmed gate results: 580 tests passing, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy; the legal-hallucination scanner (run inside the pytest suite, covering the four new documents) returns zero violations.

**Current state after this round (Phase 11D):** Phase 10A–10G all locked; **Phase 10 CLOSED**; the Post-Phase-10 Historical State Reconciliation was the last locked work item before Phase 11; Phase 11A locked; Phase 11B locked; **Phase 11C — Failure-Mode / Regression Hardening — locked (the last locked phase)**; Phase 11 — Release Candidate Hardening — is in progress; Phase 11D — Release Candidate Evidence Pack — is an implementation candidate, pending review, **not locked**. Phase 12 has not started. Phase 9C remains optional/not scheduled.

## Phase 11D — Release Candidate Evidence Pack (LOCKED / ACCEPTED / CANONICAL — Phase 11 CLOSED — 2026-05-26)

Lock closure recorded out-of-band. Phase 11D — the fourth and final planned subphase of Phase 11 — Release Candidate Hardening — was an evidence, closure-readiness, and proof-consolidation round that consolidated the release-candidate evidence produced by Phases 11A, 11B, and 11C into a reviewer-facing index, recorded the canonical validation results, prepared a Phase 11 closure checklist, and wrote a Phase 12 readiness handoff. It added four `docs/` documents (`release-candidate-evidence-pack.md`, `final-validation-summary.md`, `phase11-closure-checklist.md`, `phase12-readiness-handoff.md`) and synchronized the State Preservation Bundle. It added no product feature, no UI, no server, no JavaScript, no generated audio, no new dependency, and no database schema change, and changed no `pyproject.toml`, `uv.lock`, `src/`, or `tests/` content.

Phase 11D completed the Phase Closure Protocol out-of-band, in the GPT/Gemini review workflow: GPT-5.5 Phase 11D review PASS; Gemini Phase 11D review SAFE TO LOCK; no required edits. The user, as final decision-maker, then locked Phase 11D and made the explicit Phase 11 closure decision, and authorized Phase 12. **With Phase 11D locked, Phase 11 — Release Candidate Hardening — is formally CLOSED.** The locked Phase 11D artifact is `storytime-phase11d-release-candidate-evidence-pack.tar.gz`, SHA-256 `07a3973e3dbb69d760ff2c330418f85101c2afa1464fc0eed752fc7053894d94`. This out-of-band closure was a user/mediator decision supplied to the Phase 12A round; it was not contained in the Phase 11D archive itself, which captured the pre-lock implementation-candidate state. This lock-closure entry is recorded into the append-only round log by the Phase 12A round as part of its state synchronization; the Phase 11D implementation-output entry above is preserved as written. The Phase 12A round did not re-perform the GPT-5.5 / Gemini reviews. Validation basis at lock: 580 tests passing, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy, legal-hallucination scanner zero violations.

**Current state after this lock (Phase 11D / Phase 11 closure):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 11D is the last locked phase. Phase 12 — Portfolio / SE Demo Packaging — is started in the round below. Phase 9C remains optional/not scheduled.

## Phase 12 — Portfolio / SE Demo Packaging STARTED / Phase 12A — Portfolio / SE Demo Packaging Baseline (implementation candidate — pending review — not locked — 2026-05-26)

Phase start and implementation round. With Phase 11 closed, the user authorized **Phase 12 — Portfolio / SE Demo Packaging**, and Phase 12 is **STARTED**. Phase 12A — Portfolio / SE Demo Packaging Baseline — is the first subphase of Phase 12. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 12A awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 12A does **not** lock Phase 12A, does **not** close Phase 12, and does **not** start Phase 12B or any later Phase 12 subphase.

Phase 12A is a documentation and portfolio-packaging round that explains and packages the already-locked Phases 0–11 — it builds no product behaviour. It makes StoryTime explainable as a Solutions Engineer / observability / OpenTelemetry portfolio project. It added four `docs/` documents — `portfolio-overview.md` (the plain-English portfolio overview and reviewer entry point), `solutions-engineer-narrative.md` (30-second / 2-minute / deep pitches plus business, observability, OpenTelemetry, governance, and failure-mode framings, and a "what not to claim" section), `portfolio-demo-script.md` (a narrated, reviewer-facing demo walkthrough that defers to `docs/demo.md` as the authoritative command source), and `interview-talking-points.md` (concise, study-friendly talking points) — refined `README.md` with a portfolio-facing "For reviewers" section and an updated phase table, and synchronized the State Preservation Bundle. The portfolio documents are honest about scope: no claim of production deployment, users, an SLA, cloud hosting, active alerting, an error-budget policy, integration with any named commercial observability vendor, a legal determination, or a rights-clearance capability.

Confirmed constraints: no new product feature; no UI; no server; no dashboard; no browser mutation control; no JavaScript; no external assets; no CDN; no generated audio; no screenshots/images/PDF/PowerPoint/binary assets; no new dependency; no database schema change; no change to pipeline behaviour, `storytime rerun` behaviour, or Trust Envelope enforcement; no ARCH-LOCKed contract change; no source change. `pyproject.toml`, `uv.lock`, and the `src/` tree are byte-for-byte unchanged from the source artifact. The only `tests/` change is a narrow, explicitly authorized advance of the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 12A current-state expectations (premature Phase 12A lock, premature Phase 12 closure, and premature Phase 12B-or-later start are all guarded; historical lock-record coverage is strengthened, not weakened).

Confirmed gate results: 585 tests passing (580 from the closed Phase 11 baseline plus 5 net from the authorized advance of the state-discipline guard), ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy; the legal-hallucination scanner (run inside the pytest suite, covering the four new documents) returns zero violations.

**Current state after this round (Phase 12 start / Phase 12A):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 11D — Release Candidate Evidence Pack — is the last locked phase; **Phase 12 — Portfolio / SE Demo Packaging — is STARTED**; Phase 12A — Portfolio / SE Demo Packaging Baseline — is an implementation candidate, pending review, **not locked**. Phase 12B and later subphases of Phase 12 have not started. Phase 9C remains optional/not scheduled.

## Phase 12A.1 — State-Hygiene Cleanup (bounded cleanup of the Phase 12A round — 2026-05-26)

Cleanup round. Phase 12A.1 is a narrow, documentation-only state-hygiene cleanup of the Phase 12A — Portfolio / SE Demo Packaging Baseline round. It is **not** a new phase and **not** a lock; Phase 12A remains the current implementation candidate, pending review, not locked.

A pre-lock review of the Phase 12A artifact (GPT-5.5) found one minor state-hygiene issue: some historical notes inside the living / current-state documents still carried stale present-tense phrasing — describing Phase 11A, Phase 11B, or Phase 11C as "the last locked phase", and pointing the reader to a superseded "Phase 11D note above" / "Phase 11C note above" / "Phase 11B note above" for current status. The authoritative top-of-file current-state entries were already correct; the stale phrasing sat only inside older point-in-time notes and could mislead a cold session.

Phase 12A.1 took the Phase 12A artifact (`storytime-phase12a-portfolio-se-demo-packaging-baseline.tar.gz`, SHA-256 `54909ee9da9ea20c0a416de733e2a7d1e1b4722ef3799e21c374698be778ffaa`) as its source. It revised the stale phrasing in the historical notes of the four living / current-state documents — `LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, and `docs/roadmap.md` — so those notes now read explicitly as superseded point-in-time records: stale "is the last locked phase" wording became "was the last locked phase at that point in the project history"; stale "current status is in the Phase 11x note above" pointers now point to the Phase 12A current-state note; and the Phase 11A historical notes now record that Phase 11B, Phase 11C, and Phase 11D have since also been locked and Phase 11 is closed. A concise Phase 12A.1 cleanup note was prepended to the top of each of the four living documents. Remaining "is the last locked phase" wording was confirmed to refer only to Phase 11D, which is correct and current.

Confirmed constraints: documentation / state-hygiene wording only. No `src/`, no `tests/`, no `pyproject.toml`, no `uv.lock`, and no dependency change; no product, runtime, pipeline, `storytime rerun`, or Trust Envelope behaviour change; no ARCH-LOCKed contract change; no new product feature, UI, server, JavaScript, generated audio, screenshot, or binary asset. The append-only locked-decision documents `docs/canonical-state.md` and the round log in this `docs/phase-history.md` were not rewritten — this entry is a new append, and historical chronology is preserved throughout. The six Docker-free validation gates were re-run and remain green: 585 tests pass, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy, legal-hallucination scanner zero violations.

**Current state after this cleanup (Phase 12A.1):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 11D — Release Candidate Evidence Pack — is the last locked phase; **Phase 12 — Portfolio / SE Demo Packaging — is STARTED**; Phase 12A — Portfolio / SE Demo Packaging Baseline — remains an implementation candidate, pending review, **not locked**, with the Phase 12A.1 state-hygiene cleanup applied. Phase 12B and later subphases of Phase 12 have not started. Phase 9C remains optional/not scheduled.

---

## Phase 12A — Portfolio / SE Demo Packaging Baseline — LOCK (LOCKED / ACCEPTED / CANONICAL — 2026-05-26)

Lock closure. Phase 12A — Portfolio / SE Demo Packaging Baseline — the first subphase of Phase 12 — Portfolio / SE Demo Packaging — is locked, accepted, and canonical with explicit user approval. Phase 12A completed the Phase Closure Protocol: implementation, GPT-5.5 review, Gemini critique, the accepted Phase 12A.1 state-hygiene cleanup sub-round, and an explicit user lock decision.

The locked Phase 12A lineage is `storytime-phase12a-portfolio-se-demo-packaging-baseline.tar.gz` with the accepted Phase 12A.1 state-hygiene cleanup `storytime-phase12a1-state-hygiene-cleanup.tar.gz` (SHA-256 `5f9eca1cc8c2efb55d57f87becdc53cd0d8e514221947e445965232f608b621a`) folded into it. Phase 12A.1 is an accepted documentation-only cleanup sub-round folded into the Phase 12A lock lineage — it is not an independently locked phase.

The Phase 12A and Phase 12A.1 round entries earlier in this file are preserved as written and are superseded for status purposes by this lock-closure entry.

**Current state after this lock (Phase 12A):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; **Phase 12A — Portfolio / SE Demo Packaging Baseline — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — is STARTED** and not closed. Phase 12B has not started before the Phase 12B round below. Phase 9C remains optional/not scheduled.

---

## Phase 12B — Portfolio Evidence Pack / Reviewer Assets (implementation candidate — pending review — not locked — 2026-05-26)

Implementation round. Phase 12B is the second subphase of Phase 12 — Portfolio / SE Demo Packaging. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 12B awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 12B does **not** lock Phase 12B, does **not** close Phase 12, and does **not** start Phase 12C or any later Phase 12 subphase.

Phase 12B is a reviewer / evidence packaging round. It took the locked Phase 12A lineage artifact `storytime-phase12a1-state-hygiene-cleanup.tar.gz` (SHA-256 `5f9eca1cc8c2efb55d57f87becdc53cd0d8e514221947e445965232f608b621a`, verified on extraction) as its source. It added four `docs/` documents — `portfolio-evidence-index.md` (a claim-to-evidence index), `se-interview-evidence-matrix.md` (a Solutions-Engineer competency-to-evidence matrix with an honesty checklist), `demo-reviewer-checklist.md` (a reviewer wrapper over `docs/demo.md`, explicitly not a duplicate command script), and `portfolio-public-copy.md` (disciplined, non-hype public-facing copy with an honest "what it is not" scope statement) — lightly updated `README.md` to point reviewers to the new evidence documents, and synchronized the State Preservation Bundle.

Confirmed constraints: documentation / reviewer-asset packaging only. No new product feature, UI, server, dashboard, browser mutation control, JavaScript, external asset, CDN, generated audio, screenshot/image/PDF/PowerPoint/binary asset, new dependency, or database schema change; no change to pipeline behaviour, `storytime rerun`, or Trust Envelope enforcement; no ARCH-LOCKed contract change; no source change. `pyproject.toml`, `uv.lock`, and the `src/` tree are byte-for-byte unchanged from the source artifact. The only `tests/` change is the narrow, explicitly authorized §5 mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` to the Phase 12B current-state expectations (`_CURRENT_PHASE` → "phase 12b", `_LAST_LOCKED_PHASE` → "phase 12a", `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 12B lock, a premature Phase 12 closure, and a premature Phase 12C-or-later start). The guard is strengthened, not weakened — it additionally requires the Phase 12A lock record in the append-only history. The append-only locked-decision documents `docs/canonical-state.md` and the round log in this `docs/phase-history.md` were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

Confirmed gate results: 588 tests pass, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy, legal-hallucination scanner zero violations.

**Current state after this round (Phase 12B):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; **Phase 12A — Portfolio / SE Demo Packaging Baseline — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — is STARTED**; Phase 12B — Portfolio Evidence Pack / Reviewer Assets — is an implementation candidate, pending review, **not locked**. Phase 12C and later subphases of Phase 12 have not started. Phase 9C remains optional/not scheduled.

---

## Phase 12B.1 — State-Hygiene Cleanup (bounded cleanup of the Phase 12B round — not locked) — 2026-05-26

Cleanup round. Phase 12B.1 is a narrow, documentation-only state-hygiene cleanup of the Phase 12B — Portfolio Evidence Pack / Reviewer Assets round. It is **not** a new phase and **not** a lock; Phase 12B remains the current implementation candidate, pending review, not locked.

A pre-Gemini-review check of the Phase 12B artifact (GPT-5.5) found one minor state-hygiene issue: some historical notes inside the living / current-state documents still carried stale Phase 12A.1-era present-tense phrasing — "Phase 12A remains an implementation candidate pending review", "Phase 11D remains the last locked phase", "Phase 12B and later subphases have not started", and parentheticals describing Phase 12A as "the current implementation candidate". The authoritative top-of-file current-state entries (the Phase 12B notes) were already correct; the stale phrasing sat only inside older point-in-time notes and could mislead a cold session.

Phase 12B.1 took the Phase 12B artifact (`storytime-phase12b-portfolio-evidence-pack-reviewer-assets.tar.gz`, SHA-256 `dc7c0013a240e648f5a94f04871b86f45af3e152c923b949aad36beb7e6da8e5`) as its source. It revised the stale wording in the historical notes of the four living / current-state documents — `LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`, and `docs/roadmap.md` — so those notes now read explicitly as superseded point-in-time records (the Phase 12A.1 note body reframed to past tense; parentheticals corrected to "Phase 12A is locked, and Phase 12B is the current implementation candidate"). For the append-only-style log entries in `docs/artifact-manifest.md` and `docs/verification-log.md`, Phase 12B.1 added concise supersession notes to the affected historical entries rather than rewriting them. It fixed one stale parenthetical in `docs/open-issues.md`. A concise Phase 12B.1 cleanup note was prepended to each of the four living documents. The current state is unambiguous: Phase 12A LOCKED (with Phase 12A.1 folded into its lock lineage), Phase 12B implementation candidate / pending review / not locked, Phase 12C and later not started, Phase 12 STARTED and not closed.

Confirmed constraints: documentation / state-hygiene wording only. No `src/`, no `tests/`, no `pyproject.toml`, no `uv.lock`, and no dependency change; no product, runtime, pipeline, `storytime rerun`, or Trust Envelope behaviour change; no ARCH-LOCKed contract change; no new product feature, UI, server, JavaScript, generated audio, screenshot, or binary asset. The append-only locked-decision documents `docs/canonical-state.md` and the round log in this `docs/phase-history.md` were not rewritten — this entry is a new append, and historical chronology is preserved throughout. The six Docker-free validation gates were re-run and remain green: 588 tests pass, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy, legal-hallucination scanner zero violations.

**Current state after this cleanup (Phase 12B.1):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; **Phase 12A — Portfolio / SE Demo Packaging Baseline — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — is STARTED**; Phase 12B — Portfolio Evidence Pack / Reviewer Assets — remains an implementation candidate, pending review, **not locked**, with the Phase 12B.1 state-hygiene cleanup applied. Phase 12C and later subphases of Phase 12 have not started. Phase 9C remains optional/not scheduled.

## Phase 12B.2 — Phase 13 GUI Roadmap Preservation (bounded cleanup of the Phase 12B round — not locked) — 2026-05-26

Cleanup round. Phase 12B.2 is a narrow, documentation-only roadmap-preservation cleanup sub-round of the Phase 12B — Portfolio Evidence Pack / Reviewer Assets round. It is **not** a new phase and **not** a lock; Phase 12B remained the current implementation candidate, pending review, not locked, while it ran.

Phase 12B.2 preserved a future Operator GUI / Decoupled Frontend vision inside the repository so a cold LLM session can see it, without starting that work. It added one new documentation file, `docs/GUI_vision.md`, recording the user's GUI requirement and the architecture interpretation; added a Phase 13 — Operator GUI / Decoupled Frontend Vision — roadmap note to the body of `docs/roadmap.md` describing the planned 13A–13F decomposition; and prepended a current-state round note to `LLM_DIRECTOR.md`, `docs/handoff-state.md`, and `docs/roadmap.md`. Phase 13 is roadmap-preserved as future work only and has **not** started — no React, Vite, TypeScript, frontend directory, dependency, package file, or UI code was added. Phase 12B.2 changed no `src/`, `tests/`, `pyproject.toml`, `uv.lock`, dependency, or product/runtime behaviour, and no append-only locked decision; it preserved all historical chronology.

**Current state after this cleanup (Phase 12B.2):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; **Phase 12A — Portfolio / SE Demo Packaging Baseline — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — is STARTED**; Phase 12B — Portfolio Evidence Pack / Reviewer Assets — remained an implementation candidate, pending review, **not locked**, with the Phase 12B.1 and Phase 12B.2 cleanup sub-rounds applied. Phase 12C and later subphases of Phase 12 had not started. Phase 13 — Operator GUI / Decoupled Frontend Vision — roadmap-preserved only, not started. Phase 9C remains optional/not scheduled.

## Phase 12B.3 — Residual Living-Doc State-Wording Cleanup (bounded cleanup of the Phase 12B round — not locked) — 2026-05-26

Cleanup round. Phase 12B.3 is a narrow, documentation-only residual state-hygiene cleanup sub-round of the Phase 12B round, run after Phase 12B.2. It is **not** a new phase and **not** a lock; Phase 12B remained the current implementation candidate, pending review, not locked, while it ran.

Phase 12B.3 removed remaining stale present-tense historical wording that described Phase 12A as the current implementation candidate inside older Phase 11-era notes of the living / cold-session documents; those passages now point readers to the active Phase 12B current-state notes at the top of each living document. It changed no `src/`, `tests/`, `pyproject.toml`, `uv.lock`, dependency, frontend, GUI, runtime asset, or product/runtime behaviour, and no append-only locked decision; it preserved all historical chronology.

**Current state after this cleanup (Phase 12B.3):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; **Phase 12A — Portfolio / SE Demo Packaging Baseline — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — is STARTED**; Phase 12B — Portfolio Evidence Pack / Reviewer Assets — remained an implementation candidate, pending review, **not locked**, with the Phase 12B.1 / 12B.2 / 12B.3 cleanup sub-rounds applied. Phase 12C and later subphases of Phase 12 had not started. Phase 13 — Operator GUI / Decoupled Frontend Vision — roadmap-preserved only, not started. Phase 9C remains optional/not scheduled.

## Phase 12B — Portfolio Evidence Pack / Reviewer Assets — LOCK (LOCKED / ACCEPTED / CANONICAL — 2026-05-26)

Lock closure, recorded out-of-band. Phase 12B — Portfolio Evidence Pack / Reviewer Assets — the second subphase of Phase 12 — Portfolio / SE Demo Packaging — is locked, accepted, and canonical with explicit user approval. Phase 12B completed the Phase Closure Protocol: implementation, GPT-5.5 review, the accepted Phase 12B.1 state-hygiene cleanup, Phase 12B.2 Phase 13 GUI roadmap-preservation cleanup, and Phase 12B.3 residual living-doc state-wording cleanup sub-rounds, Gemini critique of the combined Phase 12B sequence (SAFE TO LOCK, no required edits), and an explicit user lock decision.

The locked Phase 12B lineage is `storytime-phase12b-portfolio-evidence-pack-reviewer-assets.tar.gz` with the accepted Phase 12B.1 / 12B.2 / 12B.3 cleanup sub-rounds folded into it; the folded lineage artifact is `storytime-phase12b3-residual-state-wording-cleanup.tar.gz` (SHA-256 `ce0fb2d1bea4eaa636be7796613f9a9aa56cba4b8bf34c0ae5440c3509de4a45`). Phase 12B.1, Phase 12B.2, and Phase 12B.3 are accepted documentation-only cleanup sub-rounds folded into the Phase 12B lock lineage — they are not independently locked phases.

This out-of-band closure was a user/mediator decision supplied to the Phase 12C round; it was not contained in the Phase 12B sequence archive itself, which captured the pre-lock implementation-candidate / cleanup-lineage state. This lock-closure entry is recorded into the append-only round log by the Phase 12C round as part of its state synchronization — the same after-the-fact lock-recording pattern used for Phase 11D and the Phase 12A lock. The Phase 12C round did not re-perform the GPT-5.5 / Gemini reviews. The Phase 12B, 12B.1, 12B.2, and 12B.3 round entries earlier in this file are preserved as written and are superseded for status purposes by this lock-closure entry. Validation basis at lock: 588 tests passing, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 contracts kept, `storytime doctor` healthy, legal-hallucination scanner zero violations.

**Current state after this lock (Phase 12B):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A locked; **Phase 12B — Portfolio Evidence Pack / Reviewer Assets — locked (the last locked phase)** (the accepted Phase 12B.1 / 12B.2 / 12B.3 cleanup sub-rounds folded into its lock lineage); **Phase 12 — Portfolio / SE Demo Packaging — is STARTED** and not closed. Phase 12C has not started before the Phase 12C round below. Phase 13 — Operator GUI / Decoupled Frontend Vision — is roadmap-preserved only and has not started. Phase 9C remains optional/not scheduled.

## Phase 12C — Portfolio Demo Narrative / Public Presentation Kit (implementation candidate — pending review — not locked — 2026-05-26)

Implementation round. Phase 12C is the third subphase of Phase 12 — Portfolio / SE Demo Packaging. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 12C awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 12C does **not** lock Phase 12C, does **not** close Phase 12, and does **not** start Phase 12D or any later Phase 12 subphase.

Phase 12C is a documentation-first portfolio-packaging round that converts the project's existing technical evidence into polished, reusable public-presentation assets — it builds on, and explains, the already-locked Phases 0–12B and adds no product behaviour. It took the locked Phase 12B sequence lineage artifact `storytime-phase12b3-residual-state-wording-cleanup.tar.gz` (SHA-256 `ce0fb2d1bea4eaa636be7796613f9a9aa56cba4b8bf34c0ae5440c3509de4a45`, verified on extraction) as its source. It added four `docs/` documents — `portfolio-demo-narrative.md` (a concise demo narrative: what StoryTime is, why it exists, the problem it demonstrates, why observability matters, what the operator sees, what the reviewer should notice, the SE / Dynatrace-style credibility mapping, and the intentional out-of-scope boundaries), `demo-talk-track.md` (a spoken walkthrough at 5-minute, 10-minute, and 20-minute lengths, with interviewer Q&A pivots and a "what to say if the demo cannot be run live" fallback), `interview-story-bank.md` (reusable Solutions-Engineer / observability interview answer frames for the seven standard project-interview questions, with a cross-cutting honesty checklist), and `public-repository-readiness.md` (a checklist and guardrails for preparing the repository for public viewing — a public-safe README check, a secrets/config check, a demo-data check, a screenshot-placeholder check, a known-limitations check, and "do not publish until verified" hard gates) — lightly updated `README.md` to point reviewers to the new presentation documents, and synchronized the State Preservation Bundle.

Confirmed constraints: documentation-first portfolio packaging only. No new product feature, UI, server, dashboard, browser mutation control, JavaScript, frontend directory, React/Vite/TypeScript file, external asset, CDN, generated audio, screenshot/image/PDF/PowerPoint/binary asset, demo video, new dependency, or database schema change; no change to pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, API, CLI, or telemetry behaviour; no ARCH-LOCKed contract change; no source change; no Phase 13 GUI implementation. `pyproject.toml`, `uv.lock`, and the `src/` tree are byte-for-byte unchanged from the source artifact. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 12C current-state expectations: `_CURRENT_PHASE` advanced to "phase 12c", `_LAST_LOCKED_PHASE` advanced to "phase 12b", `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 12C lock, a premature Phase 12 closure, and a premature Phase 12D-or-later start, and the append-only lock-record checks extended to additionally require the Phase 12B lock record. The guard is strengthened, not weakened. This test update was explicitly authorized because the test is intentionally phase-specific and otherwise blocks the approved phase transition. The append-only locked-decision documents `docs/canonical-state.md` and the round log in this `docs/phase-history.md` were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

Confirmed gate results: 590 tests passing (588 from the Phase 12B baseline, plus 2 net from the strengthened state-discipline guard — the advance adds two parametrized append-only lock-record cases requiring the Phase 12B record), ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy; the legal-hallucination scanner (run inside the pytest suite, covering the four new documents) returns zero violations.

**Current state after this round (Phase 12C):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A locked; **Phase 12B — Portfolio Evidence Pack / Reviewer Assets — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — is STARTED**; Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — is an implementation candidate, pending review, **not locked**. Phase 12D and later subphases of Phase 12 have not started. Phase 13 — Operator GUI / Decoupled Frontend Vision — is roadmap-preserved only and has not started. Phase 9C remains optional/not scheduled.

## Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — LOCK (LOCKED / ACCEPTED / CANONICAL — 2026-05-26)

Lock closure. Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — the third subphase of Phase 12 — Portfolio / SE Demo Packaging — is locked, accepted, and canonical with explicit user approval. Phase 12C completed the Phase Closure Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini returned **SAFE TO LOCK** with no critical findings, no non-blocking findings, and no required edits — state discipline, scope/code/dependency assessment, and validation assessment all passed — and the user then locked Phase 12C.

The locked Phase 12C artifact is `storytime-phase12c-portfolio-demo-narrative-public-presentation-kit.tar.gz`, SHA-256 `4c98a25d6bb0ae751b4ba33851bc60e7d7805d4fd31ebcfc45c2d30a659301da`. Phase 12C was a documentation-first portfolio-packaging round: it added four public-presentation `docs/` documents (`portfolio-demo-narrative.md`, `demo-talk-track.md`, `interview-story-bank.md`, `public-repository-readiness.md`), lightly updated `README.md`, advanced the state-discipline guard under the authorized §5 mechanical exception, and synchronized the State Preservation Bundle; it changed no `src/`, `pyproject.toml`, `uv.lock`, dependency, or product behaviour.

This lock-closure entry is recorded into the append-only round log by the Phase 12D round as part of its state synchronization — the same after-the-fact lock-recording pattern used for Phase 11D, Phase 12A, and Phase 12B. The Phase 12D round did not re-perform the GPT-5.5 / Gemini reviews. The Phase 12C round entry earlier in this file is preserved as written and is superseded for status purposes by this lock-closure entry. Validation basis at lock: 590 tests passing, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 contracts kept, `storytime doctor` healthy, legal-hallucination scanner zero violations.

**Current state after this lock (Phase 12C):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A locked; Phase 12B locked; **Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — is STARTED** and not closed. Phase 12D has not started before the Phase 12D round below. Phase 13 — Operator GUI / Decoupled Frontend Vision — is roadmap-preserved only and has not started. Phase 9C remains optional/not scheduled.

## Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition (implementation candidate — pending review — not locked — 2026-05-26)

Implementation round. Phase 12D is the fourth subphase of Phase 12 — Portfolio / SE Demo Packaging. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 12D awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 12D does **not** lock Phase 12D, does **not** close Phase 12, and does **not** start Phase 12E or any later Phase 12 subphase.

Phase 12D is a documentation-only closure-definition round. It does not itself close Phase 12 — it prepares the Phase 12 closure decision so a reviewer can determine whether Phase 12D can lock and whether Phase 12 can close. It took the locked Phase 12C artifact `storytime-phase12c-portfolio-demo-narrative-public-presentation-kit.tar.gz` (SHA-256 `4c98a25d6bb0ae751b4ba33851bc60e7d7805d4fd31ebcfc45c2d30a659301da`, verified on extraction) as its source. It added three `docs/` documents — `phase12-closure-plan.md` (Phase 12 closure criteria, the completed Phase 12A–12C asset inventory, the closure-readiness checklist, the remaining-gaps / no-go criteria, the close-after-12D vs bounded-cleanup vs separate-12E recommendation, and the Phase 13 boundary statement), `final-portfolio-handoff.md` (a cold-reader handoff with current-state snapshot, 5-minute / 15-minute / deep-architecture reviewer paths, a suggested demo flow, an evidence map, explicit limitations, and the next-phase boundary), and `phase12-final-review-checklist.md` (the checklist a reviewer uses at the Phase 12D / Phase 12 closure gate) — and synchronized the State Preservation Bundle.

Confirmed constraints: documentation-only closure-definition round. No new product feature, UI, server, dashboard, browser mutation control, JavaScript, frontend directory, React/Vite/TypeScript file, external asset, CDN, generated audio, screenshot/image/PDF/PowerPoint/binary asset, demo video, new dependency, or database schema change; no change to pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, API, CLI, or telemetry behaviour; no ARCH-LOCKed contract change; no source change; no Phase 13 GUI implementation. `pyproject.toml`, `uv.lock`, and the `src/` tree are byte-for-byte unchanged from the source artifact. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 12D current-state expectations: `_CURRENT_PHASE` advanced to "phase 12d", `_LAST_LOCKED_PHASE` advanced to "phase 12c", and `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 12D lock, a premature Phase 12 closure, and a premature Phase 12E-or-later start. The guard is strengthened, not weakened — the append-only lock-record checks now additionally require the Phase 12C lock record. This test update was explicitly authorized because the test is intentionally phase-specific and otherwise blocks the approved phase transition. The append-only locked-decision documents `docs/canonical-state.md` and the round log in this `docs/phase-history.md` were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

Confirmed gate results: 592 tests passing (590 from the Phase 12C baseline, plus 2 net from the strengthened state-discipline guard — the advance adds two parametrized append-only lock-record cases requiring the Phase 12C record), ruff clean, mypy clean (85 source files, strict), import-linter 2/2 kept, `storytime doctor` healthy; the legal-hallucination scanner (run inside the pytest suite, covering the three new documents) returns zero violations.

**Current state after this round (Phase 12D):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A locked; Phase 12B locked; **Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — locked (the last locked phase)**; **Phase 12 — Portfolio / SE Demo Packaging — is STARTED**; Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — is an implementation candidate, pending review, **not locked**. Phase 12 is not closed. Phase 12E is optional, future, contingency-only work and has not started. Phase 13 — Operator GUI / Decoupled Frontend Vision — is roadmap-preserved only and has not started. Phase 9C remains optional/not scheduled.

## Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — LOCK (LOCKED / ACCEPTED / CANONICAL — Phase 12 CLOSED — 2026-05-27)

Lock closure recorded. Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — the fourth subphase of Phase 12 — Portfolio / SE Demo Packaging — is locked, accepted, and canonical with explicit user approval. Locked artifact: `storytime-phase12d-phase12-closure-plan-final-portfolio-handoff.tar.gz`, SHA-256 `64ad09e875f0653608e0deb756f11ee5adc0d2ff1265e2039cbc51491f286cf8`.

Phase 12D completed the Phase Closure Protocol — implementation, GPT-5.5 review, and Gemini critique. The Gemini review returned the verdict to lock Phase 12D and close Phase 12, with no critical findings, no non-blocking findings, and no required edits. The user, as final decision-maker, then locked Phase 12D and formally closed Phase 12 — Portfolio / SE Demo Packaging. This out-of-band closure was a user/mediator decision supplied to the Phase 13A round; it was not contained in the Phase 12D artifact itself, which captured the pre-lock implementation-candidate state. The Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — round records this lock and closure into this append-only round log as part of its state synchronization; it did not re-perform the GPT-5.5 / Gemini reviews. This is the same after-the-fact lock-recording pattern used for Phase 11D, Phase 12A, Phase 12B, and Phase 12C. The Phase 12D "implementation candidate" entry earlier in this append-only file is preserved as written and is superseded for status purposes by this lock-closure entry. Validation basis at lock: 592 tests passing, ruff clean, mypy clean (85 source files, strict), import-linter 2/2 contracts kept, `storytime doctor` healthy, legal-hallucination scanner zero violations.

**Phase 12 — Portfolio / SE Demo Packaging — is CLOSED.** All four of its subphases — Phase 12A, Phase 12B, Phase 12C, and Phase 12D — are locked. Phase 12A.1 is folded into the Phase 12A lock lineage, and Phase 12B.1 / 12B.2 / 12B.3 are folded into the Phase 12B lock lineage, as accepted cleanup sub-rounds. Phase 12E was optional, contingency-only work that would have existed only if the Phase 12D review had found a substantive packaging gap; the review found none, so Phase 12E was not needed and never started.

**Current state after this lock (Phase 12D / Phase 12 closure):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12D is the last locked phase**; **Phase 12 — Portfolio / SE Demo Packaging — is CLOSED**. Phase 13 — Portfolio Website / Operator GUI — is STARTED before the Phase 13A round below. Phase 9C remains optional/not scheduled.

---

## Phase 13A — Portfolio Website / Operator GUI Architecture Baseline (implementation candidate — pending review — not locked — 2026-05-27)

Implementation round. Phase 13A is the first subphase of Phase 13 — Portfolio Website / Operator GUI — the phase that follows the closed Phase 12. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 13A awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 13A does **not** lock Phase 13A, does **not** close Phase 13, and does **not** start Phase 13B or any later Phase 13 subphase.

Phase 13A is a documentation-only architecture-baseline round under no new architecture amendment — it designs the portfolio website and the decoupled operator GUI on paper and refines the earlier `docs/GUI_vision.md` sketch into an authoritative Phase 13 plan, without building any of it. It took the locked Phase 12D artifact `storytime-phase12d-phase12-closure-plan-final-portfolio-handoff.tar.gz` (SHA-256 `64ad09e875f0653608e0deb756f11ee5adc0d2ff1265e2039cbc51491f286cf8`, verified on extraction) as its source. It added five `docs/` documents — `phase13-portfolio-website-architecture.md`, `frontend-backend-contract.md`, `phase13-roadmap.md`, `portfolio-website-content-model.md`, and `operator-gui-view-model.md` — lightly updated `README.md`, and synchronized the State Preservation Bundle. `docs/GUI_vision.md`, the original verbatim vision capture, is left unchanged; the five new documents supersede it as the authoritative Phase 13 plan.

Confirmed constraints: documentation-only architecture-baseline round. Phase 13A is a planning round; it does not implement the portfolio website and does not implement the operator GUI. No React, Vite, TypeScript, JavaScript, CSS, or HTML application code; no `frontend/` / `web/` / `app/` directory; no `package.json` or `vite.config`; no new product feature, UI, server, dashboard, browser mutation control, external asset, CDN, generated audio, screenshot/image/PDF/PowerPoint/binary asset, demo video, new dependency, or database schema change; no change to pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, API, CLI, or telemetry behaviour; no ARCH-LOCKed contract change; no source change. `pyproject.toml`, `uv.lock`, and the `src/` tree are byte-for-byte unchanged from the source artifact. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` so it tracks the Phase 13A current-state expectations: `_CURRENT_PHASE` advanced to "phase 13a", `_LAST_LOCKED_PHASE` advanced to "phase 12d", `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 13A lock, a premature Phase 13 closure, and a premature Phase 13B-or-later start, and a new `_FORBIDDEN_FRONTEND_CLAIMS` list with a parametrized `test_no_frontend_implementation_claimed` check guarding against a false claim that Phase 13A built the frontend, the portfolio website, or the operator GUI. The guard is strengthened, not weakened — the append-only lock-record checks now additionally require the Phase 12D lock record. This test update was explicitly authorized because the test is intentionally phase-specific and otherwise blocks the approved phase transition. The append-only locked-decision documents `docs/canonical-state.md` and this `docs/phase-history.md` round log were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

**Current state after this round (Phase 13A):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; **Phase 12D is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**; Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — is an implementation candidate, pending review, **not locked**. Phase 13B and every later Phase 13 subphase have not started; Phase 13 is not closed. Phase 9C remains optional/not scheduled.

## Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — LOCK (LOCKED / ACCEPTED / CANONICAL — 2026-05-27)

Lock closure. Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — completed the Phase Closure Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no required edits, and the user, as final decision-maker, locked Phase 13A. Locked artifact lineage: `storytime-phase13a-portfolio-website-operator-gui-architecture-baseline.tar.gz`, SHA-256 `100098aa6280b740a6eeb862c1e1923d2e031bd02a06786b7a8b8ec07facf1c0`.

Phase 13A — the first subphase of Phase 13 — Portfolio Website / Operator GUI — is locked, accepted, and canonical. It was a documentation-only architecture-baseline round: it designed the portfolio website and the decoupled operator GUI on paper and added five architecture-baseline `docs/` documents, with no frontend application code and no change to `pyproject.toml`, `uv.lock`, or `src/`. **Phase 13A is the last locked phase.** Phase 13 remains STARTED and is not closed. This lock was recorded into the State Preservation Bundle by the Phase 13B round as an after-the-fact lock record, the same pattern used for Phase 11D and the Phase 12 subphases; the Phase 13A "implementation candidate" entry above is preserved as written and superseded for status purposes by this lock entry.

## Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold (implementation candidate — pending review — not locked — 2026-05-27)

Implementation round. Phase 13B is the second subphase of Phase 13 — Portfolio Website / Operator GUI — and the first round of Phase 13 in which frontend code is written. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 13B awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 13B does **not** lock Phase 13B, does **not** close Phase 13, and does **not** start Phase 13C or any later Phase 13 subphase.

Phase 13B took the locked Phase 13A artifact `storytime-phase13a-portfolio-website-operator-gui-architecture-baseline.tar.gz` (SHA-256 `100098aa6280b740a6eeb862c1e1923d2e031bd02a06786b7a8b8ec07facf1c0`, verified on extraction) as its source. Against the locked Phase 13A contract it implements a deliberately bounded frontend — a typed static portfolio shell plus one visual operator view. It adds a new top-level `frontend/` directory: a React + TypeScript (strict) + Vite project, standard CSS, and no external UI / component / state / charting library, containing the frontend read-model contract (`frontend/src/types/storytime.ts`), a static demo dataset of exactly two mock pipeline runs (one golden-path, one governance review-required, in `frontend/src/data/storytime-demo-data.ts`), the portfolio homepage, one Pipeline Run Detail view with a visual Stage Timeline, honest placeholder components for the future portfolio sections and operator views, the scaffold files (`package.json`, `package-lock.json`, `tsconfig.json`, `vite.config.ts`, `index.html`), and a frontend README. It lightly updated `README.md` and synchronized the State Preservation Bundle.

Confirmed constraints: Phase 13B introduces a static, read-only, demo-data-backed frontend shell. It is not backend-connected, uses no live or runtime data, implements no mutations (retry, re-run, and review-decision actions appear only as visibly-disabled affordances), and is not production-hosted or cloud-deployed; it contacts no backend (no `fetch()`, no `axios`, no network call). No backend integration, live data, mutation behaviour, cloud deployment, or Phase 13C+ work exists. No change to pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, API, CLI, telemetry, Docker behaviour, or the database schema; no ARCH-LOCKed contract change. `pyproject.toml`, `uv.lock`, and the `src/` tree are byte-for-byte unchanged from the source artifact. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` to the Phase 13B current-state expectations (`_CURRENT_PHASE` → "phase 13b", `_LAST_LOCKED_PHASE` → "phase 13a", `_FORBIDDEN_FUTURE_CLAIMS` refreshed, and the Phase 13A `_FORBIDDEN_FRONTEND_CLAIMS` list replaced by a `_FORBIDDEN_OVERCLAIM_CLAIMS` list with a `test_no_overclaim` check, since Phase 13B legitimately builds a frontend but must not overclaim it). The guard is strengthened, not weakened — the append-only lock-record checks now additionally require the Phase 13A lock record. This test update was explicitly authorized because the test is intentionally phase-specific and otherwise blocks the approved phase transition. The append-only locked-decision documents `docs/canonical-state.md` and this `docs/phase-history.md` round log were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

**Current state after this round (Phase 13B):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 CLOSED**; Phase 12A–12D all locked; **Phase 12 CLOSED**; Phase 13A locked; **Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**; Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — is an implementation candidate, pending review, **not locked**. Phase 13C and every later Phase 13 subphase have not started; Phase 13 is not closed. Phase 9C remains optional/not scheduled.

## Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — LOCK (LOCKED / ACCEPTED / CANONICAL — 2026-05-27)

Lock closure. Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — completed the Phase Closure Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no required edits, and the user, as final decision-maker, locked Phase 13B. Locked artifact lineage: `storytime-phase13b-typed-static-portfolio-shell-minimal-visual-pipeline-scaffold.tar.gz`, SHA-256 `9319ece26f5b457ddbbefaab346aba61cb61f65a6b7b729b5acaa12f30df3f24`.

Phase 13B — the second subphase of Phase 13 — Portfolio Website / Operator GUI — is locked, accepted, and canonical. It was the first frontend implementation round: it added the bounded React + TypeScript + Vite static frontend shell — the read-model contract, a two-run static demo dataset, the portfolio homepage, one Pipeline Run Detail view with a visual Stage Timeline, honest placeholders, and a frontend README — with no change to `pyproject.toml`, `uv.lock`, or `src/`. **Phase 13B is the last locked phase.** Phase 13 remains STARTED and is not closed. This lock was recorded into the State Preservation Bundle by the Phase 13C round as an after-the-fact lock record, the same pattern used for Phase 11D and the Phase 12 subphases; the Phase 13B "implementation candidate" entry above is preserved as written and superseded for status purposes by this lock entry.

## Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment (implementation candidate — pending review — not locked — 2026-05-27)

Implementation round. Phase 13C is the third subphase of Phase 13 — Portfolio Website / Operator GUI. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 13C awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 13C does **not** lock Phase 13C, does **not** close Phase 13, and does **not** start Phase 13D or any later Phase 13 subphase.

Phase 13C took the locked Phase 13B artifact `storytime-phase13b-typed-static-portfolio-shell-minimal-visual-pipeline-scaffold.tar.gz` (SHA-256 `9319ece26f5b457ddbbefaab346aba61cb61f65a6b7b729b5acaa12f30df3f24`, verified on extraction) as its source. It establishes a truthful, reproducible, read-only data boundary between backend truth and the Phase 13B frontend — realizing "backend owns truth, frontend owns understanding": the backend defines the export shape and the frontend mirrors it. Phase 13C adds a small read-only backend export module `src/storytime/operator_export.py` and a `storytime export-demo-ui` CLI command that together produce a deterministic static JSON export, committed at `frontend/src/data/storytime-demo-export.json` with a top-level `schemaVersion` (`"1.0"`); the export contract document `docs/frontend-static-export-contract.md`; the frontend / GUI deferred-work register `docs/frontend-gui-deferred-work-register.md`; a frontend adapter `frontend/src/data/adapter.ts` and a `StaticDemoExport` type; backend contract tests `tests/test_operator_export.py`; and it rewires the homepage and the Pipeline Run Detail / Stage Timeline view to consume the export through the adapter (the hand-authored `frontend/src/data/storytime-demo-data.ts` is removed, superseded by the generated export plus the adapter). It updated user-visible Phase 13B → 13C wording in the frontend, lightly updated `README.md`, and synchronized the State Preservation Bundle.

Confirmed constraints: Phase 13C is a static, read-only data-boundary round. The export is deterministic — built entirely from fixed demo data with no `datetime.now()`, no `uuid`, and no randomness, serialized with sorted keys and a stable format, so generating it twice yields byte-identical JSON (proven: export SHA-256 `0b2989554a1f9fae1c5963527d3f59f882381f253aced2582087c233d42d6156`). Phase 13C does not make the frontend live: it adds no server, no live API, no `fetch`/`axios`, no watcher, no mutation, no authentication, no cloud deployment, and no production hosting. Unlike Phase 13B it adds small backend code — but it is read-only and deterministic and changes no core pipeline runtime behaviour, no governance, no telemetry, no CLI behaviour beyond the new read-only `export-demo-ui` command, no database schema, and no ARCH-LOCKed contract; `uv.lock` and root dependencies are unchanged. The only `src/` changes are the new `operator_export.py` module and the `export-demo-ui` command plus its import in `cli/app.py`; `pyproject.toml` changes only by adding `storytime.operator_export` to the two import-linter contract lists. The `tests/` changes are the new `tests/test_operator_export.py` and the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` to the Phase 13C current-state expectations (`_CURRENT_PHASE` → "phase 13c", `_LAST_LOCKED_PHASE` → "phase 13b", `_FORBIDDEN_FUTURE_CLAIMS` refreshed, `_FORBIDDEN_OVERCLAIM_CLAIMS` re-anchored to Phase 13C). The guard is strengthened, not weakened — the append-only lock-record checks now additionally require the Phase 13B lock record. This test update was explicitly authorized because the test is intentionally phase-specific and otherwise blocks the approved phase transition. The append-only locked-decision documents `docs/canonical-state.md` and this `docs/phase-history.md` round log were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

**Current state after this round (Phase 13C):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; Phase 13A locked; Phase 13B locked; **Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**; Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment — is an implementation candidate, pending review, **not locked**. Phase 13D and every later Phase 13 subphase have not started; Phase 13 is not closed. Phase 9C remains optional/not scheduled.

## Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment — LOCK (LOCKED / ACCEPTED / CANONICAL — 2026-05-27)

Lock closure. Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment — completed the Phase Closure Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no required edits, and the user, as final decision-maker, locked Phase 13C. Locked artifact lineage: `storytime-phase13c-deterministic-read-only-static-export-frontend-data-alignment.tar.gz`, SHA-256 `1c24cf03283590d7f095d3805bc8f5d560e3583131c04e5be0359e0053145507`.

Phase 13C — the third subphase of Phase 13 — Portfolio Website / Operator GUI — is locked, accepted, and canonical. It established the deterministic, read-only data boundary between backend truth and the Phase 13B frontend: a small read-only backend export module and `storytime export-demo-ui` CLI command producing the deterministic static JSON export with a top-level `schemaVersion`, the export contract document, the frontend deferred-work register, the frontend adapter and `StaticDemoExport` type, backend contract tests, and the rewired homepage and Pipeline Run Detail / Stage Timeline. The export is deterministic and read-only; no live API, no `fetch`/`axios`, no mutation, no authentication, no cloud deployment, and no production hosting were introduced; no core pipeline runtime behaviour and no root dependency changed. **Phase 13C is the last locked phase.** Phase 13 remains STARTED and is not closed. This lock was recorded into the State Preservation Bundle by the Phase 13D round as an after-the-fact lock record, the same pattern used for Phase 11D, the Phase 12 subphases, and Phase 13B; the Phase 13C "implementation candidate" entry above is preserved as written and superseded for status purposes by this lock entry.

## Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) (implementation candidate — pending review — not locked — 2026-05-27)

Implementation round. Phase 13D is the fourth subphase of Phase 13 — Portfolio Website / Operator GUI. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 13D awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 13D does **not** lock Phase 13D, does **not** close Phase 13, and does **not** start Phase 13E or any later Phase 13 subphase.

Phase 13D took the locked Phase 13C artifact `storytime-phase13c-deterministic-read-only-static-export-frontend-data-alignment.tar.gz` (SHA-256 `1c24cf03283590d7f095d3805bc8f5d560e3583131c04e5be0359e0053145507`, verified on extraction) as its source. It is a frontend-only round that expands two of the honest Phase 13B/13C placeholder views into real read-only operator views: **Governance / Safety** (per-run Trust Envelope decisions, source authorization categories, the governance-gate result per run, the display-discipline honesty list, evidence references, and visibly-disabled future review actions) and **Failure / Recovery** (the failure / review queue joined to per-run failure summaries, affected stage, related governance decision, evidence links, the operator inspect-next guidance, and visibly-disabled recovery actions, with an inspect-this-run drill-down callback into the existing Pipeline Run Detail view). The view choice and ordering followed the Phase 13C deferred-work register's view-expansion recommendation. Phase 13D added two new view components and their CSS Modules (`frontend/src/components/GovernanceSafetyView.tsx` / `.module.css` and `frontend/src/components/FailureRecoveryView.tsx` / `.module.css`), two domain-specific view-model adapters (`frontend/src/data/governanceAdapter.ts` and `frontend/src/data/failureAdapter.ts`) projecting the locked Phase 13C export, an ambient CSS-Modules TypeScript declaration (`frontend/src/types/css-modules.d.ts`), App-level navigation rewiring with a read-only "Data source · Demo Snapshot" header chip backed by the existing `EXPORT_META` adapter export and an inspect-this-run drill-down callback (plain prop drilling, no router), a small `.data-chip` rule in the shared global stylesheet for the header chip, and documentation updates including a deferred-register entry for the future **Demo / Blue / Green Data Snapshot Switcher**. It synchronized the State Preservation Bundle.

Confirmed constraints: Phase 13D is a static, read-only, export-backed frontend round. It did **not** modify the backend export generator (`src/storytime/operator_export.py`), the committed static export JSON (`frontend/src/data/storytime-demo-export.json`), or the `storytime export-demo-ui` CLI contract; both protected files are byte-identical to the Phase 13C source (verified by `diff -q`). Phase 13D added no server, no live API, no `fetch`/`axios`, no watcher, no backend-to-frontend runtime coupling, no mutation, no authentication, no cloud deployment, and no production hosting; the recovery / review affordances are surfaced as visibly-disabled future actions labelled with the phase that would enable them (Phase 13E). No `src/`, `pyproject.toml`, `uv.lock`, or root dependency changed. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` to the Phase 13D current-state expectations (`_CURRENT_PHASE` → "phase 13d", `_LAST_LOCKED_PHASE` → "phase 13c", `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 13D lock, premature Phase 13 closure, and a premature Phase 13E-or-later start; `_FORBIDDEN_OVERCLAIM_CLAIMS` re-anchored to Phase 13D; a new `test_handoff_state_records_phase_13c_locked` check added; the append-only lock-record checks now additionally require the Phase 13C lock record). The guard is strengthened, not weakened. This test update was explicitly authorized because the test is intentionally phase-specific and otherwise blocks the approved phase transition. The append-only locked-decision documents `docs/canonical-state.md` and this `docs/phase-history.md` round log were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

**Current state after this round (Phase 13D):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; **Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**; Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) — is an implementation candidate, pending review, **not locked**. Phase 13E and every later Phase 13 subphase have not started; Phase 13 is not closed. Phase 9C remains optional/not scheduled.

## Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) — LOCK (LOCKED / ACCEPTED / CANONICAL — 2026-05-27)

Lock closure. Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) — completed the Phase Closure Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no required edits, and the user, as final decision-maker, locked Phase 13D. Locked artifact lineage: `storytime-phase13d-operator-workflow-view-expansion-governance-failure.tar.gz`, SHA-256 `5ec0b1edaaedfed2f3ae9b3e221e6a9089c52b8df152c4824503e7ca796894f3`.

Phase 13D — the fourth subphase of Phase 13 — Portfolio Website / Operator GUI — is locked, accepted, and canonical. It expanded two of the honest Phase 13B/13C placeholder views into real read-only operator views: Governance / Safety and Failure / Recovery, each with per-run drill-down to Pipeline Run Detail. It added two new view components and their CSS Modules, two domain-specific view-model adapters, an ambient CSS-Modules TypeScript declaration, App-level navigation rewiring with the read-only "Data source · Demo Snapshot" header chip, and a small `.data-chip` rule in the shared global stylesheet (the only global addition). The protected Phase 13C boundary held: `src/storytime/operator_export.py`, the committed static export JSON, and the `storytime export-demo-ui` CLI contract were byte-identical to the Phase 13C source. No live integration, mutation, authentication, or hosting was introduced; no core pipeline runtime behaviour and no root dependency changed. **Phase 13D is the last locked phase.** Phase 13 remains STARTED and is not closed. This lock was recorded into the State Preservation Bundle by the Phase 13D.1 round as an after-the-fact lock record, the same pattern used for Phase 11D, the Phase 12 subphases, Phase 13B, and Phase 13C; the Phase 13D "implementation candidate" entry above is preserved as written and superseded for status purposes by this lock entry.

## Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline (implementation candidate — pending review — not locked — 2026-05-27)

Implementation round. Phase 13D.1 is a static / read-only refinement sub-round of the locked Phase 13D, intended to strengthen the operator GUI and portfolio / reviewer flow before any future controlled local action or mutation-boundary work. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 13D.1 awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 13D.1 does **not** lock Phase 13D.1, does **not** close Phase 13, and does **not** start Phase 13E or any later Phase 13 subphase.

Phase 13D.1 took the locked Phase 13D artifact `storytime-phase13d-operator-workflow-view-expansion-governance-failure.tar.gz` (SHA-256 `5ec0b1edaaedfed2f3ae9b3e221e6a9089c52b8df152c4824503e7ca796894f3`, verified on extraction) as its source. It standardizes the disabled future-action display across views into a reusable typed component (`frontend/src/components/DisabledFutureActionCard.tsx` plus its CSS Module) backed by real `<button disabled={true}>` elements with no `onClick` handlers and no fake mutation props — Governance / Safety and Failure / Recovery were refactored to consume it; replaces the honest Evidence / Validation placeholder with a real read-only view (`frontend/src/components/EvidenceValidationView.tsx` plus its CSS Module) carrying the mandatory **STATIC PORTFOLIO DATA — NOT A LIVE CI/CD DASHBOARD** disclaimer and pointing to repository-relative evidence (`docs/verification-log.md`, `docs/frontend-static-export-contract.md`, `docs/frontend-gui-deferred-work-register.md`, `docs/phase-history.md`, `docs/artifact-manifest.md`, `tests/test_failure_mode_regression.py`, `tests/test_operator_export.py`) without fabricating runtime CI status; adds an evidence view-model helper (`frontend/src/data/evidenceAdapter.ts`) organising the static evidence categories and the Demo / Active / Candidate Data Source framing (Active and Candidate as **data snapshots, not deployment environments**, no switching implemented); and extracts navigation / view-key metadata from `App.tsx` into a small typed `frontend/src/navigation.ts` helper to keep `App.tsx` readable while preserving plain `useState` navigation and the `inspectRun(runId)` prop-drilled drill-down (no router). It synchronizes the State Preservation Bundle including the deferred-work register.

Confirmed constraints: Phase 13D.1 is a static, read-only, export-backed frontend round. It did **not** modify the backend export generator (`src/storytime/operator_export.py`), the committed static export JSON (`frontend/src/data/storytime-demo-export.json`), the `storytime export-demo-ui` CLI contract, or `src/storytime/cli/app.py`; all four protected files / contracts are byte-identical to the Phase 13D source (verified by `diff -q`). Phase 13D.1 added no server, no live API, no `fetch`/`axios`/`localhost`/network call, no watcher, no backend-to-frontend runtime coupling, no mutation, no authentication, no cloud deployment, and no production hosting; the visibly-disabled review and recovery affordances remain visibly disabled and carry no mutation handlers. No `src/`, `pyproject.toml`, `uv.lock`, or root dependency changed. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` to the Phase 13D.1 current-state expectations (`_CURRENT_PHASE` → "phase 13d.1", `_LAST_LOCKED_PHASE` → "phase 13d", `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 13D.1 lock, premature Phase 13 closure, and a premature Phase 13E-or-later start while allowing the now-legitimate "phase 13d is locked" claims; `_FORBIDDEN_OVERCLAIM_CLAIMS` re-anchored to Phase 13D.1 with new entries forbidding live-CI, snapshot-switching, and promotion overclaims; a new `test_handoff_state_records_phase_13d_locked` check added; the append-only lock-record checks now additionally require the Phase 13D lock record; the "current phase not claimed locked" check rewritten to do a direct substring scan rather than fragment-splitting, because the period inside "Phase 13D.1" is itself a fragment-split character). The guard is strengthened, not weakened. This test update was explicitly authorized because the test is intentionally phase-specific and otherwise blocks the approved phase transition. The append-only locked-decision documents `docs/canonical-state.md` and this `docs/phase-history.md` round log were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

**Current state after this round (Phase 13D.1):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; Phase 13D locked; **Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**; Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline — is an implementation candidate, pending review, **not locked**. Phase 13E and every later Phase 13 subphase have not started; Phase 13 is not closed. Phase 9C remains optional/not scheduled.

## Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline — LOCK (LOCKED / ACCEPTED / CANONICAL — 2026-05-27)

Lock closure. Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline — completed the Phase Closure Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no required edits, and the user, as final decision-maker, locked Phase 13D.1. Locked artifact lineage: `storytime-phase13d1-static-operator-gui-refinement-evidence-disabled-actions.tar.gz`, SHA-256 `812841381075e0e7839266512eb6d7f41bf2d890ee4c82b91627ce824f5b1eae`.

Phase 13D.1 — a sub-round of Phase 13D — is locked, accepted, and canonical. It standardized the disabled future-action display across views into a reusable typed component (`DisabledFutureActionCard` / `DisabledFutureActionList` — real `<button disabled={true}>` with no `onClick`), refactored Governance / Safety and Failure / Recovery to consume it, replaced the Evidence / Validation placeholder with a real read-only view carrying the mandatory STATIC PORTFOLIO DATA disclaimer and repository-relative evidence references, added the evidence adapter with the Demo / Active / Candidate Data Source framing, and extracted navigation metadata from `App.tsx` into `frontend/src/navigation.ts` (slimming `App.tsx` from 228 to 136 lines). The protected Phase 13D boundary held: `src/storytime/operator_export.py`, the committed `frontend/src/data/storytime-demo-export.json`, the `storytime export-demo-ui` CLI contract, and `src/storytime/cli/app.py` were byte-identical to the Phase 13D source. No live integration, mutation, authentication, or hosting was introduced; no core pipeline runtime behaviour and no root dependency changed. **Phase 13D.1 is the last locked phase.** Phase 13 remains STARTED and is not closed. This lock was recorded into the State Preservation Bundle by the Phase 13D.2 round as an after-the-fact lock record, the same pattern used for Phase 11D, the Phase 12 subphases, Phase 13B, Phase 13C, and Phase 13D; the Phase 13D.1 "implementation candidate" entry above is preserved as written and superseded for status purposes by this lock entry.

## Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path (implementation candidate — pending review — not locked — 2026-05-27)

Implementation round. Phase 13D.2 is a static / read-only demo-readiness sub-round of the locked Phase 13D.1, turning the existing operator GUI views into a coherent guided reviewer / demo path before any future controlled local action or mutation-boundary work. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 13D.2 awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 13D.2 does **not** lock Phase 13D.2, does **not** close Phase 13, and does **not** start Phase 13E or any later Phase 13 subphase.

Phase 13D.2 took the locked Phase 13D.1 artifact `storytime-phase13d1-static-operator-gui-refinement-evidence-disabled-actions.tar.gz` (SHA-256 `812841381075e0e7839266512eb6d7f41bf2d890ee4c82b91627ce824f5b1eae`, verified on extraction) as its source. It replaces the honest Demo Walkthrough placeholder with a real read-only view (`frontend/src/components/DemoWalkthroughView.tsx` plus its CSS Module) backed by a static view-model adapter (`frontend/src/data/demoWalkthroughAdapter.ts`) holding the long-form route content. The view offers four reviewer routes — a 5-minute scan, a 10-minute SE-style demo, a technical deep-dive, and a self-guided reviewer path — switched by a simple segmented control backed by local `useState<RouteId>` (no router, no Context, no persistence). Each step carries title, target view, what to inspect, what it proves, talking points, and an in-line navigation affordance into the relevant existing view; steps that point to a specific run identify it by stable id (`run-2026-0518-golden` or `run-2026-0520-review`). The view also includes architecture-checkpoint cards (local-first design, deterministic static export, backend owns truth / frontend owns understanding, read-only operator surface, static evidence boundary, disabled-action boundary, Demo / Active / Candidate as **data snapshots, not deployment environments**, and why Phase 13E must be explicitly gated), a deliberate "what is intentionally deferred" section, and interview / SE talking-point callout cards. Phase 13D.2 absorbs ~80–90% of an Architecture Story narrative via these embedded checkpoints but does NOT implement a full standalone Architecture Story page — that stays deferred and is recorded as a new item in `docs/frontend-gui-deferred-work-register.md` ("Standalone Architecture Story / System Boundary Reference"). Navigation: `frontend/src/navigation.ts` updated so Demo Walkthrough is a real view (remaining placeholders still point to Phase 13E or later); `frontend/src/App.tsx` lightly updated to render the new view and pass a navigation callback down; no router, no Context, no global state introduced.

Confirmed constraints: Phase 13D.2 is a static, read-only, export-backed frontend round. It did **not** modify the backend export generator (`src/storytime/operator_export.py`), the committed static export JSON (`frontend/src/data/storytime-demo-export.json`), the `storytime export-demo-ui` CLI contract, or `src/storytime/cli/app.py`; all four protected files / contracts are byte-identical to the Phase 13D.1 source (verified by `diff -q`). Phase 13D.2 added no server, no live API, no `fetch`/`axios`/`localhost`/network call, no watcher, no backend-to-frontend runtime coupling, no mutation, no authentication, no cloud deployment, no production hosting, no dynamic file loading, and no Demo / Active / Candidate switching; the visibly-disabled review and recovery affordances remain visibly disabled and carry no mutation handlers. No `src/`, `pyproject.toml`, `uv.lock`, `frontend/package.json`, `frontend/package-lock.json`, or root dependency changed. The only `tests/` change is the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` to the Phase 13D.2 current-state expectations (`_CURRENT_PHASE` → "phase 13d.2", `_LAST_LOCKED_PHASE` → "phase 13d.1", `_FORBIDDEN_FUTURE_CLAIMS` refreshed to forbid a premature Phase 13D.2 lock, premature Phase 13 closure, and a premature Phase 13E-or-later start while allowing the now-legitimate "phase 13d.1 is locked" claims; `_FORBIDDEN_OVERCLAIM_CLAIMS` re-anchored to Phase 13D.2 with new entries forbidding live-CI / live-telemetry, snapshot-switching, dynamic-loading, and standalone-architecture-story overclaims; a new `test_handoff_state_records_phase_13d1_locked` check added; the append-only lock-record checks now additionally require the Phase 13D.1 lock record). The guard is strengthened, not weakened. This test update was explicitly authorized because the test is intentionally phase-specific and otherwise blocks the approved phase transition. The append-only locked-decision documents `docs/canonical-state.md` and this `docs/phase-history.md` round log were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

**Current state after this round (Phase 13D.2):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; Phase 13D locked; Phase 13D.1 locked; **Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**; Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path — is an implementation candidate, pending review, **not locked**. Phase 13E and every later Phase 13 subphase have not started; Phase 13 is not closed. Phase 9C remains optional/not scheduled.

## Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path — LOCK (LOCKED / ACCEPTED / CANONICAL — 2026-05-27)

Lock closure recorded. Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path — a sub-round of Phase 13D.1 — is locked, accepted, and canonical with explicit user approval. Locked artifact lineage: `storytime-phase13d2-static-demo-walkthrough-reviewer-story-path.tar.gz`, SHA-256 `cd553679ce109483b69e99f51fceab34af216c9b1ce7dfe859fc7b78c13cd429`. Phase 13D.2 completed its Phase Closure Protocol: implementation, GPT-5.5 review, and Gemini critique. Gemini returned SAFE TO LOCK with no required edits; the user then locked Phase 13D.2. This is the same after-the-fact lock-recording pattern used for the earlier subphases. The Phase 13D.2 "implementation candidate" entry above is preserved as written and is superseded for status purposes by this lock-closure entry. **Current state after this lock (Phase 13D.2):** Phase 10–12 all closed; Phase 13A–13D.2 all locked; **Phase 13D.2 is the last locked phase**; Phase 13 is STARTED.

## Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary (implementation candidate — pending review — not locked — 2026-05-27)

Implementation round. Phase 13E is a static, **Demo-mode-only**, **non-consequential** sub-round of the locked Phase 13D.2, intended to turn the existing visibly-disabled future-action affordances into explainable, non-executing action previews before any future real local action or mutation work. Per the Phase Closure Protocol it is implementation output, **not** a locked phase: Phase 13E awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 13E does **not** lock Phase 13E, does **not** close Phase 13, and does **not** start Phase 13F or any later Phase 13 subphase.

Phase 13E took the locked Phase 13D.2 artifact `storytime-phase13d2-static-demo-walkthrough-reviewer-story-path.tar.gz` (SHA-256 `cd553679ce109483b69e99f51fceab34af216c9b1ce7dfe859fc7b78c13cd429`, verified on extraction) as its source. It adds a static Demo-mode Action Preview system — `frontend/src/data/actionPreviewAdapter.ts` (typed static view-model holding action-preview definitions and operating-mode constants for Demo / Local / Cloud-Distributed) and `frontend/src/components/ActionPreviewPanel.tsx` plus its CSS Module (presentation panel rendering the selected preview). The panel is integrated into Failure / Recovery, Governance / Safety, and Evidence / Validation **alongside** the existing `DisabledFutureActionCard` (which remains unchanged: a real `<button disabled={true}>` with no `onClick`). A separate, clearly-labelled "Preview action plan" control opens an inline preview panel; the preview never looks like execution. The first set of previews covers retry-failed-stage (target run `run-2026-0520-review`, stage `run-2026-0520-review:governance-gate`), inspect-trust-envelope (target run `run-2026-0520-review`), record-review-decision (target run `run-2026-0520-review`, related disabled action `run-2026-0520-review:open-review`), regenerate-operator-report (target evidence/report surface), and refresh-export (target static export). Phase 13E introduces or clarifies the eventual operating-mode model — **Demo mode** (curated, safe, non-consequential, portfolio-ready; the only mode implemented), **Local mode** (future real local operator workflows; not implemented), and **Cloud / Distributed mode** (future hosted/distributed execution; not implemented) — distinct from the existing **Demo / Active / Candidate** data-snapshot labels.

Confirmed constraints: Phase 13E is a static, Demo-mode-only, export-backed frontend round. It did **not** modify `src/storytime/operator_export.py`, the committed static export JSON, the `storytime export-demo-ui` CLI contract, or `src/storytime/cli/app.py`; all four protected files / contracts are byte-identical to the Phase 13D.2 source (verified by `diff -q`). Phase 13E added no server, no live API, no `fetch`/`axios`/`localhost`/network call, no `localStorage`/`sessionStorage`, no router/hash routing/browser History API, no Context provider, no global preview/action state, no actual retry/rerun/approval/report regeneration/export refresh, no authentication, no Local mode, no Cloud/Distributed mode, no audit-record generation (nothing executed), no production hosting, no fake-execution surface, no snapshot switching, and no dynamic file loading; the disabled future-action affordances remain visibly disabled and carry no mutation handlers — the Phase 13D.1 `DisabledFutureActionCard` was not modified. No `src/`, `pyproject.toml`, `uv.lock`, `frontend/package.json`, `frontend/package-lock.json`, or root dependency changed. The `tests/` changes are the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` to the Phase 13E current-state expectations (current-phase / last-locked / forbidden-future / no-overclaim re-anchored to Phase 13E; new `test_handoff_state_records_phase_13d2_locked` check; prior 13E-explicit framing check renamed to `test_handoff_state_addresses_phase_13f_explicitly`; future-phase fragment scan advanced to `13f`/`13g`; the append-only lock-record checks now also require the Phase 13D.2 lock record), and one new `tests/test_action_preview_data_integrity.py` that asserts run-id and stage-id targets referenced by the action-preview adapter exist in the committed static export — at minimum asserting `run-2026-0518-golden` and `run-2026-0520-review` are present in both. Coverage is strengthened, not weakened. The append-only locked-decision documents `docs/canonical-state.md` and this `docs/phase-history.md` round log were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

**Current state after this round (Phase 13E):** Phase 10A–10G all locked; **Phase 10 CLOSED**; Phase 11A–11D all locked; **Phase 11 — Release Candidate Hardening — CLOSED**; Phase 12A–12D all locked; **Phase 12 — Portfolio / SE Demo Packaging — CLOSED**; Phase 13A locked; Phase 13B locked; Phase 13C locked; Phase 13D locked; Phase 13D.1 locked; Phase 13D.2 locked; **Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path — is the last locked phase**; **Phase 13 — Portfolio Website / Operator GUI — is STARTED**; Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary — is an implementation candidate, pending review, **not locked**. Phase 13F and every later Phase 13 subphase have not started; Phase 13 is not closed. Phase 9C remains optional/not scheduled.

## Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary (LOCKED / ACCEPTED — 2026-05-27)

Lock closure recorded. Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary — a sub-round of Phase 13D.2 — is locked and accepted with explicit user approval. Locked artifact `storytime-phase13e-demo-mode-action-preview-operator-intent-boundary.tar.gz`, SHA-256 `a997f2ca9d213e28e140f47c63336367c8feda46ed994b41300f86b99f8d8164`. Phase 13E completed the Phase Closure Protocol — implementation, GPT-5.5 review, and Gemini critique; Gemini returned SAFE TO LOCK with no required edits, and the user, as final decision-maker, then locked Phase 13E. This is the same after-the-fact lock-recording pattern used for the earlier Phase 13 subphases; the Phase 13F round records this lock and did not re-perform the reviews. The protected Phase 13D.2 boundary held (`src/storytime/operator_export.py`, the committed static export JSON, the `storytime export-demo-ui` CLI contract, and `src/storytime/cli/app.py` byte-identical to the Phase 13D.2 source; `DisabledFutureActionCard` byte-identical and truly disabled). Phase 13E is the source/base artifact for Phase 13F. The Phase 13E "implementation candidate" entry earlier in this append-only log is preserved as written and is superseded for status purposes by this lock-closure entry.

**Current state after this lock (Phase 13E):** Phase 10A–10G locked / **Phase 10 CLOSED**; Phase 11A–11D locked / **Phase 11 CLOSED**; Phase 12A–12D locked / **Phase 12 CLOSED**; Phase 13A–13D, 13D.1, 13D.2, 13E all locked; **Phase 13E is the last locked phase**; **Phase 13 STARTED**. Phase 13F is the implementation candidate in the round below. Phase 9C optional/not scheduled.

## Phase 13F — Local Bridge Architecture & Contract Baseline (implementation candidate — pending review — not locked — 2026-05-27)

Implementation round. Phase 13F is a documentation-and-static-fixture architecture / contract baseline sub-round of the locked Phase 13E — the architectural lock before any Python local-bridge implementation is allowed (it is to the Local Bridge what Phase 13A was to the operator GUI). Per the Phase Closure Protocol it is implementation output, **not** a locked phase: it awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval. Phase 13F does **not** lock Phase 13F, does **not** close Phase 13, and does **not** start Phase 13G.

Phase 13F took the locked Phase 13E artifact (SHA-256 `a997f2ca9d213e28e140f47c63336367c8feda46ed994b41300f86b99f8d8164`, verified on extraction) as its source. It adds eleven new architecture / contract docs (`docs/local-bridge-architecture.md` with the execution-timing policy and Gemini-risk table, `docs/externalized-state-architecture.md`, `docs/browser-storage-policy.md`, `docs/local-mode-workspace-layout.md`, `docs/storage-targets-architecture.md`, `docs/action-execution-boundary.md`, `docs/local-action-dto-spec.md`, `docs/local-action-audit-spec.md`, `docs/local-mode-storage-contract.md`, `docs/local-action-queue-observability.md`, `docs/phase13f-local-bridge-contract-readiness.md`), a set of non-runtime JSON example fixtures under `docs/examples/` (labelled future / documentation-only), and one new Python test (`tests/test_local_mode_contract_examples.py`) validating those fixtures with plain Python (no JSON-schema dependency). It establishes the central principle that the frontend is an operator surface, not the durable storage layer (durable state lives outside the browser in an explicit workspace / storage target, avoiding the RoundTable browser-storage failure mode), and settles the Hybrid Option C decisions: the async execution-timing policy (`202 Accepted` + `actionRequestId`/`jobId`, acceptance ≠ success, export refresh after a durable write, refresh-race avoidance), the loopback-only / strict-origin / no-arbitrary-command / command-pattern-router security boundary, the action allowlist (`retry_failed_stage`, `inspect_trust_envelope`, `refresh_export`) with higher-risk actions deferred, and the queue-observability model with a conservative local load-limit policy and distributed/cloud carry-forward.

Confirmed constraints: Phase 13F implements **no** runtime code. It did **not** modify `src/`, `frontend/src/` (including `frontend/src/data/storytime-demo-export.json`), `frontend/package.json`, `frontend/package-lock.json`, `pyproject.toml`, or `uv.lock`; all byte-identical to the locked Phase 13E source (verified by `diff -q`). No local bridge, no server, no async queue, no queue workers, no queue metrics / exporters, no OpenTelemetry, no storage providers, no provider integrations, no runtime schema validation, no router / history, no browser storage, no real Local mode, no Cloud/Distributed mode, and no mutation / action execution were implemented; the browser remains non-durable and the example fixtures are documentation artifacts only. The only `tests/` changes are the narrow, explicitly authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` to the Phase 13F current-state expectations (current-phase / last-locked / forbidden-future / no-overclaim re-anchored to Phase 13F; new `test_handoff_state_records_phase_13e_locked` check; prior 13F-explicit framing check renamed to `test_handoff_state_addresses_phase_13g_explicitly`; future-phase fragment scan advanced to `13g`/`13h`; the append-only lock-record checks now also require the Phase 13E lock record), and the new `tests/test_local_mode_contract_examples.py`. Coverage is strengthened, not weakened. The append-only locked-decision documents `docs/canonical-state.md` and this `docs/phase-history.md` round log were not rewritten — this entry is a new append, and historical chronology is preserved throughout.

**Current state after this round (Phase 13F):** Phase 10A–10G locked / **Phase 10 CLOSED**; Phase 11A–11D locked / **Phase 11 CLOSED**; Phase 12A–12D locked / **Phase 12 CLOSED**; Phase 13A–13D, 13D.1, 13D.2, 13E all locked; **Phase 13E is the last locked phase**; **Phase 13 STARTED**; Phase 13F — Local Bridge Architecture & Contract Baseline — is an implementation candidate, pending review, **not locked**. Phase 13G and every later Phase 13 subphase have not started; Phase 13 is not closed. Phase 9C optional/not scheduled.

---

---

## Appendix — Historical RoundTable Lineage, Phases 0–7 (Historical RoundTable export, 2026-05-24)

> **Historical recovery input — not current state.** This appendix summarizes
> early StoryTime lineage reconstructed from the RoundTable full-project export
> `ROUNDTABLE_PROJECT_StoryTime__formerly_podcast_pipeline__2026-05-24.json`
> (RoundTable schema 0.11.0, exported 2026-05-24T01:01:02Z). That export is
> **stale**: its newest StoryTime round is Round 22 (Phase 7C planning). It is
> **superseded by later Phase 8–10 artifact history** and by the current
> Phase 10 closure recorded above and in `docs/canonical-state.md`. Per the
> chronology rule, where this appendix and later locked artifact history
> conflict, **the later locked history wins**. This appendix was added by the
> Post-Phase-10 Historical State Reconciliation; it adds no current-state
> authority. The current state remains: Phase 10G locked, Phase 10 CLOSED,
> Phase 11 — Release Candidate Hardening — not started.

This appendix complements the Round 1–18 table at the top of this file; it does
not replace it. Its purpose is cold-session continuity for the early
process/doctrine lineage that the terse table rows under-capture.

**Project origin and RoundTable-native restart.** StoryTime was formerly named
*Podcast Pipeline*. Early in the RoundTable workflow (Round 1, 2026-05-21) the
project adopted a **RoundTable-native restart doctrine**: pre-existing legacy
planning artifacts could not be treated as canonical; they had to be re-ratified
natively through Phase 0 and Phase 1, making the RoundTable canonical history —
not the legacy artifacts — the source of truth. Any prior external scaffold was
retained only as non-canonical reference. A public-facing record rule was also
set: private future-platform names are replaced with "future projects" in
public-facing canonical artifacts.

**Planning ratification (Phases 0–1 and the Phase Closure Protocol).** Round 2
recorded multi-model agreement (GPT-5.5, Claude Opus 4.7, Gemini 3 Thinking)
that StoryTime should not enter Phase 2 implementation until the legacy planning
was ratified inside RoundTable, and named three canonical documents to produce:
`docs/product-charter.md`, `docs/architecture-baseline.md`, and
`docs/phase-closure-protocol.md`. Round 2 also stated eleven hard architectural
decisions (among them: `pipeline_run_id` is the durable correlation key, not
`trace_id`; only the telemetry adapter may import OpenTelemetry; stages
communicate through artifact envelopes, not shared mutable memory; approval is a
persisted pipeline stage; the source manifest is a closed CC0 / US-public-domain
schema; import direction is mechanically enforced). Round 3 accepted a Gemini
critique and rejected generating all three documents in one mega-prompt
(truncation/compression risk), adopting **one canonical document per round**
(3.1 Charter, 3.2 Architecture Baseline, 3.3 Phase Closure Protocol, 3.4
verification/lock), with the rule that document-generation models may transcribe
ratified decisions but may not resolve open architectural ambiguities.

- **Phase 0 — Product Charter: locked (Round 4).** GPT-5.5 generated
  `docs/product-charter.md`; Gemini found Sections 1–13 strong and flagged a
  blocking issue in Section 15 (it defined document-lock criteria rather than
  product/MVP acceptance criteria); GPT-5.5 produced a surgical Section 14/15
  patch; Gemini accepted it; Phase 0 was locked.
- **Phase 1 — Architecture Baseline: locked (Round 5).** Claude Opus 4.7
  generated `docs/architecture-baseline.md`; Gemini reviewed it as ready to lock
  with no required edits. Clarifications A1 (stage-specific adapters such as TTS
  are not placed in the global RunnerContext) and A2 (`StateUpdate` is bundled
  inside `StageResult`) were accepted as canonical.
- **Phase Closure Protocol: locked (Round 6).** GPT-5.5 generated
  `docs/phase-closure-protocol.md`; Gemini verified it against all 23 acceptance
  criteria and recommended lock. With all three planning documents locked, the
  RoundTable-native restart was complete at the planning-governance level.

**Phases 2–5 implementation lineage.**

- **Phase 2 — Repo Scaffold + Local Development Environment: locked (Rounds
  7–8).** Round 7 resolved Phase 2 prerequisites and chose the high-assurance
  route — Claude Opus 4.7 builds the scaffold; Claude Sonnet 4.6 is reserved for
  bounded cleanup only. Ten prerequisite corrections were accepted, including:
  `event_log` is an append-only SQLite table (not JSONL) and forensic/audit-only
  in Phase 2; event persistence and state updates share a transaction where
  practical; `# ARCH-LOCK` / `# DO NOT REFACTOR` annotations defend load-bearing
  boundaries (missing ones are a scaffold rejection condition); `ffmpeg` is not
  required for Phase 2 tests but a `doctor` check is; `uv` is preferred with
  pinned versions; canonical state is mirrored into `docs/canonical-state.md` as
  an append-only locked-decision log. Round 8: Opus implemented the scaffold,
  GPT-5.5 reviewed and smoke-verified, Gemini found it architecturally ready and
  requested one administrative cleanup (replace repo marker docs with the full
  locked canonical documents); Phase 2 was locked.
- **Phase 3 — Thin Vertical Slice MVP: locked (Round 9).** Opus-first
  implementation of ingest → synthesize → assemble → publish persisted to
  SQLite; Gemini identified two cleanup blockers (restore the granular CLI
  command surface; add `storytime.pipeline` to import-linter coverage); Claude
  completed the bounded cleanup; GPT and Gemini confirmed; Phase 3 was locked.
- **Phase 4 / 4.1 — Interactive Approval & Pipeline Rehydration: locked (Round
  10).** Opus implemented persisted approval gates and resume/rehydration;
  Gemini raised semantic caveats (opt-in approval, rejected-run status, duplicate
  approval-event taxonomy); the Phase 4.1 cleanup separated source/manifest
  approval from operator approval and wired the audio approval gate. Mediator
  rulings: approval stays opt-in for Phase 4/4.1; rejected approvals map to run
  status `failed`; full W3C linked-trace propagation was deferred to Phase 5
  rather than faked.
- **Phase 5 — OpenTelemetry Instrumentation Foundation: locked (Round 11).**
  Opus implemented one `pipeline.run` / `pipeline.resume` span model with child
  stage spans, a real W3C `Link` from a resumed run's trace to the pre-pause
  trace, and a closed metric instrument set; OpenTelemetry stayed confined to
  one adapter module with `NoopTelemetry` as the default. OI-2 (trace-link
  propagation) was closed with a genuine implementation.

**Phase 6–7 planning and recovery lineage.**

- **Phase 6 split (Round 12).** Phase 6 was split into Phase 6A (Observability
  Infrastructure, Dashboards-as-Code, Demo Harness) and Phase 6B (SLO narrative,
  runbooks, demo walkthrough, documentation polish), with Phase 6A routed
  Opus-first. A standing constraint was recorded: dashboards chart only the
  eight real Phase 5 metrics, and there is to be **no custom telemetry schema** —
  telemetry must be able to feed any backend. (The repo's own later history
  records the out-of-band Phase 6S execution and the Phase 6A/6B locks.)
- **Phase 7B planning (Round 16).** GPT-5.5 and Gemini agreed on Option B1 —
  uncontainerized per-slot StoryTime processes plus a higher-assurance
  front-door / active-slot switching model — and explicitly rejected/deferred
  app containerization (B2), docs-only (B3), and Kubernetes/Terraform (B4). No
  Architecture Baseline amendment was approved; app containerization remained
  prohibited absent an explicit future baseline amendment.
- **RoundTable desync / recovery checkpoint (Round 20).** RoundTable
  experienced a state-sync/desync issue while the user worked ahead through
  Phase 7A, Phase 7B planning, and Phase 7B implementation. The project was
  resynced by an explicit recovery checkpoint that recovered the true state:
  Phase 7A accepted as lean blue/green Option A; Phase 7B implementation output
  produced but not yet locked pending Gemini review of the actual artifact (an
  earlier Gemini response had reviewed the implementation *prompt*, not the
  output). The checkpoint instruction was to resume from the checkpoint and not
  replay prior rounds — the same "prefer the newest explicit recovery
  checkpoint" doctrine this repository's State Preservation Bundle still uses.
- **Phase 7B lock (Round 21)** and **Phase 7C planning (Round 22)** are the last
  StoryTime rounds in the export: Gemini reviewed the actual Phase 7B artifact
  and it was locked, and Round 22 began Phase 7C as a formal Architecture
  Baseline Amendment planning round (app containerization / cloud-deploy
  readiness), deferring Phase 8 multi-backend telemetry fan-out until the
  amendment planning completed. Everything after Round 22 — Phase 7C, Phase 7D,
  Phases 8–10, and the Phase 10 closure — is recorded in this repository's own
  later history above, which supersedes this export.

**Model-routing doctrine (historical, observed across Phases 0–7).** The
RoundTable workflow used a consistent multi-model division of labour:
**GPT-5.5** as mediator/architect and first reviewer; **Claude Opus 4.7** as the
high-assurance implementer for architecture-sensitive work; **Gemini 3 Thinking**
as the independent critic/reviewer after implementation; **Claude Sonnet 4.6**
reserved for bounded cleanup, targeted fixes, and test additions only. The
export's compatibility notes also recorded per-model cautions (e.g. GPT-5.5
thinking-mode responses may omit section headers; Gemini may drift adversarial
without explicit framing; Opus may truncate on very large refactors; Sonnet
context-compaction may drop detail; Haiku may pad short summaries). This doctrine
is descriptive history — it is not a current routing instruction.


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
