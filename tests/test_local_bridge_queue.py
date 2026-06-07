"""Phase 13G — local-bridge in-memory queue / worker tests.

These exercise the single-concurrency observable queue directly (no HTTP), to
lock its core guarantees: at most one in-flight worker, finite capacity with
explicit backpressure, idempotency-key deduplication that never double-executes,
an observable snapshot, and clean worker shutdown.
"""

from __future__ import annotations

import threading
import time
from typing import Any

import pytest

from storytime.local_bridge.action_queue import (
    STATE_COMPLETED,
    STATE_FAILED,
    ActionQueue,
    Job,
    QueueFull,
)


def _job(idx: int, *, idem: str | None = None) -> Job:
    return Job(
        action_request_id=f"act-{idx}",
        job_id=f"job-{idx}",
        request_id=f"req-{idx}",
        action="retry_failed_stage",
        idempotency_key=idem,
    )


def _drain(queue: ActionQueue, timeout: float = 5.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        snap = queue.snapshot()
        if snap["queueDepth"] == 0 and snap["inFlightCount"] == 0:
            return
        time.sleep(0.01)
    raise AssertionError("queue did not drain in time")


def test_single_concurrency_is_never_exceeded() -> None:
    """At most one job is ever in flight, even under a burst of submissions."""
    observed_max = 0
    in_flight = 0
    lock = threading.Lock()

    def executor(job: Job) -> dict[str, Any]:
        nonlocal observed_max, in_flight
        with lock:
            in_flight += 1
            observed_max = max(observed_max, in_flight)
        time.sleep(0.02)
        with lock:
            in_flight -= 1
        return {"status": STATE_COMPLETED}

    queue = ActionQueue(executor, capacity=16)
    queue.start()
    try:
        for i in range(8):
            queue.submit(_job(i))
        _drain(queue)
    finally:
        queue.stop()
    assert observed_max == 1, f"single-concurrency violated: max in-flight {observed_max}"
    assert queue.snapshot()["completedCount"] == 8


def test_capacity_backpressure_rejects_when_full() -> None:
    """A full queue raises QueueFull rather than silently accepting work."""
    release = threading.Event()

    def executor(job: Job) -> dict[str, Any]:
        release.wait(timeout=5.0)
        return {"status": STATE_COMPLETED}

    queue = ActionQueue(executor, capacity=2)
    queue.start()
    try:
        queue.submit(_job(0))  # will start running and block
        time.sleep(0.05)
        queue.submit(_job(1))  # queued (outstanding = 2)
        with pytest.raises(QueueFull):
            queue.submit(_job(2))  # capacity exceeded → backpressure
        assert queue.snapshot()["rejectedCount"] == 1
        release.set()
        _drain(queue)
    finally:
        release.set()
        queue.stop()


def test_duplicate_idempotency_key_does_not_double_execute() -> None:
    executions = 0
    lock = threading.Lock()
    proceed = threading.Event()

    def executor(job: Job) -> dict[str, Any]:
        nonlocal executions
        proceed.wait(timeout=5.0)
        with lock:
            executions += 1
        return {"status": STATE_COMPLETED}

    queue = ActionQueue(executor, capacity=8)
    queue.start()
    try:
        first, dup1 = queue.submit(_job(0, idem="same-key"))
        second, dup2 = queue.submit(_job(1, idem="same-key"))
        assert dup1 is False
        assert dup2 is True
        assert second.action_request_id == first.action_request_id
        proceed.set()
        _drain(queue)
    finally:
        proceed.set()
        queue.stop()
    assert executions == 1, "duplicate idempotency key caused a second execution"
    assert queue.snapshot()["deduplicatedCount"] == 1


def test_failed_executor_marks_job_failed_not_completed() -> None:
    def executor(job: Job) -> dict[str, Any]:
        raise RuntimeError("boom")

    queue = ActionQueue(executor, capacity=4)
    queue.start()
    try:
        job, _ = queue.submit(_job(0))
        _drain(queue)
        stored = queue.get_job(job.action_request_id)
        assert stored is not None
        assert stored.status == STATE_FAILED
        assert stored.error == "RuntimeError"
    finally:
        queue.stop()
    assert queue.snapshot()["failedCount"] == 1


def test_honest_failed_result_marks_job_failed() -> None:
    """A handler reporting status=failed (not raising) is recorded as failed."""

    def executor(job: Job) -> dict[str, Any]:
        return {"status": STATE_FAILED, "code": "not_retryable_status"}

    queue = ActionQueue(executor, capacity=4)
    queue.start()
    try:
        job, _ = queue.submit(_job(0))
        _drain(queue)
        stored = queue.get_job(job.action_request_id)
        assert stored is not None and stored.status == STATE_FAILED
    finally:
        queue.stop()


def test_worker_shuts_down_cleanly() -> None:
    def executor(job: Job) -> dict[str, Any]:
        return {"status": STATE_COMPLETED}

    queue = ActionQueue(executor, capacity=4)
    queue.start()
    queue.submit(_job(0))
    _drain(queue)
    queue.stop(timeout=5.0)
    # After a clean stop the worker thread is no longer alive.
    assert not queue._worker.is_alive()  # noqa: SLF001 - intentional shutdown assertion


def test_snapshot_exposes_required_observability_concepts() -> None:
    def executor(job: Job) -> dict[str, Any]:
        return {"status": STATE_COMPLETED}

    queue = ActionQueue(executor, capacity=8)
    snap = queue.snapshot()
    for key in (
        "queueDepth",
        "inFlightCount",
        "completedCount",
        "failedCount",
        "rejectedCount",
        "deadLetterCount",
        "oldestQueuedAgeSeconds",
        "longestInFlightAgeSeconds",
        "retryCount",
        "capacity",
        "saturationRatio",
        "maxConcurrency",
    ):
        assert key in snap, f"snapshot missing observability concept {key!r}"
    assert snap["maxConcurrency"] == 1
    assert snap["capacity"] == 8


def test_invalid_capacity_is_rejected() -> None:
    with pytest.raises(ValueError):
        ActionQueue(lambda job: {"status": STATE_COMPLETED}, capacity=0)
