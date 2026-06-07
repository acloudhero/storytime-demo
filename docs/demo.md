# StoryTime Operator Demo Runbook
<!-- CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md -->
> **Canonical demo path.** For the current, authoritative reviewer/demo
> walkthrough — the system modes and boundaries, the optional loopback
> local bridge, the one controlled retry (acceptance is not success), the
> manual snapshot reload (a read-model refresh, not a live sync), and the
> governed mock-first TTS proof (provider-backed audio remains deferred) —
> see [docs/demo-walkthrough.md](demo-walkthrough.md), the single source of
> truth and evidence map. This document is a secondary/historical narrative;
> where it differs, the canonical walkthrough wins.


This runbook walks a human operator through demonstrating StoryTime from a
clean local environment, using the **demo seed data and golden-path
fixtures** in `demo/`. It is written for someone preparing a portfolio demo.

> For a tighter, narrated **presentation** sequence of the same scenarios — the
> version to follow when demoing live to a reviewer or interviewer — see
> `docs/demo-script.md`. This runbook remains the authoritative source for the
> exact fixture commands and expected state.

It is **local-first**: every step runs on one machine. It needs no cloud
account, no paid APIs, and no external services, and it relies on no generated
audio being checked into the repository.

The demo does not fake success. Each scenario drives the real existing
pipeline, operator report, failure queue, Trust Envelope governance, and
`storytime rerun` command. The fixture definitions in `demo/fixtures/` describe
what each scenario demonstrates and the state to expect.

## What you will demonstrate

| # | Scenario | Shows |
|---|----------|-------|
| 1 | Successful golden path | one-in / one-out clean run to completion |
| 2 | Retryable technical failure | failure-queue visibility, report failure summary |
| 3 | Governance-blocked | Trust Envelope BLOCKED decision, report-safe wording |
| 4 | Needs-review / approval gate | operator review gate, queue visibility |
| 5 | Rerun requested | the bounded mark-for-rerun reset and audit event |
| 6 | Completed after rerun | recovery to completion with the audit trail preserved |

## Before you start

Confirm the local environment is healthy:

```bash
uv sync --frozen --extra dev
uv run storytime doctor
```

`storytime doctor` reports whether `ffmpeg` is available. The assemble stage
needs `ffmpeg` to encode MP3 audio:

- Scenarios 1, 4, and 6 expect `ffmpeg` **present** so a run can complete.
- Scenario 2 (and the failed run reused by scenarios 5 and 6) needs a genuine
  stage failure, produced by running with `ffmpeg` **absent** — see
  "Producing the technical failure" below.

Pick a clean working directory for demo runs so you do not mix demo state into
other work. The examples below use the repository root and the default `runs/`
and `feed/` locations; set `STORYTIME_RUNS_DIR` and `STORYTIME_FEED_DIR` if you
want the demo state somewhere separate.

## Scenario 1 — Successful golden path

A clean, authorised source runs end to end and completes.

```bash
uv run storytime validate-manifest demo/seed/demo-golden-path.json
uv run storytime run -m demo/seed/demo-golden-path.json --auto-approve
uv run storytime status <run-id>
```

Expect `COMPLETED`. `--auto-approve` records genuine approval decisions — it is
a local convenience, never a silent bypass. The run does **not** appear in the
failure queue.

## Scenario 2 — Retryable technical failure

An authorised run that ingests cleanly (APPROVED Trust Envelope) but fails at a
genuine pipeline stage, and is therefore eligible for re-run.

### Producing the technical failure

StoryTime does not fabricate failures. The reproducible, environment-
independent way to produce one with existing mechanisms is to run the
retryable-failure manifest with `ffmpeg` absent from `PATH`, so the assemble
stage fails with `FfmpegUnavailable`.

A simple way to do that for one run is a temporary `PATH` that excludes
`ffmpeg`. For example, create a small directory of symlinks to the few tools
the run needs (`python3`, `sh`, `env`, `uv`, …) but not `ffmpeg`, and run with
`PATH` set to it:

```bash
PATH=/path/to/ffmpeg-free-bin \
  uv run storytime run -m demo/seed/demo-retryable-failure.json --auto-approve
```

On a host that simply has no `ffmpeg` installed, a normal run of this manifest
fails at assemble with no extra steps.

Expect `FAILED ... at stage 'assemble'` with `FfmpegUnavailable`.

### Seeing it in the queue and report

```bash
uv run storytime queue --status failed
uv run storytime report generate
```

The queue shows the run as `failed` with failure code `FfmpegUnavailable` and
failure category `stage_failure`, governance `APPROVED`, and a next hint
pointing at re-run. Open `operator-report/index.html` to see the failure
summary and the re-run eligibility guidance.

