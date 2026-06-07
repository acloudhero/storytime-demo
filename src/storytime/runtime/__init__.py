"""Local-first, cloud-shaped runtime skeleton (Phase 15A).

This package adds runtime ROLE separation (api / worker / combined), a
configuration-derived health and readiness model, and a runtime configuration
boundary on top of the proven, LOCKED Phase 14D local contracts. It implements
no cloud behaviour: no external broker, no distributed worker, no object
storage, no authentication, no public ingress, and no new dependency. Every
type here is pure data derived from the immutable
:class:`~storytime.config.StoryTimeConfig`; importing or constructing them
starts no worker and binds no socket.

Phase 15B adds, additively, a pure-data cloud boundary-readiness model
(:mod:`storytime.runtime.boundary_readiness`) describing four cloud-growth
seams — queue/worker, artifact/storage, observability/export, and
recovery/idempotency — without implementing any cloud behaviour or changing
any existing contract.
"""

from __future__ import annotations

from storytime.runtime.boundary_readiness import (
    ALL_BOUNDARY_STATUSES,
    ALL_OVERALL_READINESS,
    BoundaryReadinessSnapshot,
    BoundaryStatus,
    BoundarySummary,
    OverallReadiness,
    evaluate_boundary_readiness,
    parse_boundary_status,
)
from storytime.runtime.config import (
    LOCAL_DEPLOYMENT,
    RUNTIME_ROLE_ENV,
    RuntimeConfig,
    load_runtime_config,
)
from storytime.runtime.health import (
    API_BIND_HOST,
    DependencyStatus,
    RuntimeDependency,
    RuntimeHealth,
    api_bind_is_loopback,
    evaluate_runtime_health,
)
from storytime.runtime.roles import (
    ALL_ROLES,
    DEFAULT_RUNTIME_ROLE,
    RoleDefinition,
    RuntimeRole,
    parse_role,
    role_definition,
)

__all__ = [
    "ALL_BOUNDARY_STATUSES",
    "ALL_OVERALL_READINESS",
    "ALL_ROLES",
    "API_BIND_HOST",
    "BoundaryReadinessSnapshot",
    "BoundaryStatus",
    "BoundarySummary",
    "DEFAULT_RUNTIME_ROLE",
    "DependencyStatus",
    "LOCAL_DEPLOYMENT",
    "OverallReadiness",
    "RUNTIME_ROLE_ENV",
    "RoleDefinition",
    "RuntimeConfig",
    "RuntimeDependency",
    "RuntimeHealth",
    "RuntimeRole",
    "api_bind_is_loopback",
    "evaluate_boundary_readiness",
    "evaluate_runtime_health",
    "load_runtime_config",
    "parse_boundary_status",
    "parse_role",
    "role_definition",
]
