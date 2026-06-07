<!--
  CANONICAL WALKTHROUGH — single source of truth for the StoryTime reviewer /
  demo path. Other demo/portfolio/narrative docs should point here or be marked
  superseded; do not fork a competing walkthrough. This is a written companion
  to the in-app Demo Walkthrough view (frontend/src/components/DemoWalkthroughView.tsx),
  which renders the same path against the existing read-only views.
-->

# StoryTime — Demo Walkthrough (canonical)

**What this is.** The one canonical, reviewer-facing walkthrough for StoryTime
after Phase 13J. It is read-aloud friendly and time-boxed, and every major claim
points to real repository evidence (see the [Evidence map](#evidence-map)). It
describes the system that exists today; it does not promise anything that does
not.

**One-sentence story.** StoryTime is a governed, observable, local-first
content-to-audio pipeline that demonstrates how a safe operator surface can
explain and control a local backend chain without giving the browser unsafe
authority.

## Truth labels (machine-checkable)

These structured labels are the load-bearing truths of the demo. Prose elsewhere
must stay consistent with them.

```yaml
static_demo: safe-read-only-snapshot
snapshot_sync: manual            # the visible snapshot changes only on an operator reload
live_sync: none                  # there is no automatic/background sync
local_bridge: optional-loopback-only
controlled_retry: one-action     # retry_failed_stage is the only frontend-submitted action
retry_semantics: acceptance-is-not-success
manual_reload: operator-triggered-read-model-refresh
tts_provider_mode: mock
tts_real_provider: deferred       # not bundled, disabled; provider-backed audio remains deferred
tts_owner: backend-cli            # generation is backend/CLI-owned; the browser cannot trigger it
tts_frontend_artifact_read: none  # the frontend does not read local TTS artifacts directly
tts_evidence: artifact-plus-manifest-plus-audit
browser_authority: operator-surface-not-source-of-truth
runtime_outputs: under-runs-gitignored-excluded-from-artifacts
deferred: frontend-generation, real-provider-adapter, audio-playback, rss-publishing, full-local-mode, cloud-distributed-mode
phase_state: 13J-locked; 13K-candidate-pending-review-not-locked; phase-13-open
```

## 1. At a glance (30 seconds)

StoryTime runs end-to-end on one machine: a CLI-driven pipeline, a local SQLite
store, on-disk artifact envelopes, and a deterministic operator export. The
website you are looking at is a static, read-only operator console rendered from
a committed export snapshot — it earns trust by being honest about what it is.

Why it is credible at a glance: every run is observable, a fail-closed human
governance gate authorizes a source before expensive work, the one state-changing
action the browser can submit is a single controlled retry to a loopback bridge,
and a governed mock-first TTS proof produces a local audio artifact with a
manifest and an audit trail. Everything beyond that is clearly marked deferred.

## 2. Guided demo (5–7 minutes)

A spoken-pace tour. Each stop says what to click, what it proves, and what to say.

1. **Overview — what StoryTime is (≈30s).** Open the Overview. The header chip
   reads *Demo Snapshot*; the banner names this a static, read-only build with no
   backend. Say: "the data is a committed export, not a live feed." The mode
   overview and boundary legend distinguish four surfaces: Static Demo, Local
   Bridge, Governed Local TTS Proof, and Manual Snapshot Reload.

2. **The browser is an operator surface, not the source of truth (≈30s).** Point
   at the boundary legend. Say: "static demo data, backend-owned local execution,
   and governed backend proof are three different things; the browser observes and
   submits narrow operator intents — the backend owns execution and state."

3. **Pipeline run detail (≈1m).** Open a run from the run list. Walk the stage
   timeline and the governance decision. Say: "every stage has measured timing and
   a status; a human-decided Trust Envelope authorized this source before any
   expensive stage ran."

4. **Local bridge — readiness and queue (≈1m).** Open Local Bridge. The operator
   workflow lists the order: understand mode → check readiness → review queue and
   lifecycle → submit a controlled retry → observe lifecycle → manually reload →
   inspect the TTS proof. These probes are read-only and loopback-only.

5. **Controlled retry (≈1m).** Show the controlled retry panel. Say: "this is the
   only state-changing action the browser submits, and it submits exactly one
   action type — `retry_failed_stage` — to a loopback bridge. A 202 means the
   request was accepted and queued; acceptance is not success, so the operator
   must observe the lifecycle."

6. **Manual snapshot reload (≈45s).** Show the reload panel. Say: "the visible
   snapshot is a transient read model; it refreshes only when the operator
   reloads the committed export, and the reload is validated all-or-nothing. It is
   a manual read-model refresh, and there is no automatic or background sync."

7. **Governed local TTS proof (≈1m).** Scroll to the read-only TTS proof summary.
   Say: "StoryTime can generate a local audio artifact through a governed,
   observable, auditable backend boundary. The provider here is the deterministic
   mock; a provider-backed adapter remains deferred and is not bundled. Generation
   is owned by the backend CLI (`storytime tts-proof`); the browser cannot trigger
   it, and this panel only reads static evidence. Mock output is labeled mock — it
   is not presented as provider audio." Note the artifact + manifest + audit/event
   lifecycle and the labeled (not authoritative) cost estimate.

Close: "Everything you saw is governed, observable, and local-first, and every
boundary is explicit. What is not built yet is clearly marked deferred."

## 3. Technical inspection appendix (≈15 minutes)

For an engineer reading the system itself.

- **Static export boundary.** The GUI imports one committed snapshot,
  `frontend/src/data/storytime-demo-export.json`, produced by
  `src/storytime/operator_export.py` (`storytime export-demo-ui`). The snapshot is
  deterministic; the same input yields the same export.
- **Read-only vs the optional bridge.** The static demo path makes no backend
  calls. The optional Local Bridge surface adds GET-only loopback observability
  (`frontend/src/data/localBridgeClient.ts`), one controlled retry POST
  (`frontend/src/data/localBridgeActions.ts`, action `retry_failed_stage` only),
  and a manual export reload (`frontend/src/data/staticExportReload.ts`). All are
  operator-initiated; there is no polling, WebSocket, EventSource, or background
  reload, and no browser durable storage.
- **Governed local TTS proof.** `src/storytime/tts_proof/` composes the existing
  deterministic mock TTS adapter behind a governance/cost guard
  (`boundary.py`), writes one atomic local WAV plus a manifest (`manifest.py`),
  and records a typed audit/event lifecycle (`events.py`) for an approved fixture
  (`fixtures/approved_proof_fixture.txt`). Source text is recorded as a SHA-256
  hash and character count — never raw text. A provider-backed adapter is not
  bundled and fails closed; provider-backed audio remains deferred.
- **Runtime outputs.** Proof runs write under `runs/`, which is git-ignored and
  excluded from locked artifacts by `scripts/build-artifact.sh`. Nothing the demo
  generates is committed.
- **State discipline.** `tests/test_failure_mode_regression.py` mechanically
  enforces the phase/lock/no-overclaim state; the frontend boundary guards
  (`tests/test_frontend_*`) and the TTS proof guards
  (`tests/test_tts_proof_*`) lock the safety boundaries described above.

Safe local run (mock-only): generate the export with `storytime export-demo-ui`,
run `storytime tts-proof` to produce the governed mock artifact under `runs/`, and
build the frontend with `npm run build`. Do **not** enable a provider-backed
adapter, supply provider credentials, or expose the bridge beyond loopback — the
canonical demo is mock-first and local-safe.

## 4. Deferred-capability register

Clearly not built yet (each is intentionally deferred, not hidden):

- **Frontend TTS generation** — the browser cannot trigger generation; it remains
  backend/CLI-owned.
- **Provider-backed TTS adapter** — not bundled; provider-backed audio remains
  deferred.
- **Audio playback in the browser** — deferred; the proof panel is read-only
  evidence, not a player.
- **RSS / episode publishing** — deferred.
- **Full Local mode** — deferred; today's local surface is the optional loopback
  bridge plus manual reload.
- **Cloud / distributed mode** — deferred; StoryTime is local-first.

## 5. Evidence map

Every major claim maps to a real repository path. Inspect these directly.

| Claim | Evidence path | What to inspect |
| --- | --- | --- |
| Operator console / mode + boundary vocabulary | `frontend/src/data/operatorConsole.ts` | Mode and boundary content the GUI renders |
| Mode overview UI | `frontend/src/components/ModeOverview.tsx` | The four-mode cards |
| Boundary legend UI | `frontend/src/components/BoundaryLegend.tsx` | Static / local / proof distinction |
| Operator workflow UI | `frontend/src/components/OperatorWorkflow.tsx` | The ordered local workflow |
| Read-only TTS proof summary UI | `frontend/src/components/TTSProofSummary.tsx` | Read-only evidence, no controls |
| In-app walkthrough path | `frontend/src/components/DemoWalkthroughView.tsx` | Rendered reviewer path |
| Walkthrough content model | `frontend/src/data/demoWalkthroughAdapter.ts` | Routes, deferred items, evidence refs |
| Static demo data source | `frontend/src/data/storytime-demo-export.json` | The one committed snapshot |
| Export generator | `src/storytime/operator_export.py` | Emits the typed export |
| Read-only bridge client (GET only) | `frontend/src/data/localBridgeClient.ts` | No mutation verbs |
| Controlled retry (single POST) | `frontend/src/data/localBridgeActions.ts` | `retry_failed_stage` only |
| Manual static export reload | `frontend/src/data/staticExportReload.ts` | Operator-triggered, validated |
| Local bridge backend | `src/storytime/local_bridge/` | Loopback bridge implementation |
| Governed TTS proof package | `src/storytime/tts_proof/` | Guarded mock-first chain |
| Governed boundary | `src/storytime/tts_proof/boundary.py` | Guard → mock → atomic write |
| TTS manifest | `src/storytime/tts_proof/manifest.py` | Manifest shape |
| TTS audit/event lifecycle | `src/storytime/tts_proof/events.py` | Event taxonomy |
| Approved fixture | `src/storytime/tts_proof/fixtures/approved_proof_fixture.txt` | The one allowlisted input |
| TTS proof behavior tests | `tests/test_tts_proof_governed_boundary.py` | Artifact/manifest/audit/redaction/cost |
| TTS proof static guards | `tests/test_tts_proof_static_guards.py` | No frontend generation control |
| Operator GUI polish guards | `tests/test_frontend_operator_gui_polish.py` | Read-only TTS framing |
| Bridge observability guards | `tests/test_frontend_bridge_observability.py` | GET-only, loopback-only |
| Controlled retry guards | `tests/test_frontend_controlled_retry_submission.py` | Acceptance ≠ success |
| Manual reload guards | `tests/test_frontend_static_export_reload.py` | No auto reload / sockets / storage |
| State-discipline guard | `tests/test_failure_mode_regression.py` | Phase / lock / no-overclaim |
| Archive hygiene / builder | `scripts/build-artifact.sh` | Runtime outputs excluded |
| Static export contract | `docs/frontend-static-export-contract.md` | The contract the GUI depends on |
| Local bridge architecture | `docs/local-bridge-architecture.md` | Bridge boundary design |
| Deferred-work register | `docs/frontend-gui-deferred-work-register.md` | Deferred items of record |

---

_Current state: Phase 13J locked; Phase 13K implementation candidate / pending
review / not locked; Phase 13 remains open (closure is a separate later
decision). If the committed export's baked phase value differs from this, treat
it as snapshot provenance — "snapshot generated by" — not the current system
phase._
