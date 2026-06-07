"""PipelineRunner -- stage orchestration.

ARCH-LOCK: Persist-before-telemetry, single transaction
DO NOT REFACTOR: a stage's events and StateUpdate are persisted to SQLite in
ONE transaction BEFORE any telemetry is emitted. Telemetry is a view over
local truth, never its source, and must never gate persistence.
Rationale: Hard decision 9 and Round 7 prerequisite corrections 1-3.

Phase 3 status: execute_stage runs a single stage end-to-end with correct
telemetry + persistence wiring; run_sequence threads a list of stages,
passing each stage's output artifacts to the next.

Phase 4 status: _persist also records each stage's produced artifact keys to
the stage_artifact table (inside the same single transaction), and
resume_sequence executes the not-yet-completed tail of a stage list so an
interrupted run can be rehydrated from SQLite without regenerating completed
upstream artifacts (docs/open-issues.md, OI-10).

Phase 5 status: the runner is observability-native.

* Span shape: a sequence (run_sequence / resume_sequence) opens exactly ONE
  ``pipeline.run`` / ``pipeline.resume`` span, and every stage is a child
  ``pipeline.stage.<name>`` span -- instead of the Phase 3-4 shape of one run
  span per stage. Standalone execute_stage keeps its own one-stage run span.
* Trace propagation: after a stage runs, the runner stamps that stage's own
  span ``traceparent`` into the artifact envelopes the stage produced, and
  threads it into the next stage's StageInput.inbound_traceparent. Stages stay
  completely telemetry-unaware; the runner owns trace-context propagation.
* Linked resume: resume_sequence opens its run span with a W3C Link to the
  pre-pause trace (OI-2), so a long approval pause is a new, linked trace
  rather than one pretend-uninterrupted span.
* Metrics: each sequence records pipeline_runs_total; stage completion / failure
  counters and the duration histograms are owned by the telemetry adapter.

Everything here stays correct under NoopTelemetry: handles then carry a None
traceparent, no envelope is rewritten, and pipeline_run_id -- never trace_id --
is the durable correlation key.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace

from storytime.adapters.telemetry import RunHandle
from storytime.adapters.telemetry.base import ATTR_STAGE
from storytime.adapters.telemetry.metrics import METRIC_RUNS_TOTAL
from storytime.artifacts import (
    ArtifactEnvelopeError,
    TraceContext,
    from_json,
    to_json,
)
from storytime.dto import StageInput, StageResult, StageStatus, StateUpdate
from storytime.events import EventType, PipelineEvent
from storytime.runner.context import RunnerContext
from storytime.stages.base import Stage


@dataclass(frozen=True, slots=True)
class StageOutcome:
    """One stage's place in an executed sequence: its name and its result."""

    stage_name: str
    result: StageResult


