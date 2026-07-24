"""Text helpers."""

import re
import unicodedata

_NON_WORD = re.compile(r"[^\w\s-]", re.UNICODE)
_SEPARATORS = re.compile(r"[-\s]+")


def slugify(value, separator="-", max_length=None):
    """Return a URL-safe slug for ``value``.

    Accents are folded to ASCII, punctuation is dropped, and runs of
    whitespace or hyphens collapse into a single ``separator``.

    >>> slugify("Héllo,  World!")
    'hello-world'
    """
    value = unicodedata.normalize("NFKD", str(value))
    value = value.encode("ascii", "ignore").decode("ascii")
    value = _NON_WORD.sub("", value).strip().lower()
    value = _SEPARATORS.sub(separator, value)

    if max_length is not None and len(value) > max_length:
        value = value[:max_length].rstrip(separator)

    return value


def truncate(text, length, suffix="…", whole_words=True):
    """Shorten ``text`` to at most ``length`` characters including ``suffix``.

    The returned string is never longer than ``length`` — the suffix is
    budgeted for rather than appended on top, which is what makes this
    safe for fixed-width columns.

    >>> truncate("hello world", 8)
    'hello…'
    """
    if len(suffix) > length:
        raise ValueError("suffix is longer than the requested length")

    if len(text) <= length:
        return text

    clipped = text[: length - len(suffix)]

    if whole_words:
        head, separator, _ = clipped.rpartition(" ")
        if separator:
            clipped = head

    return clipped.rstrip() + suffix
