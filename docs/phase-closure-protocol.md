# StoryTime Phase Closure Protocol

## 1. Purpose

The StoryTime Phase Closure Protocol defines how RoundTable determines whether a phase is complete, whether a phase may be locked, and whether the project may advance to the next phase.

StoryTime is not only a content-to-audio pipeline. It is also a proving ground for a disciplined AI-assisted development process intended to scale to future projects. For that reason, phase closure must be explicit, reviewable, and user-approved.

This protocol exists to prevent a common AI-build failure mode:

- A model produces output.
- The output looks plausible.
- The project treats the output as finished.
- Later phases build on hidden defects, missing tests, unverified assumptions, or architectural drift.

StoryTime rejects that pattern.

A phase is not complete because a model says it is complete.

A phase is not complete because files were generated.

A phase is not complete because code compiles once.

A phase is not complete because a mediator summary sounds confident.

A phase is complete only when the required phase artifacts exist, have been reviewed against the phase acceptance criteria, have survived critique, have been cleaned up if necessary, have passed re-review when required, and have been explicitly approved by the user.

This protocol defines the governance layer that sits above implementation.

It applies to:

1. Planning phases.
2. Canonical document generation.
3. Architecture ratification.
4. Scaffold implementation.
5. Vertical-slice implementation.
6. Cleanup rounds.
7. Verification rounds.
8. Phase lock decisions.
9. Model-routing decisions for future phases.

The user remains the final decision-maker at every phase boundary.

## 2. Core Principle: Implementation Output Is Not Phase Completion

The core principle of this protocol is:

Implementation output is not phase completion.

A Claude implementation, GPT document, Gemini critique, scaffold package, code diff, generated file, passing command, or model statement is only a phase artifact. It is not a phase lock.

A phase moves through three different states:

1. Output produced.
2. Output reviewed.
3. Phase locked.

These states must not be collapsed.

Output produced means a model has generated something requested by the phase.

Output reviewed means the output has been evaluated against the phase criteria, architecture rules, and known risks.

Phase locked means the user has explicitly accepted the reviewed output as canonical for that phase.

The difference matters.

A code phase can produce a scaffold that imports successfully while still violating architecture boundaries.

A document phase can produce a polished Markdown file while still missing a hard decision.

A test phase can produce passing tests while failing to test the acceptance criteria that matter.

A mediator phase can produce a clean summary while accidentally converting unresolved assumptions into canonical state.

Therefore, every phase requires review before lock.

The phase closure process must preserve:

1. Evidence.
2. Review.
3. Critique.
4. Cleanup.
5. Re-review when needed.
6. User approval.
7. Canonical state update.
8. Explicit phase lock.

No phase advances merely because the previous model output was impressive.

## 3. Standard Phase Closure Loop

The standard StoryTime phase closure loop is:

1. GPT-5.5 defines the phase brief, scope, acceptance criteria, and model routing.
2. The selected implementation or generation model produces the phase artifact.
3. GPT-5.5 reviews the output against the phase brief and canonical state.
4. Gemini reviews the output as an independent critic.
5. GPT-5.5 synthesizes the reviews into agreements, disagreements, risks, open questions, and recommended decisions.
6. If defects exist, GPT-5.5 creates a cleanup or fix prompt.
7. Claude performs the cleanup or fix when implementation or structured editing is required.
8. GPT-5.5 re-reviews the cleaned output.
9. Gemini re-reviews the cleaned output when the defect affected architecture, process integrity, public-facing records, or phase acceptance.
10. GPT-5.5 recommends whether the phase can lock.
11. GPT-5.5 recommends which models should participate in the next phase.
12. The user reviews the recommendation.
13. The user approves, rejects, edits, or defers the lock.
14. If approved, the canonical state is updated.
15. The phase is marked locked.
16. Only then may the next phase begin.

The loop may be shortened only when the phase is low-risk and the user explicitly approves the shorter path.

The loop may be extended when:

1. Multiple reviewers identify blockers.
2. The output violates a hard decision.
3. The output introduces unplanned architecture.
4. The output creates source-of-truth confusion.
5. The output cannot be verified.
6. The output is missing required artifacts.
7. The output is too compressed to be implementation-safe.
8. The user is uncertain or disoriented about the process state.

The default is rigor over speed at phase boundaries.

Speed is appropriate inside bounded implementation tasks.

Rigor is required when deciding what becomes canonical.

## 4. Failure / Iteration Branch

When a phase artifact fails review, the project must not proceed by pretending the failure is minor.

A failed review must be classified.

