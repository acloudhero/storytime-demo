"""Phase 14A.1 — controlled, durable proof-run harness.

This is the backend-owned "first real operator proof loop". A proof run is a
**real durable run** recorded in the SQLite state store: it creates a
``pipeline_run`` row, records ``stage_execution`` rows, appends append-only
``event_log`` events, writes a real evidence artifact to the run directory, and
records that artifact in ``stage_artifact``. Because the state lives in SQLite,
the run survives a local-live server restart — it is not an in-memory fake.

Safety boundary (Phase 14A.1 §6/§8):
- The browser submits **no** free text, path, URL, provider, or credential. The
  only accepted input is an optional fixture id drawn from a fixed allowlist.
- The run uses an approved, public-domain (CC0) demo fixture already in the
  repo. Only bounded fixture metadata (title / source id / licence / text hash)
  is recorded — never raw story text.
- The harness invokes **no** real TTS provider, **no** ffmpeg, and **no**
  network; it is deterministic and local-safe. It mirrors the pipeline's
  durable-state contracts without running fragile audio/provider paths.
"""

from __future__ import annotations

import json
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path

from storytime.events import EventType, PipelineEvent
from storytime.local_live.artifact_store import LocalFilesystemArtifactStore
from storytime.local_live.observability import (
    ARTIFACT_RECORDED,
    STAGE_COMPLETED,
    STAGE_STARTED,
    NullQueueWorkerObserver,
    QueueWorkerEventSink,
    emit,
)
from storytime.state.store import RunRecord, StateStore

# Fixed allowlist of approved proof fixtures. The browser may name one of these
# ids and nothing else; an unknown id is rejected. Each maps to an approved,
# public-domain demo manifest already committed to the repo.
APPROVED_FIXTURES: dict[str, str] = {
    "golden-path": "demo-golden-path.json",
}
DEFAULT_FIXTURE = "golden-path"

@dataclass(frozen=True, slots=True)
class _StageStep:
    """One step in a deterministic proof scenario.

    ``outcome`` is ``"completed"`` or ``"fail"``. A completed step records a
    completed ``stage_execution`` plus its ``event``. A failing step records a
    failed ``stage_execution`` (with ``error_kind`` / ``error_message``),
    optionally emits ``event`` (e.g. a governance evaluation that came back
    blocked), and terminates the run as failed.
    """

    stage: str
    event: EventType | None
    outcome: str
    error_kind: str | None = None
    error_message: str | None = None


# Allowlisted, deterministic proof scenarios. Each proves the durable
# state/stage/event/artifact contracts end to end without any real provider,
# ffmpeg, RSS, cloud, or network. Phase 14B.1 adds the two controlled failure
# scenarios so a reviewer can see intelligible failure evidence, not only a
# success.
DEFAULT_SCENARIO = "success"

# Phase 14C.1.1: the durable failure reason recorded when a local worker
# recovers a stale work item whose run had already committed one or more stage
# executions but never reached a terminal state. The run is failed cleanly
# without re-executing completed stages (no resumable partial-stage
# continuation — that would be a later phase if ever needed).
STALE_PARTIAL_REASON = (
    "local worker recovered a stale partial execution; run failed without "
    "re-executing completed stages"
)
STALE_PARTIAL_ERROR_KIND = "StalePartialExecution"

_SCENARIOS: dict[str, tuple[_StageStep, ...]] = {
    "success": (
        _StageStep("ingest", EventType.TEXT_INGESTED, "completed"),
        _StageStep("governance", EventType.GOVERNANCE_EVALUATED, "completed"),
        _StageStep("synthesize", EventType.SYNTHESIS_COMPLETED, "completed"),
        _StageStep("assemble", EventType.ASSEMBLY_COMPLETED, "completed"),
    ),
    "governance_failure": (
        _StageStep("ingest", EventType.TEXT_INGESTED, "completed"),
        _StageStep(
            "governance",
            EventType.GOVERNANCE_EVALUATED,
            "fail",
            error_kind="GovernanceBlocked",
            error_message=(
                "source rejected by the fail-closed governance gate "
                "(deterministic proof scenario)"
            ),
        ),
    ),
    "artifact_validation_failure": (
        _StageStep("ingest", EventType.TEXT_INGESTED, "completed"),
        _StageStep("governance", EventType.GOVERNANCE_EVALUATED, "completed"),
        _StageStep("synthesize", EventType.SYNTHESIS_COMPLETED, "completed"),
        _StageStep(
            "assemble",
            None,
            "fail",
            error_kind="ArtifactValidationFailed",
            error_message=(
                "assembled artifact failed deterministic validation: the "
                "recorded sha256 did not match the evidence artifact "
                "(proof scenario)"
            ),
        ),
    ),
}

