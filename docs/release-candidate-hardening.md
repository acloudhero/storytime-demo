# StoryTime — Release Candidate Hardening Baseline

The overview document for Phase 11A — Release Candidate Hardening Baseline. It
explains what the hardening baseline is, records the artifact-hygiene and
known-limitations baselines, and indexes the other Phase 11A hardening
documents.

Read `LLM_DIRECTOR.md` first; `docs/handoff-state.md` is the authoritative
current-status snapshot; `docs/phase11-plan.md` is the Phase 11 decomposition.

**Status update.** This document describes Phase 11A. Phase 11A, Phase 11B, and
Phase 11C are now locked. Phase 11D — Release Candidate Evidence Pack — is the
current subphase (an implementation candidate pending review); it consolidates
the release-candidate evidence into a reviewer-facing pack and is summarised in
the "Phase 11 decomposition"
section below.

## What Phase 11A is

Phase 11A is the **first Release Candidate Hardening phase**. It does not add
product features, does not begin Phase 12 portfolio packaging, and does not
reopen Phase 10. It hardens the repository into a clean release-candidate
baseline by improving documentation, verification surfaces, setup
reproducibility, runbook clarity, state-document coherence, and artifact
hygiene.

The goal is a repository that is safer for a fresh clone, a cold-session LLM
handoff, an operator/demo run, the later Phase 11B/11C/11D subphases, and an
eventual Phase 12 portfolio packaging.

Phase 11A is **documentation-first**. It adds no product behaviour, no UI, no
server, no new dependency, and no schema change. It is an implementation
candidate pending GPT-5.5 review, Gemini critique, and explicit user approval —
it is not locked, and it does not by itself start Phase 11B, 11C, 11D, or
Phase 12.

## The Phase 11A hardening documents

| Document | Purpose |
|----------|---------|
| `docs/release-candidate-hardening.md` | This overview; the artifact-hygiene and known-limitations baselines. |
| `docs/phase11-plan.md` | The Phase 11 subphase decomposition (11A–11D). |
| `docs/local-setup-runbook.md` | Step-by-step local setup, fresh clone to verified environment. |
| `docs/fresh-clone-checklist.md` | The fresh-clone path condensed to a checklist. |
| `docs/rc-validation-checklist.md` | The six canonical validation commands and their expected results. |
| `docs/security-secrets-checklist.md` | The local-first security and secrets hygiene baseline. |
| `docs/demo-reproducibility-checklist.md` | How to reproduce the demo fixtures without generated audio or external APIs. |

These complement — they do not replace — the existing State Preservation
Bundle (`LLM_DIRECTOR.md` and the `docs/` state files) and the Phase 10G
portfolio/closure documents.

## Fresh-clone and setup baseline

The exact expected setup path is: clone the repository, install `uv` and the
Python requirements, sync dependencies with `uv sync --frozen --extra dev`, run
the validation commands, run `storytime doctor`, locate the `demo/` fixtures,
and understand the runtime-output directories. `docs/local-setup-runbook.md`
walks this in full; `docs/fresh-clone-checklist.md` is the at-a-glance version.

## Validation baseline

The six Docker-free quality gates are the canonical validation surface:

```bash
uv sync --frozen --extra dev
uv run pytest -q
uv run ruff check .
uv run mypy
uv run lint-imports
uv run storytime doctor
```

At the Phase 11A baseline: 549 tests pass, ruff and mypy (85 source files,
strict) are clean, the two import-linter contracts are kept, and
`storytime doctor` reports a healthy environment. The legal-hallucination
verification gate runs inside the pytest suite and reports zero violations.
See `docs/rc-validation-checklist.md` for per-gate detail.

## Artifact hygiene baseline

A release archive must contain the **source tree, tests, docs, config, demo
fixtures, and lock/build files** — and nothing that is runtime output, a local
cache, a secret, or a large binary.

The following must **never** appear in a release artifact:

```text
.mypy_cache / .ruff_cache / .pytest_cache / .import_linter_cache
__pycache__/  and  *.pyc
.venv/  /  venv/
runs/  (including runs/state.db and any generated database file)
feed/
logs/
operator-report/
generated audio — .wav / .mp3
screenshots / images / other binary assets (unless explicitly requested later)
PDFs / PowerPoints / slide decks
node_modules/
build/  /  dist/  /  *.egg-info/
.env and any *.secret.env / *.local.env file with real values
nested release archives — *.tar.gz
.git/
large binary artifacts of any kind
```

