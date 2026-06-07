> **Public demo (Phase 15C — current candidate; NOT locked):** a cloud-hosted **static** operator console of this local-first, observability-native pipeline and its cloud-readiness seams. It is read-only and demo-data-backed; no backend runs behind it, and nothing is deployed to the cloud except static files. See `DEMO.md` for the public link, build/deploy steps, and a two-minute talk track, and `docs/phase15c-minimal-cloud-demo.md` for the full design. Phase 15A and 15B are LOCKED; Phase 15C is the current candidate (pending review, NOT locked); Phase 15D, Phase 15E, and Phase 15F are NOT STARTED.

> **Phase 14D — Cloud / Distributed Architecture Baseline from Proven Local Contracts (LOCKED).** Phase 13 is CLOSED; **Phase 14A.1, 14B.1, 14C.1, 14C.2, 14C.3, 14C.4, 14C.5.1, and 14D are LOCKED** (14D is the last locked phase; 14D locked via `storytime-phase14d-cloud-distributed-architecture-baseline.tar.gz`, SHA-256 `a4ccc8aa59beaf6365081973d1c3d78235df028ef0f3214979e9d3b98f4dcce6`; 14C.5.1 locked via `storytime-phase14c5-1-durable-recovery-control-plane-boundary.tar.gz`, SHA-256 `73a9ee1bdcbca295037f4852375d3f6b1ff155c3a0ea9d1b0fe498de3862e604`). Phase 14 — Live System / Cloud-Distributed — is STARTED. Phase 14D is a documentation-and-mapping round only: it takes the proven, LOCKED local contracts (request acceptance, the durable `WorkQueue` port, the `LocalWorker`, the `ArtifactStore` port, the durable `recovery_action` control plane, in-process observation, and the operator read-model) and records, on paper, the shape each would take in a future cloud / distributed deployment, as the readiness basis for a possible later Phase 15. It implements no cloud behavior of any kind: no external broker, no Redis/NATS/SQS/Temporal/Celery, no Kubernetes, no Terraform, no object storage, no S3/MinIO, no signed URLs, no distributed worker, no authentication, no provider TTS, no audio, no RSS, and no new dependency; it changes no backend, frontend, bridge, queue/worker, recovery, artifact-store, or observation behavior. The previously sketched provider-TTS / frontend-audio / RSS content-production items (formerly the 14D.1–14D.4 labels) are now **deferred future work**, not part of Phase 14D. Phase 14E (Local Release Candidate / Full Local Mode Closure) and Phase 15 (Cloud / Distributed Runtime) remain **NOT STARTED**.

> **Phase 14C.5.1 — Durable Recovery Control Plane Boundary (historical — now LOCKED; see the Phase 14D banner above for current state).** Phase 13 is CLOSED; **Phase 14A.1, 14B.1, 14C.1, 14C.2, 14C.3, and 14C.4 are LOCKED** (14C.4 is the last locked phase; locked via `storytime-phase14c4-minimal-observability-boundary-queue-worker.tar.gz`, SHA-256 `12b951e0a9b6b17f5c73aacf0d055b257bd4a715908f7f5078d401eae2a66d3b`). Phase 14 — Live System / Cloud-Distributed — is STARTED. Phase 14C.5.1 adds the smallest durable, backend-owned recovery control plane: a durable `recovery_action` lineage table (source of truth) linking an original failed execution to a bounded recovery execution, a backend-owned recovery eligibility policy, duplicate-prevention and a bounded attempt limit, a recovery read-model projection, local SQLite concurrency guardrails, and a cloud-queue mapping CONTRACT document. The Phase 14C.4 observer events are explanatory only and are NOT the recovery-lineage source of truth. It does not expand the Phase 14C.4 observer event schema and changes no queue/worker or ArtifactStore semantics. It absorbs the previously planned Phase 14C.5 through Phase 14C.10 local recovery-control-plane scope (historical labels only). No cloud queue, external broker, dead-letter queue, automatic retries, exponential backoff, retry scheduler, distributed worker, cloud lease, distributed lock, cloud object store, provider TTS, audio, RSS, or auth exists yet. Phase 14D / 14E remain **NOT STARTED**.

> **Phase 14C.4 — Minimal Observability Boundary for Queue/Worker (historical — now LOCKED; see the Phase 14C.5.1 banner above for current state).** Phase 13 is CLOSED; **Phase 14A.1, 14B.1, 14C.1, 14C.2, and 14C.3 are LOCKED** (14C.3 is the last locked phase). Phase 14 — Live System / Cloud-Distributed — is STARTED. Phase 14C.4 adds a small backend-owned, in-process observation boundary for the local queue/worker lifecycle: safe, vendor-neutral event names (`work.enqueued/claimed/started`, `stage.started/completed`, `artifact.recorded`, `work.completed/failed`) and safe fields (existing local identifiers, timestamps, status), emitted fail-soft at the existing lifecycle points. It changes no queue/worker or ArtifactStore semantics and adds no dependency. It is **not** a telemetry platform: no OpenTelemetry SDK, no collector, no Prometheus endpoint, no Grafana dashboards, no vendor exporters, no alerting, no SLOs, no sampling, no distributed tracing, no cloud telemetry, and no retry/recovery lineage. Phase 14C.5 / 14D / 14E remain **NOT STARTED**.

> **Phase 14C.3 — Object Storage Boundary / Artifact Store Adapter (historical — now LOCKED; see the Phase 14C.4 banner above for current state).** Phase 13 is CLOSED; **Phase 14A.1, 14B.1, 14C.1, and 14C.2 are LOCKED** (14C.2 is the last locked phase). Phase 14 — Live System / Cloud-Distributed — is STARTED. Phase 14C.3 puts artifact handling behind a backend-owned `ArtifactStore` port with a single LOCAL filesystem adapter (`LocalFilesystemArtifactStore`): it validates logical keys (rejecting absolute paths, `..` traversal, backslash separators, and symlink escapes), keeps artifacts under a configured root, and returns safe artifact evidence only, so the browser never learns filesystem paths or storage credentials. It changes no queue/worker semantics and adds no dependency. It is **not** cloud storage, **not** S3, **not** MinIO, and **not** public artifact serving; no cloud adapter, external object store, signed URLs, auth, retry/recovery lineage, or observability deepening exists yet. Phase 14C.4 / 14D / 14E remain **NOT STARTED**.

> **Phase 14C.2 — Contracts-as-Built / Cloud-Distributed Seam Baseline (historical — now LOCKED; see the Phase 14C.3 banner above for current state).** Phase 13 is CLOSED; **Phase 14A.1, 14B.1, and 14C.1 are LOCKED** (14C.1 is the last locked phase). Phase 14 — Live System / Cloud-Distributed — is STARTED. Phase 14C.2 is a documentation / contracts / guardrail round: it documents the seams Phase 14C.1 actually built (request acceptance, the queue port, the SQLite adapter, worker execution, stale-claim and stale-partial recovery, read-model/DTO safety, the frontend boundary) in `docs/phase14-contracts-as-built.md`, and defines the cloud/distributed seam baseline for future phases. It changes no runtime behavior and adds no dependency. It is **not** cloud/distributed implementation: not a cloud queue, not an external broker, not object storage, not an auth boundary, not a retry/recovery lineage, and it describes local no-double-execution under the tested SQLite/local-worker model rather than exactly-once semantics across a distributed system. Phase 14C.3 / 14D / 14E remain **NOT STARTED**.

> **Phase 14C.1 — Local Durable Queue / Worker Shape Proof (historical — now LOCKED; see the Phase 14C.2 banner above for current state).** Phase 13 is CLOSED; **Phase 14A.1 and 14B.1 are LOCKED** (14B.1 is the last locked phase). Phase 14 — Live System / Cloud-Distributed — is STARTED. Phase 14C.1 builds on the locked Phase 14B.1 proof loop and proves the local durable execution spine: a proof-run request reserves a run and enqueues a durable work item (a local work-queue port with a SQLite adapter), and a single bounded local worker claims and executes it — separating request acceptance from execution, with atomic claiming, lease-based stale-claim recovery, and no double execution. It adds no new dependency. It is a LOCAL queue/worker shape proof: not a cloud queue, not a distributed system, no external broker; and adds no provider TTS, audio playback, RSS publishing, authentication, or cloud deployment. Phase 14C.2 / 14D / 14E remain **NOT STARTED**.

> **Phase 14B.1 — Live Proof Loop Hardening / Operator Trust (historical — now LOCKED; see the Phase 14C.1 banner above for current state).**
>
> **Phase 13 is CLOSED** and **Phase 14A.1 — Local Live Proof Loop Before Cloud — is LOCKED** (the last locked phase). **Phase 14 — Live System / Cloud-Distributed — is STARTED.** Phase 14B.1 builds on the locked Phase 14A.1 proof loop and makes it harder to dismiss: it adds controlled, deterministic, **durable failure/recovery proof scenarios** (a `governance_failure` and an `artifact_validation_failure` alongside the existing `success`) so a reviewer can see StoryTime produce intelligible failure evidence, not only a green run; plus operator-UX and read-model/DTO hardening, Windows operator docs, and cloud-ready boundary docs. It adds no new dependency. The reserved future combined bundle (cloud/distributed, provider-backed TTS, frontend audio, audio playback, RSS, auth) is renamed **Phase 14C.1+** and is **NOT STARTED**.
>
> **Run the local live proof loop**
>
> Terminal 1 (backend, loopback only):
> ```bash
> uv sync --frozen --extra dev
> uv run storytime local-live          # serves http://127.0.0.1:8770
> ```
> Terminal 2 (frontend dev server):
> ```bash
> cd frontend
> npm install
> npm run dev                          # serves http://localhost:5173
> ```
> On **Windows PowerShell**, use the same commands from `C:\Users\<you>\Desktop\storytime` (and `...\storytime\frontend` in terminal 2); see **Windows operator quickstart** below for troubleshooting.
>
> Then open http://localhost:5173, go to **Live Proof Loop**, confirm backend health, then click **Run success scenario** and inspect the run's stages / artifacts / events. As of Phase 14C.1 the request **enqueues** a durable work item (the run starts `queued`) and a single bounded **local worker** drains it (`queued → running → completed/failed`) — request acceptance is separated from execution. Next click **Run governance-failure scenario** (and **Run artifact-validation-failure scenario**): each produces a durable **failed** run with a clear failure-reason panel and a marked failed stage. Restart `storytime local-live` and confirm the prior runs — success *and* failure — are still listed. The backend owns truth and durable state; the browser only requests, and can trigger only allowlisted scenarios (no arbitrary input). The API binds loopback only with a strict origin allowlist (no wildcard CORS). This is a LOCAL queue/worker shape — not a cloud queue or distributed system. See `docs/phase14-queue-worker.md`, `docs/phase14-proof-loop.md`, and `docs/phase14-cloud-distributed-roadmap.md`.

> **Phase 13L note — Phase 13 Closure / Demo-Local Completion Lock (current sub-phase).**
>
> **Lock lineage:** Phase 13A–13F LOCKED · Phase 13D.1 / 13D.2 LOCKED · Phase 13G LOCKED · Phase 13G.1 LOCKED · Phase 13H LOCKED · Phase 13H.1 LOCKED · Phase 13H.2 LOCKED · Phase 13H.3 LOCKED · Phase 13I LOCKED · Phase 13J LOCKED · Phase 13K LOCKED (Demo Walkthrough Refresh / Governed Local Chain Story Path). Phase 13K is the last locked phase.
> **This sub-phase:** Phase 13L — Phase 13 Closure / Demo-Local Completion Lock — implementation candidate; pending review; NOT locked. It is a closure / documentation round: it records Phase 13K as locked, prepares the Phase 13 closure as a candidate, summarizes the Demo + Local proof track, preserves `docs/demo-walkthrough.md` as the canonical reviewer path, and writes an architecture-first readiness handoff for the next, not-yet-started Phase 14 (`docs/phase14-readiness-handoff.md`). It adds no runtime capability and changes no source, frontend, or dependency.
> **Closure framing:** Like the Phase 12D closure round before it, Phase 13L only *prepares* the Phase 13 closure. Phase 13 closure is a candidate that is not yet externally locked; Phase 13 will be formally closed only after Phase 13L review/lock. Until then Phase 13 remains STARTED and is not closed.
> **Phase 14 (next, not started):** Phase 14 — Cloud/Distributed — has not started. Phase 14A — Cloud/Distributed Architecture Baseline — is the next proposed architecture baseline and is NOT STARTED; Phase 13L does not implement, start, or design it in detail.
> **Invariants:** docs and tests only. No new backend behavior, no new local bridge action, no generate_tts, no frontend TTS generation, no audio playback, no provider integration, no browser durable storage, no polling / live sync, no cloud / distributed / full Local mode, no RSS publishing, no authentication, and no cloud deployment. The read-only bridge client stays GET-only; retry_failed_stage stays the only submittable action; the backend bridge (`src/storytime/local_bridge/`), the `src/storytime/tts_proof/` package, the committed static export contract, and the locked Phase 13J / 13K surfaces are untouched.
> **Honest framing (unchanged):** an accepted retry is shown as accepted, not succeeded; a manual reload is a read-model refresh, not a live sync; the browser is not durable; mock output is labeled mock, not real provider audio; the real provider stays deferred / disabled; full Local mode and Cloud/Distributed mode do not exist.
> **Deferred to future (Phase 14) work:** frontend TTS generation, a real provider adapter, audio playback, batch generation, RSS publishing, authentication, and cloud/distributed mode all remain deferred.

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

