"""Phase 14C.4 — tests for the minimal queue/worker observability boundary.

Prove the boundary exists, emits safe ordered lifecycle events, preserves
queue/worker semantics and scenarios, is fail-soft, and never leaks unsafe
substrings (paths, roots, credentials, secrets, tokens, signed URLs, raw text).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from storytime.local_live import observability as obs_mod
from storytime.local_live.observability import (
    EVENT_NAMES,
    InMemoryQueueWorkerObserver,
    NullQueueWorkerObserver,
    QueueWorkerEvent,
    QueueWorkerEventSink,
    emit,
)
from storytime.local_live.server import LocalLiveService

_REPO_ROOT = Path(__file__).resolve().parents[1]
_FIXTURES_DIR = _REPO_ROOT / "demo" / "seed"

_SUCCESS_ORDER = (
    "work.enqueued",
    "work.claimed",
    "work.started",
    "stage.started",
    "stage.completed",
    "stage.started",
    "stage.completed",
    "stage.started",
    "stage.completed",
    "stage.started",
    "stage.completed",
    "artifact.recorded",
    "work.completed",
)

_LEAK_SUBSTRINGS = (
    "/tmp/",
    "/home/",
    "C:\\",
    ".db",
    "signed_url",
    "credential",
    "secret",
    "token",
    "api_key",
    "authorization",
    "bearer",
    "bucket",
    "s3://",
    "minio",
    "raw_text",
    "story_text",
    "prompt",
)


def _service(tmp_path: Path, observer: QueueWorkerEventSink) -> tuple[LocalLiveService, Path]:
    runs = tmp_path / "runs"
    runs.mkdir(parents=True, exist_ok=True)
    svc = LocalLiveService(
        db_path=runs / "state.db",
        runs_dir=runs,
        fixtures_dir=_FIXTURES_DIR,
        observer=observer,
    )
    return svc, runs


def _run(svc: LocalLiveService, scenario: str) -> dict:
    _, body = svc.create_proof_run({"scenario": scenario})
    svc.drain_queue()
    _, detail = svc.run_detail(body["runId"])
    return detail


# -- 1/2: boundary type + safe event shape --------------------------------


def test_boundary_protocol_and_sinks_exist() -> None:
    assert hasattr(QueueWorkerEventSink, "record")
    # Both sinks satisfy the protocol shape.
    assert hasattr(NullQueueWorkerObserver(), "record")
    rec = InMemoryQueueWorkerObserver()
    assert rec.events == ()


def test_event_record_uses_safe_neutral_fields() -> None:
    fields = set(QueueWorkerEvent.__dataclass_fields__)
    assert fields == {
        "event_name",
        "created_at",
        "run_id",
        "work_item_id",
        "stage_name",
        "artifact_key",
        "status",
        "failure_reason",
        "worker_id",
        "attempt_number",
    }
    # to_dict omits unpopulated fields.
    ev = QueueWorkerEvent(event_name="work.enqueued", created_at="t", run_id="r")
    assert ev.to_dict() == {"eventName": "work.enqueued", "createdAt": "t", "runId": "r"}


def test_event_name_vocabulary_is_bounded() -> None:
    # No retry/recovery or cloud/distributed names crept in.
    assert frozenset(
        {
            "work.enqueued",
            "work.claimed",
            "work.started",
            "stage.started",
            "stage.completed",
            "artifact.recorded",
            "work.completed",
            "work.failed",
        }
    ) == EVENT_NAMES


# -- 3/4: lifecycle events emitted in deterministic order -----------------


def test_success_emits_expected_events_in_order(tmp_path: Path) -> None:
    rec = InMemoryQueueWorkerObserver()
    svc, _ = _service(tmp_path, rec)
    detail = _run(svc, "success")
    assert detail["status"] == "completed"
    assert rec.event_names() == _SUCCESS_ORDER


# -- 5/6/7: failure scenarios preserved + safe failed event ---------------


def test_governance_failure_emits_work_failed_and_preserved(tmp_path: Path) -> None:
    rec = InMemoryQueueWorkerObserver()
    svc, _ = _service(tmp_path, rec)
    detail = _run(svc, "governance_failure")
    assert detail["status"] == "failed"
    assert detail["failureReason"]
    assert rec.event_names()[-1] == "work.failed"
    # A safe stage.completed(failed) was emitted for the failing stage.
    assert any(
        e.event_name == "stage.completed" and e.status == "failed" for e in rec.events
    )


def test_artifact_validation_failure_preserved(tmp_path: Path) -> None:
    rec = InMemoryQueueWorkerObserver()
    svc, _ = _service(tmp_path, rec)
    detail = _run(svc, "artifact_validation_failure")
    assert detail["status"] == "failed"
    assert "work.failed" in rec.event_names()


# -- 8: artifact.recorded uses logical key --------------------------------


def test_artifact_recorded_uses_logical_key(tmp_path: Path) -> None:
    rec = InMemoryQueueWorkerObserver()
    svc, _ = _service(tmp_path, rec)
    _run(svc, "success")
    recorded = [e for e in rec.events if e.event_name == "artifact.recorded"]
    assert len(recorded) == 1
    key = recorded[0].artifact_key
    assert key is not None
    assert not key.startswith("/")
    assert ".." not in key
    assert key.endswith("/proof/evidence.json")


# -- 9/10/11: no unsafe leakage -------------------------------------------


@pytest.mark.parametrize(
    "scenario", ["success", "governance_failure", "artifact_validation_failure"]
)
def test_events_have_no_unsafe_substrings(tmp_path: Path, scenario: str) -> None:
    rec = InMemoryQueueWorkerObserver()
    svc, runs = _service(tmp_path, rec)
    _run(svc, scenario)
    blob = json.dumps([e.to_dict() for e in rec.events])
    present = [s for s in _LEAK_SUBSTRINGS if s in blob]
    assert not present, f"observation events leaked unsafe substrings: {present}"
    assert str(runs) not in blob, "events leaked the artifact/runs root path"


# -- 12/13: semantics + scenarios unchanged -------------------------------


@pytest.mark.parametrize(
    ("scenario", "status"),
    [
        ("success", "completed"),
        ("governance_failure", "failed"),
        ("artifact_validation_failure", "failed"),
    ],
)
def test_observation_does_not_change_outcomes(
    tmp_path: Path, scenario: str, status: str
) -> None:
    # With a recording observer.
    rec = InMemoryQueueWorkerObserver()
    svc_a, _ = _service(tmp_path / "a", rec)
    assert _run(svc_a, scenario)["status"] == status
    # With the default no-op observer (unchanged behavior).
    svc_b, _ = _service(tmp_path / "b", NullQueueWorkerObserver())
    assert _run(svc_b, scenario)["status"] == status


# -- fail-soft -------------------------------------------------------------


class _ThrowingSink:
    def record(self, event: QueueWorkerEvent) -> None:
        raise RuntimeError("observation boom")


def test_observation_is_fail_soft(tmp_path: Path) -> None:
    # A sink that always raises must not break the proof loop.
    svc, _ = _service(tmp_path, _ThrowingSink())
    detail = _run(svc, "success")
    assert detail["status"] == "completed"


def test_emit_helper_is_fail_soft() -> None:
    # Direct emit() with a throwing sink does not propagate.
    emit(_ThrowingSink(), "work.enqueued", run_id="r")  # must not raise


def test_default_observer_module_has_no_telemetry_imports() -> None:
    source = (
        _REPO_ROOT / "src" / "storytime" / "local_live" / "observability.py"
    ).read_text(encoding="utf-8")
    # Scan import statements only (prose negations like "no OpenTelemetry SDK"
    # in the module docstring are fine and expected).
    import_lines = [
        ln.strip().lower()
        for ln in source.splitlines()
        if ln.strip().startswith(("import ", "from "))
    ]
    forbidden_pkgs = (
        "opentelemetry",
        "prometheus",
        "grafana",
        "datadog",
        "newrelic",
        "structlog",
        "loguru",
        "boto3",
    )
    for line in import_lines:
        for pkg in forbidden_pkgs:
            assert pkg not in line, f"observability module imports {pkg!r}: {line!r}"
    # Sanity: the module is the one under test.
    assert obs_mod.WORK_ENQUEUED == "work.enqueued"
