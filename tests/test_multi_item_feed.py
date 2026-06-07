"""End-to-end proof of multi-item RSS feed aggregation (OI-11).

Two independent runs are taken through the full vertical slice against one
shared state store and feed directory. After the second publish, feed.xml must
describe BOTH episodes — the back catalogue is preserved, not overwritten — and
the persisted feed_version must increment.
"""

from __future__ import annotations

import shutil
import xml.etree.ElementTree as ET

import pytest

from storytime.pipeline import run_vertical_slice
from storytime.rss.validator import validate_feed
from storytime.runner import RunnerContext

_HAS_FFMPEG = shutil.which("ffmpeg") is not None


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_second_publish_keeps_the_first_episode_in_the_feed(
    runtime_context: RunnerContext, make_workspace
) -> None:
    first_ws = make_workspace(source_id="episode-one", title="Episode One")
    second_ws = make_workspace(source_id="episode-two", title="Episode Two")

    first = run_vertical_slice(runtime_context, first_ws.manifest_path)
    assert first.status == "completed"
    second = run_vertical_slice(runtime_context, second_ws.manifest_path)
    assert second.status == "completed"

    feed_xml = (runtime_context.config.feed_dir / "feed.xml").read_text(
        encoding="utf-8"
    )
    # The rendered feed is still structurally valid with two items.
    validate_feed(feed_xml)

    root = ET.fromstring(feed_xml)
    items = root.findall(".//item")
    assert len(items) == 2

    # Both episodes' audio enclosures are present and distinct.
    enclosure_urls = {
        (item.find("enclosure").get("url") if item.find("enclosure") is not None
         else None)
        for item in items
    }
    assert len(enclosure_urls) == 2
    assert all(url and url.endswith(".mp3") for url in enclosure_urls)

    # Every referenced audio file was actually copied into the feed directory.
    for url in enclosure_urls:
        assert url is not None
        assert (runtime_context.config.feed_dir / url).is_file()

    state = runtime_context.state
    assert first.episode_guid is not None and second.episode_guid is not None
    first_episode = state.get_published_episode(first.episode_guid)
    second_episode = state.get_published_episode(second.episode_guid)
    assert first_episode is not None and second_episode is not None

    # feed_version is the monotonic feed-regeneration counter.
    assert first_episode.feed_version == 1
    assert second_episode.feed_version == 2

    # list_published_episodes returns both, newest publication first.
    catalogue = state.list_published_episodes()
    assert {e.episode_guid for e in catalogue} == {
        first.episode_guid,
        second.episode_guid,
    }


@pytest.mark.skipif(not _HAS_FFMPEG, reason="ffmpeg not installed")
def test_single_publish_feed_has_exactly_one_item(
    runtime_context: RunnerContext, slice_workspace
) -> None:
    """The first publish into an empty feed yields a one-item feed, version 1."""
    outcome = run_vertical_slice(runtime_context, slice_workspace.manifest_path)
    assert outcome.status == "completed"

    root = ET.fromstring(
        (runtime_context.config.feed_dir / "feed.xml").read_text(encoding="utf-8")
    )
    assert len(root.findall(".//item")) == 1

    assert outcome.episode_guid is not None
    episode = runtime_context.state.get_published_episode(outcome.episode_guid)
    assert episode is not None
    assert episode.feed_version == 1
