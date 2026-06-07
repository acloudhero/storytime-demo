"""Storage adapter interface.

ARCH-LOCK: Storage Seam
DO NOT REFACTOR: Pipeline code that needs to read/write run artifacts should
go through a StorageAdapter, not hard-coded open() calls scattered across
stages. The local implementation is filesystem-backed today; the cloud phase
swaps in an object-store implementation behind this same interface.
Rationale: Architecture Baseline section 19 — this seam is what keeps the
future cloud migration mechanical.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable


@runtime_checkable
class StorageAdapter(Protocol):
    """Key-addressed storage for run artifacts. Keys are relative paths."""

    def resolve(self, key: str) -> Path: ...

    def exists(self, key: str) -> bool: ...

    def write_bytes(self, key: str, data: bytes) -> None: ...

    def read_bytes(self, key: str) -> bytes: ...

    def write_text(self, key: str, text: str) -> None: ...

    def write_text_atomic(self, key: str, text: str) -> None:
        """Write *text* to *key* atomically: a reader sees the old or new file.

        ARCH-LOCK: Atomic feed publish (Architecture Baseline section 14)
        DO NOT REFACTOR: feed.xml MUST be replaced atomically — written to a
        temp key, then swapped into place — so a crash mid-write can never
        leave a partial or malformed feed where a good one was. Do not collapse
        this back into a plain write_text in the publish stage.
        Rationale: section 14 requires "write to a temp file, validate, then
        atomically replace"; the cloud StorageAdapter implements the same
        guarantee with its backend's atomic primitive.
        """
        ...

    def read_text(self, key: str) -> str: ...
