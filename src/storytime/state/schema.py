"""SQLite schema definition and migrations.

ARCH-LOCK: SQLite is the source of truth
DO NOT REFACTOR: event_log is an append-only SQLite table. Do not move it to
JSONL, and do not turn it into a replayable event-sourcing log in Phase 2 — it
is forensic/audit-only here.
Rationale: Architecture Baseline section 5 and Round 7 prerequisite
corrections 1 and 3.
"""

from __future__ import annotations

# Bump this when adding a migration. current_schema_version() compares against
# the schema_version table to decide which migrations to apply.
SCHEMA_VERSION = 7

_MIGRATION_0001 = """
CREATE TABLE schema_version (
    version     INTEGER NOT NULL,
    applied_at  TEXT NOT NULL
);

CREATE TABLE pipeline_run (
    pipeline_run_id      TEXT PRIMARY KEY,
    created_at           TEXT NOT NULL,
    updated_at           TEXT NOT NULL,
    current_stage        TEXT NOT NULL,
    status               TEXT NOT NULL,
    source_manifest_hash TEXT NOT NULL,
    run_dir              TEXT NOT NULL
);

CREATE TABLE stage_execution (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_run_id  TEXT NOT NULL REFERENCES pipeline_run(pipeline_run_id),
    stage_name       TEXT NOT NULL,
    started_at       TEXT NOT NULL,
    ended_at         TEXT,
    status           TEXT NOT NULL,
    trace_id         TEXT,
    span_id          TEXT,
    parent_trace_id  TEXT,
    error_kind       TEXT,
    error_message    TEXT
);

CREATE TABLE approval (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_run_id   TEXT NOT NULL REFERENCES pipeline_run(pipeline_run_id),
    stage_name        TEXT NOT NULL,
    decision          TEXT NOT NULL,
    operator          TEXT NOT NULL,
    decided_at        TEXT NOT NULL,
    notes             TEXT,
    inbound_trace_id  TEXT,
    outbound_trace_id TEXT
);

-- ARCH-LOCK: event_log is append-only and forensic-only in Phase 2.
CREATE TABLE event_log (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_run_id  TEXT NOT NULL,
    occurred_at      TEXT NOT NULL,
    event_type       TEXT NOT NULL,
    payload_json     TEXT NOT NULL,
    trace_id         TEXT,
    span_id          TEXT
);

CREATE TABLE published_episode (
    episode_guid     TEXT PRIMARY KEY,
    pipeline_run_id  TEXT NOT NULL REFERENCES pipeline_run(pipeline_run_id),
    title            TEXT NOT NULL,
    published_at     TEXT NOT NULL,
    audio_path       TEXT NOT NULL,
    audio_bytes      INTEGER NOT NULL,
    duration_seconds REAL NOT NULL,
    feed_version     INTEGER NOT NULL
);

CREATE INDEX idx_event_log_run ON event_log(pipeline_run_id);
CREATE INDEX idx_stage_execution_run ON stage_execution(pipeline_run_id);
"""

# ARCH-LOCK: SQLite is the source of truth (continued)
# DO NOT REFACTOR: stage_artifact records the artifact-envelope keys a stage
# produced, so a resumed run can rehydrate prior-stage outputs from SQLite.
# artifact_key is a RELATIVE storage key (resolved through the configured
# StorageAdapter root), never an absolute path — a run must survive its
# workspace being relocated. Like event_log this table is append-only.
# Rationale: Phase 4 OI-10 (resume/rehydration) and the filesystem-relativity
# requirement of the Phase 4 task spec.
_MIGRATION_0002 = """
CREATE TABLE stage_artifact (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_run_id  TEXT NOT NULL REFERENCES pipeline_run(pipeline_run_id),
    stage_name       TEXT NOT NULL,
    artifact_key     TEXT NOT NULL,          -- relative storage key, not absolute
    recorded_at      TEXT NOT NULL
);

CREATE INDEX idx_stage_artifact_run ON stage_artifact(pipeline_run_id);
"""

# Phase 4.1: pipeline_run.gates records which interactive approval gates a run
# was configured with ("text", "audio"), stored as a comma-joined label list.
# This is run-level CONFIGURATION, not derived state: resume must rebuild the
# exact stage list a run was created with, including a gate that has not been
# reached yet (e.g. an audio-gated run resumed while still paused at the text
# gate). An additive, defaulted column keeps every pre-4.1 run row valid
# (DEFAULT '' = no gates). gates carries only short, environment-agnostic
# labels — never a host name, slot, or absolute path — so it stays compatible
# with future Phase 7 blue/green attribution.
_MIGRATION_0003 = """
ALTER TABLE pipeline_run ADD COLUMN gates TEXT NOT NULL DEFAULT '';
"""

# Phase 6 (OI-11): published_episode.description stores the episode-level
# description text. The publish stage already builds this for the episode it
# publishes; persisting it is what lets a later publish regenerate a faithful
# MULTI-ITEM feed in which every prior <item> keeps its own description rather
# than an empty placeholder. An additive, defaulted column keeps every pre-6
# published_episode row valid (DEFAULT '' = no stored description, rendered as
# an empty <description>, still schema-valid).
_MIGRATION_0004 = """
ALTER TABLE published_episode ADD COLUMN description TEXT NOT NULL DEFAULT '';
"""

