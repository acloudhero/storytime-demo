"""Content hashing.

SHA-256 is the integrity primitive across StoryTime: source texts, artifact
payloads, and audio files are all hashed and the digest is recorded.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

_CHUNK = 65536


def sha256_bytes(data: bytes) -> str:
    """Return the hex SHA-256 digest of *data*."""
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str, *, encoding: str = "utf-8") -> str:
    """Return the hex SHA-256 digest of *text* encoded with *encoding*."""
    return sha256_bytes(text.encode(encoding))


def sha256_file(path: Path) -> str:
    """Return the hex SHA-256 digest of the file at *path*, read in chunks."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(_CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()
