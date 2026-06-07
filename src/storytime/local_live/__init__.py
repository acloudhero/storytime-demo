"""Phase 14A.1/14B.1/14C.1 — local-live proof loop package.

A loopback-only, standard-library HTTP service that exposes backend-owned
durable SQLite state to the operator console's Live Proof Loop surface, plus a
controlled, fixture-based proof-run action. Phase 14C.1 separates request
acceptance from execution: a request reserves a run and enqueues a durable work
item, and a local worker claims and executes it. See:

- :mod:`storytime.local_live.read_model` — typed read-model DTOs.
- :mod:`storytime.local_live.proof_run` — the durable proof-run harness.
- :mod:`storytime.local_live.queue` — the local durable work-queue port + SQLite adapter.
- :mod:`storytime.local_live.worker` — the bounded local worker.
- :mod:`storytime.local_live.server` — the loopback HTTP API.
"""

from __future__ import annotations

from storytime.local_live.artifact_store import (
    ArtifactEvidence,
    ArtifactNotFoundError,
    ArtifactStore,
    ArtifactStoreError,
    LocalFilesystemArtifactStore,
    UnsafeArtifactKeyError,
)
from storytime.local_live.observability import (
    InMemoryQueueWorkerObserver,
    NullQueueWorkerObserver,
    QueueWorkerEvent,
    QueueWorkerEventSink,
    emit,
)
from storytime.local_live.proof_run import (
    APPROVED_FIXTURES,
    APPROVED_SCENARIOS,
    DEFAULT_FIXTURE,
    DEFAULT_SCENARIO,
    ProofRunError,
    execute_proof_run,
    reserve_proof_run,
    run_proof_fixture,
)
from storytime.local_live.queue import (
    SqliteWorkQueue,
    WorkQueue,
    WorkState,
)
from storytime.local_live.recovery import (
    DEFAULT_MAX_RECOVERY_ATTEMPTS,
    RecoveryEligibility,
    evaluate_recovery_eligibility,
    request_recovery,
)
from storytime.local_live.server import (
    LocalLiveService,
    default_allowed_origins,
    make_server,
    serve,
)
from storytime.local_live.worker import BackgroundWorker, LocalWorker

__all__ = [
    "APPROVED_FIXTURES",
    "APPROVED_SCENARIOS",
    "DEFAULT_FIXTURE",
    "DEFAULT_SCENARIO",
    "ArtifactEvidence",
    "ArtifactNotFoundError",
    "ArtifactStore",
    "ArtifactStoreError",
    "BackgroundWorker",
    "DEFAULT_MAX_RECOVERY_ATTEMPTS",
    "InMemoryQueueWorkerObserver",
    "LocalFilesystemArtifactStore",
    "LocalLiveService",
    "LocalWorker",
    "NullQueueWorkerObserver",
    "ProofRunError",
    "QueueWorkerEvent",
    "QueueWorkerEventSink",
    "RecoveryEligibility",
    "SqliteWorkQueue",
    "UnsafeArtifactKeyError",
    "WorkQueue",
    "WorkState",
    "default_allowed_origins",
    "emit",
    "evaluate_recovery_eligibility",
    "execute_proof_run",
    "make_server",
    "reserve_proof_run",
    "request_recovery",
    "run_proof_fixture",
    "serve",
]
