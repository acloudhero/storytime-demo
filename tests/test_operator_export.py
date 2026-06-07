"""Phase 13C — deterministic static export contract tests.

These tests protect the read-only static UI export produced by
``storytime.operator_export`` (and the ``storytime export-demo-ui`` CLI
command) and the committed artifact ``frontend/src/data/storytime-demo-export.json``.

They lock the Phase 13C contract guarantees:

* the export builds, renders to JSON, and round-trips through ``json.loads``;
* a top-level ``schemaVersion`` is present, and the required top-level sections
  exist;
* the export is deterministic — repeated builds and repeated renders are
  byte-identical, and the committed JSON file matches a fresh render;
* run / stage / artifact / link ids are strings;
* run, stage, and governance statuses are drawn from the known allowed sets;
* timestamps are valid ISO-8601 strings;
* evidence links and artifacts are typed objects, not loose strings;
* governance text is display-safe — no raw ``blocked_reason`` free text, no
  legal-overclaiming vocabulary;
* disabled future actions stay disabled and never imply mutation is available.

The tests assert the JSON contract that the frontend TypeScript types in
``frontend/src/types/storytime.ts`` mirror; the TypeScript side is checked
separately by the frontend ``tsc`` typecheck and build.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

import pytest

from storytime.operator_export import (
    DEFAULT_EXPORT_RELPATH,
    EXPORT_KIND,
    GENERATED_BY,
    SCHEMA_VERSION,
    build_static_demo_export,
    render_export_json,
    write_static_demo_export,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]

_RUN_STATUSES = {
    "queued",
    "running",
    "succeeded",
    "failed",
    "blocked",
    "recovered",
}
_STAGE_STATUSES = {
    "not_started",
    "running",
    "succeeded",
    "failed",
    "blocked",
    "skipped",
}
_GOVERNANCE_STATUSES = {"allowed", "review_required", "blocked"}


def _export() -> dict[str, Any]:
    """Return a freshly built export envelope."""
    return build_static_demo_export()


def _is_iso8601(value: str) -> bool:
    """True if *value* parses as an ISO-8601 timestamp."""
    try:
        dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


class TestExportEnvelope:
    """The export envelope shape and metadata."""

    def test_export_builds_and_is_a_mapping(self) -> None:
        assert isinstance(_export(), dict)

    def test_export_renders_and_round_trips(self) -> None:
        text = render_export_json(_export())
        assert text.endswith("\n")
        assert json.loads(text) == _export()

    def test_schema_version_present(self) -> None:
        export = _export()
        assert export["schemaVersion"] == SCHEMA_VERSION
        assert isinstance(export["schemaVersion"], str)
        assert export["schemaVersion"].strip()

    def test_required_top_level_sections_exist(self) -> None:
        export = _export()
        for key in (
            "schemaVersion",
            "generatedBy",
            "exportKind",
            "project",
            "runs",
            "failureQueue",
        ):
            assert key in export, f"export missing top-level section: {key}"
        assert export["generatedBy"] == GENERATED_BY
        assert export["exportKind"] == EXPORT_KIND
        assert isinstance(export["project"], dict)
        assert isinstance(export["runs"], list) and export["runs"]
        assert isinstance(export["failureQueue"], list)

    def test_project_summary_shape(self) -> None:
        project = _export()["project"]
        for key in (
            "name",
            "tagline",
            "description",
            "currentPhase",
            "currentPhaseStatus",
            "demonstrates",
            "notClaims",
            "reviewerPaths",
        ):
            assert key in project, f"project missing key: {key}"
        assert isinstance(project["reviewerPaths"], list)
        assert project["reviewerPaths"], "reviewerPaths is empty"
        for path in project["reviewerPaths"]:
            assert isinstance(path["id"], str)
            assert isinstance(path["steps"], list) and path["steps"]


class TestDeterminism:
    """The export must be byte-stable."""

    def test_repeated_builds_are_equal(self) -> None:
        assert build_static_demo_export() == build_static_demo_export()

    def test_repeated_renders_are_byte_identical(self) -> None:
        first = render_export_json(build_static_demo_export())
        second = render_export_json(build_static_demo_export())
        assert first == second

    def test_render_is_sorted_and_stable(self) -> None:
        text = render_export_json(_export())
        # sort_keys=True => the top-level keys appear in sorted order.
        parsed_keys = list(json.loads(text).keys())
        assert parsed_keys == sorted(parsed_keys)

    def test_write_is_idempotent(self, tmp_path: Path) -> None:
        target = tmp_path / "export.json"
        write_static_demo_export(target)
        first = target.read_bytes()
        write_static_demo_export(target)
        second = target.read_bytes()
        assert first == second

    def test_committed_export_matches_fresh_render(self) -> None:
        """The committed JSON artifact equals a fresh deterministic render.

        If this fails, regenerate with ``uv run storytime export-demo-ui``.
        """
        committed = _REPO_ROOT / DEFAULT_EXPORT_RELPATH
        assert committed.is_file(), f"missing committed export: {committed}"
        expected = render_export_json(build_static_demo_export())
        assert committed.read_text(encoding="utf-8") == expected


class TestRunContract:
    """Per-run shape, ids, statuses, and timestamps."""

    def test_run_ids_and_labels_are_strings(self) -> None:
        for run in _export()["runs"]:
            assert isinstance(run["id"], str) and run["id"]
            assert isinstance(run["label"], str) and run["label"]

    def test_run_statuses_are_allowed(self) -> None:
        for run in _export()["runs"]:
            assert run["status"] in _RUN_STATUSES

    def test_run_timestamps_are_iso8601(self) -> None:
        for run in _export()["runs"]:
            assert _is_iso8601(run["createdAt"])
            assert _is_iso8601(run["updatedAt"])

    def test_stage_contract(self) -> None:
        for run in _export()["runs"]:
            stages = run["stages"]
            assert stages, f"run {run['id']} has no stages"
            orders = [stage["order"] for stage in stages]
            assert orders == sorted(orders), "stages are not order-sorted"
            for stage in stages:
                assert isinstance(stage["id"], str) and stage["id"]
                assert isinstance(stage["name"], str)
                assert isinstance(stage["order"], int)
                assert isinstance(stage["isApprovalGate"], bool)
                assert stage["status"] in _STAGE_STATUSES
                for field in ("startedAt", "endedAt"):
                    if field in stage:
                        assert _is_iso8601(stage[field])

    def test_governance_statuses_are_allowed(self) -> None:
        for run in _export()["runs"]:
            assert run["governance"]["status"] in _GOVERNANCE_STATUSES

    def test_artifacts_and_links_are_typed_objects(self) -> None:
        for run in _export()["runs"]:
            for artifact in run["artifacts"]:
                assert isinstance(artifact, dict)
                assert isinstance(artifact["id"], str)
                assert isinstance(artifact["reference"], str)
                assert artifact["kind"] in {
                    "audio",
                    "feed",
                    "episode_metadata",
                    "report",
                }
            links = run["observability"]["links"]
            for link in links:
                assert isinstance(link, dict)
                assert isinstance(link["id"], str)
                assert isinstance(link["reference"], str)
                assert link["kind"] in {
                    "doc",
                    "report",
                    "dashboard",
                    "trace",
                    "artifact",
                    "external",
                }


class TestSafetyDiscipline:
    """Display-safety: no raw blocked reasons, no legal overclaiming, no
    mutation availability implied by a disabled action."""

    def test_governance_text_is_display_safe(self) -> None:
        # The export must not carry a raw free-text "blocked_reason" field, and
        # the source category must be a short structured code, not prose.
        for run in _export()["runs"]:
            governance = run["governance"]
            assert "blocked_reason" not in governance
            assert "blockedReason" not in governance
            category = governance["sourceCategory"]
            assert isinstance(category, str)
            assert " " not in category, "sourceCategory should be a code"

    def test_failure_uses_structured_error_kind_only(self) -> None:
        for run in _export()["runs"]:
            failure = run.get("failure")
            if failure is None:
                continue
            assert set(failure.keys()) == {"errorKind", "operatorGuidance"}
            # error kind is a structured upper-case code, not a raw message
            assert failure["errorKind"] == failure["errorKind"].upper()
            assert "raw_message" not in failure

    def test_no_legal_overclaiming_vocabulary(self) -> None:
        text = render_export_json(_export()).lower()
        for banned in (
            "guaranteed copyright",
            "certified copyright",
            "legal advice provided",
            "copyright cleared",
        ):
            assert banned not in text, f"overclaiming phrase present: {banned}"

    def test_disabled_actions_stay_disabled(self) -> None:
        for run in _export()["runs"]:
            for action in run["disabledActions"]:
                assert isinstance(action["disabledReason"], str)
                assert action["disabledReason"].strip()
                assert isinstance(action["enabledByPhase"], str)
                assert isinstance(action["isMutation"], bool)
                # a disabled action carries no payload that could be invoked
                assert "payload" not in action
                assert "endpoint" not in action

    def test_allowed_actions_are_non_mutating(self) -> None:
        for run in _export()["runs"]:
            for action in run["allowedActions"]:
                # the only allowed-action kinds are non-mutating affordances
                assert action["kind"] in {"copy_command", "open_reference"}


class TestFailureQueue:
    """The failure / review queue projection."""

    def test_failure_queue_entries_are_typed(self) -> None:
        for item in _export()["failureQueue"]:
            assert isinstance(item["runId"], str)
            assert isinstance(item["runLabel"], str)
            assert item["reason"] in {
                "failed",
                "blocked",
                "needs_review",
                "awaiting_approval",
            }
            assert isinstance(item["summary"], str)
            assert isinstance(item["inspectNext"], str)

    def test_failure_queue_runs_exist_in_runs(self) -> None:
        export = _export()
        run_ids = {run["id"] for run in export["runs"]}
        for item in export["failureQueue"]:
            assert item["runId"] in run_ids


@pytest.mark.parametrize("attr", ["SCHEMA_VERSION", "GENERATED_BY", "EXPORT_KIND"])
def test_module_constants_are_nonempty_strings(attr: str) -> None:
    import storytime.operator_export as module

    value = getattr(module, attr)
    assert isinstance(value, str) and value.strip()
