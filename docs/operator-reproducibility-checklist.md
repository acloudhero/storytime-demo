# StoryTime — Operator Reproducibility Checklist

The end-to-end path an operator, a reviewer, a hiring manager, or a future LLM
session follows to go from a freshly unpacked StoryTime artifact to a verified,
demonstrable local environment — and to confirm, step by step, that the
repository reproduces the documented state.

This is a Phase 11B — Fresh Clone / Operator Reproducibility — surface. Where
`docs/fresh-clone-checklist.md` is the at-a-glance setup path and
`docs/local-setup-runbook.md` is the step-by-step runbook, this document is the
**verification** view: it pairs each step with the result Phase 11B observed
when it actually walked the path, so a reviewer can compare their own run
against a known-good reference. It adds no product behaviour; it documents and
verifies the path Phase 11A established.

Read `LLM_DIRECTOR.md` first; `docs/handoff-state.md` is the authoritative
current-status snapshot.

## How to use this checklist

Walk the steps in order. Each step states what to do, what success looks like,
and — in the "Phase 11B observed" line — the exact result recorded when
Phase 11B ran this path against the Phase 11A baseline artifact. If your result
matches, the step reproduces. If it does not, treat the difference as a
release-candidate finding: record it rather than working around it silently,
and consult `docs/fresh-clone-troubleshooting.md`.

Nothing in this checklist needs a cloud account, an API key, a credential, or
network access beyond the single package download that `uv sync` performs.

## Step 1 — Clone or unpack the artifact

- [ ] Obtain the repository: clone it, or extract the release tarball.
- [ ] Change into the repository root — the directory that contains
      `pyproject.toml`, `README.md`, and `LLM_DIRECTOR.md`.
- [ ] If you were given an artifact SHA-256, verify it before trusting the
      contents (`sha256sum <artifact>.tar.gz`).

Success looks like: a working directory whose top level holds `pyproject.toml`,
`README.md`, `LLM_DIRECTOR.md`, `Makefile`, `uv.lock`, and the `src/`, `tests/`,
`docs/`, `config/`, `demo/`, and `scripts/` directories.

*Phase 11B observed:* the Phase 11A baseline artifact unpacked to exactly that
layout; the source SHA-256 matched the value recorded for it in
`docs/artifact-manifest.md`.

## Step 2 — Inspect the state documents

- [ ] Read `LLM_DIRECTOR.md` — the first-read instructions, roles, and rules.
- [ ] Read `docs/handoff-state.md` — the authoritative current-status snapshot:
      current phase, last locked phase, next action, what not to replay.
- [ ] Skim `docs/roadmap.md`, `docs/phase-history.md`, and
      `docs/canonical-state.md` for the phase lineage and locked decisions.

Success looks like: the State Preservation Bundle agrees with itself — the
current phase, the last locked phase, and the next action read consistently
across `LLM_DIRECTOR.md`, `docs/handoff-state.md`, and `docs/roadmap.md`.

*Phase 11B observed:* the Bundle was internally consistent. At the Phase 11A
baseline it stated Phase 10 CLOSED, Phase 11A as the implementation candidate,
and Phase 11B/11C/11D not started — with `docs/handoff-state.md` authoritative
for current status, as the Bundle's own rule prescribes.

## Step 3 — Confirm the prerequisites

- [ ] Python ≥ 3.11 is on `PATH` (3.12 is the developed-and-tested version).
- [ ] `uv` is installed — see https://docs.astral.sh/uv/.
- [ ] `ffmpeg` is installed **only if** you intend to run the pipeline through
      the assemble stage (MP3 encoding). It is not needed for setup or for the
      six quality gates. `storytime doctor` reports whether it is found.
- [ ] Docker is **not** required for setup, validation, or the demo fixtures.

*Phase 11B observed:* Python 3.12 and a current `uv` release satisfied every
gate. `ffmpeg` was present and was used only by the optional level-2 scenario
execution; the six gates passed without depending on it.

## Step 4 — Sync dependencies

- [ ] Run `uv sync --frozen --extra dev` from the repository root.

`--frozen` installs exactly what `uv.lock` pins and fails rather than silently
re-resolving — the intended release-candidate behaviour. Success looks like:
`.venv` created, runtime and dev dependencies installed, `storytime` installed
as an editable package, and `uv.lock` left unmodified.

*Phase 11B observed:* `uv sync --frozen --extra dev` resolved and installed
from the committed `uv.lock` without modifying it.

## Step 5 — Run the six quality gates

- [ ] Run the six Docker-free gates from the repository root, in order:

```bash
uv sync --frozen --extra dev
uv run pytest -q
uv run ruff check .
uv run mypy
uv run lint-imports
uv run storytime doctor
```

`docs/rc-validation-checklist.md` is the canonical per-gate detail. Success
looks like every gate green: the suite passes, ruff and mypy are clean, both
import contracts are kept, and `doctor` reports a healthy environment.

