# StoryTime — Phase 11 Plan: Release Candidate Hardening

Phase 11 turns the post-Phase-10 codebase into a release candidate: not new
product behaviour, but a repository that a fresh clone, a cold LLM session, and
an operator/demo run can all proceed from safely and reproducibly.

This document is a **plan**. It records the intended decomposition of Phase 11
into subphases. It does **not** by itself implement Phase 11C or 11D — each of
those is a separate, scoped, reviewed round under the Phase Closure Protocol
(`docs/phase-closure-protocol.md`).

**Update — Phase 11D is now the current round.** Phase 11A, Phase 11B, and
Phase 11C are locked; Phase 11C — Failure-Mode / Regression Hardening — is the
last locked phase. Phase 11D — Release Candidate Evidence Pack — is in progress
as an implementation candidate pending review. The subphase table and the
per-subphase notes below have been updated to reflect that. See
`docs/handoff-state.md` for the authoritative current status.

Read `LLM_DIRECTOR.md` first; `docs/handoff-state.md` is the authoritative
current-status snapshot.

## Where Phase 11 sits

- **Phase 10 — Product UI / Operator Experience — is CLOSED.** All sub-phases
  (10A–10G) are locked.
- The **Post-Phase-10 Historical State Reconciliation** (the RoundTable JSON
  historical backfill) was the last locked work item before Phase 11.
- **Phase 11 — Release Candidate Hardening** is the current phase. **Phase 11A,
  Phase 11B, and Phase 11C are locked**; Phase 11C is the last locked phase;
  **Phase 11D — Release Candidate Evidence Pack — is the current subphase**, an
  implementation candidate pending review.

Phase 11 is hardening, not feature work. It is bounded by the same scope
discipline every StoryTime phase observes: no cloud, no registry, no
Kubernetes/Terraform, no CI/CD, no auth, no multi-tenancy, no new product
behaviour, and no new dependency unless a phase explicitly authorizes it.

## Subphase decomposition

| Subphase | Scope | Status |
|----------|-------|--------|
| 11A | Release Candidate Hardening Baseline — audit and document the repository's non-feature surfaces (fresh-clone readiness, validation commands, artifact hygiene, security/secrets posture, demo reproducibility, known limitations) and decompose Phase 11 | locked |
| 11B | Fresh Clone / Operator Reproducibility — verify the documented setup and demo paths actually run cleanly from a genuine fresh clone; close any gap found in 11A | locked |
| 11C | Failure-Mode / Regression Hardening — exercise and document failure modes and regression surfaces; confirm the fail-closed and read-only invariants hold under stress | locked |
| 11D | Release Candidate Evidence Pack — assemble the verification evidence, hygiene proof, and reviewer-facing summary for a release-candidate sign-off | implementation candidate / pending review (this round) |

### Phase 11A — Release Candidate Hardening Baseline (locked)

Phase 11A is documentation-first. It audited and documented the
repository's non-feature surfaces and produced the release-candidate hardening
baseline so the later subphases can proceed from a stable, understandable base.
It added no product behaviour and changed no dependency. Phase 11A deliverables:

- `docs/release-candidate-hardening.md` — the release-candidate hardening
  baseline overview.
- `docs/fresh-clone-checklist.md` — the exact fresh-clone setup path.
- `docs/local-setup-runbook.md` — a step-by-step local setup runbook.
- `docs/rc-validation-checklist.md` — the canonical validation commands and
  their expected results.
- `docs/security-secrets-checklist.md` — the local-first security and secrets
  hygiene baseline.
- `docs/demo-reproducibility-checklist.md` — how a reviewer reproduces the
  demo fixtures without generated audio or external APIs.
- `docs/phase11-plan.md` — this document.

### Phase 11B — Fresh Clone / Operator Reproducibility (locked)

Phase 11B took the Phase 11A documentation as a specification and verified it
against reality: it walked the documented setup, validation, and demo paths
exactly as written from a clean checkout and recorded the result. It re-ran the
six Docker-free quality gates and the documented operator commands from a fresh
extraction and confirmed they reproduce the Phase 11A baseline. It added two
reproducibility documents — `docs/operator-reproducibility-checklist.md` and
`docs/fresh-clone-troubleshooting.md` — refined the Phase 11A reproducibility
documents, and aligned the documented setup commands. It added no product
behaviour and changed no dependency. Phase 11B is locked.

### Phase 11C — Failure-Mode / Regression Hardening (locked)

Phase 11C exercised and documented the system's failure modes — the
governance-blocked path, the retryable stage failure, the operator-rejection
path, the ineligible-rerun decisions, the static-report safety invariants — and
confirmed the read-only-first and fail-closed invariants hold. It inventoried
the highest-risk failure and regression paths, mapped the tests and gates that
protect each one, documented operator failure-response, and added one focused
regression test module (`tests/test_failure_mode_regression.py`, the
state-documentation discipline guard). It is hardening and documentation work;
it added no product behaviour, changed no dependency, and changed no source. It
added four `docs/` documents (`failure-mode-regression-hardening.md`,
`regression-risk-register.md`, `failure-mode-test-matrix.md`,
`operator-failure-response.md`). Phase 11C is locked; it is the last locked
phase.

### Phase 11D — Release Candidate Evidence Pack (implementation candidate / pending review — this round)

The current round, and the closing subphase of Phase 11. It assembles the
release-candidate evidence — the verification log, the archive-hygiene proof,
the reproducibility confirmation, the validation results — into a
reviewer-facing pack that supports a release-candidate sign-off decision. It
added four `docs/` documents (`release-candidate-evidence-pack.md`,
`final-validation-summary.md`, `phase11-closure-checklist.md`,
`phase12-readiness-handoff.md`), refreshed the Phase 11 status documents, and
synchronized the State Preservation Bundle. It added no product behaviour,
changed no dependency, and changed no source or test. Phase 11D is an
implementation candidate, pending review, not locked; it does not close
Phase 11 and does not start Phase 12.

## What Phase 11 is not

- It is not Phase 12 portfolio packaging or publishing.
- It does not reopen Phase 10 or any earlier locked phase.
- It does not add product features, UI, servers, telemetry backends, cloud
  deployment, new schema, or new dependencies.
- Subphase order (11A → 11B → 11C → 11D) is the plan; each subphase is locked
  under the Phase Closure Protocol before the next begins, and the user may
  re-sequence or rescope a subphase at a review gate.

## Acceptance gates (unchanged)

Every Phase 11 subphase that is an implementation round must pass the six
Docker-free quality gates (`docs/rc-validation-checklist.md`) and complete the
Phase Closure Protocol — implementation output → GPT-5.5 review → Gemini
critique → explicit user approval. Implementation output is never, by itself,
phase completion.
