from devutils import partition


def test_splits_by_predicate():
    matching, rest = partition(lambda n: n % 2 == 0, range(6))
    assert matching == [0, 2, 4]
    assert rest == [1, 3, 5]


def test_preserves_order_within_each_side():
    matching, rest = partition(lambda c: c.isupper(), "aBcDeF")
    assert matching == ["B", "D", "F"]
    assert rest == ["a", "c", "e"]


def test_all_matching():
    matching, rest = partition(bool, [1, 2, 3])
    assert matching == [1, 2, 3]
    assert rest == []


def test_none_matching():
    matching, rest = partition(bool, [0, "", None])
    assert matching == []
    assert rest == [0, "", None]


def test_empty():
    assert partition(bool, []) == ([], [])


def test_consumes_generator_once():
    calls = []

    def counting():
        for n in range(4):
            calls.append(n)
            yield n

    matching, rest = partition(lambda n: n > 1, counting())
    assert matching == [2, 3]
    assert rest == [0, 1]
    assert calls == [0, 1, 2, 3]


def test_predicate_called_once_per_item():
    calls = []

    def predicate(n):
        calls.append(n)
        return n % 2 == 0

    partition(predicate, range(4))
    assert calls == [0, 1, 2, 3]
