"""Internal pipeline event model.

ARCH-LOCK: Internal Event Model (data only)
DO NOT REFACTOR: Events are immutable data. Do not attach behaviour, do not
introduce an event bus, and do not let events import other storytime modules.
Rationale: Hard decision 9 of the Architecture Baseline. Stages return events
inside StageResult; the runner persists them to the SQLite event_log BEFORE
emitting telemetry. Telemetry is a view over this data, never its source.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class EventType(StrEnum):
    """The closed set of internal event types for the Phase 1/2 pipeline."""

    RUN_CREATED = "RunCreated"
    TEXT_INGESTED = "TextIngested"
    # SourceManifestApproved records the rights-clearance approval embedded in
    # the *source manifest* (recorded automatically during ingest). It is
    # deliberately distinct from TextApproved, which records an *operator*
    # decision at the interactive text approval gate. Before Phase 4.1 ingest
    # emitted TextApproved too, making a gated run's event_log carry two
    # TextApproved events with different meanings (Phase 4 accepted ruling 3).
    SOURCE_MANIFEST_APPROVED = "SourceManifestApproved"
    # GovernanceEvaluated records the Phase 9B fail-closed governance gate
    # decision for a source (Architecture Baseline §24.6/§24.12). Emitted by
    # ingest when it derives the run's Trust Envelope. Its payload carries only
    # bounded status metadata — the decision, the licence type, the source ref
    # — never raw source text, notes, or the review_context_summary (§24.12).
    GOVERNANCE_EVALUATED = "GovernanceEvaluated"
    TEXT_APPROVAL_REQUESTED = "TextApprovalRequested"
    TEXT_APPROVED = "TextApproved"
    TEXT_REJECTED = "TextRejected"
    SYNTHESIS_STARTED = "SynthesisStarted"
    SYNTHESIS_COMPLETED = "SynthesisCompleted"
    SYNTHESIS_FAILED = "SynthesisFailed"
    AUDIO_APPROVAL_REQUESTED = "AudioApprovalRequested"
    AUDIO_APPROVED = "AudioApproved"
    AUDIO_REJECTED = "AudioRejected"
    ASSEMBLY_COMPLETED = "AssemblyCompleted"
    RSS_PUBLISHED = "RSSPublished"
    RSS_PUBLISH_FAILED = "RSSPublishFailed"
    RUN_COMPLETED = "RunCompleted"
    RUN_FAILED = "RunFailed"
    RUNS_CLEANED = "RunsCleaned"
    # Phase 10D: the audit record for a governed operator re-run. Written to
    # the append-only event_log when `storytime rerun` resets a failed run to
    # the resumable state. Carries only bounded status metadata — no raw text.
    RUN_RERUN_REQUESTED = "RunRerunRequested"


@dataclass(frozen=True, slots=True)
class PipelineEvent:
    """A single immutable pipeline event.

    payload must be JSON-serializable and small: paths, hashes, counts,
    durations. Large blobs (audio bytes, full texts) must never appear here.
    """

    event_type: EventType
    pipeline_run_id: str
    occurred_at: datetime
    stage_name: str
    payload: Mapping[str, object]

    def payload_json(self) -> str:
        """Return the payload as a compact, sorted JSON string for storage.

        Raises TypeError if the payload is not JSON-serializable, which keeps
        the "small, serializable payload" rule enforced at write time.
        """
        return json.dumps(dict(self.payload), sort_keys=True, separators=(",", ":"))
