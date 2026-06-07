> **Phase 14C.5.1 — Durable Recovery Control Plane Boundary (current sub-phase; implementation candidate; pending review; NOT locked).** Phase 13 is CLOSED; **Phase 14A.1, 14B.1, 14C.1, 14C.2, 14C.3, and 14C.4 are LOCKED** (14C.4 is the last locked phase; locked via `storytime-phase14c4-minimal-observability-boundary-queue-worker.tar.gz`, SHA-256 `12b951e0a9b6b17f5c73aacf0d055b257bd4a715908f7f5078d401eae2a66d3b`). Phase 14 — Live System / Cloud-Distributed — is STARTED. Phase 14C.5.1 adds the smallest durable, backend-owned recovery control plane: a durable `recovery_action` lineage table (source of truth) linking an original failed execution to a bounded recovery execution, a backend-owned recovery eligibility policy, duplicate-prevention and a bounded attempt limit, a recovery read-model projection, local SQLite concurrency guardrails, and a cloud-queue mapping CONTRACT document. The Phase 14C.4 observer events are explanatory only and are NOT the recovery-lineage source of truth. It does not expand the Phase 14C.4 observer event schema and changes no queue/worker or ArtifactStore semantics. It absorbs the previously planned Phase 14C.5 through Phase 14C.10 local recovery-control-plane scope (historical labels only). No cloud queue, external broker, dead-letter queue, automatic retries, exponential backoff, retry scheduler, distributed worker, cloud lease, distributed lock, cloud object store, provider TTS, audio, RSS, or auth exists yet. Phase 14D / 14E remain **NOT STARTED**.

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

# Phase 10G lock closure note — Phase 10 CLOSED

**Date:** 2026-05-25
**Locked artifact:** `storytime-phase10g1-uvlock-reversion-cleanup.tar.gz`
**SHA-256:** `8a0cc9a5b6426a291bec3a793e41501c7d3492187dd48b4f7729ea95e501a0c1`
**Status:** Phase 10G — Portfolio Narrative / Phase 10 Closure is **LOCKED / ACCEPTED / CANONICAL**. **Phase 10 is formally CLOSED.**
**Last locked phase:** Phase 10G — Portfolio Narrative / Phase 10 Closure.
**Next phase:** Phase 11 — Release Candidate Hardening *(Phase 11 has since been completed and is CLOSED — Phase 11A through 11D all locked; Phase 12 — Portfolio / SE Demo Packaging — has since been completed and is CLOSED — Phase 12A through 12D all locked; Phase 13 — Portfolio Website / Operator GUI — is now STARTED. See the "Recovered current state" section below for the authoritative current status)*.

Phase 10G — the documentation, portfolio-narrative, demo-explanation, and Phase 10 closure phase — is locked. It added the Phase 10 portfolio/closure documents (`docs/portfolio-narrative.md`, `docs/demo-script.md`, `docs/operator-experience-walkthrough.md`, `docs/command-reference.md`, `docs/known-limitations.md`, `docs/observability-governance-talking-points.md`, `docs/phase10-acceptance-checklist.md`, `docs/screenshot-instructions.md`) and synchronized the State Preservation Bundle. It was documentation-first: no new product feature, no UI, no server, no generated audio committed, no JavaScript, no screenshots/binary assets, no new dependency, and no change to pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, or the database schema. Phase 10G completed the Phase Closure Protocol and was locked with explicit user approval. With Phase 10G locked, **Phase 10 — Product UI / Operator Experience — is formally CLOSED** (Phases 10A–10G all locked); the next phase is **Phase 11 — Release Candidate Hardening**, not started. This note was synchronized by the Post-Phase-10 Closure State Synchronization task.

*(The Phase 10F lock closure note and the Phase 10C lock closure note below are historical records. Phase 10A, 10B, 10C, 10C.1, 10D, 10D.1, 10E — with the 10E.1 / 10E.2 cleanup sequence — 10F, and 10G are all locked; Phase 10 is closed.)*

---

# Phase 10F lock closure note

**Date:** 2026-05-25
**Lock archive:** `storytime-phase10f-demo-seed-data-golden-path-fixtures.tar.gz`
**SHA-256:** `e060570a94fb19f790c539542b3ef7445111430bc308668675548f66fa48df55`
**Status:** Phase 10F — Demo Seed Data / Golden Path Fixtures is **LOCKED / ACCEPTED / CANONICAL**.

Phase 10F added curated demo seed data and golden-path fixture scenarios — the `demo/` directory (four original CC0 seed texts plus schema-valid manifests, a demo-only blocked-source deny-list, and six fixture definitions), the `docs/demo.md` operator runbook, and `tests/test_demo_fixtures.py`. It was fixture / demo-readiness work that exercises the existing system: no new product feature, no UI, no server, no generated audio committed, no JavaScript, no new dependency, and no change to pipeline behaviour, `storytime rerun`, Trust Envelope enforcement, or the database schema. Phase 10F completed the Phase Closure Protocol and was locked with explicit user approval.

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

# RoundTable Import Bridge

## Purpose

This document allows GPT-5.5 to reconstruct RoundTable state from the
repository artifact if RoundTable state is lost, stale, or contaminated. Until
RoundTable is restored, the repository archive plus the State Preservation
Bundle is the portable project memory. Read `LLM_DIRECTOR.md` first.

## Import mode

- Preferred: generate a RoundTable JSON import from this document and the State
  Preservation Bundle.
- Fallback: manually recreate project state using the sections below.
- **Do not replay stale or superseded RoundTable rounds.**
- **Prefer the repository State Preservation Bundle if it contains a newer
  explicit recovery checkpoint than RoundTable.** It does — see "Recovered
  current state".

## Project identity

- Project name: StoryTime
- Former name: Podcast Pipeline
- Project description: a local-first, CLI-driven, observability-native
  content-to-audio pipeline that converts approved CC0 / US-public-domain text
  into podcast-ready audio, an RSS feed, and a traceable record of every run.
  SQLite plus on-disk artifact envelopes are the source of truth; OpenTelemetry
  is an optional view. Built as a portfolio-grade OpenTelemetry / cloud-native
  demo and a proving ground for the Kaname / RoundTable workflow.
