"""Iterable helpers."""

import collections
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


def partition(predicate, iterable):
    """Split ``iterable`` into ``(matching, rest)`` lists.

    Unlike the ``itertools`` recipe, this consumes the input exactly once
    and calls ``predicate`` exactly once per item — so it is safe with
    generators and with expensive or side-effecting predicates.

    >>> partition(lambda n: n % 2 == 0, range(6))
    ([0, 2, 4], [1, 3, 5])
    """
    matching = []
    rest = []

    for item in iterable:
        if predicate(item):
            matching.append(item)
        else:
            rest.append(item)

    return matching, rest


def windowed(iterable, size):
    """Yield overlapping tuples of ``size`` consecutive items.

    Where :func:`chunked` splits an iterable into disjoint batches, this
    slides — useful for comparing each item with its neighbours.

    Yields a new tuple per window rather than a live view, so windows can
    be collected into a list without aliasing each other. Nothing is
    yielded if the input is shorter than ``size``.

    >>> list(windowed([1, 2, 3, 4], 2))
    [(1, 2), (2, 3), (3, 4)]
    """
    if size < 1:
        raise ValueError("size must be at least 1")

    window = collections.deque(maxlen=size)

    for item in iterable:
        window.append(item)
        if len(window) == size:
            yield tuple(window)


def group_by(key, iterable, transform=None):
    """Group items into a dict of lists keyed by ``key(item)``.

    Unlike :func:`itertools.groupby`, the input does not need to be
    sorted — that function only groups *adjacent* equal keys, which
    silently produces duplicate groups on unsorted data.

    Returns a plain dict, not a defaultdict, so a missing key raises
    ``KeyError`` instead of quietly creating an empty group.

    >>> group_by(len, ["a", "bb", "cc", "d"])
    {1: ['a', 'd'], 2: ['bb', 'cc']}
    """
    grouped = {}

    for item in iterable:
        value = item if transform is None else transform(item)
        grouped.setdefault(key(item), []).append(value)

    return grouped
