"""Ingest stage — manifest-driven ingest of a local approved text file.

ARCH-LOCK: Stage Boundary (see storytime.stages.base)
DO NOT REFACTOR: IngestStage takes a RunnerContext + StageInput and returns a
StageResult. It does not write to SQLite directly, does not call other stages,
and does not import OpenTelemetry. The text-hash check is load-bearing: it is
how StoryTime refuses to ingest text that does not match its approved,
manifest-declared digest.
Rationale: Architecture Baseline sections 8-9 and hard decision 10.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from storytime.adapters.telemetry.attributes import (
    ATTR_ARTIFACT_HASH_PRESENT,
    ATTR_ARTIFACT_KIND,
    ATTR_ARTIFACT_VERSION,
)
from storytime.artifacts import (
    ARTIFACT_VERSION,
    ArtifactEnvelope,
    PayloadKind,
    TraceContext,
    to_json,
)
from storytime.dto import ApprovalIntent, StageInput, StageResult, StateUpdate, TrustEnvelopeIntent
from storytime.events import EventType, PipelineEvent
from storytime.governance import (
    BlockedSourceConfigError,
    evaluate_envelope,
    load_blocked_sources,
    trust_envelope_from_manifest,
    write_trust_envelope,
)
from storytime.manifest import ManifestValidationError, load_manifest
from storytime.util.hashing import sha256_text

if TYPE_CHECKING:
    from storytime.runner.context import RunnerContext


class IngestStage:
    """Validates the source text against its manifest and emits a text artifact.

    The manifest carries a rights-clearance approval block, so a successful
    ingest also records that *manifest provenance* approval — an approval row
    with stage_name "ingest" and a SourceManifestApproved event (hard decision
    6: approval is a persisted pipeline step). This is distinct from the
    operator decision at the interactive text approval gate, which is recorded
    under stage_name "approve_text" with a TextApproved/TextRejected event.
    """

    name = "ingest"

    def run(self, ctx: RunnerContext, stage_input: StageInput) -> StageResult:
        """Run ingest. The manifest path is supplied via StageInput.params."""
        run_id = stage_input.pipeline_run_id
        now = ctx.clock.now()

        manifest_path_raw = stage_input.params.get("manifest_path")
        if not isinstance(manifest_path_raw, str):
            return self._fail(
                run_id,
                now,
                "MissingManifestPath",
                "ingest requires a 'manifest_path' string in StageInput.params",
            )
        manifest_path = Path(manifest_path_raw)

        try:
            manifest = load_manifest(manifest_path)
        except ManifestValidationError as exc:
            return self._fail(
                run_id, now, "ManifestInvalid", "; ".join(exc.messages)
            )

        text_file = (manifest_path.parent / manifest.text_path).resolve()
        if not text_file.is_file():
            return self._fail(
                run_id,
                now,
                "SourceTextMissing",
                f"manifest text_path does not resolve to a file: {text_file}",
            )

        text = text_file.read_text(encoding=manifest.text_encoding)
        actual_sha256 = sha256_text(text, encoding=manifest.text_encoding)
        if actual_sha256 != manifest.text_sha256:
            return self._fail(
                run_id,
                now,
                "TextHashMismatch",
                (
                    f"source text digest {actual_sha256} does not match the "
                    f"manifest text_sha256 {manifest.text_sha256}; ingest refuses "
                    "to proceed with unverified text"
                ),
            )

        text_bytes = len(text.encode(manifest.text_encoding))
        text_key = f"{stage_input.run_dir}/artifacts/ingest/text.txt"
        ctx.storage.write_text(text_key, text)

        envelope_key = f"{stage_input.run_dir}/artifacts/ingest/text.plain.json"
        envelope = ArtifactEnvelope(
            artifact_version=ARTIFACT_VERSION,
            pipeline_run_id=run_id,
            stage=self.name,
            produced_at=now.isoformat(),
            payload_kind=PayloadKind.TEXT_PLAIN,
            payload_path=text_key,
            payload_sha256=actual_sha256,
            payload_bytes=text_bytes,
            trace_context=TraceContext(traceparent=stage_input.inbound_traceparent),
            producer={
                "source_id": manifest.source_id,
                "license": manifest.license,
                "title": manifest.title,
                "author": manifest.author,
            },
        )
        ctx.storage.write_text(envelope_key, to_json(envelope))

        # Phase 9B (Architecture Baseline §24.6/§24.7/§24.8): derive the
        # governance Trust Envelope from the manifest the operator wrote, and
        # apply the operator's local blocked-source list. This transcribes a
        # *human* licensing decision (the manifest's licence field and approval
        # block) into the durable Trust Envelope artifact — it is not legal
        # automation or model inference (§24.2/§24.3). The durable artifact is
        # the governance source of truth; a SQLite projection is recorded via
        # the StateUpdate intent the runner applies.
        try:
            blocked_sources = load_blocked_sources(
                ctx.config.governance_blocked_sources_path
            )
        except BlockedSourceConfigError as exc:
            # A malformed blocked-source config is unverifiable governance
            # input: fail closed rather than ignore a broken deny-list.
            return self._fail(
                run_id, now, "BlockedSourceConfigInvalid", str(exc)
            )

        trust_envelope = trust_envelope_from_manifest(
            manifest,
            blocked_sources=blocked_sources,
            artifact_hash_refs=(actual_sha256,),
        )
        trust_envelope_storage_key = write_trust_envelope(
            ctx.storage, stage_input.run_dir, trust_envelope
        )
        trust_envelope_intent = TrustEnvelopeIntent(
            source_ref=trust_envelope.source_ref,
            schema_version=trust_envelope.schema_version,
            license_type=str(trust_envelope.license_type),
            decision=str(trust_envelope.decision),
            decision_timestamp=trust_envelope.decision_timestamp,
            approver_id=trust_envelope.approver_id,
            envelope_key=trust_envelope_storage_key,
            blocked_reason=trust_envelope.blocked_reason,
        )
        # GovernanceEvaluated carries only bounded status metadata (§24.12) —
        # no raw text, notes, or review summary.
        governance_event = PipelineEvent(
            event_type=EventType.GOVERNANCE_EVALUATED,
            pipeline_run_id=run_id,
            occurred_at=now,
            stage_name=self.name,
            payload={
                "source_ref": trust_envelope.source_ref,
                "decision": str(trust_envelope.decision),
                "license_type": str(trust_envelope.license_type),
            },
        )
        gate = evaluate_envelope(trust_envelope)
        if not gate.passed:
            # §24.6 fail-closed gate, checked early: a source without an
            # APPROVED Trust Envelope never proceeds. The Trust Envelope
            # projection is still recorded (the FAILED StateUpdate carries the
            # intent) so the blocking decision is durably on the audit record.
            failed_event = PipelineEvent(
                event_type=EventType.RUN_FAILED,
                pipeline_run_id=run_id,
                occurred_at=now,
                stage_name=self.name,
                payload={"error_kind": "SourceNotApproved", "stage": self.name},
            )
            return StageResult.failed(
                "SourceNotApproved",
                gate.reason,
                events=(governance_event, failed_event),
                state_update=StateUpdate(
                    run_status="failed",
                    current_stage=self.name,
                    trust_envelope=trust_envelope_intent,
                ),
            )

        events = (
            PipelineEvent(
                event_type=EventType.TEXT_INGESTED,
                pipeline_run_id=run_id,
                occurred_at=now,
                stage_name=self.name,
                payload={
                    "source_id": manifest.source_id,
                    "text_sha256": actual_sha256,
                    "text_bytes": text_bytes,
                    "license": manifest.license,
                },
            ),
            PipelineEvent(
                event_type=EventType.SOURCE_MANIFEST_APPROVED,
                pipeline_run_id=run_id,
                occurred_at=now,
                stage_name=self.name,
                payload={
                    "approved_by": manifest.approval.approved_by,
                    "approved_at": manifest.approval.approved_at,
                },
            ),
            governance_event,
        )
        state_update = StateUpdate(
            run_status="running",
            current_stage=self.name,
            approval=ApprovalIntent(
                stage_name=self.name,
                decision="approved",
                operator=manifest.approval.approved_by,
                notes=manifest.approval.review_notes,
            ),
            trust_envelope=trust_envelope_intent,
        )
        return StageResult.succeeded(
            state_update,
            events=events,
            output_artifacts=(envelope_key,),
            span_attributes={
                ATTR_ARTIFACT_KIND: str(PayloadKind.TEXT_PLAIN),
                ATTR_ARTIFACT_VERSION: str(ARTIFACT_VERSION),
                ATTR_ARTIFACT_HASH_PRESENT: "true",
            },
        )

    def _fail(
        self, run_id: str, occurred_at: datetime, kind: str, message: str
    ) -> StageResult:
        """Build a FAILED result with a RUN_FAILED forensic event."""
        event = PipelineEvent(
            event_type=EventType.RUN_FAILED,
            pipeline_run_id=run_id,
            occurred_at=occurred_at,
            stage_name=self.name,
            payload={"error_kind": kind, "stage": self.name},
        )
        return StageResult.failed(
            kind,
            message,
            events=(event,),
            state_update=StateUpdate(run_status="failed", current_stage=self.name),
        )
