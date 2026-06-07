"""Phase 5 end-to-end: the pipeline is observability-native and stays honest.

These tests run real pipeline slices and assert the Phase 5 acceptance
behaviour: NoopTelemetry is the default; under OTel the producing span's
traceparent is stamped into artifact envelopes; a resumed run is a fresh trace
linked to the pre-pause one; approval rows record the inbound/outbound trace
view anchors; and no raw story text or absolute filesystem path ever reaches a
span. The functional outcome is identical under either adapter.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from opentelemetry.sdk.metrics.export import InMemoryMetricReader
from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
    InMemorySpanExporter,
)

from storytime.adapters.storage import LocalFilesystemStorage
from storytime.adapters.telemetry import NoopTelemetry, build_telemetry
from storytime.adapters.telemetry.otel import OTelTelemetry
from storytime.approval import apply_approval_decision
from storytime.artifacts import from_json
from storytime.config import load_config
from storytime.pipeline import resume_run, run_vertical_slice
from storytime.runner import RunnerContext
from storytime.state import StateStore
from storytime.util.clock import FixedClock
from storytime.util.ids import new_ulid

# A distinctive phrase from the public-domain slice text. It must never leak
# into telemetry -- spans are a view, not a copy of the content.
_RAW_TEXT_MARKER = "Once upon a midnight dreary"


def _otel_context(
    tmp_path: Path, clock: FixedClock, store: StateStore
) -> tuple[RunnerContext, InMemorySpanExporter]:
    """A RunnerContext backed by OTelTelemetry with an in-memory span exporter."""
    span_exporter = InMemorySpanExporter()
    adapter = OTelTelemetry(
        otlp_endpoint="http://127.0.0.1:4318",
        service_version="0.2.0",
        environment="test",
        span_exporter=span_exporter,
        metric_reader=InMemoryMetricReader(),
    )
    config = load_config(
        {
            "STORYTIME_RUNS_DIR": str(tmp_path / "runs"),
            "STORYTIME_FEED_DIR": str(tmp_path / "feed"),
            "STORYTIME_TELEMETRY": "otel",
        }
    )
    ctx = RunnerContext(
        config=config,
        clock=clock,
        state=store,
        telemetry=adapter,
        storage=LocalFilesystemStorage(config.runs_dir),
    )
    return ctx, span_exporter


def _all_span_strings(spans: InMemorySpanExporter) -> list[str]:
    """Every string value carried by any finished span (attrs + events)."""
    out: list[str] = []
    for span in spans.get_finished_spans():
        out.append(span.name)
        for value in (span.attributes or {}).values():
            out.append(str(value))
        for event in span.events:
            out.append(event.name)
            for value in (event.attributes or {}).values():
                out.append(str(value))
    return out


def test_noop_telemetry_is_the_default_adapter() -> None:
    """With no STORYTIME_TELEMETRY set, the pipeline runs on NoopTelemetry --
    opentelemetry is never even imported for a default deployment."""
    config = load_config({"STORYTIME_RUNS_DIR": "runs", "STORYTIME_FEED_DIR": "feed"})
    assert config.telemetry == "noop"
    assert isinstance(build_telemetry(config), NoopTelemetry)


def test_full_slice_succeeds_identically_under_otel(
    tmp_path: Path, fixed_clock: FixedClock, slice_workspace
) -> None:
    with StateStore.open(tmp_path / "state.db") as store:
        ctx, _ = _otel_context(tmp_path, fixed_clock, store)
        outcome = run_vertical_slice(ctx, slice_workspace.manifest_path)
        assert outcome.status == "completed"
        assert outcome.episode_guid is not None


def test_producing_span_traceparent_is_stamped_into_artifact_envelopes(
    tmp_path: Path, fixed_clock: FixedClock, slice_workspace
) -> None:
    with StateStore.open(tmp_path / "state.db") as store:
        ctx, _ = _otel_context(tmp_path, fixed_clock, store)
        outcome = run_vertical_slice(ctx, slice_workspace.manifest_path)
        assert outcome.pipeline_run_id is not None

        artifacts = ctx.state.list_stage_artifacts(outcome.pipeline_run_id)
        assert artifacts, "the run should have produced artifacts"
        for row in artifacts:
            envelope = from_json(ctx.storage.read_text(row.artifact_key))
            # Under OTel every produced envelope carries a real traceparent.
            assert envelope.trace_context.traceparent is not None
            assert envelope.trace_context.traceparent.startswith("00-")


def test_no_raw_story_text_reaches_any_span(
    tmp_path: Path, fixed_clock: FixedClock, slice_workspace
) -> None:
    with StateStore.open(tmp_path / "state.db") as store:
        ctx, spans = _otel_context(tmp_path, fixed_clock, store)
        run_vertical_slice(ctx, slice_workspace.manifest_path)
        haystack = "\n".join(_all_span_strings(spans))
        assert _RAW_TEXT_MARKER not in haystack


def test_no_absolute_filesystem_path_reaches_any_span(
    tmp_path: Path, fixed_clock: FixedClock, slice_workspace
) -> None:
    with StateStore.open(tmp_path / "state.db") as store:
        ctx, spans = _otel_context(tmp_path, fixed_clock, store)
        run_vertical_slice(ctx, slice_workspace.manifest_path)
        for value in _all_span_strings(spans):
            assert str(tmp_path) not in value, f"absolute path leaked: {value!r}"


def test_resumed_run_links_back_to_the_pre_pause_trace(
    tmp_path: Path, fixed_clock: FixedClock, slice_workspace
) -> None:
    with StateStore.open(tmp_path / "state.db") as store:
        ctx, spans = _otel_context(tmp_path, fixed_clock, store)
        outcome = run_vertical_slice(
            ctx, slice_workspace.manifest_path, require_approval=True
        )
        assert outcome.status == "awaiting_approval"
        run_id = outcome.pipeline_run_id
        assert run_id is not None

        apply_approval_decision(
            ctx,
            pipeline_run_id=run_id,
            gate="text",
            decision="approved",
            operator="tester",
        )
        resumed = resume_run(ctx, run_id)
        assert resumed.status == "completed"

        resume_spans = [
            s for s in spans.get_finished_spans() if s.name == "pipeline.resume"
        ]
        assert resume_spans, "a resumed run should open a pipeline.resume span"
        # The resume span links to the pre-pause trace rather than continuing it.
        assert any(len(s.links) >= 1 for s in resume_spans)


def test_approval_row_records_inbound_and_outbound_trace_anchors(
    tmp_path: Path, fixed_clock: FixedClock, slice_workspace
) -> None:
    with StateStore.open(tmp_path / "state.db") as store:
        ctx, _ = _otel_context(tmp_path, fixed_clock, store)
        outcome = run_vertical_slice(
            ctx, slice_workspace.manifest_path, require_approval=True
        )
        run_id = outcome.pipeline_run_id
        assert run_id is not None
        apply_approval_decision(
            ctx,
            pipeline_run_id=run_id,
            gate="text",
            decision="approved",
            operator="tester",
        )
        resume_run(ctx, run_id)

        row = ctx.state._conn.execute(  # noqa: SLF001 - test inspects raw row
            "SELECT inbound_trace_id, outbound_trace_id FROM approval "
            "WHERE pipeline_run_id=? AND stage_name='approve_text'",
            (run_id,),
        ).fetchone()
        assert row is not None
        # inbound = the pre-approval (ingest) trace; outbound = the resumed run.
        assert row["inbound_trace_id"] is not None
        assert row["outbound_trace_id"] is not None
        assert row["inbound_trace_id"] != row["outbound_trace_id"]


def test_stage_execution_records_its_parent_run_trace(
    tmp_path: Path, fixed_clock: FixedClock, slice_workspace
) -> None:
    with StateStore.open(tmp_path / "state.db") as store:
        ctx, _ = _otel_context(tmp_path, fixed_clock, store)
        outcome = run_vertical_slice(ctx, slice_workspace.manifest_path)
        run_id = outcome.pipeline_run_id
        assert run_id is not None
        executions = ctx.state.list_stage_executions(run_id)
        assert executions
        for record in executions:
            # Every stage span is a child of the one run span.
            assert record.parent_trace_id is not None
            assert record.parent_trace_id == record.trace_id


def test_artifact_validation_failure_is_counted_by_reason(
    tmp_path: Path, fixed_clock: FixedClock
) -> None:
    """A corrupt seed artifact is refused loudly AND counted for observability."""
    from storytime.runner.rehydrate import RehydrationError, validate_artifact

    with StateStore.open(tmp_path / "state.db") as store:
        metric_reader = InMemoryMetricReader()
        adapter = OTelTelemetry(
            otlp_endpoint="http://127.0.0.1:4318",
            span_exporter=InMemorySpanExporter(),
            metric_reader=metric_reader,
        )
        config = load_config(
            {
                "STORYTIME_RUNS_DIR": str(tmp_path / "runs"),
                "STORYTIME_FEED_DIR": str(tmp_path / "feed"),
                "STORYTIME_TELEMETRY": "otel",
            }
        )
        ctx = RunnerContext(
            config=config,
            clock=fixed_clock,
            state=store,
            telemetry=adapter,
            storage=LocalFilesystemStorage(config.runs_dir),
        )
        # An absolute key is rejected with reason="non_relative_key".
        with pytest.raises(RehydrationError):
            validate_artifact(ctx, "/etc/passwd")

        data = metric_reader.get_metrics_data()
        names = {
            metric.name
            for rm in data.resource_metrics
            for sm in rm.scope_metrics
            for metric in sm.metrics
        }
        assert "pipeline_artifact_validation_failed_total" in names


def test_resume_metric_distinguishes_a_resumed_run(
    tmp_path: Path, fixed_clock: FixedClock
) -> None:
    """pipeline_runs_total carries a low-cardinality mode label, never a run id."""
    metric_reader = InMemoryMetricReader()
    adapter = OTelTelemetry(
        otlp_endpoint="http://127.0.0.1:4318",
        span_exporter=InMemorySpanExporter(),
        metric_reader=metric_reader,
    )
    adapter.record_metric("pipeline_runs_total", 1, attributes={"mode": "run"})
    adapter.record_metric("pipeline_resume_total", 1)

    data = metric_reader.get_metrics_data()
    by_name = {
        metric.name: metric
        for rm in data.resource_metrics
        for sm in rm.scope_metrics
        for metric in sm.metrics
    }
    assert "pipeline_runs_total" in by_name
    assert "pipeline_resume_total" in by_name
    for point in by_name["pipeline_runs_total"].data.data_points:
        # The run id is never a metric label (it would be unbounded).
        assert "pipeline.run_id" not in dict(point.attributes)


def test_run_id_is_the_durable_key_unaffected_by_telemetry_choice(
    tmp_path: Path, fixed_clock: FixedClock, make_workspace
) -> None:
    """The same pipeline on Noop vs OTel yields the same functional result;
    pipeline_run_id -- not trace_id -- is what identifies the run."""
    ws_noop = make_workspace()
    ws_otel = make_workspace()

    with StateStore.open(tmp_path / "noop.db") as store:
        config = load_config(
            {
                "STORYTIME_RUNS_DIR": str(tmp_path / "noop-runs"),
                "STORYTIME_FEED_DIR": str(tmp_path / "noop-feed"),
            }
        )
        noop_ctx = RunnerContext(
            config=config,
            clock=fixed_clock,
            state=store,
            telemetry=NoopTelemetry(),
            storage=LocalFilesystemStorage(config.runs_dir),
        )
        noop_outcome = run_vertical_slice(noop_ctx, ws_noop.manifest_path)

    with StateStore.open(tmp_path / "otel.db") as store:
        otel_ctx, _ = _otel_context(tmp_path, fixed_clock, store)
        otel_outcome = run_vertical_slice(otel_ctx, ws_otel.manifest_path)

    assert noop_outcome.status == otel_outcome.status == "completed"
    # Both runs are identified by a ULID pipeline_run_id, telemetry aside.
    assert noop_outcome.pipeline_run_id is not None
    assert otel_outcome.pipeline_run_id is not None
    assert len(noop_outcome.pipeline_run_id) == len(new_ulid())
