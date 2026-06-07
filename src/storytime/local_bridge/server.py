"""Loopback-only local bridge HTTP server (Phase 13G — runtime).

This is the first runtime local bridge, implemented against the locked Phase
13F architecture (``docs/local-bridge-architecture.md``). It is intentionally
small and dependency-free: a standard-library ``http.server`` listener that

- binds **loopback only** (``127.0.0.1`` / ``::1``) and refuses every all-interfaces bind and
  every non-loopback host (§5),
- enforces a **strict origin policy**: a request carrying an ``Origin`` header
  that does not exactly match the allowed loopback origin set is answered
  ``403 Forbidden``; no wildcard ``Access-Control-Allow-Origin`` is ever emitted
  (§6),
- accepts only a versioned, allowlisted **action-request DTO** — never a
  free-form command / SQL / file path (§7-8),
- routes each action through a **command-pattern router** to exactly one
  pre-approved handler (§10),
- returns **202 Accepted** with an ``actionRequestId`` / ``jobId`` for the one
  long-running action, executes it on a **single-concurrency** worker, and lets
  the caller read status later (§15) — acceptance is never success.

It is **not** full Local mode, not Cloud/Distributed mode, has no frontend
wiring, no provider integrations, no persistent or external queue, and writes
nothing outside its explicitly-configured workspace.
"""

from __future__ import annotations

import json
import threading
from dataclasses import dataclass, field
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from storytime.http import UnsafeBindError, validate_bind_host
from storytime.local_bridge.action_queue import (
    DEFAULT_CAPACITY,
    ActionQueue,
    Job,
    QueueFull,
)
from storytime.local_bridge.actions import (
    BridgeContext,
    execute_retry_failed_stage,
    plan_route,
)
from storytime.local_bridge.dto import (
    SCHEMA_VERSION,
    ValidatedRequest,
    ValidationError,
    validate_request,
)
from storytime.local_bridge.responses import (
    build_accepted_response,
    build_deduplicated_response,
    build_rejected_response,
    build_validated_response,
)
from storytime.util.clock import Clock, SystemClock
from storytime.util.ids import new_ulid

# The bridge schema / version reported on /ready.
BRIDGE_VERSION = "0.1.0"
RUNTIME_MODE = "local-bridge"

# Loopback host literals used to validate the connecting client address.
_LOOPBACK_CLIENT_HOSTS: frozenset[str] = frozenset(
    {"127.0.0.1", "::1", "::ffff:127.0.0.1"}
)


def default_allowed_origins(host: str, port: int) -> frozenset[str]:
    """Return the default strict origin allowlist for a loopback bind.

    Only loopback origins on the bound port are allowed by default; there is no
    wildcard. An operator can pass an explicit set to widen this to, e.g., the
    GUI's own loopback port — but never to a non-loopback origin.
    """
    return frozenset(
        {
            f"http://127.0.0.1:{port}",
            f"http://localhost:{port}",
            f"http://[::1]:{port}",
        }
    )


