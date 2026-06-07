# StoryTime — Portfolio Overview
<!-- CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md -->
> **Canonical demo path.** For the current, authoritative reviewer/demo
> walkthrough — the system modes and boundaries, the optional loopback
> local bridge, the one controlled retry (acceptance is not success), the
> manual snapshot reload (a read-model refresh, not a live sync), and the
> governed mock-first TTS proof (provider-backed audio remains deferred) —
> see [docs/demo-walkthrough.md](demo-walkthrough.md), the single source of
> truth and evidence map. This document is a secondary/historical narrative;
> where it differs, the canonical walkthrough wins.


A plain-English account of what StoryTime is and why it exists, written for
someone deciding — in a few minutes — whether this project is worth a closer
look. It is the entry point to the Phase 12 portfolio packaging layer.

This document does not add or change product behaviour. It explains the system
that Phases 0–11 already built and hardened. Where it makes a claim, that claim
is backed by something concrete in the repository — a test, a config file, or
another document — and the companion documents say where.

Companion documents: `docs/solutions-engineer-narrative.md` (how to explain
StoryTime in an interview), `docs/portfolio-demo-script.md` (a reviewer-facing
walkthrough), `docs/interview-talking-points.md` (concise, study-friendly
points), `docs/portfolio-narrative.md` (the Phase 10 narrative this layer
builds on), and `docs/known-limitations.md` (the honest boundaries).

---

## 1. What StoryTime is

StoryTime is a **local-first, observability-native content-to-audio pipeline**.
It turns approved CC0 / US-public-domain text into podcast-ready audio, an RSS
feed, and a traceable record of every run. It runs entirely on one machine,
from the command line, with no cloud account and no required network calls.

A run moves a source text through five canonical stages — **ingest →
synthesize → assemble → publish**, with operator **approval** gates woven in.
Every step is persisted to a SQLite state database and to versioned, hashed
artifact envelopes. SQLite plus those envelopes (and the durable Trust Envelope
governance record) are the source of truth; OpenTelemetry is an optional *view*
over that truth, never the truth itself.

That one-sentence description is accurate, but it undersells the point. The
podcast pipeline is the *vehicle*. The actual subject of the project is
**engineering and operational discipline** — observability done honestly,
boundaries enforced mechanically, governance that does not overclaim, and a
process that produces an auditable history of its own decisions.

## 2. Why it exists

Most "content pipeline" demos optimise for one happy path: input goes in,
output comes out, the slide says *done*. StoryTime was built on the opposite
premise — that the questions worth answering arrive *after* the happy path:

- When a run fails, can an operator tell **why**, and **what to do next**?
- When governance blocks a source, is that decision **visible, bounded, and
  honestly worded**, without leaking internals or overclaiming a legal outcome?
- When an operator wants to retry a failed run, can the system **prove the
  retry is safe** before mutating anything?
- Can a reviewer **reproduce** every one of those scenarios on their own
  machine, in minutes, with no account and no network?

StoryTime exists to answer those questions concretely, in a system small enough
to read end to end. It is a proving ground: a place to practise observability
thinking, failure-mode discipline, and operator-experience design where every
claim can be checked.

## 3. The problem it demonstrates

The problem StoryTime is really about is **operating a multi-stage workflow you
can trust**. A real distributed system has the same shape as this pipeline —
work moves through stages, each stage can fail, state has to survive a crash, a
human sometimes has to intervene, and someone afterwards needs to reconstruct
what happened. StoryTime takes that shape and makes every part of it
inspectable:

- stages that hand off through immutable, hash-verified artifacts rather than
  shared mutable memory;
- a single durable source of truth, with telemetry as a separate, optional view;
- failure surfaced as structured state, not as a stack trace an operator has to
  decode;
- one governed, audited way to mutate state, and nothing else.

It is a deliberately small system that practises the habits a large one needs.

## 4. Why it matters for observability, OpenTelemetry, and SE work

For an observability or Solutions Engineering audience, three properties are
the point:

