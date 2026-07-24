"""Small, dependency-free helpers."""

from devutils.control import retry
from devutils.iterables import chunked
from devutils.mappings import deep_merge
from devutils.size import humanize_bytes
from devutils.text import slugify

__version__ = "0.1.0"

__all__ = ["chunked", "deep_merge", "humanize_bytes", "retry", "slugify"]
