# StoryTime — Demo Talk Track
<!-- CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md -->
> **Canonical demo path.** For the current, authoritative reviewer/demo
> walkthrough — the system modes and boundaries, the optional loopback
> local bridge, the one controlled retry (acceptance is not success), the
> manual snapshot reload (a read-model refresh, not a live sync), and the
> governed mock-first TTS proof (provider-backed audio remains deferred) —
> see [docs/demo-walkthrough.md](demo-walkthrough.md), the single source of
> truth and evidence map. This document is a secondary/historical narrative;
> where it differs, the canonical walkthrough wins.


A spoken walkthrough script for demonstrating StoryTime, written to be
**said out loud**. It gives the same demo at three lengths — 5, 10, and 20
minutes — plus interviewer Q&A pivots and a fallback for when the demo cannot
be run live.

This document adds no product behaviour. It is a presentation aid for the
system Phases 0–11 built and hardened. For the exact fixture commands and
expected state it defers to `docs/demo.md` (the authoritative operator
runbook) and `docs/demo-reviewer-checklist.md` (the reviewer pre-flight and
what-to-look-for index). The narrative spine behind this script is
`docs/portfolio-demo-narrative.md`.

**How to use it.** Pick the length that fits the slot. Each version is written
as connected speech with `[stage direction]` cues in brackets — the cues are
for you, not to be read aloud. The talk track emphasises, in order: topology,
telemetry, failure diagnosis, governance, local-first design, and
reproducibility. Practise once against `docs/demo.md` so the commands and the
words line up.

---

## 5-minute version — the elevator demo

*Audience: a recruiter or hiring manager who needs the shape of the project
fast. Goal: they leave able to repeat what StoryTime is and why it is
credible.*

> "StoryTime is a local-first, observability-native content-to-audio pipeline.
> It turns approved public-domain text into podcast audio, an RSS feed, and a
> traceable record of every run — and it runs entirely on one machine, from
> the command line, with no cloud account.
>
> The podcast pipeline is the vehicle. The real subject is engineering
> discipline. Let me show you the three things that make that concrete.
>
> [Topology] First, the shape. A run moves through five stages — ingest,
> synthesize, assemble, publish — with operator approval gates woven in. The
> stages never call each other; they hand off through versioned,
> hash-verified artifact envelopes. SQLite and those on-disk artifacts are the
> single source of truth.
>
> [Telemetry] Second, observability. StoryTime emits real OpenTelemetry —
> one span per run, child spans per stage, a small set of purposeful metrics.
> But telemetry is a *view*, not the truth: persistence to SQLite happens
> before any telemetry is emitted, and with the default no-op adapter the
> pipeline behaves identically with no telemetry at all. There's even a test
> that fails the build if a dashboard charts a metric the code doesn't emit —
> the dashboards can't outrun the data.
>
> [Failure and governance] Third, the part most demos skip: what happens when
> things go wrong. A failed run shows up in a deterministic triage queue with
> a structured reason and a next action. Governance is a fail-closed gate that
> records a *human* licensing decision and blocks the expensive stages unless
> the source is approved — and it's careful never to claim it made a *legal*
> decision.
>
> [Close] It's local-first, reproducible by anyone in minutes, and it was
> built phase by phase under an explicit review-and-lock process with an
> append-only history. What it deliberately is *not* is a production service —
> no users, no SLA, no cloud — and naming that boundary is part of the story."

*If you have a terminal: run `uv run storytime doctor` and one golden-path run
(`docs/demo.md` Scenario 1) while you speak the topology paragraph — a healthy
doctor line and a `COMPLETED` status are enough visual proof for five minutes.*

---

## 10-minute version — the observability/SE demo

*Audience: a Solutions Engineer interviewer or an observability-minded
technical reviewer. Goal: they see causal diagnosis and operator confidence
made visible.*

**[0:00 — Frame it]**

> "StoryTime is a local-first, observability-native content-to-audio pipeline.
> I'll demo it as what it really is: a controlled environment for practising
> observability, reliability, and governance reasoning where every claim is
> checkable. Three acts — the happy path, a failure, and recovery."

**[1:00 — Act 1: topology and the happy path]**

> "[Run `storytime doctor`, then the Scenario 1 golden-path run.] A run moves
> through ingest, synthesize, assemble, publish. The stages communicate only
> through versioned, hash-verified artifact envelopes — there's no shared
> mutable context object. SQLite in WAL mode plus those envelopes are the
> source of truth, and `pipeline_run_id`, a ULID, is the correlation key
> across all of it.
>
> Notice the run completed and it does *not* appear in the failure queue.
> That's the baseline."

**[3:30 — Act 2: a failure, and diagnosing it]**

