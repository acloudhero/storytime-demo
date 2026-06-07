"""Phase 10C — operator failure / review queue tests.

These tests exercise the read-only ``storytime queue`` command and the
``storytime.operator_queue`` module against five run shapes (completed, failed,
governance-blocked, needs-review, awaiting-approval) and lock the Phase 10C
guarantees: a bounded default limit, deterministic most-recently-updated-first
sorting, ``--status`` / ``--run-id`` filtering, deterministic ``--json``
output, no raw-content / no-secret / no-overclaiming leakage, no state
mutation, and no dependency on report generation.

Fixtures are built directly through the StateStore — the smallest local
fixtures that produce the five run shapes without running the whole pipeline.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from typer.testing import CliRunner

from storytime.cli.app import app
from storytime.governance import FORBIDDEN_LEGAL_TERMS
from storytime.operator_queue import (
    DEFAULT_LIMIT,
    collect_queue,
    render_json,
    render_table,
)
from storytime.state import RunRecord, StateStore

# --- poison markers --------------------------------------------------------
# Strings planted in fields the queue MUST NOT surface — the unbounded stage
# error_message and the structured-but-free-text governance blocked_reason.
# The queue surfaces only the structured error_kind code and the decision
# enum, so none of these may appear in any queue output.
_NARRATION_POISON = "NARRATIONTEXTPOISON-synthesized-script-body-once-upon-a-midnight"
_SECRET_POISON = "sk-SECRETTOKENPOISON-0123456789abcdef-api-key"  # noqa: S105
_BLOCKED_REASON_POISON = "BLOCKEDREASONPOISON-long-free-text-governance-rationale"

_RUN_COMPLETED = "01RUNCOMPLETED000000000000"
_RUN_FAILED = "01RUNFAILED000000000000000"
_RUN_BLOCKED = "01RUNBLOCKED00000000000000"
_RUN_NEEDS_REVIEW = "01RUNNEEDSREVIEW0000000000"
_RUN_AWAITING = "01RUNAWAITINGAPPROVAL00000"

runner = CliRunner()


def _seed_runs(store: StateStore) -> None:
    """Seed five run shapes into the state store.

    completed         -> all stages SUCCEEDED, APPROVED envelope; NOT in queue.
    failed            -> a stage with a structured error_kind + poisoned
                         error_message; in queue (reason: failed).
    governance-blocked-> BLOCKED envelope with a poisoned blocked_reason; in
                         queue (reasons: failed + blocked).
    needs-review      -> NEEDS_REVIEW envelope; in queue (reason: needs-review).
    awaiting-approval -> run status awaiting_approval; in queue.
    """
    with store.transaction():
        # -- completed (healthy; must NOT appear in the queue) ------------
        store.create_run(
            RunRecord(
                pipeline_run_id=_RUN_COMPLETED,
                created_at="2026-05-20T10:00:00+00:00",
                updated_at="2026-05-20T10:05:00+00:00",
                current_stage="publish",
                status="completed",
                source_manifest_hash="a" * 64,
                run_dir=_RUN_COMPLETED,
            )
        )
        store.record_stage_execution(
            pipeline_run_id=_RUN_COMPLETED,
            stage_name="publish",
            started_at="2026-05-20T10:00:00+00:00",
            ended_at="2026-05-20T10:05:00+00:00",
            status="SUCCEEDED",
        )

        # -- failed (structured stage error + poisoned error_message) -----
        store.create_run(
            RunRecord(
                pipeline_run_id=_RUN_FAILED,
                created_at="2026-05-21T10:00:00+00:00",
                updated_at="2026-05-21T10:02:00+00:00",
                current_stage="synthesize",
                status="failed",
                source_manifest_hash="b" * 64,
                run_dir=_RUN_FAILED,
            )
        )
        store.record_stage_execution(
            pipeline_run_id=_RUN_FAILED,
            stage_name="synthesize",
            started_at="2026-05-21T10:01:00+00:00",
            ended_at="2026-05-21T10:02:00+00:00",
            status="FAILED",
            error_kind="TtsError",
            error_message=f"{_NARRATION_POISON} {_SECRET_POISON}",
        )

        # -- governance-blocked (failed run + BLOCKED envelope) -----------
        store.create_run(
            RunRecord(
                pipeline_run_id=_RUN_BLOCKED,
                created_at="2026-05-22T10:00:00+00:00",
                updated_at="2026-05-22T10:01:00+00:00",
                current_stage="ingest",
                status="failed",
                source_manifest_hash="c" * 64,
                run_dir=_RUN_BLOCKED,
            )
        )
        store.record_stage_execution(
            pipeline_run_id=_RUN_BLOCKED,
            stage_name="ingest",
            started_at="2026-05-22T10:00:00+00:00",
            ended_at="2026-05-22T10:01:00+00:00",
            status="FAILED",
            error_kind="SourceNotApproved",
        )
        store.record_trust_envelope(
            pipeline_run_id=_RUN_BLOCKED,
            source_ref="blocked-source",
            schema_version="1",
            license_type="BLOCKED",
            decision="BLOCKED",
            decision_timestamp="2026-05-22T09:55:00+00:00",
            approver_id="operator",
            blocked_reason=_BLOCKED_REASON_POISON,
            envelope_key=f"{_RUN_BLOCKED}/governance/trust-envelope.json",
            recorded_at="2026-05-22T10:00:30+00:00",
        )

        # -- needs-review (NEEDS_REVIEW envelope) -------------------------
        store.create_run(
            RunRecord(
                pipeline_run_id=_RUN_NEEDS_REVIEW,
                created_at="2026-05-23T10:00:00+00:00",
                updated_at="2026-05-23T10:01:00+00:00",
                current_stage="ingest",
                status="running",
                source_manifest_hash="d" * 64,
                run_dir=_RUN_NEEDS_REVIEW,
            )
        )
        store.record_trust_envelope(
            pipeline_run_id=_RUN_NEEDS_REVIEW,
            source_ref="review-source",
            schema_version="1",
            license_type="UNKNOWN",
            decision="NEEDS_REVIEW",
            decision_timestamp="2026-05-23T09:55:00+00:00",
            approver_id="operator",
            blocked_reason=None,
            envelope_key=f"{_RUN_NEEDS_REVIEW}/governance/trust-envelope.json",
            recorded_at="2026-05-23T10:00:30+00:00",
        )

        # -- awaiting-approval --------------------------------------------
        store.create_run(
            RunRecord(
                pipeline_run_id=_RUN_AWAITING,
                created_at="2026-05-24T10:00:00+00:00",
                updated_at="2026-05-24T10:01:00+00:00",
                current_stage="approve_text",
                status="awaiting_approval",
                source_manifest_hash="e" * 64,
                run_dir=_RUN_AWAITING,
                gates=("text",),
            )
        )


@pytest.fixture()
def seeded_store(tmp_path: Path) -> Iterator[StateStore]:
    """An open StateStore seeded with the five run shapes."""
    with StateStore.open(tmp_path / "state.db") as store:
        _seed_runs(store)
        yield store


# --- queue membership ------------------------------------------------------


def test_queue_lists_runs_needing_attention(seeded_store: StateStore) -> None:
    items = collect_queue(seeded_store)
    queued = {item.run_id for item in items}
    assert _RUN_FAILED in queued
    assert _RUN_BLOCKED in queued
    assert _RUN_NEEDS_REVIEW in queued
    assert _RUN_AWAITING in queued


def test_queue_excludes_healthy_completed_runs(seeded_store: StateStore) -> None:
    items = collect_queue(seeded_store)
    assert _RUN_COMPLETED not in {item.run_id for item in items}


def test_queue_supports_empty_state(tmp_path: Path) -> None:
    with StateStore.open(tmp_path / "empty.db") as store:
        assert collect_queue(store) == ()
        assert render_table(()) == "no runs need attention."
        assert render_json(()) == "[]"


# --- filtering -------------------------------------------------------------


def test_queue_status_filter_failed(seeded_store: StateStore) -> None:
    items = collect_queue(seeded_store, status="failed")
    ids = {item.run_id for item in items}
    # The failed run and the governance-blocked run (also status=failed).
    assert _RUN_FAILED in ids
    assert _RUN_BLOCKED in ids
    assert _RUN_AWAITING not in ids


def test_queue_status_filter_blocked(seeded_store: StateStore) -> None:
    items = collect_queue(seeded_store, status="blocked")
    assert {item.run_id for item in items} == {_RUN_BLOCKED}


def test_queue_status_filter_needs_review(seeded_store: StateStore) -> None:
    items = collect_queue(seeded_store, status="needs-review")
    assert {item.run_id for item in items} == {_RUN_NEEDS_REVIEW}


def test_queue_status_filter_awaiting_approval(seeded_store: StateStore) -> None:
    items = collect_queue(seeded_store, status="awaiting-approval")
    assert {item.run_id for item in items} == {_RUN_AWAITING}


def test_queue_unknown_status_is_rejected(seeded_store: StateStore) -> None:
    from storytime.operator_queue import QueueStatusError

    with pytest.raises(QueueStatusError):
        collect_queue(seeded_store, status="not-a-status")


def test_queue_run_id_filter(seeded_store: StateStore) -> None:
    items = collect_queue(seeded_store, run_id=_RUN_FAILED)
    assert {item.run_id for item in items} == {_RUN_FAILED}
    # A healthy run filtered by run-id yields an empty queue.
    assert collect_queue(seeded_store, run_id=_RUN_COMPLETED) == ()


# --- limit -----------------------------------------------------------------


def test_queue_applies_a_bounded_default_limit(seeded_store: StateStore) -> None:
    assert DEFAULT_LIMIT == 20
    # The default path never returns an unbounded backlog.
    items = collect_queue(seeded_store)
    assert len(items) <= DEFAULT_LIMIT


def test_queue_limit_caps_results(seeded_store: StateStore) -> None:
    items = collect_queue(seeded_store, limit=2)
    assert len(items) == 2


def test_queue_rejects_non_positive_limit(seeded_store: StateStore) -> None:
    with pytest.raises(ValueError):
        collect_queue(seeded_store, limit=0)


# --- determinism / sorting -------------------------------------------------


def test_queue_is_sorted_most_recently_updated_first(
    seeded_store: StateStore,
) -> None:
    items = collect_queue(seeded_store)
    updated = [item.updated_at for item in items]
    assert updated == sorted(updated, reverse=True)
    # The most recently updated attention run is the awaiting-approval one.
    assert items[0].run_id == _RUN_AWAITING


def test_queue_output_is_deterministic(seeded_store: StateStore) -> None:
    first = render_json(collect_queue(seeded_store))
    second = render_json(collect_queue(seeded_store))
    assert first == second
    assert render_table(collect_queue(seeded_store)) == render_table(
        collect_queue(seeded_store)
    )


# --- JSON output -----------------------------------------------------------


def test_queue_json_has_only_allowlisted_fields(seeded_store: StateStore) -> None:
    import json

    payload = json.loads(render_json(collect_queue(seeded_store)))
    expected = {
        "run_id",
        "status",
        "stage",
        "governance_decision",
        "failure_code",
        "failure_category",
        "updated_at",
        "created_at",
        "report_path",
        "trust_envelope_path",
        "next_hint",
    }
    assert payload, "expected a non-empty queue"
    for entry in payload:
        assert set(entry.keys()) == expected


def test_queue_json_surfaces_structured_failure_and_governance(
    seeded_store: StateStore,
) -> None:
    import json

    payload = {
        e["run_id"]: e for e in json.loads(render_json(collect_queue(seeded_store)))
    }
    assert payload[_RUN_FAILED]["failure_code"] == "TtsError"
    assert payload[_RUN_FAILED]["failure_category"] == "stage_failure"
    assert payload[_RUN_BLOCKED]["governance_decision"] == "BLOCKED"
    assert payload[_RUN_BLOCKED]["failure_category"] == "governance"
    assert payload[_RUN_NEEDS_REVIEW]["governance_decision"] == "NEEDS_REVIEW"


# --- privacy / no-raw-content ----------------------------------------------


def test_queue_excludes_narration_and_secret_content(
    seeded_store: StateStore,
) -> None:
    # The poisoned error_message must never reach table or JSON output —
    # the queue surfaces only the structured error_kind code.
    table = render_table(collect_queue(seeded_store))
    payload = render_json(collect_queue(seeded_store))
    for text in (table, payload):
        assert _NARRATION_POISON not in text
        assert _SECRET_POISON not in text


def test_queue_excludes_free_text_blocked_reason(
    seeded_store: StateStore,
) -> None:
    # The free-text governance blocked_reason is never surfaced — only the
    # bounded decision enum is.
    table = render_table(collect_queue(seeded_store))
    payload = render_json(collect_queue(seeded_store))
    for text in (table, payload):
        assert _BLOCKED_REASON_POISON not in text


def test_queue_excludes_forbidden_legal_compliance_phrases(
    seeded_store: StateStore,
) -> None:
    # Reuse the locked forbidden-term set rather than re-listing the phrases.
    table = render_table(collect_queue(seeded_store)).lower()
    payload = render_json(collect_queue(seeded_store)).lower()
    for term in FORBIDDEN_LEGAL_TERMS:
        assert term.lower() not in table
        assert term.lower() not in payload


# --- next hint -------------------------------------------------------------


def test_queue_next_hint_is_a_non_mutating_suggestion(
    seeded_store: StateStore,
) -> None:
    hints = {item.run_id: item.next_hint for item in collect_queue(seeded_store)}
    # The awaiting-approval hint points at the existing canonical command.
    assert "storytime approve" in hints[_RUN_AWAITING]
    # No hint instructs an automated mutation.
    for hint in hints.values():
        lowered = hint.lower()
        assert "automatically" not in lowered
        assert "delete this" not in lowered
        assert "safe to publish" not in lowered


def test_queue_report_path_is_a_relative_reference(
    seeded_store: StateStore,
) -> None:
    for item in collect_queue(seeded_store):
        assert item.report_path == f"operator-report/run-{item.run_id}.html"
        assert not item.report_path.startswith("/")


# --- no mutation -----------------------------------------------------------


def test_queue_does_not_mutate_state(seeded_store: StateStore) -> None:
    before = seeded_store.list_runs()
    before_stages = {
        r.pipeline_run_id: seeded_store.list_stage_executions(r.pipeline_run_id)
        for r in before
    }
    collect_queue(seeded_store)
    collect_queue(seeded_store, status="failed")
    collect_queue(seeded_store, run_id=_RUN_BLOCKED)
    assert seeded_store.list_runs() == before
    for run_id, stages in before_stages.items():
        assert seeded_store.list_stage_executions(run_id) == stages


# --- CLI -------------------------------------------------------------------


def _env(tmp_path: Path) -> dict[str, str]:
    return {
        "STORYTIME_RUNS_DIR": str(tmp_path / "runs"),
        "STORYTIME_FEED_DIR": str(tmp_path / "feed"),
        "STORYTIME_TELEMETRY": "noop",
    }


def test_cli_queue_lists_attention_runs(tmp_path: Path) -> None:
    with StateStore.open(tmp_path / "runs" / "state.db") as store:
        _seed_runs(store)
    result = runner.invoke(app, ["queue"], env=_env(tmp_path))
    assert result.exit_code == 0, result.output
    assert _RUN_FAILED in result.output
    assert _RUN_COMPLETED not in result.output
    assert "need attention" in result.output


def test_cli_queue_json_is_machine_readable(tmp_path: Path) -> None:
    import json

    with StateStore.open(tmp_path / "runs" / "state.db") as store:
        _seed_runs(store)
    result = runner.invoke(app, ["queue", "--json"], env=_env(tmp_path))
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert isinstance(payload, list)
    assert any(e["run_id"] == _RUN_BLOCKED for e in payload)


def test_cli_queue_status_filter(tmp_path: Path) -> None:
    with StateStore.open(tmp_path / "runs" / "state.db") as store:
        _seed_runs(store)
    result = runner.invoke(
        app, ["queue", "--status", "blocked"], env=_env(tmp_path)
    )
    assert result.exit_code == 0, result.output
    assert _RUN_BLOCKED in result.output
    assert _RUN_AWAITING not in result.output


def test_cli_queue_unknown_status_exits_nonzero(tmp_path: Path) -> None:
    with StateStore.open(tmp_path / "runs" / "state.db") as store:
        _seed_runs(store)
    result = runner.invoke(
        app, ["queue", "--status", "bogus"], env=_env(tmp_path)
    )
    assert result.exit_code == 1
    assert "unknown status" in result.output


def test_cli_queue_run_id_not_found_exits_nonzero(tmp_path: Path) -> None:
    with StateStore.open(tmp_path / "runs" / "state.db") as store:
        _seed_runs(store)
    result = runner.invoke(
        app, ["queue", "--run-id", "01NOSUCHRUN0000000000000XX"], env=_env(tmp_path)
    )
    assert result.exit_code == 1
    assert "no run found" in result.output


def test_cli_queue_does_not_require_report_generation(tmp_path: Path) -> None:
    # The queue runs without an operator-report directory ever being created.
    with StateStore.open(tmp_path / "runs" / "state.db") as store:
        _seed_runs(store)
    result = runner.invoke(app, ["queue"], env=_env(tmp_path))
    assert result.exit_code == 0, result.output
    assert not (tmp_path / "operator-report").exists()


def test_cli_queue_is_discoverable(tmp_path: Path) -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "queue" in result.output
