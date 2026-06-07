# StoryTime — Portfolio Demo Narrative
<!-- CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md -->
> **Canonical demo path.** For the current, authoritative reviewer/demo
> walkthrough — the system modes and boundaries, the optional loopback
> local bridge, the one controlled retry (acceptance is not success), the
> manual snapshot reload (a read-model refresh, not a live sync), and the
> governed mock-first TTS proof (provider-backed audio remains deferred) —
> see [docs/demo-walkthrough.md](demo-walkthrough.md), the single source of
> truth and evidence map. This document is a secondary/historical narrative;
> where it differs, the canonical walkthrough wins.


A concise, public-presentation account of StoryTime, written so that a
reviewer can understand the project's value in **5–10 minutes without having
to run the full system first**. It is the narrative spine of the Phase 12C
public presentation kit.

This document adds no product behaviour. It explains and packages the system
that Phases 0–11 already built, hardened, and verified. Every claim here is
backed by something concrete in the repository — a test, a config file, a
source module, or another document — and the companion evidence document
(`docs/portfolio-evidence-index.md`) says where.

Companion Phase 12C documents: `docs/demo-talk-track.md` (a spoken
walkthrough at three lengths), `docs/interview-story-bank.md` (reusable
interview answer frames), and `docs/public-repository-readiness.md` (the
checklist for preparing the repository for public viewing). Earlier portfolio
documents this narrative builds on: `docs/portfolio-overview.md`,
`docs/solutions-engineer-narrative.md`, and `docs/portfolio-narrative.md`.

---

## 1. What StoryTime is

StoryTime is a **local-first, observability-native content-to-audio
pipeline**. It converts approved CC0 / US-public-domain text into
podcast-ready audio, an RSS feed, and a traceable record of every run. It runs
entirely on one machine, from the command line, with no cloud account and no
required network calls.

A run moves a source text through five canonical stages — **ingest →
synthesize → assemble → publish**, with operator **approval** gates woven in.
Every step is persisted to a SQLite state database (WAL mode) and to versioned,
hash-verified artifact envelopes. SQLite, those envelopes, and the durable
Trust Envelope governance record are the source of truth; OpenTelemetry is an
optional *view* over that truth, never the truth itself.

That description is accurate, but it understates the point. The podcast
pipeline is the **vehicle**. The **subject** is engineering and operational
discipline: observability done honestly, architectural boundaries enforced
mechanically, fail-closed governance that does not overclaim, an operator
experience designed around failure as much as success, and a development
process that produces an auditable history of its own decisions.

## 2. Why it exists

Most "content pipeline" demos optimise for one happy path: input goes in,
output comes out, the slide says *done*. StoryTime was built on the opposite
premise — that the questions worth answering arrive *after* the happy path:

- When a run fails, can an operator tell **why**, and **what to do next**,
  without decoding a stack trace?
- When governance blocks a source, is that decision **visible, bounded, and
  honestly worded**, without leaking internals and without overclaiming a
  legal outcome?
- When an operator wants to retry a failed run, can the system **prove the
  retry is safe** before mutating any state?
- Can a reviewer **reproduce** every one of those scenarios on their own
  machine, in minutes, with no account and no network?

StoryTime exists to answer those questions concretely, in a system small
enough to read end to end. It is a deliberate proving ground: a place to
practise observability thinking, failure-mode discipline, and
operator-experience design in a setting where every claim can be checked.

## 3. What problem it demonstrates

The real problem StoryTime is about is **operating a multi-stage workflow you
can trust**. A distributed system has the same shape as this pipeline — work
moves through stages, each stage can fail, state must survive a crash, a human
sometimes has to intervene, and someone afterwards has to reconstruct what
happened. StoryTime takes that shape and makes every part of it inspectable:

- stages hand off through immutable, hash-verified artifact envelopes rather
  than shared mutable memory;
- a single durable source of truth, with telemetry as a separate, optional
  view that can fail without the pipeline failing;
- failure is surfaced as structured state — an `error_kind` code and a
  triage queue entry — not as a stack trace the operator must interpret;
- there is exactly one governed, audited way to mutate run state, and nothing
  else.