# The public allowlist of scenario ids the browser may name.
APPROVED_SCENARIOS: tuple[str, ...] = tuple(_SCENARIOS)


class ProofRunError(ValueError):
    """Raised when a proof run is requested with unsafe or unknown input."""


@dataclass(frozen=True, slots=True)
class FixtureMeta:
    """Bounded, safe metadata extracted from an approved fixture manifest."""

    fixture_id: str
    source_id: str
    title: str
    license: str
    text_sha256: str
    manifest_sha256: str


def default_fixtures_dir(start: Path | None = None) -> Path:
    """Locate the repo's ``demo/seed`` directory by walking up from *start*.

    Falls back to ``demo/seed`` relative to the current directory. The proof
    fixtures are repo files (not packaged), so resolution is path-based.
    """
    here = (start or Path.cwd()).resolve()
    for base in (here, *here.parents):
        candidate = base / "demo" / "seed"
        if (candidate / APPROVED_FIXTURES[DEFAULT_FIXTURE]).is_file():
            return candidate
    return Path("demo/seed")


def resolve_fixture(fixture_id: str | None) -> str:
    """Validate and normalise a requested fixture id against the allowlist."""
    chosen = (fixture_id or DEFAULT_FIXTURE).strip()
    if chosen not in APPROVED_FIXTURES:
        allowed = ", ".join(sorted(APPROVED_FIXTURES))
        raise ProofRunError(
            f"unknown proof fixture {chosen!r}; allowed: {allowed}"
        )
    return chosen


def resolve_scenario(scenario_id: str | None) -> str:
    """Validate and normalise a requested scenario id against the allowlist."""
    chosen = (scenario_id or DEFAULT_SCENARIO).strip()
    if chosen not in _SCENARIOS:
        allowed = ", ".join(APPROVED_SCENARIOS)
        raise ProofRunError(
            f"unknown proof scenario {chosen!r}; allowed: {allowed}"
        )
    return chosen


def load_fixture_meta(fixture_id: str, fixtures_dir: Path) -> FixtureMeta:
    """Read bounded, safe metadata from an approved fixture manifest.

    Never returns or reads the raw story text body — only manifest metadata.
    """
    chosen = resolve_fixture(fixture_id)
    manifest_path = fixtures_dir / APPROVED_FIXTURES[chosen]
    if not manifest_path.is_file():
        raise ProofRunError(
            f"approved fixture manifest is missing: {manifest_path}"
        )
    raw = manifest_path.read_bytes()
    manifest = json.loads(raw)
    return FixtureMeta(
        fixture_id=chosen,
        source_id=str(manifest.get("source_id", chosen)),
        title=str(manifest.get("title", "")),
        license=str(manifest.get("license", "")),
        text_sha256=str(manifest.get("text_sha256", "")),
        manifest_sha256=sha256(raw).hexdigest(),
    )


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _new_run_id() -> str:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    return f"proof-{stamp}-{secrets.token_hex(3)}"


def reserve_proof_run(
    store: StateStore,
    *,
    runs_dir: Path,
    fixture_id: str | None = None,
    scenario: str | None = None,
    fixtures_dir: Path | None = None,
) -> str:
    """Reserve a durable proof run in the ``queued`` state; return its run id.

    This is the *request-path* half of the proof loop: it validates the
    fixture/scenario, creates the durable ``pipeline_run`` row in a ``queued``
    state, and records the ``RUN_CREATED`` event — but it does NOT execute any
    stages. Execution is performed later by a local worker via
    :func:`execute_proof_run`, so request acceptance is separated from
    execution. Raises :class:`ProofRunError` on an unknown fixture/scenario.
    """
    chosen = resolve_fixture(fixture_id)
    chosen_scenario = resolve_scenario(scenario)
    seed_dir = fixtures_dir or default_fixtures_dir()
    meta = load_fixture_meta(chosen, seed_dir)

    run_id = _new_run_id()
    created = _now()
    run_dir = runs_dir / run_id

    store.create_run(
        RunRecord(
            pipeline_run_id=run_id,
            created_at=created,
            updated_at=created,
            current_stage="queued",
            status="queued",
            source_manifest_hash=meta.manifest_sha256,
            run_dir=str(run_dir),
        )
    )
    store.append_event(
        PipelineEvent(
            event_type=EventType.RUN_CREATED,
            pipeline_run_id=run_id,
            occurred_at=datetime.now(UTC),
            stage_name="run",
            payload={
                "mode": "proof",
                "mock": True,
                "scenario": chosen_scenario,
                "fixtureId": meta.fixture_id,
                "sourceId": meta.source_id,
                "license": meta.license,
                "lifecycle": "queued",
            },
        )
    )
    store._conn.commit()  # noqa: SLF001 - persist reservation durably
    return run_id


