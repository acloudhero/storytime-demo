"""Phase 14C.3 — tests for the backend-owned artifact storage seam.

Cover the ArtifactStore port + the single LocalFilesystemArtifactStore adapter:
write/read, metadata, key-safety (traversal/absolute/backslash/symlink-escape),
deterministic missing behavior, proof-run routing through the store, scenario
integrity, and read-model/DTO path-leak safety.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from storytime.local_live import artifact_store as artifact_store_module
from storytime.local_live.artifact_store import (
    ArtifactEvidence,
    ArtifactNotFoundError,
    ArtifactStore,
    LocalFilesystemArtifactStore,
    UnsafeArtifactKeyError,
)
from storytime.local_live.server import LocalLiveService

_REPO_ROOT = Path(__file__).resolve().parents[1]
_FIXTURES_DIR = _REPO_ROOT / "demo" / "seed"

# Substrings that must never appear in browser-visible artifact evidence.
_LEAK_SUBSTRINGS = (
    "/tmp/",
    "/home/",
    "C:\\",
    ".db",
    "signed_url",
    "credential",
    "secret",
    "token",
    "bucket",
)
# Cloud/SDK names that must not appear in the storage module (no dependency drift
# toward provider SDKs).
_FORBIDDEN_MODULE_TERMS = (
    "boto3",
    "google.cloud",
    "azure.storage",
    "minio",
    "s3object",
    "blobclient",
    "signed url",
    "presigned",
)


@pytest.fixture()
def store(tmp_path: Path) -> LocalFilesystemArtifactStore:
    root = tmp_path / "artifacts"
    root.mkdir()
    return LocalFilesystemArtifactStore(root=root)


@pytest.fixture()
def service(tmp_path: Path) -> LocalLiveService:
    runs = tmp_path / "runs"
    runs.mkdir()
    return LocalLiveService(
        db_path=runs / "state.db", runs_dir=runs, fixtures_dir=_FIXTURES_DIR
    )


def _run(service: LocalLiveService, scenario: str) -> dict:
    _, body = service.create_proof_run({"scenario": scenario})
    service.drain_queue()
    _, detail = service.run_detail(body["runId"])
    return detail


# -- 1/2: port + single adapter -------------------------------------------


def test_artifact_store_port_is_neutral_protocol() -> None:
    # The port exposes only neutral, storage-agnostic operations.
    for method in ("write", "read", "exists", "evidence", "validate_key"):
        assert hasattr(ArtifactStore, method)
    # Evidence carries only neutral fields — no bucket/region/url/credential.
    fields = set(ArtifactEvidence.__dataclass_fields__)
    assert fields == {
        "artifact_id",
        "artifact_key",
        "content_hash",
        "size_bytes",
        "media_type",
        "created_at",
        "metadata",
    }


def test_local_filesystem_is_the_only_adapter() -> None:
    # Exactly one concrete adapter is implemented in the module.
    concrete = [
        name
        for name, obj in vars(artifact_store_module).items()
        if isinstance(obj, type)
        and name.endswith("ArtifactStore")
        and name != "ArtifactStore"
    ]
    assert concrete == ["LocalFilesystemArtifactStore"], concrete


def test_storage_module_has_no_cloud_sdk_terms() -> None:
    source = (
        _REPO_ROOT / "src" / "storytime" / "local_live" / "artifact_store.py"
    ).read_text(encoding="utf-8")
    lowered = source.lower()
    present = [t for t in _FORBIDDEN_MODULE_TERMS if t in lowered]
    assert not present, f"storage module references forbidden terms: {present}"


# -- 3/4: write/read + metadata -------------------------------------------


def test_write_then_read_roundtrip(store: LocalFilesystemArtifactStore) -> None:
    ev = store.write(
        artifact_key="run-1/proof/evidence.json",
        content=b'{"ok": true}',
        media_type="application/json",
        created_at="2026-05-29T00:00:00+00:00",
    )
    assert isinstance(ev, ArtifactEvidence)
    assert store.exists("run-1/proof/evidence.json")
    assert store.read("run-1/proof/evidence.json") == b'{"ok": true}'


def test_metadata_hash_size_media(store: LocalFilesystemArtifactStore) -> None:
    content = b"hello-artifact"
    ev = store.write(
        artifact_key="a/b/file.json", content=content, created_at="2026-05-29T00:00:00+00:00"
    )
    from hashlib import sha256

    assert ev.content_hash == sha256(content).hexdigest()
    assert ev.size_bytes == len(content)
    assert ev.media_type == "application/json"  # inferred from .json suffix
    # evidence() recomputes the same safe facts from disk.
    ev2 = store.evidence("a/b/file.json")
    assert ev2 is not None
    assert ev2.content_hash == ev.content_hash
    assert ev2.size_bytes == ev.size_bytes


# -- 5/6/7: key safety -----------------------------------------------------


@pytest.mark.parametrize(
    "bad_key",
    [
        "../escape.json",
        "a/../../b.json",
        "/etc/passwd",
        "/abs/path.json",
        "a\\b.json",
        "C:\\Windows\\x.json",
        "..",
        "",
        "   ",
    ],
)
def test_unsafe_keys_rejected(
    store: LocalFilesystemArtifactStore, bad_key: str
) -> None:
    with pytest.raises(UnsafeArtifactKeyError):
        store.validate_key(bad_key)
    # write and read also reject (write raises before touching disk).
    with pytest.raises(UnsafeArtifactKeyError):
        store.write(
            artifact_key=bad_key, content=b"x", created_at="2026-05-29T00:00:00+00:00"
        )
    # exists never raises; it returns False for unsafe keys.
    assert store.exists(bad_key) is False


@pytest.mark.skipif(
    sys.platform.startswith("win"), reason="symlink escape test is POSIX-oriented"
)
def test_symlink_escape_rejected(tmp_path: Path) -> None:
    root = tmp_path / "artifacts"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.txt").write_bytes(b"top secret")
    # A symlink inside the root that points outside the root.
    link = root / "link"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError):  # pragma: no cover - env without symlinks
        pytest.skip("filesystem does not support symlinks")
    store = LocalFilesystemArtifactStore(root=root)
    # Reading through the symlink escapes the root and must be rejected.
    with pytest.raises(UnsafeArtifactKeyError):
        store.read("link/secret.txt")
    with pytest.raises(UnsafeArtifactKeyError):
        store.write(
            artifact_key="link/evil.txt",
            content=b"x",
            created_at="2026-05-29T00:00:00+00:00",
        )


# -- 8: deterministic missing ---------------------------------------------


def test_missing_artifact_is_deterministic(
    store: LocalFilesystemArtifactStore,
) -> None:
    assert store.exists("run-x/proof/none.json") is False
    assert store.evidence("run-x/proof/none.json") is None
    with pytest.raises(ArtifactNotFoundError):
        store.read("run-x/proof/none.json")


# -- 9/10/11/12: proof-run routing + scenarios ----------------------------


def test_proof_artifacts_route_through_store(service: LocalLiveService) -> None:
    detail = _run(service, "success")
    assert detail["status"] == "completed"
    assert detail["artifacts"], "no artifact recorded for the run"
    key = detail["artifacts"][0]["key"]
    store = LocalFilesystemArtifactStore(root=service.runs_dir)
    # The recorded logical key resolves through the store and the bytes are real.
    assert store.exists(key)
    payload = json.loads(store.read(key))
    assert payload["kind"] == "storytime-proof-run-evidence"


@pytest.mark.parametrize(
    ("scenario", "status"),
    [
        ("success", "completed"),
        ("governance_failure", "failed"),
        ("artifact_validation_failure", "failed"),
    ],
)
def test_scenarios_intact_through_store(
    service: LocalLiveService, scenario: str, status: str
) -> None:
    detail = _run(service, scenario)
    assert detail["status"] == status
    assert detail["artifacts"], "evidence artifact missing after routing"
    if status == "failed":
        assert detail["failureReason"]


# -- 13/14: read-model / DTO path-leak safety -----------------------------


def test_read_model_artifacts_have_no_absolute_paths(
    service: LocalLiveService,
) -> None:
    detail = _run(service, "success")
    for art in detail["artifacts"]:
        assert not art["key"].startswith("/"), art["key"]
        assert ":" not in art["key"][:3], art["key"]  # no Windows drive prefix
        assert ".." not in art["key"]


def test_browser_evidence_has_no_leak_substrings(
    service: LocalLiveService,
) -> None:
    detail = _run(service, "success")
    _, runs_body = service.list_runs()
    artifact_root = str(service.runs_dir)
    for payload in (detail, runs_body):
        blob = json.dumps(payload)
        present = [s for s in _LEAK_SUBSTRINGS if s in blob]
        assert not present, f"DTO leaked unsafe substrings: {present}"
        assert artifact_root not in blob, "DTO leaked the artifact root path"
