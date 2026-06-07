"""In-memory single-concurrency action queue / worker (Phase 13G — runtime).

This is the first runtime implementation of the queue whose *observable*
surface Phase 13F specified in ``docs/local-action-queue-observability.md``. It
is deliberately minimal and local-only:

- **strict single concurrency**: at most one long-running worker is in flight at
  a time (``docs/local-action-queue-observability.md`` §5) — local mode prefers
  predictable safety over throughput and never autoscales;
- **finite capacity + explicit backpressure**: the queue never silently accepts
  unbounded work; a full queue rejects with a typed error;
- **idempotency-key deduplication**: a duplicate key returns the original job's
  handle and never enqueues a second execution
  (``docs/action-execution-boundary.md`` §8);
- **observable snapshot**: depth, in-flight, completed, failed, rejected,
  dead-letter, oldest-queued age, longest-in-flight age, retry count, capacity,
  and saturation ratio (§2);
- **clean shutdown**: the worker drains via a sentinel and joins, so tests and
  operators can stop the bridge without corrupting state.

There is no external queue, no external broker or task framework, no worker pool, no autoscaling,
and no metrics exporter — those are explicitly forbidden for this phase.
"""

from __future__ import annotations

import queue as _stdlib_queue
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

# Job lifecycle states. ``accepted`` and ``queued`` collapse to the same waiting
# state here (a job is enqueued the moment it is accepted), but both names are
# reported so the contract's distinct states are observable.
STATE_ACCEPTED = "accepted"
STATE_QUEUED = "queued"
STATE_RUNNING = "running"
STATE_COMPLETED = "completed"
STATE_FAILED = "failed"
STATE_REJECTED = "rejected"
STATE_DEAD_LETTER = "dead_letter"

_TERMINAL_STATES: frozenset[str] = frozenset(
    {STATE_COMPLETED, STATE_FAILED, STATE_REJECTED, STATE_DEAD_LETTER}
)

# The default conservative local load limit (outstanding queued + in-flight).
DEFAULT_CAPACITY = 8


class QueueFull(Exception):
    """Raised when the queue is at capacity — explicit backpressure, not silence."""


@dataclass(slots=True)
class Job:
    """A single queued / executing action and its observable lifecycle state."""

    action_request_id: str
    job_id: str
    request_id: str
    action: str
    idempotency_key: str | None
    status: str = STATE_QUEUED
    created_monotonic: float = field(default_factory=time.monotonic)
    started_monotonic: float | None = None
    ended_monotonic: float | None = None
    result: dict[str, Any] | None = None
    error: str | None = None
    retry_count: int = 0

    def public_state(self) -> dict[str, Any]:
        """Return the JSON-safe status view used by ``GET /actions/{id}``."""
        return {
            "actionRequestId": self.action_request_id,
            "jobId": self.job_id,
            "requestId": self.request_id,
            "action": self.action,
            "status": self.status,
            "result": self.result,
            "error": self.error,
            "retryCount": self.retry_count,
        }


# An executor takes a job and returns a result dict, or raises to fail the job.
Executor = Callable[[Job], dict[str, Any]]