It is a deliberately small system that practises the habits a large one needs.
The diagnostic question a reviewer should keep in mind is: *given a run that
went wrong, how quickly and how confidently can an operator establish what
happened and what to do?* StoryTime is built so the answer is "quickly, from
structured state, without guessing."

## 4. Why observability matters here

For an observability or Solutions Engineering audience, three properties are
the point — and each is enforced, not merely asserted.

**Observability is a design property, not a decoration.** StoryTime emits real
OpenTelemetry traces and metrics — one `pipeline.run` span per run with child
stage spans, and a closed set of eight purposeful, low-cardinality metrics. It
holds them to an enforced *metric honesty* rule: an automated test fails the
build if a dashboard charts a metric the code does not actually emit. The
project has no dashboard it cannot back with real data, and where a metric is
absent that absence is documented rather than hidden.

**Telemetry is a view, not the source of truth.** Persistence to SQLite
happens *before* telemetry emission. With the default `noop` telemetry adapter
no telemetry is emitted at all, and the pipeline behaves identically — so
observability can degrade or fail without the pipeline degrading or failing.
All OpenTelemetry imports are confined to a single adapter module, and that
confinement is enforced two ways: an import-linter contract and an
AST-scanning test.

**It is vendor-neutral by construction.** StoryTime emits standard
OpenTelemetry to a local Collector. The Collector pattern is exactly what
makes fan-out to a commercial platform — Dynatrace, New Relic, or any other
OTLP-compatible backend — a *configuration* change rather than a *code*
change. StoryTime does not integrate any commercial observability vendor
today, and it does not claim to. What it demonstrates is an architecture that
*could* fan out without rework — which is the more honest and the more useful
thing to show a reviewer.

The causal-diagnosis story is the one to make visible in a demo: a run fails,
the structured `error_kind` and the failure queue say *what kind* of failure
and *where*, the static report's failure summary says *what to do next*, and
the trace — when telemetry is enabled — shows the stage timeline. Cause,
location, and next action are all legible without guesswork.

## 5. What the operator sees

StoryTime's operator experience is three deliberate layers, built in that
order under a locked operator-experience law (Architecture Baseline §25):

1. **See** — `storytime report generate` writes a static, local, read-only
   HTML report of a run: its stage timeline, its governance decision, its
   failure summary, and a command reference for what to do next. It is a
   regenerable snapshot — no server, no websocket, no auto-refresh, no
   JavaScript, no external assets. If the report and the database ever
   disagree, the database wins; the report says so.
2. **Triage** — `storytime queue` is a deterministic, read-only failure /
   review queue: the runs needing operator attention (failed, blocked by
   governance, needs-review, or awaiting an approval decision), each with why
   it needs attention and which command or artifact to inspect next. It is a
   viewer — it has no `pop`, `claim`, or `ack`, and it mutates nothing.
3. **Act** — `storytime rerun` is the single, deliberately bounded mutation
   surface: an audited re-run of a failed run, gated on governance. It
   supports `--dry-run` so an operator can confirm a retry is safe *before*
   anything changes, the actual mutation is one bounded status reset, and
   every real mutation writes a `RunRerunRequested` audit event.

The operator sees a system that is honest about its own state: a run that
failed, was re-run, and then completed keeps its whole journey on one
append-only record.

## 6. What the reviewer should notice

A reviewer skimming StoryTime should notice the things that are *enforced*,
because enforcement is what separates a claim from a habit:

- **Boundaries are mechanical.** The "telemetry lives in one adapter" rule and
  the "events package imports nothing internal" rule are import-linter
  contracts; an AST-scanning test independently checks the telemetry
  confinement. A boundary that is only a convention drifts; these cannot.
- **Honesty is tested.** The metric-honesty test fails the build on a
  dashboard / code mismatch. A static legal-hallucination scanner fails the
  build if governance copy overclaims a legal outcome. The state-discipline
  guard fails the build if the project's own status documents drift.
- **Failure is designed for, not patched in.** There is a failure queue, a
  report failure summary, an operator failure-response playbook
  (`docs/operator-failure-response.md`), a regression risk register, and a
  failure-mode test matrix.
