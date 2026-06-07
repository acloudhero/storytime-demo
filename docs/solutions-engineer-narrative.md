# StoryTime — Solutions Engineer Narrative
<!-- CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md -->
> **Canonical demo path.** For the current, authoritative reviewer/demo
> walkthrough — the system modes and boundaries, the optional loopback
> local bridge, the one controlled retry (acceptance is not success), the
> manual snapshot reload (a read-model refresh, not a live sync), and the
> governed mock-first TTS proof (provider-backed audio remains deferred) —
> see [docs/demo-walkthrough.md](demo-walkthrough.md), the single source of
> truth and evidence map. This document is a secondary/historical narrative;
> where it differs, the canonical walkthrough wins.


A document built to help explain StoryTime in interviews and conversations,
oriented toward a **Solutions Engineer** or observability-focused role. It
gives the project at several depths — a 30-second pitch, a 2-minute pitch, and
a deep technical explanation — plus framings for the business, observability,
OpenTelemetry, and governance angles a Solutions Engineer is asked about.

It is honest about scope. StoryTime demonstrates **observability-native
thinking** and an architecture **compatible with** OpenTelemetry-centred
operations. It does **not** integrate, and this document does not claim it
integrates, any specific commercial observability vendor.

This document is part of Phase 12A and adds no product behaviour. Companion
documents: `docs/portfolio-overview.md`, `docs/interview-talking-points.md`,
`docs/portfolio-demo-script.md`, `docs/observability-governance-talking-points.md`,
and `docs/known-limitations.md`.

---

## 1. 30-second pitch

> "StoryTime is a local-first content-to-audio pipeline I built to be
> observable and operable *honestly*. It turns approved public-domain text into
> podcast audio and an RSS feed, but the real subject is engineering
> discipline: SQLite is the source of truth, OpenTelemetry is a view over it,
> every architectural boundary is enforced by a test or a linter, and the
> operator experience is three layers — a static report to see, a deterministic
> queue to triage, and one governed, audited command to act. It runs on one
> machine with no cloud account, and every claim in it is backed by a test or a
> document."

## 2. 2-minute pitch

> "StoryTime is a Python content-to-audio pipeline — approved text in, podcast
> audio plus an RSS feed plus a traceable run record out. I built it as a
> proving ground for the engineering and operational discipline a real
> distributed system needs, in a system small enough to read end to end.
>
> The architecture is deliberate. A run moves through five stages — ingest,
> synthesize, assemble, publish, with operator approval gates woven in — and the
> stages communicate only through versioned, hash-verified artifact envelopes,
> never through shared mutable state. SQLite and those on-disk artifacts are the
> single source of truth. OpenTelemetry is an *optional view* over that truth:
> with the default no-op adapter, no telemetry is emitted and the pipeline
> behaves identically, so observability can fail without the pipeline failing.
>
> It is observability-native, held to an honesty standard. There's one
> `pipeline.run` span per run with child stage spans, eight purposeful
> low-cardinality metrics, and six dashboards provisioned as code — and an
> automated test fails the build if a dashboard charts a metric the code
> doesn't actually emit.
>
> It has a real governance layer — a fail-closed gate that records a human
> licensing decision and hard-blocks before the expensive stages unless the
> source is approved — and it's careful never to overclaim: it records a human
> decision, it doesn't perform a legal determination.
>
> And it's built for operators: a static read-only HTML report, a deterministic
> failure-triage queue, and exactly one governed, audited mutation command. It's
> local-first, reproducible by anyone in minutes, and built under a multi-model
> review process with an append-only history. What it deliberately is *not* is a
> production service — no users, no SLA, no cloud — and naming that boundary is
> part of the story."

## 3. Deep technical explanation

For a technical interviewer who wants the architecture, not the elevator pitch.