- Current phase: **Phase 13 — Portfolio Website / Operator GUI — is STARTED.** Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment — is the current subphase: an implementation candidate, pending review, **not locked**. Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — is locked and is the last locked phase; Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — is also locked. Phase 12 — Portfolio / SE Demo Packaging — is CLOSED (Phase 12A through 12D all locked; Phase 12A.1 and Phase 12B.1 / 12B.2 / 12B.3 are folded into their parent lock lineages as accepted cleanup sub-rounds). Phase 10 — Product UI / Operator Experience — is CLOSED (2026-05-25) and **Phase 11 — Release Candidate Hardening — is CLOSED** (Phase 11A through 11D all locked); `docs/architecture-baseline.md` Section 24 (governance) and Section 25 (operator experience) are canonical. Phase 13 is not closed. Phase 13D and every later Phase 13 subphase have not started — they are future, planned work, decomposed in `docs/phase13-roadmap.md`.
- Last locked phase: **Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold**, locked under the Phase Closure Protocol (GPT-5.5 review, then Gemini SAFE TO LOCK with no required edits, then an explicit user lock decision); locked artifact `storytime-phase13b-typed-static-portfolio-shell-minimal-visual-pipeline-scaffold.tar.gz` (SHA-256 `9319ece26f5b457ddbbefaab346aba61cb61f65a6b7b729b5acaa12f30df3f24`). It is the second subphase of Phase 13 and the source/base artifact for Phase 13C. Phase 13A — Portfolio Website / Operator GUI Architecture Baseline — is also locked (artifact `storytime-phase13a-portfolio-website-operator-gui-architecture-baseline.tar.gz`, SHA-256 `100098aa6280b740a6eeb862c1e1923d2e031bd02a06786b7a8b8ec07facf1c0`). Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition — is also locked (artifact `storytime-phase12d-phase12-closure-plan-final-portfolio-handoff.tar.gz`, SHA-256 `64ad09e875f0653608e0deb756f11ee5adc0d2ff1265e2039cbc51491f286cf8`); with Phase 12D locked, **Phase 12 — Portfolio / SE Demo Packaging — is CLOSED**. Phase 12C — Portfolio Demo Narrative / Public Presentation Kit — is also locked (artifact `storytime-phase12c-portfolio-demo-narrative-public-presentation-kit.tar.gz`, SHA-256 `4c98a25d6bb0ae751b4ba33851bc60e7d7805d4fd31ebcfc45c2d30a659301da`), as is Phase 12B (lineage `storytime-phase12b3-residual-state-wording-cleanup.tar.gz`, SHA-256 `ce0fb2d1bea4eaa636be7796613f9a9aa56cba4b8bf34c0ae5440c3509de4a45`) and Phase 12A (lineage with `storytime-phase12a1-state-hygiene-cleanup.tar.gz`, SHA-256 `5f9eca1cc8c2efb55d57f87becdc53cd0d8e514221947e445965232f608b621a`). Phase 11D — Release Candidate Evidence Pack — is locked (SHA-256 `07a3973e3dbb69d760ff2c330418f85101c2afa1464fc0eed752fc7053894d94`); with Phase 11D locked, **Phase 11 — Release Candidate Hardening — is CLOSED**. The locked phase that closed Phase 10 was Phase 10G — Portfolio Narrative / Phase 10 Closure (locked artifact `storytime-phase10g1-uvlock-reversion-cleanup.tar.gz`, SHA-256 `8a0cc9a5b6426a291bec3a793e41501c7d3492187dd48b4f7729ea95e501a0c1`).
- Last locked work item before Phase 11: **Post-Phase-10 Historical State Reconciliation** — a documentation/state-history checkpoint between Phase 10 closure and Phase 11 start (not a new phase), locked 2026-05-25; locked artifact `storytime-post-phase10-roundtable-historical-backfill.tar.gz` (SHA-256 `367e647c46aa6e4fd039369da30859b11ca783249569df291343db133ef4cfdd`).
- Next required action: **submit the Phase 13C artifact (`storytime-phase13c-deterministic-read-only-static-export-frontend-data-alignment.tar.gz`) for GPT-5.5 review and Gemini critique under the Phase Closure Protocol, then an explicit user decision** — before locking Phase 13C. Do not mark Phase 13C locked, do not mark Phase 13 closed, and do not begin Phase 13D (or any later Phase 13 subphase, or any further frontend / operator-GUI view expansion) without the Phase Closure Protocol and an explicit gate. Phase 13C is a deterministic, read-only static data-boundary round; the later Phase 13 subphases (13D–13G) follow only after their own review gates. Do not re-open any locked phase (0–11D, 12A, 12B, 12C, 12D, 13A, 13B) and do not re-run the Post-Phase-10 Historical State Reconciliation or re-import the RoundTable JSON. Phase 9C remains optional and not scheduled.



## Canonical source files

- `LLM_DIRECTOR.md`
- `docs/handoff-state.md`
- `docs/canonical-state.md`
- `docs/phase-history.md`
- `docs/roadmap.md`
- `docs/open-issues.md`
- `docs/architecture-baseline.md`
- `docs/product-charter.md`
- `docs/phase-closure-protocol.md`
- `docs/verification-log.md`
- `docs/artifact-manifest.md`

## Model roster

- GPT-5.5 Thinking — Mediator / Architect / State Keeper / Prompt Engineer /
  Reviewer
- Claude Opus 4.7 — Chief Implementation / Hardening Engineer
- Gemini 3 Thinking — Independent Critic / Architecture Reviewer
- Claude Sonnet 4.6 — bounded cleanup only when explicitly directed

## Workflow rules

- Implementation output is not phase completion.
- GPT-5.5 reviews implementation; Gemini critiques it; the user explicitly
  approves a phase lock.
- Cleanup occurs only if blockers or targeted issues exist.
- Canonical state updates are append-only unless correcting a known error;
  corrections are labeled, never silent deletions.
