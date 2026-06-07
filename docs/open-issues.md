> **Phase 15C — Minimal Cloud Demo Deployment / Portfolio Readiness (current implementation candidate; pending review; NOT locked).** No new blocking issue is opened by Phase 15C; it is a narrow, demo-first phase that deploys the existing static operator console publicly, pending operator validation and GPT/Gemini review. The known native-Windows POSIX-sensitive pytest failures recorded in `docs/verification-log.md` are pre-existing baseline behaviours (NTFS executable bit, bash-backed script tests, `os.uname`, CRLF hash behaviour, symlink privilege), not Phase 15C defects. Phase 15A and 15B remain LOCKED; Phase 15C is the current candidate (NOT locked); Phase 14E remains NOT STARTED and was not opened (intentionally bypassed); Phase 15D, Phase 15E, and Phase 15F remain NOT STARTED.

> **Phase 15B — Cloud Boundary Readiness (LOCKED).** Phase 15B is now LOCKED with no open issues from the review: the Gemini implementation review returned SAFE TO LOCK with no critical findings, no non-blocking findings, and no required edits, and the GPT preliminary review passed. No new blocking issue is opened by the lock. The native-Windows POSIX-sensitive pytest failures recorded in `docs/verification-log.md` are known baseline behaviours (NTFS executable bit, bash-backed script tests, `os.uname`, CRLF hash behaviour, symlink privilege), not Phase 15B defects, and are deferred-by-design rather than open issues. Phase 12 is CLOSED; Phase 13 is CLOSED; Phase 14 remains STARTED (not closed) with Phase 14D LOCKED; Phase 15A is LOCKED; Phase 14E remains NOT STARTED and was not opened (intentionally bypassed); Phase 15 remains STARTED; Phase 15C, Phase 15D, and Phase 15E remain NOT STARTED.

> **Phase 15B — Cloud Boundary Readiness (current implementation candidate; pending review; NOT locked).** No new blocking issue is opened by Phase 15B; it is an additive, pure-data boundary-readiness phase pending operator validation and GPT/Gemini review. The known native-Windows POSIX-sensitive pytest failures recorded in `docs/verification-log.md` are pre-existing baseline behaviours (NTFS executable bit, bash-backed script tests, `os.uname`, CRLF hash behaviour, symlink privilege), not Phase 15B defects. Phase 15A remains LOCKED; Phase 15B is the current candidate (NOT locked); Phase 14E remains NOT STARTED and was not opened (intentionally bypassed); Phase 15C, Phase 15D, and Phase 15E remain NOT STARTED.

> **Phase 15A — Cloud Runtime Skeleton (LOCKED).** Phase 15A is now LOCKED with no open issues from the review: the Gemini implementation review returned SAFE TO LOCK with no critical findings, no non-blocking findings, and no required edits, and the GPT preliminary review passed. No new blocking issue is opened by the lock. The 14 native-Windows pytest failures recorded in `docs/verification-log.md` are known POSIX-sensitive baseline behaviours (NTFS executable bit, bash-backed script tests, `os.uname`, CRLF hash behaviour, symlink privilege), not Phase 15A defects, and are deferred-by-design rather than open issues. Phase 12 is CLOSED; Phase 13 is CLOSED; Phase 14 remains STARTED (not closed) with Phase 14D LOCKED; Phase 14E remains NOT STARTED and was not opened (intentionally bypassed); Phase 15 remains STARTED; Phase 15B, Phase 15C, Phase 15D, and Phase 15E remain NOT STARTED.

> **Phase 15A — Cloud Runtime Skeleton (current implementation candidate; pending review; NOT locked).** Phase 14D remains the last locked phase; Phase 15 — Cloud / Distributed Runtime — is STARTED, with Phase 15A as the current candidate awaiting review on top of the LOCKED Phase 14D local contracts. Phase 14E remains NOT STARTED (intentionally bypassed). This candidate opens no new blocking issue: it adds a pure-data `storytime.runtime` package (the `api` / `worker` / `combined` role vocabulary with default `combined`, a configuration-derived health/readiness model, and a runtime config boundary reading only `STORYTIME_RUNTIME_ROLE`), documentation, state records, and guard tests, and changes no existing behaviour. Known limitations are deferred-by-design, not defects: it does not implement an external broker, no distributed worker, no object storage, no authentication, no public ingress, no provider TTS, no audio, and no RSS; the `STORYTIME_DEPLOYMENT` dimension is documented as DEFERRED and is not read as active configuration; the role model is descriptive pure data and binds no socket, opens no database, and drains no queue. It is not a distributed system and does not run in the cloud. Phase 15B, Phase 15C, Phase 15D, and Phase 15E remain NOT STARTED, with the later cloud decomposition recorded in the Phase 14D baseline document.

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

# Phase 14C.4 open issues — Minimal Observability Boundary for Queue/Worker

**Date:** 2026-05-29. Phase 14C.4 adds a minimal, backend-owned, in-process observation boundary on the locked Phase 14C.3 baseline.

- **Ephemeral by design.** Observation events are in-process only (no new table/broker/stream); they do not survive process exit and are not exposed to the browser in this phase. Durable/queryable observation and any read-model exposure are deferred.
- **Minimal vocabulary.** A small, vendor-neutral event set is defined now; full telemetry, a collector, exporters, dashboards, alerting/SLOs, sampling, and distributed tracing are explicitly out of scope and deferred to later observability phases.
- **Fail-soft.** A sink error is swallowed (bounded stderr diagnostic) so observation can never break the proof loop or add a worker failure mode.
- **No retry/recovery.** Phase 14C.4 prepares for Phase 14C.5 (Durable Retry / Recovery Lineage) but implements none of it.
- Phase 14C.4 remains implementation candidate / pending review / NOT locked; Phase 14C.5 / 14D / 14E remain NOT STARTED.

# Phase 14C.3 open issues — Object Storage Boundary / Artifact Store Adapter

**Date:** 2026-05-29. Phase 14C.3 adds a backend-owned artifact storage seam (local filesystem adapter) on the locked Phase 14C.2 baseline.

- **Local adapter only.** `LocalFilesystemArtifactStore` is the single adapter. No cloud adapter, external object store, S3/MinIO adapter, signed URLs, or public artifact serving exists yet — those are future work (the cloud/distributed seam baseline is documented in `docs/phase14-contracts-as-built.md`).
- **Key safety is enforced at the adapter.** Absolute paths, `..` traversal, backslash separators, and symlink escapes are rejected; artifacts stay under the configured root. Browser evidence is a relative logical key + content hash/size/media — never a path, root, bucket, signed URL, or credential.
- **Scenarios + queue/worker unchanged.** Routing the evidence write through the store did not change queue/worker semantics or scenario outcomes.
- Phase 14C.3 remains implementation candidate / pending review / NOT locked; Phase 14C.4 / 14D / 14E remain NOT STARTED.

# Phase 14C.2 open issues — Contracts-as-Built / Cloud-Distributed Seam Baseline

**Date:** 2026-05-29. Phase 14C.2 is a docs/contracts/guardrail round on the locked Phase 14C.1 spine; it changes no runtime behavior.

- **Contracts describe local reality, not distributed guarantees.** `docs/phase14-contracts-as-built.md` documents local no-double-execution under the tested SQLite/local-worker model — explicitly NOT exactly-once semantics across a distributed system. SQLite concurrency limits remain a known local constraint; SQLite is an adapter, not the architecture.
- **Seams are documented, not implemented.** The queue-adapter, worker-execution, artifact-storage, auth-capable-API, observability, and hosted-durable-state seams are named as future replacement points. No cloud adapter, external broker, distributed worker pool, object storage, auth, retry/recovery lineage, provider TTS, audio, or RSS exists yet.
- **Guard remains substring-based.** The state-discipline guard uses positive-claim forbidden phrases and line-scoped checks; it is intentionally not a prose-quality judge.
- Phase 14C.2 remains implementation candidate / pending review / NOT locked; Phase 14C.3 / 14D / 14E remain NOT STARTED.

# Phase 14C.1.1 cleanup note — Stale Partial Execution Recovery

**Date:** 2026-05-29. Narrow pre-lock cleanup of the Phase 14C.1 candidate (not a new phase).

- **Stale partial execution now handled.** Earlier the queue/worker recovered a worker lost *before* executing stages; it now also handles a worker lost *after* committing one or more stages but before terminal completion — the recovered run is **failed cleanly** with no re-execution and no duplicate stages (a durable `RunFailed` event records the stale-partial recovery). True resumable partial-stage continuation is intentionally NOT implemented and remains possible later work if ever needed.
- Phase 14C.1 remains implementation candidate / pending review / NOT locked; Phase 14C.2 / 14D / 14E remain NOT STARTED.

# Phase 14C.1 open issues — Local Durable Queue / Worker Shape Proof