Failure categories:

1. Missing artifact.
2. Incomplete artifact.
3. Wrong artifact type.
4. Scope violation.
5. Architecture violation.
6. Test failure.
7. Import-boundary violation.
8. Public-facing language violation.
9. Security or licensing violation.
10. Source-of-truth ambiguity.
11. Compression or truncation.
12. Unresolved assumption converted into canonical state.
13. Implementation output treated as phase completion.
14. Phase acceptance criteria not met.

When a failure is identified, GPT-5.5 must determine the repair path.

Possible repair paths:

1. Surgical patch.
2. Full regeneration.
3. Cleanup implementation pass.
4. Architecture clarification round.
5. Additional critic review.
6. User decision round.
7. Deferral into open issues.
8. Rejection of the artifact.

A surgical patch is preferred when the document or implementation is mostly sound and the defect is localized.

Full regeneration is preferred when the artifact is structurally unreliable, compressed, contradictory, or missing core sections.

A cleanup implementation pass is preferred when code exists but violates constraints in a fixable way.

An architecture clarification round is required when models disagree about a load-bearing design decision.

A user decision round is required when the next step depends on a product, process, or risk tolerance choice that only the user can make.

If a defect is repaired, the repair must be reviewed.

The reviewer should focus on the changed area and any affected dependencies.

A repair does not automatically lock the phase.

A repaired artifact returns to the review loop.

## 5. GPT-5.5 Review Responsibility

GPT-5.5 is the mediator, architect, state keeper, phase planner, prompt engineer, and synthesis layer.

GPT-5.5 is responsible for preserving coherence.

GPT-5.5 must review phase artifacts against:

1. The user's stated intent.
2. The current canonical state.
3. The active phase brief.
4. The phase acceptance criteria.
5. Hard architectural decisions.
6. Prior model agreements and disagreements.
7. Public-facing record rules.
8. Known open questions.
9. Model-role boundaries.
10. Phase advancement rules.

GPT-5.5 must not simply average model opinions.

If Gemini identifies a process risk and Opus identifies an implementation constraint, GPT-5.5 must synthesize them according to role weight.

If Sonnet produces working code that violates the Architecture Baseline, GPT-5.5 must reject the shortcut even if the code works.

If Opus produces a sophisticated artifact that exceeds scope, GPT-5.5 must trim the phase boundary.

If Gemini raises an adversarial critique that protects canonical integrity, GPT-5.5 must not dismiss it merely because it slows the process.

GPT-5.5 must identify:

1. Agreements.
2. Disagreements.
3. Risks.
4. Open questions.
5. Required edits.
6. Suggested user decisions.
7. Next actions.
8. Next-round prompt.
9. Canonical state update.

GPT-5.5 must also distinguish between:

1. Canonical content.
2. Process commentary.
3. Raw notes.
4. Model response records.
5. Future open issues.
6. Implementation artifacts.

GPT-5.5 should flag when a model response contains material that belongs in one category but not another.

For example:

- Opus commentary may belong in the RoundTable response record.
- The extracted Markdown artifact may belong in canonical docs.
- A model's warning may belong in open issues.
- A temporary scaffolding question may not belong in the Product Charter.

GPT-5.5 must keep these categories separate.

## 6. Gemini Critique Responsibility

Gemini's role is independent critic and architecture reviewer.

Gemini should challenge:

1. Hidden coupling.
2. Overengineering.
3. Underengineering.
4. Architecture theater.
5. Source-of-truth drift.
6. Missing acceptance criteria.
7. Truncation and compression.
8. Output that looks complete but is not verifiable.
9. Model hallucination.
10. Phase boundary confusion.
11. Public-facing language leakage.
12. Undeclared implementation assumptions.
13. Unsafe shortcuts.
14. Canonical state ambiguity.

Gemini is not required to be agreeable.

Gemini should be adversarial but fair.

Gemini should recognize when an artifact is ready.

Gemini should not create additional process loops merely for ceremony.

A Gemini critique is most valuable when it identifies whether the current artifact can safely become canonical.

Gemini should answer:

1. Is this artifact complete?
2. Is this artifact phase-appropriate?
3. Does this artifact preserve the hard decisions?
4. Does this artifact introduce hidden risk?
5. Does this artifact require edits?
6. Is this artifact ready to lock?
7. If not, what exact changes are required?

Gemini should not rewrite the artifact unless asked.

Gemini should provide recommended edits when blockers exist.

Gemini should distinguish between blockers and non-blocking caveats.

