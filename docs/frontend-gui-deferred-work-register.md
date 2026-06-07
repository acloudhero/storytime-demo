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

# StoryTime — Frontend / GUI Deferred-Work Register

A dedicated tracking document for frontend / GUI / portfolio-website work that
is intentionally **deferred** from the current phase. It is the frontend
counterpart of the backend `docs/open-issues.md` pattern.

**This register tracks; it does not authorize.** Listing an item here does not
permit it to be built. Every future frontend item still requires explicit
phase authorization through the Phase Closure Protocol.

Every frontend / GUI phase from Phase 13C onward must update this register
when a deferred item is added, completed, split, or intentionally abandoned,
or when a new near-term risk is found.

**Status:** maintained as of Phase 13F — Local Bridge Architecture &
Contract Baseline (implementation candidate, pending review, not
locked). Phase 13E — Demo-Mode Action Preview / Operator Intent
Boundary — is locked and is the last locked phase; Phase 13G and
later are not started. **Phase 13F documents the Local Bridge
architecture & contract. It does not implement the bridge.**

---

## 1. Placeholder view expansion (deferred from Phase 13B / 13C)

The Phase 13B shell shipped honest placeholder components for these views.
As of the Phase 13D.2 candidate, Governance / Safety, Failure / Recovery,
Evidence / Validation, and Demo Walkthrough are **implemented** as real
read-only views; the remaining placeholders are still placeholders.

| View | Kind | Deferred to / status | Notes |
|------|------|----------------------|-------|
| Architecture Story | Portfolio section | Phase 13E or later | Pipeline, observability, governance, contract walkthrough. **Phase 13D.2 absorbed ~80–90% of this narrative into the Demo Walkthrough's embedded architecture-checkpoint cards.** A standalone Architecture Story page is now tracked separately in §13 below as deferred. |
| Demo Walkthrough | Portfolio section | **Implemented — Phase 13D.2 candidate** | Real read-only guided reviewer / demo path view (`frontend/src/components/DemoWalkthroughView.tsx` plus its CSS Module) backed by a static view-model adapter (`frontend/src/data/demoWalkthroughAdapter.ts`). Offers four routes — 5-minute scan, 10-minute SE-style demo, technical deep-dive, self-guided reviewer — switched by a simple segmented control via local `useState<RouteId>` (no router, no Context, no persistence). Each step carries title, target view, what to inspect, what it proves, talking points, and an in-line navigation affordance into the relevant existing view; steps pointing to a specific run identify it by stable id (`run-2026-0518-golden` or `run-2026-0520-review`). Includes architecture-checkpoint cards, a "what is intentionally deferred" section, and interview / SE talking-point callout cards. Backed by the locked Phase 13D.1 static export — no fetch, no mutation, no dynamic file loading. |
| Evidence / Validation | Portfolio section | **Implemented — Phase 13D.1 (locked)** | Real read-only view: mandatory STATIC PORTFOLIO DATA — NOT A LIVE CI/CD DASHBOARD disclaimer, claims-vs-proof categories, repository-relative evidence references, Demo / Active / Candidate Data Source framing (data snapshots, not deployment environments), static scope facts from the locked Phase 13C export. No live CI status, no fabricated test results. |
| Governance / Safety | Operator/portfolio view | **Implemented — Phase 13D (locked); refactored — Phase 13D.1 (locked)** | Per-run Trust Envelope decisions, source authorization, governance gate, display-discipline honesty list, evidence references, visibly-disabled review actions (rendered via the shared `DisabledFutureActionCard` / `DisabledFutureActionList` — see §10), drill-down to Pipeline Run Detail. |
| Failure / Recovery | Operator view | **Implemented — Phase 13D (locked); refactored — Phase 13D.1 (locked)** | Failure / review queue with per-row affected stage, structured failure summary, related governance decision, evidence, inspect-next guidance, visibly-disabled recovery actions (rendered via the shared `DisabledFutureActionCard` / `DisabledFutureActionList` — see §10), drill-down to Pipeline Run Detail. |
| Roadmap | Portfolio section | Phase 13E or later | The 13A–13G subphase decomposition and status. |
| Settings / Config | Operator view | Phase 13E or later | The Demo / Active / Candidate data-snapshot selector (see §8); not implemented in Phase 13D.2 — only Demo is available, and Phase 13D.2 carries forward the static Demo Snapshot framing from Phase 13D.1's Evidence view. |

