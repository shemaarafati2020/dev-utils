import pytest

from devutils import truncate


def test_short_text_untouched():
    assert truncate("hello", 10) == "hello"


def test_exact_length_untouched():
    assert truncate("hello", 5) == "hello"


def test_truncates_with_ellipsis():
    assert truncate("hello world", 8) == "hello…"


def test_result_never_exceeds_length():
    text = "the quick brown fox jumps"
    for limit in range(2, len(text) + 5):
        assert len(truncate(text, limit)) <= limit


def test_custom_suffix():
    assert truncate("hello world", 9, suffix="...") == "hello..."


def test_whole_words_false_cuts_mid_word():
    assert truncate("hello world", 8, whole_words=False) == "hello w…"


def test_falls_back_to_hard_cut_when_no_space_fits():
    assert truncate("supercalifragilistic", 10) == "supercali…"


def test_suffix_longer_than_limit_raises():
    with pytest.raises(ValueError):
        truncate("hello world", 2, suffix="......")


def test_empty_text():
    assert truncate("", 5) == ""
