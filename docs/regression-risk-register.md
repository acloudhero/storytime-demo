# Regression Risk Register — Phase 11C

This register inventories the highest-risk failure and regression paths that
already exist in StoryTime and records, for each one, what could go wrong and
how well it is currently protected. It is a Phase 11C — Failure-Mode /
Regression Hardening deliverable. It describes existing behaviour; it does not
propose new behaviour.

Each entry has a **status**:

- **Test-covered** — an automated test or validation gate fails if the
  behaviour regresses. See `failure-mode-test-matrix.md` for the exact tests.
- **Documented-only** — the behaviour is correct and described, but is
  protected by review and documentation rather than by a dedicated test,
  usually because it is a property of how a component is used rather than a
  single code path.
- **Deferred** — verification or evidence work that deliberately belongs to a
  later phase, with the destination named.

## R1 — Failure queue surfaces the wrong runs, or stops being read-only

**Risk.** The operator failure / review queue (`storytime queue`) could begin
to omit runs that need attention, surface healthy runs as if they needed
attention, or — most seriously — gain a mutation path and stop being a
read-only view.

**Existing behaviour.** The queue is a semantic, read-only query over the
SQLite state of truth. It surfaces runs that are failed, blocked by
governance, marked needs-review, or awaiting an operator approval decision,
and for each one names an existing command to look at next. It never pops,
claims, acknowledges, or mutates anything.

**Status:** Test-covered. The queue's selection logic and its read-only
nature are exercised by the operator-queue tests.

## R2 — A re-run corrupts prior state or bypasses governance

**Risk.** `storytime rerun` is an explicit operator mutation. A regression
could let it re-run a run that should not be retried — for example a
governance-blocked run, a needs-review run, an operator-rejected run, or a run
with no Trust Envelope — or let it overwrite prior decisions or audit history.

**Existing behaviour.** Re-run eligibility is evaluated by a pure decision
function before anything is written. A run is eligible only if it exists,
failed because of a genuine stage failure, and carries an `APPROVED` Trust
Envelope. A `BLOCKED`, `NEEDS_REVIEW`, denied, or missing envelope, and an
operator-rejected run, are all rejected with a distinct, stable reason code. A
`--dry-run` invocation changes nothing. An applied re-run resets only the
bounded run status to the resumable state and writes exactly one
`RUN_RERUN_REQUESTED` audit event; it does not erase prior decisions.

**Status:** Test-covered. The rerun decision function and CLI are exercised
for each rejection reason and for the bounded, audited apply path.

## R3 — Raw governance `blocked_reason` leaks into a shareable report

**Risk.** A governance-blocked run carries a raw `blocked_reason` string. If
it reached the static HTML operator report, a shareable artifact would expose
internal governance detail.

**Existing behaviour.** The report renderer applies the Architecture Baseline
redaction rule: when a run is blocked it emits exactly one bounded sentence —
`Decision detail: blocked by governance policy; inspect Trust Envelope locally
if authorized.` — and never the raw reason. The raw reason remains available
to the local authorized operator through the CLI, which is the intended
local-inspection model; the redaction requirement is specific to the
shareable HTML artifact, not the local CLI.

**Status:** Test-covered. The operator-report tests assert both that the raw
reason is absent from every generated page and that the safe sentence is
present on the blocked run's detail page.

## R4 — The static report becomes interactive or fetches external assets

**Risk.** The operator report is designed to be a local, air-gapped, read-only
artifact. A regression could introduce a `<script>` tag, an external CDN or
font reference, a form, or a mutation control, turning a safe static document
into something that executes code or calls out over the network.

**Existing behaviour.** Every generated page is self-contained: styling is an
embedded block, there are no script tags, no `http://` or `https://` asset
references, no forms, and no buttons that mutate state. Re-run instructions
appear as plain-text commands, not as actionable controls. Report generation
itself never mutates state.

**Status:** Test-covered. The operator-report tests assert the absence of
scripts, external assets, forms, and mutation controls, and assert that
generation does not mutate state.

## R5 — Demo fixtures gain binary, generated, or secret content

**Risk.** The demo seed data and fixtures are meant to be small, text-based,
deterministic, and local-first. A regression could add generated audio, a
binary stub, a runtime database, or an embedded secret, making the demo unsafe
to ship or non-deterministic.