@dataclass
class Bridge:
    """The bridge controller: owns the queue, context, and request registry.

    The HTTP handler is a thin translation layer over this object's methods,
    which return ``(status_code, body_dict)`` and never touch sockets — so the
    routing / validation logic is unit-testable without a live server.
    """

    context: BridgeContext
    capacity: int = DEFAULT_CAPACITY
    _queue: ActionQueue = field(init=False)
    _requests: dict[str, ValidatedRequest] = field(default_factory=dict, init=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False)

    def __post_init__(self) -> None:
        self._queue = ActionQueue(self._executor, capacity=self.capacity)

    # -- worker executor ---------------------------------------------------

    def _executor(self, job: Job) -> dict[str, Any]:
        with self._lock:
            request = self._requests.get(job.action_request_id)
        if request is None:  # defensive: should never happen
            return {
                "status": "failed",
                "code": "request_not_found",
                "message": "no validated request registered for this job",
            }
        return execute_retry_failed_stage(request, self.context)

    # -- lifecycle ---------------------------------------------------------

    def start(self) -> None:
        self._queue.start()

    def stop(self, *, timeout: float = 5.0) -> None:
        self._queue.stop(timeout=timeout)

    @property
    def queue(self) -> ActionQueue:
        return self._queue

    # -- endpoint handlers (transport-free) --------------------------------

    def health(self) -> tuple[int, dict[str, Any]]:
        return HTTPStatus.OK, {"status": "ok", "schemaVersion": SCHEMA_VERSION}

    def ready(self, allowed_origins: frozenset[str]) -> tuple[int, dict[str, Any]]:
        return HTTPStatus.OK, {
            "status": "ready",
            "schemaVersion": SCHEMA_VERSION,
            "bridgeVersion": BRIDGE_VERSION,
            "runtimeMode": RUNTIME_MODE,
            "loopbackOnly": True,
            "allowedOrigins": sorted(allowed_origins),
            "wildcardOriginAllowed": False,
            "workspaceConfigured": True,
            "workspaceId": self.context.workspace_id,
            "executableActions": ["retry_failed_stage"],
            "validationOnlyActions": ["inspect_trust_envelope"],
            "notImplementedActions": ["refresh_export"],
            "queueImplemented": True,
            "maxConcurrency": 1,
            "queueCapacity": self._queue.capacity,
        }

    def queue_snapshot(self) -> tuple[int, dict[str, Any]]:
        return HTTPStatus.OK, self._queue.snapshot()

    def action_status(self, action_request_id: str) -> tuple[int, dict[str, Any]]:
        job = self._queue.get_job(action_request_id)
        if job is None:
            return HTTPStatus.NOT_FOUND, build_rejected_response(
                None,
                [
                    ValidationError(
                        code="not_found",
                        message=f"no action with id {action_request_id!r}",
                    )
                ],
            )
        return HTTPStatus.OK, job.public_state()

    def submit_action(self, payload: Any) -> tuple[int, dict[str, Any]]:
        """Validate, route, and (for async actions) enqueue an action request."""
        request, errors = validate_request(payload)
        if request is None:
            request_id = (
                str(payload.get("requestId"))
                if isinstance(payload, dict) and payload.get("requestId")
                else None
            )
            return HTTPStatus.UNPROCESSABLE_ENTITY, build_rejected_response(
                request_id, errors
            )

        route = plan_route(request)
        if route.kind == "sync":
            return HTTPStatus.OK, build_validated_response(
                request.request_id,
                warnings=list(route.warnings),
                not_implemented=route.not_implemented,
            )
        if route.kind == "reject":
            return HTTPStatus.UNPROCESSABLE_ENTITY, build_rejected_response(
                request.request_id,
                [
                    ValidationError(
                        code="no_route",
                        message="action has no runtime route in this phase",
                        field="action",
                    )
                ],
            )

        # Async: enqueue a controlled job.
        action_request_id = f"act-{new_ulid()}"
        job_id = f"job-{new_ulid()}"
        job = Job(
            action_request_id=action_request_id,
            job_id=job_id,
            request_id=request.request_id,
            action=request.action,
            idempotency_key=request.idempotency_key,
        )
        with self._lock:
            self._requests[action_request_id] = request
        try:
            registered, deduplicated = self._queue.submit(job)
        except QueueFull as exc:
            with self._lock:
                self._requests.pop(action_request_id, None)
            return HTTPStatus.TOO_MANY_REQUESTS, build_rejected_response(
                request.request_id,
                [
                    ValidationError(
                        code="queue_full",
                        message=str(exc),
                    )
                ],
            )

        if deduplicated:
            return HTTPStatus.ACCEPTED, build_deduplicated_response(
                request.request_id,
                action_request_id=registered.action_request_id,
                job_id=registered.job_id,
                export_refresh_required=True,
            )
        return HTTPStatus.ACCEPTED, build_accepted_response(
            request.request_id,
            action_request_id=action_request_id,
            job_id=job_id,
            export_refresh_required=True,
            warnings=list(route.warnings),
        )


