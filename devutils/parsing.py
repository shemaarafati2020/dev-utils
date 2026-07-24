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


_DURATION_SCALE = {
    "ms": 0.001,
    "s": 1,
    "m": 60,
    "h": 3600,
    "d": 86400,
    "w": 604800,
}

# "ms" must precede "m" in the alternation, or "5ms" parses as 5 minutes.
_DURATION_UNIT = "(?:ms|s|m|h|d|w)"
_DURATION_COMPONENT = re.compile(r"(\d+(?:\.\d+)?)\s*(%s)" % _DURATION_UNIT)
_DURATION_WHOLE = re.compile(r"(?:\d+(?:\.\d+)?\s*%s\s*)+" % _DURATION_UNIT)
_BARE_NUMBER = re.compile(r"\d+(?:\.\d+)?")


def parse_duration(value):
    """Parse a duration string such as ``"1h30m"`` into seconds.

    The inverse of :func:`devutils.human_duration` — every value that
    function emits parses back to the same number. A bare number is read
    as seconds.

    >>> parse_duration("1h30m")
    5400
    >>> parse_duration("500ms")
    0.5
    """
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if value < 0:
            raise ValueError("duration must be non-negative")
        return value

    text = str(value).strip().lower()

    if _BARE_NUMBER.fullmatch(text):
        total = float(text)
    elif _DURATION_WHOLE.fullmatch(text):
        total = sum(
            float(number) * _DURATION_SCALE[unit]
            for number, unit in _DURATION_COMPONENT.findall(text)
        )
    else:
        raise ValueError("cannot parse %r as a duration" % (value,))

    return int(total) if float(total).is_integer() else total
