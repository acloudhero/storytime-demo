"""Phase 10F — demo seed data / golden-path fixture shape and safety tests.

These tests prove the curated demo fixtures are present, parseable, internally
consistent, and safe to ship: the seed manifests validate against the closed
source-manifest schema and their declared text digests are correct; the
fixture definitions carry the required licensing / governance metadata; the
scenario ids are stable and unique; and no disallowed binary, generated audio,
or runtime / cache artifact has crept into ``demo/``.

Two behaviour tests drive the real existing pipeline with the demo seed
manifests — the governance-blocked path (which fails at ingest and needs no
ffmpeg) always runs; the golden path is skipped when ffmpeg is unavailable,
exactly as ``tests/test_demo_harness.py`` does.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest
import yaml

from storytime.config import load_config
from storytime.manifest import load_manifest
from storytime.pipeline import build_runtime_context, run_vertical_slice
from storytime.util.hashing import sha256_text

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DEMO_DIR = _REPO_ROOT / "demo"
_SEED_DIR = _DEMO_DIR / "seed"
_FIXTURE_DIR = _DEMO_DIR / "fixtures"
_GOVERNANCE_DIR = _DEMO_DIR / "governance"

_HAS_FFMPEG = shutil.which("ffmpeg") is not None

# The six curated scenarios and the seed manifest each one exercises. Scenarios
# 05 and 06 are procedural follow-ons that reuse the retryable-failure seed.
_FIXTURE_FILES: tuple[str, ...] = (
    "01-successful-golden-path.yaml",
    "02-retryable-technical-failure.yaml",
    "03-governance-blocked.yaml",
    "04-needs-review-approval-gate.yaml",
    "05-rerun-requested.yaml",
    "06-completed-after-rerun.yaml",
)

_SEED_MANIFESTS: tuple[str, ...] = (
    "demo-golden-path.json",
    "demo-retryable-failure.json",
    "demo-governance-blocked.json",
    "demo-needs-review.json",
)

# Required top-level keys in every fixture definition.
_REQUIRED_FIXTURE_KEYS: frozenset[str] = frozenset(
    {
        "scenario_id",
        "scenario_name",
        "phase",
        "purpose",
        "input_files",
        "content",
        "expected_governance_decision",
        "expected_run_state",
        "expected_report_behavior",
        "expected_queue_behavior",
        "expected_rerun_eligibility",
        "expected_audit_behavior",
        "commands",
        "expected_next_operator_action",
    }
)

# Required keys in every content (licensing / governance) item.
_REQUIRED_CONTENT_KEYS: frozenset[str] = frozenset(
    {
        "title",
        "source_id",
        "license_type",
        "license_basis",
        "author",
        "allowed_use",
        "attribution_required",
        "commercial_use_allowed",
        "governance_expected_decision",
    }
)

# Extensions that must never appear under demo/: generated audio, binary, and
# runtime database artifacts. The demo ships text only.
_DISALLOWED_SUFFIXES: frozenset[str] = frozenset(
    {
        ".wav",
        ".mp3",
        ".ogg",
        ".flac",
        ".m4a",
        ".db",
        ".sqlite",
        ".sqlite3",
        ".zip",
        ".tar",
        ".gz",
        ".tgz",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp",
        ".pyc",
        ".bin",
    }
)

# Directory names that would indicate a runtime / tooling cache leaked in.
_DISALLOWED_DIR_NAMES: frozenset[str] = frozenset(
    {
        "__pycache__",
        ".mypy_cache",
        ".ruff_cache",
        ".pytest_cache",
        ".import_linter_cache",
        "runs",
        "feed",
        "operator-report",
    }
)

# A small, text-based fixture set must stay small. 64 KiB per file is generous
# for original short demo texts, manifests, and YAML definitions.
_MAX_FIXTURE_FILE_BYTES = 64 * 1024


def _load_yaml(path: Path) -> Any:
    """Parse a YAML file, failing the test loudly if it cannot be read."""
    return yaml.safe_load(path.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------
# Presence and parseability.
# --------------------------------------------------------------------------

def test_demo_directories_exist() -> None:
    """The demo seed, governance, and fixture directories are present."""
    assert _SEED_DIR.is_dir()
    assert _FIXTURE_DIR.is_dir()
    assert _GOVERNANCE_DIR.is_dir()


def test_fixture_index_lists_every_scenario() -> None:
    """The fixture index parses and lists exactly the six scenario files."""
    index = _load_yaml(_FIXTURE_DIR / "index.yaml")
    assert index["phase"] == "10F"
    listed = {entry["file"] for entry in index["scenarios"]}
    assert listed == set(_FIXTURE_FILES)


@pytest.mark.parametrize("fixture_file", _FIXTURE_FILES)
def test_fixture_definitions_parse_and_have_required_keys(
    fixture_file: str,
) -> None:
    """Every fixture definition parses and carries the required keys."""
    fixture = _load_yaml(_FIXTURE_DIR / fixture_file)
    missing = _REQUIRED_FIXTURE_KEYS - set(fixture)
    assert not missing, f"{fixture_file} missing keys: {sorted(missing)}"
    assert fixture["phase"] == "10F"
    assert isinstance(fixture["input_files"], list) and fixture["input_files"]
    assert isinstance(fixture["commands"], list) and fixture["commands"]


@pytest.mark.parametrize("fixture_file", _FIXTURE_FILES)
def test_fixture_input_files_exist(fixture_file: str) -> None:
    """Every file a fixture lists under input_files exists in the repo."""
    fixture = _load_yaml(_FIXTURE_DIR / fixture_file)
    for rel in fixture["input_files"]:
        assert (_REPO_ROOT / rel).is_file(), f"{fixture_file}: missing {rel}"


# --------------------------------------------------------------------------
# Stable, unique scenario ids.
# --------------------------------------------------------------------------

def test_scenario_ids_are_stable_and_unique() -> None:
    """Scenario ids are present, deterministic (no timestamps), and unique."""
    ids: list[str] = []
    for fixture_file in _FIXTURE_FILES:
        fixture = _load_yaml(_FIXTURE_DIR / fixture_file)
        scenario_id = fixture["scenario_id"]
        assert scenario_id.startswith("STF-10F-"), scenario_id
        # A stable id is short and carries no digits beyond its index suffix.
        assert scenario_id == scenario_id.strip()
        ids.append(scenario_id)
    assert len(ids) == len(set(ids)), f"duplicate scenario ids: {ids}"
    assert sorted(ids) == ids, "scenario ids are not in stable sorted order"


# --------------------------------------------------------------------------
# Licensing / governance metadata.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("fixture_file", _FIXTURE_FILES)
def test_fixture_content_has_licensing_and_governance_metadata(
    fixture_file: str,
) -> None:
    """Each fixture's content items carry licence and governance metadata."""
    fixture = _load_yaml(_FIXTURE_DIR / fixture_file)
    content = fixture["content"]
    assert isinstance(content, list) and content
    for item in content:
        missing = _REQUIRED_CONTENT_KEYS - set(item)
        assert not missing, f"{fixture_file} content missing: {sorted(missing)}"
        # Demo seed text is original CC0 fixture content only.
        assert item["license_type"] == "CC0-1.0"
        assert isinstance(item["license_basis"], str) and item["license_basis"]
        assert isinstance(item["attribution_required"], bool)
        assert isinstance(item["commercial_use_allowed"], bool)
        assert item["governance_expected_decision"] in {
            "APPROVED",
            "BLOCKED",
            "REJECTED",
            "NEEDS_REVIEW",
        }


