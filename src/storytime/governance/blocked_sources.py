"""Local blocked-source configuration (Architecture Baseline §24.9).

ARCH-LOCK: Blocked sources are a local, explicit, inspectable file
DO NOT REFACTOR: The blocked-source list is a static, committed, human-curated
local YAML file. It MUST NOT become a cloud service, fetch a remote blocklist,
or scrape or classify websites (§24.9). Matching is deterministic substring
matching against operator-supplied patterns — never model inference and never
viewpoint/topic classification (§24.5: governance is source authorization, not
viewpoint acceptability).
Rationale: §24.9 defines the blocked-source policy; Phase 9B implements it as
the simplest honest thing — a reviewable file the operator owns.

A source matched here resolves to a BLOCKED governance decision (§24.5/§24.9).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


class BlockedSourceConfigError(ValueError):
    """Raised when the blocked-source config file is present but malformed.

    A *missing* file is not an error — an absent blocklist simply blocks
    nothing (a blocklist is a deny-list; absence denies nothing). A *malformed*
    file is an error: a broken blocklist must fail loudly, never be silently
    ignored.
    """


@dataclass(frozen=True, slots=True)
class BlockedSource:
    """One operator-curated blocked-source entry (§24.9).

    ``pattern`` is matched, case-insensitively, as a substring of a candidate
    source's URL or reference id. ``reason`` is the operator's justification;
    ``added`` and ``note`` are optional bookkeeping.
    """

    pattern: str
    reason: str
    added: str | None = None
    note: str | None = None


def _coerce_entry(raw: object, index: int) -> BlockedSource:
    """Build a BlockedSource from one raw YAML list item, validating it."""
    if not isinstance(raw, dict):
        raise BlockedSourceConfigError(
            f"blocked_sources[{index}] must be a mapping, got {type(raw).__name__}"
        )
    pattern = raw.get("pattern")
    reason = raw.get("reason")
    if not isinstance(pattern, str) or not pattern.strip():
        raise BlockedSourceConfigError(
            f"blocked_sources[{index}] requires a non-empty string 'pattern'"
        )
    if not isinstance(reason, str) or not reason.strip():
        raise BlockedSourceConfigError(
            f"blocked_sources[{index}] requires a non-empty string 'reason'"
        )
    added = raw.get("added")
    note = raw.get("note")
    allowed = {"pattern", "reason", "added", "note"}
    unknown = set(raw) - allowed
    if unknown:
        raise BlockedSourceConfigError(
            f"blocked_sources[{index}] has unknown key(s): {sorted(unknown)}"
        )
    return BlockedSource(
        pattern=pattern.strip(),
        reason=reason.strip(),
        added=str(added) if added is not None else None,
        note=str(note) if note is not None else None,
    )


def load_blocked_sources(path: Path) -> tuple[BlockedSource, ...]:
    """Load the blocked-source entries from the YAML file at *path*.

    A missing file yields an empty tuple — an absent deny-list blocks nothing,
    which is the safe default (it never makes the fail-closed gate fail open;
    the gate's APPROVED requirement is independent of this list). A present but
    malformed file raises BlockedSourceConfigError.
    """
    if not path.is_file():
        return ()
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise BlockedSourceConfigError(
            f"blocked-source config {path} is not valid YAML: {exc}"
        ) from exc
    if raw is None:
        return ()
    if not isinstance(raw, dict) or "blocked_sources" not in raw:
        raise BlockedSourceConfigError(
            f"blocked-source config {path} must be a mapping with a "
            "'blocked_sources' list"
        )
    entries = raw["blocked_sources"]
    if entries is None:
        return ()
    if not isinstance(entries, list):
        raise BlockedSourceConfigError(
            f"blocked-source config {path}: 'blocked_sources' must be a list"
        )
    return tuple(_coerce_entry(item, i) for i, item in enumerate(entries))


def match_blocked_source(
    blocked: tuple[BlockedSource, ...], *candidates: str | None
) -> BlockedSource | None:
    """Return the first BlockedSource whose pattern matches any *candidate*.

    Matching is deterministic, case-insensitive substring matching: a candidate
    (a source URL or reference id) matches an entry when the entry's pattern
    appears within it. ``None`` candidates are ignored. Returns ``None`` when
    nothing matches.
    """
    haystacks = [c.lower() for c in candidates if c]
    for entry in blocked:
        needle = entry.pattern.lower()
        if any(needle in hay for hay in haystacks):
            return entry
    return None
