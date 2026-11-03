"""classifier.py —— 根据标题与标签，把一篇 Markdown 归入某个主题桶。

主题桶是硬编码的小集合，覆盖软件工程学生常见的笔记场景；
匹配不到的统一归入「其他 / Uncategorized」。

判定顺序：
  1. 先把所有 tags 在所有桶的关键词里扫一遍 —— 标签命中优先；
  2. 再把 title 在所有桶的关键词里扫一遍 —— 标题兜底；
  3. 都没命中 → 默认桶。
桶的顺序即 THEME_RULES 顺序，作为同优先级下的先后依据。
"""

from __future__ import annotations

from typing import Dict, Iterable, Tuple


# (桶名, 命中关键词列表) —— 按顺序匹配，先命中先归
THEME_RULES: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("课程笔记", ("课程", "上课", "lecture", "note", "笔记", "高数", "数学", "操作系统", "数据结构", "算法", "数据库", "计算机")),
    ("作业与考试", ("作业", "assignment", "考试", "exam", "四级", "六级", "期末", "期中", "测验", "错题")),
    ("AI 与工具", ("ai", "claude", "gpt", "chatgpt", "prompt", "skill", "智能体", "agent", "豆包", "copilot")),
    ("项目与代码", ("项目", "project", "repo", "github", "代码", "code", "python", "java", "前端", "后端", "debug", "调试")),
    ("活动与实践", ("活动", "三下乡", "社团", "志愿", "比赛", "竞赛", "实习", "实践", "团建")),
    ("生活与心情", ("日记", "心情", "生活", "随笔", "感想", "吐槽", "emo")),
    ("读书笔记", ("读书", "书", "小说", "阅读", "读后感")),
)

DEFAULT_BUCKET = "其他 / Uncategorized"


def classify_by_theme(record: Dict[str, Iterable[str] | str]) -> str:
    """根据 record 中的 title 和 tags 返回主题桶名。

    判定优先级：tags 命中 > title 命中。
    """
    title = str(record.get("title", "")).lower()
    tags = [t.lower() for t in record.get("tags", [])]  # type: ignore[union-attr]

    # 第一轮：tags 命中
    for bucket, keywords in THEME_RULES:
        for kw in keywords:
            kw_l = kw.lower()
            if any(kw_l == t or kw_l in t for t in tags):
                return bucket

    # 第二轮：title 命中
    for bucket, keywords in THEME_RULES:
        for kw in keywords:
            if kw.lower() in title:
                return bucket

    return DEFAULT_BUCKET
