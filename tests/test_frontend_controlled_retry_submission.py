"""Phase 13H.1 — controlled retry submission guard tests.

Phase 13H.1 crosses the frontend mutation boundary for the first time, in the
narrowest possible way: a single controlled ``POST /actions`` that submits one
action type — ``retry_failed_stage`` — to the loopback bridge. These
repository-consistent, grep-style static guards lock that boundary:

- the submit path POSTs only to ``/actions`` and uses only ``retry_failed_stage``,
- no arbitrary action-type input and no free-form command / SQL / path field,
- the read-only observability client stays GET-only (no mutation leaked in),
- loopback-only is preserved and no browser durable storage / socket / 3rd-party
  client is used,
- no static-export refresh or cache-busting is introduced,
- a 202 is labelled accepted / queued, never "succeeded",
- submission is wired to an explicit click handler, not a render-driven effect,
- the backend already answers the CORS ``OPTIONS`` preflight for loopback only,
- the static demo fallback and the read-only lifecycle panel remain intact.

Actual TypeScript validity is enforced by ``npm run typecheck`` / ``npm run
build``; phase-state discipline is enforced by ``test_failure_mode_regression``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]
_FE = _REPO_ROOT / "frontend" / "src"
_DATA = _FE / "data"
_COMP = _FE / "components"

_ACTIONS = _DATA / "localBridgeActions.ts"
_SUBMIT_PANEL = _COMP / "LocalRetrySubmitPanel.tsx"
_READONLY_CLIENT = _DATA / "localBridgeClient.ts"
_LIFECYCLE_PANEL = _COMP / "LocalActionLifecyclePanel.tsx"
_VIEW = _COMP / "LocalBridgeView.tsx"
_SERVER = _REPO_ROOT / "src" / "storytime" / "local_bridge" / "server.py"

# Phase 14A.1 added a second controlled mutation surface: the local-live proof
# client POSTs an empty/`{fixture}` body to the loopback `/api/proof-runs`
# endpoint. It is the only mutating call in that client and submits no arbitrary
# input, so it joins the tracked mutation set rather than leaking POST into a
# read-only file.
_LIVE_PROOF_CLIENT = _DATA / "liveProofClient.ts"

# The mutation set: the only files allowed to contain a POST.
_MUTATION_FILES: tuple[Path, ...] = (_ACTIONS, _SUBMIT_PANEL, _LIVE_PROOF_CLIENT)

_MUTATION_METHODS: tuple[str, ...] = ("PUT", "PATCH", "DELETE")

_FORBIDDEN_USAGE: tuple[str, ...] = (
    "localStorage",
    "sessionStorage",
    "IndexedDB",
    "indexedDB",
    "document.cookie",
    "WebSocket",
    "EventSource",
    "XMLHttpRequest",
    "axios",
)

# Other allowlisted / deferred backend actions that must NOT be submittable.
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
    assert path.is_file(), f"expected Phase 13H.1 file missing: {path}"
    return path.read_text(encoding="utf-8")


# ── existence ──────────────────────────────────────────────────────────────


def test_controlled_submit_files_exist() -> None:
    assert _ACTIONS.is_file(), "localBridgeActions.ts is missing"
    assert _SUBMIT_PANEL.is_file(), "LocalRetrySubmitPanel.tsx is missing"


# ── POST only to /actions ────────────────────────────────────────────────────


def test_submit_posts_only_to_actions() -> None:
    source = _read(_ACTIONS)
    assert 'method: "POST"' in source, "submit client does not POST"
    assert "`${baseUrl}/actions`" in source, "submit target is not /actions"
    # Exactly one network call, and it is the single POST.
    assert source.count("fetch(") == 1, "more than one fetch in submit module"
    assert source.count('method: "POST"') == 1, "more than one POST in submit module"
    # The POST target is exactly /actions (not a /actions/{id} sub-path); the
    # only "/actions/" mention is the doc comment about the GET status endpoint.
    assert "fetch(`${baseUrl}/actions/`" not in source
    assert "fetch(`${baseUrl}/actions/${" not in source


def test_no_other_mutation_verbs_in_mutation_files() -> None:
    for path in _MUTATION_FILES:
        source = _read(path)
        for method in _MUTATION_METHODS:
            assert method not in source, f"{path.name} contains verb {method!r}"


def test_post_appears_only_in_mutation_files() -> None:
    """No frontend file outside the mutation set contains an HTTP POST."""
    for path in sorted(_FE.rglob("*.ts")) + sorted(_FE.rglob("*.tsx")):
        if path in _MUTATION_FILES:
            continue
        source = path.read_text(encoding="utf-8")
        assert 'method: "POST"' not in source, (
            f"{path.relative_to(_FE)} performs a POST outside the submit module"
        )


# ── only retry_failed_stage; no arbitrary action input ───────────────────────


def test_only_retry_failed_stage_is_submittable() -> None:
    source = _read(_ACTIONS)
    assert 'RETRY_FAILED_STAGE = "retry_failed_stage"' in source, (
        "the single action constant is missing"
    )
    assert "action: RETRY_FAILED_STAGE" in source, (
        "submitted action is not pinned to the constant"
    )
    for other in _OTHER_ACTIONS:
        assert other not in source, (
            f"submit module references another action type {other!r}"
        )


def test_no_arbitrary_action_type_input_exposed() -> None:
    """The submit panel exposes constrained fields only — no action selector and
    no free-form command / SQL / shell / path input. The action type is a
    hardcoded constant in the submit module, never a UI input."""
    panel = _read(_SUBMIT_PANEL)
    # No action-type input / selector of any kind.
    assert "actionType" not in panel
    assert "<select" not in panel, "submit panel exposes an action selector"
    # The only inputs are the three constrained, contract-shaped fields.
    for field_id in ('id="retry-run-id"', 'id="retry-stage-id"', 'id="retry-intent"'):
        assert field_id in panel, f"submit panel missing constrained field {field_id}"
    # No free-form command / SQL / path input attributes (id / placeholder).
    lowered = panel.lower()
    for attr in ('id="command', 'id="shell', 'id="sql', 'id="path', 'id="filepath'):
        assert attr not in lowered, f"submit panel exposes a forbidden input {attr!r}"


# ── read-only observability stays GET-only ───────────────────────────────────


def test_readonly_client_stays_get_only() -> None:
    source = _read(_READONLY_CLIENT)
    assert 'method: "GET"' in source
    for method in ("POST", "PUT", "PATCH", "DELETE"):
        assert method not in source, (
            f"read-only client leaked a mutation method {method!r}"
        )


# ── loopback-only / no storage / no sockets / no 3rd-party ───────────────────


def test_submit_is_loopback_only() -> None:
    source = _read(_ACTIONS)
    assert "isLoopbackBridgeUrl" in source, "submit does not reuse the loopback guard"
    assert "blockedNonLoopback" in source, "submit does not refuse non-loopback URLs"
    for forbidden in ("https://", "0.0.0.0", "192.168", "10.0.0"):
        assert forbidden not in source, (
            f"submit module references non-loopback literal {forbidden!r}"
        )


@pytest.mark.parametrize("path", _MUTATION_FILES, ids=lambda p: p.name)
def test_no_durable_storage_or_sockets(path: Path) -> None:
    source = _read(path)
    for marker in _FORBIDDEN_USAGE:
        assert marker not in source, f"{path.name} uses forbidden API {marker!r}"


# ── no export refresh / cache-busting ────────────────────────────────────────


def test_no_export_refresh_or_cache_busting() -> None:
    for path in _MUTATION_FILES:
        source = _read(path)
        assert "storytime-demo-export" not in source, (
            f"{path.name} references the static export file"
        )
        for buster in ("cache-bust", "cachebust", "?t=", "Date.now() +"):
            assert buster not in source, f"{path.name} looks like a cache-buster"
    # The submit module explicitly disclaims touching the export.
    assert "never touches the static export" in _read(_ACTIONS)


# ── acceptance is not success ────────────────────────────────────────────────


def test_202_labelled_accepted_not_successful() -> None:
    panel = _read(_SUBMIT_PANEL)
    assert "acceptance is not success" in panel.lower(), (
        "submit panel does not state acceptance is not success"
    )
    # It must not claim the retry itself succeeded on a mere accept.
    for success_lie in ("retry succeeded", "retry complete", "successfully retried"):
        assert success_lie not in panel.lower(), (
            f"submit panel falsely claims success: {success_lie!r}"
        )


# ── submission tied to explicit handler, not an effect ───────────────────────


def test_submission_is_click_driven_not_effect_driven() -> None:
    panel = _read(_SUBMIT_PANEL)
    view = _read(_VIEW)
    # The panel's button triggers submission via onClick.
    assert "onClick={onSubmit}" in panel, "submit button is not click-driven"
    # The view drives the submit only from the panel's onSubmit callback.
    assert "void submitRetry()" in view
    # The only effect in the view is the unmount guard — its body must not submit.
    # Anchor on the effect CALL site (not the `useEffect` import token).
    effect_body = view.split("useEffect(() =>", 1)[1].split("}, [])", 1)[0]
    assert "submitRetry" not in effect_body, (
        "submitRetry appears inside a useEffect body (render-driven submission)"
    )
    assert "fetch(" not in effect_body and "submit" not in effect_body.lower(), (
        "the view's effect performs a network/submit side effect"
    )


# ── backend OPTIONS preflight already supported (loopback-only) ──────────────


def test_backend_handles_options_preflight_loopback_only() -> None:
    server = _read(_SERVER)
    assert "def do_OPTIONS" in server, "bridge has no OPTIONS handler"
    assert "Access-Control-Allow-Methods" in server
    assert "POST" in server and "OPTIONS" in server
    # Never a wildcard origin.
    assert '"*"' not in server, "bridge emits a wildcard origin"
    assert "origin_forbidden" in server, "OPTIONS does not fail closed on bad origin"


# ── static demo & read-only lifecycle intact ─────────────────────────────────


def test_static_demo_fallback_intact() -> None:
    app = _read(_FE / "App.tsx")
    assert "Static demo build" in app
    # The submit module never throws — every failure is a typed result.
    actions = _read(_ACTIONS)
    assert "ok: false" in actions and "kind:" in actions


def test_lifecycle_panel_remains_read_only() -> None:
    panel = _read(_LIFECYCLE_PANEL)
    for method in ("POST", "PUT", "PATCH", "DELETE"):
        assert method not in panel, f"lifecycle panel gained a mutation verb {method!r}"
    for creator in ("randomUUID", "crypto.", "Math.random"):
        assert creator not in panel, f"lifecycle panel creates an id via {creator!r}"


# ── stale Phase 13H.1-era wording must not regress (Phase 13H.2 cleanup) ─────

# The six read-only "constrained" files (the same set guarded by
# tests/test_frontend_bridge_observability.py) must never again describe browser
# submission as a *future / deferred* step. The single controlled submission
# landed in locked Phase 13H.1 and now lives in localBridgeActions.ts /
# LocalRetrySubmitPanel.tsx, so these read-only surfaces must describe the
# boundary as it is today. Honest panel-scoped copy ("this status panel submits
# nothing; the only browser-initiated submission is the Controlled local retry
# request panel") and the export / read-model deferral to the not-started Phase
# 13H.3 are both fine; what must stay gone is any claim that *submission itself*
# is deferred to Phase 13H.1.
_READONLY_CONSTRAINED_FILES: tuple[Path, ...] = (
    _DATA / "localBridgeClient.ts",
    _DATA / "localBridgeTypes.ts",
    _COMP / "LocalBridgeStatusPanel.tsx",
    _COMP / "LocalQueueStatusPanel.tsx",
    _LIFECYCLE_PANEL,
    _VIEW,
)

_STALE_SUBMISSION_DEFERRAL_WORDING: tuple[str, ...] = (
    "deferred to Phase 13H.1",
    "submission is deferred",
    "action submission is deferred",
    "submits nothing; frontend action submission",
    "frontend action submission is deferred",
    "Local Bridge view submits nothing",
)


@pytest.mark.parametrize(
    "path", _READONLY_CONSTRAINED_FILES, ids=lambda p: p.name
)
def test_no_stale_submission_deferral_wording(path: Path) -> None:
    """Read-only files no longer claim submission is deferred to Phase 13H.1.

    Regression guard for the Phase 13H.2 boundary cleanup: the controlled
    submission landed in locked Phase 13H.1, so these read-only surfaces must
    describe a GET-only client whose single sibling submission path lives in
    localBridgeActions.ts — not a future Phase 13H.1 step. The export /
    read-model deferral to the not-started Phase 13H.3 and the honest
    panel-scoped "submits nothing" copy are intentionally unaffected.
    """
    text = _read(path)
    for phrase in _STALE_SUBMISSION_DEFERRAL_WORDING:
        assert phrase not in text, (
            f"{path.name} still contains stale submission-deferral wording: "
            f"{phrase!r}"
        )
