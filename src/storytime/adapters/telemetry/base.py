"""Telemetry adapter interface and OTel-free handle types.

ARCH-LOCK: Telemetry Import Boundary
DO NOT REFACTOR: This module, and every module except
storytime.adapters.telemetry.otel, must NOT import opentelemetry. Handle types
here must never carry an OTel Span object.
Rationale: Hard decision 2 of the Architecture Baseline. OpenTelemetry is a
view over local truth; if Span objects leak into handles, DTOs, or business
logic, the pipeline becomes coupled to a telemetry vendor.

Phase 5 widens the adapter so the pipeline is observability-native:

* the run/stage handles carry a *serializable* W3C ``traceparent`` string
  (never a live Span / SpanContext object), so the runner can persist it into
  SQLite and stamp it into artifact envelopes;
* ``on_run_started`` accepts ``link_traceparents`` so a resumed run can attach
  a real W3C Link to the trace it continues from -- without pretending a paused
  approval gate was one uninterrupted active span;
* ``record_metric`` lets the runner / approval service / rehydration code emit
  a small, fixed set of pipeline metrics (see
  storytime.adapters.telemetry.metrics).

Every method must remain safe under NoopTelemetry: functional behaviour never
depends on the adapter, and ``pipeline_run_id`` -- not ``trace_id`` -- is the
durable correlation key.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from storytime.events import PipelineEvent

# -- stable, low-cardinality span/metric attribute keys ----------------------
# The runner builds attribute maps with these keys; the OTel adapter writes
# them onto spans. Keeping the names here (not scattered as string literals)
# keeps docs/telemetry-map.md and the code in agreement.
ATTR_RUN_ID = "pipeline.run_id"
ATTR_STAGE = "pipeline.stage"
ATTR_STATUS = "pipeline.status"
ATTR_RESUME = "pipeline.resume"
ATTR_APPROVAL_STAGE = "pipeline.approval.stage"
ATTR_APPROVAL_DECISION = "pipeline.approval.decision"
ATTR_ERROR_KIND = "error.kind"
ATTR_ERROR_MESSAGE = "error.message"


@dataclass(frozen=True, slots=True)
class RunHandle:
    """An opaque, OTel-free reference to an in-progress run's telemetry scope.

    ``traceparent`` is the serializable W3C trace context of the run span (or
    None under NoopTelemetry). It is a *string*, never a live Span object, so
    it is safe to thread into DTOs, SQLite rows, and artifact envelopes.
    """

    pipeline_run_id: str
    handle_id: str
    trace_id: str | None = None
    traceparent: str | None = None


@dataclass(frozen=True, slots=True)
class StageHandle:
    """An opaque, OTel-free reference to an in-progress stage's telemetry scope.

    ``traceparent`` is the serializable W3C trace context of the stage span;
    the runner stamps it into the stage's output artifact envelopes so a later
    process can reconstruct the trace. None under NoopTelemetry.
    """

    pipeline_run_id: str
    stage_name: str
    handle_id: str
    trace_id: str | None = None
    span_id: str | None = None
    traceparent: str | None = None


@runtime_checkable
class TelemetryAdapter(Protocol):
    """Maps pipeline lifecycle and events onto a telemetry backend.

    The pipeline calls these hooks; the runner reads trace_id / span_id /
    traceparent off the returned handles to persist into SQLite and stamp into
    artifact envelopes. Functional behaviour must never depend on the adapter --
    NoopTelemetry is always a valid choice.
    """

    def on_run_started(
        self,
        pipeline_run_id: str,
        attributes: Mapping[str, str],
        *,
        resume: bool = False,
        link_traceparents: Sequence[str] = (),
    ) -> RunHandle:
        """Open a run-level span.

        When *resume* is true and *link_traceparents* is non-empty, the run
        span attaches a W3C Link to each prior trace instead of continuing it,
        so a long approval pause never renders as one giant active span.
        """
        ...

    def on_stage_started(
        self, run: RunHandle, stage_name: str, attributes: Mapping[str, str]
    ) -> StageHandle: ...

    def on_stage_ended(
        self,
        stage: StageHandle,
        *,
        status: str,
        error_kind: str | None = None,
        error_message: str | None = None,
        attributes: Mapping[str, str] | None = None,
    ) -> None:
        """Close a stage span.

        *attributes* carries the stage's own low-cardinality span facts
        (StageResult.span_attributes -- artifact.kind, audio.format, ...);
        the adapter sanitises them before attaching. *error_kind* /
        *error_message* are set when the stage failed.
        """
        ...

    def on_event(self, stage: StageHandle, event: PipelineEvent) -> None:
        """Add *event* to *stage*'s span as a span event (a view of event_log)."""
        ...

    def on_run_ended(self, run: RunHandle, status: str) -> None: ...

    def start_linked_run(
        self, pipeline_run_id: str, prior_traceparent: str | None
    ) -> RunHandle:
        """Open a run span that Links to *prior_traceparent* (resume helper)."""
        ...

    def record_metric(
        self,
        name: str,
        value: float = 1.0,
        *,
        attributes: Mapping[str, str] | None = None,
    ) -> None:
        """Record a metric point. Unknown metric names are ignored safely."""
        ...
