"""Local durable work queue — port + SQLite adapter (Phase 14C.1).

This is the seam that separates request *acceptance* from *execution*: a proof
run request enqueues a durable work item, and a local worker later claims and
executes it. It is deliberately shaped as a replaceable **port** (``WorkQueue``)
with a **SQLite adapter** (``SqliteWorkQueue``) as the first local
implementation, so the contract is queue-shaped rather than SQLite-shaped — a
future hosted/distributed adapter could implement the same port without the rest
of the system changing.

This is a LOCAL durable queue. It is NOT a cloud queue, a distributed queue, an
external broker, or a production task system. The claim/lease/recovery mechanics
exist to prevent double-execution and to recover stale claims after a local
worker is lost — proving the *shape* of durable execution locally, not exactly
-once distributed execution.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Protocol

from storytime.state import StateStore, WorkItemRecord

# Default lease window for a claimed item. If a worker claims an item and is
# then lost (crash, interruption) without completing it, the lease expires and
# stale-claim recovery can requeue it for another worker.
DEFAULT_LEASE_SECONDS = 30
# A claimed item that has been attempted this many times without completing is
# failed rather than requeued, so a poison item cannot loop forever.
DEFAULT_MAX_ATTEMPTS = 5


class WorkState(StrEnum):
    """Lifecycle states of a durable work item."""

    QUEUED = "queued"
    CLAIMED = "claimed"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _lease_until(seconds: int) -> str:
    from datetime import timedelta

    return (datetime.now(UTC) + timedelta(seconds=seconds)).isoformat()


class WorkQueue(Protocol):
    """The local durable work-queue port.

    A replaceable contract. ``SqliteWorkQueue`` is the first local adapter; a
    future hosted adapter could implement the same methods. ``owner`` is the
    claiming worker's identity and is used only for lease ownership — it is an
    adapter-internal mechanic and is not part of the safe read model.
    """

    def enqueue(
        self, *, work_id: str, pipeline_run_id: str, scenario: str, fixture_id: str
    ) -> WorkItemRecord:
        """Durably enqueue a new work item in the ``queued`` state."""
        ...

    def claim(
        self, *, owner: str, lease_seconds: int = DEFAULT_LEASE_SECONDS
    ) -> WorkItemRecord | None:
        """Atomically claim the oldest queued item, or return None if empty."""
        ...

    def mark_running(self, *, work_id: str, owner: str) -> bool:
        """Transition a claimed item owned by *owner* to running."""
        ...

    def mark_completed(self, *, work_id: str, owner: str) -> bool:
        """Transition a claimed/running item owned by *owner* to completed."""
        ...

    def mark_failed(self, *, work_id: str, owner: str, reason: str) -> bool:
        """Transition a claimed/running item owned by *owner* to failed."""
        ...

    def recover_stale(
        self, *, max_attempts: int = DEFAULT_MAX_ATTEMPTS
    ) -> tuple[WorkItemRecord, ...]:
        """Requeue or fail items whose lease has expired (stale-claim recovery)."""
        ...

    def get(self, work_id: str) -> WorkItemRecord | None:
        """Return a work item by id, or None."""
        ...

    def list_items(self) -> tuple[WorkItemRecord, ...]:
        """Return all work items, oldest enqueued first."""
        ...


class SqliteWorkQueue:
    """SQLite-backed local adapter implementing :class:`WorkQueue`.

    Delegates to the existing :class:`StateStore` so the queue uses the same
    durable SQLite source-of-truth, WAL journalling, and migration discipline as
    the rest of the system rather than a separate persistence pattern.
    """

    def __init__(self, store: StateStore) -> None:
        self._store = store

    def enqueue(
        self, *, work_id: str, pipeline_run_id: str, scenario: str, fixture_id: str
    ) -> WorkItemRecord:
        self._store.enqueue_work(
            work_id=work_id,
            pipeline_run_id=pipeline_run_id,
            scenario=scenario,
            fixture_id=fixture_id,
            enqueued_at=_now(),
        )
        item = self._store.get_work_item(work_id)
        if item is None:  # pragma: no cover - enqueue just inserted it
            raise RuntimeError(f"work item {work_id!r} vanished after enqueue")
        return item

    def claim(
        self, *, owner: str, lease_seconds: int = DEFAULT_LEASE_SECONDS
    ) -> WorkItemRecord | None:
        return self._store.claim_next_work(
            owner=owner, now=_now(), lease_expires_at=_lease_until(lease_seconds)
        )

    def mark_running(self, *, work_id: str, owner: str) -> bool:
        return self._store.mark_work_running(work_id=work_id, owner=owner, now=_now())

    def mark_completed(self, *, work_id: str, owner: str) -> bool:
        return self._store.mark_work_completed(work_id=work_id, owner=owner, now=_now())

    def mark_failed(self, *, work_id: str, owner: str, reason: str) -> bool:
        return self._store.mark_work_failed(
            work_id=work_id, owner=owner, now=_now(), reason=reason
        )

    def recover_stale(
        self, *, max_attempts: int = DEFAULT_MAX_ATTEMPTS
    ) -> tuple[WorkItemRecord, ...]:
        return self._store.recover_stale_work(now=_now(), max_attempts=max_attempts)

    def get(self, work_id: str) -> WorkItemRecord | None:
        return self._store.get_work_item(work_id)

    def list_items(self) -> tuple[WorkItemRecord, ...]:
        return self._store.list_work_items()
