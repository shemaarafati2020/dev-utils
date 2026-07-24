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


_DURATION_UNITS = (("d", 86400), ("h", 3600), ("m", 60), ("s", 1))


def human_duration(seconds, max_units=None):
    """Format a duration in seconds as a compact human-readable string.

    Zero-valued units are skipped rather than padded, so an exact hour
    reads ``1h`` and not ``1h 0m 0s``.

    >>> human_duration(3661)
    '1h 1m 1s'
    >>> human_duration(0.25)
    '250ms'
    """
    if seconds < 0:
        raise ValueError("seconds must be non-negative")

    if seconds < 1:
        milliseconds = int(seconds * 1000)
        return "%dms" % milliseconds if milliseconds else "0s"

    remaining = int(seconds)
    parts = []
    for label, size in _DURATION_UNITS:
        value, remaining = divmod(remaining, size)
        if value:
            parts.append("%d%s" % (value, label))

    if max_units is not None:
        parts = parts[:max_units]

    return " ".join(parts)
