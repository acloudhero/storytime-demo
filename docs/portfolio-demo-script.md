# StoryTime — Portfolio Demo Script
<!-- CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md -->
> **Canonical demo path.** For the current, authoritative reviewer/demo
> walkthrough — the system modes and boundaries, the optional loopback
> local bridge, the one controlled retry (acceptance is not success), the
> manual snapshot reload (a read-model refresh, not a live sync), and the
> governed mock-first TTS proof (provider-backed audio remains deferred) —
> see [docs/demo-walkthrough.md](demo-walkthrough.md), the single source of
> truth and evidence map. This document is a secondary/historical narrative;
> where it differs, the canonical walkthrough wins.


A practical walkthrough for **presenting StoryTime to a portfolio reviewer** —
a hiring manager, a Solutions Engineer interviewer, a technical recruiter, or an
engineering manager. It sequences the project into a narrated ~10–15 minute
demo and gives the talking point for each step.

This script is the *portfolio-review* companion to two existing documents:
`docs/demo.md` is the authoritative operator runbook (the exact `demo/` fixture
commands and expected state), and `docs/demo-script.md` is the Phase 10G
presentation script. **When any command detail differs, `docs/demo.md` is
authoritative.** This document does not invent commands and does not require
new screenshots, generated audio, or any binary asset — every command below is
a real, existing StoryTime command (see `docs/command-reference.md`).

This document is part of Phase 12A and adds no product behaviour. Companion
documents: `docs/portfolio-overview.md`, `docs/solutions-engineer-narrative.md`,
`docs/interview-talking-points.md`.

---

## How to use this script

Two modes, and it is fine to say which one you are in:

- **Live mode** — run the commands as you talk. Most credible; needs a synced
  environment and, for the scenarios that complete a run, `ffmpeg` present.
- **Narrated mode** — walk the reviewer through the fixture definitions in
  `demo/fixtures/` and the operator report instead of executing live. Faster,
  fully deterministic, and still honest because the fixtures record the expected
  state. Good when time is tight or no environment is available.

A run id is generated when a run starts; later commands take it as an argument.
Capture it from `storytime status` or `storytime queue` output rather than
guessing.

---

## Step 0 — Opening explanation (about 60 seconds)

Set the frame before touching a terminal.

> "StoryTime is a local-first, observability-native content-to-audio pipeline.
> It turns approved public-domain text into podcast audio and an RSS feed. But
> the pipeline is the vehicle — what I actually want to show you is engineering
> discipline: a single source of truth, observability done honestly, a
> fail-closed governance gate, and an operator experience designed around
> failure, not just the happy path. Everything you'll see runs on this one
> machine, with no cloud account and no network."

This tells the reviewer what to watch for, so the rest of the demo lands as
evidence rather than as a feature tour.

## Step 1 — What to show first: the shape of the system

Before any run, show the repository and the environment check.

```bash
uv run storytime doctor
```

> "`doctor` is a read-only environment check — Python version, SQLite with WAL
> journaling, optional OpenTelemetry, optional `ffmpeg`. Notice it's read-only:
> a recurring theme here is that inspection commands never change state."

Point at the repository layout — `src/storytime/` with one package per concern,
`docs/` as living project memory, `demo/` for reproducible fixtures, `tests/`
for the boundary and behaviour tests.

> "The structure is the first signal: small, bounded packages, and every
> architectural boundary has a test or a linter contract behind it."

## Step 2 — Explain the local-first architecture

> "Local-first is a charter decision, not a limitation. Every command works
> against a local SQLite database and an on-disk artifact tree. There's no
> server for the pipeline, no database service, no external API. The core
> pipeline and the entire test suite run offline. The only outbound-network path
> that exists at all is telemetry export from the Collector — and that's
> disabled by default.
>
> Two payoffs. First, the trust surface is just the local filesystem — nothing
> leaves the machine. Second, this demo is reproducible: you could extract the
> repo and see exactly what I'm seeing, in minutes, with nothing to provision."

## Step 3 — Explain a pipeline run

Validate a manifest, then run the golden path.

```bash
uv run storytime validate-manifest demo/seed/demo-golden-path.json
uv run storytime run -m demo/seed/demo-golden-path.json --auto-approve
uv run storytime status <run-id>
```

> "The source manifest is a closed JSON Schema — `additionalProperties: false`
> — so input is constrained to recognised public-domain licensing before a run
> can even start. The run moves through five stages: ingest, synthesize,
> assemble, publish, with approval gates woven in. The stages don't call each
> other — they hand off through versioned, hash-verified artifact envelopes. And
> `--auto-approve` records *genuine* approval decisions; it's a local
> convenience, never a silent bypass."

Expect `COMPLETED`. Mention that `pipeline_run_id` — a ULID — is the durable key
that ties together SQLite rows, artifacts, the event log, and traces.

## Step 4 — Explain governance blocking

