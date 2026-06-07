"""PublishStage: multi-item RSS feed generation with enclosures to episode audio.

Phase 6 (OI-11): the feed is multi-item. PublishStage asks an injected
EpisodeCatalog for the previously published episodes, prepends the episode it
is publishing now, validates the rendered feed, and replaces feed.xml
atomically. These tests cover the single-item base case and the multi-item
aggregation, GUID de-duplication, and feed-version behaviour.
"""

from __future__ import annotations

import shutil
import xml.etree.ElementTree as ET

import pytest

from storytime.adapters.storage import LocalFilesystemStorage
from storytime.adapters.tts import MockTTS
from storytime.dto import StageInput, StageStatus
from storytime.events import EventType
from storytime.rss import EmptyEpisodeCatalog, EpisodeCatalog, FeedItem
from storytime.runner import RunnerContext
from storytime.stages import (
    AssembleStage,
    IngestStage,
    PublishStage,
    SynthesizeStage,
)
from storytime.stages.encode import FfmpegMp3Encoder

_HAS_FFMPEG = shutil.which("ffmpeg") is not None
RUN_ID = "01TESTPUBLISH00000000000001"


class _FixedCatalog:
    """An EpisodeCatalog returning a fixed, hand-built list of prior episodes."""

    def __init__(self, items: tuple[FeedItem, ...]) -> None:
        self._items = items

    def published_feed_items(self) -> tuple[FeedItem, ...]:
        return self._items


def _prior_item(guid: str, *, title: str = "An Earlier Episode") -> FeedItem:
    """Build a stand-in FeedItem for an already-published episode."""
    return FeedItem(
        guid=guid,
        title=title,
        description=f"{title} description.",
        audio_url=f"audio/{guid}.mp3",
        audio_bytes=4096,
        duration_seconds=12.0,
        published_at="Mon, 01 Jan 2024 00:00:00 -0000",
    )


def _assemble_artifacts(
    ctx: RunnerContext, manifest_path: str
) -> tuple[str, ...]:
    """Run ingest + synthesize + assemble; return the assemble artifacts."""
    ingest = IngestStage().run(
        ctx,
        StageInput(
            pipeline_run_id=RUN_ID,
            stage_name="ingest",
            run_dir=RUN_ID,
            params={"manifest_path": manifest_path},
        ),
    )
    synth = SynthesizeStage(MockTTS()).run(
        ctx,
        StageInput(
            pipeline_run_id=RUN_ID,
            stage_name="synthesize",
            run_dir=RUN_ID,
            input_artifacts=ingest.output_artifacts,
        ),
    )
    assemble = AssembleStage(
        FfmpegMp3Encoder.autodetect(),
        episode_title="The Raven",
        episode_description="A public-domain reading.",
    ).run(
        ctx,
        StageInput(
            pipeline_run_id=RUN_ID,
            stage_name="assemble",
            run_dir=RUN_ID,
            input_artifacts=synth.output_artifacts,
        ),
    )
    assert assemble.status is StageStatus.SUCCEEDED
    return assemble.output_artifacts


def _publish_stage(
    ctx: RunnerContext, *, episode_catalog: EpisodeCatalog | None = None
) -> PublishStage:
    """Build a PublishStage; defaults to an empty (first-publish) catalog."""
    return PublishStage(
        LocalFilesystemStorage(ctx.config.feed_dir),
        channel_title="StoryTime",
        channel_link="http://127.0.0.1:8000/feed.xml",
        channel_description="StoryTime test feed.",
        episode_catalog=episode_catalog or EmptyEpisodeCatalog(),
    )