- **Local shape, not distributed semantics.** The queue/worker proves a LOCAL durable execution shape with bounded stale-claim recovery and no double execution under the tested local worker model. It is explicitly NOT full distributed exactly-once execution, a cloud queue, or an external broker. Hosted/distributed adapters remain future work (Phase 14C.2 documents the contracts-as-built seam).
- **Single local worker.** Execution is drained by one bounded local worker (a single background thread in the running server; synchronous in tests). A worker pool / supervisor is out of scope.
- **No retry action yet.** Phase 14C.1 recovers stale claims internally but adds no operator-facing retry/recovery action; durable retry/recovery lineage is Phase 14C.5.
- **Windows smoke is operator-run**, as in prior phases; the queue/worker path uses no chmod/os.uname/bash/symlinks/ffmpeg.
- **Deferred (NOT STARTED):** Phase 14C.2 seam baseline, 14C.3 object storage, 14C.4/14C.6 observability, 14C.5 retry lineage, 14C.7 auth boundary; the Phase 14D content arc (provider TTS, audio understanding, RSS); and Phase 14E closure.

# Phase 14B.1 open issues — Live Proof Loop Hardening / Operator Trust

- **No JavaScript test runner.** The frontend has no Jest/Vitest suite, so the new failure-rendering UX (failure-reason panel, marked failed stage, bounded post-run refresh) is covered only by `tsc` typecheck, the Vite build, the typed client, a forbidden-token scan, and manual smoke — not by automated component tests. Adding a JS test runner remains optional future work.
- **Windows smoke is operator-run.** The PowerShell two-terminal smoke (success + both failure scenarios + restart-persistence) is documented but was not executed in the build environment; the operator should run it. Some older-phase tests assume POSIX behaviour and may fail under native Windows `pytest`; this is pre-existing and unrelated to the proof loop, which uses no `chmod`/`os.uname`/bash/symlinks/ffmpeg.
- **Failure proof only (no retry).** Phase 14B.1 intentionally implements controlled failure *proof*; a durable retry/recovery action is deferred to Phase 14C.1+.
- **Deferred (Phase 14C.1+, NOT STARTED):** real provider-backed TTS, frontend audio/TTS generation, audio playback, cloud/distributed mode, authentication, and RSS publishing.

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

# Phase 13F note — Local Bridge Architecture & Contract Baseline

**Phase 13F — Local Bridge Architecture & Contract Baseline — is the
current implementation candidate (pending review, NOT locked).**
Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary — is
locked and is the last locked phase (SHA-256
`a997f2ca9d213e28e140f47c63336367c8feda46ed994b41300f86b99f8d8164`).
**Phase 12 — Portfolio / SE Demo Packaging — is CLOSED**, **Phase 11
— Release Candidate Hardening — is CLOSED**, and Phase 10 is CLOSED.
**Phase 13 — Portfolio Website / Operator GUI — is STARTED.** Phase
13G and every later Phase 13 subphase have not started — they are
future, planned work only. Phase 9C remains optional and not
scheduled.

Phase 13F is a documentation-and-static-fixture architecture /
contract baseline — the architectural lock before any Python
local-bridge implementation is allowed. It adds eleven new
architecture / contract docs, non-runtime JSON example fixtures under
`docs/examples/`, and one new Python contract-examples test; it
establishes that the frontend is an operator surface, not the durable
storage layer, and settles the future local-bridge execution-timing
policy, security boundary, action allowlist, and queue-observability
model. Phase 13F implements no runtime code (no local bridge, no
server, no async queue, no workers, no metrics exporters, no storage
providers, no real Local mode, no Cloud/Distributed mode, no mutation
execution); the browser remains non-durable.

**Open-issues update.** Phase 13F introduces no new open issues. The
standing carryover item is unchanged: OI-15 — Cleanup verification
tooling — remains open and tracked in this file. Phase 13F also
records, as forward-looking design context (not open issues), the
deferred Local-mode work enumerated in
`docs/phase13f-local-bridge-contract-readiness.md` and
`docs/frontend-gui-deferred-work-register.md`: the local bridge
itself, the async action queue and its observability instrumentation,
queue workers, metrics exporters, storage providers, and real Local /
Cloud-Distributed mode all remain deferred to later, separately-gated
phases.

*(The Phase 13E-era and earlier notes below are historical records.
Phase 13E is LOCKED; Phase 13F is the current implementation
candidate. The open issues themselves continue uninterrupted below.)*

---
# Phase 13E note — Demo-Mode Action Preview / Operator Intent Boundary (historical record — Phase 13E is LOCKED; see the Phase 13F note above)

**Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary —
was the implementation candidate while this note was written. Phase
13E has since been LOCKED and is the last locked phase.** Phase 13D.2
— Static Demo Walkthrough / Reviewer Story Path — is locked. **Phase 12 — Portfolio
/ SE Demo Packaging — is CLOSED**, **Phase 11 — Release Candidate
Hardening — is CLOSED**, and Phase 10 is CLOSED. **Phase 13 —
Portfolio Website / Operator GUI — is STARTED.** Phase 13G and every
later Phase 13 subphase have not started — they are future, planned
work only. Phase 9C remains optional and not scheduled.

Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary —
is a static, **Demo-mode-only**, **non-consequential** sub-round of
the locked Phase 13D.2. It turns the existing visibly-disabled
future-action affordances into explainable, non-executing action
previews via a new static view-model adapter
(`actionPreviewAdapter.ts`), a new presentation panel
(`ActionPreviewPanel.tsx` + CSS Module), and light integration into
Failure / Recovery, Governance / Safety, and Evidence / Validation
alongside the existing disabled-action display (which remains
unchanged). It introduces or clarifies the eventual operating-mode
model — Demo / Local / Cloud-Distributed — distinct from the
existing Demo / Active / Candidate data-snapshot labels. Phase 13E
introduced no new open issues. The standing carryover items are
unchanged: OI-15 — Cleanup verification tooling —
remains open and tracked in this file.

*(The Phase 13D.2-era note below is a historical record. Phase 13D.2
is LOCKED; Phase 13E is LOCKED. The
open issues themselves continue uninterrupted below.)*

---
# Phase 13D.2 note — Static Demo Walkthrough / Reviewer Story Path (historical record — see the Phase 13E note above)

**Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path —
was the implementation candidate while this note was written. Phase
13D.2 has since been LOCKED and is the last locked phase.** Phase
13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action
Discipline — is locked. **Phase 12 — Portfolio / SE Demo Packaging
— is CLOSED**, **Phase 11 — Release Candidate Hardening — is
CLOSED**, and Phase 10 is CLOSED. **Phase 13 — Portfolio Website /
Operator GUI — is STARTED.** Phase 13E and every later Phase 13
subphase have not started — they are future,
planned work.

Phase 13D.1 opened no new open issue and closed no open issue. It is a
frontend-only static / read-only refinement sub-round over the locked
Phase 13D operator views: it standardized the disabled future-action
display into a reusable component (real `<button disabled={true}>`, no
`onClick`), replaced the Evidence / Validation placeholder with a real
read-only view carrying the mandatory STATIC PORTFOLIO DATA — NOT A LIVE
CI/CD DASHBOARD disclaimer and repository-relative evidence references,
added a Demo / Active / Candidate Data Source framing block (data
snapshots, not deployment environments — no switcher implemented), and
extracted the nav metadata from `App.tsx` into a small typed
`frontend/src/navigation.ts` helper. It modified no backend code:
`src/storytime/operator_export.py`, the committed
`frontend/src/data/storytime-demo-export.json`, the `storytime
export-demo-ui` CLI contract, and `src/storytime/cli/app.py` are
byte-identical to the Phase 13D source. **OI-15 — `storytime clean`
retention policy — remains the one open standing carryover** and is
intentionally deferred until a future Post-Phase-13 / hosting / GA-prep
round.

The frontend / GUI deferred-work register
(`docs/frontend-gui-deferred-work-register.md`) was updated in Phase
13D.1 to record: the Evidence / Validation view as **implemented**
(§1, §11); the Governance / Safety and Failure / Recovery views as
**refactored** to use the shared disabled-action component (§1, §10);
§4 CSS scalability debt as still **partially addressed**, with Phase
13D.1 adding no new global selectors; §5 view-expansion recommendations
marked as **delivered**; §8 Demo / Blue / Green Data Snapshot Switcher
explicitly renamed to **Demo / Active / Candidate Data Snapshot
Switcher** (data snapshots, not deployment environments — still
deferred); §9 runtime schema validation / async export loading still
deferred; new §10 (disabled-action component) and §11 (Evidence view)
and §12 (navigation extraction) describing what Phase 13D.1
implemented.

Items that remain deferred to Phase 13E or later: real local actions /
mutation boundary; runtime schema validation (Zod / Valibot); async or
file-backed export loading; the actual Demo / Active / Candidate
snapshot switcher; the remaining placeholder views (Architecture Story,
Demo Walkthrough, Roadmap, Settings / Config).

