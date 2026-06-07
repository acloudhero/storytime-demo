# Operator Re-Run

> **Status:** Phase 10D — Pipeline Re-Run / Mutation Actions is **locked /
> accepted / canonical**. This document describes the locked behaviour.

The **operator re-run** is StoryTime's first operator *mutation* surface: the
`storytime rerun` command. Phases 10B and 10C gave operators read-only ways to
*see* pipeline state — the HTML report and the failure queue. Phase 10D adds
the first way to *change* it, under strict guardrails: an operator can ask for
a failed run to be retried, and the system performs that retry only when it
can prove doing so is safe.

It is the Phase 10D implementation under the locked Architecture Baseline
Section 25 operator-experience law.

## What `rerun` does — and does not do

`storytime rerun` does exactly one thing when it proceeds: it resets a failed
run's persisted status from `failed` back to the existing `running` state, so
the existing `storytime run --resume` path can re-execute the run from the
stage it failed at. That single status update is the whole mutation. The
command then writes one audit record and tells you the next command to run.

`rerun` is deliberately small. It is **not** a workflow engine. It adds no
message broker, no background worker, no daemon, no scheduler, no job queue,
no new run lifecycle state, no new database column, no web server, no
dashboard, no authentication, and no cloud dependency. It runs no pipeline
work itself and starts no automatic retry loop — it resets state and hands
control back to the operator, who runs the existing resume command explicitly.

## Using `rerun`

```bash
uv run storytime rerun <run-id> --dry-run        # preview eligibility only
uv run storytime rerun <run-id>                  # apply the re-run reset
uv run storytime rerun <run-id> --from-stage <stage>   # explicit confirmation
uv run storytime rerun <run-id> --json           # machine-readable output
```

A typical recovery flow:

```bash
uv run storytime queue                  # find the failed run
uv run storytime rerun <run-id> --dry-run   # check it is safe to retry
uv run storytime rerun <run-id>             # apply the reset
uv run storytime run --resume <run-id>      # re-execute from the failed stage
```

`--dry-run` previews the eligibility decision and changes nothing — not the
run, not the audit log. Without `--dry-run`, an eligible run is reset and an
audit event is written; an ineligible run is rejected with a clear reason and
the command exits non-zero. `--from-stage` is an optional explicit
confirmation: if supplied it must name the stage the run failed at (the stage
the re-run will resume from). Re-running from an *earlier* stage is out of
scope for Phase 10D (see "Known limitations" below).

## When a re-run is allowed

A re-run proceeds only when **all** of the following hold:

- The target run exists.
- The run is in the `failed` state.
- The failure was a genuine pipeline-stage failure — not an operator
  rejection at an approval gate.
- A Trust Envelope governance record exists for the run.
- The Trust Envelope decision is `APPROVED`.
- Any supplied `--from-stage` names the stage the run failed at.

If any check fails, the re-run is rejected. The command defaults to rejection
whenever safety cannot be proven. Each rejection carries a stable decision
code:

| Code | Meaning |
|------|---------|
| `eligible` | The run may be re-run. |
| `run_not_found` | No run exists with that id. |
| `not_retryable_status` | The run is not in the `failed` state (e.g. completed, running). |
| `operator_rejected` | The run was rejected by an operator at an approval gate; a re-run cannot override that decision. |
| `governance_blocked` | The run's Trust Envelope decision is `BLOCKED`. |
| `trust_envelope_missing` | No Trust Envelope governance record exists for the run. |
| `trust_envelope_denied` | The Trust Envelope decision is not approved (e.g. `REJECTED`, `NEEDS_REVIEW`). |
| `stage_unknown` | `--from-stage` named a stage that is not a known pipeline stage. |
| `stage_mismatch` | `--from-stage` named a valid stage that is not the run's failed stage. |
| `unsafe_unknown_state` | The run is failed but its state cannot be classified safely. |

A re-run never bypasses governance. A run that is blocked, denied, or has no
Trust Envelope is rejected — an operator cannot retry blocked or unresolved
content merely by asking. A run rejected by an operator at an approval gate is
also rejected: re-running it would override the operator's decision.

## The audit trail

Every actual re-run mutation is recorded as a `RunRerunRequested` event in the
existing append-only `event_log`. The audit payload carries only bounded
metadata — a mutation id, the from-stage, the previous and new run status, the
governance decision, and the dry-run flag. It contains no raw story text, no
raw transcript, no raw source body, and no raw exception text.

A dry run writes no audit event (it changes no state). A rejected re-run
attempt also writes no audit event; the command instead produces deterministic
rejection output so the operator sees exactly why the request was refused.

## Output safety

Both the human-readable and `--json` output contain only bounded, structured
fields: the run id, source id, current status, requested action, from-stage,
eligibility verdict, decision code, a short safe message, the audit/mutation
id, the previous and new status, the governance decision, and a suggested next
action. They never include raw story text, raw transcripts, raw source bodies,
long raw exception messages, or sensitive governance internals. The `--json`
output keys are a fixed allowlist, so output is stable in structure.

## Relationship to Phase 10C

Phase 10C's `storytime queue` is **read-only** — it shows which runs need
attention and never changes anything. Phase 10D's `storytime rerun` is the
explicit, governed **mutation** counterpart. The two compose naturally: use
`queue` to find a failed run, then `rerun` to retry it if it is safe. Phase
10D does not change the queue's behaviour; the queue remains read-only.

## Known limitations

- **Re-run resumes from the failed stage only.** Phase 10D re-runs a run from
  the stage it failed at. Re-running from an arbitrary earlier stage — which
  would require invalidating already-completed stages — is intentionally out
  of scope for this phase. `--from-stage` therefore only accepts the run's
  failed stage, as an explicit operator confirmation.
- **`rerun` does not execute the pipeline.** It resets state and writes an
  audit record; the operator runs `storytime run --resume <run-id>` to
  actually re-execute. This keeps the mutation bounded and free of any hidden
  or long-running work.
