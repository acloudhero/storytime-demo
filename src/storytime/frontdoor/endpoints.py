"""Slot endpoint discovery — where each blue/green slot's feed server listens.

The front door forwards to the *active* slot's loopback feed port. Those ports
are not a new source of truth: each slot already declares its
``STORYTIME_HTTP_HOST`` / ``STORYTIME_HTTP_PORT`` in
``config/deploy/<slot>.env`` (Phase 7A). ``build_slot_endpoints`` reads those
files so the env files stay authoritative — the front door never hard-codes a
slot's port.

The env-file reader here is a deliberately tiny ``KEY=VALUE`` parser: it does
no shell evaluation, no interpolation, and no command execution, so loading a
slot's endpoint can never run code.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from storytime.config import is_valid_slot_name
from storytime.http import validate_bind_host


class SlotEndpointError(ValueError):
    """Raised when a slot's deploy env file does not yield a usable endpoint."""


@dataclass(frozen=True, slots=True)
class SlotEndpoint:
    """Where one slot's feed HTTP server listens (loopback host + port)."""

    slot: str
    host: str
    port: int

    @property
    def address(self) -> str:
        """The ``host:port`` the front door dials for this slot."""
        return f"{self.host}:{self.port}"


def _read_env_file(path: Path) -> dict[str, str]:
    """Parse a ``config/deploy/<slot>.env`` file into a plain dict.

    Skips blank lines and ``#`` comments; splits each remaining line on its
    first ``=``. No shell evaluation, no interpolation — an injection-free
    reader. A line without ``=`` is ignored.
    """
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            continue
        key, _, value = stripped.partition("=")
        values[key.strip()] = value.strip()
    return values


def build_slot_endpoints(deploy_dir: Path) -> dict[str, SlotEndpoint]:
    """Discover every slot's feed endpoint from ``config/deploy/<slot>.env``.

    Each ``*.env`` file under *deploy_dir* names a slot (the filename stem) and
    declares ``STORYTIME_HTTP_HOST`` / ``STORYTIME_HTTP_PORT``. A file whose
    stem is not a safe slot name is skipped. The resolved host is run through
    ``validate_bind_host`` so the front door can only ever forward to a
    *loopback* upstream — forwarding to a routable host would be a network
    egress StoryTime forbids.

    Raises ``SlotEndpointError`` for a slot env file that exists but has no
    usable integer port, so a misconfigured slot fails loudly at front-door
    startup rather than silently disappearing.
    """
    endpoints: dict[str, SlotEndpoint] = {}
    for env_path in sorted(deploy_dir.glob("*.env")):
        slot = env_path.stem
        if not is_valid_slot_name(slot):
            continue
        values = _read_env_file(env_path)
        host = values.get("STORYTIME_HTTP_HOST", "127.0.0.1")
        port_raw = values.get("STORYTIME_HTTP_PORT", "").strip()
        if not port_raw:
            raise SlotEndpointError(
                f"slot {slot!r} env file {env_path} has no STORYTIME_HTTP_PORT"
            )
        try:
            port = int(port_raw)
        except ValueError as exc:
            raise SlotEndpointError(
                f"slot {slot!r} env file {env_path} has a non-integer "
                f"STORYTIME_HTTP_PORT {port_raw!r}"
            ) from exc
        # The front door forwards only to a loopback upstream.
        loopback_host = validate_bind_host(host)
        endpoints[slot] = SlotEndpoint(slot=slot, host=loopback_host, port=port)
    return endpoints
