"""State-discipline guard for the Phase 14D cloud/distributed architecture baseline.

This is a pure-text documentation guard (it imports only ``pathlib`` and
``pytest`` and never imports application code). It mirrors
``tests/test_contracts_as_built_doc.py``: it pins the structure and the honest
state wording of the Phase 14D deliverable so a cold-session reviewer can trust
that the document maps the locked local contracts to a *future* cloud/distributed
architecture and does not overclaim that any cloud behavior was implemented.

Phase 14D is the current implementation candidate (pending review, NOT locked).
Phase 14C.5.1 is the last locked phase. Phase 14E and Phase 15 are NOT STARTED.
"""

from __future__ import annotations

import pathlib

import pytest

_DOC = pathlib.Path(__file__).resolve().parents[1] / (
    "docs/phase14d-cloud-distributed-architecture-baseline.md"
)
_REGISTER = pathlib.Path(__file__).resolve().parents[1] / (
    "docs/phase14d-deferred-cloud-work-register.md"
)

# Required headers, in document order. These are the at-minimum sections the
# Phase 14D architecture content checklist requires.
_REQUIRED_HEADERS = (
    "# Phase 14D \u2014 Cloud / Distributed Architecture Baseline from Proven "
    "Local Contracts",
    "## 1. Purpose",
    "## 2. Non-goals",
    "## 3. As-built mapping principle",
    "## 4. Locked local contract inventory",
    "## 5. Future deployable service shape",
    "## 6. Contract-by-contract mapping",
    "### 6.A Local API / Bridge boundary",
    "### 6.B WorkQueue boundary",
    "### 6.C Worker boundary",
    "### 6.D ArtifactStore boundary",
    "### 6.E Recovery control plane boundary",
    "### 6.F Observability boundary",
    "### 6.G Read model / operator visibility boundary",
    "## 7. Data ownership boundaries",
    "## 8. Local assumptions that break in cloud",
    "## 9. Demo / Local / Cloud mode boundary",
    "## 10. Blue/green compatibility notes",
    "## 11. Phase 15 readiness implications",
    "## 12. Deferred cloud work register",
    "## 13. Explicit statement \u2014 no cloud behavior implemented",
)

# State phrases that must be present (checked case-insensitively). These pin the
# honest phase state: 14C.5.1 locked / last locked, 14D as the pending-review
# candidate that implements no cloud behavior, and 14E/15 not started.
_REQUIRED_STATE_PHRASES = (
    "phase 14d",
    "phase 14c.5.1",
    "locked",
    "last locked phase",
    "complete through 14c.5.1",
    "cloud / distributed architecture baseline from proven local contracts",
    "as-built",
    "implements no cloud",
    "not started",
    "phase 14e",
    "phase 15",
)

# Key contract terms that must appear so the document maps real, proven local
# seams rather than gesturing at a greenfield cloud design.
_REQUIRED_CONTRACT_TERMS = (
    "workqueue",
    "sqliteworkqueue",
    "artifactstore",
    "localfilesystemartifactstore",
    "normalize_artifact_key",
    "storageadapter",
    "recovery_action",
    "evaluate_recovery_eligibility",
    "queueworkerevent",
    "queueworkereventsink",
    "read model",
    "202 accepted",
    "queued \u2192 claimed \u2192 running",
    "local-first sqlite proof",
)

# Recommended (not active) Phase 15 sequencing must be present and framed as
# future. We only assert the labels appear; their future framing is covered by
# _FORBIDDEN_FUTURE_CLAIMS below and by tests/test_failure_mode_regression.py.
_REQUIRED_PHASE15_LABELS = (
    "phase 15a",
    "phase 15b",
    "phase 15c",
    "phase 15d",
    "phase 15e",
)

# Positive-claim overclaim phrases that must NOT appear. The document's honest
# negations ("does not implement S3", "no external broker", "future adapter")
# cannot match these.
_FORBIDDEN_OVERCLAIM_PHRASES = (
    "cloud queue implemented",
    "external broker implemented",
    "object storage implemented",
    "object-storage adapter implemented",
    "artifact store implemented",
    "distributed worker implemented",
    "distributed worker pool implemented",
    "provider tts implemented",
    "rss publishing implemented",
    "authentication implemented",
    "auth boundary implemented",
    "signed urls implemented",
    "kubernetes implemented",
    "terraform implemented",
    "runs as a distributed system",
    "is now a distributed system",
    "runs in the cloud",
    "deploys to the cloud",
)

