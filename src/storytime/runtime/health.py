"""Configuration-derived health and readiness model for the runtime skeleton.

ARCH-LOCK: Pure, configuration-derived health (Phase 15A)
DO NOT REFACTOR: :func:`evaluate_runtime_health` is pure and side-effect-free.
It derives a description of the runtime from the immutable config and the
runtime role alone — it instantiates no worker, queue, or artifact store, binds
no socket, opens no database, and wraps nothing. The dependency descriptors
name the proven LOCAL contracts (``StateStore``, ``SqliteWorkQueue``,
``LocalFilesystemArtifactStore``, the in-process observer) by name; they are
documentation, not adapters. The API role reuses the LOCKED loopback bind guard
(:func:`~storytime.http.server.validate_bind_host`) rather than introducing a
new bind. ``to_summary`` exposes no secrets, credentials, or filesystem paths.
Rationale: Phase 15A — Cloud Runtime Skeleton (local-first, reversible).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from storytime.config import StoryTimeConfig
from storytime.http.server import UnsafeBindError, validate_bind_host
from storytime.runtime.config import RuntimeConfig
from storytime.runtime.roles import RuntimeRole

# The API role binds the same loopback host the LOCKED HTTP server enforces.
# It is reused, not redefined: api_bind_is_loopback delegates to the existing
# validate_bind_host guard so the loopback-only contract has a single source.
API_BIND_HOST = "127.0.0.1"


class DependencyStatus(StrEnum):
    """Whether a local dependency is configured for, or not used by, a role.

    Phase 15A is local-first, so a dependency is either ``configured`` (present
    and used by the role) or ``not-applicable`` (the role does not use it by
    default — for example the API role does not drain the work queue). There is
    deliberately no live-probe status: readiness here is configuration-level,
    not a liveness check.
    """

    CONFIGURED = "configured"
    NOT_APPLICABLE = "not-applicable"


@dataclass(frozen=True, slots=True)
class RuntimeDependency:
    """An immutable description of one local dependency for a runtime role.

    ``detail`` names the proven local contract and how the role relates to it.
    It never contains a filesystem path, secret, or credential.
    """

    name: str
    status: DependencyStatus
    detail: str


@dataclass(frozen=True, slots=True)
class RuntimeHealth:
    """An immutable, configuration-derived health/readiness description.

    Pure data: it is produced by :func:`evaluate_runtime_health` from the
    config and role and reflects no live process state. ``ready`` and
    ``status`` are derived; ``to_summary`` renders a safe, secret-free mapping
    suitable for logging or a future read-only endpoint.
    """

    runtime_role: RuntimeRole
    deployment: str
    environment: str
    slot: str
    serves_api: bool
    runs_worker_loop: bool
    allows_public_ingress: bool
    allows_wildcard_cors: bool
    dependencies: tuple[RuntimeDependency, ...]
    warnings: tuple[str, ...] = field(default=())

    @property
    def ready(self) -> bool:
        """True when the runtime is configuration-ready.

        Every dependency must be either configured or explicitly
        not-applicable, the runtime must allow neither public ingress nor
        wildcard CORS (the LOCKED local contract), and no warnings may have
        been raised. A future MISSING dependency status would flip this to
        False without changing the readiness rule.
        """
        dependencies_ready = all(
            dep.status in (DependencyStatus.CONFIGURED, DependencyStatus.NOT_APPLICABLE)
            for dep in self.dependencies
        )
        ingress_safe = not self.allows_public_ingress and not self.allows_wildcard_cors
        return dependencies_ready and ingress_safe and not self.warnings

    @property
    def status(self) -> str:
        """``"ok"`` when :attr:`ready`, otherwise ``"degraded"``."""
        return "ok" if self.ready else "degraded"

    def to_summary(self) -> dict[str, object]:
        """Return a safe, JSON-friendly summary with no secrets or paths."""
        return {
            "runtime_role": str(self.runtime_role),
            "deployment": self.deployment,
            "environment": self.environment,
            "slot": self.slot,
            "serves_api": self.serves_api,
            "runs_worker_loop": self.runs_worker_loop,
            "allows_public_ingress": self.allows_public_ingress,
            "allows_wildcard_cors": self.allows_wildcard_cors,
            "ready": self.ready,
            "status": self.status,
            "dependencies": [
                {
                    "name": dep.name,
                    "status": str(dep.status),
                    "detail": dep.detail,
                }
                for dep in self.dependencies
            ],
            "warnings": list(self.warnings),
        }


def api_bind_is_loopback(host: str = API_BIND_HOST) -> bool:
    """True if *host* is a loopback bind accepted by the LOCKED HTTP guard.

    Delegates to :func:`~storytime.http.server.validate_bind_host` so the API
    role inherits the same loopback-only contract and introduces no new bind
    path. Returns False (rather than raising) for an unsafe host so callers can
    treat it as a boolean readiness signal.
    """
    try:
        validate_bind_host(host)
    except UnsafeBindError:
        return False
    return True


def _dependencies_for(
    role: RuntimeRole,
    config: StoryTimeConfig,
) -> tuple[RuntimeDependency, ...]:
    """Return the four local dependency descriptors for *role*.

    The descriptors are derived from the role and the telemetry mode only. No
    component is instantiated, probed, or wrapped, and no filesystem path is
    included.
    """
    serves_api = role.serves_api_by_default
    runs_worker = role.runs_worker_loop_by_default

    if runs_worker and serves_api:
        state_detail = (
            "Backend-owned SQLite state store (StateStore): read for the "
            "operator read-model and updated as the pipeline executes; the "
            "durable source of truth."
        )
    elif runs_worker:
        state_detail = (
            "Backend-owned SQLite state store (StateStore): claimed and "
            "updated as the pipeline executes; the durable source of truth."
        )
    else:
        state_detail = (
            "Backend-owned SQLite state store (StateStore): read for the "
            "operator read-model; the durable source of truth."
        )

    if runs_worker:
        queue = RuntimeDependency(
            name="work_queue",
            status=DependencyStatus.CONFIGURED,
            detail=(
                "Local durable work queue (SqliteWorkQueue) behind the "
                "WorkQueue port, drained by the in-process local worker. No "
                "external broker and no distributed worker."
            ),
        )
    else:
        queue = RuntimeDependency(
            name="work_queue",
            status=DependencyStatus.NOT_APPLICABLE,
            detail=(
                "Local durable work queue (SqliteWorkQueue) behind the "
                "WorkQueue port; the api role does not drain it by default."
            ),
        )

    if runs_worker and serves_api:
        artifact_detail = (
            "Local filesystem artifact store (LocalFilesystemArtifactStore) "
            "behind the ArtifactStore port: written by the worker and surfaced "
            "read-only by the read-model. No object storage and no signed URLs."
        )
    elif runs_worker:
        artifact_detail = (
            "Local filesystem artifact store (LocalFilesystemArtifactStore) "
            "behind the ArtifactStore port, written as the pipeline executes. "
            "No object storage and no signed URLs."
        )
    else:
        artifact_detail = (
            "Local filesystem artifact store (LocalFilesystemArtifactStore) "
            "behind the ArtifactStore port, surfaced read-only by the "
            "read-model. No object storage and no signed URLs."
        )

    observer_detail = (
        "In-process, fail-soft queue/worker observation (QueueWorkerEvent); "
        f"telemetry export mode is {config.telemetry!r}. No collector, no "
        "dashboards, and no distributed tracing."
    )

    return (
        RuntimeDependency(
            name="state_store",
            status=DependencyStatus.CONFIGURED,
            detail=state_detail,
        ),
        queue,
        RuntimeDependency(
            name="artifact_store",
            status=DependencyStatus.CONFIGURED,
            detail=artifact_detail,
        ),
        RuntimeDependency(
            name="observer",
            status=DependencyStatus.CONFIGURED,
            detail=observer_detail,
        ),
    )


def evaluate_runtime_health(
    runtime_config: RuntimeConfig,
    config: StoryTimeConfig,
) -> RuntimeHealth:
    """Return a pure, configuration-derived :class:`RuntimeHealth`.

    Side-effect-free: it derives every field from *runtime_config* and *config*
    and the role's default behaviour. It starts no worker, binds no socket, and
    opens no database. Public ingress and wildcard CORS are always disallowed —
    the LOCKED local-live contract — so a healthy local runtime is also a safe
    one.
    """
    role = runtime_config.role
    return RuntimeHealth(
        runtime_role=role,
        deployment=runtime_config.deployment,
        environment=runtime_config.environment,
        slot=runtime_config.deployment_slot,
        serves_api=role.serves_api_by_default,
        runs_worker_loop=role.runs_worker_loop_by_default,
        allows_public_ingress=False,
        allows_wildcard_cors=False,
        dependencies=_dependencies_for(role, config),
        warnings=(),
    )
