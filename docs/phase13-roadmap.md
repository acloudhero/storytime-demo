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

# StoryTime — Phase 13 Roadmap

The subphase decomposition for Phase 13 — Portfolio Website / Operator GUI. It
breaks Phase 13 into safe, reviewable subphases so the end goal (a working
portfolio website that is also the first operator GUI) is reached without an
unconstrained "build the whole frontend" round, and so architecture planning
(Phase 13A) cannot drift into frontend implementation.

This roadmap is the Phase 13A decomposition of record. It refines the earlier,
tentative 13A-13F sketch in `docs/GUI_vision.md` and the Phase 13 note in
`docs/roadmap.md` (both written during the Phase 12B.2 roadmap-preservation
cleanup, before Phase 13 started). Where this document and that earlier sketch
differ - names, ordering, the added Phase 13G - this document governs.

**Status.** Phase 13 is STARTED. Phase 13A — Portfolio Website / Operator
GUI Architecture Baseline —, Phase 13B — Typed Static Portfolio Shell /
Minimal Visual Pipeline Scaffold —, Phase 13C — Deterministic Read-Only
Static Export / Frontend Data Alignment —, Phase 13D — Operator
Workflow View Expansion (Governance / Safety, Failure / Recovery) —,
Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled
Action Discipline —, Phase 13D.2 — Static Demo Walkthrough /
Reviewer Story Path —, and Phase 13E — Demo-Mode Action Preview /
Operator Intent Boundary — are locked; Phase 13E is the last locked
phase. Phase 13F — Local Bridge Architecture & Contract Baseline —
is the current implementation candidate (pending review, not locked).
Phase 13G and every later Phase 13 subphase are NOT STARTED. Each
subphase below begins only after the previous one has completed the
Phase Closure Protocol and been locked by explicit user decision.

**Roadmap reconciliation note (Phase 13F round).** Earlier drafts of
this roadmap numbered the first real-mutation subphase as "Phase
13F — Controlled Local Actions / Safe Mutation Boundary". Phase 13F is
instead a documentation-and-static-fixture **Local Bridge Architecture
& Contract Baseline** — the architecture lock that must precede any
bridge / mutation code (architecture before code, the same principle
that put Phase 13A before any frontend code). The real-mutation
subphase has therefore shifted to **Phase 13G — Local Bridge
Implementation / Controlled Local Actions / Safe Mutation Boundary**,
the Portfolio Website Polish subphase to **Phase 13H**, and the
optional Deployment / Hosting Readiness subphase to **Optional Phase
13I**. All of 13G / 13H / 13I are NOT STARTED.

## Decomposition principles

- **Architecture before code.** Phase 13A settles the architecture, the
  content model, the view model, and the contract. No frontend code is written
  until Phase 13A is reviewed and locked.
- **Contract before screens.** The frontend/backend contract
  (`docs/frontend-backend-contract.md`) is defined before screens are built,
  and screens are built against a static/mock adapter before any backend API
  exists, so the frontend can exist independently of the backend.
- **Read-only before mutation.** Every operator surface is read-only until the
  explicitly gated mutation subphase (Phase 13G — Local Bridge Implementation /
  Controlled Local Actions). Phase 13E previews intent without executing, and
  Phase 13F writes the bridge / mutation contract without implementing it; the
  GUI does not become a control panel before the contract and safety boundaries
  are mature.
- **One reviewable subphase at a time.** Each subphase has a bounded scope, an
  explicit forbidden list, acceptance criteria, and a review gate. Each is
  locked under the Phase Closure Protocol before the next begins.
- **Local-first preserved throughout.** No subphase requires a cloud account; a
  public-hostable static build remains possible at every stage from 13B on.

## Phase 13A — Portfolio Website / Operator GUI Architecture Baseline

**Objective.** Design the Phase 13 frontend: the portfolio website and operator
GUI architecture, the audiences and review paths, the website and operator
information architectures, the frontend/backend contract, the content model,
the operator view model, and this subphase decomposition.