class ActionQueue:
    """A bounded, single-concurrency, observable in-memory action queue.

    The queue owns exactly one worker thread. Submitting an action enqueues it
    and returns immediately (the HTTP layer turns this into ``202 Accepted``);
    the worker executes one job at a time. All shared state is guarded by a
    single lock; the worker never holds the lock while executing the (possibly
    slow) action.
    """

    def __init__(
        self,
        executor: Executor,
        *,
        capacity: int = DEFAULT_CAPACITY,
    ) -> None:
        if capacity < 1:
            raise ValueError("queue capacity must be >= 1")
        self._executor = executor
        self._capacity = capacity
        self._lock = threading.Lock()
        self._jobs: dict[str, Job] = {}
        self._idempotency: dict[str, str] = {}
        self._ready: _stdlib_queue.Queue[str | None] = _stdlib_queue.Queue()
        self._worker = threading.Thread(
            target=self._run, name="storytime-local-bridge-worker", daemon=True
        )
        self._started = False
        self._stopping = False
        # Cumulative counters.
        self._accepted_total = 0
        self._completed_total = 0
        self._failed_total = 0
        self._rejected_total = 0
        self._dead_letter_total = 0
        self._deduplicated_total = 0
        self._retry_total = 0
        # Single in-flight job id (single-concurrency invariant: 0 or 1).
        self._in_flight_id: str | None = None

    # -- lifecycle ---------------------------------------------------------

    def start(self) -> None:
        with self._lock:
            if self._started:
                return
            self._started = True
        self._worker.start()

    def stop(self, *, timeout: float = 5.0) -> None:
        """Signal the worker to drain and stop, then join it cleanly."""
        with self._lock:
            if not self._started or self._stopping:
                self._stopping = True
                return
            self._stopping = True
        self._ready.put(None)  # sentinel
        self._worker.join(timeout=timeout)

    # -- submission --------------------------------------------------------

    def submit(self, job: Job) -> tuple[Job, bool]:
        """Enqueue *job*.

        Returns ``(job, deduplicated)``. When ``job.idempotency_key`` matches an
        already-seen key, the original job is returned with ``deduplicated=True``
        and no new execution is enqueued. Raises :class:`QueueFull` when the
        outstanding (queued + in-flight) count is already at capacity.
        """
        with self._lock:
            if job.idempotency_key is not None:
                existing_id = self._idempotency.get(job.idempotency_key)
                if existing_id is not None:
                    self._deduplicated_total += 1
                    return self._jobs[existing_id], True

            outstanding = sum(
                1
                for j in self._jobs.values()
                if j.status not in _TERMINAL_STATES
            )
            if outstanding >= self._capacity:
                self._rejected_total += 1
                raise QueueFull(
                    f"queue at capacity ({self._capacity}); request rejected "
                    "with backpressure"
                )

            job.status = STATE_QUEUED
            self._jobs[job.action_request_id] = job
            if job.idempotency_key is not None:
                self._idempotency[job.idempotency_key] = job.action_request_id
            self._accepted_total += 1
            self._retry_total += job.retry_count

        self._ready.put(job.action_request_id)
        return job, False

    # -- worker loop -------------------------------------------------------

    def _run(self) -> None:
        while True:
            item = self._ready.get()
            try:
                if item is None:  # sentinel → drain done, exit
                    return
                self._execute(item)
            finally:
                self._ready.task_done()

    def _execute(self, action_request_id: str) -> None:
        with self._lock:
            job = self._jobs.get(action_request_id)
            if job is None or job.status != STATE_QUEUED:
                return
            job.status = STATE_RUNNING
            job.started_monotonic = time.monotonic()
            self._in_flight_id = action_request_id

        # Execute OUTSIDE the lock so the snapshot / status endpoints stay
        # responsive while a long-running action is in flight.
        try:
            result = self._executor(job)
        except Exception as exc:  # noqa: BLE001 - failures are recorded, not raised
            with self._lock:
                job.status = STATE_FAILED
                job.ended_monotonic = time.monotonic()
                job.error = type(exc).__name__
                self._failed_total += 1
                self._in_flight_id = None
            return

        with self._lock:
            job.result = result
            job.ended_monotonic = time.monotonic()
            # The executor reports honest outcome via result["status"].
            outcome = str(result.get("status", STATE_COMPLETED))
            if outcome == STATE_FAILED:
                job.status = STATE_FAILED
                self._failed_total += 1
            else:
                job.status = STATE_COMPLETED
                self._completed_total += 1
            self._in_flight_id = None

    # -- observation -------------------------------------------------------

    def get_job(self, action_request_id: str) -> Job | None:
        with self._lock:
            return self._jobs.get(action_request_id)

    def snapshot(self) -> dict[str, Any]:
        """Return the observable queue snapshot (point-in-time gauges)."""
        now = time.monotonic()
        with self._lock:
            queued = [j for j in self._jobs.values() if j.status == STATE_QUEUED]
            in_flight = [j for j in self._jobs.values() if j.status == STATE_RUNNING]
            depth = len(queued)
            oldest_queued_age = (
                max(now - j.created_monotonic for j in queued) if queued else 0.0
            )
            longest_in_flight_age = (
                max(
                    now - (j.started_monotonic or now) for j in in_flight
                )
                if in_flight
                else 0.0
            )
            saturation = depth / self._capacity if self._capacity else 0.0
            return {
                "queueDepth": depth,
                "inFlightCount": len(in_flight),
                "completedCount": self._completed_total,
                "failedCount": self._failed_total,
                "rejectedCount": self._rejected_total,
                "deadLetterCount": self._dead_letter_total,
                "deduplicatedCount": self._deduplicated_total,
                "oldestQueuedAgeSeconds": round(oldest_queued_age, 6),
                "longestInFlightAgeSeconds": round(longest_in_flight_age, 6),
                "retryCount": self._retry_total,
                "acceptedCount": self._accepted_total,
                "capacity": self._capacity,
                "saturationRatio": round(saturation, 6),
                "maxConcurrency": 1,
            }

    @property
    def capacity(self) -> int:
        return self._capacity
