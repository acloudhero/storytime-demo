"""Phase 14C.5.1 — tests for the durable recovery control-plane boundary.

Cover durable recovery lineage, backend-owned eligibility policy, duplicate
prevention / attempt limits, recovery read-model visibility, local concurrency
guardrails, and boundary preservation (observer schema, artifact store, deps).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from storytime.local_live.observability import QueueWorkerEvent
from storytime.local_live.queue import SqliteWorkQueue
from storytime.local_live.recovery import (
    DEFAULT_MAX_RECOVERY_ATTEMPTS,
    evaluate_recovery_eligibility,
)
from storytime.local_live.server import LocalLiveService
from storytime.state.store import StateStore

_REPO_ROOT = Path(__file__).resolve().parents[1]
_FIXTURES_DIR = _REPO_ROOT / "demo" / "seed"

_LEAK_SUBSTRINGS = (
    "/tmp/",
    "/home/",
    "C:\\",
    ".db",
    "signed_url",
    "credential",
    "secret",
    "token",
    "bucket",
    "s3://",
    "minio",
)


@pytest.fixture()
def service(tmp_path: Path) -> LocalLiveService:
    runs = tmp_path / "runs"
    runs.mkdir()
    return LocalLiveService(
        db_path=runs / "state.db", runs_dir=runs, fixtures_dir=_FIXTURES_DIR
    )


def _failed_run(service: LocalLiveService, scenario: str = "artifact_validation_failure") -> str:
    _, body = service.create_proof_run({"scenario": scenario})
    service.drain_queue()
    return body["runId"]


# -- Recovery lineage ------------------------------------------------------


def test_recovery_lineage_recorded_and_links_identities(service: LocalLiveService) -> None:
    rid = _failed_run(service)
    status, view = service.request_recovery({"runId": rid, "requestedBy": "op"})
    assert status == 201
    assert view["status"] == "created"
    assert view["originalRunId"] == rid
    assert view["recoveryRunId"] and view["recoveryRunId"] != rid
    assert view["recoveryWorkItemId"]
    assert view["recoveryActionId"].startswith("recovery-")


def test_recovery_lineage_survives_restart(service: LocalLiveService) -> None:
    rid = _failed_run(service)
    service.request_recovery({"runId": rid})
    reopened = LocalLiveService(
        db_path=service.db_path, runs_dir=service.runs_dir, fixtures_dir=_FIXTURES_DIR
    )
    _, body = reopened.recovery_for_run(rid)
    assert len(body["recoveryActions"]) == 1
    assert body["recoveryActions"][0]["status"] == "created"


def test_recovery_action_id_is_stable(service: LocalLiveService) -> None:
    rid = _failed_run(service)
    _, view = service.request_recovery({"runId": rid})
    action_id = view["recoveryActionId"]
    with StateStore.open(service.db_path) as store:
        again = store.get_recovery_action(action_id)
    assert again is not None
    assert again.recovery_action_id == action_id


def test_recovery_status_transitions_are_bounded(service: LocalLiveService) -> None:
    rid = _failed_run(service)
    _, view = service.request_recovery({"runId": rid})
    assert view["status"] in {"requested", "created", "rejected", "failed"}


# -- Eligibility policy ----------------------------------------------------


def test_unknown_original_rejected(service: LocalLiveService) -> None:
    service.create_proof_run({"scenario": "success"})  # ensure db exists
    with StateStore.open(service.db_path) as store:
        result = evaluate_recovery_eligibility(store, "does-not-exist")
    assert not result.eligible
    assert result.decision == "unknown_original"
    assert result.reason


def test_non_failed_rejected(service: LocalLiveService) -> None:
    _, body = service.create_proof_run({"scenario": "success"})
    service.drain_queue()
    with StateStore.open(service.db_path) as store:
        result = evaluate_recovery_eligibility(store, body["runId"])
    assert result.decision == "not_failed"


def test_in_progress_rejected(service: LocalLiveService) -> None:
    # Enqueued but not drained -> queued/in-progress.
    _, body = service.create_proof_run({"scenario": "success"})
    with StateStore.open(service.db_path) as store:
        result = evaluate_recovery_eligibility(store, body["runId"])
    assert result.decision == "in_progress"


def test_failed_eligible_accepted(service: LocalLiveService) -> None:
    rid = _failed_run(service)
    with StateStore.open(service.db_path) as store:
        result = evaluate_recovery_eligibility(store, rid)
    assert result.eligible
    assert result.decision == "retry_eligible"


def test_governance_blocked_rejected(service: LocalLiveService) -> None:
    rid = _failed_run(service, scenario="governance_failure")
    with StateStore.open(service.db_path) as store:
        result = evaluate_recovery_eligibility(store, rid)
    assert not result.eligible
    assert result.decision == "blocked_by_governance"


def test_eligibility_includes_durable_reason(service: LocalLiveService) -> None:
    rid = _failed_run(service, scenario="governance_failure")
    _, view = service.request_recovery({"runId": rid})
    assert view["status"] == "rejected"
    assert view["decision"] == "blocked_by_governance"
    assert view["rejectionReason"]


# -- Duplicate prevention / attempt limits ---------------------------------


def test_duplicate_active_recovery_rejected(service: LocalLiveService) -> None:
    rid = _failed_run(service)
    s1, _ = service.request_recovery({"runId": rid})
    s2, v2 = service.request_recovery({"runId": rid})
    assert s1 == 201
    assert s2 == 200
    assert v2["status"] == "rejected"
    assert v2["decision"] in {"duplicate_recovery", "max_attempts_reached"}


def test_attempt_limit_enforced(service: LocalLiveService) -> None:
    rid = _failed_run(service)
    # First recovery consumes the single default attempt.
    service.request_recovery({"runId": rid})
    # Drain the recovery run so no active recovery remains, then re-request:
    service.drain_queue()
    with StateStore.open(service.db_path) as store:
        result = evaluate_recovery_eligibility(
            store, rid, max_attempts=DEFAULT_MAX_RECOVERY_ATTEMPTS
        )
    assert result.decision == "max_attempts_reached"


def test_attempt_count_is_durable(service: LocalLiveService) -> None:
    rid = _failed_run(service)
    service.request_recovery({"runId": rid})
    with StateStore.open(service.db_path) as store:
        work = store.get_work_item_for_run(rid)
        assert work is not None
        assert store.count_recovery_attempts_for(work.work_id) == 1


def test_lineage_unambiguous_after_rejected_duplicate(service: LocalLiveService) -> None:
    rid = _failed_run(service)
    service.request_recovery({"runId": rid})
    service.request_recovery({"runId": rid})  # rejected duplicate
    with StateStore.open(service.db_path) as store:
        actions = store.list_recovery_actions_for_run(rid)
        active = [a for a in actions if a.status in {"requested", "created"}]
    assert len(active) == 1  # exactly one active/created recovery


# -- Read model / visibility ----------------------------------------------


def test_read_model_returns_identities_and_metadata(service: LocalLiveService) -> None:
    rid = _failed_run(service)
    service.request_recovery({"runId": rid, "requestedBy": "operator", "reason": "retry"})
    _, body = service.recovery_for_run(rid)
    action = body["recoveryActions"][0]
    for key in (
        "originalRunId",
        "originalWorkItemId",
        "recoveryRunId",
        "recoveryWorkItemId",
        "recoveryReason",
        "requestedBy",
        "requestedAt",
        "status",
        "attemptNumber",
    ):
        assert key in action


def test_rejected_recovery_is_durably_visible(service: LocalLiveService) -> None:
    rid = _failed_run(service, scenario="governance_failure")
    service.request_recovery({"runId": rid})
    _, body = service.recovery_for_run(rid)
    assert len(body["recoveryActions"]) == 1
    assert body["recoveryActions"][0]["status"] == "rejected"
    assert body["recoveryActions"][0]["decision"] == "blocked_by_governance"


def test_recovery_read_model_has_no_unsafe_substrings(service: LocalLiveService) -> None:
    rid = _failed_run(service)
    service.request_recovery({"runId": rid})
    _, body = service.recovery_for_run(rid)
    blob = json.dumps(body)
    present = [s for s in _LEAK_SUBSTRINGS if s in blob]
    assert not present, f"recovery DTO leaked: {present}"
    assert str(service.runs_dir) not in blob


# -- Concurrency guardrails ------------------------------------------------


def test_two_workers_cannot_claim_same_item(service: LocalLiveService) -> None:
    # Enqueue one item; two sequential claims -> only the first wins.
    service.create_proof_run({"scenario": "success"})
    with StateStore.open(service.db_path) as store:
        queue = SqliteWorkQueue(store)
        first = queue.claim(owner="worker-a")
        second = queue.claim(owner="worker-b")
    assert first is not None
    assert second is None


def test_recovery_rejected_while_original_running(service: LocalLiveService) -> None:
    _, body = service.create_proof_run({"scenario": "success"})  # queued, not drained
    status, view = service.request_recovery({"runId": body["runId"]})
    assert status == 200
    assert view["decision"] == "in_progress"


def test_atomic_creation_prevents_duplicate_active(service: LocalLiveService) -> None:
    # Deterministic sequential race simulation: two atomic creates, same original
    # work item; only one becomes active.
    rid = _failed_run(service)
    with StateStore.open(service.db_path) as store:
        work = store.get_work_item_for_run(rid)
        assert work is not None
        from storytime.state.store import RecoveryActionRecord

        base = RecoveryActionRecord(
            recovery_action_id="recovery-A",
            original_run_id=rid,
            original_work_item_id=work.work_id,
            recovery_run_id=None,
            recovery_work_item_id=None,
            recovery_reason="r",
            requested_by="op",
            requested_at="t",
            status="requested",
            decision="retry_eligible",
            rejection_reason=None,
            attempt_number=1,
            updated_at="t",
        )
        from dataclasses import replace

        first = store.atomically_create_recovery_action(base, max_attempts=5)
        second = store.atomically_create_recovery_action(
            replace(base, recovery_action_id="recovery-B"), max_attempts=5
        )
    assert first is True
    assert second is False  # duplicate active prevented


def test_stale_claim_cleanup_still_intact(service: LocalLiveService) -> None:
    # The existing stale-claim recovery path remains callable and bounded.
    with StateStore.open(service.db_path) as store:
        recovered = store.recover_stale_work(now="2099-01-01T00:00:00+00:00", max_attempts=3)
    assert recovered == ()  # nothing stale in a fresh store


# -- Boundary preservation -------------------------------------------------


def test_observer_event_schema_unchanged(service: LocalLiveService) -> None:
    # QueueWorkerEvent must NOT gain recovery-correlation fields.
    fields = set(QueueWorkerEvent.__dataclass_fields__)
    assert fields == {
        "event_name",
        "created_at",
        "run_id",
        "work_item_id",
        "stage_name",
        "artifact_key",
        "status",
        "failure_reason",
        "worker_id",
        "attempt_number",
    }
    assert "recovery_action_id" not in fields
    assert "original_run_id" not in fields


def test_recovery_lineage_not_reconstructed_from_observer_events(
    service: LocalLiveService,
) -> None:
    # Recovery lineage is sourced from the durable recovery_action table, which
    # is populated even though the worker drain that produced the failure used
    # the default no-op observer (no observer events were retained).
    rid = _failed_run(service)
    service.request_recovery({"runId": rid})
    with StateStore.open(service.db_path) as store:
        assert len(store.list_recovery_actions_for_run(rid)) == 1


def test_recovery_does_not_break_artifact_store_evidence(service: LocalLiveService) -> None:
    rid = _failed_run(service)
    service.request_recovery({"runId": rid})
    # Original run still exposes its artifact evidence safely (logical key).
    _, detail = service.run_detail(rid)
    assert detail["artifacts"], "original artifact evidence missing"
    assert not detail["artifacts"][0]["key"].startswith("/")
