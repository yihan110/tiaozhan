"""md_sorter —— 扫描目录下的 Markdown 文件，自动按主题分类并生成索引。

Public API:
    scan_markdown_files(root) -> list[Path]
    parse_title_and_tags(path) -> dict
    classify_by_theme(record) -> str
    build_index(records) -> str
    write_manifest(records, out_path) -> None
"""

__version__ = "0.1.0"
__all__ = [
    "scan_markdown_files",
    "parse_title_and_tags",
    "classify_by_theme",
    "build_index",
    "write_manifest",
]

from .scanner import scan_markdown_files
from .parser import parse_title_and_tags
from .classifier import classify_by_theme
from .indexer import build_index, write_manifest
