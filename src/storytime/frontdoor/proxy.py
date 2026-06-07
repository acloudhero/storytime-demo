"""The native StoryTime front door — a loopback-only reverse proxy.

Phase 7B front-door decision: rather than depend on an external proxy binary
(Caddy / nginx) the operator must install and that the test suite cannot
exercise, the front door is native Python over the standard library only. It
keeps StoryTime's local-first, zero-external-dependency property, stays fully
covered by the normal test suite, and stays inside the same ruff / mypy /
import-linter discipline as the rest of the codebase.

ARCH-LOCK: Loopback-only front door
DO NOT REFACTOR: the front door binds through ``storytime.http.validate_bind_host``,
the same guard the feed server uses — it rejects ``0.0.0.0`` / ``::`` and any
non-loopback host. The front door also forwards only to loopback slot
endpoints. StoryTime, front door included, serves the local operator only.
Rationale: Architecture Baseline section 15.

How it works:

* The front door binds ONE stable loopback port (default ``127.0.0.1:8080``).
* On every request it reads the active-slot pointer — the single source of
  truth — and forwards to that slot's feed endpoint. A switch therefore takes
  effect for the next request with no proxy reload and no front-door restart:
  updating the pointer file is the whole switch.
* It relays the upstream response faithfully, including ``Range`` / ``206`` /
  ``Content-Range``, so podcast-client byte-range streaming works through the
  front door unchanged.
* It never reads or writes pipeline state, and it imports no ``opentelemetry``:
  the front door is outside the pipeline telemetry path.

It is demo-grade: loopback-only, single-process, no TLS, no auth. That is the
deliberate Option B1 scope.
"""

from __future__ import annotations

import http.client
import http.server
from pathlib import Path
from typing import ClassVar

from storytime.frontdoor.active_slot import ActiveSlotError, read_active_slot
from storytime.frontdoor.endpoints import SlotEndpoint
from storytime.http import validate_bind_host

# Hop-by-hop headers are connection-scoped and must not be relayed by a proxy
# (RFC 7230 section 6.1). Stripped from the upstream response before relay.
_HOP_BY_HOP_HEADERS = frozenset(
    {
        "connection",
        "keep-alive",
        "proxy-authenticate",
        "proxy-authorization",
        "te",
        "trailers",
        "transfer-encoding",
        "upgrade",
    }
)

# Request headers the front door forwards to the upstream slot. Deliberately a
# small allow-list: enough for feed/audio delivery and byte-range streaming,
# nothing that would let a client steer the proxy.
_FORWARDABLE_REQUEST_HEADERS = frozenset(
    {
        "accept",
        "accept-encoding",
        "if-modified-since",
        "if-none-match",
        "if-range",
        "range",
        "user-agent",
    }
)

# Bytes moved per write while streaming a (possibly large) upstream body.
_STREAM_CHUNK = 64 * 1024

# Connect/read timeout when dialing an upstream slot. A slot whose process is
# not running fails fast to an honest 502 rather than hanging the front door.
_UPSTREAM_TIMEOUT_SECONDS = 5.0


