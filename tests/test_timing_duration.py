import pytest

from devutils import human_duration


@pytest.mark.parametrize(
    "seconds,expected",
    [
        (0, "0s"),
        (0.004, "4ms"),
        (0.25, "250ms"),
        (1, "1s"),
        (45, "45s"),
        (90, "1m 30s"),
        (3600, "1h"),
        (3661, "1h 1m 1s"),
        (86400, "1d"),
        (90061, "1d 1h 1m 1s"),
    ],
)
def test_formats(seconds, expected):
    assert human_duration(seconds) == expected


def test_max_units_truncates_least_significant():
    assert human_duration(90061, max_units=2) == "1d 1h"


def test_sub_millisecond_floor():
    assert human_duration(0.0001) == "0s"


def test_negative_rejected():
    with pytest.raises(ValueError):
        human_duration(-1)
