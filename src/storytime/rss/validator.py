"""RSS feed structural validator.

ARCH-LOCK: Validate before the atomic replace
DO NOT REFACTOR: validate_feed runs in the publish stage on the freshly built
feed XML BEFORE it is atomically swapped into place. A feed that fails
validation must abort the publish; a partial or malformed feed.xml must never
replace a good one.
Rationale: Architecture Baseline section 14 — "feed.xml is written atomically:
write to a temp file, validate, then atomically replace ... Feed validity is
checked in the publish stage before the replace."

This validator is intentionally a structural safety net, not a full RSS/iTunes
schema. build_feed produces a correct feed by construction; validate_feed
guards against a regression in the builder or a corrupted channel slipping
through. It imports only the standard library.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET


class FeedValidationError(ValueError):
    """Raised when a rendered RSS feed fails structural validation."""


def validate_feed(xml: str) -> None:
    """Validate *xml* as a StoryTime RSS 2.0 feed; raise on any problem.

    Checks, in order: the document is well-formed XML; the root is
    ``<rss version="2.0">``; there is exactly one ``<channel>``; the channel
    carries non-empty ``title``, ``link``, and ``description``; and every
    ``<item>`` carries a ``<guid>`` and an ``<enclosure>`` with non-empty
    ``url``, ``length``, and ``type`` attributes.
    """
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as exc:
        raise FeedValidationError(f"feed is not well-formed XML: {exc}") from exc

    if root.tag != "rss":
        raise FeedValidationError(f"feed root element is {root.tag!r}, expected 'rss'")
    if root.get("version") != "2.0":
        raise FeedValidationError(
            f"feed rss version is {root.get('version')!r}, expected '2.0'"
        )

    channels = root.findall("channel")
    if len(channels) != 1:
        raise FeedValidationError(
            f"feed must contain exactly one <channel>, found {len(channels)}"
        )
    channel = channels[0]

    for required in ("title", "link", "description"):
        element = channel.find(required)
        if element is None or not (element.text or "").strip():
            raise FeedValidationError(
                f"feed channel is missing a non-empty <{required}>"
            )

    for index, item in enumerate(channel.findall("item")):
        if item.find("guid") is None:
            raise FeedValidationError(f"feed item {index} is missing a <guid>")
        enclosure = item.find("enclosure")
        if enclosure is None:
            raise FeedValidationError(f"feed item {index} is missing an <enclosure>")
        for attribute in ("url", "length", "type"):
            if not (enclosure.get(attribute) or "").strip():
                raise FeedValidationError(
                    f"feed item {index} enclosure is missing a non-empty "
                    f"{attribute!r} attribute"
                )


__all__ = ["FeedValidationError", "validate_feed"]
