# StoryTime — Operator Experience Walkthrough
<!-- CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md -->
> **Canonical demo path.** For the current, authoritative reviewer/demo
> walkthrough — the system modes and boundaries, the optional loopback
> local bridge, the one controlled retry (acceptance is not success), the
> manual snapshot reload (a read-model refresh, not a live sync), and the
> governed mock-first TTS proof (provider-backed audio remains deferred) —
> see [docs/demo-walkthrough.md](demo-walkthrough.md), the single source of
> truth and evidence map. This document is a secondary/historical narrative;
> where it differs, the canonical walkthrough wins.


How the Phase 10 operator-experience surfaces fit together, in the order an
operator would actually use them. This is the connective-tissue document: the
per-feature guides (`docs/operator-report.md`, `docs/operator-queue.md`,
`docs/operator-rerun.md`) each describe one surface in depth; this walkthrough
shows how they compose into a single workflow.

For the exact command syntax see `docs/command-reference.md`. For a guided
demo see `docs/demo.md` and `docs/demo-script.md`.

---

## The shape of the operator experience

Phase 10 builds the operator experience as three layers over the existing
local-first pipeline, introduced in deliberate order:

1. **See** — the static HTML operator report (Phase 10B, refined in 10E).
2. **Triage** — the read-only failure/review queue (Phase 10C).
3. **Act** — the single governed mutation command, `storytime rerun`
   (Phase 10D).

The ordering is not incidental. Read-only visibility came first; the one
mutation surface came last, and only after the read-only surfaces existed to
make its effects observable. This is the Phase 10A operator-experience law
("read-only-first") expressed as a delivery sequence.

Underneath all three sits one principle: **SQLite plus the on-disk artifact
envelopes and the durable Trust Envelope are the source of truth.** The report
is a projection of that truth. The queue is a query over it. The `rerun`
command mutates it through exactly one bounded, audited operation. Nothing in
the operator layer is a second source of truth.

## Step 1 — Run the pipeline

Everything starts with a run. An operator validates a manifest and runs the
pipeline:

```bash
uv run storytime validate-manifest <manifest.json>
uv run storytime run -m <manifest.json> --auto-approve
```

A run moves the source through ingest → synthesize → assemble → publish, with
operator approval gates available, and persists every step to SQLite and to
hashed artifact envelopes. The fail-closed governance gate derives the Trust
Envelope at ingest and hard-blocks before TTS and before RSS publishing unless
the envelope is `APPROVED`.

A run ends in one of a few states: completed, failed at a stage, blocked by
governance, or paused awaiting an operator approval decision. The operator
layer exists to make each of those states **legible and actionable**.

## Step 2 — See: the static operator report

```bash
uv run storytime report generate
# open operator-report/index.html in a browser
```

The report is the operator's browsable overview of **every** run. It is a
generated, static, local, read-only HTML directory — an `index.html` executive
summary, a `runs.html` list, and a `run-<run_id>.html` detail page per run,
plus a local `style.css`. It opens directly from the filesystem; no web server
and no network are needed.

What the operator gets from the report:

- an executive status summary across all runs,
- per-run status, stage outcomes, and governance decision,
- a failure summary and re-run eligibility / action guidance for failed runs,
- a contextual command reference.

What the report deliberately does not do: it carries no JavaScript, no form,
and no control that changes state, and its field allowlist keeps raw story
text, transcripts, secrets, and long free-text notes out of the output. It is
evidence, not a control panel. See `docs/operator-report.md`.

## Step 3 — Triage: the failure / review queue

The report shows everything; the queue answers the narrower, faster question —
**which runs need me right now, and why?**

```bash
uv run storytime queue                          # all runs needing attention
uv run storytime queue --status failed          # filter by attention reason
uv run storytime queue --json                   # machine-readable
```

A run appears in the queue when it matches an attention reason — failed,
blocked by governance, marked needs-review, or awaiting an operator approval
decision. For each run, the queue shows why it needs attention and which
command, report page, or artifact to look at next. It is read-only,
deterministic, and bounded (`--limit` defaults to 20), and it surfaces
structured fields only — the `error_kind` code, never the free-text
`error_message`; the governance decision enum, never the raw `blocked_reason`.

The queue changes nothing. It is the triage step that *routes* the operator to
the right next action. See `docs/operator-queue.md`.

## Step 4 — Decide what the run needs

Triage produces a decision, and the right next action depends on *why* the run
is in the queue:

| Why the run is queued | The correct operator action |
|-----------------------|------------------------------|
| Failed at a genuine pipeline stage, `APPROVED` Trust Envelope | Re-run it — proceed to Step 5. |
| Awaiting an operator approval decision | Record a decision: `storytime approve <run-id> --stage <text\|audio> --decision <approve\|reject>`, then `storytime run --resume <run-id>`. |
| Blocked by governance (`BLOCKED` Trust Envelope) | Inspect the Trust Envelope locally if authorized. A re-run cannot override a governance block. |
| Rejected by an operator at an approval gate | The rejection stands; a re-run cannot override an operator decision. |

The `storytime rerun` command encodes exactly this logic as eligibility
checks — so an operator who reaches for `rerun` on the wrong kind of run gets a
clear, stable rejection instead of an unsafe mutation.

## Step 5 — Act: the governed re-run

For a run that failed at a genuine stage and carries an `APPROVED` Trust
Envelope, the operator uses the one mutation surface:

```bash
uv run storytime rerun <run-id> --dry-run    # preview eligibility; change nothing
uv run storytime rerun <run-id>              # apply the bounded reset
uv run storytime run --resume <run-id>       # re-execute from the failed stage
```

`storytime rerun` is the only operator mutation command in the system. It does
exactly one thing when it proceeds: it resets the failed run's persisted status
from `failed` back to the existing resumable `running` state, and writes one
`RunRerunRequested` audit event with bounded metadata only. That single status
update is the whole mutation.

Three properties make this safe:

- **It proves safety before acting.** The run must exist, be `failed`, have
  failed at a genuine stage (not an operator rejection), and carry an
  `APPROVED` Trust Envelope. Any failed check produces a stable decision code
  and a non-zero exit — `rerun` defaults to rejection whenever safety cannot be
  proven.
- **`--dry-run` is a true preview.** It evaluates eligibility and changes
  nothing — not the run, not the audit log.
- **It runs no pipeline work.** `rerun` resets state and hands control back to
  the operator, who runs `storytime run --resume` explicitly. There is no retry
  loop, scheduler, daemon, broker, or worker.

See `docs/operator-rerun.md` for the full eligibility table and audit-trail
detail.

## Step 6 — Confirm: re-read the truth

After a re-run and resume, the operator returns to the read-only surfaces to
confirm the outcome:

```bash
uv run storytime status <run-id>
uv run storytime report generate
```

A run that failed, was re-run, and completed preserves its **whole journey** on
the append-only event log — the `RunFailed` event, the `RunRerunRequested`
event, and the recovered-completion events all sit on the record together.
Nothing is rewritten or erased. The detail page for that run is the closing
piece of evidence: a failure observed, a governed re-run requested, a resume
command used, and a completed result with auditability intact.

## The workflow in one loop

```
run  ──▶  report (see)  ──▶  queue (triage)  ──▶  decide
                                                   │
              ┌────────────────────────────────────┤
              ▼                                     ▼
      rerun --dry-run                         approve / resume
              │                               (operator gate)
              ▼
      rerun  ──▶  run --resume  ──▶  report (confirm)
```

Read-only visibility surrounds a single, governed, audited mutation. That shape
— **see, triage, act safely, confirm** — is the Phase 10 operator experience.
