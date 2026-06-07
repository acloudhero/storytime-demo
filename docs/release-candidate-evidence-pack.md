# StoryTime — Release Candidate Evidence Pack — Phase 11D

The overview document for Phase 11D — Release Candidate Evidence Pack, the
fourth and final planned Release Candidate Hardening subphase. It consolidates
the release-candidate evidence produced by Phases 11A, 11B, and 11C into one
reviewer-facing index so that a reviewer, a future LLM session, or the user can
quickly answer: what has been hardened, what evidence proves it, what
validation was run, what remains out of scope, and what is ready for Phase 12.

Read `LLM_DIRECTOR.md` first; `docs/handoff-state.md` is the authoritative
current-status snapshot; `docs/phase11-plan.md` is the Phase 11 decomposition.

**Status.** This document is part of Phase 11D — Release Candidate Evidence
Pack — an implementation candidate, pending review, **not locked**. Phase 11D
does not close Phase 11 and does not start Phase 12. Phase 11C — Failure-Mode /
Regression Hardening — is the last locked phase.

## What Phase 11D is

Phase 11D is an evidence, closure-readiness, and proof-consolidation round. It
answers a single release-candidate question:

> Can we prove this release candidate is ready to show, explain, hand off, and
> package?

Phase 11D is **not** product development. It adds no product feature, no UI, no
server, no new dependency, no schema change, and no source or test change. It
adds documentation only — this evidence pack and three companion documents —
and synchronizes the State Preservation Bundle. The preferred and actual
outcome is documentation/evidence consolidation with `pyproject.toml`,
`uv.lock`, `src/`, and `tests/` byte-for-byte unchanged from the locked
Phase 11C artifact.

## The Phase 11D documents

| Document | Purpose |
|----------|---------|
| `docs/release-candidate-evidence-pack.md` | This overview and the release-candidate evidence index. |
| `docs/final-validation-summary.md` | The canonical Phase 11D validation results — the six Docker-free gates plus the governance scanner. |
| `docs/phase11-closure-checklist.md` | What Phases 11A–11D each contributed; the checklist that supports a later, explicit Phase 11 closure decision. |
| `docs/phase12-readiness-handoff.md` | What Phase 12 may safely do, and the boundary Phase 11D must not cross. |

These complement — they do not replace — the State Preservation Bundle
(`LLM_DIRECTOR.md` and the `docs/` state files), the Phase 11A–11C hardening
documents, and the Phase 10G portfolio/closure documents.

## A. Release-candidate evidence index

Each release-candidate claim below is mapped to the document(s) and test(s)
that already prove it. Phase 11D adds no new evidence-generating test: every
claim is already covered, and this index makes the existing coverage legible.

| # | Release-candidate claim | Supporting evidence |
|---|-------------------------|---------------------|
| 1 | Fresh-clone path is documented and reproducible | `docs/fresh-clone-checklist.md`, `docs/local-setup-runbook.md`, `docs/fresh-clone-troubleshooting.md`; verified in `docs/verification-log.md` (Phase 11B entry) |
| 2 | Operator reproducibility is documented and verified | `docs/operator-reproducibility-checklist.md`; the documented operator commands re-run from a clean extraction (`docs/verification-log.md`, Phase 11B entry) |
| 3 | The six Docker-free validation gates pass | `docs/rc-validation-checklist.md`; `docs/final-validation-summary.md`; `docs/verification-log.md` (Phase 11D entry) — 580 tests, ruff/mypy clean, import-linter 2/2, `storytime doctor` healthy |
| 4 | Failure-mode / regression coverage is inventoried and mapped | `docs/failure-mode-regression-hardening.md`, `docs/regression-risk-register.md` (R1–R9), `docs/failure-mode-test-matrix.md`; `tests/test_failure_mode_regression.py` |
| 5 | Governance-blocked content fails closed and the raw reason is not leaked | `tests/test_operator_report.py`, `tests/test_governance_gate.py`, `tests/test_governance_pipeline.py`, `tests/test_blocked_sources.py`; `docs/regression-risk-register.md` (R3) |
| 6 | The static HTML operator report is air-gapped and read-only | `tests/test_operator_report.py`; `docs/known-limitations.md` ("The static report is read-only") |
| 7 | The legal-hallucination / static-report safety gate reports zero violations | `tests/test_legal_hallucination_gate.py` (runs inside the pytest suite); `docs/final-validation-summary.md` |
| 8 | Demo fixtures are local-first, text-based, and deterministic | `tests/test_demo_fixtures.py`; `docs/demo-reproducibility-checklist.md`; `demo/` is text-only with no runtime DB, audio, or secrets |
| 9 | `storytime rerun` mutation is governed, bounded, and audited | `tests/test_operator_rerun.py`, `tests/test_operator_queue.py`; `docs/known-limitations.md` ("Browser-based mutation controls are intentionally absent") |
| 10 | Artifact hygiene is clean (no caches, runtime DBs, audio, binaries, secrets) | `docs/release-candidate-hardening.md` ("Artifact hygiene baseline"); the per-archive hygiene record in `docs/verification-log.md` and `docs/artifact-manifest.md` |
| 11 | Phase 10 is closed; Phase 11 is hardened across 11A–11C | `docs/canonical-state.md`, `docs/phase-history.md`, `docs/handoff-state.md`; `docs/phase11-closure-checklist.md` |
| 12 | State-documentation discipline is test-covered, not prose-only | `tests/test_failure_mode_regression.py` (the state-doc discipline guard added in Phase 11C) |

