"""Phase 13K guards — canonical demo walkthrough truthfulness, evidence-map
path existence, and demo/portfolio sprawl reconciliation.

These tests are intentionally *structured* and *negation-aware* rather than
brittle prose scanners (see the Phase 13K prompt's negation-aware requirement):

* The evidence-map test parses only the structured evidence-map table rows and
  asserts each referenced path exists (accepting both files and directories).
* The truthfulness test asserts the machine-checkable truth labels are present,
  asserts a small set of unambiguous unsafe tokens are absent, and uses a
  per-line negation-aware check for risky active phrases so honest negated /
  deferred caveats ("provider-backed audio remains deferred", "not a live
  sync") are never punished.
* The reconciliation test asserts exactly one canonical walkthrough exists and
  that the pre-existing stale demo/portfolio cluster points at it.
"""

from __future__ import annotations

import re
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
_DOCS = _REPO / "docs"
_CANONICAL = _DOCS / "demo-walkthrough.md"
_ADAPTER = _REPO / "frontend" / "src" / "data" / "demoWalkthroughAdapter.ts"

# The pre-existing demo/portfolio/narrative/script/interview cluster that must
# defer to the canonical walkthrough (kept in sync with the reconciliation step).
_CLUSTER = (
    "demo.md", "demo-script.md", "demo-talk-track.md",
    "demo-reviewer-checklist.md", "demo-reproducibility-checklist.md",
    "observability-demo.md",
    "operator-experience-walkthrough.md",
    "solutions-engineer-narrative.md", "se-interview-evidence-matrix.md",
    "interview-story-bank.md", "interview-talking-points.md",
    "portfolio-demo-script.md", "portfolio-demo-narrative.md",
    "portfolio-narrative.md", "portfolio-overview.md",
    "portfolio-public-copy.md", "portfolio-notes.md",
    "portfolio-evidence-index.md", "portfolio-website-content-model.md",
    "final-portfolio-handoff.md",
)

_CANONICAL_MARKER = "CANONICAL WALKTHROUGH"
_POINTER_MARKER = "CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md"

# Negation / deferral cues: if any appear on a line, a risky active phrase on the
# same line is treated as an honest caveat, not an overclaim.
_NEG = (
    "no ", "not ", "n't", "never", "without", "cannot", "can't",
    "deferred", "remains", "rather than", "instead of", "manual",
    "none", "read-only", "labeled mock", "is git-ignored", "excluded",
    "backend/cli", "backend-cli", "operator-", "loopback", "hash",
)

# Risky phrases that, if asserted *affirmatively* (no negation cue on the line),
# would be an overclaim about capabilities StoryTime does not have.
_RISKY_ACTIVE = (
    "live sync", "real provider audio", "provider-backed audio",
    "full local mode", "cloud mode", "distributed mode", "rss publishing",
    "audio playback", "frontend tts generation", "browser generates",
    "generates audio in the browser",
)

# Unambiguous tokens that must never appear in the walkthrough / adapter, in any
# form (unsafe instructions or capability claims that have no honest phrasing).
_ABSOLUTE_FORBIDDEN = (
    "generate_tts",
    "storytime_tts_real_provider_enabled=true",
    "0.0.0.0",
    "ngrok",
    "disable cors",
    "acceptance is success",
    "acceptance means success",
    "acceptance equals success",
)

# Machine-checkable truth labels the canonical doc must carry.
_REQUIRED_LABELS = (
    "tts_provider_mode: mock",
    "tts_real_provider: deferred",
    "snapshot_sync: manual",
    "live_sync: none",
    "retry_semantics: acceptance-is-not-success",
    "manual_reload: operator-triggered-read-model-refresh",
    "browser_authority: operator-surface-not-source-of-truth",
    "tts_owner: backend-cli",
    "tts_evidence: artifact-plus-manifest-plus-audit",
)


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


class TestCanonicalWalkthroughExists:
    def test_canonical_doc_present(self) -> None:
        assert _CANONICAL.exists(), "docs/demo-walkthrough.md is missing"

    def test_required_sections_present(self) -> None:
        text = _read(_CANONICAL)
        for heading in (
            "## 1. At a glance",
            "## 2. Guided demo",
            "## 3. Technical inspection appendix",
            "## 4. Deferred-capability register",
            "## 5. Evidence map",
        ):
            assert heading in text, f"canonical walkthrough missing section: {heading}"


class TestTruthLabelsPresent:
    def test_required_truth_labels(self) -> None:
        lowered = _read(_CANONICAL).lower()
        for label in _REQUIRED_LABELS:
            assert label in lowered, f"canonical walkthrough missing truth label: {label!r}"

    def test_phase_state_label_is_honest(self) -> None:
        lowered = _read(_CANONICAL).lower()
        assert "phase_state:" in lowered
        for token in ("13j-locked", "13k-candidate", "phase-13-open"):
            assert token in lowered, f"phase_state label missing token: {token!r}"

    def test_deferred_register_lists_capabilities(self) -> None:
        lowered = _read(_CANONICAL).lower()
        for token in (
            "frontend tts generation",
            "provider-backed tts adapter",
            "audio playback",
            "rss",
            "full local mode",
            "cloud",
        ):
            assert token in lowered, f"deferred register missing: {token!r}"


