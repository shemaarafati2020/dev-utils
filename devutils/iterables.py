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


def unique(iterable, key=None):
    """Yield items from ``iterable``, skipping ones already seen.

    Order-preserving — the first occurrence of each item survives, which
    is the difference between this and ``set(iterable)``. Lazy, so it
    works on generators and infinite sources.

    Pass ``key`` to dedupe unhashable items by some hashable projection,
    e.g. ``unique(rows, key=lambda r: r["id"])``.

    >>> list(unique([3, 1, 3, 2, 1]))
    [3, 1, 2]
    """
    seen = set()

    for item in iterable:
        marker = item if key is None else key(item)
        if marker not in seen:
            seen.add(marker)
            yield item