class PipelineRunner:
    """Invokes stages and persists their results. The only orchestrator."""

    def __init__(self, ctx: RunnerContext) -> None:
        self._ctx = ctx

    @property
    def context(self) -> RunnerContext:
        return self._ctx

    def _apply_state_update(
        self, stage_input: StageInput, update: StateUpdate, *, updated_at: str
    ) -> None:
        run = self._ctx.state.get_run(stage_input.pipeline_run_id)
        if run is None:
            return
        if update.run_status is not None or update.current_stage is not None:
            self._ctx.state.update_run_state(
                stage_input.pipeline_run_id,
                status=(
                    update.run_status if update.run_status is not None else run.status
                ),
                current_stage=(
                    update.current_stage
                    if update.current_stage is not None
                    else run.current_stage
                ),
                updated_at=updated_at,
            )
        # Phase 3: translate the declarative approval / published_episode
        # intents into their tables. This runs inside the runner's single
        # transaction (see _persist), so the event_log and these rows agree.
        if update.approval is not None:
            self._ctx.state.record_approval(
                pipeline_run_id=stage_input.pipeline_run_id,
                stage_name=update.approval.stage_name,
                decision=update.approval.decision,
                operator=update.approval.operator,
                decided_at=updated_at,
                notes=update.approval.notes,
            )
        if update.published_episode is not None:
            episode = update.published_episode
            self._ctx.state.record_published_episode(
                episode_guid=episode.episode_guid,
                pipeline_run_id=stage_input.pipeline_run_id,
                title=episode.title,
                published_at=updated_at,
                audio_path=episode.audio_path,
                audio_bytes=episode.audio_bytes,
                duration_seconds=episode.duration_seconds,
                # Phase 6 (OI-11): the publish stage owns the feed-version
                # counter; the runner records the value it computed rather
                # than the Phase 3 placeholder of a constant 1.
                feed_version=episode.feed_version,
                description=episode.description,
            )
        # Phase 9B (§24.7/§24.8): record the SQLite projection of the run's
        # Trust Envelope. The ingest stage has already written the durable
        # Trust Envelope artifact (the governance source of truth); this
        # writes only the queryable projection, inside the same transaction as
        # the stage's events so the projection and the event_log agree.
        if update.trust_envelope is not None:
            te = update.trust_envelope
            self._ctx.state.record_trust_envelope(
                pipeline_run_id=stage_input.pipeline_run_id,
                source_ref=te.source_ref,
                schema_version=te.schema_version,
                license_type=te.license_type,
                decision=te.decision,
                decision_timestamp=te.decision_timestamp,
                approver_id=te.approver_id,
                blocked_reason=te.blocked_reason,
                envelope_key=te.envelope_key,
                recorded_at=updated_at,
            )

    def _persist(
        self,
        stage_input: StageInput,
        result: StageResult,
        *,
        started_at: str,
        ended_at: str,
        trace_id: str | None,
        span_id: str | None,
        parent_trace_id: str | None = None,
    ) -> None:
        """Persist events, the stage_execution row, and the StateUpdate atomically.

        *parent_trace_id* is the run span's trace id (Phase 5): persisting it on
        the stage_execution row records the run-span -> stage-span hierarchy in
        SQLite, so the trace tree is reconstructable from local truth alone.
        """
        ctx = self._ctx
        with ctx.state.transaction():
            # 1. Append-only event_log: the stage's events come first.
            ctx.state.append_events(result.events, trace_id=trace_id, span_id=span_id)
            # 2. Forensic record of this stage execution.
            ctx.state.record_stage_execution(
                pipeline_run_id=stage_input.pipeline_run_id,
                stage_name=stage_input.stage_name,
                started_at=started_at,
                ended_at=ended_at,
                status=str(result.status),
                trace_id=trace_id,
                span_id=span_id,
                parent_trace_id=parent_trace_id,
                error_kind=result.error_kind,
                error_message=result.error_message,
            )
            # 3. Persist the stage's produced artifact keys so a resumed run
            #    can rehydrate them from SQLite (Phase 4 OI-10). Keys are
            #    relative storage keys; this stays inside the one transaction.
            if result.output_artifacts:
                ctx.state.record_stage_artifacts(
                    pipeline_run_id=stage_input.pipeline_run_id,
                    stage_name=stage_input.stage_name,
                    artifact_keys=result.output_artifacts,
                    recorded_at=ended_at,
                )
            # 4. Apply the declarative StateUpdate to the run row.
            self._apply_state_update(stage_input, result.state_update, updated_at=ended_at)

    def _stamp_trace_context(
        self, stage_input: StageInput, result: StageResult, traceparent: str
    ) -> None:
        """Write this stage's span *traceparent* into its own output envelopes.

        Phase 5 trace propagation. Only an envelope whose ``stage`` field equals
        the executing stage is rewritten: an approval gate passes upstream
        envelopes straight through, and those must keep their original
        producer's trace context, not be relabelled with the gate's trace.

        Stamping is a telemetry view and must never break a run: a stamp that
        fails to read / parse / rewrite is skipped, leaving the stage-written
        envelope (carrying the inbound traceparent) intact. Under NoopTelemetry
        this method is never called -- there is no traceparent to stamp.
        """
        storage = self._ctx.storage
        for artifact_key in result.output_artifacts:
            try:
                envelope = from_json(storage.read_text(artifact_key))
            except (ArtifactEnvelopeError, FileNotFoundError, OSError):
                continue
            if envelope.stage != stage_input.stage_name:
                # A gate-passthrough (or otherwise foreign) envelope: leave it.
                continue
            stamped = replace(
                envelope,
                trace_context=TraceContext(
                    traceparent=traceparent,
                    tracestate=envelope.trace_context.tracestate,
                ),
            )
            try:
                storage.write_text(artifact_key, to_json(stamped))
            except OSError:
                continue

    def _run_failure_result(
        self, stage_input: StageInput, exc: Exception
    ) -> StageResult:
        """Convert an unexpected stage exception into a FAILED StageResult."""
        return StageResult.failed(
            error_kind=type(exc).__name__,
            error_message=str(exc),
            events=(
                PipelineEvent(
                    event_type=EventType.RUN_FAILED,
                    pipeline_run_id=stage_input.pipeline_run_id,
                    occurred_at=self._ctx.clock.now(),
                    stage_name=stage_input.stage_name,
                    payload={"error": str(exc)},
                ),
            ),
        )

    def _execute_stage_in_run(
        self,
        stage: Stage,
        stage_input: StageInput,
        run_handle: RunHandle,
    ) -> tuple[StageResult, str | None]:
        """Execute one stage as a child of an already-open run span.

        Returns the StageResult and the stage span's traceparent (None under
        NoopTelemetry). The traceparent is this stage's OUTPUT trace context:
        the caller stamps it into the stage's envelopes and threads it into the
        next stage's StageInput.inbound_traceparent.
        """
        ctx = self._ctx
        started_at = ctx.clock.now()
        stage_handle = ctx.telemetry.on_stage_started(
            run_handle, stage_input.stage_name, {}
        )

        try:
            result = stage.run(ctx, stage_input)
        except Exception as exc:  # noqa: BLE001 - converted into a FAILED result
            result = self._run_failure_result(stage_input, exc)

        ended_at = ctx.clock.now()

        # Stamp this stage's span traceparent into the envelopes it produced,
        # so a downstream process can reconstruct the trace from the artifact.
        if stage_handle.traceparent is not None:
            self._stamp_trace_context(stage_input, result, stage_handle.traceparent)

        # Persist FIRST (source of truth), then emit telemetry (the view).
        self._persist(
            stage_input,
            result,
            started_at=started_at.isoformat(),
            ended_at=ended_at.isoformat(),
            trace_id=stage_handle.trace_id,
            span_id=stage_handle.span_id,
            parent_trace_id=run_handle.trace_id,
        )
        # Span events are added to the (still-open) stage span, then the stage
        # span is closed -- on_event must precede on_stage_ended.
        for event in result.events:
            ctx.telemetry.on_event(stage_handle, event)
        ctx.telemetry.on_stage_ended(
            stage_handle,
            status=str(result.status),
            error_kind=result.error_kind,
            error_message=result.error_message,
            attributes=result.span_attributes,
        )
        return result, stage_handle.traceparent

    def execute_stage(self, stage: Stage, stage_input: StageInput) -> StageResult:
        """Execute one stage as a standalone run with its own run span.

        This is the single-stage entry point (the granular per-stage path and
        direct unit use). A sequence uses run_sequence / resume_sequence, which
        open one shared run span for all their stages.
        """
        ctx = self._ctx
        run_handle = ctx.telemetry.on_run_started(
            stage_input.pipeline_run_id, {ATTR_STAGE: stage_input.stage_name}
        )
        ctx.telemetry.record_metric(METRIC_RUNS_TOTAL, attributes={"mode": "stage"})
        result, _ = self._execute_stage_in_run(stage, stage_input, run_handle)
        ctx.telemetry.on_run_ended(run_handle, status=str(result.status))
        return result

    def run_sequence(
        self,
        stages: Sequence[Stage],
        *,
        pipeline_run_id: str,
        run_dir: str,
        first_stage_params: Mapping[str, object] | None = None,
    ) -> tuple[StageOutcome, ...]:
        """Execute *stages* in order under ONE run span, threading artifacts.

        Each stage's output_artifacts become the next stage's input_artifacts,
        and each stage's span traceparent becomes the next stage's
        inbound_traceparent (the first stage inherits the run span's). Stage
        params are passed only to the first stage. Sequencing stops at the
        first stage that does not return SUCCEEDED. This method is generic: it
        imports no concrete stage, only the Stage protocol.
        """
        ctx = self._ctx
        run_handle = ctx.telemetry.on_run_started(pipeline_run_id, {})
        ctx.telemetry.record_metric(METRIC_RUNS_TOTAL, attributes={"mode": "run"})
        outcomes = self._drive(
            stages,
            run_handle=run_handle,
            pipeline_run_id=pipeline_run_id,
            run_dir=run_dir,
            skip_stage_names=frozenset(),
            seed_artifacts=(),
            seed_traceparent=run_handle.traceparent,
            first_stage_params=first_stage_params,
            stage_params={},
            stop_after=None,
        )
        ctx.telemetry.on_run_ended(run_handle, status=_sequence_status(outcomes))
        return outcomes

    def resume_sequence(
        self,
        stages: Sequence[Stage],
        *,
        pipeline_run_id: str,
        run_dir: str,
        completed_stage_names: frozenset[str],
        seed_artifacts: tuple[str, ...],
        stage_params: Mapping[str, Mapping[str, object]] | None = None,
        stop_after: str | None = None,
        link_traceparent: str | None = None,
    ) -> tuple[StageOutcome, ...]:
        """Execute the not-yet-completed tail of *stages* for a resumed run.

        Stages whose name is in *completed_stage_names* are skipped -- their
        output artifacts are NOT regenerated. *seed_artifacts* are the output
        artifacts of the last completed stage and become the input artifacts
        of the first executed stage; thereafter artifacts thread normally.
        Per-stage params are supplied via *stage_params* (the resume engine
        uses this to inject a gate's persisted approval decision). Sequencing
        stops at the first non-SUCCEEDED result, or after the stage named
        *stop_after* (used by the granular per-stage CLI commands).

        Phase 5 / OI-2: the whole resumed tail runs under one ``pipeline.resume``
        span that carries a W3C Link to *link_traceparent* (the pre-pause
        trace), so the resume is a new, causally-linked trace rather than a
        pretend-continuous span. The first resumed stage inherits
        *link_traceparent* as its inbound_traceparent, expressing that it
        consumes artifacts produced under that prior trace.

        Like run_sequence this method is generic: it imports no concrete stage,
        only the Stage protocol.
        """
        ctx = self._ctx
        links = (link_traceparent,) if link_traceparent else ()
        run_handle = ctx.telemetry.on_run_started(
            pipeline_run_id, {}, resume=True, link_traceparents=links
        )
        ctx.telemetry.record_metric(METRIC_RUNS_TOTAL, attributes={"mode": "resume"})
        # The first resumed stage's inbound trace context is the pre-pause
        # trace it builds on; when there is none (or NoopTelemetry) it inherits
        # the resume run span's traceparent, exactly as run_sequence does.
        seed_traceparent = link_traceparent or run_handle.traceparent
        outcomes = self._drive(
            stages,
            run_handle=run_handle,
            pipeline_run_id=pipeline_run_id,
            run_dir=run_dir,
            skip_stage_names=completed_stage_names,
            seed_artifacts=seed_artifacts,
            seed_traceparent=seed_traceparent,
            first_stage_params=None,
            stage_params=stage_params or {},
            stop_after=stop_after,
        )
        ctx.telemetry.on_run_ended(run_handle, status=_sequence_status(outcomes))
        return outcomes

    def _drive(
        self,
        stages: Sequence[Stage],
        *,
        run_handle: RunHandle,
        pipeline_run_id: str,
        run_dir: str,
        skip_stage_names: frozenset[str],
        seed_artifacts: tuple[str, ...],
        seed_traceparent: str | None,
        first_stage_params: Mapping[str, object] | None,
        stage_params: Mapping[str, Mapping[str, object]],
        stop_after: str | None,
    ) -> tuple[StageOutcome, ...]:
        """Shared driver for run_sequence / resume_sequence.

        Threads both artifacts and trace context from stage to stage under the
        single open *run_handle*. ``first_stage_params`` (run_sequence) and
        ``stage_params`` (resume_sequence) are mutually exclusive in practice;
        a fresh run passes the former, a resume the latter.
        """
        outcomes: list[StageOutcome] = []
        carried_artifacts: tuple[str, ...] = seed_artifacts
        inbound_traceparent: str | None = seed_traceparent
        executed_index = 0
        for stage in stages:
            if stage.name in skip_stage_names:
                continue
            params: Mapping[str, object]
            if executed_index == 0 and first_stage_params is not None:
                params = dict(first_stage_params)
            else:
                params = dict(stage_params.get(stage.name, {}))
            stage_input = StageInput(
                pipeline_run_id=pipeline_run_id,
                stage_name=stage.name,
                run_dir=run_dir,
                inbound_traceparent=inbound_traceparent,
                input_artifacts=carried_artifacts,
                params=params,
            )
            result, stage_traceparent = self._execute_stage_in_run(
                stage, stage_input, run_handle
            )
            outcomes.append(StageOutcome(stage_name=stage.name, result=result))
            executed_index += 1
            if result.status is not StageStatus.SUCCEEDED:
                break
            carried_artifacts = result.output_artifacts
            # The next stage's inbound trace context is this stage's span.
            inbound_traceparent = stage_traceparent
            if stop_after is not None and stage.name == stop_after:
                break
        return tuple(outcomes)


def _sequence_status(outcomes: tuple[StageOutcome, ...]) -> str:
    """Summarise a sequence's outcomes into a single run-span status string.

    The run span's status is a coarse view: ``failed`` if any stage failed,
    ``awaiting_approval`` if the sequence paused at a gate, else ``succeeded``.
    pipeline_run_id and the per-stage rows in SQLite remain the precise record.
    """
    saw_pause = False
    for outcome in outcomes:
        if outcome.result.status is StageStatus.FAILED:
            return "failed"
        if outcome.result.status is StageStatus.AWAITING_APPROVAL:
            saw_pause = True
    return "awaiting_approval" if saw_pause else "succeeded"
