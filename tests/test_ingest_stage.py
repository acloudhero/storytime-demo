"""IngestStage: manifest-driven ingest and text-hash verification."""

from __future__ import annotations

from storytime.artifacts import PayloadKind, from_json
from storytime.dto import StageInput, StageStatus
from storytime.events import EventType
from storytime.runner import RunnerContext
from storytime.stages import IngestStage

RUN_ID = "01TESTINGEST00000000000001"


def _stage_input(manifest_path: str) -> StageInput:
    return StageInput(
        pipeline_run_id=RUN_ID,
        stage_name="ingest",
        run_dir=RUN_ID,
        params={"manifest_path": manifest_path},
    )


def test_ingest_success_writes_validated_text_artifact(
    runtime_context: RunnerContext, slice_workspace
) -> None:
    result = IngestStage().run(
        runtime_context, _stage_input(str(slice_workspace.manifest_path))
    )

    assert result.status is StageStatus.SUCCEEDED
    assert len(result.output_artifacts) == 1

    # The artifact envelope is written AND parses under the versioned reader.
    envelope = from_json(
        runtime_context.storage.read_text(result.output_artifacts[0])
    )
    assert envelope.artifact_version == 1
    assert envelope.payload_kind is PayloadKind.TEXT_PLAIN
    assert envelope.pipeline_run_id == RUN_ID
    assert envelope.stage == "ingest"
    assert envelope.payload_sha256 == slice_workspace.text_sha256
    assert envelope.payload_bytes > 0

    event_types = {event.event_type for event in result.events}
    assert EventType.TEXT_INGESTED in event_types
    # Ingest records the manifest's rights-clearance approval as
    # SourceManifestApproved — never TextApproved, which is reserved for the
    # operator decision at the interactive text approval gate.
    assert EventType.SOURCE_MANIFEST_APPROVED in event_types
    assert EventType.TEXT_APPROVED not in event_types

    # The manifest's approval block is recorded as a provenance approval intent.
    approval = result.state_update.approval
    assert approval is not None
    assert approval.decision == "approved"
    assert approval.operator == "operator"


def test_ingest_rejects_text_hash_mismatch(
    runtime_context: RunnerContext, make_workspace
) -> None:
    # The manifest declares a digest that does not match the real text.
    workspace = make_workspace(text_sha256="f" * 64)
    result = IngestStage().run(
        runtime_context, _stage_input(str(workspace.manifest_path))
    )

    assert result.status is StageStatus.FAILED
    assert result.error_kind == "TextHashMismatch"
    assert result.state_update.run_status == "failed"
    assert any(e.event_type is EventType.RUN_FAILED for e in result.events)


def test_ingest_rejects_missing_source_text(
    runtime_context: RunnerContext, make_workspace
) -> None:
    workspace = make_workspace(text_path="not-the-real-file.txt")
    result = IngestStage().run(
        runtime_context, _stage_input(str(workspace.manifest_path))
    )

    assert result.status is StageStatus.FAILED
    assert result.error_kind == "SourceTextMissing"


def test_ingest_requires_manifest_path_param(
    runtime_context: RunnerContext,
) -> None:
    bare_input = StageInput(
        pipeline_run_id=RUN_ID, stage_name="ingest", run_dir=RUN_ID
    )
    result = IngestStage().run(runtime_context, bare_input)

    assert result.status is StageStatus.FAILED
    assert result.error_kind == "MissingManifestPath"
