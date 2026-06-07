# StoryTime — Fresh Clone Troubleshooting

The likely failures a reviewer or operator hits when setting up StoryTime from
a fresh clone, and the safe response to each. This is a Phase 11B — Fresh
Clone / Operator Reproducibility — surface. It documents problems; it changes
no behaviour and adds no product feature.

The guiding principle, from `docs/fresh-clone-checklist.md`: if a step's result
differs from what the documentation says, that is a **release-candidate
finding** — record it, do not silently work around it. This document exists so
the common findings already have a known, safe answer.

Read `LLM_DIRECTOR.md` first; `docs/handoff-state.md` is the authoritative
current-status snapshot. The happy-path setup is in
`docs/local-setup-runbook.md`; the verification path is in
`docs/operator-reproducibility-checklist.md`.

## Before troubleshooting: confirm the baseline

Most "it does not work" reports trace back to one of three environment facts.
Check these first:

1. **You are at the repository root** — the directory with `pyproject.toml`,
   `README.md`, and `LLM_DIRECTOR.md`. `uv` commands resolve the project from
   the working directory.
2. **`uv` is installed and on `PATH`** — `uv --version` prints a version.
3. **Python ≥ 3.11 is available** — `uv` selects the interpreter; 3.12 is the
   developed-and-tested version.

`uv run storytime doctor` summarises the environment and is the fastest single
check. It is read-only and safe to run at any time.

## `uv` is not installed

**Symptom:** `uv: command not found`, or your shell cannot find `uv` after
installing it.

**Why:** `uv` is the environment and dependency manager for the whole project;
nothing in the documented path runs without it. A just-installed `uv` may not
be on `PATH` in the current shell.

**Safe response:** install `uv` from https://docs.astral.sh/uv/, then open a
new shell (or re-source your shell profile) so the updated `PATH` takes effect.
Confirm with `uv --version`. Do not substitute a hand-rolled `pip install` into
a system Python — the project is validated against the `uv`-managed
environment and the committed `uv.lock`.

## Wrong Python version

**Symptom:** `uv sync` reports it cannot find a compatible interpreter, or
`storytime doctor` reports the Python version as below the minimum.

**Why:** `pyproject.toml` sets `requires-python = ">=3.11"`. An older
interpreter is rejected by design.

**Safe response:** install Python 3.11 or newer (3.12 recommended). `uv` can
manage interpreters for you (`uv python install`), or it will use a compatible
one already on the system. Re-run `uv sync --frozen --extra dev`, then
`uv run storytime doctor` to confirm the version line reads `ok`.

## Virtual-environment confusion

**Symptom:** imports fail, `storytime` is "not found", or commands seem to use
the wrong packages — often after manually activating or creating a different
virtual environment.

**Why:** `uv sync` creates and manages the project's `.venv`. `uv run`
executes inside that environment automatically. Mixing in a separately
activated venv, a global interpreter, or a stale `.venv` from another project
layout causes the resolved packages to disagree with `uv.lock`.

**Safe response:** prefer `uv run <command>` for every project command — it
does not need a manually activated environment. If the environment looks
inconsistent, delete `.venv` and re-run `uv sync --frozen --extra dev` to
rebuild it cleanly from the lockfile. `.venv` is git-ignored runtime state, so
removing it is safe and loses nothing from the source tree.

## `uv sync` wants to change the lockfile

**Symptom:** `uv sync` (without `--frozen`) re-resolves dependencies, or
`uv sync --frozen` fails reporting the lockfile is out of date.

**Why:** the release-candidate path uses `uv sync --frozen --extra dev` on
purpose — `--frozen` installs exactly what `uv.lock` pins and fails rather than
silently re-resolving. A plain `uv sync` is allowed to re-resolve and can
modify `uv.lock`.

**Safe response:** always use `uv sync --frozen --extra dev` for setup and
validation, as `docs/rc-validation-checklist.md` prescribes. If `--frozen`
itself fails, do **not** drop the flag to "make it work" and do **not** commit
a regenerated `uv.lock` — a lockfile change is a release-candidate matter that
must follow the dependency policy in `docs/release-candidate-hardening.md` and
be recorded in `docs/verification-log.md`. Note that `make sync` is a developer
convenience that runs a plain `uv sync --extra dev`; the canonical,
reproducible form is the explicit `uv sync --frozen --extra dev`.

## `ffmpeg` is missing

**Symptom:** `storytime doctor` reports `ffmpeg` as not found; or a pipeline
run fails at the assemble stage with an `ffmpeg`-unavailable error.

**Why:** `ffmpeg` encodes the MP3 episode at the assemble stage. It is
**optional** — the six quality gates and the whole test suite pass without it,
and `doctor` reports a missing `ffmpeg` without marking the environment
unhealthy.