The placeholder text in the Phase 13D.2 frontend now states that expansion
of the remaining placeholders is planned for Phase 13E or later.

## 2. Phase 13C.2 follow-up items

**None currently required.** The Phase 13C token-exhaustion escape hatch was
**not** used. The full Phase 13C scope was implemented in one round: the
backend static export contract, the deterministic export generator and CLI
command, the committed JSON artifact, the frontend TypeScript type alignment,
the frontend adapter, and the React component rewiring (homepage and Pipeline
Run Detail / Stage Timeline now consume the export through the adapter). The
frontend typechecks and builds. No deferred React rewiring remains, so no
Phase 13C.2 cleanup round is needed.

## 3. Schema / type drift risks

- The backend export shape (`storytime.operator_export`, `schemaVersion`
  `"1.0"`) and the frontend types (`frontend/src/types/storytime.ts`) are
  **aligned** as of Phase 13C. The frontend gained a `StaticDemoExport`
  envelope type that mirrors the export's top-level shape; the existing
  per-run read-model types already matched the backend-native shape (they were
  designed in Phase 13B to be flat and serialization-friendly), so drift was
  minimal.
- The runs-list summary (`PipelineRunSummary`) is **derived in the adapter**,
  not stored in the export. If a future export adds a stored summary, the
  adapter must stop deriving it — track that as a drift point.
- `schemaVersion` is the drift tripwire. A breaking export-shape change must
  bump it, update `docs/frontend-static-export-contract.md`, and update the
  mirrored frontend types in the same round.
- No fields are currently provisional; the contract is documented in full in
  `docs/frontend-static-export-contract.md`.

## 4. CSS / frontend scalability debt

- The frontend uses a single global stylesheet, `frontend/src/styles.css`,
  for the shell (header, nav, panels, chips, page-title, etc.).
- **Phase 13D / 13D.1 status — partially addressed.** Phase 13D introduced
  CSS Modules for the two new operator views
  (`GovernanceSafetyView.module.css`, `FailureRecoveryView.module.css`).
  Phase 13D.1 continues the pattern for every new component:
  `DisabledFutureActionCard.module.css` and
  `EvidenceValidationView.module.css`. New components from this point
  forward should keep following this pattern: a co-located `*.module.css`
  file that consumes the shared global CSS custom-property tokens
  (`--panel`, `--rule`, `--signal`, `--ink`, etc.) but defines no global
  selectors. The global stylesheet remains in place for the shell and for
  the Phase 13B/13C components — they are **not** migrated as part of
  Phase 13D or 13D.1, because both prompts explicitly disallow broad
  refactors. Phase 13D added one `.data-chip` rule to the global
  stylesheet for the header chip; Phase 13D.1 adds **no** new global
  selectors.
- **Still deferred:** a wholesale migration of the shell and Phase
  13B/13C components to CSS Modules (or another scoped approach), if and
  when the view count grows further. This is debt, not a defect, and
  does not need fixing in Phase 13D.1.

## 5. View-expansion recommendations (delivered in Phase 13D / 13D.1)

Recommended order for the first Phase 13D — Operator Workflow View
Expansion round (now historical; both views are locked or refactored):

1. **Governance / Safety** — highest-value first. StoryTime's distinctive
   engineering claim is its honest, fail-closed, human-decided governance
   layer. A Governance / Safety view makes that legible and is the strongest
   single proof to a Solutions Engineer or hiring manager that StoryTime is a
   governed, observability-native pipeline rather than a basic script.
