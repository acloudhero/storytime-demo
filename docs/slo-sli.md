# SLO / SLI Model

> **Demo-grade.** StoryTime is a local-first portfolio project. This document
> describes how its real telemetry *would* support service-level objectives and
> indicators. It does **not** claim production SLOs, an error budget process,
> on-call, or alerting — none of those exist. Every SLI below is derived from a
> metric StoryTime actually emits; nothing here is invented to look complete.

## 1. The honest starting point

StoryTime emits exactly eight metrics (`storytime.adapters.telemetry.metrics`):

| Metric | Kind | Labels (Prometheus form) |
|--------|------|--------------------------|
| `pipeline_runs_total` | counter | `mode` (`run`/`resume`/`stage`) |
| `pipeline_stage_completed_total` | counter | `pipeline_stage` |
| `pipeline_stage_failed_total` | counter | `pipeline_stage` |
| `pipeline_approvals_total` | counter | `gate`, `decision` |
| `pipeline_resume_total` | counter | — |
| `pipeline_artifact_validation_failed_total` | counter | `reason` |
| `pipeline_stage_duration_seconds` | histogram | `pipeline_stage` |
| `pipeline_run_duration_seconds` | histogram | `pipeline_status` |

An SLI can only be built from those series. The dotted OpenTelemetry label
keys `pipeline.stage` / `pipeline.status` appear in Prometheus with an
underscore (`pipeline_stage` / `pipeline_status`); this document uses the
Prometheus form because that is what a query or dashboard sees.

## 2. SLIs that the current metrics support

These four SLIs are genuinely derivable today. Each is an *indicator* — a
measurement — not yet an *objective*.

### 2.1 Stage success ratio (a quality SLI)

```
sum(rate(pipeline_stage_completed_total[30m]))
/
(
  sum(rate(pipeline_stage_completed_total[30m]))
  + sum(rate(pipeline_stage_failed_total[30m]))
)
```

The fraction of stage executions that finished successfully. It can be sliced
`by (pipeline_stage)` to see which stage is weakest. This is the closest thing
StoryTime has to an "availability" signal.

### 2.2 Run completion ratio (a throughput / outcome SLI)

```
sum(rate(pipeline_run_duration_seconds_count{pipeline_status="succeeded"}[30m]))
/
sum(rate(pipeline_run_duration_seconds_count[30m]))
```

The fraction of finished run spans whose terminal status was `succeeded`
(versus `failed` or `awaiting_approval`). Note `awaiting_approval` is a
*healthy* pause, not a failure — see §4.

### 2.3 Stage latency (a latency SLI)

```
histogram_quantile(0.95,
  sum by (le, pipeline_stage) (rate(pipeline_stage_duration_seconds_bucket[30m])))
```

The p95 wall-clock duration of a stage execution. The "Stage Duration"
dashboard charts p50 and p95.

### 2.4 Artifact integrity (a correctness SLI)

```
sum(rate(pipeline_artifact_validation_failed_total[30m]))
```

Artifact-envelope validation failures during rehydration. The healthy value is
**zero** — any non-zero rate means a persisted artifact's hash, envelope, or
key did not validate. The `reason` label names which check failed.

## 3. An SLO model over those SLIs

An SLO is an SLI plus a target plus a window. The table below is an
**illustrative, demo-grade** model — reasonable starting targets for a local
pipeline, explicitly *not* committed production objectives and *not* backed by
an error-budget or alerting process.

| SLI | Illustrative target | Window | Rationale |
|-----|--------------------|--------|-----------|
| Stage success ratio | ≥ 99% | rolling 30 days | A stage failing is a real defect; the demo pipeline is deterministic, so near-100% is expected. |
| Run completion ratio | ≥ 95% of *non-paused* runs | rolling 30 days | Excludes `awaiting_approval`, which is a healthy pause, not a miss. |
| Stage latency (p95) | ≤ a few seconds, MockTTS path | rolling 7 days | MockTTS + local ffmpeg are fast; this catches a regression, not an absolute promise. |
| Artifact integrity | 0 validation failures | always | Integrity is binary; any failure is investigated, never budgeted. |

**How to read this:** the value of the model is the *shape* — pick an SLI
grounded in a real metric, state a target, state a window, state why. The
numbers are starting points an operator would tune against observed baselines,
not guarantees.

## 4. What cannot be measured yet — and why that is stated, not hidden

Honesty about the gaps is part of the deliverable.

