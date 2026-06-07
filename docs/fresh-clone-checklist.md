# StoryTime — Fresh Clone Checklist

The fast path: what to do, in order, to go from a fresh clone of StoryTime to a
verified working environment. Each step links to fuller detail. For the
step-by-step runbook see `docs/local-setup-runbook.md`.

This checklist is a release-candidate hardening surface, established in
Phase 11A and verified in Phase 11B. It exists so a fresh clone, a cold LLM
session, or a demo operator never has to guess the setup path. Phase 11B walked
this path from a clean extraction and confirmed every step below reproduces;
the step-by-step verification record is in
`docs/operator-reproducibility-checklist.md`.

## Before you start

- [ ] Python ≥ 3.11 is installed (3.12 recommended).
- [ ] `uv` is installed (https://docs.astral.sh/uv/).
- [ ] You are at the repository root — the directory with `pyproject.toml`,
      `README.md`, and `LLM_DIRECTOR.md`.
- [ ] `ffmpeg` is installed *if* you intend to run the pipeline to completion
      (the assemble stage encodes MP3). It is **not** needed for setup or for
      the six quality gates.

## Setup

- [ ] `uv sync --frozen --extra dev` — installs runtime + dev dependencies from
      the committed `uv.lock`, creates `.venv`, installs `storytime` editable.
- [ ] `uv run storytime doctor` — expect `environment: healthy`.

## Validate

Run the six Docker-free quality gates (`docs/rc-validation-checklist.md`):

- [ ] `uv sync --frozen --extra dev` — clean, lockfile unchanged.
- [ ] `uv run pytest -q` — full suite passes (**549 passing** at the Phase 11A
      baseline, re-confirmed by Phase 11B; fully offline).
- [ ] `uv run ruff check .` — `All checks passed!`
- [ ] `uv run mypy` — `Success: no issues found in 85 source files`.
- [ ] `uv run lint-imports` — `Contracts: 2 kept, 0 broken`.
- [ ] `uv run storytime doctor` — `environment: healthy`.

## Orient

- [ ] Read `LLM_DIRECTOR.md` first, then `docs/handoff-state.md` — the
      authoritative current-status snapshot.
- [ ] Skim `README.md` for the project overview and full command surface.
- [ ] Locate the demo fixtures in `demo/` (`docs/demo.md` is the runbook).
- [ ] Note the runtime output directories (`runs/`, `feed/`,
      `operator-report/`, `logs/`) — all git-ignored, none belong in a release
      archive.

## First commands to try

- [ ] `uv run storytime version`
- [ ] `uv run storytime --help`
- [ ] `uv run storytime validate-manifest demo/seed/demo-golden-path.json`
- [ ] `uv run storytime run -m demo/seed/demo-golden-path.json --auto-approve`
- [ ] `uv run storytime report generate` — then open
      `operator-report/index.html` in a browser (no server required).

## What you should not need

- [ ] No cloud account, API key, or credential — StoryTime is local-first and
      makes no authenticated network calls.
- [ ] No Docker — the six gates and the whole test suite are Docker-free.
      Docker is only for the optional observability stack and the optional
      containerized blue/green path.
- [ ] No `.env` file — `.env.example` is a template; the defaults work as-is.

## If something does not match

If a step's result differs from what is documented here or in
`docs/rc-validation-checklist.md`, treat it as a release-candidate finding:
record it rather than working around it silently.
`docs/fresh-clone-troubleshooting.md` lists the common fresh-clone setup
failures and the safe response to each, and
`docs/operator-reproducibility-checklist.md` pairs each step with the result
Phase 11B observed so you can compare against a known-good reference.
Phase 11B — Fresh Clone / Operator Reproducibility — verified this path; see
`docs/phase11-plan.md` for the Phase 11 decomposition.
