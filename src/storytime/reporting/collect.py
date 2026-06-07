"""Collect the operator-report model from existing authoritative state.

The collector is the only thing that fills the ``reporting.model`` dataclasses,
and it fills them *only* from existing projections (§25.4, §25.11):

* the SQLite ``pipeline_run`` / ``stage_execution`` / ``stage_artifact`` /
  ``trust_envelope`` / ``published_episode`` rows;
* the durable Trust Envelope artifact (read read-only, for the bounded
  ``review_context_summary`` the SQLite projection deliberately omits — §24.7).

It reads; it never writes, never mutates state, and never widens the schema.
Telemetry backends are never queried — observability links are built only from
explicitly configured base URLs (§25.14). If the durable Trust Envelope cannot
be read for a run, that run's governance summary degrades gracefully and the
report is still complete (§25.14 completeness principle, applied to governance).
"""

from __future__ import annotations

from collections.abc import Mapping

from storytime.adapters.storage import StorageAdapter
from storytime.governance import TrustEnvelopeError, read_trust_envelope
from storytime.operator_rerun import evaluate_rerun_eligibility
from storytime.reporting.model import (
    REVIEW_CONTEXT_SUMMARY_MAX_CHARS,
    ArtifactRef,
    GovernanceView,
    ObservabilityLink,
    OperatorReport,
    RerunView,
    RunDetail,
    RunSummary,
    StageView,
)
from storytime.state import RunRecord, StateStore

# Stage-execution statuses that count as a successful (non-failing) stage.
# Anything else, or any stage carrying a structured ``error_kind``, is treated
# as a failure for the run-detail failure summary.
_SUCCESS_STAGE_STATUSES = frozenset({"SUCCEEDED", "succeeded"})


def _bounded_summary(summary: str | None) -> str | None:
    """Return *summary* bounded to the locked §25.13 display length.

    A summary longer than ``REVIEW_CONTEXT_SUMMARY_MAX_CHARS`` is truncated and
    given a visible, unambiguous indicator — the unbounded original never
    reaches the report (§25.13). ``None`` and a blank summary both yield
    ``None`` so the renderer can show a safe placeholder.
    """
    if summary is None:
        return None
    text = summary.strip()
    if not text:
        return None
    if len(text) <= REVIEW_CONTEXT_SUMMARY_MAX_CHARS:
        return text
    return text[:REVIEW_CONTEXT_SUMMARY_MAX_CHARS].rstrip() + " […truncated]"


def _governance_view(
    store: StateStore, storage: StorageAdapter, run: RunRecord
) -> GovernanceView | None:
    """Build the governance view for *run* from the Trust Envelope, or None.

    The bounded status fields come from the SQLite ``trust_envelope``
    projection. The free-text ``review_context_summary`` is read from the
    durable Trust Envelope artifact (the projection deliberately omits it);
    any failure to read or parse that artifact is swallowed — the run's
    governance summary simply omits the rationale and the report stays
    complete.
    """
    projection = store.latest_trust_envelope(run.pipeline_run_id)
    if projection is None:
        return None

    summary: str | None = None
    try:
        envelope = read_trust_envelope(storage, run.run_dir)
        summary = _bounded_summary(envelope.review_context_summary)
    except (TrustEnvelopeError, OSError, ValueError):
        # The durable artifact is missing, unreadable, or malformed. The
        # bounded status projection above is still trustworthy; the report
        # shows the decision without the optional rationale.
        summary = None

    return GovernanceView(
        decision=projection.decision,
        license_type=projection.license_type,
        approver_id=projection.approver_id,
        decision_timestamp=projection.decision_timestamp,
        blocked_reason=projection.blocked_reason,
        review_context_summary=summary,
        trust_envelope_key=projection.envelope_key,
    )


def _stage_views(store: StateStore, run_id: str) -> tuple[StageView, ...]:
    """Project a run's stage_execution rows into ordered StageView records."""
    return tuple(
        StageView(
            name=execution.stage_name,
            status=execution.status,
            error_kind=execution.error_kind,
        )
        for execution in store.list_stage_executions(run_id)
    )


def _failure(stages: tuple[StageView, ...]) -> tuple[str | None, str | None]:
    """Return the (stage_name, structured category) of a run's failure, if any.

    A failure is the last stage carrying a structured ``error_kind`` or a
    non-success status. Only the structured *category* is surfaced — never an
    unbounded exception message or stack trace (§25.12).
    """
    failure_stage: str | None = None
    failure_category: str | None = None
    for stage in stages:
        if stage.error_kind is not None or stage.status not in _SUCCESS_STAGE_STATUSES:
            failure_stage = stage.name
            failure_category = stage.error_kind or stage.status
    return failure_stage, failure_category


