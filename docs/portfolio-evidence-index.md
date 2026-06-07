# StoryTime — Portfolio Evidence Index
<!-- CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md -->
> **Canonical demo path.** For the current, authoritative reviewer/demo
> walkthrough — the system modes and boundaries, the optional loopback
> local bridge, the one controlled retry (acceptance is not success), the
> manual snapshot reload (a read-model refresh, not a live sync), and the
> governed mock-first TTS proof (provider-backed audio remains deferred) —
> see [docs/demo-walkthrough.md](demo-walkthrough.md), the single source of
> truth and evidence map. This document is a secondary/historical narrative;
> where it differs, the canonical walkthrough wins.


*Phase 12B — Portfolio Evidence Pack / Reviewer Assets. This document is an
index, not a new claim. Every row maps a claim StoryTime's portfolio materials
already make to the concrete artifact in this repository that backs it: a test,
a configuration file, a source module, or a prior document. A reviewer should
be able to pick any claim and verify it directly.*

This index introduces no new capability and no new assertion. It points at
evidence produced and verified in Phases 0–12A. Where a claim has a natural
boundary, the boundary is named and `docs/known-limitations.md` is cited as the
authoritative scope statement.

## How to use this index

1. Pick a claim from the table below.
2. Open the evidence file at the path given.
3. For a test, run it in isolation, e.g. `uv run pytest -q tests/<file>`.
4. For a config or source file, read the cited file directly.
5. For scope and non-goals, read the cited section of
   `docs/known-limitations.md`.

All test paths are runnable offline. The six Docker-free quality gates are
listed in the project `README.md` and the `Makefile`.

## Claim-to-evidence table

### Architecture and data model

| Claim | Primary evidence | Supporting evidence |
|---|---|---|
| SQLite and on-disk artifact envelopes are the source of truth | `src/storytime/state/store.py`, `src/storytime/artifacts/envelope.py` | `tests/test_state_store.py`, `tests/test_artifact_envelope.py`, `tests/test_rehydration.py` |
| Artifact envelopes are content-hashed and integrity-checked | `src/storytime/util/hashing.py`, `src/storytime/artifacts/envelope.py`, `src/storytime/artifacts/io.py` | `tests/test_artifact_envelope.py`, `tests/test_byte_ranges.py` |
| The pipeline is five staged steps plus approval gates | `src/storytime/pipeline.py`, `src/storytime/stages/` (`ingest`, `synthesize`, `assemble`, `publish`, `approve`) | `tests/test_ingest_stage.py`, `tests/test_synthesize_stage.py`, `tests/test_assemble_stage.py`, `tests/test_publish_stage.py`, `tests/test_vertical_slice.py` |
| `pipeline_run_id` is a ULID correlation key threaded through every run | `src/storytime/util/ids.py`, `src/storytime/runner/context.py` | `tests/test_runner.py`, `tests/test_traceparent_propagation.py` |
| Internal import boundaries are enforced, not just documented | `pyproject.toml` (`[tool.importlinter]`, two contracts) | `tests/test_import_boundaries.py`, `tests/test_imports.py`, `tests/test_phase3_boundaries.py` |

### Observability

| Claim | Primary evidence | Supporting evidence |
|---|---|---|
| OpenTelemetry is confined to one adapter module | `pyproject.toml` import-linter contract "OpenTelemetry is confined to the telemetry adapter"; `src/storytime/adapters/telemetry/otel.py` is the sole OTel module | `tests/test_import_boundaries.py`, the OTel-free constants in `src/storytime/adapters/telemetry/metrics.py` |
| Telemetry is an optional view; the system runs fully without it | `src/storytime/adapters/telemetry/noop.py` (default no-op backend) | `tests/test_telemetry_noop.py`, `tests/test_telemetry_otel.py`, `tests/test_telemetry_phase5.py` |
| The metric set is small and the label vocabulary is low-cardinality | `src/storytime/adapters/telemetry/metrics.py` (named metric constants; `pipeline_run_id` is deliberately never a metric label) | `src/storytime/adapters/telemetry/attributes.py`, `src/storytime/adapters/telemetry/hygiene.py` |
| Trace context propagates across process boundaries | `src/storytime/adapters/telemetry/propagation.py` | `tests/test_traceparent_propagation.py` |
| Dashboards are defined as code and tested for metric honesty | `config/grafana/dashboards/` — six dashboards: `pipeline-overview.json`, `stage-duration.json`, `run-timeline.json`, `failures-rejections.json`, `approval-resume.json`, `artifact-validation.json` | `tests/test_dashboards.py` (asserts each dashboard references only metrics the code actually emits), `docs/dashboard-guide.md` |
| Vendor fan-out is a configuration change, not a code change | `config/vendor/otel-collector.dynatrace.example.yaml`, `config/vendor/otel-collector.newrelic.example.yaml`, `docker-compose.vendor.*.yml` | `tests/test_vendor_export_profiles.py`, `tests/test_observability_stack.py` |

### Governance and trust