**Allowed changes.** Documentation only - the five Phase 13A documents
(`phase13-portfolio-website-architecture.md`, `frontend-backend-contract.md`,
`phase13-roadmap.md`, `portfolio-website-content-model.md`,
`operator-gui-view-model.md`), the State Preservation Bundle synchronization,
and the narrow authorized advance of the state-discipline guard
`tests/test_failure_mode_regression.py`.

**Forbidden changes.** No frontend application or scaffold; no `frontend/`,
`web/`, `app/`, or `apps/frontend/` directory; no `package.json`, no
`vite.config.*`, no Node project file; no React/Vue/component/route/browser
code; no HTML/CSS/JS application files; no framework or toolchain choice; no
backend API; no adapter; no authentication; no cloud deployment; no `src/`,
`pyproject.toml`, `uv.lock`, dependency, pipeline, CLI, telemetry, or Docker
change; no generated screenshots/audio/video/binary assets.

**Acceptance criteria.** The five documents are complete, internally
consistent, honest about scope, and detailed enough for Phase 13B to build the
first scaffold without re-deciding the architecture. The State Preservation
Bundle records Phase 12 closed, Phase 13 started, and Phase 13A as an
implementation candidate. The six Docker-free validation gates pass.

**Review gate.** GPT-5.5 review, then Gemini critique, then an explicit user
lock decision. Phase 13B does not begin until Phase 13A is locked.

## Phase 13B — Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold

*Scope note: this subphase was refined after the Phase 13A architecture
baseline. Following the Gemini critique of the Phase 13B implementation plan,
its scope was tightened and given a small, concrete operator proof: rather than
the full portfolio website, Phase 13B delivers a typed static shell plus
exactly one operator view. The earlier working title for this subphase was
"Frontend Scaffold / Static Portfolio Shell"; this revised definition governs.*

**Objective.** Create the first frontend scaffold and a deliberately bounded
static shell: concrete TypeScript read-model contracts and static demo data
first, then a minimal React + Vite + TypeScript scaffold, the portfolio
homepage, and one visual operator-focused view — Pipeline Run Detail with a
Stage Timeline — as the first operator-GUI proof. All other portfolio sections
and operator views are honest, lightweight placeholders.

**Allowed changes.** A new frontend project directory; a React + TypeScript
(strict) + Vite toolchain and its package files (including the frontend
lockfile); the frontend read-model contract and a static demo dataset of
exactly two mock pipeline runs (one golden-path, one governance
review-required); the portfolio homepage; one Pipeline Run Detail view with a
Stage Timeline; placeholder components for the future views; standard CSS;
build configuration for a local-first static build; a frontend README.

**Forbidden changes.** No backend connection, data adapter, or API (the
read-only adapter is Phase 13C); no `fetch()` / `axios` / `localhost` call; no
live or runtime data; no mutation controls or enabled operator actions; no
external UI / component / state / charting library; no authentication; no cloud
deployment or production hosting; no change to `src/`, the pipeline, the CLI,
telemetry, governance, or Docker behaviour; no change to any locked
Architecture Baseline contract.

**Acceptance criteria.** The frontend builds and runs locally as static content
(`npm install`, `npm run build` succeed; strict TypeScript passes), the
homepage and the Pipeline Run Detail view present demo data honestly and are
clearly labelled as a static, read-only, demo-data-backed shell, the remaining
sections are honest placeholders that claim no functionality, and the existing
backend and its six Docker-free gates are unchanged.

**Review gate.** GPT-5.5 review, Gemini critique, explicit user lock.

**Deferred from this subphase.** The remaining operator views (dashboard, runs
list, failure queue, governance/review, observability) and the remaining
portfolio sections are deferred — they are built in Phase 13D (operator views)
and a later portfolio-content subphase, against the Phase 13C read-only data
adapter. The placeholders shipped in Phase 13B mark exactly where they land.

## Phase 13C — Deterministic Read-Only Static Export / Frontend Data Alignment

*Scope note: this subphase was refined after Gemini critique of the original
Phase 13C prompt. Its earlier working title was "Read-Only Data Adapter /
Static Demo Data"; this revised definition governs. The emphasis is on a
**deterministic, backend-defined** static export plus the frontend alignment to
it.*