**Observability is a design property, not a decoration.** StoryTime emits real
OpenTelemetry traces and metrics — one `pipeline.run` span per run with child
stage spans, and eight purposeful, low-cardinality metrics — and it holds them
to an enforced *metric honesty* rule: an automated test fails the build if a
dashboard charts a metric the code does not actually emit. The project has no
dashboard it cannot back with real data, and that absence is documented rather
than hidden.

**Telemetry is a view, not the source of truth.** Persistence to SQLite happens
*before* telemetry emission. With the default `noop` telemetry adapter no
telemetry is emitted at all and the pipeline behaves identically — observability
can fail without the pipeline failing. All OpenTelemetry imports are confined to
a single adapter module, enforced by an import-linter contract and an
AST-scanning test.

**It is vendor-neutral by construction.** StoryTime emits standard OpenTelemetry
to a local Collector. The Collector pattern is exactly what makes fan-out to a
commercial platform — Dynatrace, New Relic, or another OTLP-compatible backend —
a configuration change rather than a code change. StoryTime does *not* integrate
any commercial observability vendor today, and it does not claim to; what it
demonstrates is an architecture that *could* fan out without rework, which is
the more honest and more useful thing to show.

## 5. What makes it different from a normal content app

A normal content app would be judged on features, polish, and scale. StoryTime
is deliberately none of those things, and that is the differentiator:

- It treats **failure** as a first-class, designed-for state, with a dedicated
  read-only review queue and a documented operator response.
- It treats **governance** as a fail-closed gate that records a human decision,
  with explicit honesty rules about what it is and is not.
- It treats **auditability** as a product property — an append-only event log
  where a run that failed, was re-run, and then completed keeps its whole
  journey on one record.
- It treats its **own process** the same way: an append-only project history
  that records even an out-of-band execution (Phase 6S) honestly rather than
  quietly rewriting it.

The value is in what the system refuses to do as much as what it does.

## 6. How local-first design supports safe demoability

Local-first is a charter decision, not an accident:

- **One machine, one operator.** Every command runs against a local SQLite
  database (WAL mode) and an on-disk artifact tree. No server is required for
  the pipeline, no database service, no external API.
- **The network is optional.** The core pipeline and the entire test suite run
  offline. The only outbound-network path that exists at all — telemetry export
  from the OpenTelemetry Collector — is disabled by default and never required.
- **Reproducibility is cheap.** Because there is no shared state and no hosted
  dependency, a reviewer can extract the repository, run the demo, and see the
  exact behaviour the author sees. The Phase 10F `demo/` fixtures exist to make
  that reproducibility concrete, and Phase 11B verified the documented
  fresh-clone path against a genuine clean extraction.

For a demo, this means there is nothing to provision, no credentials to manage,
and no risk that a network hiccup derails the walkthrough — the trust surface
is just the local filesystem.

## 7. How governance and licensing constraints are represented

StoryTime has a real governance layer, defined as architecture law in
`docs/architecture-baseline.md` Section 24 and implemented in Phase 9B.

The core idea is the **Trust Envelope**: a durable, per-run record that
transcribes *the human operator's recorded licensing decision* for a source. A
fail-closed governance gate derives the Trust Envelope at ingest, checks it
early, and hard-blocks before TTS and before RSS publishing unless an
`APPROVED` envelope exists. The source manifest is a closed JSON Schema
(`additionalProperties: false`) constraining input to CC0 / US public domain.

Two honesty rules sit on top, and they matter as much as the mechanism:

- **StoryTime performs no legal determination.** The Trust Envelope records a
  human decision. The system is not a rights-clearance engine and does not
  certify copyright safety. Every governance display carries a standing "record
  of a human decision, not legal advice" disclaimer, and a static scanner runs
  inside the test suite to fail the build if legal-overclaiming vocabulary
  appears outside the documents that legitimately define it.
- **Governance is source authorization, not viewpoint moderation.** A blocked
  source is blocked on an authorization basis — *is this source allowed?* — not
  on the acceptability of its content. StoryTime is not a content-moderation
  system.

Representing constraints honestly — naming exactly what the control is and is
not — is itself part of the engineering story.

## 8. How the project demonstrates distributed workflow thinking