> "[Run Scenario 2 — the retryable technical failure.] Here's a run that
> failed at a real stage. Watch how I diagnose it. I don't read a stack
> trace — I run `storytime queue`. The queue is a deterministic, read-only
> view of every run needing attention, and for this run it tells me the
> structured failure kind and which command to inspect next.
>
> Then `storytime report generate` writes a static HTML report — stage
> timeline, failure summary, what-to-do-next. No server, no JavaScript, no
> external assets; it's a regenerable snapshot. Cause, location, next action —
> all legible without guessing. That is the causal-diagnosis story: structured
> state, not a stack trace."

**[6:00 — telemetry as the view]**

> "When telemetry is enabled, the same run is one `pipeline.run` span with
> child stage spans — the trace shows the timeline visually. But the key point
> is the *boundary*: all OpenTelemetry imports are confined to a single
> adapter module, enforced by an import-linter contract and an AST-scanning
> test. With the no-op adapter, telemetry can be entirely absent and the
> pipeline is unchanged. Observability can fail without the product failing."

**[7:30 — Act 3: governance and safe recovery]**

> "[Show Scenario 3 — governance-blocked — and Scenario 5/6 — rerun.]
> Governance is a fail-closed gate: it hard-blocks before the expensive stages
> unless an APPROVED Trust Envelope exists, and it records a *human* decision —
> it never claims a legal determination. A static scanner fails the build if
> the governance copy ever overclaims.
>
> To recover a failed run I use `storytime rerun` — the *one* bounded mutation
> command. I can run it with `--dry-run` first to confirm the retry is safe
> before anything changes. The actual mutation is a single status reset, and
> every real mutation writes an audit event. The run that failed, was re-run,
> and then completed keeps its whole journey on one append-only record."

**[9:00 — Close]**

> "Everything you saw runs on one machine, offline, reproducible in minutes —
> the `demo/` fixtures exist so a reviewer can reproduce exactly this. And it's
> vendor-neutral by construction: it emits standard OpenTelemetry to a local
> Collector, so fan-out to a commercial OTLP backend would be a configuration
> change, not a rewrite. That's the architecture an SE recommends to a
> customer — here it's demonstrated, not just described."

---

## 20-minute version — the deep technical walkthrough

*Audience: a technical interviewer who wants architecture, tradeoffs, and
process. Goal: they see depth, judgement, and honesty.*

**[0:00 — Framing, 2 min]**

Open with the 10-minute frame, then add the process point: "StoryTime was
built by a multi-model workflow under an explicit Phase Closure Protocol —
every phase implemented, independently reviewed, critiqued, and only then
locked by explicit approval. The project history is append-only. That process
is itself part of what I'm demonstrating."

**[2:00 — Architecture and contracts, 4 min]**

Walk the contract model: a single `PipelineRunner` drives five stages; a stage
takes a serializable `StageInput` DTO plus a minimal frozen `RunnerContext`
and returns a `StageResult` bundling a `StateUpdate`; there is no mutable
god-object context; a stage never calls another stage. Make the tradeoff
explicit: "This is the contract a queue-decoupled distributed pipeline needs,
practised in-process. The cost is more ceremony than a script; the benefit is
that every hand-off is inspectable and the architecture would survive being
pulled apart."

**[6:00 — Source of truth and persistence, 3 min]**

SQLite (WAL mode): run, stage, artifact, and approval tables plus an
append-only `event_log`; events and state updates persisted in the same
transaction where practical; on-disk hash-verified artifact envelopes; the
durable Trust Envelope governance record. Stress ordering: "Persistence
happens before telemetry emission. That ordering is the whole reason telemetry
can be called a view."

**[9:00 — Telemetry boundary and metric honesty, 3 min]**

One `pipeline.run` span, child stage spans, a real W3C trace `Link` from a
resumed run to its pre-pause trace, eight closed low-cardinality metrics.
`pipeline_run_id` is deliberately not a metric label — name the cardinality
tradeoff. Then the enforcement: import-linter contract, AST-scanning test, and
the metric-honesty test that fails the build on a dashboard/code mismatch.
"The dashboards are provisioned as code and cannot chart what the code does
not emit."

**[12:00 — Failure modes and the operator experience, 4 min]**

Run the failure, queue, report, and rerun scenarios from `docs/demo.md`. Tie
each to its evidence: the regression risk register, the failure-mode test
matrix, the operator failure-response playbook. Explain the three operator
layers — see, triage, act — and why they were built in that order under the
locked §25 operator-experience law. Make the safe-mutation point: `--dry-run`,
one bounded status reset, an audit event per mutation, governance never
bypassed.

**[16:00 — Governance honesty, 2 min]**

