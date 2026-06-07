"""Telemetry metric names and kinds -- OTel-free constants.

ARCH-LOCK: Telemetry Import Boundary (see storytime.adapters.telemetry.base)
DO NOT REFACTOR: This module declares the StoryTime metric vocabulary as plain
strings. It deliberately does NOT import opentelemetry, so the runner, the
approval service, and the rehydration code can name a metric without coupling
to the OpenTelemetry SDK. The SDK-level instrument objects live only in
storytime.adapters.telemetry.otel, the sole OpenTelemetry module.

The metric set is intentionally small and the label vocabulary intentionally
low-cardinality. ``pipeline_run_id`` is NEVER a metric label -- it is unbounded
and belongs on spans, not on metric time series. Metrics are a view over the
SQLite source of truth; under NoopTelemetry no metric is recorded at all.
"""

from __future__ import annotations

# -- counter metrics ---------------------------------------------------------

# Incremented once per pipeline run started (a run_sequence, a resume_sequence,
# or a standalone execute_stage). Label: ``mode`` in {run, resume, stage}.
METRIC_RUNS_TOTAL = "pipeline_runs_total"

# Incremented once per stage that finished SUCCEEDED. Label: ``pipeline.stage``.
METRIC_STAGE_COMPLETED_TOTAL = "pipeline_stage_completed_total"

# Incremented once per stage that finished FAILED. Label: ``pipeline.stage``.
METRIC_STAGE_FAILED_TOTAL = "pipeline_stage_failed_total"

# Incremented once per recorded operator approval decision.
# Labels: ``gate`` in {text, audio}, ``decision`` in {approved, rejected}.
METRIC_APPROVALS_TOTAL = "pipeline_approvals_total"

# Incremented once per resume attempt that reached stage execution.
METRIC_RESUME_TOTAL = "pipeline_resume_total"

# Incremented once per artifact-envelope validation failure during rehydration.
# Label: ``reason`` (a small, fixed set -- see storytime.runner.rehydrate).
METRIC_ARTIFACT_VALIDATION_FAILED_TOTAL = "pipeline_artifact_validation_failed_total"

# -- histogram metrics -------------------------------------------------------

# Wall-clock duration of a single stage execution, in seconds.
# Label: ``pipeline.stage``.
METRIC_STAGE_DURATION_SECONDS = "pipeline_stage_duration_seconds"

# Wall-clock duration of a whole pipeline run span, in seconds.
# Label: ``pipeline.status``.
METRIC_RUN_DURATION_SECONDS = "pipeline_run_duration_seconds"


# The closed sets the OTel adapter pre-creates instruments for. record_metric
# silently ignores any name not in one of these sets, so a typo can never
# create an unbounded, undocumented instrument.
COUNTER_METRICS: frozenset[str] = frozenset(
    {
        METRIC_RUNS_TOTAL,
        METRIC_STAGE_COMPLETED_TOTAL,
        METRIC_STAGE_FAILED_TOTAL,
        METRIC_APPROVALS_TOTAL,
        METRIC_RESUME_TOTAL,
        METRIC_ARTIFACT_VALIDATION_FAILED_TOTAL,
    }
)

HISTOGRAM_METRICS: frozenset[str] = frozenset(
    {
        METRIC_STAGE_DURATION_SECONDS,
        METRIC_RUN_DURATION_SECONDS,
    }
)

ALL_METRICS: frozenset[str] = COUNTER_METRICS | HISTOGRAM_METRICS


__all__ = [
    "ALL_METRICS",
    "COUNTER_METRICS",
    "HISTOGRAM_METRICS",
    "METRIC_APPROVALS_TOTAL",
    "METRIC_ARTIFACT_VALIDATION_FAILED_TOTAL",
    "METRIC_RESUME_TOTAL",
    "METRIC_RUNS_TOTAL",
    "METRIC_RUN_DURATION_SECONDS",
    "METRIC_STAGE_COMPLETED_TOTAL",
    "METRIC_STAGE_DURATION_SECONDS",
    "METRIC_STAGE_FAILED_TOTAL",
]
