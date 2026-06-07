# StoryTime — Portfolio Narrative
<!-- CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md -->
> **Canonical demo path.** For the current, authoritative reviewer/demo
> walkthrough — the system modes and boundaries, the optional loopback
> local bridge, the one controlled retry (acceptance is not success), the
> manual snapshot reload (a read-model refresh, not a live sync), and the
> governed mock-first TTS proof (provider-backed audio remains deferred) —
> see [docs/demo-walkthrough.md](demo-walkthrough.md), the single source of
> truth and evidence map. This document is a secondary/historical narrative;
> where it differs, the canonical walkthrough wins.


A clear, honest account of what StoryTime is, why it was built the way it was,
and what the Phase 10 operator-experience work demonstrates. It is written for
a technical reviewer, a hiring manager, or a Solutions Engineer interviewer who
has a few minutes and wants the real story — not marketing copy.

Companion documents: `docs/demo-script.md` (a step-by-step demo a human can
follow), `docs/operator-experience-walkthrough.md` (how the operator surfaces
fit together), `docs/command-reference.md` (the operator CLI),
`docs/known-limitations.md` (honest boundaries), and
`docs/observability-governance-talking-points.md` (the interview-language
version of the technical story). For the existing engineering summary see
`docs/portfolio-notes.md`.

---

## 1. What StoryTime is

StoryTime is a **local-first, observability-native content-to-audio pipeline**.
It turns approved CC0 / US-public-domain text into podcast-ready audio, an RSS
feed, and a traceable record of every run. It runs entirely on one machine,
from the command line, with no cloud account and no required network calls.

A run moves a source text through five canonical stages — **ingest →
synthesize → assemble → publish**, with operator **approval** gates woven in —
and persists every step to a SQLite state database and to versioned, hashed
artifact envelopes. SQLite plus those on-disk envelopes (and the durable Trust
Envelope governance record) are the source of truth; OpenTelemetry is an
optional *view* over that truth, never the truth itself.

The Phase 10 work — the subject of this narrative — does not add new pipeline
behaviour. It adds the **operator-experience layer**: the ways a single human
operator can *see* what the pipeline did, *triage* what needs attention, and
*act* on it safely. Phase 10 makes StoryTime legible, demonstrable, and
handoff-ready without turning it into a hosted product.

## 2. Why it matters

Most "content pipeline" demos optimise for a single happy path: input goes in,
output comes out, the slide says "done". StoryTime is built around the
assumption that the interesting questions come *after* the happy path:

- When a run fails, can an operator tell **why**, and **what to do next**?
- When governance blocks a source, is that decision **visible, bounded, and
  honestly worded** — without leaking raw internals or overclaiming a legal
  outcome?
- When an operator wants to retry a failed run, can the system **prove the
  retry is safe** before mutating anything?
- Can a reviewer **reproduce** every one of those scenarios on their own
  machine, in minutes, with no cloud account?

Phase 10 answers each of those questions with a concrete, inspectable surface.
That is the point of the project: it is a proving ground for **observability
thinking and operational discipline**, expressed in a deliberately small
system where every claim can be pointed at a test, a config file, or a doc.

## 3. Local-first architecture

Local-first is a charter decision, not a limitation reached by accident:

- **One machine, one operator.** Every command runs against a local SQLite
  database (WAL mode) and an on-disk artifact tree. There is no server process
  required for the pipeline, no database service, and no external API.
- **The network is optional.** The core pipeline and the entire test suite run
  offline. The only outbound-network path that exists at all — telemetry
  export from the OpenTelemetry Collector — is disabled by default and is
  never required.
- **Reproducibility is cheap.** Because there is no shared state and no hosted
  dependency, a reviewer can clone the repository, run the demo, and see the
  same behaviour the author sees. Phase 10F's `demo/` fixtures exist precisely
  to make that reproducibility concrete.

Local-first also makes the trust story simple: nothing leaves the machine, so
there is no data-handling surface to reason about beyond the local filesystem.

## 4. Manual, operator-controlled workflow

StoryTime is deliberately **operator-driven**. It is not an autonomous content
platform. A human:

- chooses the source manifest and runs the pipeline,
- decides at each approval gate whether a run proceeds,
- inspects failures and governance decisions,
- and explicitly requests a re-run when one is warranted.

There is no scheduler, no background worker, no automatic retry loop, and no
daemon. Every state change is the result of an operator command. This is what
makes the system honest about what it is: a tool an operator *uses*, not a
service that runs itself. Phase 10's operator surfaces (report, queue, rerun)
all preserve that property — even `storytime rerun`, the one mutation command,
hands control straight back to the operator rather than executing the pipeline
itself.

## 5. Trust Envelope and the governance posture

