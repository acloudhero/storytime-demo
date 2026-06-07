"""RSS feed builder (skeleton).

Builds an RSS 2.0 feed with the iTunes podcast namespace from episode data.
Uses the standard library xml.etree so the scaffold adds no XML dependency.

Phase 2 status: skeleton. It emits a well-formed feed; full iTunes-tag
coverage, enclosure byte-length verification against published audio, and
feed-versioning are Phase 3 work (see docs/open-issues.md).
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

_ITUNES_NS = "http://www.itunes.com/dtds/podcast-1.0.dtd"


@dataclass(frozen=True, slots=True)
class FeedItem:
    """One podcast episode entry."""

    guid: str
    title: str
    description: str
    audio_url: str
    audio_bytes: int
    duration_seconds: float
    published_at: str  # RFC 822 date string


@dataclass(frozen=True, slots=True)
class FeedChannel:
    """Podcast-level feed metadata."""

    title: str
    link: str
    description: str
    language: str = "en-us"
    items: tuple[FeedItem, ...] = field(default_factory=tuple)


def _seconds_to_hms(seconds: float) -> str:
    total = int(seconds)
    return f"{total // 3600:02d}:{(total % 3600) // 60:02d}:{total % 60:02d}"


def build_feed(channel: FeedChannel) -> str:
    """Render *channel* as an RSS 2.0 + iTunes XML string."""
    # register_namespace makes ElementTree emit a single xmlns:itunes
    # declaration on serialization; declaring it manually here too would
    # produce a duplicate attribute and a malformed feed.
    ET.register_namespace("itunes", _ITUNES_NS)
    rss = ET.Element("rss", {"version": "2.0"})
    chan = ET.SubElement(rss, "channel")
    ET.SubElement(chan, "title").text = channel.title
    ET.SubElement(chan, "link").text = channel.link
    ET.SubElement(chan, "description").text = channel.description
    ET.SubElement(chan, "language").text = channel.language

    for item in channel.items:
        entry = ET.SubElement(chan, "item")
        ET.SubElement(entry, "title").text = item.title
        ET.SubElement(entry, "description").text = item.description
        guid = ET.SubElement(entry, "guid", {"isPermaLink": "false"})
        guid.text = item.guid
        ET.SubElement(entry, "pubDate").text = item.published_at
        ET.SubElement(
            entry,
            "enclosure",
            {
                "url": item.audio_url,
                "length": str(item.audio_bytes),
                "type": "audio/mpeg",
            },
        )
        ET.SubElement(entry, f"{{{_ITUNES_NS}}}duration").text = _seconds_to_hms(
            item.duration_seconds
        )

    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(
        rss, encoding="unicode"
    )
