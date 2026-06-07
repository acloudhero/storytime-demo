"""The active-slot pointer — the single source of truth for the front door.

The front door routes all traffic to exactly one slot at a time: the *active*
slot. Phase 7B makes that an explicit, persisted fact in a tiny pointer file
(default ``config/deploy/active-slot``) holding one slot name, e.g. ``blue``.

ARCH-LOCK: Active-slot value safety
DO NOT REFACTOR: only a value accepted by ``storytime.config.is_valid_slot_name``
may ever be read as, or written as, the active slot — the same
``[a-z0-9][a-z0-9._-]*`` rule ``load_config`` enforces. A traversal-like,
whitespace-bearing, or shell-unsafe value can therefore never become the
active slot. Do not loosen this to "any string".
Rationale: Phase 7B — the active slot is consumed by the front door and named
in operator commands; it must be a safe token.

Design choices that keep this honest:

* The pointer is plain text, one token, trivial to inspect with ``cat``.
* It survives a process / front-door restart — it is just a file.
* ``read_active_slot`` never raises an unexpected exception on a missing,
  empty, or garbage file: it raises the typed ``ActiveSlotError`` the front
  door turns into an honest 503, rather than crashing.
* ``write_active_slot`` is atomic (temp file + ``os.replace`` in the same
  directory) so a crash mid-write can never leave a torn pointer.
"""

from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from pathlib import Path

from storytime.config import is_valid_slot_name

# The conventional pointer filename, alongside the per-slot env files.
DEFAULT_ACTIVE_SLOT_FILENAME = "active-slot"


class ActiveSlotError(ValueError):
    """Raised when an active-slot value is missing, empty, or unsafe."""


@dataclass(frozen=True, slots=True)
class ActiveSlotState:
    """The resolved, validated active-slot pointer."""

    slot: str
    path: Path


def read_active_slot(path: Path) -> ActiveSlotState:
    """Read and validate the active-slot pointer at *path*.

    Raises ``ActiveSlotError`` if the file is absent, empty, or holds a value
    that is not a safe slot name. The front door catches that and answers a
    503 rather than failing hard — a missing pointer is an operator-fixable
    condition, not a crash.
    """
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ActiveSlotError(f"active-slot pointer not found: {path}") from exc
    except OSError as exc:
        raise ActiveSlotError(
            f"active-slot pointer could not be read: {path}: {exc}"
        ) from exc

    slot = raw.strip()
    if not slot:
        raise ActiveSlotError(f"active-slot pointer is empty: {path}")
    if not is_valid_slot_name(slot):
        raise ActiveSlotError(
            f"active-slot pointer holds an unsafe slot value {slot!r} "
            f"(must match [a-z0-9][a-z0-9._-]* — no slashes, traversal, or "
            f"whitespace): {path}"
        )
    return ActiveSlotState(slot=slot, path=path)


def write_active_slot(path: Path, slot: str) -> ActiveSlotState:
    """Validate *slot* and write it to the pointer at *path* atomically.

    Refuses to write an unsafe slot value (``ActiveSlotError``). The write is
    atomic: a temp file in the same directory plus ``os.replace``, so a reader
    always sees either the old pointer or the complete new one.
    """
    if not is_valid_slot_name(slot):
        raise ActiveSlotError(
            f"refusing to write unsafe slot value {slot!r} as the active slot "
            f"(must match [a-z0-9][a-z0-9._-]*)"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(slot + "\n")
        os.replace(tmp_path, path)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise
    return ActiveSlotState(slot=slot, path=path)