**Objective.** Implement the read side of the frontend/backend contract as a
truthful, reproducible data boundary: a backend-native static export contract,
a deterministic read-only export generator, a committed static JSON export with
a top-level `schemaVersion`, frontend TypeScript types mirroring that export,
and a frontend adapter — so the portfolio and operator shell render realistic
data with no live backend. The principle is "backend owns truth, frontend owns
understanding": where the Phase 13B frontend mock contract and the
backend-native export shape disagree, the frontend yields.

**Allowed changes.** A small read-only, deterministic backend export module
and/or a read-only CLI command (`storytime export-demo-ui`); the committed
static JSON export under `frontend/src/data/`; the export contract document;
the frontend / GUI deferred-work register; frontend TypeScript types, a
frontend adapter module, and the rewiring of existing views onto the adapter;
import-linter contract entries for the new backend module.

**Forbidden changes.** No mutation; no write path; no live API server, no
`fetch`/`axios`, no watcher, no backend-to-frontend runtime coupling; no
authentication; no cloud deployment or production hosting; no new frontend UI /
component / state / charting / router library; no deep implementation of the
Phase 13B placeholder views; no change to core `src/` pipeline runtime
behaviour, governance, telemetry, or the SQLite schema; no root dependency
change. The backend code added must be read-only and deterministic.

**Acceptance criteria.** The export is deterministic — generating it twice
yields byte-identical JSON — and carries a top-level `schemaVersion`. The
frontend builds and typechecks against the aligned export through the adapter,
and the homepage and Pipeline Run Detail / Stage Timeline render from it with
no live backend. Display obeys the section 25 rules — no raw content, no
secrets, no raw blocked reasons, no overclaiming. The backend gates remain
green.

**Review gate.** GPT-5.5 review, Gemini critique, explicit user lock.

**Deferred from this subphase.** The operator workflow views (dashboard, runs
list, failure queue, governance/safety) remain placeholders and are built in
Phase 13D against this Phase 13C export contract. A future file-backed or
local-API adapter that produces the same contract shape from real local state
is also deferred. See `docs/frontend-gui-deferred-work-register.md`.

## Phase 13D — Operator Workflow Views

**Status.** **Locked.** The Phase 13D candidate delivered the **Governance
/ Safety** and **Failure / Recovery** views per the ordering
recommendation below, completed its Phase Closure Protocol (GPT-5.5
review, then Gemini SAFE TO LOCK with no required edits), and was locked
by explicit user decision. The remaining views in this subphase's scope
(the dashboard expansion, demo walkthrough, etc.) carry forward — Phase
13D.1 added the Evidence / Validation view below; Architecture Story,
Demo Walkthrough, Roadmap, and Settings / Config remain deferred to
Phase 13E or later.

**Objective.** Build the operator GUI views against the read-only
adapter: the dashboard, pipeline runs, pipeline run detail, stage
timeline, episode artifacts, failure queue, governance/review, and
observability evidence views, per `docs/operator-gui-view-model.md`.

**Allowed changes.** The operator GUI views and their navigation; empty,
loading, and error states; the read-only presentation of run, stage,
failure, governance, and observability data.

**Forbidden changes.** No mutation controls and no enabled operator
actions (retry, re-run, mark review, regenerate report stay disabled -
that is 13E); no backend API write path; no authentication; no cloud
deployment; no change to `src/`, the pipeline, the CLI, governance,
telemetry, or Docker behaviour.

**Acceptance criteria.** The operator GUI views render correctly against
demo data and (where available) local read-only data; the run-detail and
stage-timeline views make a run legible; all action affordances are
visibly present but disabled; empty/loading/error states and the
accessibility requirements from the view model are met.

**Delivered first views (locked).** Phase 13D expanded the placeholder
views in the recommended order: (1) **Governance / Safety** and (2)
**Failure / Recovery**. Both consume the locked Phase 13C static export
through new domain-specific view-model adapters
(`frontend/src/data/governanceAdapter.ts` and `failureAdapter.ts`) and
introduce CSS Modules for their two new components — the scoped styling
strategy carried forward into Phase 13D.1.

