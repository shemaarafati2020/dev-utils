import pytest

from devutils import group_by


def test_groups_by_key():
    assert group_by(len, ["a", "bb", "cc", "d"]) == {1: ["a", "d"], 2: ["bb", "cc"]}


def test_preserves_order_within_groups():
    rows = [
        {"team": "a", "n": 1},
        {"team": "b", "n": 2},
        {"team": "a", "n": 3},
    ]
    grouped = group_by(lambda r: r["team"], rows)
    assert [r["n"] for r in grouped["a"]] == [1, 3]


def test_unlike_itertools_groupby_does_not_need_sorted_input():
    # itertools.groupby would produce three groups here, not two.
    assert group_by(len, ["a", "bb", "c"]) == {1: ["a", "c"], 2: ["bb"]}


def test_empty_input():
    assert group_by(len, []) == {}


def test_returns_plain_dict():
    grouped = group_by(len, ["a"])
    assert type(grouped) is dict
    with pytest.raises(KeyError):
        grouped[99]


def test_works_on_generators():
    assert group_by(lambda n: n % 2, (n for n in range(4))) == {0: [0, 2], 1: [1, 3]}


def test_transform_applied_to_values():
    rows = [{"team": "a", "n": 1}, {"team": "a", "n": 2}]
    assert group_by(lambda r: r["team"], rows, transform=lambda r: r["n"]) == {"a": [1, 2]}


def test_unhashable_key_raises():
    with pytest.raises(TypeError):
        group_by(lambda n: [n], [1, 2])
