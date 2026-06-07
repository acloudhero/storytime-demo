"""Backend-owned artifact storage seam (Phase 14C.3).

Phase 14C.3 puts artifact handling behind a backend-owned **port**
(:class:`ArtifactStore`) with a single local **adapter**
(:class:`LocalFilesystemArtifactStore`). The point of the seam is twofold:

1. keep artifact ownership in the backend, behind a neutral contract whose terms
   are storage-agnostic (``artifact_key``, ``content``, ``content_hash``,
   ``media_type``, ``size_bytes``, ``metadata``, ``created_at``) — no cloud,
   bucket, region, ACL, signed-URL, or credential concepts; and
2. guarantee the browser never learns filesystem paths or storage credentials —
   the adapter validates logical keys, keeps every artifact under a configured
   root, and returns only safe :class:`ArtifactEvidence`.

This is LOCAL filesystem storage only — not a cloud object store, not an
external object store, and not public artifact serving. A future hosted adapter
could implement the same port, but none exists yet.
"""

from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path, PurePosixPath
from typing import Protocol

# Logical artifact keys use POSIX-style forward-slash separators and must be
# relative, with no traversal. Media types are inferred from a small, explicit,
# deterministic suffix map (no dependency on platform mimetypes databases).
_MEDIA_TYPES = {
    ".json": "application/json",
    ".txt": "text/plain",
    ".md": "text/markdown",
    ".wav": "audio/wav",
    ".mp3": "audio/mpeg",
}
_DEFAULT_MEDIA_TYPE = "application/octet-stream"


class ArtifactStoreError(Exception):
    """Base error for artifact-store operations."""


class UnsafeArtifactKeyError(ArtifactStoreError):
    """Raised when a logical artifact key is absolute, traversing, or escapes."""


class ArtifactNotFoundError(ArtifactStoreError):
    """Raised when reading a logical artifact key that does not exist."""


@dataclass(frozen=True, slots=True)
class ArtifactEvidence:
    """Safe, browser-shareable evidence about a stored artifact.

    Contains only neutral, non-sensitive facts. It never carries an absolute
    filesystem path, a storage root, a credential, a bucket, or a URL.
    """

    artifact_id: str
    artifact_key: str
    content_hash: str
    size_bytes: int
    media_type: str
    created_at: str
    metadata: dict[str, str] = field(default_factory=dict)


def media_type_for(artifact_key: str) -> str:
    """Infer a media type from a logical key suffix (deterministic, local)."""
    suffix = PurePosixPath(artifact_key).suffix.lower()
    return _MEDIA_TYPES.get(suffix, _DEFAULT_MEDIA_TYPE)


def normalize_artifact_key(artifact_key: str) -> str:
    """Validate and normalize a logical artifact key.

    A safe key is a non-empty, relative, POSIX-style path with no drive letter,
    no leading separator, no backslashes, and no ``.``/``..`` segments. Returns
    the normalized key, or raises :class:`UnsafeArtifactKeyError`.
    """
    if not isinstance(artifact_key, str) or not artifact_key.strip():
        raise UnsafeArtifactKeyError("artifact key must be a non-empty string")
    if "\\" in artifact_key:
        raise UnsafeArtifactKeyError("artifact key must not contain backslashes")
    if artifact_key.startswith("/"):
        raise UnsafeArtifactKeyError("artifact key must be relative")
    # Reject Windows drive-letter / absolute forms (e.g. "C:\\", "C:/").
    if len(artifact_key) >= 2 and artifact_key[1] == ":":
        raise UnsafeArtifactKeyError("artifact key must not be an absolute path")
    if os.path.isabs(artifact_key):
        raise UnsafeArtifactKeyError("artifact key must be relative")
    segments = [s for s in artifact_key.split("/") if s != ""]
    if not segments:
        raise UnsafeArtifactKeyError("artifact key has no usable segments")
    for seg in segments:
        if seg == "." or seg == "..":
            raise UnsafeArtifactKeyError("artifact key must not contain . or ..")
    return "/".join(segments)


