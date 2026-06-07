"""Runtime configuration boundary for the local-first runtime skeleton.

ARCH-LOCK: Local-only deployment for Phase 15A
DO NOT REFACTOR: ``RuntimeConfig.deployment`` is fixed to ``"local"`` in this
phase. Phase 15A adds the *vocabulary* for a deployment dimension but binds it
to local only; ``STORYTIME_DEPLOYMENT`` is documented as DEFERRED and is NOT
read here. The only new environment variable Phase 15A reads is
``STORYTIME_RUNTIME_ROLE``. Everything else is derived from the already-proven,
immutable :class:`~storytime.config.StoryTimeConfig`, so this boundary adds no
new dependency and changes no existing behaviour.
Rationale: Phase 15A — Cloud Runtime Skeleton (local-first, reversible).
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from storytime.config import StoryTimeConfig
from storytime.runtime.roles import DEFAULT_RUNTIME_ROLE, RuntimeRole, parse_role

# The only deployment Phase 15A supports. The dimension exists so a later phase
# can extend it; here it is local-only and deliberately not environment-driven.
LOCAL_DEPLOYMENT = "local"

# The single new environment variable Phase 15A introduces.
RUNTIME_ROLE_ENV = "STORYTIME_RUNTIME_ROLE"


@dataclass(frozen=True, slots=True)
class RuntimeConfig:
    """Immutable runtime shape derived from the process configuration.

    Carries the resolved :class:`RuntimeRole`, a deployment label fixed to
    ``"local"`` for Phase 15A, and the environment / slot copied from the
    immutable :class:`~storytime.config.StoryTimeConfig` so the health model can
    report them without re-reading the environment. It is pure data:
    constructing it starts no worker, binds no socket, and touches no
    filesystem.
    """

    role: RuntimeRole
    deployment: str = LOCAL_DEPLOYMENT
    environment: str = "local"
    deployment_slot: str = ""


def load_runtime_config(
    config: StoryTimeConfig,
    environ: dict[str, str] | None = None,
) -> RuntimeConfig:
    """Build a :class:`RuntimeConfig` from *config* and *environ*.

    Reads ``STORYTIME_RUNTIME_ROLE`` only; an unset or empty value selects the
    default ``combined`` role so existing local behaviour is preserved exactly.
    A non-empty unrecognised value raises ValueError (via
    :func:`~storytime.runtime.roles.parse_role`) so misconfiguration fails fast.
    The deployment is fixed to ``"local"``; the environment and slot are taken
    from the immutable :class:`~storytime.config.StoryTimeConfig`.
    """
    env = dict(os.environ) if environ is None else environ
    raw_role = env.get(RUNTIME_ROLE_ENV, "").strip()
    role = parse_role(raw_role) if raw_role else DEFAULT_RUNTIME_ROLE
    return RuntimeConfig(
        role=role,
        deployment=LOCAL_DEPLOYMENT,
        environment=config.environment,
        deployment_slot=config.deployment_slot,
    )
