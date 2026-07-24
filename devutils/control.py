"""Control-flow helpers."""

import functools
import time


def retry(attempts=3, delay=0.1, backoff=2.0, exceptions=(Exception,)):
    """Retry the wrapped callable on failure with exponential backoff.

    The final attempt's exception propagates unchanged, so callers still
    see the real failure rather than a wrapper error.

    >>> @retry(attempts=5, delay=0)
    ... def flaky():
    ...     ...
    """
    if attempts < 1:
        raise ValueError("attempts must be at least 1")

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == attempts:
                        raise
                    if current_delay:
                        time.sleep(current_delay)
                    current_delay *= backoff

        return wrapper

    return decorator


def memoize(ttl=None):
    """Cache a function's return value per argument set.

    Differs from :func:`functools.lru_cache` in two ways that matter for
    caching remote lookups: entries can expire via ``ttl`` seconds, and
    ``f(a=1, b=2)`` and ``f(b=2, a=1)`` share one entry.

    Exceptions are never cached — a failed call is retried next time.

    >>> @memoize(ttl=60)
    ... def lookup(user_id):
    ...     ...
    """
    def decorator(func):
        cache = {}
        stats = {"hits": 0, "misses": 0}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            hash(key)  # Fail loudly now rather than silently not caching.

            if key in cache:
                value, expires_at = cache[key]
                if expires_at is None or time.monotonic() < expires_at:
                    stats["hits"] += 1
                    return value
                del cache[key]

            stats["misses"] += 1
            value = func(*args, **kwargs)
            expires_at = None if ttl is None else time.monotonic() + ttl
            cache[key] = (value, expires_at)
            return value

        def cache_clear():
            cache.clear()
            stats["hits"] = 0
            stats["misses"] = 0

        def cache_info():
            return {"hits": stats["hits"], "misses": stats["misses"], "size": len(cache)}

        wrapper.cache_clear = cache_clear
        wrapper.cache_info = cache_info
        return wrapper

    return decorator
