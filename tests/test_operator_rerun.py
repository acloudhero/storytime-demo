"""Phase 10D — operator pipeline re-run / mutation tests.

These tests exercise the governed `storytime rerun` mutation and the
`storytime.operator_rerun` eligibility / mutation layer against seven run
shapes and lock the Phase 10D guarantees: a re-run proceeds only for a failed,
genuinely stage-failed, governance-approved run; a dry run mutates nothing; an
actual re-run mutates only `pipeline_run.status` and writes one audit event; a
governance-blocked, denied, missing-envelope, operator-rejected, completed, or
unknown-state run is rejected; JSON output is allowlisted; human output leaks
no raw content; and the Phase 10C read-only queue is unaffected.

Fixtures are built directly through the StateStore — the smallest local
fixtures that produce the run shapes without running the whole pipeline.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

import pytest
from typer.testing import CliRunner

from storytime.cli.app import app
from storytime.operator_rerun import (
    CODE_ELIGIBLE,
    CODE_GOVERNANCE_BLOCKED,
    CODE_NOT_RETRYABLE_STATUS,
    CODE_OPERATOR_REJECTED,
    CODE_RUN_NOT_FOUND,
    CODE_STAGE_MISMATCH,
    CODE_STAGE_UNKNOWN,
    CODE_TRUST_ENVELOPE_DENIED,
    CODE_TRUST_ENVELOPE_MISSING,
    CODE_UNSAFE_UNKNOWN_STATE,
    evaluate_rerun_eligibility,
    perform_rerun,
    render_rerun_json,
    render_rerun_text,
)
from storytime.state import RunRecord, StateStore
from storytime.util.clock import FixedClock

# A poison string planted in the unbounded stage error_message — the re-run
# surface must never echo it; it surfaces only the structured error_kind.
_ERROR_MESSAGE_POISON = "ERRORMESSAGEPOISON-once-upon-a-midnight-stack-trace-body"

_RUN_ELIGIBLE = "01RUNELIGIBLE00000000000000"
_RUN_BLOCKED = "01RUNBLOCKED000000000000000"
_RUN_DENIED = "01RUNDENIED0000000000000000"
_RUN_NO_ENVELOPE = "01RUNNOENVELOPE000000000000"
_RUN_OPERATOR_REJECTED = "01RUNOPREJECTED000000000000"
_RUN_COMPLETED = "01RUNCOMPLETED00000000000000"[:26]
_RUN_INCONSISTENT = "01RUNINCONSISTENT0000000000"

runner = CliRunner()


def _add_run(store: StateStore, run_id: str, status: str, stage: str) -> None:
    store.create_run(
        RunRecord(
            pipeline_run_id=run_id,
            created_at="2026-05-25T10:00:00+00:00",
            updated_at="2026-05-25T10:01:00+00:00",
            current_stage=stage,
            status=status,
            source_manifest_hash="a" * 64,
            run_dir=run_id,
        )
    )


def _add_envelope(store: StateStore, run_id: str, decision: str) -> None:
    store.record_trust_envelope(
        pipeline_run_id=run_id,
        source_ref=f"source-{run_id[:8].lower()}",
        schema_version="1",
        license_type="US_PUBLIC_DOMAIN" if decision == "APPROVED" else "BLOCKED",
        decision=decision,
        decision_timestamp="2026-05-25T09:55:00+00:00",
        approver_id="operator",
        blocked_reason=None if decision == "APPROVED" else "blocked-reason-text",
        envelope_key=f"{run_id}/governance/trust-envelope.json",
        recorded_at="2026-05-25T10:00:30+00:00",
    )


def _seed(store: StateStore) -> None:
    """Seed seven run shapes covering the Phase 10D decision space."""
    with store.transaction():
        # eligible: failed at synthesize (TtsError), APPROVED envelope
        _add_run(store, _RUN_ELIGIBLE, "failed", "synthesize")
        store.record_stage_execution(
            pipeline_run_id=_RUN_ELIGIBLE,
            stage_name="ingest",
            started_at="2026-05-25T10:00:00+00:00",
            ended_at="2026-05-25T10:00:30+00:00",
            status="succeeded",
        )
        store.record_stage_execution(
            pipeline_run_id=_RUN_ELIGIBLE,
            stage_name="synthesize",
            started_at="2026-05-25T10:00:30+00:00",
            ended_at="2026-05-25T10:01:00+00:00",
            status="failed",
            error_kind="TtsError",
            error_message=_ERROR_MESSAGE_POISON,
        )
        _add_envelope(store, _RUN_ELIGIBLE, "APPROVED")

        # governance-blocked: failed at ingest, BLOCKED envelope
        _add_run(store, _RUN_BLOCKED, "failed", "ingest")
        store.record_stage_execution(
            pipeline_run_id=_RUN_BLOCKED,
            stage_name="ingest",
            started_at="2026-05-25T10:00:00+00:00",
            ended_at="2026-05-25T10:00:30+00:00",
            status="failed",
            error_kind="SourceNotApproved",
        )
        _add_envelope(store, _RUN_BLOCKED, "BLOCKED")

        # trust-envelope-denied: failed at synthesize, NEEDS_REVIEW envelope
        _add_run(store, _RUN_DENIED, "failed", "synthesize")
        store.record_stage_execution(
            pipeline_run_id=_RUN_DENIED,
            stage_name="synthesize",
            started_at="2026-05-25T10:00:30+00:00",
            ended_at="2026-05-25T10:01:00+00:00",
            status="failed",
            error_kind="TtsError",
        )
        _add_envelope(store, _RUN_DENIED, "NEEDS_REVIEW")

        # no-envelope: failed at synthesize, no Trust Envelope projection
        _add_run(store, _RUN_NO_ENVELOPE, "failed", "synthesize")
        store.record_stage_execution(
            pipeline_run_id=_RUN_NO_ENVELOPE,
            stage_name="synthesize",
            started_at="2026-05-25T10:00:30+00:00",
            ended_at="2026-05-25T10:01:00+00:00",
            status="failed",
            error_kind="TtsError",
        )

        # operator-rejected: failed at approve_text gate (TextRejected)
        _add_run(store, _RUN_OPERATOR_REJECTED, "failed", "approve_text")
        store.record_stage_execution(
            pipeline_run_id=_RUN_OPERATOR_REJECTED,
            stage_name="approve_text",
            started_at="2026-05-25T10:00:30+00:00",
            ended_at="2026-05-25T10:01:00+00:00",
            status="failed",
            error_kind="TextRejected",
        )
        _add_envelope(store, _RUN_OPERATOR_REJECTED, "APPROVED")

        # completed: not a re-run target
        _add_run(store, _RUN_COMPLETED, "completed", "publish")
        store.record_stage_execution(
            pipeline_run_id=_RUN_COMPLETED,
            stage_name="publish",
            started_at="2026-05-25T10:00:30+00:00",
            ended_at="2026-05-25T10:01:00+00:00",
            status="succeeded",
        )
        _add_envelope(store, _RUN_COMPLETED, "APPROVED")

        # inconsistent: status failed but no failed stage execution
        _add_run(store, _RUN_INCONSISTENT, "failed", "synthesize")
        _add_envelope(store, _RUN_INCONSISTENT, "APPROVED")


@pytest.fixture()
def seeded_store(tmp_path: Path) -> Iterator[StateStore]:
    """An open StateStore seeded with the seven Phase 10D run shapes."""
    with StateStore.open(tmp_path / "state.db") as store:
        _seed(store)
        yield store


@pytest.fixture()
def clock() -> FixedClock:
    from datetime import UTC, datetime

    return FixedClock(datetime(2026, 5, 25, 12, 0, 0, tzinfo=UTC))


# --- eligibility decisions -------------------------------------------------


def test_eligible_failed_run_is_eligible(seeded_store: StateStore) -> None:
    decision = evaluate_rerun_eligibility(seeded_store, _RUN_ELIGIBLE)
    assert decision.eligible
    assert decision.code == CODE_ELIGIBLE
    assert decision.from_stage == "synthesize"
    assert decision.governance_status == "APPROVED"


def test_nonexistent_run_is_rejected(seeded_store: StateStore) -> None:
    decision = evaluate_rerun_eligibility(seeded_store, "01NOSUCHRUN0000000000000XX")
    assert not decision.eligible
    assert decision.code == CODE_RUN_NOT_FOUND


def test_completed_run_is_not_retryable(seeded_store: StateStore) -> None:
    decision = evaluate_rerun_eligibility(seeded_store, _RUN_COMPLETED)
    assert not decision.eligible
    assert decision.code == CODE_NOT_RETRYABLE_STATUS


def test_governance_blocked_run_is_rejected(seeded_store: StateStore) -> None:
    decision = evaluate_rerun_eligibility(seeded_store, _RUN_BLOCKED)
    assert not decision.eligible
    assert decision.code == CODE_GOVERNANCE_BLOCKED


def test_needs_review_envelope_is_rejected(seeded_store: StateStore) -> None:
    decision = evaluate_rerun_eligibility(seeded_store, _RUN_DENIED)
    assert not decision.eligible
    assert decision.code == CODE_TRUST_ENVELOPE_DENIED


def test_missing_trust_envelope_is_rejected(seeded_store: StateStore) -> None:
    decision = evaluate_rerun_eligibility(seeded_store, _RUN_NO_ENVELOPE)
    assert not decision.eligible
    assert decision.code == CODE_TRUST_ENVELOPE_MISSING


def test_operator_rejected_run_is_rejected(seeded_store: StateStore) -> None:
    # A run rejected by the operator at an approval gate cannot be re-run —
    # that would override the operator's explicit decision.
    decision = evaluate_rerun_eligibility(seeded_store, _RUN_OPERATOR_REJECTED)
    assert not decision.eligible
    assert decision.code == CODE_OPERATOR_REJECTED


def test_inconsistent_failed_run_is_rejected(seeded_store: StateStore) -> None:
    decision = evaluate_rerun_eligibility(seeded_store, _RUN_INCONSISTENT)
    assert not decision.eligible
    assert decision.code == CODE_UNSAFE_UNKNOWN_STATE


def test_unknown_from_stage_is_rejected(seeded_store: StateStore) -> None:
    decision = evaluate_rerun_eligibility(
        seeded_store, _RUN_ELIGIBLE, requested_from_stage="not-a-stage"
    )
    assert not decision.eligible
    assert decision.code == CODE_STAGE_UNKNOWN


def test_mismatched_from_stage_is_rejected(seeded_store: StateStore) -> None:
    # A valid stage that is not the run's failed stage is rejected.
    decision = evaluate_rerun_eligibility(
        seeded_store, _RUN_ELIGIBLE, requested_from_stage="ingest"
    )
    assert not decision.eligible
    assert decision.code == CODE_STAGE_MISMATCH


def test_matching_from_stage_is_eligible(seeded_store: StateStore) -> None:
    decision = evaluate_rerun_eligibility(
        seeded_store, _RUN_ELIGIBLE, requested_from_stage="synthesize"
    )
    assert decision.eligible
    assert decision.code == CODE_ELIGIBLE


# --- dry run vs actual mutation --------------------------------------------


def test_dry_run_does_not_mutate_state(
    seeded_store: StateStore, clock: FixedClock
) -> None:
    before = seeded_store.get_run(_RUN_ELIGIBLE)
    before_events = seeded_store.count_events(_RUN_ELIGIBLE)
    result = perform_rerun(seeded_store, clock, _RUN_ELIGIBLE, dry_run=True)
    assert result.decision.eligible
    assert not result.performed
    after = seeded_store.get_run(_RUN_ELIGIBLE)
    assert after == before  # run row unchanged
    assert seeded_store.count_events(_RUN_ELIGIBLE) == before_events  # no audit event


def test_eligible_run_can_be_previewed(
    seeded_store: StateStore, clock: FixedClock
) -> None:
    result = perform_rerun(seeded_store, clock, _RUN_ELIGIBLE, dry_run=True)
    assert result.decision.eligible
    assert not result.performed
    assert result.mutation_id is None


def test_actual_rerun_resets_status_to_running(
    seeded_store: StateStore, clock: FixedClock
) -> None:
    result = perform_rerun(seeded_store, clock, _RUN_ELIGIBLE)
    assert result.performed
    assert result.previous_status == "failed"
    assert result.new_status == "running"
    after = seeded_store.get_run(_RUN_ELIGIBLE)
    assert after is not None
    assert after.status == "running"


def test_actual_rerun_mutates_only_bounded_state(
    seeded_store: StateStore, clock: FixedClock
) -> None:
    before = seeded_store.get_run(_RUN_ELIGIBLE)
    assert before is not None
    before_stages = seeded_store.list_stage_executions(_RUN_ELIGIBLE)
    perform_rerun(seeded_store, clock, _RUN_ELIGIBLE)
    after = seeded_store.get_run(_RUN_ELIGIBLE)
    assert after is not None
    # Only status (and updated_at) change; identity, stage, gates untouched.
    assert after.pipeline_run_id == before.pipeline_run_id
    assert after.current_stage == before.current_stage
    assert after.created_at == before.created_at
    assert after.gates == before.gates
    assert after.source_manifest_hash == before.source_manifest_hash
    # The re-run command runs no pipeline work: stage executions are unchanged.
    assert seeded_store.list_stage_executions(_RUN_ELIGIBLE) == before_stages


def test_actual_rerun_writes_one_audit_event(
    seeded_store: StateStore, clock: FixedClock
) -> None:
    before = seeded_store.count_events(_RUN_ELIGIBLE)
    result = perform_rerun(seeded_store, clock, _RUN_ELIGIBLE)
    assert result.performed
    assert seeded_store.count_events(_RUN_ELIGIBLE) == before + 1
    assert "RunRerunRequested" in seeded_store.event_types(_RUN_ELIGIBLE)
    assert result.mutation_id is not None and result.mutation_id


def test_rejected_run_is_not_mutated(
    seeded_store: StateStore, clock: FixedClock
) -> None:
    before = seeded_store.get_run(_RUN_BLOCKED)
    before_events = seeded_store.count_events(_RUN_BLOCKED)
    result = perform_rerun(seeded_store, clock, _RUN_BLOCKED)
    assert not result.decision.eligible
    assert not result.performed
    assert seeded_store.get_run(_RUN_BLOCKED) == before
    assert seeded_store.count_events(_RUN_BLOCKED) == before_events


def test_rerun_makes_run_resumable(
    seeded_store: StateStore, clock: FixedClock
) -> None:
    # After a re-run reset, the run is no longer in the terminal failed state.
    perform_rerun(seeded_store, clock, _RUN_ELIGIBLE)
    after = seeded_store.get_run(_RUN_ELIGIBLE)
    assert after is not None
    assert after.status != "failed"
    assert after.status == "running"


# --- output: JSON allowlist + privacy --------------------------------------


def test_json_output_is_allowlisted(
    seeded_store: StateStore, clock: FixedClock
) -> None:
    result = perform_rerun(seeded_store, clock, _RUN_ELIGIBLE)
    payload = json.loads(render_rerun_json(result))
    expected = {
        "run_id",
        "source_id",
        "current_status",
        "requested_action",
        "from_stage",
        "dry_run",
        "eligible",
        "code",
        "message",
        "mutation_id",
        "previous_status",
        "new_status",
        "governance_status",
        "next_action",
    }
    assert set(payload.keys()) == expected


def test_json_output_structure_is_stable(seeded_store: StateStore) -> None:
    # Two dry-run evaluations of identical state yield identical JSON.
    from datetime import UTC, datetime

    c = FixedClock(datetime(2026, 5, 25, 12, 0, 0, tzinfo=UTC))
    first = render_rerun_json(perform_rerun(seeded_store, c, _RUN_BLOCKED))
    second = render_rerun_json(perform_rerun(seeded_store, c, _RUN_BLOCKED))
    assert first == second


def test_output_does_not_expose_raw_error_message(
    seeded_store: StateStore, clock: FixedClock
) -> None:
    # The poisoned unbounded error_message must never reach the re-run output.
    result = perform_rerun(seeded_store, clock, _RUN_ELIGIBLE, dry_run=True)
    text = render_rerun_text(result)
    payload = render_rerun_json(result)
    assert _ERROR_MESSAGE_POISON not in text
    assert _ERROR_MESSAGE_POISON not in payload
    # The structured error category is acceptable; the raw message is not.


# --- CLI -------------------------------------------------------------------


def _env(tmp_path: Path) -> dict[str, str]:
    return {
        "STORYTIME_RUNS_DIR": str(tmp_path / "runs"),
        "STORYTIME_FEED_DIR": str(tmp_path / "feed"),
        "STORYTIME_TELEMETRY": "noop",
    }


def test_cli_rerun_dry_run_previews_without_mutation(tmp_path: Path) -> None:
    with StateStore.open(tmp_path / "runs" / "state.db") as store:
        _seed(store)
    result = runner.invoke(
        app, ["rerun", _RUN_ELIGIBLE, "--dry-run"], env=_env(tmp_path)
    )
    assert result.exit_code == 0, result.output
    assert "dry run" in result.output.lower()
    with StateStore.open(tmp_path / "runs" / "state.db") as store:
        run = store.get_run(_RUN_ELIGIBLE)
        assert run is not None and run.status == "failed"


def test_cli_rerun_applies_the_reset(tmp_path: Path) -> None:
    with StateStore.open(tmp_path / "runs" / "state.db") as store:
        _seed(store)
    result = runner.invoke(app, ["rerun", _RUN_ELIGIBLE], env=_env(tmp_path))
    assert result.exit_code == 0, result.output
    assert "RE-RUN APPLIED" in result.output
    assert "storytime run --resume" in result.output
    with StateStore.open(tmp_path / "runs" / "state.db") as store:
        run = store.get_run(_RUN_ELIGIBLE)
        assert run is not None and run.status == "running"


def test_cli_rerun_rejects_governance_blocked_run(tmp_path: Path) -> None:
    with StateStore.open(tmp_path / "runs" / "state.db") as store:
        _seed(store)
    result = runner.invoke(app, ["rerun", _RUN_BLOCKED], env=_env(tmp_path))
    assert result.exit_code == 1
    assert "governance_blocked" in result.output


def test_cli_rerun_json_mode(tmp_path: Path) -> None:
    with StateStore.open(tmp_path / "runs" / "state.db") as store:
        _seed(store)
    result = runner.invoke(
        app, ["rerun", _RUN_ELIGIBLE, "--dry-run", "--json"], env=_env(tmp_path)
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["run_id"] == _RUN_ELIGIBLE
    assert payload["eligible"] is True


def test_cli_rerun_is_discoverable(tmp_path: Path) -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "rerun" in result.output


# --- Phase 10C queue is unaffected -----------------------------------------


def test_phase_10c_queue_still_works(tmp_path: Path) -> None:
    # The Phase 10C read-only queue command still lists failed runs and is
    # itself read-only — Phase 10D does not degrade it.
    with StateStore.open(tmp_path / "runs" / "state.db") as store:
        _seed(store)
    result = runner.invoke(app, ["queue"], env=_env(tmp_path))
    assert result.exit_code == 0, result.output
    assert _RUN_ELIGIBLE in result.output
    # The queue did not mutate any run.
    with StateStore.open(tmp_path / "runs" / "state.db") as store:
        run = store.get_run(_RUN_ELIGIBLE)
        assert run is not None and run.status == "failed"
