"""Iterable helpers."""

import itertools


def chunked(iterable, size):
    """Yield successive lists of at most ``size`` items from ``iterable``.

    Works with any iterable, including generators and infinite ones, and
    never materialises more than one chunk at a time. The final chunk is
    short rather than padded.

    >>> list(chunked(range(5), 2))
    [[0, 1], [2, 3], [4]]
    """
    if size < 1:
        raise ValueError("size must be at least 1")

    iterator = iter(iterable)
    while True:
        chunk = list(itertools.islice(iterator, size))
        if not chunk:
            return
        yield chunk
