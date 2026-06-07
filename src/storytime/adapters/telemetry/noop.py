"""No-op telemetry adapter.

ARCH-LOCK: NoopTelemetry is the decoupling guarantee
DO NOT REFACTOR: NoopTelemetry must remain a complete, side-effect-free
implementation of TelemetryAdapter. The functional test suite runs against it.
Rationale: Architecture Baseline section 11 -- "deleting the OTel adapter and
running with NoopTelemetry must leave every functional test green."

Every handle NoopTelemetry returns carries trace_id / span_id / traceparent =
None. The pipeline still works because pipeline_run_id is the durable
correlation key; a None traceparent threaded through the runner, the artifact
envelope, and SQLite is treated uniformly as "no trace context".
"""

from __future__ import annotations

import itertools
from collections.abc import Mapping, Sequence

from storytime.adapters.telemetry.base import RunHandle, StageHandle
from storytime.events import PipelineEvent

_counter = itertools.count(1)


class NoopTelemetry:
    """A telemetry adapter that records nothing. The default adapter."""

    def on_run_started(
        self,
        pipeline_run_id: str,
        attributes: Mapping[str, str],
        *,
        resume: bool = False,
        link_traceparents: Sequence[str] = (),
    ) -> RunHandle:
        return RunHandle(
            pipeline_run_id=pipeline_run_id,
            handle_id=f"noop-run-{next(_counter)}",
        )

    def on_stage_started(
        self, run: RunHandle, stage_name: str, attributes: Mapping[str, str]
    ) -> StageHandle:
        return StageHandle(
            pipeline_run_id=run.pipeline_run_id,
            stage_name=stage_name,
            handle_id=f"noop-stage-{next(_counter)}",
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
        return None

    def on_event(self, stage: StageHandle, event: PipelineEvent) -> None:
        return None

    def on_run_ended(self, run: RunHandle, status: str) -> None:
        return None

    def start_linked_run(
        self, pipeline_run_id: str, prior_traceparent: str | None
    ) -> RunHandle:
        return RunHandle(
            pipeline_run_id=pipeline_run_id,
            handle_id=f"noop-linked-run-{next(_counter)}",
        )

    def record_metric(
        self,
        name: str,
        value: float = 1.0,
        *,
        attributes: Mapping[str, str] | None = None,
    ) -> None:
        return None