The fail-closed gate, the Trust Envelope schema, the source-authorization-not-
viewpoint framing, and the static legal-hallucination scanner. "The
discipline here is *not* overclaiming. Governance records a human decision; it
is not a rights-clearance engine, and the wording is tested to stay honest."

**[18:00 — Tradeoffs, limits, and what's next, 2 min]**

Be direct about scope: local-first, single operator, no cloud, no vendor
integration, no GUI yet. Mention the preserved, not-started Phase 13 Operator
GUI vision as considered future work. Close on reproducibility: "Every
scenario you saw is in `demo/`; extract the repo and you get the exact
behaviour I get. The honest summary is that this is a proving ground, not a
shipped product — and being precise about that is the point."

---

## Interviewer Q&A pivots

Short, honest pivots for questions a demo invites. Each lands on something
concrete.

- **"Why a podcast pipeline?"** → "It's a vehicle. I needed a multi-stage
  workflow with real failure modes, a governance question, and an operator —
  small enough to read end to end. The subject is the discipline, not
  podcasts."
- **"Is this in production?"** → "No — and that's deliberate. No users, no
  SLA, no cloud. It's a controlled environment where every claim is checkable.
  `docs/known-limitations.md` states every boundary."
- **"Do you integrate Dynatrace / New Relic?"** → "No, and I don't claim to.
  It emits standard OpenTelemetry to a local Collector. The honest, useful
  claim is that the architecture makes vendor fan-out a configuration change,
  not a rewrite — I can show you the Collector config."
- **"How would I know your observability claims are true?"** → "There's a test
  that fails the build if a dashboard charts a metric the code doesn't emit,
  and the telemetry boundary is enforced by a linter and an AST test.
  `docs/portfolio-evidence-index.md` maps every claim to its evidence."
- **"What was the hardest tradeoff?"** → "Keeping telemetry strictly a view.
  It would have been easier to let observability and persistence interleave.
  Persisting before emitting, and confining all OTel to one adapter, cost
  discipline but bought the property that observability can fail without the
  product failing."
- **"What would you do next?"** → "A decoupled operator GUI — Phase 13 in the
  roadmap. The CLI and the static report are honest but not tactile; a
  read-only console over a stable contract would make the system legible at a
  glance. It's scoped in `docs/GUI_vision.md` and intentionally not started."
- **"How do you explain this to a non-technical stakeholder?"** → "I'd use the
  portfolio overview's framing: it's a workflow you can trust — you can always
  tell what happened, why, and what to do next. Then I'd show the report,
  because a person can read it without knowing the code."

---

## What to say if the demo cannot be run live

If a terminal is unavailable, the network is restricted, or time is short, the
demo still works as a *narrated* walkthrough — StoryTime is designed so its
evidence is readable without running it.

> "I can't run it live here, so let me walk you through it using the artifacts
> the project already contains — and everything I describe is reproducible
> later from the repository in minutes.
>
> Start with `docs/demo.md`: it defines six scenarios — a clean golden path, a
> retryable failure, a governance block, a needs-review gate, a rerun request,
> and a completed-after-rerun recovery. Each one drives the real pipeline; none
> of them fakes success.
>
> For the happy path, picture a run moving through ingest, synthesize,
> assemble, publish, persisted to SQLite at every step. For the failure path,
> the run lands in the `storytime queue` output with a structured reason, and
> `storytime report generate` produces a static HTML report — I can describe
> its stage timeline and failure summary, and the report is a file, not a
> service. For governance, a fail-closed gate records a human decision and
> blocks the expensive stages unless the source is approved.
>
> If you want to verify any of this rather than take my word for it,
> `docs/portfolio-evidence-index.md` maps every claim to the test or file that
> backs it, and `docs/demo-reviewer-checklist.md` is the pre-flight for
> running it yourself."

Fallback talking points, in priority order, if you have only a minute:

1. **Topology** — five stages, artifact-envelope hand-offs, SQLite as the
   single source of truth.
2. **Telemetry as a view** — persistence before emission; the no-op adapter;
   the metric-honesty test.
3. **Failure diagnosis** — structured `error_kind`, the deterministic queue,
   the static report's next-action guidance.
4. **Governance** — fail-closed, human decision, never a legal claim, copy
   tested by a scanner.
5. **Local-first reproducibility** — one machine, offline, the `demo/`
   fixtures, the Phase 11B fresh-clone verification.

Never claim a validation, a run, or a result that did not actually happen in
front of the audience — the honesty discipline is part of what is being
demonstrated.

---

This document is part of Phase 12C — Portfolio Demo Narrative / Public
Presentation Kit. Phase 12C is a documentation-only portfolio packaging phase;
it changes no product, runtime, API, CLI, or telemetry behaviour.
