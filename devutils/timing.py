"""Timing helpers."""

import time


class Timer:
    """Context manager measuring wall-clock time of a block.

    Uses :func:`time.perf_counter`, so the reading is monotonic and
    unaffected by system clock adjustments mid-block.

    >>> with Timer() as t:
    ...     pass
    >>> t.elapsed >= 0
    True

    The elapsed time is available inside the block too, as a running
    total since entry.
    """

    def __init__(self):
        self._start = None
        self._elapsed = None

    def __enter__(self):
        self._start = time.perf_counter()
        self._elapsed = None
        return self

    def __exit__(self, exc_type, exc, tb):
        self._elapsed = time.perf_counter() - self._start
        return False

    @property
    def elapsed(self):
        """Seconds elapsed — running while inside the block, final after."""
        if self._start is None:
            raise RuntimeError("Timer has not been entered")
        if self._elapsed is None:
            return time.perf_counter() - self._start
        return self._elapsed
