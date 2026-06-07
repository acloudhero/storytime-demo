"""Operator failure / review queue — a read-only CLI view (Phase 10C).

ARCH-LOCK: The operator queue is a view, never a broker
DO NOT REFACTOR: This module implements the Phase 10C "operator failure /
review queue" under the locked Architecture Baseline Section 25. The word
"queue" here means *an operator-facing, filtered, read-only view of runs that
need attention* — it is a semantic query over the existing SQLite
source-of-truth state. It is NOT a durable, broker-backed queue: there is no
message broker, no background worker, no new queue storage, no new lifecycle
state, and no ``pop`` / ``dequeue`` / ``claim`` / ``ack`` behaviour. Nothing
here mutates state.

The queue surfaces runs that are failed, blocked by governance, marked
needs-review, or awaiting an operator approval decision, and for each one tells
the operator *why* it needs attention and *which existing command, report, or
artifact* to look at next. Every "next hint" is a suggestion that points at an
existing command — the queue never executes anything.

The queue reads only bounded, structured fields — run and stage identifiers
and statuses, the §24.8 governance decision enum, the structured stage
``error_kind`` code, and timestamps. It never reads or emits raw story text,
narration, transcripts, secrets, long free-text governance notes, unbounded
exception messages, or raw telemetry (§25.12 report field blacklist, applied
to the queue). This module imports no OpenTelemetry and no web/template code.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import dataclass

from storytime.reporting import run_detail_filename
from storytime.state import StateStore

# The bounded default for ``--limit``. The queue is always bounded — it never
# floods the terminal with an unbounded backlog — so there is deliberately no
# "unlimited" option. 20 is a small, reviewable default.
DEFAULT_LIMIT = 20

# The directory the Phase 10B operator report is generated into by default
# (`storytime report generate`). The queue only *references* a run's report
# detail page by its deterministic relative path; it never generates it.
_REPORT_DIR = "operator-report"

# Stage-execution statuses that count as a successful (non-failing) stage.
_SUCCESS_STAGE_STATUSES = frozenset({"SUCCEEDED", "succeeded"})

# The four attention reasons a run can be in the queue for. These are derived
# from existing authoritative state — they are not new database states.
REASON_FAILED = "failed"
REASON_BLOCKED = "blocked"
REASON_NEEDS_REVIEW = "needs-review"
REASON_AWAITING_APPROVAL = "awaiting-approval"

# The valid values for the ``--status`` filter, in display order.
QUEUE_STATUS_FILTERS: tuple[str, ...] = (
    REASON_FAILED,
    REASON_BLOCKED,
    REASON_NEEDS_REVIEW,
    REASON_AWAITING_APPROVAL,
)

# The exact, ordered key allowlist for ``--json`` output. JSON emission uses
# this list explicitly — it never serialises the dataclass wholesale — so a
# field can never leak into JSON by accident.
_JSON_FIELDS: tuple[str, ...] = (
    "run_id",
    "status",
    "stage",
    "governance_decision",
    "failure_code",
    "failure_category",
    "updated_at",
    "created_at",
    "report_path",
    "trust_envelope_path",
    "next_hint",
)


@dataclass(frozen=True, slots=True)
class QueueItem:
    """One run that needs operator attention — a bounded, read-only projection.

    Every field is a bounded, structured projection of existing authoritative
    state. ``failure_code`` is the structured stage ``error_kind`` (e.g.
    ``"TtsError"``, ``"SourceNotApproved"``) — never an unbounded exception
    message. ``failure_category`` is a coarse, deterministic bucket
    (``"governance"`` or ``"stage_failure"``). ``reasons`` is the set of
    attention reasons this run matched, used for ``--status`` filtering and the
    human view; it is deliberately not part of the JSON allowlist.
    """

    run_id: str
    status: str
    stage: str
    governance_decision: str | None
    failure_code: str | None
    failure_category: str | None
    created_at: str
    updated_at: str
    report_path: str
    trust_envelope_path: str | None
    next_hint: str
    reasons: tuple[str, ...]

    def as_json_dict(self) -> dict[str, str | None]:
        """Return the JSON-safe mapping, restricted to the field allowlist."""
        values: dict[str, str | None] = {
            "run_id": self.run_id,
            "status": self.status,
            "stage": self.stage,
            "governance_decision": self.governance_decision,
            "failure_code": self.failure_code,
            "failure_category": self.failure_category,
            "updated_at": self.updated_at,
            "created_at": self.created_at,
            "report_path": self.report_path,
            "trust_envelope_path": self.trust_envelope_path,
            "next_hint": self.next_hint,
        }
        # Guard: the emitted keys are exactly the allowlist, nothing more.
        return {key: values[key] for key in _JSON_FIELDS}


class QueueStatusError(ValueError):
    """Raised when an unknown ``--status`` filter value is supplied."""


def _last_failure_code(store: StateStore, run_id: str) -> str | None:
    """Return the structured error_kind of a run's last failing stage, or None.

    Only the structured *code* is returned — never the (possibly unbounded)
    ``error_message`` text, which the queue must not display (§25.12).
    """
    code: str | None = None
    for execution in store.list_stage_executions(run_id):
        if execution.error_kind is not None:
            code = execution.error_kind
        elif execution.status not in _SUCCESS_STAGE_STATUSES:
            code = code or execution.status
    return code


def _next_hint(reasons: tuple[str, ...], run_id: str) -> str:
    """Return a deterministic, suggestion-only next step for a queued run.

    Every hint points at an existing read-only command or inspection step, or
    — only for an awaiting-approval run — at the existing canonical
    ``storytime approve`` command. The hint is advice; the queue never runs it.
    """
    if REASON_AWAITING_APPROVAL in reasons:
        return (
            f"Run is awaiting an operator decision; use `storytime approve "
            f"{run_id}` to record one."
        )
    if REASON_BLOCKED in reasons:
        return (
            "Blocked by governance: inspect the Trust Envelope artifact and "
            "review the source authorization record."
        )
    if REASON_NEEDS_REVIEW in reasons:
        return (
            "Source is marked needs-review: review the governance decision "
            "before continuing."
        )
    if REASON_FAILED in reasons:
        return (
            f"Run failed: inspect `storytime status {run_id}` and the run "
            "report detail page."
        )
    return (
        "Open the run report detail page; run `storytime report generate` to "
        "refresh the operator report."
    )


def _build_item(store: StateStore, run_id: str) -> QueueItem | None:
    """Build the QueueItem for a run, or None if the run needs no attention.

    A run needs attention when it has failed, was blocked by governance, is
    marked needs-review, or is awaiting an operator approval decision. A
    healthy ``running`` / ``completed`` run with no adverse governance returns
    None and never appears in the queue.
    """
    run = store.get_run(run_id)
    if run is None:
        return None

    envelope = store.latest_trust_envelope(run_id)
    governance_decision = None if envelope is None else envelope.decision
    trust_envelope_path = None if envelope is None else envelope.envelope_key
    failure_code = _last_failure_code(store, run_id)

    reasons: list[str] = []
    if run.status == "failed" or failure_code is not None:
        reasons.append(REASON_FAILED)
    if governance_decision == "BLOCKED":
        reasons.append(REASON_BLOCKED)
    if governance_decision == "NEEDS_REVIEW":
        reasons.append(REASON_NEEDS_REVIEW)
    if run.status == "awaiting_approval":
        reasons.append(REASON_AWAITING_APPROVAL)

    if not reasons:
        return None

    # failure_category is a coarse, deterministic bucket: a governance reason
    # dominates; otherwise a structured stage failure.
    if REASON_BLOCKED in reasons or REASON_NEEDS_REVIEW in reasons:
        failure_category: str | None = "governance"
    elif REASON_FAILED in reasons:
        failure_category = "stage_failure"
    else:
        failure_category = None

    ordered = tuple(r for r in QUEUE_STATUS_FILTERS if r in reasons)
    return QueueItem(
        run_id=run.pipeline_run_id,
        status=run.status,
        stage=run.current_stage,
        governance_decision=governance_decision,
        failure_code=failure_code,
        failure_category=failure_category,
        created_at=run.created_at,
        updated_at=run.updated_at,
        report_path=f"{_REPORT_DIR}/{run_detail_filename(run.pipeline_run_id)}",
        trust_envelope_path=trust_envelope_path,
        next_hint=_next_hint(ordered, run.pipeline_run_id),
        reasons=ordered,
    )


def collect_queue(
    store: StateStore,
    *,
    status: str | None = None,
    run_id: str | None = None,
    limit: int = DEFAULT_LIMIT,
) -> tuple[QueueItem, ...]:
    """Collect the bounded, deterministically-sorted operator-attention queue.

    *status*, when given, must be one of :data:`QUEUE_STATUS_FILTERS` and keeps
    only runs that match that attention reason. *run_id*, when given, restricts
    the queue to that one run. *limit* (a positive integer) bounds the number
    of items returned — the queue is always bounded.

    Items are sorted most-recently-updated first, with the run id as a stable
    tie-breaker, so the output is deterministic for identical state. This
    function only reads SQLite; it mutates nothing.

    Raises :class:`QueueStatusError` for an unknown *status* and ``ValueError``
    for a non-positive *limit*.
    """
    if status is not None and status not in QUEUE_STATUS_FILTERS:
        raise QueueStatusError(
            f"unknown status filter {status!r}; expected one of: "
            f"{', '.join(QUEUE_STATUS_FILTERS)}"
        )
    if limit < 1:
        raise ValueError(f"limit must be a positive integer, got {limit}")

    candidate_ids: Iterable[str]
    if run_id is not None:
        candidate_ids = [run_id]
    else:
        candidate_ids = [run.pipeline_run_id for run in store.list_runs()]

    items: list[QueueItem] = []
    for candidate in candidate_ids:
        item = _build_item(store, candidate)
        if item is None:
            continue
        if status is not None and status not in item.reasons:
            continue
        items.append(item)

    items.sort(key=lambda i: (i.updated_at, i.run_id), reverse=True)
    return tuple(items[:limit])


def render_json(items: tuple[QueueItem, ...]) -> str:
    """Render the queue as deterministic JSON — a list of allowlisted objects.

    Keys are sorted and the output is stable for identical input, so it is
    safe to snapshot-test. Only the 11 allowlisted fields are emitted.
    """
    payload = [item.as_json_dict() for item in items]
    return json.dumps(payload, indent=2, sort_keys=True)


def render_table(items: tuple[QueueItem, ...]) -> str:
    """Render the queue as a plain-text, terminal-friendly block list.

    A compact per-run block — no table library, no curses, no TUI, no paging.
    Deterministic: it contains no generation timestamp. An empty queue yields
    a single "no runs need attention." line.
    """
    if not items:
        return "no runs need attention."

    lines: list[str] = [f"{len(items)} run(s) need attention:", ""]
    for item in items:
        governance = item.governance_decision or "-"
        if item.failure_code is None:
            failure = "-"
        elif item.failure_category is None:
            failure = item.failure_code
        else:
            failure = f"{item.failure_code} ({item.failure_category})"
        lines.append(f"  {item.run_id}  [{', '.join(item.reasons)}]")
        lines.append(f"    status:     {item.status}   stage: {item.stage}")
        lines.append(f"    governance: {governance}")
        lines.append(f"    failure:    {failure}")
        lines.append(f"    updated:    {item.updated_at}")
        lines.append(f"    report:     {item.report_path}")
        if item.trust_envelope_path is not None:
            lines.append(f"    envelope:   {item.trust_envelope_path}")
        lines.append(f"    hint:       {item.next_hint}")
        lines.append("")
    return "\n".join(lines).rstrip()