2. **Failure / Recovery** — second. The failure / review queue shows that
   the system reasons about what went wrong and what to do next. Together
   with Governance / Safety it demonstrates operational maturity: the
   pipeline is built to be operated, observed, and recovered, not just run
   once.

These two views also reuse data already present in the static export (the
per-run `governance` block and the `failureQueue`), so Phase 13D expanded
them against the existing Phase 13C contract with no schema change. **Both
were delivered in Phase 13D (locked).** Phase 13D.1 then refactored their
disabled-action rendering to use a shared component (see §10) and added
the Evidence / Validation view (see §11).

## 6. Action / mutation boundary items

The export and UI carry **disabled future actions** that must stay
non-functional until the explicitly gated mutation subphase (Phase 13E):

- `Re-run this pipeline run` (golden run) — mutation; enabled by Phase 13E.
- `Open review workflow` (review run) — mutation; enabled by Phase 13E.
- `Retry after review` (review run) — mutation; enabled by Phase 13E.

These are shown in the UI as visibly-disabled affordances with an
`isMutation` flag and no invokable payload. The non-mutating allowed actions
(copy-command, open-reference) are not mutations and may stay live. No action
may become functional before Phase 13E and its safety review.

## 7. Portfolio / public-site polish items

Deferred polish, none scheduled, each needing its own future authorization
(largely Phase 13F — Portfolio Website Polish / Public Demo Packaging):

- Screenshots / visual assets for the portfolio and the README.
- Public hosting / deployment of the static build (optional Phase 13G).
- Navigation refinement as the view count grows (e.g. grouped nav, breadcrumbs).
- Copy editing pass on portfolio prose for a public audience.
- Accessibility audit (keyboard paths, ARIA, contrast) as views expand.
- A public-facing demo walkthrough and reviewer on-ramp.

## 8. Demo / Active / Candidate Data Snapshot Switcher (refined — Phase 13D.1; deferred)

> **Naming note (Phase 13D.1).** This section was originally titled
> "Demo / Blue / Green" in the Phase 13D register. Phase 13D.1 renames
> the future snapshots to **Active** and **Candidate** to remove any
> ambiguity with blue/green deployment terminology. These are **data
> snapshots**, not deployment environments — the planned switcher would
> change which static read-only data the frontend reads, never which
> host, environment, or instance serves the page. The static framing
> added to the new Evidence / Validation view in Phase 13D.1 documents
> the same.

A future Settings / Config affordance that lets an operator switch the
frontend between named **read-only data snapshots** at browser load
time. It is a data-snapshot concept, not a deployment concept and not a
backend mutation:

- **Demo** — the existing bundled portfolio dataset
  (`frontend/src/data/storytime-demo-export.json`). Always available;
  safe; the default. This is the only snapshot present in Phase 13D.1.
- **Active** — a future read-only snapshot representing the operator's
  current local export of their own runs (generated by `storytime
  export-demo-ui` or its evolution). Loaded into the frontend as a static
  asset; never mutates the backend.
- **Candidate** — a future read-only candidate / alternate snapshot,
  useful for comparing two snapshots side-by-side or validating a
  change.

Constraints any future implementation must satisfy:

- Snapshots are **read-only data sources** the frontend consumes;
  switching snapshots **must never delete or modify backend data** and
  must not trigger any pipeline mutation.
- The future affordance described as "promote Candidate to Active"
  remains **disabled** until the explicit safe-mutation-boundary
  subphase (Phase 13E or later) reviews and authorizes it. Until then,
  the UI may surface a visibly-disabled "Promote" affordance but never
  an enabled one.
- The UI wording must avoid destructive phrasings like "clear all
  pipeline data"; the user-facing language is about *which snapshot to
  view*, not about backend state.
- The selector belongs in Settings / Config and must clearly state
  which snapshots are actually available (in Phase 13D.1: only Demo).
  The current Phase 13D.1 header surfaces this honestly as a read-only
  chip ("Data source · Demo Snapshot"), and the Evidence / Validation
  view re-states it in its Data Source / Demo Snapshot framing.