class _BridgeHandler(BaseHTTPRequestHandler):
    """A loopback-only handler translating HTTP to :class:`Bridge` calls."""

    # Bound per server by :func:`build_handler`.
    bridge: Bridge
    allowed_origins: frozenset[str]

    server_version = "StoryTimeLocalBridge"
    protocol_version = "HTTP/1.1"

    # Silence default request logging to stderr in tests / operator use.
    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        return

    # -- origin / loopback enforcement ------------------------------------

    def _client_is_loopback(self) -> bool:
        host = self.client_address[0] if self.client_address else ""
        return host in _LOOPBACK_CLIENT_HOSTS

    def _origin_ok(self) -> bool:
        """True if there is no Origin header or it exactly matches the allowlist."""
        origin = self.headers.get("Origin")
        if origin is None:
            return True
        return origin in self.allowed_origins

    def _send(
        self, status: int, body: dict[str, Any], *, echo_origin: bool = True
    ) -> None:
        payload = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        # Echo the EXACT allowed origin only — never a wildcard.
        origin = self.headers.get("Origin")
        if echo_origin and origin is not None and origin in self.allowed_origins:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(payload)

    def _reject(self, status: int, code: str, message: str) -> None:
        self._send(
            status,
            build_rejected_response(
                None, [ValidationError(code=code, message=message)]
            ),
        )

    def _guard(self) -> bool:
        """Run connection-level guards; return True if the request may proceed."""
        if not self._client_is_loopback():
            self._reject(
                HTTPStatus.FORBIDDEN,
                "non_loopback_client",
                "bridge serves loopback clients only",
            )
            return False
        if not self._origin_ok():
            self._reject(
                HTTPStatus.FORBIDDEN,
                "origin_forbidden",
                "request Origin is not in the allowed loopback origin set",
            )
            return False
        return True

    # -- method dispatch ---------------------------------------------------

    def do_OPTIONS(self) -> None:  # noqa: N802 - dispatch name
        # CORS preflight: fail closed on a present-but-unknown origin.
        if not self._client_is_loopback():
            self._reject(
                HTTPStatus.FORBIDDEN,
                "non_loopback_client",
                "bridge serves loopback clients only",
            )
            return
        origin = self.headers.get("Origin")
        if origin is not None and origin not in self.allowed_origins:
            self._reject(
                HTTPStatus.FORBIDDEN,
                "origin_forbidden",
                "request Origin is not in the allowed loopback origin set",
            )
            return
        self.send_response(HTTPStatus.NO_CONTENT)
        if origin is not None:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802 - dispatch name
        if not self._guard():
            return
        path = self.path.split("?", 1)[0].rstrip("/") or "/"
        if path == "/health":
            self._send(*self.bridge.health())
        elif path == "/ready":
            self._send(*self.bridge.ready(self.allowed_origins))
        elif path == "/queue":
            self._send(*self.bridge.queue_snapshot())
        elif path.startswith("/actions/"):
            action_request_id = path[len("/actions/") :]
            self._send(*self.bridge.action_status(action_request_id))
        else:
            self._reject(
                HTTPStatus.NOT_FOUND, "unknown_path", f"no GET route for {path!r}"
            )

    def do_POST(self) -> None:  # noqa: N802 - dispatch name
        if not self._guard():
            return
        path = self.path.split("?", 1)[0].rstrip("/") or "/"
        if path != "/actions":
            self._reject(
                HTTPStatus.NOT_FOUND, "unknown_path", f"no POST route for {path!r}"
            )
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._reject(
                HTTPStatus.BAD_REQUEST, "bad_length", "invalid Content-Length"
            )
            return
        raw = self.rfile.read(length) if length > 0 else b""
        ctype = self.headers.get("Content-Type", "")
        if "application/json" not in ctype.lower():
            self._reject(
                HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                "unsupported_media_type",
                "Content-Type must be application/json",
            )
            return
        try:
            payload = json.loads(raw.decode("utf-8")) if raw else None
        except (ValueError, UnicodeDecodeError):
            self._reject(
                HTTPStatus.BAD_REQUEST, "malformed_json", "request body is not valid JSON"
            )
            return
        self._send(*self.bridge.submit_action(payload))

    # Unsupported methods → 405.
    def _method_not_allowed(self) -> None:
        self._reject(
            HTTPStatus.METHOD_NOT_ALLOWED,
            "method_not_allowed",
            f"method {self.command!r} is not supported",
        )

    do_PUT = _method_not_allowed  # noqa: N815
    do_DELETE = _method_not_allowed  # noqa: N815
    do_PATCH = _method_not_allowed  # noqa: N815
    do_HEAD = _method_not_allowed  # noqa: N815


