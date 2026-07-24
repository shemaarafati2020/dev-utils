
import pytest

from devutils import atomic_write


def test_writes_file(tmp_path):
    target = tmp_path / "out.txt"
    with atomic_write(target) as f:
        f.write("hello")
    assert target.read_text() == "hello"


def test_overwrites_existing(tmp_path):
    target = tmp_path / "out.txt"
    target.write_text("old")
    with atomic_write(target) as f:
        f.write("new")
    assert target.read_text() == "new"


def test_original_untouched_when_block_raises(tmp_path):
    target = tmp_path / "out.txt"
    target.write_text("old")

    with pytest.raises(ValueError):
        with atomic_write(target) as f:
            f.write("partial")
            raise ValueError("boom")

    assert target.read_text() == "old"


def test_no_file_created_when_block_raises(tmp_path):
    target = tmp_path / "out.txt"

    with pytest.raises(ValueError):
        with atomic_write(target):
            raise ValueError("boom")

    assert not target.exists()


def test_no_temp_files_left_behind(tmp_path):
    target = tmp_path / "out.txt"

    with atomic_write(target) as f:
        f.write("ok")

    with pytest.raises(ValueError):
        with atomic_write(target):
            raise ValueError("boom")

    assert [p.name for p in tmp_path.iterdir()] == ["out.txt"]


def test_target_absent_until_block_exits(tmp_path):
    target = tmp_path / "out.txt"

    with atomic_write(target) as f:
        f.write("hello")
        assert not target.exists()

    assert target.read_text() == "hello"


def test_binary_mode(tmp_path):
    target = tmp_path / "out.bin"
    with atomic_write(target, mode="wb") as f:
        f.write(b"\x00\x01\x02")
    assert target.read_bytes() == b"\x00\x01\x02"


def test_accepts_str_path(tmp_path):
    target = tmp_path / "out.txt"
    with atomic_write(str(target)) as f:
        f.write("hello")
    assert target.read_text() == "hello"


def test_temp_file_is_in_target_directory(tmp_path):
    # The rename can only be atomic if the temp file shares a filesystem
    # with the target, which we approximate by sharing the directory.
    target = tmp_path / "out.txt"
    with atomic_write(target):
        siblings = list(tmp_path.iterdir())
        assert len(siblings) == 1
        assert siblings[0].name.startswith("out.txt.")
        assert siblings[0].name.endswith(".tmp")