This item is deferred. It is **not** implemented in Phase 13D.1.

## 9. Runtime data validation / schema discipline (Phase 13D / 13D.1; deferred)

Phase 13C established the export contract and the frontend's static type
mirror, and Phase 13D / 13D.1 consume the export through TypeScript
types only. There is no runtime validation step between "the JSON
literal at build time" and "the React component tree" — TypeScript
catches shape drift at compile time but does not detect a hand-edited
export file with the wrong shape, a missing field at runtime, or an
unexpected `schemaVersion`.

Deferred items:

- **Runtime schema validation (e.g. Zod, Valibot, or a hand-written
  validator)** at the adapter boundary, run once when the export is
  imported, with a clear failure mode if the shape does not match.
- **`schemaVersion` enforcement at runtime** — currently the adapter
  assumes `"1.0"`; a mismatch should produce a visible operator-friendly
  error surface, not a silent partial render.
- **Asynchronous / file-backed export loading** — Phase 13D / 13D.1
  load the export synchronously via a static `import`. A future
  file-backed or operator-local snapshot mode (see §8) will require an
  async loader, a loading state, an error state, and possibly an export
  discovery mechanism. None of this is implemented in Phase 13D.1.

These are all future work and are **not** required by Phase 13D.1's
acceptance criteria.

## 10. Disabled future-action display standardization (Implemented — Phase 13D.1)

Phase 13D shipped two operator views (Governance / Safety and Failure /
Recovery) that each contained a near-identical local `DisabledActionRow`
function for rendering visibly-disabled future actions. Phase 13D.1
extracts this into a shared component:

- `frontend/src/components/DisabledFutureActionCard.tsx` — the reusable
  card. Renders the action as a **real** `<button disabled={true}>`
  element with **no** `onClick` handler (not even a no-op). Adjacent
  metadata is rendered as subtext: a `disabled` pill, an optional
  `mutation` pill, the `enabled by …` phase label, the `disabledReason`,
  and a derived `safetyNote` (different copy depending on `isMutation`,
  with an optional explicit override).
- `frontend/src/components/DisabledFutureActionCard.module.css` — the
  matching CSS Module. Consumes the existing global tokens and mirrors
  the field-instrument visual language of the Phase 13D views.
- A `DisabledFutureActionList` wrapper handles arrays of actions, an
  optional heading / preface, optional per-id `safetyNote` overrides,
  and an optional empty-state message.

The Governance / Safety and Failure / Recovery views in Phase 13D.1
import and use this list instead of their previous local rows; the
visual is unchanged, the disabled control is now a real disabled
button rather than a styled `<div>`, and there is no chance of one view
drifting toward a "fake action handler" pattern. Harmless navigation
affordances (e.g. "Inspect this run in Pipeline Run Detail →") remain
in the consuming views and are deliberately **not** routed through this
component — they are not disabled future actions.

The component has no action-execution prop. A future Phase 13E (or
later) that introduces real local-action handlers behind a safety gate
will live in a separate component or a deliberately wrapping
component; it will not silently pass handlers through this one.

## 11. Evidence / Validation static view (Implemented — Phase 13D.1)

Phase 13D.1 replaces the Phase 13B/13C Evidence / Validation placeholder
with a real read-only view:

- `frontend/src/components/EvidenceValidationView.tsx` and the matching
  CSS Module. The page renders the mandatory **STATIC PORTFOLIO DATA —
  NOT A LIVE CI/CD DASHBOARD** disclaimer prominently, a scope strip of
  static facts derived from the locked Phase 13C export
  (`schemaVersion`, `generatedBy`, run / failure-queue / governance-row
  counts), a claims-vs-proof category grid (Backend Validation Gates,
  Frontend Validation Gates, No-Network Discipline, Deterministic
  Export, Archive Hygiene, State-Discipline Guard, Append-Only History),
  a Data Source / Demo Snapshot framing card (Demo current; Active /
  Candidate as future data snapshots, not deployment environments), a
  repository-references list, and a short talking-points block.
