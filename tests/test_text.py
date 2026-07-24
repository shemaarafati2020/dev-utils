import pytest

from devutils import slugify


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("Hello, World!", "hello-world"),
        ("Héllo   Wörld", "hello-world"),
        ("  leading and trailing  ", "leading-and-trailing"),
        ("already-slugged", "already-slugged"),
        ("multiple---hyphens", "multiple-hyphens"),
        ("", ""),
    ],
)
def test_slugify(raw, expected):
    assert slugify(raw) == expected


def test_custom_separator():
    assert slugify("Hello World", separator="_") == "hello_world"


def test_max_length_does_not_end_in_separator():
    assert slugify("one two three", max_length=8) == "one-two"
