"""Runtime role vocabulary for the local-first, cloud-shaped runtime skeleton.

ARCH-LOCK: Local-first runtime roles (Phase 15A)
DO NOT REFACTOR: The three runtime roles — ``api``, ``worker``, and
``combined`` — describe how a single LOCAL process is *shaped*, not a cloud
deployment. ``combined`` is the default so the proven local behaviour (one
process that both serves the loopback read-model and drains the local work
queue) is preserved exactly. These roles add no external broker, no
distributed worker, no public ingress, and no new dependency; they only name a
separation that already exists in the LOCKED local contracts so a later phase
could split them without re-litigating the boundary.
Rationale: Phase 15A — Cloud Runtime Skeleton (local-first, reversible).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RuntimeRole(StrEnum):
    """A local runtime role: how one process is shaped, not where it runs."""

    API = "api"
    WORKER = "worker"
    COMBINED = "combined"

    @property
    def serves_api_by_default(self) -> bool:
        """True if the role serves the loopback operator read-model by default."""
        return self in (RuntimeRole.API, RuntimeRole.COMBINED)

    @property
    def runs_worker_loop_by_default(self) -> bool:
        """True if the role drains the local work queue by default."""
        return self in (RuntimeRole.WORKER, RuntimeRole.COMBINED)


# ``combined`` preserves the proven local single-process behaviour, so it is
# the default whenever STORYTIME_RUNTIME_ROLE is unset or empty.
DEFAULT_RUNTIME_ROLE = RuntimeRole.COMBINED

# Every role, in declaration order, for enumeration in tests and documentation.
ALL_ROLES: tuple[RuntimeRole, ...] = tuple(RuntimeRole)


@dataclass(frozen=True, slots=True)
class RoleDefinition:
    """An immutable, human-facing description of a runtime role.

    Pure data derived from the role alone: it instantiates nothing, binds
    nothing, and starts no worker. It exists so the health model and the
    documentation can describe each role's intent by name without wiring any
    component.
    """

    role: RuntimeRole
    title: str
    serves_api: bool
    runs_worker_loop: bool
    summary: str


_ROLE_DEFINITIONS: dict[RuntimeRole, RoleDefinition] = {
    RuntimeRole.API: RoleDefinition(
        role=RuntimeRole.API,
        title="API",
        serves_api=True,
        runs_worker_loop=False,
        summary=(
            "Serves the loopback operator read-model only. It does not drain "
            "the local work queue by default and binds no public interface."
        ),
    ),
    RuntimeRole.WORKER: RoleDefinition(
        role=RuntimeRole.WORKER,
        title="worker",
        serves_api=False,
        runs_worker_loop=True,
        summary=(
            "Drains the existing local durable work queue and executes the "
            "proven pipeline. It serves no public API and adds no broker."
        ),
    ),
    RuntimeRole.COMBINED: RoleDefinition(
        role=RuntimeRole.COMBINED,
        title="combined",
        serves_api=True,
        runs_worker_loop=True,
        summary=(
            "One local process that both serves the loopback read-model and "
            "drains the local work queue — the proven local default."
        ),
    ),
}


def role_definition(role: RuntimeRole) -> RoleDefinition:
    """Return the immutable :class:`RoleDefinition` for *role*."""
    return _ROLE_DEFINITIONS[role]


def parse_role(value: str) -> RuntimeRole:
    """Return the :class:`RuntimeRole` named by *value* (case-insensitive).

    Raises ValueError on an unrecognised value so a misconfigured
    ``STORYTIME_RUNTIME_ROLE`` fails fast at startup rather than silently
    falling back to a default.
    """
    normalized = value.strip().lower()
    try:
        return RuntimeRole(normalized)
    except ValueError:
        valid = ", ".join(role.value for role in RuntimeRole)
        raise ValueError(
            f"unknown runtime role {value!r}; valid roles are: {valid}"
        ) from None
