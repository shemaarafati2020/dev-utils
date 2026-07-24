import pytest

from devutils import flatten_dict


def test_flattens_nested_keys():
    nested = {"db": {"host": "localhost", "port": 5432}, "debug": True}
    assert flatten_dict(nested) == {
        "db.host": "localhost",
        "db.port": 5432,
        "debug": True,
    }


def test_deeply_nested():
    assert flatten_dict({"a": {"b": {"c": 1}}}) == {"a.b.c": 1}


def test_custom_separator():
    assert flatten_dict({"a": {"b": 1}}, separator="__") == {"a__b": 1}


def test_prefix():
    assert flatten_dict({"a": 1}, prefix="app") == {"app.a": 1}


def test_empty_dict_value_is_preserved_as_leaf():
    assert flatten_dict({"a": {}, "b": 1}) == {"a": {}, "b": 1}


def test_lists_are_leaves():
    assert flatten_dict({"a": [{"b": 1}]}) == {"a": [{"b": 1}]}


def test_empty_input():
    assert flatten_dict({}) == {}


def test_rejects_separator_collision():
    with pytest.raises(ValueError, match="separator"):
        flatten_dict({"a.b": {"c": 1}})