When Gemini verifies a patch that it previously requested, another Gemini round is not automatically required unless the patch introduces new risk.

## 7. Claude Cleanup Responsibility

Claude's responsibility depends on which Claude model is used.

Claude Opus is used for:

1. Deep implementation.
2. Hard engineering review.
3. Architecture-sensitive document generation.
4. Complex refactors.
5. State durability.
6. Observability boundaries.
7. Failure recovery.
8. Release hardening.
9. Dense technical artifact production.

Claude Sonnet is used for:

1. Everyday implementation.
2. Scaffold creation.
3. Test additions.
4. Bug fixes.
5. UI/API work when applicable.
6. Documentation updates.
7. Cleanup passes.
8. Bounded iteration after the architecture is locked.

Claude cleanup passes should be narrowly scoped.

A cleanup prompt should tell Claude:

1. What artifact or files to edit.
2. What not to edit.
3. Which defects to fix.
4. Which architecture rules must remain unchanged.
5. Which tests to run.
6. Which output sections to return.
7. Which risks require mediator review.

Claude must not use a cleanup pass to redesign locked architecture.

Claude must not resolve open questions unless the prompt explicitly authorizes it.

Claude must not add features during cleanup.

Claude must not convert phase cleanup into the next phase.

Claude's cleanup output is not automatically accepted.

It returns to GPT-5.5 and Gemini review when the cleanup affects architecture, phase gates, canonical documents, or implementation correctness.

## 8. Re-Review Requirement

Re-review is required when a phase artifact has been edited after a blocking review.

The level of re-review depends on the type of change.

GPT-5.5 re-review is required after every cleanup that affects:

1. Canonical documents.
2. Architecture boundaries.
3. Acceptance criteria.
4. Phase status.
5. User-facing decisions.
6. Implementation gates.
7. Open questions.
8. Test obligations.

Gemini re-review is required when cleanup affects:

1. Architecture.
2. Process integrity.
3. Canonical state.
4. Hard decisions.
5. Public-facing records.
6. Phase-lock criteria.
7. Any issue Gemini previously identified as blocking.

Opus re-review is required when cleanup affects:

1. Durable state.
2. Artifact contracts.
3. Trace-context propagation.
4. DTO/stage model.
5. Telemetry boundaries.
6. Failure recovery.
7. Complex implementation mechanics.

Sonnet re-review is useful when cleanup affects:

1. Scaffold feasibility.
2. File layout.
3. CLI ergonomics.
4. Test execution.
5. Simple implementation correctness.

Re-review should be scoped.

If only Section 15 of a document changed, the re-review should focus on Section 15 and dependent sections.

If the entire architecture was regenerated, full re-review is required.

If a model verifies an exact patch in the same cycle, another separate round is not automatically required.

The goal is to catch meaningful risk, not to create bureaucratic drag.

## 9. Next-Phase Model-Routing Recommendation

Before a phase advances, GPT-5.5 must recommend which models should participate in the next phase.

This recommendation must be explicit.

The recommendation should consider:

1. Phase type.
2. Artifact type.
3. Engineering risk.
4. Architecture sensitivity.
5. Implementation complexity.
6. Need for independent critique.
7. Cost and token efficiency.
8. User workflow load.
9. Known model strengths.
10. Known model failure modes.

General routing guidance:

GPT-5.5 Thinking should be used for:

1. Phase planning.
2. Mediator synthesis.
3. Canonical state updates.
4. Prompt generation.
5. Architecture consistency.
6. Acceptance criteria.
7. Review synthesis.
8. Process governance.

Claude Opus should be used for:

1. Hard implementation.
2. Architecture-sensitive generation.
3. Deep refactors.
4. Observability instrumentation.
5. Distributed workflow design.
6. Durable state and recovery.
7. Hardening.
8. Complex debugging.

Claude Sonnet should be used for:

1. Scaffold implementation.
2. Everyday coding.
3. Bounded fixes.
4. Tests.
5. Small docs updates.
6. Phase cleanup after architecture is locked.

Gemini should be used for:

1. Independent critique.
2. Architecture review.
3. Process risk review.
4. Hidden coupling detection.
5. Anti-overengineering review.
6. Canonical lock verification.

Haiku may be used for:

1. Checklist compression.
2. Summaries.
3. File inventories.
4. Change logs.
5. Low-risk documentation cleanup.

Model routing must be approved by the user before the next phase begins.

The next phase should not start merely because a model is available.

## 10. User Approval Requirement

The user is the final decision-maker.

No phase is locked without user approval.

The user may:

