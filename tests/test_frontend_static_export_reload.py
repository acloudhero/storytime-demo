"""Phase 13H.3 — manual static export reload / read-model replacement guards.

Phase 13H.3 adds a manual, operator-triggered way to reload the committed
static export snapshot and replace the frontend's transient in-memory read
model. These are repository-consistent, grep-style static guards (no JS
runtime, no browser, no dev server), in the same style as the Phase 13H /
13H.1 / 13H.2 frontend guards. They lock the safety boundary:

- manual reload exists and is triggered only by an explicit operator action,
- there is no auto-reload on mount, no polling, no interval, no socket,
- no browser durable storage is used,
- the reload fetch is limited to the known committed static export asset, with
  no operator-supplied / arbitrary URL,
- any cache-busting is limited to that one static-export fetch,
- invalid / partial / empty / schema-incompatible exports are rejected and the
  previous in-memory snapshot is retained (all-or-nothing replacement),
- the local bridge boundary is unchanged: ``localBridgeClient.ts`` stays
  GET-only, ``localBridgeActions.ts`` stays the only controlled POST path, and
  ``retry_failed_stage`` stays the only submittable action,
- no full Local mode / cloud overclaim wording is introduced,
- export reload and retry submission stay separate operator actions.

TypeScript validity is enforced separately by ``npm run typecheck`` and
``npm run build``.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]
_FE = _REPO_ROOT / "frontend" / "src"
_DATA = _FE / "data"
_COMP = _FE / "components"

_RELOAD_MODULE = _DATA / "staticExportReload.ts"
_RELOAD_PANEL = _COMP / "StaticExportReloadPanel.tsx"
_VIEW = _COMP / "LocalBridgeView.tsx"
_CLIENT = _DATA / "localBridgeClient.ts"
_ACTIONS = _DATA / "localBridgeActions.ts"
_LIFECYCLE = _COMP / "LocalActionLifecyclePanel.tsx"

_EXPORT_BASENAME = "storytime-demo-export.json"

# Browser-durable / live-integration APIs that must never appear in the new
# Phase 13H.3 reload surface.
_FORBIDDEN_RUNTIME: tuple[str, ...] = (
    "localStorage",
    "sessionStorage",
    "indexedDB",
    "IndexedDB",
    "document.cookie",
    "WebSocket",
    "EventSource",
    "setInterval",
    "ServiceWorker",
    "serviceWorker",
    "caches.open",
    "caches.match",
)

# Overclaiming reload labels the prompt explicitly forbids.
_FORBIDDEN_LABELS: tuple[str, ...] = (
    "Sync local mode",
    "Refresh live backend",
    "Apply retry result",
    "Update database",
    "Complete local workflow",
)

# Other allowlisted / deferred backend actions that must NOT be referenced by
# the reload surface (only retry_failed_stage is submittable, and the reload
# module submits nothing at all).
_OTHER_ACTIONS: tuple[str, ...] = (
    "inspect_trust_envelope",
    "refresh_export",
    "refresh_static_export",
    "record_review_decision",
    "regenerate_operator_report",
    "publish_episode",
    "delete_artifact",
    "provider_sync",
)


def _read(path: Path) -> str:
    assert path.is_file(), f"expected Phase 13H.3 file missing: {path}"
    return path.read_text(encoding="utf-8")


# ── existence ────────────────────────────────────────────────────────────────


def test_reload_module_and_panel_exist() -> None:
    assert _RELOAD_MODULE.is_file(), "staticExportReload.ts is missing"
    assert _RELOAD_PANEL.is_file(), "StaticExportReloadPanel.tsx is missing"


# ── 1. manual, user-triggered reload ─────────────────────────────────────────


def test_reload_is_user_triggered_onclick() -> None:
    """The panel triggers reload only from a button onClick handler."""
    panel = _read(_RELOAD_PANEL)
    assert "onClick=" in panel, "reload panel has no onClick affordance"
    assert "handleReload" in panel, "reload panel has no reload handler"
    assert "reloadStaticExport" in panel, (
        "reload panel never calls the reload adapter"
    )
    # The button calls the handler.
    assert re.search(r"onClick=\{\s*\(\)\s*=>\s*\{\s*void handleReload\(\)",
                     panel), "reload is not wired to the button onClick"


def test_panel_has_reload_button_label() -> None:
    """The affordance uses an honest reload label, not an overclaiming one."""
    panel = _read(_RELOAD_PANEL)
    assert "Reload static export snapshot" in panel


# ── 2/3/4. no auto-reload, no polling, no sockets ────────────────────────────


def test_no_auto_reload_on_mount() -> None:
    """No effect-driven or load-time reload: the panel uses no useEffect, and
    the module does not invoke its own reload at import time."""
    panel = _read(_RELOAD_PANEL)
    assert "useEffect" not in panel, "reload panel must not use useEffect"
    module = _read(_RELOAD_MODULE)
    # The function is defined exactly once and never invoked within its own
    # module (no module-scope / import-time reload).
    assert module.count("reloadStaticExport") == 1, (
        "reload module should only define reloadStaticExport, never call it"
    )
    assert "export async function reloadStaticExport(" in module, (
        "reloadStaticExport is not the single exported definition"
    )


@pytest.mark.parametrize("path", [_RELOAD_MODULE, _RELOAD_PANEL], ids=lambda p: p.name)
def test_no_polling_interval_or_sockets(path: Path) -> None:
    text = _read(path)
    for token in _FORBIDDEN_RUNTIME:
        assert token not in text, f"{path.name} uses forbidden runtime API {token!r}"


def test_single_timer_is_a_bounded_abort_only() -> None:
    """The module's only setTimeout is a single bounded abort deadline that is
    cleared — not a recurring schedule or polling loop."""
    module = _read(_RELOAD_MODULE)
    assert "setInterval" not in module
    assert module.count("setTimeout(") <= 1, (
        "reload module schedules more than one timer"
    )
    assert "clearTimeout(" in module, "the abort deadline is never cleared"


# ── 5. no browser durable storage ────────────────────────────────────────────


@pytest.mark.parametrize("path", [_RELOAD_MODULE, _RELOAD_PANEL], ids=lambda p: p.name)
def test_no_browser_durable_storage(path: Path) -> None:
    text = _read(path)
    for token in ("localStorage", "sessionStorage", "indexedDB", "IndexedDB",
                  "document.cookie", "history.pushState", "history.replaceState"):
        assert token not in text, f"{path.name} writes durable browser state via {token!r}"


# ── 6/7. fetch limited to the known static export; no arbitrary URL ──────────


def test_fetch_limited_to_static_export_asset() -> None:
    """The reload fetch targets only the committed static export asset, resolved
    at build time from import.meta.url — never an operator-supplied URL."""
    module = _read(_RELOAD_MODULE)
    assert _EXPORT_BASENAME in module, "reload module does not reference the export"
    assert "import.meta.url" in module, (
        "reload module does not resolve the build-time asset URL"
    )
    assert module.count("fetch(") == 1, (
        "reload module should perform exactly one fetch"
    )
    # The fetched URL is built from the fixed asset constant, not a parameter.
    assert "STATIC_EXPORT_ASSET_URL" in module


def test_no_arbitrary_url_input() -> None:
    """No operator-typed URL: the panel exposes no input field, and the reload
    adapter takes no URL argument."""
    panel = _read(_RELOAD_PANEL)
    assert "<input" not in panel, "reload panel must not expose a URL input"
    assert "fetch(" not in panel, "reload panel must fetch only via the adapter"
    module = _read(_RELOAD_MODULE)
    # reloadStaticExport accepts only an optional abort signal, never a URL.
    signature = re.search(
        r"export async function reloadStaticExport\(([^)]*)\)", module
    )
    assert signature is not None, "reloadStaticExport signature not found"
    assert "url" not in signature.group(1).lower(), (
        "reloadStaticExport must not accept a URL argument"
    )


# ── 8. cache-busting limited to the static export reload ─────────────────────


def test_cache_busting_limited_to_static_export_reload() -> None:
    module = _read(_RELOAD_MODULE)
    assert "reload=" in module and "Date.now()" in module, (
        "static export reload does not apply its documented cache-bust param"
    )
    # No other bridge module applies cache-busting.
    for other in (_CLIENT, _ACTIONS):
        text = _read(other)
        assert "reload=" not in text and "?t=" not in text, (
            f"{other.name} unexpectedly applies a cache-bust param"
        )


# ── 9/10/11. validate, retain-on-failure, all-or-nothing ─────────────────────


def test_invalid_exports_are_rejected() -> None:
    """The validator returns null for bad shapes and the fetch maps that to a
    typed rejection rather than a partial result."""
    module = _read(_RELOAD_MODULE)
    assert "deriveValidatedReadModel" in module
    # The validator bails out (returns null) on shape failures.
    assert module.count("return null;") >= 5, (
        "validator does not reject enough malformed-shape cases"
    )
    assert 'kind: "schema"' in module, "no typed schema-rejection result"
    assert 'kind: "parse"' in module, "no typed parse-rejection result"
    assert 'kind: "empty"' in module, "no typed empty-rejection result"


def test_previous_snapshot_retained_on_failure() -> None:
    """On a failed reload the panel keeps the previous read model and only flips
    status / source — it never clears or partially mutates the snapshot."""
    panel = _read(_RELOAD_PANEL)
    assert "retained-after-failure" in panel, (
        "panel does not mark a retained snapshot after failure"
    )
    # setReadModel is called only in the success branch (see all-or-nothing).
    assert panel.count("setReadModel(") == 1, (
        "panel mutates the read model outside the single success replacement"
    )


def test_all_or_nothing_replacement() -> None:
    """Replacement is wholesale on success only; there is no partial merge."""
    panel = _read(_RELOAD_PANEL)
    assert "if (result.ok)" in panel, "panel does not branch on a typed result"
    # The single setReadModel call replaces with the whole validated model.
    assert "setReadModel(result.readModel)" in panel, (
        "panel does not replace the snapshot wholesale on success"
    )
    module = _read(_RELOAD_MODULE)
    for merge in ("Object.assign", "...prev", "...current", "spread"):
        assert merge not in module, f"reload module appears to merge data via {merge!r}"


# ── 12/13/14/15. bridge boundary unchanged ───────────────────────────────────


def test_client_stays_get_only() -> None:
    client = _read(_CLIENT)
    for method in ("POST", "PUT", "PATCH", "DELETE"):
        assert method not in client, f"localBridgeClient.ts gained mutation verb {method!r}"
    assert "GET" in client or "method" not in client.lower()


def test_actions_is_the_only_post_path() -> None:
    """POST appears in localBridgeActions.ts, and not in the reload surface."""
    assert "POST" in _read(_ACTIONS), "localBridgeActions.ts lost its POST path"
    for path in (_RELOAD_MODULE, _RELOAD_PANEL, _CLIENT):
        text = _read(path)
        for method in ("POST", "PUT", "PATCH", "DELETE"):
            assert method not in text, (
                f"{path.name} unexpectedly contains mutation verb {method!r}"
            )


def test_reload_surface_does_not_submit_or_add_actions() -> None:
    """The reload module/panel submit nothing and add no action type."""
    for path in (_RELOAD_MODULE, _RELOAD_PANEL):
        text = _read(path)
        assert "localBridgeActions" not in text, (
            f"{path.name} must not import the controlled submission module"
        )
        assert "submitRetryFailedStage" not in text
        for action in _OTHER_ACTIONS:
            assert action not in text, (
                f"{path.name} references a non-allowlisted action {action!r}"
            )


def test_only_retry_failed_stage_remains_submittable() -> None:
    """The single submittable action is still retry_failed_stage, owned by the
    actions module — unchanged by this phase."""
    actions = _read(_ACTIONS)
    assert "retry_failed_stage" in actions
    for action in _OTHER_ACTIONS:
        assert action not in actions, (
            f"localBridgeActions.ts gained a non-allowlisted action {action!r}"
        )


# ── 16. no full Local mode overclaim ─────────────────────────────────────────


@pytest.mark.parametrize("path", [_RELOAD_MODULE, _RELOAD_PANEL], ids=lambda p: p.name)
def test_no_overclaim_labels(path: Path) -> None:
    text = _read(path)
    for label in _FORBIDDEN_LABELS:
        assert label not in text, f"{path.name} uses overclaiming label {label!r}"
    lowered = text.lower()
    # "full local mode" may appear only as a deferral, never as a claim.
    idx = lowered.find("full local mode")
    if idx != -1:
        window = lowered[idx : idx + 80]
        assert "deferred" in window or "remain" in window, (
            f"{path.name} claims full Local mode without a deferral cue"
        )


# ── 17. reload and retry stay separate; reload is honest ─────────────────────


def test_reload_does_not_imply_retry_success() -> None:
    """Copy keeps export reload and retry submission as separate actions and
    does not claim a reload proves a retry succeeded."""
    panel = _read(_RELOAD_PANEL)
    lowered = panel.lower()
    assert "does not prove a retry succeeded" in lowered or (
        "reloading the snapshot does not prove" in lowered
    ), "panel does not separate reload from retry success"
    assert "non-durable" in lowered, "panel does not state the browser is non-durable"


def test_view_wires_the_reload_panel() -> None:
    view = _read(_VIEW)
    assert "StaticExportReloadPanel" in view, (
        "LocalBridgeView does not render the reload panel"
    )
