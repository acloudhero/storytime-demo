# StoryTime — Demo Script
<!-- CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md -->
> **Canonical demo path.** For the current, authoritative reviewer/demo
> walkthrough — the system modes and boundaries, the optional loopback
> local bridge, the one controlled retry (acceptance is not success), the
> manual snapshot reload (a read-model refresh, not a live sync), and the
> governed mock-first TTS proof (provider-backed audio remains deferred) —
> see [docs/demo-walkthrough.md](demo-walkthrough.md), the single source of
> truth and evidence map. This document is a secondary/historical narrative;
> where it differs, the canonical walkthrough wins.


A step-by-step script for **presenting** StoryTime live, from a clean local
environment, to a reviewer, hiring manager, or Solutions Engineer interviewer.

This script is the *presentation* companion to **`docs/demo.md`**, the full
operator demo runbook. `docs/demo.md` is the authoritative source for the exact
fixture commands and expected state; this script sequences those scenarios into
a ~10–15 minute narrated walkthrough with talking points. When the two
disagree on a command, `docs/demo.md` is authoritative.

Every command below is a real, existing StoryTime command — see
`docs/command-reference.md`. No command in this script is invented.

---

## Before the demo

- Have a clean working directory and a synced environment (see "Step 0").
- Decide where demo state lives. The examples use the default `runs/`,
  `feed/`, and `operator-report/` locations; set `STORYTIME_RUNS_DIR` and
  `STORYTIME_FEED_DIR` if you want demo state isolated from other work.
- Know your `ffmpeg` situation. Scenarios that **complete** a run need
  `ffmpeg` present; the **technical-failure** scenario needs a genuine stage
  failure, produced by running with `ffmpeg` absent from `PATH`. `docs/demo.md`
  ("Producing the technical failure") explains the reproducible way to do this.
- A run id is generated when you start a run. Several later commands take that
  run id as an argument — capture it from `storytime status` or
  `storytime queue` output rather than guessing.

> **Timing note.** Steps 4, 7, and 11 each execute a real pipeline run, which
> takes a short but non-zero time. If you are tight on time, you can *describe*
> a scenario from its fixture definition in `demo/fixtures/` instead of
> executing it live — the fixture records the expected state. Say which you are
> doing.

---

## Step 0 — Start from a clean local environment

> **Talking point:** "StoryTime is local-first. Everything you are about to
> see runs on this one machine, with no cloud account and no external service."

```bash
uv sync --frozen --extra dev
```

This installs the pinned runtime and dev dependencies into a local `.venv`.

## Step 1 — Health check

```bash
uv run storytime doctor
```

> **Talking point:** "`doctor` is a read-only environment check. It confirms
> the Python version, SQLite with WAL journaling, optional OpenTelemetry, and
> whether `ffmpeg` is available — `ffmpeg` is what the assemble stage needs to
> encode MP3 audio."

Expect an `environment: healthy` summary.

## Step 2 — Inspect the demo fixtures

```bash
cat demo/fixtures/index.yaml
ls demo/fixtures demo/seed demo/governance
```

> **Talking point:** "These six fixtures are reproducible scenarios. They are
> *inputs and expected-state descriptions* — they do not fake a success path.
> Each one drives the real pipeline. The seed texts are original content
> dedicated to the public domain under CC0-1.0, so the demo depends on no
> external or ambiguously-licensed material."

## Step 3 — Validate the golden-path manifest

```bash
uv run storytime validate-manifest demo/seed/demo-golden-path.json
```

> **Talking point:** "The source manifest is a closed JSON Schema —
> `additionalProperties: false`. Input is constrained to recognised CC0 /
> US-public-domain licensing before a run can even start."

## Step 4 — Run the successful golden path

```bash
uv run storytime run -m demo/seed/demo-golden-path.json --auto-approve
uv run storytime status <run-id>
```

> **Talking point:** "This is the one-in / one-out happy path: ingest →
> synthesize → assemble → publish. `--auto-approve` records *genuine* approval
> decisions — it is a local convenience, never a silent bypass."

Expect `COMPLETED`. Capture the run id from the output.

## Step 5 — Open the static operator report

```bash
uv run storytime report generate
# then open operator-report/index.html in a browser — no server required
```

