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
**Status:** Phase 13F — Local Bridge Architecture & Contract Baseline — is an **implementation candidate, pending review — NOT locked.** Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary — is **LOCKED** and is the last locked phase (SHA-256 `a997f2ca9d213e28e140f47c63336367c8feda46ed994b41300f86b99f8d8164`). Phase 13 — Portfolio Website / Operator GUI — remains **STARTED** and is not closed. Phase 13G and every later Phase 13 subphase have not started.

Phase 13F is a documentation-and-static-fixture architecture / contract baseline — the architectural lock before any Python local-bridge implementation is allowed (to the Local Bridge what Phase 13A was to the operator GUI). It establishes that the frontend is an operator surface, not the durable storage layer (durable state lives outside the browser in an explicit workspace / storage target, avoiding the RoundTable browser-storage failure mode); it adds eleven new architecture / contract docs, non-runtime JSON example fixtures under `docs/examples/`, and one new Python contract-examples test; and it settles the future local-bridge execution-timing policy (async, `202 Accepted` + `actionRequestId`/`jobId`, acceptance ≠ success, export refresh after a durable write), the loopback-only / strict-origin / no-arbitrary-command / command-pattern-router security boundary, the action allowlist (`retry_failed_stage`, `inspect_trust_envelope`, `refresh_export`) with higher-risk actions deferred, and the queue-observability model. Phase 13F implements **no** runtime code (no local bridge, no server, no async queue, no workers, no metrics exporters, no OpenTelemetry, no storage providers, no real Local mode, no Cloud/Distributed mode, no mutation execution); the browser remains non-durable; `src/`, `frontend/src/`, `frontend/package.json`, `frontend/package-lock.json`, `pyproject.toml`, `uv.lock`, and `frontend/src/data/storytime-demo-export.json` are byte-identical to the locked Phase 13E source. Per the Phase Closure Protocol it awaits GPT-5.5 review, Gemini critique, any cleanup, and an explicit user lock decision; it does not lock Phase 13F, close Phase 13, or start Phase 13G.

---

# Phase 13E implementation-candidate note — Demo-Mode Action Preview / Operator Intent Boundary (historical — Phase 13E is LOCKED; see the Phase 13F note above)

**Date:** 2026-05-27
**Status:** Historical record. Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary — has since been **LOCKED** and is the last locked phase; Phase 13F is the current implementation candidate (see above). Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path — was the last locked phase when this note was written.

Phase 13E is the first sub-round to explicitly model operator intent
rather than only displaying read-only state — but it is deliberately a
**Demo-mode**, non-consequential sub-round of Phase 13D.2. It adds a
static Demo-mode Action Preview system
(`frontend/src/data/actionPreviewAdapter.ts` plus
`frontend/src/components/ActionPreviewPanel.tsx` and its CSS Module)
that turns the existing visibly-disabled future-action affordances
into explainable, non-executing action previews. A "Preview action
plan" control opens an inline preview panel alongside the existing
`DisabledFutureActionCard`, which is unchanged (still a real
`<button disabled={true}>` with no `onClick`). The first set of
previews covers retry-failed-stage, inspect-trust-envelope,
record-review-decision, regenerate-operator-report, and refresh-export.

Phase 13E introduces or clarifies the eventual operating-mode model
— **Demo mode** (the only mode implemented), **Local mode** (future
real local operator workflows; not implemented), and **Cloud /
Distributed mode** (future hosted/distributed execution; not
implemented) — distinct from the existing Demo / Active / Candidate
**data-snapshot** labels. The previews never look like execution:
no fake loading spinner, no simulated success, no `setTimeout`
workflow, and no "Submitted" / "Succeeded" / "Audit created"
rendering anywhere. The user journey ends at an explicitly disabled
execution boundary.

Phase 13E is static, Demo-mode-only, and export-backed. It adds no
server, no live API, no `fetch`/`axios`/`localhost`/network call, no
`localStorage`/`sessionStorage`, no router/hash routing/browser
History API, no Context provider, no global preview/action state, no
actual retry / rerun / approval / report regeneration / export
refresh, no authentication, no Local mode, no Cloud/Distributed
mode, no audit-record generation, no production hosting, and no
fake-execution surface. It does **not** modify the protected backend
contract files (`src/storytime/operator_export.py`,
`frontend/src/data/storytime-demo-export.json`,
`src/storytime/cli/app.py`, the `storytime export-demo-ui` CLI
contract) — all four are byte-identical to the Phase 13D.2 source.
`pyproject.toml`, `uv.lock`, `frontend/package.json`, and
`frontend/package-lock.json` are unchanged.

Per the Phase Closure Protocol, Phase 13E is an implementation
candidate, pending review, **not locked**. It does not lock Phase
13E, does not close Phase 13, and does not start Phase 13F.

*(The Phase 13D.2-era note below is a historical record. Phase 13D.2
is LOCKED; Phase 13E is the current implementation candidate.)*

---
# Phase 13D.2 implementation-candidate note — Static Demo Walkthrough / Reviewer Story Path (historical record — Phase 13D.2 is LOCKED; see the Phase 13E note above)

**Date:** 2026-05-27
**Status:** Historical record. Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path — was the implementation candidate when this note was written. Phase 13D.2 has since been **LOCKED** and is the last locked phase; Phase 13E is now the current implementation candidate — see the Phase 13E note above. Phase 13 — Portfolio Website / Operator GUI — remains **STARTED** and is not closed. Phase 13F and every later Phase 13 subphase have not started.

Phase 13D.2 is the static / read-only demo-readiness sub-round of Phase
13D.1. It turns the existing operator GUI views into a coherent guided
reviewer / demo path so a hiring manager, Solutions Engineer leader,
technical reviewer, or self-guided portfolio visitor can understand
what StoryTime is, what to inspect first, why the static export
boundary matters, how governance and failure handling prove
operational maturity, how Evidence / Validation backs the claims, what
is intentionally disabled, what Phase 13E would enable later, and how
the backend / frontend architecture works at a high level. It replaces
the honest Demo Walkthrough placeholder with a real read-only view
(`frontend/src/components/DemoWalkthroughView.tsx` plus its CSS Module)
backed by a static view-model adapter
(`frontend/src/data/demoWalkthroughAdapter.ts`). The view offers four
reviewer routes — a 5-minute scan, a 10-minute SE-style demo, a
technical deep-dive, and a self-guided reviewer path — switched by a
simple segmented control backed by local `useState<RouteId>` (no
router, no Context, no persistence). Each step carries title, target
view, what to inspect, what it proves, talking points, and an in-line
navigation affordance into the relevant existing view; steps that
point to a specific run identify it by stable id
(`run-2026-0518-golden` or `run-2026-0520-review`). The view also
includes architecture-checkpoint cards (local-first design,
deterministic static export, backend-owns-truth /
frontend-owns-understanding, read-only operator surface, static
evidence boundary, disabled-action boundary, Demo / Active /
Candidate as **data snapshots, not deployment environments**, and
why Phase 13E must be explicitly gated); a deliberate "what is
intentionally deferred" section; and interview / SE talking-point
callout cards. Phase 13D.2 absorbs ~80–90% of an Architecture Story
narrative via these embedded checkpoints but does NOT implement a
full standalone Architecture Story page — that stays deferred.

Phase 13D.2 is a static, read-only, export-backed frontend round. It
does **not** modify the backend export generator
(`src/storytime/operator_export.py`), the committed static export
JSON (`frontend/src/data/storytime-demo-export.json`), the `storytime
export-demo-ui` CLI contract, or `src/storytime/cli/app.py`; all four
protected files / contracts are byte-identical to the Phase 13D.1
source. Phase 13D.2 adds no server, no live API, no `fetch`/`axios`/
`localhost`/network call, no mutation, no authentication, no cloud
deployment, no production hosting, no dynamic file loading, and no
Demo / Active / Candidate switching. No `src/`, `pyproject.toml`,
`uv.lock`, `frontend/package.json`, `frontend/package-lock.json`, or
root dependency changed. Its only `tests/` change is the narrow,
explicitly authorized mechanical advance of the state-discipline
guard to the Phase 13D.2 current-state expectations.

Per the Phase Closure Protocol, Phase 13D.2 does not lock Phase
13D.2, does not close Phase 13, and does not start Phase 13E. Phase
13E and later subphases are future, planned work only — decomposed
in `docs/phase13-roadmap.md`.

*(Every Phase 13D.1-era and earlier note below is a historical
record. Phase 13D.1 is LOCKED; Phase 13D.2 is the current
implementation candidate. The "# StoryTime Roadmap" section below
carries the authoritative current plan.)*

---
# Phase 13D.1 implementation-candidate note — Static Operator GUI Refinement / Evidence & Disabled Action Discipline (locked — historical record; see the Phase 13D.2 note above)

**Date:** 2026-05-27
**Status:** Historical record. This note described Phase 13D.1 while it was an implementation candidate. Phase 13D.1 has since been **LOCKED** and is the last locked phase; Phase 13D.2 is now the current implementation candidate — see the Phase 13D.2 note above and the "# StoryTime Roadmap" section below.

