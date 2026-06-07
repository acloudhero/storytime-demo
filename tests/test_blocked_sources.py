"""Blocked-source configuration: loading and matching (Architecture Baseline §24.9).

The blocked-source list is a local, explicit, human-curated YAML file. A
missing file blocks nothing; a malformed file fails loudly; matching is
deterministic, case-insensitive substring matching.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from storytime.governance import (
    BlockedSource,
    BlockedSourceConfigError,
    load_blocked_sources,
    match_blocked_source,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]


def _write(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "blocked-sources.yaml"
    path.write_text(body, encoding="utf-8")
    return path


def test_missing_file_is_an_empty_blocklist(tmp_path: Path) -> None:
    # A deny-list that does not exist denies nothing — this is the safe
    # default and never makes the fail-closed gate fail open.
    assert load_blocked_sources(tmp_path / "does-not-exist.yaml") == ()


def test_empty_list_loads_as_empty(tmp_path: Path) -> None:
    assert load_blocked_sources(_write(tmp_path, "blocked_sources: []\n")) == ()


def test_entries_are_parsed(tmp_path: Path) -> None:
    body = (
        "blocked_sources:\n"
        '  - pattern: "blocked.example.invalid"\n'
        '    reason: "operator-blocked example domain"\n'
        '    added: "2026-05-24"\n'
        '    note: "illustrative"\n'
    )
    entries = load_blocked_sources(_write(tmp_path, body))
    assert len(entries) == 1
    assert entries[0] == BlockedSource(
        pattern="blocked.example.invalid",
        reason="operator-blocked example domain",
        added="2026-05-24",
        note="illustrative",
    )


def test_malformed_yaml_raises(tmp_path: Path) -> None:
    with pytest.raises(BlockedSourceConfigError):
        load_blocked_sources(_write(tmp_path, "blocked_sources: [unclosed\n"))


def test_missing_blocked_sources_key_raises(tmp_path: Path) -> None:
    with pytest.raises(BlockedSourceConfigError):
        load_blocked_sources(_write(tmp_path, "something_else: []\n"))


def test_entry_without_pattern_raises(tmp_path: Path) -> None:
    body = 'blocked_sources:\n  - reason: "no pattern here"\n'
    with pytest.raises(BlockedSourceConfigError):
        load_blocked_sources(_write(tmp_path, body))


def test_entry_without_reason_raises(tmp_path: Path) -> None:
    body = 'blocked_sources:\n  - pattern: "x.invalid"\n'
    with pytest.raises(BlockedSourceConfigError):
        load_blocked_sources(_write(tmp_path, body))


def test_entry_with_unknown_key_raises(tmp_path: Path) -> None:
    body = (
        "blocked_sources:\n"
        '  - pattern: "x.invalid"\n'
        '    reason: "r"\n'
        '    severity: "high"\n'
    )
    with pytest.raises(BlockedSourceConfigError):
        load_blocked_sources(_write(tmp_path, body))


def test_match_is_case_insensitive_substring() -> None:
    blocked = (BlockedSource(pattern="Bad.Example.Invalid", reason="r"),)
    hit = match_blocked_source(blocked, "https://bad.example.invalid/page.txt")
    assert hit is not None and hit.reason == "r"


def test_match_returns_none_when_nothing_matches() -> None:
    blocked = (BlockedSource(pattern="blocked.invalid", reason="r"),)
    assert match_blocked_source(blocked, "https://example.org/ok.txt") is None


def test_match_ignores_none_candidates() -> None:
    blocked = (BlockedSource(pattern="x.invalid", reason="r"),)
    assert match_blocked_source(blocked, None, None) is None


def test_match_checks_every_candidate() -> None:
    blocked = (BlockedSource(pattern="raven-source", reason="r"),)
    # The pattern matches the source id, not the URL.
    hit = match_blocked_source(blocked, "https://example.org/ok.txt", "raven-source")
    assert hit is not None


def test_committed_config_loads_and_is_empty() -> None:
    # The repo ships config/governance/blocked-sources.yaml as an empty list so
    # the local CC0 / public-domain demo is never blocked.
    committed = _REPO_ROOT / "config" / "governance" / "blocked-sources.yaml"
    assert committed.is_file()
    assert load_blocked_sources(committed) == ()
