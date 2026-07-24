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


def flatten_dict(mapping, separator=".", prefix=""):
    """Flatten a nested dict into a single level of dotted keys.

    Only dicts are descended into — lists and empty dicts are treated as
    leaf values, so the result round-trips back through a config loader.

    >>> flatten_dict({"db": {"host": "localhost"}})
    {'db.host': 'localhost'}
    """
    flat = {}

    for key, value in mapping.items():
        key = str(key)
        if separator in key:
            raise ValueError(
                "key %r already contains the separator %r" % (key, separator)
            )

        full_key = prefix + separator + key if prefix else key

        if isinstance(value, dict) and value:
            flat.update(flatten_dict(value, separator, full_key))
        else:
            flat[full_key] = value

    return flat
