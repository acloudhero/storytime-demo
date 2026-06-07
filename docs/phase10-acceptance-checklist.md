# Phase 10 — Acceptance Checklist

A checklist that verifies the StoryTime **Phase 10 operator-experience layer**
is complete and ready for closure. It is written to be usable by an independent
reviewer (GPT / Gemini) and, after review, by the user as a lock checklist.

**Status of this checklist:** Phase 10G is an **implementation candidate,
pending review, not locked**. This checklist asserts that Phase 10 is *ready
to be reviewed for closure* — it does **not** declare Phase 10 closed. Phase 10
is closed only after independent review and explicit user approval. See
`docs/handoff-state.md` for the authoritative current status.

How to read the table: each item has an expected state and where to verify it.
A reviewer should confirm each independently rather than trusting the check
mark.

---

## A. Operator-experience surfaces exist

| # | Item | Expected state | Verify at |
|---|------|----------------|-----------|
| A1 | Operator baseline exists | Architecture Baseline §25 defines the Phase 10 operator-experience law; locked | `docs/architecture-baseline.md` §25; `docs/roadmap.md` |
| A2 | Static HTML operator report exists | `storytime report generate` produces a static, local, read-only HTML report | `src/storytime/reporting/`, `docs/operator-report.md` |
| A3 | Static report is refined | Executive summary, rerun eligibility guidance, failure summary, command reference, semantic badges, improved governance block (Phase 10E) | `docs/operator-report.md`, `docs/roadmap.md` (Phase 10E) |
| A4 | Failure queue CLI exists | `storytime queue` — read-only, deterministic, bounded failure/review queue | `src/storytime/operator_queue.py`, `docs/operator-queue.md` |
| A5 | Governed rerun command exists | `storytime rerun` — the single operator mutation surface | `src/storytime/operator_rerun.py`, `docs/operator-rerun.md` |

## B. Mutation is bounded, governed, and audited

| # | Item | Expected state | Verify at |
|---|------|----------------|-----------|
| B1 | Rerun mutation is bounded | `rerun` performs exactly one mutation: reset a failed run's status to the resumable state; it runs no pipeline work | `docs/operator-rerun.md`, `src/storytime/operator_rerun.py` |
| B2 | Rerun mutation is audited | Each applied re-run writes one `RunRerunRequested` event with bounded metadata only | `docs/operator-rerun.md`, `tests/test_operator_rerun.py` |
| B3 | Rerun cannot bypass governance | A run that is `BLOCKED`, denied, or envelope-missing is rejected with a stable decision code and non-zero exit | `docs/operator-rerun.md` (eligibility table) |
| B4 | `--dry-run` is a true preview | `rerun --dry-run` changes nothing — not the run, not the audit log | `docs/operator-rerun.md`, `tests/test_operator_rerun.py` |
| B5 | Governance-blocked wording is safe | The report shows the required wording and never the raw `blocked_reason`: **"Decision detail: blocked by governance policy; inspect Trust Envelope locally if authorized."** | `src/storytime/reporting/render.py`, `docs/operator-report.md` |

## C. Demo and fixtures

| # | Item | Expected state | Verify at |
|---|------|----------------|-----------|
| C1 | Demo seed data / fixtures exist | `demo/` holds four CC0 seed texts, a demo-only deny-list, and six golden-path fixture definitions | `demo/seed/`, `demo/governance/`, `demo/fixtures/` |
| C2 | Demo runbook exists | `docs/demo.md` walks an operator through the six scenarios with real commands | `docs/demo.md` |
| C3 | Demo fixtures drive the real system | Fixtures are input/expected-state descriptions; no scenario fakes a success path | `demo/fixtures/*.yaml`, `demo/README.md` |
| C4 | Demo seed content is safely licensed | Every seed text is original content dedicated to the public domain under CC0-1.0 | `demo/README.md`, `demo/fixtures/*.yaml` |

## D. Scope discipline — what Phase 10 did NOT add