*(Every Phase 13D-era and earlier note below is a historical record.
Phase 13D is LOCKED; Phase 13D.1 is the current implementation
candidate.)*

---
# Phase 13D note — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) (historical record — Phase 13D is LOCKED; see the Phase 13D.1 note above)

**Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure
/ Recovery) — is the current implementation candidate (pending review, NOT
locked).** Phase 13C — Deterministic Read-Only Static Export / Frontend Data
Alignment — is locked and is the last locked phase. **Phase 12 — Portfolio /
SE Demo Packaging — is CLOSED**, **Phase 11 — Release Candidate Hardening —
is CLOSED**, and Phase 10 is CLOSED. **Phase 13 — Portfolio Website /
Operator GUI — is STARTED.** Phase 13E and every later Phase 13 subphase
have not started — they are future, planned work.

Phase 13D opened no new open issue and closed no open issue. It is a
frontend-only round that expanded two placeholder operator views into real
read-only views against the locked Phase 13C deterministic static export. It
modified no backend code: `src/storytime/operator_export.py`, the committed
`frontend/src/data/storytime-demo-export.json`, and the `storytime
export-demo-ui` CLI contract are byte-identical to the Phase 13C source.
**OI-15 — `storytime clean` retention policy — remains the one open
standing carryover** and is intentionally deferred until a future
Post-Phase-13 / hosting / GA-prep round.

The frontend / GUI deferred-work register
(`docs/frontend-gui-deferred-work-register.md`) was updated in Phase 13D to
record:

- Governance / Safety and Failure / Recovery as **implemented** (no longer
  placeholder rows in §1).
- §4 CSS scalability debt as **partially addressed**: CSS Modules are
  introduced for the two new Phase 13D components, the existing global
  stylesheet is not migrated, and a single small `.data-chip` rule is the
  only global addition. A wholesale shell/Phase-13B/C migration remains
  deferred.
- A new §8 — **Demo / Blue / Green Data Snapshot Switcher** — as a future
  Settings / Config affordance, with constraints (read-only data sources,
  no backend mutation, no destructive UI wording, the "Promote" action
  remains disabled until an explicit safe-mutation subphase).
- A new §9 — **Runtime data validation / schema discipline** — capturing
  Zod / runtime schema validation, runtime `schemaVersion` enforcement,
  and asynchronous / file-backed export loading as deferred future items.

These are tracking entries; they authorize nothing. No new open issue is
opened by Phase 13D.

*(The Phase 13C-era note below is a historical record. Phase 13C is LOCKED;
Phase 13D is the current implementation candidate.)*

---
# Phase 13C note — Deterministic Read-Only Static Export / Frontend Data Alignment (historical record — Phase 13C is LOCKED; see the Phase 13D note above)

**Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment —
is the current implementation candidate (pending review, NOT locked).** Phase
13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — is
locked and is the last locked phase. **Phase 12 — Portfolio / SE Demo Packaging
— is CLOSED** (Phase 12A through 12D all locked), **Phase 11 — Release
Candidate Hardening — is CLOSED**, and Phase 10 is CLOSED. **Phase 13 —
Portfolio Website / Operator GUI — is STARTED.** Phase 13D and every later
Phase 13 subphase have not started — they are future, planned work.

Phase 13C opened no new open issue and closed no open issue. It establishes a
deterministic, read-only static data boundary between backend truth and the
Phase 13B frontend: it adds a small read-only backend export module
(`src/storytime/operator_export.py`) and a `storytime export-demo-ui` CLI
command producing a deterministic static JSON export with a top-level
`schemaVersion`, the export contract document
`docs/frontend-static-export-contract.md`, the frontend / GUI deferred-work
register `docs/frontend-gui-deferred-work-register.md`, a frontend adapter and
a `StaticDemoExport` type, backend contract tests, and it rewires the homepage
and Pipeline Run Detail / Stage Timeline onto the adapter. It lightly updated
`README.md` and `frontend/README.md`, advanced the state-discipline guard
`tests/test_failure_mode_regression.py` under the narrow, explicitly authorized
mechanical exception, and synchronized the State Preservation Bundle. The
frontend remains static, read-only, and export-backed; the backend code added
is read-only and deterministic and changed no core pipeline runtime behaviour
and no root dependency. The new frontend / GUI deferred-work register
(`docs/frontend-gui-deferred-work-register.md`) now tracks deferred frontend
work; it is a tracking document and authorizes nothing. **OI-15 — `storytime
clean` retention policy — remains the one open standing carryover** and is
unchanged by Phase 13C.

*(The Phase 13B note and Phase 12D note below — and the Phase 12C, Phase 12B,
Phase 12A, Phase 11C, Phase 11B, Phase 11A, and Phase 10G notes further below —
are historical records. Phase 13B is locked; Phase 12, Phase 11, and Phase 10
are closed; Phase 13C is the current implementation candidate.)*

---

# Phase 13B note — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold (historical record — Phase 13B is LOCKED; see the Phase 13C note above)

**Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold —
is LOCKED and is the last locked phase.** *(Historical record — current status
is in the Phase 13C note above.)* Phase 13A — Portfolio Website / Operator GUI
Architecture Baseline — is locked. **Phase 12 — Portfolio / SE Demo Packaging —
is CLOSED** (Phase 12A through 12D all locked), **Phase 11 — Release Candidate
Hardening — is CLOSED**, and Phase 10 is CLOSED. **Phase 13 — Portfolio Website
/ Operator GUI — is STARTED.**

Phase 13B opened no new open issue and closed no open issue. It was the first
frontend implementation round of Phase 13: against the locked Phase 13A
contract it added a new top-level `frontend/` directory — a React + TypeScript +
Vite project containing the frontend read-model contract, a static demo
dataset of two mock pipeline runs, the portfolio homepage, one Pipeline Run
Detail view with a visual Stage Timeline, honest placeholders for the future
views, and a frontend README — lightly updating `README.md`, advancing the
state-discipline guard `tests/test_failure_mode_regression.py` under the
narrow, explicitly authorized mechanical exception, and synchronizing the State
Preservation Bundle. The frontend is static, read-only, and demo-data-backed;
it contacts no backend. Phase 13B changed no backend source code, no
dependency, and no product behaviour. **OI-15 — `storytime clean` retention
policy — remains the one open standing carryover** and is unchanged by Phase
13B.

*(The Phase 12D note and Phase 12C note below — and the Phase 12B, Phase 12A,
Phase 11C, Phase 11B, Phase 11A, and Phase 10G notes further below —
are historical records. Phase 13B is locked; Phase 12, Phase 11, and Phase 10
are closed; Phase 13C is the current implementation candidate.)*

---

# Phase 12D note — Phase 12 Closure Plan / Final Portfolio Handoff Definition (historical record — Phase 12D is LOCKED; Phase 12 is CLOSED)

**Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — is
LOCKED and is the last locked phase, and Phase 12 — Portfolio / SE Demo
Packaging — is CLOSED.** *(Historical record — current status is in the
Phase 13C note above.)* Phase 12C —
Portfolio Demo Narrative / Public Presentation Kit — is locked. Phase 12A and
Phase 12B are also locked. **Phase 11 — Release
Candidate Hardening — is CLOSED; Phase 12 — Portfolio / SE Demo Packaging — is
CLOSED.** Phase 10 is CLOSED. Phase 12E was optional, contingency-only work and
was never needed and never started; Phase 13 — Portfolio Website / Operator
GUI — is STARTED.

Phase 12D opened no new open issue and closed no open issue. It is a
documentation-only closure-definition round: it added three closure-definition
`docs/` documents (`phase12-closure-plan.md`, `final-portfolio-handoff.md`,
`phase12-final-review-checklist.md`), lightly updated `README.md`, advanced the
state-discipline guard `tests/test_failure_mode_regression.py` under the
narrow, explicitly authorized mechanical exception, and synchronized the State
Preservation Bundle. It changed no source code, no dependency, and no product
behaviour. **OI-15 — `storytime clean` retention policy — remains the one open
standing carryover** and is unchanged by Phase 12D.

*(The Phase 12C note and Phase 12B note below — and the Phase 12A, Phase 11C,
Phase 11B, Phase 11A, and Phase 10G notes further below — are historical
records. Phase 12C is locked; Phase 11 and Phase 10 are closed; Phase 12D is
the current implementation candidate.)*

---

# Phase 12C note — Portfolio Demo Narrative / Public Presentation Kit (historical record — Phase 12C is LOCKED)

**Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — is LOCKED**
and is the last locked phase. *(Historical record — current status is in the
Phase 12D note above.)* Phase 12B — Portfolio Evidence Pack / Reviewer Assets —
is also locked (the accepted Phase 12B.1 / 12B.2 / 12B.3 cleanup sub-rounds are
folded into its lock lineage). **Phase 11 — Release Candidate Hardening — is
CLOSED; Phase 12 — Portfolio / SE Demo Packaging — is STARTED** and not closed.
Phase 10 is CLOSED. Phase 12D is the current implementation candidate;
Phase 12E and later subphases have not started.

