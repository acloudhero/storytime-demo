"""SQLite state store.

ARCH-LOCK: Single-transaction persistence
DO NOT REFACTOR: A stage's events and its state mutations must be committed in
ONE transaction (use StateStore.transaction()). Do not split them into
separate autocommitted writes.
Rationale: Round 7 prerequisite correction 2. Partial persistence would let
the event_log and the run state disagree after a crash.

The store imports only storytime.events. It deals in primitives so that the
state layer stays free of higher-level orchestration types (Architecture
Baseline section 3, module import direction).
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from storytime.events import PipelineEvent
from storytime.state.schema import MIGRATIONS


@dataclass(frozen=True, slots=True)
class RunRecord:
    """A row of the pipeline_run table."""

    pipeline_run_id: str
    created_at: str
    updated_at: str
    current_stage: str
    status: str
    source_manifest_hash: str
    run_dir: str
    # Phase 4.1: the interactive approval gates this run was configured with
    # ("text" and/or "audio"). Empty for an ungated run. Resume rebuilds the
    # run's exact stage list from this, so a gate that has not been reached
    # yet is still re-inserted.
    gates: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class WorkItemRecord:
    """A row of the work_queue table (Phase 14C.1 local durable queue).

    owner and lease_expires_at are the claim/lease mechanics used to prevent
    double-execution and recover stale claims; they are adapter-internal and
    must never be exposed through the read model.
    """

    work_id: str
    pipeline_run_id: str
    scenario: str
    fixture_id: str
    state: str
    owner: str | None
    lease_expires_at: str | None
    attempts: int
    enqueued_at: str
    updated_at: str
    failure_reason: str | None


@dataclass(frozen=True, slots=True)
class RecoveryActionRecord:
    """A row of the recovery_action table (Phase 14C.5.1 recovery lineage).

    Durable, backend-owned recovery lineage. It links the ORIGINAL failed
    execution identity (``original_run_id`` / ``original_work_item_id``) to the
    NEW recovery execution identity (``recovery_run_id`` /
    ``recovery_work_item_id``), and is the SOURCE OF TRUTH for recovery lineage.
    Observer (QueueWorkerEvent) events remain explanatory only. ``decision`` /
    ``rejection_reason`` carry the bounded eligibility outcome when a request is
    rejected. ``status`` moves through requested -> created | rejected | failed.
    """

    recovery_action_id: str
    original_run_id: str
    original_work_item_id: str
    recovery_run_id: str | None
    recovery_work_item_id: str | None
    recovery_reason: str
    requested_by: str
    requested_at: str
    status: str
    decision: str | None
    rejection_reason: str | None
    attempt_number: int
    updated_at: str


@dataclass(frozen=True, slots=True)
class PublishedEpisodeRecord:
    """A row of the published_episode table."""

    episode_guid: str
    pipeline_run_id: str
    title: str
    published_at: str
    audio_path: str
    audio_bytes: int
    duration_seconds: float
    feed_version: int
    # Phase 6 (OI-11): episode-level description, persisted so a later publish
    # can regenerate a faithful multi-item feed. Defaulted for pre-6 rows.
    description: str = ""


@dataclass(frozen=True, slots=True)
class StageExecutionRecord:
    """A row of the stage_execution table."""

    pipeline_run_id: str
    stage_name: str
    started_at: str
    ended_at: str | None
    status: str
    trace_id: str | None
    span_id: str | None
    error_kind: str | None
    error_message: str | None
    parent_trace_id: str | None = None


@dataclass(frozen=True, slots=True)
class ApprovalRecord:
    """A row of the approval table — a persisted operator decision."""

    pipeline_run_id: str
    stage_name: str
    decision: str
    operator: str
    decided_at: str
    notes: str | None


@dataclass(frozen=True, slots=True)
class StageArtifactRecord:
    """A row of the stage_artifact table — one artifact-envelope key.

    artifact_key is a RELATIVE storage key; resume resolves it through the
    configured StorageAdapter root so a relocated workspace still rehydrates.
    """

    pipeline_run_id: str
    stage_name: str
    artifact_key: str
    recorded_at: str


@dataclass(frozen=True, slots=True)
class TrustEnvelopeRecord:
    """A row of the trust_envelope projection table (Phase 9B, §24.7/§24.8).

    This is the SQLite *projection* of a run's Trust Envelope governance
    record. The durable Trust Envelope artifact named by ``envelope_key`` is
    the governance source of truth; this row is an operational-query
    convenience rebuildable from it. The projection carries only bounded status
    fields — never the free-text review_context_summary / governance_notes,
    which stay in the durable artifact.
    """

    pipeline_run_id: str
    source_ref: str
    schema_version: str
    license_type: str
    decision: str
    decision_timestamp: str
    approver_id: str
    blocked_reason: str | None
    envelope_key: str
    recorded_at: str


class StateStore:
    """A thin, explicit wrapper over the StoryTime SQLite database."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._conn = connection

    # -- lifecycle ---------------------------------------------------------

    @classmethod
    def open(cls, db_path: Path) -> StateStore:
        """Open (creating if needed) the database at *db_path*.

        Enables WAL journalling and foreign keys, then applies migrations.
        """
        db_path.parent.mkdir(parents=True, exist_ok=True)
        # isolation_level=None -> autocommit; transactions are explicit.
        conn = sqlite3.connect(db_path, isolation_level=None)
        conn.row_factory = sqlite3.Row
        # ARCH-LOCK: WAL mode is mandatory (Architecture Baseline section 5).
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        store = cls(conn)
        store._apply_migrations()
        return store

    def close(self) -> None:
        """Close the underlying connection."""
        self._conn.close()

    def __enter__(self) -> StateStore:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # -- introspection -----------------------------------------------------

    def journal_mode(self) -> str:
        """Return the active SQLite journal mode (expected: 'wal')."""
        row = self._conn.execute("PRAGMA journal_mode").fetchone()
        return str(row[0]).lower()

    def current_schema_version(self) -> int:
        """Return the highest applied schema version (0 if none)."""
        table = self._conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='schema_version'"
        ).fetchone()
        if table is None:
            return 0
        row = self._conn.execute("SELECT MAX(version) AS v FROM schema_version").fetchone()
        return int(row["v"]) if row is not None and row["v"] is not None else 0

    def table_names(self) -> set[str]:
        """Return the set of user table names in the database."""
        rows = self._conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        return {str(r["name"]) for r in rows}

    def _apply_migrations(self) -> None:
        current = self.current_schema_version()
        for version, ddl in MIGRATIONS:
            if version > current:
                self._conn.executescript(ddl)
                self._conn.execute(
                    "INSERT INTO schema_version(version, applied_at) "
                    "VALUES (?, datetime('now'))",
                    (version,),
                )

    # -- transactions ------------------------------------------------------

    @contextmanager
    def transaction(self) -> Iterator[None]:
        """Run a block as a single SQLite transaction (BEGIN/COMMIT/ROLLBACK)."""
        self._conn.execute("BEGIN")
        try:
            yield
        except BaseException:
            self._conn.execute("ROLLBACK")
            raise
        else:
            self._conn.execute("COMMIT")

    # -- writes ------------------------------------------------------------

    def create_run(self, run: RunRecord) -> None:
        """Insert a new pipeline_run row."""
        self._conn.execute(
            "INSERT INTO pipeline_run "
            "(pipeline_run_id, created_at, updated_at, current_stage, status, "
            " source_manifest_hash, run_dir, gates) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                run.pipeline_run_id,
                run.created_at,
                run.updated_at,
                run.current_stage,
                run.status,
                run.source_manifest_hash,
                run.run_dir,
                ",".join(run.gates),
            ),
        )

    def update_run_state(
        self,
        pipeline_run_id: str,
        *,
        status: str,
        current_stage: str,
        updated_at: str,
    ) -> None:
        """Update the status/current_stage of an existing run."""
        self._conn.execute(
            "UPDATE pipeline_run SET status=?, current_stage=?, updated_at=? "
            "WHERE pipeline_run_id=?",
            (status, current_stage, updated_at, pipeline_run_id),
        )

    def append_event(
        self,
        event: PipelineEvent,
        *,
        trace_id: str | None = None,
        span_id: str | None = None,
    ) -> None:
        """Append a single event to the append-only event_log."""
        self._conn.execute(
            "INSERT INTO event_log "
            "(pipeline_run_id, occurred_at, event_type, payload_json, trace_id, span_id) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                event.pipeline_run_id,
                event.occurred_at.isoformat(),
                str(event.event_type),
                event.payload_json(),
                trace_id,
                span_id,
            ),
        )

    def append_events(
        self,
        events: Iterable[PipelineEvent],
        *,
        trace_id: str | None = None,
        span_id: str | None = None,
    ) -> None:
        """Append several events. Call inside transaction() for atomicity."""
        for event in events:
            self.append_event(event, trace_id=trace_id, span_id=span_id)

    def record_stage_execution(
        self,
        *,
        pipeline_run_id: str,
        stage_name: str,
        started_at: str,
        ended_at: str | None,
        status: str,
        trace_id: str | None = None,
        span_id: str | None = None,
        parent_trace_id: str | None = None,
        error_kind: str | None = None,
        error_message: str | None = None,
    ) -> None:
        """Insert a stage_execution row."""
        self._conn.execute(
            "INSERT INTO stage_execution "
            "(pipeline_run_id, stage_name, started_at, ended_at, status, "
            " trace_id, span_id, parent_trace_id, error_kind, error_message) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                pipeline_run_id,
                stage_name,
                started_at,
                ended_at,
                status,
                trace_id,
                span_id,
                parent_trace_id,
                error_kind,
                error_message,
            ),
        )

    # -- reads -------------------------------------------------------------

    @staticmethod
    def _run_record_from_row(row: sqlite3.Row) -> RunRecord:
        """Build a RunRecord from a pipeline_run row, parsing the gates column.

        gates is stored comma-joined; a pre-4.1 row (migration 0003 DEFAULT '')
        parses to the empty tuple, i.e. an ungated run.
        """
        raw_gates = str(row["gates"] or "")
        gates = tuple(g for g in raw_gates.split(",") if g)
        return RunRecord(
            pipeline_run_id=row["pipeline_run_id"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            current_stage=row["current_stage"],
            status=row["status"],
            source_manifest_hash=row["source_manifest_hash"],
            run_dir=row["run_dir"],
            gates=gates,
        )

    def get_run(self, pipeline_run_id: str) -> RunRecord | None:
        """Return the run with *pipeline_run_id*, or None if absent."""
        row = self._conn.execute(
            "SELECT * FROM pipeline_run WHERE pipeline_run_id=?",
            (pipeline_run_id,),
        ).fetchone()
        if row is None:
            return None
        return self._run_record_from_row(row)

    def list_runs(self) -> tuple[RunRecord, ...]:
        """Return every pipeline_run row, newest first."""
        rows = self._conn.execute(
            "SELECT * FROM pipeline_run "
            "ORDER BY created_at DESC, pipeline_run_id DESC"
        ).fetchall()
        return tuple(self._run_record_from_row(r) for r in rows)

    def count_events(self, pipeline_run_id: str) -> int:
        """Return the number of event_log rows for *pipeline_run_id*."""
        row = self._conn.execute(
            "SELECT COUNT(*) AS n FROM event_log WHERE pipeline_run_id=?",
            (pipeline_run_id,),
        ).fetchone()
        return int(row["n"])

    # -- Phase 3 writes: approval / published_episode -----------------------

    def record_approval(
        self,
        *,
        pipeline_run_id: str,
        stage_name: str,
        decision: str,
        operator: str,
        decided_at: str,
        notes: str | None = None,
        inbound_trace_id: str | None = None,
        outbound_trace_id: str | None = None,
    ) -> None:
        """Insert an approval row. Call inside transaction() for atomicity."""
        self._conn.execute(
            "INSERT INTO approval "
            "(pipeline_run_id, stage_name, decision, operator, decided_at, "
            " notes, inbound_trace_id, outbound_trace_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                pipeline_run_id,
                stage_name,
                decision,
                operator,
                decided_at,
                notes,
                inbound_trace_id,
                outbound_trace_id,
            ),
        )

    def set_approval_outbound_trace(
        self, *, pipeline_run_id: str, stage_name: str, trace_id: str
    ) -> None:
        """Stamp an approval row's outbound_trace_id, but only if still NULL.

        Phase 5: the outbound trace is the resumed run's trace -- the trace
        that continues *out of* an approval gate. It is recorded once, on the
        first resume that crosses the gate; a later resume must not overwrite
        the original linked-trace anchor, hence ``WHERE outbound_trace_id IS
        NULL``. This is view metadata layered onto the durable approval row;
        it never changes the recorded decision. Call inside transaction().
        """
        self._conn.execute(
            "UPDATE approval SET outbound_trace_id=? "
            "WHERE pipeline_run_id=? AND stage_name=? AND outbound_trace_id IS NULL",
            (trace_id, pipeline_run_id, stage_name),
        )

    def record_published_episode(
        self,
        *,
        episode_guid: str,
        pipeline_run_id: str,
        title: str,
        published_at: str,
        audio_path: str,
        audio_bytes: int,
        duration_seconds: float,
        feed_version: int,
        description: str = "",
    ) -> None:
        """Insert a published_episode row. Call inside transaction()."""
        self._conn.execute(
            "INSERT INTO published_episode "
            "(episode_guid, pipeline_run_id, title, published_at, audio_path, "
            " audio_bytes, duration_seconds, feed_version, description) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                episode_guid,
                pipeline_run_id,
                title,
                published_at,
                audio_path,
                audio_bytes,
                duration_seconds,
                feed_version,
                description,
            ),
        )

    # -- Phase 3 reads ------------------------------------------------------

    def count_approvals(self, pipeline_run_id: str) -> int:
        """Return the number of approval rows for *pipeline_run_id*."""
        row = self._conn.execute(
            "SELECT COUNT(*) AS n FROM approval WHERE pipeline_run_id=?",
            (pipeline_run_id,),
        ).fetchone()
        return int(row["n"])

    @staticmethod
    def _published_episode_from_row(row: sqlite3.Row) -> PublishedEpisodeRecord:
        """Build a PublishedEpisodeRecord from a published_episode row.

        description is read defensively: a pre-Phase-6 row predates migration
        0004 only if the database was never migrated, which open() prevents —
        but ``row["description"] or ""`` keeps a NULL impossible-to-reach value
        harmless.
        """
        return PublishedEpisodeRecord(
            episode_guid=row["episode_guid"],
            pipeline_run_id=row["pipeline_run_id"],
            title=row["title"],
            published_at=row["published_at"],
            audio_path=row["audio_path"],
            audio_bytes=int(row["audio_bytes"]),
            duration_seconds=float(row["duration_seconds"]),
            feed_version=int(row["feed_version"]),
            description=str(row["description"] or ""),
        )

    def get_published_episode(
        self, episode_guid: str
    ) -> PublishedEpisodeRecord | None:
        """Return the published_episode with *episode_guid*, or None."""
        row = self._conn.execute(
            "SELECT * FROM published_episode WHERE episode_guid=?",
            (episode_guid,),
        ).fetchone()
        if row is None:
            return None
        return self._published_episode_from_row(row)

    def list_published_episodes(self) -> tuple[PublishedEpisodeRecord, ...]:
        """Return every published_episode row, newest publication first.

        Phase 6 (OI-11): the publish stage aggregates these prior episodes into
        a multi-item feed. published_at is a stored ISO-8601 timestamp, so a
        lexical ORDER BY DESC is also a chronological newest-first order;
        episode_guid (a ULID) is the stable tie-breaker.
        """
        rows = self._conn.execute(
            "SELECT * FROM published_episode "
            "ORDER BY published_at DESC, episode_guid DESC"
        ).fetchall()
        return tuple(self._published_episode_from_row(r) for r in rows)

    def event_types(self, pipeline_run_id: str) -> tuple[str, ...]:
        """Return the event_log event types for a run, in insertion order."""
        rows = self._conn.execute(
            "SELECT event_type FROM event_log WHERE pipeline_run_id=? ORDER BY id",
            (pipeline_run_id,),
        ).fetchall()
        return tuple(str(r["event_type"]) for r in rows)

    def list_stage_executions(
        self, pipeline_run_id: str
    ) -> tuple[StageExecutionRecord, ...]:
        """Return the stage_execution rows for a run, in insertion order."""
        rows = self._conn.execute(
            "SELECT * FROM stage_execution WHERE pipeline_run_id=? ORDER BY id",
            (pipeline_run_id,),
        ).fetchall()
        return tuple(
            StageExecutionRecord(
                pipeline_run_id=r["pipeline_run_id"],
                stage_name=r["stage_name"],
                started_at=r["started_at"],
                ended_at=r["ended_at"],
                status=r["status"],
                trace_id=r["trace_id"],
                span_id=r["span_id"],
                error_kind=r["error_kind"],
                error_message=r["error_message"],
                parent_trace_id=r["parent_trace_id"],
            )
            for r in rows
        )

    # -- Phase 4 writes: stage_artifact -------------------------------------

    def record_stage_artifacts(
        self,
        *,
        pipeline_run_id: str,
        stage_name: str,
        artifact_keys: Iterable[str],
        recorded_at: str,
    ) -> None:
        """Append a stage's produced artifact-envelope keys. Call in transaction().

        artifact_keys are relative storage keys. Storing them lets a resumed
        run rehydrate prior-stage outputs from SQLite (Phase 4 OI-10).
        """
        for key in artifact_keys:
            self._conn.execute(
                "INSERT INTO stage_artifact "
                "(pipeline_run_id, stage_name, artifact_key, recorded_at) "
                "VALUES (?, ?, ?, ?)",
                (pipeline_run_id, stage_name, key, recorded_at),
            )

    # -- Phase 4 reads ------------------------------------------------------

    def list_stage_artifacts(
        self, pipeline_run_id: str
    ) -> tuple[StageArtifactRecord, ...]:
        """Return the stage_artifact rows for a run, in insertion order."""
        rows = self._conn.execute(
            "SELECT * FROM stage_artifact WHERE pipeline_run_id=? ORDER BY id",
            (pipeline_run_id,),
        ).fetchall()
        return tuple(
            StageArtifactRecord(
                pipeline_run_id=r["pipeline_run_id"],
                stage_name=r["stage_name"],
                artifact_key=r["artifact_key"],
                recorded_at=r["recorded_at"],
            )
            for r in rows
        )

    # -- Phase 9B writes / reads: trust_envelope projection -----------------

    def record_trust_envelope(
        self,
        *,
        pipeline_run_id: str,
        source_ref: str,
        schema_version: str,
        license_type: str,
        decision: str,
        decision_timestamp: str,
        approver_id: str,
        blocked_reason: str | None,
        envelope_key: str,
        recorded_at: str,
    ) -> None:
        """Insert the SQLite projection of a run's Trust Envelope.

        Call inside transaction(). This is a *projection* of the durable Trust
        Envelope artifact (the governance source of truth, §24.7); ``envelope_key``
        is the relative storage key of that artifact. Only bounded status
        fields are projected — the free-text review summary / notes stay in the
        durable artifact.
        """
        self._conn.execute(
            "INSERT INTO trust_envelope "
            "(pipeline_run_id, source_ref, schema_version, license_type, "
            " decision, decision_timestamp, approver_id, blocked_reason, "
            " envelope_key, recorded_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                pipeline_run_id,
                source_ref,
                schema_version,
                license_type,
                decision,
                decision_timestamp,
                approver_id,
                blocked_reason,
                envelope_key,
                recorded_at,
            ),
        )

    @staticmethod
    def _trust_envelope_from_row(row: sqlite3.Row) -> TrustEnvelopeRecord:
        """Build a TrustEnvelopeRecord from a trust_envelope row."""
        return TrustEnvelopeRecord(
            pipeline_run_id=row["pipeline_run_id"],
            source_ref=row["source_ref"],
            schema_version=row["schema_version"],
            license_type=row["license_type"],
            decision=row["decision"],
            decision_timestamp=row["decision_timestamp"],
            approver_id=row["approver_id"],
            blocked_reason=row["blocked_reason"],
            envelope_key=row["envelope_key"],
            recorded_at=row["recorded_at"],
        )

    def latest_trust_envelope(
        self, pipeline_run_id: str
    ) -> TrustEnvelopeRecord | None:
        """Return the most recent trust_envelope projection row for a run, or None.

        The projection is queryable status; the durable artifact named by
        ``envelope_key`` remains the governance source of truth.
        """
        row = self._conn.execute(
            "SELECT * FROM trust_envelope WHERE pipeline_run_id=? "
            "ORDER BY id DESC LIMIT 1",
            (pipeline_run_id,),
        ).fetchone()
        if row is None:
            return None
        return self._trust_envelope_from_row(row)

    def list_trust_envelopes(
        self, pipeline_run_id: str
    ) -> tuple[TrustEnvelopeRecord, ...]:
        """Return the trust_envelope projection rows for a run, in insertion order."""
        rows = self._conn.execute(
            "SELECT * FROM trust_envelope WHERE pipeline_run_id=? ORDER BY id",
            (pipeline_run_id,),
        ).fetchall()
        return tuple(self._trust_envelope_from_row(r) for r in rows)

    def list_approvals(self, pipeline_run_id: str) -> tuple[ApprovalRecord, ...]:
        """Return the approval rows for a run, oldest decision first."""
        rows = self._conn.execute(
            "SELECT * FROM approval WHERE pipeline_run_id=? ORDER BY id",
            (pipeline_run_id,),
        ).fetchall()
        return tuple(
            ApprovalRecord(
                pipeline_run_id=r["pipeline_run_id"],
                stage_name=r["stage_name"],
                decision=r["decision"],
                operator=r["operator"],
                decided_at=r["decided_at"],
                notes=r["notes"],
            )
            for r in rows
        )

    def latest_approval(
        self, pipeline_run_id: str, stage_name: str
    ) -> ApprovalRecord | None:
        """Return the most recent approval row for a run's gate, or None.

        *stage_name* is the gate stage ("approve_text" / "approve_audio"), so
        the manifest-derived ingest approval row is never mistaken for an
        operator gate decision.
        """
        row = self._conn.execute(
            "SELECT * FROM approval WHERE pipeline_run_id=? AND stage_name=? "
            "ORDER BY id DESC LIMIT 1",
            (pipeline_run_id, stage_name),
        ).fetchone()
        if row is None:
            return None
        return ApprovalRecord(
            pipeline_run_id=row["pipeline_run_id"],
            stage_name=row["stage_name"],
            decision=row["decision"],
            operator=row["operator"],
            decided_at=row["decided_at"],
            notes=row["notes"],
        )

    # -- work queue (Phase 14C.1 local durable queue) ----------------------

    @staticmethod
    def _work_item_from_row(row: sqlite3.Row) -> WorkItemRecord:
        return WorkItemRecord(
            work_id=row["work_id"],
            pipeline_run_id=row["pipeline_run_id"],
            scenario=row["scenario"],
            fixture_id=row["fixture_id"],
            state=row["state"],
            owner=row["owner"],
            lease_expires_at=row["lease_expires_at"],
            attempts=int(row["attempts"]),
            enqueued_at=row["enqueued_at"],
            updated_at=row["updated_at"],
            failure_reason=row["failure_reason"],
        )

    def enqueue_work(
        self,
        *,
        work_id: str,
        pipeline_run_id: str,
        scenario: str,
        fixture_id: str,
        enqueued_at: str,
    ) -> None:
        """Insert a durable queued work item (state='queued')."""
        self._conn.execute(
            "INSERT INTO work_queue(work_id, pipeline_run_id, scenario, "
            "fixture_id, state, owner, lease_expires_at, attempts, enqueued_at, "
            "updated_at, failure_reason) VALUES (?, ?, ?, ?, 'queued', NULL, "
            "NULL, 0, ?, ?, NULL)",
            (work_id, pipeline_run_id, scenario, fixture_id, enqueued_at, enqueued_at),
        )

    def claim_next_work(
        self, *, owner: str, now: str, lease_expires_at: str
    ) -> WorkItemRecord | None:
        """Atomically claim the oldest queued work item for *owner*.

        Uses ``BEGIN IMMEDIATE`` to take a write lock so concurrent claimers
        serialise, then a conditional update guarded on ``state='queued'`` so
        only one claimer can win a given item — preventing double-claim and
        therefore double-execution.
        """
        self._conn.execute("BEGIN IMMEDIATE")
        try:
            row = self._conn.execute(
                "SELECT work_id FROM work_queue WHERE state='queued' "
                "ORDER BY enqueued_at, work_id LIMIT 1"
            ).fetchone()
            if row is None:
                self._conn.execute("COMMIT")
                return None
            work_id = row["work_id"]
            cur = self._conn.execute(
                "UPDATE work_queue SET state='claimed', owner=?, "
                "lease_expires_at=?, attempts=attempts+1, updated_at=? "
                "WHERE work_id=? AND state='queued'",
                (owner, lease_expires_at, now, work_id),
            )
            if cur.rowcount != 1:
                # Lost the race to another claimer.
                self._conn.execute("COMMIT")
                return None
            self._conn.execute("COMMIT")
        except BaseException:
            self._conn.execute("ROLLBACK")
            raise
        claimed = self._conn.execute(
            "SELECT * FROM work_queue WHERE work_id=?", (work_id,)
        ).fetchone()
        return self._work_item_from_row(claimed)

    def mark_work_running(self, *, work_id: str, owner: str, now: str) -> bool:
        """Transition a claimed item owned by *owner* to running."""
        cur = self._conn.execute(
            "UPDATE work_queue SET state='running', updated_at=? "
            "WHERE work_id=? AND owner=? AND state='claimed'",
            (now, work_id, owner),
        )
        return cur.rowcount == 1

    def mark_work_completed(self, *, work_id: str, owner: str, now: str) -> bool:
        """Transition a claimed/running item owned by *owner* to completed."""
        cur = self._conn.execute(
            "UPDATE work_queue SET state='completed', updated_at=? "
            "WHERE work_id=? AND owner=? AND state IN ('claimed','running')",
            (now, work_id, owner),
        )
        return cur.rowcount == 1

    def mark_work_failed(
        self, *, work_id: str, owner: str, now: str, reason: str
    ) -> bool:
        """Transition a claimed/running item owned by *owner* to failed."""
        cur = self._conn.execute(
            "UPDATE work_queue SET state='failed', failure_reason=?, "
            "updated_at=? WHERE work_id=? AND owner=? AND state IN "
            "('claimed','running')",
            (reason, now, work_id, owner),
        )
        return cur.rowcount == 1

    def recover_stale_work(
        self, *, now: str, max_attempts: int
    ) -> tuple[WorkItemRecord, ...]:
        """Requeue or fail claimed/running items whose lease has expired.

        Simulates recovery after a worker is lost mid-claim/run: an expired
        lease is reset to ``queued`` (clearing the owner) so another worker can
        pick it up, unless it has already used up ``max_attempts``, in which
        case it is marked ``failed`` so it cannot loop forever. Runs under
        ``BEGIN IMMEDIATE`` so recovery and claiming cannot race.
        """
        self._conn.execute("BEGIN IMMEDIATE")
        try:
            rows = self._conn.execute(
                "SELECT * FROM work_queue WHERE state IN ('claimed','running') "
                "AND lease_expires_at IS NOT NULL AND lease_expires_at < ? "
                "ORDER BY enqueued_at, work_id",
                (now,),
            ).fetchall()
            recovered: list[WorkItemRecord] = []
            for row in rows:
                work_id = row["work_id"]
                if int(row["attempts"]) >= max_attempts:
                    self._conn.execute(
                        "UPDATE work_queue SET state='failed', "
                        "failure_reason=?, owner=NULL, lease_expires_at=NULL, "
                        "updated_at=? WHERE work_id=?",
                        (
                            "work item lease expired after maximum attempts "
                            "(local stale-claim recovery)",
                            now,
                            work_id,
                        ),
                    )
                else:
                    self._conn.execute(
                        "UPDATE work_queue SET state='queued', owner=NULL, "
                        "lease_expires_at=NULL, updated_at=? WHERE work_id=?",
                        (now, work_id),
                    )
                recovered.append(
                    self._work_item_from_row(
                        self._conn.execute(
                            "SELECT * FROM work_queue WHERE work_id=?", (work_id,)
                        ).fetchone()
                    )
                )
            self._conn.execute("COMMIT")
        except BaseException:
            self._conn.execute("ROLLBACK")
            raise
        return tuple(recovered)

    def get_work_item(self, work_id: str) -> WorkItemRecord | None:
        """Return a work item by id, or None."""
        row = self._conn.execute(
            "SELECT * FROM work_queue WHERE work_id=?", (work_id,)
        ).fetchone()
        return self._work_item_from_row(row) if row is not None else None

    def get_work_item_for_run(self, pipeline_run_id: str) -> WorkItemRecord | None:
        """Return the most recent work item for a run, or None."""
        row = self._conn.execute(
            "SELECT * FROM work_queue WHERE pipeline_run_id=? "
            "ORDER BY enqueued_at DESC, work_id DESC LIMIT 1",
            (pipeline_run_id,),
        ).fetchone()
        return self._work_item_from_row(row) if row is not None else None

    def list_work_items(self) -> tuple[WorkItemRecord, ...]:
        """Return all work items, oldest enqueued first."""
        rows = self._conn.execute(
            "SELECT * FROM work_queue ORDER BY enqueued_at, work_id"
        ).fetchall()
        return tuple(self._work_item_from_row(r) for r in rows)

    # -- recovery lineage (Phase 14C.5.1) ----------------------------------

    @staticmethod
    def _recovery_action_from_row(row: sqlite3.Row) -> RecoveryActionRecord:
        return RecoveryActionRecord(
            recovery_action_id=row["recovery_action_id"],
            original_run_id=row["original_run_id"],
            original_work_item_id=row["original_work_item_id"],
            recovery_run_id=row["recovery_run_id"],
            recovery_work_item_id=row["recovery_work_item_id"],
            recovery_reason=row["recovery_reason"],
            requested_by=row["requested_by"],
            requested_at=row["requested_at"],
            status=row["status"],
            decision=row["decision"],
            rejection_reason=row["rejection_reason"],
            attempt_number=int(row["attempt_number"]),
            updated_at=row["updated_at"],
        )

    def insert_recovery_action(self, record: RecoveryActionRecord) -> None:
        """Insert a recovery-action row (used for durably-visible rejections)."""
        self._conn.execute(
            "INSERT INTO recovery_action (recovery_action_id, original_run_id, "
            "original_work_item_id, recovery_run_id, recovery_work_item_id, "
            "recovery_reason, requested_by, requested_at, status, decision, "
            "rejection_reason, attempt_number, updated_at) VALUES "
            "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                record.recovery_action_id,
                record.original_run_id,
                record.original_work_item_id,
                record.recovery_run_id,
                record.recovery_work_item_id,
                record.recovery_reason,
                record.requested_by,
                record.requested_at,
                record.status,
                record.decision,
                record.rejection_reason,
                record.attempt_number,
                record.updated_at,
            ),
        )

    def active_recovery_action_for(
        self, original_work_item_id: str
    ) -> RecoveryActionRecord | None:
        """Return an in-flight recovery action (status 'requested') if any.

        'requested' is the brief in-flight window before a recovery execution is
        created; it is the slot used for duplicate-prevention under concurrency.
        A 'created' action is a consumed attempt (counted by
        :meth:`count_recovery_attempts_for`), not an in-flight duplicate.
        """
        row = self._conn.execute(
            "SELECT * FROM recovery_action WHERE original_work_item_id=? "
            "AND status = 'requested' "
            "ORDER BY requested_at DESC, recovery_action_id DESC LIMIT 1",
            (original_work_item_id,),
        ).fetchone()
        return self._recovery_action_from_row(row) if row is not None else None

    def count_recovery_attempts_for(self, original_work_item_id: str) -> int:
        """Count recovery actions that consume an attempt (non-rejected)."""
        row = self._conn.execute(
            "SELECT COUNT(*) AS n FROM recovery_action "
            "WHERE original_work_item_id=? AND status IN "
            "('requested','created','failed')",
            (original_work_item_id,),
        ).fetchone()
        return int(row["n"]) if row is not None else 0

    def atomically_create_recovery_action(
        self, record: RecoveryActionRecord, *, max_attempts: int
    ) -> bool:
        """Create a recovery action iff no active one exists and attempts remain.

        Uses ``BEGIN IMMEDIATE`` to take a write lock so two concurrent recovery
        requests for the same original failed work item cannot both create an
        active recovery action (duplicate-prevention under local SQLite). Returns
        True if the row was created, False if a duplicate-active or
        max-attempts condition lost the race.
        """
        self._conn.execute("BEGIN IMMEDIATE")
        try:
            active = self._conn.execute(
                "SELECT 1 FROM recovery_action WHERE original_work_item_id=? "
                "AND status = 'requested' LIMIT 1",
                (record.original_work_item_id,),
            ).fetchone()
            if active is not None:
                self._conn.execute("COMMIT")
                return False
            used = self._conn.execute(
                "SELECT COUNT(*) AS n FROM recovery_action "
                "WHERE original_work_item_id=? AND status IN "
                "('requested','created','failed')",
                (record.original_work_item_id,),
            ).fetchone()
            if int(used["n"]) >= max_attempts:
                self._conn.execute("COMMIT")
                return False
            self._conn.execute(
                "INSERT INTO recovery_action (recovery_action_id, "
                "original_run_id, original_work_item_id, recovery_run_id, "
                "recovery_work_item_id, recovery_reason, requested_by, "
                "requested_at, status, decision, rejection_reason, "
                "attempt_number, updated_at) VALUES "
                "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    record.recovery_action_id,
                    record.original_run_id,
                    record.original_work_item_id,
                    record.recovery_run_id,
                    record.recovery_work_item_id,
                    record.recovery_reason,
                    record.requested_by,
                    record.requested_at,
                    record.status,
                    record.decision,
                    record.rejection_reason,
                    record.attempt_number,
                    record.updated_at,
                ),
            )
            self._conn.execute("COMMIT")
        except BaseException:
            self._conn.execute("ROLLBACK")
            raise
        return True

    def update_recovery_action(
        self,
        recovery_action_id: str,
        *,
        status: str | None = None,
        recovery_run_id: str | None = None,
        recovery_work_item_id: str | None = None,
        decision: str | None = None,
        rejection_reason: str | None = None,
        updated_at: str,
    ) -> None:
        """Update mutable recovery-action fields (only provided ones change)."""
        sets = ["updated_at=?"]
        params: list[object] = [updated_at]
        if status is not None:
            sets.append("status=?")
            params.append(status)
        if recovery_run_id is not None:
            sets.append("recovery_run_id=?")
            params.append(recovery_run_id)
        if recovery_work_item_id is not None:
            sets.append("recovery_work_item_id=?")
            params.append(recovery_work_item_id)
        if decision is not None:
            sets.append("decision=?")
            params.append(decision)
        if rejection_reason is not None:
            sets.append("rejection_reason=?")
            params.append(rejection_reason)
        params.append(recovery_action_id)
        self._conn.execute(
            f"UPDATE recovery_action SET {', '.join(sets)} "
            "WHERE recovery_action_id=?",
            tuple(params),
        )

    def get_recovery_action(
        self, recovery_action_id: str
    ) -> RecoveryActionRecord | None:
        """Return a recovery action by id, or None."""
        row = self._conn.execute(
            "SELECT * FROM recovery_action WHERE recovery_action_id=?",
            (recovery_action_id,),
        ).fetchone()
        return self._recovery_action_from_row(row) if row is not None else None

    def list_recovery_actions_for_run(
        self, original_run_id: str
    ) -> tuple[RecoveryActionRecord, ...]:
        """Return recovery actions for an original run, oldest first."""
        rows = self._conn.execute(
            "SELECT * FROM recovery_action WHERE original_run_id=? "
            "ORDER BY requested_at, recovery_action_id",
            (original_run_id,),
        ).fetchall()
        return tuple(self._recovery_action_from_row(r) for r in rows)

    def list_recovery_actions(self) -> tuple[RecoveryActionRecord, ...]:
        """Return all recovery actions, oldest requested first."""
        rows = self._conn.execute(
            "SELECT * FROM recovery_action "
            "ORDER BY requested_at, recovery_action_id"
        ).fetchall()
        return tuple(self._recovery_action_from_row(r) for r in rows)
