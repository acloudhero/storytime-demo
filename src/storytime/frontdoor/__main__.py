"""``python -m storytime.frontdoor`` — run / switch / inspect the front door.

CLI-adjacent on purpose: like ``python -m storytime.demo``, this is a
deployment/demo tool kept out of the locked ``storytime`` command surface
(Architecture Baseline section 4). The launcher scripts ``run-frontdoor.sh``
and ``switch-slot.sh`` wrap it.

Subcommands::

    python -m storytime.frontdoor serve   [--host H] [--port P] [--deploy-dir D]
                                          [--active-slot-file F]
    python -m storytime.frontdoor switch  <blue|green> [--deploy-dir D]
                                          [--active-slot-file F]
    python -m storytime.frontdoor status  [--deploy-dir D] [--active-slot-file F]

Paths default relative to the current directory (run from the repository
root, as the launcher scripts ensure): ``config/deploy`` and
``config/deploy/active-slot``.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from storytime.frontdoor.active_slot import (
    DEFAULT_ACTIVE_SLOT_FILENAME,
    ActiveSlotError,
    read_active_slot,
)
from storytime.frontdoor.endpoints import SlotEndpointError, build_slot_endpoints
from storytime.frontdoor.proxy import FrontDoorServer
from storytime.frontdoor.switch import SwitchError, switch_active_slot
from storytime.http import UnsafeBindError

_DEFAULT_DEPLOY_DIR = Path("config/deploy")
_DEFAULT_FRONT_DOOR_HOST = "127.0.0.1"
_DEFAULT_FRONT_DOOR_PORT = 8080


def _add_path_args(parser: argparse.ArgumentParser) -> None:
    """Add the shared --deploy-dir / --active-slot-file options."""
    parser.add_argument(
        "--deploy-dir",
        type=Path,
        default=_DEFAULT_DEPLOY_DIR,
        help="Directory of per-slot env files. Default: config/deploy",
    )
    parser.add_argument(
        "--active-slot-file",
        type=Path,
        default=None,
        help="Active-slot pointer file. Default: <deploy-dir>/active-slot",
    )


def _resolve_active_slot_path(args: argparse.Namespace) -> Path:
    """The active-slot pointer path: explicit, or <deploy-dir>/active-slot."""
    if args.active_slot_file is not None:
        path: Path = args.active_slot_file
        return path
    deploy_dir: Path = args.deploy_dir
    return deploy_dir / DEFAULT_ACTIVE_SLOT_FILENAME


def _cmd_serve(args: argparse.Namespace) -> int:
    """Run the front-door reverse proxy. Blocks until interrupted."""
    active_slot_path = _resolve_active_slot_path(args)
    try:
        endpoints = build_slot_endpoints(args.deploy_dir)
    except (OSError, SlotEndpointError, UnsafeBindError) as exc:
        print(f"front door: cannot start — {exc}", file=sys.stderr)
        return 2
    if not endpoints:
        print(
            f"front door: no slots configured under {args.deploy_dir} "
            "(expected config/deploy/<slot>.env files)",
            file=sys.stderr,
        )
        return 2
    try:
        server = FrontDoorServer(
            host=args.host,
            port=args.port,
            slot_endpoints=endpoints,
            active_slot_path=active_slot_path,
        )
    except UnsafeBindError as exc:
        print(f"front door: refusing to start — {exc}", file=sys.stderr)
        return 2

    known = ", ".join(
        f"{e.slot}->{e.address}" for e in sorted(endpoints.values(), key=lambda e: e.slot)
    )
    print(
        f"StoryTime front door on http://{server.bind_host}:{args.port}/  "
        f"(slots: {known})"
    )
    try:
        active = read_active_slot(active_slot_path).slot
        print(f"  active slot: {active}  (pointer: {active_slot_path})")
    except ActiveSlotError as exc:
        print(f"  active slot: UNSET/INVALID — requests will 503 until fixed ({exc})")
    print("  press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:  # pragma: no cover - interactive stop
        print("\nfront door stopped.")
    return 0


def _cmd_switch(args: argparse.Namespace) -> int:
    """Switch the active slot. Rollback is this command targeting the old slot."""
    active_slot_path = _resolve_active_slot_path(args)
    try:
        result = switch_active_slot(
            deploy_dir=args.deploy_dir,
            active_slot_path=active_slot_path,
            target_slot=args.slot,
        )
    except (SwitchError, ActiveSlotError, OSError, SlotEndpointError, UnsafeBindError) as exc:
        print(f"switch failed: {exc}", file=sys.stderr)
        return 1
    print(result.describe())
    print(
        "  the front door reads the pointer per request — no proxy reload or "
        "restart is needed."
    )
    return 0


def _cmd_status(args: argparse.Namespace) -> int:
    """Print the active slot, the pointer path, and the discovered endpoints."""
    active_slot_path = _resolve_active_slot_path(args)
    print(f"front-door active-slot pointer: {active_slot_path}")
    try:
        state = read_active_slot(active_slot_path)
        print(f"  active slot: {state.slot}")
    except ActiveSlotError as exc:
        print(f"  active slot: UNSET/INVALID ({exc})")
        state = None

    try:
        endpoints = build_slot_endpoints(args.deploy_dir)
    except (OSError, SlotEndpointError, UnsafeBindError) as exc:
        print(f"  configured slots: ERROR — {exc}", file=sys.stderr)
        return 2
    print(f"  configured slots ({args.deploy_dir}):")
    for endpoint in sorted(endpoints.values(), key=lambda e: e.slot):
        mark = (
            "  <- active"
            if state is not None and endpoint.slot == state.slot
            else ""
        )
        print(f"    {endpoint.slot:>8}: {endpoint.address}{mark}")
    if not endpoints:
        print("    (none)")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Parse arguments, dispatch the subcommand, return an exit code."""
    parser = argparse.ArgumentParser(
        prog="python -m storytime.frontdoor",
        description="Run, switch, or inspect the StoryTime blue/green front door.",
    )
    sub = parser.add_subparsers(dest="command")

    serve = sub.add_parser("serve", help="run the front-door reverse proxy")
    serve.add_argument(
        "--host",
        default=_DEFAULT_FRONT_DOOR_HOST,
        help="Loopback host to bind. Default: 127.0.0.1",
    )
    serve.add_argument(
        "--port",
        type=int,
        default=_DEFAULT_FRONT_DOOR_PORT,
        help="Stable front-door port. Default: 8080",
    )
    _add_path_args(serve)
    serve.set_defaults(func=_cmd_serve)

    switch = sub.add_parser(
        "switch", help="switch the active slot (rollback = switch back)"
    )
    switch.add_argument("slot", help="target slot, e.g. 'blue' or 'green'")
    _add_path_args(switch)
    switch.set_defaults(func=_cmd_switch)

    status = sub.add_parser(
        "status", help="show the active slot and configured endpoints"
    )
    _add_path_args(status)
    status.set_defaults(func=_cmd_status)

    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 2
    exit_code: int = args.func(args)
    return exit_code


if __name__ == "__main__":  # pragma: no cover - module entry point
    sys.exit(main())