StoryTime has a real governance layer, defined as architecture law in
`docs/architecture-baseline.md` Section 24 (Phase 9A) and implemented in
Phase 9B.

The core idea is the **Trust Envelope**: a durable, per-run record
(`governance/trust-envelope.json`, with a rebuildable SQLite projection) that
transcribes *the human operator's recorded licensing decision* for a source.
A fail-closed governance gate derives the Trust Envelope at ingest, checks it
early, and hard-blocks before TTS and before RSS publishing unless an
`APPROVED` envelope exists.

Two honesty rules sit on top of this:

- **StoryTime performs no legal determination.** The Trust Envelope records a
  human decision. The system is not a rights-clearance engine and does not
  certify copyright safety. Every governance display carries a standing "record
  of a human decision, not legal advice" disclaimer.
- **Governance is source authorization, not viewpoint moderation.** A blocked
  source is blocked on an *authorization* basis (is this source allowed?), not
  a content-acceptability basis. StoryTime is not a content-moderation system.

Phase 10 consumes this posture without weakening it. The operator report and
queue display the stable `APPROVED` / `REJECTED` / `BLOCKED` / `NEEDS_REVIEW`
decision enum and a bounded, report-safe wording — never the raw
`blocked_reason` text. The `storytime rerun` command refuses to re-run any run
whose Trust Envelope is not `APPROVED`: a re-run can never bypass governance.

## 6. The static HTML operator report

Phase 10B introduced, and Phase 10E refined, a **generated, static, local,
read-only HTML operator report**. `storytime report generate` writes a small
report directory — `index.html`, `runs.html`, one `run-<run_id>.html` detail
page per run, and a local `style.css` — from the existing SQLite state and
on-disk artifacts.

What makes it a good portfolio artifact is what it deliberately is *not*:

- It is **static HTML**. No JavaScript, no frontend framework, no build
  pipeline, no external assets, and no CDN. It opens directly in a browser with
  no web server and no network connection.
- It is **read-only**. It contains no form, no button, and no control that
  changes state. It is a faithful projection of the source of truth, not a
  second source of truth.
- It is **field-bounded**. An explicit allowlist/blacklist keeps raw story
  text, transcripts, secrets, long free-text notes, and raw telemetry out of
  the report. `review_context_summary` is capped at 500 characters, and that
  cap is enforced by a test.

The report is the project's answer to "show me what every run did" — an
inspectable, shareable, offline evidence surface.

## 7. Failure queue visibility

Phase 10C added the read-only `storytime queue` command. Where the report is a
browsable overview of *every* run, the queue is a fast command-line answer to
**"which runs need me, why, and what should I look at next?"**

A run appears in the queue when it matches an attention reason — failed,
blocked by governance, marked needs-review, or awaiting an operator approval
decision. For each run the queue shows why it needs attention and which
existing command, report, or artifact to inspect next.

The queue is conceptually a dead-letter / review queue, but it is honestly
*not* a broker-backed one: there is no message broker, no background worker, no
new queue storage, no new run state, and no `pop` / `claim` / `ack` behaviour.
It is a deterministic, bounded semantic query over the existing SQLite
source-of-truth state. It changes nothing.

## 8. The governed rerun command

Phase 10D added `storytime rerun` — StoryTime's **first and only operator
mutation surface**. It re-runs a failed pipeline run, but only when it can
*prove* doing so is safe.

A re-run proceeds only when the run exists, is in the `failed` state, failed
because of a genuine pipeline-stage failure (not an operator approval-gate
rejection), and carries an `APPROVED` Trust Envelope. When eligible, it
performs exactly **one** bounded mutation — resetting the run's status to the
resumable `running` state — and writes one `RunRerunRequested` audit event with
bounded metadata only. The operator then runs `storytime run --resume <run-id>`
explicitly to re-execute.

Everything about `rerun` is designed to keep the mutation small and honest:
`--dry-run` previews the eligibility decision and changes nothing; an
ineligible run is rejected with a stable decision code and a non-zero exit
code; the command runs no pipeline work itself and starts no retry loop. It is
the deliberate, governed counterpart to the read-only queue.

## 9. Demo seed data and golden-path fixtures

Phase 10F added the `demo/` directory: four original CC0 demo seed texts with
schema-valid manifests, a demo-only blocked-source deny-list, and six
golden-path fixture definitions (`demo/fixtures/`) covering the successful
golden path, a retryable technical failure, a governance-blocked source, a
needs-review / approval-gate run, a rerun-requested run, and a
completed-after-rerun run.

The fixtures are **inputs and expected-state descriptions**, not generated
runtime artifacts. They do not fake a success path — every scenario drives the
real existing pipeline, report, queue, governance gate, and `rerun` command.
The seed texts are original content written for the project and dedicated to
the public domain under CC0-1.0, so the demo never depends on external or
ambiguously-licensed material. The operator runbook that walks through them is
`docs/demo.md`.

