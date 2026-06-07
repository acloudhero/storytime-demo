# StoryTime — Interview Talking Points
<!-- CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md -->
> **Canonical demo path.** For the current, authoritative reviewer/demo
> walkthrough — the system modes and boundaries, the optional loopback
> local bridge, the one controlled retry (acceptance is not success), the
> manual snapshot reload (a read-model refresh, not a live sync), and the
> governed mock-first TTS proof (provider-backed audio remains deferred) —
> see [docs/demo-walkthrough.md](demo-walkthrough.md), the single source of
> truth and evidence map. This document is a secondary/historical narrative;
> where it differs, the canonical walkthrough wins.


Concise, study-friendly talking points for explaining StoryTime in an
interview. Each point is short enough to read aloud and is backed by something
concrete in the repository. Use it to rehearse; pair it with
`docs/solutions-engineer-narrative.md` for the longer pitches and
`docs/portfolio-demo-script.md` for a live walkthrough.

This document is part of Phase 12A and adds no product behaviour. It is honest
about scope — every boundary in `docs/known-limitations.md` still applies.

---

## System architecture

> "StoryTime is a five-stage content-to-audio pipeline — ingest, synthesize,
> assemble, publish, with operator approval gates woven in. A single
> `PipelineRunner` orchestrates it. The stages never call each other and never
> share mutable state: they hand off through versioned, hash-verified artifact
> envelopes. SQLite plus those on-disk artifacts are the single source of truth."

Key follow-ups if asked:
- No mutable god-object context — stages take a `StageInput` DTO and a frozen
  `RunnerContext`, and return a `StageResult`.
- `pipeline_run_id`, a ULID, is the durable correlation key across SQLite,
  artifacts, the event log, and traces.
- Backed by: `docs/architecture-baseline.md`, `docs/portfolio-overview.md`.

## OpenTelemetry instrumentation strategy

> "Observability is a design property, not a decoration. One `pipeline.run` span
> per run with child stage spans, eight purposeful low-cardinality metrics, six
> dashboards provisioned as code. Two rules make it honest: all OpenTelemetry
> imports are confined to one adapter module — enforced by an import-linter
> contract and an AST test — and an automated test fails the build if a
> dashboard charts a metric the code doesn't actually emit."

Key follow-up: telemetry goes as standard OTLP to a local Collector; the
Collector is the fan-out point, so routing to a backend would be a Collector
config change, not an application change. No commercial vendor integration is
implemented, and I don't claim one.

## Local-first design

> "Local-first is a charter decision. Every command runs against a local SQLite
> database and an on-disk artifact tree — no server, no database service, no
> external API. The core pipeline and the whole test suite run offline. It buys
> two things: a tiny trust surface, since nothing leaves the machine, and cheap
> reproducibility, since anyone can run the exact same scenarios in minutes."

Backed by: `docs/portfolio-overview.md` §6, `docs/known-limitations.md`.

## Workflow durability

> "The pipeline is single-process, but it's built with the discipline a durable
> distributed workflow needs. Approval gates are persisted pipeline stages — a
> paused run exits its process cleanly and resumes later as a fresh trace linked
> back to the original. Resume rebuilds a run from SQLite and hash-verifies every
> reused artifact before continuing, so a tampered artifact is refused, not
> silently trusted."

Key follow-up: the storage and event adapters are deliberately seam-shaped so
they could be swapped for cloud-native equivalents — that swap is not
implemented, but the contracts make it a clean substitution.

## Governance boundaries

> "There's a real, fail-closed governance gate. It derives a per-run Trust
> Envelope at ingest from the operator's licensing decision and hard-blocks the
> run before TTS and before RSS publishing unless the envelope is `APPROVED`.
> The crucial part is the honesty: it records a human decision — it performs no
> legal determination and is not a rights-clearance engine. Governance is source
> authorization, not viewpoint moderation."

Key follow-up: a static scanner runs inside the test suite and fails the build
if legal-overclaiming vocabulary appears outside the documents that legitimately
define it. Knowing exactly where a control's authority ends — and enforcing that
in code — is the point. Backed by: `docs/architecture-baseline.md` Section 24.

## Failure handling

> "Failure is a first-class, designed-for state. A failed run lands in a
> read-only `storytime queue` with a structured failure code and a next-step
> hint. There's exactly one mutation surface — `storytime rerun` — and it proves
> the retry is safe before acting: `--dry-run` previews the eligibility decision
> and changes nothing, the real command performs one bounded state reset and
> writes one audit event, and it hands control back to the operator rather than
> running a retry loop."