- `frontend/src/data/evidenceAdapter.ts` — the view-model adapter that
  organises the categories and references. No `fetch`, no file I/O, no
  runtime parsing of `docs/`. Counts come from the existing
  `adapter.ts` / `governanceAdapter.ts` exports of the locked Phase 13C
  static export.

What this view deliberately is **not**: a live CI/CD dashboard, a
runtime-polled health surface, a "latest test results" panel with fake
green/red status, or a fabricated freshness timestamp.

## 12. Navigation metadata extraction (Implemented — Phase 13D.1)

Phase 13D.1 lifts the static nav metadata (the `View` type union, the
`NAV` array, the `PLACEHOLDERS` map) out of `App.tsx` and into
`frontend/src/navigation.ts`. `App.tsx` keeps its plain `useState`
navigation and the `inspectRun(runId)` callback; no router, no
Context, no global state. Before Phase 13D.1 `App.tsx` was 228 lines —
above the ~200-line guardrail from the Phase 13D.1 prompt — and is now
136 lines. The extracted module exports only static data and a type
alias; it does not own any state.

## 13. Demo Walkthrough / Reviewer Story Path (Implemented — Phase 13D.2)

Phase 13D.2 replaces the honest Demo Walkthrough placeholder with a
real read-only guided reviewer / demo path view
(`frontend/src/components/DemoWalkthroughView.tsx` plus its CSS Module),
backed by a static view-model adapter
(`frontend/src/data/demoWalkthroughAdapter.ts`) that holds the
long-form route content. The adapter exports route definitions, step
definitions, architecture checkpoints, intentionally-deferred items,
interview / SE talking points, repository references, and stable run
ids (`run-2026-0518-golden`, `run-2026-0520-review`). The view is a
presentation shell that iterates over the adapter data; no long-form
prose lives inside the component.

The view offers four reviewer routes — a 5-minute scan, a 10-minute
SE-style demo, a technical deep-dive, and a self-guided reviewer path
— switched by a simple segmented control backed by local
`useState<RouteId>` (no router, no Context, no persistence, no URL
params, no localStorage). Each step carries title, target view, what
to inspect, what it proves, talking points, and an in-line navigation
affordance into the relevant existing view; steps that point to a
specific run identify it by stable id so the reviewer is never asked
to guess which run proves the point. The view also includes
architecture-checkpoint cards (local-first design, deterministic
static export, backend owns truth / frontend owns understanding,
read-only operator surface, static evidence boundary, disabled-action
boundary, Demo / Active / Candidate as data snapshots not deployment
environments, why Phase 13E must be explicitly gated), a deliberate
"what is intentionally deferred" section, and interview / SE
talking-point callout cards. No CSS art / SVG / diagrams / images —
only typography, lists, and callout boxes, per the explicit prompt
constraint.

`frontend/src/navigation.ts` was updated so the Demo Walkthrough entry
has `soon: false` and sits next to Evidence / Validation in the nav
order; the `PLACEHOLDERS` map no longer includes `demo` (it's now a
real view) but still includes Architecture Story, Roadmap, and
Settings / Config, all pointing to Phase 13E or later.
`frontend/src/App.tsx` renders `<DemoWalkthroughView onNavigate={setView}
onInspectRun={inspectRun} />` for the `"demo"` view key; brand tag and
footer copy advance to Phase 13D.2. App.tsx remained well under the
~200-line guardrail.

## 14. Standalone Architecture Story / System Boundary Reference (deferred)

Phase 13D.2 deliberately absorbs ~80–90% of an Architecture Story
narrative into the Demo Walkthrough as embedded architecture-checkpoint
cards (eight cards covering local-first design, deterministic static
export, backend-owns-truth / frontend-owns-understanding, read-only
operator surface, static evidence boundary, disabled-action boundary,
Demo / Active / Candidate data-snapshot concept, and why Phase 13E
must be explicitly gated). That coverage answers the core reviewer
questions about the system boundary without a separate page.

