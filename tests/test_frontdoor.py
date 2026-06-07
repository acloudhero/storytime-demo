"""Phase 7B — blue/green front door: active slot, switch/rollback, proxy.

Coverage:

* the active-slot pointer accepts ``blue`` / ``green`` and rejects invalid or
  traversal-like values, and reads of a missing/garbage file fail typed
  (``ActiveSlotError``) rather than crashing;
* slot endpoints are discovered from the real ``config/deploy/*.env`` files
  and point only to known slots on loopback ports;
* the front door refuses a non-loopback bind;
* switch blue->green and green->blue update the active-slot pointer, rollback
  is the same mechanism, and a switch never mutates ``runs/`` or ``feed/``;
* the front door, end to end, proxies to the active slot, follows a switch on
  the next request, relays Range/206, and answers 502/503 honestly;
* the launcher / switch scripts contain no installer commands and fail
  cleanly when the runtime is absent.

The proxy integration tests use in-process stub upstream servers on ephemeral
loopback ports — there is no external proxy binary, so these run in the normal
suite with no skips.
"""

from __future__ import annotations

import http.client
import http.server
import subprocess
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import pytest

from storytime.config import load_config
from storytime.frontdoor.active_slot import (
    ActiveSlotError,
    read_active_slot,
    write_active_slot,
)
from storytime.frontdoor.endpoints import SlotEndpoint, build_slot_endpoints
from storytime.frontdoor.proxy import FrontDoorServer
from storytime.frontdoor.switch import SwitchError, switch_active_slot
from storytime.http import UnsafeBindError

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DEPLOY_DIR = _REPO_ROOT / "config" / "deploy"
_SCRIPTS_DIR = _REPO_ROOT / "scripts"


# --------------------------------------------------------------------------
# Test infrastructure: in-process stub upstream + running-server helpers.
# --------------------------------------------------------------------------

def _make_stub_handler(marker: str) -> type[http.server.BaseHTTPRequestHandler]:
    """A stub upstream feed server that identifies itself with *marker*.

    Honours a Range header by answering 206 + Content-Range, so the front
    door's range relay can be exercised.
    """

    class _StubHandler(http.server.BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.0"

        def _body(self) -> bytes:
            return f"feed-from-{marker}".encode()

        def do_GET(self) -> None:  # noqa: N802
            body = self._body()
            range_header = self.headers.get("Range")
            if range_header is not None:
                # bytes=0-3 -> 206 with the first 4 bytes.
                self.send_response(206)
                self.send_header("Content-Type", "application/rss+xml")
                self.send_header("Content-Range", f"bytes 0-3/{len(body)}")
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Content-Length", "4")
                self.send_header("X-Stub-Slot", marker)
                self.end_headers()
                self.wfile.write(body[:4])
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/rss+xml")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Stub-Slot", marker)
            self.end_headers()
            self.wfile.write(body)

        def do_HEAD(self) -> None:  # noqa: N802
            body = self._body()
            self.send_response(200)
            self.send_header("Content-Type", "application/rss+xml")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Stub-Slot", marker)
            self.end_headers()

        def log_message(self, format: str, *args: object) -> None:  # noqa: A002
            return

    return _StubHandler


@contextmanager
def _running(server: http.server.HTTPServer) -> Iterator[int]:
    """Run *server* in a daemon thread; yield its bound port; stop on exit."""
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server.server_address[1]
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


@contextmanager
def _stub_upstream(marker: str) -> Iterator[int]:
    """Run a stub upstream on an ephemeral loopback port; yield the port."""
    server = http.server.ThreadingHTTPServer(
        ("127.0.0.1", 0), _make_stub_handler(marker)
    )
    with _running(server) as port:
        yield port