# Phase 13F implementation-candidate note — Local Bridge Architecture & Contract Baseline

**Round type:** Phase 13F — Local Bridge Architecture & Contract Baseline — a documentation-and-static-fixture architecture / contract baseline over the locked Phase 13E operator GUI (the architectural lock before any Python local-bridge implementation; to the Local Bridge what Phase 13A was to the operator GUI). No runtime code.
**Status:** Phase 13F is an **implementation candidate / pending review — NOT locked.**
**Last locked phase:** Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary (locked; SHA-256 `a997f2ca9d213e28e140f47c63336367c8feda46ed994b41300f86b99f8d8164`).

Phase 13F establishes that **the frontend is an operator surface, not the durable storage layer**: durable state must live outside the browser in an explicit external workspace / storage target with clear export, reset, backup, and recovery semantics, so StoryTime never repeats the RoundTable browser-storage failure mode. The browser may hold transient UI state only; `localStorage` / `sessionStorage` / `IndexedDB` remain forbidden. Phase 13F adds eleven new architecture / contract docs (`docs/local-bridge-architecture.md`, `docs/externalized-state-architecture.md`, `docs/browser-storage-policy.md`, `docs/local-mode-workspace-layout.md`, `docs/storage-targets-architecture.md`, `docs/action-execution-boundary.md`, `docs/local-action-dto-spec.md`, `docs/local-action-audit-spec.md`, `docs/local-mode-storage-contract.md`, `docs/local-action-queue-observability.md`, `docs/phase13f-local-bridge-contract-readiness.md`), a set of non-runtime JSON example fixtures under `docs/examples/` (labelled future / documentation-only), and one new Python test (`tests/test_local_mode_contract_examples.py`) validating those fixtures with plain Python (no JSON-schema dependency). It settles the future local-bridge execution-timing policy (async long-running actions; `202 Accepted` + `actionRequestId`/`jobId`; acceptance is not success; export refresh after a durable write), the loopback-only / strict-origin / no-arbitrary-command / command-pattern-router security boundary, the action allowlist (`retry_failed_stage`, `inspect_trust_envelope`, `refresh_export`) with higher-risk actions deferred, and the queue-observability model.

Phase 13F implements **NO** runtime code: no local bridge, no server, no async queue, no queue workers, no queue metrics / exporters, no OpenTelemetry, no storage providers, no provider integrations, no runtime schema validation, no router / history, no browser storage, no real Local mode, no Cloud/Distributed mode, and no mutation / action execution. The browser remains non-durable; the example fixtures are documentation artifacts only and never claim Phase 13F executed anything. Phase 13F does **not** modify `src/`, `frontend/src/`, `frontend/package.json`, `frontend/package-lock.json`, `pyproject.toml`, `uv.lock`, or `frontend/src/data/storytime-demo-export.json`; all are byte-identical to the locked Phase 13E source. The only allowed code changes are the narrow, explicitly-authorized mechanical advance of the state-discipline guard `tests/test_failure_mode_regression.py` and the new `tests/test_local_mode_contract_examples.py`. Per the Phase Closure Protocol, Phase 13F awaits GPT-5.5 review, Gemini critique, any cleanup, and explicit user approval; it does **not** lock Phase 13F, does **not** close Phase 13, and does **not** start Phase 13G. Phase 13G and every later Phase 13 subphase have **not** started.

---

# Phase 13E implementation-candidate note — Demo-Mode Action Preview / Operator Intent Boundary (historical — Phase 13E is LOCKED; see the Phase 13F note above)

**Round type:** Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary — a frontend-only, static, Demo-mode-only, non-consequential sub-round over the locked Phase 13D.2 operator GUI.
**Status:** Historical record. Phase 13E has since been **LOCKED** and is the last locked phase; Phase 13F is the current implementation candidate (see above).
**Last locked phase:** Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path.

Phase 13E turns the existing visibly-disabled future-action affordances
into explainable, non-executing **action previews** so the operator
GUI can demonstrate serious operator intent without becoming
consequential. The right framing is: *demo mode may preview serious
operator intent — demo mode must not create consequential changes.*
Phase 13E adds a static view-model adapter
(`frontend/src/data/actionPreviewAdapter.ts`) holding typed
action-preview definitions (stable id, label, category, current mode
(Demo), execution status (Preview only / non-consequential), target
object references for run id / stage id / governance decision id /
failure queue item / evidence artifact, target context label, what
the operator is trying to accomplish, why it is blocked in Demo mode,
precondition checklist, evidence to inspect first, risk level and
explanation, illustrative future Local-mode request shape labelled
"Future request shape — illustrative only, not executable in Demo
mode", Cloud/Distributed considerations, audit expectations, failure
behaviour expectation, what remains disabled, related view, optional
related run id) plus operating-mode model constants for Demo / Local
/ Cloud-Distributed; a new presentation component
(`frontend/src/components/ActionPreviewPanel.tsx` plus its CSS
Module) that maps over the adapter data and renders the selected
preview with the required safety / honesty labels ("Demo mode",
"Preview only", "No state changed", "Action plan, not action result",
"Execution requires future Local mode", "Cloud/Distributed execution
is not implemented", "No audit record generated because nothing
executed", "No local bridge is running", "No backend command was
called"); and light integration into the existing Failure /
Recovery, Governance / Safety, and Evidence / Validation views
**alongside** the existing `DisabledFutureActionCard` /
`DisabledFutureActionList` (which remains unchanged: a real
`<button disabled={true}>` with no `onClick`). A separate, clearly
labelled "Preview action plan" affordance opens an inline preview
panel via local `useState<ActionPreviewId | null>` (no router, no
Context, no persistence, no `localStorage`, no `sessionStorage`, no
URL or History API manipulation). The first set of previews covers
retry-failed-stage (target run `run-2026-0520-review`, stage
`run-2026-0520-review:governance-gate`), inspect-trust-envelope
(target run `run-2026-0520-review`, non-mutating inspection),
record-review-decision (target run `run-2026-0520-review`, related
disabled action `run-2026-0520-review:open-review`),
regenerate-operator-report (target evidence/report surface), and
refresh-export (target static export). Phase 13E introduces or
clarifies the eventual operating-mode model — Demo / Local /
Cloud-Distributed — distinct from the existing Demo / Active /
Candidate data-snapshot framing: only Demo mode is implemented;
Local mode and Cloud/Distributed mode remain future / not
implemented.

Phase 13E is static and Demo-mode-only: no server, no live API, no
`fetch`/`axios`/`localhost`/network call, no `localStorage` /
`sessionStorage`, no router / hash routing / browser History API, no
Context provider, no global preview/action state, no actual retry /
rerun / approval / report regeneration / export refresh, no
authentication, no Local mode, no Cloud/Distributed mode, no
audit-record generation (nothing executed), no production hosting,
no cloud deployment, no fake-execution surface, no Demo / Active /
Candidate snapshot switching, and no dynamic file loading. It does
**not** modify the backend export generator
(`src/storytime/operator_export.py`), the committed static export
JSON (`frontend/src/data/storytime-demo-export.json`), the
`storytime export-demo-ui` CLI contract, or
`src/storytime/cli/app.py`; all four protected files / contracts
are byte-identical to the Phase 13D.2 source. No `src/`,
`pyproject.toml`, `uv.lock`, `frontend/package.json`,
`frontend/package-lock.json`, or root dependency changed. The
`tests/` changes are the narrow, explicitly authorized mechanical
advance of the state-discipline guard
`tests/test_failure_mode_regression.py` to the Phase 13E
current-state expectations, and one new
`tests/test_action_preview_data_integrity.py` that asserts run-id
and other target ids referenced by the action-preview adapter
exist in the committed static export.

Per the Phase Closure Protocol, Phase 13E is an implementation
candidate, pending review, **not locked**; it does not lock Phase
13E, does not close Phase 13, and does not start Phase 13F. Phase
13F and every later Phase 13 subphase have **not** started.

*(The Phase 13D.2-era note below is a historical record. Phase
13D.2 is LOCKED; Phase 13E is the current implementation candidate.)*

---
# Phase 13D.2 implementation-candidate note — Static Demo Walkthrough / Reviewer Story Path (historical record — Phase 13D.2 is LOCKED; see the Phase 13E note above)

**Round type:** Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path — a frontend-only static / read-only demo-readiness sub-round over the locked Phase 13D.1 operator GUI.
**Status:** Historical record. Phase 13D.2 has since been **LOCKED** and is the last locked phase; Phase 13E is now the current implementation candidate — see the Phase 13E note above.
**Last locked phase:** Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline.

Phase 13D.2 replaces the honest Demo Walkthrough placeholder with a real
read-only guided reviewer / demo path view
(`frontend/src/components/DemoWalkthroughView.tsx` plus its CSS Module)
backed by a static view-model adapter
(`frontend/src/data/demoWalkthroughAdapter.ts`) that holds the long-form
route content. The view offers four reviewer routes — a 5-minute scan,
a 10-minute SE-style demo, a technical deep-dive, and a self-guided
reviewer path — switched by a simple segmented control backed by local
`useState<RouteId>` (no router, no Context, no persistence). Each step
carries title, target view, what to inspect, what it proves, talking
points, and an in-line navigation affordance into the relevant existing
view; steps that point to a specific run identify it by stable id
(`run-2026-0518-golden` for the golden-path run; `run-2026-0520-review`
for the review-required run). The view also includes
architecture-checkpoint cards covering local-first design, deterministic
static export, backend owns truth / frontend owns understanding,
read-only operator surface, static evidence boundary, disabled-action
boundary, Demo / Active / Candidate as data snapshots not deployment
environments, and why Phase 13E must be explicitly gated; a deliberate
"what is intentionally deferred" section; and interview / SE
talking-point callout cards. Phase 13D.2 absorbs ~80–90% of an
Architecture Story narrative via these embedded checkpoints but does
NOT implement a full standalone Architecture Story page — that stays
deferred and is tracked in `docs/frontend-gui-deferred-work-register.md`.
`frontend/src/navigation.ts` was updated so Demo Walkthrough is a real
view (the remaining placeholders — Architecture Story, Roadmap,
Settings / Config — still point to Phase 13E or later). `App.tsx` was
lightly updated to render the new view and pass navigation callbacks
down; it still uses plain `useState` with no router. Phase 13D.2 is
static and read-only: no server, no live API, no
`fetch`/`axios`/`localhost`/network call, no mutation, no
authentication, no cloud deployment, no production hosting, no
dynamic file loading, and no Demo / Active / Candidate switching. It
does **not** modify the backend export generator
(`src/storytime/operator_export.py`), the committed static export
JSON (`frontend/src/data/storytime-demo-export.json`), the `storytime
export-demo-ui` CLI contract, or `src/storytime/cli/app.py`; all four
protected files / contracts are byte-identical to the Phase 13D.1
source. No `src/`, `pyproject.toml`, `uv.lock`,
`frontend/package.json`, `frontend/package-lock.json`, or root
dependency changed. Its only `tests/` change is the narrow, explicitly
authorized mechanical advance of the state-discipline guard
`tests/test_failure_mode_regression.py` to the Phase 13D.2 current-state
expectations.

Per the Phase Closure Protocol, Phase 13D.2 is an implementation
candidate, pending review, **not locked**; it does not lock Phase
13D.2, does not close Phase 13, and does not start Phase 13E. Phase
13E and every later Phase 13 subphase have **not** started.

*(The Phase 13D.1-era note below is a historical record. Phase 13D.1
is LOCKED; Phase 13D.2 is the current implementation candidate.)*

---
# Phase 13D.1 implementation-candidate note — Static Operator GUI Refinement / Evidence & Disabled Action Discipline (historical record — Phase 13D.1 is LOCKED; see the Phase 13D.2 note above)

**Round type:** Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline — a frontend-only static / read-only refinement sub-round over the locked Phase 13D operator GUI.
**Status:** Historical record. Phase 13D.1 has since been **LOCKED** and is the last locked phase; Phase 13D.2 is now the current implementation candidate — see the Phase 13D.2 note above.
**Last locked phase:** Phase 13D — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery).

