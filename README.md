# dev-utils

[![CI](https://github.com/shemaarafati2020/dev-utils/actions/workflows/ci.yml/badge.svg)](https://github.com/shemaarafati2020/dev-utils/actions/workflows/ci.yml)

Small, dependency-free Python helpers I keep re-writing across projects.

## Install

```bash
pip install -e .
```

## Usage

```python
from devutils import chunked, humanize_bytes, retry, slugify

slugify("Héllo,  World!")            # 'hello-world'
humanize_bytes(1536)                 # '1.5 KiB'
humanize_bytes(1500, binary=False)   # '1.5 kB'
list(chunked(range(5), 2))           # [[0, 1], [2, 3], [4]]

@retry(attempts=3, delay=0.1)
def fetch():
    ...
```

| Helper | Module | Purpose |
| --- | --- | --- |
| `slugify` | `devutils.text` | URL-safe slugs, accent folding, optional truncation |
| `humanize_bytes` | `devutils.size` | Byte counts as KiB/MiB or kB/MB |
| `retry` | `devutils.control` | Retry with exponential backoff |
| `chunked` | `devutils.iterables` | Lazily batch an iterable into fixed-size lists |

## Development

```bash
python -m pytest
```

## License

MIT