> **Talking point:** "This is a generated, static, read-only HTML report. No
> JavaScript, no web server, no network — it opens straight from the
> filesystem. It is a faithful projection of the SQLite source of truth. There
> is no button here that changes state; the report shows, it does not act."

Show the executive summary, the run list, and the golden-path run's detail
page.

## Step 6 — Show the governance posture / Trust Envelope

On the completed run's detail page, point at the governance section.

> **Talking point:** "Every run carries a Trust Envelope — a durable record of
> the human operator's licensing decision. The report shows the stable
> decision enum: `APPROVED`, `REJECTED`, `BLOCKED`, or `NEEDS_REVIEW`. It
> carries a standing disclaimer that this is a record of a human decision, not
> legal advice. StoryTime does not perform a legal determination."

## Step 7 — Show failure-queue behaviour

Produce the retryable technical failure (see `docs/demo.md`, "Producing the
technical failure" — run the retryable-failure manifest with `ffmpeg` absent),
then:

```bash
uv run storytime queue
uv run storytime queue --status failed
```

> **Talking point:** "`queue` answers one question: which runs need me, why,
> and what do I look at next? It is read-only — a deterministic semantic query
> over SQLite, not a broker-backed queue. It changes nothing."

Show that the failed run appears with its `error_kind` failure code and a
next-step hint.

## Step 8 — Show re-run eligibility (dry run)

```bash
uv run storytime rerun <failed-run-id> --dry-run
```

> **Talking point:** "`--dry-run` previews the eligibility decision and changes
> *nothing*. This failed at a genuine pipeline stage and carries an `APPROVED`
> Trust Envelope, so the decision code is `eligible`."

## Step 9 — Run the governed re-run, then resume

```bash
uv run storytime rerun <failed-run-id>            # apply the bounded reset
uv run storytime run --resume <failed-run-id>     # re-execute from the failed stage
```

> **Talking point:** "`rerun` is the *only* operator mutation surface in the
> whole system. It does exactly one thing: reset the failed run's status to the
> resumable state, and write one audit event. It runs no pipeline work itself
> — it hands control back to me, and I run `--resume` explicitly. There is no
> retry loop, no scheduler, no daemon."

## Step 10 — Show a governance-blocked scenario and explain the block

```bash
STORYTIME_BLOCKED_SOURCES=demo/governance/demo-blocked-sources.yaml \
  uv run storytime run -m demo/seed/demo-governance-blocked.json
uv run storytime queue --status blocked
uv run storytime rerun <blocked-run-id> --dry-run
```

> **Talking point:** "This source is matched by a demo-only deny-list, so the
> fail-closed governance gate stops the run at ingest with a `BLOCKED` Trust
> Envelope. Notice the `rerun --dry-run` decision code: `governance_blocked`.
> A re-run can *never* bypass governance — a blocked run is simply not
> eligible. The report and queue show the safe wording, never the raw
> `blocked_reason`."

The demo deny-list is supplied for one run through the existing
`STORYTIME_BLOCKED_SOURCES` environment variable. It changes no enforcement
code and no committed configuration.

## Step 11 — Show the completed-after-rerun narrative

Return to the run from Steps 7–9. With `ffmpeg` available again, it has been
resumed and should now complete.

```bash
uv run storytime status <run-id>
uv run storytime report generate
```

> **Talking point:** "Open the detail page for this run. Its event list
> preserves the entire journey in order — the failure, the re-run request, and
> the recovered completion. Nothing is rewritten or erased. That append-only
> audit trail is the whole point."

## Step 12 — Close on the value

> **Closing talking point:** "What you just saw is an observability-native
> operator experience over a local-first pipeline. A static report you can
> inspect offline. A deterministic failure queue that tells an operator what to
> do next. A single governed, audited mutation command that proves a retry is
> safe before changing anything. A fail-closed governance gate that a re-run
> cannot bypass. And six reproducible fixtures so you can run every one of
> these scenarios yourself. The discipline — read-only first, bounded
> mutation, honest governance wording, append-only audit — is the deliverable."

---

## What this demo is not

It does not deploy to the cloud, start a server, or require paid services. It
checks in no generated audio. It demonstrates governance and pipeline
behaviour — it is not a content library, and the governance status it shows is
a record of a human operator decision, not legal advice or a certification of
copyright safety. See `docs/known-limitations.md`.
