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
