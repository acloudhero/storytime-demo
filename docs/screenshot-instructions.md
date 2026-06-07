# StoryTime — Screenshot & Evidence Instructions

Guidance for a future operator who wants to capture **visual or textual
evidence** of a StoryTime demo — for a portfolio page, a slide, or a review
write-up.

This phase (Phase 10G) **does not generate or commit any screenshots, images,
or binary assets.** This document is an *instruction list* only: it tells a
human what to capture, manually, on their own machine, outside the repository.
Captured screenshots should be kept in the operator's own portfolio workspace,
**not** committed to this repository — the repository stays source- and
text-based (see `docs/known-limitations.md` and the archive-hygiene rule).

For the demo itself see `docs/demo-script.md` (the presentation script) and
`docs/demo.md` (the full operator runbook).

---

## How to use this document

Run the demo from `docs/demo-script.md`. At the points listed below, pause and
capture evidence. Each item lists **what to capture**, **how to produce it**,
and **why it matters** for a portfolio or review audience.

Two kinds of evidence are useful:

- **Screenshots** — of the rendered static HTML operator report in a browser.
- **Text captures** — terminal output from CLI commands (a copied text block or
  a terminal screenshot). Text captures are often better than screenshots for
  CLI output: they are smaller, searchable, and easy to verify.

Capture only what the demo actually produced on your machine. Do not stage or
edit evidence.

---

## Evidence checklist

### 1. Operator report — executive summary

- **What to capture:** the `operator-report/index.html` page in a browser.
- **How:** run `storytime report generate`, then open
  `operator-report/index.html`.
- **Why it matters:** shows the static, read-only operator report and its
  executive status summary across all runs — the project's top-level "what
  happened" surface.

### 2. Operator report — a run detail page

- **What to capture:** a `run-<run_id>.html` detail page, ideally for the
  completed golden-path run.
- **How:** from the report, open the detail page for a completed run.
- **Why it matters:** shows per-run stage outcomes and the governance section
  on a single, inspectable page.

### 3. Governance warning / Trust Envelope block

- **What to capture:** the governance section on a detail page for a
  **governance-blocked** run (Scenario 3 of the demo).
- **How:** run the governance-blocked scenario, regenerate the report, open
  that run's detail page.
- **Why it matters:** shows the governance decision enum and the report-safe
  wording — *"Decision detail: blocked by governance policy; inspect Trust
  Envelope locally if authorized."* — and the standing "record of a human
  decision, not legal advice" disclaimer. This demonstrates honest governance
  display: no raw `blocked_reason`, no legal overclaiming.

### 4. Failure queue CLI output

- **What to capture:** the terminal output of `storytime queue` and/or
  `storytime queue --status failed` with at least one run present.
- **How:** produce the retryable technical failure (see `docs/demo.md`), then
  run the queue command.
- **Why it matters:** shows the read-only triage surface — a run's attention
  reason, its structured failure code, and the suggested next action. A text
  capture is recommended here.

### 5. Rerun dry-run output

- **What to capture:** the terminal output of
  `storytime rerun <run-id> --dry-run` for an **eligible** failed run.
- **How:** run `rerun --dry-run` against the failed run from item 4.
- **Why it matters:** shows the eligibility preview and the `eligible` decision
  code, and demonstrates that the preview changes nothing.

### 6. Rerun dry-run on a blocked run

- **What to capture:** the terminal output of
  `storytime rerun <blocked-run-id> --dry-run`.
- **How:** run `rerun --dry-run` against the governance-blocked run.
- **Why it matters:** shows the `governance_blocked` decision code — concrete
  evidence that a re-run cannot bypass governance.

### 7. Rerun-requested audit evidence

- **What to capture:** the terminal output of `storytime rerun <run-id>` when
  it applies the reset (the previous/new status and the audit/mutation id), and
  the run's event history after a `RunRerunRequested` event has been written.
- **How:** run `rerun` (without `--dry-run`) on an eligible run, then inspect
  the run with `storytime status <run-id>`.
- **Why it matters:** shows the single bounded mutation and the audit event —
  the core "bounded, audited mutation" talking point.

### 8. Completed-after-rerun event trail

- **What to capture:** the event history / detail page of a run that **failed,
  was re-run, and then completed** (Scenario 6 of the demo).
- **How:** resume the re-run from item 7 with `ffmpeg` available, then
  `storytime status <run-id>` and/or the report detail page.
- **Why it matters:** shows the whole journey preserved in order — the
  failure, the re-run request, and the recovered completion — demonstrating the
  append-only audit trail.

### 9. Demo fixtures directory

- **What to capture:** a listing of `demo/fixtures/`, `demo/seed/`, and
  `demo/governance/`, and optionally the contents of `demo/fixtures/index.yaml`.
- **How:** `ls demo/fixtures demo/seed demo/governance` and
  `cat demo/fixtures/index.yaml`.
- **Why it matters:** shows the reproducible scenario set — concrete evidence
  that the demo drives real, curated inputs.

### 10. Test / gate results

- **What to capture:** the terminal output of the quality gates —
  `uv run pytest -q`, `uv run ruff check .`, `uv run mypy`,
  `uv run lint-imports`, and `uv run storytime doctor`.
- **How:** run each gate locally.
- **Why it matters:** shows the project passes its own validation gates — a
  credibility anchor for any reviewer. A text capture is recommended.

---

## What NOT to do

- **Do not commit captured screenshots or images to this repository.** Keep
  them in your own portfolio workspace. The repository is intentionally
  source- and text-based, and committing binary portfolio assets would violate
  the archive-hygiene rule (see `docs/known-limitations.md`).
- **Do not generate audio for evidence and commit it.** Generated audio is
  git-ignored runtime output.
- **Do not edit or stage captures.** Capture what the demo actually produced.
- **Do not create a slide deck, PDF, or other binary deliverable inside this
  repository.** This document, like all Phase 10G output, is Markdown only.