def _publish_input(artifacts: tuple[str, ...]) -> StageInput:
    return StageInput(
        pipeline_run_id=RUN_ID,
        stage_name="publish",
        run_dir=RUN_ID,
        input_artifacts=artifacts,
    )


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_publish_writes_feed_referencing_audio(
    runtime_context: RunnerContext, slice_workspace
) -> None:
    artifacts = _assemble_artifacts(
        runtime_context, str(slice_workspace.manifest_path)
    )
    result = _publish_stage(runtime_context).run(
        runtime_context, _publish_input(artifacts)
    )

    assert result.status is StageStatus.SUCCEEDED

    feed_dir = runtime_context.config.feed_dir
    feed_xml = feed_dir / "feed.xml"
    assert feed_xml.is_file()

    # The feed is well-formed and its enclosure points at the episode audio.
    root = ET.fromstring(feed_xml.read_text(encoding="utf-8"))
    enclosure = root.find(".//enclosure")
    assert enclosure is not None
    audio_url = enclosure.get("url") or ""
    assert audio_url.startswith("audio/")
    assert audio_url.endswith(".mp3")
    assert enclosure.get("type") == "audio/mpeg"

    # The referenced audio file was actually copied into the feed directory.
    assert (feed_dir / audio_url).is_file()

    event_types = {event.event_type for event in result.events}
    assert {EventType.RSS_PUBLISHED, EventType.RUN_COMPLETED} <= event_types

    published = result.state_update.published_episode
    assert published is not None
    assert published.audio_path == audio_url
    # First publish: an empty catalog -> exactly one item, feed version 1.
    assert published.feed_version == 1
    assert len(root.findall(".//item")) == 1
    assert result.state_update.run_status == "completed"


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_publish_aggregates_prior_episodes_into_multi_item_feed(
    runtime_context: RunnerContext, slice_workspace
) -> None:
    """OI-11: prior episodes from the catalog appear alongside the new one."""
    artifacts = _assemble_artifacts(
        runtime_context, str(slice_workspace.manifest_path)
    )
    prior = (_prior_item("01PRIOREP000000000000000AA"),
             _prior_item("01PRIOREP000000000000000BB"))
    result = _publish_stage(
        runtime_context, episode_catalog=_FixedCatalog(prior)
    ).run(runtime_context, _publish_input(artifacts))

    assert result.status is StageStatus.SUCCEEDED

    root = ET.fromstring(
        (runtime_context.config.feed_dir / "feed.xml").read_text(encoding="utf-8")
    )
    items = root.findall(".//item")
    # Two prior episodes + the one just published.
    assert len(items) == 3

    guids = {(item.find("guid").text if item.find("guid") is not None else "")
             for item in items}
    assert "01PRIOREP000000000000000AA" in guids
    assert "01PRIOREP000000000000000BB" in guids

    # The newly published episode is first (the feed stays newest-first).
    first_guid = items[0].find("guid")
    assert first_guid is not None
    assert first_guid.text not in {
        "01PRIOREP000000000000000AA", "01PRIOREP000000000000000BB"
    }

    # feed_version is len(prior) + 1.
    published = result.state_update.published_episode
    assert published is not None
    assert published.feed_version == 3


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_publish_deduplicates_a_republished_episode_by_guid(
    runtime_context: RunnerContext, slice_workspace
) -> None:
    """A catalog entry sharing the new episode's GUID is not duplicated."""
    artifacts = _assemble_artifacts(
        runtime_context, str(slice_workspace.manifest_path)
    )
    # First publish with an empty catalog to learn the episode's GUID.
    first = _publish_stage(runtime_context).run(
        runtime_context, _publish_input(artifacts)
    )
    assert first.state_update.published_episode is not None
    guid = first.state_update.published_episode.episode_guid

    # Re-publish with a catalog that already contains that exact GUID.
    result = _publish_stage(
        runtime_context,
        episode_catalog=_FixedCatalog((_prior_item(guid, title="Stale Copy"),)),
    ).run(runtime_context, _publish_input(artifacts))

    assert result.status is StageStatus.SUCCEEDED
    root = ET.fromstring(
        (runtime_context.config.feed_dir / "feed.xml").read_text(encoding="utf-8")
    )
    # The shared GUID appears once, not twice; feed_version stays 1.
    assert len(root.findall(".//item")) == 1
    published = result.state_update.published_episode
    assert published is not None
    assert published.feed_version == 1


def test_publish_without_required_artifacts_fails(
    runtime_context: RunnerContext,
) -> None:
    result = _publish_stage(runtime_context).run(
        runtime_context,
        StageInput(
            pipeline_run_id=RUN_ID,
            stage_name="publish",
            run_dir=RUN_ID,
            input_artifacts=(),
        ),
    )
    assert result.status is StageStatus.FAILED
    assert result.error_kind == "MissingInputArtifact"
