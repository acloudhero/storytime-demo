# Operator Queue

The **operator queue** is a read-only, terminal-native view of the StoryTime
pipeline runs that need operator attention. It is the Phase 10C complement to
the Phase 10B static HTML operator report: where the report is a browsable
overview of every run, the queue is a quick command-line answer to "which runs
need me, why, and what should I look at next?"

It is the Phase 10C implementation under the locked Architecture Baseline
Section 25 operator-experience law.

## Using the queue

```bash
uv run storytime queue                          # all runs needing attention
uv run storytime queue --status failed          # only failed runs
uv run storytime queue --status blocked         # only governance-blocked runs
uv run storytime queue --status needs-review    # only needs-review runs
uv run storytime queue --status awaiting-approval
uv run storytime queue --run-id <run_id>        # restrict to one run
uv run storytime queue --limit 20               # bound the number of results
uv run storytime queue --json                   # machine-readable output
```

`storytime queue` reads the local SQLite state database and prints a compact
list of the runs that need attention. It is a viewer only — it changes no
state, runs no other command, and needs no web server.

## What "queue" means here

The word "queue" means an **operator-facing, filtered, read-only view** of runs
needing attention — conceptually a dead-letter / review queue. It is a semantic
query over the existing SQLite source-of-truth state. It is **not** a durable,
broker-backed queue: there is no message broker, no background worker, no new
queue storage, no new run state, and no `pop` / `dequeue` / `claim` / `ack`
behaviour. Nothing in the queue mutates state.

## What statuses it surfaces

A run appears in the queue when it matches one or more **attention reasons**,
all derived from existing authoritative state:

| Reason | Meaning |
|--------|---------|
| `failed` | The run's status is `failed`, or a stage recorded a structured failure (`error_kind`). |
| `blocked` | The run's Trust Envelope governance decision is `BLOCKED`. |
| `needs-review` | The run's Trust Envelope governance decision is `NEEDS_REVIEW`. |
| `awaiting-approval` | The run is paused at an operator approval gate (`awaiting_approval`). |

`--status` filters to one reason. A run can match more than one — a
governance-blocked run is typically both `failed` and `blocked`. Healthy
`running` and `completed` runs never appear in the queue.

## What fields it displays

For each queued run the queue shows: the run id, the run status, the current /
last stage, the governance decision (if a Trust Envelope exists), a structured
failure code and a coarse failure category (if the run failed), the created /
updated timestamps, a relative path to the run's Phase 10B report detail page,
the Trust Envelope artifact path (if available), and a `next_hint` — a
suggestion of which existing command or inspection step to use next.

`failure_code` is the structured stage `error_kind` (for example `TtsError` or
`SourceNotApproved`). `failure_category` is a coarse, deterministic bucket —
`governance` for a governance-blocked or needs-review run, `stage_failure` for
a structured stage failure.

The `next_hint` is always a **suggestion**, never an automated action — for
example, "Run is awaiting an operator decision; use `storytime approve
<run_id>` to record one." It points at existing commands; the queue never
executes them. It never recommends an automated retry, deletion, publication,
or any copyright/compliance judgement.

## What it intentionally excludes

The queue surfaces only bounded, structured fields. It never displays raw
source story text, source body, generated narration text, TTS or audio
transcripts, full reviewer notes, long free-text governance notes, secrets,
tokens, API keys, full environment dumps, unbounded exception messages, or raw
telemetry. When a stage failure has an unbounded `error_message`, the queue
shows only the structured `error_kind` code — never the message text. When a
governance decision has a free-text `blocked_reason`, the queue shows only the
decision enum (`APPROVED` / `REJECTED` / `BLOCKED` / `NEEDS_REVIEW`), never the
reason text. The queue makes no legal, copyright, or compliance certification
claim; it uses neutral governance vocabulary only.

## JSON output

`storytime queue --json` emits a deterministic JSON array. Each object contains
exactly these allowlisted fields, with sorted keys:

`run_id`, `status`, `stage`, `governance_decision`, `failure_code`,
`failure_category`, `updated_at`, `created_at`, `report_path`,
`trust_envelope_path`, `next_hint`.

The JSON is produced from an explicit field allowlist — no other field can
leak into it — and is stable for identical state, so it is safe to script
against or snapshot-test.

## Default limit and sort order

The queue is always bounded. `--limit` defaults to **20**; there is
deliberately no "unlimited" option, so the queue never floods the terminal
with an unbounded backlog. `--limit` must be a positive integer.

Results are sorted **most recently updated first**, with the run id as a
stable tie-breaker. "Most recently updated" is used because it is unambiguous
and deterministic; the run that changed most recently is the one most likely
to need a decision now.

## Relationship to the Phase 10B report

The queue complements, and does not replace, the Phase 10B static HTML report.
For each run the queue prints a relative path to that run's report detail page
(`operator-report/run-<run_id>.html`). That path is a deterministic reference
— the queue does not generate, embed, or modify the report. If the report has
not been generated yet, run `storytime report generate` (the existing Phase
10B command) to produce it. The queue never runs the report generator itself.

## Determinism

The queue output contains no generation timestamp and no randomness. Given
identical SQLite state it produces byte-for-byte identical human and JSON
output, so both are safe to snapshot-test.

## What the queue is not

The queue is a read-only viewer. It has no `pop` / `dequeue` / `claim` / `ack`
behaviour and no retry, approve, reject, delete, publish, or unpublish action.
It introduces no web server, dashboard, frontend framework, authentication,
cloud service, persistent backend, message broker, background worker, or
terminal-UI dependency, and it adds no new Python dependency — it is built
entirely from the existing CLI tooling and the standard library.

The queue itself never *changes* a run. The separate `storytime rerun` command
(Phase 10D — locked) is the explicit, governed *mutation* counterpart: use
`queue` to find a failed run, then `rerun` to retry it if it is provably safe.
See `docs/operator-rerun.md`. Phase 10D does not change the queue's read-only
behaviour.

## Verification

Phase 10C ships with `tests/test_operator_queue.py` (29 tests) covering queue
membership, the empty state, `--status` / `--run-id` filtering, the bounded
default limit, deterministic sorting and JSON output, the no-raw-content /
no-secret / no-overclaiming guarantees, the non-mutating `next_hint`, and the
fact that the command neither mutates state nor requires report generation.
The six Docker-free quality gates pass — `uv sync --frozen`, pytest, ruff,
mypy, import-linter, and `storytime doctor` — and the static legal/compliance
scanner returns zero violations.
