"""OTelTelemetry: real OpenTelemetry instrumentation, exercised in-memory.

The adapter accepts an injected InMemorySpanExporter / InMemoryMetricReader so
its real behaviour -- span hierarchy, traceparent identity, W3C Links across a
resume, metric recording, and data hygiene -- is asserted without a running
collector. This test module imports opentelemetry directly: the import-linter
boundary covers ``src`` only, and a telemetry-adapter test is precisely where
inspecting OTel objects is legitimate.
"""

from __future__ import annotations

from datetime import UTC, datetime

from opentelemetry.sdk.metrics.export import InMemoryMetricReader
from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
    InMemorySpanExporter,
)

from storytime.adapters.telemetry.otel import OTelTelemetry
from storytime.adapters.telemetry.propagation import (
    format_traceparent,
    is_valid_traceparent,
    parse_traceparent,
)
from storytime.events import EventType, PipelineEvent


def _adapter() -> tuple[OTelTelemetry, InMemorySpanExporter, InMemoryMetricReader]:
    span_exporter = InMemorySpanExporter()
    metric_reader = InMemoryMetricReader()
    adapter = OTelTelemetry(
        otlp_endpoint="http://127.0.0.1:4318",
        service_version="0.2.0",
        environment="test",
        deployment_slot="blue",
        span_exporter=span_exporter,
        metric_reader=metric_reader,
    )
    return adapter, span_exporter, metric_reader


def _event(stage: str = "ingest") -> PipelineEvent:
    return PipelineEvent(
        event_type=EventType.TEXT_INGESTED,
        pipeline_run_id="run-1",
        occurred_at=datetime(2026, 1, 1, tzinfo=UTC),
        stage_name=stage,
        payload={"source_id": "the-raven", "license": "PD-US"},
    )


def _metric_points(reader: InMemoryMetricReader) -> dict[str, list]:
    """Return {metric_name: [data points]} collected so far."""
    data = reader.get_metrics_data()
    points: dict[str, list] = {}
    if data is None:
        return points
    for resource_metric in data.resource_metrics:
        for scope_metric in resource_metric.scope_metrics:
            for metric in scope_metric.metrics:
                points.setdefault(metric.name, []).extend(
                    metric.data.data_points
                )
    return points


def test_run_and_stage_form_a_parent_child_span_hierarchy() -> None:
    adapter, spans, _ = _adapter()
    run = adapter.on_run_started("run-1", {})
    stage = adapter.on_stage_started(run, "ingest", {})
    adapter.on_stage_ended(stage, status="succeeded")
    adapter.on_run_ended(run, "succeeded")

    finished = {s.name: s for s in spans.get_finished_spans()}
    assert "pipeline.run" in finished
    assert "pipeline.stage.ingest" in finished
    # The stage span is a child of the run span: same trace, parent linkage.
    run_span = finished["pipeline.run"]
    stage_span = finished["pipeline.stage.ingest"]
    assert stage_span.context.trace_id == run_span.context.trace_id
    assert stage_span.parent is not None
    assert stage_span.parent.span_id == run_span.context.span_id


def test_pipeline_run_id_is_a_span_attribute_on_every_span() -> None:
    adapter, spans, _ = _adapter()
    run = adapter.on_run_started("run-xyz", {})
    stage = adapter.on_stage_started(run, "synthesize", {})
    adapter.on_stage_ended(stage, status="succeeded")
    adapter.on_run_ended(run, "succeeded")

    for span in spans.get_finished_spans():
        assert span.attributes.get("pipeline.run_id") == "run-xyz"


def test_handles_carry_a_real_w3c_traceparent() -> None:
    adapter, _, _ = _adapter()
    run = adapter.on_run_started("run-1", {})
    stage = adapter.on_stage_started(run, "ingest", {})
    assert is_valid_traceparent(run.traceparent)
    assert is_valid_traceparent(stage.traceparent)
    # The stage span shares the run's trace but has its own span id.
    run_parsed = parse_traceparent(run.traceparent)
    stage_parsed = parse_traceparent(stage.traceparent)
    assert run_parsed is not None and stage_parsed is not None
    assert run_parsed.trace_id == stage_parsed.trace_id
    assert run_parsed.span_id != stage_parsed.span_id
    adapter.on_stage_ended(stage, status="succeeded")
    adapter.on_run_ended(run, "succeeded")


