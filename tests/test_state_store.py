"""SQLite state store: initialisation, WAL, schema, event_log, transactions."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from storytime.events import EventType, PipelineEvent
from storytime.state import SCHEMA_VERSION, RunRecord, StateStore


def test_database_uses_wal_journal_mode(state_store: StateStore) -> None:
    assert state_store.journal_mode() == "wal"


def test_migrations_create_all_tables_and_set_version(state_store: StateStore) -> None:
    assert state_store.current_schema_version() == SCHEMA_VERSION
    expected = {
        "schema_version",
        "pipeline_run",
        "stage_execution",
        "approval",
        "event_log",
        "published_episode",
    }
    assert expected.issubset(state_store.table_names())


def test_create_and_read_run(state_store: StateStore, sample_run: RunRecord) -> None:
    state_store.create_run(sample_run)
    fetched = state_store.get_run(sample_run.pipeline_run_id)
    assert fetched == sample_run


def test_get_missing_run_returns_none(state_store: StateStore) -> None:
    assert state_store.get_run("does-not-exist") is None


def _event(run_id: str, kind: EventType) -> PipelineEvent:
    return PipelineEvent(
        event_type=kind,
        pipeline_run_id=run_id,
        occurred_at=datetime(2026, 1, 1, tzinfo=UTC),
        stage_name="ingest",
        payload={"k": "v"},
    )


def test_event_log_append_and_count(
    state_store: StateStore, sample_run: RunRecord
) -> None:
    state_store.create_run(sample_run)
    run_id = sample_run.pipeline_run_id
    assert state_store.count_events(run_id) == 0
    state_store.append_event(_event(run_id, EventType.RUN_CREATED))
    state_store.append_event(_event(run_id, EventType.TEXT_INGESTED))
    assert state_store.count_events(run_id) == 2


def test_transaction_rollback_discards_writes(
    state_store: StateStore, sample_run: RunRecord
) -> None:
    """Negative case: a failed transaction must leave the event_log untouched."""
    state_store.create_run(sample_run)
    run_id = sample_run.pipeline_run_id

    with pytest.raises(RuntimeError, match="boom"), state_store.transaction():
        state_store.append_event(_event(run_id, EventType.RUN_CREATED))
        state_store.append_event(_event(run_id, EventType.SYNTHESIS_STARTED))
        raise RuntimeError("boom")

    assert state_store.count_events(run_id) == 0


def test_transaction_commit_persists_writes(
    state_store: StateStore, sample_run: RunRecord
) -> None:
    state_store.create_run(sample_run)
    run_id = sample_run.pipeline_run_id
    with state_store.transaction():
        state_store.append_event(_event(run_id, EventType.RUN_CREATED))
    assert state_store.count_events(run_id) == 1