class ArtifactStore(Protocol):
    """Backend-owned artifact storage port.

    A replaceable contract over artifact content. The terms are deliberately
    storage-neutral; there are no cloud, bucket, region, credential, or URL
    concepts. ``LocalFilesystemArtifactStore`` is the only adapter today.
    """

    def write(
        self,
        *,
        artifact_key: str,
        content: bytes,
        media_type: str | None = None,
        metadata: dict[str, str] | None = None,
        created_at: str,
    ) -> ArtifactEvidence:
        """Durably store ``content`` under ``artifact_key``; return safe evidence."""
        ...

    def read(self, artifact_key: str) -> bytes:
        """Return the stored content, or raise :class:`ArtifactNotFoundError`."""
        ...

    def exists(self, artifact_key: str) -> bool:
        """Return whether an artifact exists for ``artifact_key``."""
        ...

    def evidence(self, artifact_key: str) -> ArtifactEvidence | None:
        """Return safe evidence for a stored artifact, or None if absent."""
        ...

    def validate_key(self, artifact_key: str) -> str:
        """Validate/normalize a logical key; raise on an unsafe key."""
        ...


class LocalFilesystemArtifactStore:
    """The only artifact-store adapter: local filesystem under a fixed root.

    Owns an artifact root and keeps every artifact under it. Logical keys are
    validated and normalized; absolute paths, ``..`` traversal, backslash
    separators, and symlink escapes are rejected. Writes are atomic
    (temp file + ``os.replace``). Only safe evidence is returned — never an
    absolute path or any storage internal.

    This is local filesystem storage only — not a cloud object store, not an
    external object store, and not public artifact serving.
    """

    def __init__(self, *, root: Path) -> None:
        self._root = Path(root)

    # -- key / path safety -------------------------------------------------

    def validate_key(self, artifact_key: str) -> str:
        return normalize_artifact_key(artifact_key)

    def _resolved_under_root(self, artifact_key: str) -> Path:
        """Resolve a validated key to an absolute path guaranteed under root.

        Uses ``Path.resolve`` (which follows symlinks) and an explicit
        containment check, so a symlink that points outside the root is
        rejected rather than followed.
        """
        key = self.validate_key(artifact_key)
        root_resolved = self._root.resolve()
        target = (self._root / key).resolve()
        if target != root_resolved and root_resolved not in target.parents:
            raise UnsafeArtifactKeyError(
                "artifact key resolves outside the artifact root"
            )
        return target

    # -- operations --------------------------------------------------------

    def write(
        self,
        *,
        artifact_key: str,
        content: bytes,
        media_type: str | None = None,
        metadata: dict[str, str] | None = None,
        created_at: str,
    ) -> ArtifactEvidence:
        if not isinstance(content, bytes | bytearray):
            raise ArtifactStoreError("artifact content must be bytes")
        key = self.validate_key(artifact_key)
        target = self._resolved_under_root(key)
        target.parent.mkdir(parents=True, exist_ok=True)
        # Atomic write: temp file in the destination directory, then replace.
        fd, tmp_name = tempfile.mkstemp(dir=str(target.parent), suffix=".tmp")
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(content)
            os.replace(tmp_name, target)
        except BaseException:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)
            raise
        return ArtifactEvidence(
            artifact_id=key,
            artifact_key=key,
            content_hash=sha256(bytes(content)).hexdigest(),
            size_bytes=len(content),
            media_type=media_type or media_type_for(key),
            created_at=created_at,
            metadata=dict(metadata or {}),
        )

    def read(self, artifact_key: str) -> bytes:
        target = self._resolved_under_root(artifact_key)
        if not target.is_file():
            raise ArtifactNotFoundError(f"no artifact for key {artifact_key!r}")
        return target.read_bytes()

    def exists(self, artifact_key: str) -> bool:
        try:
            target = self._resolved_under_root(artifact_key)
        except UnsafeArtifactKeyError:
            return False
        return target.is_file()

    def evidence(self, artifact_key: str) -> ArtifactEvidence | None:
        try:
            target = self._resolved_under_root(artifact_key)
        except UnsafeArtifactKeyError:
            return None
        if not target.is_file():
            return None
        data = target.read_bytes()
        key = self.validate_key(artifact_key)
        stat = target.stat()
        from datetime import UTC, datetime

        created = datetime.fromtimestamp(stat.st_mtime, tz=UTC).isoformat()
        return ArtifactEvidence(
            artifact_id=key,
            artifact_key=key,
            content_hash=sha256(data).hexdigest(),
            size_bytes=len(data),
            media_type=media_type_for(key),
            created_at=created,
        )
