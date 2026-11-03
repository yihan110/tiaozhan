"""indexer.py —— 把解析后的记录聚合成 INDEX.md 与 manifest.json。"""

from __future__ import annotations

import json
from collections import OrderedDict, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List


def build_index(records: List[Dict[str, object]], source_root: str) -> str:
    """根据 records 生成 Markdown 索引文本。

    输出结构：
        # Markdown 笔记索引
        扫描目录: <source_root>
        共 N 篇
        ## 主题桶 A
        - [标题](相对路径)  —— 标签: #x #y
        ## 主题桶 B
        ...
    """
    buckets: "OrderedDict[str, List[Dict[str, object]]]" = OrderedDict()
    # 保持 THEME_RULES 的顺序，未命中的「其他」放最后
    from .classifier import DEFAULT_BUCKET, THEME_RULES

    for bucket, _ in THEME_RULES:
        buckets[bucket] = []
    buckets[DEFAULT_BUCKET] = []

    for rec in records:
        bucket = str(rec.get("theme", DEFAULT_BUCKET))
        buckets.setdefault(bucket, []).append(rec)

    lines: List[str] = []
    lines.append("# Markdown 笔记索引")
    lines.append("")
    lines.append(f"- 扫描目录: `{source_root}`")
    lines.append(f"- 共收录 **{len(records)}** 篇 Markdown 文件")
    lines.append("")

    for bucket, items in buckets.items():
        if not items:
            continue
        lines.append(f"## {bucket}（{len(items)}）")
        lines.append("")
        for rec in sorted(items, key=lambda r: str(r.get("path", ""))):
            title = str(rec.get("title", "untitled"))
            rel = str(rec.get("path", ""))
            tags = rec.get("tags", []) or []
            tag_str = " ".join(f"#{t}" for t in tags) if tags else ""
            row = f"- [{title}]({rel})"
            if tag_str:
                row += f"  —— {tag_str}"
            lines.append(row)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_manifest(records: List[Dict[str, object]], out_path: str | Path) -> Path:
    """把 records 写成 UTF-8 JSON（带缩进，便于人读）。"""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "count": len(records),
        "files": records,
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return out
