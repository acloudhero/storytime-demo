# Failure-Mode / Regression Hardening — Phase 11C

Phase 11C is the third Release Candidate Hardening subphase. Where Phase 11A
established the hardening baseline and Phase 11B verified fresh-clone /
operator reproducibility, Phase 11C answers a different release-candidate
question:

> What breaks, how do we know, and can we prove the system fails safely?

Phase 11C is a failure-mode and regression-hardening round. It does not add
product behaviour. It inventories the highest-risk failure and regression
paths that already exist in StoryTime, records which tests and gates protect
each one, documents how a local operator should respond when a run fails, and
adds focused regression tests where a genuine coverage gap was found. It is an
implementation candidate, pending review — it is **not** a locked phase, and
it does not start Phase 11D or Phase 12.

## What Phase 11C covers

Phase 11C is scoped to the failure and regression surfaces that a release
candidate must be able to *prove* behave safely:

- the operator failure / review queue (`storytime queue`);
- retry / re-run behaviour (`storytime rerun`) and the state it mutates;
- governance-blocked content and the safe wording shown for it;
- the static HTML operator report and its air-gapped, read-only properties;
- demo seed fixtures and their small, text-based, deterministic shape;
- the static legal-hallucination verification gate;
- operator-facing error paths and failure messages;
- state preservation around failed and re-run runs;
- traceability of blocked, failed, and retried stages.

## The Phase 11C documents

Phase 11C produces four documents, each with a distinct job:

- **This document** — the overview: what Phase 11C is, what it verified, and
  how its parts fit together.
- **`regression-risk-register.md`** — the risk inventory. Every risky path
  above, the failure it represents, its current coverage status (test-covered,
  documented-only, or deliberately deferred), and where any deferred work
  belongs.
- **`failure-mode-test-matrix.md`** — the regression coverage map. Each risky
  path mapped to the specific tests and validation gates that protect it, so a
  reviewer can see at a glance what a regression would break.
- **`operator-failure-response.md`** — the operator playbook. How a local
  operator should respond to common failure states without bypassing
  governance, deleting state, or inventing product behaviour.

## What Phase 11C verified

Phase 11C confirmed, against the Phase 11B source tree, that the
release-candidate failure-mode invariants hold:

- **Governance-blocked content stays safe.** When a run carries a `BLOCKED`
  Trust Envelope, the static report shows exactly one bounded sentence —
  `Decision detail: blocked by governance policy; inspect Trust Envelope
  locally if authorized.` — and never the raw `blocked_reason` value. The raw
  reason is visible only through the local authorized CLI, never in the
  shareable HTML artifact.
- **The static report stays air-gapped and read-only.** No `<script>` tags,
  no external CDN/font/asset references, no forms, and no mutation controls
  appear in any generated page. Report generation never mutates state.
- **Re-run cannot bypass governance.** `storytime rerun` rejects a run whose
  Trust Envelope is `BLOCKED`, `NEEDS_REVIEW`, denied, or missing, and rejects
  an operator-rejected run; an eligible re-run resets only bounded state and
  writes exactly one `RUN_RERUN_REQUESTED` audit event.
- **The failure queue is a read-only view.** `storytime queue` surfaces runs
  that need attention and points at an existing command for each; it never
  executes, claims, or mutates anything.
- **Demo fixtures stay local-first and text-based.** The demo seed manifests
  and fixture definitions remain small text files with no generated audio, no
  binary stubs, no runtime database, and no embedded secrets.
- **The legal-hallucination gate stays clean.** The static scanner reports
  zero forbidden-vocabulary violations across the repository, including the
  documents Phase 11C adds.
- **State documentation stays honest.** The State Preservation Bundle records
  Phase 11C as the current implementation candidate, keeps Phase 11B as the
  last locked phase, and does not claim that Phase 11D or Phase 12 has started
  or locked.

For the test and gate evidence behind each of these statements, see
`failure-mode-test-matrix.md`; for the full risk inventory and the status of
each path, see `regression-risk-register.md`.

## Regression tests added in Phase 11C

The existing suite already covers most failure-mode invariants directly (the
test matrix records exactly where). Phase 11C adds one focused test module,
`tests/test_failure_mode_regression.py`, for the one area that had no direct
test: **state-documentation discipline**. Those tests assert that the State
Preservation Bundle keeps Phase 11C marked as a pending-review implementation
candidate, keeps Phase 11B as the last locked phase, does not claim a future
phase has started or locked, and still retains the append-only historical
lock records that earlier phases wrote. This converts a previously
prose-only project rule into an executable regression guard.

Phase 11C adds no product behaviour, no new mutation path, and no source
change. `pyproject.toml` and `uv.lock` are unchanged; the `src/` tree is
unchanged; the only `tests/` change is the new regression module described
above.

## What Phase 11C does not do

Phase 11C does not begin Phase 11D release-evidence packaging — it only notes,
in the risk register, which evidence remains to be captured there. It does not
begin Phase 12 portfolio packaging. It does not reopen Phase 10. It does not
refactor product code, change the pipeline architecture, add operator actions,
or make the static report interactive. Anything that would change product
behaviour is out of scope and deferred to a future, separately reviewed phase.
