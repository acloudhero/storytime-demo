"""Phase 3 architecture-boundary checks.

These tests prove the Phase 3 implementation did not erode the locked
architecture: ARCH-LOCK annotations survive, and no cloud / event-bus /
watcher dependency was smuggled in. OpenTelemetry import isolation is covered
separately by test_import_boundaries.py.
"""

from __future__ import annotations

from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src" / "storytime"

# ARCH-LOCK annotations that must survive Phase 3 unchanged.
_REQUIRED_ARCH_LOCKS = (
    "ARCH-LOCK: Persist-before-telemetry, single transaction",
    "ARCH-LOCK: Telemetry Import Boundary",
    "ARCH-LOCK: Sole OpenTelemetry Integration Point",
    "ARCH-LOCK: DTO Boundary",
    "ARCH-LOCK: Stage Boundary",
    "ARCH-LOCK: RunnerContext is minimal and frozen",
    "ARCH-LOCK: Artifact Envelope Contract",
    "ARCH-LOCK: Artifact Compatibility Reader",
    "ARCH-LOCK: Manifest Closed Schema",
    "ARCH-LOCK: SQLite is the source of truth",
    "ARCH-LOCK: Single-transaction persistence",
    "ARCH-LOCK: TTS Adapter Contract",
    "ARCH-LOCK: MockTTS is a real generator, not a no-op",
    "ARCH-LOCK: Internal Event Model",
    "ARCH-LOCK: Storage Seam",
)

# Tokens that would indicate a forbidden cloud / bus / watcher dependency.
_FORBIDDEN_IMPORTS = (
    "import boto3",
    "from boto3",
    "import watchdog",
    "from watchdog",
    "import google.cloud",
    "from google.cloud",
    "import pika",
    "import kafka",
    "import celery",
)


def _all_source() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8") for path in _SRC.rglob("*.py")
    )


def test_required_arch_lock_comments_remain() -> None:
    source = _all_source()
    missing = [marker for marker in _REQUIRED_ARCH_LOCKS if marker not in source]
    assert missing == [], f"ARCH-LOCK annotations removed or altered: {missing}"


def test_no_cloud_event_bus_or_watcher_imports() -> None:
    offenders: list[str] = []
    for path in _SRC.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for token in _FORBIDDEN_IMPORTS:
            if token in text:
                offenders.append(f"{path.name}: {token}")
    assert offenders == [], f"forbidden cloud/bus/watcher imports: {offenders}"