class FrontDoorHandler(http.server.BaseHTTPRequestHandler):
    """Reverse-proxy handler: resolve the active slot, forward, relay.

    ``slot_endpoints`` and ``active_slot_path`` are bound per server by
    ``FrontDoorServer.build_handler`` — the standard three-argument handler
    constructor is left untouched (the same pattern ``RangeFileHandler`` uses).
    """

    # Bound per server by FrontDoorServer.build_handler().
    slot_endpoints: ClassVar[dict[str, SlotEndpoint]]
    active_slot_path: ClassVar[Path]

    server_version = "StoryTimeFrontDoor"
    # HTTP/1.0: one request per connection, Content-Length-delimited bodies —
    # the same simple model the feed server uses.
    protocol_version = "HTTP/1.0"

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler dispatch name
        """Proxy a GET to the active slot, with a body."""
        self._proxy(include_body=True)

    def do_HEAD(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler dispatch name
        """Proxy a HEAD to the active slot — response headers only."""
        self._proxy(include_body=False)

    # -- active-slot resolution ---------------------------------------------

    def _resolve_endpoint(self) -> SlotEndpoint | None:
        """Return the active slot's endpoint, or None after sending an error.

        A missing/garbage active-slot pointer, or an active slot with no known
        endpoint, is an honest 503 — the front door has nowhere safe to route.
        """
        try:
            state = read_active_slot(self.active_slot_path)
        except ActiveSlotError as exc:
            self._send_plain(
                503, f"front door has no valid active slot: {exc}"
            )
            return None
        endpoint = self.slot_endpoints.get(state.slot)
        if endpoint is None:
            known = ", ".join(sorted(self.slot_endpoints)) or "(none)"
            self._send_plain(
                503,
                f"active slot {state.slot!r} has no known feed endpoint "
                f"(known slots: {known})",
            )
            return None
        return endpoint

    # -- the proxy body ------------------------------------------------------

    def _proxy(self, *, include_body: bool) -> None:
        endpoint = self._resolve_endpoint()
        if endpoint is None:
            return

        forwarded = {
            key: value
            for key, value in self.headers.items()
            if key.lower() in _FORWARDABLE_REQUEST_HEADERS
        }
        forwarded["Host"] = endpoint.address
        forwarded["Connection"] = "close"
        # An honest marker so an operator can see, in the upstream slot's view,
        # that a request arrived via the front door and for which slot.
        forwarded["X-StoryTime-Front-Door"] = endpoint.slot

        connection = http.client.HTTPConnection(
            endpoint.host, endpoint.port, timeout=_UPSTREAM_TIMEOUT_SECONDS
        )
        try:
            connection.request(self.command, self.path, headers=forwarded)
            upstream = connection.getresponse()
        except (OSError, http.client.HTTPException) as exc:
            connection.close()
            self._send_plain(
                502,
                f"front door could not reach the {endpoint.slot!r} slot at "
                f"{endpoint.address} ({type(exc).__name__}). Is that slot's "
                "feed server running?",
            )
            return

        try:
            self._relay(upstream, include_body=include_body)
        finally:
            connection.close()

    def _relay(
        self, upstream: http.client.HTTPResponse, *, include_body: bool
    ) -> None:
        """Relay *upstream*'s status, headers, and body to the client.

        Status and headers are passed through verbatim (minus hop-by-hop
        headers), so a 206 Partial Content with a Content-Range — the upstream
        feed server's honest answer to a Range request — reaches the podcast
        client unchanged.
        """
        self.send_response(upstream.status)
        for key, value in upstream.getheaders():
            if key.lower() in _HOP_BY_HOP_HEADERS:
                continue
            self.send_header(key, value)
        self.end_headers()
        if not include_body:
            return
        try:
            while True:
                chunk = upstream.read(_STREAM_CHUNK)
                if not chunk:
                    break
                self.wfile.write(chunk)
        except (BrokenPipeError, ConnectionResetError):
            # A podcast client commonly closes the connection once it has
            # buffered enough; that is normal, not a front-door fault.
            return

    def _send_plain(self, status: int, message: str) -> None:
        """Send a short text/plain status response from the front door itself."""
        body = (message + "\n").encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command == "HEAD":
            return
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            return

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        """Silence per-request logging; the launcher prints its own line."""
        return


class FrontDoorServer:
    """A loopback-only reverse proxy in front of the blue/green slots."""

    def __init__(
        self,
        *,
        host: str,
        port: int,
        slot_endpoints: dict[str, SlotEndpoint],
        active_slot_path: Path,
    ) -> None:
        # ARCH-LOCK: the bind host is validated before it is ever bound.
        self._host = validate_bind_host(host)
        self._port = port
        self._slot_endpoints = dict(slot_endpoints)
        self._active_slot_path = active_slot_path

    @property
    def bind_host(self) -> str:
        return self._host

    @property
    def slot_endpoints(self) -> dict[str, SlotEndpoint]:
        return dict(self._slot_endpoints)

    def build_handler(self) -> type[FrontDoorHandler]:
        """Return a FrontDoorHandler subclass bound to this server's routing."""
        endpoints = self._slot_endpoints
        active_path = self._active_slot_path

        class _BoundFrontDoorHandler(FrontDoorHandler):
            slot_endpoints = endpoints
            active_slot_path = active_path

        return _BoundFrontDoorHandler

    def make_server(self) -> http.server.ThreadingHTTPServer:
        """Construct (but do not start) the front-door server bound to loopback.

        ThreadingHTTPServer so a slow audio download on one connection does not
        block the operator's other requests.
        """
        return http.server.ThreadingHTTPServer(
            (self._host, self._port), self.build_handler()
        )

    def serve_forever(self) -> None:  # pragma: no cover - blocking, not unit-tested
        """Start serving. Blocks until interrupted."""
        with self.make_server() as server:
            server.serve_forever()


__all__ = ["FrontDoorHandler", "FrontDoorServer"]