**Review gate.** GPT-5.5 review, Gemini SAFE TO LOCK, explicit user lock — all complete.

## Phase 13D.1 — Static Operator GUI Refinement / Evidence & Disabled Action Discipline

**Status.** **Locked** (2026-05-27; Gemini SAFE TO LOCK, no required edits;
user accepted). Phase 13D.1 is the last locked phase before Phase 13D.2.

**Objective.** Strengthen the operator GUI and portfolio / reviewer flow
before any controlled local action or mutation-boundary work, while
staying static and read-only. Phase 13D.1 makes the GUI more reviewable
and less likely to require rework when future controlled local actions
arrive: it standardizes the disabled future-action display across views,
replaces the Evidence / Validation placeholder with a real read-only
view, adds a small Demo / Active / Candidate Data Source framing card
(data snapshots, not deployment environments — no switcher implemented),
and lightly cleans navigation organization by extracting nav metadata
out of `App.tsx`.

**Allowed changes.** New reusable disabled-action component (real
`<button disabled={true}>`, no `onClick`, no fake handlers); new
real read-only Evidence / Validation view with the mandatory STATIC
PORTFOLIO DATA — NOT A LIVE CI/CD DASHBOARD disclaimer and
repository-relative evidence references; new evidence adapter (static
copy, no fetching, no runtime doc parsing, no live status); navigation
metadata extraction; small typed nav helper; CSS Modules for every new
component.

**Forbidden changes.** No mutation, no live API, no `fetch`/`axios`/
`localhost`/network call, no real action handlers, no Demo / Active /
Candidate snapshot switching, no promotion of candidate to active, no
backend command execution, no file writes, no server, no Phase 13E+
behaviour. No change to `src/storytime/operator_export.py`, the
committed static export JSON, the `storytime export-demo-ui` CLI
contract, or `src/storytime/cli/app.py`.

**Delivered at lock.** The new reusable `DisabledFutureActionCard` /
`DisabledFutureActionList` component pair backed by real
`<button disabled={true}>` elements with no `onClick` handlers; the
Governance / Safety and Failure / Recovery views refactored to consume
the new component; the real read-only Evidence / Validation view
(`EvidenceValidationView.tsx` + CSS Module) carrying the mandatory
STATIC PORTFOLIO DATA — NOT A LIVE CI/CD DASHBOARD disclaimer and
repository-relative evidence references; the evidence adapter
(`evidenceAdapter.ts`) with Demo / Active / Candidate Data Source
framing; the navigation-metadata extraction
(`frontend/src/navigation.ts`) with App.tsx slimmed from 228 to 136
lines; all gates green; state-discipline guard advanced for Phase
13D.1; protected backend contracts byte-identical to Phase 13D.

**Review gate.** GPT-5.5 review, Gemini critique, explicit user lock.
Completed 2026-05-27.

## Phase 13D.2 — Static Demo Walkthrough / Reviewer Story Path

**Status.** **Locked** (2026-05-27; Gemini SAFE TO LOCK, no required edits;
user accepted). Phase 13D.2 is the last locked phase before Phase 13E.

**Objective.** Turn the existing operator GUI views into a coherent
guided reviewer / demo path before any controlled local action or
mutation-boundary work. The view should answer "what should I click
first?", "what does this prove?", "what do I say about this in an
interview?", "where is the architecture boundary?", "how is this
local-first and safe?", "why is the frontend read-only?", and "what is
next, and why is it not live yet?". Phase 13D.2 deliberately absorbs
~80–90% of an Architecture Story narrative into the walkthrough as
embedded architecture-checkpoint cards, while leaving a standalone
Architecture Story page deferred.