Phase 12C opened no new open issue and closed no open issue. It is a
documentation-first portfolio-packaging round: it added four public-presentation
`docs/` documents (`portfolio-demo-narrative.md`, `demo-talk-track.md`,
`interview-story-bank.md`, `public-repository-readiness.md`), lightly updated
`README.md` to point reviewers to them, advanced the state-discipline guard
`tests/test_failure_mode_regression.py` under the narrow, explicitly authorized
mechanical exception, and synchronized the State Preservation Bundle. It
changed no source code, no dependency, and no product behaviour. **OI-15 —
`storytime clean` retention policy — remains the one open standing carryover**
and was unchanged by Phase 12C.

---

# Phase 12B note — Portfolio Evidence Pack / Reviewer Assets (locked — historical record)

**Phase 12B — Portfolio Evidence Pack / Reviewer Assets — is LOCKED** and is
the last locked phase (the accepted Phase 12B.1 / 12B.2 / 12B.3 cleanup
sub-rounds are folded into its lock lineage). *(Historical record — current
status is in the Phase 12D note at the top of this file.)* Phase 12A —
Portfolio / SE Demo Packaging Baseline — is also locked. **Phase 11 — Release
Candidate Hardening — is CLOSED; Phase 12 — Portfolio / SE Demo Packaging — is
STARTED** and not closed. Phase 10 is CLOSED. At the time this note was
written, Phase 12C was the current implementation candidate; Phase 12C has
since been locked and Phase 12D is now the current implementation candidate.

Phase 12B opened no new open issue and closed no open issue. It is a reviewer /
evidence packaging round: it added four reviewer/evidence `docs/` documents
(`portfolio-evidence-index.md`, `se-interview-evidence-matrix.md`,
`demo-reviewer-checklist.md`, `portfolio-public-copy.md`), lightly updated
`README.md` to point reviewers to them, advanced the state-discipline guard
`tests/test_failure_mode_regression.py` under the explicitly authorized §5
mechanical exception, and synchronized the State Preservation Bundle. It
changed no source code, no dependency, and no product behaviour. **OI-15 —
`storytime clean` retention policy — remains the one open standing carryover**
and is unchanged by Phase 12B.

*(The Phase 12A note below — and the Phase 11C, Phase 11B, Phase 11A, and
Phase 10G notes further below — are historical records. Phase 12A is locked;
Phase 11 and Phase 10 are closed; Phase 12B is the current implementation
candidate.)*

---

# Phase 12A note — Portfolio / SE Demo Packaging Baseline (locked — historical record)

**Phase 12A — Portfolio / SE Demo Packaging Baseline — is LOCKED** and is the
last locked phase (locked after the accepted Phase 12A.1 state-hygiene cleanup
sub-round). *(Historical record — current status is in the Phase 12B note
above.)* **Phase 11 — Release Candidate Hardening — is CLOSED; Phase 12 —
Portfolio / SE Demo Packaging — is STARTED.** Phase 10 is CLOSED.

Phase 12A opened no new open issue and closed no open issue. It is a
documentation and portfolio-packaging round: it added four portfolio `docs/`
documents (`portfolio-overview.md`, `solutions-engineer-narrative.md`,
`portfolio-demo-script.md`, `interview-talking-points.md`), refined `README.md`
for a portfolio-facing reviewer, advanced the state-discipline guard
`tests/test_failure_mode_regression.py` under explicit authorization, and
synchronized the State Preservation Bundle. It changed no source code, no
dependency, and no product behaviour. **OI-15 — `storytime clean` retention
policy — remains the one open standing carryover** and is unchanged by
Phase 12A.

*(The Phase 11C note below — and the Phase 11B, Phase 11A, and Phase 10G notes
further below — are historical records. Phase 11D is locked and Phase 11 is
closed; Phase 12A is locked, and Phase 12B is the current implementation
candidate.)*

---

# Phase 11C note — Failure-Mode / Regression Hardening (locked — historical record)

**Phase 11C — Failure-Mode / Regression Hardening — is LOCKED.** Phase 11 —
Release Candidate Hardening — is CLOSED. *(This note was originally written
when Phase 11C was the current implementation candidate; Phase 11C, and
subsequently Phase 11D, were locked under the Phase Closure Protocol, and
Phase 11 was formally closed. Current status is in the Phase 12A note above.)*

Phase 11C opened no new open issue and closed no open issue. It is a
failure-mode and regression-hardening round: it inventoried the highest-risk
failure and regression paths that already exist in StoryTime, recorded which
tests and gates protect each one, documented operator failure-response, and
added one focused regression test module
(`tests/test_failure_mode_regression.py`). It changed no source code, no
dependency, and no product behaviour. **OI-15 — `storytime clean` retention
policy — remains the one open standing carryover** and is unchanged by
Phase 11C.

*(The Phase 11B note below is a historical record — Phase 11B is locked. The
Phase 11A note and the Phase 10G lock closure note further below are
historical records; Phase 10 and Phase 11 are CLOSED; Phase 12A is the current
implementation candidate — see the Phase 12A note at the top of this file.)*

---

# Phase 11B note — Fresh Clone / Operator Reproducibility (locked — historical record)

**Phase 11B — Fresh Clone / Operator Reproducibility — is LOCKED and is the
last locked phase.** *(This note was originally written when Phase 11B was an
implementation candidate; Phase 11B was subsequently locked under the Phase
Closure Protocol and is the source/base artifact for Phase 11C. Current status
is in the Phase 11C note above.)*

Phase 11B opened no new open issue and closed no open issue. It was a
fresh-clone / operator reproducibility verification round; it changed no
source code, no dependency, and no product behaviour. OI-15 — `storytime
clean` retention policy — remained the one open standing carryover and was
unchanged by Phase 11B.

*(The Phase 11A note below is a historical record — Phase 11A is locked. The
Phase 10G lock closure note further below is a historical record; Phase 10 is
CLOSED.)*

---

# Phase 11A note — Release Candidate Hardening Baseline (locked — historical record)

**Date:** 2026-05-25
**Status:** Phase 11A — Release Candidate Hardening Baseline is **LOCKED / ACCEPTED / CANONICAL**. *(This note was originally written when Phase 11A was an implementation candidate; Phase 11A was subsequently locked under the Phase Closure Protocol. Phase 11B is now also locked and is the last locked phase; current status is in the notes above.)*

Phase 11A — the first subphase of Phase 11 — Release Candidate Hardening — is a
documentation-first hardening round. It audits and documents the repository's
non-feature surfaces and adds seven `docs/` hardening documents
(`release-candidate-hardening.md`, `phase11-plan.md`, `local-setup-runbook.md`,
`fresh-clone-checklist.md`, `rc-validation-checklist.md`,
`security-secrets-checklist.md`, `demo-reproducibility-checklist.md`) plus the
synchronized State Preservation Bundle. It added no product feature, no UI, no
server, no JavaScript, no generated audio, no new dependency, and no schema
change; it changed no `pyproject.toml`, `uv.lock`, `src/`, or `tests/` content.
**Phase 11A opened no open issue and closed none** — the standing carryover
register is unchanged: **OI-15** remains the active standing functional
carryover; **OI-3**, **OI-5**, **OI-21**, **OI-22** remain unscheduled
environment/optional items; none block any phase gate.

The Post-Phase-10 Historical State Reconciliation — the last locked work item
before Phase 11 — likewise opened and closed no open issue.

*(The Phase 10G lock closure note below is a historical record. Phase 10 and
Phase 11 are CLOSED; Phase 11A through 11D are locked; Phase 12A is the current
implementation candidate — see the Phase 12A note at the top of this file.)*

---

# Phase 10G lock closure note — Phase 10 CLOSED

**Date:** 2026-05-25
**Locked artifact:** `storytime-phase10g1-uvlock-reversion-cleanup.tar.gz`
**SHA-256:** `8a0cc9a5b6426a291bec3a793e41501c7d3492187dd48b4f7729ea95e501a0c1`
**Status:** Phase 10G — Portfolio Narrative / Phase 10 Closure is **LOCKED / ACCEPTED / CANONICAL**. **Phase 10 is formally CLOSED.**
**Last locked phase:** Phase 10G — Portfolio Narrative / Phase 10 Closure.
**Next phase:** Phase 11 — Release Candidate Hardening *(now in progress — see the Phase 11C implementation-candidate note at the top of this file for current status; Phase 11A and Phase 11B are locked)*.