StoryTime is single-process and local, but it is built with the discipline a
distributed workflow demands:

- **Stages communicate through artifacts, not shared memory.** Each stage
  consumes and produces versioned, hashed artifact envelopes; it never calls
  another stage and never mutates shared state. This is the same contract a
  queue-decoupled distributed pipeline needs.
- **A durable correlation key.** `pipeline_run_id` (a ULID) correlates SQLite
  rows, artifacts, the event log, traces, and the operator's mental model — and
  it is deliberately *not* a metric label, keeping metric cardinality bounded.
- **Resume and rehydration are real.** A paused or failed run is rebuilt from
  SQLite; every reused artifact is hash-verified before the run continues, so a
  tampered artifact is refused rather than silently trusted.
- **Approval gates are persisted pipeline stages.** A paused run exits its
  process cleanly and resumes later as a new, linked trace — the durable-workflow
  pattern of a long-running process that survives a restart.

The architecture is intentionally shaped so that the local adapters (storage,
events) could be swapped for cloud-native equivalents without changing the
pipeline's contracts. That swap is *not* implemented — but the seams are real.

## 9. How the project demonstrates operator experience

Phase 10 extended observability from *machine* telemetry to *operator*
observability — three layers a single human can rely on:

- **See** — a generated, static, read-only HTML operator report. No JavaScript,
  no server, no external assets; it opens straight from the filesystem and is a
  faithful projection of the SQLite source of truth.
- **Triage** — a deterministic, read-only `storytime queue` command that answers
  one question: which runs need an operator, why, and what to look at next.
- **Act** — exactly one governed mutation surface, `storytime rerun`, which
  proves a re-run is safe before performing a single bounded state change and
  writing one audit event.

Every state change goes through an explicit CLI command; there is no "retry"
button anywhere. Keeping mutation in the CLI and out of the browser keeps the
report honestly read-only and the mutation surface small and auditable.

## 10. How the project demonstrates observability architecture

The observability story is structural, not bolted on:

- **Real OpenTelemetry**, confined to one adapter module, enforced by an
  import-linter contract and an AST test.
- **Eight purposeful, low-cardinality metrics**, six dashboards provisioned as
  code, and an SLI model (`docs/slo-sli.md`) built strictly from metrics that
  actually exist — explicit about what cannot yet be measured.
- **Metric honesty as a build gate** — a dashboard cannot reference a metric the
  system does not emit.
- **An optional local stack** — Collector, Prometheus, Loki, Jaeger, Grafana —
  that runs under Docker for those who want to *see* the telemetry, while the
  six quality gates and the whole test suite stay Docker-free.
- **An append-only event log** in SQLite that records every meaningful state
  transition, so a run's whole journey — including failure and recovery — is
  reconstructable without trusting a running service.

## 11. Current status

Phase 10 (operator experience) is closed. Phase 11 (release-candidate
hardening) is closed: its four subphases hardened the fresh-clone path,
verified operator reproducibility, inventoried and test-mapped the failure and
regression surfaces, and consolidated the release-candidate evidence. The six
Docker-free quality gates pass — 580 tests, ruff and mypy (strict) clean,
import-linter contracts kept, `storytime doctor` healthy, and the
legal-hallucination scanner reporting zero violations.

Phase 12 — Portfolio / SE Demo Packaging — is the current phase, and this
document is part of **Phase 12A**, its baseline. Phase 12A is documentation and
packaging only: it adds no product feature and changes no runtime behaviour.
For the always-current status see `docs/handoff-state.md`.

## 12. What StoryTime is not

Naming the non-goals is itself a discipline signal. StoryTime is **not** a
production SaaS dashboard or hosted product, not a multi-user system with
accounts or authentication, not cloud-deployed, not a fully automated content
platform, not a legal-advice or rights-clearance engine, and not a commercial
text-to-speech platform. Its TTS is mock-grade and audio quality is not
measured. The value is the engineering and operational discipline demonstrated
in a deliberately small, fully inspectable system — not operational scale.
`docs/known-limitations.md` states these boundaries in full and explains which
are deliberate architecture choices.
