"""NoopTelemetry: a complete, side-effect-free TelemetryAdapter."""

from __future__ import annotations

from datetime import UTC, datetime

from storytime.adapters.telemetry import NoopTelemetry, TelemetryAdapter
from storytime.adapters.telemetry.base import RunHandle, StageHandle
from storytime.events import EventType, PipelineEvent


def test_noop_satisfies_the_telemetry_protocol() -> None:
    assert isinstance(NoopTelemetry(), TelemetryAdapter)


def test_noop_run_and_stage_lifecycle_returns_handles() -> None:
    telemetry = NoopTelemetry()
    run = telemetry.on_run_started("run-1", {"k": "v"})
    assert isinstance(run, RunHandle)
    assert run.pipeline_run_id == "run-1"

    stage = telemetry.on_stage_started(run, "ingest", {})
    assert isinstance(stage, StageHandle)
    assert stage.stage_name == "ingest"


def test_noop_handles_carry_no_trace_ids() -> None:
    """NoopTelemetry produces no trace context; the pipeline still works
    because pipeline_run_id is the durable correlation key."""
    run = NoopTelemetry().on_run_started("run-1", {})
    assert run.trace_id is None


def test_noop_event_and_end_hooks_are_silent() -> None:
    telemetry = NoopTelemetry()
    run = telemetry.on_run_started("run-1", {})
    stage = telemetry.on_stage_started(run, "ingest", {})
    event = PipelineEvent(
        event_type=EventType.TEXT_INGESTED,
        pipeline_run_id="run-1",
        occurred_at=datetime(2026, 1, 1, tzinfo=UTC),
        stage_name="ingest",
        payload={},
    )
    # These return None and must not raise.
    assert telemetry.on_event(stage, event) is None
    assert telemetry.on_stage_ended(stage, status="succeeded") is None
    assert telemetry.on_run_ended(run, "completed") is None


def test_noop_metric_and_linked_run_hooks_are_silent() -> None:
    """The Phase 5 additions stay no-ops under NoopTelemetry."""
    telemetry = NoopTelemetry()
    assert telemetry.record_metric("pipeline_runs_total", 1) is None
    assert (
        telemetry.record_metric(
            "pipeline_approvals_total", 1, attributes={"gate": "text"}
        )
        is None
    )
    linked = telemetry.start_linked_run("run-1", "00-" + "a" * 32 + "-" + "b" * 16 + "-01")
    assert isinstance(linked, RunHandle)
    assert linked.trace_id is None
