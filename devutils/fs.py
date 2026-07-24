"""Filesystem helpers."""

import contextlib
import os
import tempfile


@contextlib.contextmanager
def atomic_write(path, mode="w", encoding="utf-8", **kwargs):
    """Write to ``path`` atomically via a temporary file and a rename.

    Readers see either the old contents or the new ones, never a
    half-written file — which is what makes this safe for config files
    and caches that another process may read at any moment.

    If the block raises, the temporary file is removed and ``path`` is
    left untouched.

    >>> with atomic_write("out.json") as f:  # doctest: +SKIP
    ...     json.dump(data, f)
    """
    path = os.fspath(path)
    directory = os.path.dirname(os.path.abspath(path))

    if "b" in mode:
        encoding = None

    # Same directory as the target, so the rename stays within one
    # filesystem and is therefore atomic.
    fd, temp_path = tempfile.mkstemp(
        dir=directory, prefix=os.path.basename(path) + ".", suffix=".tmp"
    )

    try:
        with os.fdopen(fd, mode, encoding=encoding, **kwargs) as handle:
            yield handle
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        with contextlib.suppress(OSError):
            os.unlink(temp_path)
        raise

    os.replace(temp_path, path)
