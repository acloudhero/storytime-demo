# Operator Failure-Response Playbook — Phase 11C

This document tells a local StoryTime operator how to respond when a run does
not complete cleanly. It is a Phase 11C — Failure-Mode / Regression Hardening
deliverable. Every response below uses an existing, read-only or
already-governed command. None of them bypasses governance, deletes state, or
invents product behaviour.

Three rules apply to every situation:

1. **Inspect before acting.** Always look at the run's state and report
   before deciding what to do.
2. **Never bypass governance.** A governance block is a decision, not a bug.
   No operator response should attempt to route around it.
3. **Never hand-edit state.** The SQLite state store and the on-disk artifact
   envelopes are the source of truth. Repair a run through the governed
   commands, never by editing the database or the artifact files directly.

## First step for any failure: triage

When something looks wrong, start with the failure / review queue:

```bash
uv run storytime queue
```

The queue is a read-only view. It lists every run that needs attention —
failed, blocked by governance, marked needs-review, or awaiting an operator
approval decision — and for each one tells you *why* and *which command,
report, or artifact to look at next*. It never executes anything.

Then look at the specific run and the report:

```bash
uv run storytime status RUN_ID
uv run storytime report generate
```

`status` prints the run's stage history and governance decision. `report
generate` refreshes the static HTML operator report; open the run's detail
page for the executive summary, the stage table, and the suggested next
action. Report generation is read-only and never mutates state.

## Situation: a stage failed for a technical reason

**Symptom.** The queue lists the run as failed; `status` shows a stage with a
failed status and a structured failure category.

**Response.** A genuine stage failure on a run that carries an `APPROVED`
Trust Envelope is the case re-run is designed for. Preview first:

```bash
uv run storytime rerun RUN_ID --dry-run
```

The dry run changes nothing; it only reports whether the run is eligible and
which stage it would re-run from. If it reports eligible, apply it:

```bash
uv run storytime rerun RUN_ID
uv run storytime run --resume RUN_ID
```

The applied re-run resets only the bounded run status to the resumable state
and writes one `RUN_RERUN_REQUESTED` audit event; it does not erase prior
decisions or history. `run --resume` then re-executes from the failed stage.

**Do not** edit the state database to mark the run complete, and do not delete
the run directory to "start over" — that destroys the audit trail.

## Situation: the run is blocked by governance

**Symptom.** The queue lists the run as blocked; the report's governance
section shows `BLOCKED` and the bounded sentence `Decision detail: blocked by
governance policy; inspect Trust Envelope locally if authorized.`

**Response.** This is a governance decision, not a failure to repair. A re-run
will be rejected by design — `storytime rerun` refuses a run with a `BLOCKED`
Trust Envelope, because a re-run must never bypass a governance block.

If you are an authorized local operator and need the underlying detail,
inspect the Trust Envelope artifact locally — its key is shown in the report's
governance section, and the local CLI `status` view shows the recorded reason.
The raw reason is deliberately kept out of the shareable HTML report; it is
available only through local, authorized inspection.

If the block is correct, the run stays blocked — that is the system working.
If you believe a source was blocked in error, the correct path is to revisit
the source's licensing and governance metadata and the blocked-source list,
not to force the run through.

## Situation: the run is waiting for an approval decision

**Symptom.** The queue lists the run as awaiting approval, or `status` shows
an operator approval gate with no decision.

**Response.** The run is paused on purpose, waiting for a human decision. Use
the existing approval command for the configured gate to record your decision.
The run does not need re-running; it needs a decision. Re-run is for failed
stages, not for paused approval gates — `storytime rerun` rejects an
operator-rejected run rather than re-running it.

## Situation: the run is marked needs-review

**Symptom.** The queue lists the run as needs-review; the governance section
shows a `NEEDS_REVIEW` decision.

**Response.** A `NEEDS_REVIEW` Trust Envelope means governance has not reached
an `APPROVED` decision. Re-run will be rejected, exactly as it is for a
blocked run. Resolve the review through the normal governance path — confirm
the source's licensing and governance metadata and record the governance
decision — rather than attempting to re-run around it.

## Situation: the report or a command shows an error message

**Symptom.** A command exits non-zero with a message, or the report's failure
category is populated.

**Response.** StoryTime's operator-facing messages are intentionally bounded:
they describe the failure category and the next action, and they do not print
raw stack traces, unbounded exception text, or raw internal error strings. Read
the message, then follow the triage step above — `queue`, `status`, `report
generate` — to see the structured context. If you need a machine-readable
form, `storytime rerun RUN_ID --json` emits a deterministic, allowlisted set
of fields.

If a command genuinely cannot run at all — for example a missing toolchain
prerequisite — run:

```bash
uv run storytime doctor
```

`doctor` checks the local environment (Python version, SQLite, optional
ffmpeg, optional OpenTelemetry) and reports what is missing. For fresh-clone
and setup problems, see `fresh-clone-troubleshooting.md`.

## What never to do

- Do not hand-edit `runs/state.db` or any artifact envelope to change a run's
  status, decision, or history.
- Do not delete a run directory to clear a failure; that destroys traceable
  state. Re-run the run through the governed command instead.
- Do not attempt to re-run a blocked, needs-review, denied, or
  missing-envelope run; the re-run command will reject it, and that rejection
  is correct.
- Do not edit the static HTML report to remove a governance warning or change
  a decision; the report is a generated projection, not a source of truth.
- Do not treat a governance block as a technical failure. A block is a
  decision; the response is to revisit the source's governance metadata, not
  to route around the decision.

## Where this fits

This playbook covers operator response. For the inventory of risky paths and
their coverage status see `regression-risk-register.md`; for the test and gate
evidence see `failure-mode-test-matrix.md`; for the Phase 11C overview see
`failure-mode-regression-hardening.md`.
