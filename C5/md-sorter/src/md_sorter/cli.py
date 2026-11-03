"""cli.py —— 命令行入口：python -m md_sorter <input_dir> -o <output_dir>。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from . import __version__
from .classifier import classify_by_theme
from .indexer import build_index, write_manifest
from .parser import parse_title_and_tags
from .scanner import scan_markdown_files


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="md-sorter",
        description="扫描目录下的 Markdown 文件，按主题自动分类并生成 INDEX.md + manifest.json。",
    )
    p.add_argument("input_dir", help="要扫描的目录路径")
    p.add_argument(
        "-o",
        "--output-dir",
        default="./md_sorter_output",
        help="输出目录（默认 ./md_sorter_output）",
    )
    p.add_argument("--version", action="version", version=f"md-sorter {__version__}")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    in_dir = Path(args.input_dir).expanduser().resolve()
    out_dir = Path(args.output_dir).expanduser().resolve()

    if not in_dir.exists() or not in_dir.is_dir():
        print(f"[错误] 输入目录不存在或不是目录: {in_dir}", file=sys.stderr)
        return 2

    print(f"[1/3] 扫描 Markdown 文件: {in_dir}")
    files = scan_markdown_files(in_dir)
    print(f"      共发现 {len(files)} 个 .md 文件")

    print("[2/3] 解析标题与标签 ...")
    records = []
    for f in files:
        rec = parse_title_and_tags(f)
        # 把 path 改成相对输入目录的 posix 路径，方便别人 clone 后直接点开
        try:
            rec["path"] = f.relative_to(in_dir).as_posix()
        except ValueError:
            rec["path"] = f.as_posix()
        rec["theme"] = classify_by_theme(rec)
        records.append(rec)

    print("[3/3] 写入索引 ...")
    out_dir.mkdir(parents=True, exist_ok=True)
    index_path = out_dir / "INDEX.md"
    manifest_path = out_dir / "manifest.json"

    index_path.write_text(build_index(records, str(in_dir)), encoding="utf-8")
    write_manifest(records, manifest_path)

    # 统计每个桶的数量
    from collections import Counter

    counter = Counter(r["theme"] for r in records)
    print("")
    print("完成 ✅")
    print(f"  - 索引文件: {index_path}")
    print(f"  - 元数据:   {manifest_path}")
    print("  - 主题分布:")
    for theme, n in counter.most_common():
        print(f"      · {theme}: {n}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