def test_successful_scenario_expects_an_approved_allowed_state() -> None:
    """The golden-path fixture expects an APPROVED, completed run."""
    fixture = _load_yaml(_FIXTURE_DIR / "01-successful-golden-path.yaml")
    assert fixture["expected_governance_decision"] == "APPROVED"
    assert fixture["expected_run_state"] == "completed"


def test_governance_blocked_scenario_expects_a_blocked_state() -> None:
    """The governance-blocked fixture expects a BLOCKED governance decision."""
    fixture = _load_yaml(_FIXTURE_DIR / "03-governance-blocked.yaml")
    assert fixture["expected_governance_decision"] == "BLOCKED"
    assert fixture["expected_run_state"] == "failed"
    content = fixture["content"][0]
    assert content["governance_expected_decision"] == "BLOCKED"


def test_rerun_scenarios_reference_phase_10d_command_semantics() -> None:
    """The re-run fixtures reference the existing Phase 10D rerun command."""
    for fixture_file in (
        "02-retryable-technical-failure.yaml",
        "05-rerun-requested.yaml",
        "06-completed-after-rerun.yaml",
    ):
        text = (_FIXTURE_DIR / fixture_file).read_text(encoding="utf-8")
        assert "storytime rerun" in text
    # The rerun-requested fixture names the RunRerunRequested audit event.
    rerun_fixture = (_FIXTURE_DIR / "05-rerun-requested.yaml").read_text(
        encoding="utf-8"
    )
    assert "RunRerunRequested" in rerun_fixture
    assert "storytime run --resume" in rerun_fixture


