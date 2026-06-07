"""Local, loopback-only HTTP server for previewing the feed and episode audio.

ARCH-LOCK: Loopback-only bind
DO NOT REFACTOR: validate_bind_host MUST reject 0.0.0.0, ::, empty hosts, and
any non-loopback address. Do not "allow it behind a flag". StoryTime serves
only to the local operator.
Rationale: Architecture Baseline section 15. Source material and run artifacts
must never be exposed on a network interface.

ARCH-LOCK: Range-capable audio serving (Phase 6, OI-7)
DO NOT REFACTOR: audio is served through RangeFileHandler, which honours HTTP
byte-range requests via the pure parse_byte_range function. Do not swap in
http.server.SimpleHTTPRequestHandler — Architecture Baseline section 15 states
the stdlib handler "does not handle ranges correctly and is not used for
audio", and mainstream podcast clients issue range requests for enclosures.
Rationale: Architecture Baseline section 15.
"""

from __future__ import annotations

import http.server
import urllib.parse
from pathlib import Path
from typing import ClassVar

from storytime.http.ranges import RangeNotSatisfiable, parse_byte_range

# Hosts that resolve to the local loopback interface only.
_LOOPBACK_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})

# The relative name of the feed document; a request for "/" serves it.
_FEED_DOCUMENT = "feed.xml"

# How many bytes to move per write while streaming a (possibly large) file.
_STREAM_CHUNK = 64 * 1024

# Content types StoryTime serves. Anything else is octet-stream.
_CONTENT_TYPES = {
    ".xml": "application/rss+xml",
    ".mp3": "audio/mpeg",
}
_DEFAULT_CONTENT_TYPE = "application/octet-stream"


class UnsafeBindError(ValueError):
    """Raised when an HTTP bind host is not a loopback address."""


def validate_bind_host(host: str) -> str:
    """Return *host* if it is a loopback address, else raise UnsafeBindError.

    Explicitly rejects 0.0.0.0 and :: (all-interfaces binds) and empty hosts.
    """
    normalized = host.strip().lower()
    if normalized in ("", "0.0.0.0", "::", "*"):
        raise UnsafeBindError(
            f"refusing to bind HTTP server to non-loopback host {host!r}; "
            "StoryTime serves the local operator only"
        )
    if normalized not in _LOOPBACK_HOSTS:
        raise UnsafeBindError(
            f"host {host!r} is not a recognised loopback address "
            f"(allowed: {sorted(_LOOPBACK_HOSTS)})"
        )
    return normalized


def _content_type(path: Path) -> str:
    """Return the Content-Type StoryTime serves *path* with."""
    return _CONTENT_TYPES.get(path.suffix.lower(), _DEFAULT_CONTENT_TYPE)


