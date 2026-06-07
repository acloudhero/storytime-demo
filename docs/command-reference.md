# StoryTime — Operator Command Reference

A concise reference for the `storytime` command-line interface, written for an
operator. For each command it states the purpose, when to use it, the safe
output expectation, **whether it mutates state**, and any operator caution.

This reference describes the CLI as it exists in the current repository. Every
command listed is real. For deeper per-feature detail see
`docs/operator-report.md`, `docs/operator-queue.md`, and
`docs/operator-rerun.md`; for the guided demo see `docs/demo.md` and
`docs/demo-script.md`.

All commands are shown with the `uv run` prefix used throughout the project.

## Mutation boundary at a glance

The single most important distinction for an operator is **read-only vs.
state-changing**.

| Command | Mutates state? |
|---------|----------------|
| `storytime version` | No |
| `storytime doctor` | No |
| `storytime validate-manifest` | No |
| `storytime status` | No |
| `storytime queue` | No |
| `storytime report generate` | No (writes a generated report directory; changes no run state) |
| `storytime rerun … --dry-run` | No |
| `storytime serve` | No (serves the feed read-only over loopback) |
| `storytime run` | **Yes** — executes the pipeline and writes run state |
| `storytime run --resume` | **Yes** — continues a run and writes run state |
| `storytime ingest` / `synthesize` / `assemble` / `publish` | **Yes** — per-stage execution |
| `storytime approve` | **Yes** — records an operator approval decision |
| `storytime rerun` (without `--dry-run`) | **Yes** — the one bounded re-run reset + audit event |

The Phase 10 operator surfaces are read-only by design — **except**
`storytime rerun`, which is the single, deliberately bounded mutation command.

---

## Read-only commands

### `storytime version`

- **Purpose:** print the StoryTime version.
- **When to use it:** to confirm which build you are running.
- **Safe output expectation:** a version string.
- **Mutates state:** no.

### `storytime doctor`

- **Purpose:** check the local environment — Python version, SQLite + WAL
  journal mode, optional OpenTelemetry, and whether `ffmpeg` is available.
- **When to use it:** first, before a demo or after setting up the environment.
- **Safe output expectation:** a list of `ok` / informational lines and an
  `environment: healthy` summary. `ffmpeg` is reported as optional; the
  assemble stage needs it to encode MP3 audio.
- **Mutates state:** no.

### `storytime validate-manifest <path>`

- **Purpose:** validate a source manifest JSON file against the closed manifest
  schema (`additionalProperties: false`, licensing constrained to recognised
  CC0 / US-public-domain values).
- **When to use it:** before running a new or edited manifest.
- **Safe output expectation:** a pass result, or a clear schema-validation
  error pointing at the problem.
- **Mutates state:** no.

### `storytime status [<run-id>]`

- **Purpose:** show run state from SQLite. With a run id, show that run; with
  no argument, list all runs.
- **When to use it:** to check the outcome of a run, or to find a run id.
- **Safe output expectation:** structured run/stage state. No raw story text.
- **Mutates state:** no.

### `storytime queue`

- **Purpose:** a read-only, bounded, terminal-native list of the runs that need
  operator attention — failed, blocked by governance, marked needs-review, or
  awaiting an operator approval decision. For each run it shows why it needs
  attention and what to inspect next.
- **When to use it:** to triage — "which runs need me, and why?"
- **Options:**
  - `--status <failed|blocked|needs-review|awaiting-approval>` — filter by
    attention reason.
  - `--run-id <run-id>` — restrict the queue to one run.
  - `--limit <n>` — bound the number of runs shown (default 20).
  - `--json` — emit deterministic machine-readable JSON.
- **Safe output expectation:** a compact, deterministic list, most-recently-
  updated first. It surfaces structured fields only — the `error_kind` code,
  never the free-text `error_message`; the governance decision enum, never the
  raw `blocked_reason`.
- **Mutates state:** **no.** The queue is a viewer only — no message broker, no
  background worker, no `pop` / `claim` / `ack`, no other command invoked.

### `storytime report generate`

- **Purpose:** generate the static, local, read-only HTML operator report from
  the SQLite state database and on-disk artifacts.
- **When to use it:** to produce or refresh a browsable overview of every run.
- **Options:**
  - `--output <dir>` — write the report into a custom directory (default
    `operator-report/`).
- **Safe output expectation:** a report directory — `index.html`, `runs.html`,
  one `run-<run_id>.html` page per run, and a local `style.css`. It opens
  directly in a browser; no web server and no network are required. The report
  contains no JavaScript and no control that changes state.
- **Mutates state:** **no run state.** It writes a generated report directory
  (git-ignored runtime output, like `runs/`); it changes no run, no artifact,
  and no governance record.
- **Operator caution:** the report is a *projection*. SQLite plus the on-disk
  artifact envelopes and the Trust Envelope remain the source of truth — if the
  report and the database ever disagree, the database is authoritative;
  regenerate the report.

### `storytime serve`

- **Purpose:** serve the local feed directory over a loopback-only,
  range-capable HTTP server, so a podcast client can stream episode audio.
