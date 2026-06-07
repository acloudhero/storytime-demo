"""Phase 14C.1 — tests for the local durable queue / worker shape.

These prove the separation of request acceptance from execution: a proof-run
request enqueues a durable work item, a local worker claims and executes it, the
lifecycle is durable and restart-aware, stale claims are recovered without
double execution, and the safe read model never leaks claim/lease internals.

This is a LOCAL durable queue/worker shape proof — not cloud, distributed, or a
broker.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from storytime.local_live.proof_run import reserve_proof_run
from storytime.local_live.queue import SqliteWorkQueue, WorkState
from storytime.local_live.server import LocalLiveService
from storytime.local_live.worker import LocalWorker
from storytime.state import StateStore

_REPO_ROOT = Path(__file__).resolve().parents[1]
_FIXTURES_DIR = _REPO_ROOT / "demo" / "seed"
_PAST = "2000-01-01T00:00:00+00:00"
_PAST_LEASE = "2000-01-01T00:00:01+00:00"
_FAILURE_SCENARIOS = ("governance_failure", "artifact_validation_failure")


@pytest.fixture()
def service(tmp_path: Path) -> LocalLiveService:
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    return LocalLiveService(
        db_path=runs_dir / "state.db",
        runs_dir=runs_dir,
        fixtures_dir=_FIXTURES_DIR,
    )


def _iter_strings(value: Any) -> Iterator[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from _iter_strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from _iter_strings(v)


# -- request enqueues instead of executing inline -------------------------


def test_request_enqueues_not_inline(service: LocalLiveService) -> None:
    status, body = service.create_proof_run({"scenario": "success"})
    assert status == 202
    assert body["status"] == "queued"
    assert body["queueState"] == "queued"
    run_id = body["runId"]
    # Before any worker runs, the run is queued with no executed stages.
    _, detail = service.run_detail(run_id)
    assert detail["status"] == "queued"
    assert detail["stages"] == []
    assert detail["queue"]["state"] == "queued"


def test_queue_item_persists_in_sqlite(service: LocalLiveService) -> None:
    _, body = service.create_proof_run({"scenario": "success"})
    work_id = body["workId"]
    # Durable: a fresh connection still sees the queued item.
    with StateStore.open(service.db_path) as store:
        item = store.get_work_item(work_id)
        assert item is not None
        assert item.state == WorkState.QUEUED
        assert item.pipeline_run_id == body["runId"]
        assert item.scenario == "success"


# -- worker claims and executes -------------------------------------------


def test_worker_claims_and_completes(service: LocalLiveService) -> None:
    _, body = service.create_proof_run({"scenario": "success"})
    worker = LocalWorker(
        db_path=service.db_path,
        runs_dir=service.runs_dir,
        fixtures_dir=_FIXTURES_DIR,
    )
    item = worker.run_once()
    assert item is not None
    assert item.state == WorkState.COMPLETED
    _, detail = service.run_detail(body["runId"])
    assert detail["status"] == "completed"
    assert len(detail["stages"]) == 4
    # The queue is now empty.
    assert worker.run_once() is None


@pytest.mark.parametrize("scenario", _FAILURE_SCENARIOS)
def test_failure_scenario_through_worker(
    service: LocalLiveService, scenario: str
) -> None:
    _, body = service.create_proof_run({"scenario": scenario})
    service.drain_queue()
    _, detail = service.run_detail(body["runId"])
    assert detail["status"] == "failed"
    assert detail["failureReason"]
    assert detail["queue"]["state"] == "failed"
    event_types = [e["eventType"] for e in detail["events"]]
    assert "RunFailed" in event_types


# -- stale-claim recovery / no double execution ---------------------------


def test_stale_claim_recovered_and_executes_once(service: LocalLiveService) -> None:
    # Reserve + enqueue, then simulate a worker that claimed the item and was
    # lost (an expired lease) before executing anything.
    _, body = service.create_proof_run({"scenario": "success"})
    run_id = body["runId"]
    with StateStore.open(service.db_path) as store:
        claimed = store.claim_next_work(
            owner="lost-worker", now=_PAST, lease_expires_at=_PAST_LEASE
        )
        store._conn.commit()  # noqa: SLF001
        assert claimed is not None
        assert claimed.state == WorkState.CLAIMED
    worker = LocalWorker(
        db_path=service.db_path,
        runs_dir=service.runs_dir,
        fixtures_dir=_FIXTURES_DIR,
    )
    # Recovery requeues the stale claim; the worker then executes it ONCE.
    recovered = worker.recover_stale()
    assert recovered == 1
    worker.drain()
    _, detail = service.run_detail(run_id)
    assert detail["status"] == "completed"
    assert len(detail["stages"]) == 4  # executed exactly once, not duplicated


def test_no_duplicate_execution_on_redelivery(service: LocalLiveService) -> None:
    _, body = service.create_proof_run({"scenario": "success"})
    run_id = body["runId"]
    service.drain_queue()
    _, detail1 = service.run_detail(run_id)
    stages1 = len(detail1["stages"])
    # Simulate a duplicate delivery: enqueue another work item for the SAME run.
    with StateStore.open(service.db_path) as store:
        SqliteWorkQueue(store).enqueue(
            work_id=f"dup-{run_id}",
            pipeline_run_id=run_id,
            scenario="success",
            fixture_id="golden-path",
        )
        store._conn.commit()  # noqa: SLF001
    service.drain_queue()
    _, detail2 = service.run_detail(run_id)
    # Execution is idempotent per run: the stage count does not grow.
    assert len(detail2["stages"]) == stages1 == 4


def test_claim_is_atomic_single_winner(service: LocalLiveService) -> None:
    service.create_proof_run({"scenario": "success"})
    with StateStore.open(service.db_path) as store:
        first = store.claim_next_work(
            owner="worker-a", now=_PAST, lease_expires_at="2099-01-01T00:00:00+00:00"
        )
        store._conn.commit()  # noqa: SLF001
        second = store.claim_next_work(
            owner="worker-b", now=_PAST, lease_expires_at="2099-01-01T00:00:00+00:00"
        )
        store._conn.commit()  # noqa: SLF001
    assert first is not None
    assert second is None  # only one queued item; no double-claim


# -- read-model safety -----------------------------------------------------


def test_read_model_exposes_safe_lifecycle(service: LocalLiveService) -> None:
    _, body = service.create_proof_run({"scenario": "success"})
    _, runs_body = service.list_runs()
    summary = runs_body["runs"][0]
    assert summary["queue"]["state"] in {s.value for s in WorkState}
    assert summary["queue"]["scenario"] == "success"
    _, health = service.health()
    assert health["execution"] == "queued-then-local-worker"
    assert "queueCounts" in health


def test_read_model_hides_claim_internals(service: LocalLiveService) -> None:
    _, body = service.create_proof_run({"scenario": "success"})
    # Claim with a distinctive owner + lease so we can prove they never surface.
    secret_owner = "secret-owner-zzz"
    secret_lease = "2099-12-31T23:59:59+00:00"
    with StateStore.open(service.db_path) as store:
        store.claim_next_work(
            owner=secret_owner, now=_PAST, lease_expires_at=secret_lease
        )
        store._conn.commit()  # noqa: SLF001
    _, runs_body = service.list_runs()
    _, detail = service.run_detail(body["runId"])
    _, health = service.health()
    for payload in (runs_body, detail, health):
        blob = json.dumps(payload)
        assert secret_owner not in blob, "claim owner leaked to read model"
        assert secret_lease not in blob, "lease expiry leaked to read model"
        assert "lease" not in blob.lower(), "lease internals leaked"
        for s in _iter_strings(payload):
            assert not s.startswith("/"), f"absolute POSIX path leaked: {s!r}"
            assert not (len(s) > 2 and s[1] == ":" and s[2] == "\\"), (
                f"absolute Windows path leaked: {s!r}"
            )


# -- schema migration idempotency -----------------------------------------


def test_schema_v7_and_queue_and_recovery_tables(
    service: LocalLiveService,
) -> None:
    with StateStore.open(service.db_path) as store:
        assert store.current_schema_version() == 7
        assert "work_queue" in store.table_names()
        assert "recovery_action" in store.table_names()
    # Reopening applies no further migrations and does not error.
    with StateStore.open(service.db_path) as store:
        assert store.current_schema_version() == 7


def test_reserve_then_execute_is_idempotent_run(service: LocalLiveService) -> None:
    # reserve_proof_run creates a queued run with no stages; executing twice via
    # the worker path still yields a single execution.
    with StateStore.open(service.db_path) as store:
        run_id = reserve_proof_run(
            store,
            runs_dir=service.runs_dir,
            scenario="success",
            fixtures_dir=_FIXTURES_DIR,
        )
        store._conn.commit()  # noqa: SLF001
        assert store.list_stage_executions(run_id) == ()
        SqliteWorkQueue(store).enqueue(
            work_id=f"work-{run_id}",
            pipeline_run_id=run_id,
            scenario="success",
            fixture_id="golden-path",
        )
        store._conn.commit()  # noqa: SLF001
    service.drain_queue()
    service.drain_queue()  # second drain finds nothing queued
    _, detail = service.run_detail(run_id)
    assert detail["status"] == "completed"
    assert len(detail["stages"]) == 4


# -- stale PARTIAL execution recovery (Phase 14C.1.1) ---------------------


def test_stale_partial_execution_recovered_fails_clean(
    service: LocalLiveService,
) -> None:
    """A worker lost AFTER committing a stage (but before terminal completion)
    is recovered by failing the run cleanly — no re-execution, no new stages.
    """
    # Reserve + enqueue.
    _, body = service.create_proof_run({"scenario": "success"})
    run_id = body["runId"]
    work_id = body["workId"]

    # Simulate a worker that claimed the item, started running, committed ONE
    # stage execution, then was lost (lease already expired).
    with StateStore.open(service.db_path) as store:
        claimed = store.claim_next_work(
            owner="lost-worker", now=_PAST, lease_expires_at=_PAST_LEASE
        )
        store._conn.commit()  # noqa: SLF001
        assert claimed is not None and claimed.work_id == work_id
        store.mark_work_running(work_id=work_id, owner="lost-worker", now=_PAST)
        store.record_stage_execution(
            pipeline_run_id=run_id,
            stage_name="ingest",
            started_at=_PAST,
            ended_at=_PAST,
            status="completed",
        )
        store.update_run_state(
            run_id, status="running", current_stage="ingest", updated_at=_PAST
        )
        store._conn.commit()  # noqa: SLF001
        stages_before = len(store.list_stage_executions(run_id))
    assert stages_before == 1

    worker = LocalWorker(
        db_path=service.db_path,
        runs_dir=service.runs_dir,
        fixtures_dir=_FIXTURES_DIR,
    )
    # Recover the stale (expired-lease) running claim, then run the worker.
    assert worker.recover_stale() == 1
    worker.drain()

    _, detail = service.run_detail(run_id)
    # Run failed cleanly; queue failed; reason visible; no duplicate stages.
    assert detail["status"] == "failed"
    assert detail["queue"]["state"] == "failed"
    assert detail["failureReason"]
    assert "stale partial execution" in detail["failureReason"].lower()
    assert len(detail["stages"]) == stages_before  # no new stages added
    event_types = [e["eventType"] for e in detail["events"]]
    assert "RunFailed" in event_types
    run_failed = next(e for e in detail["events"] if e["eventType"] == "RunFailed")
    assert run_failed["payload"].get("lifecycle") == "stale-partial-recovery"


def test_stale_recovery_idempotent_when_already_terminal(
    service: LocalLiveService,
) -> None:
    """A redelivered item for an already-completed run is an idempotent no-op."""
    _, body = service.create_proof_run({"scenario": "success"})
    run_id = body["runId"]
    service.drain_queue()
    _, d1 = service.run_detail(run_id)
    assert d1["status"] == "completed"
    stages1 = len(d1["stages"])
    # Redeliver a work item for the already-completed run.
    with StateStore.open(service.db_path) as store:
        SqliteWorkQueue(store).enqueue(
            work_id=f"redeliver-{run_id}",
            pipeline_run_id=run_id,
            scenario="success",
            fixture_id="golden-path",
        )
        store._conn.commit()  # noqa: SLF001
    service.drain_queue()
    _, d2 = service.run_detail(run_id)
    assert d2["status"] == "completed"  # unchanged, still terminal
    assert len(d2["stages"]) == stages1  # no re-execution
