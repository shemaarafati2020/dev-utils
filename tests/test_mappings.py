from devutils import deep_merge


def test_merges_nested_keys():
    base = {"a": {"x": 1, "y": 2}, "b": 3}
    assert deep_merge(base, {"a": {"y": 99}}) == {"a": {"x": 1, "y": 99}, "b": 3}


def test_adds_missing_keys():
    assert deep_merge({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}


def test_scalar_replaces_dict():
    assert deep_merge({"a": {"x": 1}}, {"a": "replaced"}) == {"a": "replaced"}


def test_dict_replaces_scalar():
    assert deep_merge({"a": 1}, {"a": {"x": 2}}) == {"a": {"x": 2}}


def test_lists_are_replaced_not_concatenated():
    assert deep_merge({"a": [1, 2]}, {"a": [3]}) == {"a": [3]}


def test_inputs_are_not_mutated():
    base = {"a": {"x": 1}}
    override = {"a": {"y": 2}}
    deep_merge(base, override)
    assert base == {"a": {"x": 1}}
    assert override == {"a": {"y": 2}}


def test_result_does_not_alias_input():
    base = {"a": {"x": [1]}}
    result = deep_merge(base, {})
    result["a"]["x"].append(2)
    assert base["a"]["x"] == [1]


def test_empty_override_returns_equal_copy():
    assert deep_merge({"a": 1}, {}) == {"a": 1}
