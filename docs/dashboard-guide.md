# Dashboard Interpretation Guide

How to read StoryTime's six Grafana dashboards. They are provisioned as code
from `config/grafana/dashboards/` and appear in Grafana's "StoryTime" folder
(http://127.0.0.1:3000). Every panel queries Prometheus and uses only the eight
real Phase 5 metrics — see `docs/slo-sli.md` for the metric catalogue.

## Reading any StoryTime dashboard — three rules

1. **Counters are process-lifetime totals.** `pipeline_runs_total` and the
   other `_total` series count since the StoryTime process started emitting.
   A "stat" panel showing `sum(...)` is a cumulative total, not a rate. After a
   demo run, restarting the process and running again continues the count only
   if the collector/Prometheus kept the series; a fresh Prometheus starts at
   zero.
2. **Rates and quantiles need traffic in the window.** Panels using
   `rate(...[5m])` or `histogram_quantile(...)` are empty or flat until enough
   data points exist inside the window. Run the demo harness a few times, then
   wait for the 5-minute window to populate.
3. **Label names use underscores.** The OpenTelemetry label keys
   `pipeline.stage` and `pipeline.status` reach Prometheus as `pipeline_stage`
   and `pipeline_status`. `mode`, `gate`, `decision`, and `reason` have no dot
   and are unchanged.

## 1. Pipeline Overview — `pipeline-overview.json`

The at-a-glance dashboard. Six "stat" panels plus two time series.

| Panel | Query (paraphrased) | How to read it |
|-------|--------------------|----------------|
| Pipeline runs | `sum(pipeline_runs_total)` | Total run/resume/stage invocations counted. |
| Stages completed | `sum(pipeline_stage_completed_total)` | Total stage executions that finished `succeeded`. |
| Stages failed | `sum(pipeline_stage_failed_total)` | Total stage executions that finished `failed`. Healthy demo value is low; the demo's rejection and artifact-failure scenarios deliberately produce some. |
| Approvals recorded | `sum(pipeline_approvals_total)` | Total operator approval decisions (approve + reject, text + audio). |
| Resume attempts | `sum(pipeline_resume_total)` | Total resume invocations that reached stage execution. |
| Artifact validation failures | `sum(pipeline_artifact_validation_failed_total)` | Should be **0** in a clean run; the demo's `artifact_validation_failure` scenario intentionally drives it to 1+. |
| Run starts by mode (rate) | `sum by (mode) (rate(pipeline_runs_total[5m]))` | Run cadence split into `run` / `resume` / `stage`. |
| Stage completions vs failures (rate) | two series | Visual ratio of healthy to failed stage executions over time. |

**What "good" looks like:** completions climbing, failures flat near zero,
artifact-validation at zero. The demo deliberately disturbs the last two so you
can see them move.

## 2. Stage Duration — `stage-duration.json`

Per-stage latency from the `pipeline_stage_duration_seconds` histogram. Stage
names on the `pipeline_stage` label: `ingest`, `approve_text`, `synthesize`,
`approve_audio`, `assemble`, `publish`.

| Panel | How to read it |
|-------|----------------|
| Stage duration p95 by stage | The slow tail per stage. On the MockTTS path every stage is fast; `assemble` (ffmpeg MP3 encode) is usually the largest. |
| Stage duration p50 by stage | The typical case per stage. |
| Stage executions per second by stage | Throughput per stage — derived from the histogram's `_count`. |
| Mean stage duration (5m) | `_sum / _count` over 5 minutes — a single blended average. |

**Caveat:** quantile panels need several executions inside the 5-minute window
before they read meaningfully. One demo run is not enough for a stable p95.

## 3. Approval & Resume Behavior — `approval-resume.json`

Operator decisions and run resumes.

| Panel | How to read it |
|-------|----------------|
| Approvals recorded | All approval decisions. |
| Resume attempts | All resumes. |
| Approved | `pipeline_approvals_total{decision="approved"}` — decisions that let a run proceed. |
| Rejected | `pipeline_approvals_total{decision="rejected"}` — decisions that ended a run as `failed`. |
| Approval decisions by gate and decision | Time series split by `gate` (`text`/`audio`) × `decision`. Tells you which gate is being exercised and how. |
| Resume attempts per second | Resume cadence. Each approve-then-resume demo scenario adds one. |

**Interpretation:** a high reject count is not a system fault — it is operators
doing their job. Pair this dashboard with "Failure & Rejection Behavior", which
shows the *consequence* of rejections.

## 4. Failure & Rejection Behavior — `failures-rejections.json`

Separates two different "bad" outcomes.

| Panel | How to read it |
|-------|----------------|
| Stage failures | `sum(pipeline_stage_failed_total)` — stages that errored. A genuine defect signal. |
| Rejected approvals | `sum(pipeline_approvals_total{decision="rejected"})` — operator rejections. **Expected behaviour, not a defect.** |
| Stage failures by stage | Which stage is failing. |
| Rejection rate by gate | Whether rejections cluster at the text or audio gate. |

**The key distinction:** a *stage failure* is the pipeline breaking; a
*rejection* is the pipeline working — a human said no and the run correctly
ended `failed`. Both end a run, but only the first is a problem to fix.

## 5. Artifact Validation Failures — `artifact-validation.json`

Artifact-envelope integrity during rehydration.

| Panel | How to read it |
|-------|----------------|
| Total validation failures | `sum(pipeline_artifact_validation_failed_total)` — healthy value is **0**. |
| Validation failures by reason | Split by the `reason` label. |
| Validation failure rate by reason | The same, as a rate over time. |

The `reason` label is a closed set: `non_relative_key`, `envelope_missing`,
`envelope_invalid`, `unsupported_version`, `non_relative_payload`,
`payload_missing`, `hash_mismatch`. The demo's `artifact_validation_failure`
scenario tampers with a persisted payload, so it shows up here as
`hash_mismatch`. Any non-zero value outside that demo scenario means real
on-disk corruption or a code defect and should be investigated via the trace
and SQLite — see `docs/runbook.md`.

## 6. Run Timeline — `run-timeline.json`

Whole-run duration and cadence.

| Panel | How to read it |
|-------|----------------|
| Run duration p95 by terminal status | p95 of `pipeline_run_duration_seconds`, split by `pipeline_status` (`succeeded`/`failed`/`awaiting_approval`). |
| Run starts per second by mode | Run cadence by `mode`. |
| Completed-run cadence by status | How many runs reach each terminal status over time. |
| Mean run duration (5m) | Blended average run duration. |

**Important caveat (also in `docs/slo-sli.md` §4):** this dashboard measures
*active span time per invocation*. A run that pauses at an approval gate ends
its process; the resume is a separate trace. So a run's `awaiting_approval`
span and its later `resume` span are two measurements — this dashboard does
**not** show human-inclusive end-to-end wall-clock, and it is not trying to.

## Pivoting from a dashboard to a single run

Dashboards are aggregate. When a panel shows something wrong, switch surfaces:

1. **Jaeger** (http://127.0.0.1:16686) — search by the `pipeline.run_id` span
   attribute to see one run's span tree, including `error.kind` /
   `error.message` on a failed stage span.
2. **SQLite** — the authoritative record; query the `pipeline_run`,
   `stage_execution`, `event_log`, and `approval` rows by `pipeline_run_id`.

Metrics tell you *when and what*; traces and SQLite tell you *which run and
why*. See `docs/slo-sli.md` §6 for the full correlation model.
