# StoryTime — Local Setup Runbook

A step-by-step runbook for setting up StoryTime on a local machine, from a
fresh clone to a verified, ready-to-use environment. It is written for a
reviewer, an operator, or a cold LLM session that needs the repository running.

StoryTime is **local-first**: every step here runs on one machine, needs no
cloud account, and makes no authenticated network calls. The only network
access in the whole setup is the package download that `uv sync` performs, and
the only optional Docker use is the observability stack and the optional
containerized blue/green path — neither is needed to set up or validate the
project.

For the condensed version of this path see `docs/fresh-clone-checklist.md`.

## Prerequisites

| Tool | Requirement | Notes |
|------|-------------|-------|
| Python | ≥ 3.11 | Developed and tested on 3.12. |
| uv | current release | Environment and dependency manager — see https://docs.astral.sh/uv/. |
| ffmpeg | optional | Needed only when a pipeline run reaches the assemble stage (MP3 encoding). `storytime doctor` reports whether it is found. The six quality gates do not need it. |
| Docker | optional | Only for the optional observability stack and the optional containerized blue/green path. Not needed for setup or validation. |

## Step 1 — Obtain the repository

Clone or extract the repository and change into its root directory (the
directory containing `pyproject.toml`, `README.md`, and `LLM_DIRECTOR.md`).

## Step 2 — Install dependencies

```bash
uv sync --frozen --extra dev
```

This creates `.venv`, installs the runtime and dev dependencies exactly as
pinned by `uv.lock`, and installs `storytime` as an editable package. The
`--frozen` flag means the install uses the committed lockfile and never
silently re-resolves — that is the intended release-candidate behaviour.

## Step 3 — Check the environment

```bash
uv run storytime doctor
```

Expect an `environment: healthy` summary. `doctor` reports the Python version,
SQLite availability and WAL journal mode, whether OpenTelemetry is importable
(optional), and whether `ffmpeg` is on `PATH` (optional). A missing `ffmpeg` is
reported but does not make the environment unhealthy.

## Step 4 — Run the validation gates

Run the six Docker-free quality gates to confirm a known-good state:

```bash
uv sync --frozen --extra dev
uv run pytest -q
uv run ruff check .
uv run mypy
uv run lint-imports
uv run storytime doctor
```

See `docs/rc-validation-checklist.md` for the expected result of each gate.
At the Phase 11A baseline the suite is **549 passing**, ruff and mypy are
clean, and the two import contracts are kept. Phase 11B re-ran all six gates
from a fresh extraction and confirmed this result reproduces exactly.

## Step 5 — Locate the demo fixtures

The demo seed data and golden-path fixtures live in `demo/`:

- `demo/seed/` — four original CC0 demo seed texts plus schema-valid manifests.
- `demo/fixtures/` — six golden-path fixture definitions plus an index.
- `demo/governance/demo-blocked-sources.yaml` — a demo-only blocked-source
  deny-list, supplied per run through `STORYTIME_BLOCKED_SOURCES`.

`docs/demo.md` is the operator demo runbook; `docs/demo-script.md` is the
narrated presentation version; `docs/demo-reproducibility-checklist.md`
explains how to verify the fixtures without generated audio or external APIs.

## Step 6 — Understand the expected outputs

Running StoryTime produces **runtime output** that is never source-controlled:

- `runs/` — per-run working directories and the SQLite state database
  (`runs/state.db`). The source of truth for run state.
- `feed/` — published RSS feed and audio.
- `operator-report/` — the generated static HTML operator report
  (`storytime report generate`).
- `logs/` — structured demo logs, when the observability demo is used.

All four are git-ignored. Deleting them resets local state; the source tree,
`demo/` fixtures, and `config/` are unaffected. None of these directories
belongs in a release archive — see `docs/release-candidate-hardening.md`.

## First commands to try

```bash
uv run storytime version
uv run storytime --help
uv run storytime validate-manifest demo/seed/demo-golden-path.json
uv run storytime run -m demo/seed/demo-golden-path.json --auto-approve
uv run storytime status
uv run storytime report generate    # then open operator-report/index.html
```

`docs/command-reference.md` describes every command, including which commands
are read-only and which change state.

## Environment configuration (optional)

StoryTime reads a small set of environment variables with safe defaults; no
configuration is required for the default local setup. `.env.example` is the
template — copy it to `.env` (git-ignored) only if you want to override a
default. No value in `.env.example` is a secret. See
`docs/security-secrets-checklist.md` for the secrets posture.

## Related documents

- `docs/fresh-clone-checklist.md` — this path condensed to a checklist.
- `docs/operator-reproducibility-checklist.md` — the step-by-step verification
  path, with the reference results Phase 11B observed walking it.
- `docs/fresh-clone-troubleshooting.md` — common fresh-clone setup failures
  and their safe responses.
- `docs/rc-validation-checklist.md` — the validation gates in detail.
- `docs/demo-reproducibility-checklist.md` — reproducing the demo fixtures.
- `docs/security-secrets-checklist.md` — the security and secrets baseline.
- `README.md` — project overview and the full command surface.
