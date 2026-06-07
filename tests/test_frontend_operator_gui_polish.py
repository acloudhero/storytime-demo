"""Phase 13J — operator GUI polish / read-only TTS understanding guards.

Repository-consistent, grep-style static guards (no JS runtime, no browser, no
dev server), in the same style as the Phase 13H/13H.1/13H.3 frontend guards.
They lock the Phase 13J boundary: the operator-console polish and the READ-ONLY
governed-TTS-proof understanding add no execution path and no unsafe control,
and the honest framing is preserved.

Specifically:

- the new presentation content and components exist and are wired into the
  Overview (mode overview + boundary legend) and the Local Bridge surface
  (operator workflow + read-only TTS proof summary),
- the new components add no Generate-audio button, no ``generate_tts`` action,
  no new POST path, no file / directory / URL / credential input, and no
  provider-selection control,
- the new components use no browser durable storage, no WebSocket / EventSource
  / polling, and no render-driven effect (they are purely presentational, with
  no event handlers at all),
- the TTS copy is read-only / proof / mock / backend-owned, the real provider
  is described as deferred / disabled (never active), mock output is not
  described as real provider audio, an accepted retry is not described as
  completed, and a manual reload is not described as a live sync,
- full Local mode and Cloud / Distributed mode are not claimed active.

TypeScript validity is enforced separately by ``npm run typecheck`` and
``npm run build``; phase-state discipline is enforced by
``test_failure_mode_regression``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]
_FE = _REPO_ROOT / "frontend" / "src"
_DATA = _FE / "data"
_COMP = _FE / "components"

_CONTENT = _DATA / "operatorConsole.ts"
_BADGE = _COMP / "ConsoleBadge.tsx"
_MODE = _COMP / "ModeOverview.tsx"
_LEGEND = _COMP / "BoundaryLegend.tsx"
_FLOW = _COMP / "OperatorWorkflow.tsx"
_TTS = _COMP / "TTSProofSummary.tsx"
_MODULE_CSS = _COMP / "consolePolish.module.css"
_HOME = _COMP / "HomePage.tsx"
_VIEW = _COMP / "LocalBridgeView.tsx"

_NEW_FILES: tuple[Path, ...] = (
    _CONTENT, _BADGE, _MODE, _LEGEND, _FLOW, _TTS, _MODULE_CSS,
)
# The new TSX components only (CSS / content excluded where token rules differ).
_NEW_COMPONENTS: tuple[Path, ...] = (_BADGE, _MODE, _LEGEND, _FLOW, _TTS)


def _read(path: Path) -> str:
    assert path.is_file(), f"expected Phase 13J file missing: {path}"
    text = path.read_text(encoding="utf-8")
    assert text.strip(), f"file is unexpectedly empty: {path}"
    return text


# ── 1. new files exist and are wired ─────────────────────────────────────────


@pytest.mark.parametrize("path", _NEW_FILES, ids=lambda p: p.name)
def test_new_file_exists(path: Path) -> None:
    _read(path)


def test_overview_wires_mode_overview_and_boundary_legend() -> None:
    home = _read(_HOME)
    assert 'from "./ModeOverview"' in home, "HomePage does not import ModeOverview"
    assert 'from "./BoundaryLegend"' in home, "HomePage does not import BoundaryLegend"
    assert "<ModeOverview" in home and "<BoundaryLegend" in home, (
        "HomePage does not render the mode overview / boundary legend"
    )


def test_local_bridge_wires_workflow_and_tts_summary() -> None:
    view = _read(_VIEW)
    assert 'from "./OperatorWorkflow"' in view, "view does not import OperatorWorkflow"
    assert 'from "./TTSProofSummary"' in view, "view does not import TTSProofSummary"
    assert "<OperatorWorkflow" in view and "<TTSProofSummary" in view, (
        "Local Bridge view does not render the workflow / TTS proof summary"
    )


# ── 2. no execution path / unsafe control in the new components ──────────────


def test_no_generate_audio_button_or_tts_trigger() -> None:
    for path in (*_NEW_COMPONENTS, _CONTENT):
        lowered = _read(path).lower()
        assert "generate audio" not in lowered, f"{path.name} has a Generate-audio affordance"
        assert "generate_tts" not in lowered, f"{path.name} references generate_tts"
        assert "generateaudio" not in lowered, f"{path.name} references generateAudio"


def test_no_buttons_or_event_handlers_in_new_components() -> None:
    # The new components are purely presentational: no controls, no handlers.
    for path in _NEW_COMPONENTS:
        text = _read(path)
        assert "<button" not in text, f"{path.name} introduces a button control"
        for handler in ("onClick", "onChange", "onInput", "onSubmit", "onKeyDown"):
            assert handler not in text, f"{path.name} introduces a {handler} handler"


def test_no_network_or_post_in_new_components() -> None:
    for path in _NEW_COMPONENTS:
        text = _read(path)
        assert "fetch(" not in text, f"{path.name} performs a fetch"
        for verb in ("POST", "PUT", "PATCH", "DELETE"):
            assert verb not in text, f"{path.name} references mutation verb {verb!r}"


def test_no_file_directory_url_or_credential_inputs() -> None:
    for path in _NEW_COMPONENTS:
        text = _read(path)
        lowered = text.lower()
        assert "<input" not in text, f"{path.name} adds an input control"
        assert "<select" not in text, f"{path.name} adds a select/provider control"
        assert "<textarea" not in text, f"{path.name} adds a textarea control"
        assert "webkitdirectory" not in lowered, f"{path.name} adds a directory picker"
        # No credential-bearing input attributes (the no-<input> rule above
        # already makes a credential field impossible; these catch any attempt).
        for attr in (
            'type="file"',
            'type="password"',
            'autocomplete="current-password"',
            'autocomplete="new-password"',
        ):
            assert attr not in lowered, f"{path.name} adds a credential/file input ({attr})"


def test_no_durable_storage_or_sockets_or_polling_in_new_files() -> None:
    forbidden = (
        "localStorage", "sessionStorage", "indexedDB", "IndexedDB",
        "document.cookie", "WebSocket", "EventSource", "setInterval",
        "setTimeout", "ServiceWorker", "serviceWorker", "useEffect",
    )
    for path in _NEW_FILES:
        text = _read(path)
        for token in forbidden:
            assert token not in text, f"{path.name} uses forbidden runtime API {token!r}"


# ── 3. TTS copy is read-only / mock / backend-owned and honest ───────────────


def test_tts_content_is_read_only_mock_and_backend_owned() -> None:
    content = _read(_CONTENT)
    lowered = content.lower()
    assert "read-only" in lowered, "TTS content never states it is read-only"
    assert "mock" in lowered, "TTS content never names the mock provider"
    assert "backend" in lowered, "TTS content never states backend ownership"
    assert "cannot trigger" in lowered, (
        "TTS content never states the browser cannot trigger generation"
    )
    # The read-only summary component echoes the read-only framing.
    assert "read-only" in _read(_TTS).lower()


def test_real_provider_described_as_deferred_or_disabled_not_active() -> None:
    lowered = _read(_CONTENT).lower()
    assert "deferred" in lowered, "real provider not described as deferred"
    assert "disabled" in lowered, "real provider not described as disabled"
    # Never claim the real provider is active / enabled / live.
    for claim in (
        "real provider is active",
        "real provider is enabled",
        "real provider is live",
        "uses a real provider",
    ):
        assert claim not in lowered, f"TTS content claims the real provider is active: {claim!r}"


def test_mock_not_described_as_real_provider_audio() -> None:
    # The honest phrasing lives in the content source; the component renders it.
    content_lowered = _read(_CONTENT).lower()
    assert "not real provider audio" in content_lowered, (
        "operatorConsole.ts does not state mock output is not real provider audio"
    )
    assert "summary.ownership" in _read(_TTS), (
        "TTSProofSummary does not render the ownership / boundary notes"
    )
    for path in (_CONTENT, _TTS):
        lowered = _read(path).lower()
        for claim in (
            "mock output is real provider audio",
            "mock is real provider audio",
            "mock output is real audio",
        ):
            assert claim not in lowered, f"{path.name} conflates mock with real audio: {claim!r}"


def test_acceptance_not_equated_with_success() -> None:
    lowered = _read(_CONTENT).lower()
    assert "acceptance is not success" in lowered, (
        "operator flow copy does not keep acceptance distinct from success"
    )
    for claim in ("acceptance is success", "acceptance equals success", "accepted means completed"):
        assert claim not in lowered, f"copy conflates acceptance with success: {claim!r}"


def test_reload_not_described_as_live_sync() -> None:
    lowered = _read(_CONTENT).lower()
    assert "not a live sync" in lowered, "copy does not state reload is not a live sync"
    for claim in ("reload is live sync", "reload is a live sync", "live sync of"):
        assert claim not in lowered, f"copy describes reload as live sync: {claim!r}"


def test_no_full_local_or_cloud_mode_claimed_active() -> None:
    for path in (*_NEW_COMPONENTS, _CONTENT):
        lowered = _read(path).lower()
        idx = lowered.find("full local mode")
        if idx != -1:
            window = lowered[idx : idx + 90]
            assert (
                "deferred" in window
                or "remain" in window
                or "do not exist" in window
                or "not exist" in window
            ), f"{path.name} claims full Local mode without a deferral / negation cue"
        for claim in ("cloud mode is active", "distributed mode is active", "in cloud mode"):
            assert claim not in lowered, f"{path.name} claims a cloud/distributed mode: {claim!r}"
