# StoryTime — Demo Reproducibility Checklist
<!-- CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md -->
> **Canonical demo path.** For the current, authoritative reviewer/demo
> walkthrough — the system modes and boundaries, the optional loopback
> local bridge, the one controlled retry (acceptance is not success), the
> manual snapshot reload (a read-model refresh, not a live sync), and the
> governed mock-first TTS proof (provider-backed audio remains deferred) —
> see [docs/demo-walkthrough.md](demo-walkthrough.md), the single source of
> truth and evidence map. This document is a secondary/historical narrative;
> where it differs, the canonical walkthrough wins.


How a reviewer verifies StoryTime's demo seed data and golden-path fixtures
**reproducibly**, on one machine, with no generated audio committed to the
repository and no external API. This is a Phase 11A hardening surface: it makes
the demo verification path explicit; it changes no behaviour.

Phase 11B — Fresh Clone / Operator Reproducibility — walked this path from a
clean extraction: it ran the level-1 fixture integrity test and executed the
golden-path scenario through to a completed run, and confirmed both reproduce
as documented below.

The demo fixtures themselves were locked in Phase 10F and explained for
presentation in Phase 10G. This document does not change them — it documents
how to confirm they still hold.

## Two levels of verification

There are two distinct ways to verify the demo, and they need different things:

1. **Fixture integrity** — confirm the seed data and fixture definitions are
   well-formed, schema-valid, and internally consistent. This needs **no
   pipeline run, no `ffmpeg`, and no audio**.
2. **Scenario execution** — actually drive the six demo scenarios through the
   real pipeline. This needs `ffmpeg` for the scenarios that run to completion.

A reviewer who only wants to confirm the demo is sound can stop after level 1.

## Level 1 — Fixture integrity (no audio, no ffmpeg)

The locked Phase 10F test file `tests/test_demo_fixtures.py` checks the seed
manifests, the fixture definitions, and their safety properties. Run it
directly:

```bash
uv run pytest -q tests/test_demo_fixtures.py
```

Expect all fixture tests to pass. This verifies — with no pipeline run — that:

- the four `demo/seed/` manifests are valid against the closed manifest schema;
- the six `demo/fixtures/` definitions and the index are well-formed and
  consistent;
- the demo content stays CC0 / public-domain and carries no forbidden
  vocabulary;
- the demo-only blocked-source deny-list is shaped correctly.

A full `uv run pytest -q` run includes these tests as part of the 549-test
baseline.

## Level 2 — Scenario execution (the six demo scenarios)

`docs/demo.md` is the authoritative operator runbook for executing the
scenarios; `docs/demo-script.md` is the narrated presentation version. The six
scenarios are:

| # | Scenario | `ffmpeg` needed? |
|---|----------|------------------|
| 1 | Successful golden path | yes — the run completes through assemble |
| 2 | Retryable technical failure | produced **by running with `ffmpeg` absent** |
| 3 | Governance-blocked source | no — the fail-closed gate stops the run at ingest |
| 4 | Needs-review / approval gate | yes — the run completes after approval |
| 5 | Rerun requested | no — the bounded reset acts on the scenario-2 failed run |
| 6 | Completed after rerun | yes — the run resumes to completion with `ffmpeg` available |

Key points for reproducibility:

- **No generated audio is committed.** The pipeline produces MP3 audio at the
  assemble stage, but audio is runtime output under `runs/` / `feed/` —
  git-ignored, never in the repository or a release archive. A reviewer
  regenerates it by running the pipeline locally.
- **The technical failure is not faked.** Scenario 2 produces a genuine stage
  failure by running the retryable-failure manifest with `ffmpeg` absent from
  `PATH`, so assemble fails with `FfmpegUnavailable`. `docs/demo.md` describes
  the `PATH`-without-`ffmpeg` technique.
- **The governance-blocked scenario uses an env var, not committed config.**
  Scenario 3 supplies `demo/governance/demo-blocked-sources.yaml` for one run
  via `STORYTIME_BLOCKED_SOURCES`. The repository's
  `config/governance/blocked-sources.yaml` stays empty; no enforcement code
  changes.
- **No external API or paid service is involved** in any scenario. Everything
  runs on one machine.

## Reset between demo runs

Demo runs land in `runs/` and `feed/` (or wherever `STORYTIME_RUNS_DIR` /
`STORYTIME_FEED_DIR` point), and the report in `operator-report/`. All three
are git-ignored runtime output. Delete them to reset; the `demo/` seed data and
fixtures are unaffected.

## Reproducibility checklist

- [ ] `uv run pytest -q tests/test_demo_fixtures.py` passes — fixture integrity
      confirmed with no pipeline run and no `ffmpeg`.
- [ ] The `demo/` directory is present and complete: `demo/seed/` (4 texts +
      4 manifests), `demo/fixtures/` (6 definitions + index),
      `demo/governance/demo-blocked-sources.yaml`, `demo/README.md`.
- [ ] No generated audio (`.wav` / `.mp3`) is present in the repository or
      archive.
- [ ] `config/governance/blocked-sources.yaml` is empty — the demo blocks
      nothing by default.
- [ ] (Optional, level 2) `ffmpeg` is available, and the six scenarios in
      `docs/demo.md` produce the documented states.

## Related documents

- `docs/demo.md` — the operator demo runbook (authoritative for scenario
  commands and expected state).
- `docs/demo-script.md` — the narrated presentation demo script.
- `docs/operator-reproducibility-checklist.md` — the step-by-step fresh-clone
  verification path, including the demo-fixture steps Phase 11B observed.
- `docs/fresh-clone-troubleshooting.md` — common setup failures, including the
  missing-`ffmpeg` case relevant to level-2 scenario execution.
- `docs/release-candidate-hardening.md` — the hardening baseline overview.
- `docs/known-limitations.md` — including why the needs-review scenario uses
  the operator approval gate.
