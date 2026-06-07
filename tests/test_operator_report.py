"""Phase 10B — operator report tests (Architecture Baseline Section 25).

These tests exercise the generated static operator report against three run
shapes (completed, governance-blocked, failed) and lock the Section 25
guarantees: no raw content, no secrets, no long free-text governance notes, no
forbidden legal/compliance overclaiming, byte-for-byte determinism under a
fixed injected timestamp, optional sanitized observability links, an
air-gapped report (no external CDN/font/script/asset), and a read-only command
that mutates no state.

The fixtures are built directly through the StateStore and the durable Trust
Envelope writer — the smallest local fixtures that produce the three run
shapes without running the whole pipeline.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from typer.testing import CliRunner

from storytime.adapters.storage import LocalFilesystemStorage
from storytime.cli.app import app
from storytime.governance import FORBIDDEN_LEGAL_TERMS
from storytime.governance.io import write_trust_envelope
from storytime.governance.trust_envelope import (
    TRUST_ENVELOPE_SCHEMA_VERSION,
    GovernanceDecision,
    LicenseType,
    TrustEnvelope,
)
from storytime.reporting import (
    REVIEW_CONTEXT_SUMMARY_MAX_CHARS,
    generate_report,
)
from storytime.state import RunRecord, StateStore

# --- poison markers --------------------------------------------------------
# Unique strings planted in fields the report MUST NOT surface. If any of these
# reaches the generated HTML, a Section 25 privacy guarantee has been broken.
_RAW_STORY_POISON = "RAWSTORYTEXTPOISON-once-upon-a-midnight-dreary-while-i-pondered"
_NARRATION_POISON = "NARRATIONTEXTPOISON-synthesized-audio-script-body"
_SECRET_POISON = "sk-SECRETTOKENPOISON-0123456789abcdef-api-key"  # noqa: S105
_SUMMARY_TAIL_POISON = "SUMMARYTAILPOISON-this-must-be-truncated-away"

# A long governance_notes value: raw-content + secret + narration poisons plus
# bulk text. governance_notes is never projected into the report model, so the
# whole blob must be absent from every generated page.
_LONG_GOVERNANCE_NOTES = (
    f"{_RAW_STORY_POISON} {_NARRATION_POISON} {_SECRET_POISON} "
    + ("deliberation history padding. " * 60)
)

# A review_context_summary longer than the locked display bound, ending in a
# poison marker beyond the bound so a correct truncation drops the marker.
_LONG_SUMMARY = (
    "Operator verified the source authorization record. "
    * 20
) + _SUMMARY_TAIL_POISON

_RUN_COMPLETED = "01RUNCOMPLETED000000000000"
_RUN_BLOCKED = "01RUNBLOCKED00000000000000"
_RUN_FAILED = "01RUNFAILED000000000000000"

runner = CliRunner()


def _seed_runs(store: StateStore, storage: LocalFilesystemStorage) -> None:
    """Seed three run shapes into the state store and durable artifacts.

    completed -> all stages SUCCEEDED, APPROVED Trust Envelope, published audio.
    blocked   -> BLOCKED Trust Envelope with a blocked reason; a long, poisoned
                 review summary and poisoned governance notes.
    failed    -> a stage carrying a structured error_kind, no Trust Envelope.
    """
    # -- completed run ----------------------------------------------------
    with store.transaction():
        store.create_run(
            RunRecord(
                pipeline_run_id=_RUN_COMPLETED,
                created_at="2026-05-20T10:00:00+00:00",
                updated_at="2026-05-20T10:05:00+00:00",
                current_stage="publish",
                status="completed",
                source_manifest_hash="a" * 64,
                run_dir=_RUN_COMPLETED,
                gates=("text",),
            )
        )
        for stage in ("ingest", "synthesize", "assemble", "publish"):
            store.record_stage_execution(
                pipeline_run_id=_RUN_COMPLETED,
                stage_name=stage,
                started_at="2026-05-20T10:00:00+00:00",
                ended_at="2026-05-20T10:05:00+00:00",
                status="SUCCEEDED",
                trace_id="trace-completed-0001",
            )
        store.record_stage_artifacts(
            pipeline_run_id=_RUN_COMPLETED,
            stage_name="synthesize",
            artifact_keys=[f"{_RUN_COMPLETED}/synthesize/audio-envelope.json"],
            recorded_at="2026-05-20T10:03:00+00:00",
        )
        store.record_published_episode(
            episode_guid="01EPISODECOMPLETED00000000",
            pipeline_run_id=_RUN_COMPLETED,
            title="The Raven",
            published_at="2026-05-20T10:05:00+00:00",
            audio_path=f"{_RUN_COMPLETED}/assemble/the-raven.mp3",
            audio_bytes=123456,
            duration_seconds=42.0,
            feed_version=1,
        )
        store.record_trust_envelope(
            pipeline_run_id=_RUN_COMPLETED,
            source_ref="the-raven",
            schema_version=TRUST_ENVELOPE_SCHEMA_VERSION,
            license_type=str(LicenseType.US_PUBLIC_DOMAIN),
            decision=str(GovernanceDecision.APPROVED),
            decision_timestamp="2026-05-20T09:55:00+00:00",
            approver_id="operator",
            blocked_reason=None,
            envelope_key=f"{_RUN_COMPLETED}/governance/trust-envelope.json",
            recorded_at="2026-05-20T10:00:30+00:00",
        )
    write_trust_envelope(
        storage,
        _RUN_COMPLETED,
        TrustEnvelope(
            schema_version=TRUST_ENVELOPE_SCHEMA_VERSION,
            source_ref="the-raven",
            license_type=LicenseType.US_PUBLIC_DOMAIN,
            decision=GovernanceDecision.APPROVED,
            decision_timestamp="2026-05-20T09:55:00+00:00",
            approver_id="operator",
            review_context_summary="Public-domain text confirmed by the operator.",
        ),
    )

    # -- governance-blocked run ------------------------------------------
    with store.transaction():
        store.create_run(
            RunRecord(
                pipeline_run_id=_RUN_BLOCKED,
                created_at="2026-05-21T11:00:00+00:00",
                updated_at="2026-05-21T11:01:00+00:00",
                current_stage="ingest",
                status="blocked",
                source_manifest_hash="b" * 64,
                run_dir=_RUN_BLOCKED,
            )
        )
        store.record_stage_execution(
            pipeline_run_id=_RUN_BLOCKED,
            stage_name="ingest",
            started_at="2026-05-21T11:00:00+00:00",
            ended_at="2026-05-21T11:01:00+00:00",
            status="FAILED",
            error_kind="GovernanceBlocked",
        )
        store.record_trust_envelope(
            pipeline_run_id=_RUN_BLOCKED,
            source_ref="blocked-source",
            schema_version=TRUST_ENVELOPE_SCHEMA_VERSION,
            license_type=str(LicenseType.BLOCKED),
            decision=str(GovernanceDecision.BLOCKED),
            decision_timestamp="2026-05-21T10:55:00+00:00",
            approver_id="operator",
            blocked_reason="Source matched the local blocked-source list.",
            envelope_key=f"{_RUN_BLOCKED}/governance/trust-envelope.json",
            recorded_at="2026-05-21T11:00:30+00:00",
        )
    write_trust_envelope(
        storage,
        _RUN_BLOCKED,
        TrustEnvelope(
            schema_version=TRUST_ENVELOPE_SCHEMA_VERSION,
            source_ref="blocked-source",
            license_type=LicenseType.BLOCKED,
            decision=GovernanceDecision.BLOCKED,
            decision_timestamp="2026-05-21T10:55:00+00:00",
            approver_id="operator",
            blocked_reason="Source matched the local blocked-source list.",
            governance_notes=_LONG_GOVERNANCE_NOTES,
            review_context_summary=_LONG_SUMMARY,
        ),
    )

    # -- failed (non-governance) run -------------------------------------
    with store.transaction():
        store.create_run(
            RunRecord(
                pipeline_run_id=_RUN_FAILED,
                created_at="2026-05-22T12:00:00+00:00",
                updated_at="2026-05-22T12:02:00+00:00",
                current_stage="synthesize",
                status="failed",
                source_manifest_hash="c" * 64,
                run_dir=_RUN_FAILED,
            )
        )
        store.record_stage_execution(
            pipeline_run_id=_RUN_FAILED,
            stage_name="ingest",
            started_at="2026-05-22T12:00:00+00:00",
            ended_at="2026-05-22T12:01:00+00:00",
            status="SUCCEEDED",
        )
        store.record_stage_execution(
            pipeline_run_id=_RUN_FAILED,
            stage_name="synthesize",
            started_at="2026-05-22T12:01:00+00:00",
            ended_at="2026-05-22T12:02:00+00:00",
            status="FAILED",
            error_kind="TtsError",
        )


@pytest.fixture()
def seeded(tmp_path: Path) -> Iterator[tuple[StateStore, LocalFilesystemStorage]]:
    """An open StateStore plus storage, seeded with the three run shapes."""
    storage = LocalFilesystemStorage(tmp_path / "runs")
    with StateStore.open(tmp_path / "runs" / "state.db") as store:
        _seed_runs(store, storage)
        yield store, storage


def _generate(
    seeded: tuple[StateStore, LocalFilesystemStorage],
    out: Path,
    *,
    generated_at: str = "2026-05-24T00:00:00+00:00",
    observability: dict[str, str] | None = None,
) -> dict[str, str]:
    """Generate the report into *out* and return {filename: text}."""
    store, storage = seeded
    result = generate_report(
        store,
        storage,
        out,
        generated_at=generated_at,
        feed_reference="feed.xml",
        observability=observability,
    )
    return {p.name: p.read_text(encoding="utf-8") for p in result.files}


# --- the three run shapes generate -----------------------------------------


def test_report_generates_for_a_completed_run(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    detail = files[f"run-{_RUN_COMPLETED}.html"]
    assert "completed" in detail
    assert "SUCCEEDED" in detail
    assert "APPROVED" in detail
    assert "the-raven.mp3" in detail  # audio artifact reference present


def test_report_generates_for_a_governance_blocked_run(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    detail = files[f"run-{_RUN_BLOCKED}.html"]
    assert "BLOCKED" in detail
    # Raw blocked_reason must NOT appear — §25.12 redaction rule.
    assert "Source matched the local blocked-source list." not in detail
    # The exact full phrase must appear as one rendered string.
    _phrase = (
        "Decision detail: blocked by governance policy;"
        " inspect Trust Envelope locally if authorized."
    )
    assert _phrase in detail

def test_raw_blocked_reason_never_rendered(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    """§25.12 redaction: raw blocked_reason must never reach the HTML report."""
    files = _generate(seeded, tmp_path / "out")
    # The blocked run's seed data contains a raw blocked reason string.
    # It must not appear in any generated page.
    for name, text in files.items():
        assert "Source matched the local blocked-source list." not in text, name
    # The required safe wording must appear on the blocked-run detail page.
    detail = files[f"run-{_RUN_BLOCKED}.html"]
    # The exact full phrase must appear as one rendered value string.
    _phrase = (
        "Decision detail: blocked by governance policy;"
        " inspect Trust Envelope locally if authorized."
    )
    assert _phrase in detail


def test_report_generates_for_a_failed_run(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    detail = files[f"run-{_RUN_FAILED}.html"]
    assert "TtsError" in detail  # structured failure category surfaced
    assert "Failure" in detail


def test_report_has_index_runs_and_one_page_per_run(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    for name in (
        "index.html",
        "runs.html",
        "style.css",
        f"run-{_RUN_COMPLETED}.html",
        f"run-{_RUN_BLOCKED}.html",
        f"run-{_RUN_FAILED}.html",
    ):
        assert name in files, name
    # The run list links to every run detail page.
    for run_id in (_RUN_COMPLETED, _RUN_BLOCKED, _RUN_FAILED):
        assert f"run-{run_id}.html" in files["runs.html"]


# --- privacy / no-raw-content ----------------------------------------------


def test_report_excludes_raw_story_narration_and_secret_content(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    for name, text in files.items():
        assert _RAW_STORY_POISON not in text, name
        assert _NARRATION_POISON not in text, name
        assert _SECRET_POISON not in text, name


def test_report_excludes_long_free_text_governance_notes(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    # governance_notes is never projected into the report model; the long
    # padded blob must not appear anywhere.
    files = _generate(seeded, tmp_path / "out")
    for name, text in files.items():
        assert "deliberation history padding." not in text, name


def test_review_context_summary_is_bounded_and_truncated(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    detail = files[f"run-{_RUN_BLOCKED}.html"]
    # The over-long summary is truncated: the tail poison is dropped and a
    # visible truncation indicator is shown.
    assert _SUMMARY_TAIL_POISON not in detail
    assert "[…truncated]" in detail
    # No single displayed summary line exceeds the locked bound (plus the
    # short truncation indicator).
    for line in detail.splitlines():
        if "truncated" in line:
            assert len(line) <= REVIEW_CONTEXT_SUMMARY_MAX_CHARS + 80


def test_report_excludes_forbidden_legal_compliance_phrases(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    # Reuse the locked §24.14 forbidden-term set rather than re-listing the
    # phrases here, so this test file holds no forbidden literal of its own.
    files = _generate(seeded, tmp_path / "out")
    for name, text in files.items():
        lowered = text.lower()
        for term in FORBIDDEN_LEGAL_TERMS:
            assert term.lower() not in lowered, f"{term} in {name}"


# --- determinism -----------------------------------------------------------


def test_report_is_byte_for_byte_deterministic(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    first = _generate(seeded, tmp_path / "a", generated_at="2026-05-24T00:00:00+00:00")
    second = _generate(seeded, tmp_path / "b", generated_at="2026-05-24T00:00:00+00:00")
    assert first == second


def test_report_generated_at_comes_from_the_injected_timestamp(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out", generated_at="2099-01-02T03:04:05+00:00")
    assert "2099-01-02T03:04:05+00:00" in files["index.html"]


# --- allowed fields / projections ------------------------------------------


def test_report_shows_allowed_governance_and_run_fields(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    detail = files[f"run-{_RUN_COMPLETED}.html"]
    # Allowed §25.12 fields are present.
    assert _RUN_COMPLETED in detail
    assert "US_PUBLIC_DOMAIN" in detail
    assert "operator" in detail
    assert "ingest" in detail and "publish" in detail
    assert "Trust Envelope" in detail


# --- observability links ---------------------------------------------------


def test_observability_links_absent_by_default_report_still_complete(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out", observability=None)
    detail = files[f"run-{_RUN_COMPLETED}.html"]
    assert "No observability links configured" in detail


def test_observability_link_is_optional_and_sanitized(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(
        seeded,
        tmp_path / "out",
        observability={"jaeger_trace_base_url": "http://127.0.0.1:16686/trace"},
    )
    detail = files[f"run-{_RUN_COMPLETED}.html"]
    # The link is built from the configured base plus the run's trace id; it
    # carries no token or secret.
    assert "http://127.0.0.1:16686/trace/trace-completed-0001" in detail
    assert "token" not in detail.lower()
    assert "api-key" not in detail.lower()
    # A run with no recorded trace id gets no link, and the report is complete.
    blocked = files[f"run-{_RUN_BLOCKED}.html"]
    assert "No observability links configured" in blocked


# --- air-gapped: no external assets ----------------------------------------


def test_report_has_no_external_cdn_fonts_scripts_or_assets(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    # No observability configured -> the report must contain zero network URLs.
    files = _generate(seeded, tmp_path / "out", observability=None)
    for name, text in files.items():
        lowered = text.lower()
        assert "http://" not in lowered, name
        assert "https://" not in lowered, name
        assert "<script" not in lowered, name
        assert "cdn." not in lowered, name
        assert "googleapis" not in lowered, name
        assert "@font-face" not in lowered, name
        assert "unpkg" not in lowered and "jsdelivr" not in lowered, name
    # The only stylesheet reference is the local style.css.
    assert 'href="style.css"' in files["index.html"]


# --- read-only: no mutation ------------------------------------------------


def test_report_generation_does_not_mutate_state(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    store, _ = seeded
    before_runs = store.list_runs()
    before_stages = {
        r.pipeline_run_id: store.list_stage_executions(r.pipeline_run_id)
        for r in before_runs
    }
    before_envelopes = {
        r.pipeline_run_id: store.list_trust_envelopes(r.pipeline_run_id)
        for r in before_runs
    }
    _generate(seeded, tmp_path / "out")
    assert store.list_runs() == before_runs
    for run_id, stages in before_stages.items():
        assert store.list_stage_executions(run_id) == stages
    for run_id, envelopes in before_envelopes.items():
        assert store.list_trust_envelopes(run_id) == envelopes


def test_report_html_does_not_contain_forms_or_mutation_controls(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    for name, text in files.items():
        lowered = text.lower()
        assert "<form" not in lowered, name
        assert "<button" not in lowered, name
        assert "<input" not in lowered, name
        assert "method=\"post\"" not in lowered, name


# --- CLI -------------------------------------------------------------------


def test_cli_report_generate_writes_the_report(tmp_path: Path) -> None:
    runs_dir = tmp_path / "runs"
    storage = LocalFilesystemStorage(runs_dir)
    with StateStore.open(runs_dir / "state.db") as store:
        _seed_runs(store, storage)

    out = tmp_path / "operator-report"
    result = runner.invoke(
        app,
        ["report", "generate", "--output", str(out)],
        env={
            "STORYTIME_RUNS_DIR": str(runs_dir),
            "STORYTIME_FEED_DIR": str(tmp_path / "feed"),
            "STORYTIME_TELEMETRY": "noop",
        },
    )
    assert result.exit_code == 0, result.output
    assert (out / "index.html").exists()
    assert (out / f"run-{_RUN_COMPLETED}.html").exists()
    assert "3 run(s)" in result.output


def test_cli_report_generate_does_not_mutate_state(tmp_path: Path) -> None:
    runs_dir = tmp_path / "runs"
    storage = LocalFilesystemStorage(runs_dir)
    with StateStore.open(runs_dir / "state.db") as store:
        _seed_runs(store, storage)
        before = store.list_runs()

    result = runner.invoke(
        app,
        ["report", "generate", "--output", str(tmp_path / "out")],
        env={
            "STORYTIME_RUNS_DIR": str(runs_dir),
            "STORYTIME_FEED_DIR": str(tmp_path / "feed"),
            "STORYTIME_TELEMETRY": "noop",
        },
    )
    assert result.exit_code == 0, result.output
    with StateStore.open(runs_dir / "state.db") as store:
        assert store.list_runs() == before


def test_cli_report_command_is_discoverable(tmp_path: Path) -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "report" in result.output


# ==========================================================================
# Phase 10E — refined report tests
# ==========================================================================


# --- executive summary -----------------------------------------------------


def test_detail_page_has_executive_summary_section(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    for run_id in (_RUN_COMPLETED, _RUN_BLOCKED, _RUN_FAILED):
        detail = files[f"run-{run_id}.html"]
        assert "Executive Summary" in detail, run_id


def test_executive_summary_shows_status_badge(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    # Status badges use badge-* CSS classes
    assert "badge-completed" in files[f"run-{_RUN_COMPLETED}.html"]
    assert "badge-failed" in files[f"run-{_RUN_FAILED}.html"]


def test_executive_summary_shows_next_action(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    detail = files[f"run-{_RUN_FAILED}.html"]
    # The failed run with no Trust Envelope should not show eligible
    assert "Next action" in detail


# --- rerun eligibility section --------------------------------------------


def test_rerun_section_present_on_all_detail_pages(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    for run_id in (_RUN_COMPLETED, _RUN_BLOCKED, _RUN_FAILED):
        detail = files[f"run-{run_id}.html"]
        assert "Rerun Eligibility" in detail, run_id


def test_rerun_ineligible_for_completed_run(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    detail = files[f"run-{_RUN_COMPLETED}.html"]
    # completed run: not applicable — rerun section should say so
    assert "not applicable" in detail.lower() or "not_retryable_status" in detail.lower()
    # ELIGIBLE label must not appear in the rendered body content
    assert ">ELIGIBLE<" not in detail


def test_rerun_shows_ineligible_for_no_trust_envelope(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    # Failed run has no Trust Envelope — should be NOT ELIGIBLE
    detail = files[f"run-{_RUN_FAILED}.html"]
    assert "NOT ELIGIBLE" in detail or "badge-ineligible" in detail


def test_rerun_shows_ineligible_for_governance_blocked(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    detail = files[f"run-{_RUN_BLOCKED}.html"]
    assert "NOT ELIGIBLE" in detail or "badge-ineligible" in detail


def test_rerun_commands_are_plain_text_not_buttons(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    for name, text in files.items():
        lowered = text.lower()
        # Commands must not appear as form buttons or input elements
        assert "<button" not in lowered, name
        assert "<input" not in lowered, name
        assert "<form" not in lowered, name


def test_rerun_eligible_run_shows_commands(
    tmp_path: Path,
) -> None:
    """An APPROVED failed run should show rerun commands in the detail page."""
    from storytime.adapters.storage import LocalFilesystemStorage
    from storytime.governance.io import write_trust_envelope
    from storytime.governance.trust_envelope import (
        TRUST_ENVELOPE_SCHEMA_VERSION,
        GovernanceDecision,
        LicenseType,
        TrustEnvelope,
    )
    from storytime.reporting import generate_report
    from storytime.state import RunRecord, StateStore

    _RUN_ELIGIBLE = "01RUNELIGIBLE0000000000000"
    runs_dir = tmp_path / "runs"
    storage = LocalFilesystemStorage(runs_dir)
    with StateStore.open(runs_dir / "state.db") as store:
        with store.transaction():
            store.create_run(
                RunRecord(
                    pipeline_run_id=_RUN_ELIGIBLE,
                    created_at="2026-05-25T10:00:00+00:00",
                    updated_at="2026-05-25T10:02:00+00:00",
                    current_stage="synthesize",
                    status="failed",
                    source_manifest_hash="e" * 64,
                    run_dir=_RUN_ELIGIBLE,
                )
            )
            store.record_stage_execution(
                pipeline_run_id=_RUN_ELIGIBLE,
                stage_name="ingest",
                started_at="2026-05-25T10:00:00+00:00",
                ended_at="2026-05-25T10:01:00+00:00",
                status="SUCCEEDED",
            )
            store.record_stage_execution(
                pipeline_run_id=_RUN_ELIGIBLE,
                stage_name="synthesize",
                started_at="2026-05-25T10:01:00+00:00",
                ended_at="2026-05-25T10:02:00+00:00",
                status="FAILED",
                error_kind="TtsError",
            )
            store.record_trust_envelope(
                pipeline_run_id=_RUN_ELIGIBLE,
                source_ref="eligible-source",
                schema_version=TRUST_ENVELOPE_SCHEMA_VERSION,
                license_type=str(LicenseType.US_PUBLIC_DOMAIN),
                decision=str(GovernanceDecision.APPROVED),
                decision_timestamp="2026-05-25T09:55:00+00:00",
                approver_id="operator",
                blocked_reason=None,
                envelope_key=f"{_RUN_ELIGIBLE}/governance/trust-envelope.json",
                recorded_at="2026-05-25T10:00:30+00:00",
            )
        write_trust_envelope(
            storage,
            _RUN_ELIGIBLE,
            TrustEnvelope(
                schema_version=TRUST_ENVELOPE_SCHEMA_VERSION,
                source_ref="eligible-source",
                license_type=LicenseType.US_PUBLIC_DOMAIN,
                decision=GovernanceDecision.APPROVED,
                decision_timestamp="2026-05-25T09:55:00+00:00",
                approver_id="operator",
            ),
        )

        out = tmp_path / "report"
        result = generate_report(
            store, storage, out,
            generated_at="2026-05-25T12:00:00+00:00",
        )
        files = {p.name: p.read_text(encoding="utf-8") for p in result.files}

    detail = files[f"run-{_RUN_ELIGIBLE}.html"]
    # Should show ELIGIBLE badge
    assert "badge-eligible" in detail or "ELIGIBLE" in detail
    # Should show rerun commands as plain text
    assert f"storytime rerun {_RUN_ELIGIBLE}" in detail
    assert "storytime run --resume" in detail
    # Must not be in a button or form
    lowered = detail.lower()
    assert "<button" not in lowered
    assert "<form" not in lowered


# --- no JavaScript check --------------------------------------------------


def test_report_contains_no_javascript(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    for name, text in files.items():
        lowered = text.lower()
        assert "<script" not in lowered, f"<script> tag found in {name}"
        assert "javascript:" not in lowered, f"javascript: found in {name}"
        assert "onclick" not in lowered, f"onclick found in {name}"
        assert "onload" not in lowered, f"onload found in {name}"
        assert "onerror" not in lowered, f"onerror found in {name}"


# --- command reference section --------------------------------------------


def test_command_reference_section_present(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    for run_id in (_RUN_COMPLETED, _RUN_BLOCKED, _RUN_FAILED):
        detail = files[f"run-{run_id}.html"]
        assert "Command Reference" in detail, run_id
        assert "storytime rerun" in detail, run_id
        assert "storytime queue" in detail, run_id


def test_command_reference_plain_text_in_pre_block(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    for run_id in (_RUN_COMPLETED, _RUN_BLOCKED, _RUN_FAILED):
        detail = files[f"run-{run_id}.html"]
        assert 'class="command-block"' in detail, run_id


# --- embedded CSS check ---------------------------------------------------


def test_report_has_embedded_style_block(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    for name, text in files.items():
        if name.endswith(".html"):
            assert "<style>" in text.lower() or "<style\n" in text.lower() or "style>" in text, (
                f"No embedded <style> in {name}"
            )


def test_report_no_raw_exception_tracebacks(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    """Traceback-like text should never appear in the generated report."""
    files = _generate(seeded, tmp_path / "out")
    for name, text in files.items():
        lowered = text.lower()
        assert "traceback (most recent call last)" not in lowered, name
        assert "file \"/home" not in lowered, name
        assert "file \"/usr" not in lowered, name


# --- status badges on index / runs pages ----------------------------------


def test_run_list_pages_have_status_badges(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    assert "badge-" in files["index.html"]
    assert "badge-" in files["runs.html"]


def test_index_shows_attention_summary(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    # There is at least one failed run → the index should show an attention note
    index_lower = files["index.html"].lower()
    assert "need attention" in index_lower or "failed" in index_lower


# --- governance warning prominence ----------------------------------------


def test_governance_warning_visually_prominent(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    """The governance warning must use the governance-warning CSS class."""
    files = _generate(seeded, tmp_path / "out")
    for name, text in files.items():
        if name.endswith(".html"):
            assert "governance-warning" in text, (
                f"governance-warning class missing from {name}"
            )


# --- safety: no raw content in the new sections ---------------------------


def test_new_sections_do_not_expose_raw_content(
    seeded: tuple[StateStore, LocalFilesystemStorage], tmp_path: Path
) -> None:
    files = _generate(seeded, tmp_path / "out")
    for name, text in files.items():
        assert _RAW_STORY_POISON not in text, name
        assert _NARRATION_POISON not in text, name
        assert _SECRET_POISON not in text, name
        assert _SUMMARY_TAIL_POISON not in text, name
