import itertools

import pytest

from devutils import chunked


def test_even_split():
    assert list(chunked(range(6), 2)) == [[0, 1], [2, 3], [4, 5]]


def test_final_chunk_is_short_not_padded():
    assert list(chunked(range(5), 2)) == [[0, 1], [2, 3], [4]]


def test_empty_input():
    assert list(chunked([], 3)) == []


def test_size_larger_than_input():
    assert list(chunked([1, 2], 10)) == [[1, 2]]


def test_consumes_generators_lazily():
    infinite = itertools.count()
    first_two = list(itertools.islice(chunked(infinite, 3), 2))
    assert first_two == [[0, 1, 2], [3, 4, 5]]


def test_rejects_zero_size():
    with pytest.raises(ValueError):
        list(chunked([1, 2], 0))
