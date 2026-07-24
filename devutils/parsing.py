"""Parsing helpers."""

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
