"""Mapping helpers."""

import copy


def deep_merge(base, override):
    """Recursively merge ``override`` into ``base``, returning a new dict.

    Nested dicts are merged key by key; every other type is replaced
    outright. Neither input is mutated — useful for layering a user
    config over a default one.

    >>> deep_merge({"a": {"x": 1, "y": 2}}, {"a": {"y": 99}})
    {'a': {'x': 1, 'y': 99}}
    """
    merged = copy.deepcopy(base)

    for key, value in override.items():
        if (
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(value, dict)
        ):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)

    return merged
