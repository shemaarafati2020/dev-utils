import time

import pytest

from devutils import Timer


def test_measures_elapsed_time():
    with Timer() as t:
        time.sleep(0.02)
    assert t.elapsed >= 0.02


def test_elapsed_is_frozen_after_exit():
    with Timer() as t:
        time.sleep(0.01)
    first = t.elapsed
    time.sleep(0.01)
    assert t.elapsed == first


def test_elapsed_runs_while_inside_block():
    with Timer() as t:
        time.sleep(0.01)
        during = t.elapsed
        time.sleep(0.01)
        assert t.elapsed > during


def test_elapsed_before_entry_raises():
    with pytest.raises(RuntimeError):
        Timer().elapsed


def test_records_time_even_when_block_raises():
    t = Timer()
    with pytest.raises(ValueError):
        with t:
            time.sleep(0.01)
            raise ValueError("boom")
    assert t.elapsed >= 0.01


def test_does_not_suppress_exceptions():
    with pytest.raises(ValueError):
        with Timer():
            raise ValueError("boom")


def test_reusable():
    t = Timer()
    with t:
        time.sleep(0.01)
    first = t.elapsed
    with t:
        pass
    assert t.elapsed < first
