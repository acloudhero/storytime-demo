"""Configuration-derived cloud boundary-readiness model (Phase 15B).

ARCH-LOCK: Pure, configuration-derived boundary readiness (Phase 15B)
DO NOT REFACTOR: :func:`evaluate_boundary_readiness` is pure and
side-effect-free. It derives a *description* of four cloud-growth seams — the
queue/worker, artifact/storage, observability/export, and
recovery/idempotency boundaries — from the immutable config and the runtime
role alone. It starts no worker, claims no queue work, binds no socket, opens
no database, and instantiates, wraps, proxies, or adapts none of the proven
LOCAL contracts. Every boundary names the proven local backend and its
source of truth by description only; it changes no WorkQueue, ArtifactStore,
StateStore, recovery, or observer semantics.

The model is provider-neutral on purpose: it never names a specific broker,
object-storage service, telemetry vendor, or orchestration tool. Those belong
in documentation as deferred examples, not in the runtime readiness surface.
The model states, for each seam, what is locally active, what is deferred to a
future phase, and what must remain true before any cloud implementation may
cross the boundary — it does not implement that cloud behaviour.

Rationale: Phase 15B — Cloud Boundary Readiness (local-first, reversible).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from storytime.config import StoryTimeConfig
from storytime.runtime.config import RuntimeConfig
from storytime.runtime.roles import RuntimeRole


class BoundaryStatus(StrEnum):
    """The current posture of one cloud-growth boundary. Closed vocabulary.

    Phase 15B is local-first, so a boundary is either ``local-active`` (the
    proven local backend is the active implementation and the cloud
    implementation is deferred to a later phase) or ``not-applicable`` (the
    seam does not apply to the given runtime role — for example queue draining
    on the api role). There is deliberately no ``cloud-ready`` value: nothing
    here implements or certifies cloud behaviour.
    """

    LOCAL_ACTIVE = "local-active"
    NOT_APPLICABLE = "not-applicable"


class OverallReadiness(StrEnum):
    """The overall posture of a readiness snapshot. Closed vocabulary.

    ``ready-for-local`` means every boundary is locally active (or not
    applicable) with no blockers — local operation is ready and cloud work is
    cleanly deferred. ``blocked`` is the fail-closed value: if any boundary
    records a blocker, the snapshot is blocked rather than silently ready.
    """

    READY_FOR_LOCAL = "ready-for-local"
    BLOCKED = "blocked"


ALL_BOUNDARY_STATUSES: tuple[BoundaryStatus, ...] = tuple(BoundaryStatus)
ALL_OVERALL_READINESS: tuple[OverallReadiness, ...] = tuple(OverallReadiness)

# The four cloud-growth seams this phase models, in a stable order.
QUEUE_BOUNDARY = "queue_worker"
ARTIFACT_BOUNDARY = "artifact_storage"
OBSERVABILITY_BOUNDARY = "observability_export"
RECOVERY_BOUNDARY = "recovery_idempotency"


def parse_boundary_status(value: str) -> BoundaryStatus:
    """Return the :class:`BoundaryStatus` for *value*, failing closed.

    Case-insensitive. Raises :class:`ValueError` on any unrecognised value so
    an unknown status can never silently pass as a valid boundary posture.
    """
    normalized = value.strip().lower()
    for status in BoundaryStatus:
        if status.value == normalized:
            return status
    raise ValueError(f"unknown boundary status: {value!r}") from None


@dataclass(frozen=True, slots=True)
class BoundarySummary:
    """An immutable, pure-data description of one cloud-growth boundary.

    Every field is descriptive. ``active_backend`` and ``source_of_truth`` name
    the proven local backend; ``required_before_cloud`` lists the invariants
    that any future cloud implementation must preserve; ``deferred_capabilities``
    names the future work (provider-neutral); ``explicit_non_goals`` records
    what Phase 15B deliberately does not do; ``known_blockers`` is empty unless
    something would block local readiness. No field contains a secret, a
    credential, a filesystem path, or a provider-specific name.
    """

    boundary_name: str
    active_backend: str
    status: BoundaryStatus
    source_of_truth: str
    current_guarantees: tuple[str, ...]
    required_before_cloud: tuple[str, ...]
    deferred_capabilities: tuple[str, ...]
    explicit_non_goals: tuple[str, ...]
    known_blockers: tuple[str, ...] = ()

    def to_summary(self) -> dict[str, object]:
        """Return a safe, JSON-friendly mapping for this boundary."""
        return {
            "boundary_name": self.boundary_name,
            "active_backend": self.active_backend,
            "status": str(self.status),
            "source_of_truth": self.source_of_truth,
            "current_guarantees": list(self.current_guarantees),
            "required_before_cloud": list(self.required_before_cloud),
            "deferred_capabilities": list(self.deferred_capabilities),
            "explicit_non_goals": list(self.explicit_non_goals),
            "known_blockers": list(self.known_blockers),
        }


@dataclass(frozen=True, slots=True)
class BoundaryReadinessSnapshot:
    """An immutable, configuration-derived readiness snapshot for four seams.

    Pure data: produced by :func:`evaluate_boundary_readiness` from the runtime
    config and the immutable config. It reflects no live process state.
    ``overall_status``, ``blockers``, and ``deferred_capabilities`` are derived
    from the four boundary summaries; ``to_summary`` renders a safe,
    secret-free, JSON-friendly mapping suitable for logging, a test, or a
    future read-only status surface.
    """

    generated_for_runtime_role: RuntimeRole
    deployment: str
    environment: str
    queue: BoundarySummary
    artifacts: BoundarySummary
    observability: BoundarySummary
    recovery: BoundarySummary
    warnings: tuple[str, ...] = ()

    @property
    def boundaries(self) -> tuple[BoundarySummary, ...]:
        """The four boundary summaries in a stable order."""
        return (self.queue, self.artifacts, self.observability, self.recovery)

    @property
    def blockers(self) -> tuple[str, ...]:
        """Every known blocker across the four boundaries, in order."""
        collected: list[str] = []
        for boundary in self.boundaries:
            collected.extend(boundary.known_blockers)
        return tuple(collected)

    @property
    def deferred_capabilities(self) -> tuple[str, ...]:
        """Every deferred future capability across the four boundaries."""
        collected: list[str] = []
        for boundary in self.boundaries:
            collected.extend(boundary.deferred_capabilities)
        return tuple(collected)

    @property
    def overall_status(self) -> OverallReadiness:
        """``ready-for-local`` unless any boundary records a blocker."""
        if self.blockers or self.warnings:
            return OverallReadiness.BLOCKED
        return OverallReadiness.READY_FOR_LOCAL

    def to_summary(self) -> dict[str, object]:
        """Return a safe, JSON-friendly summary with no secrets or paths."""
        return {
            "generated_for_runtime_role": str(self.generated_for_runtime_role),
            "deployment": self.deployment,
            "environment": self.environment,
            "overall_status": str(self.overall_status),
            "boundaries": {
                self.queue.boundary_name: self.queue.to_summary(),
                self.artifacts.boundary_name: self.artifacts.to_summary(),
                self.observability.boundary_name: self.observability.to_summary(),
                self.recovery.boundary_name: self.recovery.to_summary(),
            },
            "blockers": list(self.blockers),
            "warnings": list(self.warnings),
            "deferred_capabilities": list(self.deferred_capabilities),
        }


def _queue_boundary(role: RuntimeRole) -> BoundarySummary:
    """Queue/worker boundary derived from the role's default behaviour."""
    drains_queue = role.runs_worker_loop_by_default
    status = BoundaryStatus.LOCAL_ACTIVE if drains_queue else BoundaryStatus.NOT_APPLICABLE
    if drains_queue:
        active_backend = (
            "Local durable work queue behind the existing WorkQueue port, "
            "drained by the single in-process local worker."
        )
    else:
        active_backend = (
            "Local durable work queue behind the existing WorkQueue port; the "
            "api role does not claim or drain queue work by default."
        )
    return BoundarySummary(
        boundary_name=QUEUE_BOUNDARY,
        active_backend=active_backend,
        status=status,
        source_of_truth=(
            "Backend-owned durable state: queue rows and run/stage state live in "
            "the local SQLite store, not in any observation stream."
        ),
        current_guarantees=(
            "A single in-process worker claims, completes, and fails work durably.",
            "Claim, lease, completion, and failure semantics are the existing "
            "locked WorkQueue behaviour and are unchanged.",
            "Attempt limits and recovery eligibility remain backend-decided.",
        ),
        required_before_cloud=(
            "Any future external/cloud queue must preserve single-delivery-effect "
            "claim semantics so no work item executes twice.",
            "Cross-worker safety (lease ownership, reclaim on expiry) must be "
            "proven before more than one worker drains the queue.",
            "Stage execution must be idempotent before distributed retry is "
            "allowed.",
            "Durable backend state must remain the source of truth; the queue "
            "transport must not become authoritative.",
        ),
        deferred_capabilities=(
            "External/cloud message-broker queue transport (deferred to a future phase).",
            "Replica-safe distributed worker pool (deferred).",
            "Dead-letter handling and dead-letter replay (deferred).",
            "Backoff/retry policy expansion (deferred).",
        ),
        explicit_non_goals=(
            "No external message broker and no broker URL or credential config.",
            "No distributed worker pool and no distributed claim loop.",
            "No queue wrapper, proxy, or adapter around the existing WorkQueue.",
            "No change to claim, lease, completion, failure, or attempt-limit behaviour.",
            "No automatic polling daemon, scheduler, or background supervisor.",
        ),
    )