## Scenario 3 — Governance-blocked path

A source whose URL is matched by the **demo** blocked-source deny-list resolves
to a `BLOCKED` governance decision; the fail-closed gate stops the run.

```bash
STORYTIME_BLOCKED_SOURCES=demo/governance/demo-blocked-sources.yaml \
  uv run storytime run -m demo/seed/demo-governance-blocked.json
uv run storytime queue --status blocked
```

Expect `FAILED ... at stage 'ingest'` with a `BLOCKED` Trust Envelope. The
report and queue present the decision enum and the report-safe wording
("Decision detail: blocked by governance policy; inspect Trust Envelope
locally if authorized.") — never the raw `blocked_reason` text.

The demo deny-list is supplied for **one run** through the existing
`STORYTIME_BLOCKED_SOURCES` environment variable. This changes no enforcement
code and no committed configuration: the repository's
`config/governance/blocked-sources.yaml` stays empty. The block is a
source-authorisation decision; the seed text itself is original CC0 content.

A `BLOCKED` run is **not** eligible for re-run:

```bash
uv run storytime rerun <run-id> --dry-run    # decision code: governance_blocked
```

## Scenario 4 — Needs-review / approval-gate path

A run that pauses at the operator text approval gate awaiting a human
decision.

```bash
uv run storytime run -m demo/seed/demo-needs-review.json --require-approval
uv run storytime queue --status awaiting-approval
```

Expect `AWAITING APPROVAL` at the `approve_text` gate. The run is held by the
operator gate, not by governance (governance is `APPROVED`). Record a decision
to move it forward:

```bash
uv run storytime approve <run-id> --stage text --decision approve
uv run storytime run --resume <run-id>
```

An `awaiting_approval` run is **not** in the `failed` state, so `storytime
rerun` reports `not_retryable_status`: the correct action is to record an
approval decision, not to re-run.

> **Note on NEEDS_REVIEW.** This scenario uses the operator approval gate,
> which the system supports cleanly. A governance Trust Envelope decision of
> `NEEDS_REVIEW` is a distinct state the current local manifest path does not
> reach — the manifest schema restricts `license` to the recognised
> `CC0-1.0` / `PD-US` values, both of which map to an `APPROVED` envelope. The
> fixture definition `04-needs-review-approval-gate.yaml` records this
> limitation. Phase 10F documents it rather than inventing a workflow to
> manufacture a `NEEDS_REVIEW` decision.

## Scenario 5 — Rerun requested

The bounded mark-for-rerun reset, applied to the failed eligible run from
scenario 2.

```bash
uv run storytime rerun <run-id> --dry-run     # preview eligibility, change nothing
uv run storytime rerun <run-id>               # apply the reset
uv run storytime status <run-id>
```

`storytime rerun` resets the failed run's status from `failed` back to the
resumable `running` state and writes one `RunRerunRequested` audit event with
bounded metadata only. `--dry-run` previews the decision and changes nothing.
The command runs no pipeline work itself — it hands control back to you.

## Scenario 6 — Completed after rerun

Recovering the run to completion, with the whole journey preserved on the
audit record.

With `ffmpeg` available again, resume the run that was reset in scenario 5:

```bash
uv run storytime run --resume <run-id>
uv run storytime status <run-id>
uv run storytime report generate
```

Expect `COMPLETED`. The run's event list preserves the entire journey in
order — the failure (`RunFailed`), the re-run request (`RunRerunRequested`),
and the recovered completion (`AssemblyCompleted`, `RSSPublished`,
`RunCompleted`). Nothing is rewritten or erased.

This is the natural closing beat of the operator demo: a failure observed, a
governed re-run requested, a resume command used, and a completed result with
auditability intact.

## Report inspection path

At any point, regenerate and open the static operator report:

```bash
uv run storytime report generate
# then open operator-report/index.html in a browser — no server required
```

The report is the Phase 10B / 10E static, local, read-only HTML view. It
contains no JavaScript and no controls that change state; it is a faithful
projection of the SQLite state and the durable artifacts. See
`docs/operator-report.md`.

## Cleaning up

Demo runs land under `runs/` and `feed/` (or wherever `STORYTIME_RUNS_DIR` /
`STORYTIME_FEED_DIR` point), and the report under `operator-report/`. All three
are git-ignored runtime output. Delete those directories to reset between
demos; the seed data and fixtures in `demo/` are unaffected.

## What this demo is not

The demo does not deploy to the cloud, start a server, or require paid
services. It checks in no generated audio. It demonstrates governance and
pipeline behaviour — it is not a content library, and the governance status it
shows is a record of a human operator decision, not legal advice or
certification of copyright safety.
