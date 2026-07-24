"""Small, dependency-free helpers."""

from devutils.control import memoize, retry
from devutils.fs import atomic_write
from devutils.iterables import chunked, partition, unique
from devutils.mappings import deep_merge, flatten_dict
from devutils.parsing import parse_bool, parse_size
from devutils.size import humanize_bytes
from devutils.text import slugify, truncate
from devutils.timing import Timer, human_duration

__version__ = "0.1.0"

__all__ = [
    "Timer",
    "atomic_write",
    "chunked",
    "deep_merge",
    "flatten_dict",
    "human_duration",
    "humanize_bytes",
    "memoize",
    "parse_bool",
    "parse_size",
    "partition",
    "retry",
    "slugify",
    "truncate",
    "unique",
]