**Pipeline and contracts.** A run is orchestrated by a single `PipelineRunner`
through five stages. Stages take a serializable `StageInput` DTO plus a minimal
frozen `RunnerContext` and return a `StageResult` bundling a `StateUpdate` —
there is no mutable god-object context. Inter-stage communication is exclusively
through versioned, hashed artifact envelopes that carry the W3C `traceparent`
where applicable. A stage never calls another stage. This is the contract a
queue-decoupled distributed pipeline needs, practised in-process.

**Source of truth.** Durable state lives in SQLite (WAL mode): run, stage,
artifact, and approval tables, plus an append-only `event_log`. Events and state
updates are persisted in the same transaction where practical. On-disk artifact
envelopes and the durable Trust Envelope governance record complete the source
of truth. `pipeline_run_id` — a ULID — is the durable correlation key across all
of it, and is deliberately *not* a metric label so metric cardinality stays
bounded.

**Telemetry boundary.** All OpenTelemetry imports are confined to
`adapters/telemetry`, enforced two ways: an import-linter contract and an
AST-scanning test. The default adapter is `NoopTelemetry`; the OTLP-over-HTTP
exporter is opt-in. Persistence happens before emission, so telemetry is a
strict view over authoritative state.

**Resume and rehydration.** A paused approval gate or a failed stage leaves a
run that is rebuilt from SQLite on resume; every already-completed artifact is
hash-verified before reuse. A tampered artifact is refused, not silently
trusted. A resumed run is a fresh trace carrying a W3C `Link` back to the
pre-pause trace.

**Governance.** Architecture Baseline Section 24 defines the Trust Envelope
model and a fail-closed gate. The gate derives the envelope at ingest from the
operator's manifest, checks it early, and hard-blocks before TTS and before RSS
publishing unless the envelope is `APPROVED`. A static legal-hallucination
scanner runs inside the pytest suite.

**Operator experience.** Architecture Baseline Section 25 defines a
read-only-first operator law. Three surfaces implement it: a generated static
HTML report (`storytime report generate`), a read-only failure/review queue
(`storytime queue`), and one governed mutation command (`storytime rerun`) with
a `--dry-run` preview, a stable decision code, and an audit event.

**Enforcement.** Boundaries are mechanically defended: import-linter contracts,
the AST telemetry-boundary test, the closed manifest JSON Schema, `ARCH-LOCK`
annotations on load-bearing code, the metric-honesty dashboard test, and a
state-discipline regression test that asserts the project's own state documents
stay honest. Six Docker-free quality gates — `uv sync --frozen`, pytest, ruff,
mypy (strict), lint-imports, `storytime doctor` — gate every phase.

## 4. Business-value framing

For a non-engineering or mixed audience, the value translates cleanly:

- **Trustworthy automation.** The pipeline automates a multi-stage workflow
  while keeping a human in control at the decisions that matter. Automation
  earns trust by being inspectable, not by being opaque.
- **Lower operational risk.** Failure is a designed-for state with a clear
  operator response, not an incident that needs an expert to decode. Recovery is
  bounded and audited.
- **Reproducibility lowers cost.** Anyone can reproduce any scenario locally in
  minutes. That is the same property that, in a real product, shortens
  incident triage and onboarding.
- **Honest scoping.** The project says exactly what it does and does not do.
  That candour is what makes its claims worth relying on — the same trait a
  customer wants from a vendor.

## 5. Observability-value framing

> "Observability here is a design property with an automated guardrail, not a
> dashboard added at the end. The system emits real traces and metrics, the
> durable record is separate from the telemetry view, and the build fails if a
> dashboard ever charts a metric the code doesn't emit."

The Solutions Engineering point: StoryTime models *good observability hygiene* —
bounded cardinality, a clear source-of-truth boundary, instrumentation that
fails safe, and dashboards that cannot drift from reality. Those are exactly the
habits an SE coaches a customer toward. The project is a worked example of them.

## 6. OpenTelemetry-value framing

> "StoryTime is instrumented with vendor-neutral OpenTelemetry — standard spans
> and metrics emitted over OTLP to a local Collector. The Collector is the fan-
> out point: routing that telemetry to a backend is a Collector configuration
> change, not an application change."

