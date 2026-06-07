# StoryTime — Portfolio Website Content Model
<!-- CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md -->
> **Canonical demo path.** For the current, authoritative reviewer/demo
> walkthrough — the system modes and boundaries, the optional loopback
> local bridge, the one controlled retry (acceptance is not success), the
> manual snapshot reload (a read-model refresh, not a live sync), and the
> governed mock-first TTS proof (provider-backed audio remains deferred) —
> see [docs/demo-walkthrough.md](demo-walkthrough.md), the single source of
> truth and evidence map. This document is a secondary/historical narrative;
> where it differs, the canonical walkthrough wins.


What the eventual Phase 13 portfolio website must present, section by section.
It converts the Phase 0-12 portfolio evidence the repository already contains
into a set of website sections, so a future implementation round knows what
each page is for and where its content comes from.

**Phase 13A defines this content model; it does not build the website.** No
pages, HTML, or frontend code are created in Phase 13A. The content for each
section already exists in the repository - this model maps it; it does not
invent new claims. See `docs/phase13-portfolio-website-architecture.md` and
`docs/phase13-roadmap.md`.

## Audience and purpose

The portfolio website is the public-presentation half of the Phase 13 property
(the other half is the operator GUI, specified in
`docs/operator-gui-view-model.md`). It must work for a hiring manager, a
technical interviewer, and an observability reviewer, and it must let any of
them understand StoryTime without cloning the repository or running a backend.

Two rules apply to every section below:

- **Honesty.** The website presents StoryTime as a portfolio-grade engineering
  artifact, not a deployed product. It must not claim users, an SLA, cloud
  hosting, active alerting, an error-budget policy, a commercial-vendor
  integration, a legal determination, or a rights-clearance capability. Every
  claim must be backed by a real repository artifact.
- **Evidence-linked.** Each section names the existing documents and artifacts
  its content comes from, so a reviewer can verify it and a future
  implementation round knows the source material.

## Homepage narrative

**Purpose.** Tell a first-time visitor, in one screen, what StoryTime is and
why it is worth a closer look, and route them to a review path that fits their
time budget.

**Content.** A concise statement that StoryTime is a local-first,
observability-native, CLI-driven content-to-audio pipeline; that the podcast
pipeline is the vehicle and the subject is engineering and operational
discipline; that it is a portfolio project, not a deployed product. The tiered
reviewer paths (5-minute, 15-minute, deep) as the primary call to action.

**Source material.** `docs/portfolio-overview.md`,
`docs/portfolio-demo-narrative.md`, `docs/final-portfolio-handoff.md`, the
`README.md` "For reviewers" section, `docs/portfolio-public-copy.md`.

## Architecture section

**Purpose.** Explain how StoryTime is built so a technical reviewer can judge
the engineering.

**Content.** The five-stage pipeline (ingest -> synthesize -> assemble ->
publish) with the operator approval gates; SQLite plus on-disk artifact
envelopes as the source of truth and OpenTelemetry as an optional view; stages
communicating only through versioned, hashed artifact envelopes; the
mechanically enforced import boundaries (import-linter); the `PipelineRunner`
as the sole orchestrator; and the multi-model RoundTable workflow under the
Phase Closure Protocol.

**Source material.** `docs/architecture-baseline.md`, `docs/canonical-state.md`,
`docs/telemetry-map.md`, `docs/phase-closure-protocol.md`, `LLM_DIRECTOR.md`.

## Observability section

**Purpose.** Show the observability story - the strongest Solutions-Engineer /
OpenTelemetry signal in the project.

**Content.** What telemetry StoryTime emits (one `pipeline.run` span per run
with child stage spans, W3C trace context stamped into artifact envelopes,
linked traces across approval gates, a closed metric set); the Collector-owned
fan-out model and why it keeps telemetry vendor-neutral; the dashboards-as-code
and the demo harness; the SLO/SLI narrative and its honest account of what
cannot be measured. It must say plainly that telemetry is optional - the
default `noop` adapter changes no behaviour - and that there is no production
deployment and no commercial-vendor integration.

**Source material.** `docs/slo-sli.md`, `docs/dashboard-guide.md`,
`docs/observability-demo.md`, `docs/telemetry-map.md`, `docs/runbook.md`,
`docs/observability-governance-talking-points.md`, `docs/portfolio-notes.md`.

## Governance / safety section

**Purpose.** Show that StoryTime handles content governance honestly and
fails closed.

**Content.** The Trust Envelope - a durably recorded, human-decided licensing
record; the fail-closed gate that hard-blocks before TTS, audio, and RSS
publish unless an `APPROVED` envelope exists; governance as source
authorization, not viewpoint moderation; the static legal-hallucination gate.
The honest non-goals stated explicitly: StoryTime is not a legal
rights-clearance engine, performs no legal determination, and is not a
content-moderation system; the operator is the source of truth for licensing
decisions.

**Source material.** `docs/architecture-baseline.md` section 24,
`docs/observability-governance-talking-points.md`, `docs/known-limitations.md`,
the `storytime.governance` package as referenced evidence.