```bash
STORYTIME_BLOCKED_SOURCES=demo/governance/demo-blocked-sources.yaml \
  uv run storytime run -m demo/seed/demo-governance-blocked.json
uv run storytime queue --status blocked
```

> "This source is matched by a demo-only deny-list, so the fail-closed
> governance gate stops the run at ingest with a `BLOCKED` Trust Envelope. The
> Trust Envelope is a durable, per-run record of the human operator's licensing
> decision. Two things to notice. One: it fails *closed* — the run is blocked
> before any expensive or externally sensitive stage. Two: the wording is
> honest. StoryTime records a human decision; it does not perform a legal
> determination and is not a rights-clearance engine. Every governance display
> says exactly that."

The demo deny-list is supplied for one run through an environment variable; it
changes no enforcement code and no committed configuration.

## Step 5 — Explain the failure queue and the retry story

Produce the retryable technical failure (see `docs/demo.md`, "Producing the
technical failure"), then:

```bash
uv run storytime queue
uv run storytime queue --status failed
uv run storytime rerun <failed-run-id> --dry-run
uv run storytime rerun <failed-run-id>
uv run storytime run --resume <failed-run-id>
```

> "`queue` answers one question deterministically: which runs need me, why, and
> what do I look at next. It's read-only — a semantic query over SQLite, not a
> broker-backed queue, with no worker and no hidden state.
>
> `rerun` is the *only* mutation surface in the whole system. `--dry-run`
> previews the eligibility decision and changes nothing. The real `rerun`
> performs exactly one bounded change — resetting the failed run to a resumable
> state — and writes one audit event. It runs no pipeline work itself; it hands
> control back to me, and I run `--resume` explicitly. No retry loop, no
> scheduler, no daemon. And a re-run can never bypass governance — a blocked run
> is simply not eligible."

This is the sequence to land slowly: it is the clearest evidence of
failure-mode discipline.

## Step 6 — Explain the static operator report

```bash
uv run storytime report generate
# then open operator-report/index.html in a browser — no server required
```

> "This is a generated, static, read-only HTML report. No JavaScript, no web
> server, no external assets, no network — it opens straight from the
> filesystem. It's a faithful projection of the SQLite source of truth, not a
> second source of truth. There is no button here that changes state: the report
> *shows*, it never *acts*. And it's field-bounded — an explicit allowlist keeps
> raw story text, transcripts, secrets, and long free-text notes out of it
> entirely, and that's enforced by tests."

Open the completed run's detail page; show the run list, the governance
section, and — for the run from Step 5 — the event list preserving the failure,
the re-run request, and the recovery in order.

> "Nothing is rewritten or erased. That append-only audit trail — a run that
> failed, was re-run, and then completed, with its whole journey intact — is the
> point."

## Step 7 — Explain observability: traces, metrics, logs (conceptually)

You do not need the Docker stack running to explain this; describe the
architecture.

> "Under the hood the pipeline emits real OpenTelemetry — one `pipeline.run`
> span per run with child stage spans, and eight purposeful, low-cardinality
> metrics. Three things make it honest.
>
> One: telemetry is a *view*, not the source of truth. SQLite is written before
> any telemetry is emitted; with the default no-op adapter, no telemetry is
> emitted and the pipeline behaves identically. Observability can fail without
> the pipeline failing.
>
> Two: metric honesty is a build gate. There are six dashboards provisioned as
> code, and an automated test fails the build if a dashboard charts a metric the
> code doesn't actually emit. There is no dashboard the system can't back with
> real data.
>
> Three: it's vendor-neutral. Telemetry goes as standard OTLP to a local
> Collector. The Collector is the fan-out point — routing it to a backend would
> be a Collector configuration change, not an application change. I want to be
> precise here: there's no commercial vendor integration in this project. What I
> built is the architecture that would make one a configuration exercise."

If you do have the optional stack running, this is the moment to show spans in
Jaeger and the provisioned Grafana dashboards.

## Step 8 — Close the demo with business value

> "So what you've seen is an observability-native operator experience over a
> local-first pipeline. A static report you can inspect offline. A deterministic
> failure queue that tells an operator what to do next. One governed, audited
> mutation command that proves a retry is safe before changing anything. A
> fail-closed governance gate that a re-run cannot bypass. And reproducible
> fixtures so you can run every one of these scenarios yourself.
>
> The business value translates directly: automation you can trust because it's
> inspectable, failure handled as a designed-for state instead of an incident,
> recovery that's bounded and audited, and a project that says exactly what it
> does and does not do. The discipline — read-only first, bounded mutation,
> honest governance wording, append-only audit, metric honesty — is the
> deliverable. The podcast pipeline is just how I made it concrete."

---

## What this demo is not

It does not deploy to the cloud, start a hosted service, or require paid
services or credentials. It commits no generated audio and needs no
screenshots. It demonstrates governance and pipeline behaviour — it is not a
content library, and the governance status it shows is a record of a human
operator decision, not legal advice or a certification of copyright safety. See
`docs/known-limitations.md` for the boundaries in full.
