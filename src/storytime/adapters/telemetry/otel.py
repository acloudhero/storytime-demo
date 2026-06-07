"""OpenTelemetry telemetry adapter.

ARCH-LOCK: Sole OpenTelemetry Integration Point
DO NOT REFACTOR: This is the ONLY module in StoryTime permitted to import
opentelemetry. Do not import opentelemetry anywhere else. Do not return OTel
Span / SpanContext / Context objects from these methods -- only the OTel-free
RunHandle / StageHandle, whose trace fields are plain strings.
Rationale: Hard decision 2 of the Architecture Baseline. Confining the
dependency here keeps OpenTelemetry a swappable view over local truth.

Phase 5 status: real instrumentation foundation.

* Span hierarchy: one ``pipeline.run`` (or ``pipeline.resume``) span per run,
  one ``pipeline.stage.<name>`` child span per stage execution.
* Trace context: every handle carries a serializable W3C ``traceparent``; the
  runner persists it and stamps it into artifact envelopes.
* Linked traces: ``on_run_started(resume=True, link_traceparents=[...])``
  attaches a real W3C Link to the prior trace -- a long approval pause is a new
  linked trace, never one pretend-uninterrupted span.
* Metrics: a small fixed instrument set (storytime.adapters.telemetry.metrics)
  over a MeterProvider. Labels are low-cardinality; pipeline_run_id is never a
  metric label.

Telemetry export must never block the pipeline: a bounded BatchSpanProcessor
and a PeriodicExportingMetricReader are used by default; a collector outage
drops spans/metrics with a warning rather than stalling a run. Tests inject an
in-memory exporter / reader instead.
"""

from __future__ import annotations

import itertools
import time
from collections.abc import Mapping, Sequence
from typing import Any

# ARCH-LOCK: the opentelemetry import lives here and ONLY here.
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.metrics import Counter, Histogram
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    MetricReader,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    SimpleSpanProcessor,
    SpanExporter,
)
from opentelemetry.trace import Link, Span, SpanContext, TraceFlags

from storytime.adapters.telemetry import metrics as metric_names
from storytime.adapters.telemetry.base import (
    ATTR_ERROR_KIND,
    ATTR_ERROR_MESSAGE,
    ATTR_RESUME,
    ATTR_RUN_ID,
    ATTR_STAGE,
    ATTR_STATUS,
    RunHandle,
    StageHandle,
)
from storytime.adapters.telemetry.hygiene import sanitize
from storytime.adapters.telemetry.propagation import (
    format_traceparent,
    parse_traceparent,
)
from storytime.events import PipelineEvent

_counter = itertools.count(1)

# Event-payload keys that are known-safe to surface as span-event attributes.
# Story text, full manifests, and absolute paths are never in this set; the
# hygiene module (storytime.adapters.telemetry.hygiene) is the second-line
# backstop that redacts paths and bounds length on whatever does pass.
_SAFE_EVENT_KEYS: frozenset[str] = frozenset(
    {
        "source_id",
        "license",
        "gate",
        "operator",
        "decision",
        "tts_name",
        "tts_version",
        "audio_bytes",
        "text_bytes",
        "duration_seconds",
        "error_kind",
        "stage",
        "reason",
        "episode_guid",
        "approved_by",
    }
)


def _safe_attr_value(value: object) -> str | int | float | bool | None:
    """Coerce *value* to a bounded, hygienic span-attribute value, or None.

    Numbers and booleans pass through; strings are routed through the hygiene
    module (absolute paths redacted, length bounded); anything else is dropped.
    """
    if isinstance(value, bool | int | float):
        return value
    if isinstance(value, str):
        return sanitize(value)
    return None


