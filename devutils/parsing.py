"""Parsing helpers."""

import re

_TRUE = frozenset({"1", "true", "t", "yes", "y", "on"})
_FALSE = frozenset({"0", "false", "f", "no", "n", "off", ""})

_MISSING = object()


def parse_bool(value, default=_MISSING):
    """Interpret a config or environment string as a boolean.

    Exists because ``bool(os.environ["DEBUG"])`` is ``True`` for the
    string ``"false"``, which is a reliably annoying bug.

    >>> parse_bool("false")
    False
    >>> parse_bool("on")
    True
    """
    if isinstance(value, bool):
        return value

    if value is None:
        normalised = ""
    else:
        normalised = str(value).strip().lower()

    if normalised in _TRUE:
        return True
    if normalised in _FALSE:
        return False

    if default is not _MISSING:
        return default

    raise ValueError("cannot interpret %r as a boolean" % (value,))


_SIZE_PATTERN = re.compile(r"^(\d+(?:\.\d+)?)\s*([a-z]*)$")

_SIZE_UNITS = {"": 1, "b": 1}
for _i, _prefix in enumerate("kmgtpe", start=1):
    _SIZE_UNITS[_prefix + "b"] = 1000 ** _i
    _SIZE_UNITS[_prefix + "ib"] = 1024 ** _i


def parse_size(value):
    """Parse a human-written byte size into an integer number of bytes.

    The inverse of :func:`devutils.humanize_bytes` — every value that
    function emits parses back to the same number.

    ``KiB`` is 1024 and ``kB`` is 1000, matching the IEC and SI meanings
    rather than guessing.

    >>> parse_size("1.5 KiB")
    1536
    >>> parse_size("1 kB")
    1000
    """
    if isinstance(value, int) and not isinstance(value, bool):
        if value < 0:
            raise ValueError("size must be non-negative")
        return value

    match = _SIZE_PATTERN.match(str(value).strip().lower())
    if not match:
        raise ValueError("cannot parse %r as a byte size" % (value,))

    number, unit = match.groups()
    if unit not in _SIZE_UNITS:
        raise ValueError("unknown size unit %r" % (unit,))

    return int(round(float(number) * _SIZE_UNITS[unit]))