This is the framing a Solutions Engineer needs and it is carefully bounded.
StoryTime demonstrates the **OpenTelemetry Collector pattern**: applications
emit once, to the Collector, and the Collector owns multi-backend fan-out. That
pattern is *why* a project instrumented this way could later route telemetry to
a platform such as Dynatrace, New Relic, or any OTLP-compatible backend without
touching application code. StoryTime does **not** implement any such vendor
integration, and saying it did would be overclaiming. What it shows is the
architecture that makes such an integration a configuration exercise.

## 7. Governance / compliance framing

> "StoryTime has a real, fail-closed governance gate — but it is scoped
> honestly. It records the human operator's licensing decision in a durable
> Trust Envelope and hard-blocks the pipeline before the expensive stages unless
> that decision is `APPROVED`. It performs no legal determination and is not a
> rights-clearance engine."

The framing worth making explicit in an interview: the interesting part is the
**discipline of not overclaiming**. The governance layer is a fail-closed
project control. Every governance display carries a standing "record of a human
decision, not legal advice" disclaimer, and a static scanner in the test suite
fails the build if legal-overclaiming vocabulary appears where it should not.
Governance is *source authorization* — is this source allowed? — not viewpoint
moderation. Knowing exactly where a control's authority ends, and enforcing that
boundary in code, is the governance story.

## 8. Failure-mode demonstration framing

> "The most useful thing I can show isn't the happy path — it's a failure. A
> run fails at a real pipeline stage; it appears in the read-only queue with a
> structured failure code and a next-step hint; `rerun --dry-run` proves the
> retry is eligible without changing anything; the governed `rerun` performs one
> bounded state reset and writes one audit event; the run resumes and completes;
> and the operator report shows the whole journey — failure, re-run request, and
> recovery — preserved in order on one append-only record."

For an SRE / Solutions Engineering audience this is the strongest sequence.
Phase 11C inventoried the highest-risk failure and regression paths and mapped
each to the tests and gates that protect it (`docs/regression-risk-register.md`,
`docs/failure-mode-test-matrix.md`). The demonstrable point is that failure is
*designed for*: it is structured state with a documented operator response, and
recovery is bounded, governed, and audited — never a silent retry loop.

## 9. Why this project is relevant to a Dynatrace-style SE role

A Solutions Engineer at an observability platform spends the day doing four
things: explaining observability architecture clearly, demonstrating it
credibly, helping customers instrument honestly, and being trusted to say what a
product does and does not do. StoryTime is built to exercise all four:

- **Explaining architecture.** The whole project is a worked, readable example
  of source-of-truth-vs-view, bounded cardinality, and the Collector fan-out
  pattern — the concepts an SE explains daily.
- **Demonstrating credibly.** It is local-first and reproducible, so a demo
  needs no provisioning and cannot be derailed by a network issue. Every
  scenario, including failure and recovery, can be run live.
- **Instrumenting honestly.** The metric-honesty build gate is a concrete
  artifact of the discipline an SE coaches: dashboards that cannot drift from
  what the system actually emits.
- **Being trusted on scope.** StoryTime states its boundaries plainly and does
  not claim a vendor integration it does not have. That is the same credibility
  a customer expects from an SE.

The honest version of the relevance claim: StoryTime does not prove production
observability operations at scale, and this document does not say it does. It
demonstrates that the person who built it can reason about observability
architecture, instrument a system the right way, explain it at any depth, and
hold a hard line on what is and is not true — which is the substance of
Solutions Engineering readiness.

## 10. What not to claim

To keep every conversation honest, do **not** say StoryTime:

- integrates with, or is instrumented for, any named commercial observability
  vendor — it emits standard OpenTelemetry to a local Collector only;
- has production alerting, paging, or an error-budget policy — it has none;
- is deployed, has users, or has operational scale — it is a local,
  single-operator project;
- performs a legal determination or clears rights — governance records a human
  decision and is not a legal authority.

Stating the boundaries is part of the credibility, not a weakness in it.
