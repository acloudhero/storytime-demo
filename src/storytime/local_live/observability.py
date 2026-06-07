"""Minimal queue/worker observability boundary (Phase 14C.4).

A small, backend-owned, **in-process** boundary that makes the local queue/worker
lifecycle explainable:

    work.enqueued -> work.claimed -> work.started -> stage.started ->
    stage.completed -> artifact.recorded -> work.completed | work.failed

It is deliberately minimal. It is **not** a telemetry stack: there is no
OpenTelemetry SDK, no collector, no exporters, no Prometheus endpoint, no
dashboards, no alerting, no SLOs, no sampling, and no distributed tracing. Event
names and fields are vendor-neutral and schema-stable so a *future*
collector-oriented phase could map them outward — this phase does not build that
collector.

Design notes:

- **Stdlib only.** No new dependencies.
- **Ephemeral by default.** The default sink is a no-op; an in-memory recorder
  is provided for tests/inspection. No new database table, broker, or stream is
  introduced (see the durable-vs-ephemeral decision in
  ``docs/phase14-contracts-as-built.md`` Section L).
- **Fail-soft.** Emission never breaks the proof loop: :func:`emit` catches sink
  errors and writes a bounded diagnostic to stderr.
- **Safe fields only.** Events carry existing local lifecycle
  identifiers/timestamps/status values — never raw text, secrets, credentials,
  filesystem paths, artifact roots, or signed URLs.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Protocol

# Stable, minimal event-name vocabulary for the current queue/worker lifecycle.
# These mirror lifecycle concepts that already exist in the codebase; no
# retry/recovery or cloud/distributed event names appear here.
WORK_ENQUEUED = "work.enqueued"
WORK_CLAIMED = "work.claimed"
WORK_STARTED = "work.started"
STAGE_STARTED = "stage.started"
STAGE_COMPLETED = "stage.completed"
ARTIFACT_RECORDED = "artifact.recorded"
WORK_COMPLETED = "work.completed"
WORK_FAILED = "work.failed"

EVENT_NAMES: frozenset[str] = frozenset(
    {
        WORK_ENQUEUED,
        WORK_CLAIMED,
        WORK_STARTED,
        STAGE_STARTED,
        STAGE_COMPLETED,
        ARTIFACT_RECORDED,
        WORK_COMPLETED,
        WORK_FAILED,
    }
)


def _now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(frozen=True, slots=True)
class QueueWorkerEvent:
    """One safe, bounded observation of the local queue/worker lifecycle.

    Every field is an existing local lifecycle identifier/timestamp/status. No
    raw text, secret, credential, filesystem path, artifact root, or signed URL
    is ever carried here. Optional fields are only populated when the value is a
    materialized variable at the moment of emission.
    """

    event_name: str
    created_at: str
    run_id: str | None = None
    work_item_id: str | None = None
    stage_name: str | None = None
    artifact_key: str | None = None
    status: str | None = None
    failure_reason: str | None = None
    worker_id: str | None = None
    attempt_number: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return a safe dict with only the populated fields."""
        data: dict[str, Any] = {"eventName": self.event_name, "createdAt": self.created_at}
        if self.run_id is not None:
            data["runId"] = self.run_id
        if self.work_item_id is not None:
            data["workItemId"] = self.work_item_id
        if self.stage_name is not None:
            data["stageName"] = self.stage_name
        if self.artifact_key is not None:
            data["artifactKey"] = self.artifact_key
        if self.status is not None:
            data["status"] = self.status
        if self.failure_reason is not None:
            data["failureReason"] = self.failure_reason
        if self.worker_id is not None:
            data["workerId"] = self.worker_id
        if self.attempt_number is not None:
            data["attemptNumber"] = self.attempt_number
        return data


class QueueWorkerEventSink(Protocol):
    """Backend-owned observation sink port.

    A replaceable contract. The default is a no-op; an in-memory recorder is
    provided for tests. A future collector-oriented phase could implement this
    port to fan out to a vendor — that is out of scope here.
    """

    def record(self, event: QueueWorkerEvent) -> None:
        """Record one lifecycle observation."""
        ...


class NullQueueWorkerObserver:
    """Default no-op sink: observation is off unless a recorder is injected."""

    def record(self, event: QueueWorkerEvent) -> None:  # noqa: D401 - no-op
        return None


class InMemoryQueueWorkerObserver:
    """In-process recorder that collects events in order (ephemeral).

    Used by tests and for local inspection. Events do not survive process exit;
    this phase deliberately does not persist them to a database, broker, or
    stream.
    """

    def __init__(self) -> None:
        self._events: list[QueueWorkerEvent] = []

    def record(self, event: QueueWorkerEvent) -> None:
        self._events.append(event)

    @property
    def events(self) -> tuple[QueueWorkerEvent, ...]:
        return tuple(self._events)

    def event_names(self) -> tuple[str, ...]:
        return tuple(e.event_name for e in self._events)


def emit(
    sink: QueueWorkerEventSink,
    event_name: str,
    *,
    run_id: str | None = None,
    work_item_id: str | None = None,
    stage_name: str | None = None,
    artifact_key: str | None = None,
    status: str | None = None,
    failure_reason: str | None = None,
    worker_id: str | None = None,
    attempt_number: int | None = None,
) -> None:
    """Build and record a lifecycle event, fail-soft.

    A synchronous, side-effect-safe helper. If the sink raises, the error is
    swallowed (with a bounded diagnostic to stderr) so observation can never
    break the queue/worker proof loop or introduce a new worker failure mode.
    """
    event = QueueWorkerEvent(
        event_name=event_name,
        created_at=_now(),
        run_id=run_id,
        work_item_id=work_item_id,
        stage_name=stage_name,
        artifact_key=artifact_key,
        status=status,
        failure_reason=failure_reason,
        worker_id=worker_id,
        attempt_number=attempt_number,
    )
    try:
        sink.record(event)
    except Exception as exc:  # noqa: BLE001 - observation must be fail-soft
        # Bounded diagnostic only; never re-raise into the worker.
        print(
            f"[storytime] queue/worker observation sink error for "
            f"{event_name!r}: {type(exc).__name__}",
            file=sys.stderr,
        )