- **The process is auditable.** The project history is append-only and records
  even an out-of-band execution (Phase 6S) honestly rather than quietly
  rewriting it. Every phase was implemented, independently reviewed,
  critiqued, and only then locked by explicit user approval.
- **Scope is named.** The project states plainly what it is not — see
  Section 8 and `docs/known-limitations.md`.

The single most reviewer-useful artifact is `docs/portfolio-evidence-index.md`:
it maps each portfolio claim to the test, config, source file, or document
that backs it, so a skeptical reviewer can verify rather than trust.

## 7. How this maps to SE / Dynatrace-style credibility

For a Solutions Engineer role in the observability space — the kind of role a
Dynatrace, New Relic, or comparable vendor hires for — the relevant
credibility signals are not "I built a big app." They are:

- **Can you reason about telemetry honestly?** StoryTime shows OpenTelemetry
  used as a first-class design input — one run span, child stage spans,
  purposeful low-cardinality metrics, `pipeline_run_id` deliberately *not* a
  metric label so cardinality stays bounded — and an enforced rule that the
  dashboards never outrun the data.
- **Can you explain the value of a Collector-centric, vendor-neutral
  architecture?** StoryTime is built exactly so that fan-out to a commercial
  OTLP backend is a configuration change. That is the architecture an SE
  recommends to a customer, demonstrated rather than described.
- **Can you talk about reliability and failure without hand-waving?**
  StoryTime treats failure as structured state, has a documented operator
  response, and proves its safe-mutation and fail-closed invariants with
  tests. An SE has to make reliability concrete for a customer; this project
  is a worked example.
- **Can you explain a technical system to a non-technical stakeholder?** The
  portfolio layer — overview, narrative, talk track, public copy — exists to
  do exactly that, and the talk track scales from 5 to 20 minutes for
  different audiences.
- **Are you honest about limits?** An SE who overclaims loses a customer's
  trust. StoryTime's discipline about *not* claiming a vendor integration, a
  legal determination, or a production deployment is itself the credibility
  signal.

The honest framing for an interview is: *StoryTime is not a product I shipped
to users; it is a controlled environment where I practised the observability,
reliability, and governance reasoning an SE role depends on, and made every
piece of that reasoning checkable.*

## 8. What is intentionally out of scope

Naming the boundaries is part of the narrative — it demonstrates scoping
discipline and keeps every other claim trustworthy. StoryTime intentionally
does **not**:

- run as a hosted product — there are no users, no SLA, no uptime story, and
  no operational scale claim; it is local-first by charter decision;
- integrate any named commercial observability vendor — it emits standard
  OpenTelemetry and is *compatible with* OTLP fan-out, which is a different
  and more honest claim;
- perform a legal determination or rights-clearance — its governance gate
  records a *human* licensing decision and is careful never to word itself as
  a legal outcome;
- deploy to the cloud, or include an image registry, Kubernetes, or
  Terraform — the optional containerized blue/green path (Phase 7) is local,
  single-host, and demo-grade;
- offer a graphical user interface today. A future **Phase 13 — Operator GUI
  / Decoupled Frontend Vision** is preserved in the roadmap and in
  `docs/GUI_vision.md` as planned, **not started** work; the public/demo
  narrative would later benefit from that GUI as a tactile visibility layer,
  but Phase 12C neither begins nor depends on it.

For the complete, considered list of non-goals see `docs/known-limitations.md`
and the "Deferred / not authorized" section of `docs/roadmap.md`.

---

## How to use this document

- **As a reviewer:** read Sections 1–3 and 6 for a five-minute understanding;
  read Sections 4–5 and 7 for the ten-minute observability/SE view; verify any
  claim through `docs/portfolio-evidence-index.md`.
- **As the project author preparing a demo:** pair this narrative with
  `docs/demo-talk-track.md` for the spoken version and
  `docs/demo-reviewer-checklist.md` for the live walkthrough.
- **As an interviewer-facing study aid:** pair it with
  `docs/interview-story-bank.md`, which turns this narrative into reusable
  answer frames.

This document is part of Phase 12C — Portfolio Demo Narrative / Public
Presentation Kit. Phase 12C is a documentation-only portfolio packaging phase;
it changes no product, runtime, API, CLI, or telemetry behaviour.
