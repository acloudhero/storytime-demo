# StoryTime — Release Candidate Validation Checklist

The canonical validation commands for StoryTime, the order to run them in, and
what a healthy result looks like. This is the checklist a reviewer or an
implementer runs to confirm the repository is in a known-good state.

All six gates are **Docker-free** and run offline. They require no cloud
account, no external API, and no network access. This is a release-candidate
invariant — it must stay true.

## The six quality gates

Run these from the repository root, in order:

```bash
uv sync --frozen --extra dev
uv run pytest -q
uv run ruff check .
uv run mypy
uv run lint-imports
uv run storytime doctor
```

`make check` wraps the lint, typecheck, imports, and test gates as one target;
`make sync` and `make run-doctor` cover the other two. The explicit `uv run`
commands above are the canonical form and are what this checklist refers to.

## Expected results

| # | Command | Expected result |
|---|---------|-----------------|
| 1 | `uv sync --frozen --extra dev` | Resolves and installs from the committed `uv.lock` without modifying it; creates `.venv`; installs `storytime` as an editable package. |
| 2 | `uv run pytest -q` | The full suite passes — **549 passed** at the Phase 11A/11B baseline; **580 passed** after Phase 11C added `tests/test_failure_mode_regression.py` (31 tests). The suite is fully offline. |
| 3 | `uv run ruff check .` | `All checks passed!` |
| 4 | `uv run mypy` | `Success: no issues found in 85 source files` (strict mode). |
| 5 | `uv run lint-imports` | `Contracts: 2 kept, 0 broken` — the two ARCH-LOCKed import contracts (OpenTelemetry confined to the telemetry adapter; `events` is a leaf package). |
| 6 | `uv run storytime doctor` | `environment: healthy` — Python ≥ 3.11, SQLite with WAL, optional OpenTelemetry reported as available-or-not, optional `ffmpeg` reported as found-or-not. |

The legal-hallucination verification gate (Architecture Baseline §24.14) runs
**inside** the pytest suite as `tests/test_legal_hallucination_gate.py`: it
scans the repository's code, config, and non-governance docs for forbidden
legal-certification vocabulary and must report zero violations. A green
`pytest` run therefore already includes a clean legal-hallucination scan.

## Notes on the gates

- **`--frozen` is deliberate.** `uv sync --frozen` installs exactly what
  `uv.lock` pins and fails rather than silently re-resolving. A release
  candidate must build from the locked resolution; do not drop `--frozen` to
  "make it work".
- **`ffmpeg` is optional for the gates.** `storytime doctor` reports whether
  `ffmpeg` is present. The six gates and the whole test suite pass without it.
  `ffmpeg` is only needed when a real pipeline run reaches the assemble stage
  (MP3 encoding) — see `docs/demo-reproducibility-checklist.md`.
- **Test count is a baseline, not a contract.** 549 is the Phase 11A baseline,
  re-confirmed unchanged by Phase 11B. Phase 11C added 31 tests in
  `tests/test_failure_mode_regression.py`, making **580** the locked Phase 11C
  baseline; Phase 11D carries that 580 unchanged (it adds no test). A later
  phase that legitimately adds tests will change the number; the gate is "the
  suite passes", not "the suite is exactly 580".
- **Docker is never required.** The optional observability stack and the
  optional containerized blue/green path use Docker, but no quality gate does.
  Do not introduce a Docker dependency into the gate path.

## If a gate fails

Treat a failing gate as a release-candidate blocker. Do not work around it,
and do not edit `pyproject.toml` or `uv.lock` to make a gate pass unless the
failure is itself a genuine lockfile/dependency blocker — in which case follow
the dependency policy in `docs/release-candidate-hardening.md` and record the
before/after rationale in `docs/verification-log.md`.
`docs/fresh-clone-troubleshooting.md` lists the common fresh-clone causes of a
gate not reproducing and the safe response to each.

## Related documents

- `docs/local-setup-runbook.md` — step-by-step environment setup.
- `docs/fresh-clone-checklist.md` — the fresh-clone path at a glance.
- `docs/operator-reproducibility-checklist.md` — the step-by-step verification
  path, with the gate results Phase 11B observed.
- `docs/fresh-clone-troubleshooting.md` — common setup failures and safe
  responses.
- `docs/release-candidate-hardening.md` — the hardening baseline overview.
- `docs/verification-log.md` — the recorded verification evidence per phase.