Phase 13D.1 is the static / read-only refinement sub-round of Phase 13D. It
strengthens the operator GUI and portfolio / reviewer flow before any
future controlled local action or mutation-boundary work. It standardizes
the disabled future-action display across views into a reusable typed
component
(`frontend/src/components/DisabledFutureActionCard.tsx` plus its CSS
Module) backed by real `<button disabled={true}>` elements with no
`onClick` handlers and no fake mutation props; replaces the honest
Evidence / Validation placeholder with a real read-only **Evidence /
Validation** view
(`frontend/src/components/EvidenceValidationView.tsx` plus its CSS Module)
that carries the mandatory **STATIC PORTFOLIO DATA — NOT A LIVE CI/CD
DASHBOARD** disclaimer, points to repository-relative evidence
(`docs/verification-log.md`, `docs/frontend-static-export-contract.md`,
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

Phase 13D.1 is a static, read-only, export-backed frontend round. It
does **not** modify the backend export generator
(`src/storytime/operator_export.py`), the committed static export JSON
(`frontend/src/data/storytime-demo-export.json`), the `storytime
export-demo-ui` CLI contract, or `src/storytime/cli/app.py`; all four
protected files / contracts are byte-identical to the Phase 13D source.
Phase 13D.1 adds no server, no live API, no `fetch`/`axios`/`localhost`/
network call, no mutation, no authentication, no cloud deployment, and
no production hosting. No `src/`, `pyproject.toml`, `uv.lock`, or root
dependency changed. Its only `tests/` change is the narrow, explicitly
authorized mechanical advance of the state-discipline guard to the
Phase 13D.1 current-state expectations.

Per the Phase Closure Protocol, Phase 13D.1 does not lock Phase 13D.1,
does not close Phase 13, and does not start Phase 13E. Phase 13E and
later subphases are future, planned work only — decomposed in
`docs/phase13-roadmap.md`.

*(Every Phase 13D-era and earlier note below is a historical record.
Phase 13D is LOCKED; Phase 13D.1 is the current implementation
candidate. The "# StoryTime Roadmap" section below carries the
authoritative current plan.)*

---
# Phase 13D implementation-candidate note — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) (locked — historical record; see the Phase 13D.1 note above)

**Date:** 2026-05-27
**Status:** Historical record. This note described Phase 13D while it was an implementation candidate. Phase 13D has since been **LOCKED** and is the last locked phase; Phase 13D.1 is now the current implementation candidate — see the Phase 13D.1 note above and the "# StoryTime Roadmap" section below.

Phase 13D is the fourth subphase of Phase 13. It is a frontend-only round
that takes the locked Phase 13C deterministic static export contract and
expands two of the Phase 13B/13C placeholder views into real read-only
operator views: **Governance / Safety** (per-run Trust Envelope decisions,
source authorization categories, the governance-gate result per run, the
display-discipline honesty list, evidence references, and the
visibly-disabled future review actions) and **Failure / Recovery** (the
failure / review queue joined to per-run failure summaries, affected
stage, related governance decision, evidence links, the operator
inspect-next guidance, and visibly-disabled recovery actions, with an
inspect-this-run drill-down callback into the existing Pipeline Run Detail
view). The view choice and ordering follow the Phase 13C deferred-work
register's view-expansion recommendation.

Phase 13D adds two new view components and their CSS Modules
(`frontend/src/components/GovernanceSafetyView.tsx` /
`GovernanceSafetyView.module.css` and
`frontend/src/components/FailureRecoveryView.tsx` /
`FailureRecoveryView.module.css`), two domain-specific view-model adapters
(`frontend/src/data/governanceAdapter.ts` and
`frontend/src/data/failureAdapter.ts`) that project the locked Phase 13C
export, an ambient CSS-Modules TypeScript declaration
(`frontend/src/types/css-modules.d.ts`), App-level navigation rewiring with
a "Data source · Demo Snapshot" header chip backed by the existing
`EXPORT_META` adapter export and an inspect-this-run drill-down callback
into the existing Pipeline Run Detail view (plain prop drilling, no
router). It synchronizes the State Preservation Bundle.

Phase 13D is a static, read-only, export-backed frontend round. It does
**not** modify the backend export generator
(`src/storytime/operator_export.py`), the committed static export JSON
(`frontend/src/data/storytime-demo-export.json`), or the `storytime
export-demo-ui` contract; both protected files are byte-identical to the
Phase 13C source. Phase 13D adds no server, no live API, no `fetch`/
`axios`, no mutation, no authentication, no cloud deployment, and no
production hosting; recovery / review affordances are surfaced as
visibly-disabled future actions labelled with the phase that would enable
them (Phase 13E). No `src/`, `pyproject.toml`, `uv.lock`, or root
dependency changed. Its only `tests/` change is the narrow, explicitly
authorized mechanical advance of the state-discipline guard
`tests/test_failure_mode_regression.py` to the Phase 13D current-state
expectations.

Per the Phase Closure Protocol, Phase 13D does not lock Phase 13D, does
not close Phase 13, and does not start Phase 13E. Phase 13E and later
subphases are future, planned work only — decomposed in
`docs/phase13-roadmap.md`.

*(Every Phase 13C-era and earlier note below is a historical record. Phase
13C is LOCKED; Phase 13D is the current implementation candidate. The
"# StoryTime Roadmap" section below carries the authoritative current
plan.)*

---
# Phase 13C implementation-candidate note — Deterministic Read-Only Static Export / Frontend Data Alignment (locked — historical record; see the Phase 13D note above)

**Date:** 2026-05-27
**Status:** Historical record. This note described Phase 13C while it was an implementation candidate. Phase 13C has since been **LOCKED** and is the last locked phase; Phase 13D is now the current implementation candidate — see the Phase 13D note above and the "# StoryTime Roadmap" section below.

Phase 13C is the third subphase of Phase 13. It establishes a truthful,
reproducible, read-only data boundary between backend truth and the Phase 13B
frontend — realizing the "backend owns truth, frontend owns understanding"
contract. It adds a small read-only backend export module
(`src/storytime/operator_export.py`) and a `storytime export-demo-ui` CLI
command that produce a deterministic static JSON export
(`frontend/src/data/storytime-demo-export.json`, carrying a top-level
`schemaVersion`); the export contract document
`docs/frontend-static-export-contract.md`; the frontend deferred-work register
`docs/frontend-gui-deferred-work-register.md`; a frontend adapter
(`frontend/src/data/adapter.ts`) and a `StaticDemoExport` type; backend
contract tests (`tests/test_operator_export.py`); and it rewires the homepage
and Pipeline Run Detail / Stage Timeline to consume the export through the
adapter. It synchronized the State Preservation Bundle.

Phase 13C is a static, read-only data-boundary round. The export is
deterministic — built from fixed demo data, no `datetime.now()`, no `uuid`, no
randomness; generating it twice yields byte-identical JSON. Phase 13C does not
make the frontend live: no server, no live API, no `fetch`/`axios`, no
mutation, no authentication, no cloud deployment, no production hosting. Unlike
Phase 13B it adds small backend code, but that code is read-only and
deterministic and changes no core pipeline runtime behaviour, no governance, no
telemetry, no root dependency, and no `uv.lock`. Its `tests/` changes are the
new `tests/test_operator_export.py` and the narrow, explicitly authorized
mechanical advance of the state-discipline guard to the Phase 13C current-state
expectations.

Per the Phase Closure Protocol, Phase 13C does not lock Phase 13C, does not
close Phase 13, and does not start Phase 13D. Phase 13D and later subphases are
future, planned work only — decomposed in `docs/phase13-roadmap.md`.

*(Every Phase 13B-era and earlier note below is a historical record. Phase 13B
is LOCKED; Phase 13C is the current implementation candidate. The
"# StoryTime Roadmap" section below carries the authoritative current plan.)*

---
# Phase 13B implementation-candidate note — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold (locked — historical record; see the Phase 13C note above)

**Date:** 2026-05-27
**Status:** Historical record. This note described Phase 13B while it was an implementation candidate. Phase 13B has since been **LOCKED** and is the last locked phase; Phase 13C is now the current implementation candidate — see the Phase 13C note above and the "# StoryTime Roadmap" section below.

Phase 13B is the second subphase of Phase 13 and the first round that writes
frontend code. Against the locked Phase 13A architecture contract it implements
a deliberately bounded frontend: a typed static portfolio shell plus one visual
operator view. It adds a new top-level `frontend/` directory — a React +
TypeScript (strict) + Vite project, standard CSS, and no external UI /
component / state / charting library — containing the frontend read-model
contract, a static demo dataset of exactly two mock pipeline runs, the
portfolio homepage, one Pipeline Run Detail view with a visual Stage Timeline,
honest placeholders for the future portfolio sections and operator views, and a
frontend README. It lightly updates `README.md` and synchronizes the State
Preservation Bundle.

Phase 13B is a static, read-only, demo-data-backed shell. It is not
backend-connected, uses no live or runtime data, implements no mutations
(retry, re-run, and review-decision actions appear only as visibly-disabled
affordances), and is not production-hosted or cloud-deployed; it contacts no
backend. It changed no backend `src/` content, `pyproject.toml`, `uv.lock`,
pipeline behaviour, CLI, API, telemetry, or Docker behaviour; its only `tests/`
change is the narrow, explicitly authorized mechanical advance of the
state-discipline guard to the Phase 13B current-state expectations.

Per the Phase Closure Protocol, Phase 13B does not lock Phase 13B, does not
close Phase 13, and does not start Phase 13C. Phase 13C and later subphases are
future, planned work only — decomposed in `docs/phase13-roadmap.md`.

*(Every Phase 13A-era and earlier note below is a historical record. Phase 13A
is LOCKED; Phase 13B is the current implementation candidate. The
"# StoryTime Roadmap" section below carries the authoritative current plan.)*

---
# Phase 13A implementation-candidate note — Portfolio Website / Operator GUI Architecture Baseline (locked — historical record; see the Phase 13B note above)

**Date:** 2026-05-27
**Round type:** Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — documentation-only architecture-baseline round (documentation only).
**Status:** Historical record. This note described Phase 13A while it was an implementation candidate. Phase 13A has since been **LOCKED** and is the last locked phase; Phase 13B is now the current implementation candidate — see the Phase 13B note above and the "# StoryTime Roadmap" section below.

Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — is now
**LOCKED** and is the last locked phase. **Phase 12 — Portfolio / SE Demo
Packaging — is CLOSED** (Phase 12A through 12D all locked). Phase 12D completed
its Phase Closure Protocol out-of-band: the Gemini review returned the verdict
to lock Phase 12D and close Phase 12, with no required edits, and the user then
locked Phase 12D and formally closed Phase 12. Phase 12E was optional,
contingency-only work; the Phase 12D review found no substantive gap, so
Phase 12E was not needed and never started. **Phase 13 — Portfolio Website /
Operator GUI — is STARTED.** Phase 13B and every later Phase 13 subphase have
**not** started — they are future, planned work, decomposed in the Phase 13
roadmap section below and in `docs/phase13-roadmap.md`.

Phase 13A is the first subphase of Phase 13 — Portfolio Website / Operator
GUI — the phase that follows the closed Phase 12. It is a documentation-only
architecture-baseline round: it designs the portfolio website and the
decoupled operator GUI on paper, and refines the earlier `docs/GUI_vision.md`
sketch into an authoritative Phase 13 plan. It adds five `docs/` documents —
`phase13-portfolio-website-architecture.md`, `frontend-backend-contract.md`,
`phase13-roadmap.md`, `portfolio-website-content-model.md`, and
`operator-gui-view-model.md` — lightly updates `README.md`, advances the
state-discipline guard `tests/test_failure_mode_regression.py` under the
narrow, explicitly authorized mechanical exception, and synchronizes the State
Preservation Bundle. It changes no `src/`, `pyproject.toml`, `uv.lock`,
dependency, product, runtime, API, CLI, or telemetry behaviour.

Phase 13A is a planning round; it does **not** implement the portfolio
website and does **not** implement the operator GUI. It adds no React, Vite,
TypeScript, JavaScript, CSS, or HTML application code, no `frontend/` /
`web/` / `app/` directory, no `package.json` or `vite.config`, no UI, no
server, and no new dependency. Per the Phase Closure Protocol, Phase 13A is an
implementation candidate, pending review — it is **not** a locked phase until
GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval
complete. Phase 13A does **not** lock Phase 13A, does **not** close Phase 13,
and does **not** start Phase 13B.

*(The "StoryTime Roadmap" body below — and the Phase 13 roadmap section — are
the durable forward-looking roadmap; `docs/handoff-state.md` is authoritative
for current status. The Phase 12D-era and Phase 12C-era notes below — and the
Phase 12B-era, Phase 12A.1, Phase 12A, and Phase 11x notes further below — are
historical records. Phase 12D is locked and Phase 12 is closed; Phase 13A is
the current implementation candidate.)*

---

# Phase 12D note — Phase 12 Closure Plan / Final Portfolio Handoff Definition (locked — Phase 12 CLOSED — historical record; see the Phase 13A note above)

**Date:** 2026-05-26
**Round type:** Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — documentation-only closure-definition round (documentation only).
**Status:** Historical record. This note described Phase 12D while it was an implementation candidate. Phase 12D has since been **LOCKED**, and with it **Phase 12 — Portfolio / SE Demo Packaging — is CLOSED**; Phase 13A is now the current implementation candidate — see the Phase 13A note above.

Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — was, at the
time of this round, the last locked phase; Gemini returned SAFE TO LOCK with no
required edits and the user locked Phase 12C. **Phase 12 — Portfolio / SE Demo
Packaging — has since been CLOSED**, with Phase 12D as its final locked
subphase. Phase 12E was optional, contingency-only work — it would have existed
only if the Phase 12D review had found a substantive gap — and, the review
finding none, was not needed and never started. Phase 13 — Portfolio Website /
Operator GUI — is now STARTED; see the Phase 13A note above and the Phase 13
roadmap section below.

Phase 12D is the fourth subphase of Phase 12. It is a documentation-only
closure-definition round: it defines what it means to close Phase 12, records
the final Phase 12A–12C portfolio asset inventory, and prepares the Phase 12
closure decision. It adds three `docs/` documents — `phase12-closure-plan.md`,
`final-portfolio-handoff.md`, and `phase12-final-review-checklist.md` — lightly
updates `README.md`, advances the state-discipline guard
`tests/test_failure_mode_regression.py` under the narrow, explicitly authorized
mechanical exception, and synchronizes the State Preservation Bundle. It
changed no `src/`, `pyproject.toml`, `uv.lock`, dependency, product, runtime,
API, CLI, or telemetry behaviour, and added no Phase 13 GUI implementation.

*(The "StoryTime Roadmap" body below — and the Phase 13 roadmap section — are
the durable forward-looking roadmap; `docs/handoff-state.md` is authoritative
for current status. The Phase 12C-era and Phase 12B-era notes below — and the
Phase 12A.1, Phase 12A, and Phase 11x notes further below — are historical
records. Phase 12D is locked and Phase 12 is closed; Phase 13A is the current
implementation candidate.)*

---

# Phase 12C implementation-candidate note — Portfolio Demo Narrative / Public Presentation Kit (historical record — Phase 12C is LOCKED; see the Phase 12D note above)

**Date:** 2026-05-26
**Round type:** Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — documentation-first portfolio packaging (documentation only).
**Status:** Historical record. This note described Phase 12C while it was an implementation candidate. Phase 12C has since been **LOCKED** and is the last locked phase; Phase 12D is now the current implementation candidate — see the Phase 12D note above.

Phase 12B — Portfolio Evidence Pack / Reviewer Assets — is now **LOCKED** and is
the last locked phase; the accepted Phase 12B.1 / 12B.2 / 12B.3 cleanup
sub-rounds are folded into its lock lineage and are not independently locked
phases. **Phase 12 — Portfolio / SE Demo Packaging — is STARTED** and is not
closed. Phase 12D and every later Phase 12 subphase have **not** started.
Phase 13 — Operator GUI / Decoupled Frontend Vision — is roadmap-preserved only
(see the Phase 13 roadmap note below and `docs/GUI_vision.md`) and has **not**
started.

Phase 12C is the third subphase of Phase 12. It is a documentation-first
portfolio-packaging round: it converts the project's existing technical
evidence into polished, reusable public-presentation assets. It adds four
`docs/` documents — `portfolio-demo-narrative.md` (a concise demo narrative),
`demo-talk-track.md` (a 5/10/20-minute spoken walkthrough),
`interview-story-bank.md` (reusable interview answer frames), and
`public-repository-readiness.md` (a public-viewing readiness checklist) —
lightly updates `README.md` to point reviewers to them, advances the
state-discipline guard `tests/test_failure_mode_regression.py` under the
narrow, explicitly authorized mechanical exception, and synchronizes the State
Preservation Bundle. It changes no `src/`, `pyproject.toml`, `uv.lock`,
dependency, product, runtime, API, CLI, or telemetry behaviour, and adds no
Phase 13 GUI implementation. Per the Phase Closure Protocol, Phase 12C is an
implementation candidate, pending review, **not locked**; it does not lock
Phase 12C, does not close Phase 12, and does not start Phase 12D.

*(The "StoryTime Roadmap" body below — and the Phase 13 roadmap note — are the
durable forward-looking roadmap; `docs/handoff-state.md` is authoritative for
current status. The Phase 12B-era notes below — the Phase 12B.3, 12B.2, 12B.1,
and Phase 12B notes — and the Phase 12A.1, Phase 12A, and Phase 11x notes
further below, are historical records. Phase 12B is LOCKED; Phase 12C is the
current implementation candidate.)*

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
**Round type:** Phase 12B — Portfolio Evidence Pack / Reviewer Assets — reviewer/evidence documentation packaging (documentation only).
**Status:** Phase 12B — Portfolio Evidence Pack / Reviewer Assets is an **implementation candidate / pending review — NOT locked.**

Phase 12A — Portfolio / SE Demo Packaging Baseline — is now **LOCKED** and is
the last locked phase; the accepted Phase 12A.1 state-hygiene cleanup sub-round
is folded into the Phase 12A lock lineage and is not an independently locked
phase. **Phase 12 — Portfolio / SE Demo Packaging — is STARTED and is not
closed.** Phase 12C and every later Phase 12 subphase have **not** started.

Phase 12B is the second subphase of Phase 12. It adds four reviewer/evidence
`docs/` documents — `portfolio-evidence-index.md`, `se-interview-evidence-matrix.md`,
`demo-reviewer-checklist.md`, and `portfolio-public-copy.md` — lightly updates
`README.md`, and synchronizes the State Preservation Bundle. It changed no
`src/`, `pyproject.toml`, `uv.lock`, dependency, or runtime/product behaviour;
its only `tests/` change is the narrow, explicitly authorized §5 mechanical
advance of the state-discipline guard `tests/test_failure_mode_regression.py`
to the Phase 12B current-state expectations. Per the Phase Closure Protocol,
Phase 12B is an implementation candidate, pending review, **not locked**.

*(The Phase 12A.1 and Phase 12A notes below are historical records — Phase 12A
is locked. The "StoryTime Roadmap" body further down has been updated to the
Phase 12B state.)*

---

# Phase 12A.1 state-hygiene cleanup note — Portfolio / SE Demo Packaging Baseline (folded into the Phase 12A lock — historical record)

**Date:** 2026-05-26
**Round type:** bounded state-hygiene cleanup of the Phase 12A round (documentation only).
**Status:** Historical record. Phase 12A has since been **LOCKED**; the Phase 12A.1 cleanup is folded into the Phase 12A lock lineage as an accepted sub-round. Current status is in the Phase 12B note above.

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

**Phase 12A — Portfolio / SE Demo Packaging Baseline — is LOCKED / ACCEPTED /
CANONICAL** (locked after the accepted Phase 12A.1 state-hygiene cleanup
sub-round, which is folded into the Phase 12A lock lineage). *(This note is a
historical record — current status is in the Phase 12B note above.)* Phase 12A
is the last locked phase. **Phase 11 — Release Candidate Hardening — is CLOSED.
Phase 12 — Portfolio / SE Demo Packaging — is STARTED.** Phase 10 is CLOSED.

Before Phase 12A, the Phase 11D — Release Candidate Evidence Pack artifact
completed its Phase Closure Protocol out-of-band in the GPT/Gemini review
workflow (GPT-5.5 review PASS; Gemini review SAFE TO LOCK; no required edits);
the user, as final decision-maker, then locked Phase 11D, formally closed
Phase 11, and authorized Phase 12. That out-of-band closure was a user/mediator
decision supplied to — and recorded, not re-reviewed, by — the Phase 12A round.

Phase 12A is the first subphase of Phase 12 — Portfolio / SE Demo Packaging. It
is a documentation and portfolio-packaging round: it makes StoryTime
explainable as a Solutions Engineer / observability / OpenTelemetry portfolio
project without adding any product feature or changing any runtime behaviour.
It added four `docs/` documents — `portfolio-overview.md`,
`solutions-engineer-narrative.md`, `portfolio-demo-script.md`, and
`interview-talking-points.md` — refined `README.md` for a portfolio-facing
reviewer, and synchronized the State Preservation Bundle. It added no product
feature, no UI, no server, no JavaScript, no generated audio, no
screenshots/binary assets, no new dependency, and no schema change; it changed
no pipeline behaviour, `storytime rerun`, or Trust Envelope enforcement, and
changed no `pyproject.toml`, `uv.lock`, or `src/` content. The only `tests/`
change is a narrow, explicitly authorized advance of the state-discipline guard
`tests/test_failure_mode_regression.py` to the Phase 12A current-state
expectations. Per the Phase Closure Protocol, Phase 12A does **not** lock
Phase 12A, does **not** close Phase 12, and does **not** start Phase 12B; Phase
12B and later subphases have not started and are planned, future work.

*(The Phase 11D note below — now a historical record, since Phase 11D is locked
and Phase 11 is closed — and the Phase 11C, Phase 11B, Phase 11A, and Phase 10G
notes further below are historical records.)*

---

# Phase 11D note — Release Candidate Evidence Pack (locked — historical record)

**Phase 11D — Release Candidate Evidence Pack — is LOCKED; with it locked,
Phase 11 — Release Candidate Hardening — is CLOSED.** *(This note was written
when Phase 11D was an implementation candidate; it was subsequently locked
out-of-band under the Phase Closure Protocol and Phase 11 was formally closed.
Current status is in the Phase 12B note above.)* Phase 11C —
Failure-Mode / Regression Hardening — was the previous locked phase.
Phase 10 is CLOSED.

Phase 11D is the fourth and final planned Release Candidate Hardening subphase.
It is an evidence, closure-readiness, and proof-consolidation round: it
consolidates the release-candidate evidence produced by Phases 11A, 11B, and
11C into a reviewer-facing index, records the canonical validation results,
prepares a Phase 11 closure checklist, and writes a Phase 12 readiness handoff.
It added four `docs/` documents — `release-candidate-evidence-pack.md`,
`final-validation-summary.md`, `phase11-closure-checklist.md`, and
`phase12-readiness-handoff.md` — refreshed the status notes in
`docs/phase11-plan.md`, `docs/release-candidate-hardening.md`, and
`docs/rc-validation-checklist.md`, and synchronized the State Preservation
Bundle. It added no product feature, no UI, no server, no JavaScript, no
generated audio, no screenshots/binary assets, no new dependency, and no schema
change; it changed no pipeline behaviour, `storytime rerun`, or Trust Envelope
enforcement, and changed no `pyproject.toml`, `uv.lock`, `src/`, or `tests/`
content. It is documentation/evidence consolidation only and added no test.
Phase 11D subsequently completed the Phase Closure Protocol out-of-band and was
locked by explicit user decision; with Phase 11D locked, Phase 11 — Release
Candidate Hardening — is CLOSED.

*(The Phase 11C note below — and the Phase 11B, Phase 11A, and Phase 10G notes
further below — are historical records. Phase 11D is locked and Phase 11 is
closed; Phase 12A — Portfolio / SE Demo Packaging Baseline — is the current
implementation candidate, recorded in the Phase 12A note at the top of this
file.)*

---

# Phase 11C note — Failure-Mode / Regression Hardening (locked — historical record)

**Phase 11C — Failure-Mode / Regression Hardening — was locked. It was the last locked phase at that point in the project history.** Phase 11B — Fresh Clone / Operator Reproducibility — was the
previous locked phase. Phase 10 is CLOSED.

Phase 11C is the third Release Candidate Hardening subphase. It is a
failure-mode and regression-hardening round: it inventories the highest-risk
failure and regression paths that already exist in StoryTime, records which
tests and gates protect each one, and documents operator failure-response. It
added four `docs/` documents — `failure-mode-regression-hardening.md`,
`regression-risk-register.md`, `failure-mode-test-matrix.md`,
`operator-failure-response.md` — and one focused regression test module,
`tests/test_failure_mode_regression.py` (the state-documentation discipline
guard), and synchronized the State Preservation Bundle. It added no product
feature, no UI, no server, no JavaScript, no generated audio, no
screenshots/binary assets, no new dependency, and no schema change; it changed
no pipeline behaviour, `storytime rerun`, or Trust Envelope enforcement, and
changed no `pyproject.toml`, `uv.lock`, or `src/` content. The only `tests/`
change is the new regression module. Phase 11C did **not** mark Phase 11
complete and did **not** start Phase 11D or Phase 12.

*(This Phase 11C note is a superseded point-in-time record. Current state is recorded in the active Phase 12B / Phase 12B.2 notes at the top of this file; the Phase 12A, Phase 11B, Phase 11A, and Phase 10G notes below are historical records.)*

---

# Phase 11B note — Fresh Clone / Operator Reproducibility (locked — historical record)

**Phase 11B — Fresh Clone / Operator Reproducibility — was LOCKED and was the last locked phase at that point in the project history.** *(This is a superseded point-in-time record, originally written when Phase 11B was an implementation candidate; Phase 11B was subsequently locked under the Phase Closure Protocol and is the source/base artifact for Phase 11C. Current status is in the Phase 12B note above.)* Locked artifact
`storytime-phase11b-fresh-clone-operator-reproducibility.tar.gz` (SHA-256
`08b72f2833da9adf3b8acc1f3170334eb7c5f998e19263838efbce2f571cc73f`).

Phase 11B is the second Release Candidate Hardening subphase. It is a
fresh-clone / operator reproducibility verification round: it extracted the
locked Phase 11A artifact into a clean tree, walked the documented setup,
validation, and demo paths exactly as written, and confirmed they reproduce
the Phase 11A baseline. It added two reproducibility documents
(`docs/operator-reproducibility-checklist.md`,
`docs/fresh-clone-troubleshooting.md`), refined the Phase 11A reproducibility
documents, aligned the `README.md` setup command with the canonical
`uv sync --frozen --extra dev` form, and synchronized the State Preservation
Bundle. It added no product feature, no UI, no server, no JavaScript, no
generated audio, no screenshots/binary assets, no new dependency, and no
schema change; it changed no pipeline behaviour, `storytime rerun`, or Trust
Envelope enforcement, and changed no `pyproject.toml`, `uv.lock`, `src/`, or
`tests/` content.

*(The Phase 11A note below is a historical record — Phase 11A is locked. The
Phase 10G lock closure note further below is a historical record; Phase 10 is
CLOSED.)*

---

# Phase 11A note — Release Candidate Hardening Baseline (locked — historical record)

**Date:** 2026-05-25
**Locked artifact:** `storytime-phase11a-release-candidate-hardening-baseline.tar.gz` (SHA-256 `664f8ba4ae90cf6a98ccc7d20369e690eac74497ab78f2b7067f0aac2079a7aa`).
**Status:** Phase 11A — Release Candidate Hardening Baseline is **LOCKED / ACCEPTED / CANONICAL**. *(This is a superseded point-in-time record, originally written when Phase 11A was an implementation candidate; Phase 11A was subsequently locked under the Phase Closure Protocol. Phase 11B, Phase 11C, and Phase 11D have since also been locked and Phase 11 — Release Candidate Hardening — is CLOSED; current status is in the Phase 12B note above.)*
**Last locked work item before Phase 11A:** Post-Phase-10 Historical State Reconciliation.

Phase 11A is the first Release Candidate Hardening subphase — a
documentation-first round that audited and documented the repository's
non-feature surfaces (fresh-clone readiness, the validation-command baseline,
artifact hygiene, the security/secrets posture, demo reproducibility, known
limitations) and decomposed Phase 11. It added seven `docs/` hardening
documents (`release-candidate-hardening.md`, `phase11-plan.md`,
`local-setup-runbook.md`, `fresh-clone-checklist.md`,
`rc-validation-checklist.md`, `security-secrets-checklist.md`,
`demo-reproducibility-checklist.md`) and synchronized the State Preservation
Bundle. It added no product feature, UI, server, JavaScript, generated audio,
screenshots/binary assets, new dependency, or schema change, and changed no
`pyproject.toml`, `uv.lock`, `src/`, or `tests/` content.

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
**Next phase:** Phase 11 — Release Candidate Hardening *(Phase 11 has since been completed and is CLOSED — Phase 11A through 11D all locked; Phase 12 — Portfolio / SE Demo Packaging — is now STARTED. See the Phase 12A note at the top of this file for current status)*.
**Next action:** Begin Phase 11 — Release Candidate Hardening — under the Phase Closure Protocol when scheduled.

Phase 10G — the documentation, portfolio-narrative, demo-explanation, and Phase 10 closure phase — is locked. It added `docs/portfolio-narrative.md`, `docs/demo-script.md`, `docs/operator-experience-walkthrough.md`, `docs/command-reference.md`, `docs/known-limitations.md`, `docs/observability-governance-talking-points.md`, `docs/phase10-acceptance-checklist.md`, and `docs/screenshot-instructions.md`, and synchronized the State Preservation Bundle. It added no product feature, no UI, no server, no JavaScript, no generated audio, no screenshots/binary assets, and no new dependency; it changed no pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, or the database schema. Phase 10G completed the Phase Closure Protocol (GPT-5.5 review PASS; Gemini review SAFE WITH EDITS; the Phase 10G.1 `uv.lock` cleanup — the suspected drift was a false positive; GPT-5.5 Phase 10G.1 verification PASS; Gemini Phase 10G.1 final verification SAFE TO LOCK; explicit user lock approval). With Phase 10G locked, **Phase 10 — Product UI / Operator Experience — is formally CLOSED** (Phases 10A–10G all locked). The next phase is **Phase 11 — Release Candidate Hardening**, which has **not started**. This note was synchronized by the Post-Phase-10 Closure State Synchronization task.

*(The Phase 10F lock closure note and the Phase 10E / Phase 10C lock closure notes below are historical records. Phase 10A, 10B, 10C, 10C.1, 10D, 10D.1, 10E — with the 10E.1 / 10E.2 cleanup sequence — 10F, and 10G are all locked; Phase 10 is closed.)*

---

# Phase 10F lock closure note

**Date:** 2026-05-25
**Lock archive:** `storytime-phase10f-demo-seed-data-golden-path-fixtures.tar.gz`
**SHA-256:** `e060570a94fb19f790c539542b3ef7445111430bc308668675548f66fa48df55`
**Status:** Phase 10F — Demo Seed Data / Golden Path Fixtures is **LOCKED / ACCEPTED / CANONICAL**.
**Last locked phase:** Phase 10F.
**Next phase:** Phase 10G — Portfolio Narrative / Phase 10 Closure.

Phase 10F added curated demo seed data and golden-path fixture scenarios — the `demo/` directory (four original CC0 seed texts plus schema-valid manifests, a demo-only blocked-source deny-list, and six fixture definitions), the `docs/demo.md` operator runbook, and `tests/test_demo_fixtures.py`. It was fixture / demo-readiness work that exercises the existing system only: no new product feature, no UI, no server, no generated audio committed, no JavaScript, no new dependency, and no change to pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, or the database schema. Phase 10F completed the Phase Closure Protocol and was locked with explicit user approval.

*(The Phase 10E lock closure note and the Phase 10C lock closure note below are historical records, superseded by this Phase 10F closure.)*

---

# Phase 10E lock closure note

**Date:** 2026-05-25
**Lock archive:** `storytime-phase10e2-final-cleanup-v2-normalized.tar.gz`
**Status:** Phase 10E — Static HTML Operator Report Refinement is **LOCKED / ACCEPTED / CANONICAL**, with the Phase 10E.1 / 10E.2 cleanup sequence accepted and the 10E.2 normalized cleanup as canonical state.
**Last locked phase:** Phase 10E / 10E.2 normalized cleanup.
**Next phase:** Phase 10F — Demo Seed Data / Golden Path Fixtures.

Phase 10E refined the existing generated static HTML operator report for clarity, usability, and demo readiness, keeping the report a local, static, read-only artifact (no JavaScript, no external assets, no browser-side mutation controls, no backend behavior change). The Phase 10E.1 / 10E.2 cleanup sequence addressed raw `blocked_reason` redaction, archive hygiene, and state-preservation synchronization. Phase 10E was reviewed and locked with explicit user approval.

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

# StoryTime Roadmap

The durable, forward-looking phase roadmap and model-routing map. Companion
documents: `docs/canonical-state.md` is the append-only locked-decision log,
`docs/phase-history.md` is the round-by-round record, and
`docs/handoff-state.md` is the authoritative current-status snapshot. If this
file disagrees with `docs/handoff-state.md` on current status, handoff-state
is authoritative. Read `LLM_DIRECTOR.md` first.

## Status: Phase 13 STARTED — Phase 13A–13F locked — Phase 13D.1 / 13D.2 locked — Phase 13G / 13G.1 locked — Phase 13H / 13H.1 / 13H.2 / 13H.3 locked — Phase 13I locked — Phase 13J locked — Phase 13K locked — Phase 13L closure candidate (pending review, NOT locked) — Phase 13 closure prepared but not yet externally locked — Phase 14 NOT STARTED (Phase 14A is the next proposed architecture baseline) — Phase 12 CLOSED — Phase 11 CLOSED — Phase 10 CLOSED

All of Phase 7, Phase 8, Phase 9A, Phase 9B, Phase 10A through 10G, and
Phase 11A through 11D are locked. Architecture Baseline Section 24 (governance)
and Section 25 (operator experience) remain canonical.

**Phase 10 — Product UI / Operator Experience — is formally CLOSED**: all of
its sub-phases (10A through 10G) are locked; the locked Phase 10G artifact is
`storytime-phase10g1-uvlock-reversion-cleanup.tar.gz` (SHA-256
`8a0cc9a5b6426a291bec3a793e41501c7d3492187dd48b4f7729ea95e501a0c1`).

The **Post-Phase-10 Historical State Reconciliation** — a documentation/
state-history checkpoint between Phase 10 closure and Phase 11 start, **not a
new phase** — was the last locked work item before Phase 11; its locked
artifact is
`storytime-post-phase10-roundtable-historical-backfill.tar.gz` (SHA-256
`367e647c46aa6e4fd039369da30859b11ca783249569df291343db133ef4cfdd`).

**Phase 11 — Release Candidate Hardening — is CLOSED.** Its four subphases —
11A, 11B, 11C, and 11D — are all locked; the user locked Phase 11D and formally
closed Phase 11.

**Phase 12 — Portfolio / SE Demo Packaging — is CLOSED.** Its four subphases
are all locked: Phase 12A — Portfolio / SE Demo Packaging Baseline (the
accepted Phase 12A.1 state-hygiene cleanup folded into its lock lineage),
Phase 12B — Portfolio Evidence Pack / Reviewer Assets (the accepted Phase
12B.1 / 12B.2 / 12B.3 cleanup sub-rounds folded into its lock lineage),
Phase 12C — Portfolio Demo Narrative / Public Presentation Kit, and Phase 12D —
Phase 12 Closure Plan / Final Portfolio Handoff Definition. Phase 12D is the
last locked phase. Phase 12D completed its Phase Closure Protocol out-of-band —
the Gemini review returned the verdict to lock Phase 12D and close Phase 12,
with no required edits — and the user then locked Phase 12D and formally closed
Phase 12. Phase 12E was optional, contingency-only work; the Phase 12D review
found no substantive gap, so Phase 12E was not needed and never started.

**Phase 13 — Portfolio Website / Operator GUI — is STARTED. Phase 13A —
Portfolio Website / Operator GUI Architecture Baseline — is locked and is the
last locked phase. Phase 13B — Typed Static Portfolio Shell / Minimal Visual
Pipeline Scaffold — is the current subphase:** an implementation candidate,
pending review, not locked. Phase 13A was a documentation-only
architecture-baseline round; Phase 13B is the first frontend implementation
round and adds a bounded React + TypeScript + Vite frontend — a static,
read-only, demo-data-backed portfolio shell plus one Pipeline Run Detail view
with a visual Stage Timeline. Phase 13C through Phase 13G are future, planned
work and have not started; Phase 13 is not closed. Phase 9C remains optional
and not scheduled.


## Completed phases (locked)

| Phase | Scope | Status |
|-------|-------|--------|
| 0 | Product Charter | locked |
| 1 | Architecture Baseline | locked |
| — | Phase Closure Protocol | locked |
| 2 | Repository scaffold + dev environment | locked |
| 3 | Thin vertical slice (ingest → synthesize → assemble → publish) | locked |
| 4 / 4.1 | Persisted approval gates + resume/rehydration | locked |
| 5 | OpenTelemetry instrumentation foundation | locked |
| 6S | Range-capable feed serving + multi-item RSS | locked |
| 6A | Observability stack, dashboards-as-code, demo harness | locked |
| 6B | SLO/SLI narrative, runbook, demo walkthrough | locked |
| 7A | Blue/Green Option A — per-slot processes | locked |
| 7B | Higher-Assurance Front Door / Active-Slot Switching | locked |
| 7C / 7C.1 | Architecture Baseline §16 amendment — App Containerization | locked |
| 7D | Optional Local App Containerization | locked |
| 7D.1 | Operational Cleanup — Compose Build Race Fix | locked |
| 8A | Architecture Baseline Amendment — Collector-Owned Telemetry Fan-Out | locked |
| 8B | Local Multi-Backend Stack Expansion — Loki + local log routing | locked |
| 8B.1 | Operational cleanup — `./logs` directory preflight | locked |
| 8C / 8C.1 | Optional Vendor Export Profiles — disabled-by-default per-vendor export; 8C.1 split into two independent profiles | locked |
| 9A / 9A.1 | Governance Baseline Amendment — Architecture Baseline §24 (Trust Envelope, licensing, fail-closed gating); 9A.1 cleanup folded in source-authorization-not-viewpoint and early fail-closed clarifications | locked |
| 9B / 9B.1 | Minimal Trust Envelope Implementation — governance package, durable Trust Envelope artifact + SQLite projection, fail-closed gate, blocked-source config, static legal-hallucination gate; 9B.1 scanner hardening folded in | locked |
| 10A | Operator Experience Baseline Amendment — Architecture Baseline §25 (read-only-first operator law and Phase 10B static report handoff) | locked |
| 10B | Generated Local HTML Operator Report — static local read-only operator report and `storytime report generate` | locked |
| 10C / 10C.1 | Operator CLI Helpers / Failure Queue — the `storytime queue` read-only failure/review queue; 10C.1 state-preservation cleanup folded in | locked |
| 10D / 10D.1 | Pipeline Re-Run / Mutation Actions — the governed `storytime rerun` command; 10D.1 state-preservation cleanup + LLM director hardening folded in | locked |
| 10E | Static HTML Operator Report Refinement — refined static report; 10E.1 / 10E.2 cleanup sequence accepted | locked |
| 10F | Demo Seed Data / Golden Path Fixtures — `demo/` seed data + golden-path fixtures, `docs/demo.md`, fixture tests | locked |
| 10G | Portfolio Narrative / Phase 10 Closure — Phase 10 portfolio/closure documents + State Preservation Bundle sync | locked — **Phase 10 CLOSED** |
| — | Post-Phase-10 Historical State Reconciliation — RoundTable JSON historical backfill into the historical living docs (not a new phase) | locked |
| 11A | Release Candidate Hardening Baseline | locked |
| 11B | Fresh Clone / Operator Reproducibility | locked |
| 11C | Failure-Mode / Regression Hardening | locked |
| 11D | Release Candidate Evidence Pack | locked |
| 11 | Release Candidate Hardening (subphases 11A–11D) — overall phase | **CLOSED** |
| 12A | Portfolio / SE Demo Packaging Baseline — portfolio/SE-facing documents and README portfolio refinement | locked |
| 12B | Portfolio Evidence Pack / Reviewer Assets — reviewer/evidence documents and a light README reviewer-pointer refinement; 12B.1 / 12B.2 / 12B.3 cleanup sub-rounds folded in (12B.2 preserved the Phase 13 GUI roadmap vision) | locked |
| 12C | Portfolio Demo Narrative / Public Presentation Kit — public-presentation documents and a light README reviewer-pointer refinement | locked |
| 12D | Phase 12 Closure Plan / Final Portfolio Handoff Definition — closure-definition documents (`phase12-closure-plan.md`, `final-portfolio-handoff.md`, `phase12-final-review-checklist.md`) and a light README reviewer-pointer refinement | locked |
| 12 | Portfolio / SE Demo Packaging (subphases 12A–12D) — overall phase | **CLOSED** |
| 13A | Portfolio Website / Operator GUI Architecture Baseline — five architecture-baseline `docs/` documents (Phase 13 architecture, frontend/backend contract, Phase 13 roadmap, website content model, operator GUI view model); documentation only | locked |
| 13B | Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — the bounded React + TypeScript + Vite frontend: read-model contract, static demo dataset, portfolio homepage, one Pipeline Run Detail view with a Stage Timeline, placeholders, frontend README | locked |

### Phase 7 lock ledger

- **Phase 7A — Blue/Green Option A.** Per-slot processes; `deployment_slot`
  scopes state/feed roots; per-slot env files and `run-slot.sh`.
- **Phase 7B — Higher-Assurance Front Door / Active-Slot Switching.** Native
  Python loopback-only reverse proxy on a stable port; persisted active-slot
  pointer; pointer-based switch/rollback.
- **Phase 7C / 7C.1 — Architecture Baseline Amendment for App
  Containerization.** §16 amended (authored, Gemini-reviewed SAFE-WITH-EDITS,
  revised, locked) to permit optional, local, single-host, demo-grade app
  containerization.
- **Phase 7D — Optional Local App Containerization.** `Dockerfile`,
  `.dockerignore`, optional `docker-compose.app.yml`; per-slot named volumes;
  loopback-only `network_mode: host`; stable slot-derived `service.instance.id`.
  (Implemented as the Phase 7C.1 amendment's implementation; earlier referred
  to as "Phase 7C.1 / 7D".)
- **Phase 7D.1 — Operational Cleanup: Compose Build Race Fix.** One service
  owns the shared-image build; the consuming service uses `pull_policy: never`;
  `docker compose build` and a fresh-cache `up -d` both work. Live Docker
  smoke-tested on Windows Docker Desktop / WSL2 (see `docs/verification-log.md`).

## Current phase

**Phase 13 — Portfolio Website / Operator GUI — is STARTED.** Phase 10 —
Product UI / Operator Experience — is CLOSED; **Phase 11 — Release Candidate
Hardening — is CLOSED** (all four subphases 11A–11D locked); and **Phase 12 —
Portfolio / SE Demo Packaging — is CLOSED** (all four subphases 12A–12D
locked). The Post-Phase-10 Historical State Reconciliation was the last locked
work item before Phase 11.

**Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — is
the last locked phase.** Phase 12A, Phase 12B, and Phase 12C are also locked.
Phase 12D completed its Phase Closure Protocol out-of-band — the Gemini review
returned the verdict to lock Phase 12D and close Phase 12, with no required
edits — and the user then locked Phase 12D and formally closed Phase 12.
Phase 12E was optional, contingency-only work; the Phase 12D review found no
substantive gap, so Phase 12E was not needed and never started.

**Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — is
locked.** Phase 13A completed its Phase Closure Protocol (GPT-5.5 review, then
Gemini SAFE TO LOCK with no required edits, then an explicit user lock
decision). It was a documentation-only architecture-baseline round; its five
architecture documents are the authoritative Phase 13 plan.

**Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold —
is locked and is the last locked phase.** Phase 13B completed its Phase Closure
Protocol (GPT-5.5 review, then Gemini SAFE TO LOCK with no required edits, then
an explicit user lock decision). It was the first frontend implementation
round: against the locked Phase 13A contract it added the bounded React +
TypeScript + Vite frontend — a static, read-only, demo-data-backed portfolio
shell plus one Pipeline Run Detail view with a visual Stage Timeline, and
honest placeholders for the future views.

**Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment —
is the current subphase:** an implementation candidate, pending review, **not
locked**. Per the Phase Closure Protocol it is not lock-ready until GPT-5.5
review, Gemini critique, any cleanup, and explicit user approval complete.
Phase 13C establishes a deterministic, read-only static data boundary between
backend truth and the Phase 13B frontend: it adds a small read-only backend
export module and a `storytime export-demo-ui` CLI command producing a
deterministic static JSON export with a top-level `schemaVersion`, the export
contract document, a frontend deferred-work register, a frontend adapter and a
`StaticDemoExport` type, backend contract tests, and it rewires the homepage
and Pipeline Run Detail / Stage Timeline onto the adapter. Phase 13C does not
lock Phase 13C, does not close Phase 13, and does not begin Phase 13D.
**Phase 13D through Phase 13G have not started**; they are future, planned
work, decomposed in the Phase 13 roadmap section below and in
`docs/phase13-roadmap.md`.

## Phase 12 — Portfolio / SE Demo Packaging (CLOSED)

Phase 12 packaged and explained the already-hardened release candidate as a
portfolio and Solutions-Engineering demo. It was **packaging and explanation**,
not product development: it built on what Phases 0–11 produced and verified,
and it did not change product behaviour to tell the story.
`docs/phase12-readiness-handoff.md` records the boundary — what Phase 12 could
safely do, and what it must not (no new product features, servers, dashboards,
cloud deployment, new dependencies, or unamended Architecture Baseline change).
**Phase 12 is CLOSED** — all four subphases are locked, and the user formally
closed Phase 12 after Phase 12D was locked out-of-band.

| Subphase | Scope | Status |
|----------|-------|--------|
| 12A | Portfolio / SE Demo Packaging Baseline — portfolio-facing documents (`portfolio-overview.md`, `solutions-engineer-narrative.md`, `portfolio-demo-script.md`, `interview-talking-points.md`) and a README portfolio refinement | locked |
| 12B | Portfolio Evidence Pack / Reviewer Assets — reviewer/evidence documents (`portfolio-evidence-index.md`, `se-interview-evidence-matrix.md`, `demo-reviewer-checklist.md`, `portfolio-public-copy.md`) and a light README reviewer-pointer refinement; 12B.1 / 12B.2 / 12B.3 cleanup sub-rounds folded in | locked |
| 12C | Portfolio Demo Narrative / Public Presentation Kit — public-presentation documents (`portfolio-demo-narrative.md`, `demo-talk-track.md`, `interview-story-bank.md`, `public-repository-readiness.md`) and a light README reviewer-pointer refinement | locked |
| 12D | Phase 12 Closure Plan / Final Portfolio Handoff Definition — closure-definition documents (`phase12-closure-plan.md`, `final-portfolio-handoff.md`, `phase12-final-review-checklist.md`) and a light README reviewer-pointer refinement | locked |
| 12E | Optional final bounded cleanup — it would have existed only if the Phase 12D review had found a substantive packaging gap a bounded cleanup could not fix | not needed; never started — the Phase 12D review found no such gap |

Phase 12A — locked — was documentation and portfolio-packaging only: it
added the four portfolio `docs/` documents above and refined `README.md` with a
portfolio-facing "For reviewers" section.

Phase 12B — locked — was reviewer/evidence documentation packaging only. It
added the four reviewer/evidence `docs/` documents above, lightly updated
`README.md`, advanced the state-discipline guard, and synchronized the State
Preservation Bundle. Its accepted Phase 12B.1 / 12B.2 / 12B.3 cleanup
sub-rounds are folded into its lock lineage; Phase 12B.2 preserved the GUI
vision in the roadmap and `docs/GUI_vision.md`.

Phase 12C — locked — was documentation-first public-presentation packaging
only. It added the four public-presentation `docs/` documents above (a concise
demo narrative, a 5/10/20-minute spoken talk track, a reusable interview story
bank, and a public-repository readiness checklist), lightly updated
`README.md`, advanced the state-discipline guard, and synchronized the State
Preservation Bundle.

Phase 12D — locked — was a documentation-only closure-definition round. It
added three `docs/` documents — `phase12-closure-plan.md` (the Phase 12 closure
criteria, the Phase 12A–12C asset inventory, the closure-readiness checklist,
the remaining-gaps / no-go criteria, the close-after-12D vs bounded-cleanup vs
separate-12E recommendation, and the Phase 13 boundary statement),
`final-portfolio-handoff.md` (a cold-reader handoff), and
`phase12-final-review-checklist.md` (the reviewer checklist for the Phase 12D /
Phase 12 closure gate) — lightly updated `README.md`, advanced the
state-discipline guard `tests/test_failure_mode_regression.py`, and
synchronized the State Preservation Bundle. It added no product feature, no UI,
no server, no JavaScript, no frontend directory, no generated audio, no demo
video, no new dependency, and no schema change, and changed no `pyproject.toml`,
`uv.lock`, or `src/` content. Phase 12D completed its Phase Closure Protocol
out-of-band — the Gemini review returned the verdict to lock Phase 12D and
close Phase 12, with no required edits — and the user then locked Phase 12D and
formally closed Phase 12.

## Phase 13 — Portfolio Website / Operator GUI (STARTED)

**Phase 13 — Portfolio Website / Operator GUI — is STARTED.** It is the
project track that follows the closed Phase 12. Phase 13 will design, and in
its later subphases build, two related frontends: a portfolio-facing website
that presents StoryTime to reviewers, and a decoupled operator GUI that lets a
local operator see and (in later subphases only) act on pipeline state through
a real interaction layer rather than only the CLI and documents. The
authoritative Phase 13 plan is the set of five Phase 13A architecture
documents listed below; `docs/GUI_vision.md` is the original, verbatim vision
capture and is preserved unchanged.

**Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — is
locked.** Phase 13A was a documentation-only architecture-baseline round. It
designed the portfolio website and the decoupled operator GUI on paper and
refined the earlier `docs/GUI_vision.md` sketch into an authoritative Phase 13
plan, without building any of it. Phase 13A added five `docs/` documents and
synchronized the State Preservation Bundle:

- `phase13-portfolio-website-architecture.md` — the Phase 13 purpose, the
  end-state website and operator-GUI vision, the audiences and review paths,
  the website and operator information architectures, the local-first and
  future-cloud compatibility rules, and the Phase 13 success criteria.
- `frontend-backend-contract.md` — the "backend owns truth, frontend owns
  understanding" data contract: read-model categories, future action
  categories, the actions deliberately disabled for this round, and candidate
  data-source options.
- `phase13-roadmap.md` — the Phase 13A–13G subphase decomposition, with each
  subphase's objective, allowed and forbidden scope, acceptance criteria, and
  review gate.
- `portfolio-website-content-model.md` — the website section inventory mapped
  to existing repository source documents, with a content-honesty checklist.
- `operator-gui-view-model.md` — the operator-GUI view inventory, the disabled
  and future actions, the empty / error / loading states, and the
  accessibility and readability requirements.

**Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold —
is locked.** Phase 13B was the first frontend implementation round. Against the
locked Phase 13A contract it added a new top-level `frontend/` directory — a
React + TypeScript (strict) + Vite project, standard CSS, no external UI /
component / state / charting library — containing the frontend read-model
contract, a static demo dataset of exactly two mock pipeline runs (one
golden-path, one governance review-required), the portfolio homepage, one
Pipeline Run Detail view with a visual Stage Timeline, honest placeholders for
the future portfolio sections and operator views, and a frontend README. It
changed no `src/`, `pyproject.toml`, or `uv.lock`.

**Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment —
is the current subphase: an implementation candidate, pending review, not
locked.** Phase 13C establishes a truthful, reproducible, read-only data
boundary between backend truth and the Phase 13B frontend. It adds a small
read-only backend export module (`src/storytime/operator_export.py`) and a
`storytime export-demo-ui` CLI command that produce a deterministic static JSON
export (`frontend/src/data/storytime-demo-export.json`, carrying a top-level
`schemaVersion`); the export contract document
`docs/frontend-static-export-contract.md`; the frontend deferred-work register
`docs/frontend-gui-deferred-work-register.md`; a frontend adapter
(`frontend/src/data/adapter.ts`) and a `StaticDemoExport` type; backend
contract tests (`tests/test_operator_export.py`); and it rewires the homepage
and Pipeline Run Detail / Stage Timeline to consume the export through the
adapter. The export is deterministic — built from fixed demo data, no
`datetime.now()`, no `uuid`, no randomness; generating it twice yields
byte-identical JSON. Phase 13C is static and read-only: no server, no live API,
no `fetch`/`axios`, no mutation, no cloud deployment, no production hosting.
Unlike Phase 13B it adds small backend code, but that code is read-only and
deterministic and changes no core pipeline runtime behaviour and no root
dependency or `uv.lock`. Its `tests/` changes are the new
`tests/test_operator_export.py` and the narrow, explicitly authorized
mechanical advance of the state-discipline guard
`tests/test_failure_mode_regression.py`.

The Phase 13A–13G decomposition, recorded in full in `docs/phase13-roadmap.md`
and subject to per-subphase review and explicit authorization:

| Subphase | Scope | Status |
|----------|-------|--------|
| 13A | Portfolio Website / Operator GUI Architecture Baseline — design the website and the decoupled operator GUI on paper: purpose, end-state vision, information architecture, frontend/backend data contract, content model, view model, and the 13A–13G decomposition (documentation only) | locked |
| 13B | Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — the first frontend round: the frontend read-model contract and static demo data, a React + TypeScript + Vite scaffold, the portfolio homepage, one Pipeline Run Detail view with a visual Stage Timeline, and honest placeholders for the remaining views | locked |
| 13C | Deterministic Read-Only Static Export / Frontend Data Alignment — a backend-defined deterministic read-only static export (module + `storytime export-demo-ui` CLI command + committed JSON with a `schemaVersion`), a frontend adapter and `StaticDemoExport` type aligned to it, and the homepage and Pipeline Run Detail view rewired onto the adapter; static and read-only, no live backend | implementation candidate / pending review (not locked) |
| 13D | Operator Workflow Views — the remaining read-only operator GUI views (dashboard, runs list, failure queue, governance/review, observability) built against the read-only adapter | not started |
| 13E | Controlled Local Actions / Safe Mutation Boundary — the first, explicitly gated operator actions, each mapping to an existing governed backend operation; the single subphase that introduces mutation | not started |
| 13F | Portfolio Website Polish / Public Demo Packaging — final content pass, tiered reviewer paths, demo walkthrough, and a clean public-hostable static build | not started |
| 13G | Deployment / Hosting Readiness — optional; only if public hosting is wanted: prepare the static portfolio build for hosting, with the local-first operator GUI unaffected | not started (optional / contingency) |

Phase 13 guardrails (from `docs/phase13-portfolio-website-architecture.md` and
`docs/frontend-backend-contract.md`):

- The design comes before the build. Phase 13A produces the contract, content
  model, and view model; the build subphases consume them.
- The frontend is decoupled from the backend deployment mode and does not know
  whether it is backed by local files, a local API, containers, or a future
  cloud API.
- The operator GUI is read-only until a later subphase explicitly authorizes
  bounded, governed operator actions.
- No backend rewrite: contracts and adapters come before any product-behaviour
  change.
- Local-first demoability and future cloud compatibility are both preserved;
  no subphase requires cloud deployment.

Companion preserved vision file: `docs/GUI_vision.md` (original verbatim
capture, left unchanged).

## Phase 11 — Release Candidate Hardening (CLOSED)

Phase 11 turned the post-Phase-10 codebase into a release candidate: not new
product behaviour, but a repository a fresh clone, a cold LLM session, and an
operator/demo run can all proceed from safely and reproducibly. It was split
into staged subphases, each closed under the Phase Closure Protocol before the
next began. The full plan is `docs/phase11-plan.md`. **Phase 11 is CLOSED** —
all four subphases are locked, and the user formally closed Phase 11 after
Phase 11D was locked out-of-band.

| Subphase | Scope | Status |
|----------|-------|--------|
| 11A | Release Candidate Hardening Baseline — audit and document the repository's non-feature surfaces (fresh-clone readiness, validation commands, artifact hygiene, security/secrets posture, demo reproducibility, known limitations) and decompose Phase 11 | locked |
| 11B | Fresh Clone / Operator Reproducibility — verify the documented setup and demo paths run cleanly from a genuine fresh clone; close any gap found in 11A | locked |
| 11C | Failure-Mode / Regression Hardening — exercise and document failure modes and regression surfaces; confirm the fail-closed and read-only invariants hold | locked |
| 11D | Release Candidate Evidence Pack — assemble the verification evidence, hygiene proof, and reviewer-facing summary for a release-candidate sign-off | locked |

Phase 11A — locked — is documentation-first and added no product behaviour. It
produced seven `docs/` hardening documents — `release-candidate-hardening.md`
(the hardening baseline overview), `phase11-plan.md` (the decomposition in
full), `local-setup-runbook.md`, `fresh-clone-checklist.md`,
`rc-validation-checklist.md`, `security-secrets-checklist.md`, and
`demo-reproducibility-checklist.md`.

Phase 11B — locked — is a fresh-clone / operator reproducibility verification
round. It walked the Phase 11A setup, validation, and demo paths from a clean
extraction and confirmed they reproduce the documented baseline (the six
Docker-free gates pass; the documented operator commands run as written). It
added two reproducibility documents — `operator-reproducibility-checklist.md`
and `fresh-clone-troubleshooting.md` — refined the Phase 11A reproducibility
documents, aligned the `README.md` setup command with the canonical
`uv sync --frozen --extra dev` form, and synchronized the State Preservation
Bundle. It added no UI, server, JavaScript, generated audio, new dependency,
or schema change, and changed no `pyproject.toml`, `uv.lock`, `src/`, or
`tests/` content.

Phase 11C — locked — is a failure-mode and
regression-hardening round. It inventoried the highest-risk failure and
regression paths that already exist in StoryTime (the failure / review queue,
retry / re-run behaviour, governance-blocked content, static report safety,
demo fixture invariants, the legal-hallucination gate, operator-safe failure
messages, state preservation around failed runs), recorded which tests and
gates protect each one, and documented operator failure-response. It added
four `docs/` documents — `failure-mode-regression-hardening.md`,
`regression-risk-register.md`, `failure-mode-test-matrix.md`,
`operator-failure-response.md` — and one focused regression test module,
`tests/test_failure_mode_regression.py` (the state-documentation discipline
guard), and synchronized the State Preservation Bundle. It added no UI,
server, JavaScript, generated audio, new dependency, or schema change, and
changed no `pyproject.toml`, `uv.lock`, or `src/` content; the only `tests/`
change is the new regression module.

Phase 11D — Release Candidate Evidence Pack — is locked; it is the last locked
phase. It was an evidence, closure-readiness, and proof-consolidation round: it
consolidated the release-candidate evidence from Phases 11A, 11B, and 11C
into a reviewer-facing index, recorded the canonical validation results, and
prepared a Phase 11 closure checklist and a Phase 12 readiness handoff. It
added four `docs/` documents — `release-candidate-evidence-pack.md`,
`final-validation-summary.md`, `phase11-closure-checklist.md`,
`phase12-readiness-handoff.md`. It added no product behaviour, no dependency,
no source, and no test. Phase 11D completed its Phase Closure Protocol
out-of-band (GPT-5.5 PASS; Gemini SAFE TO LOCK) and was locked by explicit user
decision; with Phase 11D locked, Phase 11 — Release Candidate Hardening — is
CLOSED.

## Phase 8 — Multi-Backend Telemetry Fan-Out

Phase 8 is split into three phases, each closed under the Phase Closure
Protocol before the next begins:

| Sub-phase | Scope | Status |
|-----------|-------|--------|
| 8A | Architecture Baseline amendment — Collector-owned fan-out governance (`docs/architecture-baseline.md` §23) | **locked** |
| 8B | Local Multi-Backend Stack Expansion — add Loki + log routing; prove local topology; no vendor credentials, no egress | **locked** |
| 8B.1 | Operational cleanup — `./logs` directory preflight (Makefile targets + docs) | **locked** |
| 8C | Optional Vendor Export Profiles — disabled-by-default vendor export over standard OTLP / OTLP-HTTP; 8C.1 cleanup split it into two independent per-vendor profiles | **locked** (8C.1 accepted as part of the lock) — **completes Phase 8** |

The locked Phase 8A amendment (§23) governs all Phase 8 work:

- **Collector-owned fan-out.** Only the OpenTelemetry Collector performs
  multi-backend fan-out; application services emit telemetry solely to the
  local Collector endpoint.
- **No vendor SDKs in application code.** No vendor Python SDK, agent, or
  telemetry package in app code or runtime dependencies. Generic OpenTelemetry
  SDK usage stays as established by Phase 5.
- **Standard OTLP only.** `otlp` / `otlphttp` exporter families only;
  proprietary exporters, the Datadog exporter, and vendor/sidecar/host agents
  are forbidden absent a future amendment.
- **Local-first preserved.** The only outbound-network exception is explicitly
  enabled telemetry export from the Collector. The core app and the whole test
  suite still run offline; vendor credentials are never required by default.
- **Disabled by default.** `STORYTIME_TELEMETRY=noop` stays the default;
  vendor fan-out needs explicit environment configuration; no real secrets in
  committed files.
- **Local stack:** OpenTelemetry Collector, Prometheus, Loki, Jaeger, Grafana.
- **Vendor priority:** Dynatrace (primary), New Relic (secondary), Datadog
  (deferred unless clean standard OTLP support is possible).

Phase 8 is complete: all three sub-phases (8A, 8B / 8B.1, 8C / 8C.1) are locked
under the Phase Closure Protocol. There is no Phase 8D.

## Phase 9 — Security, Licensing, and Governance

Phase 9 is split into three phases, each closed under the Phase Closure
Protocol before the next begins. The accepted structure is a hybrid of the
"governance baseline first" and "minimal Trust Envelope" options:

| Sub-phase | Scope | Status |
|-----------|-------|--------|
| 9A / 9A.1 | Governance Baseline Amendment — `docs/architecture-baseline.md` §24: the governance model, Trust Envelope schema, fail-closed gating law; the 9A.1 cleanup folded in the source-authorization-not-viewpoint and early fail-closed clarifications | **locked** |
| 9B | Minimal Trust Envelope Implementation — implements the §24 Trust Envelope schema, the fail-closed governance gate, the local blocked-source config, and the static legal-hallucination grep/regex gate; the 9B.1 cleanup hardened that scanner against binary/generated files | **locked** (9B.1 folded into the lock, 2026-05-24) |
| 9C | Docs / Audit Polish — optional follow-up | not scheduled (superseded; Phase 10 is next) |

**Phase 9A — Governance Baseline Amendment** is **locked**
(`docs/architecture-baseline.md` Section 24 is canonical). It is
architecture/documentation only and authorized no implementation. Section 24
establishes the governance law: StoryTime is not a legal rights-clearance
engine and the human operator is the source of truth for licensing decisions;
governance is source authorization, not viewpoint acceptability (StoryTime
governance is not a content-moderation system); no legal automation or legal
hallucination; the allowed source categories (`CC0`, `US_PUBLIC_DOMAIN`,
`EXPLICIT_PERMISSION`, `LOCAL_TEST_FIXTURE`, with no `AMBIGUOUS` category); the
disallowed/blocked categories; a fail-closed gate that should check governance
as early as practical and must hard-block before TTS, audio processing, or RSS
publish unless an `APPROVED` Trust Envelope exists; the Trust Envelope concept
and its canonical minimum schema; the local blocked-source-config direction;
the reinforced secrets policy; an honest local-first deletion/retention
posture; the carried-forward telemetry/privacy hygiene; public/demo
disclaimers; the future legal-hallucination grep/regex gate; and the Phase 10
dependency contract. It completed the Phase Closure Protocol — authored by
Opus, reviewed by GPT-5.5, reviewed by Gemini (`SAFE WITH EDITS`, the two edits
folded in by the Phase 9A.1 cleanup), locked with explicit user approval
(2026-05-24).

**Phase 9B — Minimal Trust Envelope Implementation** is **locked (2026-05-24),
with the Phase 9B.1 cleanup folded into the lock.** It implemented the §24
governance law as the concrete artifact/projection: the `storytime.governance`
package (Trust Envelope model + canonical §24.8 closed schema), the durable
Trust Envelope artifact (`governance/trust-envelope.json`, the governance
source of truth) plus a rebuildable SQLite projection (schema migration `0005`,
the `trust_envelope` table), the fail-closed gate wired into `ingest` (early
check), `synthesize` (hard block before TTS), and `publish` (hard block before
RSS), the local `config/governance/blocked-sources.yaml` deny-list, and the
static legal-hallucination grep/regex gate. It changed no ARCH-LOCKed contract
and added no legal automation, AI copyright classifier, compliance scoring,
authentication, scraping, or hosted service. Phase 9B completed the Phase
Closure Protocol — implemented by Opus, reviewed by GPT-5.5, critiqued by
Gemini (`SAFE WITH MINOR CLEANUP`) — and the **Phase 9B.1 cleanup** applied
Gemini's single required item, hardening the static forbidden-term scanner
against binary/generated files and cache/virtualenv/`runs`/`feed` directories.
Phase 9B.1 is accepted as part of the Phase 9B lock. Five new Phase 9B test
files (53 tests) plus seven Phase 9B.1 hardening tests bring the suite to **418
passing**; all six Docker-free gates pass. **Phase 9C — Docs / Audit Polish**
was an optional follow-up; it is not scheduled — the next phase is Phase 10.

## Phase 10 — Product UI / Operator Experience

Phase 10 is the operator experience layer over the existing local-first
pipeline — the consumer of the locked Section 24 §24.15 dependency contract. It
is split into staged, conditional phases, each closed under the Phase Closure
Protocol before the next begins:

| Sub-phase | Scope | Status |
|-----------|-------|--------|
| 10A | Operator Experience Baseline Amendment — `docs/architecture-baseline.md` §25: the operator-experience law, the Phase 10B target / hard floor / hard ceiling, the report data model + field allowlist/blacklist, the Phase 10B handoff | locked |
| 10B | Generated Local HTML Operator Report — a generated, static, local, read-only HTML operator report built to the §25.23 handoff | locked (2026-05-24) |
| 10C | Operator CLI Helpers / Failure Queue — the `storytime.operator_queue` module and the read-only `storytime queue` failure/review-queue command | locked (2026-05-25) |
| 10C.1 | State Preservation Synchronization Cleanup — docs/state-preservation sync after the Phase 10C lock | locked (2026-05-25) |
| 10D | Pipeline Re-Run / Mutation Actions — the `storytime.operator_rerun` module and the governed `storytime rerun` mutation command | locked (2026-05-25) |
| 10E | Static HTML Operator Report Refinement — executive status summary, rerun eligibility guidance, failure summary, command reference, semantic badges, improved CSS | locked (2026-05-25); Phase 10E.1 / 10E.2 cleanup sequence accepted |
| 10F | Demo Seed Data / Golden Path Fixtures — curated `demo/` seed data and six golden-path fixture definitions, the `docs/demo.md` operator runbook, and `tests/test_demo_fixtures.py` | locked (2026-05-25) |
| 10G | Portfolio Narrative / Phase 10 Closure — the Phase 10 portfolio narrative, presentation demo script, operator-experience walkthrough, command reference, known-limitations doc, observability/governance talking points, Phase 10 acceptance checklist, and screenshot/evidence instructions; State Preservation Bundle synchronized | locked (2026-05-25) — **closes Phase 10** |

**Phase 10A — Operator Experience Baseline Amendment** is **locked** — `docs/architecture-baseline.md` Section 25, "Operator Experience
Baseline". It is architecture/documentation only and authorizes no
implementation. Section 25 establishes the operator-experience law: the
operator experience goal (a single local human operator; no SaaS/multi-user
personas); the read-only-first rule; the source-of-truth rule (SQLite +
artifact envelopes + the durable Trust Envelope stay authoritative; reports and
observability dashboards are projections/links, never truth); the governance
display rule (allowed bounded fields vs a forbidden legal/compliance
overclaiming vocabulary extending §24.3 / §24.14, plus a standing "record of a
human decision, not legal advice or certification of copyright safety"
disclaimer); the viewpoint-neutrality carryover (§24.5 preserved — no
content-moderation labels); the Phase 10B target (a generated, static, local,
read-only HTML operator report); the Phase 10B hard floor (a report directory
with a latest-runs summary, a run list, and a single-run detail page) and hard
ceiling (no mutation, forms, state-changing buttons, approval/retry/delete
workflow, server, live polling, websockets, frontend framework, build pipeline,
auth, cloud, dashboard recreation, embedded telemetry charts, or visual-polish
pass — skeleton HTML plus minimal static CSS only); the deterministic report
data model with explicit field sources; the report field allowlist/blacklist
(no raw story/narration text, transcripts, secrets, long free-text notes, raw
telemetry, or embedded dashboard data); the bounded `review_context_summary`
rule (a 500-character display cap, testable); the observability-link rule
(links only, no embedded data, no secrets in URLs); the determinism/snapshot,
privacy/no-raw-content, and governance-copy-linting test requirements; a
performance guardrail; three Phase 10B example run shapes; a full Phase 10B
handoff section; the no-auth/no-cloud/no-server and mutation-gate rules; the
stop/revert criterion; and this Phase 10A / 10B / 10C / 10D split. It must
complete the Phase Closure Protocol — GPT-5.5 review, Gemini critique, any
required revision, and explicit user approval — before Section 25 becomes
locked, canonical law.

**Phase 10B — Generated Local HTML Operator Report** has been **implemented as
a candidate (2026-05-24)**. It is implementation output under the locked
Section 25 law; per the Phase Closure Protocol it is not a locked phase until
GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval
complete. Phase 10B added the new `storytime.reporting` package (a
deterministic report data model, a collector over existing SQLite projections
and the durable Trust Envelope, a pure standard-library HTML renderer, and a
generator) and the `storytime report generate` CLI command. It generates a
static, local, read-only HTML operator report — `operator-report/index.html`,
`runs.html`, and a `run-<run_id>.html` detail page per run, plus a single local
`style.css` — from the existing SQLite state and artifact envelopes. It keeps
SQLite plus the on-disk artifact envelopes (and the durable Trust Envelope) as
the source of truth, presents governance status faithfully (the stable
`APPROVED` / `REJECTED` / `BLOCKED` / `NEEDS_REVIEW` enum) with no
legal/compliance overclaiming and the §25.5 disclaimer, bounds
`review_context_summary` to 500 characters, and introduces no auth, cloud,
server, mutation UI, frontend framework, build pipeline, or external asset. It
made no database schema change and added no dependency; 19 new tests and all
six Docker-free gates pass. The authoritative archive is
`storytime-phase10b-generated-local-operator-report.tar.gz`. See
`docs/operator-report.md` for the operator guide.

**Phase 10C — Operator CLI Helpers / Failure Queue** is **locked / accepted /
canonical (2026-05-25)**. It is implementation output under the locked
Section 25 law; per the Phase Closure Protocol it is not a locked phase until
GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval
complete. Phase 10C added the new `storytime.operator_queue` standard-library
module (the `QueueItem` bounded projection, a `collect_queue` semantic query
over the existing SQLite run/stage/Trust-Envelope state, and plain-text and
deterministic-JSON renderers) and the read-only `storytime queue` CLI command
with `--status`, `--run-id`, `--limit`, and `--json` flags. The command
surfaces the runs needing operator attention — failed, blocked by governance,
marked needs-review, or awaiting an operator approval decision — with, for
each run, why it needs attention and which existing command/report/artifact to
inspect next. It is a viewer only: it adds no message broker, background
worker, new queue storage, new run state, or `pop`/`dequeue`/`claim`/`ack`
behaviour; it mutates nothing and runs no other command. It is bounded
(`--limit` defaults to 20) and deterministic (no generation timestamp), and it
surfaces only structured fields — the `error_kind` code, never the free-text
`error_message`; the §24.8 decision enum, never the free-text `blocked_reason`.
It made no database schema change and added no dependency; 29 new tests and all
six Docker-free gates pass. Locked artifact SHA-256:
`e30aaa57f900756e62347ddaac2df658d96065c9e1061679adb31594c73e2543`. See
`docs/operator-queue.md` for the operator guide.

**Phase 10D — Pipeline Re-Run / Mutation Actions** is **locked (2026-05-25)**:
the `storytime.operator_rerun` module and the governed `storytime rerun`
command — StoryTime's first operator mutation surface. It made no database
schema change and added no dependency. Phase 10D.1 — State Preservation
Cleanup + LLM Director Hardening — is locked. See `docs/operator-rerun.md` for
the operator guide.

**Phase 10E — Static HTML Operator Report Refinement** is **locked
(2026-05-25)**, with the Phase 10E.1 / 10E.2 cleanup sequence accepted and the
10E.2 normalized cleanup as canonical state. It refined the static operator
report — executive status summary, rerun eligibility guidance, failure
summary, command reference, semantic badges, improved CSS — keeping the report
a local, static, read-only artifact with no JavaScript, no external assets,
and no backend behaviour change.

**Phase 10F — Demo Seed Data / Golden Path Fixtures** is **locked
(2026-05-25)**. Phase 10F added the `demo/` directory — four original CC0 demo
seed texts with schema-valid manifests, a demo-only blocked-source deny-list,
and six fixture definitions covering the successful golden path, a retryable
technical failure, a governance-blocked source, a needs-review / approval-gate
run, a rerun-requested run, and a completed-after-rerun run — plus the
`docs/demo.md` operator runbook and `tests/test_demo_fixtures.py`. It added no
product feature, no UI, no server, no generated audio, no JavaScript, and no
new dependency; it changed no pipeline, `storytime rerun`, Trust Envelope, or
schema behaviour. See `docs/demo.md` for the operator demo runbook.

**Phase 10G — Portfolio Narrative / Phase 10 Closure** is **locked
(2026-05-25)** — the locked artifact is
`storytime-phase10g1-uvlock-reversion-cleanup.tar.gz` (SHA-256
`8a0cc9a5b6426a291bec3a793e41501c7d3492187dd48b4f7729ea95e501a0c1`).
Phase 10G was a documentation, portfolio-narrative, demo-explanation, and
Phase 10 closure round. It added the Phase 10 portfolio/closure documents —
`docs/portfolio-narrative.md`, `docs/demo-script.md`,
`docs/operator-experience-walkthrough.md`, `docs/command-reference.md`,
`docs/known-limitations.md`, `docs/observability-governance-talking-points.md`,
`docs/phase10-acceptance-checklist.md`, and `docs/screenshot-instructions.md` —
and synchronized the State Preservation Bundle. It added no product feature, no
UI, no server, no JavaScript, no generated audio, no screenshots/binary assets,
and no new dependency; it changed no pipeline, `storytime rerun`, Trust
Envelope, or schema behaviour. All six Docker-free gates pass. Phase 10G
completed the Phase Closure Protocol and was locked with explicit user
approval; with it, **Phase 10 — Product UI / Operator Experience — is formally
CLOSED**. Phase 11 — Release Candidate Hardening — is now in progress; see the
"Phase 11 — Release Candidate Hardening" section above for its current status.

## Deferred / not authorized

Each requires its own phase and, where it touches the baseline, an explicit
amendment:

- `storytime clean` retention policy (OI-15) — standing functional carryover,
  independent of the deployment track.
- Optional future front-door containerization.
- Cloud deployment.
- Image-registry / image-promotion path.
- Postgres migration (SQLite remains the source of truth).
- Production-grade blue/green state convergence / DB migration strategy.
- Multi-host / HA, production auth, active alerting, error-budget policy.
- OI-3 (observability-image re-verification) and OI-5 (optional TOML file
  config) — unscheduled.

## Phase acceptance gates

Every implementation phase must pass:

1. The six quality gates, all Docker-free:
   - `uv sync --frozen --extra dev`
   - `uv run pytest -q`
   - `uv run ruff check .`
   - `uv run mypy`
   - `uv run lint-imports`
   - `uv run storytime doctor`
2. The Phase Closure Protocol: implementation output → GPT-5.5 review →
   Gemini critique → explicit user approval. Implementation output is never,
   by itself, phase completion.
3. For containerized work specifically: a live Docker smoke check on a
   Docker-capable host. The six gates themselves never require Docker.

## Model-routing expectations

- **GPT-5.5 Thinking** — Mediator / Architect / State Keeper / Prompt Engineer
  / Reviewer.
- **Claude Opus 4.7** — Chief Implementation / Hardening Engineer.
- **Gemini 3 Thinking** — Independent Critic / Architecture Reviewer.
- **Claude Sonnet 4.6** — bounded cleanup only when explicitly directed.

## Architecture-amendment requirements

Changes to the locked Architecture Baseline (`docs/architecture-baseline.md`)
require an explicit, user-approved amendment routed through RoundTable —
authored, Gemini-reviewed, revised if needed, then locked — before any
implementation depends on the change. An amendment is never introduced as an
implementation detail. Precedent: the Phase 7C / 7C.1 amendment to §16.

## Portfolio / demo narrative alignment

StoryTime is also a portfolio-grade engineering artifact. The roadmap is
sequenced so the project always tells a coherent story:

- Phases 0–5 establish a disciplined, observable pipeline (charter, locked
  architecture, vertical slice, approval/resume, OpenTelemetry foundation).
- Phases 6S/6A/6B make the observability *visible and explained* — range-capable
  serving, dashboards-as-code, a demo harness, and an SLO/runbook narrative.
- Phase 7 demonstrates cloud-shaped operational maturity *without leaving
  local-first* — blue/green slots, a front door with active-slot switching,
  and an optional, demo-grade containerized path under an explicit baseline
  amendment.
- Phase 8 will show multi-backend telemetry fan-out (local stack first, vendor
  routing later) — again optional and Collector-owned, so the local-first
  promise and the "telemetry is an optional view" invariant hold.
- Phase 9 adds an honest governance layer — a human-decided, durably recorded
  Trust Envelope and a fail-closed gate before the expensive/externally
  sensitive stages — without ever claiming the system performs legal
  rights-clearance. Governance law (Phase 9A) is defined before the minimal
  implementation (Phase 9B).
- Phase 10 makes the pipeline *legible to a local operator* — a generated,
  static, read-only operator report that faithfully shows what each run did
  and what governance recorded — again local-first, with the operator-experience
  law (Phase 10A) defined before the report is built (Phase 10B), and without
  becoming a hosted SaaS product.

Each phase is meant to be demoable on one machine with no cloud account, and
each is reviewed and locked before the next begins.
