"""Phase 15C — Minimal Cloud Demo Deployment: static-demo guard tests.

These deterministic tests prevent the public static demo from overclaiming and
record the Phase 15C state discipline. They assert the required disclaimer is
present (verbatim) in the frontend source and the demo docs, that the two
backend-dependent views are gated for the public static demo, that no forbidden
cloud/live-backend overclaim appears in the public-facing demo copy, that a
single static deployment config exists, and that the phase ledger is honest
(Phase 15C candidate / pending review / NOT locked; Phase 15A and 15B LOCKED;
Phase 14E and Phase 15D+ NOT STARTED).
"""

from __future__ import annotations

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_DOCS = _REPO_ROOT / "docs"
_FRONTEND = _REPO_ROOT / "frontend"
_FRONTEND_SRC = _FRONTEND / "src"

_DESIGN_DOC = _DOCS / "phase15c-minimal-cloud-demo.md"
_DEMO_MD = _REPO_ROOT / "DEMO.md"
_README = _REPO_ROOT / "README.md"
_DEMO_MODE = _FRONTEND_SRC / "data" / "demoMode.ts"
_STATIC_NOTICE = _FRONTEND_SRC / "components" / "StaticDemoNotice.tsx"
_APP = _FRONTEND_SRC / "App.tsx"
_PAGES_WORKFLOW = _REPO_ROOT / ".github" / "workflows" / "pages.yml"

# The exact, verbatim public-demo disclaimer.
_REQUIRED_DISCLAIMER = (
    "This is a cloud-hosted static operator demo of a local-first, "
    "observability-native pipeline and its cloud-readiness seams."
)

_STATE_DOCS = (
    _REPO_ROOT / "LLM_DIRECTOR.md",
    _DOCS / "handoff-state.md",
    _DOCS / "roadmap.md",
    _DOCS / "canonical-state.md",
    _DOCS / "phase-history.md",
)

# Public-facing demo copy scanned for forbidden overclaims. Scoped to the
# Phase 15C surface (docs + the frontend files this phase authored/edited) so
# the scan is deterministic and does not false-positive on unrelated copy.
_PUBLIC_COPY_FILES = (
    _DEMO_MD,
    _DESIGN_DOC,
    _DEMO_MODE,
    _STATIC_NOTICE,
    _APP,
)