| # | Item | Expected state | Verify at |
|---|------|----------------|-----------|
| D1 | No generated audio/binary artifacts committed | No `.wav` / `.mp3` or other generated audio in the repository | repository tree; `.gitignore` |
| D2 | No JavaScript / browser mutation controls | The operator report is static HTML, read-only, with no JS and no state-changing control | `src/storytime/reporting/render.py`, `docs/operator-report.md` |
| D3 | No server / dashboard / auth / cloud expansion | Phase 10 added no server runtime, dashboard service, authentication, or cloud deployment | `docs/roadmap.md`, `docs/known-limitations.md` |
| D4 | No new dependency or schema change | Phase 10B–10G added no new runtime dependency and no database schema change | `pyproject.toml`, `uv.lock`, `docs/phase-history.md` |

## E. State preservation and documentation

| # | Item | Expected state | Verify at |
|---|------|----------------|-----------|
| E1 | State preservation docs are synchronized | First-read/current-state docs agree: Phase 10F locked; Phase 10G implementation candidate, pending review; Phase 11 not started | `LLM_DIRECTOR.md`, `docs/handoff-state.md`, `docs/roadmap.md`, `docs/canonical-state.md` |
| E2 | Known limitations are documented | An honest known-limitations document exists and avoids overclaiming | `docs/known-limitations.md` |
| E3 | Phase 10G produced closure docs | Portfolio narrative, demo script, operator walkthrough, command reference, talking points, and this checklist exist | `docs/portfolio-narrative.md`, `docs/demo-script.md`, `docs/operator-experience-walkthrough.md`, `docs/command-reference.md`, `docs/observability-governance-talking-points.md`, this file |
| E4 | Verification evidence is recorded | Phase 10G gate results are recorded in the verification log | `docs/verification-log.md` |

## F. Quality gates

| # | Item | Expected state | Verify at |
|---|------|----------------|-----------|
| F1 | Test suite passes | `uv run pytest -q` — all tests pass | run locally |
| F2 | Lint passes | `uv run ruff check .` — clean | run locally |
| F3 | Type check passes | `uv run mypy` — clean (strict) | run locally |
| F4 | Import contracts pass | `uv run lint-imports` — contracts kept | run locally |
| F5 | Environment healthy | `uv run storytime doctor` — healthy | run locally |
| F6 | Legal-hallucination scanner clean | `tests/test_legal_hallucination_gate.py` passes — zero violations | run as part of F1 |

The most recently recorded gate results are in `docs/verification-log.md`.

---

## What proves Phase 10 is complete

Phase 10 set out to make StoryTime understandable, operable, and demoable by a
single local human operator without becoming a hosted SaaS product. The
evidence that the operator-experience layer is complete:

1. **The operator-experience law is locked** (Phase 10A, Architecture Baseline
   §25) and every Phase 10 implementation phase was built to it.
2. **An operator can see, triage, and act.** The static report (10B/10E), the
   failure queue (10C), and the governed rerun command (10D) together provide
   the full see → triage → act loop described in
   `docs/operator-experience-walkthrough.md`.
3. **Mutation is bounded, governed, and audited.** `storytime rerun` is the
   single mutation surface; it proves safety before acting, never bypasses
   governance, and writes an audit event.
4. **The work is demoable and reproducible.** Phase 10F's six fixtures and
   `docs/demo.md` let a reviewer reproduce every scenario locally.
5. **Scope discipline held.** Phase 10 added no JavaScript, no browser mutation
   control, no server, no dashboard, no auth, no cloud, no new dependency, no
   schema change, and committed no generated audio or binary artifacts.
6. **The story is documented honestly.** Phase 10G's closure documents explain
   what StoryTime is, why it matters, how to demo it, and where its boundaries
   are — without overclaiming.

## What this checklist does NOT do

- It does **not** mark Phase 10G locked.
- It does **not** mark Phase 10 closed.
- It does **not** start Phase 11.

Phase 10G is an implementation candidate. The required next action is
independent review (GPT-5.5 and Gemini); if that review is clean, the user may
then lock Phase 10G and close Phase 10. See `docs/handoff-state.md`.
