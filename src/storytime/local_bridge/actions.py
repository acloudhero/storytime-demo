"""Command-pattern router and action handlers (Phase 13G — runtime).

The router maps each allowlisted action name to **exactly one** pre-approved
handler (``docs/local-bridge-architecture.md`` §10). There is no generic
"run this" path: an action that is not on the allowlist never reaches a
handler — it is rejected during DTO validation, before routing.

Handlers in this phase:

- ``retry_failed_stage`` — the one action with **real execution behaviour**. It
  maps to the existing, locked, governed :func:`storytime.operator_rerun.perform_rerun`
  abstraction (Phase 10D), which performs a single bounded state reset of a
  *failed* run back to the resumable ``running`` state and writes one append-only
  audit event. It runs only against the bridge's explicitly-configured workspace
  (a temporary, isolated workspace in tests), never a real user workspace, never
  touching audio, network, providers, or the frontend export. It is naturally
  idempotent: a second retry of an already-reset run is reported honestly as
  not-retryable rather than re-executing.
- ``inspect_trust_envelope`` — validation-only (read-only inspection is deferred).
- ``refresh_export`` — accepted / not-implemented (the bridge does not write the
  export in this phase; faking success is explicitly forbidden).

A handler never accepts an arbitrary command, SQL string, or file path; the
only inputs are the typed, already-validated DTO fields.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from storytime.local_bridge.action_queue import STATE_COMPLETED, STATE_FAILED
from storytime.local_bridge.dto import ValidatedRequest
from storytime.operator_rerun import perform_rerun
from storytime.state import StateStore
from storytime.util.clock import Clock

# Actions that, when accepted, are dispatched asynchronously to the worker.
ASYNC_ACTIONS: frozenset[str] = frozenset({"retry_failed_stage"})

# Allowlisted actions that have no execution behaviour this phase. They return a
# synchronous validation-only / not-implemented response and are never enqueued.
SYNC_VALIDATION_ONLY_ACTIONS: frozenset[str] = frozenset({"inspect_trust_envelope"})
SYNC_NOT_IMPLEMENTED_ACTIONS: frozenset[str] = frozenset({"refresh_export"})


class WorkspaceMismatch(Exception):
    """Raised when a request targets a workspace the bridge is not bound to."""


@dataclass(frozen=True, slots=True)
class BridgeContext:
    """The bridge's bound execution context.

    ``workspace_id`` and ``workspace_root`` identify the single workspace the
    bridge may act on. The bridge fails closed if a request names a different
    workspace. ``db_path`` is the SQLite state store inside that workspace.
    """

    workspace_id: str
    workspace_root: Path
    clock: Clock

    @property
    def db_path(self) -> Path:
        return self.workspace_root / "state.db"


def _check_workspace(request: ValidatedRequest, ctx: BridgeContext) -> None:
    """Fail closed unless the request targets the bound workspace."""
    requested_id = str(request.workspace.get("id", ""))
    if requested_id != ctx.workspace_id:
        raise WorkspaceMismatch(
            f"request workspace id {requested_id!r} does not match the bound "
            f"workspace; refusing to act"
        )


def execute_retry_failed_stage(
    request: ValidatedRequest, ctx: BridgeContext
) -> dict[str, Any]:
    """Execute ``retry_failed_stage`` against the bound workspace.

    Maps to the governed Phase 10D re-run reset. Returns an honest result dict:
    ``status: "completed"`` only when the bounded state reset actually happened,
    ``status: "failed"`` otherwise (with the stable rerun decision code). This
    runs inside the worker thread, so it opens its own thread-local StateStore.
    """
    _check_workspace(request, ctx)

    run_id = str(request.target.get("runId", "")).strip()
    if not run_id:
        return {
            "status": STATE_FAILED,
            "code": "missing_run_id",
            "message": "retry_failed_stage requires target.runId.",
            "performed": False,
        }

    # Open a thread-local store inside the worker thread; SQLite connections are
    # thread-bound, so the store is created and closed here, not shared.
    with StateStore.open(ctx.db_path) as store:
        result = perform_rerun(store, ctx.clock, run_id)

    decision = result.decision
    if result.performed:
        return {
            "status": STATE_COMPLETED,
            "code": decision.code,
            "message": decision.message,
            "performed": True,
            "runId": run_id,
            "fromStage": decision.from_stage,
            "previousStatus": result.previous_status,
            "newStatus": result.new_status,
            "mutationId": result.mutation_id,
        }
    return {
        "status": STATE_FAILED,
        "code": decision.code,
        "message": decision.message,
        "performed": False,
        "runId": run_id,
    }


@dataclass(frozen=True, slots=True)
class RoutePlan:
    """The router's decision for a validated request.

    ``kind`` is one of ``"async"`` (enqueue + ``202 Accepted``), ``"sync"``
    (immediate validation-only / not-implemented response), or ``"reject"``.
    """

    kind: str
    not_implemented: bool = False
    warnings: tuple[str, ...] = ()


def plan_route(request: ValidatedRequest) -> RoutePlan:
    """Map a validated request to its routing decision.

    Validation has already proved the action is allowlisted, so this only needs
    to decide async-vs-sync and which synchronous shape applies.
    """
    if request.action in ASYNC_ACTIONS:
        return RoutePlan(
            kind="async",
            warnings=(
                "Acceptance is not success. Read final status from the action "
                "status endpoint keyed by actionRequestId.",
            ),
        )
    if request.action in SYNC_VALIDATION_ONLY_ACTIONS:
        return RoutePlan(
            kind="sync",
            not_implemented=False,
            warnings=(
                "Read-only inspection is validation-only in this phase; no "
                "inspection result is produced.",
            ),
        )
    if request.action in SYNC_NOT_IMPLEMENTED_ACTIONS:
        return RoutePlan(
            kind="sync",
            not_implemented=True,
            warnings=(
                "refresh_export is accepted-but-not-implemented this phase; the "
                "bridge does not write the export. Acceptance is not success.",
            ),
        )
    # Defensive: an allowlisted action with no route is a closed-fail reject.
    return RoutePlan(kind="reject")
