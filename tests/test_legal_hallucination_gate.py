"""The static legal-hallucination verification gate (Architecture Baseline §24.14).

StoryTime must never *claim* a legal determination, compliance certification,
or AI rights clearance. This gate scans the repository's code, config, and
non-governance docs for the §24.14 forbidden vocabulary; the governance
documents that legitimately *define* or *quote* that vocabulary are allowlisted.
"""

from __future__ import annotations

from pathlib import Path

from storytime.governance import (
    FORBIDDEN_LEGAL_TERMS,
    GOVERNANCE_DOC_ALLOWLIST,
    scan_for_forbidden_terms,
)
from storytime.governance.legal_terms import LegalTermViolation

_REPO_ROOT = Path(__file__).resolve().parents[1]


def test_repository_has_no_forbidden_legal_certification_vocabulary() -> None:
    """The whole repository (minus allowlisted governance docs) is clean."""
    violations = scan_for_forbidden_terms(_REPO_ROOT)
    assert violations == [], (
        "forbidden legal-certification vocabulary found:\n"
        + "\n".join(
            f"  {v.path}:{v.line_number}: {v.term!r} -> {v.line}"
            for v in violations
        )
    )


def test_forbidden_set_covers_the_section_24_14_minimum() -> None:
    """The forbidden set includes every §24.14 minimum term."""
    minimum = {
        "legal_verified_by_llm",
        "copyright_cleared_by_ai",
        "compliance_score",
        "rights_confidence_score",
        "copyright_safe_score",
        "GDPR compliant",
        "CCPA compliant",
        "legal clearance",
        "legally certified",
        "AI-verified copyright",
    }
    assert minimum <= set(FORBIDDEN_LEGAL_TERMS)


def test_gate_detects_an_introduced_violation(tmp_path: Path) -> None:
    """A planted forbidden term is detected — the gate is not a no-op."""
    (tmp_path / "src").mkdir()
    planted = tmp_path / "src" / "planted.py"
    planted.write_text(
        '# this file falsely claims a compliance_score\n', encoding="utf-8"
    )
    violations = scan_for_forbidden_terms(tmp_path)
    assert any(v.term == "compliance_score" for v in violations)
    assert all(isinstance(v, LegalTermViolation) for v in violations)


def test_gate_allowlists_governance_documents(tmp_path: Path) -> None:
    """A governance doc that defines the vocabulary is not flagged."""
    docs = tmp_path / "docs"
    docs.mkdir()
    # architecture-baseline.md is allowlisted: §24 must define the terms.
    (docs / "architecture-baseline.md").write_text(
        "Section 24 forbids any claim of legal clearance.\n", encoding="utf-8"
    )
    assert "docs/architecture-baseline.md" in GOVERNANCE_DOC_ALLOWLIST
    assert scan_for_forbidden_terms(tmp_path) == []


# -- Phase 9B.1 scanner hardening -------------------------------------------

def test_scanner_ignores_binary_file_extensions(tmp_path: Path) -> None:
    """Binary-extension files are never opened — even if they contain the text.

    A `.db` / `.wav` / `.pyc` file whose bytes happen to spell a forbidden
    term must not be flagged: it is not on the text allowlist, so the scanner
    never reads it.
    """
    (tmp_path / "src").mkdir()
    for name in ("state.db", "audio.wav", "module.pyc", "art.png"):
        (tmp_path / "src" / name).write_bytes(b"compliance_score legally certified")
    assert scan_for_forbidden_terms(tmp_path) == []


def test_scanner_does_not_crash_on_binary_bytes(tmp_path: Path) -> None:
    """A real binary blob with a non-text extension does not crash the scan."""
    (tmp_path / "src").mkdir()
    # Bytes that are not valid UTF-8 and not text at all.
    (tmp_path / "src" / "blob.db").write_bytes(bytes(range(256)) * 8)
    # Must complete and return a list, never raise.
    assert scan_for_forbidden_terms(tmp_path) == []


def test_scanner_does_not_crash_on_invalid_utf8_in_text_file(
    tmp_path: Path,
) -> None:
    """An allowlisted text file with invalid UTF-8 bytes is read safely.

    errors="replace" means the stray bytes become U+FFFD instead of raising;
    the file's valid text is still scanned, so a planted forbidden term in the
    same file is still caught.
    """
    (tmp_path / "src").mkdir()
    planted = tmp_path / "src" / "messy.py"
    # A valid line with a forbidden term, then a line of invalid UTF-8 bytes.
    planted.write_bytes(
        b"# declares a compliance_score here\n"
        b"# next bytes are invalid utf-8: \xff\xfe\x80\x81\n"
    )
    violations = scan_for_forbidden_terms(tmp_path)
    # No crash, and the forbidden term in the valid text is still detected.
    assert any(v.term == "compliance_score" for v in violations)


def test_scanner_ignores_generated_run_and_feed_directories(
    tmp_path: Path,
) -> None:
    """Forbidden text under runs/ and feed/ is ignored — generated artifacts."""
    for generated in ("runs", "feed"):
        d = tmp_path / generated
        d.mkdir()
        (d / "note.txt").write_text(
            "this run output mentions a compliance_score\n", encoding="utf-8"
        )
    assert scan_for_forbidden_terms(tmp_path) == []


def test_scanner_ignores_virtualenv_and_cache_directories(
    tmp_path: Path,
) -> None:
    """Forbidden text under .venv/, .git/, and cache dirs is ignored."""
    for ignored in (".venv", ".git", "__pycache__", ".mypy_cache"):
        d = tmp_path / ignored
        d.mkdir()
        (d / "vendored.py").write_text(
            "# vendored code claiming legally certified status\n",
            encoding="utf-8",
        )
    assert scan_for_forbidden_terms(tmp_path) == []


def test_scanner_prunes_ignored_directories_nested_under_a_source_tree(
    tmp_path: Path,
) -> None:
    """An ignored directory nested inside a real source tree is still pruned."""
    pkg = tmp_path / "src" / "storytime"
    nested_cache = pkg / "__pycache__"
    nested_cache.mkdir(parents=True)
    # A real source file IS scanned ...
    (pkg / "real.py").write_text("# a clean module\n", encoding="utf-8")
    # ... but a forbidden term inside the nested __pycache__ is not.
    (nested_cache / "cached.py").write_text(
        "# stale cache claiming a compliance_score\n", encoding="utf-8"
    )
    assert scan_for_forbidden_terms(tmp_path) == []


def test_scanner_still_detects_violation_in_non_allowlisted_doc(
    tmp_path: Path,
) -> None:
    """A non-governance doc with a forbidden claim is still flagged.

    The hardening must not weaken detection: a `.md` file that is NOT in the
    governance allowlist (e.g. a runbook) is still scanned and flagged.
    """
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "runbook.md").write_text(
        "Our pipeline is GDPR compliant and AI-verified copyright safe.\n",
        encoding="utf-8",
    )
    violations = scan_for_forbidden_terms(tmp_path)
    found = {v.term for v in violations}
    assert "GDPR compliant" in found
