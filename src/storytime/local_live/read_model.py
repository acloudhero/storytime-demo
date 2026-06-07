"""Phase 14A.1 — local-live read model.

Typed, deterministic DTOs that project the backend-owned SQLite state
(``pipeline_run``, ``stage_execution``, ``event_log``, ``stage_artifact``) into
a small, safe JSON shape for the operator console's Live Proof Loop surface.

Boundary notes:
- The read model is **read-only** and derived from durable backend state. It is
  never the source of truth — SQLite is (Architecture Baseline §5).
- It deliberately exposes only bounded metadata: ids, statuses, stage names,
  timestamps, artifact keys/hashes/sizes, and small JSON event payloads. It
  never exposes raw story text — only an approved fixture's title / source id /
  licence, which are public-domain demo metadata.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from storytime.state.store import (
    RecoveryActionRecord,
    RunRecord,
    StageArtifactRecord,
    StageExecutionRecord,
    StateStore,
)

# The bounded set of run statuses the live surface understands. Any other
# status from the store is passed through verbatim (the frontend renders it as
# an unknown/neutral state) — the read model never invents a status.
KNOWN_STATUSES = frozenset(
    {"running", "completed", "failed", "blocked", "awaiting_approval"}
)


@dataclass(frozen=True, slots=True)
class LiveStage:
    """One persisted stage execution."""

    stage_name: str
    status: str
    started_at: str
    ended_at: str | None
    error_kind: str | None
    error_message: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "stageName": self.stage_name,
            "status": self.status,
            "startedAt": self.started_at,
            "endedAt": self.ended_at,
            "errorKind": self.error_kind,
            "errorMessage": self.error_message,
        }


@dataclass(frozen=True, slots=True)
class LiveArtifact:
    """One persisted artifact-evidence record.

    ``key`` is the relative storage key recorded in SQLite. ``sha256`` and
    ``bytes`` are computed by resolving the key under the runs directory when
    the file exists; both are ``None`` when the file cannot be resolved (the
    record still proves the artifact was registered).
    """

    stage_name: str
    key: str
    name: str
    recorded_at: str
    sha256: str | None
    bytes: int | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "stageName": self.stage_name,
            "key": self.key,
            "name": self.name,
            "recordedAt": self.recorded_at,
            "sha256": self.sha256,
            "bytes": self.bytes,
        }


@dataclass(frozen=True, slots=True)
class RecoveryLineageView:
    """One durable recovery-lineage record, projected for the operator.

    Links the original failed execution identity to the recovery execution
    identity, plus the bounded recovery reason / requester / timestamp / status.
    For a rejected request, ``decision`` and ``rejection_reason`` carry the
    bounded eligibility outcome. Contains only safe, bounded fields — never a
    filesystem path, storage root, credential, or raw text.
    """

    recovery_action_id: str
    original_run_id: str
    original_work_item_id: str
    recovery_run_id: str | None
    recovery_work_item_id: str | None
    recovery_reason: str
    requested_by: str
    requested_at: str
    status: str
    attempt_number: int
    decision: str | None
    rejection_reason: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "recoveryActionId": self.recovery_action_id,
            "originalRunId": self.original_run_id,
            "originalWorkItemId": self.original_work_item_id,
            "recoveryRunId": self.recovery_run_id,
            "recoveryWorkItemId": self.recovery_work_item_id,
            "recoveryReason": self.recovery_reason,
            "requestedBy": self.requested_by,
            "requestedAt": self.requested_at,
            "status": self.status,
            "attemptNumber": self.attempt_number,
            "decision": self.decision,
            "rejectionReason": self.rejection_reason,
        }


def map_recovery_action(record: RecoveryActionRecord) -> RecoveryLineageView:
    """Project a durable recovery_action row to a safe operator view."""
    return RecoveryLineageView(
        recovery_action_id=record.recovery_action_id,
        original_run_id=record.original_run_id,
        original_work_item_id=record.original_work_item_id,
        recovery_run_id=record.recovery_run_id,
        recovery_work_item_id=record.recovery_work_item_id,
        recovery_reason=record.recovery_reason,
        requested_by=record.requested_by,
        requested_at=record.requested_at,
        status=record.status,
        attempt_number=record.attempt_number,
        decision=record.decision,
        rejection_reason=record.rejection_reason,
    )


@dataclass(frozen=True, slots=True)
class LiveEvent:
    """One append-only audit event (bounded payload only)."""

    occurred_at: str
    event_type: str
    payload: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "occurredAt": self.occurred_at,
            "eventType": self.event_type,
            "payload": self.payload,
        }


@dataclass(frozen=True, slots=True)
class LiveWorkItem:
    """Safe, browser-visible view of a durable work item (Phase 14C.1).

    Exposes only the lifecycle-relevant fields. The claim/lease mechanics
    (owner, lease expiry) are adapter-internal and are deliberately NOT exposed
    — no lease tokens, owners, or database internals reach the read model.
    """

    work_id: str
    state: str
    scenario: str
    attempts: int
    enqueued_at: str
    updated_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "workId": self.work_id,
            "state": self.state,
            "scenario": self.scenario,
            "attempts": self.attempts,
            "enqueuedAt": self.enqueued_at,
            "updatedAt": self.updated_at,
        }


@dataclass(frozen=True, slots=True)
class LiveRunSummary:
    """A compact summary of a durable run for the runs list."""

    run_id: str
    status: str
    current_stage: str
    created_at: str
    updated_at: str
    stage_count: int
    artifact_count: int
    event_count: int
    queue: LiveWorkItem | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "runId": self.run_id,
            "status": self.status,
            "currentStage": self.current_stage,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "stageCount": self.stage_count,
            "artifactCount": self.artifact_count,
            "eventCount": self.event_count,
            "stateOwner": "backend-sqlite",
            "queue": self.queue.to_dict() if self.queue is not None else None,
        }


@dataclass(frozen=True, slots=True)
class LiveRunDetail:
    """Full detail of a durable run: summary + stages + artifacts + events."""

    summary: LiveRunSummary
    stages: tuple[LiveStage, ...]
    artifacts: tuple[LiveArtifact, ...]
    events: tuple[LiveEvent, ...]
    failure_reason: str | None

    def to_dict(self) -> dict[str, Any]:
        data = self.summary.to_dict()
        data.update(
            {
                "stages": [s.to_dict() for s in self.stages],
                "artifacts": [a.to_dict() for a in self.artifacts],
                "events": [e.to_dict() for e in self.events],
                "failureReason": self.failure_reason,
            }
        )
        return data


def _artifact_hash_and_size(
    runs_dir: Path, key: str
) -> tuple[str | None, int | None]:
    """Resolve a relative artifact key under runs_dir; return (sha256, bytes).

    Returns (None, None) if the file does not exist or cannot be read. The key
    is sanitised: a key that resolves outside runs_dir is rejected (defence in
    depth — proof artifacts are always written under the run directory).
    """
    try:
        base = runs_dir.resolve()
        candidate = (base / key).resolve()
        if base not in candidate.parents and candidate != base:
            return (None, None)
        if not candidate.is_file():
            return (None, None)
        raw = candidate.read_bytes()
    except OSError:
        return (None, None)
    return (hashlib.sha256(raw).hexdigest(), len(raw))


def map_stage(record: StageExecutionRecord) -> LiveStage:
    return LiveStage(
        stage_name=record.stage_name,
        status=record.status,
        started_at=record.started_at,
        ended_at=record.ended_at,
        error_kind=record.error_kind,
        error_message=record.error_message,
    )


def map_artifact(record: StageArtifactRecord, runs_dir: Path) -> LiveArtifact:
    sha256, size = _artifact_hash_and_size(runs_dir, record.artifact_key)
    name = record.artifact_key.rsplit("/", 1)[-1]
    return LiveArtifact(
        stage_name=record.stage_name,
        key=record.artifact_key,
        name=name,
        recorded_at=record.recorded_at,
        sha256=sha256,
        bytes=size,
    )


def _events_for_run(store: StateStore, run_id: str) -> tuple[LiveEvent, ...]:
    """Read append-only events for a run, parsing each bounded JSON payload."""
    rows = store._conn.execute(  # noqa: SLF001 - read model is store-internal
        "SELECT occurred_at, event_type, payload_json FROM event_log "
        "WHERE pipeline_run_id=? ORDER BY id",
        (run_id,),
    ).fetchall()
    events: list[LiveEvent] = []
    for row in rows:
        try:
            payload = json.loads(row["payload_json"])
        except (json.JSONDecodeError, TypeError):
            payload = {}
        if not isinstance(payload, dict):
            payload = {"value": payload}
        events.append(
            LiveEvent(
                occurred_at=row["occurred_at"],
                event_type=row["event_type"],
                payload=payload,
            )
        )
    return tuple(events)


def _summary(
    store: StateStore, run: RunRecord
) -> LiveRunSummary:
    stages = store.list_stage_executions(run.pipeline_run_id)
    artifacts = store.list_stage_artifacts(run.pipeline_run_id)
    event_count = store.count_events(run.pipeline_run_id)
    work = store.get_work_item_for_run(run.pipeline_run_id)
    queue = (
        LiveWorkItem(
            work_id=work.work_id,
            state=work.state,
            scenario=work.scenario,
            attempts=work.attempts,
            enqueued_at=work.enqueued_at,
            updated_at=work.updated_at,
        )
        if work is not None
        else None
    )
    return LiveRunSummary(
        run_id=run.pipeline_run_id,
        status=run.status,
        current_stage=run.current_stage,
        created_at=run.created_at,
        updated_at=run.updated_at,
        stage_count=len(stages),
        artifact_count=len(artifacts),
        event_count=event_count,
        queue=queue,
    )


def list_run_summaries(store: StateStore) -> tuple[LiveRunSummary, ...]:
    """Return a summary for every durable run, newest first."""
    runs = store.list_runs()
    # list_runs() orders oldest-first by created_at; present newest first.
    return tuple(_summary(store, run) for run in reversed(runs))


def get_run_detail(
    store: StateStore, run_id: str, runs_dir: Path
) -> LiveRunDetail | None:
    """Return full detail for one run, or None if it does not exist."""
    run = store.get_run(run_id)
    if run is None:
        return None
    stages = tuple(map_stage(s) for s in store.list_stage_executions(run_id))
    artifacts = tuple(
        map_artifact(a, runs_dir) for a in store.list_stage_artifacts(run_id)
    )
    events = _events_for_run(store, run_id)
    failure_reason: str | None = None
    for stage in stages:
        if stage.status == "failed" and stage.error_message:
            failure_reason = stage.error_message
            break
    # Fallback: a run can fail without a failed *stage* — e.g. Phase 14C.1.1
    # stale-partial recovery fails the run via a RunFailed event without adding
    # a stage. Surface that event's reason so the failure is always visible.
    if failure_reason is None:
        for event in reversed(events):
            if event.event_type == "RunFailed":
                reason = event.payload.get("reason")
                if isinstance(reason, str) and reason:
                    failure_reason = reason
                    break
    return LiveRunDetail(
        summary=_summary(store, run),
        stages=stages,
        artifacts=artifacts,
        events=events,
        failure_reason=failure_reason,
    )