- **Audio quality / TTS correctness.** No metric measures whether synthesized
  audio is intelligible or correct. MockTTS produces a deterministic WAV; there
  is nothing to assert about its quality. A TTS-quality SLI would need new
  instruments first.
- **RSS feed correctness / subscriber experience.** No metric measures whether
  `feed.xml` is well-formed for a given podcast client, or whether a subscriber
  successfully fetched an episode. The feed *is* validated in-process before
  the atomic write (Phase 6S), but that validation is not surfaced as a metric.
- **Serving health.** Phase 6S added a range-capable HTTP server, but no
  request-rate, latency, or status-code metric exists for it. Serving is
  currently un-instrumented.
- **True end-to-end "text in → episode out" wall-clock.** A run that pauses at
  an approval gate ends its process; the resume is a *new* trace.
  `pipeline_run_duration_seconds` therefore measures *active span time per
  invocation*, not the human-inclusive wall-clock across an approval pause.
  Total human-inclusive latency is intentionally not a single metric.
- **Per-run / per-source slicing of metrics.** `pipeline_run_id` is
  deliberately **not** a metric label — it is unbounded and would explode
  cardinality. Metrics answer "how is the pipeline doing in aggregate"; to
  inspect *one* run you pivot to a trace or to SQLite (see §6).

### Why TTS and RSS dashboards are deferred

Phase 6A built six dashboards over the eight real metrics and deliberately did
**not** create a TTS/Audio dashboard or an RSS-Publish-Health dashboard: no
Phase 5 metric measures those domains, and inventing a metric to fill a panel
would make the dashboards lie. Those dashboards become possible only after a
future telemetry phase adds the supporting instruments. This is the
"metric honesty" rule (`tests/test_dashboards.py` enforces it) applied to
roadmap decisions, not just to existing panels.

## 5. Why SQLite is the source of truth and OpenTelemetry is a view

StoryTime's durable record of a run is **SQLite** — the `pipeline_run`,
`stage_execution`, `stage_artifact`, `approval`, and append-only `event_log`
tables — plus the artifact envelopes on disk. Persistence to SQLite always
happens *before* any telemetry is emitted; telemetry never gates a write.

OpenTelemetry traces and metrics are a **view** over that truth. The
consequences that matter for an SLO discussion:

- If the collector is down, spans and metrics are dropped (non-blocking export)
  — but the run still completes and SQLite still has the complete, correct
  record. Observability can fail without the pipeline failing.
- A metric is therefore an *approximate, aggregate* view. The authoritative
  answer to "what happened to this run" is always SQLite, not a dashboard.
- Under the default `NoopTelemetry` adapter no telemetry is emitted at all and
  the pipeline behaves identically. The dashboards are an opt-in lens, not a
  dependency.

This is why the SLO model is framed as "indicators over a view": useful for
spotting trends and regressions, never the system of record.

## 6. How `pipeline_run_id` correlates the three surfaces

`pipeline_run_id` (a ULID) is the durable correlation key across every surface:

| Surface | Where `pipeline_run_id` appears | What it answers |
|---------|--------------------------------|-----------------|
| **SQLite / event_log** | primary/foreign key on every run-related row | the authoritative, complete history of one run |
| **Traces (Jaeger)** | the `pipeline.run_id` span attribute on every span | the causal, timed story of one run, including linked resume traces |
| **Metrics (Prometheus/Grafana)** | **deliberately absent** as a label | aggregate fleet health only — never one run |

The intended workflow: a **dashboard** shows that something is wrong in
aggregate (e.g. the stage-failure panel ticks up). You then **pivot to a
trace** — search Jaeger by the `pipeline.run_id` attribute — to see the failing
run's span tree and `error.kind` / `error.message`. For the fully
authoritative record you query **SQLite** by `pipeline_run_id`. Metrics narrow
*when and what*; traces and SQLite tell you *which run and why*.

A resumed run is a new trace carrying a W3C `Link` back to the pre-pause trace,
but it keeps the same `pipeline_run_id` — so the correlation key survives the
approval-pause boundary even though the trace identity does not.

## 7. Non-goals (restated for SLO context)

- No alerting, no Alertmanager, no Slack/PagerDuty, no on-call rotation.
- No error-budget accounting or burn-rate policy.
- No production reliability claim of any kind.
- No cloud, blue/green, or vendor-backend SLOs.

See `docs/dashboard-guide.md` for per-panel interpretation, `docs/runbook.md`
for operator procedures, and `docs/observability-demo.md` for the end-to-end
walkthrough.