Phase 10G — the documentation, portfolio-narrative, demo-explanation, and Phase 10 closure phase — is locked. It added the Phase 10 portfolio/closure documents (`docs/portfolio-narrative.md`, `docs/demo-script.md`, `docs/operator-experience-walkthrough.md`, `docs/command-reference.md`, `docs/known-limitations.md`, `docs/observability-governance-talking-points.md`, `docs/phase10-acceptance-checklist.md`, `docs/screenshot-instructions.md`) and synchronized the State Preservation Bundle. It was documentation-first: no new product feature, no UI, no server, no generated audio committed, no JavaScript, no screenshots/binary assets, no new dependency, and no change to pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, or the database schema. **Phase 10G opened no open issue and closed none** — the standing carryover register is unchanged. The subsequent Post-Phase-10 Closure State Synchronization (which produced this note) likewise opened and closed no open issue. With Phase 10G locked, **Phase 10 — Product UI / Operator Experience — is formally CLOSED** (Phases 10A–10G all locked); the next phase is **Phase 11 — Release Candidate Hardening**, not started.

*(The Phase 10F lock closure note and the Phase 10C lock closure note below are historical records. Phase 10A, 10B, 10C, 10C.1, 10D, 10D.1, 10E — with the 10E.1 / 10E.2 cleanup sequence — 10F, and 10G are all locked; Phase 10 is closed.)*

---

# Phase 10F lock closure note

**Date:** 2026-05-25
**Lock archive:** `storytime-phase10f-demo-seed-data-golden-path-fixtures.tar.gz`
**SHA-256:** `e060570a94fb19f790c539542b3ef7445111430bc308668675548f66fa48df55`
**Status:** Phase 10F — Demo Seed Data / Golden Path Fixtures is **LOCKED / ACCEPTED / CANONICAL**.

Phase 10F added curated demo seed data and golden-path fixture scenarios — the `demo/` directory (four original CC0 seed texts plus schema-valid manifests, a demo-only blocked-source deny-list, and six fixture definitions), the `docs/demo.md` operator runbook, and `tests/test_demo_fixtures.py`. It was fixture / demo-readiness work that exercises the existing system: no new product feature, no UI, no server, no generated audio committed, no JavaScript, no new dependency, and no change to pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, or the database schema. **Phase 10F opened no open issue and closed none.** Phase 10F completed the Phase Closure Protocol and was locked with explicit user approval.

*(The Phase 10C lock closure note below is a historical record, superseded by this Phase 10F closure.)*

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

# Open Issues

## Phase 10B lock note

Phase 10B — Generated Local HTML Operator Report is locked (2026-05-24). *(Historical state at time of Phase 10B lock — Phase 10C has since been locked; see Phase 10C lock closure note above.)*


Living list of carryover items and decisions. Not locked. Rows marked
**Done** record when and how an issue was resolved. Rows marked
**carryover** form the backlog for the next phase and are collected under
"Carryover backlog" at the end of this file.

