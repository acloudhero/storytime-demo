# StoryTime — Final Portfolio Handoff
<!-- CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md -->
> **Canonical demo path.** For the current, authoritative reviewer/demo
> walkthrough — the system modes and boundaries, the optional loopback
> local bridge, the one controlled retry (acceptance is not success), the
> manual snapshot reload (a read-model refresh, not a live sync), and the
> governed mock-first TTS proof (provider-backed audio remains deferred) —
> see [docs/demo-walkthrough.md](demo-walkthrough.md), the single source of
> truth and evidence map. This document is a secondary/historical narrative;
> where it differs, the canonical walkthrough wins.


A concise handoff for a cold reader: a fresh LLM session, a hiring manager, a
technical interviewer, or an observability reviewer. It explains what the final
Phase 12 portfolio package contains, how to navigate it, and the recommended
review path for each kind of reviewer.

This document is written by Phase 12D — Phase 12 Closure Plan / Final Portfolio
Handoff Definition. It is a navigation and orientation document; it adds no
product behaviour and grants no authority to begin Phase 13.

## Current state snapshot

- **What StoryTime is.** A local-first, CLI-driven, observability-native
  content-to-audio pipeline: it converts approved CC0 / US-public-domain text
  into podcast-ready audio, an RSS feed, and a traceable record of every run.
  SQLite plus on-disk artifact envelopes are the source of truth; OpenTelemetry
  is an optional view. It is a portfolio-grade Solutions-Engineering /
  OpenTelemetry demo.
- **What it is not.** It is not a deployed product — no users, no SLA, no cloud
  tenancy — and it says so plainly in `docs/known-limitations.md`. No public
  release has happened; `docs/public-repository-readiness.md` is the gated
  checklist for that future action.
- **Phase state.** Phase 10 — Product UI / Operator Experience — is CLOSED.
  Phase 11 — Release Candidate Hardening — is CLOSED. Phase 12 — Portfolio / SE
  Demo Packaging — is STARTED and **not** closed. Phase 12A, 12B, and 12C are
  locked; Phase 12C is the last locked phase. Phase 12D — Phase 12 Closure Plan
  / Final Portfolio Handoff Definition — is an implementation candidate,
  pending review, **not** locked. Phase 12E is optional, future,
  contingency-only work and is not started. Phase 13 — Operator GUI / Decoupled
  Frontend Vision — is roadmap-preserved only and **not** started.
- **Authoritative current status** lives in `docs/handoff-state.md`; the
  append-only history lives in `docs/canonical-state.md` and
  `docs/phase-history.md`.

## Portfolio review path: 5-minute reviewer

For a hiring manager or recruiter deciding whether to look closer:

1. `README.md` — the "For reviewers — start here" section: what it is, status,
   how to run it, where to read the story.
2. `docs/portfolio-demo-narrative.md` — the concise demo narrative: the
   business problem, the architecture, why observability matters, the
   governance posture, and the intentional out-of-scope boundaries.
3. `docs/portfolio-overview.md` — the plain-English portfolio overview.

Five minutes here is enough to judge whether StoryTime demonstrates the
engineering and Solutions-Engineering skills being screened for.

## Portfolio review path: 15-minute technical reviewer

For a technical interviewer who wants to confirm the claims are real:

1. The 5-minute path above.
2. `docs/portfolio-evidence-index.md` — the claim-to-evidence index: each
   portfolio claim mapped to the test, config, source file, or document that
   backs it. Spot-check two or three claims against the named files.
3. `docs/se-interview-evidence-matrix.md` — the Solutions-Engineer
   competency-to-evidence matrix.
4. `docs/demo.md` with `docs/demo-reviewer-checklist.md` — the reproducible
   demo and its reviewer wrapper; skim to confirm the demo is real and offline.
5. `docs/known-limitations.md` — confirm the project states its own boundaries
   honestly.

## Portfolio review path: deep architecture reviewer

For an observability or architecture reviewer who wants the full picture:

1. The 15-minute path above.
2. `docs/architecture-baseline.md` — the canonical architecture, including
   Section 24 (governance law) and Section 25 (operator-experience law).
3. `docs/telemetry-map.md` and `docs/slo-sli.md` — the OpenTelemetry surface
   and the service-level indicators.
4. `docs/observability-governance-talking-points.md` and
   `docs/observability-demo.md` — how the observability and governance story is
   told and demonstrated.
5. `docs/phase-history.md` and `docs/canonical-state.md` — the full RoundTable
   phase lineage, every lock recorded append-only.
6. `tests/` and the six Docker-free validation gates — run them; they are
   offline and deterministic.

## Suggested demo flow

Use `docs/demo-talk-track.md`, which scripts the demo at 5-, 10-, and
20-minute lengths and includes interviewer Q&A pivots and a "what to say if the
demo cannot be run live" fallback. The authoritative commands are in
`docs/demo.md`; the talk track narrates them and does not replace them. A
typical live flow: run `storytime doctor`, run the seeded demo pipeline, show
the generated operator report and the run record, then open the trace view to
show the same run as telemetry. The narration emphasises that SQLite and the
artifact envelopes are the source of truth and the dashboard is a projection.

## Evidence map

| What a reviewer wants to confirm | Where to confirm it |
|----------------------------------|---------------------|
| The pipeline runs and is reproducible | `docs/demo.md`, `docs/fresh-clone-checklist.md`, `docs/operator-reproducibility-checklist.md` |
| Claims map to real artifacts | `docs/portfolio-evidence-index.md` |
| Solutions-Engineering competencies are demonstrated | `docs/se-interview-evidence-matrix.md` |
| The architecture and its governance/operator law | `docs/architecture-baseline.md` (Sections 24–25) |
| Observability is real, not decorative | `docs/telemetry-map.md`, `docs/slo-sli.md`, `docs/observability-demo.md` |
| Failure modes are understood and tested | `docs/failure-mode-test-matrix.md`, `docs/regression-risk-register.md` |
| The project states its own limits | `docs/known-limitations.md` |
| Release-candidate hardening was done | `docs/release-candidate-evidence-pack.md`, `docs/final-validation-summary.md` |
| Phase history and every lock | `docs/canonical-state.md`, `docs/phase-history.md` |

## Explicit limitations

- StoryTime is a portfolio and demo project, not a deployed service. There are
  no real users, no SLA commitment, and no cloud tenancy.
- No public release has been performed. `docs/public-repository-readiness.md`
  is a pre-publication checklist with hard "do not publish until verified"
  gates; it is not evidence that publication happened.
- The observability vendor integrations are export profiles and demo wiring,
  not a live monitored production estate.
- `docs/known-limitations.md` is the authoritative, complete statement of
  scope boundaries and should be read alongside any portfolio claim.

## Next-phase boundary

After Phase 12 closes, the likely next major phase is Phase 13 — Operator GUI /
Decoupled Frontend Vision — preserved in the roadmap and in
`docs/GUI_vision.md`. Phase 13 is **NOT STARTED**. Nothing in Phase 12,
including Phase 12D, implements a GUI or frontend, creates a frontend
directory, adds JavaScript or UI runtime code, or chooses a framework. Phase 13
requires its own explicit authorization under the Phase Closure Protocol;
closing Phase 12 does not start it. Until that authorization, the Phase 13
material in the repository is vision and roadmap only.