def _artifact_boundary() -> BoundarySummary:
    """Artifact/object-storage boundary (role-independent: backend-owned)."""
    return BoundarySummary(
        boundary_name=ARTIFACT_BOUNDARY,
        active_backend=(
            "Local filesystem artifact storage behind the existing ArtifactStore "
            "port, written by the worker and surfaced read-only by the read-model."
        ),
        status=BoundaryStatus.LOCAL_ACTIVE,
        source_of_truth=(
            "Backend-owned storage plus the manifest / envelope / SHA-256 "
            "semantics; the browser never learns a path, URL, or credential."
        ),
        current_guarantees=(
            "Artifact keys are normalized to portable relative paths.",
            "Envelopes are validated and payload SHA-256 digests are verified on read.",
            "Archive hygiene excludes generated runtime output from packaged artifacts.",
        ),
        required_before_cloud=(
            "Any future object-storage backend must preserve key normalization "
            "and reject path traversal.",
            "Envelope and SHA-256 validation must hold unchanged across the "
            "storage boundary.",
            "Access must stay server-mediated; the browser must never receive a "
            "raw path, URL, or credential.",
        ),
        deferred_capabilities=(
            "Managed object-storage backend (deferred to a future phase).",
            "Server-mediated time-limited download links (deferred).",
            "Public artifact serving (deferred and currently a non-goal).",
        ),
        explicit_non_goals=(
            "No object-storage backend, bucket config, or credential config.",
            "No public artifact serving and no externally signed links.",
            "No artifact wrapper, proxy, or adapter around the existing ArtifactStore.",
            "No change to key normalization, envelope validation, or hash semantics.",
        ),
    )


