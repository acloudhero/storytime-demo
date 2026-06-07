"""Telemetry data-hygiene helpers — OTel-free string sanitisation.

ARCH-LOCK: Telemetry Import Boundary (see storytime.adapters.telemetry.base)
DO NOT REFACTOR: This module sanitises strings *before* they are attached to a
span, span event, metric, or log. It deliberately does NOT import
opentelemetry. The OTel adapter routes every operator-facing string
(``error.message``, event payloads) through here so that the data-hygiene
rules of the Phase 5 task are enforced at one choke point.

Rules enforced (Phase 5 task, section 5 "Do not record"):

* No absolute filesystem paths. A run is workspace-relocatable; an absolute
  path in a span would also leak the host layout. Absolute POSIX and Windows
  paths are redacted to ``<path>``.
* Bounded length. A span attribute must never carry a large payload, so every
  sanitised value is truncated to ``MAX_ATTR_LEN`` characters.

What this module does NOT do: it is not a secrets scrubber and is not a
substitute for emitting safe data in the first place. Stages and the runner
must still avoid putting raw story text or full manifests into events; this is
the backstop, not the primary control.
"""

from __future__ import annotations

import re

# A span attribute value is truncated to this many characters. Long enough for
# a readable error message, short enough that no payload can ride along.
MAX_ATTR_LEN = 256

_TRUNCATION_MARKER = "...<truncated>"

# Absolute POSIX path: a leading "/" then at least two "/"-separated segments,
# e.g. /home/user/runs/state.db. A bare "/" or a single "/v1" is left alone so
# that, for example, an OTLP path fragment is not over-redacted.
_POSIX_ABS_PATH = re.compile(r"/(?:[^/\s]+/)+[^/\s]*")

# Absolute Windows path: a drive letter then a slash and at least one segment,
# e.g. C:\Users\me\runs or C:/Users/me/runs.
_WINDOWS_ABS_PATH = re.compile(r"[A-Za-z]:[\\/](?:[^\\/\s]+[\\/]?)+")

_REDACTED_PATH = "<path>"


def redact_paths(value: str) -> str:
    """Return *value* with absolute filesystem paths replaced by ``<path>``.

    Both absolute POSIX paths and absolute Windows paths are redacted.
    Relative storage keys (``run-id/artifacts/...``) are deliberately left
    intact — they are portable and safe, and carry useful context.
    """
    redacted = _WINDOWS_ABS_PATH.sub(_REDACTED_PATH, value)
    return _POSIX_ABS_PATH.sub(_REDACTED_PATH, redacted)


def truncate(value: str, *, limit: int = MAX_ATTR_LEN) -> str:
    """Return *value* truncated to *limit* characters with a clear marker."""
    if len(value) <= limit:
        return value
    head = limit - len(_TRUNCATION_MARKER)
    if head <= 0:
        return value[:limit]
    return value[:head] + _TRUNCATION_MARKER


def sanitize(value: str | None) -> str | None:
    """Sanitise *value* for use as a span attribute / span-event attribute.

    Redacts absolute filesystem paths, then bounds the length. ``None`` passes
    through as ``None`` so an absent attribute stays absent.
    """
    if value is None:
        return None
    return truncate(redact_paths(value))


__all__ = ["MAX_ATTR_LEN", "redact_paths", "sanitize", "truncate"]