| ID    | Issue | Disposition |
|-------|-------|-------------|
| OI-1  | Multi-stage sequencing and resume/rehydration from SQLite are not implemented. `PipelineRunner.execute_stage` runs one stage. | **Done (Phase 3).** `PipelineRunner.run_sequence` threads four stages and stops on the first non-`SUCCEEDED` result. Resume/rehydration of a partially completed run is tracked separately as OI-10. |
| OI-2  | Linked traces and W3C `traceparent` threading: stages do not propagate a `traceparent`, and `OTelTelemetry.start_linked_run` starts a fresh root span instead of attaching a `Link` to the prior trace. | **Done (Phase 5).** Genuine implementation, no placeholders. (a) The runner stamps each stage's own span `traceparent` into its `StageInput` before the stage runs, so the stage writes that traceparent into the `trace_context` of every artifact envelope it produces; (b) `stage_execution.parent_trace_id` records the run-span → stage-span hierarchy; (c) a resumed run opens a `pipeline.resume` span that carries a real W3C `Link` to the pre-pause trace — `build_resume_plan` recovers that `prior_traceparent` from the last completed stage's artifact envelope `trace_context`; (d) `traceparent` survives the process-exit boundary of a paused run inside the durable artifact envelope, and the `approval` row records `inbound_trace_id` (written at decision time by `apply_approval_decision`) and `outbound_trace_id` (written once by the first resume that crosses the gate). One deliberate, documented simplification: regime 2 (non-approval continuation) uses the same "new trace + Link to prior" model as regime 3 (the approval boundary) rather than a pure single-trace continuation — two linked traces is a valid, honest topology and avoids pretending a separate CLI invocation was one uninterrupted span. Everything stays correct under `NoopTelemetry`, where every `traceparent` is `None` and `pipeline_run_id` remains the durable correlation key. See `docs/telemetry-map.md`. |
| OI-3  | Observability-stack Docker image tags are pinned but unverified in the build environment. Phase 6A adds two more: `prom/prometheus:v2.55.1` and `grafana/grafana:11.4.0`, alongside `jaegertracing/all-in-one:1.62.0` and `otel/opentelemetry-collector-contrib:0.114.0`. | Docker was unavailable in the Phase 5/6S/6A build environments, so all four tags remain unverified there. Re-verify on a machine with Docker: `docker compose -f docker-compose.observability.yml pull` and `... config`. The StoryTime test suite never requires the stack, so this does not block any phase gate. |
| OI-4  | `StateUpdate.approval` and `StateUpdate.published_episode` intents are defined but the runner does not yet write them to the `approval` / `published_episode` tables. | **Done (Phase 3).** `run_sequence._apply_state_update` translates an `approval` intent via `record_approval` and a `published_episode` intent via `record_published_episode`, inside the stage's single persistence transaction. |
| OI-5  | `config/storytime.toml` is a sample only; configuration is environment-driven. | Optional; Phase 4 or later. Add a TOML config loader only if file-based config is wanted. |
| OI-6  | The three locked planning docs were marker files, not full-text copies. | **Done.** The Phase 2 documentation-sync round replaced the markers with the full canonical text of the product charter, architecture baseline, and phase-closure protocol. |
| OI-7  | HTTP server uses stdlib `http.server`, which does not support HTTP range requests — acceptable for the Phase 2 skeleton, not for serving real audio. | **Done (Phase 6S).** `RangeFileHandler` serves the feed directory over a loopback-only `ThreadingHTTPServer` and honours HTTP byte ranges through the pure, separately tested `parse_byte_range`: a `Range` header yields `206 Partial Content` with a `Content-Range`; an unsatisfiable range yields `416` with `Content-Range: bytes */<size>`; an absent or malformed header serves the whole file (`200`). `Accept-Ranges: bytes` is always sent; `feed.xml` is served as `application/rss+xml` and `*.mp3` as `audio/mpeg`. The handler never escapes the feed root (a `../` request is a `404`). The canonical `storytime serve [--port]` command (Architecture Baseline section 4) starts it. `SimpleHTTPRequestHandler` is no longer used — an ARCH-LOCK on `http/server.py` records why. `parse_byte_range`, which had no tests despite its docstring, now has exhaustive coverage. |
| OI-8  | mypy is scoped to the `storytime` package; `tests/` is validated by pytest only. | Acceptable; revisit if test typing regressions appear. |
| OI-9  | The canonical interactive approval step — an operator decision recorded against a pending run, with persisted approval/rejection gates between stages — is not implemented. | **Done (Phase 4).** `ApprovalGateStage` is a real, pure pipeline stage that returns `AWAITING_APPROVAL`; the run pauses and the process exits cleanly. `storytime approve` records a genuine operator decision (an `approval` row with `stage_name="approve_text"` plus a `TextApproved`/`TextRejected` event, in one transaction). The text gate emits `TextApprovalRequested`. Audio-gate wiring was completed in Phase 4.1 (OI-13). |
| OI-10 | Resume/rehydration: a run cannot be reloaded from SQLite and continued from its last completed stage. `run_sequence` always executes a fresh slice end to end. | **Done (Phase 4).** `PipelineRunner.resume_sequence` executes only the not-yet-completed tail of a run; `storytime.runner.rehydrate` reconstructs and validates a `ResumePlan` from SQLite (run row, `stage_execution` rows, the new `stage_artifact` table) and artifact envelopes. Completed-stage artifacts are rehydrated, hash-verified, and never regenerated. `storytime run --resume` and the granular stage commands are backed by it. |
| OI-11 | The RSS feed is single-item: `publish` writes a `feed.xml` describing only the current episode and does not aggregate previously published episodes for the channel. | **Done (Phase 6S).** `PublishStage` builds a multi-item feed: the episode being published is prepended to every prior episode and the whole feed is re-rendered, so a subscriber sees the full back catalogue. Prior episodes are supplied by an injected, read-only `EpisodeCatalog` (the `StateEpisodeCatalog` adapter, wired in the composition root) — the stage never imports `storytime.state`, preserving the publish-stage boundary (clarification A1). Migration `0004` adds `published_episode.description` so each prior `<item>` keeps its own description on regeneration; `feed_version` is now the real monotonic feed-regeneration counter (`len(prior) + 1`) the stage computes, not a hardcoded `1`. The rendered feed is validated and then swapped into place atomically via the new `StorageAdapter.write_text_atomic` — closing the section-14 validate-before-atomic-replace gap that the prior single-item write did not honour. The current GUID is de-duplicated out of the prior set defensively. |
| OI-12 | The canonical per-stage CLI commands (`ingest`, `approve`, `synthesize`, `assemble`, `publish`) are present in the CLI surface and in `--help`, but report an intentional Phase 4 deferral when invoked instead of executing a stage. | **Done (Phase 4).** The per-stage commands now do real work: `ingest` starts a gated run and pauses at the approval gate; `approve` records the operator decision; `synthesize`/`assemble`/`publish` rehydrate the run from SQLite and carry it forward one stage. The Phase 3 surface test (`tests/test_cli_surface.py`) was updated from the interim deferral contract to this real-behaviour contract — the one Phase 3 test changed by Phase 4. |
| OI-13 | The audio approval gate (`approve_audio`) is built but not wired. `ApprovalGateStage` is generic and `audio_approval_gate()` exists, but only the text gate is inserted into the slice. | **Done (Phase 4.1).** The audio gate is wired between `synthesize` and `assemble`. The stage order is no longer a fixed constant: `canonical_stage_order(gates)` weaves `approve_text` after `ingest` and `approve_audio` after `synthesize` according to the run's gate set. `--require-audio-approval` is an independent opt-in (`storytime run` and `storytime ingest`); `--require-approval` keeps its Phase 4 text-only meaning, so a run may have neither, either, or both gates. `storytime approve <run> --stage audio --decision approve|reject` records the operator decision (an `approval` row with `stage_name="approve_audio"`). A run pauses after audio synthesis and before assembly; resume continues into `assemble`/`publish`; audio rejection moves the run to `failed` and blocks downstream stages; a duplicate audio approval fails cleanly. Migration `0003` adds `pipeline_run.gates` so a paused run's gate set survives the process-exit boundary and is known at resume. |
| OI-14 | Event taxonomy: ingest provenance approval and the operator text gate both emitted `TextApproved`, disambiguated only by `stage_name`. Phase 4 mediator ruling accepted this for Phase 4 but asked for a cleanup. | **Done (Phase 4.1).** Ingest now emits `SourceManifestApproved` (`EventType.SOURCE_MANIFEST_APPROVED`) for the manifest's rights-clearance/provenance approval. The interactive operator gate keeps `TextApproved` / `TextRejected`. The two concepts no longer share an event name, the `EventType` `StrEnum` stays closed (one additive member), and approval auditability is unchanged. Two Phase 3 assertions that counted the old name were updated (`tests/test_ingest_stage.py`, `tests/test_vertical_slice.py`). |
| OI-15 | `storytime clean` (retention policy — Architecture Baseline sections 4 and 18: `--older-than`, `--keep-published`, `--dry-run`) appears in the canonical CLI surface but is not implemented. | **Phase 7 carryover.** Surfaced during Phase 6S as the next functional gap once serving and multi-item publishing exist. Implement the retention sweep over `runs/` with `published_episode` awareness. |
| OI-16 | The OpenTelemetry Collector config had only a `traces` pipeline, so the Phase 5 metric instruments were emitted by the app but landed nowhere — no metrics backend existed. | **Done (Phase 6A).** `config/otel-collector.yaml` gains a `metrics` pipeline with a `prometheus` exporter (`add_metric_suffixes: false`, so series keep their exact declared names); `docker-compose.observability.yml` adds a Prometheus that scrapes the collector and a Grafana with provisioned datasources (Prometheus + Jaeger) and six provisioned dashboards. `tests/test_dashboards.py` enforces that every dashboard panel references only a real Phase 5 metric. |
| OI-17 | No blue/green deployment path existed. The Phase 5 telemetry-resource fields (`environment`, `deployment_slot`) were defined but unused: nothing scoped run/feed state to a slot, the slot was never set by any real deployment, and there was no deployment documentation. | **Done (Phase 7A).** Blue/green Option A — the lean, demo-shaped first deployment path. `deployment_slot` now scopes the default state and feed roots (`runs/<slot>`, `feed/<slot>`) so blue and green get independent SQLite databases and feeds; an explicit `STORYTIME_RUNS_DIR`/`STORYTIME_FEED_DIR` still overrides. The slot is validated as a safe path segment (no traversal). `storytime doctor` prints a deployment-identity banner; `config/deploy/blue.env` + `green.env` and `scripts/run-slot.sh` make the two slots runnable; `deployment.environment`/`deployment.slot` reach the OTel `Resource`. The app is deliberately **not** containerized (Architecture Baseline §16); the Option A deployment unit is an uncontainerized per-slot process. No automated traffic cutover — switching is an honest operator step. See `docs/deployment-bluegreen-option-a.md`. |
| OI-18 | Option A had no stable entry point: a consumer had to know which slot's port was live, and there was no explicit, persisted record of which slot was active. | **Done (Phase 7B).** Blue/green Option B — a higher-assurance front door over the Phase 7A slots. A native Python, loopback-only reverse proxy (`storytime.frontdoor`, standard library only — deliberately not an external Caddy/nginx binary, so the front door stays zero-dependency and fully testable in the normal suite) binds one stable port (default `127.0.0.1:8080`) and, on every request, routes to the slot named by a persisted active-slot pointer (`config/deploy/active-slot`). The pointer accepts only safe slot names (the same `[a-z0-9][a-z0-9._-]*` rule as Phase 7A; traversal/unsafe values rejected) and is the documented single source of truth. `switch_active_slot` provides a scripted switch — and rollback is the identical mechanism targeting the previous slot — writing only the pointer, never touching `runs/`/`feed/`. `scripts/run-frontdoor.sh` and `scripts/switch-slot.sh` are the launchers; `python -m storytime.frontdoor` exposes `serve`/`switch`/`status`. The front door is outside the pipeline telemetry path and imports no `opentelemetry` (import-linter contract extended to cover it). The app remains uncontainerized (Architecture Baseline §16 unamended; a doc note records that future containerization needs an explicit amendment). See `docs/deployment-bluegreen-option-b.md`. |
| OI-19 | The app was uncontainerized: Architecture Baseline §16 noted that any application containerization would require an explicit, user-approved amendment, and no such amendment existed. | **Done (Phase 7C / 7C.1 amendment + Phase 7C.1 / 7D implementation).** Phase 7C authored an Architecture Baseline §16 amendment; Gemini reviewed it (SAFE WITH EDITS), Phase 7C.1 applied the four required edits, and the amendment was **locked** with user approval. The implementation round delivered **optional, local, single-host, demo-grade** app containerization: an application `Dockerfile` (pinned base, non-root user, frozen `uv.lock` install, `ffmpeg`), a `.dockerignore` (excludes `runs/`, `feed/`, `.env`, secret patterns, caches), and an optional `docker-compose.app.yml` running the blue and green slots from one image. Each slot's SQLite state and feed sit on per-slot **named Docker volumes** (host bind mounts of the state DB prohibited); the compose uses `network_mode: host` so each slot binds `127.0.0.1` itself with §15 `validate_bind_host` unchanged (no `0.0.0.0` bind anywhere); `service.instance.id` is pinned to a stable slot-derived value (`storytime-<slot>`) identical bare-metal and containerized, with OpenTelemetry Docker/host/process resource detectors banned. Bare-metal local Python remains the default; the six gates stay Docker-free. The Phase 7B front door stays a host process. No cloud, registry publishing, Kubernetes, Terraform, CI/CD, or vendor fan-out is introduced. Per the Phase Closure Protocol the implementation is output only, not phase completion. See `docs/deployment-containerized.md`. |
| OI-20 | The documented `docker compose -f docker-compose.app.yml build` failed: both `storytime-blue` and `storytime-green` declared `build:` and exported the same `storytime-app:local` tag, so a parallel build raced on the image export (`image "storytime-app:local": already exists`). A single-service build workaround was needed. | **Done (Phase 7D.1 — operational cleanup).** `docker-compose.app.yml` now has exactly one builder: `storytime-blue` owns the sole `build:` section and exports `storytime-app:local`; `storytime-green` has no `build:` section, runs the same image, and is marked `pull_policy: never` so a fresh-cache `up -d` does not attempt to pull the local-only tag from a registry. `docker compose build` and `docker compose up -d` (including on an empty cache) both work without per-service targeting. The runtime architecture is unchanged — one shared image, `network_mode: host`, per-slot ports/volumes, host front door. Five regression tests in `tests/test_containerization.py` lock the build contract. |
| OI-21 | The Phase 8B Loki image tag (`grafana/loki:3.3.2`) and the new `config/loki.yaml` are pinned but unverified in the build environment. | Docker was unavailable in the Phase 8B build environment, so the Loki image tag and `config/loki.yaml` could not be exercised there — exactly parallel to OI-3 for the other observability images. Re-verify on a machine with Docker: `docker compose -f docker-compose.observability.yml pull` then `... config`, then bring the stack up and confirm Loki ingests the demo log via the Collector `filelog` → `otlphttp` path. The StoryTime test suite never requires the stack (332 static/offline tests pass), so this does not block any phase gate. |
| OI-22 | The Phase 8C optional vendor export profiles — the `docker-compose.vendor.dynatrace.yml` / `docker-compose.vendor.newrelic.yml` override merges and live telemetry export to Dynatrace / New Relic — are unverified in the build environment. | Docker was unavailable in the Phase 8C / 8C.1 build environment, so the Compose override merges (`-f docker-compose.observability.yml -f docker-compose.vendor.dynatrace.yml config`, and likewise for New Relic) and live vendor export could not be exercised — parallel to OI-3 and OI-21. The Phase 8C deliverable is config + docs + static governance tests, all of which pass offline; the static tests confirm each vendor config/override is well-formed, opt-in, secret-free, resilient, and single-vendor, but not that a real vendor endpoint accepts the data. Re-verify on a machine with Docker: render each merged config with `docker compose ... config`, create `config/vendor.secret.env` from the template with real values, bring the stack up with the base file plus one vendor override, and confirm the vendor backend ingests telemetry. The StoryTime test suite never requires the stack, so this does not block any phase gate. |

