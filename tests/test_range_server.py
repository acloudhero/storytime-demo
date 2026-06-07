"""Integration tests for the loopback range-capable feed server (OI-7).

A real ThreadingHTTPServer is started on an ephemeral loopback port and driven
with http.client. These tests cover full responses, 206 partial content for
the three range forms, 416 for an unsatisfiable range, HEAD, content types,
the 404 for a missing file, and — load-bearing — that a path-traversal request
cannot read a file outside the feed root.
"""

from __future__ import annotations

import http.client
import threading
from collections.abc import Iterator
from pathlib import Path

import pytest

from storytime.http.server import LocalFeedServer

# A feed.xml body long enough to exercise non-trivial ranges.
_FEED_BODY = (
    b'<?xml version="1.0" encoding="UTF-8"?>\n'
    b'<rss version="2.0"><channel><title>StoryTime</title>'
    b"<link>http://127.0.0.1/feed.xml</link>"
    b"<description>Local test feed.</description></channel></rss>"
)

# Deterministic "audio" payload — 2 KiB of a repeating byte pattern.
_AUDIO_BODY = bytes(range(256)) * 8


@pytest.fixture()
def feed_root(tmp_path: Path) -> Path:
    """A feed directory holding feed.xml and audio/episode.mp3.

    A secret file is placed OUTSIDE the feed root so a traversal test can
    prove it is unreachable.
    """
    root = tmp_path / "feed"
    (root / "audio").mkdir(parents=True)
    (root / "feed.xml").write_bytes(_FEED_BODY)
    (root / "audio" / "episode.mp3").write_bytes(_AUDIO_BODY)
    (tmp_path / "secret.txt").write_bytes(b"TOP SECRET")
    return root


@pytest.fixture()
def server_port(feed_root: Path) -> Iterator[int]:
    """Start the feed server on an ephemeral loopback port; yield the port."""
    server = LocalFeedServer(
        host="127.0.0.1", port=0, directory=feed_root
    ).make_server()
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield int(port)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def _request(
    port: int, path: str, *, method: str = "GET", headers: dict[str, str] | None = None
) -> tuple[int, dict[str, str], bytes]:
    """Issue one HTTP request; return (status, headers, body)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    try:
        conn.request(method, path, headers=headers or {})
        response = conn.getresponse()
        body = response.read()
        return response.status, dict(response.getheaders()), body
    finally:
        conn.close()


# -- whole-file responses ----------------------------------------------------

def test_get_feed_returns_full_document_as_rss(server_port: int) -> None:
    status, headers, body = _request(server_port, "/feed.xml")
    assert status == 200
    assert headers["Content-Type"] == "application/rss+xml"
    assert headers["Accept-Ranges"] == "bytes"
    assert headers["Content-Length"] == str(len(_FEED_BODY))
    assert body == _FEED_BODY


def test_root_path_serves_the_feed_document(server_port: int) -> None:
    status, _headers, body = _request(server_port, "/")
    assert status == 200
    assert body == _FEED_BODY


def test_get_audio_uses_the_audio_mpeg_type(server_port: int) -> None:
    status, headers, body = _request(server_port, "/audio/episode.mp3")
    assert status == 200
    assert headers["Content-Type"] == "audio/mpeg"
    assert body == _AUDIO_BODY


# -- partial content ---------------------------------------------------------

def test_closed_range_returns_206_with_the_exact_slice(server_port: int) -> None:
    status, headers, body = _request(
        server_port, "/audio/episode.mp3", headers={"Range": "bytes=100-199"}
    )
    assert status == 206
    assert headers["Content-Range"] == f"bytes 100-199/{len(_AUDIO_BODY)}"
    assert headers["Content-Length"] == "100"
    assert body == _AUDIO_BODY[100:200]


def test_open_ended_range_returns_206_tail(server_port: int) -> None:
    start = len(_AUDIO_BODY) - 50
    status, headers, body = _request(
        server_port, "/audio/episode.mp3", headers={"Range": f"bytes={start}-"}
    )
    assert status == 206
    assert body == _AUDIO_BODY[start:]
    assert headers["Content-Range"] == (
        f"bytes {start}-{len(_AUDIO_BODY) - 1}/{len(_AUDIO_BODY)}"
    )


def test_suffix_range_returns_206_last_n_bytes(server_port: int) -> None:
    status, _headers, body = _request(
        server_port, "/audio/episode.mp3", headers={"Range": "bytes=-64"}
    )
    assert status == 206
    assert body == _AUDIO_BODY[-64:]


def test_unsatisfiable_range_returns_416(server_port: int) -> None:
    size = len(_AUDIO_BODY)
    status, headers, body = _request(
        server_port,
        "/audio/episode.mp3",
        headers={"Range": f"bytes={size + 10}-{size + 20}"},
    )
    assert status == 416
    assert headers["Content-Range"] == f"bytes */{size}"
    assert body == b""


def test_malformed_range_is_ignored_and_serves_200(server_port: int) -> None:
    # A malformed Range header is ignored; the whole file is served (RFC 7233).
    status, _headers, body = _request(
        server_port, "/audio/episode.mp3", headers={"Range": "bytes=not-a-range"}
    )
    assert status == 200
    assert body == _AUDIO_BODY


# -- HEAD --------------------------------------------------------------------

def test_head_returns_headers_and_no_body(server_port: int) -> None:
    status, headers, body = _request(server_port, "/feed.xml", method="HEAD")
    assert status == 200
    assert headers["Content-Length"] == str(len(_FEED_BODY))
    assert body == b""


def test_head_with_range_reports_206_headers_without_a_body(
    server_port: int,
) -> None:
    status, headers, body = _request(
        server_port,
        "/audio/episode.mp3",
        method="HEAD",
        headers={"Range": "bytes=0-9"},
    )
    assert status == 206
    assert headers["Content-Range"] == f"bytes 0-9/{len(_AUDIO_BODY)}"
    assert body == b""


# -- error and safety cases --------------------------------------------------

def test_missing_file_returns_404(server_port: int) -> None:
    status, _headers, _body = _request(server_port, "/audio/nope.mp3")
    assert status == 404


def test_path_traversal_cannot_escape_the_feed_root(server_port: int) -> None:
    """Load-bearing: a ../ request must not read a file outside the root."""
    for attack in (
        "/../secret.txt",
        "/audio/../../secret.txt",
        "/%2e%2e/secret.txt",
    ):
        status, _headers, body = _request(server_port, attack)
        assert status == 404, attack
        assert b"SECRET" not in body, attack


def test_unsupported_method_is_rejected(server_port: int) -> None:
    # BaseHTTPRequestHandler answers a method with no handler with 501.
    status, _headers, _body = _request(server_port, "/feed.xml", method="POST")
    assert status == 501
