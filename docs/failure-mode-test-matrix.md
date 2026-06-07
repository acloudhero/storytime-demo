# Failure-Mode Test Matrix — Phase 11C

This matrix maps each risky failure / regression path in
`regression-risk-register.md` to the specific tests and validation gates that
protect it. A reviewer can use it to see, for any risky path, exactly what
would break if the behaviour regressed. It is a Phase 11C — Failure-Mode /
Regression Hardening deliverable and describes existing coverage.

Test names below are stable identifiers in the repository's `tests/` tree.
Where a whole module protects a path, the module is named without enumerating
every test in it.

## Risk-to-coverage map

| Risk | Risky path | Protecting tests / gates |
|------|------------|--------------------------|
| R1 | Failure queue selection and read-only nature | `tests/test_operator_queue.py` — the queue surfaces failed / blocked / needs-review / awaiting-approval runs, omits healthy runs, and exposes no mutation path |
| R2 | Re-run cannot bypass governance or corrupt state | `tests/test_operator_rerun.py` — `test_governance_blocked_run_is_rejected`, `test_needs_review_envelope_is_rejected`, `test_missing_trust_envelope_is_rejected`, `test_operator_rejected_run_is_rejected`, `test_dry_run_does_not_mutate_state`, `test_actual_rerun_mutates_only_bounded_state`, `test_actual_rerun_writes_one_audit_event`, `test_cli_rerun_rejects_governance_blocked_run` |
| R3 | Raw `blocked_reason` redaction in the static report | `tests/test_operator_report.py` — `test_raw_blocked_reason_never_rendered`, `test_report_generates_for_a_governance_blocked_run` |
| R4 | Static report stays air-gapped, non-interactive, read-only | `tests/test_operator_report.py` — `test_report_has_no_external_cdn_fonts_scripts_or_assets`, `test_report_contains_no_javascript`, `test_report_html_does_not_contain_forms_or_mutation_controls`, `test_rerun_commands_are_plain_text_not_buttons`, `test_report_generation_does_not_mutate_state` |
| R5 | Demo fixtures stay small, text-based, local-first | `tests/test_demo_fixtures.py` — `test_demo_directory_holds_only_small_text_files`, `test_no_runtime_database_or_cache_under_demo`, `test_demo_manifests_carry_no_raw_secrets_or_credentials`, `test_seed_manifests_validate_against_the_closed_schema` |
| R6 | Legal-hallucination gate keeps detecting forbidden vocabulary | `tests/test_legal_hallucination_gate.py` — `test_repository_has_no_forbidden_legal_certification_vocabulary`, `test_forbidden_set_covers_the_section_24_14_minimum`, `test_gate_detects_an_introduced_violation` |
| R7 | Operator-facing failure messages do not expose internals | `tests/test_operator_report.py` — `test_report_no_raw_exception_tracebacks`; `tests/test_operator_rerun.py` — `test_output_does_not_expose_raw_error_message`, `test_json_output_is_allowlisted` |
| R8 | State preservation around failed / re-run runs | run level: `tests/test_operator_rerun.py`, `tests/test_state_store.py`, `tests/test_rehydration.py`; documentation level: `tests/test_failure_mode_regression.py` (added in Phase 11C) |
| R9 | Traceability of blocked / failed / retried stages | `tests/test_operator_queue.py`, `tests/test_operator_report.py`, `tests/test_runner.py`, `tests/test_rehydration.py` |

## Validation gates

The six Docker-free validation gates run on every release-candidate phase and
back the matrix above. A regression in a risky path typically shows up as a
failing gate before it reaches a reviewer:

| Gate | Command | What it protects |
|------|---------|------------------|
| Tests | `uv run pytest -q` | Every test in the matrix above |
| Lint | `uv run ruff check .` | Style and a class of latent bugs |
| Types | `uv run mypy` | Type-contract regressions across the source tree |
| Import contracts | `uv run lint-imports` | The locked module-boundary contracts |
| Environment | `uv run storytime doctor` | The local toolchain prerequisites |
| Legal-hallucination | run inside `uv run pytest -q` as `tests/test_legal_hallucination_gate.py` | R6 — no forbidden-vocabulary claims anywhere in the tree |

## Coverage gaps and their status

The matrix is deliberately honest about what is *not* directly test-covered:

- **R7 — full breadth of CLI error strings.** The rendered report and the
  re-run JSON output are test-covered. The general property that *every*
  operator-facing message across *every* command is bounded is documented in
  `operator-failure-response.md` and protected by review, because it is a
  construction convention spread across commands rather than one code path.
- **R8 — documentation-level state discipline.** Before Phase 11C this was
  documented-only. Phase 11C adds `tests/test_failure_mode_regression.py`,
  which asserts that the State Preservation Bundle keeps Phase 11C marked as a
  pending-review implementation candidate, keeps Phase 11B as the last locked
  phase, does not claim Phase 11D or Phase 12 has started or locked, and still
  retains the append-only historical lock records. This closes the gap.

No risky path in the register is both uncovered and unexplained. Paths that
are documented-only rather than test-covered are named as such here and in the
register, with the reason.

## What Phase 11C added to the matrix

Phase 11C added one test module — `tests/test_failure_mode_regression.py` —
covering R8's documentation-level state discipline. It made no source change,
so the behaviour every other row protects is unchanged from the Phase 11B
baseline; the matrix simply now records that coverage explicitly in one place.