The remaining ~10–20% of a full standalone Architecture Story page is
**deferred** to a possible later Phase 13 subphase. A standalone page
would add:

- a deeper system-boundary explanation that goes beyond what fits in
  a walkthrough checkpoint card;
- a fuller local-first architecture write-up, naming each component
  (ingest, synthesize, assemble, publish, governance, failure queue,
  telemetry pipeline, operator export) and the data each one owns;
- a future cloud-path explanation, framed as optional and gated;
- public-portfolio polish (a page a hiring manager could share around
  on its own);
- interview leave-behind material a candidate could point an
  interviewer at after a conversation.

This deferred item is **not** authorization. Like every other entry in
this register, it requires explicit phase authorization through the
Phase Closure Protocol. It is scoped to be **static / read-only** when
it is eventually built; it does not justify any live integration or
mutation work. The placeholder for the Architecture Story entry in
`frontend/src/navigation.ts` carries copy that points at this deferred
item and notes Phase 13D.2's embedded coverage.

## 15. Demo-Mode Action Preview / Operator Intent Boundary (Implemented — Phase 13E)

Phase 13E adds a static, Demo-mode-only Action Preview system that
turns the existing visibly-disabled future-action affordances into
explainable, non-executing **action previews**. The new files are
`frontend/src/data/actionPreviewAdapter.ts` (typed static view-model
holding action-preview definitions and operating-mode constants for
Demo / Local / Cloud-Distributed), `frontend/src/components/ActionPreviewPanel.tsx`
(a presentation shell that maps over the adapter data and renders the
selected preview with safety / honesty labels), and
`frontend/src/components/ActionPreviewPanel.module.css` (the
co-located CSS Module). The panel is integrated into Failure /
Recovery, Governance / Safety, and Evidence / Validation
**alongside** the existing `DisabledFutureActionCard` /
`DisabledFutureActionList` — which is unchanged: still a real
`<button disabled={true}>` with no `onClick`, no `onMouseDown`, no
silent handler — via a separate, clearly-labelled "Preview action
plan" affordance.