- **When to use it:** to play back published feed audio locally.
- **Options:**
  - `--port <n>` — bind a specific loopback port (defaults to the configured
    HTTP port).
- **Safe output expectation:** a server bound to `127.0.0.1` only; it never
  serves outside the local host.
- **Mutates state:** no — it serves existing feed files read-only.

---

## State-changing commands

### `storytime run`

- **Purpose:** execute the pipeline for a source manifest, or resume a paused
  run.
- **When to use it:** to process a source, or to continue a run that was
  paused at an approval gate or reset by `rerun`.
- **Key options:**
  - `--manifest` / `-m <path>` — the source manifest to run.
  - `--resume <run-id>` — continue a paused or reset run; completed-stage
    artifacts are hash-verified, never regenerated.
  - `--require-approval` — insert the persisted text approval gate; the run
    pauses for an operator decision and the process exits cleanly.
  - `--require-audio-approval` — insert the persisted audio approval gate after
    synthesis.
  - `--auto-approve` — insert the text gate but satisfy gates automatically by
    recording genuine approval decisions. A local convenience, never a silent
    bypass.
- **Safe output expectation:** progress through the stages and a final run
  status (`COMPLETED`, `FAILED ... at stage '<stage>'`, or a paused state).
- **Mutates state:** **yes** — it executes the pipeline and writes run, stage,
  artifact, and governance state.
- **Operator caution:** a run blocked by the fail-closed governance gate stops
  before TTS and before RSS publishing. `--auto-approve` does not bypass
  governance — it only satisfies the operator *text* gate.

### `storytime ingest` / `synthesize` / `assemble` / `publish`

- **Purpose:** run an individual pipeline stage, carrying a run forward from
  the previous stage.
- **When to use it:** for stage-by-stage operation or inspection;
  `storytime run --resume` is the usual path.
- **Safe output expectation:** the stage's outcome and updated run state.
- **Mutates state:** **yes** — each writes stage and artifact state for the run.

### `storytime approve <run-id>`

- **Purpose:** record an operator approval decision for a run paused at an
  approval gate.
- **When to use it:** when a run is `AWAITING APPROVAL` at the text or audio
  gate.
- **Key options:**
  - `--stage <text|audio>` — which approval gate to decide.
  - `--decision <approve|reject>` — the operator decision.
  - `--operator <name>` — the name recorded as the deciding operator.
  - `--notes <text>` — optional free-text review notes.
- **Safe output expectation:** confirmation that the decision was recorded.
- **Mutates state:** **yes** — it writes a persisted, audited approval decision.
- **Operator caution:** an approval decision is durable and recorded. A run
  *rejected* by an operator at a gate cannot later be re-run by `storytime
  rerun` — re-running it would override the operator's decision.

### `storytime rerun <run-id>`

- **Purpose:** re-run a failed pipeline run — StoryTime's single operator
  *mutation* surface — but only when it can prove the re-run is safe.
- **When to use it:** when `storytime queue` shows a failed run that failed at
  a genuine pipeline stage and you want to retry it.
- **Key options:**
  - `--dry-run` — preview the eligibility decision only; **change no state.**
  - `--from-stage <stage>` — optional explicit confirmation; if supplied it
    must name the stage the run failed at.
  - `--json` — emit deterministic machine-readable JSON.
- **Eligibility:** a re-run proceeds only when the run exists, is in the
  `failed` state, failed because of a genuine stage failure (not an operator
  approval-gate rejection), and carries an `APPROVED` Trust Envelope. Each
  outcome carries a stable decision code, including `eligible`, `run_not_found`,
  `not_retryable_status`, `operator_rejected`, `governance_blocked`,
  `trust_envelope_missing`, `trust_envelope_denied`, `stage_unknown`,
  `stage_mismatch`, and `unsafe_unknown_state`.
- **Safe output expectation:** an eligibility verdict, decision code, short
  safe message, and (when applied) the audit/mutation id and the previous and
  new status. Output is restricted to a fixed allowlist of bounded fields — no
  raw story text, no raw exception text.
- **Mutates state:** **yes, when not `--dry-run` and the run is eligible** — it
  performs exactly one bounded mutation: resetting the failed run's status to
  the resumable `running` state, and writing one `RunRerunRequested` audit
  event. With `--dry-run`, or when the run is ineligible, it changes nothing.
- **Operator caution:** `rerun` does **not** execute the pipeline. After an
  eligible re-run it resets state and tells you to run
  `storytime run --resume <run-id>` explicitly. It never bypasses governance: a
  `BLOCKED`, denied, or envelope-missing run is rejected with a non-zero exit
  code. Run `--dry-run` first.

---

## A typical recovery flow

```bash
uv run storytime queue                       # find the failed run
uv run storytime rerun <run-id> --dry-run    # confirm it is safe to retry
uv run storytime rerun <run-id>              # apply the bounded reset
uv run storytime run --resume <run-id>       # re-execute from the failed stage
uv run storytime report generate            # refresh the static report
```

`queue` is read-only triage; `rerun --dry-run` is a read-only safety check;
`rerun` is the one bounded mutation; `run --resume` does the actual
re-execution; `report generate` refreshes the read-only projection.