## Demo walkthrough section

**Purpose.** Let a reviewer who will not run the backend still see what a run
looks like end to end.

**Content.** A narrated walk through the demo scenarios - the successful golden
path, a retryable technical failure, a governance-blocked source, a
needs-review approval gate, a rerun. What the operator sees at each step. This
section pairs naturally with the operator-GUI demo-data mode: the same demo
fixtures back both.

**Source material.** `docs/demo.md`, `docs/portfolio-demo-narrative.md`,
`docs/demo-talk-track.md`, `docs/portfolio-demo-script.md`, `docs/demo-script.md`,
`docs/operator-experience-walkthrough.md`, the `demo/` fixtures.

## Evidence / review packet section

**Purpose.** Let any reviewer verify any claim, and let a Solutions-Engineer
interviewer map competencies to evidence.

**Content.** The claim-to-evidence index - each portfolio claim mapped to the
test, config file, source module, or document that backs it; the
Solutions-Engineer competency-to-evidence matrix; the release-candidate
evidence pack and the final validation summary. The message of this section is
"check anything here against a real file".

**Source material.** `docs/portfolio-evidence-index.md`,
`docs/se-interview-evidence-matrix.md`,
`docs/release-candidate-evidence-pack.md`, `docs/final-validation-summary.md`,
`docs/verification-log.md`.

## Project timeline section

**Purpose.** Tell the story of disciplined iteration - StoryTime as a project
that advanced through reviewed, locked phases.

**Content.** The phase history from Phase 0 through the current phase, told as a
narrative: each phase implemented, independently reviewed, critiqued, and only
then locked by explicit decision; the append-only state discipline; the
RoundTable recovery doctrine. It should make the *process* legible, since the
process is itself part of the portfolio.

**Source material.** `docs/phase-history.md`, `docs/canonical-state.md`,
`docs/roadmap.md`, `docs/phase-closure-protocol.md`.

## Technical depth section

**Purpose.** Give a reviewer who wants the full picture a deeper, honest
technical read.

**Content.** The locked Architecture Baseline and its amendments (section 16
containerization, section 23 telemetry fan-out, section 24 governance, section
25 operator experience); the DTO / context model; the blue/green deployment
path; the optional local containerization; the failure-mode and
regression-hardening posture. This section is for the reader who will not be
satisfied by the overview.

**Source material.** `docs/architecture-baseline.md`,
`docs/deployment-bluegreen-option-a.md`,
`docs/deployment-bluegreen-option-b.md`, `docs/deployment-containerized.md`,
`docs/failure-mode-regression-hardening.md`, `docs/regression-risk-register.md`,
`docs/failure-mode-test-matrix.md`.

## Limitations section

**Purpose.** State the boundaries and non-goals plainly - the honesty of this
section is itself a credibility signal.

**Content.** StoryTime is not a deployed product; no users, no SLA, no cloud
tenancy; no commercial-vendor observability integration; no legal
rights-clearance; the known functional carryover (the unimplemented
`storytime clean` retention policy, OI-15); the demo-grade nature of the
containerization and blue/green paths. The website must not soften these.

**Source material.** `docs/known-limitations.md`, `docs/open-issues.md`,
`docs/portfolio-public-copy.md` ("what it is not").

## Future roadmap section

**Purpose.** Show what is intentionally not built yet, including the Phase 13
GUI track itself.

**Content.** The deferred / not-authorized items (cloud deployment,
image-registry path, Postgres migration, production blue/green convergence,
multi-host / HA, authentication); the Phase 13 portfolio-website / operator-GUI
track and its subphase plan. The website should be candid that it is itself the
output of an in-progress phase.

**Source material.** `docs/roadmap.md` (deferred / not-authorized section and
the Phase 13 material), `docs/phase13-roadmap.md`, `docs/GUI_vision.md`,
`docs/phase13-portfolio-website-architecture.md`.

## Call-to-action / reviewer path section

**Purpose.** Tell a reviewer exactly how to go deeper, in the order that suits
them.

**Content.** The tiered reviewer paths spelled out: the 5-minute path (read the
narrative and the overview), the 15-minute path (architecture and evidence),
the deep path (full architecture and the technical-depth section); how to clone
and run the demo; how to use the reviewer checklist; how to contact the author.
This section operationalizes the homepage's call to action.

**Source material.** `docs/final-portfolio-handoff.md`,
`docs/demo-reviewer-checklist.md`, `docs/fresh-clone-checklist.md`,
`docs/local-setup-runbook.md`, the `README.md` "For reviewers" section.

## Content honesty checklist

Before the portfolio website is published (Phase 13F and the
`docs/public-repository-readiness.md` gates), every section must pass:

- No claim of a production deployment, users, an SLA, or cloud hosting.
- No claim of a commercial-vendor observability integration.
- No claim of a legal determination or rights-clearance capability.
- Every factual claim traceable to a repository artifact.
- The limitations section present, prominent, and unsoftened.
- The website's own in-progress status (Phase 13) stated honestly.