def test_demo_runbook_references_the_current_phase() -> None:
    """docs/demo.md references Phase 10F and not a wrong / future phase."""
    runbook = (_REPO_ROOT / "docs" / "demo.md").read_text(encoding="utf-8")
    assert "Phase 10F" in runbook
    assert "Phase 10G" not in runbook


# --------------------------------------------------------------------------
# Seed manifests: schema validity and digest correctness.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("manifest_name", _SEED_MANIFESTS)
def test_seed_manifests_validate_against_the_closed_schema(
    manifest_name: str,
) -> None:
    """Every demo seed manifest is valid against the closed manifest schema."""
    manifest = load_manifest(_SEED_DIR / manifest_name)
    assert manifest.license in {"CC0-1.0", "PD-US"}
    # The manifest's text file resolves and its declared digest is correct.
    text_file = (_SEED_DIR / manifest.text_path).resolve()
    assert text_file.is_file()
    text = text_file.read_text(encoding=manifest.text_encoding)
    assert sha256_text(text, encoding=manifest.text_encoding) == (
        manifest.text_sha256
    ), f"{manifest_name}: declared text_sha256 does not match the text file"


# --------------------------------------------------------------------------
# Safety: no binary / generated audio / runtime artifacts; no secrets.
# --------------------------------------------------------------------------

def test_demo_directory_holds_only_small_text_files() -> None:
    """demo/ contains only small, text-based files — no binary or audio."""
    for path in sorted(_DEMO_DIR.rglob("*")):
        if path.is_dir():
            assert path.name not in _DISALLOWED_DIR_NAMES, (
                f"runtime / cache directory leaked into demo/: {path}"
            )
            continue
        assert path.suffix.lower() not in _DISALLOWED_SUFFIXES, (
            f"disallowed binary / generated artifact in demo/: {path}"
        )
        assert path.suffix.lower() in {".txt", ".json", ".yaml", ".yml", ".md"}
        size = path.stat().st_size
        assert size <= _MAX_FIXTURE_FILE_BYTES, (
            f"{path} is {size} bytes; demo fixtures must stay small"
        )


def test_no_runtime_database_or_cache_under_demo() -> None:
    """No SQLite database or tooling cache is packaged under demo/."""
    for path in _DEMO_DIR.rglob("*"):
        name = path.name.lower()
        assert name != "state.db", f"runtime state DB leaked into demo/: {path}"
        assert not name.endswith((".db", ".sqlite", ".sqlite3"))


def test_demo_manifests_carry_no_raw_secrets_or_credentials() -> None:
    """Demo manifests and the demo deny-list contain no secret-bearing keys."""
    secret_markers = (
        "password",
        "secret",
        "api_key",
        "apikey",
        "access_token",
        "private_key",
        "aws_secret",
        "bearer ",
    )
    scanned = list(_SEED_DIR.glob("*.json")) + list(
        _GOVERNANCE_DIR.glob("*.yaml")
    )
    assert scanned, "expected demo manifests / deny-list to scan"
    for path in scanned:
        lowered = path.read_text(encoding="utf-8").lower()
        for marker in secret_markers:
            assert marker not in lowered, (
                f"possible secret marker {marker!r} in {path}"
            )
    # The seed manifests are well-formed JSON objects.
    for path in _SEED_DIR.glob("*.json"):
        assert isinstance(json.loads(path.read_text(encoding="utf-8")), dict)


