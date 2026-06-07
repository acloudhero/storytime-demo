"""Phase 14C.2 — guardrail tests for the contracts-as-built seam baseline doc.

These verify document presence, the required section headers, required
current-state phrases, key contract terms, and the absence of forbidden
overclaim phrases. They deliberately do NOT judge prose quality or whether prose
is "aspirational" — only structural and substring facts.
"""

from __future__ import annotations

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DOC = _REPO_ROOT / "docs" / "phase14-contracts-as-built.md"

_REQUIRED_HEADERS = (
    "### A. Request Acceptance Contract",
    "### B. Queue Port Contract",
    "### C. SQLite Adapter Contract",
    "### D. Worker Execution Contract",
    "### E. Stale Claim Recovery Contract",
    "### F. Stale Partial Execution Recovery Contract",
    "### G. Read-Model / DTO Safety Contract",
    "### H. Frontend Boundary Contract",
    "### I. Cloud/Distributed Seam Baseline",
    "### J. Future Phase Dependency Map",
)

# Current-state phrases that must appear (case-insensitive).
_REQUIRED_STATE_PHRASES = (
    "phase 14c.1",
    "locked",
    "phase 14c.2",
    "implementation candidate",
    "pending review",
    "not locked",
    "not started",
)

# Key contract terms that must appear (the document must describe the real
# seams, not just gesture at the source tree).
_REQUIRED_CONTRACT_TERMS = (
    "workqueue",
    "sqliteworkqueue",
    "enqueue",
    "claim",
    "lease",
    "queued → claimed → running",
    "execute_proof_run",
    "runfailed",
    "liveworkitem",
    "schema",
    "version 6",
    "loopback",
    "local no-double-execution",
    "local worker recovered a stale partial execution; run failed without "
    "re-executing completed stages",
)

# Positive-claim overclaim phrases that must NOT appear. Phrased so the
# document's honest negations ("no external broker exists yet", "not a cloud
# queue", "does not provide exactly-once semantics across a distributed system")
# cannot match.
_FORBIDDEN_OVERCLAIM_PHRASES = (
    "exactly-once distributed execution",
    "distributed exactly-once execution",
    "cloud queue implemented",
    "cloud adapter implemented",
    "external broker implemented",
    "object storage implemented",
    "object-storage adapter implemented",
    "artifact store implemented",
    "authentication implemented",
    "auth boundary implemented",
    "retry lineage implemented",
    "retry/recovery lineage implemented",
    "distributed worker pool implemented",
    "provider tts implemented",
    "rss publishing implemented",
    "runs as a distributed system",
    "is now a distributed system",
)


def _doc_text() -> str:
    return _DOC.read_text(encoding="utf-8")


def test_contracts_doc_exists() -> None:
    assert _DOC.is_file(), "docs/phase14-contracts-as-built.md is missing"
    assert _doc_text().strip(), "contracts-as-built doc is empty"


def test_contracts_doc_has_all_required_headers() -> None:
    lines = set(_doc_text().splitlines())
    missing = [h for h in _REQUIRED_HEADERS if h not in lines]
    assert not missing, f"contracts-as-built doc missing headers: {missing}"


def test_contracts_doc_headers_in_order() -> None:
    text = _doc_text()
    positions = [text.find(h) for h in _REQUIRED_HEADERS]
    assert all(p >= 0 for p in positions), "a required header is absent"
    assert positions == sorted(positions), "headers A–J are not in order"


def test_contracts_doc_records_current_state() -> None:
    lowered = _doc_text().lower()
    missing = [p for p in _REQUIRED_STATE_PHRASES if p not in lowered]
    assert not missing, f"contracts-as-built doc missing state phrases: {missing}"


def test_contracts_doc_has_key_contract_terms() -> None:
    lowered = _doc_text().lower()
    missing = [t for t in _REQUIRED_CONTRACT_TERMS if t not in lowered]
    assert not missing, f"contracts-as-built doc missing contract terms: {missing}"


def test_contracts_doc_has_no_overclaim_phrases() -> None:
    lowered = _doc_text().lower()
    present = [p for p in _FORBIDDEN_OVERCLAIM_PHRASES if p in lowered]
    assert not present, f"contracts-as-built doc contains overclaim phrases: {present}"


def test_contracts_doc_contains_abstract_protocol_snippets() -> None:
    # The doc must write out the abstract boundary shapes, not only cite source.
    text = _doc_text()
    assert "class WorkQueue(Protocol):" in text, "no WorkQueue Protocol snippet"
    assert "class WorkerExecution(Protocol):" in text, "no worker boundary snippet"


# Phase 14C.3.1: stale state wording that must not recur. Phase 14C.3 is the
# current candidate (not a future/NOT-STARTED phase), and a LOCAL artifact-store
# adapter now exists, so the ambiguous "no object-storage adapter exists yet"
# wording must stay qualified to cloud/external/public/S3/MinIO.
_FORBIDDEN_STALE_WORDING = (
    "phase 14c.3 and every later phase are",
    "no object-storage adapter exists yet",
)


def test_contracts_doc_has_no_stale_state_wording() -> None:
    lowered = _doc_text().lower()
    present = [p for p in _FORBIDDEN_STALE_WORDING if p in lowered]
    assert not present, f"contracts-as-built doc has stale state wording: {present}"