This is what turns "trust me, it works" into "run these six scenarios
yourself".

## 10. Observability-native thinking

StoryTime is built so that *being observable* is a first-class property, held
to an honesty standard:

- **Real OpenTelemetry**, not log scraping — one `pipeline.run` span per run
  with child stage spans, and eight purposeful, low-cardinality metrics.
- **Metric honesty as an enforced rule.** A test fails the build if a
  dashboard charts a metric the code does not actually emit. The project has
  no dashboards it cannot back with real data, and that absence is documented,
  not hidden.
- **Telemetry is a view, not the truth.** Persistence to SQLite happens
  *before* telemetry emission; with the default `noop` adapter no telemetry is
  emitted and the pipeline behaves identically. Observability can fail without
  the pipeline failing.

Phase 10 extends this thinking from *machine* observability (traces, metrics)
to *operator* observability: the report and the queue are the human-facing
projection of the same source of truth, and the `rerun` audit event extends
the same append-only event log. The architecture is **compatible with
observability-native, OpenTelemetry-centred operations** — it is not, and does
not claim to be, instrumented for any specific commercial observability
vendor.

## 11. Auditability

Every meaningful state transition is recorded in an append-only `event_log` in
SQLite. A completed run carries its whole journey in order — creation,
ingestion, governance evaluation, synthesis, assembly, RSS publication,
completion. A run that failed, was re-run, and then completed preserves *all*
of that: the `RunFailed` event, the `RunRerunRequested` event, and the
recovered-completion events all sit on the record together. Nothing is
rewritten or erased.

The same discipline applies to the project's own history. The State
Preservation Bundle (see Section 13) is append-only for locked decisions and
round records; stale status lines are corrected and labelled, never deleted.
Auditability is a property of both the product and the process.

## 12. Privacy and redaction discipline

Because StoryTime is local-first, the privacy surface is small by
construction — nothing leaves the machine. On top of that, the operator
surfaces apply explicit redaction discipline:

- The operator report and queue surface **structured fields only** — the
  `error_kind` code, never the free-text `error_message`; the governance
  decision enum, never the raw `blocked_reason`.
- The report's field allowlist keeps raw story text, transcripts, secrets, and
  long free-text notes out of generated output entirely.
- The `rerun` command's human-readable and JSON output are restricted to a
  fixed allowlist of bounded fields, and the audit payload carries metadata
  only — no raw story text, no raw transcript, no raw exception text.
- A static legal-hallucination scanner runs as part of the test suite and
  fails the build if forbidden legal-overclaiming vocabulary appears anywhere
  outside the governance documents that legitimately define it.

Redaction here is not an afterthought; it is enforced by tests.

## 13. How the project is built — the RoundTable process

StoryTime is built by a multi-model "RoundTable" workflow under an explicit
**Phase Closure Protocol**. Implementation output is never, by itself, a locked
phase. Each phase is implemented, then independently reviewed, critiqued,
cleaned up if needed, and only then locked by explicit user approval.

Because the RoundTable workflow itself can lose state between sessions, the
repository carries a **State Preservation Bundle** — `LLM_DIRECTOR.md` plus the
`docs/` state files — that is the portable project memory. A dedicated State
Preservation Synchronization Gate ensures that bundle is internally consistent
and cold-session safe before any artifact is considered review-ready. This
process discipline is itself part of the portfolio story: it shows phased
delivery, independent review, and an honest, append-only history.

## 14. What StoryTime is not

Naming the non-goals is itself a discipline signal. StoryTime is **not**:

- a production SaaS dashboard or hosted product,
- a multi-user system with accounts, roles, or authentication,
- a cloud-deployed service,
- a fully automated content platform,
- a legal-advice or rights-clearance engine,
- a commercial text-to-speech platform.

The value is in the **engineering and operational discipline** demonstrated in
a deliberately small, fully inspectable system — not in operational scale.
`docs/known-limitations.md` states these boundaries in full and explains which
of them are deliberate architecture choices.

## 15. The one-paragraph version

> StoryTime is a local-first, observability-native content-to-audio pipeline
> with a disciplined operator-experience layer: a static, read-only HTML
> operator report; a deterministic failure/review queue; a single governed,
> audited mutation command (`storytime rerun`); a fail-closed Trust Envelope
> governance gate; and reproducible demo fixtures. It runs on one machine with
> no cloud account, keeps SQLite and on-disk artifacts as the source of truth,
> treats OpenTelemetry as an optional view, and is built under a multi-model
> review process with an append-only project history. Every claim above is
> backed by a test, a config file, or a document in this repository.