**Delivered at lock.** A new real read-only Demo Walkthrough view
(`DemoWalkthroughView.tsx` plus its CSS Module) replacing the Phase
13D.1 placeholder; a new static view-model adapter
(`demoWalkthroughAdapter.ts`) holding the long-form route content
(route definitions, step definitions, architecture checkpoints,
deferred-work explanations, interview / SE talking points, repository
references, stable run-id constants); a simple segmented control with
local `useState<RouteId>` switching between four reviewer routes
(5-minute scan, 10-minute SE-style demo, technical deep-dive,
self-guided reviewer); in-line navigation affordances on route steps
calling back into the existing App-level `setView` / `inspectRun`
callbacks (no router); `frontend/src/navigation.ts` promoting Demo
Walkthrough to a real view; `App.tsx` rendering the new view; eight
embedded architecture-checkpoint cards absorbing ~80–90% of an
Architecture Story narrative; the deferred-work register updated
(Demo Walkthrough marked implemented; new "Standalone Architecture
Story / System Boundary Reference" deferred item).

**Review gate.** GPT-5.5 review, Gemini critique, explicit user lock.
Completed 2026-05-27.

## Phase 13E — Demo-Mode Action Preview / Operator Intent Boundary

**Status.** **Locked** (2026-05-27; Gemini SAFE TO LOCK, no required edits;
user accepted). Locked artifact
`storytime-phase13e-demo-mode-action-preview-operator-intent-boundary.tar.gz`,
SHA-256 `a997f2ca9d213e28e140f47c63336367c8feda46ed994b41300f86b99f8d8164`.
Phase 13E is the last locked phase before Phase 13F.

**Objective.** Turn the existing visibly-disabled future-action
affordances into explainable, non-executing **action previews** so
the operator GUI can demonstrate serious operator intent without
becoming consequential. The right framing is: *demo mode may
preview serious operator intent — demo mode must not create
consequential changes.* Phase 13E also introduces or clarifies the
eventual operating-mode model (Demo / Local / Cloud-Distributed) so
the reviewer understands why execution is deferred to future Local
mode or Cloud/Distributed mode, distinct from the existing **Demo /
Active / Candidate** data-snapshot framing.

**Allowed changes.** A new static view-model adapter
(`frontend/src/data/actionPreviewAdapter.ts`) holding typed
action-preview definitions (stable id, label, category, current
mode (Demo), execution status (Preview only / non-consequential),
target object references for run / stage / governance decision /
failure queue / evidence artifact, target context label, what the
operator is trying to accomplish, why blocked in Demo mode,
precondition checklist, evidence to inspect first, risk level and
explanation, illustrative future Local-mode request shape labelled
"Future request shape — illustrative only, not executable in Demo
mode", Cloud/Distributed considerations, audit expectations,
failure behaviour expectation, what remains disabled, related
view, optional related run id) plus operating-mode model constants
for Demo / Local / Cloud-Distributed; a new presentation component
(`frontend/src/components/ActionPreviewPanel.tsx` plus its CSS
Module) that maps over adapter data and renders the selected
preview with safety / honesty labels; light integration into
Failure / Recovery, Governance / Safety, and Evidence / Validation
**alongside** the existing `DisabledFutureActionCard` /
`DisabledFutureActionList` (real `<button disabled={true}>` with no
`onClick` — unchanged) via a separate, clearly-labelled "Preview
action plan" affordance that opens an inline preview panel using
local `useState<ActionPreviewId | null>` (no router, no Context, no
persistence); a first set of 3–5 action previews
(retry-failed-stage, inspect-trust-envelope, record-review-decision,
regenerate-operator-report, refresh-export); a small new Python
data-integrity test
(`tests/test_action_preview_data_integrity.py`) asserting run-id
and stage-id targets referenced by the adapter exist in the
committed static export — using existing pytest, no new dependency;
docs updates to the deferred-work register and the rest of the
State Preservation Bundle.

**Forbidden changes.** No real mutation path: no actual retry,
rerun, approval, rejection, report regeneration, file write,
database change, backend API call, subprocess or CLI execution, local
HTTP bridge, local server, `storytime serve`, `storytime ui --live`,
or POST/PUT/PATCH/DELETE call. No Local mode, no Cloud/Distributed
mode, no Demo / Local / Cloud mode switching, no Demo / Active /
Candidate snapshot switching, no persisted action history, no
generated audit logs pretending execution occurred, no dynamic
local file loading, no runtime export reload, no hash routing, no
browser History API routing, no Phase 13F+ work. No `fetch`,
`axios`, `XMLHttpRequest`, `WebSocket`, `localStorage`,
`sessionStorage`, router libraries, state libraries, UI libraries,
charting libraries, schema-validation dependencies, backend web
frameworks, local server dependencies, or new React Context
providers such as `ActionContext`, `PreviewContext`, or
`ModalContext`. No global preview / action state; action-preview
state stays local and transient. No `onClick` on the existing
disabled button; the existing `DisabledFutureActionCard` must not
be modified. No simulated execution, no fake loading spinners, no
mock success toasts, no `setTimeout`-based fake workflows, no fake
progress bars, no "Succeeded" / "Submitted" / "Completed" / "Audit
created" rendering for preview actions; the user journey must end
at an explicitly disabled execution boundary. No change to
`src/storytime/operator_export.py`, the committed static export
JSON, the `storytime export-demo-ui` CLI contract, or
`src/storytime/cli/app.py`. No standalone Architecture Story page
(it remains deferred from Phase 13D.2 §14).

**Acceptance criteria.** The Action Preview system is data-driven
(long-form preview content lives in the adapter, not buried in
JSX); the component maps over adapter data and renders the selected
preview; 3–5 previews exist initially with the listed required
fields; the panel is integrated into the recommended views
alongside, not replacing, the existing disabled-action display; the
existing disabled buttons remain visibly disabled and unhandled
(`grep -n "DisabledFutureActionCard" frontend/src` shows no new
`onClick` on the disabled element); the panel uses local `useState`
only (no Context, no router, no `localStorage` / `sessionStorage`,
no URL or History API manipulation); the required safety / honesty
labels are present in the rendered output ("Demo mode", "Preview
only", "No state changed", "Action plan, not action result",
"Execution requires future Local mode", "Cloud/Distributed
execution is not implemented", "No audit record generated because
nothing executed", "No local bridge is running", "No backend
command was called"); the data-integrity test passes and asserts
all hardcoded action-preview run-id targets exist in the static
export; all gates green (backend pytest / ruff / mypy /
import-linter / doctor; frontend typecheck / build); the
state-discipline guard is advanced for Phase 13E; protected backend
contracts are byte-identical to Phase 13D.2; the Evidence /
Validation STATIC PORTFOLIO DATA disclaimer remains undiluted; the
operating-mode model (Demo / Local / Cloud-Distributed) is
explained in the adapter copy and distinguished from the
data-snapshot framing (Demo / Active / Candidate).

**Review gate.** GPT-5.5 review, Gemini critique, explicit user
lock.

## Phase 13F — Local Bridge Architecture & Contract Baseline

**Status.** Implementation candidate (pending review, not locked).

**Objective.** Establish the architecture and contract for a future local
bridge — the trusted local process that a future Local mode would use to
execute the operator actions Phase 13E only previews — **without implementing
any of it**. This is the architecture lock before any bridge / mutation code,
the same "architecture before code" principle that placed Phase 13A before any
frontend code. The central principle established: *the frontend is an operator
surface, not the durable storage layer* — durable state lives outside the
browser in an explicit workspace / storage target with clear export, reset,
backup, and recovery semantics, so StoryTime never repeats the RoundTable
browser-storage failure mode.

**Allowed changes.** Eleven new architecture / contract docs
(`docs/local-bridge-architecture.md` with the execution-timing policy and
Gemini-risk table, `docs/externalized-state-architecture.md`,
`docs/browser-storage-policy.md`, `docs/local-mode-workspace-layout.md`,
`docs/storage-targets-architecture.md`, `docs/action-execution-boundary.md`,
`docs/local-action-dto-spec.md`, `docs/local-action-audit-spec.md`,
`docs/local-mode-storage-contract.md`,
`docs/local-action-queue-observability.md`,
`docs/phase13f-local-bridge-contract-readiness.md`); non-runtime JSON example
fixtures under `docs/examples/`; one new Python contract-examples test
(`tests/test_local_mode_contract_examples.py`, plain Python, no JSON-schema
dependency); the narrow, explicitly authorized mechanical advance of the
state-discipline guard; and the State Preservation Bundle synchronization.

**Forbidden changes.** No runtime code: no local bridge, no server, no socket,
no subprocess, no async queue, no queue workers, no queue metrics / exporters,
no OpenTelemetry instrumentation, no storage providers, no provider
integrations, no runtime schema validation, no router / history, no browser
storage, no real Local mode, no Cloud/Distributed mode, no mutation / action
execution. No change to `src/`, `frontend/src/`, `frontend/package.json`,
`frontend/package-lock.json`, `pyproject.toml`, `uv.lock`, or
`frontend/src/data/storytime-demo-export.json`. No new dependency.

**Acceptance criteria.** The docs are explicit enough to prevent future
implementation drift; the security boundary (loopback-only, strict origin, no
arbitrary command, command-pattern router, action allowlist), the
execution-timing policy (async long-running actions, `202 Accepted` +
`actionRequestId`/`jobId`, acceptance ≠ success, export refresh after a durable
write, refresh-race avoidance), and the queue-observability model are all
defined but not implemented; the example fixtures are valid, allowlist-only,
secret-free, and labelled future / documentation-only; the contract-examples
test passes; protected surfaces are byte-identical to the locked Phase 13E
source.

**Review gate.** GPT-5.5 review, Gemini critique, explicit user lock.

## Phase 13G — Local Bridge Implementation / Controlled Local Actions / Safe Mutation Boundary

**Status.** Not started.

**Objective.** Implement the smallest possible loopback-only Python local bridge
against the Phase 13F contract, and add the first controlled operator actions to
the GUI — and only within an explicit, safe mutation boundary. This is the
single subphase that introduces a real bridge and real (non-preview) mutation,
on top of the Phase 13E preview surface and the Phase 13F contract.

**Allowed changes.** A minimal Python-owned local bridge (loopback-only binding,
strict origin allowlist, command-pattern router, action allowlist
`retry_failed_stage` / `inspect_trust_envelope` / `refresh_export`), the
observable async action queue, and the action model from
`docs/frontend-backend-contract.md` implemented for local operation only. Each
mutation maps to an existing governed backend operation and obeys the locked
Architecture Baseline section 25 mutation gate and Trust Envelope governance.

**Forbidden changes.** No mutation that bypasses governance or the section 25
rules; no new mutation that does not map to an existing governed CLI operation;
no destructive action; no arbitrary command / shell / SQL; no non-loopback
binding; no provider credentials in the browser; no authentication assumption;
no cloud deployment; no change to what the underlying governed operations do —
the bridge invokes them, it does not redefine them.

**Acceptance criteria.** Operator actions are available only for eligible runs,
always route through the existing governed operations, never bypass the Trust
Envelope or the fail-closed gate, are confirmable and auditable, and run through
an observable queue. A reviewer can confirm the mutation boundary and the bridge
security boundary are explicit and safe.

**Review gate.** GPT-5.5 review, Gemini critique, explicit user lock. This gate
is the most safety-sensitive in Phase 13.

## Phase 13H — Portfolio Website Polish / Public Demo Packaging

**Status.** Not started.

**Objective.** Polish the portfolio website and package it for public demo:
final content pass, the tiered reviewer paths, the demo walkthrough, and a
clean public-hostable static build.

**Allowed changes.** Content and presentation polish; the public demo packaging
and static-build output; alignment with `docs/public-repository-readiness.md`.

**Forbidden changes.** No new operator mutation; no backend behaviour change;
no authentication; no cloud deployment (hosting readiness is the optional 13I);
no new product feature.

**Acceptance criteria.** The portfolio website is honest, complete, and
reviewer-ready; the demo walkthrough works without a live backend; the public
build passes the public-repository-readiness gates.

**Review gate.** GPT-5.5 review, Gemini critique, explicit user lock.

## Optional Phase 13I — Deployment / Hosting Readiness

**Status.** Not started (optional / contingency).

**Objective.** If, and only if, public hosting is wanted: prepare the static
portfolio build for hosting. This subphase is optional and exists only if a
hosting need is explicitly identified.

**Allowed changes.** Hosting configuration for a static build; documentation of
the hosting path; the public-readiness checklist applied.

**Forbidden changes.** No cloud *backend*; no hosted operator API; no
authentication; no multi-tenancy; no change that makes the operator GUI depend
on a cloud backend. Hosting, if done, hosts the static portfolio site, not a
live operator backend, unless a separate future phase explicitly authorizes
otherwise.

**Acceptance criteria.** If undertaken: a documented, repeatable way to host
the static portfolio build, with the local-first operator GUI unaffected. If a
hosting need is never identified, Phase 13I is simply not done and Phase 13
closes after Phase 13H.

**Review gate.** GPT-5.5 review, Gemini critique, explicit user lock.



## Subphase summary

| Subphase | Scope | Status |
|----------|-------|--------|
| 13A | Portfolio Website / Operator GUI Architecture Baseline - architecture, content model, view model, frontend/backend contract, this roadmap (documentation only) | locked |
| 13B | Typed Static Portfolio Shell / Minimal Visual Pipeline Scaffold - the first frontend scaffold: typed read-model contract and static demo data, the portfolio homepage, one Pipeline Run Detail view with a Stage Timeline, and placeholders for the remaining views | locked |
| 13C | Deterministic Read-Only Static Export / Frontend Data Alignment - a backend-native deterministic read-only static export (module + `storytime export-demo-ui` CLI command + committed JSON with a `schemaVersion`), frontend types and an adapter aligned to it, and the homepage and Pipeline Run Detail view rewired onto the adapter; static and read-only, no live backend | locked |
| 13D | Operator Workflow View Expansion - real read-only Governance / Safety and Failure / Recovery views with domain-specific adapters and inspect-this-run drill-down | locked |
| 13D.1 | Static Operator GUI Refinement / Evidence & Disabled Action Discipline - reusable disabled-action component, real Evidence / Validation view (STATIC PORTFOLIO DATA disclaimer), Demo / Active / Candidate Data Source framing, navigation-metadata extraction | locked |
| 13D.2 | Static Demo Walkthrough / Reviewer Story Path - real read-only guided demo walkthrough view with four reviewer routes, embedded architecture-checkpoint cards, deferred-work section, interview talking-point cards; absorbs ~80–90% of an Architecture Story narrative | locked |
| 13E | Demo-Mode Action Preview / Operator Intent Boundary - static Demo-mode Action Preview system (adapter + panel + CSS Module) wired alongside the existing disabled-action display; first set of action previews (retry-failed-stage, inspect-trust-envelope, record-review-decision, regenerate-operator-report, refresh-export); operating-mode model (Demo / Local / Cloud-Distributed) clarified distinct from data-snapshot framing (Demo / Active / Candidate); non-consequential, no mutation | locked |
| 13F | Local Bridge Architecture & Contract Baseline - documentation-and-static-fixture architecture / contract baseline for a future local bridge (eleven architecture docs, non-runtime JSON example fixtures, one contract-examples test); externalized-state principle, browser-storage policy, loopback-only / no-arbitrary-command security boundary, async execution-timing policy, future action DTO / audit contracts, queue-observability model; no runtime code | implementation candidate / pending review (not locked) |
| 13G | Local Bridge Implementation / Controlled Local Actions / Safe Mutation Boundary - minimal loopback-only Python bridge + observable queue + the first gated operator actions, on top of the Phase 13E preview surface and the Phase 13F contract | not started |
| 13H | Portfolio Website Polish / Public Demo Packaging - polish and public demo packaging | not started |
| 13I | Deployment / Hosting Readiness - optional, only if public hosting is wanted | not started (optional / contingency) |

## Guardrail: do not implement the frontend during architecture planning

Phase 13A is architecture and documentation only. The first line of frontend
code belongs to Phase 13B and may be written only after Phase 13A is reviewed
and locked. Any frontend directory, package file, framework choice, component,
route, or browser-runtime file appearing in a Phase 13A artifact is a scope
violation and a reason to reject the round. The end result of Phase 13 is a
portfolio website - but Phase 13A only designs it.
