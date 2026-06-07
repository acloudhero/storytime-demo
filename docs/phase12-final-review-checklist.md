# StoryTime — Phase 12 Final Review Checklist

The checklist a reviewer — GPT-5.5, Gemini, or an Opus review gate — should use
to evaluate whether **Phase 12D can be locked** and whether **Phase 12 can be
closed**. It is written by Phase 12D — Phase 12 Closure Plan / Final Portfolio
Handoff Definition.

**This checklist does not lock Phase 12D and does not close Phase 12.** It
gives the reviewer a structured basis for that decision. Locking Phase 12D and
closing Phase 12 are explicit decisions made at the review gate under
`docs/phase-closure-protocol.md`.

**How to use it.** Work top to bottom. Every check should be confirmable from
the repository alone. A check that fails is either a no-go for closing Phase 12
or, if it is minor and documentation-local, a candidate for a bounded
`Phase 12D.1` cleanup folded into the Phase 12D lock — see
`docs/phase12-closure-plan.md` for the close / cleanup / Phase 12E decision.

## 1. State accuracy

- [ ] `docs/handoff-state.md` records Phase 10 CLOSED, Phase 11 CLOSED, and
  Phase 12 STARTED / not closed.
- [ ] Phase 12A, Phase 12B, and Phase 12C are recorded as locked, with Phase
  12C named as the last locked phase.
- [ ] Phase 12D is recorded as an implementation candidate, pending review,
  **not** locked — no document claims Phase 12D is locked.
- [ ] No document claims Phase 12 is closed; closing Phase 12 is framed as the
  pending decision this round prepares.
- [ ] Phase 12E, if mentioned, is marked optional / future / contingency-only /
  not started — no document claims Phase 12E has started or locked.
- [ ] Phase 13 is marked roadmap-preserved only and NOT STARTED.

## 2. Living-doc consistency

- [ ] `LLM_DIRECTOR.md`, `README.md`, `docs/handoff-state.md`,
  `docs/roadmap.md`, `docs/canonical-state.md`, `docs/phase-history.md`,
  `docs/artifact-manifest.md`, `docs/verification-log.md`,
  `docs/open-issues.md`, and `docs/roundtable-import-bridge.md` all describe the
  same current state (Phase 12C last locked; Phase 12D candidate; Phase 12
  started, not closed).
- [ ] The append-only documents (`docs/canonical-state.md`,
  `docs/phase-history.md`) retain every prior lock record and add the Phase 12C
  lock entry and the Phase 12D round entry as new appends — no history is
  rewritten or truncated.
- [ ] Any superseded current-state note is clearly marked historical, so a cold
  session cannot misread it as current.

## 3. Portfolio artifact completeness

- [ ] Every asset listed in the Phase 12 asset inventory
  (`docs/phase12-closure-plan.md`) exists in `docs/`.
- [ ] The Phase 12D documents — `docs/phase12-closure-plan.md`,
  `docs/final-portfolio-handoff.md`, and this checklist — are present.
- [ ] `docs/portfolio-evidence-index.md` and
  `docs/se-interview-evidence-matrix.md` point only at files that exist.
- [ ] The reviewer entry paths in `docs/final-portfolio-handoff.md` resolve to
  real documents.

## 4. Public-safety / readiness posture

- [ ] `docs/public-repository-readiness.md` is present and frames public
  release as a gated future action with "do not publish until verified" hard
  gates — not as a completed event.
- [ ] No document claims StoryTime is publicly released, production-deployed,
  or feature-complete beyond what the evidence supports.
- [ ] `docs/known-limitations.md` remains the authoritative, honest statement
  of scope boundaries.

## 5. No product / runtime changes

- [ ] `src/` is byte-for-byte unchanged from the Phase 12C source artifact.
- [ ] No change to pipeline behaviour, `storytime rerun`, Trust Envelope
  enforcement, API, CLI, or telemetry behaviour.
- [ ] No database schema change and no ARCH-LOCKed contract change.

## 6. No dependency drift

- [ ] `pyproject.toml` and `uv.lock` are byte-for-byte unchanged from the
  Phase 12C source artifact.
- [ ] No new dependency, package file, or lockfile change of any kind.

## 7. No GUI / frontend / Phase 13 implementation

- [ ] No frontend directory, JavaScript, browser-app code, UI runtime code,
  React/Vite/TypeScript file, framework scaffolding, component file, route, or
  UI asset was added.
- [ ] Phase 13 GUI work is not implemented; the Phase 13 material remains
  roadmap and vision only (`docs/roadmap.md` Phase 13 note, `docs/GUI_vision.md`).

## 8. Validation evidence

- [ ] The six Docker-free gates were run and their results recorded honestly in
  `docs/verification-log.md`: `uv sync --frozen --extra dev`, `uv run pytest -q`,
  `uv run ruff check .`, `uv run mypy`, `uv run lint-imports`,
  `uv run storytime doctor`.
- [ ] If `tests/test_failure_mode_regression.py` was advanced, the change is the
  narrow, explicitly authorized mechanical state-discipline guard advance only,
  and the guard is strengthened, not weakened.
- [ ] No validation is claimed to pass without having been run.

## 9. Archive hygiene

- [ ] The delivered archive contains no `.pytest_cache`, `.ruff_cache`,
  `.mypy_cache`, `__pycache__`, `*.pyc`, virtual environment, `.git`,
  `node_modules`, package cache, generated audio, generated screenshot or
  video, secret, local `.env` file, runtime database, or nested review bundle.
- [ ] The archive contains only the intended documentation, README, state, and
  authorized test changes over the Phase 12C source artifact.

## Reviewer decision

After completing the checklist, the reviewer should record one of:

- **Lock Phase 12D and close Phase 12** — all checks pass; Phase 12D is the
  designated closure round and no further packaging subphase is needed. This is
  the outcome `docs/phase12-closure-plan.md` recommends when the review is clean.
- **Lock Phase 12D after a bounded `Phase 12D.1` cleanup, then close Phase 12** —
  only minor, documentation-local issues were found; fix them in a bounded
  cleanup folded into the Phase 12D lock lineage.
- **Do not lock yet; a substantive gap needs a separate `Phase 12E`** — a
  substantive packaging gap was found that a bounded cleanup cannot fix.
- **Lock Phase 12D only, defer the Phase 12 closure decision** — Phase 12D is
  sound but the reviewer wants the Phase 12 closure decision taken separately.

In every case, the decision is the reviewer's and the user's at the gate; this
checklist informs it and does not pre-empt it.
