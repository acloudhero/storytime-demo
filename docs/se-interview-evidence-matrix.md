# StoryTime — Solutions Engineer Interview Evidence Matrix
<!-- CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md -->
> **Canonical demo path.** For the current, authoritative reviewer/demo
> walkthrough — the system modes and boundaries, the optional loopback
> local bridge, the one controlled retry (acceptance is not success), the
> manual snapshot reload (a read-model refresh, not a live sync), and the
> governed mock-first TTS proof (provider-backed audio remains deferred) —
> see [docs/demo-walkthrough.md](demo-walkthrough.md), the single source of
> truth and evidence map. This document is a secondary/historical narrative;
> where it differs, the canonical walkthrough wins.


*Phase 12B — Portfolio Evidence Pack / Reviewer Assets. This document maps
Solutions-Engineer and technical pre-sales competencies to the places in
StoryTime where each is demonstrated, and to an honest way to talk about it.
It indexes existing material; it does not restate the pitches in
`docs/solutions-engineer-narrative.md` or the talking points in
`docs/interview-talking-points.md` — read those for the narrative form.*

The matrix is a study and preparation aid. Every "evidence" cell points to
something concrete in the repository; every "what not to claim" cell keeps the
framing honest. StoryTime is a portfolio project, not a deployed product, and
the talking points below are written to be defensible on that basis.

## How to use this matrix

For each competency: read the evidence, then practise the talking point out
loud, then internalise the "what not to claim" line so the claim stays inside
what the repository can actually back. If an interviewer asks for proof, the
evidence column is what you open.

## The matrix

### 1. Observability fluency

- **Evidence.** `src/storytime/adapters/telemetry/` (the telemetry adapter and
  its no-op and OTel backends); `config/grafana/dashboards/` (six
  dashboards-as-code); `tests/test_dashboards.py` (metric-honesty test);
  `tests/test_telemetry_noop.py` and `tests/test_telemetry_otel.py`.
- **Talking point.** "StoryTime treats observability as a first-class concern
  but an optional view: the system records its truth in SQLite, and telemetry
  is layered on top. I can show traces, eight low-cardinality metrics, and six
  dashboards defined as code — with a test that fails if a dashboard
  references a metric the code does not emit."
- **What not to claim.** Do not call it a production monitoring stack; there is
  no alerting and no error budget. Say "observability instrumentation and
  dashboards", not "an SRE practice".

### 2. OpenTelemetry depth

- **Evidence.** `src/storytime/adapters/telemetry/otel.py` (the only module
  that imports the OTel SDK); the import-linter contract "OpenTelemetry is
  confined to the telemetry adapter" in `pyproject.toml`;
  `tests/test_import_boundaries.py`; `src/storytime/adapters/telemetry/propagation.py`
  and `tests/test_traceparent_propagation.py`.
- **Talking point.** "I made a deliberate architectural decision to confine
  OpenTelemetry to a single adapter, and I enforce it mechanically with an
  import-linter contract in CI — so the rest of the codebase names metrics
  with plain string constants and never couples to the SDK. Trace context
  propagates via standard `traceparent` headers."
- **What not to claim.** Do not claim OTel expertise across languages or
  signals you have not exercised here; the project covers traces and metrics
  in Python.

### 3. Vendor integration / "make it work with our tooling"

- **Evidence.** `config/vendor/otel-collector.dynatrace.example.yaml` and
  `config/vendor/otel-collector.newrelic.example.yaml`;
  `docker-compose.vendor.dynatrace.yml` and `docker-compose.vendor.newrelic.yml`;
  `tests/test_vendor_export_profiles.py`.
- **Talking point.** "Because telemetry exits through an OTel Collector,
  pointing StoryTime at a commercial backend is a Collector configuration
  change, not a code change. The repository includes example Collector
  profiles for two vendors to demonstrate that fan-out pattern."
- **What not to claim.** These are *example configurations*. Do not claim a
  certified or production integration with any named vendor.

### 4. Troubleshooting and failure-mode reasoning

- **Evidence.** `docs/failure-mode-regression-hardening.md`,
  `docs/regression-risk-register.md`, `docs/failure-mode-test-matrix.md`,
  `docs/operator-failure-response.md`; `tests/test_failure_mode_regression.py`;
  `src/storytime/operator_rerun.py` and `tests/test_operator_rerun.py`.
