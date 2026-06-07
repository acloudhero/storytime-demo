"""Gated CLI entrypoint for the local bridge (Phase 13G — runtime).

Invoke with::

    python -m storytime.local_bridge --host 127.0.0.1 --port 8765 \\
        --workspace <path> --workspace-id <id>

This entrypoint is **strictly gated**:

- it REQUIRES an explicit ``--workspace`` and refuses to start without one (the
  bridge must never run against a default / real user workspace implicitly),
- ``--host`` defaults to ``127.0.0.1`` and any non-loopback host is refused by
  :func:`storytime.http.validate_bind_host` (all-interfaces and non-loopback hosts refused),
- the workspace path must exist; the bridge writes nothing outside it.

It uses only the standard library (``argparse``) and adds no dependency. It is a
thin convenience wrapper over :class:`storytime.local_bridge.server.LocalBridgeServer`;
all behaviour lives in the importable, tested modules.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from storytime.http import UnsafeBindError
from storytime.local_bridge.server import LocalBridgeServer


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m storytime.local_bridge",
        description="StoryTime loopback-only local bridge (Phase 13G).",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="loopback host to bind (default: 127.0.0.1; non-loopback refused)",
    )
    parser.add_argument(
        "--port", type=int, default=8765, help="port to bind (default: 8765)"
    )
    parser.add_argument(
        "--workspace",
        required=True,
        help="REQUIRED explicit workspace root; the bridge refuses to start without it",
    )
    parser.add_argument(
        "--workspace-id",
        default="ws-local-0001",
        help="workspace identity the bridge will accept actions for",
    )
    args = parser.parse_args(argv)

    workspace_root = Path(args.workspace).expanduser().resolve()
    if not workspace_root.is_dir():
        print(
            f"refusing to start: workspace path {workspace_root} does not exist",
            file=sys.stderr,
        )
        return 2

    try:
        server = LocalBridgeServer(
            host=args.host,
            port=args.port,
            workspace_id=args.workspace_id,
            workspace_root=workspace_root,
        )
    except UnsafeBindError as exc:
        print(f"refusing to start: {exc}", file=sys.stderr)
        return 2

    server.serve_forever_in_thread()
    print(
        f"StoryTime local bridge listening on {server.url} "
        f"(workspace={workspace_root}); Ctrl-C to stop.",
        file=sys.stderr,
    )
    try:
        # Block the main thread until interrupted.
        import threading

        threading.Event().wait()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