Phase 13D.1 standardizes the disabled future-action display across views
into a reusable typed component (real `<button disabled={true}>`, no
`onClick`, no fake handlers); replaces the Evidence / Validation
placeholder with a real read-only view carrying the mandatory **STATIC
PORTFOLIO DATA — NOT A LIVE CI/CD DASHBOARD** disclaimer and
repository-relative evidence references; adds a Demo / Active / Candidate
Data Source framing card (data snapshots, not deployment environments —
no switcher implemented); and extracts navigation metadata from `App.tsx`
into a small typed helper while preserving plain `useState` navigation
(no router). Phase 13D.1 does **not** modify the backend export
generator, the committed static export JSON, the `storytime
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
later subphases are future, planned work only.

*(The Phase 13D and earlier notes below are historical records. Phase
13D is LOCKED; Phase 13D.1 is the current implementation candidate.)*

---
# Phase 13D implementation-candidate note — Operator Workflow View Expansion (Governance / Safety, Failure / Recovery) (historical record — Phase 13D is LOCKED; see the Phase 13D.1 note above)

**Round type:** Phase 13D — Operator Workflow View Expansion — a frontend-only round expanding two placeholder operator views against the locked Phase 13C deterministic static export.
**Status:** Historical record. This note described Phase 13D while it was an implementation candidate. Phase 13D has since been **LOCKED** and is the last locked phase; Phase 13D.1 is now the current implementation candidate — see the Phase 13D.1 note above.

Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment —
is now **LOCKED** and is the last locked phase: it completed its Phase
Closure Protocol (GPT-5.5 review, then Gemini SAFE TO LOCK with no required
edits, then an explicit user lock decision). **Phase 13 — Portfolio
Website / Operator GUI — is STARTED.** Phase 12 — Portfolio / SE Demo
Packaging — is CLOSED, as are Phase 11 and Phase 10. Phase 13E and every
later Phase 13 subphase have **not** started — they are future, planned
work only.

Phase 13D is the fourth subphase of Phase 13. It is a frontend-only round
that takes the locked Phase 13C deterministic static export contract and
expands two of the honest placeholder views into real read-only operator
views: **Governance / Safety** (per-run Trust Envelope decisions, source
authorization categories, governance-gate result per run, display-discipline
honesty list, evidence references, visibly-disabled review actions, and a
drill-down to the existing Pipeline Run Detail view) and **Failure /
Recovery** (the failure / review queue joined to per-run failure summaries,
affected stage, related governance decision, evidence links, the operator
inspect-next guidance, and visibly-disabled recovery actions, with the same
drill-down). Per Gemini's Phase 13C guidance, Phase 13D introduces **CSS
Modules for the two new components only** as the scoped styling strategy;
the existing global stylesheet continues to back the Phase 13B/13C shell.
It adds two domain-specific view-model adapters
(`frontend/src/data/governanceAdapter.ts` and
`frontend/src/data/failureAdapter.ts`) projecting the locked Phase 13C
export, an ambient CSS-Modules TypeScript declaration, App-level
navigation rewiring with a read-only "Data source · Demo Snapshot" header
chip, and the documentation updates including a deferred-register entry
for the future **Demo / Blue / Green Data Snapshot Switcher**. It
synchronizes the State Preservation Bundle.

Phase 13D is static, read-only, and export-backed. It adds no server, no
live API, no `fetch`/`axios`, no watcher, no mutation, no authentication,
no cloud deployment, and no production hosting; the recovery / review
affordances are surfaced as visibly-disabled future actions labelled with
the phase that would enable them (Phase 13E). It **does not** modify the
backend export generator (`src/storytime/operator_export.py`), the
committed static export JSON
(`frontend/src/data/storytime-demo-export.json`), or the `storytime
export-demo-ui` CLI contract; both protected files are byte-identical to
the Phase 13C source. No `src/`, `pyproject.toml`, `uv.lock`, or root
dependency changed.

Per the Phase Closure Protocol, Phase 13D is implementation output —
**not** a locked phase until GPT-5.5 review, Gemini critique, any cleanup,
and explicit user approval complete. Phase 13D does **not** lock Phase 13D,
does **not** close Phase 13, and does **not** start Phase 13E. Phase 13 is
in progress and not closed.

*(The Phase 13C-era note below is preserved as a historical record. Phase
13C is LOCKED; Phase 13D is the current implementation candidate.)*

---
# Phase 13C implementation-candidate note — Deterministic Read-Only Static Export / Frontend Data Alignment (historical record — Phase 13C is LOCKED; see the Phase 13D note above)

**Round type:** Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment — a read-only static data-boundary round.
**Status:** Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment is an **implementation candidate / pending review — NOT locked.**

Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold —
is now **LOCKED** and is the last locked phase: it completed its Phase Closure
Protocol (GPT-5.5 review, then Gemini SAFE TO LOCK with no required edits, then
an explicit user lock decision). **Phase 13 — Portfolio Website / Operator
GUI — is STARTED.** Phase 12 — Portfolio / SE Demo Packaging — is CLOSED, as
are Phase 11 and Phase 10. Phase 13D and every later Phase 13 subphase have
**not** started — they are future, planned work only.

Phase 13C is the third subphase of Phase 13. It establishes a truthful,
reproducible, read-only data boundary between backend truth and the Phase 13B
frontend, realizing the "backend owns truth, frontend owns understanding"
contract: the backend defines the export shape, and the frontend mirrors it.
Phase 13C adds a small read-only backend export module
(`src/storytime/operator_export.py`) and a `storytime export-demo-ui` CLI
command that produce a deterministic static JSON export
(`frontend/src/data/storytime-demo-export.json`, carrying a top-level
`schemaVersion`); the export contract document
`docs/frontend-static-export-contract.md`; the frontend / GUI deferred-work
register `docs/frontend-gui-deferred-work-register.md`; a frontend adapter
(`frontend/src/data/adapter.ts`) and a `StaticDemoExport` type; backend
contract tests (`tests/test_operator_export.py`); and it rewires the homepage
and Pipeline Run Detail / Stage Timeline to consume the export through the
adapter. It lightly updates this README and `frontend/README.md` and
synchronizes the State Preservation Bundle.

Phase 13C is a static, read-only data-boundary round. The export is
deterministic — built from fixed demo data, with no `datetime.now()`, no
`uuid`, and no randomness; generating it twice yields byte-identical JSON.
Phase 13C does not make the frontend live: it adds no server, no live API, no
`fetch`/`axios`, no mutation, no authentication, no cloud deployment, and no
production hosting. Unlike Phase 13B it adds small backend code, but that code
is read-only and deterministic and changes no core pipeline runtime behaviour,
governance, telemetry, the database schema, `uv.lock`, or any root dependency.
Its `tests/` changes are the new `tests/test_operator_export.py` and the
narrow, explicitly authorized mechanical advance of the state-discipline guard
`tests/test_failure_mode_regression.py` to the Phase 13C current-state
expectations. Per the Phase Closure Protocol, Phase 13C is an implementation
candidate, pending review, **not locked**.

*(The Phase 13B note and Phase 12D note below — and the Phase 12C-era,
Phase 12B-era, Phase 12A, and Phase 11x notes further below — are historical
records. `docs/handoff-state.md` is the authoritative current-status snapshot.)*

---

# Phase 13B implementation-candidate note — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold (locked — historical record; see the Phase 13C note above)

**Round type:** Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — first frontend implementation round of Phase 13.
**Status:** Historical record. This note described Phase 13B while it was an implementation candidate. Phase 13B has since been **LOCKED** and is the last locked phase; Phase 13C is now the current implementation candidate — see the Phase 13C note above.

Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — is now
**LOCKED** and is the last locked phase: it completed its Phase Closure
Protocol (GPT-5.5 review, then Gemini SAFE TO LOCK with no required edits, then
an explicit user lock decision). **Phase 13 — Portfolio Website / Operator
GUI — is STARTED.** Phase 12 — Portfolio / SE Demo Packaging — is CLOSED, as
are Phase 11 and Phase 10. Phase 13C and every later Phase 13 subphase have
**not** started — they are future, planned work only.

Phase 13B is the second subphase of Phase 13 and the first round that writes
frontend code. Against the locked Phase 13A architecture contract it implements
a deliberately bounded frontend: a typed static portfolio shell plus one visual
operator view. It adds a new top-level `frontend/` directory — a React +
TypeScript (strict) + Vite project, standard CSS, and no external UI /
component / state / charting library — containing the frontend read-model
contract (`frontend/src/types/storytime.ts`), a static demo dataset of exactly
two mock pipeline runs (`frontend/src/data/storytime-demo-data.ts`), the
portfolio homepage, one Pipeline Run Detail view with a visual Stage Timeline,
honest placeholder components for the future portfolio sections and operator
views, and a frontend README (`frontend/README.md`). It lightly updates this
README and synchronizes the State Preservation Bundle.

Phase 13B is a static, read-only, demo-data-backed shell. It is not
backend-connected, uses no live or runtime data, implements no mutations
(retry, re-run, and review-decision actions appear only as visibly-disabled
affordances), and is not production-hosted or cloud-deployed; it contacts no
backend — there is no `fetch()`, no `axios`, and no network call. It changes no
`src/`, `pyproject.toml`, `uv.lock`, backend dependency, product, runtime, API,
CLI, telemetry, or Docker behaviour; the backend is untouched. Its only
`tests/` change is the narrow, explicitly authorized mechanical advance of the
state-discipline guard `tests/test_failure_mode_regression.py` to the Phase
13B current-state expectations. Per the Phase Closure Protocol, Phase 13B is an
implementation candidate, pending review, **not locked**.

*(The Phase 13A note and Phase 12D note below — and the Phase 12C-era,
Phase 12B-era, Phase 12A, and Phase 11x notes further below — are historical
records. `docs/handoff-state.md` is the authoritative current-status snapshot.)*

---

# Phase 13A implementation-candidate note — Portfolio Website / Operator GUI Architecture Baseline (locked — historical record; see the Phase 13B note above)

**Round type:** Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — documentation-only architecture-baseline round (documentation only).
**Status:** Historical record. This note described Phase 13A while it was an implementation candidate. Phase 13A has since been **LOCKED** and is the last locked phase; Phase 13B is now the current implementation candidate — see the Phase 13B note above.

Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — is now
**LOCKED** and is the last locked phase. **Phase 12 — Portfolio / SE Demo
Packaging — is CLOSED** (Phase 12A through 12D all locked). Phase 12D completed
its Phase Closure Protocol out-of-band: the Gemini review returned the verdict
to lock Phase 12D and close Phase 12, with no critical findings, no
non-blocking findings, and no required edits; the user, as final
decision-maker, then locked Phase 12D and formally closed Phase 12. Phase 12E
was optional, contingency-only work that would have existed only if the Phase
12D review had found a substantive packaging gap — it found none, so Phase 12E
was not needed and never started. **Phase 13 — Portfolio Website / Operator
GUI — is STARTED.** Phase 13B and every later Phase 13 subphase have **not**
started — they are future, planned work only.

Phase 13A is the first subphase of Phase 13 — Portfolio Website / Operator
GUI — the phase that follows the closed Phase 12. It is a documentation-only
architecture-baseline round: it designs the portfolio website and the
decoupled operator GUI on paper, and refines the earlier `docs/GUI_vision.md`
sketch into an authoritative Phase 13 plan, without building any of it. It
adds five `docs/` documents — `phase13-portfolio-website-architecture.md` (the
Phase 13 purpose, the end-state website and operator-GUI vision, audiences and
review paths, the website and operator information architectures, the
local-first and future-cloud compatibility rules, and the Phase 13 success
criteria), `frontend-backend-contract.md` (the "backend owns truth, frontend
owns understanding" data contract — read-model categories, future action
categories, the actions deliberately disabled for this round, and candidate
data-source options), `phase13-roadmap.md` (the Phase 13A–13G subphase
decomposition), `portfolio-website-content-model.md` (the website section
inventory mapped to existing repository source documents, with a
content-honesty checklist), and `operator-gui-view-model.md` (the operator-GUI
view inventory, disabled and future actions, empty / error / loading states,
and accessibility requirements) — lightly updates this README, and
synchronizes the State Preservation Bundle.

Phase 13A is a planning round; it does **not** implement the portfolio website
and does **not** implement the operator GUI. It adds no React, Vite,
TypeScript, JavaScript, CSS, or HTML application code, no `frontend/` / `web/`
/ `app/` directory, no `package.json` or `vite.config`, no UI, no server, and
no new dependency, and it changes no `src/`, `pyproject.toml`, `uv.lock`,
dependency, product, runtime, API, CLI, or telemetry behaviour. Its only
`tests/` change is the narrow, explicitly authorized mechanical advance of the
state-discipline guard `tests/test_failure_mode_regression.py` to the Phase
13A current-state expectations. Per the Phase Closure Protocol, Phase 13A is
an implementation candidate, pending review, **not locked**.

*(The Phase 12D note below — and the Phase 12C-era, Phase 12B-era, Phase 12A,
and Phase 11x notes further below — are historical records. `docs/handoff-state.md`
is the authoritative current-status snapshot.)*

---

# Phase 12D note — Phase 12 Closure Plan / Final Portfolio Handoff Definition (locked — Phase 12 CLOSED — historical record; see the Phase 13A note above)

**Round type:** Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — documentation-only closure-definition round (documentation only).
**Status:** Historical record. This note described Phase 12D while it was an implementation candidate. Phase 12D has since been **LOCKED**, and with it **Phase 12 — Portfolio / SE Demo Packaging — is CLOSED**; Phase 13A is now the current implementation candidate — see the Phase 13A note above.

Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — was, at the
time of this round, the last locked phase. Gemini returned SAFE TO LOCK for
Phase 12C with no critical findings, no non-blocking findings, and no required
edits; the user then locked Phase 12C. Phase 12A and Phase 12B are also locked
(the Phase 12B.1 / 12B.2 / 12B.3 cleanup sub-rounds are folded into the
Phase 12B lock lineage). **Phase 12 — Portfolio / SE Demo Packaging — has
since been CLOSED**, with Phase 12D as its final locked subphase. Phase 12E
was optional, future, contingency-only work that would have existed only if
the Phase 12D review had found a substantive packaging gap; it found none, so
Phase 12E was not needed and never started. Phase 13 — Portfolio Website /
Operator GUI — is now STARTED; see the Phase 13A note above.

Phase 12D is the fourth subphase of Phase 12. It is a documentation-only
closure-definition round: it defines what it means to close Phase 12, records
the final Phase 12A–12C portfolio asset inventory, and prepares the Phase 12
closure decision — it does **not** itself close Phase 12. It adds three
`docs/` documents — `phase12-closure-plan.md` (the Phase 12 closure criteria,
the asset inventory, the closure-readiness checklist, and the close-after-12D
vs bounded-cleanup vs separate-12E recommendation), `final-portfolio-handoff.md`
(a cold-reader handoff with tiered reviewer paths, a suggested demo flow, and an
evidence map), and `phase12-final-review-checklist.md` (the reviewer checklist
for the Phase 12D / Phase 12 closure gate) — lightly updates this README, and
synchronizes the State Preservation Bundle. It changes no `src/`,
`pyproject.toml`, `uv.lock`, dependency, product, runtime, API, CLI, or
telemetry behaviour, and adds no Phase 13 GUI implementation; its only `tests/`
change is the narrow, explicitly authorized mechanical advance of the
state-discipline guard `tests/test_failure_mode_regression.py`. Per the Phase
Closure Protocol, Phase 12D is an implementation candidate, pending review,
**not locked**.

*(The Phase 12C-era and Phase 12B-era notes below are historical records —
Phase 12C and Phase 12D are locked and Phase 12 is closed. `docs/handoff-state.md`
is the authoritative current-status snapshot.)*

---

# Phase 12C implementation-candidate note — Portfolio Demo Narrative / Public Presentation Kit (historical record — Phase 12C is LOCKED; see the Phase 12D note above)

**Round type:** Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — documentation-first portfolio packaging (documentation only).
**Status:** Historical record. This note described Phase 12C while it was an implementation candidate. Phase 12C has since been **LOCKED** and is the last locked phase; Phase 12D is now the current implementation candidate — see the Phase 12D note above.

---

# Phase 12B.3 residual living-doc state-wording cleanup note — Portfolio Evidence Pack / Reviewer Assets (bounded cleanup, NOT A LOCK — historical record)

**Round type:** residual state-hygiene cleanup of living/cold-session documents after Phase 12B.2.
**Status:** Historical record. This was a documentation-only cleanup sub-round of the Phase 12B round; it is **not a lock**. Phase 12B has since been **LOCKED** (with Phase 12B.1 / 12B.2 / 12B.3 folded into its lock lineage), and Phase 12C is now the current implementation candidate — see the Phase 12C note above.

Phase 12B.3 removed remaining stale present-tense historical wording that described Phase 12A as the current implementation candidate inside older Phase 11 notes. Those passages now explicitly point readers to the active current-state notes at the top of each living document. This preserves historical records without allowing cold sessions to misread superseded Phase 11-era notes as current state.

No product behavior, source code, tests, dependencies, lockfiles, frontend implementation, GUI implementation, runtime assets, generated audio, server/UI behavior, or Phase 13 implementation was authorized or changed by this cleanup.

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

Phase 12A — Portfolio / SE Demo Packaging Baseline — is now **LOCKED** and is
the last locked phase. (Phase 12A.1, the accepted state-hygiene cleanup
sub-round, is folded into the Phase 12A lock lineage — it is not an
independently locked phase.) **Phase 12 — Portfolio / SE Demo Packaging — is
STARTED** and is not closed. **Phase 12C and later subphases have not started.**

Phase 12B is the second subphase of Phase 12. It is a reviewer / evidence
packaging round: it adds four `docs/` documents — `portfolio-evidence-index.md`
(a claim-to-evidence index), `se-interview-evidence-matrix.md` (a
Solutions-Engineer competency-to-evidence matrix), `demo-reviewer-checklist.md`
(a reviewer wrapper over `docs/demo.md`, not a duplicate command script), and
`portfolio-public-copy.md` (disciplined, non-hype public-facing copy) — and
lightly updates this README to point reviewers to those evidence documents. It
adds no product feature and changes no `src/`, `pyproject.toml`, `uv.lock`, or
dependency; its only `tests/` change is the narrow, explicitly authorized
mechanical advance of the state-discipline guard
`tests/test_failure_mode_regression.py` to the Phase 12B current-state
expectations. Per the Phase Closure Protocol, Phase 12B is an implementation
candidate, pending review, **not locked**.

*(The Phase 12A.1 and Phase 12A notes below are historical records — Phase 12A
is locked. See `docs/handoff-state.md` for the authoritative current status.)*

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

**Date:** 2026-05-26
**Candidate artifact:** `storytime-phase12a-portfolio-se-demo-packaging-baseline.tar.gz` (SHA-256 reported on delivery).
**Source artifact:** `storytime-phase11d-release-candidate-evidence-pack.tar.gz` (SHA-256 `07a3973e3dbb69d760ff2c330418f85101c2afa1464fc0eed752fc7053894d94`).
**Status:** Phase 12A — Portfolio / SE Demo Packaging Baseline is **LOCKED / ACCEPTED / CANONICAL** (locked after the accepted Phase 12A.1 state-hygiene cleanup sub-round). *(This note is a historical record — current status is in the Phase 12B note above.)*
**Last locked phase:** Phase 12A — Portfolio / SE Demo Packaging Baseline (this phase).
**Current phase:** Phase 12 — Portfolio / SE Demo Packaging — STARTED; Phase 12B is its current subphase *(see the Phase 12B note above)*.

Phase 12A is the first subphase of Phase 12 — Portfolio / SE Demo Packaging. It
is documentation and portfolio-packaging only: it makes StoryTime explainable as
a Solutions Engineer / observability / OpenTelemetry portfolio project without
adding any product feature or changing any runtime behaviour. It adds four
`docs/` documents — `portfolio-overview.md`, `solutions-engineer-narrative.md`,
`portfolio-demo-script.md`, and `interview-talking-points.md` — refines this
`README.md` for a portfolio-facing reviewer, and synchronizes the State
Preservation Bundle.

Phase 12A added no product feature, no UI, no server, no JavaScript, no
generated audio, no screenshots/binary assets, and no new dependency; it changed
no pipeline behaviour, `storytime rerun`, or Trust Envelope enforcement, and
changed no `pyproject.toml`, `uv.lock`, or `src/` content. The only `tests/`
change is a narrow, explicitly authorized advance of the state-discipline guard
`tests/test_failure_mode_regression.py` so it tracks the Phase 12A current-state
expectations (it now guards against a premature Phase 12A lock, a premature
Phase 12 closure, and a premature Phase 12B-or-later start). Per the Phase
Closure Protocol, Phase 12A is implementation output, not a locked phase.

**Out-of-band Phase 11 closure (recorded here honestly).** Before Phase 12A,
the Phase 11D — Release Candidate Evidence Pack artifact completed its Phase
Closure Protocol out-of-band in the GPT/Gemini review workflow: GPT-5.5 review
PASS, Gemini review SAFE TO LOCK, no required edits. The user, as final
decision-maker, then locked Phase 11D and formally closed Phase 11 — Release
Candidate Hardening, and authorized Phase 12. **Phase 11D is locked; Phase 11 is
CLOSED; Phase 12 is STARTED.** This closure was a user/mediator decision
supplied to the Phase 12A round; it was not contained in the Phase 11D archive,
which captured the pre-lock implementation-candidate state.

*(The Phase 11D note below is a historical record — Phase 11D is now locked and
Phase 11 — Release Candidate Hardening — is CLOSED.)*

---

# Phase 11D note — Release Candidate Evidence Pack (locked — historical record)

**Date:** 2026-05-25
**Status:** Phase 11D — Release Candidate Evidence Pack is **LOCKED / ACCEPTED / CANONICAL**. *(This note was originally written when Phase 11D was an implementation candidate; Phase 11D was subsequently locked out-of-band under the Phase Closure Protocol, and Phase 11 — Release Candidate Hardening — was formally CLOSED. Current status is in the Phase 12B note above.)*
**Previous locked phase:** Phase 11C — Failure-Mode / Regression Hardening.
**Current phase:** *(superseded — see the Phase 12B note above.)*

Phase 11D is the fourth and final planned Release Candidate Hardening subphase.
It is an evidence, closure-readiness, and proof-consolidation round: it
consolidates the release-candidate evidence produced by Phases 11A, 11B, and
11C into a reviewer-facing index, records the canonical validation results,
prepares a Phase 11 closure checklist, and writes a Phase 12 readiness handoff.
It added four `docs/` documents (`release-candidate-evidence-pack.md`,
`final-validation-summary.md`, `phase11-closure-checklist.md`,
`phase12-readiness-handoff.md`), refreshed the Phase 11 status documents, and
synchronized the State Preservation Bundle.

Phase 11D added no product feature, no UI, no server, no JavaScript, no
generated audio, no screenshots/binary assets, and no new dependency; it
changed no pipeline behaviour, `storytime rerun`, or Trust Envelope
enforcement, and changed no `pyproject.toml`, `uv.lock`, `src/`, or `tests/`
content. It is documentation/evidence consolidation only and added no test.
Phase 11D subsequently completed the Phase Closure Protocol out-of-band
(GPT-5.5 review PASS; Gemini review SAFE TO LOCK; no required edits) and was
locked by explicit user decision; with Phase 11D locked, **Phase 11 — Release
Candidate Hardening — is CLOSED**. See `docs/handoff-state.md` for
authoritative current status.

*(The Phase 11C note below is a historical record. Phase 11D is locked and
Phase 11 is closed; Phase 12A is locked, and Phase 12B is the current
implementation candidate — see the Phase 12B note above.)*

---

# Phase 11C note — Failure-Mode / Regression Hardening (locked — historical record)

**Date:** 2026-05-25
**Status:** Phase 11C — Failure-Mode / Regression Hardening is **LOCKED** — it was the last locked phase at that point in the project history. *(This is a superseded point-in-time record, originally written when Phase 11C was an implementation candidate; it was subsequently locked under the Phase Closure Protocol and is the source/base artifact for Phase 11D. Current status is in the Phase 12B note above.)*
**Current phase:** *(superseded — see the Phase 12B note above.)*

Phase 11C is the third Release Candidate Hardening subphase. It is a
failure-mode and regression-hardening round: it inventories the highest-risk
failure and regression paths that already exist in StoryTime — the failure /
review queue, retry / re-run behaviour, governance-blocked content, static HTML
report safety, demo fixture invariants, the legal-hallucination gate,
operator-safe failure messages, and state preservation around failed runs —
records which tests and gates protect each one, and documents how a local
operator should respond to a failure without bypassing governance or deleting
state. It added four `docs/` documents (`failure-mode-regression-hardening.md`,
`regression-risk-register.md`, `failure-mode-test-matrix.md`,
`operator-failure-response.md`) and one focused regression test module
(`tests/test_failure_mode_regression.py`, the state-documentation discipline
guard), and synchronized the State Preservation Bundle.

Phase 11C added no product feature, no UI, no server, no JavaScript, no
generated audio, no screenshots/binary assets, and no new dependency; it
changed no pipeline behaviour, `storytime rerun`, or Trust Envelope
enforcement, and changed no `pyproject.toml`, `uv.lock`, or `src/` content. The
only `tests/` change is the new regression module. Per the Phase Closure
Protocol, Phase 11C was implementation output until GPT-5.5 review, Gemini
critique, any cleanup, and explicit user approval completed; it has since been
locked. See `docs/handoff-state.md` for authoritative current status.

*(This Phase 11C note is a historical record. The Phase 11B note below is also
a historical record. Phase 11C — Failure-Mode / Regression Hardening — is
locked; Phase 11 is closed and Phase 12A is the current implementation
candidate — see the Phase 12A note at the top of this file.)*

---

# Phase 11B note — Fresh Clone / Operator Reproducibility (locked — historical record)

**Date:** 2026-05-25
**Status:** Phase 11B — Fresh Clone / Operator Reproducibility is **LOCKED** — it was the last locked phase at that point in the project history. *(This is a superseded point-in-time record, originally written when Phase 11B was an implementation candidate; Phase 11B was subsequently locked under the Phase Closure Protocol and is the source/base artifact for Phase 11C. Current status is in the Phase 12B note above.)*
**Current phase:** *(superseded — see the Phase 12B note above.)*

Phase 11B is the second Release Candidate Hardening subphase. It is a
fresh-clone and operator reproducibility verification round: it walked the
Phase 11A setup, validation, and demo paths from a clean extraction and
confirmed they reproduce the documented baseline. It added two reproducibility
documents (`docs/operator-reproducibility-checklist.md`,
`docs/fresh-clone-troubleshooting.md`), refined the Phase 11A reproducibility
documents, aligned the `README.md` setup command with the canonical
`uv sync --frozen --extra dev` form, and synchronized the State Preservation
Bundle. It added no product feature, no UI, no server, no JavaScript, no
generated audio, no screenshots/binary assets, and no new dependency; it
changed no pipeline behaviour, `storytime rerun`, or Trust Envelope
enforcement, and changed no `pyproject.toml`, `uv.lock`, `src/`, or `tests/`
content.

*(The Phase 11A note below is a historical record. Phase 11A — Release
Candidate Hardening Baseline — is locked; Phase 11 is closed and Phase 12A is
the current implementation candidate — see the Phase 12A note at the top of
this file.)*

---

# Phase 11A note — Release Candidate Hardening Baseline (locked — historical record)

**Date:** 2026-05-25
**Locked artifact:** `storytime-phase11a-release-candidate-hardening-baseline.tar.gz` (SHA-256 `664f8ba4ae90cf6a98ccc7d20369e690eac74497ab78f2b7067f0aac2079a7aa`).
**Status:** Phase 11A — Release Candidate Hardening Baseline is **LOCKED**. *(This is a superseded point-in-time record, originally written when Phase 11A was an implementation candidate; Phase 11A was subsequently locked under the Phase Closure Protocol. Phase 11B, Phase 11C, and Phase 11D have since also been locked and Phase 11 — Release Candidate Hardening — is CLOSED; current status is in the Phase 12B note above.)*
**Current phase:** *(superseded — see the Phase 12B note above.)*

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
`storytime rerun`, Trust Envelope enforcement, `pyproject.toml`, `uv.lock`,
`src/`, or `tests/`. The six Docker-free quality gates pass. See
`docs/release-candidate-hardening.md`.

*(The Phase 10G lock closure note below is a historical record. Phase 10 is
CLOSED; the Post-Phase-10 Historical State Reconciliation was the last locked
work item before Phase 11; Phase 11A and Phase 11B are locked; Phase 11C is the
current implementation candidate.)*

---

# Phase 10G lock closure note — Phase 10 CLOSED

**Date:** 2026-05-25
**Locked artifact:** `storytime-phase10g1-uvlock-reversion-cleanup.tar.gz`
**SHA-256:** `8a0cc9a5b6426a291bec3a793e41501c7d3492187dd48b4f7729ea95e501a0c1`
**Status:** Phase 10G — Portfolio Narrative / Phase 10 Closure is **LOCKED / ACCEPTED / CANONICAL**. **Phase 10 is formally CLOSED.**
**Last locked phase:** Phase 10G — Portfolio Narrative / Phase 10 Closure.
**Next phase:** Phase 11 — Release Candidate Hardening *(now in progress — see the Phase 11C implementation-candidate note at the top of this file for current status; Phase 11A and Phase 11B are locked)*.

Phase 10G — the documentation, portfolio-narrative, demo-explanation, and Phase 10 closure phase — is locked. It added `docs/portfolio-narrative.md`, `docs/demo-script.md`, `docs/operator-experience-walkthrough.md`, `docs/command-reference.md`, `docs/known-limitations.md`, `docs/observability-governance-talking-points.md`, `docs/phase10-acceptance-checklist.md`, and `docs/screenshot-instructions.md`, and synchronized the State Preservation Bundle. It added no product feature, no UI, no server, no JavaScript, no generated audio, no screenshots/binary assets, and no new dependency; it changed no pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, or the database schema. Phase 10G completed the Phase Closure Protocol (GPT-5.5 review PASS; Gemini review SAFE WITH EDITS; the Phase 10G.1 `uv.lock` cleanup; GPT-5.5 / Gemini Phase 10G.1 verification SAFE TO LOCK; explicit user lock approval). With Phase 10G locked, **Phase 10 — Product UI / Operator Experience — is formally CLOSED** (Phases 10A–10G all locked). The next phase is **Phase 11 — Release Candidate Hardening**, which has **not started**.

*(The Phase 10C lock closure note below is a historical record. Phase 10A, 10B, 10C, 10C.1, 10D, 10D.1, 10E — with the 10E.1 / 10E.2 cleanup sequence — 10F, and 10G are all locked; Phase 10 is closed.)*

---

# Phase 10F lock closure note

**Date:** 2026-05-25
**Lock archive:** `storytime-phase10f-demo-seed-data-golden-path-fixtures.tar.gz`
**SHA-256:** `e060570a94fb19f790c539542b3ef7445111430bc308668675548f66fa48df55`
**Status:** Phase 10F — Demo Seed Data / Golden Path Fixtures is **LOCKED / ACCEPTED / CANONICAL**.
**Last locked phase:** Phase 10F.
**Next phase:** Phase 10G — Portfolio Narrative / Phase 10 Closure.

Phase 10F added curated demo seed data and golden-path fixture scenarios so an operator can demonstrate the existing StoryTime pipeline, operator report, failure queue, Trust Envelope governance, and `storytime rerun` command reproducibly from a clean local environment — the `demo/` directory (four original CC0 seed texts plus schema-valid manifests, a demo-only blocked-source deny-list, and six fixture definitions), the `docs/demo.md` operator runbook, and `tests/test_demo_fixtures.py`. It was fixture / demo-readiness work: no new product feature, no UI, no server, no generated audio committed, no JavaScript, no new dependency, and no change to pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, or the database schema. Phase 10F completed the Phase Closure Protocol and was locked with explicit user approval.

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

# StoryTime

StoryTime is a local-first, observability-native pipeline that turns approved
CC0 / US public-domain text into podcast-ready audio, an RSS feed, and a
traceable record of every run.

It runs entirely on one machine, from the command line, with no cloud
services and no required network calls. SQLite and on-disk artifact envelopes
are the source of truth; OpenTelemetry is an optional *view* over that truth.

## For reviewers — start here

If you are reviewing StoryTime as a **portfolio project** — a hiring manager, a
Solutions Engineer interviewer, or a technical reviewer — here is the fast path:

- **What it is.** A local-first, observability-native content-to-audio pipeline.
  The podcast pipeline is the vehicle; the subject is engineering and
  operational discipline — honest observability, mechanically enforced
  boundaries, fail-closed governance that does not overclaim, and an
  append-only, auditable history.
- **Who built it and how.** Built by a multi-model "RoundTable" workflow under
  an explicit Phase Closure Protocol: every phase is implemented, independently
  reviewed, critiqued, and only then locked by explicit user approval.
- **Status.** Phases 0–11 are complete and locked; Phase 11 (release-candidate
  hardening) is CLOSED. Phase 12 (portfolio / SE demo packaging) is CLOSED —
  Phase 12A, 12B, 12C, and 12D are all locked. Phase 13 (portfolio website /
  operator GUI) is in progress: Phase 13A (portfolio website / operator GUI
  architecture baseline) is the current implementation candidate — a
  documentation-only design round that does **not** build the website or the
  GUI. It is **not** a deployed product — no users, no SLA, no cloud — and it
  says so plainly. `docs/known-limitations.md` states every boundary.
- **How to run it.** Install [uv](https://docs.astral.sh/uv/), then
  `uv sync --frozen --extra dev`, then `uv run storytime doctor`. The six
  Docker-free quality gates and the whole test suite run offline. The
  reproducible demo is `docs/demo.md`; to run the demo as a reviewer, use the
  wrapper `docs/demo-reviewer-checklist.md`.
- **Where to read the story.** Start with the final portfolio handoff
  (tiered reviewer paths, demo flow, evidence map):
  `docs/final-portfolio-handoff.md`. A concise demo narrative (the fastest 5–10
  minute read): `docs/portfolio-demo-narrative.md`. Plain-English overview:
  `docs/portfolio-overview.md`. Claim-to-evidence index (verify any claim
  against a real file): `docs/portfolio-evidence-index.md`. Solutions-Engineer
  competency-to-evidence matrix: `docs/se-interview-evidence-matrix.md`.
  Interview / Solutions-Engineer framing: `docs/solutions-engineer-narrative.md`,
  with reusable interview answer frames in `docs/interview-story-bank.md`. A
  narrated reviewer walkthrough: `docs/portfolio-demo-script.md`, and a spoken
  5/10/20-minute demo talk track: `docs/demo-talk-track.md`. Concise study
  points: `docs/interview-talking-points.md`. Non-hype public-facing copy:
  `docs/portfolio-public-copy.md`. The Phase 10 narrative those build on:
  `docs/portfolio-narrative.md`. How Phase 12 closes:
  `docs/phase12-closure-plan.md`. Where Phase 13 is going (the portfolio
  website and decoupled operator GUI, designed on paper, not yet built):
  `docs/phase13-portfolio-website-architecture.md`.

Every claim in those documents is backed by a test, a config file, or another
document in this repository.

## Maturity

StoryTime is well past a scaffold — it is a working end-to-end pipeline with
approval gates, resume/rehydration, multi-item RSS publishing, a range-capable
feed server, an observability stack, and a local blue/green deployment path.

| Phase | Scope | Status |
|-------|-------|--------|
| 0 | Product Charter | locked (`docs/product-charter.md`) |
| 1 | Architecture Baseline | locked (`docs/architecture-baseline.md`) |
| — | Phase Closure Protocol | locked (`docs/phase-closure-protocol.md`) |
| 2 | Repository scaffold + dev environment | locked |
| 3 | Thin vertical slice (ingest → synthesize → assemble → publish) | locked |
| 4 / 4.1 | Persisted approval gates + resume/rehydration | locked |
| 5 | OpenTelemetry instrumentation foundation | locked |
| 6S | Range-capable feed serving + multi-item RSS | locked |
| 6A | Observability stack, dashboards-as-code, demo harness | locked |
| 6B | SLO/SLI narrative, runbook, demo walkthrough | locked |
| 7A | Blue/green deployment, Option A (per-slot processes) | locked |
| 7B | Higher-assurance front door / active-slot switching | locked |
| 7C / 7C.1 | Architecture Baseline amendment — optional local app containerization | locked |
| 7D | Optional local app containerization | locked |
| 7D.1 | Operational cleanup — compose build race fix | locked |
| 8A | Architecture Baseline amendment — Collector-owned telemetry fan-out | locked |
| 8B | Local multi-backend stack expansion — Loki + local log routing | locked |
| 8B.1 | Operational cleanup — `./logs` directory preflight | locked |
| 8C / 8C.1 | Optional vendor export profiles — disabled-by-default Dynatrace / New Relic export; 8C.1 split into two independent per-vendor profiles | locked |
| 9A / 9A.1 | Governance Baseline amendment — Architecture Baseline §24 (Trust Envelope, licensing, fail-closed gating); 9A.1 cleanup added source-authorization-not-viewpoint and early fail-closed clarifications | locked |
| 9B | Minimal Trust Envelope Implementation — the `governance` package, durable Trust Envelope artifact + SQLite projection, fail-closed gate, blocked-source config, static legal-hallucination gate; 9B.1 cleanup hardened that scanner against binary/generated files | locked (9B.1 folded in) |
| 10A | Operator Experience Baseline Amendment — Architecture Baseline §25 (the Phase 10 operator-experience law: read-only-first, source-of-truth, governance display rules, the Phase 10B target / hard floor / hard ceiling, report data model, field allowlist/blacklist, Phase 10B handoff) | locked |
| 10B | Generated Local HTML Operator Report — the `storytime.reporting` package and the `storytime report generate` CLI command: a static, local, read-only HTML operator report | locked |
| 10C | Operator CLI Helpers / Failure Queue — the `storytime.operator_queue` module and the read-only `storytime queue` command: a bounded, deterministic failure/review queue | locked |
| 10C.1 | State Preservation Synchronization Cleanup — docs/state-preservation sync after the Phase 10C lock | locked |
| 10D | Pipeline Re-Run / Mutation Actions — the `storytime.operator_rerun` module and the governed `storytime rerun` command: the first operator mutation surface | locked |
| 10D.1 | State Preservation Cleanup + LLM Director Hardening | locked |
| 10E | Static HTML Operator Report Refinement — executive summary, rerun eligibility guidance, failure summary, command reference, semantic badges, improved CSS; 10E.1 / 10E.2 cleanup sequence accepted | locked |
| 10F | Demo Seed Data / Golden Path Fixtures — the `demo/` seed data and six golden-path fixture definitions, the `docs/demo.md` operator runbook, fixture tests | locked |
| 10G | Portfolio Narrative / Phase 10 Closure — Phase 10 portfolio/closure documents and State Preservation Bundle sync | locked — **Phase 10 CLOSED** |
| — | Post-Phase-10 Historical State Reconciliation — RoundTable JSON historical backfill into the historical living docs (not a new phase) | locked |
| 11A | Release Candidate Hardening Baseline — fresh-clone readiness, validation-command baseline, artifact hygiene, security/secrets posture, demo reproducibility, Phase 11 decomposition | locked |
| 11B | Fresh Clone / Operator Reproducibility — verify the documented setup, validation, and demo paths from a clean checkout; reproducibility checklist + troubleshooting guide | locked |
| 11C | Failure-Mode / Regression Hardening — inventory and test-map the failure / regression surfaces; confirm fail-closed and read-only invariants; operator failure-response playbook | locked |
| 11D | Release Candidate Evidence Pack — consolidate the release-candidate evidence, validation results, hygiene proof, and Phase 11 closure checklist into a reviewer-facing index | locked |
| 11 | Release Candidate Hardening (11A–11D) — overall phase | **CLOSED** |
| 12A | Portfolio / SE Demo Packaging Baseline — portfolio-facing documents (`portfolio-overview.md`, `solutions-engineer-narrative.md`, `portfolio-demo-script.md`, `interview-talking-points.md`) and README portfolio refinement | locked |
| 12B | Portfolio Evidence Pack / Reviewer Assets — reviewer/evidence documents (`portfolio-evidence-index.md`, `se-interview-evidence-matrix.md`, `demo-reviewer-checklist.md`, `portfolio-public-copy.md`) and a light README reviewer-pointer refinement; 12B.1 / 12B.2 / 12B.3 cleanup sub-rounds folded in (12B.2 preserved the Phase 13 GUI roadmap vision) | locked |
| 12C | Portfolio Demo Narrative / Public Presentation Kit — public-presentation documents (`portfolio-demo-narrative.md`, `demo-talk-track.md`, `interview-story-bank.md`, `public-repository-readiness.md`) and a light README reviewer-pointer refinement | locked |
| 12D | Phase 12 Closure Plan / Final Portfolio Handoff Definition — closure-definition documents (`phase12-closure-plan.md`, `final-portfolio-handoff.md`, `phase12-final-review-checklist.md`) and a light README reviewer-pointer refinement | locked |
| 12 | Portfolio / SE Demo Packaging (12A–12D) — overall phase | **CLOSED** |
| 13A | Portfolio Website / Operator GUI Architecture Baseline — documentation-only design round: five `docs/` architecture documents (`phase13-portfolio-website-architecture.md`, `frontend-backend-contract.md`, `phase13-roadmap.md`, `portfolio-website-content-model.md`, `operator-gui-view-model.md`) and a light README update; no website, GUI, or frontend code | in progress — implementation candidate (pending review, not locked) |
| 13 | Portfolio Website / Operator GUI — overall phase | STARTED (Phase 13A current; Phase 13B–13G not started; Phase 13 not closed) |

**Phase 7 and all of Phase 8 are locked; Phase 8 — Multi-Backend Telemetry
Fan-Out — is complete.** Phase 8A (`docs/architecture-baseline.md` §23 —
Collector-owned telemetry fan-out governance) is locked and canonical;
Phase 8B / 8B.1 locked the five-service local observability stack and local
log routing; and **Phase 8C — Optional Vendor Export Profiles**, with the
Phase 8C.1 cleanup, is locked. Phase 8C adds optional, disabled-by-default
Dynatrace and New Relic export profiles through the Collector, each reached
only via its own explicit, mutually exclusive `docker-compose.vendor.*.yml`
override — the default stack stays local-only. It is a configuration/
documentation phase that changes no application behaviour; it completed the
Phase Closure Protocol (GPT-5.5 review, Gemini critique — `SAFE TO LOCK` — and
user approval) and was locked 2026-05-24, completing Phase 8.

**Phase 9A — Governance Baseline Amendment** is **locked**
(`docs/architecture-baseline.md` Section 24 — Governance Baseline: Trust
Envelope, Licensing, Fail-Closed Gating). It defines StoryTime's governance
law — the human operator is the source of truth for licensing decisions,
StoryTime is not a legal rights-clearance engine, governance is source
authorization and not viewpoint acceptability, a fail-closed gate hard-blocks
before TTS/audio/RSS unless an `APPROVED` Trust Envelope exists, and the
canonical minimum Trust Envelope schema — before any Phase 9B implementation.
It completed the Phase Closure Protocol (GPT-5.5 review, Gemini critique —
`SAFE WITH EDITS`, with the Phase 9A.1 cleanup folding in the two required
clarifications — and user approval) and was locked 2026-05-24.

**Phase 9B — Minimal Trust Envelope Implementation** is **locked (2026-05-24),
with the Phase 9B.1 forbidden-term-scanner hardening cleanup folded into the
lock.** Phase 9B turned the locked Section 24 governance law into working
code: a new `storytime.governance` package (the Trust Envelope model and its
canonical §24.8 closed schema); a durable Trust Envelope artifact written per
run (`governance/trust-envelope.json`, the governance source of truth); a
rebuildable SQLite projection; a fail-closed gate that derives the Trust
Envelope at ingest from the operator's manifest, checks it early, and
hard-blocks before TTS and before RSS publishing unless an `APPROVED` envelope
exists; a local `config/governance/blocked-sources.yaml` deny-list; and a
static legal-hallucination grep/regex gate. The Trust Envelope transcribes the
human operator's recorded licensing decision — StoryTime performs no legal
determination. The **Phase 9B.1 cleanup** hardened that static forbidden-term
scanner, per Gemini's `SAFE WITH MINOR CLEANUP` review, so it cannot crash on
binary or generated files. Phase 9B completed the Phase Closure Protocol
(GPT-5.5 review, Gemini critique, the 9B.1 cleanup, and user approval) and was
locked 2026-05-24.

**Phase 10A — Operator Experience Baseline Amendment** is **locked / accepted /
canonical** — `docs/architecture-baseline.md` Section 25, "Operator Experience
Baseline". Section 25 defines the Phase 10 operator-experience law before any
Phase 10 implementation: Phase 10 makes StoryTime understandable, operable, and
demoable by a single local human operator without becoming a hosted SaaS
product; it is read-only-first; SQLite plus the on-disk artifact envelopes (and
the durable Trust Envelope) stay the source of truth; governance status is
shown faithfully (the stable `APPROVED` / `REJECTED` / `BLOCKED` /
`NEEDS_REVIEW` enum) with a standing "record of a human decision, not legal
advice" disclaimer and no legal-certification overclaiming. Section 25 also
fixes the first implementation phase — a generated, static, local, read-only
HTML operator report — with a hard floor, a hard ceiling, a report data model,
a field allowlist/blacklist, and a full Phase 10B handoff specification.

**Phase 10B — Generated Local HTML Operator Report** is **locked / accepted / canonical**. It adds the `storytime.reporting` package and `storytime report generate`, producing a static, local, read-only HTML report from existing authoritative state. The report is air-gapped/no-CDN, no-server, no-auth, no-cloud, no-frontend-framework, no-mutation, no-raw-content, and no-legal-overclaiming.

**Phase 10C — Operator CLI Helpers / Failure Queue** is **locked / accepted / canonical (2026-05-25)**. It adds the `storytime.operator_queue` module and the read-only `storytime queue` command — a bounded, deterministic command-line view of the runs that need operator attention.

**Phase 10D — Pipeline Re-Run / Mutation Actions is locked (2026-05-25).** It added the `storytime.operator_rerun` module and the governed `storytime rerun` command — StoryTime's first operator *mutation* surface: a bounded, audited re-run of a failed pipeline run, gated on Trust Envelope governance.

**Phase 10E — Static HTML Operator Report Refinement** is **locked / accepted / canonical (2026-05-25)**, with the Phase 10E.1 / 10E.2 cleanup sequence accepted. It refined the existing generated static HTML operator report with an executive status summary, rerun eligibility guidance, failure summary, command reference section, semantic status badges, improved governance warning block, and improved embedded CSS layout, keeping the report a local, static, read-only artifact with no JavaScript, no external assets, and no backend behavior change.

**Phase 10F — Demo Seed Data / Golden Path Fixtures** is **locked / accepted / canonical (2026-05-25)**. It added the `demo/` directory — four original CC0 demo seed texts with schema-valid manifests, a demo-only blocked-source deny-list, and six golden-path fixture definitions — plus the `docs/demo.md` operator demo runbook and `tests/test_demo_fixtures.py`. It exercises the real existing pipeline, report, queue, governance, and `storytime rerun`: no new product feature, no UI, no server, no generated audio committed, no JavaScript, and no new dependency. See `docs/demo.md`.

**Phase 10G — Portfolio Narrative / Phase 10 Closure** is **locked / accepted / canonical (2026-05-25)**. It was a documentation, portfolio-narrative, demo-explanation, and Phase 10 closure round. It added the Phase 10 portfolio/closure documents — `docs/portfolio-narrative.md`, `docs/demo-script.md`, `docs/operator-experience-walkthrough.md`, `docs/command-reference.md`, `docs/known-limitations.md`, `docs/observability-governance-talking-points.md`, `docs/phase10-acceptance-checklist.md`, and `docs/screenshot-instructions.md` — and synchronized the State Preservation Bundle. It added no product feature, no UI, no server, no JavaScript, no generated audio, no screenshots/binary assets, and no new dependency. The locked Phase 10G artifact is `storytime-phase10g1-uvlock-reversion-cleanup.tar.gz` (SHA-256 `8a0cc9a5b6426a291bec3a793e41501c7d3492187dd48b4f7729ea95e501a0c1`). **With Phase 10G locked, Phase 10 — Product UI / Operator Experience — is formally CLOSED**; all of its sub-phases (10A–10G) are locked. After the closure, the Post-Phase-10 Historical State Reconciliation (the RoundTable JSON historical backfill — not a new phase) was locked. **Phase 11 — Release Candidate Hardening — is now CLOSED.** Its four subphases — 11A (Release Candidate Hardening Baseline), 11B (Fresh Clone / Operator Reproducibility), 11C (Failure-Mode / Regression Hardening), and 11D (Release Candidate Evidence Pack) — are all locked; Phase 11D completed its Phase Closure Protocol out-of-band (GPT-5.5 review PASS; Gemini review SAFE TO LOCK) and the user locked Phase 11D and formally closed Phase 11.

**Phase 12 — Portfolio / SE Demo Packaging — is CLOSED.** Its four
subphases — Phase 12A (Portfolio / SE Demo Packaging Baseline), Phase 12B
(Portfolio Evidence Pack / Reviewer Assets), Phase 12C (Portfolio Demo
Narrative / Public Presentation Kit), and Phase 12D (Phase 12 Closure Plan /
Final Portfolio Handoff Definition) — are all locked. Phase 12A added four
`docs/` documents (`portfolio-overview.md`, `solutions-engineer-narrative.md`,
`portfolio-demo-script.md`, `interview-talking-points.md`); the accepted Phase
12A.1 state-hygiene cleanup sub-round is folded into the Phase 12A lock
lineage. Phase 12B added four reviewer/evidence `docs/` documents
(`portfolio-evidence-index.md`, `se-interview-evidence-matrix.md`,
`demo-reviewer-checklist.md`, `portfolio-public-copy.md`); the accepted Phase
12B.1 / 12B.2 / 12B.3 cleanup sub-rounds are folded into its lock lineage.
Phase 12C added four public-presentation `docs/` documents
(`portfolio-demo-narrative.md`, `demo-talk-track.md`, `interview-story-bank.md`,
`public-repository-readiness.md`). Phase 12D added three closure-definition
`docs/` documents (`phase12-closure-plan.md`, `final-portfolio-handoff.md`,
`phase12-final-review-checklist.md`). Phase 12D completed its Phase Closure
Protocol out-of-band — the Gemini review returned the verdict to lock Phase
12D and close Phase 12, with no required edits — and the user then locked
Phase 12D and formally closed Phase 12. Phase 12E was optional, contingency-only
work; the Phase 12D review found no substantive gap, so Phase 12E was not
needed and never started. None of the Phase 12 subphases changed any product
behaviour.

**Phase 13 — Portfolio Website / Operator GUI — is STARTED. Phase 13A —
Portfolio Website / Operator GUI Architecture Baseline — is the current
subphase, an implementation candidate pending review, not locked.** Phase 13A
is a documentation-only architecture-baseline round: it designs the
portfolio-facing website and the decoupled operator GUI on paper, and refines
the earlier `docs/GUI_vision.md` sketch into an authoritative Phase 13 plan.
It adds five `docs/` documents — `phase13-portfolio-website-architecture.md`,
`frontend-backend-contract.md`, `phase13-roadmap.md`,
`portfolio-website-content-model.md`, and `operator-gui-view-model.md` — and
lightly updates this README, with no product behaviour change. Phase 13A does
**not** build the website or the operator GUI: it adds no React, Vite,
TypeScript, JavaScript, CSS, or HTML application code, no frontend directory,
no `package.json` or `vite.config`, and no new dependency. Phase 13B through
Phase 13G are future, planned work and have not started; Phase 13 is not
closed. See `docs/phase13-portfolio-website-architecture.md`,
`docs/phase13-roadmap.md`, and `docs/handoff-state.md` for the authoritative
current status.

## Project state & RoundTable handoff

Until the RoundTable workflow is restored, this repository is the portable
project memory. **Any LLM working on StoryTime must read `LLM_DIRECTOR.md` (at
the repo root) first** — it gives the first-read order, model roles, and the
update rules.

The **State Preservation Bundle** is `LLM_DIRECTOR.md` plus the `docs/` state
files: `handoff-state.md` (authoritative current status and next action),
`roadmap.md` (phases, gates, model routing), `canonical-state.md`
(locked-decision log), `phase-history.md`, `open-issues.md`,
`verification-log.md` (verification evidence), `artifact-manifest.md` (archive
lineage and hashes), and `roundtable-import-bridge.md` (how to rebuild
RoundTable state from the Bundle). Start with `LLM_DIRECTOR.md`, then
`docs/handoff-state.md`.

## Requirements

- Python >= 3.11 (developed and tested on 3.12)
- [uv](https://docs.astral.sh/uv/) for environment and dependency management
- ffmpeg — required by the MP3 assembly stage. `storytime doctor` reports
  whether it is found.
- Docker (optional) — for the local OpenTelemetry Collector + Jaeger +
  Prometheus + Loki + Grafana observability stack, and for the optional
  containerized blue/green demo (`docker-compose.app.yml`). The pipeline, the
  bare-metal
  blue/green workflow, and the whole test suite run without it.

## Setup

    uv sync --frozen --extra dev

This creates `.venv`, installs runtime and dev dependencies, and installs
`storytime` as an editable package. `--frozen` installs exactly what `uv.lock`
pins and fails rather than silently re-resolving — the canonical, reproducible
form used by the validation gates (`docs/rc-validation-checklist.md`) and the
fresh-clone path (`docs/fresh-clone-checklist.md`).

## Windows operator quickstart (Phase 14B.1 live proof loop)

The live proof loop runs on Windows with the same two-terminal flow. From
**PowerShell**:

Terminal 1 — backend (loopback only):

```powershell
cd C:\Users\<you>\Desktop\storytime
uv sync --frozen --extra dev
uv run storytime doctor
uv run storytime local-live          # serves http://127.0.0.1:8770
```

Terminal 2 — frontend dev server:

```powershell
cd C:\Users\<you>\Desktop\storytime\frontend
npm install
npm run dev                          # serves http://localhost:5173
```

Then open http://localhost:5173 → **Live Proof Loop**, **Connect**, run the
**success** scenario, then the two **failure** scenarios, and restart the
backend to confirm every run (success and failure) is still listed.

**Troubleshooting (Windows):**

- **`npm install` fails with `ECONNRESET` / network errors** — a transient
  registry/proxy issue. Retry `npm install`; if it persists, run
  `npm cache clean --force` then `npm install`, or check a corporate
  proxy/VPN. The frontend cannot build until `npm install` completes.
- **`vite` is not recognized / `'vite' is not recognized as an internal or
  external command`** — `npm install` did not finish, so dev dependencies are
  missing. Re-run `npm install` in `...\storytime\frontend` and confirm a
  `node_modules` directory exists, then `npm run dev` again.
- **ffmpeg missing warning** — the live proof loop is mock and does **not** use
  ffmpeg; an ffmpeg "not found" notice from `doctor` is safe to ignore for the
  proof loop (ffmpeg only matters for the deferred real-audio pipeline).
- **Windows `pytest` failures referencing POSIX paths/permissions** — some
  older-phase tests assume POSIX behaviour. These are pre-existing and unrelated
  to the live proof loop; the Phase 14B.1 proof path itself uses no `chmod`,
  `os.uname`, bash-only scripts, symlinks, or ffmpeg. Run the backend gates
  under WSL/Linux for a clean pass, or scope `pytest` to
  `tests/test_local_live_proof_loop.py` and
  `tests/test_local_live_failure_recovery.py`.
- **`port already in use` / address in use** — another process holds 8770 (or
  5173). Stop the previous `local-live` server, or set a different backend port
  with the `STORYTIME_LOCAL_LIVE_PORT` environment variable and point the
  frontend's base-URL field at the new loopback URL.
- **Frontend shows "Backend Unavailable"** — the backend is not running, or the
  base URL is wrong. Confirm terminal 1 shows the server on
  `http://127.0.0.1:8770`, and that the base-URL field is a loopback origin.
