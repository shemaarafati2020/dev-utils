import pytest

from devutils import retry


def test_returns_on_first_success():
    calls = []

    @retry(attempts=3, delay=0)
    def ok():
        calls.append(1)
        return "done"

    assert ok() == "done"
    assert len(calls) == 1


def test_retries_until_success():
    calls = []

    @retry(attempts=3, delay=0)
    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise RuntimeError("not yet")
        return "done"

    assert flaky() == "done"
    assert len(calls) == 3


def test_reraises_last_exception():
    @retry(attempts=2, delay=0)
    def always_fails():
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError, match="boom"):
        always_fails()


def test_only_catches_listed_exceptions():
    calls = []

    @retry(attempts=3, delay=0, exceptions=(ValueError,))
    def wrong_error():
        calls.append(1)
        raise TypeError("unhandled")

    with pytest.raises(TypeError):
        wrong_error()
    assert len(calls) == 1


def test_preserves_metadata():
    @retry(delay=0)
    def documented():
        """Docstring survives."""

    assert documented.__name__ == "documented"
    assert documented.__doc__ == "Docstring survives."


def test_rejects_zero_attempts():
    with pytest.raises(ValueError):
        retry(attempts=0)
