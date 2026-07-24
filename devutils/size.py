"""Byte-size formatting helpers."""

_BINARY_UNITS = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB")
_DECIMAL_UNITS = ("B", "kB", "MB", "GB", "TB", "PB", "EB")


def humanize_bytes(size, binary=True, precision=1):
    """Format ``size`` bytes as a human-readable string.

    >>> humanize_bytes(1536)
    '1.5 KiB'
    >>> humanize_bytes(1500, binary=False)
    '1.5 kB'
    """
    if size < 0:
        raise ValueError("size must be non-negative")

    base = 1024 if binary else 1000
    units = _BINARY_UNITS if binary else _DECIMAL_UNITS

    value = float(size)
    for unit in units:
        if value < base or unit == units[-1]:
            if unit == "B":
                return "%d B" % int(value)
            return "%.*f %s" % (precision, value, unit)
        value /= base