- **CORS / origin rejected** — the API allows only loopback origins
  (`127.0.0.1` / `localhost`) on the dev ports. Open the frontend at
  `http://localhost:5173` (not a LAN IP or hostname); the API never uses
  wildcard CORS.

## The pipeline

A run moves a source text through five canonical stages — **ingest →
synthesize → assemble → publish**, with operator **approval** gates woven in —
persisting every step to a SQLite state database and to versioned, hashed
artifact envelopes.

    uv run storytime version
    uv run storytime doctor                       # environment + dependency check
    uv run storytime validate-manifest path/to/manifest.json
    uv run storytime run --manifest sources/the-raven.json --auto-approve
    uv run storytime status <pipeline_run_id>     # run state from SQLite
    uv run storytime --help                       # full command surface

**Approval and resume are real.** `run --require-approval` (and
`--require-audio-approval`) pause a run at a persisted gate; the process exits
cleanly. `storytime approve <run> --decision approve|reject` records the
operator decision, and `storytime run --resume` (or the per-stage commands
`ingest` / `synthesize` / `assemble` / `publish`) rehydrate the run from SQLite
and carry it forward — completed-stage artifacts are hash-verified, never
regenerated.

## Serving the feed

    uv run storytime serve            # loopback-only, range-capable HTTP server

