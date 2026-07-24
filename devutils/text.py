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
