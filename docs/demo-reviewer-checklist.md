# StoryTime — Demo Reviewer Checklist
<!-- CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md -->
> **Canonical demo path.** For the current, authoritative reviewer/demo
> walkthrough — the system modes and boundaries, the optional loopback
> local bridge, the one controlled retry (acceptance is not success), the
> manual snapshot reload (a read-model refresh, not a live sync), and the
> governed mock-first TTS proof (provider-backed audio remains deferred) —
> see [docs/demo-walkthrough.md](demo-walkthrough.md), the single source of
> truth and evidence map. This document is a secondary/historical narrative;
> where it differs, the canonical walkthrough wins.


*Phase 12B — Portfolio Evidence Pack / Reviewer Assets. This is a wrapper and
index for a reviewer who wants to run the StoryTime demo themselves. It is
**not** a command script. `docs/demo.md` is the single authoritative source
for the exact demo commands; this checklist tells you what to do before and
around those commands, and what a correct run looks like. Do not copy commands
from here — there are none to copy. Open `docs/demo.md` and follow it.*

## Authoritative sources — open these alongside this checklist

- **`docs/demo.md`** — the operator demo runbook. This is the authoritative,
  step-by-step command sequence for all six scenarios. Run the demo from this
  file.
- **`docs/portfolio-demo-script.md`** — the narrated walkthrough. Use this if
  you want the "what to say and why it matters" narration for each step.
- **`docs/command-reference.md`** — the operator CLI reference, including the
  explicit mutation boundaries of each command.
- **`docs/known-limitations.md`** — what the demo deliberately does *not* show.

This checklist references those documents; it does not reproduce them.

## Pre-flight — before you open `docs/demo.md`

Work through these once. They are setup and environment checks, not demo steps.

- [ ] **Tooling.** Install `uv` (the project's package and environment
  manager). No other global tooling is required for the core demo.
- [ ] **Clean checkout.** Extract or clone the project into a fresh directory.
  The demo assumes a clean tree; `docs/fresh-clone-checklist.md` describes the
  fresh-clone path if you want it.
- [ ] **Dependencies.** Install from the pinned lockfile (the `uv sync`
  command is given in `docs/demo.md` "Before you start" and in the project
  `README.md`). The lockfile is committed, so the install is reproducible.
- [ ] **Environment health.** Run the environment doctor (`storytime doctor`,
  per `docs/demo.md`). Expect it to report the environment as healthy: a
  supported Python, SQLite with WAL, OpenTelemetry available as optional, and
  `ffmpeg` found. If it reports a problem, resolve that before continuing.
- [ ] **Offline expectation.** The core demo runs entirely locally with no
  required network calls. The optional observability view is Docker-dependent;
  it is not needed for the six core scenarios.
- [ ] **Time budget.** Allow roughly 15–20 minutes for all six scenarios at a
  reading pace.

## Scenario-by-scenario — what to look for

Run each scenario using the commands in `docs/demo.md`. For each one below,
the checklist gives you the **intent** and the **signs of a correct run** — so
you can tell success from failure without already knowing the system.

### Scenario 1 — Successful golden path (`docs/demo.md` §"Scenario 1")
- [ ] Intent: a well-formed, authorized source runs cleanly through all five
  pipeline stages.
- [ ] Correct run: the pipeline completes; an artifact and a feed entry are
  produced; the operator report shows the run as succeeded.

### Scenario 2 — Retryable technical failure (`docs/demo.md` §"Scenario 2")
- [ ] Intent: a technical (non-governance) failure is surfaced as retryable.
- [ ] Correct run: the run appears in the failure / review queue marked
  retryable; the report explains the failure in operator-readable terms.

### Scenario 3 — Governance-blocked path (`docs/demo.md` §"Scenario 3")
- [ ] Intent: an unauthorized source is stopped by fail-closed governance.
- [ ] Correct run: the run does **not** proceed to synthesis; it is recorded
  as governance-blocked, distinct from a technical failure. This is the
  fail-closed behaviour — a block is the correct outcome here, not an error.

### Scenario 4 — Needs-review / approval gate (`docs/demo.md` §"Scenario 4")
- [ ] Intent: a run pauses at the explicit operator approval gate.
- [ ] Correct run: the run is held pending a human decision; it proceeds only
  after the approval step in `docs/demo.md` is taken.

### Scenario 5 — Rerun requested (`docs/demo.md` §"Scenario 5")
- [ ] Intent: an operator requests a re-run of a previously failed run.
- [ ] Correct run: the re-run is recorded as requested; it resumes from the
  failed stage, not from the beginning.

### Scenario 6 — Completed after rerun (`docs/demo.md` §"Scenario 6")
- [ ] Intent: the re-run from Scenario 5 completes successfully.
- [ ] Correct run: the previously failed run now shows as completed; the
  history reflects both the original failure and the successful re-run.

## Report inspection — after the scenarios

- [ ] Generate and open the static operator report as described in
  `docs/demo.md` §"Report inspection path". It opens in a browser with **no
  server required** — it is a static, read-only local HTML artifact.
- [ ] Confirm the report shows each run's status, the failure summary for the
  failed run, and the re-run lineage. The report is read-only by design; there
  are no mutation controls in the browser (see `docs/known-limitations.md`).

## Optional — observability view

- [ ] Only if you want it: the optional observability stack (traces, metrics,
  the six Grafana dashboards) is Docker-dependent and described in
  `docs/observability-demo.md` and `docs/dashboard-guide.md`. It is **not**
  required to evaluate the six core scenarios.

## Cleaning up

- [ ] Follow `docs/demo.md` §"Cleaning up" to reset the demo state. Generated
  audio, the SQLite state database, and the operator report are run
  byproducts; they are not part of the repository and are safe to remove.

## What this demo is and is not

- It exercises the **real** pipeline, governance, queue, report, and re-run
  code — it is not a mock-up of behaviour.
- It is a **local, deterministic, fixture-driven** demonstration. The fixtures
  are small CC0 examples, not a content library.
- It is **not** a production deployment, and it does not show multi-user
  access, cloud hosting, or live alerting. `docs/known-limitations.md` and
  `docs/demo.md` §"What this demo is not" state the boundaries authoritatively.

## Reviewer sign-off

- [ ] All six scenarios ran with the expected outcomes above.
- [ ] The operator report opened and reflected the runs correctly.
- [ ] Any deviation was checked against `docs/known-limitations.md` before
  being treated as a defect.

For the claim-to-evidence map behind what this demo shows, see
`docs/portfolio-evidence-index.md`.