def _observability_boundary(config: StoryTimeConfig) -> BoundarySummary:
    """Observability/export boundary derived from the telemetry mode."""
    return BoundarySummary(
        boundary_name=OBSERVABILITY_BOUNDARY,
        active_backend=(
            "In-process, fail-soft queue/worker observation with a stdlib-only "
            f"event boundary; telemetry mode is {config.telemetry!r}."
        ),
        status=BoundaryStatus.LOCAL_ACTIVE,
        source_of_truth=(
            "Durable backend state. Observations are explanatory signals only and "
            "are never the source of truth for queue, artifact, recovery, or run state."
        ),
        current_guarantees=(
            "The event vocabulary is native to the StoryTime domain.",
            "Observation is fail-soft: an observation failure never fails the pipeline.",
            "The optional tracing dependency stays confined to its adapter boundary.",
        ),
        required_before_cloud=(
            "A future export path must map native domain events to an external "
            "telemetry backend without back-propagating vendor naming into the "
            "core domain model.",
            "Observations must remain explanatory and must never become a "
            "control-plane or retry source of truth.",
        ),
        deferred_capabilities=(
            "Export to an external telemetry backend (deferred to a future phase).",
            "Collector / vendor field mapping (deferred).",
            "Dashboards, service-level objectives, and alerting (deferred).",
        ),
        explicit_non_goals=(
            "No external telemetry export wiring and no telemetry vendor integration.",
            "No collector, dashboard, service-level-objective, or alerting implementation.",
            "No expansion of the observer event vocabulary.",
            "No new telemetry dependency.",
        ),
    )


