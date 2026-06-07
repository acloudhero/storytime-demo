"""Read-only catalog of previously published episodes.

ARCH-LOCK: Stage stays off the database
DO NOT REFACTOR: the publish stage MUST obtain prior episodes through this
injected, read-only Protocol — never by importing storytime.state or running
SQL itself. This mirrors how the feed-rooted StorageAdapter is injected
(Round 5 clarification A1: stage-specific dependencies are constructor-injected
into the stage, not reached for directly).
Rationale: Architecture Baseline sections 8-9 and the publish-stage boundary —
PublishStage takes a RunnerContext + StageInput and declarative dependencies;
keeping it decoupled from the state schema is what keeps it unit-testable and
keeps the future cloud migration mechanical.

The catalog deals only in the feed-domain value type FeedItem, so this module
imports nothing but the builder. The concrete state-backed implementation lives
in the composition root (storytime.pipeline), which is allowed to know both the
state store and the feed domain.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from storytime.rss.builder import FeedItem


@runtime_checkable
class EpisodeCatalog(Protocol):
    """Supplies the already-published episodes for multi-item feed builds."""

    def published_feed_items(self) -> tuple[FeedItem, ...]:
        """Return every previously published episode as a FeedItem.

        Newest publication first. The publish stage prepends the episode it is
        currently publishing, so the rendered feed stays newest-first overall.
        An implementation MUST NOT include an episode the current run is about
        to publish; the publish stage additionally de-duplicates by GUID as a
        defensive measure.
        """
        ...


class EmptyEpisodeCatalog:
    """An EpisodeCatalog with no prior episodes.

    The honest default for a unit test, or the very first publish of a feed.
    """

    def published_feed_items(self) -> tuple[FeedItem, ...]:
        return ()


__all__ = ["EmptyEpisodeCatalog", "EpisodeCatalog"]
