import itertools

import pytest

from devutils import windowed


def test_sliding_pairs():
    assert list(windowed([1, 2, 3, 4], 2)) == [(1, 2), (2, 3), (3, 4)]


def test_size_one():
    assert list(windowed([1, 2, 3], 1)) == [(1,), (2,), (3,)]


def test_size_equal_to_length():
    assert list(windowed([1, 2, 3], 3)) == [(1, 2, 3)]


def test_size_larger_than_input_yields_nothing():
    assert list(windowed([1, 2], 5)) == []


def test_empty_input():
    assert list(windowed([], 2)) == []


def test_works_on_generators():
    assert list(windowed((n for n in range(4)), 3)) == [(0, 1, 2), (1, 2, 3)]


def test_is_lazy():
    windows = itertools.islice(windowed(itertools.count(), 3), 2)
    assert list(windows) == [(0, 1, 2), (1, 2, 3)]


def test_yields_independent_tuples():
    result = list(windowed([1, 2, 3], 2))
    assert result[0] == (1, 2)
    assert result[1] == (2, 3)


def test_rejects_zero_size():
    with pytest.raises(ValueError):
        list(windowed([1, 2], 0))
