"""Phase 13G — local-bridge safety / boundary guard tests.

Static guards over the local-bridge source that lock the phase's safety
boundary: no shell / subprocess execution, no forbidden web-framework or queue
dependency, no browser durable storage or frontend wiring, and no ``0.0.0.0``
bind in implementation code. These complement the behavioural tests; they fail
fast if a future edit drifts past the boundary.
"""

from __future__ import annotations

from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]
_BRIDGE_SRC = _REPO_ROOT / "src" / "storytime" / "local_bridge"
_FRONTEND_SRC = _REPO_ROOT / "frontend" / "src"


def _bridge_files() -> list[Path]:
    return sorted(_BRIDGE_SRC.rglob("*.py"))


def test_bridge_package_exists() -> None:
    assert _BRIDGE_SRC.is_dir()
    assert _bridge_files(), "local_bridge package has no Python modules"


@pytest.mark.parametrize("path", _bridge_files(), ids=lambda p: p.name)
def test_no_shell_or_subprocess_execution(path: Path) -> None:
    """The bridge never executes shell commands.

    Detects actual execution constructs (import / call / ``shell=True``) rather
    than bare mentions, so the DTO rejection denylist — which legitimately holds
    the string ``"subprocess"`` to *reject* such a field — does not trip this.
    """
    source = path.read_text(encoding="utf-8")
    for forbidden in (
        "import subprocess",
        "subprocess.",
        "os.system(",
        "shell=True",
        "os.popen(",
        "pty.spawn",
    ):
        assert forbidden not in source, (
            f"{path.name} contains forbidden execution primitive {forbidden!r}"
        )


@pytest.mark.parametrize("path", _bridge_files(), ids=lambda p: p.name)
def test_no_zero_bind_in_implementation(path: Path) -> None:
    """No 0.0.0.0 bind literal in bridge implementation source."""
    assert "0.0.0.0" not in path.read_text(encoding="utf-8"), (
        f"{path.name} references 0.0.0.0; the bridge binds loopback only"
    )


@pytest.mark.parametrize("path", _bridge_files(), ids=lambda p: p.name)
def test_no_forbidden_dependencies(path: Path) -> None:
    """The bridge uses only the standard library + internal storytime modules."""
    source = path.read_text(encoding="utf-8").lower()
    forbidden = (
        "import fastapi",
        "from fastapi",
        "import flask",
        "from flask",
        "import starlette",
        "import django",
        "import celery",
        "import redis",
        "import pydantic",
        "from pydantic",
        "import jsonschema",
        "from jsonschema",
        "import uvicorn",
        "import gunicorn",
        "import requests",
        "import httpx",
    )
    for needle in forbidden:
        assert needle not in source, (
            f"{path.name} imports a forbidden dependency: {needle!r}"
        )


@pytest.mark.parametrize("path", _bridge_files(), ids=lambda p: p.name)
def test_no_browser_durable_storage_or_frontend_wiring(path: Path) -> None:
    """The bridge adds no browser storage and no frontend fetch wiring."""
    source = path.read_text(encoding="utf-8")
    for needle in (
        "localStorage",
        "sessionStorage",
        "IndexedDB",
        "XMLHttpRequest",
    ):
        assert needle not in source, (
            f"{path.name} references browser storage / wiring {needle!r}"
        )


def test_frontend_src_untouched_by_bridge() -> None:
    """The bridge is a Python package; it must not live under frontend/src."""
    assert _FRONTEND_SRC.is_dir()
    # No bridge Python file should be located in the frontend tree.
    for path in _bridge_files():
        assert _FRONTEND_SRC not in path.parents, (
            "local_bridge source must not live under frontend/src"
        )


def test_single_concurrency_constant_is_one() -> None:
    """The reported max concurrency is exactly one (no multi-worker fleet)."""
    from storytime.local_bridge.action_queue import ActionQueue

    queue = ActionQueue(lambda job: {"status": "completed"}, capacity=4)
    assert queue.snapshot()["maxConcurrency"] == 1


def test_no_persistent_or_external_queue_dependency() -> None:
    """The queue is purely in-memory: it uses only stdlib queue / threading."""
    source = (_BRIDGE_SRC / "action_queue.py").read_text(encoding="utf-8").lower()
    for needle in (
        "import redis",
        "import celery",
        "from celery",
        "import kombu",
        "import pika",
        "import sqlite3",
        "import boto3",
        "import kafka",
    ):
        assert needle not in source, (
            f"action_queue.py imports an external queue backend: {needle!r}"
        )