def test_resumed_run_is_a_new_trace_linked_to_the_prior_one() -> None:
    """A resume must not fake one uninterrupted span: it is a fresh trace
    carrying a real W3C Link back to the pre-pause trace."""
    adapter, spans, _ = _adapter()
    prior = format_traceparent("a" * 32, "b" * 16)

    run = adapter.on_run_started("run-1", {}, resume=True, link_traceparents=[prior])
    adapter.on_run_ended(run, "succeeded")

    resume_span = next(
        s for s in spans.get_finished_spans() if s.name == "pipeline.resume"
    )
    # Fresh trace -- not a continuation of the prior trace id.
    assert format(resume_span.context.trace_id, "032x") != "a" * 32
    # ...but a real Link records the causal relation to the prior trace.
    assert len(resume_span.links) == 1
    assert format(resume_span.links[0].context.trace_id, "032x") == "a" * 32
    assert resume_span.attributes.get("pipeline.resume") == "true"


def test_start_linked_run_helper_attaches_the_link() -> None:
    adapter, spans, _ = _adapter()
    prior = format_traceparent("c" * 32, "d" * 16)
    run = adapter.start_linked_run("run-1", prior)
    adapter.on_run_ended(run, "succeeded")
    resume_span = next(
        s for s in spans.get_finished_spans() if s.name == "pipeline.resume"
    )
    assert len(resume_span.links) == 1
    assert format(resume_span.links[0].context.trace_id, "032x") == "c" * 32


def test_stage_contributed_attributes_reach_the_span() -> None:
    adapter, spans, _ = _adapter()
    run = adapter.on_run_started("run-1", {})
    stage = adapter.on_stage_started(run, "synthesize", {})
    adapter.on_stage_ended(
        stage,
        status="succeeded",
        attributes={"artifact.kind": "audio.wav", "tts.adapter": "mock"},
    )
    adapter.on_run_ended(run, "succeeded")
    stage_span = next(
        s for s in spans.get_finished_spans() if s.name == "pipeline.stage.synthesize"
    )
    assert stage_span.attributes.get("artifact.kind") == "audio.wav"
    assert stage_span.attributes.get("tts.adapter") == "mock"
    assert stage_span.attributes.get("pipeline.status") == "succeeded"


def test_counter_and_histogram_metrics_are_recorded() -> None:
    adapter, _, reader = _adapter()
    run = adapter.on_run_started("run-1", {})
    stage = adapter.on_stage_started(run, "ingest", {})
    adapter.on_stage_ended(stage, status="succeeded")
    adapter.on_run_ended(run, "succeeded")
    adapter.record_metric(
        "pipeline_runs_total", 1, attributes={"mode": "run"}
    )

    points = _metric_points(reader)
    # Stage completion counter and both duration histograms were emitted.
    assert "pipeline_stage_completed_total" in points
    assert "pipeline_stage_duration_seconds" in points
    assert "pipeline_run_duration_seconds" in points
    assert "pipeline_runs_total" in points


def test_unknown_metric_name_is_ignored_not_invented() -> None:
    """A typo can never silently create an unbounded, undocumented metric."""
    adapter, _, reader = _adapter()
    adapter.record_metric("totally_made_up_metric", 1)
    assert "totally_made_up_metric" not in _metric_points(reader)


def test_error_message_with_absolute_path_is_redacted_on_the_span() -> None:
    adapter, spans, _ = _adapter()
    run = adapter.on_run_started("run-1", {})
    stage = adapter.on_stage_started(run, "assemble", {})
    adapter.on_stage_ended(
        stage,
        status="failed",
        error_kind="FfmpegUnavailable",
        error_message="ffmpeg not found at /usr/local/bin/ffmpeg on this host",
    )
    adapter.on_run_ended(run, "failed")
    stage_span = next(
        s for s in spans.get_finished_spans() if s.name == "pipeline.stage.assemble"
    )
    message = stage_span.attributes.get("error.message")
    assert message is not None
    assert "/usr/local/bin/ffmpeg" not in message
    assert "<path>" in message
    assert stage_span.attributes.get("error.kind") == "FfmpegUnavailable"


def test_event_payload_is_a_span_event_with_only_safe_keys() -> None:
    adapter, spans, _ = _adapter()
    run = adapter.on_run_started("run-1", {})
    stage = adapter.on_stage_started(run, "ingest", {})
    adapter.on_event(stage, _event())
    adapter.on_stage_ended(stage, status="succeeded")
    adapter.on_run_ended(run, "succeeded")
    stage_span = next(
        s for s in spans.get_finished_spans() if s.name == "pipeline.stage.ingest"
    )
    assert len(stage_span.events) == 1
    recorded = stage_span.events[0]
    assert recorded.attributes.get("event.source_id") == "the-raven"
    assert recorded.attributes.get("event.license") == "PD-US"
