import pytest

from devutils import humanize_bytes


@pytest.mark.parametrize(
    "size,expected",
    [
        (0, "0 B"),
        (512, "512 B"),
        (1024, "1.0 KiB"),
        (1536, "1.5 KiB"),
        (1024 ** 2, "1.0 MiB"),
        (1024 ** 3 * 2, "2.0 GiB"),
    ],
)
def test_binary(size, expected):
    assert humanize_bytes(size) == expected


@pytest.mark.parametrize(
    "size,expected",
    [(1000, "1.0 kB"), (1500, "1.5 kB"), (1000 ** 3, "1.0 GB")],
)
def test_decimal(size, expected):
    assert humanize_bytes(size, binary=False) == expected


def test_precision():
    assert humanize_bytes(1536, precision=3) == "1.500 KiB"


def test_negative_rejected():
    with pytest.raises(ValueError):
        humanize_bytes(-1)