## Carryover backlog

Phase 4 closed OI-9 (interactive approval gate), OI-10 (resume/rehydration),
and OI-12 (real per-stage CLI commands). Phase 4.1 closed OI-13 (audio
approval gate wiring) and OI-14 (event-taxonomy cleanup). Phase 5 closed OI-2
(W3C `traceparent` propagation and linked traces — genuine implementation).
Phase 6S closed OI-7 (range-capable HTTP server) and OI-11 (multi-item RSS
feed aggregation). Phase 6A closed OI-16 (the collector had no metrics
pipeline). Phase 6B was documentation-only — it produced the SLO/SLI model,
runbook, dashboard guide, demo walkthrough, and portfolio notes; it closed no
OI and opened none. Phase 7A closed OI-17 (blue/green Option A deployment
path). Phase 7B (this round) closed OI-18 (blue/green Option B — the
front-door / active-slot switching path). The live backlog now is:

- **OI-15** — `storytime clean` (retention policy, Architecture Baseline
  sections 4 and 18) is defined in the canonical CLI surface but not yet
  implemented. It is a *retention* feature, distinct from blue/green
  deployment, so neither Phase 7A nor Phase 7B addressed it; it remains the
  standing functional carryover.

OI-3 and OI-5 are unscheduled: OI-3 is an environment re-verification step,
and OI-5 is optional file-config support to be picked up only if wanted.

Phase 7B is complete as implementation output (blue/green Option B — front
door + active-slot switching). What remains deferred beyond the Option A/B
deployment track: automated / health-gated promotion, app containerization (a
versioned image — would require an explicit Architecture Baseline §16
amendment), multi-host / HA, production auth, active alerting and an
error-budget policy, and (if a hosted backend is ever adopted) vendor
telemetry fan-out. None of that is built in Phase 7A or 7B; see
`docs/deployment-bluegreen-option-b.md` §8. OI-15 (`storytime clean`) remains
the standing functional carryover independent of the deployment track.

**Phase 7C / 7C.1 update.** Of the deferred items above, app containerization
is no longer "would require an amendment": the Architecture Baseline §16
amendment was authored (Phase 7C), reviewed, revised, and **locked** (Phase
7C.1), and the optional local containerization layer was implemented (Phase
7C.1 / 7D — closing OI-19). The amendment is deliberately narrow — optional,
local, single-host, demo-grade only. The following remain explicitly **not
authorized** and would each need their own amendment or phase:

- **Phase 8 — multi-backend telemetry fan-out.** Recorded direction: a local
  stack (OTel Collector, Prometheus, Loki, Jaeger, Grafana) and a vendor
  priority of Dynatrace (primary), New Relic (secondary), Datadog (deferred).
  Must stay optional, disabled by default, Collector-owned, with no vendor SDK
  in application code. Not implemented in Phase 7C.1.
- **Optional future front-door containerization** — the Phase 7B front door
  stays a host process for now; containerizing it is a possible future step,
  not authorized here.
- **Future cloud deployment** — not authorized.
- **Future image-registry / image-promotion path** — not authorized; the
  image is local-daemon only and is never pushed.
- **Future Postgres migration** — not authorized; SQLite remains the source
  of truth.
- **Future production-grade blue/green state convergence or database
  migration strategy** — not authorized; blue/green state stays strictly
  isolated with no automated cross-slot migration.

None of these carryovers is resolved by the Phase 7C.1 implementation.

**Phase 7 complete update (2026-05-24).** Phase 7 is now complete: Phase 7D
(Optional Local App Containerization) and Phase 7D.1 (Operational Cleanup —
Compose Build Race Fix) are locked, the latter confirmed by a live Docker
smoke test on Windows Docker Desktop / WSL2. **OI-20** (the parallel
`docker compose build` image-tag race) is closed — see its row above.

The live open-issue backlog is unchanged by Phase 7 completion: **OI-15**
(`storytime clean` retention policy) remains the standing functional
carryover; **OI-3** (observability-image re-verification) and **OI-5**
(optional TOML file config) remain unscheduled.

**Phase 8 — Multi-Backend Telemetry Fan-Out — is the next planned phase, not
an open issue.** It is planned, scoped future work (see `docs/roadmap.md`), not
an unresolved bug, and it does not block anything currently locked.

**Phase 8A update (2026-05-24).** Phase 8 has begun. Phase 8A authored the
Architecture Baseline amendment (`docs/architecture-baseline.md` Section 23 —
Collector-owned multi-backend telemetry fan-out governance) and accepted the
Phase 8A / 8B / 8C split. The amendment candidate completed the Phase Closure
Protocol — Opus authored it, GPT-5.5 reviewed (clean), Gemini returned
`SAFE TO LOCK`, the user approved — and **Section 23 is locked and canonical**.
Phase 8A opened and closed no OI: it is an architecture/documentation
amendment round that changed no application code, telemetry, configuration, or
tests. The live backlog is unchanged — **OI-15** (`storytime clean` retention
policy) remains the standing functional carryover; **OI-3** and **OI-5**
remain unscheduled. Phase 8B (local multi-backend stack expansion) is the next
implementation phase; Phase 8C (optional vendor export profiles) follows.

**Phase 8B.1 update (2026-05-24).** After GPT-5.5 review and Gemini critique
returned `SAFE WITH MINOR CLEANUP` for Phase 8B, Phase 8B.1 applied that narrow
operational cleanup — a `./logs` directory preflight (Makefile `logs-dir` /
`observability-up` / `demo` targets plus doc updates) so the Collector
bind-mount cannot leave the directory root-owned and unwritable by the local
demo. Phase 8B.1 **opened and closed no issue**. **OI-21** is unaffected and
still open: it tracks live Docker verification of the Loki image tag,
`config/loki.yaml`, and the `filelog → otlphttp → Loki` path — the preflight
cleanup does not change that the stack itself is still unverified in a
Docker-less environment. The backlog is unchanged: **OI-15** active; **OI-3**,
**OI-5**, **OI-21** unscheduled; none block any phase gate (the 346-test suite
is fully offline).

**Phase 8C lock (2026-05-24).** Phase 8A, 8B / 8B.1, and **Phase 8C — Optional
Vendor Export Profiles — with the Phase 8C.1 cleanup are all locked**, locked
with explicit user approval (Gemini verdict `SAFE TO LOCK`). Phase 8C added
disabled-by-default Dynatrace and New Relic export profiles; the Phase 8C.1
cleanup split the single combined override into two independent, mutually
exclusive `docker-compose.vendor.dynatrace.yml` / `docker-compose.vendor.newrelic.yml`
overrides, each with its own `config/vendor/otel-collector.*.example.yaml`,
governed by the locked Section 23. **Phase 8 — Multi-Backend Telemetry Fan-Out
— is complete.** Phase 8C opened **OI-22** (the override merges and live vendor
export are unverified without Docker — parallel to OI-3 / OI-21) and closed no
issue; OI-22 remains open and was not a lock prerequisite. The backlog:
**OI-15** active (standing functional carryover); **OI-3**, **OI-5**,
**OI-21**, **OI-22** unscheduled environment/optional items; none block any
phase gate (the 358-test suite is fully offline).

