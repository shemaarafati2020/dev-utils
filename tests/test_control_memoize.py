import time

import pytest

from devutils import memoize


def test_caches_repeated_calls():
    calls = []

    @memoize()
    def double(n):
        calls.append(n)
        return n * 2

    assert double(2) == 4
    assert double(2) == 4
    assert calls == [2]


def test_distinct_arguments_cached_separately():
    calls = []

    @memoize()
    def double(n):
        calls.append(n)
        return n * 2

    double(1)
    double(2)
    double(1)
    assert calls == [1, 2]


def test_keyword_order_does_not_matter():
    calls = []

    @memoize()
    def add(a, b):
        calls.append((a, b))
        return a + b

    assert add(a=1, b=2) == 3
    assert add(b=2, a=1) == 3
    assert calls == [(1, 2)]


def test_ttl_expiry():
    calls = []

    @memoize(ttl=0.05)
    def now(n):
        calls.append(n)
        return n

    now(1)
    now(1)
    assert calls == [1]
    time.sleep(0.06)
    now(1)
    assert calls == [1, 1]


def test_none_is_cached_not_recomputed():
    calls = []

    @memoize()
    def returns_none():
        calls.append(1)
        return None

    assert returns_none() is None
    assert returns_none() is None
    assert len(calls) == 1


def test_exceptions_are_not_cached():
    calls = []

    @memoize()
    def flaky():
        calls.append(1)
        if len(calls) == 1:
            raise ValueError("boom")
        return "ok"

    with pytest.raises(ValueError):
        flaky()
    assert flaky() == "ok"
    assert len(calls) == 2


def test_cache_clear():
    calls = []

    @memoize()
    def double(n):
        calls.append(n)
        return n * 2

    double(2)
    double.cache_clear()
    double(2)
    assert calls == [2, 2]


def test_cache_info():
    @memoize()
    def double(n):
        return n * 2

    double(1)
    double(1)
    double(2)
    info = double.cache_info()
    assert info["hits"] == 1
    assert info["misses"] == 2
    assert info["size"] == 2


def test_preserves_metadata():
    @memoize()
    def documented():
        """Docstring survives."""

    assert documented.__name__ == "documented"
    assert documented.__doc__ == "Docstring survives."


def test_unhashable_argument_raises():
    @memoize()
    def identity(value):
        return value

    with pytest.raises(TypeError):
        identity([1, 2])