# Phase 9B (Architecture Baseline §24.7/§24.8): trust_envelope is the SQLite
# PROJECTION of the Trust Envelope governance record. The durable Trust
# Envelope artifact on disk (governance/trust-envelope.json in the run dir) is
# the governance SOURCE OF TRUTH for portability/recovery; this table is an
# operational-query convenience and is rebuildable from the durable artifacts —
# it must never be treated as the source of truth (§24.7).
#
# The projection deliberately stores only the bounded status fields plus the
# relative storage key of the durable artifact. Free-text governance fields
# (review_context_summary, governance_notes) stay in the durable artifact only
# and are kept out of SQLite, consistent with the §24.12 telemetry/privacy
# posture of not spreading free-text governance content.
#
# It is append-only like event_log / stage_artifact: a run records its
# governance decision once, at ingest.
_MIGRATION_0005 = """
CREATE TABLE trust_envelope (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_run_id     TEXT NOT NULL REFERENCES pipeline_run(pipeline_run_id),
    source_ref          TEXT NOT NULL,
    schema_version      TEXT NOT NULL,
    license_type        TEXT NOT NULL,
    decision            TEXT NOT NULL,
    decision_timestamp  TEXT NOT NULL,
    approver_id         TEXT NOT NULL,
    blocked_reason      TEXT,
    envelope_key        TEXT NOT NULL,          -- relative storage key, not absolute
    recorded_at         TEXT NOT NULL
);

CREATE INDEX idx_trust_envelope_run ON trust_envelope(pipeline_run_id);
"""

# Phase 14C.1 (Local Durable Queue / Worker Shape Proof): work_queue is the
# durable backing table for the local work queue. It records one work item per
# accepted proof-run request, separating request acceptance (which enqueues)
# from execution (which a local worker performs after claiming the item). This
# is a LOCAL durable queue adapter, not a cloud/distributed/broker queue.
#
# It follows the same append-friendly, additive migration discipline as the
# other tables. owner and lease_expires_at are the claim/lease mechanics used to
# prevent double-execution and to recover stale claims after a worker is lost;
# they are adapter-internal and are never exposed through the read model.
# state moves through: queued -> claimed -> running -> completed | failed.
_MIGRATION_0006 = """
CREATE TABLE work_queue (
    work_id          TEXT PRIMARY KEY,
    pipeline_run_id  TEXT NOT NULL,
    scenario         TEXT NOT NULL,
    fixture_id       TEXT NOT NULL,
    state            TEXT NOT NULL,          -- queued|claimed|running|completed|failed
    owner            TEXT,                   -- claim/lease owner; adapter-internal
    lease_expires_at TEXT,                   -- ISO timestamp; adapter-internal
    attempts         INTEGER NOT NULL DEFAULT 0,
    enqueued_at      TEXT NOT NULL,
    updated_at       TEXT NOT NULL,
    failure_reason   TEXT
);

CREATE INDEX idx_work_queue_state ON work_queue(state);
"""

# Phase 14C.5.1 (Durable Recovery Control Plane Boundary): recovery_action is
# the durable, backend-owned recovery-lineage table. It links a recovery action
# back to the ORIGINAL failed execution identity (original_run_id /
# original_work_item_id) and to the NEW recovery execution identity
# (recovery_run_id / recovery_work_item_id), and records why recovery was
# requested, by whom, when, and the bounded recovery-action status. It is the
# SOURCE OF TRUTH for recovery lineage — observer (QueueWorkerEvent) events
# remain explanatory only and must never be the lineage database.
#
# This is a LOCAL durable recovery-lineage/audit table for the local SQLite
# proof. It is NOT a cloud workflow store, NOT a distributed retry engine, NOT a
# dead-letter queue, and NOT a scheduler. decision/rejection_reason hold the
# bounded eligibility outcome for a rejected request so rejected recovery actions
# are durably visible to the operator. attempt_number records the bounded
# recovery attempt. status moves through: requested -> created | rejected |
# failed.
_MIGRATION_0007 = """
CREATE TABLE recovery_action (
    recovery_action_id     TEXT PRIMARY KEY,
    original_run_id        TEXT NOT NULL,
    original_work_item_id  TEXT NOT NULL,
    recovery_run_id        TEXT,
    recovery_work_item_id  TEXT,
    recovery_reason        TEXT NOT NULL,
    requested_by           TEXT NOT NULL,
    requested_at           TEXT NOT NULL,
    status                 TEXT NOT NULL,   -- requested|created|rejected|failed
    decision               TEXT,            -- bounded eligibility decision
    rejection_reason       TEXT,            -- safe reason when rejected
    attempt_number         INTEGER NOT NULL DEFAULT 1,
    updated_at             TEXT NOT NULL
);

CREATE INDEX idx_recovery_action_original_run
    ON recovery_action(original_run_id);
CREATE INDEX idx_recovery_action_original_work
    ON recovery_action(original_work_item_id);
"""

# Ordered list of (version, ddl). Apply every migration whose version is
# greater than the database's current schema version.
MIGRATIONS: tuple[tuple[int, str], ...] = (
    (1, _MIGRATION_0001),
    (2, _MIGRATION_0002),
    (3, _MIGRATION_0003),
    (4, _MIGRATION_0004),
    (5, _MIGRATION_0005),
    (6, _MIGRATION_0006),
    (7, _MIGRATION_0007),
)