class OTelTelemetry:
    """A telemetry adapter backed by OpenTelemetry traces + metrics."""

    def __init__(
        self,
        *,
        otlp_endpoint: str,
        service_name: str = "storytime",
        service_version: str = "0.0.0",
        environment: str = "local",
        deployment_slot: str = "",
        service_instance_id: str = "",
        span_exporter: SpanExporter | None = None,
        metric_reader: MetricReader | None = None,
    ) -> None:
        # Resource identity is generic and configurable: no hostname, no path,
        # no "local only" hard-coding. deployment.slot is a future-compatible
        # placeholder for Phase 7 blue/green and is omitted when unset.
        #
        # ARCH-LOCK: Resource Identity Contract (Phase 7C / 7C.1 amendment)
        # DO NOT REFACTOR: These explicitly-constructed resource attributes are
        # the AUTHORITATIVE telemetry identity. service.instance.id is pinned
        # by config to a stable slot-derived value (storytime-<slot>); it must
        # never be a container ID, PID, or hostname. Do NOT add an automatic
        # Docker/host/process resource detector, and do NOT add a resource-
        # detector package (e.g. opentelemetry-resourcedetector-docker): a
        # detector-supplied container identity would fragment the blue/green
        # service entity on every rebuild. Resource.create() merges only the
        # SDK default + the OTEL_RESOURCE_ATTRIBUTES env detector, and the
        # explicit attributes below are merged last, so they always win.
        resource_attrs: dict[str, Any] = {
            "service.name": service_name,
            "service.version": service_version,
            "deployment.environment": environment,
        }
        if deployment_slot:
            resource_attrs["deployment.slot"] = deployment_slot
        if service_instance_id:
            resource_attrs["service.instance.id"] = service_instance_id
        resource = Resource.create(resource_attrs)

        # -- traces ----------------------------------------------------------
        provider = TracerProvider(resource=resource)
        if span_exporter is not None:
            # Test / introspection path: synchronous, immediate export.
            provider.add_span_processor(SimpleSpanProcessor(span_exporter))
        else:
            # Default: bounded batch processor over OTLP/HTTP. Export must
            # never block pipeline progress (Architecture Baseline 11/16).
            provider.add_span_processor(
                BatchSpanProcessor(
                    OTLPSpanExporter(endpoint=f"{otlp_endpoint}/v1/traces")
                )
            )
        self._provider = provider
        self._tracer = provider.get_tracer("storytime.pipeline")

        # -- metrics ---------------------------------------------------------
        if metric_reader is not None:
            reader: MetricReader = metric_reader
        else:
            reader = PeriodicExportingMetricReader(
                OTLPMetricExporter(endpoint=f"{otlp_endpoint}/v1/metrics")
            )
        self._meter_provider = MeterProvider(
            resource=resource, metric_readers=[reader]
        )
        meter = self._meter_provider.get_meter("storytime.pipeline")
        self._counters: dict[str, Counter] = {
            name: meter.create_counter(name)
            for name in sorted(metric_names.COUNTER_METRICS)
        }
        self._histograms: dict[str, Histogram] = {
            name: meter.create_histogram(name)
            for name in sorted(metric_names.HISTOGRAM_METRICS)
        }

        # handle_id -> live span. Spans never leave this module.
        self._spans: dict[str, Span] = {}
        # handle_id -> monotonic start time, for duration histograms.
        self._started_at: dict[str, float] = {}

    # -- span identity helpers ----------------------------------------------

    def _register(self, span: Span, prefix: str) -> str:
        handle_id = f"{prefix}-{next(_counter)}"
        self._spans[handle_id] = span
        self._started_at[handle_id] = time.monotonic()
        return handle_id

    @staticmethod
    def _ids(span: Span) -> tuple[str, str]:
        ctx = span.get_span_context()
        return (format(ctx.trace_id, "032x"), format(ctx.span_id, "016x"))

    @staticmethod
    def _traceparent(span: Span) -> str:
        ctx = span.get_span_context()
        return format_traceparent(
            format(ctx.trace_id, "032x"),
            format(ctx.span_id, "016x"),
            sampled=ctx.trace_flags.sampled,
        )

    @staticmethod
    def _links(link_traceparents: Sequence[str]) -> list[Link]:
        """Build W3C Links from prior traceparents, skipping invalid ones."""
        links: list[Link] = []
        for raw in link_traceparents:
            parsed = parse_traceparent(raw)
            if parsed is None:
                continue
            span_context = SpanContext(
                trace_id=int(parsed.trace_id, 16),
                span_id=int(parsed.span_id, 16),
                is_remote=True,
                trace_flags=TraceFlags(int(parsed.flags, 16)),
            )
            links.append(Link(span_context, attributes={"storytime.link": "resume"}))
        return links

    # -- run / stage lifecycle ----------------------------------------------

    def on_run_started(
        self,
        pipeline_run_id: str,
        attributes: Mapping[str, str],
        *,
        resume: bool = False,
        link_traceparents: Sequence[str] = (),
    ) -> RunHandle:
        span_name = "pipeline.resume" if resume else "pipeline.run"
        span_attributes: dict[str, Any] = {
            ATTR_RUN_ID: pipeline_run_id,
            ATTR_RESUME: "true" if resume else "false",
        }
        span_attributes.update(self._clean(attributes))
        span = self._tracer.start_span(
            span_name,
            attributes=span_attributes,
            links=self._links(link_traceparents),
        )
        handle_id = self._register(span, "otel-run")
        trace_id, _ = self._ids(span)
        return RunHandle(
            pipeline_run_id=pipeline_run_id,
            handle_id=handle_id,
            trace_id=trace_id,
            traceparent=self._traceparent(span),
        )

    def on_stage_started(
        self, run: RunHandle, stage_name: str, attributes: Mapping[str, str]
    ) -> StageHandle:
        parent = self._spans.get(run.handle_id)
        ctx = trace.set_span_in_context(parent) if parent is not None else None
        span_attributes: dict[str, Any] = {
            ATTR_RUN_ID: run.pipeline_run_id,
            ATTR_STAGE: stage_name,
        }
        span_attributes.update(self._clean(attributes))
        span = self._tracer.start_span(
            f"pipeline.stage.{stage_name}",
            context=ctx,
            attributes=span_attributes,
        )
        handle_id = self._register(span, "otel-stage")
        trace_id, span_id = self._ids(span)
        return StageHandle(
            pipeline_run_id=run.pipeline_run_id,
            stage_name=stage_name,
            handle_id=handle_id,
            trace_id=trace_id,
            span_id=span_id,
            traceparent=self._traceparent(span),
        )

    def on_stage_ended(
        self,
        stage: StageHandle,
        *,
        status: str,
        error_kind: str | None = None,
        error_message: str | None = None,
        attributes: Mapping[str, str] | None = None,
    ) -> None:
        span = self._spans.pop(stage.handle_id, None)
        started = self._started_at.pop(stage.handle_id, None)
        if span is None:
            return
        span.set_attribute(ATTR_STATUS, status)
        # Stage-contributed, low-cardinality facts (artifact.kind, audio.format,
        # tts.adapter, rss.item_count, ...). Routed through hygiene like any
        # other string attribute.
        for key, value in self._clean(attributes or {}).items():
            span.set_attribute(key, value)
        if error_kind is not None:
            span.set_attribute(ATTR_ERROR_KIND, error_kind)
        if error_message is not None:
            sanitized = sanitize(error_message) or ""
            span.set_attribute(ATTR_ERROR_MESSAGE, sanitized)
            span.set_status(trace.Status(trace.StatusCode.ERROR, sanitized))
        span.end()

        # Stage-level metrics. Labels stay low-cardinality (stage name only).
        stage_attrs = {ATTR_STAGE: stage.stage_name}
        if status == "succeeded":
            self._add(metric_names.METRIC_STAGE_COMPLETED_TOTAL, 1.0, stage_attrs)
        elif status == "failed":
            self._add(metric_names.METRIC_STAGE_FAILED_TOTAL, 1.0, stage_attrs)
        if started is not None:
            self._record_hist(
                metric_names.METRIC_STAGE_DURATION_SECONDS,
                time.monotonic() - started,
                stage_attrs,
            )

    def on_event(self, stage: StageHandle, event: PipelineEvent) -> None:
        span = self._spans.get(stage.handle_id)
        if span is None:
            return
        attributes: dict[str, Any] = {
            ATTR_RUN_ID: event.pipeline_run_id,
            ATTR_STAGE: event.stage_name,
        }
        for key, value in event.payload.items():
            if key not in _SAFE_EVENT_KEYS:
                continue
            coerced = _safe_attr_value(value)
            if coerced is not None:
                attributes[f"event.{key}"] = coerced
        span.add_event(str(event.event_type), attributes=attributes)

    def on_run_ended(self, run: RunHandle, status: str) -> None:
        span = self._spans.pop(run.handle_id, None)
        started = self._started_at.pop(run.handle_id, None)
        if span is not None:
            span.set_attribute(ATTR_STATUS, status)
            span.end()
        if started is not None:
            self._record_hist(
                metric_names.METRIC_RUN_DURATION_SECONDS,
                time.monotonic() - started,
                {ATTR_STATUS: status},
            )
        # Flush so a short-lived CLI process does not drop spans on exit.
        self._provider.force_flush()
        self._meter_provider.force_flush()

    def start_linked_run(
        self, pipeline_run_id: str, prior_traceparent: str | None
    ) -> RunHandle:
        """Open a resume run span Linked to *prior_traceparent*.

        A resume is always a new trace; the Link expresses the causal relation
        to the pre-pause trace without pretending the gap was one active span.
        """
        links = [prior_traceparent] if prior_traceparent else []
        return self.on_run_started(
            pipeline_run_id, {}, resume=True, link_traceparents=links
        )

    # -- metrics -------------------------------------------------------------

    def record_metric(
        self,
        name: str,
        value: float = 1.0,
        *,
        attributes: Mapping[str, str] | None = None,
    ) -> None:
        attrs = dict(attributes or {})
        if name in self._counters:
            self._add(name, value, attrs)
        elif name in self._histograms:
            self._record_hist(name, value, attrs)
        # Unknown metric names are ignored: a typo can never silently create
        # an unbounded, undocumented instrument.

    def _add(self, name: str, value: float, attributes: Mapping[str, str]) -> None:
        counter = self._counters.get(name)
        if counter is not None:
            counter.add(value, dict(attributes))

    def _record_hist(
        self, name: str, value: float, attributes: Mapping[str, str]
    ) -> None:
        histogram = self._histograms.get(name)
        if histogram is not None:
            histogram.record(value, dict(attributes))

    # -- helpers / lifecycle -------------------------------------------------

    @staticmethod
    def _clean(attributes: Mapping[str, str]) -> dict[str, str]:
        """Sanitise attribute values: redact absolute paths, bound length.

        The single hygiene choke point for span / span-event string
        attributes (storytime.adapters.telemetry.hygiene).
        """
        cleaned: dict[str, str] = {}
        for key, value in attributes.items():
            sanitised = sanitize(str(value))
            if sanitised is not None:
                cleaned[key] = sanitised
        return cleaned

    def shutdown(self) -> None:
        """Flush and shut down both providers. Safe to call once at process end."""
        self._provider.shutdown()
        self._meter_provider.shutdown()
