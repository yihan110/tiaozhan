"""端到端测试：跑一次 CLI，验证产物文件生成。"""

from pathlib import Path

from md_sorter.cli import main


def test_cli_end_to_end(tmp_path: Path) -> None:
    # 准备输入目录
    src = tmp_path / "notes"
    src.mkdir()
    (src / "readme.md").write_text("# AI 学习笔记\n\n用 #Claude 写 prompt。\n", encoding="utf-8")
    (src / "exam.md").write_text("# 四级听力错题整理\n\n总结 #考试 经验。\n", encoding="utf-8")

    out = tmp_path / "out"
    rc = main([str(src), "-o", str(out)])
    assert rc == 0

    assert (out / "INDEX.md").exists()
    assert (out / "manifest.json").exists()

    index_text = (out / "INDEX.md").read_text(encoding="utf-8")
    assert "AI 学习笔记" in index_text
    assert "四级听力错题整理" in index_text
    assert "AI 与工具" in index_text
    assert "作业与考试" in index_text


def test_cli_bad_input_dir(tmp_path: Path) -> None:
    rc = main([str(tmp_path / "no_such"), "-o", str(tmp_path / "out")])
    assert rc == 2