- Architecture Baseline changes require an explicit, user-approved amendment
  routed through RoundTable — never an implementation-level change.
- Do not replay stale or superseded RoundTable rounds.

## Recovered current state

StoryTime is a working end-to-end local pipeline: ingest → synthesize →
assemble → publish, with persisted operator approval gates, resume/rehydration
from SQLite, multi-item RSS publishing, a range-capable loopback feed server,
an OpenTelemetry instrumentation foundation, an observability stack with
dashboards-as-code and a demo harness, and a local blue/green deployment path
that can optionally run as local containers.

This is the current recovery checkpoint. **Phase 8 is complete** — Phase 8A
(Architecture Baseline §23), Phase 8B / 8B.1 (local multi-backend stack
expansion + `./logs` preflight), and Phase 8C / 8C.1 (optional vendor export
profiles) are all locked with explicit user approval. **Phase 9A — Governance
Baseline Amendment is locked** — `docs/architecture-baseline.md` **Section
24**, "Governance Baseline (Trust Envelope, Licensing, Fail-Closed Gating)", is
canonical architecture law. Section 24 defines StoryTime's governance law
before Phase 9B implements it: StoryTime is not a legal rights-clearance
engine and the human operator is the source of truth for licensing decisions;
governance is source authorization, not viewpoint acceptability (StoryTime
governance is not a content-moderation system); no legal automation / legal
hallucination; the allowed and disallowed source categories; a fail-closed
gate that should check governance as early as practical and must hard-block
before TTS, audio processing, or RSS publish unless an `APPROVED` Trust
Envelope exists; the Trust Envelope concept and its canonical minimum schema;
the local blocked-source-config direction; the reinforced secrets policy; an
honest local-first deletion/retention posture; carried-forward
telemetry/privacy hygiene; public/demo disclaimers; the future
legal-hallucination grep/regex gate; and the Phase 10 dependency contract.
Phase 9A completed the Phase Closure Protocol — authored by Opus, reviewed by
GPT-5.5, reviewed by Gemini (`SAFE WITH EDITS`, the two edits folded in by the
Phase 9A.1 cleanup), locked with explicit user approval (2026-05-24). **Phase
9B — Minimal Trust Envelope Implementation has been implemented and delivered
as a candidate (2026-05-24)**: the `storytime.governance` package (Trust
Envelope model + canonical §24.8 closed schema), the durable Trust Envelope
artifact (`governance/trust-envelope.json`, the governance source of truth),
the rebuildable `trust_envelope` SQLite projection (schema migration `0005`),
the fail-closed gate wired into `ingest` (early check), `synthesize` (hard
block before TTS), and `publish` (hard block before RSS), the local
`config/governance/blocked-sources.yaml` deny-list, and the static
legal-hallucination grep/regex gate. It implements exactly the locked Section
24 law, changed no ARCH-LOCKed contract, and added no legal automation or
overclaiming. The **Phase 9B.1 cleanup** (2026-05-24) hardened the static
forbidden-term scanner — per Gemini's `SAFE WITH MINOR CLEANUP` review — so it
cannot crash on binary/generated files or descend into
cache/virtualenv/`runs`/`feed` directories; it changed only the scanner, its
test, and the State Preservation Bundle docs. **Phase 9B completed the Phase
Closure Protocol and is locked with explicit user approval (2026-05-24)**, with
the Phase 9B.1 cleanup folded into the lock.

