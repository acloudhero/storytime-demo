"""PipelineRunner: transactional persist-before-telemetry wiring."""

from __future__ import annotations

from pathlib import Path

from storytime.adapters.storage import LocalFilesystemStorage
from storytime.adapters.telemetry import NoopTelemetry
from storytime.config import load_config
from storytime.dto import StageInput, StageResult, StageStatus, StateUpdate
from storytime.events import EventType, PipelineEvent
from storytime.runner import PipelineRunner, RunnerContext
from storytime.state import RunRecord, StateStore
from storytime.util.clock import FixedClock


def _context(state_store: StateStore, fixed_clock: FixedClock, tmp_path: Path) -> RunnerContext:
    config = load_config(
        {"STORYTIME_RUNS_DIR": str(tmp_path / "runs"), "STORYTIME_TELEMETRY": "noop"}
    )
    return RunnerContext(
        config=config,
        clock=fixed_clock,
        state=state_store,
        telemetry=NoopTelemetry(),
        storage=LocalFilesystemStorage(tmp_path),
    )


def _stage_input(run_id: str) -> StageInput:
    return StageInput(pipeline_run_id=run_id, stage_name="demo", run_dir="runs/demo")


class _OkStage:
    name = "demo"

    def run(self, ctx: RunnerContext, stage_input: StageInput) -> StageResult:
        event = PipelineEvent(
            event_type=EventType.RUN_COMPLETED,
            pipeline_run_id=stage_input.pipeline_run_id,
            occurred_at=ctx.clock.now(),
            stage_name="demo",
            payload={"ok": True},
        )
        return StageResult.succeeded(
            StateUpdate(run_status="completed", current_stage="demo"),
            events=(event,),
        )


class _BoomStage:
    name = "demo"

    def run(self, ctx: RunnerContext, stage_input: StageInput) -> StageResult:
        raise ValueError("stage exploded")


def test_successful_stage_persists_event_and_state(
    state_store: StateStore, fixed_clock: FixedClock, sample_run: RunRecord, tmp_path: Path
) -> None:
    state_store.create_run(sample_run)
    runner = PipelineRunner(_context(state_store, fixed_clock, tmp_path))

    result = runner.execute_stage(_OkStage(), _stage_input(sample_run.pipeline_run_id))

    assert result.status is StageStatus.SUCCEEDED
    # The stage's event was persisted to the append-only event_log.
    assert state_store.count_events(sample_run.pipeline_run_id) == 1
    # The StateUpdate was applied to the run row.
    run = state_store.get_run(sample_run.pipeline_run_id)
    assert run is not None
    assert run.status == "completed"
    assert run.current_stage == "demo"


def test_raising_stage_becomes_a_failed_result(
    state_store: StateStore, fixed_clock: FixedClock, sample_run: RunRecord, tmp_path: Path
) -> None:
    """Negative case: an exception in a stage is captured as FAILED, not raised."""
    state_store.create_run(sample_run)
    runner = PipelineRunner(_context(state_store, fixed_clock, tmp_path))

    result = runner.execute_stage(_BoomStage(), _stage_input(sample_run.pipeline_run_id))

    assert result.status is StageStatus.FAILED
    assert result.error_kind == "ValueError"
    assert result.error_message is not None and "exploded" in result.error_message
    # A RUN_FAILED event was still persisted for forensics.
    assert state_store.count_events(sample_run.pipeline_run_id) == 1


def test_failed_result_factory_defaults_to_empty_state_update() -> None:
    result = StageResult.failed("SomeError", "message")
    assert result.status is StageStatus.FAILED
    assert result.state_update == StateUpdate()
    assert result.events == ()