- **Talking point.** "I inventoried the highest-risk failure paths — the
  failure queue, retry and re-run, governance-blocked content, report safety —
  mapped each to the test that protects it, and wrote an operator
  failure-response playbook. A failed run re-runs from the failed stage, not
  from the beginning."
- **What not to claim.** Do not present the failure queue as a broker-backed
  message queue; `docs/known-limitations.md` is explicit that it is not.

### 5. Governance and trust framing

- **Evidence.** `src/storytime/governance/` (`gate.py`, `trust_envelope.py`,
  `blocked_sources.py`, `legal_terms.py`); `tests/test_governance_gate.py`,
  `tests/test_trust_envelope.py`, `tests/test_legal_hallucination_gate.py`;
  `config/governance/blocked-sources.yaml`.
- **Talking point.** "Governance is fail-closed: an unauthorized source does
  not proceed. The Trust Envelope records a human decision, and there is a test
  whose entire job is to make sure the system never emits invented
  legal-certification language. The boundary is deliberate — it is a project
  control, not legal advice."
- **What not to claim.** Never describe governance as a legal determination, a
  certification, or a compliance guarantee. Use "project control" and "records
  a human decision, not legal advice" — this is the exact framing the codebase
  enforces.

### 6. Reproducible-demo discipline

- **Evidence.** `docs/demo.md` (the authoritative runbook),
  `docs/portfolio-demo-script.md` (the narrated walkthrough),
  `docs/demo-reviewer-checklist.md` (the reviewer wrapper); `demo/fixtures/`
  (six golden-path fixtures), `demo/seed/` (CC0 seed texts);
  `tests/test_demo_fixtures.py`, `tests/test_demo_harness.py`.
- **Talking point.** "The demo is deterministic and fixture-driven, so it runs
  the same way every time. There is one authoritative runbook, a narrated
  walkthrough for presenting it, and a reviewer checklist — and the fixtures
  are tested, so the demo cannot silently drift from the code."
- **What not to claim.** The demo fixtures are small local examples, not a
  content library; do not present them as production data.

### 7. Clear, customer-facing technical communication

- **Evidence.** `docs/portfolio-overview.md`,
  `docs/solutions-engineer-narrative.md` (30-second / 2-minute / deep pitches),
  `docs/interview-talking-points.md`, `docs/observability-governance-talking-points.md`,
  `docs/portfolio-public-copy.md`.
- **Talking point.** "I can pitch the same system at three depths — a
  30-second hook, a two-minute overview, and a deep technical walkthrough —
  and I keep a 'what not to claim' section in my own materials so the framing
  stays honest."
- **What not to claim.** Do not oversell the documentation as customer
  collateral; it is portfolio material written to a disciplined standard.

### 8. Disciplined scoping and engineering process

- **Evidence.** `docs/phase-closure-protocol.md`, `docs/canonical-state.md`
  and `docs/phase-history.md` (append-only ledgers), `docs/roadmap.md`,
  `docs/known-limitations.md`; `tests/test_failure_mode_regression.py` (the
  state-documentation discipline guard); the six Docker-free gates in the
  `README.md` and `Makefile`.
- **Talking point.** "The project runs on an explicit phase-closure protocol:
  every phase is implemented, independently reviewed, critiqued, and only then
  locked. The history is append-only and there is a test that fails if the
  state documentation drifts. I am comfortable saying clearly what the project
  does *not* do — that is what `known-limitations.md` is for."
- **What not to claim.** Do not present the multi-model workflow as a team of
  people; it is a structured review process using multiple models plus a human
  decision-maker.

## Honesty checklist for any interview answer

Before making a claim about StoryTime, confirm all five:

1. There is a file in the repository that backs it (use the Evidence Index).
2. It does not imply a production deployment, users, or an SLA.
3. It does not imply a certified vendor integration.
4. It does not describe governance as a legal determination or certification.
5. If the claim has a boundary, you can state the boundary from
   `docs/known-limitations.md`.

The companion documents are `docs/portfolio-evidence-index.md` (claim-to-file
map), `docs/solutions-engineer-narrative.md` (the pitches), and
`docs/interview-talking-points.md` (concise study points).
