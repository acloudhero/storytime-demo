"""Local filesystem storage adapter."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path


class StorageKeyError(ValueError):
    """Raised when a storage key would escape the storage root."""


class LocalFilesystemStorage:
    """A StorageAdapter backed by a local directory tree rooted at *root*."""

    def __init__(self, root: Path) -> None:
        self._root = root.resolve()

    @property
    def root(self) -> Path:
        return self._root

    def resolve(self, key: str) -> Path:
        """Resolve *key* to an absolute path, rejecting traversal outside root."""
        candidate = (self._root / key).resolve()
        if candidate != self._root and self._root not in candidate.parents:
            raise StorageKeyError(f"storage key escapes root: {key!r}")
        return candidate

    def exists(self, key: str) -> bool:
        return self.resolve(key).exists()

    def write_bytes(self, key: str, data: bytes) -> None:
        path = self.resolve(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def read_bytes(self, key: str) -> bytes:
        return self.resolve(key).read_bytes()

    def write_text(self, key: str, text: str) -> None:
        path = self.resolve(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def write_text_atomic(self, key: str, text: str) -> None:
        """Write *text* to *key* via a temp file + os.replace (same directory).

        os.replace is atomic on a single filesystem; keeping the temp file in
        the destination directory guarantees that. A reader of *key* sees
        either the previous file or the complete new one, never a partial one.
        """
        path = self.resolve(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(
            dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
        )
        tmp_path = Path(tmp_name)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(text)
            os.replace(tmp_path, path)
        except BaseException:
            tmp_path.unlink(missing_ok=True)
            raise

    def read_text(self, key: str) -> str:
        return self.resolve(key).read_text(encoding="utf-8")
