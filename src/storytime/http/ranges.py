"""HTTP byte-range parsing — a pure, fully unit-tested function.

ARCH-LOCK: Range parsing is pure and load-bearing
DO NOT REFACTOR: parse_byte_range MUST stay a pure function of (header, size)
with no socket, no I/O, and no global state. The range server's correctness
depends on it; it is unit-tested exhaustively without a server, exactly as
validate_bind_host is. Do not fold this logic back into the request handler.
Rationale: Architecture Baseline section 15 — the local server "must support
HTTP range requests"; mainstream podcast clients issue them for audio and a
server that mishandles them misbehaves. Keeping the parser pure is what makes
that requirement testable.

Scope (deliberate, documented simplifications):

* A single range only. RFC 7233 permits a comma-separated multi-range request
  answered with ``multipart/byteranges``; podcast clients do not use it. A
  multi-range header is treated as "no usable range" and the caller serves the
  whole representation (200) — RFC 7233 section 3.1 explicitly allows a server
  to ignore a Range header.
* A syntactically malformed Range header is likewise ignored (caller serves
  200), per the same RFC allowance — never a 400.
* Only ``bytes`` is a supported range unit.
"""

from __future__ import annotations

from dataclasses import dataclass

# The HTTP range unit StoryTime serves. Any other unit is ignored (full 200).
_RANGE_UNIT = "bytes"


class RangeNotSatisfiable(Exception):
    """The client asked for a range that lies outside the representation.

    The caller answers this with ``416 Range Not Satisfiable`` plus a
    ``Content-Range: bytes */<size>`` header.
    """


@dataclass(frozen=True, slots=True)
class ByteRange:
    """A single satisfiable byte range, both bounds inclusive (RFC 7233)."""

    start: int
    end: int  # inclusive

    @property
    def length(self) -> int:
        """Number of bytes the range covers."""
        return self.end - self.start + 1

    def content_range(self, size: int) -> str:
        """Render the ``Content-Range`` header value for a *size*-byte file."""
        return f"{_RANGE_UNIT} {self.start}-{self.end}/{size}"


def parse_byte_range(header: str | None, size: int) -> ByteRange | None:
    """Resolve a ``Range`` header against a representation of *size* bytes.

    Returns:
      * ``None`` — no Range header, an unsupported unit, a multi-range
        request, or a malformed header. The caller serves the whole file (200).
      * a :class:`ByteRange` — exactly one satisfiable range; the caller serves
        ``206 Partial Content``.

    Raises:
      :class:`RangeNotSatisfiable` — the header is well-formed and names a
      single range, but that range lies entirely outside the file; the caller
      serves ``416``.

    *size* must be >= 0. A zero-length file makes every concrete range
    unsatisfiable.
    """
    if size < 0:
        raise ValueError(f"size must be non-negative, got {size}")
    if header is None:
        return None

    spec = header.strip()
    unit, _, rendered = spec.partition("=")
    if unit.strip().lower() != _RANGE_UNIT or not rendered.strip():
        return None

    # A single range only. A comma means a multi-range request: ignore it and
    # let the caller serve the whole file.
    if "," in rendered:
        return None

    first_raw, sep, last_raw = rendered.strip().partition("-")
    if not sep:
        # No "-" at all: not a valid byte-range-spec.
        return None
    first_raw, last_raw = first_raw.strip(), last_raw.strip()

    try:
        if not first_raw:
            # Suffix form "-N": the final N bytes.
            if not last_raw:
                return None
            suffix = int(last_raw)
            if suffix <= 0:
                # "bytes=-0" requests zero bytes — unsatisfiable per RFC 7233.
                raise RangeNotSatisfiable("suffix range of zero length")
            if size == 0:
                raise RangeNotSatisfiable("range requested on an empty file")
            start = max(0, size - suffix)
            return ByteRange(start=start, end=size - 1)

        start = int(first_raw)
        if start < 0:
            return None
        if start >= size:
            # The first-byte-pos is at or past the end of the file.
            raise RangeNotSatisfiable(
                f"range start {start} is beyond file size {size}"
            )
        if not last_raw:
            # Open-ended "first-": to the end of the file.
            return ByteRange(start=start, end=size - 1)

        end = int(last_raw)
        if end < start:
            # An inverted range is malformed: ignore it (serve 200).
            return None
        # Clamp the inclusive end to the last valid byte offset.
        return ByteRange(start=start, end=min(end, size - 1))
    except ValueError:
        # A non-integer bound: malformed header, ignore it (serve 200).
        return None


__all__ = ["ByteRange", "RangeNotSatisfiable", "parse_byte_range"]