**Phase 10A — Operator Experience Baseline Amendment is locked (2026-05-24).** Phase 10A locked `docs/architecture-baseline.md`
**Section 25**, "Operator Experience Baseline" — canonical operator-experience law. It is architecture/documentation only and authorizes no implementation by itself; it is **locked / accepted / canonical** after GPT-5.5 verification, Gemini critique, and explicit user approval. Section 25 defines
the Phase 10 operator-experience law: the operator experience goal (a single
local operator; no SaaS personas); the read-only-first rule; the
source-of-truth rule (SQLite + artifact envelopes + the durable Trust Envelope
stay authoritative; reports and observability dashboards are projections/links,
never truth); the governance display rule (allowed bounded fields vs a
forbidden legal/compliance overclaiming vocabulary; a standing "record of a
human decision, not legal advice" disclaimer); the viewpoint-neutrality
carryover; the Phase 10B target (a generated, static, local, read-only HTML
operator report) with a hard floor and hard ceiling; the report data model and
field allowlist/blacklist; the bounded `review_context_summary` rule; the
observability-link rule; the determinism/snapshot, privacy/no-raw-content, and
governance-copy-linting test requirements; a performance guardrail; the Phase
10B handoff section; the no-auth/no-cloud/no-server and mutation-gate rules;
the stop/revert criterion; and the Phase 10A / 10B / 10C / 10D split.

**Phase 10B — Generated Local HTML Operator Report is locked / accepted /
canonical (2026-05-24).** Phase 10B is the first implementation phase of
Phase 10, implementing the locked Section 25 law. It added the
`storytime.reporting` package and the `storytime report generate` CLI command,
which writes a static, local, read-only, air-gapped HTML operator report from
the existing SQLite state and artifact envelopes. The corrected Phase 10B lock
record states that Phase 10B added **no Jinja2 and no new dependency**, that
HTML rendering uses the Python standard library and `html.escape`, and that
`uv.lock` remained byte-identical to Phase 10A.

**Phase 10D — Pipeline Re-Run / Mutation Actions: locked (2026-05-25). Phase 10D.1 — State Preservation Cleanup + LLM Director Hardening: locked.** Phase 10D adds StoryTime's first operator *mutation* surface — the `storytime.operator_rerun` module and the governed `storytime rerun` command, a bounded, audited re-run of a failed pipeline run gated on Trust Envelope governance. The mutation is a single bounded status reset (`failed` -> `running`); every actual mutation writes a `RunRerunRequested` audit event. Phase 10D made no database schema change, added no dependency, and added no broker/worker/daemon/scheduler/server/dashboard/auth/cloud; 27 new tests and all six Docker-free gates pass. Phase 10D is locked. Phase 10E — Static HTML Operator Report Refinement — is locked (2026-05-25), with the Phase 10E.1 / 10E.2 cleanup sequence accepted. Phase 10F — Demo Seed Data / Golden Path Fixtures — is locked (2026-05-25). Phase 10G — Portfolio Narrative / Phase 10 Closure — is locked (2026-05-25); with it, Phase 10 — Product UI / Operator Experience — is formally CLOSED.

**Phase 10C — Operator CLI Helpers / Failure Queue is locked / accepted / canonical (2026-05-25).** Phase 10C implemented the locked Section 25 law as a read-only command-line failure / review queue. It added the new
`storytime.operator_queue` standard-library module — the `QueueItem` bounded
projection, a `collect_queue` semantic query over the existing SQLite
run/stage/Trust-Envelope state, and plain-text and deterministic-JSON
renderers — and the read-only `storytime queue` CLI command with `--status`,
`--run-id`, `--limit`, and `--json` flags. The command surfaces the runs
needing operator attention — failed, blocked by governance, marked
needs-review, or awaiting an operator approval decision — with, per run, why it
needs attention and which existing command/report/artifact to inspect next.
The queue is a viewer: it adds no message broker, background worker, new queue
storage, new run state, or `pop`/`dequeue`/`claim`/`ack` behaviour; it mutates
nothing and runs no other command. It is bounded (`--limit` defaults to 20)
and deterministic (no generation timestamp), and surfaces only structured
fields — the `error_kind` code, never the free-text `error_message`; the
§24.8 decision enum, never the free-text `blocked_reason`. Phase 10C made no
database schema change, changed no ARCH-LOCKed contract, and added no
dependency; 29 new tests and all six Docker-free gates pass. Per the Phase
Closure Protocol Phase 10C is implementation output — **a candidate, not a
locked phase** — pending GPT-5.5 review, Gemini critique, any cleanup, and
explicit user approval. *(Historical status before Phase 10D implementation;
superseded by Phase 10D implementation candidate status — see current-state
section at the top of this file.)* Phase 9C — Docs / Audit
Polish — was an optional follow-up and is not scheduled.

This checkpoint is newer than any RoundTable round text from the contaminated
Phase 7 sequence; prefer it.

## Phase lock ledger

| Phase | Artifact | Review status | Gemini status | Lock basis | Carryovers |
|-------|----------|---------------|---------------|------------|------------|
| 0 — Product Charter | `docs/product-charter.md` | reviewed | reviewed | locked (user approval) | — |
| 1 — Architecture Baseline | `docs/architecture-baseline.md` | reviewed | reviewed | locked (user approval) | — |
| Phase Closure Protocol | `docs/phase-closure-protocol.md` | reviewed | reviewed | locked (user approval) | — |
| 2 — Repo scaffold | (archive lineage) | reviewed | reviewed | locked | — |
| 3 — Thin vertical slice | (archive lineage) | reviewed | reviewed | locked | OI-12 (closed P4) |
| 4 / 4.1 — Approval gates + resume | (archive lineage) | reviewed | reviewed | locked | OI-9/10/12/13/14 closed |
| 5 — OpenTelemetry foundation | (archive lineage) | reviewed | reviewed | locked | OI-2 closed |
| 6S — Serving + multi-item feed | (archive lineage) | reviewed post-impl | reviewed | locked (reclassified out-of-band exec, accepted) | OI-7/11 closed |
| 6A — Observability infra/dashboards/harness | (archive lineage) | reviewed | reviewed | locked | OI-16 closed |
| 6B — SLO/runbook/demo docs | (archive lineage) | reviewed | reviewed | locked (documentation-only) | — |
| 7A — Blue/Green Option A | `storytime-phase7a-bluegreen-option-a.tar.gz` | reviewed | reviewed | locked | OI-17 closed |
| 7B — Higher-Assurance Front Door / Active-Slot Switching | `storytime-phase7b-bluegreen-frontdoor-switching.tar.gz` | reviewed | reviewed | locked | OI-18 closed |
| 7C / 7C.1 — Architecture Baseline Amendment for App Containerization | `RT_RESPONSE_StoryTime_Phase7C1_architecture_baseline_amendment_revised.md` | reviewed | SAFE WITH EDITS → edits applied | locked (amendment, user approval) | — |
| 7D — Optional Local App Containerization | `storytime-phase7c1-app-containerization.tar.gz` | reviewed | reviewed | locked (user approval; live Docker smoke-tested) | OI-19 closed |
| 7D.1 — Operational Cleanup: Compose Build Race Fix | `storytime-phase7d1-compose-build-fix.tar.gz` | reviewed | reviewed | locked (user approval; live Docker smoke-tested, Windows Docker Desktop / WSL2) | OI-20 closed |
| 8A — Architecture Baseline Amendment (Collector-Owned Multi-Backend Telemetry Fan-Out) | `docs/architecture-baseline.md` §23 (`storytime-phase8a-locked-state-bundle.tar.gz`) | reviewed (clean) | `SAFE TO LOCK` | locked (amendment, user approval) | — |
| 8B — Local Multi-Backend Stack Expansion | `storytime-phase8b-local-multi-backend-stack.tar.gz` | reviewed (clean, in scope) | `SAFE WITH MINOR CLEANUP` | locked (user approval, 2026-05-24) | OI-21 opened |
| 8B.1 — Operational cleanup: logs-directory preflight | `storytime-phase8b1-logs-preflight-cleanup.tar.gz` | applies the 8B review cleanup | — | locked (folds into the Phase 8B lock) | — |
| 8C — Optional Vendor Export Profiles | `storytime-phase8c1-vendor-profile-split.tar.gz` | reviewed (clean) | `SAFE WITH EDITS` → 8C.1 cleanup applied → Gemini `SAFE TO LOCK` | locked (user approval, 2026-05-24) — completes Phase 8; 8C.1 accepted as part of the lock | OI-22 opened |
| 9A / 9A.1 — Governance Baseline Amendment (Trust Envelope / licensing / fail-closed gating) | `docs/architecture-baseline.md` §24 (`storytime-phase9a-locked-state-bundle.tar.gz`) | reviewed (docs-only, review-ready) | `SAFE WITH EDITS` → 9A.1 cleanup folded in the two clarifications | locked (amendment, user approval, 2026-05-24) | — |
| 9B — Minimal Trust Envelope Implementation | `storytime-phase9b-minimal-trust-envelope-implementation.tar.gz` | reviewed (ready for Gemini) | `SAFE WITH MINOR CLEANUP` → 9B.1 cleanup applied | **locked (user approval, 2026-05-24) — 9B.1 folded into the lock** | none opened/closed |
| 9B.1 — Forbidden-Term Scanner Hardening Cleanup | `storytime-phase9b1-forbidden-scanner-hardening.tar.gz` | applies the Gemini `SAFE WITH MINOR CLEANUP` item | — | **folds into the Phase 9B lock** | none opened/closed |
| 10A — Operator Experience Baseline Amendment | `docs/architecture-baseline.md` §25 (`storytime-phase10a-locked-state-bundle.tar.gz`) | verified | `SAFE TO LOCK (PENDING VERIFICATION)` → GPT verification satisfied | **locked (user approval, 2026-05-24)** | none opened/closed |
| 10B — Generated Local HTML Operator Report | `storytime-phase10b-locked-state-bundle-corrected.tar.gz` | verified (scope, gates, report boundaries) | `SAFE TO LOCK` | **locked (user approval, 2026-05-24) — corrected record: no Jinja2, no new dependency, `uv.lock` byte-identical to Phase 10A** | none opened/closed |
| 10C — Operator CLI Helpers / Failure Queue | `storytime-phase10c-operator-cli-helpers-failure-queue.tar.gz` | GPT-5.5 Thinking PASS | Gemini/Flash Light SAFE TO LOCK | **locked (user approval, 2026-05-25)** | none opened/closed |
| 10C.1 — State Preservation Synchronization Cleanup | `storytime-phase10c1-state-preservation-sync.tar.gz` | GPT-5.5 Thinking PASS | docs/state-preservation only | **locked (user approval, 2026-05-25)** | none opened/closed |
| 10D — Pipeline Re-Run / Mutation Actions | `storytime-phase10d-pipeline-rerun-mutation-actions.tar.gz` | SAFE WITH EDITS | SAFE WITH EDITS | **locked** (via Phase 10D.1) | none opened/closed |
| 10E — Static HTML Operator Report Refinement | `storytime-phase10e2-final-cleanup-v2-normalized.tar.gz` | SAFE WITH EDITS → cleared | SAFE WITH EDITS → cleared | **locked (user approval, 2026-05-25)** (10E.1 / 10E.2 cleanup accepted) | none opened/closed |
| 10F — Demo Seed Data / Golden Path Fixtures | `storytime-phase10f-demo-seed-data-golden-path-fixtures.tar.gz` | verified | verified | **locked (user approval, 2026-05-25)** | none opened/closed |
| 10G — Portfolio Narrative / Phase 10 Closure | `storytime-phase10g1-uvlock-reversion-cleanup.tar.gz` | PASS (10G) / PASS (10G.1) | SAFE WITH EDITS (10G) → SAFE TO LOCK (10G.1) | **locked (user approval, 2026-05-25) — closes Phase 10** | none opened/closed |
| Post-Phase-10 Historical State Reconciliation | `storytime-post-phase10-roundtable-historical-backfill.tar.gz` | reviewed | reviewed | **locked (user approval, 2026-05-25)** — last locked work item before Phase 11; not a new phase | — |
| 11A — Release Candidate Hardening Baseline | `storytime-phase11a-release-candidate-hardening-baseline.tar.gz` | reviewed | reviewed | **locked (user approval, 2026-05-25)** | none opened/closed |
| 11B — Fresh Clone / Operator Reproducibility | `storytime-phase11b-fresh-clone-operator-reproducibility.tar.gz` | reviewed | reviewed | **locked (user approval, 2026-05-25)** | none opened/closed |
| 11C — Failure-Mode / Regression Hardening | `storytime-phase11c-failure-mode-regression-hardening.tar.gz` | reviewed | reviewed | **locked (user approval, 2026-05-25)** | none opened/closed |
| 11D — Release Candidate Evidence Pack | `storytime-phase11d-release-candidate-evidence-pack.tar.gz` | GPT-5.5 PASS | Gemini SAFE TO LOCK | **locked (user approval, 2026-05-26) — closes Phase 11** | none opened/closed |
| 12A — Portfolio / SE Demo Packaging Baseline | `storytime-phase12a1-state-hygiene-cleanup.tar.gz` (12A lineage, 12A.1 folded in) | GPT-5.5 reviewed | Gemini critiqued | **locked (user approval, 2026-05-26)** | none opened/closed |
| 12B — Portfolio Evidence Pack / Reviewer Assets | `storytime-phase12b3-residual-state-wording-cleanup.tar.gz` (12B lineage, 12B.1 / 12B.2 / 12B.3 folded in) | GPT-5.5 reviewed | Gemini SAFE TO LOCK (combined 12B sequence) | **locked (user approval, 2026-05-26)** | none opened/closed |
| 12C — Portfolio Demo Narrative / Public Presentation Kit | `storytime-phase12c-portfolio-demo-narrative-public-presentation-kit.tar.gz` | GPT-5.5 reviewed | Gemini SAFE TO LOCK (no required edits) | **locked (user approval, 2026-05-26)** | none opened/closed |
| 12D — Phase 12 Closure Plan / Final Portfolio Handoff Definition | `storytime-phase12d-phase12-closure-plan-final-portfolio-handoff.tar.gz` | GPT-5.5 reviewed | Gemini — lock Phase 12D and close Phase 12, no required edits | **locked (user approval, 2026-05-27) — closes Phase 12** | none opened/closed |
| 12 — Portfolio / SE Demo Packaging (subphases 12A–12D) | (overall phase) | — | — | **CLOSED (user decision, 2026-05-27)** | — |
| 13A — Portfolio Website / Operator GUI Architecture Baseline | `storytime-phase13a-portfolio-website-operator-gui-architecture-baseline.tar.gz` | GPT-5.5 reviewed | Gemini SAFE TO LOCK (no required edits) | **locked (user approval, 2026-05-27)** | none opened/closed |
| 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold | `storytime-phase13b-typed-static-portfolio-shell-minimal-visual-pipeline-scaffold.tar.gz` | GPT-5.5 reviewed | Gemini SAFE TO LOCK (no required edits) | **locked (user approval, 2026-05-27)** | none opened/closed |
| 13C — Deterministic Read-Only Static Export / Frontend Data Alignment | `storytime-phase13c-deterministic-read-only-static-export-frontend-data-alignment.tar.gz` | — | — | implementation candidate — pending review — **not locked** | none opened/closed |
| 13D–13G — Portfolio Website / Operator GUI build subphases | — | — | — | **not started** (future, planned work; decomposed in `docs/phase13-roadmap.md`) | — |

## Artifact lineage

See `docs/artifact-manifest.md` for the full table. Latest and base artifacts:

- Latest archive: `storytime-phase10d-pipeline-rerun-mutation-actions.tar.gz`
  — the Phase 10D implementation candidate: the new `storytime.operator_rerun`
  module, the governed `storytime rerun` CLI command, the `RUN_RERUN_REQUESTED`
  audit event type, `tests/test_operator_rerun.py`, `docs/operator-rerun.md`,
  and the State Preservation Bundle updated. sha256 reported on delivery.
- Prior archive (locked): `storytime-phase10c1-state-preservation-sync.tar.gz`
  — the Phase 10C.1 state-preservation cleanup: first-read documents updated
  to reflect Phase 10C locked status. sha256 reported on delivery.
- Prior archive (locked): `storytime-phase10c-operator-cli-helpers-failure-queue.tar.gz`
  — the Phase 10C implementation candidate, now the locked Phase 10C archive.
  sha256 `e30aaa57f900756e62347ddaac2df658d96065c9e1061679adb31594c73e2543`.
- Prior archive (locked): `storytime-phase10b-locked-state-bundle-corrected.tar.gz`
  — the corrected Phase 10B lock-closure archive: Phase 10B locked / accepted /
  canonical; the record corrects that Phase 10B added no Jinja2 and no new
  dependency. sha256
  `00e6d543ce334fb8be83448f3397510761568af7d4318ab8df4b9bc6ca0e0c59`.
- Prior archive: `storytime-phase10b-generated-local-operator-report.tar.gz`
  — the Phase 10B implementation candidate: the `storytime.reporting`
  package, the `storytime report generate` CLI command,
  `tests/test_operator_report.py`, `docs/operator-report.md`. sha256
  `128d9697185d0ea44431041f0db05d64fba3c763c561aae6d701a9ba8dddca89`.
- Prior archive (locked): `storytime-phase10a-locked-state-bundle.tar.gz`
  — the Phase 10A locked-state bundle: `docs/architecture-baseline.md`
  Section 25 locked / accepted / canonical. sha256
  `d9e6ce79a8bc12b26b48bfc032355b17d1acf46cc610a407cf0f65be3babf8f9`.
- Prior archive (locked): `storytime-phase9b-locked-state-bundle.tar.gz`
  — the Phase 9B lock-closure archive: Phase 9B locked (with the Phase 9B.1
  scanner-hardening cleanup folded in). sha256
  `f7d205959986907a80b101602b6f4a58032a61e0b03ab23256d9b2dc45039a4f`.
- Prior archive: `storytime-phase9b1-forbidden-scanner-hardening.tar.gz`
  — the Phase 9B.1 scanner-hardening cleanup applied on top of the Phase 9B
  implementation candidate. sha256
  `f6fd02bb780521e3bc9d9d64fc7c7a9392aa532b41d9e1cc5d27e66e5dd67608`.
- Prior archive: `storytime-phase9b-minimal-trust-envelope-implementation.tar.gz`
  — the Phase 9B implementation candidate: the `storytime.governance` package,
  the durable Trust Envelope artifact, the `trust_envelope` SQLite projection,
  the fail-closed gate, the blocked-source config, and the static
  legal-hallucination gate. sha256
  `162ad0f49a7ee7e4c21035f4f9f562962a28f407d9887bf8d14110100d3b2a3c`.
- Prior archive: `storytime-phase9a-governance-baseline-amendment.tar.gz` —
  the Phase 9A **candidate** archive (authored, pre-cleanup, pre-lock). sha256
  `bc35f7a1af6764f70b788515bdc842fad5c55a4d9a7ad7f75917a5d23e64fac6`.
- Prior archive (locked): `storytime-phase8c-locked-state-bundle.tar.gz` —
  the Phase 8C / 8C.1 lock-closure archive; Phase 8 complete.
- Prior code archive: `storytime-phase8c1-vendor-profile-split.tar.gz` —
  the **locked** Phase 8C / 8C.1 authoritative code archive (optional vendor
  export profiles, split into two independent per-vendor profiles). sha256
  `b93cc84a473fe71df2ef2f00862c9ab2a7cce019c11da83ec5e738c0818c7f40`.
- Prior archive: `storytime-phase8c-vendor-export-profiles.tar.gz` —
  Phase 8C implementation output before the 8C.1 cleanup.
- Prior archive: `storytime-phase8b-local-multi-backend-stack.tar.gz` —
  Phase 8B implementation output (Loki + local log routing).
- Prior archive: `storytime-phase8a-locked-state-bundle.tar.gz` — Phase 7D.1
  code plus the full State Preservation Bundle, with the Phase 8A Architecture
  Baseline amendment (`docs/architecture-baseline.md` Section 23) **locked**.
- Phase 7D.1 code archive: `storytime-phase7d1-compose-build-fix.tar.gz` —
  sha256 `b5489f10b02b3fd4ee5690f6f9053038a32c4655cb13ba318a5236145e77ff5b`.
- Phase 7D archive: `storytime-phase7c1-app-containerization.tar.gz` — sha256
  `9b450cf86aaa39dbec38c138c98e39d55842cda11deb95506ac6644172016fcd`.
- Phase 7B archive: `storytime-phase7b-bluegreen-frontdoor-switching.tar.gz` —
  sha256 `f3ca94b0fa2f31efa082622918908f1da15d0b1a6cc60e951473699ad87c504a`.
- Phase 7A archive: `storytime-phase7a-bluegreen-option-a.tar.gz` — sha256
  `4b4ce674945c497d538c547bda7e5ed514684fd77b454edbe2893b9b1cfa570f`.

## Open issues / carryovers

See `docs/open-issues.md` for the full register. Active items:

- **OI-15** — `storytime clean` retention policy is in the canonical CLI
  surface but unimplemented. Standing functional carryover, independent of the
  deployment track. Not a Phase 8 prerequisite.
- **OI-3** — observability-stack Docker image tags pinned but unverified in a
  build environment; unscheduled re-verification step.
- **OI-5** — optional TOML file-config support; unscheduled, only if wanted.
- Recently resolved: OI-17 (Option A), OI-18 (front door), OI-19
  (containerization), OI-20 (compose build race).
- **OI-21** — the Phase 8B Loki image tag (`grafana/loki:3.3.2`) and
  `config/loki.yaml` are pinned but unverified in the Docker-less build
  environment; re-verify on a Docker host (parallel to OI-3).
- **OI-22** — the Phase 8C per-vendor Compose override merges and live vendor
  export are unverified without Docker; re-verify on a Docker host (parallel
  to OI-3 / OI-21).
- Phase 8 (multi-backend telemetry fan-out) is **complete**: the Phase 8A
  Architecture Baseline amendment (`docs/architecture-baseline.md` Section 23),
  Phase 8B / 8B.1 (local multi-backend stack expansion + `./logs` preflight),
  and Phase 8C / 8C.1 (optional vendor export profiles) are all **locked**.
- **Phase 9A — Governance Baseline Amendment is locked** (2026-05-24);
  `docs/architecture-baseline.md` Section 24 is canonical. **Phase 9B — Minimal
  Trust Envelope Implementation is locked (2026-05-24)**, with the **Phase 9B.1
  forbidden-term-scanner hardening cleanup folded into the lock**. **Phase 10A
  — Operator Experience Baseline Amendment is locked** (2026-05-24);
  `docs/architecture-baseline.md` Section 25 is canonical operator-experience
  law. **Phase 10B — Generated Local HTML Operator Report is locked
  (2026-05-24)** — the `storytime.reporting` package and the `storytime report
  generate` CLI command; the corrected lock record states Phase 10B added no
  Jinja2 and no new dependency. **Phase 10C — Operator CLI Helpers / Failure
  Queue has been implemented as a candidate (2026-05-25)** — the
  `storytime.operator_queue` module and the read-only `storytime queue` CLI
  command — pending GPT-5.5 review, Gemini critique, any cleanup, and explicit
  user lock. Phase 10C opened no open issue and closed none; it made no
  database schema change and added no dependency. *(Historical status before
  Phase 10D implementation; superseded by Phase 10D implementation candidate
  status — see current-state section at the top of this file.)*
  Phase 9C — Docs / Audit Polish — was an optional follow-up and is not
  scheduled.

## Historical RoundTable export — 2026-05-24 (how to interpret it)

A RoundTable full-project export exists as a historical recovery input:
`ROUNDTABLE_PROJECT_StoryTime__formerly_podcast_pipeline__2026-05-24.json`
(SHA-256 `8b6a089f5e5a4bc58b2387b0fc3f8b90e548a9d9237423ba88d0dd64dcddfdb4`;
RoundTable schema 0.11.0 / app 0.12.0; exported 2026-05-24T01:01:02Z;
`exportType: roundtable.fullProjectExport`; `source: local-browser`).

**Status: historical recovery input — not current-state authority.** Treat it
strictly as recovery material for early lineage. Its newest StoryTime round is
Round 22 (Phase 7C planning); it predates and is **superseded by** all later
Phase 8–10 artifact history and by the Phase 10 closure. The export's own
embedded "current phase" text (e.g. "Phase 7C Planning") is **stale** and must
never be promoted into a first-read current-state document.

**How to read it.** The export's `payload.appState` contains three RoundTable
projects; only `proj-cc9a7838-…` — "StoryTime (formerly podcast pipeline)" — is
StoryTime. The other two (`proj_demo_001` "RoundTable", and an "Untitled
Project") are unrelated RoundTable demo-app/project state and must **not** be
imported into StoryTime docs. The StoryTime project's `canonicalState` field
holds Rounds 1–22 of early planning/implementation lineage; its `decisions`
array holds the matching ratified decisions. A concise, quarantined summary of
the StoryTime-relevant Phase 0–7 lineage has been integrated into
`docs/phase-history.md` (see its "Appendix — Historical RoundTable Lineage,
Phases 0–7" section). That appendix — not this raw export — is the doc-resident
historical record.

**Conflict / chronology rule.** Where the export disagrees with later locked
artifact history, the later locked history wins. Priority order: (1) the current
verified state (Phase 10 CLOSED, Phase 11 — Release Candidate Hardening — CLOSED
with Phase 11A–11D all locked, Phase 12 — Portfolio / SE Demo Packaging — CLOSED
with Phase 12A–12D all locked, and Phase 13 — Portfolio Website / Operator
GUI — STARTED with Phase 13B — Typed Static Portfolio Shell / Minimal Visual
Pipeline Scaffold — locked (the last locked phase) and Phase 13C —
Deterministic Read-Only Static Export / Frontend Data Alignment — the current
implementation candidate, per `docs/handoff-state.md` and
`docs/canonical-state.md`); (2) the Phase 8–13B locked artifact history
already in this repository; (3) this historical RoundTable export for Phases
0–7. Do not overwrite valid Phase 8–13B history
with older export-derived state, and do not delete valid existing history.

**Early-artifact lineage observed in the export (historical).** The export
records two early Phase 7 implementation artifacts by name —
`storytime-phase7a-bluegreen-option-a.tar.gz` (Phase 7A, lean blue/green
Option A) and `storytime-phase7b-bluegreen-frontdoor-switching.tar.gz`
(Phase 7B implementation output) — and a Round 20 desync/recovery checkpoint.
These are historical references only; the authoritative artifact lineage is the
"Artifact lineage" section above and `docs/artifact-manifest.md`.

## RoundTable JSON construction instructions

GPT-5.5 should construct the import JSON by:

1. Creating project identity from the Project Identity section above.
2. Creating canonical state from `docs/canonical-state.md`.
3. Creating phase history from `docs/phase-history.md`.
4. Creating open issues from `docs/open-issues.md`.
5. Creating roadmap / current-next-phase from `docs/roadmap.md`.
6. Creating the model roster from the Model Roster section above.
7. Creating latest artifact lineage from `docs/artifact-manifest.md`.
8. Creating a recovery note from `docs/handoff-state.md`.
9. Marking the current phase as "Phase 13 — Portfolio Website / Operator GUI —
   STARTED; Phase 13C — Deterministic Read-Only Static Export / Frontend Data
   Alignment — implementation candidate, pending review, not locked. Phase
   13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold — is
   locked and is the last locked phase. Phase 12 — Portfolio / SE Demo
   Packaging — is CLOSED (Phase 12A through 12D all locked). Phase 10 —
   Product UI / Operator Experience — is CLOSED (2026-05-25) and Phase 11 —
   Release Candidate Hardening — is CLOSED (Phase 11A–11D all locked); Phase
   9B locked; the Post-Phase-10 Historical State Reconciliation was the last
   locked work item before Phase 11; `docs/architecture-baseline.md` Section
   24 canonical governance law and Section 25 canonical operator-experience
   law" and the next required action as "submit the Phase 13D artifact for
   GPT-5.5 review and Gemini critique under the Phase Closure Protocol, then
   an explicit user decision on whether to lock Phase 13D; do not start Phase
   13E or any later Phase 13 subphase, or any further mutation-capable
   operator-GUI work, without an explicit gate", exactly as stated here and in
   `docs/handoff-state.md`.
10. Not replaying stale or superseded rounds — treat phases 0–7D.1, 8A,
    8B / 8B.1, 8C / 8C.1, 9A, 9B (with 9B.1 folded in), 10A–10G, 11A–11D,
    12A (with the Phase 12A.1 cleanup folded in), 12B (with the Phase
    12B.1 / 12B.2 / 12B.3 cleanup sub-rounds folded in), 12C, 12D, 13A,
    13B, and 13C as locked; Phase 10, Phase 11, and Phase 12 are all
    CLOSED; the Post-Phase-10 Historical State Reconciliation is locked —
    do not re-run it or re-import the RoundTable JSON. Phase 13 — Portfolio
    Website / Operator GUI — is STARTED (Phase 13A, Phase 13B, and Phase
    13C are locked; Phase 13D is the current implementation candidate;
    Phase 13E through Phase 13G are future, planned work and have not
    started); Phase 9C was an optional follow-up and is not scheduled.

## Import validation checklist

- Current phase: **Phase 13 — Portfolio Website / Operator GUI — STARTED; Phase 13F — Local Bridge Architecture & Contract Baseline — is the current implementation candidate pending review (not locked); Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary — is locked (the last locked phase)**; Phase 10, Phase 11, and Phase 12 are all CLOSED; matches `docs/handoff-state.md`.
- Last locked phase is **Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary** (locked artifact `storytime-phase13e-demo-mode-action-preview-operator-intent-boundary.tar.gz`, SHA-256 `a997f2ca9d213e28e140f47c63336367c8feda46ed994b41300f86b99f8d8164`); Phase 13A, Phase 13B, Phase 13C, Phase 13D, Phase 13D.1, Phase 13D.2, Phase 12A–12D, Phase 11A–11D, and Phase 10A–10G are also locked; the last locked work item before Phase 11 is the **Post-Phase-10 Historical State Reconciliation** (locked artifact `storytime-post-phase10-roundtable-historical-backfill.tar.gz`, SHA-256 `367e647c46aa6e4fd039369da30859b11ca783249569df291343db133ef4cfdd`); all match `docs/canonical-state.md`.
- Phase history includes all locked phases (0, 1, Phase Closure Protocol, 2, 3,
  4/4.1, 5, 6S, 6A, 6B, 7A, 7B, 7C/7C.1, 7D, 7D.1, 8A, 8B, 8B.1, 8C / 8C.1,
  9A, 9B with 9B.1, 10A–10G, 11A–11D, 12A, 12B, 12C, 12D, 13A, 13B, 13C,
  13D, 13D.1, 13D.2, and 13E); Phase 10, Phase 11, and Phase 12 are all closed; the Phase 13F
  round is recorded as an implementation candidate.
- Roadmap matches handoff-state: Phase 10A–10G locked; Phase 10 CLOSED; Phase 11A–11D locked; Phase 11 — Release Candidate Hardening — CLOSED; Phase 12A–12D locked; Phase 12 — Portfolio / SE Demo Packaging — CLOSED; Phase 13A, Phase 13B, Phase 13C, Phase 13D, Phase 13D.1, Phase 13D.2, and Phase 13E locked; Phase 13 — Portfolio Website / Operator GUI — STARTED, Phase 13F implementation candidate; Phase 13G–13H not started; Phase 9C not scheduled.
- Open issues are preserved (OI-15 active; OI-3, OI-5, OI-21, OI-22
  unscheduled; OI-20 closed).
- Model roster is present (GPT-5.5, Claude Opus 4.7, Gemini 3, Claude Sonnet
  4.6).
- Artifact lineage is preserved (`docs/artifact-manifest.md`).
- No stale RoundTable rounds are replayed.
