"""StoryTime blue/green front door (Phase 7B, Option B1).

A higher-assurance, still local and demo-grade blue/green entry point: a
single stable loopback address in front of the Phase 7A per-slot processes,
with an explicit, persisted *active-slot* pointer and a scripted switch /
rollback.

Front-door mechanism: a **native Python reverse proxy** (standard library
only) — deliberately not an external Caddy/nginx binary. This keeps
StoryTime's local-first, zero-external-dependency property intact, keeps the
front door fully covered by the normal test suite, and keeps it inside the
same ruff / mypy / import-linter discipline as the rest of the codebase. See
``docs/deployment-bluegreen-option-b.md`` for the rationale.

This package imports no ``opentelemetry``: the front door is outside the
pipeline telemetry path (pipeline telemetry attribution stays controlled by
each backend slot's own config — see ``docs/telemetry-map.md``).
"""

from __future__ import annotations

from storytime.frontdoor.active_slot import (
    DEFAULT_ACTIVE_SLOT_FILENAME,
    ActiveSlotError,
    ActiveSlotState,
    read_active_slot,
    write_active_slot,
)
from storytime.frontdoor.endpoints import SlotEndpoint, build_slot_endpoints
from storytime.frontdoor.proxy import FrontDoorHandler, FrontDoorServer
from storytime.frontdoor.switch import SwitchError, SwitchResult, switch_active_slot

__all__ = [
    "DEFAULT_ACTIVE_SLOT_FILENAME",
    "ActiveSlotError",
    "ActiveSlotState",
    "FrontDoorHandler",
    "FrontDoorServer",
    "SlotEndpoint",
    "SwitchError",
    "SwitchResult",
    "build_slot_endpoints",
    "read_active_slot",
    "switch_active_slot",
    "write_active_slot",
]