# Affirmative overclaim phrases that must never appear in public-facing copy.
# These are affirmative multi-word claims; honest negations in the demo copy
# are deliberately phrased to avoid these exact substrings.
_FORBIDDEN_OVERCLAIM_PHRASES = (
    "production cloud backend",
    "production saas",
    "live distributed worker",
    "live cloud worker",
    "live backend",
    "cloud queue implemented",
    "s3 implemented",
    "redis implemented",
    "object storage implemented",
    "external broker implemented",
    "distributed recovery implemented",
    "provider telemetry export implemented",
    "runs in production",
    "cloud-native production deployment",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestRequiredDisclaimer:
    def test_disclaimer_in_frontend_source(self) -> None:
        assert _DEMO_MODE.is_file(), "frontend/src/data/demoMode.ts is missing"
        assert _REQUIRED_DISCLAIMER in _read(_DEMO_MODE), (
            "verbatim demo disclaimer missing from frontend source"
        )

    def test_disclaimer_in_design_doc(self) -> None:
        assert _DESIGN_DOC.is_file(), "phase15c design doc is missing"
        assert _REQUIRED_DISCLAIMER in _read(_DESIGN_DOC), (
            "verbatim demo disclaimer missing from the Phase 15C design doc"
        )

    def test_disclaimer_in_public_demo_readme(self) -> None:
        assert _DEMO_MD.is_file(), "DEMO.md is missing"
        assert _REQUIRED_DISCLAIMER in _read(_DEMO_MD), (
            "verbatim demo disclaimer missing from DEMO.md"
        )


class TestBackendViewsGated:
    def test_static_demo_flag_defined(self) -> None:
        source = _read(_DEMO_MODE)
        assert "STATIC_DEMO_MODE" in source
        assert "STATIC_DEMO_ACTION_MESSAGE" in source

    def test_static_demo_notice_component_exists(self) -> None:
        assert _STATIC_NOTICE.is_file(), "StaticDemoNotice component is missing"
        source = _read(_STATIC_NOTICE)
        assert "STATIC_DEMO_ACTION_MESSAGE" in source
        assert "loopback" in source.lower()

    def test_app_gates_backend_dependent_views(self) -> None:
        source = _read(_APP)
        # Both backend-dependent views must be gated behind the static-demo
        # flag and rendered as the local-only notice on the public demo.
        assert "STATIC_DEMO_MODE" in source
        assert "StaticDemoNotice" in source
        for view_key in ('case "bridge":', 'case "liveproof":'):
            assert view_key in source, f"missing view branch {view_key!r}"


class TestNoOverclaims:
    def test_no_forbidden_overclaim_in_public_copy(self) -> None:
        for path in _PUBLIC_COPY_FILES:
            assert path.is_file(), f"expected public-copy file missing: {path.name}"
            lowered = _read(path).lower()
            present = [p for p in _FORBIDDEN_OVERCLAIM_PHRASES if p in lowered]
            assert not present, f"{path.name} makes overclaim(s): {present}"

    def test_deployment_config_is_static_only(self) -> None:
        assert _PAGES_WORKFLOW.is_file(), "GitHub Pages workflow is missing"
        # Scan only non-comment lines: the workflow's honest negation comments
        # (e.g. "no serverless function") must not trip the backend-surface
        # check, but actual YAML keys/values would.
        config_lines = [
            ln
            for ln in _read(_PAGES_WORKFLOW).splitlines()
            if not ln.lstrip().startswith("#")
        ]
        workflow = "\n".join(config_lines).lower()
        assert "frontend/dist" in workflow
        for forbidden in ("lambda", "serverless", "ecs", "app runner", "cloud run"):
            assert forbidden not in workflow, f"workflow references {forbidden!r}"


class TestPhaseStateDiscipline:
    def test_phase_15a_and_15b_locked(self) -> None:
        for doc in _STATE_DOCS:
            lowered = _read(doc).lower()
            a_lines = [ln for ln in lowered.splitlines() if "15a" in ln]
            b_lines = [ln for ln in lowered.splitlines() if "15b" in ln]
            assert any("locked" in ln for ln in a_lines), (
                f"{doc.name} does not record Phase 15A as locked"
            )
            assert any("locked" in ln for ln in b_lines), (
                f"{doc.name} does not record Phase 15B as locked"
            )

    def test_phase_15c_candidate_not_locked(self) -> None:
        for doc in _STATE_DOCS:
            lowered = _read(doc).lower()
            assert "phase 15c" in lowered
            assert "not locked" in lowered
            assert "phase 15c is locked" not in lowered

    def test_phase_14e_not_started_and_not_opened(self) -> None:
        forbidden = (
            "phase 14e is locked",
            "phase 14e has started",
            "phase 14e is the current",
        )
        for doc in _STATE_DOCS:
            lowered = _read(doc).lower()
            assert "phase 14e" in lowered
            assert "not started" in lowered
            for claim in forbidden:
                assert claim not in lowered, f"{doc.name} claims {claim!r}"

    def test_phase_15d_15e_15f_remain_not_started(self) -> None:
        forbidden = (
            "phase 15d has started",
            "phase 15d is locked",
            "phase 15e has started",
            "phase 15e is locked",
            "phase 15f has started",
            "phase 15f is locked",
        )
        for doc in _STATE_DOCS:
            lowered = _read(doc).lower()
            for claim in forbidden:
                assert claim not in lowered, f"{doc.name} claims {claim!r}"
