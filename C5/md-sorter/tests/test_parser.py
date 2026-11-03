"""测试 parser.parse_title_and_tags。"""

from pathlib import Path

from md_sorter.parser import parse_title_and_tags


def test_parse_extracts_h1(tmp_path: Path) -> None:
    p = tmp_path / "x.md"
    p.write_text("# 高数第二章 极限\n\n正文内容...\n", encoding="utf-8")
    rec = parse_title_and_tags(p)
    assert rec["title"] == "高数第二章 极限"


def test_parse_fallback_to_stem_when_no_h1(tmp_path: Path) -> None:
    p = tmp_path / "mynote.md"
    p.write_text("纯正文，没有一级标题。\n", encoding="utf-8")
    rec = parse_title_and_tags(p)
    assert rec["title"] == "mynote"


def test_parse_extracts_inline_tags(tmp_path: Path) -> None:
    p = tmp_path / "y.md"
    p.write_text("# 读书笔记\n\n这是 #AI 和 #Prompt 的一点感想。\n", encoding="utf-8")
    rec = parse_title_and_tags(p)
    assert "ai" in rec["tags"]
    assert "prompt" in rec["tags"]


def test_parse_handles_garbage_file(tmp_path: Path) -> None:
    p = tmp_path / "bad.md"
    # 写入非法 UTF-8 字节
    p.write_bytes(b"\xff\xfe\x00bad bytes \x81")
    rec = parse_title_and_tags(p)
    # 不抛异常，title 降级
    assert "读取失败" in rec["title"]
