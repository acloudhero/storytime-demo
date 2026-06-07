"""HTTP serving must bind only to the loopback interface."""

from __future__ import annotations

from pathlib import Path

import pytest

from storytime.http import LocalFeedServer, UnsafeBindError, validate_bind_host


def test_loopback_hosts_are_accepted() -> None:
    assert validate_bind_host("127.0.0.1") == "127.0.0.1"
    assert validate_bind_host("localhost") == "localhost"
    assert validate_bind_host("::1") == "::1"
    assert validate_bind_host(" 127.0.0.1 ") == "127.0.0.1"


def test_all_interfaces_bind_is_rejected() -> None:
    """Negative case: 0.0.0.0 must be refused."""
    with pytest.raises(UnsafeBindError):
        validate_bind_host("0.0.0.0")


def test_ipv6_all_interfaces_bind_is_rejected() -> None:
    with pytest.raises(UnsafeBindError):
        validate_bind_host("::")


def test_empty_host_is_rejected() -> None:
    with pytest.raises(UnsafeBindError):
        validate_bind_host("")


def test_public_address_is_rejected() -> None:
    with pytest.raises(UnsafeBindError):
        validate_bind_host("192.168.1.50")


def test_server_construction_rejects_unsafe_host(tmp_path: Path) -> None:
    with pytest.raises(UnsafeBindError):
        LocalFeedServer(host="0.0.0.0", port=8000, directory=tmp_path)


def test_server_construction_accepts_loopback(tmp_path: Path) -> None:
    server = LocalFeedServer(host="127.0.0.1", port=8000, directory=tmp_path)
    assert server.bind_host == "127.0.0.1"
