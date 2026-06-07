"""Exhaustive tests for the pure HTTP byte-range parser (OI-7).

parse_byte_range is the load-bearing, side-effect-free core of the range
server. Architecture Baseline section 15 calls for range support; this is the
exhaustive, server-free coverage its docstring promises.
"""

from __future__ import annotations

import pytest

from storytime.http.ranges import ByteRange, RangeNotSatisfiable, parse_byte_range

_SIZE = 1000


# -- no usable range: caller serves the whole file (200) ---------------------

def test_absent_header_returns_none() -> None:
    assert parse_byte_range(None, _SIZE) is None


def test_unsupported_unit_returns_none() -> None:
    assert parse_byte_range("items=0-10", _SIZE) is None


def test_empty_range_set_returns_none() -> None:
    assert parse_byte_range("bytes=", _SIZE) is None


def test_multi_range_request_returns_none() -> None:
    # RFC 7233 multipart/byteranges is intentionally unsupported.
    assert parse_byte_range("bytes=0-99,200-299", _SIZE) is None


def test_missing_dash_returns_none() -> None:
    assert parse_byte_range("bytes=500", _SIZE) is None


def test_non_integer_bound_returns_none() -> None:
    assert parse_byte_range("bytes=abc-def", _SIZE) is None


def test_inverted_range_returns_none() -> None:
    assert parse_byte_range("bytes=500-100", _SIZE) is None


def test_negative_first_byte_returns_none() -> None:
    assert parse_byte_range("bytes=-5-100", _SIZE) is None


def test_bare_suffix_dash_returns_none() -> None:
    assert parse_byte_range("bytes=-", _SIZE) is None


# -- explicit ranges ---------------------------------------------------------

def test_closed_range_is_parsed_inclusive() -> None:
    result = parse_byte_range("bytes=0-499", _SIZE)
    assert result == ByteRange(start=0, end=499)
    assert result is not None and result.length == 500


def test_open_ended_range_runs_to_last_byte() -> None:
    assert parse_byte_range("bytes=500-", _SIZE) == ByteRange(start=500, end=999)


def test_closed_range_end_is_clamped_to_last_byte() -> None:
    # An end past EOF is clamped, not rejected.
    assert parse_byte_range("bytes=900-100000", _SIZE) == ByteRange(
        start=900, end=999
    )


def test_single_byte_range() -> None:
    result = parse_byte_range("bytes=0-0", _SIZE)
    assert result == ByteRange(start=0, end=0)
    assert result is not None and result.length == 1


def test_whitespace_is_tolerated() -> None:
    assert parse_byte_range("  bytes = 10 - 20 ", _SIZE) == ByteRange(
        start=10, end=20
    )


# -- suffix ranges ("the last N bytes") --------------------------------------

def test_suffix_range_returns_the_tail() -> None:
    assert parse_byte_range("bytes=-100", _SIZE) == ByteRange(start=900, end=999)


def test_suffix_larger_than_file_clamps_to_whole_file() -> None:
    assert parse_byte_range("bytes=-5000", _SIZE) == ByteRange(start=0, end=999)


# -- unsatisfiable ranges raise (caller answers 416) -------------------------

def test_start_at_or_past_eof_is_unsatisfiable() -> None:
    with pytest.raises(RangeNotSatisfiable):
        parse_byte_range("bytes=1000-1100", _SIZE)


def test_zero_length_suffix_is_unsatisfiable() -> None:
    with pytest.raises(RangeNotSatisfiable):
        parse_byte_range("bytes=-0", _SIZE)


def test_any_concrete_range_on_an_empty_file_is_unsatisfiable() -> None:
    with pytest.raises(RangeNotSatisfiable):
        parse_byte_range("bytes=-100", 0)
    with pytest.raises(RangeNotSatisfiable):
        parse_byte_range("bytes=0-10", 0)


def test_open_ended_zero_start_on_empty_file_is_unsatisfiable() -> None:
    with pytest.raises(RangeNotSatisfiable):
        parse_byte_range("bytes=0-", 0)


# -- input validation --------------------------------------------------------

def test_negative_size_is_a_value_error() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        parse_byte_range("bytes=0-10", -1)


# -- ByteRange value object --------------------------------------------------

def test_byte_range_content_range_header_rendering() -> None:
    assert ByteRange(start=0, end=499).content_range(_SIZE) == "bytes 0-499/1000"


def test_byte_range_is_frozen() -> None:
    one = ByteRange(start=1, end=2)
    with pytest.raises(AttributeError):
        one.start = 9  # type: ignore[misc]
