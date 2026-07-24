import pytest

from devutils import human_duration, parse_duration


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("0s", 0),
        ("30s", 30),
        ("1m", 60),
        ("1m30s", 90),
        ("1h", 3600),
        ("1h30m", 5400),
        ("1h1m1s", 3661),
        ("1d", 86400),
        ("1d1h1m1s", 90061),
        ("1w", 604800),
    ],
)
def test_parses_compound(raw, expected):
    assert parse_duration(raw) == expected


def test_spaces_between_components():
    assert parse_duration("1d 1h 1m 1s") == 90061


def test_milliseconds():
    assert parse_duration("500ms") == 0.5
    assert parse_duration("250ms") == 0.25


def test_ms_is_not_read_as_minutes():
    assert parse_duration("5ms") != parse_duration("5m")
    assert parse_duration("5ms") == 0.005


def test_bare_number_is_seconds():
    assert parse_duration("90") == 90


def test_numbers_pass_through():
    assert parse_duration(90) == 90
    assert parse_duration(1.5) == 1.5


def test_case_insensitive():
    assert parse_duration("1H30M") == 5400


def test_fractional_components():
    assert parse_duration("1.5h") == 5400


@pytest.mark.parametrize("seconds", [0, 30, 90, 3661, 86400, 90061])
def test_round_trips_with_human_duration(seconds):
    assert parse_duration(human_duration(seconds)) == seconds


@pytest.mark.parametrize("raw", ["", "abc", "1x", "h", "1h junk", "1..5h"])
def test_invalid_raises(raw):
    with pytest.raises(ValueError):
        parse_duration(raw)


def test_negative_raises():
    with pytest.raises(ValueError):
        parse_duration(-5)


def test_returns_int_when_whole():
    assert isinstance(parse_duration("1h"), int)
    assert isinstance(parse_duration("500ms"), float)