def _get(port: int, path: str = "/", headers: dict[str, str] | None = None
         ) -> tuple[int, dict[str, str], bytes]:
    """Issue a GET to 127.0.0.1:*port* and return (status, headers, body)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    try:
        conn.request("GET", path, headers=headers or {})
        response = conn.getresponse()
        return (
            response.status,
            {k.lower(): v for k, v in response.getheaders()},
            response.read(),
        )
    finally:
        conn.close()


# --------------------------------------------------------------------------
# Active-slot pointer.
# --------------------------------------------------------------------------

def test_active_slot_accepts_blue(tmp_path: Path) -> None:
    pointer = tmp_path / "active-slot"
    write_active_slot(pointer, "blue")
    assert read_active_slot(pointer).slot == "blue"


def test_active_slot_accepts_green(tmp_path: Path) -> None:
    pointer = tmp_path / "active-slot"
    write_active_slot(pointer, "green")
    assert read_active_slot(pointer).slot == "green"


@pytest.mark.parametrize("bad", ["BLUE", "blue green", "blue!", "", "  "])
def test_active_slot_rejects_invalid_values(tmp_path: Path, bad: str) -> None:
    pointer = tmp_path / "active-slot"
    pointer.write_text(bad, encoding="utf-8")
    with pytest.raises(ActiveSlotError):
        read_active_slot(pointer)


@pytest.mark.parametrize("bad", ["../green", "../../etc/passwd", "blue/green", "/abs", ".hidden"])
def test_active_slot_rejects_traversal_like_values(tmp_path: Path, bad: str) -> None:
    pointer = tmp_path / "active-slot"
    pointer.write_text(bad, encoding="utf-8")
    with pytest.raises(ActiveSlotError):
        read_active_slot(pointer)
    # write must refuse the same unsafe values.
    with pytest.raises(ActiveSlotError):
        write_active_slot(pointer, bad)


def test_active_slot_missing_file_raises_typed_error(tmp_path: Path) -> None:
    """A missing pointer is a typed ActiveSlotError, not an unhandled crash."""
    with pytest.raises(ActiveSlotError):
        read_active_slot(tmp_path / "does-not-exist")


def test_active_slot_write_is_round_trippable(tmp_path: Path) -> None:
    pointer = tmp_path / "nested" / "active-slot"
    state = write_active_slot(pointer, "green")
    assert state.slot == "green"
    assert read_active_slot(pointer).slot == "green"


# --------------------------------------------------------------------------
# Slot endpoint discovery — against the real config/deploy/*.env files.
# --------------------------------------------------------------------------

def test_endpoints_resolve_known_slot_ports() -> None:
    endpoints = build_slot_endpoints(_DEPLOY_DIR)
    assert set(endpoints) == {"blue", "green"}
    assert endpoints["blue"].port == 8000
    assert endpoints["green"].port == 8001


def test_endpoints_point_only_to_loopback_known_slots() -> None:
    """Every discovered endpoint is a known slot on a loopback host."""
    endpoints = build_slot_endpoints(_DEPLOY_DIR)
    for slot, endpoint in endpoints.items():
        assert slot in {"blue", "green"}
        assert endpoint.host in {"127.0.0.1", "localhost", "::1"}
        assert endpoint.slot == slot


# --------------------------------------------------------------------------
# Front-door bind safety.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("unsafe", ["0.0.0.0", "::", ""])
def test_frontdoor_refuses_non_loopback_bind(tmp_path: Path, unsafe: str) -> None:
    with pytest.raises(UnsafeBindError):
        FrontDoorServer(
            host=unsafe,
            port=8080,
            slot_endpoints={},
            active_slot_path=tmp_path / "active-slot",
        )


def test_frontdoor_accepts_loopback_bind(tmp_path: Path) -> None:
    server = FrontDoorServer(
        host="127.0.0.1",
        port=0,
        slot_endpoints={},
        active_slot_path=tmp_path / "active-slot",
    )
    assert server.bind_host == "127.0.0.1"


# --------------------------------------------------------------------------
# Switch / rollback.
# --------------------------------------------------------------------------

def test_switch_blue_to_green_updates_pointer(tmp_path: Path) -> None:
    pointer = tmp_path / "active-slot"
    write_active_slot(pointer, "blue")
    result = switch_active_slot(
        deploy_dir=_DEPLOY_DIR, active_slot_path=pointer, target_slot="green"
    )
    assert result.previous_slot == "blue"
    assert result.new_slot == "green"
    assert result.unchanged is False
    assert read_active_slot(pointer).slot == "green"


def test_switch_green_to_blue_updates_pointer(tmp_path: Path) -> None:
    pointer = tmp_path / "active-slot"
    write_active_slot(pointer, "green")
    result = switch_active_slot(
        deploy_dir=_DEPLOY_DIR, active_slot_path=pointer, target_slot="blue"
    )
    assert result.previous_slot == "green"
    assert result.new_slot == "blue"
    assert read_active_slot(pointer).slot == "blue"


def test_rollback_is_switching_back(tmp_path: Path) -> None:
    """Rollback uses the identical mechanism, targeting the previous slot."""
    pointer = tmp_path / "active-slot"
    write_active_slot(pointer, "blue")
    # switch forward
    switch_active_slot(
        deploy_dir=_DEPLOY_DIR, active_slot_path=pointer, target_slot="green"
    )
    assert read_active_slot(pointer).slot == "green"
    # rollback == switch back
    rollback = switch_active_slot(
        deploy_dir=_DEPLOY_DIR, active_slot_path=pointer, target_slot="blue"
    )
    assert rollback.previous_slot == "green"
    assert rollback.new_slot == "blue"
    assert read_active_slot(pointer).slot == "blue"


def test_switch_to_same_slot_reports_unchanged(tmp_path: Path) -> None:
    pointer = tmp_path / "active-slot"
    write_active_slot(pointer, "blue")
    result = switch_active_slot(
        deploy_dir=_DEPLOY_DIR, active_slot_path=pointer, target_slot="blue"
    )
    assert result.unchanged is True
    assert read_active_slot(pointer).slot == "blue"


def test_switch_rejects_unconfigured_slot(tmp_path: Path) -> None:
    pointer = tmp_path / "active-slot"
    write_active_slot(pointer, "blue")
    with pytest.raises(SwitchError, match="not configured"):
        switch_active_slot(
            deploy_dir=_DEPLOY_DIR, active_slot_path=pointer, target_slot="purple"
        )
    # the pointer is unchanged after a failed switch.
    assert read_active_slot(pointer).slot == "blue"


@pytest.mark.parametrize("unsafe", ["../etc", "blue/green", "Blue", "x y"])
def test_switch_rejects_unsafe_slot(tmp_path: Path, unsafe: str) -> None:
    pointer = tmp_path / "active-slot"
    write_active_slot(pointer, "blue")
    with pytest.raises(SwitchError):
        switch_active_slot(
            deploy_dir=_DEPLOY_DIR, active_slot_path=pointer, target_slot=unsafe
        )


def test_switch_does_not_mutate_slot_state_or_feed_roots(tmp_path: Path) -> None:
    """A switch writes only the pointer — runs/ and feed/ are untouched."""
    pointer = tmp_path / "active-slot"
    write_active_slot(pointer, "blue")

    # Stand in for the inactive slot's preserved state and feed.
    runs_blue = tmp_path / "runs" / "blue"
    feed_green = tmp_path / "feed" / "green"
    runs_blue.mkdir(parents=True)
    feed_green.mkdir(parents=True)
    state_marker = runs_blue / "state.db"
    feed_marker = feed_green / "feed.xml"
    state_marker.write_text("blue-state", encoding="utf-8")
    feed_marker.write_text("green-feed", encoding="utf-8")
    before = {
        state_marker: (state_marker.read_text(), state_marker.stat().st_mtime_ns),
        feed_marker: (feed_marker.read_text(), feed_marker.stat().st_mtime_ns),
    }

    switch_active_slot(
        deploy_dir=_DEPLOY_DIR, active_slot_path=pointer, target_slot="green"
    )

    for path, (content, mtime) in before.items():
        assert path.read_text() == content
        assert path.stat().st_mtime_ns == mtime


def test_switch_with_local_deploy_dir(tmp_path: Path) -> None:
    """switch_active_slot resolves slots from whatever deploy dir it is given."""
    deploy = tmp_path / "deploy"
    deploy.mkdir()
    (deploy / "blue.env").write_text(
        "STORYTIME_HTTP_HOST=127.0.0.1\nSTORYTIME_HTTP_PORT=9000\n",
        encoding="utf-8",
    )
    (deploy / "green.env").write_text(
        "STORYTIME_HTTP_HOST=127.0.0.1\nSTORYTIME_HTTP_PORT=9001\n",
        encoding="utf-8",
    )
    pointer = deploy / "active-slot"
    result = switch_active_slot(
        deploy_dir=deploy, active_slot_path=pointer, target_slot="green"
    )
    assert result.endpoint.port == 9001
    assert read_active_slot(pointer).slot == "green"


# --------------------------------------------------------------------------
# Front-door reverse proxy — end-to-end integration (no external binary).
# --------------------------------------------------------------------------

def test_frontdoor_proxies_to_active_slot_and_follows_a_switch(
    tmp_path: Path,
) -> None:
    """The front door routes to the active slot, and a switch retargets it."""
    pointer = tmp_path / "active-slot"
    write_active_slot(pointer, "blue")

    with _stub_upstream("blue") as blue_port, _stub_upstream("green") as green_port:
        endpoints = {
            "blue": SlotEndpoint("blue", "127.0.0.1", blue_port),
            "green": SlotEndpoint("green", "127.0.0.1", green_port),
        }
        front = FrontDoorServer(
            host="127.0.0.1", port=0,
            slot_endpoints=endpoints, active_slot_path=pointer,
        )
        with _running(front.make_server()) as fd_port:
            # active = blue
            status, headers, body = _get(fd_port)
            assert status == 200
            assert body == b"feed-from-blue"
            assert headers.get("x-stub-slot") == "blue"

            # switch -> green; the running front door follows on next request.
            switch_active_slot(
                deploy_dir=_DEPLOY_DIR,  # only used for validation here
                active_slot_path=pointer,
                target_slot="green",
            )
            status, headers, body = _get(fd_port)
            assert status == 200
            assert body == b"feed-from-green"
            assert headers.get("x-stub-slot") == "green"

            # rollback -> blue.
            write_active_slot(pointer, "blue")
            _, _, body = _get(fd_port)
            assert body == b"feed-from-blue"


def test_frontdoor_relays_range_request(tmp_path: Path) -> None:
    """A Range request is relayed; the upstream 206 + Content-Range pass through."""
    pointer = tmp_path / "active-slot"
    write_active_slot(pointer, "blue")
    with _stub_upstream("blue") as blue_port:
        endpoints = {"blue": SlotEndpoint("blue", "127.0.0.1", blue_port)}
        front = FrontDoorServer(
            host="127.0.0.1", port=0,
            slot_endpoints=endpoints, active_slot_path=pointer,
        )
        with _running(front.make_server()) as fd_port:
            status, headers, body = _get(
                fd_port, headers={"Range": "bytes=0-3"}
            )
    assert status == 206
    assert headers.get("content-range", "").startswith("bytes 0-3/")
    assert body == b"feed"


def test_frontdoor_502_when_active_slot_process_is_down(tmp_path: Path) -> None:
    """An active slot whose feed server is not running yields an honest 502."""
    pointer = tmp_path / "active-slot"
    write_active_slot(pointer, "blue")
    # Point blue at a port nothing is listening on.
    endpoints = {"blue": SlotEndpoint("blue", "127.0.0.1", 9)}
    front = FrontDoorServer(
        host="127.0.0.1", port=0,
        slot_endpoints=endpoints, active_slot_path=pointer,
    )
    with _running(front.make_server()) as fd_port:
        status, _, body = _get(fd_port)
    assert status == 502
    assert b"blue" in body


def test_frontdoor_503_when_active_slot_pointer_is_invalid(tmp_path: Path) -> None:
    """A missing or garbage active-slot pointer yields an honest 503."""
    pointer = tmp_path / "active-slot"  # never created
    front = FrontDoorServer(
        host="127.0.0.1", port=0,
        slot_endpoints={"blue": SlotEndpoint("blue", "127.0.0.1", 8000)},
        active_slot_path=pointer,
    )
    with _running(front.make_server()) as fd_port:
        status, _, body = _get(fd_port)
    assert status == 503
    assert b"active slot" in body


def test_frontdoor_503_when_active_slot_has_no_endpoint(tmp_path: Path) -> None:
    """An active slot with no configured endpoint yields an honest 503."""
    pointer = tmp_path / "active-slot"
    write_active_slot(pointer, "green")  # valid name, but no green endpoint
    front = FrontDoorServer(
        host="127.0.0.1", port=0,
        slot_endpoints={"blue": SlotEndpoint("blue", "127.0.0.1", 8000)},
        active_slot_path=pointer,
    )
    with _running(front.make_server()) as fd_port:
        status, _, body = _get(fd_port)
    assert status == 503
    assert b"green" in body


# --------------------------------------------------------------------------
# Phase 7A behaviour is unchanged.
# --------------------------------------------------------------------------

def test_no_slot_local_behaviour_unchanged() -> None:
    """With no slot, config still resolves the plain runs/ and feed/ layout."""
    config = load_config({})
    assert config.runs_dir == Path("runs")
    assert config.feed_dir == Path("feed")
    assert config.deployment_slot == ""


# --------------------------------------------------------------------------
# Launcher / switch scripts — safety rules validated as data.
# --------------------------------------------------------------------------

_FORBIDDEN_INSTALLER_TOKENS = ("wget", "curl", "apt-get", "pip install", "brew install")


@pytest.mark.parametrize("script_name", ["run-frontdoor.sh", "switch-slot.sh"])
def test_scripts_contain_no_installer_commands(script_name: str) -> None:
    """The Phase 7B scripts must never download or install a binary."""
    text = (_SCRIPTS_DIR / script_name).read_text(encoding="utf-8")
    for token in _FORBIDDEN_INSTALLER_TOKENS:
        assert token not in text, f"{script_name} must not invoke {token!r}"


@pytest.mark.parametrize("script_name", ["run-frontdoor.sh", "switch-slot.sh"])
def test_scripts_are_strict_mode(script_name: str) -> None:
    """The scripts use `set -euo pipefail` so a failure stops them cleanly."""
    text = (_SCRIPTS_DIR / script_name).read_text(encoding="utf-8")
    assert "set -euo pipefail" in text


def test_run_frontdoor_script_fails_cleanly_without_runtime() -> None:
    """run-frontdoor.sh exits non-zero with a clear message if uv is absent.

    Run with a PATH that excludes uv. The script must report the missing
    runtime and exit 2 — it must not hang, crash, or attempt an install.
    """
    result = subprocess.run(
        ["bash", str(_SCRIPTS_DIR / "run-frontdoor.sh")],
        env={"PATH": "/usr/bin:/bin"},
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    assert result.returncode == 2
    assert "uv" in result.stderr