`serve` exposes the feed directory over a local `127.0.0.1` HTTP server that
honours byte-range requests (`206 Partial Content`), so a real podcast client
can stream episode audio. It binds loopback only and never serves outside the
local host.

## Operator report

    uv run storytime report generate                       # -> operator-report/
    uv run storytime report generate --output my-report    # custom directory

`report generate` writes a static, local, read-only HTML operator report from
the SQLite state database and on-disk artifacts — `index.html`, `runs.html`,
one `run-<run_id>.html` detail page per run, and a local `style.css`. Open
`index.html` directly in a browser; no web server is required and the report
renders with no network connection. The report is read-only — it shows what
each run did and what governance recorded, and contains no control that
changes state. It is generated runtime output (git-ignored, like `runs/`). See
`docs/operator-report.md` for what the report includes and excludes.

## Operator queue

    uv run storytime queue                       # runs needing attention
    uv run storytime queue --status failed       # filter by attention reason
    uv run storytime queue --run-id <run_id>     # restrict to one run
    uv run storytime queue --json                # machine-readable output

`queue` prints a read-only, bounded, terminal-native list of the pipeline runs
that need operator attention — failed, blocked by governance, marked
needs-review, or awaiting an operator approval decision. For each run it shows
why it needs attention and which existing command, report, or artifact to look
at next. It is a viewer only — it changes no state, runs no other command, and
needs no web server. Output is most-recently-updated first and deterministic;
`--limit` defaults to 20. See `docs/operator-queue.md` for the statuses it
surfaces and the fields it displays.

