"""测试 scanner.scan_markdown_files。"""

from pathlib import Path

import pytest

from md_sorter.scanner import scan_markdown_files


def test_scan_finds_md_files(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("# A\n", encoding="utf-8")
    (tmp_path / "b.markdown").write_text("# B\n", encoding="utf-8")
    (tmp_path / "c.txt").write_text("ignore me\n", encoding="utf-8")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "c.md").write_text("# C\n", encoding="utf-8")

    found = scan_markdown_files(tmp_path)
    names = sorted(p.name for p in found)
    assert names == ["a.md", "b.markdown", "c.md"]


def test_scan_skips_hidden_and_venv(tmp_path: Path) -> None:
    (tmp_path / "real.md").write_text("# real\n", encoding="utf-8")
    venv = tmp_path / ".venv"
    venv.mkdir()
    (venv / "should_be_skipped.md").write_text("# skip\n", encoding="utf-8")
    hidden = tmp_path / ".hidden_dir"
    hidden.mkdir()
    (hidden / "also_skip.md").write_text("# skip\n", encoding="utf-8")

    found = scan_markdown_files(tmp_path)
    assert [p.name for p in found] == ["real.md"]


def test_scan_missing_dir_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        scan_markdown_files(tmp_path / "no_such_dir")
