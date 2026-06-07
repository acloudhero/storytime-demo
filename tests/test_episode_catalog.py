"""EpisodeCatalog: the read-only catalog of prior episodes for OI-11.

EmptyEpisodeCatalog is the honest first-publish / unit-test default.
StateEpisodeCatalog (the composition-root adapter) translates persisted
published_episode rows into feed-domain FeedItem values, newest first, with
the stored ISO-8601 publication time rendered as an RFC-822 pubDate.
"""

from __future__ import annotations

from email.utils import parsedate_to_datetime

from storytime.pipeline import StateEpisodeCatalog
from storytime.rss import EmptyEpisodeCatalog
from storytime.state import RunRecord, StateStore

_RUN_ID = "01RUN000000000000000000000"


def test_empty_catalog_has_no_items() -> None:
    assert EmptyEpisodeCatalog().published_feed_items() == ()


def _record(
    store: StateStore,
    *,
    guid: str,
    published_at: str,
    title: str,
    description: str,
    feed_version: int,
) -> None:
    """Persist one published_episode row, creating its parent run on demand."""
    if store.get_run(_RUN_ID) is None:
        store.create_run(
            RunRecord(
                pipeline_run_id=_RUN_ID,
                created_at="2026-01-01T00:00:00+00:00",
                updated_at="2026-01-01T00:00:00+00:00",
                current_stage="publish",
                status="completed",
                source_manifest_hash="c" * 64,
                run_dir=f"runs/{_RUN_ID}",
            )
        )
    with store.transaction():
        store.record_published_episode(
            episode_guid=guid,
            pipeline_run_id=_RUN_ID,
            title=title,
            published_at=published_at,
            audio_path=f"audio/{guid}.mp3",
            audio_bytes=2048,
            duration_seconds=8.0,
            feed_version=feed_version,
            description=description,
        )


def test_state_catalog_is_empty_before_any_publish(state_store: StateStore) -> None:
    assert StateEpisodeCatalog(state_store).published_feed_items() == ()


def test_state_catalog_returns_episodes_newest_first(
    state_store: StateStore,
) -> None:
    _record(
        state_store,
        guid="01EP0000000000000000000OLD",
        published_at="2026-01-01T00:00:00+00:00",
        title="Older Episode",
        description="The older one.",
        feed_version=1,
    )
    _record(
        state_store,
        guid="01EP0000000000000000000NEW",
        published_at="2026-03-01T00:00:00+00:00",
        title="Newer Episode",
        description="The newer one.",
        feed_version=2,
    )

    items = StateEpisodeCatalog(state_store).published_feed_items()
    assert [item.title for item in items] == ["Newer Episode", "Older Episode"]


def test_state_catalog_preserves_description_and_audio(
    state_store: StateStore,
) -> None:
    _record(
        state_store,
        guid="01EP00000000000000000000XX",
        published_at="2026-02-02T12:00:00+00:00",
        title="An Episode",
        description="A persisted description.",
        feed_version=5,
    )
    (item,) = StateEpisodeCatalog(state_store).published_feed_items()
    assert item.guid == "01EP00000000000000000000XX"
    assert item.description == "A persisted description."
    assert item.audio_url == "audio/01EP00000000000000000000XX.mp3"


def test_state_catalog_renders_pubdate_as_rfc822(
    state_store: StateStore,
) -> None:
    """The stored ISO-8601 published_at is converted to a parseable RFC-822 date."""
    _record(
        state_store,
        guid="01EP00000000000000000000DT",
        published_at="2026-04-05T06:07:08+00:00",
        title="Dated Episode",
        description="",
        feed_version=1,
    )
    (item,) = StateEpisodeCatalog(state_store).published_feed_items()
    # parsedate_to_datetime round-trips a valid RFC-822 date back to the
    # original instant; an unparseable string would raise here.
    parsed = parsedate_to_datetime(item.published_at)
    assert parsed.year == 2026
    assert parsed.month == 4
    assert parsed.day == 5
