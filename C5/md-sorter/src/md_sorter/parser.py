"""parser.py —— 解析单个 Markdown 文件，提取一级标题与正文标签。"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict


# 匹配一级标题：# 标题（行首，最多 3 个空格缩进）
_H1_RE = re.compile(r"^\s{0,3}#\s+(.+?)\s*#*\s*$")
# 匹配行内标签：形如 #课程 或 #AI  （# 后跟 2-15 个非空白、非标点字符）
_TAG_RE = re.compile(r"(?<!\w)#([\u4e00-\u9fa5A-Za-z][\u4e00-\u9fa5A-Za-z0-9_-]{1,14})")


def parse_title_and_tags(path: str | Path) -> Dict[str, object]:
    """读取一个 Markdown 文件，返回 {path, title, tags, size_bytes, line_count}。

    - title: 第一个一级标题的文本；若没有则用文件名（去后缀）。
    - tags: 正文中出现的 #标签 集合（小写去重）。
    - 读取失败（编码错误 / 空文件）时降级处理，不抛异常。
    """
    p = Path(path)
    record: Dict[str, object] = {
        "path": p.as_posix(),
        "title": p.stem,
        "tags": [],
        "size_bytes": p.stat().st_size if p.exists() else 0,
        "line_count": 0,
    }

    try:
        text = p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError, PermissionError) as exc:
        record["title"] = f"{p.stem} (读取失败: {exc.__class__.__name__})"
        return record

    record["line_count"] = text.count("\n") + (1 if text and not text.endswith("\n") else 0)

    for line in text.splitlines():
        m = _H1_RE.match(line)
        if m:
            record["title"] = m.group(1).strip()
            break

    tags: set[str] = set()
    for m in _TAG_RE.finditer(text):
        tag = m.group(1).lower()
        # 排除掉看起来像一级标题前缀的（# 后紧跟空格的已被 H1 正则匹配过，这里不会重复）
        if tag:
            tags.add(tag)
    record["tags"] = sorted(tags)
    return record