def _recovery_boundary() -> BoundarySummary:
    """Recovery/idempotency/distributed-safety boundary (backend-owned)."""
    return BoundarySummary(
        boundary_name=RECOVERY_BOUNDARY,
        active_backend=(
            "Backend-owned durable recovery lineage and eligibility, recorded in "
            "the local SQLite store and decided by the backend."
        ),
        status=BoundaryStatus.LOCAL_ACTIVE,
        source_of_truth=(
            "Durable backend state: recovery eligibility, attempt limits, and "
            "lineage are read from the store, never from observations."
        ),
        current_guarantees=(
            "Recovery eligibility is backend-decided and bounded by existing attempt limits.",
            "Recovery lineage is durably recorded; rejected requests stay visible.",
            "A single in-process worker prevents double execution within one process.",
        ),
        required_before_cloud=(
            "Cross-worker duplicate prevention must be proven before more than "
            "one worker can execute recovery.",
            "Distributed idempotency and coordination must be backend-decided and "
            "durable, not inferred from observations.",
            "Attempt-limit and eligibility semantics must remain unchanged across "
            "the distributed boundary.",
        ),
        deferred_capabilities=(
            "Distributed idempotency store (deferred to a future phase).",
            "Cross-worker duplicate prevention and distributed coordination (deferred).",
            "Cloud retry orchestration (deferred).",
            "Dead-letter replay (deferred).",
        ),
        explicit_non_goals=(
            "No distributed lock or coordination service.",
            "No new retry engine, idempotency store, or duplicate-prevention mechanism.",
            "No change to attempt limits or recovery eligibility behaviour.",
            "No scheduler, background worker, or dead-letter replay.",
        ),
    )


def evaluate_boundary_readiness(
    runtime_config: RuntimeConfig,
    config: StoryTimeConfig,
) -> BoundaryReadinessSnapshot:
    """Return a pure, configuration-derived :class:`BoundaryReadinessSnapshot`.

    Side-effect-free: it derives every boundary from *runtime_config* and
    *config* and the role's default behaviour. It starts no worker, claims no
    queue work, binds no socket, and opens no database. The local backends are
    active and proven; all cloud-growth capability is recorded as deferred and
    is not implemented here.
    """
    role = runtime_config.role
    return BoundaryReadinessSnapshot(
        generated_for_runtime_role=role,
        deployment=runtime_config.deployment,
        environment=runtime_config.environment,
        queue=_queue_boundary(role),
        artifacts=_artifact_boundary(),
        observability=_observability_boundary(config),
        recovery=_recovery_boundary(),
        warnings=(),
    )
