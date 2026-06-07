"""Publish stage — copies the episode audio into the feed and writes feed.xml.

ARCH-LOCK: Stage Boundary
DO NOT REFACTOR: PublishStage takes a RunnerContext + StageInput and returns a
StageResult. The feed-directory StorageAdapter and the EpisodeCatalog are
constructor-injected (Round 5 clarification A1); the stage does not hard-code
feed paths, does not import storytime.state, and does not write to SQLite
directly. The published episode is recorded declaratively via
StateUpdate.published_episode.
Rationale: Architecture Baseline sections 8-9, 19.

Phase 6 (OI-11): the feed is multi-item. The stage asks the injected
EpisodeCatalog for every previously published episode, prepends the episode it
is publishing now, and renders one feed with all of them — so a subscriber's
client sees the full back catalogue, not just the latest episode. The rendered
feed is validated and then swapped into place atomically (Architecture Baseline
section 14): a crash mid-publish can never leave a partial or malformed
feed.xml where a good one was.
"""

from __future__ import annotations

import json
from email.utils import format_datetime
from typing import TYPE_CHECKING

from storytime.adapters.storage import StorageAdapter
from storytime.adapters.telemetry.attributes import ATTR_RSS_ITEM_COUNT
from storytime.artifacts import ArtifactEnvelopeError, from_json
from storytime.dto import PublishedEpisodeIntent, StageInput, StageResult, StateUpdate
from storytime.events import EventType, PipelineEvent
from storytime.governance import require_approved_envelope
from storytime.rss import EpisodeCatalog, FeedChannel, FeedItem, build_feed
from storytime.rss.validator import FeedValidationError, validate_feed

if TYPE_CHECKING:
    from datetime import datetime

    from storytime.runner.context import RunnerContext

# The relative storage key of the feed document inside the feed root.
_FEED_KEY = "feed.xml"


class PublishStage:
    """Publishes one episode: copies audio into the feed and writes feed.xml."""

    name = "publish"

    def __init__(
        self,
        feed_storage: StorageAdapter,
        *,
        channel_title: str,
        channel_link: str,
        channel_description: str,
        episode_catalog: EpisodeCatalog,
    ) -> None:
        # ARCH-LOCK A1: the feed-rooted storage adapter and the read-only
        # episode catalog are both injected — the stage reaches for neither
        # a hard-coded path nor the state store.
        self._feed_storage = feed_storage
        self._channel_title = channel_title
        self._channel_link = channel_link
        self._channel_description = channel_description
        self._episode_catalog = episode_catalog

    def run(self, ctx: RunnerContext, stage_input: StageInput) -> StageResult:
        """Read MP3 + metadata artifacts, publish audio, write the RSS feed."""
        run_id = stage_input.pipeline_run_id
        now = ctx.clock.now()

        if len(stage_input.input_artifacts) < 2:
            return self._fail(
                run_id, now, "MissingInputArtifact",
                "publish requires the MP3 and episode.metadata artifacts",
            )

        try:
            mp3_envelope = from_json(
                ctx.storage.read_text(stage_input.input_artifacts[0])
            )
            metadata_envelope = from_json(
                ctx.storage.read_text(stage_input.input_artifacts[1])
            )
        except (ArtifactEnvelopeError, FileNotFoundError, OSError) as exc:
            return self._fail(
                run_id, now, "ArtifactUnreadable",
                f"cannot read upstream artifacts: {exc}",
            )

        # Phase 9B (Architecture Baseline §24.6): the fail-closed governance
        # gate, hard-blocking BEFORE RSS publishing — before any feed audio is
        # copied or feed.xml is written. Even though a run can only reach
        # publish after synthesis (which is itself gated), publish re-verifies
        # independently: the durable Trust Envelope is the governance source of
        # truth, and a run granularly resumed to publish — or whose envelope
        # was changed after synthesis — must still fail closed here. An earlier
        # APPROVED check never licenses skipping this one.
        gate = require_approved_envelope(ctx.storage, stage_input.run_dir)
        if not gate.passed:
            return self._fail(
                run_id, now, "GovernanceGateBlocked",
                f"governance gate blocked publishing before RSS: {gate.reason}",
            )

        metadata = json.loads(ctx.storage.read_text(metadata_envelope.payload_path))
        episode_guid = str(metadata["episode_guid"])
        title = str(metadata["title"])
        description = str(metadata["description"])
        duration_seconds = float(metadata["duration_seconds"])

        # Copy the MP3 payload into the feed via the injected feed storage.
        mp3_bytes = ctx.storage.read_bytes(mp3_envelope.payload_path)
        feed_audio_key = f"audio/{episode_guid}.mp3"
        self._feed_storage.write_bytes(feed_audio_key, mp3_bytes)

        current_item = FeedItem(
            guid=episode_guid,
            title=title,
            description=description,
            audio_url=feed_audio_key,
            audio_bytes=len(mp3_bytes),
            duration_seconds=duration_seconds,
            published_at=format_datetime(now),
        )

        # Phase 6 (OI-11): multi-item feed. The injected catalog supplies every
        # previously published episode; the episode being published now is
        # prepended so the feed stays newest-first. The current GUID is
        # filtered out of the prior set defensively — a re-publish must update
        # one item, never duplicate it.
        prior_items = tuple(
            item
            for item in self._episode_catalog.published_feed_items()
            if item.guid != episode_guid
        )
        feed_version = len(prior_items) + 1
        channel = FeedChannel(
            title=self._channel_title,
            link=self._channel_link,
            description=self._channel_description,
            items=(current_item, *prior_items),
        )

        # ARCH-LOCK (Architecture Baseline section 14): build, then VALIDATE,
        # then replace atomically. A feed that fails validation aborts the
        # publish — a partial or malformed feed.xml must never replace a good
        # one. validate_feed raising is caught and turned into a clean stage
        # failure rather than a half-written feed directory.
        feed_xml = build_feed(channel)
        try:
            validate_feed(feed_xml)
        except FeedValidationError as exc:
            return self._fail(
                run_id, now, "FeedValidationFailed",
                f"rendered feed failed structural validation: {exc}",
            )
        self._feed_storage.write_text_atomic(_FEED_KEY, feed_xml)

        events = (
            PipelineEvent(
                event_type=EventType.RSS_PUBLISHED,
                pipeline_run_id=run_id,
                occurred_at=now,
                stage_name=self.name,
                payload={
                    "episode_guid": episode_guid,
                    "audio_path": feed_audio_key,
                    "audio_bytes": len(mp3_bytes),
                    "feed_path": _FEED_KEY,
                    "feed_item_count": len(channel.items),
                    "feed_version": feed_version,
                },
            ),
            PipelineEvent(
                event_type=EventType.RUN_COMPLETED,
                pipeline_run_id=run_id,
                occurred_at=now,
                stage_name=self.name,
                payload={"episode_guid": episode_guid},
            ),
        )
        state_update = StateUpdate(
            run_status="completed",
            current_stage=self.name,
            published_episode=PublishedEpisodeIntent(
                episode_guid=episode_guid,
                title=title,
                audio_path=feed_audio_key,
                audio_bytes=len(mp3_bytes),
                duration_seconds=duration_seconds,
                feed_version=feed_version,
                description=description,
            ),
        )
        return StageResult.succeeded(
            state_update,
            events=events,
            span_attributes={ATTR_RSS_ITEM_COUNT: str(len(channel.items))},
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