1. Approve.
2. Reject.
3. Approve with edits.
4. Defer.
5. Request another review.
6. Reopen an earlier decision.
7. Override model recommendations.
8. Change the process.

User approval should be explicit.

Recommended approval language:

Approved: lock this phase and proceed to the next defined round.

Recommended rejection language:

Rejected: do not lock this phase. Return to cleanup or regeneration.

Recommended conditional approval language:

Approved with the following required edits before lock.

A user decision should record:

1. What was approved.
2. What was rejected.
3. What remains blocked.
4. What happens next.
5. Whether canonical state should update.
6. Whether phase lock is authorized.

The user should not be forced to decide implementation details too early.

If the models identify decisions that are not yet needed, GPT-5.5 should defer them to the appropriate phase.

If the user feels disoriented, the process should pause and re-establish:

1. Current phase.
2. Locked artifacts.
3. Open artifacts.
4. Blockers.
5. Next action.
6. User decision needed.

## 11. Definition of Phase Lock

A phase lock is the explicit state where a phase artifact becomes canonical and the project is allowed to rely on it.

A phase lock means:

1. The required phase artifact exists.
2. The artifact was reviewed.
3. Blocking critiques were resolved.
4. The user approved the artifact.
5. The canonical state was updated.
6. Future phases may depend on the artifact.
7. Changes to the artifact now require an explicit amendment process.

A phase lock does not mean:

1. The entire project is complete.
2. All future questions are resolved.
3. Implementation may automatically begin.
4. The next phase is already approved.
5. The locked artifact can never change.
6. The process should stop checking for drift.

Locked artifacts should be treated as authoritative until amended.

If a later phase reveals a defect in a locked artifact, the project may amend it, but the amendment must be explicit.

An amendment should record:

1. Which locked artifact changed.
2. Why it changed.
3. Which phase discovered the issue.
4. Which models reviewed the change.
5. What downstream prompts or code are affected.
6. User approval for the amendment.

Phase lock is a governance mechanism, not a claim of perfection.

## 12. What Gets Recorded in Canonical State

Canonical state should record only durable project truth.

Canonical state may include:

1. Project name.
2. Former project name.
3. Current phase.
4. Locked artifacts.
5. Accepted decisions.
6. Hard decisions.
7. Open prerequisites.
8. Active blockers.
9. User-approved phase locks.
10. Model-routing decisions.
11. Public-facing language rules.
12. Architecture amendments.
13. Next action.

Canonical state should not include:

1. Unreviewed model speculation.
2. Raw model chatter.
3. Full commentary that belongs in response records.
4. Temporary implementation logs.
5. Stale prompt drafts.
6. Private project names in public-facing sections.
7. Unapproved assumptions as if they were decisions.
8. Large generated artifacts unless RoundTable's storage model requires embedded canonical text.

RoundTable should distinguish between:

1. Canonical state.
2. Canonical documents.
3. Model responses.
4. Raw notes.
5. Imported legacy references.
6. Phase history.
7. Open issues.
8. Decisions.

For StoryTime, canonical document tracking should include:

1. `docs/product-charter.md`
2. `docs/architecture-baseline.md`
3. `docs/phase-closure-protocol.md`
4. `docs/open-issues.md`
5. `docs/telemetry-map.md`, when created.
6. `docs/phase-history.md`, when created.

Each locked document should record:

1. Document name.
2. Phase.
3. Lock status.
4. Lock date.
5. Reviewer summary.
6. User approval.
7. Any caveats.
8. Any accepted assumptions.

## 13. What Blocks Phase Advancement

Phase advancement is blocked when any of the following are true:

1. Required phase artifact is missing.
2. Required phase artifact is incomplete.
3. Required phase artifact is only summarized.
4. Required phase artifact has not been reviewed.
5. Gemini identifies a blocker.
6. GPT-5.5 identifies unresolved architecture drift.
7. Opus identifies a hard engineering blocker.
8. Required tests fail.
9. Acceptance criteria are not met.
10. The user has not approved lock.
11. Canonical state has not been updated.
12. A hard decision is missing or contradicted.
13. Public-facing language rules are violated.
14. Implementation exceeds the phase scope.
15. A model resolves an open question without authorization.
16. The phase depends on a decision the user has not made.
17. Source-of-truth status is ambiguous.
18. The next phase would build on unverified work.

Phase advancement may also be blocked by user workflow concerns.

If the user reports that process context is broken, that they cannot find the source of truth, or that RoundTable is no longer native to the workflow, the process should pause and repair state before advancing.

A clean process is part of the product.