| Claim | Primary evidence | Supporting evidence |
|---|---|---|
| Governance is fail-closed: an unauthorized source does not proceed | `src/storytime/governance/gate.py`, `src/storytime/governance/trust_envelope.py` | `tests/test_governance_gate.py`, `tests/test_governance_pipeline.py`, `tests/test_trust_envelope.py` |
| Source authorization is driven by an explicit allow/deny configuration | `config/governance/blocked-sources.yaml`, `src/storytime/governance/blocked_sources.py`, `src/storytime/governance/schema.py` | `tests/test_blocked_sources.py` |
| The Trust Envelope records a human decision, not a legal determination | `src/storytime/governance/trust_envelope.py`; scope stated in `docs/known-limitations.md` ("Governance checks are project controls, not legal advice") | `docs/observability-governance-talking-points.md` |
| The system does not emit invented legal-certification language | `src/storytime/governance/legal_terms.py` (forbidden-vocabulary set) | `tests/test_legal_hallucination_gate.py` (scans documents and output for the forbidden vocabulary) |
| The approval gate is an explicit operator decision point | `src/storytime/approval.py`, `src/storytime/stages/approve.py` | `tests/test_approval_gate.py`, `tests/test_resume_cli.py` |

### Operator experience

| Claim | Primary evidence | Supporting evidence |
|---|---|---|
| The operator report is a static, read-only local HTML artifact | `src/storytime/reporting/generate.py`, `src/storytime/reporting/render.py`, `src/storytime/reporting/collect.py` | `tests/test_operator_report.py`; scope in `docs/known-limitations.md` ("The static report is read-only") |
| A failed run can be re-run from the failed stage | `src/storytime/operator_rerun.py` | `tests/test_operator_rerun.py`, `tests/test_resume_cli.py` |
| The failure / review queue is a first-class operator surface | `src/storytime/operator_queue.py` | `tests/test_operator_queue.py` |
| The CLI surface is explicit and its mutation boundaries are defined | `src/storytime/cli/app.py` | `tests/test_cli_surface.py`, `docs/command-reference.md` |
| `storytime doctor` reports environment health offline | `src/storytime/doctor.py` | `tests/test_doctor.py` |

### Output and distribution

| Claim | Primary evidence | Supporting evidence |
|---|---|---|
| StoryTime produces a valid podcast RSS feed | `src/storytime/rss/builder.py`, `src/storytime/rss/validator.py`, `src/storytime/rss/catalog.py` | `tests/test_multi_item_feed.py`, `tests/test_episode_catalog.py` |
| Audio artifacts support HTTP range requests | `src/storytime/http/ranges.py`, `src/storytime/http/server.py` | `tests/test_range_server.py`, `tests/test_byte_ranges.py` |
| The HTTP server binds locally and is not exposed by default | `src/storytime/http/server.py` | `tests/test_http_bind_safety.py` |
| TTS is adapter-based and mock-grade by default | `src/storytime/adapters/tts/` (`mock.py`, `piper.py`, `manual_import.py`) | `tests/test_tts_mock.py`, `tests/test_tts_piper_stub.py`, `tests/test_tts_manual_import.py`; scope in `docs/known-limitations.md` ("TTS is mock-grade") |

### Reproducibility and process discipline

| Claim | Primary evidence | Supporting evidence |
|---|---|---|
| The demo is deterministic and fixture-driven | `demo/fixtures/` (six golden-path fixtures), `demo/seed/` (CC0 seed texts), `src/storytime/demo/harness.py` | `tests/test_demo_fixtures.py`, `tests/test_demo_harness.py`, `docs/demo.md` |
| Six Docker-free quality gates protect every change | `README.md` (validation section), `Makefile` | gate commands: `uv sync --frozen --extra dev`, `uv run pytest -q`, `uv run ruff check .`, `uv run mypy`, `uv run lint-imports`, `uv run storytime doctor` |
| Project history is append-only and auditable | `docs/canonical-state.md`, `docs/phase-history.md` (append-only ledgers) | `tests/test_failure_mode_regression.py` (the state-documentation discipline guard) |
| Failure modes are inventoried and mapped to the tests that cover them | `docs/failure-mode-regression-hardening.md`, `docs/regression-risk-register.md`, `docs/failure-mode-test-matrix.md` | `tests/test_failure_mode_regression.py`, `docs/operator-failure-response.md` |
| The build runs from a clean clone with a pinned lockfile | `uv.lock` (committed), `pyproject.toml` | `docs/fresh-clone-checklist.md`, `docs/operator-reproducibility-checklist.md`, `tests/test_containerization.py`, `tests/test_deployment.py` |

## Boundaries — what the evidence does not claim

The evidence above demonstrates engineering and operational discipline. It does
**not** demonstrate, and StoryTime does not claim:

- a production SaaS deployment, real users, an SLA, or cloud hosting;
- active alerting or an error-budget policy;
- an integration certified with any named commercial observability vendor —
  the vendor files are example Collector configurations only;
- a legal determination about any content, or a rights-clearance capability —
  governance records a human decision, not legal advice.

Each boundary is stated authoritatively in `docs/known-limitations.md`. The
companion documents for this index are `docs/portfolio-overview.md` (the
plain-English overview), `docs/se-interview-evidence-matrix.md` (the
competency mapping), and `docs/demo-reviewer-checklist.md` (the
reviewer-facing demo wrapper).