# Forbidden future-state claims: Phase 14D is now LOCKED, so a 14D lock record
# is legitimate; the deliverable must not claim 14E/15 have started or locked.
_FORBIDDEN_FUTURE_CLAIMS = (
    "phase 14e is locked",
    "phase 14e has started",
    "phase 15 is locked",
    "phase 15 has started",
)


def _doc_text() -> str:
    return _DOC.read_text(encoding="utf-8")


def _register_text() -> str:
    return _REGISTER.read_text(encoding="utf-8")


def test_baseline_doc_exists() -> None:
    assert _DOC.is_file(), f"missing Phase 14D baseline doc: {_DOC}"


def test_baseline_doc_has_all_required_headers() -> None:
    text = _doc_text()
    missing = [h for h in _REQUIRED_HEADERS if h not in text]
    assert not missing, f"baseline doc missing required headers: {missing}"


def test_baseline_doc_headers_in_order() -> None:
    text = _doc_text()
    positions = [text.find(h) for h in _REQUIRED_HEADERS]
    assert positions == sorted(positions), "baseline doc headers are out of order"


def test_baseline_doc_records_current_state() -> None:
    lowered = _doc_text().lower()
    missing = [p for p in _REQUIRED_STATE_PHRASES if p not in lowered]
    assert not missing, f"baseline doc missing required state phrases: {missing}"


def test_baseline_doc_has_key_contract_terms() -> None:
    lowered = _doc_text().lower()
    missing = [t for t in _REQUIRED_CONTRACT_TERMS if t not in lowered]
    assert not missing, f"baseline doc missing key contract terms: {missing}"


def test_baseline_doc_has_phase15_sequence() -> None:
    lowered = _doc_text().lower()
    missing = [p for p in _REQUIRED_PHASE15_LABELS if p not in lowered]
    assert not missing, f"baseline doc missing recommended Phase 15 labels: {missing}"


def test_baseline_doc_has_no_overclaim_phrases() -> None:
    lowered = _doc_text().lower()
    present = [p for p in _FORBIDDEN_OVERCLAIM_PHRASES if p in lowered]
    assert not present, f"baseline doc has cloud-overclaim phrases: {present}"


def test_baseline_doc_has_no_future_state_claims() -> None:
    lowered = _doc_text().lower()
    present = [p for p in _FORBIDDEN_FUTURE_CLAIMS if p in lowered]
    assert not present, f"baseline doc makes forbidden future-state claims: {present}"


def test_baseline_doc_states_no_cloud_behavior_implemented() -> None:
    lowered = _doc_text().lower()
    assert "implements no cloud" in lowered or "no cloud behavior" in lowered, (
        "baseline doc must explicitly state that no cloud behavior was implemented"
    )


# --- deferred cloud work register -----------------------------------------

_REGISTER_REQUIRED_ITEMS = (
    "external broker adapter",
    "distributed worker runtime",
    "object storage adapter",
    "auth / secrets boundary",
    "cloud observability export",
    "blue/green deployment mechanics",
    "cloud recovery orchestration",
    "cloud operator api",
    "provider tts integration",
    "rss publishing",
    "audio playback / serving",
    "artifact url strategy",
    "dashboard / slo / alerting",
)

_REGISTER_REQUIRED_FIELDS = (
    "description",
    "why deferred",
    "depends on",
    "risk if implemented too early",
    "expected future phase",
)


def test_register_exists() -> None:
    assert _REGISTER.is_file(), f"missing deferred cloud work register: {_REGISTER}"


def test_register_tracks_all_items() -> None:
    lowered = _register_text().lower()
    missing = [i for i in _REGISTER_REQUIRED_ITEMS if i not in lowered]
    assert not missing, f"deferred register missing tracked items: {missing}"


def test_register_has_all_per_item_fields() -> None:
    lowered = _register_text().lower()
    missing = [f for f in _REGISTER_REQUIRED_FIELDS if f not in lowered]
    assert not missing, f"deferred register missing per-item fields: {missing}"


def test_register_has_no_overclaim_phrases() -> None:
    lowered = _register_text().lower()
    present = [p for p in _FORBIDDEN_OVERCLAIM_PHRASES if p in lowered]
    assert not present, f"deferred register has cloud-overclaim phrases: {present}"


if __name__ == "__main__":  # pragma: no cover - convenience runner
    raise SystemExit(pytest.main([__file__, "-q"]))
