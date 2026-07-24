import itertools

from devutils import unique


def test_preserves_first_occurrence_order():
    assert list(unique([3, 1, 3, 2, 1])) == [3, 1, 2]


def test_no_duplicates_is_identity():
    assert list(unique([1, 2, 3])) == [1, 2, 3]


def test_empty():
    assert list(unique([])) == []


def test_key_function():
    words = ["Apple", "APPLE", "banana", "Banana"]
    assert list(unique(words, key=str.lower)) == ["Apple", "banana"]


def test_unhashable_items_via_key():
    rows = [{"id": 1, "v": "a"}, {"id": 1, "v": "b"}, {"id": 2, "v": "c"}]
    assert list(unique(rows, key=lambda r: r["id"])) == [
        {"id": 1, "v": "a"},
        {"id": 2, "v": "c"},
    ]


def test_is_lazy():
    infinite = itertools.chain([1, 1, 2], itertools.count(3))
    assert list(itertools.islice(unique(infinite), 4)) == [1, 2, 3, 4]


def test_distinguishes_types_that_compare_equal():
    # 1 == True in Python, so a naive set-based dedupe collapses them.
    assert list(unique([1, True, 1.0], key=lambda v: (type(v), v))) == [1, True, 1.0]