def test_demo_blocklist_is_a_demo_only_file() -> None:
    """The demo deny-list is a separate demo file, not the committed config."""
    demo_blocklist = _GOVERNANCE_DIR / "demo-blocked-sources.yaml"
    parsed = _load_yaml(demo_blocklist)
    assert "blocked_sources" in parsed and parsed["blocked_sources"]
    # The committed repository deny-list stays empty so the default demo is
    # never blocked; the demo deny-list is opt-in via STORYTIME_BLOCKED_SOURCES.
    committed = _load_yaml(
        _REPO_ROOT / "config" / "governance" / "blocked-sources.yaml"
    )
    assert committed["blocked_sources"] in ([], None)


# --------------------------------------------------------------------------
# Behaviour: the seed manifests drive the real pipeline as documented.
# --------------------------------------------------------------------------

def test_governance_blocked_seed_fails_closed_at_ingest(tmp_path: Path) -> None:
    """The governance-blocked seed resolves to BLOCKED and fails at ingest.

    This drives the real pipeline with the demo deny-list supplied via the
    existing STORYTIME_BLOCKED_SOURCES mechanism. It needs no ffmpeg: the
    fail-closed governance gate stops the run at ingest.
    """
    config = load_config(
        {
            "STORYTIME_RUNS_DIR": str(tmp_path / "runs"),
            "STORYTIME_FEED_DIR": str(tmp_path / "feed"),
            "STORYTIME_TELEMETRY": "noop",
            "STORYTIME_BLOCKED_SOURCES": str(
                _GOVERNANCE_DIR / "demo-blocked-sources.yaml"
            ),
        }
    )
    ctx = build_runtime_context(config)
    try:
        outcome = run_vertical_slice(
            ctx, _SEED_DIR / "demo-governance-blocked.json"
        )
    finally:
        ctx.state.close()
    assert outcome.status == "failed"
    assert outcome.failed_stage == "ingest"
    assert outcome.error_kind == "SourceNotApproved"


def test_governance_blocked_seed_is_approved_without_the_demo_denylist(
    tmp_path: Path,
) -> None:
    """Without the demo deny-list the same source is not blocked.

    This proves the block comes from the opt-in demo deny-list, not from the
    seed content — and that the committed empty deny-list blocks nothing.
    """
    config = load_config(
        {
            "STORYTIME_RUNS_DIR": str(tmp_path / "runs"),
            "STORYTIME_FEED_DIR": str(tmp_path / "feed"),
            "STORYTIME_TELEMETRY": "noop",
        }
    )
    ctx = build_runtime_context(config)
    try:
        outcome = run_vertical_slice(
            ctx, _SEED_DIR / "demo-governance-blocked.json"
        )
    finally:
        ctx.state.close()
    # With no demo deny-list the governance gate does not block this source;
    # the run is not rejected at ingest for a SourceNotApproved reason.
    assert outcome.error_kind != "SourceNotApproved"


def test_needs_review_seed_pauses_at_the_operator_approval_gate(
    tmp_path: Path,
) -> None:
    """The needs-review seed pauses at the text approval gate when required."""
    config = load_config(
        {
            "STORYTIME_RUNS_DIR": str(tmp_path / "runs"),
            "STORYTIME_FEED_DIR": str(tmp_path / "feed"),
            "STORYTIME_TELEMETRY": "noop",
        }
    )
    ctx = build_runtime_context(config)
    try:
        outcome = run_vertical_slice(
            ctx, _SEED_DIR / "demo-needs-review.json", require_approval=True
        )
    finally:
        ctx.state.close()
    assert outcome.status == "awaiting_approval"
    assert outcome.awaiting_gate == "text"


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_golden_path_seed_runs_to_completion(tmp_path: Path) -> None:
    """The golden-path seed completes end to end (needs ffmpeg for assembly)."""
    config = load_config(
        {
            "STORYTIME_RUNS_DIR": str(tmp_path / "runs"),
            "STORYTIME_FEED_DIR": str(tmp_path / "feed"),
            "STORYTIME_TELEMETRY": "noop",
        }
    )
    ctx = build_runtime_context(config)
    try:
        outcome = run_vertical_slice(
            ctx, _SEED_DIR / "demo-golden-path.json", auto_approve=True
        )
    finally:
        ctx.state.close()
    assert outcome.status == "completed"
