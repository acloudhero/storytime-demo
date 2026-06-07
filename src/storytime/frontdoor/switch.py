"""Active-slot switch / rollback logic.

A *switch* points the front door at a different slot by updating the
active-slot pointer (the single source of truth — see
``storytime.frontdoor.active_slot``). Because the native front door reads that
pointer on every request, the switch needs no proxy reload and no front-door
restart: updating the pointer file is the entire operation.

ARCH-LOCK: Switch never touches pipeline state
DO NOT REFACTOR: ``switch_active_slot`` writes ONLY the active-slot pointer
file. It must never read, write, move, or delete anything under ``runs/`` or
``feed/``. Switching and rolling back change *routing*, never *data*; the
inactive slot is preserved byte-for-byte, which is exactly what makes a
rollback a safe switch back to it.
Rationale: Phase 7B — honest, non-destructive blue/green; Phase 7A state and
feed separation must not be weakened.

Switch safety:

* the target slot must be a safe slot name (``is_valid_slot_name``);
* the target slot must actually exist — it must have a discoverable
  ``config/deploy/<slot>.env`` yielding a usable endpoint;
* "plausible endpoint" means *configured*, not *live*: the switch does not
  require the target slot's feed process to be running (switching to a
  not-yet-started candidate is legitimate). If the target is down, the front
  door answers an honest 502 until it is started — that is a separate,
  visible operator step.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from storytime.config import is_valid_slot_name
from storytime.frontdoor.active_slot import (
    ActiveSlotError,
    read_active_slot,
    write_active_slot,
)
from storytime.frontdoor.endpoints import SlotEndpoint, build_slot_endpoints


class SwitchError(ValueError):
    """Raised when an active-slot switch cannot be performed safely."""


@dataclass(frozen=True, slots=True)
class SwitchResult:
    """The outcome of an active-slot switch."""

    previous_slot: str | None
    new_slot: str
    active_slot_path: Path
    endpoint: SlotEndpoint
    unchanged: bool

    def describe(self) -> str:
        """A one-line, operator-facing description of exactly what changed."""
        if self.unchanged:
            return (
                f"active slot unchanged: already {self.new_slot!r} "
                f"({self.endpoint.address}); pointer {self.active_slot_path} "
                "re-affirmed"
            )
        previous = self.previous_slot if self.previous_slot is not None else "(unset)"
        return (
            f"active slot switched: {previous} -> {self.new_slot} "
            f"({self.endpoint.address}); pointer {self.active_slot_path} updated"
        )


def switch_active_slot(
    *,
    deploy_dir: Path,
    active_slot_path: Path,
    target_slot: str,
) -> SwitchResult:
    """Switch the front door's active slot to *target_slot*.

    Steps (all before any write):

    1. Validate *target_slot* is a safe slot name.
    2. Discover the configured slots from *deploy_dir*.
    3. Confirm *target_slot* has a configured, plausible endpoint.
    4. Read the current pointer (may be unset).
    5. Write *target_slot* to the pointer atomically.

    Rollback is this same function called with the previously-active slot as
    *target_slot* — there is no separate rollback path. The inactive slot's
    ``runs/`` and ``feed/`` roots are never touched.

    Raises ``SwitchError`` if the target slot is unsafe or not configured.
    """
    # 1. Safe slot name.
    if not is_valid_slot_name(target_slot):
        raise SwitchError(
            f"refusing to switch to unsafe slot value {target_slot!r} "
            f"(must match [a-z0-9][a-z0-9._-]* — no slashes, traversal, or "
            f"whitespace)"
        )

    # 2-3. The target must be a configured slot with a plausible endpoint.
    endpoints = build_slot_endpoints(deploy_dir)
    endpoint = endpoints.get(target_slot)
    if endpoint is None:
        known = ", ".join(sorted(endpoints)) or "(none)"
        raise SwitchError(
            f"slot {target_slot!r} is not configured: no usable "
            f"config/deploy/{target_slot}.env found under {deploy_dir} "
            f"(configured slots: {known})"
        )

    # 4. Current pointer — absent/invalid is fine; we are about to set it.
    try:
        previous_slot: str | None = read_active_slot(active_slot_path).slot
    except ActiveSlotError:
        previous_slot = None

    # 5. Write the new pointer atomically. Idempotent: re-affirming the same
    #    slot rewrites the pointer and reports unchanged.
    write_active_slot(active_slot_path, target_slot)

    return SwitchResult(
        previous_slot=previous_slot,
        new_slot=target_slot,
        active_slot_path=active_slot_path,
        endpoint=endpoint,
        unchanged=previous_slot == target_slot,
    )


__all__ = ["SwitchError", "SwitchResult", "switch_active_slot"]
