"""Small, dependency-free helpers."""

from devutils.control import retry
from devutils.iterables import chunked, partition, unique
from devutils.mappings import deep_merge, flatten_dict
from devutils.parsing import parse_bool
from devutils.size import humanize_bytes
from devutils.text import slugify, truncate
from devutils.timing import Timer, human_duration

__version__ = "0.1.0"

__all__ = [
    "Timer",
    "chunked",
    "deep_merge",
    "flatten_dict",
    "human_duration",
    "humanize_bytes",
    "parse_bool",
    "partition",
    "retry",
    "slugify",
    "truncate",
    "unique",
]
