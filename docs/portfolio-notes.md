# Portfolio / Software-Engineering Talking Points
<!-- CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md -->
> **Canonical demo path.** For the current, authoritative reviewer/demo
> walkthrough — the system modes and boundaries, the optional loopback
> local bridge, the one controlled retry (acceptance is not success), the
> manual snapshot reload (a read-model refresh, not a live sync), and the
> governed mock-first TTS proof (provider-backed audio remains deferred) —
> see [docs/demo-walkthrough.md](demo-walkthrough.md), the single source of
> truth and evidence map. This document is a secondary/historical narrative;
> where it differs, the canonical walkthrough wins.


A concise, honest account of what the StoryTime project demonstrates as an
engineering portfolio piece. It is written to be quotable in a CV, a project
README summary, or an interview — without overclaiming.

> **What StoryTime is:** a local-first, CLI-driven, observability-native
> pipeline that turns approved CC0 / US-public-domain text into podcast audio,
> an RSS feed, and pipeline telemetry. **What it is not:** a production
> service. It has not been deployed, has no users, no alerting, and no cloud
> footprint. The value is in the *engineering discipline*, not in operational
> scale.

## 1. One-paragraph summary

StoryTime is a Python content-to-audio pipeline built under a multi-model
"RoundTable" governance process. It pairs a deliberately small, well-bounded
architecture — DTO stage contracts, a single source of truth, mechanically
enforced module boundaries — with genuine OpenTelemetry instrumentation and a
local observability stack (Collector, Prometheus, Grafana, Jaeger) provisioned
entirely as code. Every design boundary is defended by a test or a linter
contract, and the observability layer is held to a "metric honesty" rule: a
dashboard may not chart a metric the system does not actually emit.

## 2. What it demonstrates

### Observability-native design, done honestly

- Real OpenTelemetry traces and metrics, not log scraping. One `pipeline.run`
  span per run with child stage spans; eight purposeful, low-cardinality
  metrics; six dashboards-as-code.
- **Metric honesty as an enforced rule.** `tests/test_dashboards.py` fails the
  build if a dashboard references a metric the code does not emit. The project
  has no TTS or RSS dashboards *because* no metric supports them — the absence
  is a deliberate, documented decision, not an oversight.
- The SLO/SLI model (`docs/slo-sli.md`) is built strictly from real metrics and
  is explicit about what cannot be measured yet.

### Source-of-truth discipline

- SQLite (an append-only `event_log` plus run/stage/artifact/approval tables)
  and on-disk artifact envelopes are the durable record. Persistence happens
  *before* telemetry emission.
- OpenTelemetry is explicitly a **view** over that truth. With the default
  `NoopTelemetry` adapter, no telemetry is emitted and the pipeline behaves
  identically — observability can fail without the pipeline failing.
- `pipeline_run_id` (a ULID) is the durable correlation key across SQLite,
  traces, and the operator's mental model — and is deliberately *not* a metric
  label, to keep metric cardinality bounded.

### Boundaries that are mechanically enforced

- DTO stage contracts (`StageInput` / `StageResult` / `StateUpdate`) — no
  mutable god-object context.
- OpenTelemetry imports are confined to one adapter module, enforced by an
  `import-linter` contract *and* an AST-scanning test.
- The source manifest is a closed JSON Schema (`additionalProperties: false`)
  constraining input to CC0 / US public domain.
- `ARCH-LOCK` annotations mark load-bearing boundaries in the code itself.

### Migration and resume safety

- Numbered, additive SQLite migrations; resume/rehydration rebuilds a run from
  SQLite and hash-verifies every reused artifact before continuing — a tampered
  artifact is refused, not silently trusted.
- Approval gates are real persisted pipeline stages; a paused run exits its
  process cleanly and resumes as a new linked trace.

### Process discipline

- Phased delivery with an explicit Phase Closure Protocol: implementation
  output is reviewed (GPT-5.5), critiqued (Gemini), cleaned up, and only then
  locked by explicit user approval.
- An honest history: Phase 6S was an out-of-band execution caused by a
  prompt-transfer error; rather than hiding it, it was reviewed, accepted as a
  reclassified phase, and its provenance written into the canonical record
  (`docs/phase-history.md`).

## 3. Honest non-goals (say these out loud)

Naming the non-goals is itself a talking point — it shows scoping discipline.

- **Not production-ready.** Demo-grade. No users, no SLA.
- **No alerting.** No Alertmanager, Slack, PagerDuty, or on-call. An operator
  reads dashboards; nothing pages.
- **No cloud, no Kubernetes, no Terraform.** Local-first by charter. Phase 7A
  adds a lean *local* blue/green path (Option A): two slot-scoped processes
  with separated state and telemetry resource attribution. There is no cloud
  deployment, no container image, and no automated traffic cutover — those are
  deferred to Option B (see `docs/deployment-bluegreen-option-a.md` §8).
- **No vendor telemetry fan-out.** Telemetry goes to the local stack only.
- **Single-machine.** Both blue/green slots run on one host; no cross-host
  scaling or capacity story.
- **TTS is MockTTS-grade.** Real Piper TTS is stubbed; audio quality is not a
  current concern and is not measured.

## 4. Suggested phrasing for a CV / summary

> *Built an observability-native Python content pipeline: OpenTelemetry traces
> and metrics, a code-provisioned Grafana/Prometheus/Jaeger stack, and
> dashboards held to an automated "metric honesty" check. Enforced
> architectural boundaries with import-linter and AST tests; kept SQLite as the
> single source of truth with OpenTelemetry as a view over it.*

Every clause above is literally true of the repository and is backed by a
test, a config file, or a doc. If a claim cannot be pointed at, it should not
be made — that is the same honesty rule the dashboards follow.

## 5. Where to look in the repo

| To see... | Look at |
|-----------|---------|
| The telemetry architecture | `docs/telemetry-map.md` |
| The SLI model + limitations | `docs/slo-sli.md` |
| How to run the demo | `docs/observability-demo.md` |
| How to read the dashboards | `docs/dashboard-guide.md` |
| Operator procedures | `docs/runbook.md` |
| Dashboards-as-code | `config/grafana/dashboards/*.json` |
| The demo harness | `src/storytime/demo/` |
| Metric-honesty enforcement | `tests/test_dashboards.py` |
| Project history (incl. Phase 6S provenance) | `docs/phase-history.md` |