def _artifacts(
    store: StateStore,
    run: RunRecord,
    governance: GovernanceView | None,
    feed_reference: str | None,
) -> tuple[ArtifactRef, ...]:
    """Collect a run's read-only artifact references from existing projections.

    Stage-artifact envelope keys, the durable Trust Envelope key, the published
    audio path, and — when the run published — the shared RSS feed reference.
    Every entry is a reference (a relative key/path), never embedded content.
    """
    refs: list[ArtifactRef] = []
    for artifact in store.list_stage_artifacts(run.pipeline_run_id):
        refs.append(
            ArtifactRef(label=f"{artifact.stage_name} artifact", key=artifact.artifact_key)
        )
    if governance is not None and governance.trust_envelope_key is not None:
        refs.append(
            ArtifactRef(label="Trust Envelope", key=governance.trust_envelope_key)
        )
    for episode in store.list_published_episodes():
        if episode.pipeline_run_id == run.pipeline_run_id:
            refs.append(ArtifactRef(label="Audio output", key=episode.audio_path))
            if feed_reference:
                refs.append(ArtifactRef(label="RSS feed", key=feed_reference))
            break
    return tuple(refs)


def _observability_links(
    store: StateStore,
    run_id: str,
    jaeger_trace_base_url: str | None,
) -> tuple[ObservabilityLink, ...]:
    """Build optional observability links for a run (§25.14).

    The only link constructed is a Jaeger trace link, and only when a Jaeger
    base URL is explicitly configured *and* the run has a recorded trace id.
    The link is ``<base>/<trace_id>`` — a reference with no embedded data and
    no secret. With no configured base URL this returns an empty tuple and the
    report is still complete.
    """
    if not jaeger_trace_base_url:
        return ()
    trace_id: str | None = None
    for execution in store.list_stage_executions(run_id):
        if execution.trace_id:
            trace_id = execution.trace_id
            break
    if trace_id is None:
        return ()
    base = jaeger_trace_base_url.rstrip("/")
    return (ObservabilityLink(label="Trace (Jaeger)", url=f"{base}/{trace_id}"),)


def _rerun_view(store: StateStore, run: RunRecord) -> RerunView | None:
    """Project Phase 10D rerun eligibility for *run* into a bounded RerunView.

    Calls ``evaluate_rerun_eligibility`` (read-only) and projects only the
    safe, bounded fields into ``RerunView``. The raw decision message is
    operator-facing and safe; it contains no raw story text or stack traces.
    Returns ``None`` for runs that cannot meaningfully have a rerun projection
    (should not occur in practice, but degrades gracefully).
    """
    try:
        decision = evaluate_rerun_eligibility(store, run.pipeline_run_id)
    except Exception:
        # Evaluation failed unexpectedly — degrade gracefully; the report
        # stays complete without the rerun section.
        return None

    next_command: str | None = None
    if decision.eligible:
        run_id = decision.run_id
        next_command = (
            f"storytime rerun {run_id} --dry-run  # preview\n"
            f"storytime rerun {run_id}            # apply\n"
            f"storytime run --resume {run_id}      # re-execute after reset"
        )
    return RerunView(
        eligible=decision.eligible,
        code=decision.code,
        message=decision.message,
        from_stage=decision.from_stage,
        governance_status=decision.governance_status,
        next_command=next_command,
    )


def collect_report(
    store: StateStore,
    storage: StorageAdapter,
    *,
    generated_at: str,
    feed_reference: str | None = None,
    observability: Mapping[str, str] | None = None,
) -> OperatorReport:
    """Build the deterministic operator-report model from existing state.

    *store* is an open StateStore; *storage* is the run-artifact StorageAdapter
    (rooted at the runs directory). *generated_at* is an injected timestamp
    string — given identical state and an identical *generated_at* the result
    is identical, so the rendered report is byte-for-byte deterministic.

    *observability* is an optional mapping of configured observability base
    URLs (currently the key ``"jaeger_trace_base_url"``). It is the only source
    of observability links; no observability backend is ever queried.
    """
    obs = observability or {}
    jaeger_base = obs.get("jaeger_trace_base_url")

    # list_runs() is insertion order; present newest-first by created_at with
    # run_id as a stable deterministic tie-breaker.
    runs = sorted(
        store.list_runs(),
        key=lambda r: (r.created_at, r.pipeline_run_id),
        reverse=True,
    )

    summaries: list[RunSummary] = []
    details: list[RunDetail] = []
    for run in runs:
        governance = _governance_view(store, storage, run)
        stages = _stage_views(store, run.pipeline_run_id)
        failure_stage, failure_category = _failure(stages)
        summaries.append(
            RunSummary(
                run_id=run.pipeline_run_id,
                status=run.status,
                current_stage=run.current_stage,
                created_at=run.created_at,
                updated_at=run.updated_at,
                governance_decision=None if governance is None else governance.decision,
            )
        )
        details.append(
            RunDetail(
                run_id=run.pipeline_run_id,
                status=run.status,
                current_stage=run.current_stage,
                created_at=run.created_at,
                updated_at=run.updated_at,
                gates=run.gates,
                stages=stages,
                governance=governance,
                artifacts=_artifacts(store, run, governance, feed_reference),
                observability_links=_observability_links(
                    store, run.pipeline_run_id, jaeger_base
                ),
                failure_stage=failure_stage,
                failure_category=failure_category,
                rerun=_rerun_view(store, run),
            )
        )

    return OperatorReport(
        generated_at=generated_at,
        runs=tuple(summaries),
        details=tuple(details),
    )
