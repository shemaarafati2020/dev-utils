"""Small, dependency-free helpers."""

from devutils.control import retry
from devutils.iterables import chunked
from devutils.mappings import deep_merge, flatten_dict
from devutils.size import humanize_bytes
from devutils.text import slugify
from devutils.timing import Timer

__version__ = "0.1.0"

__all__ = [
    "Timer",
    "chunked",
    "deep_merge",
    "flatten_dict",
    "humanize_bytes",
    "retry",
    "slugify",
]