## Operator re-run

> Phase 10D — Pipeline Re-Run / Mutation Actions — locked.

    uv run storytime rerun <run-id> --dry-run    # preview eligibility only
    uv run storytime rerun <run-id>              # apply the re-run reset
    uv run storytime rerun <run-id> --json       # machine-readable output

`rerun` is StoryTime's first operator *mutation* command. It re-runs a failed
pipeline run, but only when it can prove that is safe: the run must exist, be
failed because of a genuine stage failure (not an operator approval-gate
rejection), and carry an `APPROVED` Trust Envelope. When eligible, it performs
one bounded mutation — resetting the run's status to the resumable state — and
writes an audit record; you then run `storytime run --resume <run-id>` to
re-execute the run from the failed stage. `--dry-run` previews the decision and
changes nothing. An ineligible run is rejected with a clear reason and a
non-zero exit code. `rerun` adds no broker, worker, daemon, scheduler, server,
dashboard, or automatic retry loop, and never bypasses governance. See
`docs/operator-rerun.md` for the eligibility rules and the audit trail.

## Portfolio & demo documentation

For explaining, demonstrating, and handing off StoryTime:

- `docs/portfolio-narrative.md` — what StoryTime is, why it matters, and what
  the Phase 10 operator-experience work demonstrates.
