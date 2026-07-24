import pytest

from devutils import humanize_bytes, parse_size


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("0", 0),
        ("512", 512),
        ("512B", 512),
        ("1 KiB", 1024),
        ("1KiB", 1024),
        ("1.5 KiB", 1536),
        ("1 MiB", 1024 ** 2),
        ("2 GiB", 1024 ** 3 * 2),
        ("1 kB", 1000),
        ("1.5 kB", 1500),
        ("1 MB", 1000 ** 2),
        ("1 GB", 1000 ** 3),
    ],
)
def test_parses(raw, expected):
    assert parse_size(raw) == expected


@pytest.mark.parametrize("raw", ["1 kib", "1 KIB", "1 KiB", "  1KiB  "])
def test_case_and_whitespace_insensitive(raw):
    assert parse_size(raw) == 1024


def test_binary_and_decimal_differ():
    assert parse_size("1 kB") != parse_size("1 KiB")


def test_integers_pass_through():
    assert parse_size(1024) == 1024


@pytest.mark.parametrize("size", [0, 512, 1024, 1536, 1024 ** 2, 1024 ** 3 * 2])
def test_round_trips_with_humanize_bytes(size):
    assert parse_size(humanize_bytes(size)) == size


@pytest.mark.parametrize("raw", ["", "abc", "1 XiB", "KiB", "1.2.3 KiB", "1 KiB extra"])
def test_invalid_raises(raw):
    with pytest.raises(ValueError):
        parse_size(raw)


def test_negative_raises():
    with pytest.raises(ValueError):
        parse_size("-1 KiB")