def build_handler(
    bridge: Bridge, allowed_origins: frozenset[str]
) -> type[_BridgeHandler]:
    """Return a handler subclass bound to *bridge* and *allowed_origins*."""

    class _BoundHandler(_BridgeHandler):
        pass

    _BoundHandler.bridge = bridge
    _BoundHandler.allowed_origins = allowed_origins
    return _BoundHandler


class LocalBridgeServer:
    """A loopback-only HTTP server hosting the local bridge.

    Refuses any non-loopback bind host at construction (reusing the project's
    audited :func:`storytime.http.validate_bind_host`, which rejects
    all-interfaces, ``::``, empty, and non-loopback hosts). Binding ``port=0`` lets the OS
    pick a free loopback port — used by tests.
    """

    def __init__(
        self,
        *,
        host: str,
        port: int,
        workspace_id: str,
        workspace_root: Path,
        clock: Clock | None = None,
        capacity: int = DEFAULT_CAPACITY,
        allowed_origins: frozenset[str] | None = None,
    ) -> None:
        self.bind_host = validate_bind_host(host)
        context = BridgeContext(
            workspace_id=workspace_id,
            workspace_root=workspace_root,
            clock=clock or SystemClock(),
        )
        self.bridge = Bridge(context=context, capacity=capacity)
        # ThreadingHTTPServer keeps the status / queue endpoints responsive
        # while a long-running action is in flight on the single worker.
        self._http = ThreadingHTTPServer(
            (self.bind_host, port), build_handler(self.bridge, frozenset())
        )
        self._http.daemon_threads = True
        self.port = self._http.server_address[1]
        origins = (
            allowed_origins
            if allowed_origins is not None
            else default_allowed_origins(self.bind_host, self.port)
        )
        # Re-bind the handler now that the real port (and thus origins) is known.
        self._http.RequestHandlerClass = build_handler(self.bridge, origins)
        self.allowed_origins = origins
        self._thread: threading.Thread | None = None

    @property
    def url(self) -> str:
        host = "127.0.0.1" if self.bind_host in ("127.0.0.1", "localhost") else self.bind_host
        return f"http://{host}:{self.port}"

    def serve_forever_in_thread(self) -> None:
        """Start the worker and serve HTTP on a background daemon thread."""
        self.bridge.start()
        self._thread = threading.Thread(
            target=self._http.serve_forever, name="storytime-local-bridge-http",
            daemon=True,
        )
        self._thread.start()

    def shutdown(self, *, timeout: float = 5.0) -> None:
        """Stop HTTP serving and drain the worker cleanly."""
        self._http.shutdown()
        self._http.server_close()
        if self._thread is not None:
            self._thread.join(timeout=timeout)
        self.bridge.stop(timeout=timeout)


__all__ = [
    "BRIDGE_VERSION",
    "Bridge",
    "LocalBridgeServer",
    "RUNTIME_MODE",
    "UnsafeBindError",
    "default_allowed_origins",
    "validate_bind_host",
]