- `docs/portfolio-demo-narrative.md` — the Phase 12C concise demo narrative:
  the 5–10 minute public-presentation account (business problem, architecture,
  observability value, governance posture, SE / Dynatrace-style credibility,
  and the intentional out-of-scope boundaries).
- `docs/portfolio-overview.md` — the Phase 12A plain-English portfolio overview
  (the entry point for a reviewer deciding whether to look closer).
- `docs/solutions-engineer-narrative.md` — how to explain StoryTime in an
  interview: 30-second / 2-minute / deep pitches plus business, observability,
  OpenTelemetry, and governance framings.
- `docs/demo-talk-track.md` — the Phase 12C spoken walkthrough script at
  5-minute, 10-minute, and 20-minute lengths, with interviewer Q&A pivots and a
  "what to say if the demo cannot be run live" fallback.
- `docs/portfolio-demo-script.md` — a narrated, reviewer-facing demo
  walkthrough (defers to `docs/demo.md` for authoritative commands).
- `docs/interview-talking-points.md` — concise, study-friendly talking points,
  one per topic, each backed by something concrete in the repository.
- `docs/interview-story-bank.md` — the Phase 12C reusable interview answer
  frames for the standard Solutions-Engineer / observability project-interview
  questions, each with an honesty checklist.
- `docs/portfolio-evidence-index.md` — the Phase 12B claim-to-evidence index:
  each portfolio claim mapped to the test, config, source file, or document
  that backs it.