This list is consistent with `.gitignore` and `.dockerignore`, which already
exclude these paths from version control and from the Docker build context.
The release archive is built from the source tree with the same exclusions
applied. `docs/security-secrets-checklist.md` covers why the secret-bearing and
runtime-output exclusions matter, and `docs/verification-log.md` records the
hygiene check performed for each archive.

## Security / secrets baseline

The local-first security expectations are: no committed real secrets (only
`.env.example` and `config/vendor.secret.env.example` placeholder templates);
secret-bearing files (`.env`, `*.secret.env`, `*.local.env`) git-ignored; no
raw source text in telemetry or logs; no network calls required for validation;
no external API required for the demo seed path; and the governance blocked
content remaining blocked. `docs/security-secrets-checklist.md` is the full
baseline.

## Demo reproducibility baseline

A reviewer can verify the Phase 10F / 10G demo fixtures at two levels: fixture
integrity (`uv run pytest -q tests/test_demo_fixtures.py`, needing no pipeline
run, no `ffmpeg`, and no audio) and scenario execution (the six scenarios in
`docs/demo.md`, needing `ffmpeg` for the scenarios that run to completion). No
generated audio is committed; no external API is involved.
`docs/demo-reproducibility-checklist.md` is the full baseline.

## Known-limitations baseline

`docs/known-limitations.md` is StoryTime's honest account of what the project
does **not** do and where its boundaries are. As of Phase 11A it remains
accurate and explicit, and it frames deliberate scope decisions as deliberate
choices rather than hidden defects. Phase 11A makes no change to it: it is a
locked Phase 10G deliverable, and its phase-status section is self-scoped ("at
the time this document was written") and already defers to
`docs/handoff-state.md` for the authoritative current status. The known
limitations therefore remain explicit, and a reader is correctly routed to the
current-state docs for status.

## Dependency and lockfile policy

The preferred Phase 11A outcome is `pyproject.toml` **unchanged** and `uv.lock`
**unchanged**, and that is the outcome of this round. Neither file may be
modified unless there is a clear release-candidate blocker that cannot be
resolved any other way. If either file ever changes in a hardening round, the
round must explain why, prove the change is required, run the full validation
gates, and record the before/after rationale in `docs/verification-log.md`.

## Release-blocker handling

Phase 11A does not refactor product code and does not change architecture. If a
hardening round discovers a release-blocking issue, it documents it as an
explicit blocker — it does not silently rewrite the system. An architecture
change still requires a user-approved amendment routed through RoundTable, per
the amendment rule in `LLM_DIRECTOR.md`.

## Phase 11 decomposition

Phase 11A is the baseline and is locked. The intended subphases are Phase 11B
(Fresh Clone / Operator Reproducibility), Phase 11C (Failure-Mode / Regression
Hardening), and Phase 11D (Release Candidate Evidence Pack) — see
`docs/phase11-plan.md`.

Phase 11B — Fresh Clone / Operator Reproducibility — is locked. It was
verification-and-documentation work that confirmed the documented setup,
validation, and demo paths reproduce the Phase 11A baseline.

Phase 11C — Failure-Mode / Regression Hardening — is locked. It was
failure-mode and regression-hardening work: it inventoried the highest-risk
failure and regression paths, mapped the tests and gates that protect each one,
documented operator failure-response, and added one focused regression test
module (`tests/test_failure_mode_regression.py`). It added four `docs/`
documents (`failure-mode-regression-hardening.md`,
`regression-risk-register.md`, `failure-mode-test-matrix.md`,
`operator-failure-response.md`).

**Phase 11D — Release Candidate Evidence Pack — is the current subphase.** It
consolidates the release-candidate evidence produced by Phases 11A, 11B, and
11C into a reviewer-facing index, records the canonical validation results,
prepares a Phase 11 closure checklist, and writes a Phase 12 readiness handoff.
It added four `docs/` documents (`release-candidate-evidence-pack.md`,
`final-validation-summary.md`, `phase11-closure-checklist.md`,
`phase12-readiness-handoff.md`). Phase 11D is an implementation candidate,
pending review, not locked; it does not close Phase 11 and does not start
Phase 12.
