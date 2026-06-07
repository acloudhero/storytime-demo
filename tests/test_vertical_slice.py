"""End-to-end vertical slice: one approved text -> audio -> RSS -> journey."""

from __future__ import annotations

import shutil
import wave
import xml.etree.ElementTree as ET

import pytest

from storytime.artifacts import from_json
from storytime.pipeline import run_vertical_slice
from storytime.runner import RunnerContext
from storytime.stages.encode import FfmpegMp3Encoder

_HAS_FFMPEG = shutil.which("ffmpeg") is not None

_EXPECTED_EVENTS = (
    "RunCreated",
    "TextIngested",
    "SourceManifestApproved",
    "GovernanceEvaluated",
    "SynthesisStarted",
    "SynthesisCompleted",
    "AssemblyCompleted",
    "RSSPublished",
    "RunCompleted",
)


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_valid_manifest_runs_the_full_slice(
    runtime_context: RunnerContext, slice_workspace
) -> None:
    outcome = run_vertical_slice(
        runtime_context, slice_workspace.manifest_path
    )

    # 1. The slice completed and produced a run id.
    assert outcome.status == "completed"
    run_id = outcome.pipeline_run_id
    assert run_id is not None

    state = runtime_context.state

    # 5. Run state is persisted.
    run = state.get_run(run_id)
    assert run is not None
    assert run.status == "completed"
    assert run.current_stage == "publish"

    # 6. event_log rows are persisted, in order.
    assert state.count_events(run_id) == len(_EXPECTED_EVENTS)
    assert state.event_types(run_id) == _EXPECTED_EVENTS

    # Stage executions: four stages, every one succeeded.
    executions = state.list_stage_executions(run_id)
    assert [e.stage_name for e in executions] == [
        "ingest",
        "synthesize",
        "assemble",
        "publish",
    ]
    assert all(e.status == "succeeded" for e in executions)

    # The manifest approval block was recorded as an approval row.
    assert state.count_approvals(run_id) == 1

    # 7. Every artifact envelope is written and validates under from_json.
    envelope_keys = (
        f"{run_id}/artifacts/ingest/text.plain.json",
        f"{run_id}/artifacts/synthesize/audio.wav.json",
        f"{run_id}/artifacts/assemble/episode.mp3.json",
        f"{run_id}/artifacts/assemble/episode.metadata.envelope.json",
    )
    envelopes = [
        from_json(runtime_context.storage.read_text(key))
        for key in envelope_keys
    ]
    for envelope in envelopes:
        assert envelope.artifact_version == 1
        assert len(envelope.payload_sha256) == 64

    # 8. The synthesized WAV payload is a real, readable WAV file.
    wav_envelope = envelopes[1]
    wav_path = runtime_context.storage.resolve(wav_envelope.payload_path)
    with wave.open(str(wav_path), "rb") as handle:
        assert handle.getnframes() > 0

    # 9. The RSS feed exists and references the published audio artifact.
    feed_xml = runtime_context.config.feed_dir / "feed.xml"
    assert feed_xml.is_file()
    root = ET.fromstring(feed_xml.read_text(encoding="utf-8"))
    enclosure = root.find(".//enclosure")
    assert enclosure is not None
    audio_url = enclosure.get("url") or ""
    assert (runtime_context.config.feed_dir / audio_url).is_file()

    # The published episode is persisted.
    assert outcome.episode_guid is not None
    episode = state.get_published_episode(outcome.episode_guid)
    assert episode is not None

    # 10. pipeline_run_id correlates run state, artifacts, events, episode.
    assert run.pipeline_run_id == run_id
    assert all(env.pipeline_run_id == run_id for env in envelopes)
    assert all(e.pipeline_run_id == run_id for e in executions)
    assert episode.pipeline_run_id == run_id


def _set_field(field: str, value: object):
    """Return a manifest-mutator that overwrites a single field."""

    def _mutate(manifest: dict[str, object]) -> None:
        manifest[field] = value

    return _mutate


def test_invalid_manifest_is_rejected(
    runtime_context: RunnerContext, make_workspace
) -> None:
    # source_id violates the closed-schema pattern.
    workspace = make_workspace(
        mutate=_set_field("source_id", "Invalid Source!")
    )
    outcome = run_vertical_slice(runtime_context, workspace.manifest_path)

    assert outcome.status == "rejected"
    assert outcome.pipeline_run_id is None
    assert outcome.messages


def test_unsupported_license_is_rejected(
    runtime_context: RunnerContext, make_workspace
) -> None:
    workspace = make_workspace(mutate=_set_field("license", "MIT"))
    outcome = run_vertical_slice(runtime_context, workspace.manifest_path)

    assert outcome.status == "rejected"
    assert outcome.pipeline_run_id is None


def test_text_hash_mismatch_fails_the_run(
    runtime_context: RunnerContext, make_workspace
) -> None:
    # Schema-valid manifest, but its declared digest does not match the text.
    workspace = make_workspace(text_sha256="f" * 64)
    outcome = run_vertical_slice(runtime_context, workspace.manifest_path)

    assert outcome.status == "failed"
    assert outcome.failed_stage == "ingest"
    assert outcome.error_kind == "TextHashMismatch"

    run = runtime_context.state.get_run(outcome.pipeline_run_id or "")
    assert run is not None
    assert run.status == "failed"


def test_ffmpeg_absent_fails_the_slice_clearly(
    runtime_context: RunnerContext, slice_workspace
) -> None:
    # Inject an encoder with no ffmpeg: the slice must fail-fast, not degrade.
    outcome = run_vertical_slice(
        runtime_context,
        slice_workspace.manifest_path,
        encoder=FfmpegMp3Encoder(None),
    )

    assert outcome.status == "failed"
    assert outcome.failed_stage == "assemble"
    assert outcome.error_kind == "FfmpegUnavailable"

    run = runtime_context.state.get_run(outcome.pipeline_run_id or "")
    assert run is not None
    assert run.status == "failed"
    # No RSS feed is silently produced when assembly fails.
    assert not (runtime_context.config.feed_dir / "feed.xml").exists()