The Action Preview panel is managed by local
`useState<ActionPreviewId | null>` only — no router, no Context, no
persistence, no URL params, no hash routing, no `localStorage`, no
`sessionStorage`, no `History` API manipulation, no global preview /
action state, no new Context provider. Each preview includes a
stable action id, label, category, current mode (Demo), execution
status (Preview only / non-consequential), target object (run id /
stage id / governance decision id / failure queue item / evidence
artifact as applicable), target context label, what the operator is
trying to accomplish, why it is blocked in Demo mode, a precondition
checklist, evidence to inspect first, risk level and explanation, an
illustrative future Local-mode request shape (a structured pseudo-DTO
labelled "Future request shape — illustrative only, not executable in
Demo mode" — never executable shell commands), Cloud/Distributed
considerations, audit expectations, failure behaviour expectation,
what remains disabled, and the related view. The required
safety / honesty labels — "Demo mode", "Preview only", "No state
changed", "Action plan, not action result", "Execution requires
future Local mode", "Cloud/Distributed execution is not implemented",
"No audit record generated because nothing executed", "No local
bridge is running", "No backend command was called" — are rendered
in the panel header for every preview. The enterprise-governance
wording — "System constraint: Action execution requires future Local
or Cloud/Distributed mode. Current operating mode is Static Demo.
This is an action plan preview only; no state changed and no audit
record was generated." — is also rendered.

The first set of previews implements five action previews:
**retry-failed-stage** (target run `run-2026-0520-review`, stage
`run-2026-0520-review:governance-gate`, related disabled action
`run-2026-0520-review:retry` — Failure / Recovery context),
**inspect-trust-envelope** (target run `run-2026-0520-review`,
non-mutating inspection — Governance / Safety context),
**record-review-decision** (target run `run-2026-0520-review`,
related disabled action `run-2026-0520-review:open-review` —
Governance / Safety context), **regenerate-operator-report** (target
evidence/report surface — Evidence / Validation and Failure /
Recovery context), and **refresh-export** (target static export
`frontend/src/data/storytime-demo-export.json` — Evidence /
Validation context, explaining that real Local mode would require a
refreshed export after action completion).

Phase 13E introduces or clarifies the eventual operating-mode model
— **Demo mode** (curated, safe, non-consequential, portfolio-ready;
the only mode implemented), **Local mode** (future real local
operator workflows; not implemented in Phase 13E), and **Cloud /
Distributed mode** (future hosted/distributed execution; not
implemented in Phase 13E) — distinct from the existing Demo /
Active / Candidate **data-snapshot** labels (which Phase 13D.1's
Evidence / Validation view already framed and which Phase 13E does
not replace).

A new Python data-integrity test
(`tests/test_action_preview_data_integrity.py`) opens both the
committed static export
(`frontend/src/data/storytime-demo-export.json`) and the action
preview adapter (`frontend/src/data/actionPreviewAdapter.ts`) as
text, extracts run-id and target-id patterns referenced by the
adapter, and asserts each exists in the committed export. The test
asserts at minimum that `run-2026-0518-golden` and
`run-2026-0520-review` are present in both. No new test framework
dependency was added; the test uses the existing pytest.

**Phase 13E models operator intent in Demo mode. It does not execute
actions.**

## 16. Items still deferred after Phase 13E

The following items remain explicitly deferred. **This register
tracks; it does not authorize.** Each item still requires a future
phase authorization through the Phase Closure Protocol.

- **Real Local mode** — Future operator workflows that load local
  exports, run on local pipeline state, execute CLI-mediated
  actions, perform controlled local mutations, write local audit
  records, and refresh the static export after an action completes.
  Local mode is **not implemented** in Phase 13E; the action
  previews only describe what a Local-mode request shape might
  look like.
- **Actual local bridge / actual local server** — No HTTP bridge,
  WebSocket bridge, or local server is implemented or contemplated
  by Phase 13E. The action previews explicitly say "No local
  bridge is running" and "No backend command was called". A future
  Local Bridge Architecture Baseline subphase would need to be
  proposed, reviewed under the Phase Closure Protocol, and locked
  before any real bridge exists.
- **CLI-mediated action execution** — Phase 13E never invokes the
  `storytime` CLI or any subprocess. Future Local mode would do so
  through a clearly-defined safety boundary.
- **Refreshed export update loop** — Future Local mode would
  re-export the static JSON after an action completed so the GUI
  could reflect new state. Phase 13E does not implement this loop;
  the `refresh-export` preview only describes it.
- **Hash routing / browser History API routing** — Phase 13E
  explicitly does not introduce hash routing, URL routing,
  `History.pushState`, or URL params; the action-preview state is
  strictly local React state.
- **Runtime schema validation** — Phase 13E adds no runtime schema
  validation library (e.g. zod, valibot, ajv) and does not implement
  defensive parsing of the committed export at runtime. The
  existing TypeScript type alignment is the contract. A future
  Runtime Contract Hardening subphase would address this.
- **Cloud / Distributed mode** — Future hosted/distributed execution
  architecture (hosted APIs, durable workers, cloud storage, auth,
  distributed orchestration, cloud observability, production-like
  governance and action execution). Phase 13E does not implement
  any of it; previews only describe what Cloud / Distributed
  considerations might look like.
- **Actual retry / rerun / approval / report-regeneration /
  export-refresh execution** — No real mutation is implemented.
  The visibly-disabled buttons stay disabled and unhandled. The
  Phase 13E action previews end at an explicitly disabled
  execution boundary.
- **Standalone Architecture Story / System Boundary Reference page**
  — Still deferred from Phase 13D.2 §14. Phase 13D.2 absorbed
  ~80–90% of an Architecture Story narrative into the Demo
  Walkthrough as embedded checkpoints. A standalone page with
  deeper system-boundary explanation, fuller local-first
  architecture write-up, future cloud-path explanation,
  public-portfolio polish, and interview leave-behind material
  remains a candidate for a possible later subphase.
- **Demo / Active / Candidate snapshot switching** — Still deferred
  from §8. Phase 13E continues to surface Demo as the only
  available snapshot and frames Active / Candidate as future
  committed snapshots, not selectable today.
- **Public hosting / production deployment** — Still deferred to a
  later, optional subphase (Phase 13H in the current roadmap).

## 17. Local Bridge architecture & contract baseline documented (Phase 13F) — bridge still deferred

Phase 13F — Local Bridge Architecture & Contract Baseline — **documents** the architecture and contract for a future local bridge. **It does not implement the bridge.** Phase 13F added eleven architecture / contract docs (`docs/local-bridge-architecture.md`, `docs/externalized-state-architecture.md`, `docs/browser-storage-policy.md`, `docs/local-mode-workspace-layout.md`, `docs/storage-targets-architecture.md`, `docs/action-execution-boundary.md`, `docs/local-action-dto-spec.md`, `docs/local-action-audit-spec.md`, `docs/local-mode-storage-contract.md`, `docs/local-action-queue-observability.md`, `docs/phase13f-local-bridge-contract-readiness.md`), a set of non-runtime JSON example fixtures under `docs/examples/`, and one new Python contract-examples test. It established the central principle that the frontend is an operator surface, not the durable storage layer, hardened the browser-storage policy (see §6 / `docs/browser-storage-policy.md`), and settled the future local-bridge security boundary, execution-timing policy, action allowlist, DTO / audit contracts, and queue-observability model.

Everything the contract describes remains **deferred and unimplemented** after Phase 13F. **This register tracks; it does not authorize.** Each item still requires a future phase authorization through the Phase Closure Protocol:

- **The local bridge itself** — no loopback-only server, socket, subprocess, or local IPC is implemented. The future minimal Python-owned bridge (loopback-only `127.0.0.1`/`::1`, strict origin allowlist, command-pattern router, action allowlist) is contracted in `docs/local-bridge-architecture.md` and deferred to the recommended Phase 13G — Local Bridge Implementation.
- **The asynchronous local action queue** — no queue, no job store, no `202 Accepted` endpoint, no polling. The async execution-timing policy (acceptance ≠ success; `actionRequestId` / `jobId`; export refresh after a durable write; refresh-race avoidance) is contracted but not implemented.
- **Queue workers** — no worker, no concurrency control, no backpressure code. The conservative local load-limit policy (one long-running action at a time first) is contracted only.
- **Queue metrics / exporters / OpenTelemetry instrumentation** — the 13 required gauges, 11 events, and 14 attributes in `docs/local-action-queue-observability.md` are defined as the minimum observable surface a future queue must expose; none are implemented, and no metrics backend or OpenTelemetry instrumentation is added.
- **Storage providers & provider integrations** — no local-disk / RAM / USB workspace implementation, and no Google Drive / iCloud / Dropbox / S3 provider. The capability matrix in `docs/storage-targets-architecture.md` is a plan; provider credentials are never browser-owned.
- **Real Local mode and Cloud / Distributed mode** — still deferred exactly as in §16; Phase 13F only writes their architecture, it does not bring either mode into existence.
- **Mutation / action execution and audit-record generation** — no operator action executes, and no audit record is generated; the example audit fixture is a documentation artifact, not a generated runtime output.
- **Runtime DTO code and runtime schema validation** — the DTO request / response / audit contracts in `docs/local-action-dto-spec.md` and `docs/local-action-audit-spec.md` are future contracts only; no DTO type, parser, or validator is added to runtime code, and no JSON-schema dependency is introduced.

**Phase 13F documents the Local Bridge architecture & contract. It does not implement the bridge.**