**Phase 9A — Governance Baseline Amendment is locked** (2026-05-24).
`docs/architecture-baseline.md` Section 24 is canonical. **Phase 9B — Minimal
Trust Envelope Implementation is locked** (2026-05-24), with the **Phase 9B.1
forbidden-term-scanner hardening cleanup folded into the lock**. Phase 9B added
the `storytime.governance` package, the durable Trust Envelope artifact, the
`trust_envelope` SQLite projection (schema migration `0005`), the fail-closed
gate, the `config/governance/blocked-sources.yaml` deny-list, and the static
legal-hallucination grep/regex gate; Phase 9B.1 hardened that scanner against
binary/generated files. **Phase 9B and Phase 9B.1 opened no open issue and
closed none** — the backlog is unchanged: **OI-15** active; **OI-3**, **OI-5**,
**OI-21**, **OI-22** unscheduled; none block any phase gate. Phase 9B promoted
`pyyaml` from a dev-only to a runtime dependency (the §24.9 blocked-source
config is YAML) and re-locked `uv.lock`; no other dependency changed and no
secret was added. The full test suite is **418 tests, fully offline**. The next
phase is **Phase 10 — Product UI / Operator Experience**, not started. Phase 9C
— Docs / Audit Polish — was an optional follow-up and is not scheduled.

**Phase 10A — Operator Experience Baseline Amendment (locked) — 2026-05-24.**
Phase 10A authored and locked an Architecture Baseline amendment —
`docs/architecture-baseline.md` Section 25, "Operator Experience Baseline" —
defining the Phase 10 operator-experience law and the Phase 10B handoff
specification. It is architecture/documentation only and authorizes no
implementation; it is **locked** and awaits GPT-5.5 review, Gemini
critique, and explicit user approval. **Phase 10A opened no open issue and
closed none** — the backlog is unchanged: **OI-15** active (standing functional
carryover); **OI-3**, **OI-5**, **OI-21**, **OI-22** unscheduled
environment/optional items; none block any phase gate. No application code,
database schema, artifact envelope code, Trust Envelope semantics, governance
gate behaviour, telemetry behaviour, configuration behaviour, test, or
dependency changed; no secret was added. The full test suite is **418 tests,
fully offline**. The first likely implementation phase is **Phase 10B —
Generated Local HTML Operator Report**, not started; Phase 10C and Phase 10D
remain future, conditional, and not started.

**Phase 10B — Generated Local HTML Operator Report (implementation candidate)
— 2026-05-24.** Phase 10B implemented the locked Section 25 operator-experience
law as the new `storytime.reporting` package and the `storytime report
generate` CLI command — a generated, static, local, read-only HTML operator
report. It is implementation output, pending GPT-5.5 review, Gemini critique,
any cleanup, and explicit user lock. **Phase 10B opened no open issue and
closed none** — the backlog is unchanged: **OI-15** active (standing functional
carryover); **OI-3**, **OI-5**, **OI-21**, **OI-22** unscheduled
environment/optional items; none block any phase gate. Phase 10B made no
database schema change, changed no ARCH-LOCKed contract, and added no
dependency; the suite is **437 tests (19 new), fully offline**, and all six
Docker-free gates pass. One **documented, non-blocking limitation** is recorded
(not opened as an OI): the SQLite projections record a per-episode audio path
but not a per-run RSS feed path — the RSS feed is the single shared
`feed/feed.xml`. The report surfaces the audio path and references the shared
feed for a run that published; a per-run feed path would require a schema
change Phase 10B deliberately does not make. If a future phase wants a per-run
feed reference, it can be scoped then; until then this is an accepted,
documented design boundary, not a bug.

**Phase 10C — Operator CLI Helpers / Failure Queue — LOCKED (2026-05-25).**
Phase 10C locked the `storytime.operator_queue` module and the read-only
`storytime queue` CLI command — a bounded, deterministic command-line failure /
review queue. Locked artifact SHA-256:
`e30aaa57f900756e62347ddaac2df658d96065c9e1061679adb31594c73e2543`. **Phase 10C opened no open issue and closed none** — the backlog is unchanged: **OI-15** active (standing functional
carryover); **OI-3**, **OI-5**, **OI-21**, **OI-22** unscheduled
environment/optional items; none block any phase gate. Phase 10C made no
database schema change, changed no ARCH-LOCKed contract, and added no
dependency; the suite is **466 tests (29 new), fully offline**, and all six Docker-free
gates pass. One **documented, non-blocking design boundary** is
recorded (not opened as an OI): the queue's attention model is derived purely
from existing authoritative state — run status, the presence of a structured
stage `error_kind`, and the Trust Envelope governance decision. The state model
has no dedicated per-run "blocked" or "needs-review" *run status* — those
attention reasons are derived from the Trust Envelope decision enum
(`BLOCKED` / `NEEDS_REVIEW`). This is the supportable, schema-faithful design;
inventing new run states would require a schema change Phase 10C deliberately
does not make.


**Future consideration (non-blocking):** If blocked-source projections grow to thousands of entries, the operator queue query/projection may need indexing, pagination, or a more explicit bounded strategy. This is not a Phase 10C blocker and requires no immediate code work.

**Phase 10D — Pipeline Re-Run / Mutation Actions — implementation candidate
(2026-05-25); pending review; not locked.** Phase 10D adds StoryTime's first
operator *mutation* surface: the `storytime.operator_rerun` module and the
governed `storytime rerun` CLI command. **Phase 10D opened no open issue and
closed none** — the backlog is unchanged: **OI-15** active; **OI-3**,
**OI-5**, **OI-21**, **OI-22** unscheduled; none block any phase gate. Phase
10D made no database schema change, changed no ARCH-LOCKed contract, and added
no dependency; the suite is **493 tests (27 new), fully offline**, and all six
Docker-free gates pass. One **documented, non-blocking design boundary** is
recorded (not opened as an OI): Phase 10D re-runs a failed run from the stage
it failed at; re-running from an arbitrary *earlier* stage — which would
require invalidating already-completed stage executions — is intentionally
out of scope for Phase 10D. `--from-stage` therefore accepts only the run's
failed stage, as an explicit operator confirmation. A later phase could add
earlier-stage re-run if a real operator need is shown; this is a deliberate
scope boundary, not a defect.

**Phase 10E — Static HTML Operator Report Refinement — locked (2026-05-25)**,
with the Phase 10E.1 / 10E.2 cleanup sequence accepted. Phase 10E opened no
open issue and closed none.

**Phase 10F — Demo Seed Data / Golden Path Fixtures — implementation
candidate (2026-05-25); pending review; not locked.** Phase 10F adds curated
demo seed data and golden-path fixtures, the `docs/demo.md` operator runbook,
and `tests/test_demo_fixtures.py`. **Phase 10F opened no open issue and closed
none** — the backlog is unchanged: **OI-15** active; **OI-3**, **OI-5**,
**OI-21**, **OI-22** unscheduled; none block any phase gate. Phase 10F made no
database schema change, changed no ARCH-LOCKed contract, and added no
dependency; the suite is **549 tests (37 new), fully offline**, and all six
Docker-free gates pass. One **documented, non-blocking limitation** is recorded
(not opened as an OI): a governance Trust Envelope `NEEDS_REVIEW` decision is
not reachable through the normal local manifest path — the closed manifest
licence enum maps only to `APPROVED` — so the needs-review fixture uses the
operator text approval gate and documents the limitation rather than inventing
a workflow.

Phase 6S implementation notes carried forward (not blockers):

- The range server is HTTP/1.0 (one request per connection,
  Content-Length-delimited bodies). That is correct and sufficient for a local
  podcast client; HTTP/1.1 keep-alive / chunked encoding is a **low-priority
  future** enhancement, not a requirement.
- Multi-item feed order is newest-publication-first with no pagination. A feed
  with a very large back catalogue would grow `feed.xml` unboundedly; a future
  phase may cap the item count or add an archive feed. Not an MVP concern.
- **True RSS item update / re-publish semantics is a post-MVP carryover.**
  Phase 6S `publish` aggregates prior episodes and re-renders the whole feed,
  but it treats each publish as a new episode prepended to the catalogue. It
  does not yet model *updating* an already-published item in place (correcting
  a description, replacing audio, or re-issuing a GUID). Genuine update /
  re-publish semantics — including how GUID stability and `<pubDate>` interact
  with a correction — is deferred to a future phase; it is not an MVP
  requirement and not a Phase 6A/6B concern.

Phase 6A carryover — addressed by Phase 6B (documentation):

- The SLO / SLI model is now `docs/slo-sli.md`: SLIs derived strictly from the
  eight real metrics, an illustrative demo-grade SLO model, and an explicit
  account of what cannot be measured yet.
- `docs/observability-demo.md` is now the full demo walkthrough (it superseded
  the short 6A guide); `docs/runbook.md` is the operator runbook;
  `docs/dashboard-guide.md` is the per-panel interpretation guide;
  `docs/portfolio-notes.md` is the SE/portfolio narrative.
- The ffmpeg-missing scenario remains a deliberate harness skip; Phase 6B did
  not change it. Demonstrating it still requires a host without ffmpeg.
- No RSS-publish-health or TTS/audio dashboard exists: the eight Phase 5
  metrics contain nothing TTS- or RSS-specific. Phase 6B documents *why* this
  is deferred (`docs/slo-sli.md` §4) rather than inventing metrics; such
  dashboards need new instruments from a future telemetry phase.