**Existing behaviour.** The `demo/` tree holds only small text files: JSON
seed manifests, plain-text sources, and YAML fixture definitions. The seed
manifests validate against the closed source-manifest schema, their declared
text digests are correct, scenario ids are stable and unique, and there is no
runtime database, cache, generated audio, or credential under `demo/`.

**Status:** Test-covered. The demo-fixture tests assert the directory holds
only small text files, carries no runtime database or cache, and contains no
raw secrets.

## R6 — The legal-hallucination gate stops detecting forbidden vocabulary

**Risk.** The static legal-hallucination gate exists so StoryTime never
*claims* a legal determination or an AI rights determination. A regression
could weaken the forbidden set, break the scanner, or let a new document
introduce forbidden vocabulary.

**Existing behaviour.** A pure-Python scanner walks the repository, reads only
text files, prunes generated directories, and reports any occurrence of the
forbidden-vocabulary set outside an allowlist of governance documents that
legitimately define the set. It returns zero violations on the current tree,
including the documents Phase 11C adds.

**Status:** Test-covered. The legal-hallucination gate tests assert a clean
repository, a forbidden set that covers the Architecture Baseline minimum, and
that an introduced violation is still detected.

## R7 — Operator-facing failure messages expose internals

**Risk.** When a stage fails or a re-run is rejected, the operator sees a
message. A regression could let an unbounded exception message, a raw stack
trace, or a raw error string reach an operator-facing surface.

**Existing behaviour.** Failure and rejection messages are bounded, structured
strings. The re-run JSON output is an allowlisted set of fields and does not
expose the raw underlying error message. The static report shows a coarse
failure category, not a raw traceback.

**Status:** Test-covered for the rendered report and the re-run JSON output.
The breadth of every possible CLI error string is **documented-only**: it is a
property of how bounded messages are constructed across commands rather than a
single code path, and is described in `operator-failure-response.md`.

## R8 — State preservation around a failed or re-run run drifts

**Risk.** A failed run, and a run that has been re-run, must leave a coherent,
inspectable trail: the failure recorded, the governance decision intact, the
audit events appended, and the State Preservation Bundle still accurate.

**Existing behaviour.** A failed run keeps its recorded failure, its Trust
Envelope, and its stage history; a re-run appends an audit event rather than
rewriting history. The State Preservation Bundle (the living docs) records the
current phase, the last locked phase, and the artifact lineage, and is
synchronized at the end of each phase.

**Status:** Mixed. Run-level state preservation is **test-covered** by the
rerun, state-store, and rehydration tests. **Documentation-level** state
discipline — that the Bundle keeps the current phase honest and does not claim
a future phase has started or locked — was previously documented-only and is
**now test-covered** by `tests/test_failure_mode_regression.py`, added in
Phase 11C.

## R9 — Traceability of blocked / failed / retried stages weakens

**Risk.** An operator must be able to follow a run from a blocked, failed, or
retried stage to the reason and the next action. A regression could break the
link between a stage outcome and its explanation.

**Existing behaviour.** Each stage outcome is recorded with a structured
status and, for failures, a structured error category; the queue and the
report turn those structured fields into a "why" and a "what to look at next"
without exposing raw internals. Re-run history is traceable through the
appended audit event.

**Status:** Test-covered indirectly through the queue, report, runner, and
rehydration tests, each of which asserts that structured stage outcomes are
preserved and surfaced. No regression in this area is currently uncovered.

## Deferred items — Phase 11D release evidence pack

The following are not Phase 11C work. They are recorded here so they are not
lost, and they belong to **Phase 11D — Release Candidate Evidence Pack**:

- assembling a single reviewer-facing evidence bundle that collects the gate
  results, the test matrix, and the risk register into one release-candidate
  sign-off document;
- capturing a worked, end-to-end failure-and-recovery transcript as evidence
  rather than as a runbook;
- any release-candidate sign-off checklist that depends on having all of
  Phase 11A–11C locked.

The following are **post-release / future cloud-native phase** concerns and
are explicitly not release-candidate blockers: multi-user authentication,
cloud deployment and image registries, and any live or real-time operator UI.
These are already recorded as deliberate non-goals in `known-limitations.md`.