- `docs/se-interview-evidence-matrix.md` — the Phase 12B Solutions-Engineer
  competency-to-evidence matrix: each SE competency mapped to where it is
  demonstrated and how to talk about it honestly.
- `docs/public-repository-readiness.md` — the Phase 12C checklist and
  guardrails for preparing the repository for public viewing (public-safe
  README check, secrets/config check, demo-data check, screenshot-placeholder
  check, known-limitations check, and "do not publish until verified" hard
  gates).
- `docs/final-portfolio-handoff.md` — the Phase 12D cold-reader handoff: a
  current-state snapshot, 5-minute / 15-minute / deep-architecture reviewer
  paths, a suggested demo flow, an evidence map, explicit limitations, and the
  next-phase boundary.
- `docs/phase12-closure-plan.md` — the Phase 12D plan that defines the Phase 12
  closure criteria, the completed Phase 12A–12C asset inventory, the
  closure-readiness checklist, and the recommendation on closing Phase 12.
- `docs/phase12-final-review-checklist.md` — the Phase 12D checklist a reviewer
  uses to decide whether Phase 12D can lock and whether Phase 12 can close.
- `docs/phase13-portfolio-website-architecture.md` — the Phase 13A architecture
  baseline: the portfolio website and decoupled operator GUI designed on paper
  (purpose, end-state vision, audiences, information architecture, local-first
  and future-cloud rules, success criteria). Phase 13A designs; it does not
  build.
- `docs/frontend-backend-contract.md` — the Phase 13A "backend owns truth,
  frontend owns understanding" data contract: read-model categories, future
  action categories, the actions disabled for this round, and candidate
  data-source options.
- `docs/phase13-roadmap.md` — the Phase 13A–13G subphase decomposition, with
  each subphase's objective, allowed and forbidden scope, acceptance criteria,
  and review gate.
- `docs/portfolio-website-content-model.md` — the Phase 13A website section
  inventory mapped to existing repository source documents, with a
  content-honesty checklist.
- `docs/operator-gui-view-model.md` — the Phase 13A operator-GUI view
  inventory: views, disabled and future actions, empty / error / loading
  states, and accessibility requirements.
- `docs/demo-reviewer-checklist.md` — the Phase 12B reviewer wrapper for
  running the demo (a pre-flight and what-to-look-for index over `docs/demo.md`,
  not a duplicate command script).
- `docs/portfolio-public-copy.md` — the Phase 12B disciplined, non-hype
  public-facing copy (short / medium / long descriptions and an honest
  "what it is not" scope statement).
- `docs/demo.md` — the operator demo runbook (the `demo/` fixtures).
- `docs/demo-script.md` — a step-by-step presentation demo script.
- `docs/operator-experience-walkthrough.md` — how the report, queue, and rerun
  surfaces compose into one workflow.
- `docs/command-reference.md` — the operator CLI, with explicit mutation
  boundaries.
- `docs/known-limitations.md` — honest boundaries and non-goals.
- `docs/observability-governance-talking-points.md` — the technical story in
  interview/portfolio language.
- `docs/phase10-acceptance-checklist.md` — the Phase 10 closure checklist.
- `docs/screenshot-instructions.md` — a manual evidence-capture checklist.

## Release-candidate hardening & reproducibility

For setting up, validating, and reproducing StoryTime from a fresh clone
(Phase 11A baseline, Phase 11B verification), for the failure-mode /
regression posture (Phase 11C), and for the release-candidate evidence index
(Phase 11D). Phase 11 — Release Candidate Hardening — is **CLOSED**; these
documents remain the reference for the hardened release-candidate state:

- `docs/release-candidate-hardening.md` — the release-candidate hardening
  baseline overview and the dependency policy.
- `docs/phase11-plan.md` — the Phase 11 subphase decomposition (11A–11D).
- `docs/fresh-clone-checklist.md` — the fresh-clone setup path at a glance.
- `docs/local-setup-runbook.md` — the step-by-step local setup runbook.
- `docs/operator-reproducibility-checklist.md` — the step-by-step verification
  path, paired with the reference results Phase 11B observed.
- `docs/fresh-clone-troubleshooting.md` — common fresh-clone setup failures and
  their safe responses.
- `docs/rc-validation-checklist.md` — the six canonical Docker-free validation
  gates and their expected results.
- `docs/security-secrets-checklist.md` — the local-first security and secrets
  baseline.
- `docs/demo-reproducibility-checklist.md` — reproducing the demo fixtures
  without generated audio or external APIs.
- `docs/failure-mode-regression-hardening.md` — the Phase 11C overview: what
  the failure-mode / regression-hardening round verified.
- `docs/regression-risk-register.md` — the inventory of risky failure /
  regression paths and each one's coverage status.
- `docs/failure-mode-test-matrix.md` — the map from each risky path to the
  tests and validation gates that protect it.
- `docs/operator-failure-response.md` — how a local operator should respond to
  common failure states without bypassing governance or deleting state.

## Local observability (optional)

    mkdir -p logs    # preflight: the Collector bind-mounts ./logs
    docker compose -f docker-compose.observability.yml up -d

Create `./logs` **before** `docker compose up` — the Collector bind-mounts it
for the `filelog` receiver, and a Docker-created directory may be root-owned
and unwritable by the local demo. `make observability-up` and `make demo` do
this preflight automatically.

Then set `STORYTIME_TELEMETRY=otel` (see `.env.example`). Spans go to Jaeger
(UI at http://127.0.0.1:16686); the eight pipeline metrics go through the
Collector to Prometheus and into six provisioned Grafana dashboards
(http://127.0.0.1:3000). Phase 8B adds Loki: the Collector `filelog` receiver
tails the demo's structured log file and routes log lines to Loki, explorable
in Grafana. Telemetry is always optional: with the default `noop` adapter the
pipeline behaves identically. `python -m storytime.demo --log-dir logs` drives
real pipeline scenarios to populate the dashboards and the log stream. See
`docs/observability-demo.md`, `docs/runbook.md`, and `docs/telemetry-map.md`.

## Blue/green deployment

**Option A — per-slot processes (Phase 7A).** Two slot-scoped `storytime`
processes — `blue` and `green` — run side by side, each with its own SQLite
state, feed, and loopback port:

    scripts/run-slot.sh blue  serve     # blue feed on 127.0.0.1:8000
    scripts/run-slot.sh green serve     # green feed on 127.0.0.1:8001

`STORYTIME_DEPLOYMENT_SLOT` scopes the state root to `runs/<slot>` and the
feed to `feed/<slot>`, so blue and green never share a database or feed. See
`docs/deployment-bluegreen-option-a.md`.

**Option B — front door + active-slot switching (Phase 7B).** A stable local
front door — a native Python, loopback-only reverse proxy — sits in front of
the two slots on one fixed port, so consumers never need to know which slot is
live:

    scripts/run-frontdoor.sh                 # front door on 127.0.0.1:8080
    python -m storytime.frontdoor status     # show the active slot
    scripts/switch-slot.sh green             # switch blue -> green
    scripts/switch-slot.sh blue              # roll back  green -> blue

A persisted active-slot pointer (`config/deploy/active-slot`) is the single
source of truth; the front door reads it per request, so a switch takes effect
with no proxy reload. No external proxy binary is required and nothing is
installed or downloaded. Switching/rolling back changes routing only — it
never merges or migrates slot state. See
`docs/deployment-bluegreen-option-b.md`.

**Optional containerized slots (Phase 7C.1 / 7D).** The blue and green slots
can optionally run as local Docker containers instead of bare-metal processes,
under the locked Phase 7C / 7C.1 Architecture Baseline amendment:

    docker compose -f docker-compose.app.yml build      # build the shared image once
    docker compose -f docker-compose.app.yml up -d       # start blue + green

`up -d` also builds the image itself if it is missing, so a fresh machine can
skip the explicit `build`. One service builds the shared `storytime-app:local`
image and the other consumes it, so the standard commands work without any
per-service workaround. Each slot gets a per-slot named volume for its SQLite
state and feed; ports stay loopback-only; the front door stays a host process.
This is **optional** and **demo-grade** — bare-metal remains the default, the
six quality gates need no Docker, and there is no cloud, registry, Kubernetes,
or Terraform. See `docs/deployment-containerized.md`.

The switch is scripted but operator-initiated — there is no automated traffic
cutover and no production zero-downtime claim.

## Development

    uv run pytest          # full test suite
    uv run ruff check .    # lint
    uv run mypy            # strict type check
    uv run lint-imports    # import-boundary contracts (import-linter)

A `Makefile` wraps these as `make test`, `make lint`, `make typecheck`,
`make imports`, and `make check` (all of them).

## Architecture in one paragraph

Each CLI invocation works against a SQLite state database (WAL mode) that —
together with on-disk artifact envelopes — is the source of truth. Stages
communicate only through versioned, hashed artifact envelopes; they never call
each other and never share mutable state. The `PipelineRunner` is the only
orchestrator. OpenTelemetry is a *view* over the local truth and is confined to
`adapters/telemetry`. See `docs/architecture-baseline.md` for the full design
and `docs/canonical-state.md` for the locked decision log.

## Repository layout

    src/storytime/
      cli/         command-line interface (Typer)
      runner/      RunnerContext + PipelineRunner
      stages/      the five concrete pipeline stages + approval gate
      dto/         StageInput / StageResult / StateUpdate
      artifacts/   versioned inter-stage artifact envelope
      manifest/    closed-schema source manifest validation
      state/       SQLite schema, migrations, StateStore
      events/      internal data-only event model
      adapters/    telemetry / tts / storage adapters
      rss/         RSS 2.0 + iTunes feed builder
      http/        loopback-only, range-capable local serving
      frontdoor/   blue/green front door — native Python reverse proxy (Phase 7B)
      demo/        bounded demo harness that drives real pipeline scenarios
      util/        ids, hashing, clock
    tests/         unit, integration, and boundary tests
    docs/          locked planning artifacts + living docs
    demo/          demo seed data + golden-path fixtures (see docs/demo.md)
    config/        storytime.toml, otel-collector.yaml, grafana/, deploy/
    scripts/       run-slot.sh, run-frontdoor.sh, switch-slot.sh