def execute_proof_run(
    store: StateStore,
    run_id: str,
    *,
    runs_dir: Path,
    fixture_id: str | None = None,
    scenario: str | None = None,
    fixtures_dir: Path | None = None,
    observer: QueueWorkerEventSink | None = None,
) -> str:
    """Execute a previously reserved proof run; return its run id.

    This is the *worker* half of the proof loop. It walks the deterministic
    scenario plan against the EXISTING run row created by
    :func:`reserve_proof_run`, persisting each stage / event / artifact and the
    terminal ``RUN_COMPLETED`` or ``RUN_FAILED`` state to SQLite. It is
    idempotent in the sense that it operates on a specific ``run_id`` and never
    creates a second run. ``scenario`` selects an allowlisted deterministic
    plan; no scenario invokes a real provider, ffmpeg, RSS, cloud, or network.

    ``observer`` receives safe, minimal queue/worker lifecycle observations
    (stage and artifact events); emission is fail-soft and never changes
    execution semantics. Defaults to a no-op sink.
    """
    sink: QueueWorkerEventSink = observer or NullQueueWorkerObserver()
    chosen = resolve_fixture(fixture_id)
    chosen_scenario = resolve_scenario(scenario)
    plan = _SCENARIOS[chosen_scenario]
    seed_dir = fixtures_dir or default_fixtures_dir()
    meta = load_fixture_meta(chosen, seed_dir)

    reserved = store.get_run(run_id)
    created = reserved.created_at if reserved is not None else _now()

    # Idempotency / stale-partial guard. A run is executed at most once. If
    # stage executions already exist for this run, a prior worker has already
    # executed (or partially executed) it, so a recovered or redelivered work
    # item must NOT re-run any stage.
    if store.list_stage_executions(run_id):
        status = reserved.status if reserved is not None else "unknown"
        if status in ("completed", "failed"):
            # Already terminal: return idempotently, leaving state untouched.
            return run_id
        # Non-terminal (e.g. queued/running) but with committed stages means a
        # worker was lost AFTER partial execution. Fail the run cleanly without
        # re-executing completed stages and without adding any stage row.
        store.update_run_state(
            run_id,
            status="failed",
            current_stage=reserved.current_stage if reserved is not None else "recover",
            updated_at=_now(),
        )
        store.append_event(
            PipelineEvent(
                event_type=EventType.RUN_FAILED,
                pipeline_run_id=run_id,
                occurred_at=datetime.now(UTC),
                stage_name="run",
                payload={
                    "mode": "proof",
                    "mock": True,
                    "lifecycle": "stale-partial-recovery",
                    "errorKind": STALE_PARTIAL_ERROR_KIND,
                    "failedStage": (
                        reserved.current_stage if reserved is not None else "recover"
                    ),
                    "reason": STALE_PARTIAL_REASON,
                },
            )
        )
        store._conn.commit()  # noqa: SLF001 - persist clean failure durably
        return run_id

    store.update_run_state(
        run_id,
        status="running",
        current_stage=plan[0].stage,
        updated_at=_now(),
    )
    store._conn.commit()  # noqa: SLF001 - persist running transition durably

    # Walk the scenario plan, persisting each transition. Stop at the first
    # failing step.
    attempted: list[str] = []
    failed_step: _StageStep | None = None
    for step in plan:
        attempted.append(step.stage)
        emit(sink, STAGE_STARTED, run_id=run_id, stage_name=step.stage, status="started")
        if step.outcome == "fail":
            store.record_stage_execution(
                pipeline_run_id=run_id,
                stage_name=step.stage,
                started_at=_now(),
                ended_at=_now(),
                status="failed",
                error_kind=step.error_kind,
                error_message=step.error_message,
            )
            if step.event is not None:
                store.append_event(
                    PipelineEvent(
                        event_type=step.event,
                        pipeline_run_id=run_id,
                        occurred_at=datetime.now(UTC),
                        stage_name=step.stage,
                        payload={
                            "mode": "proof",
                            "mock": True,
                            "outcome": "failed",
                            "decision": "blocked",
                        },
                    )
                )
            store.update_run_state(
                run_id,
                status="failed",
                current_stage=step.stage,
                updated_at=_now(),
            )
            store._conn.commit()  # noqa: SLF001 - persist failure durably
            emit(
                sink,
                STAGE_COMPLETED,
                run_id=run_id,
                stage_name=step.stage,
                status="failed",
                failure_reason=step.error_message,
            )
            failed_step = step
            break

        store.record_stage_execution(
            pipeline_run_id=run_id,
            stage_name=step.stage,
            started_at=_now(),
            ended_at=_now(),
            status="completed",
        )
        emit(
            sink,
            STAGE_COMPLETED,
            run_id=run_id,
            stage_name=step.stage,
            status="completed",
        )
        if step.event is not None:
            store.append_event(
                PipelineEvent(
                    event_type=step.event,
                    pipeline_run_id=run_id,
                    occurred_at=datetime.now(UTC),
                    stage_name=step.stage,
                    payload={"mode": "proof", "mock": True},
                )
            )
        store.update_run_state(
            run_id,
            status="running",
            current_stage=step.stage,
            updated_at=_now(),
        )
        store._conn.commit()  # noqa: SLF001 - persist each stage durably

    outcome = "failed" if failed_step is not None else "completed"

    # Write a real, deterministic evidence artifact and register it. The
    # artifact is produced for both success and failure so a reviewer can
    # inspect evidence either way; it carries only bounded fixture metadata,
    # never raw story text.
    evidence: dict[str, object] = {
        "kind": "storytime-proof-run-evidence",
        "runId": run_id,
        "mode": "proof",
        "mock": True,
        "scenario": chosen_scenario,
        "outcome": outcome,
        "createdAt": created,
        "fixture": {
            "id": meta.fixture_id,
            "sourceId": meta.source_id,
            "title": meta.title,
            "license": meta.license,
            "textSha256": meta.text_sha256,
            "manifestSha256": meta.manifest_sha256,
        },
        "stagesAttempted": attempted,
        "note": (
            "Deterministic local proof run. No real TTS provider, no ffmpeg, "
            "no network. State is backend-owned in SQLite and survives restart."
        ),
    }
    if failed_step is not None:
        evidence["failure"] = {
            "stage": failed_step.stage,
            "errorKind": failed_step.error_kind,
            "reason": failed_step.error_message,
        }
    evidence_bytes = json.dumps(evidence, indent=2, sort_keys=True).encode("utf-8")
    # Phase 14C.3: artifact writes flow through the backend-owned ArtifactStore
    # seam (local filesystem adapter) rather than a direct filesystem write. The
    # logical key stays relative; the adapter owns the root, validates the key,
    # and keeps the artifact under the runs directory. The browser never sees a
    # filesystem path — only the logical key and safe evidence.
    artifact_key = f"{run_id}/proof/evidence.json"
    artifact_store = LocalFilesystemArtifactStore(root=runs_dir)
    artifact_store.write(
        artifact_key=artifact_key,
        content=evidence_bytes,
        media_type="application/json",
        created_at=_now(),
    )
    emit(sink, ARTIFACT_RECORDED, run_id=run_id, artifact_key=artifact_key, status="recorded")
    last_stage = attempted[-1] if attempted else "assemble"
    store.record_stage_artifacts(
        pipeline_run_id=run_id,
        stage_name=last_stage,
        artifact_keys=[artifact_key],
        recorded_at=_now(),
    )

    if failed_step is not None:
        store.append_event(
            PipelineEvent(
                event_type=EventType.RUN_FAILED,
                pipeline_run_id=run_id,
                occurred_at=datetime.now(UTC),
                stage_name="run",
                payload={
                    "mode": "proof",
                    "mock": True,
                    "scenario": chosen_scenario,
                    "failedStage": failed_step.stage,
                    "errorKind": failed_step.error_kind,
                    "reason": failed_step.error_message,
                    "artifactKey": artifact_key,
                },
            )
        )
    else:
        store.update_run_state(
            run_id,
            status="completed",
            current_stage="complete",
            updated_at=_now(),
        )
        store.append_event(
            PipelineEvent(
                event_type=EventType.RUN_COMPLETED,
                pipeline_run_id=run_id,
                occurred_at=datetime.now(UTC),
                stage_name="run",
                payload={
                    "mode": "proof",
                    "mock": True,
                    "scenario": chosen_scenario,
                    "artifactKey": artifact_key,
                    "artifactSha256": sha256(evidence_bytes).hexdigest(),
                },
            )
        )
    store._conn.commit()  # noqa: SLF001 - persist terminal state durably
    return run_id


def run_proof_fixture(
    store: StateStore,
    *,
    runs_dir: Path,
    fixture_id: str | None = None,
    scenario: str | None = None,
    fixtures_dir: Path | None = None,
) -> str:
    """Reserve and immediately execute a proof run synchronously; return its id.

    A convenience that composes :func:`reserve_proof_run` and
    :func:`execute_proof_run` in one call. The local-live request path does NOT
    use this (it reserves + enqueues, and a worker executes); this remains for
    direct callers and tests that want the full run end-to-end in one step. The
    durable end state is identical to the queued/worker path.
    """
    run_id = reserve_proof_run(
        store,
        runs_dir=runs_dir,
        fixture_id=fixture_id,
        scenario=scenario,
        fixtures_dir=fixtures_dir,
    )
    return execute_proof_run(
        store,
        run_id,
        runs_dir=runs_dir,
        fixture_id=fixture_id,
        scenario=scenario,
        fixtures_dir=fixtures_dir,
    )
