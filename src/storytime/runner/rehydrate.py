"""Rehydration — reconstructing a resumable run from SQLite + artifact envelopes.

ARCH-LOCK: SQLite is the source of truth
DO NOT REFACTOR: resume reads run state, stage executions, and artifact keys
from SQLite, and prior-stage payloads from their artifact envelopes. It never
trusts an in-memory summary and never bypasses the envelope contract.

This module is pure read/validation logic. It produces a ResumePlan — the
facts the composition root (storytime.pipeline) needs to rebuild StageInput
DTOs and continue a run — but it builds no concrete stages and writes nothing.

Phase 4 (OI-10). Resume invariants enforced here:
  * completed stages form a contiguous prefix of the canonical stage order;
  * every rehydrated artifact is resolved through the configured StorageAdapter
    root (never an absolute path), version-checked, run-id-checked, and
    hash-verified before it is reused;
  * a missing, corrupted, or mismatched artifact refuses the resume loudly.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import PurePosixPath

from storytime.adapters.telemetry.attributes import LABEL_REASON
from storytime.adapters.telemetry.metrics import (
    METRIC_ARTIFACT_VALIDATION_FAILED_TOTAL,
)
from storytime.artifacts import (
    SUPPORTED_ARTIFACT_VERSIONS,
    ArtifactEnvelope,
    ArtifactEnvelopeError,
    from_json,
)
from storytime.runner.context import RunnerContext
from storytime.state import RunRecord
from storytime.util.hashing import sha256_bytes


class RehydrationError(RuntimeError):
    """Raised when a run cannot be safely rehydrated from persisted state."""


@dataclass(frozen=True, slots=True)
class GateResumeSpec:
    """Identifies one approval gate whose persisted decision resume must read.

    stage_name is the gate's stage/approval-row name ("approve_text" /
    "approve_audio"); requested_event is the event_type string whose presence
    in the event_log means the gate's *_APPROVAL_REQUESTED event was already
    emitted (so a re-run during resume does not append a duplicate).
    """

    stage_name: str
    requested_event: str


@dataclass(frozen=True, slots=True)
class ResumePlan:
    """The validated facts needed to resume a run.

    completed_stage_names are stages already SUCCEEDED (a contiguous prefix of
    the canonical order); they must not be re-executed. seed_artifacts are the
    validated output-artifact keys of the last completed stage and become the
    input of the first resumed stage. gate_decisions / gate_requests_emitted
    are keyed by gate stage name (Phase 4.1: a run may have both the text and
    audio gates), letting the composition root inject each gate's
    StageInput.params.
    """

    run: RunRecord
    completed_stage_names: frozenset[str]
    seed_artifacts: tuple[str, ...]
    gate_decisions: Mapping[str, str | None]
    gate_requests_emitted: Mapping[str, bool]
    prior_traceparent: str | None = None
    """W3C traceparent of the last completed stage's seed artifact envelope.

    Phase 5: the durable trace-context anchor a resumed run links its fresh
    trace back to. None when telemetry was disabled for the prior run (the
    envelope carries no traceparent) or when nothing has completed yet. It is
    a *view* identifier only -- pipeline_run_id remains the durable key.
    """


def load_run_or_raise(ctx: RunnerContext, pipeline_run_id: str) -> RunRecord:
    """Return the run with *pipeline_run_id*, or raise a clear RehydrationError."""
    run = ctx.state.get_run(pipeline_run_id)
    if run is None:
        raise RehydrationError(
            f"no pipeline run found with pipeline_run_id={pipeline_run_id!r}"
        )
    return run


def _is_relative_key(key: str) -> bool:
    """True if *key* is a portable relative storage key (not an absolute path).

    A run must survive its workspace being relocated; an absolute path
    persisted into SQLite or an envelope would break that. Storage keys are
    POSIX-style relative paths resolved through the StorageAdapter root.
    """
    if not key or key.startswith("/") or key.startswith("\\"):
        return False
    # A Windows drive-letter or UNC root would also be non-portable.
    if len(key) >= 2 and key[1] == ":":
        return False
    return not PurePosixPath(key).is_absolute()


def _record_validation_failure(ctx: RunnerContext, reason: str) -> None:
    """Record one artifact-validation failure metric, keyed by *reason*.

    Telemetry is a view, never a gate: this is best-effort and runs just
    before the RehydrationError is raised. Under NoopTelemetry it is a no-op.
    """
    ctx.telemetry.record_metric(
        METRIC_ARTIFACT_VALIDATION_FAILED_TOTAL,
        1,
        attributes={LABEL_REASON: reason},
    )


def validate_artifact(ctx: RunnerContext, artifact_key: str) -> ArtifactEnvelope:
    """Load and fully validate one artifact envelope for reuse during resume.

    Checks, in order: the envelope key is relative; the envelope parses and
    its artifact_version is supported; its pipeline_run_id and payload_path
    are well-formed and the payload_path is relative; the payload exists and
    its SHA-256 matches the envelope's recorded digest. Any failure raises
    RehydrationError so a resumed run refuses to build on bad state.

    Phase 5: every failure path also records one
    pipeline_artifact_validation_failed_total metric with a fixed, low-
    cardinality ``reason`` label before raising. The reason set is closed:
    non_relative_key, envelope_missing, envelope_invalid, unsupported_version,
    non_relative_payload, payload_missing, hash_mismatch.
    """
    if not _is_relative_key(artifact_key):
        _record_validation_failure(ctx, "non_relative_key")
        raise RehydrationError(
            f"artifact key is not a portable relative path: {artifact_key!r}"
        )
    try:
        envelope_text = ctx.storage.read_text(artifact_key)
    except (FileNotFoundError, OSError) as exc:
        _record_validation_failure(ctx, "envelope_missing")
        raise RehydrationError(
            f"artifact envelope is missing or unreadable: {artifact_key!r} ({exc})"
        ) from exc
    try:
        envelope = from_json(envelope_text)
    except ArtifactEnvelopeError as exc:
        _record_validation_failure(ctx, "envelope_invalid")
        raise RehydrationError(
            f"artifact envelope {artifact_key!r} is invalid: {exc}"
        ) from exc

    if envelope.artifact_version not in SUPPORTED_ARTIFACT_VERSIONS:
        _record_validation_failure(ctx, "unsupported_version")
        raise RehydrationError(
            f"artifact envelope {artifact_key!r} declares unsupported "
            f"artifact_version {envelope.artifact_version}"
        )
    if not _is_relative_key(envelope.payload_path):
        _record_validation_failure(ctx, "non_relative_payload")
        raise RehydrationError(
            f"artifact envelope {artifact_key!r} has a non-relative "
            f"payload_path: {envelope.payload_path!r}"
        )
    try:
        payload = ctx.storage.read_bytes(envelope.payload_path)
    except (FileNotFoundError, OSError) as exc:
        _record_validation_failure(ctx, "payload_missing")
        raise RehydrationError(
            f"artifact payload is missing or unreadable: "
            f"{envelope.payload_path!r} ({exc})"
        ) from exc

    actual_sha256 = sha256_bytes(payload)
    if actual_sha256 != envelope.payload_sha256:
        _record_validation_failure(ctx, "hash_mismatch")
        raise RehydrationError(
            f"artifact payload hash mismatch for {envelope.payload_path!r}: "
            f"envelope records {envelope.payload_sha256}, payload is {actual_sha256}"
        )
    return envelope


def _completed_prefix(
    canonical_order: Sequence[str], succeeded: frozenset[str]
) -> list[str]:
    """Return the longest leading run of *canonical_order* fully in *succeeded*.

    Raises RehydrationError if a stage succeeded out of order (a gap), which
    would mean the persisted run state is internally inconsistent.
    """
    prefix: list[str] = []
    for name in canonical_order:
        if name in succeeded:
            prefix.append(name)
        else:
            break
    if set(prefix) != succeeded:
        out_of_order = sorted(succeeded - set(prefix))
        raise RehydrationError(
            "inconsistent run state: stage(s) succeeded out of canonical order: "
            f"{out_of_order}"
        )
    return prefix


def build_resume_plan(
    ctx: RunnerContext,
    pipeline_run_id: str,
    *,
    canonical_order: Sequence[str],
    gate_specs: Sequence[GateResumeSpec],
) -> ResumePlan:
    """Assemble and validate a ResumePlan for *pipeline_run_id*.

    *canonical_order* is the run's full ordered stage-name list, including
    whichever approval gates the run was configured with. *gate_specs* lists
    every such gate; each gate's persisted decision and whether its request
    event was already emitted are read so the composition root can inject the
    gate StageInput.params. A run with no gates passes an empty *gate_specs*.
    """
    run = load_run_or_raise(ctx, pipeline_run_id)
    if run.status == "completed":
        raise RehydrationError(
            f"run {pipeline_run_id} is already completed; nothing to resume"
        )
    if run.status == "failed":
        raise RehydrationError(
            f"run {pipeline_run_id} is in a failed/rejected state and cannot be "
            "resumed; start a new run"
        )

    executions = ctx.state.list_stage_executions(pipeline_run_id)
    succeeded = frozenset(
        e.stage_name for e in executions if e.status == "succeeded"
    )
    prefix = _completed_prefix(canonical_order, succeeded)

    # Seed artifacts: the validated output artifacts of the last completed
    # stage. Empty when nothing has completed yet (a brand-new resume target).
    seed_artifacts: tuple[str, ...] = ()
    prior_traceparent: str | None = None
    if prefix:
        last_completed = prefix[-1]
        artifact_rows = [
            row
            for row in ctx.state.list_stage_artifacts(pipeline_run_id)
            if row.stage_name == last_completed
        ]
        for row in artifact_rows:
            envelope = validate_artifact(ctx, row.artifact_key)  # refuses on bad state
            # Phase 5: the durable trace anchor for the resumed run's linked
            # trace. Every envelope a single stage wrote carries that stage's
            # span traceparent, so the first non-None value is canonical.
            if prior_traceparent is None and envelope.trace_context.traceparent:
                prior_traceparent = envelope.trace_context.traceparent
        seed_artifacts = tuple(row.artifact_key for row in artifact_rows)

    # Read each gate's persisted decision and request-event presence. Keyed by
    # gate stage name so the text and audio gates never shadow one another.
    logged_event_types = frozenset(ctx.state.event_types(pipeline_run_id))
    gate_decisions: dict[str, str | None] = {}
    gate_requests_emitted: dict[str, bool] = {}
    for spec in gate_specs:
        approval = ctx.state.latest_approval(pipeline_run_id, spec.stage_name)
        gate_decisions[spec.stage_name] = (
            approval.decision if approval is not None else None
        )
        gate_requests_emitted[spec.stage_name] = (
            spec.requested_event in logged_event_types
        )

    return ResumePlan(
        run=run,
        completed_stage_names=frozenset(prefix),
        seed_artifacts=seed_artifacts,
        gate_decisions=gate_decisions,
        gate_requests_emitted=gate_requests_emitted,
        prior_traceparent=prior_traceparent,
    )
