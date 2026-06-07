"""Identifier generation.

pipeline_run_id and episode_guid are ULIDs: 128-bit, Crockford-base32 encoded,
lexicographically sortable by creation time.
"""

from __future__ import annotations

import os
import time

# Crockford base32 alphabet (excludes I, L, O, U to avoid ambiguity).
_CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
_ULID_LENGTH = 26


def new_ulid() -> str:
    """Return a fresh ULID string.

    The high bits encode a millisecond timestamp, so string comparison of two
    ULIDs orders them by creation time. The low 80 bits are random.
    """
    timestamp_ms = int(time.time() * 1000)
    randomness = int.from_bytes(os.urandom(10), "big")
    value = (timestamp_ms << 80) | randomness
    chars: list[str] = []
    for _ in range(_ULID_LENGTH):
        chars.append(_CROCKFORD[value & 0x1F])
        value >>= 5
    return "".join(reversed(chars))


def is_ulid(candidate: str) -> bool:
    """Return True if *candidate* is a syntactically valid ULID string."""
    if len(candidate) != _ULID_LENGTH:
        return False
    return all(char in _CROCKFORD for char in candidate.upper())