*Phase 11B observed:* all six gates passed — the suite reported **549 passed**,
`ruff` reported all checks passed, `mypy` reported no issues in 85 source files
(strict), `lint-imports` reported 2 contracts kept and 0 broken, and
`storytime doctor` reported `environment: healthy`. The static
legal-hallucination gate runs inside the pytest suite and reported zero
violations. The result matched the Phase 11A baseline exactly. See
`docs/verification-log.md` for the recorded Phase 11B gate output.

## Step 6 — Inspect the demo fixture documentation

- [ ] Confirm `demo/` is present and complete: `demo/seed/` (4 seed texts +
      4 manifests), `demo/fixtures/` (6 fixture definitions + `index.yaml`),
      `demo/governance/demo-blocked-sources.yaml`, and `demo/README.md`.
- [ ] Read `docs/demo.md` (the operator demo runbook) and
      `docs/demo-reproducibility-checklist.md` (how to verify the fixtures
      without generated audio or external APIs).

*Phase 11B observed:* `demo/` contained exactly that set of files;
`config/governance/blocked-sources.yaml` shipped empty (`blocked_sources: []`),
so the default local path blocks nothing.

## Step 7 — Run the documented local checks

These are the read-only and local-first commands a reviewer runs to confirm the
operator surfaces work. None needs a cloud account or network access.

- [ ] `uv run storytime version` — prints the version string.
- [ ] `uv run storytime --help` — prints the full command surface.
- [ ] `uv run storytime doctor` — `environment: healthy`.
- [ ] `uv run storytime validate-manifest demo/seed/demo-golden-path.json` —
      reports the manifest valid against the closed schema.
- [ ] `uv run pytest -q tests/test_demo_fixtures.py` — the demo fixture
      integrity tests pass with no pipeline run and no `ffmpeg`.

Optionally, to exercise the full pipeline (this needs `ffmpeg` and writes
git-ignored runtime output under `runs/`, `feed/`, and `operator-report/`):

- [ ] `uv run storytime run -m demo/seed/demo-golden-path.json --auto-approve`
      — the run completes through publish.
- [ ] `uv run storytime status` — lists the completed run.
- [ ] `uv run storytime report generate` — writes the static HTML report; open
      `operator-report/index.html` in a browser, no server required.

*Phase 11B observed:* every command above produced the documented result.
`version` printed `storytime 0.2.0`; `validate-manifest` reported the
golden-path manifest valid; the demo fixture integrity tests passed; and the
optional golden-path run completed through publish, `status` listed it, and
`report generate` wrote the static report directory.

## Step 8 — Confirm archive-hygiene expectations

- [ ] Understand which directories are **runtime output**, not source:
      `runs/` (including `runs/state.db`), `feed/`, `operator-report/`, and
      `logs/`. All four are git-ignored; none belongs in a release archive.
- [ ] If you ran the optional pipeline commands in Step 7, those directories
      now exist locally. Deleting them resets local state; the `src/` tree,
      `demo/` fixtures, and `config/` are unaffected.
- [ ] The full artifact-hygiene exclusion list is in
      `docs/release-candidate-hardening.md`; it is consistent with `.gitignore`
      and `.dockerignore`.

*Phase 11B observed:* the runtime-output directories were created only by the
optional Step 7 pipeline run and are correctly git-ignored. The Phase 11B
output archive excludes them, every tooling cache, `.venv`, `__pycache__`,
generated audio, and nested archives — see `docs/verification-log.md`.

## Step 9 — Confirm no real secrets are required

- [ ] No `.env` file is needed — `.env.example` is a template and the defaults
      work as-is.
- [ ] No cloud account, API key, or credential is required at any step.
- [ ] `config/vendor.secret.env.example` is a placeholder template only; it
      carries no real secret. `docs/security-secrets-checklist.md` is the full
      local-first security and secrets baseline.

*Phase 11B observed:* the whole path above ran with no `.env` file and no
credential of any kind. The only network access was the package download in
Step 4.

## Reproducibility summary

A reviewer who completes Steps 1–9 has confirmed, from a clean checkout, that
StoryTime installs, validates, and runs its documented demo path exactly as the
State Preservation Bundle describes — offline, with no secrets, and with no
generated audio committed to the repository. If any step diverges from the
"Phase 11B observed" reference, `docs/fresh-clone-troubleshooting.md` lists the
likely causes and the safe response.

## What this checklist is not

- It is not a Phase 11C failure-mode / regression exercise — it confirms the
  golden path, not the failure surfaces.
- It is not a Phase 11D release-candidate evidence pack — it verifies
  reproducibility but does not assemble the reviewer-facing sign-off pack.
- It is not a cloud-deployment guide — StoryTime is local-first and no
  cloud-native path is claimed.

## Related documents

- `docs/fresh-clone-checklist.md` — the fresh-clone setup path at a glance.
- `docs/local-setup-runbook.md` — the step-by-step setup runbook.
- `docs/rc-validation-checklist.md` — the six canonical validation gates.
- `docs/fresh-clone-troubleshooting.md` — common setup failures and safe
  responses.
- `docs/demo-reproducibility-checklist.md` — reproducing the demo fixtures.
- `docs/security-secrets-checklist.md` — the local-first security baseline.
- `docs/release-candidate-hardening.md` — the hardening baseline overview.
- `docs/verification-log.md` — the recorded verification evidence per phase.
