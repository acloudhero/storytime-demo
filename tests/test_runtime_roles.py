"""Phase 15A — Cloud Runtime Skeleton: runtime role / health guard tests.

These tests prove the smallest local-first, cloud-*shaped* runtime skeleton
without changing any locked Phase 14D behaviour. They cover the runtime role
vocabulary, the three roles (``api`` / ``worker`` / ``combined``), the
configuration-derived health / readiness model, the boundary-preservation
invariants (no new dependency, no observer-schema expansion, no WorkQueue /
ArtifactStore / recovery semantic drift), and the doc-state discipline (Phase
14D LOCKED, Phase 15A pending review / NOT locked, Phase 15B+ NOT STARTED).

The numbering in the comments tracks the Phase 15A testing requirements.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

from storytime.config import load_config
from storytime.runtime import (
    ALL_ROLES,
    API_BIND_HOST,
    DEFAULT_RUNTIME_ROLE,
    LOCAL_DEPLOYMENT,
    RUNTIME_ROLE_ENV,
    DependencyStatus,
    RuntimeHealth,
    RuntimeRole,
    api_bind_is_loopback,
    evaluate_runtime_health,
    load_runtime_config,
    parse_role,
    role_definition,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_RUNTIME_DIR = _REPO_ROOT / "src" / "storytime" / "runtime"
_DOCS = _REPO_ROOT / "docs"
_DESIGN_DOC = _DOCS / "phase15a-cloud-runtime-skeleton.md"

# Current-state living docs that record the active phase honestly.
_STATE_DOCS = (
    _REPO_ROOT / "LLM_DIRECTOR.md",
    _DOCS / "handoff-state.md",
    _DOCS / "roadmap.md",
    _DOCS / "canonical-state.md",
    _DOCS / "phase-history.md",
)

# Top-level import roots the pure-data runtime package is allowed to use.
# Everything here is the Python standard library plus first-party ``storytime``
# modules; anything else would be a new dependency.
_ALLOWED_IMPORT_ROOTS = frozenset({"__future__", "os", "dataclasses", "enum", "storytime"})

# The four backend-owned dependency descriptors the health model reports.
_EXPECTED_DEPENDENCIES = {"state_store", "work_queue", "artifact_store", "observer"}

# Tokens that must never appear in a health summary (secrets / credentials).
_SECRET_TOKENS = (
    "password",
    "secret",
    "credential",
    "api_key",
    "apikey",
    "access_key",
    "access-key",
    "private_key",
    "bearer",
)

# Cloud-provider configuration tokens for capability that does not exist yet.
_CLOUD_PROVIDER_TOKENS = (
    "aws",
    "gcp",
    "azure",
    "bucket",
    "access_key_id",
    "region=",
    "endpoint_url",
    "redis://",
    "amqp://",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _runtime_import_roots() -> set[str]:
    """Collect the top-level module roots imported anywhere in the package."""
    roots: set[str] = set()
    for source in sorted(_RUNTIME_DIR.glob("*.py")):
        tree = ast.parse(_read(source))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    roots.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                roots.add(node.module.split(".")[0])
    return roots


def _runtime_imported_modules() -> set[str]:
    """Collect the fully-qualified modules imported anywhere in the package."""
    modules: set[str] = set()
    for source in sorted(_RUNTIME_DIR.glob("*.py")):
        tree = ast.parse(_read(source))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    modules.add(alias.name)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                modules.add(node.module)
    return modules


def _summary_blob(health: RuntimeHealth) -> str:
    """A lowercased JSON serialisation of the health summary for scanning."""
    return json.dumps(health.to_summary(), default=str, sort_keys=True).lower()


# ---------------------------------------------------------------------------
# Runtime role vocabulary (requirements 1-4)
# ---------------------------------------------------------------------------
class TestRuntimeRoleVocabulary:
    def test_valid_roles_are_accepted(self) -> None:
        """1. Each valid role string parses to the matching enum member."""
        assert parse_role("api") is RuntimeRole.API
        assert parse_role("worker") is RuntimeRole.WORKER
        assert parse_role("combined") is RuntimeRole.COMBINED
        # Case-insensitive, mirroring fail-soft env parsing.
        assert parse_role("API") is RuntimeRole.API
        assert parse_role("Combined") is RuntimeRole.COMBINED

    def test_unknown_roles_are_rejected(self) -> None:
        """2. An unrecognised role fails fast rather than degrading silently."""
        for bad in ("", "primary", "leader", "cloud", "apiworker"):
            try:
                parse_role(bad)
            except ValueError:
                continue
            raise AssertionError(f"parse_role accepted invalid role {bad!r}")

    def test_default_preserves_current_local_behavior(self) -> None:
        """3. The default role is the proven local single-process shape."""
        assert DEFAULT_RUNTIME_ROLE is RuntimeRole.COMBINED
        config = load_config({})
        runtime_config = load_runtime_config(config, {})
        assert runtime_config.role is RuntimeRole.COMBINED
        # Combined both serves the read-model and drains the queue: exactly the
        # single-process local behaviour proven through Phase 14D.
        assert RuntimeRole.COMBINED.serves_api_by_default is True
        assert RuntimeRole.COMBINED.runs_worker_loop_by_default is True

    def test_role_labels_are_stable_and_documented(self) -> None:
        """4. Role string values are stable and every role has a definition."""
        assert RuntimeRole.API.value == "api"
        assert RuntimeRole.WORKER.value == "worker"
        assert RuntimeRole.COMBINED.value == "combined"
        assert set(ALL_ROLES) == set(RuntimeRole)
        for role in ALL_ROLES:
            definition = role_definition(role)
            assert definition.role is role
            assert definition.title.strip()
            assert definition.summary.strip()
        # "Documented" is concrete: the design doc names each role value.
        design = _read(_DESIGN_DOC).lower()
        for role in ALL_ROLES:
            assert f"`{role.value}`" in design, f"design doc omits role {role.value!r}"


# ---------------------------------------------------------------------------
# API runtime skeleton (requirements 5-8)
# ---------------------------------------------------------------------------
class TestApiRuntimeSkeleton:
    def _api_health(self) -> RuntimeHealth:
        config = load_config({})
        runtime_config = load_runtime_config(config, {RUNTIME_ROLE_ENV: "api"})
        return evaluate_runtime_health(runtime_config, config)

    def test_api_role_does_not_start_worker_by_default(self) -> None:
        """5. The API role does not run the worker loop by default."""
        assert RuntimeRole.API.runs_worker_loop_by_default is False
        assert self._api_health().runs_worker_loop is False

    def test_api_role_keeps_loopback_only(self) -> None:
        """6. The API role reuses the locked loopback-only bind guard."""
        assert API_BIND_HOST == "127.0.0.1"
        assert api_bind_is_loopback() is True
        # A non-loopback host is reported as not-loopback rather than accepted.
        assert api_bind_is_loopback("0.0.0.0") is False
        assert api_bind_is_loopback("::") is False

    def test_api_role_adds_no_public_ingress(self) -> None:
        """7. The API role declares no public ingress (and no wildcard CORS)."""
        health = self._api_health()
        assert health.allows_public_ingress is False
        assert health.allows_wildcard_cors is False

    def test_api_role_health_is_backend_owned(self) -> None:
        """8. API readiness derives from backend-owned dependencies only; the
        api node does not own queue draining (work_queue is not-applicable)."""
        health = self._api_health()
        statuses = {dep.name: dep.status for dep in health.dependencies}
        assert set(statuses) == _EXPECTED_DEPENDENCIES
        assert statuses["work_queue"] is DependencyStatus.NOT_APPLICABLE
        assert statuses["state_store"] is DependencyStatus.CONFIGURED
        assert statuses["artifact_store"] is DependencyStatus.CONFIGURED
        assert statuses["observer"] is DependencyStatus.CONFIGURED
        assert health.ready is True
        assert health.status == "ok"


# ---------------------------------------------------------------------------
# Worker runtime skeleton (requirements 9-12)
# ---------------------------------------------------------------------------
class TestWorkerRuntimeSkeleton:
    def _worker_health(self) -> RuntimeHealth:
        config = load_config({})
        runtime_config = load_runtime_config(config, {RUNTIME_ROLE_ENV: "worker"})
        return evaluate_runtime_health(runtime_config, config)

    def test_worker_role_exposes_no_public_api(self) -> None:
        """9. The worker role does not serve the API by default."""
        assert RuntimeRole.WORKER.serves_api_by_default is False
        assert self._worker_health().serves_api is False

    def test_worker_role_uses_existing_queue_worker_contracts(self) -> None:
        """10. The worker role drains the existing local queue (configured),
        and its descriptor names the proven WorkQueue / local worker."""
        health = self._worker_health()
        queue = next(dep for dep in health.dependencies if dep.name == "work_queue")
        assert queue.status is DependencyStatus.CONFIGURED
        assert "workqueue" in queue.detail.lower()
        assert "local worker" in queue.detail.lower()

    def test_worker_role_adds_no_external_broker(self) -> None:
        """11. No external broker appears in the worker dependencies or summary."""
        health = self._worker_health()
        names = {dep.name for dep in health.dependencies}
        assert set(names) == _EXPECTED_DEPENDENCIES  # no "broker"/"redis"/...
        blob = _summary_blob(health)
        for token in ("redis", "nats", "sqs", "temporal", "celery", "kafka", "rabbitmq"):
            assert token not in blob, f"worker summary leaked broker token {token!r}"

    def test_worker_role_does_not_touch_recovery_semantics(self) -> None:
        """12. The runtime package neither imports nor reimplements recovery;
        the health model reports no recovery dependency, so eligibility
        semantics are untouched. The locked contract still imports cleanly."""
        imported = _runtime_imported_modules()
        assert "storytime.local_live.recovery" not in imported
        names = {dep.name for dep in self._worker_health().dependencies}
        assert "recovery" not in names
        # The locked recovery contract is still importable and unchanged.
        from storytime.local_live.recovery import evaluate_recovery_eligibility

        assert callable(evaluate_recovery_eligibility)


# ---------------------------------------------------------------------------
# Combined runtime mode (requirements 13-14)
# ---------------------------------------------------------------------------
class TestCombinedRuntimeMode:
    def _combined_health(self) -> RuntimeHealth:
        config = load_config({})
        runtime_config = load_runtime_config(config, {RUNTIME_ROLE_ENV: "combined"})
        return evaluate_runtime_health(runtime_config, config)

    def test_combined_preserves_local_dev_behavior(self) -> None:
        """13. Combined both serves the read-model and drains the queue, and
        every dependency is configured: the proven local/dev behaviour."""
        health = self._combined_health()
        assert health.serves_api is True
        assert health.runs_worker_loop is True
        statuses = {dep.name: dep.status for dep in health.dependencies}
        assert set(statuses) == _EXPECTED_DEPENDENCIES
        assert all(status is DependencyStatus.CONFIGURED for status in statuses.values())
        assert health.ready is True

    def test_combined_does_not_imply_production_cloud(self) -> None:
        """14. Combined is a local shape: deployment is local, with no public
        ingress and no wildcard CORS."""
        health = self._combined_health()
        assert health.deployment == LOCAL_DEPLOYMENT == "local"
        assert health.allows_public_ingress is False
        assert health.allows_wildcard_cors is False


# ---------------------------------------------------------------------------
# Health / readiness (requirements 15-18)
# ---------------------------------------------------------------------------
class TestHealthReadiness:
    def _health_for(self, value: str) -> RuntimeHealth:
        config = load_config({})
        runtime_config = load_runtime_config(config, {RUNTIME_ROLE_ENV: value})
        return evaluate_runtime_health(runtime_config, config)

    def test_health_includes_runtime_role(self) -> None:
        """15. The health model and its summary carry the runtime role."""
        for role in ALL_ROLES:
            health = self._health_for(role.value)
            assert health.runtime_role is role
            assert health.to_summary()["runtime_role"] == role.value

    def test_health_includes_four_backend_statuses(self) -> None:
        """16. State-store, queue, artifact, and observer statuses are present."""
        for role in ALL_ROLES:
            health = self._health_for(role.value)
            names = {dep.name for dep in health.dependencies}
            assert names == _EXPECTED_DEPENDENCIES
            for dep in health.dependencies:
                assert isinstance(dep.status, DependencyStatus)

    def test_health_excludes_secrets_and_paths(self) -> None:
        """17. The summary exposes no secret, credential, or filesystem path."""
        config = load_config({})
        for role in ALL_ROLES:
            health = self._health_for(role.value)
            blob = _summary_blob(health)
            for token in _SECRET_TOKENS:
                assert token not in blob, f"summary leaked secret token {token!r}"
            # The durable state path is backend-owned and must not leak.
            assert str(config.state_db_path).lower() not in blob

    def test_health_excludes_nonexistent_cloud_provider_config(self) -> None:
        """18. The summary carries no cloud-provider config that does not exist;
        the only deployment value is the local one."""
        for role in ALL_ROLES:
            health = self._health_for(role.value)
            assert health.deployment == "local"
            blob = _summary_blob(health)
            for token in _CLOUD_PROVIDER_TOKENS:
                assert token not in blob, f"summary leaked cloud token {token!r}"


# ---------------------------------------------------------------------------
# Boundary preservation (requirements 19-24)
# ---------------------------------------------------------------------------
class TestBoundaryPreservation:
    def test_no_dependency_additions(self) -> None:
        """19. The package imports only stdlib + first-party storytime modules."""
        unexpected = _runtime_import_roots() - _ALLOWED_IMPORT_ROOTS
        assert not unexpected, f"runtime package uses unexpected imports: {unexpected}"

    def test_no_frontend_behavior_change(self) -> None:
        """20. The package is Python-only and imports no frontend/bridge module."""
        non_python = [p.name for p in _RUNTIME_DIR.iterdir() if p.is_file() and p.suffix != ".py"]
        assert not non_python, f"runtime package has non-Python files: {non_python}"
        for module in _runtime_imported_modules():
            lowered = module.lower()
            assert "frontend" not in lowered
            assert "bridge" not in lowered

    def test_no_observer_event_schema_expansion(self) -> None:
        """21. The package never imports the observability module, so it cannot
        expand the QueueWorkerEvent schema; the contract still imports."""
        imported = _runtime_imported_modules()
        assert "storytime.local_live.observability" not in imported
        from storytime.local_live.observability import QueueWorkerEvent

        assert QueueWorkerEvent is not None

    def test_no_workqueue_semantic_drift(self) -> None:
        """22. The package does not import or wrap the WorkQueue port."""
        imported = _runtime_imported_modules()
        assert "storytime.local_live.queue" not in imported
        from storytime.local_live.queue import WorkQueue

        assert WorkQueue is not None

    def test_no_artifact_store_semantic_drift(self) -> None:
        """23. The package does not import or wrap the ArtifactStore port."""
        imported = _runtime_imported_modules()
        assert "storytime.local_live.artifact_store" not in imported
        from storytime.local_live.artifact_store import ArtifactStore

        assert ArtifactStore is not None

    def test_no_recovery_eligibility_semantic_drift(self) -> None:
        """24. The package does not import recovery; eligibility is untouched."""
        imported = _runtime_imported_modules()
        assert not any(m.startswith("storytime.local_live") for m in imported), (
            f"runtime imports a local_live module: "
            f"{sorted(m for m in imported if m.startswith('storytime.local_live'))}"
        )


# ---------------------------------------------------------------------------
# Phase-state discipline (requirements 25-27)
# ---------------------------------------------------------------------------
class TestPhaseStateDiscipline:
    def test_phase_15b_plus_remain_not_started(self) -> None:
        """25. The living state docs frame Phase 15B-15E as NOT STARTED and
        never claim any of them started or locked."""
        forbidden = (
            "phase 15b has started",
            "phase 15b is locked",
            "phase 15c has started",
            "phase 15c is locked",
            "phase 15d has started",
            "phase 15d is locked",
            "phase 15e has started",
            "phase 15e is locked",
        )
        for doc in _STATE_DOCS:
            lowered = _read(doc).lower()
            assert "not started" in lowered
            for claim in forbidden:
                assert claim not in lowered, f"{doc.name} claims {claim!r}"

    def test_phase_14d_remains_locked(self) -> None:
        """26. Phase 14D is still recorded as the locked phase, and no premature
        Phase 14/15 closure or lock is claimed."""
        for doc in _STATE_DOCS:
            lowered = _read(doc).lower()
            assert "phase 14d" in lowered
            assert "locked" in lowered
            assert "phase 14 is locked" not in lowered
            assert "phase 15 is locked" not in lowered

    def test_phase_15a_is_pending_not_locked(self) -> None:
        """27. Phase 15A is recorded as the current candidate, pending review and
        NOT locked, never as locked."""
        for doc in _STATE_DOCS:
            lowered = _read(doc).lower()
            assert "phase 15a" in lowered
            assert "not locked" in lowered
            assert "phase 15a is locked" not in lowered

    def test_design_doc_exists_and_covers_required_sections(self) -> None:
        """Light existence / content check of the Phase 15A design document."""
        assert _DESIGN_DOC.is_file()
        lowered = _read(_DESIGN_DOC).lower()
        for marker in (
            "purpose",
            "non-goals",
            "runtime role",
            "health",
            "readiness",
            "configuration boundary",
            "deferred",
            "phase 15b",
            "validation",
            "storytime_runtime_role",
        ):
            assert marker in lowered, f"design doc missing section/marker {marker!r}"
        # The deployment dimension is documented as DEFERRED, not active config.
        assert "storytime_deployment" in lowered
