"""Vertical-slice composition root.

This module is the application wiring for the StoryTime vertical slice. It is
deliberately NOT the orchestrator: the PipelineRunner sequences stages
(Architecture Baseline section 9). This module builds the concrete stage list
with its injected adapters, creates or rehydrates the pipeline run, and hands
the stages to the runner.

Phase 3 slice: one approved text in -> one WAV -> one MP3 -> one RSS item ->
one traceable journey persisted in SQLite.

Phase 4 added an opt-in, persisted interactive text approval gate and
``resume_run`` — rehydrating a paused / partially completed run from SQLite
and continuing it without regenerating completed upstream artifacts
(docs/open-issues.md, OI-9 and OI-10).

Phase 4.1 wires the audio approval gate as a second, independent opt-in gate
(OI-13). A run records which gates it was created with on its pipeline_run
row; resume rebuilds that exact stage list — including a gate not yet reached.
``require_approval`` keeps its Phase 4 meaning (the text gate only), so Phase 4
behaviour and tests are unchanged.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from email.utils import format_datetime
from pathlib import Path

from storytime.adapters.storage import LocalFilesystemStorage
from storytime.adapters.telemetry import build_telemetry
from storytime.adapters.tts import MockTTS, TTSAdapter
from storytime.approval import apply_approval_decision
from storytime.artifacts import from_json
from storytime.config import StoryTimeConfig
from storytime.dto import StageStatus
from storytime.events import EventType, PipelineEvent
from storytime.manifest import ManifestValidationError, load_manifest
from storytime.rss import FeedItem
from storytime.runner import (
    GateResumeSpec,
    PipelineRunner,
    RunnerContext,
    StageOutcome,
    build_resume_plan,
    load_run_or_raise,
)
from storytime.runner.rehydrate import RehydrationError
from storytime.stages.approve import ApprovalGateStage, audio_approval_gate, text_approval_gate
from storytime.stages.assemble import AssembleStage
from storytime.stages.base import Stage
from storytime.stages.encode import FfmpegMp3Encoder, Mp3Encoder
from storytime.stages.ingest import IngestStage
from storytime.stages.publish import PublishStage
from storytime.stages.synthesize import SynthesizeStage
from storytime.state import RunRecord, StateStore
from storytime.util.clock import SystemClock
from storytime.util.hashing import sha256_file
from storytime.util.ids import new_ulid

# ARCH-LOCK: Canonical stage order
# DO NOT REFACTOR: the four pipeline stages always run in this order
# (Architecture Baseline section 9). Approval gates are real persisted stages
# woven into this order at fixed positions (see _Gate.after_stage); they are
# the only optional stages, and a run records which ones it used.
BASE_STAGE_ORDER: tuple[str, ...] = ("ingest", "synthesize", "assemble", "publish")


@dataclass(frozen=True, slots=True)
class _Gate:
    """Static description of one interactive approval gate.

    label is the operator-facing name ("text" / "audio"); stage_name is the
    gate's stage / approval-row name; after_stage is the BASE_STAGE_ORDER stage
    the gate immediately follows; requested_event is its *_APPROVAL_REQUESTED
    event type; factory builds the (generic) gate stage.
    """

    label: str
    stage_name: str
    after_stage: str
    requested_event: str
    factory: Callable[[], ApprovalGateStage]


# The two gates StoryTime supports. The text gate pauses between ingest and
# synthesize; the audio gate pauses between synthesize and assemble. Each is
# independently opt-in (Phase 4.1, OI-13).
_GATES: tuple[_Gate, ...] = (
    _Gate(
        label="text",
        stage_name="approve_text",
        after_stage="ingest",
        requested_event=str(EventType.TEXT_APPROVAL_REQUESTED),
        factory=text_approval_gate,
    ),
    _Gate(
        label="audio",
        stage_name="approve_audio",
        after_stage="synthesize",
        requested_event=str(EventType.AUDIO_APPROVAL_REQUESTED),
        factory=audio_approval_gate,
    ),
)
_GATE_BY_LABEL: dict[str, _Gate] = {gate.label: gate for gate in _GATES}
# The set of gate labels accepted on run-creation / the CLI.
VALID_GATE_LABELS: tuple[str, ...] = tuple(_GATE_BY_LABEL)


def canonical_stage_order(gates: Sequence[str]) -> tuple[str, ...]:
    """Return the ordered stage-name list for a run configured with *gates*.

    Each enabled gate's stage name is woven in immediately after the base
    stage it follows. With no gates this is exactly BASE_STAGE_ORDER. Resume
    and the rehydration prefix check reason about this run-specific order.
    """
    enabled = set(gates)
    order: list[str] = []
    for base in BASE_STAGE_ORDER:
        order.append(base)
        for gate in _GATES:
            if gate.after_stage == base and gate.label in enabled:
                order.append(gate.stage_name)
    return tuple(order)


@dataclass(frozen=True, slots=True)
class SliceOutcome:
    """The result of attempting to run or resume the vertical slice.

    status is one of:
      * "completed"          — every stage succeeded; the run is finished.
      * "awaiting_approval"  — the run paused at an approval gate and exited
                               cleanly; awaiting_gate names the gate.
      * "stage_completed"    — a granular per-stage resume finished its target
                               stage successfully; last_stage names it.
      * "failed"             — a stage returned FAILED (a gate rejection is a
                               FAILED result of the gate stage).
      * "rejected"           — the manifest failed pre-flight validation and no
                               run was ever created.
    """

    status: str
    pipeline_run_id: str | None = None
    failed_stage: str | None = None
    error_kind: str | None = None
    error_message: str | None = None
    episode_guid: str | None = None
    feed_path: str | None = None
    awaiting_gate: str | None = None
    last_stage: str | None = None
    messages: tuple[str, ...] = field(default_factory=tuple)


def build_runtime_context(config: StoryTimeConfig) -> RunnerContext:
    """Wire a RunnerContext from *config*.

    The caller owns the returned context's StateStore and must close it.
    """
    state = StateStore.open(config.state_db_path)
    return RunnerContext(
        config=config,
        clock=SystemClock(),
        state=state,
        telemetry=build_telemetry(config),
        storage=LocalFilesystemStorage(config.runs_dir),
    )


def _gate_label(gate_stage_name: str) -> str:
    """Map a gate stage name ("approve_text") to its operator label ("text")."""
    return gate_stage_name.removeprefix("approve_")


def _resolve_gates(
    *, require_approval: bool, require_audio_approval: bool, auto_approve: bool
) -> tuple[str, ...]:
    """Resolve the ordered gate-label tuple for a new run from the flags.

    The text gate is enabled by --require-approval or --auto-approve (its
    Phase 4 meaning, unchanged). The audio gate is enabled, independently, by
    --require-audio-approval. --auto-approve later satisfies whichever gates
    the run ended up with.
    """
    enabled: list[str] = []
    if require_approval or auto_approve:
        enabled.append("text")
    if require_audio_approval:
        enabled.append("audio")
    # Preserve canonical label order regardless of flag order.
    return tuple(gate.label for gate in _GATES if gate.label in enabled)


class StateEpisodeCatalog:
    """An EpisodeCatalog backed by the run's SQLite state store.

    This is the composition-root half of the OI-11 boundary: the publish stage
    depends only on the EpisodeCatalog Protocol, and this concrete adapter —
    living in the wiring module, which is allowed to know both the state store
    and the feed domain — translates persisted published_episode rows into the
    feed-domain FeedItem value type. The publish stage therefore aggregates a
    multi-item feed without ever importing storytime.state.
    """

    def __init__(self, state: StateStore) -> None:
        self._state = state

    @staticmethod
    def _to_rfc822(stored: str) -> str:
        """Convert a stored ISO-8601 published_at into an RSS RFC-822 pubDate.

        The runner persists published_at via datetime.isoformat(); RSS pubDate
        is RFC 822. A value that cannot be parsed (it never should be) is
        passed through unchanged rather than failing the whole feed build.
        """
        try:
            return format_datetime(datetime.fromisoformat(stored))
        except ValueError:
            return stored

    def published_feed_items(self) -> tuple[FeedItem, ...]:
        """Return every previously published episode as a FeedItem, newest first."""
        return tuple(
            FeedItem(
                guid=record.episode_guid,
                title=record.title,
                description=record.description,
                audio_url=record.audio_path,
                audio_bytes=record.audio_bytes,
                duration_seconds=record.duration_seconds,
                published_at=self._to_rfc822(record.published_at),
            )
            for record in self._state.list_published_episodes()
        )


def _build_stages(
    ctx: RunnerContext,
    *,
    episode_title: str,
    episode_description: str,
    tts: TTSAdapter | None,
    encoder: Mp3Encoder | None,
    gates: Sequence[str],
) -> tuple[Stage, ...]:
    """Build the concrete stage list with injected, swappable adapters.

    Each enabled approval gate is woven in after the base stage it follows, so
    the concrete stage list matches canonical_stage_order(gates). With no
    gates this is the exact Phase 3 four-stage slice.
    """
    feed_storage = LocalFilesystemStorage(ctx.config.feed_dir)
    enabled = set(gates)
    base_stages: dict[str, Stage] = {
        "ingest": IngestStage(),
        "synthesize": SynthesizeStage(tts if tts is not None else MockTTS()),
        "assemble": AssembleStage(
            encoder if encoder is not None else FfmpegMp3Encoder.autodetect(),
            episode_title=episode_title,
            episode_description=episode_description,
        ),
        "publish": PublishStage(
            feed_storage,
            channel_title="StoryTime",
            channel_link=(
                f"http://{ctx.config.http_host}:{ctx.config.http_port}/feed.xml"
            ),
            channel_description="StoryTime — local-first public-domain audio.",
            # Phase 6 (OI-11): the read-only catalog of prior episodes, backed
            # by the run's state store. PublishStage aggregates these into a
            # multi-item feed without ever importing storytime.state itself.
            episode_catalog=StateEpisodeCatalog(ctx.state),
        ),
    }
    stages: list[Stage] = []
    for base in BASE_STAGE_ORDER:
        stages.append(base_stages[base])
        for gate in _GATES:
            if gate.after_stage == base and gate.label in enabled:
                stages.append(gate.factory())
    return tuple(stages)


def _episode_metadata_from_state(
    ctx: RunnerContext, pipeline_run_id: str
) -> tuple[str, str]:
    """Reconstruct (episode_title, episode_description) from persisted state.

    On resume the source manifest is not re-supplied: the episode title and
    author come from the ingest artifact envelope's producer block, and the
    review notes from the ingest approval row. This keeps resume honest —
    metadata is rehydrated from SQLite + artifacts, never re-derived from a
    manifest path that may have moved.
    """
    ingest_keys = [
        row.artifact_key
        for row in ctx.state.list_stage_artifacts(pipeline_run_id)
        if row.stage_name == "ingest"
    ]
    title = ""
    author = ""
    if ingest_keys:
        envelope = from_json(ctx.storage.read_text(ingest_keys[0]))
        title = envelope.producer.get("title", "")
        author = envelope.producer.get("author", "")
    ingest_approval = ctx.state.latest_approval(pipeline_run_id, "ingest")
    review_notes = (
        ingest_approval.notes if ingest_approval and ingest_approval.notes else ""
    )
    description = f"{title} by {author}. {review_notes}".strip()
    return title, description


def _summarise(
    ctx: RunnerContext,
    pipeline_run_id: str,
    outcomes: tuple[StageOutcome, ...],
    *,
    stop_after: str | None = None,
) -> SliceOutcome:
    """Translate a sequence of StageOutcomes into a SliceOutcome."""
    for outcome in outcomes:
        if outcome.result.status is StageStatus.FAILED:
            return SliceOutcome(
                status="failed",
                pipeline_run_id=pipeline_run_id,
                failed_stage=outcome.stage_name,
                error_kind=outcome.result.error_kind,
                error_message=outcome.result.error_message,
            )
        if outcome.result.status is StageStatus.AWAITING_APPROVAL:
            return SliceOutcome(
                status="awaiting_approval",
                pipeline_run_id=pipeline_run_id,
                awaiting_gate=_gate_label(outcome.stage_name),
            )

    last_stage = outcomes[-1].stage_name if outcomes else None
    if last_stage == "publish" or stop_after is None:
        published = (
            outcomes[-1].result.state_update.published_episode if outcomes else None
        )
        return SliceOutcome(
            status="completed",
            pipeline_run_id=pipeline_run_id,
            episode_guid=published.episode_guid if published is not None else None,
            feed_path=str(ctx.config.feed_dir / "feed.xml"),
            last_stage=last_stage,
        )
    return SliceOutcome(
        status="stage_completed",
        pipeline_run_id=pipeline_run_id,
        last_stage=last_stage,
    )


def run_vertical_slice(
    ctx: RunnerContext,
    manifest_path: Path,
    *,
    tts: TTSAdapter | None = None,
    encoder: Mp3Encoder | None = None,
    require_approval: bool = False,
    require_audio_approval: bool = False,
    auto_approve: bool = False,
) -> SliceOutcome:
    """Run the vertical slice for one manifest.

    With every gate flag False this is the exact Phase 3 slice: ingest ->
    synthesize -> assemble -> publish, end to end.

    *require_approval* inserts the persisted text approval gate after ingest;
    *require_audio_approval* inserts the audio approval gate after synthesize.
    Either gate pauses the run cleanly with status "awaiting_approval". The two
    are independent: a run may use neither, one, or both.

    *auto_approve* inserts the text gate and then satisfies every gate the run
    has with a real, persisted approval decision (operator "auto-approve"),
    looping until the run finishes — a local convenience that still writes
    genuine approval rows and TextApproved / AudioApproved events, never an
    in-memory bypass.
    """
    # 1. Pre-flight: an invalid manifest is rejected before a run is created.
    try:
        manifest = load_manifest(manifest_path)
    except ManifestValidationError as exc:
        return SliceOutcome(
            status="rejected",
            error_kind="ManifestInvalid",
            error_message="; ".join(exc.messages),
            messages=tuple(exc.messages),
        )

    gates = _resolve_gates(
        require_approval=require_approval,
        require_audio_approval=require_audio_approval,
        auto_approve=auto_approve,
    )

    # 2. Create the pipeline run. pipeline_run_id is the durable correlation
    #    key; gates records the run's gate configuration so resume can rebuild
    #    the exact stage list (including a gate not yet reached).
    run_id = new_ulid()
    now = ctx.clock.now()
    run_record = RunRecord(
        pipeline_run_id=run_id,
        created_at=now.isoformat(),
        updated_at=now.isoformat(),
        current_stage="ingest",
        status="running",
        source_manifest_hash=sha256_file(manifest_path),
        run_dir=run_id,
        gates=gates,
    )
    with ctx.state.transaction():
        ctx.state.create_run(run_record)
        ctx.state.append_event(
            PipelineEvent(
                event_type=EventType.RUN_CREATED,
                pipeline_run_id=run_id,
                occurred_at=now,
                stage_name="pipeline",
                payload={
                    "source_id": manifest.source_id,
                    "manifest_sha256": run_record.source_manifest_hash,
                    "gates": list(gates),
                },
            )
        )

    # 3. Build the concrete stages and sequence them.
    episode_description = (
        f"{manifest.title} by {manifest.author}. {manifest.approval.review_notes}"
    ).strip()
    stages = _build_stages(
        ctx,
        episode_title=manifest.title,
        episode_description=episode_description,
        tts=tts,
        encoder=encoder,
        gates=gates,
    )
    runner = PipelineRunner(ctx)
    outcomes = runner.run_sequence(
        stages,
        pipeline_run_id=run_id,
        run_dir=run_id,
        first_stage_params={"manifest_path": str(manifest_path)},
    )

    summary = _summarise(ctx, run_id, outcomes)

    # 4. --auto-approve: satisfy each gate the run pauses at with a real
    #    persisted decision and resume, until the run finishes. Decisions flow
    #    through the same approval service `storytime approve` uses.
    if auto_approve:
        while summary.status == "awaiting_approval":
            apply_approval_decision(
                ctx,
                pipeline_run_id=run_id,
                gate=summary.awaiting_gate or "text",
                decision="approved",
                operator="auto-approve",
                notes="approved automatically by --auto-approve",
            )
            summary = resume_run(ctx, run_id, tts=tts, encoder=encoder)

    return summary


def resume_run(
    ctx: RunnerContext,
    pipeline_run_id: str,
    *,
    tts: TTSAdapter | None = None,
    encoder: Mp3Encoder | None = None,
    stop_after: str | None = None,
) -> SliceOutcome:
    """Rehydrate *pipeline_run_id* from SQLite and continue it.

    Completed stages are skipped and their artifacts are NOT regenerated; each
    approval gate the run was configured with is re-evaluated against its
    persisted decision. When *stop_after* names a stage, sequencing stops once
    that stage succeeds (used by the granular per-stage CLI commands).

    Raises RehydrationError if the run is unknown, already finished, or its
    persisted state is inconsistent — the caller surfaces that as a clear
    operator-facing error.
    """
    # The run row carries the gate configuration; resume rebuilds the exact
    # stage list the run was created with, even for a gate not yet reached.
    run = load_run_or_raise(ctx, pipeline_run_id)
    gates = run.gates
    order = canonical_stage_order(gates)
    gate_specs = tuple(
        GateResumeSpec(
            stage_name=gate.stage_name, requested_event=gate.requested_event
        )
        for gate in _GATES
        if gate.label in gates
    )

    plan = build_resume_plan(
        ctx,
        pipeline_run_id,
        canonical_order=order,
        gate_specs=gate_specs,
    )
    episode_title, episode_description = _episode_metadata_from_state(
        ctx, pipeline_run_id
    )
    stages = _build_stages(
        ctx,
        episode_title=episode_title,
        episode_description=episode_description,
        tts=tts,
        encoder=encoder,
        gates=gates,
    )
    # Inject each gate's persisted decision into its StageInput.params, so the
    # (pure) gate stages resolve approved / rejected / still-waiting without
    # touching SQLite themselves.
    stage_params: dict[str, dict[str, object]] = {
        gate.stage_name: {
            "approval_decision": plan.gate_decisions.get(gate.stage_name),
            "approval_already_requested": plan.gate_requests_emitted.get(
                gate.stage_name, False
            ),
        }
        for gate in _GATES
        if gate.label in gates
    }
    runner = PipelineRunner(ctx)
    outcomes = runner.resume_sequence(
        stages,
        pipeline_run_id=pipeline_run_id,
        run_dir=plan.run.run_dir,
        completed_stage_names=plan.completed_stage_names,
        seed_artifacts=plan.seed_artifacts,
        link_traceparent=plan.prior_traceparent,
        stage_params=stage_params,
        stop_after=stop_after,
    )
    _stamp_gate_outbound_traces(ctx, pipeline_run_id, gates)
    return _summarise(ctx, pipeline_run_id, outcomes, stop_after=stop_after)


def _stamp_gate_outbound_traces(
    ctx: RunnerContext, pipeline_run_id: str, gates: Sequence[str]
) -> None:
    """Record each crossed gate's outbound (resumed-run) trace, once.

    Phase 5: a resumed run is a fresh trace linked back to the pre-pause one.
    That fresh trace is the *outbound* side of every approval gate this resume
    crossed; the latest stage_execution row carries it. set_approval_outbound_
    trace only writes where outbound_trace_id IS NULL, so a gate keeps the
    trace of the resume that first crossed it and a no-op resume changes
    nothing. Best-effort view metadata: under NoopTelemetry there is no
    trace_id and nothing is stamped.
    """
    trace_id: str | None = None
    for record in reversed(ctx.state.list_stage_executions(pipeline_run_id)):
        if record.trace_id:
            trace_id = record.trace_id
            break
    if trace_id is None:
        return
    with ctx.state.transaction():
        for gate in _GATES:
            if gate.label in gates:
                ctx.state.set_approval_outbound_trace(
                    pipeline_run_id=pipeline_run_id,
                    stage_name=gate.stage_name,
                    trace_id=trace_id,
                )


__all__ = [
    "BASE_STAGE_ORDER",
    "RehydrationError",
    "SliceOutcome",
    "VALID_GATE_LABELS",
    "build_runtime_context",
    "canonical_stage_order",
    "resume_run",
    "run_vertical_slice",
]