**Safe response:** if you only want to validate the repository (the six gates)
or verify fixture integrity, you do not need `ffmpeg` — proceed. If you want to
run a scenario through to a finished episode, install `ffmpeg` and confirm
`storytime doctor` reports it found. Note that the demo's retryable-failure
scenario *deliberately* runs with `ffmpeg` absent to produce a genuine stage
failure — see `docs/demo-reproducibility-checklist.md`.

## Missing optional local services

**Symptom:** the observability stack, Grafana dashboards, or the containerized
blue/green path do not come up.

**Why:** those are **optional** and Docker-based. They are not part of setup,
not part of the six quality gates, and not needed for the demo fixtures.

**Safe response:** for a fresh-clone reproducibility check, skip them — the
documented validation and demo paths are Docker-free and local-first. The
optional stacks have their own runbooks (`docs/observability-demo.md`,
`docs/deployment-containerized.md`); a problem there is not a fresh-clone
blocker.

## Stale cache artifacts

**Symptom:** tests or type checks behave inconsistently between runs, or stale
results appear after switching branches or artifacts.

**Why:** `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.import_linter_cache`,
and `__pycache__` directories are local tooling caches. They are git-ignored
and never belong in a release archive, but a stale cache can occasionally
confuse a local run.

**Safe response:** run `make clean` (it removes `.pytest_cache`,
`.mypy_cache`, and `.ruff_cache`), or delete the cache directories by hand,
then re-run the gates. Removing caches is always safe — they are regenerated on
the next run.

## Permission issues

**Symptom:** a command cannot create `.venv`, `runs/`, `feed/`,
`operator-report/`, or `logs/`; or a file under one of those directories is not
writable.

**Why:** StoryTime writes runtime state under the repository directory. If the
checkout lives somewhere the current user cannot write — or if a directory was
created by a different user (for example, Docker creating `./logs` as root) —
writes fail.

**Safe response:** check out or unpack the repository somewhere the current
user owns, and ensure the user owns the runtime-output directories. The
`Makefile` `logs-dir` target intentionally creates `./logs` as the current
user before the optional observability stack runs, precisely to avoid a
root-owned `./logs`. If a runtime directory is already owned by the wrong user,
remove it (it is git-ignored runtime state) and let StoryTime recreate it.

## `storytime doctor` reports a problem

**Symptom:** `doctor` does not end with `environment: healthy`.

**Why:** `doctor` checks the Python version, SQLite availability and WAL
journal mode, optional OpenTelemetry import, and optional `ffmpeg`. A genuine
problem is almost always the Python version (see above) or SQLite.

**Safe response:** read which line is not `ok`. A missing optional dependency
(`opentelemetry`, `ffmpeg`) is reported but does **not** make the environment
unhealthy — that is expected. A failing **required** check (Python version,
SQLite) is a real blocker: fix that specific item and re-run `doctor`. Do not
proceed to a demo run while a required check fails.

## A test fails after a local mutation

**Symptom:** the suite was green, you ran a pipeline command, and now a test
fails.

**Why:** running the pipeline writes runtime state under `runs/` (including
`runs/state.db`) and `feed/`. A test that does not isolate itself from a
pre-existing local state database can be perturbed by leftover runtime data.

**Safe response:** the suite is designed to pass from a clean state. Reset the
local runtime output — delete `runs/`, `feed/`, `operator-report/`, and
`logs/` — and re-run `uv run pytest -q`. Those directories are git-ignored
runtime output; deleting them resets local state and leaves the `src/` tree,
`demo/` fixtures, and `config/` untouched. If the suite still fails from a
genuinely clean tree, that is a release-candidate finding — record it in
`docs/verification-log.md` rather than working around it.

## When a finding is real

If, after the safe response above, a step still does not reproduce the result
documented in `docs/operator-reproducibility-checklist.md` or
`docs/rc-validation-checklist.md`, do not paper over it:

- Record the exact command, the expected result, and the actual result.
- Add it to `docs/verification-log.md` as a Phase 11-series finding.
- If it points at a dependency or lockfile problem, follow the dependency
  policy in `docs/release-candidate-hardening.md` — do not edit
  `pyproject.toml` or `uv.lock` casually to silence it.
- A genuine setup/reproducibility blocker is in scope for Phase 11B to
  document and, if it is a true blocker, for a scoped fix; a deeper
  failure-mode investigation is Phase 11C work.

## Related documents

- `docs/fresh-clone-checklist.md` — the fresh-clone setup path at a glance.
- `docs/local-setup-runbook.md` — the step-by-step setup runbook.
- `docs/operator-reproducibility-checklist.md` — the step-by-step verification
  path, with the Phase 11B reference results.
- `docs/rc-validation-checklist.md` — the six canonical validation gates.
- `docs/release-candidate-hardening.md` — the hardening baseline overview and
  the dependency policy.
- `docs/known-limitations.md` — StoryTime's documented boundaries and non-goals.
