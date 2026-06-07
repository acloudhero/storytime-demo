"""Local worker — drains the durable work queue (Phase 14C.1).

The worker is the *execution* half of the separated proof loop. It claims a
queued work item, transitions it to running, executes the existing
backend-owned proof-run logic via :func:`execute_proof_run`, and marks the work
item completed or failed — reconciling the work-item state to the run's durable
terminal state.

It is deliberately LOCAL and bounded: a single in-process worker that processes
work synchronously. It is NOT an external broker worker, a cloud worker, a
distributed worker pool, a process supervisor, or a Celery/Temporal-style
orchestrator. The optional background loop (used only by the running
``storytime local-live`` server) is a single daemon thread that drains on a
bounded interval; tests drive the worker synchronously for determinism.
"""

from __future__ import annotations

import contextlib
import threading
from pathlib import Path

from storytime.local_live import read_model
from storytime.local_live.observability import (
    WORK_CLAIMED,
    WORK_COMPLETED,
    WORK_FAILED,
    WORK_STARTED,
    NullQueueWorkerObserver,
    QueueWorkerEventSink,
    emit,
)
from storytime.local_live.proof_run import execute_proof_run
from storytime.local_live.queue import (
    DEFAULT_MAX_ATTEMPTS,
    SqliteWorkQueue,
    WorkState,
)
from storytime.state import StateStore, WorkItemRecord

DEFAULT_WORKER_OWNER = "local-worker"


def _failure_reason_for(store: StateStore, run_id: str, runs_dir: Path) -> str:
    """Derive a durable failure reason for a failed run.

    Prefers the first failed stage's message; falls back to the read model's
    failure reason (which also surfaces a RunFailed event reason, e.g. the
    Phase 14C.1.1 stale-partial recovery case that fails a run without a failed
    stage).
    """
    for stage in store.list_stage_executions(run_id):
        if stage.status == "failed" and stage.error_message:
            return stage.error_message
    detail = read_model.get_run_detail(store, run_id, runs_dir)
    if detail is not None and detail.failure_reason:
        return detail.failure_reason
    return "proof run failed (no stage-level reason recorded)"


class LocalWorker:
    """A bounded local worker that claims and executes queued proof runs."""

    def __init__(
        self,
        *,
        db_path: Path,
        runs_dir: Path,
        fixtures_dir: Path | None = None,
        owner: str = DEFAULT_WORKER_OWNER,
        observer: QueueWorkerEventSink | None = None,
    ) -> None:
        self.db_path = db_path
        self.runs_dir = runs_dir
        self.fixtures_dir = fixtures_dir
        self.owner = owner
        self.observer: QueueWorkerEventSink = observer or NullQueueWorkerObserver()

    def run_once(self) -> WorkItemRecord | None:
        """Claim and execute one queued item; return it, or None if queue empty.

        Claiming is atomic (only one worker can win an item), execution is
        idempotent per run, and the work item is reconciled to the run's durable
        terminal state — so a recovered or redelivered item never causes double
        execution. Safe queue/worker lifecycle observations are emitted fail-soft
        to ``self.observer``; emission never changes execution semantics.
        """
        sink = self.observer
        with StateStore.open(self.db_path) as store:
            queue = SqliteWorkQueue(store)
            item = queue.claim(owner=self.owner)
            if item is None:
                return None
            emit(
                sink,
                WORK_CLAIMED,
                run_id=item.pipeline_run_id,
                work_item_id=item.work_id,
                worker_id=self.owner,
                attempt_number=item.attempts,
                status="claimed",
            )
            queue.mark_running(work_id=item.work_id, owner=self.owner)
            emit(
                sink,
                WORK_STARTED,
                run_id=item.pipeline_run_id,
                work_item_id=item.work_id,
                worker_id=self.owner,
                status="running",
            )
            try:
                execute_proof_run(
                    store,
                    item.pipeline_run_id,
                    runs_dir=self.runs_dir,
                    fixture_id=item.fixture_id,
                    scenario=item.scenario,
                    fixtures_dir=self.fixtures_dir,
                    observer=sink,
                )
            except Exception as exc:  # noqa: BLE001 - record, don't crash the worker
                queue.mark_failed(
                    work_id=item.work_id,
                    owner=self.owner,
                    reason=f"worker execution error: {exc}",
                )
                emit(
                    sink,
                    WORK_FAILED,
                    run_id=item.pipeline_run_id,
                    work_item_id=item.work_id,
                    worker_id=self.owner,
                    status="failed",
                    failure_reason="worker execution error",
                )
                return queue.get(item.work_id)

            # Reconcile the work-item state to the run's durable terminal state.
            run = store.get_run(item.pipeline_run_id)
            run_status = run.status if run is not None else "unknown"
            if run_status == "completed":
                queue.mark_completed(work_id=item.work_id, owner=self.owner)
                emit(
                    sink,
                    WORK_COMPLETED,
                    run_id=item.pipeline_run_id,
                    work_item_id=item.work_id,
                    worker_id=self.owner,
                    status="completed",
                )
            elif run_status == "failed":
                reason = _failure_reason_for(store, item.pipeline_run_id, self.runs_dir)
                queue.mark_failed(
                    work_id=item.work_id,
                    owner=self.owner,
                    reason=reason,
                )
                emit(
                    sink,
                    WORK_FAILED,
                    run_id=item.pipeline_run_id,
                    work_item_id=item.work_id,
                    worker_id=self.owner,
                    status="failed",
                    failure_reason=reason,
                )
            else:  # pragma: no cover - run should be terminal after execute
                queue.mark_failed(
                    work_id=item.work_id,
                    owner=self.owner,
                    reason=f"run ended in non-terminal state {run_status!r}",
                )
            return queue.get(item.work_id)

    def drain(self, *, max_items: int = 64) -> int:
        """Process queued items until the queue is empty or *max_items* reached.

        Returns the number of items processed. Recovers stale claims first so a
        previously-lost item becomes claimable again.
        """
        self.recover_stale()
        processed = 0
        while processed < max_items:
            item = self.run_once()
            if item is None:
                break
            processed += 1
        return processed

    def recover_stale(self, *, max_attempts: int = DEFAULT_MAX_ATTEMPTS) -> int:
        """Requeue or fail stale (lease-expired) claims; return count recovered."""
        with StateStore.open(self.db_path) as store:
            queue = SqliteWorkQueue(store)
            return len(queue.recover_stale(max_attempts=max_attempts))


class BackgroundWorker:
    """A single daemon thread that drains the queue on a bounded interval.

    Used only by the running ``storytime local-live`` server so the operator
    gets results without polling from the browser. Tests do not use this; they
    drive :class:`LocalWorker` synchronously for determinism. This is not a
    distributed worker pool or a process supervisor — it is one local thread.
    """

    def __init__(self, worker: LocalWorker, *, poll_seconds: float = 0.2) -> None:
        self._worker = worker
        self._poll_seconds = poll_seconds
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread is not None:
            return
        self._thread = threading.Thread(
            target=self._loop, name="storytime-local-worker", daemon=True
        )
        self._thread.start()

    def _loop(self) -> None:
        while not self._stop.is_set():
            # A single loop iteration must never kill the worker thread.
            with contextlib.suppress(Exception):
                self._worker.drain()
            self._stop.wait(self._poll_seconds)

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=5)
            self._thread = None


# WorkState is re-exported for convenience so callers importing the worker can
# reference lifecycle states without reaching into the queue module.
__all__ = [
    "BackgroundWorker",
    "DEFAULT_WORKER_OWNER",
    "LocalWorker",
    "WorkState",
]
