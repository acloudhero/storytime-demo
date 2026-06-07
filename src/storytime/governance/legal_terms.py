"""Static legal-hallucination verification gate (Architecture Baseline §24.14).

ARCH-LOCK: No legal-certification vocabulary in code, config, or non-governance docs
DO NOT REFACTOR: This scanner enforces §24.3 / §24.14 — StoryTime must never
*claim* a legal determination, compliance certification, or AI rights
clearance. The FORBIDDEN_LEGAL_TERMS set is the §24.14 minimum forbidden set.
Rationale: §24.14 mandates a static grep/regex gate. The gate's intent is
narrow: it bans *claims* of legal certification, not honest discussion of
"this is not legal advice" disclaimers — so "legal advice" is deliberately not
forbidden.

This module deliberately contains the forbidden strings (as the data to search
for), so the governance documents that *define* the forbidden vocabulary —
this module and the State Preservation Bundle docs that quote §24 — are
allowlisted. The gate must never flag a file for honestly *prohibiting* a term.

Phase 9B.1 hardening: the scanner is pure Python — deterministic, cross-platform,
and independent of grep/sed/awk or any shell. It walks the project tree once,
prunes generated/irrelevant directories (`.venv/`, `.git/`, caches, `runs/`,
`feed/`, build output), and reads only an allowlist of text-based file
extensions. Binary and generated artifacts — SQLite databases, WAV/MP3 audio,
images, archives, compiled `.pyc` caches — are never opened, because their
extensions are not on the allowlist. Allowlisted files are read with
``errors="replace"`` so a stray invalid UTF-8 byte can never raise; a file that
genuinely cannot be opened is skipped as a controlled non-fatal event. The
scanner therefore cannot crash on binary, generated, or malformed input.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

# The §24.14 minimum forbidden set: phrases that would claim a legal
# determination, compliance certification, or AI rights clearance. Matching is
# case-insensitive substring matching. Note "legal advice" is intentionally NOT
# here — disclaiming legal advice is honest and encouraged.
FORBIDDEN_LEGAL_TERMS: tuple[str, ...] = (
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
)

# Repository-relative documents that legitimately *define* or *quote* the
# forbidden vocabulary in order to ban it (§24.14). The gate must not flag
# these for honestly prohibiting a term.
GOVERNANCE_DOC_ALLOWLIST: frozenset[str] = frozenset(
    {
        # §24 defines the forbidden vocabulary as canonical governance law.
        "docs/architecture-baseline.md",
        # State Preservation Bundle docs that record / quote the §24 amendment.
        "docs/canonical-state.md",
        "docs/phase-history.md",
        "docs/verification-log.md",
        "docs/roundtable-import-bridge.md",
        "docs/handoff-state.md",
        "docs/roadmap.md",
        "docs/open-issues.md",
        "docs/artifact-manifest.md",
        # The Phase 9B implementation prompt lists the forbidden set verbatim.
        "docs/phase9b-minimal-trust-envelope-implementation-prompt.md",
        # This scanner module holds the forbidden set as the data to search.
        "src/storytime/governance/legal_terms.py",
        # The gate's own test references the forbidden vocabulary.
        "tests/test_legal_hallucination_gate.py",
    }
)

# The extension allowlist (§24.14 hardening, preferred approach): only
# text-based project files are read. Any extension not in this set — including
# every binary/generated kind (.db/.sqlite/.sqlite3, .wav/.mp3/.ogg,
# .png/.jpg/.jpeg/.gif/.webp, .zip/.tar/.gz/.tgz, .pyc) — is never opened, so
# the scanner cannot crash on binary content.
_TEXT_SUFFIXES: frozenset[str] = frozenset(
    {".py", ".md", ".yaml", ".yml", ".json", ".toml", ".txt"}
)

# Directory names pruned during the walk: virtualenvs, version control,
# tool caches, generated run/feed artifacts, and build output. Pruning these
# keeps the scan deterministic, fast, and clear of generated binary files.
_IGNORED_DIRECTORY_NAMES: frozenset[str] = frozenset(
    {
        ".venv",
        ".git",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".import_linter_cache",
        "runs",
        "feed",
        "dist",
        "build",
        "node_modules",
    }
)


@dataclass(frozen=True, slots=True)
class LegalTermViolation:
    """One occurrence of a forbidden legal-certification term."""

    path: str
    line_number: int
    term: str
    line: str


def _iter_scannable_files(repo_root: Path) -> list[Path]:
    """Return every scannable text file under *repo_root*, deterministically.

    Walks the whole tree once, pruning the ignored directories
    (``_IGNORED_DIRECTORY_NAMES``) so generated/binary artifacts are never
    descended into, and yields only files whose extension is on the text
    allowlist (``_TEXT_SUFFIXES``). Directory and file names are sorted so the
    traversal order is stable across platforms and runs.
    """
    found: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(repo_root):
        # Prune ignored directories in place; sort the rest for determinism.
        dirnames[:] = sorted(
            d for d in dirnames if d not in _IGNORED_DIRECTORY_NAMES
        )
        base = Path(dirpath)
        for name in sorted(filenames):
            path = base / name
            if path.suffix.lower() in _TEXT_SUFFIXES:
                found.append(path)
    return found


def scan_for_forbidden_terms(repo_root: Path) -> list[LegalTermViolation]:
    """Scan the repository for forbidden legal-certification vocabulary.

    Walks the whole *repo_root* tree, pruning generated/irrelevant directories
    and reading only allowlisted text files (so binary and generated artifacts
    are never opened). The governance documents in GOVERNANCE_DOC_ALLOWLIST —
    which legitimately define or quote the vocabulary in order to ban it — are
    skipped. Files are read with ``errors="replace"`` so an invalid UTF-8 byte
    cannot raise; a file that genuinely cannot be opened is skipped as a
    controlled, non-fatal event. Returns every violation found; an empty list
    means the gate passes.
    """
    violations: list[LegalTermViolation] = []
    needles = [(term, term.lower()) for term in FORBIDDEN_LEGAL_TERMS]

    for path in _iter_scannable_files(repo_root):
        try:
            rel = path.relative_to(repo_root).as_posix()
        except ValueError:
            rel = path.as_posix()
        if rel in GOVERNANCE_DOC_ALLOWLIST:
            continue
        try:
            # errors="replace": invalid UTF-8 bytes become U+FFFD rather than
            # raising, so the scanner never crashes on a malformed text file
            # and the file's valid text is still inspected.
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            # The file vanished mid-walk, or is unreadable (permissions, a
            # special file). A controlled skip — never a crash.
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            lowered = line.lower()
            for term, needle in needles:
                if needle in lowered:
                    violations.append(
                        LegalTermViolation(
                            path=rel,
                            line_number=line_number,
                            term=term,
                            line=line.strip(),
                        )
                    )
    return violations
