"""Phase 15B — Cloud Boundary Readiness: guard tests.

These tests prove the pure-data, provider-neutral boundary-readiness model and
the phase-state discipline for Phase 15B without changing any locked behaviour.
They cover the readiness model, the four cloud-growth boundaries (queue/worker,
artifact/storage, observability/export, recovery/idempotency), runtime-role
integration, and boundary preservation (no dependency, no provider token, no
local-live import, no semantic drift), plus the state-discipline records
(Phase 15A LOCKED; Phase 15B candidate / pending review / NOT locked; Phase
14E NOT STARTED and not opened; Phase 15C+ NOT STARTED).
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

from storytime.config import load_config
from storytime.runtime.boundary_readiness import (
    ALL_BOUNDARY_STATUSES,
    ALL_OVERALL_READINESS,
    ARTIFACT_BOUNDARY,
    OBSERVABILITY_BOUNDARY,
    QUEUE_BOUNDARY,
    RECOVERY_BOUNDARY,
    BoundaryReadinessSnapshot,
    BoundaryStatus,
    OverallReadiness,
    evaluate_boundary_readiness,
    parse_boundary_status,
)
from storytime.runtime.config import RUNTIME_ROLE_ENV, load_runtime_config
from storytime.runtime.roles import ALL_ROLES, RuntimeRole

_REPO_ROOT = Path(__file__).resolve().parent.parent
_DOCS = _REPO_ROOT / "docs"
_MODULE_PATH = _REPO_ROOT / "src" / "storytime" / "runtime" / "boundary_readiness.py"
_DESIGN_DOC = _DOCS / "phase15b-cloud-boundary-readiness.md"
_DEFERRED_DOC = _DOCS / "phase15b-deferred-cloud-work-register.md"

_STATE_DOCS = (
    _REPO_ROOT / "LLM_DIRECTOR.md",
    _DOCS / "handoff-state.md",
    _DOCS / "roadmap.md",
    _DOCS / "canonical-state.md",
    _DOCS / "phase-history.md",
)

# Top-level import roots the pure-data readiness module is allowed to use.
_ALLOWED_IMPORT_ROOTS = frozenset({"__future__", "dataclasses", "enum", "storytime"})

_EXPECTED_BOUNDARIES = {
    QUEUE_BOUNDARY,
    ARTIFACT_BOUNDARY,
    OBSERVABILITY_BOUNDARY,
    RECOVERY_BOUNDARY,
}

# Provider / library / infrastructure tokens that must never appear in the
# Phase 15B readiness module source (provider-neutral by construction).
_FORBIDDEN_MODULE_TOKENS = (
    "boto3",
    "redis",
    "celery",
    "kombu",
    "kafka",
    "rabbitmq",
    "temporal",
    "nats",
    "sqs",
    "minio",
    "kubernetes",
    "terraform",
    "helm",
    "datadog_api_key",
    "new_relic_license_key",
    "dynatrace_token",
    "otel_exporter_otlp_endpoint",
)

# Overclaim phrases that must never appear as active runtime claims.
_FORBIDDEN_OVERCLAIM_PHRASES = (
    "redis implemented",
    "sqs implemented",
    "nats implemented",
    "external broker implemented",
    "object storage implemented",
    "s3 adapter implemented",
    "distributed worker implemented",
    "cloud retry implemented",
    "dlq implemented",
    "collector deployed",
    "cloud deployment complete",
    "runs in the cloud",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _module_source() -> str:
    return _read(_MODULE_PATH)


def _imported_modules() -> set[str]:
    tree = ast.parse(_module_source())
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            modules.add(node.module)
    return modules


def _snapshot_for(value: str) -> BoundaryReadinessSnapshot:
    config = load_config({})
    runtime_config = load_runtime_config(config, {RUNTIME_ROLE_ENV: value})
    return evaluate_boundary_readiness(runtime_config, config)


def _blob(snapshot: BoundaryReadinessSnapshot) -> str:
    return json.dumps(snapshot.to_summary(), default=str, sort_keys=True).lower()


# ---------------------------------------------------------------------------
# Readiness model
# ---------------------------------------------------------------------------
class TestReadinessModel:
    def test_snapshot_is_pure_data_and_json_serializable(self) -> None:
        for role in ALL_ROLES:
            snapshot = _snapshot_for(role.value)
            summary = snapshot.to_summary()
            json.dumps(summary)  # must not raise
            assert summary["generated_for_runtime_role"] == role.value

    def test_snapshot_includes_four_boundaries(self) -> None:
        snapshot = _snapshot_for("combined")
        names = {b.boundary_name for b in snapshot.boundaries}
        assert names == _EXPECTED_BOUNDARIES
        assert len(snapshot.boundaries) == 4

    def test_status_vocabulary_is_closed(self) -> None:
        assert set(ALL_BOUNDARY_STATUSES) == set(BoundaryStatus)
        assert set(ALL_OVERALL_READINESS) == set(OverallReadiness)
        # The closed set is exactly these values — nothing cloud-certifying.
        assert {str(s) for s in BoundaryStatus} == {"local-active", "not-applicable"}
        assert {str(s) for s in OverallReadiness} == {"ready-for-local", "blocked"}

    def test_unknown_status_cannot_silently_pass(self) -> None:
        for bad in ("", "cloud-ready", "ready", "cloud_active", "unknown"):
            try:
                parse_boundary_status(bad)
            except ValueError:
                continue
            raise AssertionError(f"parse_boundary_status accepted {bad!r}")

    def test_active_and_deferred_are_distinguished(self) -> None:
        snapshot = _snapshot_for("combined")
        for boundary in snapshot.boundaries:
            # Active local capability is the status; future capability is listed
            # separately as deferred — the two are never conflated.
            assert boundary.status in (
                BoundaryStatus.LOCAL_ACTIVE,
                BoundaryStatus.NOT_APPLICABLE,
            )
            assert boundary.deferred_capabilities, (
                f"{boundary.boundary_name} lists no deferred capabilities"
            )
            for deferred in boundary.deferred_capabilities:
                assert "deferred" in deferred.lower()

    def test_forbidden_capabilities_not_presented_as_active(self) -> None:
        snapshot = _snapshot_for("combined")
        for boundary in snapshot.boundaries:
            # Every boundary's active backend is local / in-process, never a
            # cloud or distributed backend.
            active = boundary.active_backend.lower()
            assert "local" in active or "in-process" in active, (
                f"{boundary.boundary_name} active backend is not local/in-process"
            )
            assert boundary.explicit_non_goals, (
                f"{boundary.boundary_name} states no explicit non-goals"
            )


# ---------------------------------------------------------------------------
# Queue + worker boundary
# ---------------------------------------------------------------------------
class TestQueueBoundary:
    def test_only_local_queue_backend_is_active(self) -> None:
        worker = _snapshot_for("worker").queue
        assert worker.status is BoundaryStatus.LOCAL_ACTIVE
        assert "local" in worker.active_backend.lower()

    def test_external_broker_is_deferred(self) -> None:
        worker = _snapshot_for("worker").queue
        joined = " ".join(worker.deferred_capabilities).lower()
        assert "deferred" in joined
        assert "broker" in joined or "queue transport" in joined

    def test_api_role_does_not_drain_or_claim_queue(self) -> None:
        api = _snapshot_for("api").queue
        assert api.status is BoundaryStatus.NOT_APPLICABLE
        assert "does not" in api.active_backend.lower()

    def test_worker_readiness_does_not_change_queue_behavior(self) -> None:
        # The readiness module must not import or wrap the WorkQueue port.
        imported = _imported_modules()
        assert "storytime.local_live.queue" not in imported
        from storytime.local_live.queue import WorkQueue

        assert WorkQueue is not None


# ---------------------------------------------------------------------------
# Artifact + object-storage boundary
# ---------------------------------------------------------------------------
class TestArtifactBoundary:
    def test_only_local_artifact_backend_is_active(self) -> None:
        artifacts = _snapshot_for("combined").artifacts
        assert artifacts.status is BoundaryStatus.LOCAL_ACTIVE
        assert "local" in artifacts.active_backend.lower()

    def test_object_storage_and_signed_urls_deferred(self) -> None:
        artifacts = _snapshot_for("combined").artifacts
        joined = " ".join(artifacts.deferred_capabilities).lower()
        assert "object-storage" in joined or "object storage" in joined
        assert all("deferred" in d.lower() for d in artifacts.deferred_capabilities)

    def test_hash_envelope_source_of_truth_documented(self) -> None:
        artifacts = _snapshot_for("combined").artifacts
        guarantees = " ".join(artifacts.current_guarantees).lower()
        assert "sha-256" in guarantees or "digest" in guarantees
        assert "envelope" in guarantees
        assert "backend-owned" in artifacts.source_of_truth.lower()

    def test_artifact_boundary_does_not_wrap_store(self) -> None:
        imported = _imported_modules()
        assert "storytime.local_live.artifact_store" not in imported
        from storytime.local_live.artifact_store import ArtifactStore

        assert ArtifactStore is not None


# ---------------------------------------------------------------------------
# Observability export boundary
# ---------------------------------------------------------------------------
class TestObservabilityBoundary:
    def test_observability_remains_explanatory_not_source_of_truth(self) -> None:
        observability = _snapshot_for("combined").observability
        sot = observability.source_of_truth.lower()
        assert "durable backend state" in sot
        assert "explanatory" in sot or "not the source of truth" in sot

    def test_cloud_vendor_export_is_deferred(self) -> None:
        observability = _snapshot_for("combined").observability
        joined = " ".join(observability.deferred_capabilities).lower()
        assert "export" in joined
        assert all("deferred" in d.lower() for d in observability.deferred_capabilities)

    def test_no_observer_vocabulary_expansion(self) -> None:
        # The readiness module never imports the observability module, so it
        # cannot expand the QueueWorkerEvent schema; the contract still imports.
        imported = _imported_modules()
        assert "storytime.local_live.observability" not in imported
        from storytime.local_live.observability import QueueWorkerEvent

        assert QueueWorkerEvent is not None


# ---------------------------------------------------------------------------
# Recovery / idempotency boundary
# ---------------------------------------------------------------------------
class TestRecoveryBoundary:
    def test_recovery_source_of_truth_is_durable_backend_state(self) -> None:
        recovery = _snapshot_for("combined").recovery
        assert "durable backend state" in recovery.source_of_truth.lower()

    def test_distributed_safety_is_deferred(self) -> None:
        recovery = _snapshot_for("combined").recovery
        joined = " ".join(recovery.deferred_capabilities).lower()
        assert "idempotency" in joined
        assert "duplicate prevention" in joined or "coordination" in joined
        assert all("deferred" in d.lower() for d in recovery.deferred_capabilities)

    def test_recovery_eligibility_semantics_unchanged(self) -> None:
        # The module never imports recovery, so eligibility cannot drift; the
        # locked contract still imports cleanly.
        imported = _imported_modules()
        assert "storytime.local_live.recovery" not in imported
        from storytime.local_live.recovery import evaluate_recovery_eligibility

        assert callable(evaluate_recovery_eligibility)
        recovery = _snapshot_for("combined").recovery
        assert "backend-decided" in " ".join(recovery.current_guarantees).lower()


# ---------------------------------------------------------------------------
# Runtime role integration
# ---------------------------------------------------------------------------
class TestRuntimeRoleIntegration:
    def test_api_role_has_no_worker_claim_behavior(self) -> None:
        api = _snapshot_for("api")
        assert api.generated_for_runtime_role is RuntimeRole.API
        assert api.queue.status is BoundaryStatus.NOT_APPLICABLE

    def test_worker_role_has_queue_readiness_no_public_api(self) -> None:
        worker = _snapshot_for("worker")
        assert worker.queue.status is BoundaryStatus.LOCAL_ACTIVE
        # The readiness model binds no socket and exposes no API surface: it
        # imports neither the HTTP server nor any local-live runtime module.
        imported = _imported_modules()
        assert not any(m.startswith("storytime.local_live") for m in imported)
        assert "storytime.http.server" not in imported

    def test_combined_mode_is_local_and_non_supervisory(self) -> None:
        combined = _snapshot_for("combined")
        assert combined.generated_for_runtime_role is RuntimeRole.COMBINED
        assert combined.deployment == "local"
        # No supervisor / concurrency primitive is imported.
        imported = _imported_modules()
        for forbidden in ("multiprocessing", "threading", "asyncio", "subprocess", "socket"):
            assert forbidden not in imported


# ---------------------------------------------------------------------------
# Boundary preservation
# ---------------------------------------------------------------------------
class TestBoundaryPreservation:
    def test_no_new_dependency_in_module(self) -> None:
        roots = {m.split(".")[0] for m in _imported_modules()}
        unexpected = roots - _ALLOWED_IMPORT_ROOTS
        assert not unexpected, f"boundary module uses unexpected imports: {unexpected}"

    def test_module_imports_no_local_live(self) -> None:
        imported = _imported_modules()
        assert not any(m.startswith("storytime.local_live") for m in imported)

    def test_module_has_no_forbidden_provider_tokens(self) -> None:
        source = _module_source().lower()
        present = [tok for tok in _FORBIDDEN_MODULE_TOKENS if tok in source]
        assert not present, f"readiness module names forbidden tokens: {present}"

    def test_module_makes_no_overclaim(self) -> None:
        source = _module_source().lower()
        present = [p for p in _FORBIDDEN_OVERCLAIM_PHRASES if p in source]
        assert not present, f"readiness module overclaims: {present}"

    def test_summary_has_no_secrets_or_paths(self) -> None:
        config = load_config({})
        # The readiness model legitimately discusses the *absence* of secrets
        # (e.g. "no credential config"), so this scans for leaked secret
        # *values* / credential-name patterns and filesystem paths, not the
        # mere mention of the word "credential".
        leak_patterns = (
            "password",
            "api_key",
            "access_key",
            "secret_key",
            "_token",
            "authorization",
            "/home/",
            "/mnt/",
            str(config.state_db_path).lower(),
        )
        for role in ALL_ROLES:
            blob = _blob(_snapshot_for(role.value))
            for pattern in leak_patterns:
                assert pattern not in blob, f"summary leaked {pattern!r}"


# ---------------------------------------------------------------------------
# Phase-state discipline
# ---------------------------------------------------------------------------
class TestPhaseStateDiscipline:
    def test_phase_15a_is_locked(self) -> None:
        for doc in _STATE_DOCS:
            lowered = _read(doc).lower()
            lines = [ln for ln in lowered.splitlines() if "15a" in ln]
            assert lines, f"{doc.name} does not mention Phase 15A"
            assert any("locked" in ln for ln in lines), (
                f"{doc.name} no longer records Phase 15A as locked"
            )

    def test_phase_15b_is_candidate_not_locked(self) -> None:
        for doc in _STATE_DOCS:
            lowered = _read(doc).lower()
            assert "phase 15b" in lowered
            assert "not locked" in lowered
            assert "phase 15b is locked" not in lowered

    def test_phase_14e_not_started_and_not_opened(self) -> None:
        forbidden = ("phase 14e is locked", "phase 14e has started", "phase 14e is the current")
        for doc in _STATE_DOCS:
            lowered = _read(doc).lower()
            assert "phase 14e" in lowered
            assert "not started" in lowered
            for claim in forbidden:
                assert claim not in lowered, f"{doc.name} claims {claim!r}"

    def test_phase_15c_plus_remain_not_started(self) -> None:
        forbidden = (
            "phase 15c has started",
            "phase 15c is locked",
            "phase 15d has started",
            "phase 15d is locked",
            "phase 15e has started",
            "phase 15e is locked",
        )
        for doc in _STATE_DOCS:
            lowered = _read(doc).lower()
            for claim in forbidden:
                assert claim not in lowered, f"{doc.name} claims {claim!r}"

    def test_design_and_deferred_docs_exist(self) -> None:
        assert _DESIGN_DOC.is_file(), "phase15b design doc missing"
        assert _DEFERRED_DOC.is_file(), "phase15b deferred-work register missing"
        design = _read(_DESIGN_DOC).lower()
        for marker in (
            "purpose",
            "non-goals",
            "readiness model",
            "queue",
            "artifact",
            "observability",
            "recovery",
            "runtime-role",
            "configuration",
            "deferred",
            "phase 15c",
            "validation",
        ):
            assert marker in design, f"design doc missing section/marker {marker!r}"
