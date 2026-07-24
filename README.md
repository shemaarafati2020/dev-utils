# dev-utils

[![CI](https://github.com/shemaarafati2020/dev-utils/actions/workflows/ci.yml/badge.svg)](https://github.com/shemaarafati2020/dev-utils/actions/workflows/ci.yml)

Small, dependency-free Python helpers I keep re-writing across projects.
No runtime dependencies; tested on Python 3.9, 3.11 and 3.13.

## Install

```bash
pip install -e .
```

## API

| Helper | Module | Purpose |
| --- | --- | --- |
| `slugify` | `devutils.text` | URL-safe slugs, accent folding, optional truncation |
| `truncate` | `devutils.text` | Shorten to a hard character budget, suffix included |
| `humanize_bytes` | `devutils.size` | Byte counts as KiB/MiB or kB/MB |
| `human_duration` | `devutils.timing` | Seconds as `1d 1h 1m 1s`, zero units skipped |
| `Timer` | `devutils.timing` | Context manager for wall-clock timing |
| `retry` | `devutils.control` | Retry with exponential backoff |
| `memoize` | `devutils.control` | Caching decorator with TTL expiry |
| `chunked` | `devutils.iterables` | Lazily batch an iterable into fixed-size lists |
| `unique` | `devutils.iterables` | Order-preserving dedupe |
| `partition` | `devutils.iterables` | Split into `(matching, rest)` in one pass |
| `deep_merge` | `devutils.mappings` | Recursively layer one dict over another |
| `flatten_dict` | `devutils.mappings` | Nested dict to dotted keys |
| `parse_bool` | `devutils.parsing` | Env-var strings to real booleans |
| `atomic_write` | `devutils.fs` | Crash-safe file writes via temp file + rename |

## Usage

### Text

```python
from devutils import slugify, truncate

slugify("Héllo,  World!")              # 'hello-world'
truncate("the quick brown fox", 12)    # 'the quick…'  (never exceeds 12 chars)
```

### Formatting

```python
from devutils import humanize_bytes, human_duration

humanize_bytes(1536)                   # '1.5 KiB'
humanize_bytes(1500, binary=False)     # '1.5 kB'
human_duration(3661)                   # '1h 1m 1s'
human_duration(90061, max_units=2)     # '1d 1h'
```

### Control flow

```python
from devutils import Timer, memoize, retry

@retry(attempts=3, delay=0.1)
@memoize(ttl=60)
def fetch(user_id):
    ...

with Timer() as t:
    fetch(42)
print(f"took {t.elapsed:.3f}s")
```

### Iterables

```python
from devutils import chunked, partition, unique

list(chunked(range(5), 2))                     # [[0, 1], [2, 3], [4]]
list(unique([3, 1, 3, 2, 1]))                  # [3, 1, 2]
partition(lambda n: n % 2 == 0, range(6))      # ([0, 2, 4], [1, 3, 5])
```

### Config

```python
from devutils import deep_merge, flatten_dict, parse_bool

deep_merge({"db": {"host": "localhost", "port": 5432}}, {"db": {"port": 5433}})
# {'db': {'host': 'localhost', 'port': 5433}}

flatten_dict({"db": {"host": "localhost"}})    # {'db.host': 'localhost'}
parse_bool(os.environ.get("DEBUG"))            # 'false' -> False, unset -> False
```

### Files

```python
from devutils import atomic_write

# Readers see either the old file or the new one, never a partial write.
with atomic_write("config.json") as f:
    json.dump(config, f)
```

## Development

```bash
python -m venv .venv
.venv/bin/pip install -e . pytest
.venv/bin/python -m pytest
```

## License

MIT
