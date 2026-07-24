import pytest

from devutils import parse_bool


@pytest.mark.parametrize("raw", ["1", "true", "True", "TRUE", "t", "yes", "Y", "on", " on "])
def test_truthy(raw):
    assert parse_bool(raw) is True


@pytest.mark.parametrize("raw", ["0", "false", "False", "f", "no", "N", "off", "", "  "])
def test_falsy(raw):
    assert parse_bool(raw) is False


def test_the_string_false_is_not_truthy():
    # bool("false") is True — the whole reason this helper exists.
    assert parse_bool("false") is False


def test_none_is_false():
    assert parse_bool(None) is False


def test_actual_bools_pass_through():
    assert parse_bool(True) is True
    assert parse_bool(False) is False


def test_unrecognised_raises():
    with pytest.raises(ValueError):
        parse_bool("maybe")


def test_default_used_for_unrecognised():
    assert parse_bool("maybe", default=True) is True
    assert parse_bool("maybe", default=False) is False


def test_default_none_is_returned_not_treated_as_missing():
    assert parse_bool("maybe", default=None) is None