class TestNoActiveOverclaims:
    """Negation-aware: honest negated/deferred caveats must pass; affirmative
    overclaims must fail."""

    def _surfaces(self) -> list[tuple[str, str]]:
        out = [("demo-walkthrough.md", _read(_CANONICAL))]
        if _ADAPTER.exists():
            out.append(("demoWalkthroughAdapter.ts", _read(_ADAPTER)))
        return out

    def test_no_absolute_forbidden_tokens(self) -> None:
        for name, text in self._surfaces():
            low = text.lower()
            for token in _ABSOLUTE_FORBIDDEN:
                assert token not in low, (
                    f"{name} contains forbidden token {token!r}"
                )

    def test_risky_phrases_only_appear_negated(self) -> None:
        # A negation/deferral cue counts if it appears on the same line OR an
        # immediately adjacent line, because TypeScript string concatenation and
        # wrapped prose routinely split one sentence ("... full Local mode ...
        # are" + "deferred ...") across physical lines.
        for name, text in self._surfaces():
            lines = text.splitlines()
            for i, raw in enumerate(lines):
                low = raw.lower()
                window = " ".join(
                    lines[j].lower()
                    for j in range(max(0, i - 1), min(len(lines), i + 2))
                )
                if any(neg in window for neg in _NEG):
                    continue
                for phrase in _RISKY_ACTIVE:
                    assert phrase not in low, (
                        f"{name} appears to make an active overclaim "
                        f"({phrase!r}) without a negation/deferral cue: "
                        f"{raw.strip()!r}"
                    )

    def test_no_unsafe_provider_or_bridge_instructions(self) -> None:
        # The canonical demo is mock-first and local-safe; it must not tell a
        # reviewer to enable a real provider, set credentials, or expose the
        # bridge. The mock-safe negative guidance ("Do not enable ...") is
        # allowed; affirmative imperative forms are not.
        for name, text in self._surfaces():
            low = text.lower()
            for token in (
                "set your provider credentials",
                "enter your api key",
                "add your credentials",
                "expose the bridge to the public",
                "bind the bridge to 0.0.0.0",
            ):
                assert token not in low, (
                    f"{name} contains an unsafe instruction: {token!r}"
                )


class TestEvidenceMapPathsExist:
    """Parse the structured evidence-map table and assert each referenced path
    exists. Targets table rows only (rows whose Evidence-path cell contains a
    backticked path); prose is ignored. Accepts files and directories."""

    def _evidence_paths(self) -> list[str]:
        text = _read(_CANONICAL)
        # isolate the Evidence map section
        idx = text.find("## 5. Evidence map")
        assert idx != -1, "Evidence map section not found"
        section = text[idx:]
        paths: list[str] = []
        row_re = re.compile(r"^\|(?P<c1>[^|]*)\|(?P<c2>[^|]*)\|(?P<c3>[^|]*)\|\s*$")
        backtick_re = re.compile(r"`([^`]+)`")
        for line in section.splitlines():
            m = row_re.match(line)
            if not m:
                continue
            cell = m.group("c2")
            bt = backtick_re.search(cell)
            if not bt:
                # header row ("| Claim | Evidence path | ...") or separator
                continue
            paths.append(bt.group(1).strip())
        return paths

    def test_evidence_map_has_rows(self) -> None:
        paths = self._evidence_paths()
        assert len(paths) >= 15, (
            f"evidence map parsed too few rows ({len(paths)}); parser or table "
            f"may be malformed"
        )

    def test_every_evidence_path_exists(self) -> None:
        missing = []
        for rel in self._evidence_paths():
            if not (_REPO / rel).exists():
                missing.append(rel)
        assert not missing, f"evidence map references missing paths: {missing}"


class TestSprawlReconciled:
    def test_exactly_one_canonical_walkthrough(self) -> None:
        hits = [
            p.name
            for p in _DOCS.glob("*.md")
            if _CANONICAL_MARKER in _read(p)
        ]
        assert hits == ["demo-walkthrough.md"], (
            f"expected exactly one canonical walkthrough, found: {hits}"
        )

    def test_stale_cluster_points_to_canonical(self) -> None:
        unreconciled = []
        for name in _CLUSTER:
            p = _DOCS / name
            if not p.exists():
                continue
            text = _read(p)
            if _POINTER_MARKER not in text and "demo-walkthrough.md" not in text:
                unreconciled.append(name)
        assert not unreconciled, (
            f"stale demo/portfolio docs neither point to nor are superseded by "
            f"the canonical walkthrough: {unreconciled}"
        )
