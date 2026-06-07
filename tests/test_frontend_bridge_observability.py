"""Phase 13H — frontend bridge observability guard tests.

Phase 13H introduces the first frontend network boundary: a read-only,
loopback-only local-bridge client and three observability panels. These tests
are repository-consistent, grep-style static guards (no JS runtime, no browser,
no dev server) that lock the safety boundary:

- the bridge client uses GET only and no mutation method,
- there is no ``POST /actions`` / submission anywhere in the new frontend code,
- the new code uses no browser durable storage, no WebSocket/EventSource, and
  no third-party HTTP client,
- the client refuses non-loopback URLs,
- the queue adapter covers every observable gauge,
- the action-lifecycle adapter covers every lifecycle state,
- the lifecycle panel never creates or submits an action,
- the retry / lifecycle copy keeps acceptance distinct from success and keeps
  the static export refresh / read-model replacement deferred to the
  not-started Phase 13H.3 (the controlled submission itself already landed in
  locked Phase 13H.1 and lives in ``localBridgeActions.ts``),
- the static demo remains first-class and disabled high-risk actions stay
  disabled,
- the Local Bridge view is wired into the plain-state navigation.

The actual TypeScript validity is enforced separately by ``npm run typecheck``
and ``npm run build``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]
_FE = _REPO_ROOT / "frontend" / "src"
_DATA = _FE / "data"
_COMP = _FE / "components"

_CLIENT = _DATA / "localBridgeClient.ts"
_TYPES = _DATA / "localBridgeTypes.ts"
_STATUS_PANEL = _COMP / "LocalBridgeStatusPanel.tsx"
_QUEUE_PANEL = _COMP / "LocalQueueStatusPanel.tsx"
_LIFECYCLE_PANEL = _COMP / "LocalActionLifecyclePanel.tsx"
_VIEW = _COMP / "LocalBridgeView.tsx"

# Every new Phase 13H frontend source file.
_NEW_FILES: tuple[Path, ...] = (
    _CLIENT,
    _TYPES,
    _STATUS_PANEL,
    _QUEUE_PANEL,
    _LIFECYCLE_PANEL,
    _VIEW,
)

# HTTP mutation methods (case-sensitive uppercase tokens, as they would appear
# in a fetch ``method`` option). GET is the only method the bridge client uses.
_MUTATION_METHODS: tuple[str, ...] = ("POST", "PUT", "PATCH", "DELETE")

# Browser durable storage / live-socket / third-party-client usage markers.
_FORBIDDEN_USAGE: tuple[str, ...] = (
    "localStorage",
    "sessionStorage",
    "IndexedDB",
    "indexedDB",
    "WebSocket",
    "EventSource",
    "XMLHttpRequest",
    "axios",
    "from \"got\"",
    "superagent",
)


def _read(path: Path) -> str:
    assert path.is_file(), f"expected Phase 13H frontend file missing: {path}"
    return path.read_text(encoding="utf-8")


# ── existence ──────────────────────────────────────────────────────────────


@pytest.mark.parametrize("path", _NEW_FILES, ids=lambda p: p.name)
def test_new_frontend_file_exists(path: Path) -> None:
    assert path.is_file(), f"missing {path.name}"


# ── GET-only / no mutation methods ──────────────────────────────────────────


def test_bridge_client_uses_get_only() -> None:
    source = _read(_CLIENT)
    assert 'method: "GET"' in source, "bridge client does not pin method to GET"
    for method in _MUTATION_METHODS:
        assert method not in source, (
            f"bridge client contains mutation method {method!r}"
        )


@pytest.mark.parametrize("path", _NEW_FILES, ids=lambda p: p.name)
def test_no_mutation_methods_in_new_frontend(path: Path) -> None:
    source = _read(path)
    for method in _MUTATION_METHODS:
        assert method not in source, (
            f"{path.name} contains mutation method token {method!r}"
        )


def test_no_post_actions_submission_anywhere() -> None:
    """No new frontend file submits to /actions; the only /actions use is the
    read-only GET status path."""
    for path in _NEW_FILES:
        source = _read(path)
        # The only permitted /actions reference is the GET status sub-path.
        if "/actions" in source:
            assert "/actions/" in source, (
                f"{path.name} references /actions outside the GET status path"
            )
        for method in _MUTATION_METHODS:
            assert method not in source, f"{path.name} contains {method!r}"


# ── no browser storage / sockets / third-party client ───────────────────────


@pytest.mark.parametrize("path", _NEW_FILES, ids=lambda p: p.name)
def test_no_forbidden_usage_in_new_frontend(path: Path) -> None:
    source = _read(path)
    for marker in _FORBIDDEN_USAGE:
        assert marker not in source, (
            f"{path.name} contains forbidden usage {marker!r}"
        )


# ── loopback-only ────────────────────────────────────────────────────────────


def test_bridge_client_is_loopback_only() -> None:
    source = _read(_CLIENT)
    assert "isLoopbackBridgeUrl" in source, "missing loopback URL guard"
    assert "127.0.0.1" in source and "localhost" in source, (
        "loopback hosts not referenced"
    )
    # No https / all-interfaces / LAN literals in the client.
    for forbidden in ("https://", "0.0.0.0", "192.168", "10.0.0", "http://0"):
        assert forbidden not in source, (
            f"bridge client references non-loopback literal {forbidden!r}"
        )
    # The default base URL is an http loopback origin.
    assert 'DEFAULT_BRIDGE_BASE_URL = "http://127.0.0.1' in source


def test_loopback_guard_requires_http_scheme() -> None:
    source = _read(_CLIENT)
    assert 'parsed.protocol !== "http:"' in source, (
        "loopback guard does not reject non-http schemes"
    )


# ── safe error states ────────────────────────────────────────────────────────


def test_client_models_all_safe_error_states() -> None:
    source = _read(_CLIENT) + _read(_TYPES)
    for kind in (
        "blockedNonLoopback",
        "unavailable",
        "timeout",
        "originRejected",
        "httpError",
        "malformed",
        "unexpectedSchema",
    ):
        assert kind in source, f"client/types do not model error state {kind!r}"
    # 403 origin rejection and an abort-based timeout are handled explicitly.
    assert "403" in _read(_CLIENT)
    assert "AbortController" in _read(_CLIENT) and "AbortError" in _read(_CLIENT)


# ── adapters cover the contract ──────────────────────────────────────────────


def test_queue_adapter_covers_all_gauges() -> None:
    source = _read(_CLIENT)
    for field in (
        "queueDepth",
        "inFlightCount",
        "completedCount",
        "failedCount",
        "rejectedCount",
        "deadLetterCount",
        "oldestQueuedAgeSeconds",
        "longestInFlightAgeSeconds",
        "capacity",
        "saturationRatio",
        "maxConcurrency",
    ):
        assert field in source, f"queue adapter missing gauge {field!r}"


def test_lifecycle_adapter_covers_all_states() -> None:
    source = _read(_CLIENT) + _read(_TYPES)
    for state in (
        "accepted",
        "queued",
        "running",
        "completed",
        "failed",
        "rejected",
        "not_implemented",
    ):
        assert state in source, f"lifecycle vocabulary missing {state!r}"
    # An unrecognised state falls back to a non-success ``unknown``.
    assert "unknown" in source


# ── lifecycle panel never creates / submits an action ────────────────────────


def test_lifecycle_panel_does_not_create_or_submit_actions() -> None:
    source = _read(_LIFECYCLE_PANEL)
    for creator in ("randomUUID", "crypto.", "Math.random", "new_ulid", "uuid("):
        assert creator not in source, (
            f"lifecycle panel appears to create an id via {creator!r}"
        )
    for method in _MUTATION_METHODS:
        assert method not in source
    # It observes an EXISTING id only.
    assert "existing" in source.lower()


def test_controlled_retry_area_distinguishes_acceptance() -> None:
    """The retry/lifecycle copy keeps acceptance distinct from success and keeps
    the read-only lifecycle panel from owning the static export read model (the
    controlled submission landed in locked Phase 13H.1; the manual static export
    reload / read-model replacement is owned by the separate Phase 13H.3
    StaticExportReloadPanel, while Full Local / Cloud-Distributed mode stay
    deferred). The 'deferred' + 'export' cue therefore still appears across the
    lifecycle panel and view copy."""
    blob = _read(_LIFECYCLE_PANEL) + _read(_VIEW)
    assert "Acceptance is not success" in blob
    assert "deferred" in blob.lower() and "export" in blob.lower(), (
        "copy no longer distinguishes the deferred modes from the static export"
    )
    # Lifecycle observation is framed as separate from submission.
    assert "separate from submission" in blob.lower() or (
        "only observes" in blob.lower()
    )


# ── static demo remains first-class; disabled actions stay disabled ──────────


def test_static_demo_still_first_class() -> None:
    app = _read(_FE / "App.tsx")
    assert "Static demo build" in app, "demo banner removed from App"
    assert "DemoWalkthroughView" in app, "Demo Walkthrough no longer wired in App"


def test_disabled_future_actions_remain_disabled() -> None:
    card = _read(_COMP / "DisabledFutureActionCard.tsx")
    assert "disabled={true}" in card, (
        "DisabledFutureActionCard no longer renders a natively-disabled button"
    )
    assert "never accepts" in card, (
        "DisabledFutureActionCard lost its no-callback guarantee wording"
    )


# ── navigation wiring ─────────────────────────────────────────────────────────


def test_local_bridge_view_wired_into_navigation() -> None:
    nav = _read(_FE / "navigation.ts")
    app = _read(_FE / "App.tsx")
    assert '"bridge"' in nav, "navigation View union missing the bridge view"
    assert 'id: "bridge"' in nav, "NAV missing the Local Bridge entry"
    assert "Local Bridge" in nav, "NAV missing the Local Bridge label"
    assert 'case "bridge"' in app, "App.renderView missing the bridge case"
    assert "LocalBridgeView" in app, "App does not render LocalBridgeView"
