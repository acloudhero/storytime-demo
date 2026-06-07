"""Time source.

Time is injected, never read ad hoc, so that runs are reproducible in tests.
The RunnerContext carries a Clock; stages and the runner read time from it.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Protocol, runtime_checkable


@runtime_checkable
class Clock(Protocol):
    """A source of the current time. Implementations must return aware UTC."""

    def now(self) -> datetime: ...


class SystemClock:
    """The real clock. Returns timezone-aware UTC time."""

    def now(self) -> datetime:
        return datetime.now(UTC)


class FixedClock:
    """A deterministic clock for tests; always returns the same moment."""

    def __init__(self, moment: datetime) -> None:
        self._moment = moment

    def now(self) -> datetime:
        return self._moment


def to_iso(moment: datetime) -> str:
    """Render *moment* as an ISO-8601 string normalised to UTC."""
    return moment.astimezone(UTC).isoformat()