Key follow-up: a re-run can never bypass governance — a blocked run is simply
not eligible. Phase 11C inventoried the highest-risk failure paths and mapped
each to the tests and gates that protect it.

## Operator experience

> "Phase 10 extended observability from machine telemetry to operator
> observability — three layers: a static read-only HTML report to *see* what
> every run did, a deterministic queue to *triage* what needs attention, and one
> governed, audited command to *act*. The report has no JavaScript, no server,
> no external assets — it opens straight from the filesystem — and it's
> field-bounded so raw story text and secrets never reach generated output."

Key follow-up: every state change goes through an explicit CLI command; there is
no retry button anywhere. Keeping mutation in the CLI and out of the browser
keeps the report honestly read-only.

## Release-candidate hardening

> "Phase 11 turned the codebase into a release candidate without adding
> features. Four subphases: a documentation-first hardening baseline; a
> fresh-clone reproducibility verification done against a genuine clean
> extraction; a failure-mode and regression-hardening round that inventoried the
> risky paths and test-mapped each one; and an evidence pack consolidating the
> release-candidate proof. Six Docker-free quality gates pass — 580 tests, ruff
> and strict mypy clean, import-linter contracts kept, environment healthy."

Backed by: `docs/release-candidate-hardening.md`, `docs/final-validation-summary.md`.

## Tradeoffs and limitations

> "I'm deliberate about what StoryTime is *not*. It's not a production service —
> no users, no SLA, no cloud. No active alerting. The TTS is mock-grade and
> audio quality isn't measured. The observability stack is optional and
> Docker-dependent. The static report is a snapshot, not a live UI. Those are
> mostly deliberate scope decisions, and naming them is part of the discipline —
> a project that overclaims can't be trusted on the claims that matter."

Tradeoffs worth being able to defend:
- Static report vs. live dashboard — chose inspectable, diffable, offline-safe.
- Read-only queue vs. broker-backed queue — chose dependency-free determinism.
- Mock TTS vs. real engine — kept audio quality out of scope deliberately.
- Local-first vs. cloud — kept the trust surface small and the demo reproducible.

## Future cloud-native evolution

> "The architecture is shaped so cloud-native evolution is a substitution, not a
> rewrite. The storage and event adapters are seams; the Collector pattern means
> telemetry fan-out to a platform like Dynatrace or New Relic would be a
> Collector config change. None of that is implemented — it's deferred,
> unauthorized roadmap work — but the seams are real, and a portfolio narrative
> may *describe* the cloud-shaped architecture without claiming the project is
> cloud-deployed, because it is not."

Backed by: `docs/roadmap.md` ("Deferred / not authorized"),
`docs/phase12-readiness-handoff.md`.

## Why the project proves SE readiness

> "Solutions Engineering is four things: explaining observability architecture
> clearly, demonstrating it credibly, helping people instrument honestly, and
> being trusted on what a product does and doesn't do. StoryTime exercises all
> four — it's a readable worked example of source-of-truth-versus-view and the
> Collector pattern, it's reproducible enough to demo live with no provisioning,
> the metric-honesty build gate is the instrumentation discipline made concrete,
> and the project states its boundaries plainly. It doesn't prove production
> observability at scale, and I don't say it does — it proves I can reason
> about, build, explain, and honestly bound an observability-native system."

## The one-paragraph version

> "StoryTime is a local-first, observability-native content-to-audio pipeline
> with a disciplined operator-experience layer: a static read-only HTML report,
> a deterministic failure queue, one governed and audited mutation command, a
> fail-closed Trust Envelope governance gate, and reproducible demo fixtures. It
> runs on one machine with no cloud account, keeps SQLite as the source of truth
> and OpenTelemetry as an optional view, and is built under a multi-model review
> process with an append-only history. Every claim is backed by a test, a config
> file, or a document — and the boundaries are stated as plainly as the
> features."

---

## Quick honesty checklist before any interview

Do not say StoryTime: integrates a named commercial observability vendor; has
production alerting, paging, or an error budget; is deployed or has users;
performs a legal determination or clears rights. It emits standard
OpenTelemetry to a local Collector, it is a local single-operator project, and
its governance records a human decision. Stating the boundaries is the
credibility, not a weakness in it.
