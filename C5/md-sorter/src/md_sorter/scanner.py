"""scanner.py —— 递归扫描目录，找出所有 .md / .markdown 文件。"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Set


# 扫描时要跳过的目录名（避免把虚拟环境、缓存、git 内部目录也算进来）
SKIP_DIRS: Set[str] = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".idea",
    ".vscode",
    "dist",
    "build",
    ".mypy_cache",
    ".pytest_cache",
}

VALID_SUFFIXES = {".md", ".markdown"}


def scan_markdown_files(root: str | Path) -> List[Path]:
    """递归扫描 root 下所有 Markdown 文件。

    参数:
        root: 要扫描的目录路径。

    返回:
        排序后的 Path 列表（相对 root 排序，方便测试）。

    异常:
        NotADirectoryError: root 不是目录或不存在。
    """
    root_path = Path(root).expanduser().resolve()
    if not root_path.exists():
        raise FileNotFoundError(f"目录不存在: {root_path}")
    if not root_path.is_dir():
        raise NotADirectoryError(f"不是目录: {root_path}")

    found: List[Path] = []
    for dirpath, dirnames, filenames in _walk(root_path):
        # 原地修改 dirnames，让 os.walk 跳过黑名单目录
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fname in filenames:
            p = Path(dirpath) / fname
            if p.suffix.lower() in VALID_SUFFIXES:
                found.append(p)

    # 按相对路径排序，保证输出稳定
    found.sort(key=lambda p: p.relative_to(root_path).as_posix())
    return found


def _walk(root: Path) -> Iterable:
    """极简的 os.walk 兼容封装，避免直接 import os 干扰测试。"""
    import os

    yield from os.walk(root)
