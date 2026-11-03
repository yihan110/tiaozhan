"""测试 classifier.classify_by_theme。"""

from md_sorter.classifier import DEFAULT_BUCKET, classify_by_theme


def test_classify_ai_tag() -> None:
    rec = {"title": "随便写点", "tags": ["claude", "prompt"]}
    assert classify_by_theme(rec) == "AI 与工具"


def test_classify_course_by_title() -> None:
    rec = {"title": "数据结构第三章 树与图", "tags": []}
    assert classify_by_theme(rec) == "课程笔记"


def test_classify_default_bucket() -> None:
    rec = {"title": "随便一篇", "tags": []}
    assert classify_by_theme(rec) == DEFAULT_BUCKET


def test_classify_tag_overrides_title() -> None:
    # 标题像课程，但打了 AI 标签 —— 应优先归 AI
    rec = {"title": "操作系统课笔记", "tags": ["ai"]}
    assert classify_by_theme(rec) == "AI 与工具"