class RangeFileHandler(http.server.BaseHTTPRequestHandler):
    """A loopback-only static file handler that honours HTTP byte ranges.

    Serves GET and HEAD from ``feed_root``. The byte-range arithmetic lives in
    the pure, separately tested parse_byte_range; this handler only translates
    its result into 200 / 206 / 416 responses. The handler never escapes
    feed_root: a request whose resolved path leaves the root is a 404.

    feed_root is bound by build_request_handler, which produces a per-server
    subclass — so the standard three-argument handler constructor is used and
    no per-request wiring is needed.
    """

    # Bound per server by build_request_handler(). Declared here so the
    # methods below are type-checked against it.
    feed_root: ClassVar[Path]

    server_version = "StoryTimeFeed"
    # HTTP/1.0 keeps the response model simple: one request per connection,
    # Content-Length-delimited bodies, no chunked encoding to implement.
    protocol_version = "HTTP/1.0"

    # -- request entry points ------------------------------------------------

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler dispatch name
        """Serve a file, honouring a Range header, with a body."""
        self._serve(include_body=True)

    def do_HEAD(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler dispatch name
        """Serve a file's response headers only — same status logic as GET."""
        self._serve(include_body=False)

    # -- path resolution -----------------------------------------------------

    def _resolve(self) -> Path | None:
        """Resolve the request path to a file inside feed_root, or None.

        Returns None for a path that escapes the root, names a directory, or
        does not exist — the caller answers all three with a 404 so the
        response never reveals which case it was.
        """
        # Strip the query string, percent-decode, drop the leading slash.
        raw = urllib.parse.urlsplit(self.path).path
        decoded = urllib.parse.unquote(raw)
        relative = decoded.lstrip("/")
        if relative in ("", "."):
            relative = _FEED_DOCUMENT

        root = self.feed_root
        candidate = (root / relative).resolve()
        # Containment check: the resolved path must be the root or below it.
        # This rejects "../" traversal and absolute-path injection.
        if candidate != root and root not in candidate.parents:
            return None
        if not candidate.is_file():
            return None
        return candidate

    # -- the shared GET/HEAD body --------------------------------------------

    def _serve(self, *, include_body: bool) -> None:
        path = self._resolve()
        if path is None:
            self.send_error(404, "Not Found")
            return

        size = path.stat().st_size
        try:
            byte_range = parse_byte_range(self.headers.get("Range"), size)
        except RangeNotSatisfiable:
            # The client named a single, well-formed range that lies outside
            # the file: 416 with Content-Range: bytes */<size> (RFC 7233).
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        content_type = _content_type(path)
        if byte_range is None:
            # Whole representation: 200 OK.
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(size))
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()
            if include_body:
                self._stream(path, start=0, length=size)
            return

        # Exactly one satisfiable range: 206 Partial Content.
        self.send_response(206)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(byte_range.length))
        self.send_header("Content-Range", byte_range.content_range(size))
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()
        if include_body:
            self._stream(path, start=byte_range.start, length=byte_range.length)

    def _stream(self, path: Path, *, start: int, length: int) -> None:
        """Write *length* bytes of *path* starting at *start* to the client.

        A client that disconnects mid-download (a podcast app commonly closes
        a connection once it has buffered enough) raises BrokenPipeError /
        ConnectionResetError; that is normal, not a server fault, so it is
        swallowed rather than logged as an error.
        """
        try:
            with path.open("rb") as handle:
                handle.seek(start)
                remaining = length
                while remaining > 0:
                    chunk = handle.read(min(_STREAM_CHUNK, remaining))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    remaining -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            return

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        """Silence per-request logging; the serve command prints its own line."""
        return


def build_request_handler(directory: Path) -> type[RangeFileHandler]:
    """Return a RangeFileHandler subclass bound to serve *directory*.

    http.server instantiates the handler class per request with the standard
    (request, client_address, server) signature; binding the root as a class
    attribute on a per-server subclass keeps that signature untouched.
    """
    resolved = directory.resolve()

    class _BoundRangeFileHandler(RangeFileHandler):
        feed_root = resolved

    return _BoundRangeFileHandler


class LocalFeedServer:
    """A loopback-only, range-capable static file server for the feed directory."""

    def __init__(self, *, host: str, port: int, directory: Path) -> None:
        # ARCH-LOCK: the host is validated before it is ever bound.
        self._host = validate_bind_host(host)
        self._port = port
        self._directory = directory

    @property
    def bind_host(self) -> str:
        return self._host

    def make_server(self) -> http.server.ThreadingHTTPServer:
        """Construct (but do not start) the HTTP server bound to loopback.

        ThreadingHTTPServer so a slow audio download on one connection does
        not block the operator's other requests.
        """
        handler = build_request_handler(self._directory)
        return http.server.ThreadingHTTPServer((self._host, self._port), handler)

    def serve_forever(self) -> None:  # pragma: no cover - blocking, not unit-tested
        """Start serving. Blocks until interrupted."""
        with self.make_server() as server:
            server.serve_forever()


__all__ = [
    "LocalFeedServer",
    "RangeFileHandler",
    "UnsafeBindError",
    "build_request_handler",
    "validate_bind_host",
]