## B. Validation evidence

The canonical Phase 11D validation run — the six Docker-free quality gates plus
the in-suite legal-hallucination / governance scanner — is recorded in
`docs/final-validation-summary.md` and in the Phase 11D entry of
`docs/verification-log.md`. All six gates passed on the Phase 11C source
artifact with no source, dependency, or test change applied. If validation had
failed, the failure would have been recorded exactly as observed and returned
for human review — Phase 11D is an evidence-reporting round, not a repair
round.

## C. Phase 11 closure recommendation

`docs/phase11-closure-checklist.md` records what each Phase 11 subphase
(11A, 11B, 11C, 11D) contributed and lists the conditions for an explicit
Phase 11 closure decision. Phase 11D **does not** close Phase 11. Closing
Phase 11 is a separate, explicit decision the user makes after GPT-5.5 review,
Gemini critique, and a Phase 11D lock — see `docs/phase-closure-protocol.md`.

## D. Phase 12 readiness boundary

`docs/phase12-readiness-handoff.md` describes what Phase 12 — portfolio / demo
packaging — may safely do once Phase 11 is closed, and what Phase 11D itself
must not do. Phase 11D produces none of the Phase 12 deliverables (no portfolio
narrative rewrite, no marketing README, no LinkedIn post, no interview talking
points, no architecture diagrams, no screenshots or slides).

## E. Known limitations — final pass

`docs/known-limitations.md` is StoryTime's honest account of what the project
does **not** do. Phase 11D reviewed it and confirms it remains accurate,
explicit, and honest: it still frames the local-first scope, the absence of
multi-user auth and cloud deployment, the static read-only report, the absence
of browser mutation controls, the mock-grade TTS, the uncommitted generated
audio, the project-control (not legal-advice) nature of governance, and the
optional Docker-only observability stack as deliberate scope decisions rather
than hidden defects.

Phase 11D makes **no edit** to `docs/known-limitations.md`. It is a locked
Phase 10G deliverable; its phase-status section is self-scoped ("at the time
this document was written") and already routes the reader to
`docs/handoff-state.md` for the authoritative current status. This is the same
decision Phase 11C recorded, and it is deliberate: the limitations stay
explicit, and the current-state docs remain the single source for status.

Phase 11D does **not** overclaim. The release candidate is **not** cloud-ready,
**not** a hosted production service, and **not** publicly deployed; no
generated audio, screenshots, images, PDFs, or slide decks are committed; and
no external API integration exists. These boundaries are stated here and in
`docs/known-limitations.md` so the evidence pack cannot be read as a
production-readiness or marketing claim.

## F. Evidence capture instructions

`docs/screenshot-instructions.md` already specifies what visual and textual
evidence a future operator should capture (manually, on their own machine) for
a portfolio page or review write-up. Phase 11D reviewed it and confirms it is
ready for Phase 12: it is an instruction list only, it explicitly tells the
operator **not** to commit captured screenshots to the repository, and it
keeps the repository source- and text-based.

Phase 11D creates **no** screenshots, images, PDFs, or slide decks. Capturing
that evidence is a Phase 12 activity, performed by a human outside the
repository.

## G. Artifact hygiene proof

A release archive must contain the source tree, tests, docs, config, demo
fixtures, and lock/build files — and nothing else. The following must **never**
appear in a release artifact:

```text
.mypy_cache / .ruff_cache / .pytest_cache / .import_linter_cache
__pycache__/  and  *.pyc
.venv/  /  venv/
runs/  (including runs/state.db and any generated database file)
feed/  and any generated feed
logs/
operator-report/
generated audio — .wav / .mp3
screenshots / images / other binary assets
PDFs / PowerPoints / slide decks
node_modules/
build/  /  dist/  /  *.egg-info/
.env and any *.secret.env / *.local.env file with real values
nested release archives — *.tar.gz
.git/
large binary artifacts of any kind
```

This baseline is identical to the one in `docs/release-candidate-hardening.md`
and is consistent with `.gitignore` and `.dockerignore`. The Phase 11D archive
is built from a clean extraction of the locked Phase 11C artifact with only the
Phase 11D documentation and state edits applied; the hygiene result is recorded
in `docs/verification-log.md` and `docs/artifact-manifest.md`.

## What Phase 11D is not

- It is not Phase 12 portfolio packaging or publishing.
- It does not reopen Phase 10 or any locked Phase 11 subphase.
- It does not close Phase 11 — that is a separate, explicit user decision.
- It does not add product features, UI, servers, telemetry backends, cloud
  deployment, new schema, new dependencies, source changes, or test changes.
- It does not create screenshots, images, PDFs, slide decks, or generated
  audio.
- It does not claim evidence exists that has not been captured.
