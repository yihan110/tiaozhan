# -*- coding: utf-8 -*-
"""
AI 调用层。

设计原则：
1. 真实模式：调用 OpenAI 兼容接口（/chat/completions），Key 从环境变量或请求头传入。
2. 演示模式（无 Key 时自动启用）：使用本地规则引擎做真实的文本分析，
   包括字数统计、句子切分、关键词抽取、结构识别、维度打分、针对性建议。
   —— 这不是「假装 AI」，而是一个诚实的、可复算的本地分析器；
      输出里会明确标注 ai_mode = "mock"。
"""
from __future__ import annotations

import re
import json
from typing import Dict, Any, List

import requests

from config import Config


# ---------- 模式元数据 ----------
MODES: Dict[str, Dict[str, str]] = {
    "resume": {
        "label": "简历 / 经历优化",
        "hint": "粘贴一段简历经历、项目描述或自我介绍，AI 会帮你量化问题并给出改写方向。",
    },
    "essay": {
        "label": "文书 / 自我介绍润色",
        "hint": "粘贴申请书、自荐信、课程论文段落等，AI 会评估结构、语气与说服力。",
    },
    "comp": {
        "label": "竞赛材料整理",
        "hint": "粘贴散乱的竞赛草稿、活动记录，AI 会帮你抽出关键信息并重组为结构化要点。",
    },
    "summary": {
        "label": "长文档摘要",
        "hint": "粘贴一段较长的文字（实验报告、会议记录、文章节选），AI 会压缩为要点摘要。",
    },
}


# ============================================================
# 本地规则引擎（演示模式）—— 真实、可复算
# ============================================================

_STOPWORDS = set(
    "的 了 和 是 在 我 你 他 她 它 我们 你们 他们 这 那 就 都 而 及 与 或 "
    "一个 没有 我们 自己 可以 这是 就是 还是 但是 因为 所以 如果 虽然 "
    "the a an of to in and or is are was were for on with".split()
)


def _split_sentences(text: str) -> List[str]:
    parts = re.split(r"(?<=[。！？!?；;\n])", text)
    return [p.strip() for p in parts if p.strip()]


def _extract_keywords(text: str, topk: int = 8) -> List[str]:
    # 中文 2-4 字连续片段 + 英文单词
    tokens = re.findall(r"[一-龥]{2,4}|[A-Za-z][A-Za-z0-9+#.\-]{1,}", text)
    freq: Dict[str, int] = {}
    for t in tokens:
        if t.lower() in _STOPWORDS or t in _STOPWORDS:
            continue
        if len(t) < 2:
            continue
        freq[t] = freq.get(t, 0) + 1
    ranked = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    # 去重包含关系：保留更长的
    out: List[str] = []
    for w, c in ranked:
        if c < 1:
            continue
        if any(w in o or o in w for o in out):
            continue
        out.append(w)
        if len(out) >= topk:
            break
    return out


def _detect_structure(text: str) -> Dict[str, int]:
    return {
        "lines": len([l for l in text.splitlines() if l.strip()]),
        "has_bullets": len(re.findall(r"^\s*([-*•]|\d+[.、)])", text, re.M)) > 0,
        "has_paragraphs": len([p for p in text.split("\n\n") if p.strip()]) >= 3,
    }


def _score_text(text: str, mode: str) -> Dict[str, int]:
    n = len(text)
    sents = _split_sentences(text)
    struct = _detect_structure(text)

    # 维度打分（0-100），规则透明
    length_score = 100 if 80 <= n <= 1200 else (60 if n >= 40 else 30)
    structure_score = 80 if struct["has_bullets"] or struct["has_paragraphs"] else 45
    density = n / max(len(sents), 1)
    conciseness = 100 if 15 <= density <= 60 else 60 if density < 120 else 35
    action_words = len(re.findall(r"完成|实现|主导|负责|优化|提升|设计|搭建|撰写|组织|推动|获得|发明", text))
    action_score = min(100, 40 + action_words * 15)

    overall = int(round(length_score * 0.25 + structure_score * 0.25 +
                        conciseness * 0.2 + action_score * 0.3))
    return {
        "overall": overall,
        "length": length_score,
        "structure": structure_score,
        "conciseness": conciseness,
        "actionability": action_score,
    }


def _mock_analyze(text: str, mode: str) -> Dict[str, Any]:
    label = MODES.get(mode, MODES["resume"])["label"]
    sents = _split_sentences(text)
    kws = _extract_keywords(text)
    struct = _detect_structure(text)
    scores = _score_text(text, mode)

    # 统计
    stats = {
        "字符数": len(text),
        "句子数": len(sents),
        "行数": struct["lines"],
        "关键词": "、".join(kws) if kws else "（未抽取到明显关键词）",
    }

    # 针对性建议
    suggestions: List[str] = []
    if len(text) < 40:
        suggestions.append("内容过短：建议至少补到 80 字以上，AI 才能给出有意义的判断。")
    if len(text) > 1500:
        suggestions.append("内容偏长：建议分段，每段聚焦一个要点。")
    if not struct["has_bullets"] and mode in ("resume", "comp"):
        suggestions.append("缺少要点列表：用「-」或「1.」把经历拆成 3-5 条，每条一行。")
    action_words = len(re.findall(r"完成|实现|主导|负责|优化|提升|设计|搭建", text))
    if action_words == 0 and mode in ("resume", "comp"):
        suggestions.append("缺少动词开头：把每句话改成「动词 + 做了什么 + 结果数据」的句式。")
    if len(re.findall(r"\d", text)) == 0 and mode in ("resume", "comp"):
        suggestions.append("缺少量化数据：补一个数字（用户量、效率提升 %、排名、获奖等级）。")
    if len(sents) > 0 and sum(len(s) for s in sents) / len(sents) > 80:
        suggestions.append("句子偏长：把超过 60 字的长句拆成两句，更易读。")
    if mode == "essay" and not struct["has_paragraphs"]:
        suggestions.append("缺少分段：建议按「开头-论点-例子-结尾」分 4 段。")
    if mode == "summary" and len(text) < 100:
        suggestions.append("待摘要的原文较短：摘要价值有限，建议粘贴更长的段落。")
    if not suggestions:
        suggestions.append("结构与长度基本合理：下一步可让真实 AI 模型做语气润色和表达升级。")

    # 结构化结果（按模式给不同的 section）
    if mode == "summary":
        summary_sents = sents[:3] if len(sents) >= 3 else sents
        sections = [
            {"title": "一句话摘要", "content": "；".join(summary_sents[:1]) if summary_sents else "（空）"},
            {"title": "关键要点", "content": "\n".join(f"- {s}" for s in summary_sents[1:4]) or "（句子不足，无法拆要点）"},
            {"title": "核心关键词", "content": "、".join(kws) if kws else "（无）"},
        ]
    else:
        sections = [
            {"title": "维度打分", "content":
                f"综合分 {scores['overall']}/100\n"
                f"· 长度合适度：{scores['length']}\n"
                f"· 结构清晰度：{scores['structure']}\n"
                f"· 简洁度：{scores['conciseness']}\n"
                f"· 行动/数据密度：{scores['actionability']}"},
            {"title": "你写的内容里最突出的关键词",
             "content": "、".join(kws) if kws else "（未抽取到）"},
            {"title": "改写方向建议",
             "content": "\n".join(f"- {s}" for s in suggestions[:4])},
        ]

    return {
        "mode": mode,
        "mode_label": label,
        "ai_mode": "mock",
        "ai_mode_note": "本地规则引擎演示模式（未调用外部 AI）。配置 OPENAI_API_KEY 后切换为真实大模型分析。",
        "scores": scores,
        "stats": stats,
        "sections": sections,
        "suggestions": suggestions,
    }


# ============================================================
# 真实 AI 调用（OpenAI 兼容）
# ============================================================

_SYSTEM_PROMPTS = {
    "resume": "你是资深校招面试官和简历优化教练。请以中文输出，结构为：1) 综合打分(0-100)与各维度；2) 最突出的关键词；3) 3-5 条具体改写建议（动词开头+数据化）；4) 一段改写示范。",
    "essay": "你是中文文书写作教练。请以中文输出：1) 综合打分；2) 结构/语气/说服力诊断；3) 3-5 条修改建议；4) 一段润色示范。",
    "comp": "你是大学生竞赛项目教练。请把用户散乱的竞赛材料整理为：1) 项目一句话定位；2) 3-5 条结构化要点（背景-动作-结果）；3) 还缺什么信息。",
    "summary": "你是文档摘要助手。请把用户输入压缩为：1) 一句话摘要；2) 3-5 条关键要点；3) 核心关键词。",
}


def _real_analyze(text: str, mode: str, api_key: str = "") -> Dict[str, Any]:
    key = api_key or Config.OPENAI_API_KEY
    if not key:
        raise RuntimeError("未配置 OPENAI_API_KEY")

    system = _SYSTEM_PROMPTS.get(mode, _SYSTEM_PROMPTS["resume"])
    payload = {
        "model": Config.OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": f"用户输入（{MODES.get(mode, MODES['resume'])['label']}）：\n\n{text}"},
        ],
        "temperature": 0.4,
    }
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    url = Config.OPENAI_BASE_URL.rstrip("/") + "/chat/completions"
    r = requests.post(url, headers=headers, json=payload, timeout=Config.OPENAI_TIMEOUT)
    r.raise_for_status()
    data = r.json()
    content = data["choices"][0]["message"]["content"]

    # 本地仍然做一份统计，便于前端展示
    kws = _extract_keywords(text)
    return {
        "mode": mode,
        "mode_label": MODES.get(mode, MODES["resume"])["label"],
        "ai_mode": "real",
        "ai_mode_note": f"由 {Config.OPENAI_MODEL}（{Config.OPENAI_BASE_URL}）生成。",
        "scores": _score_text(text, mode),
        "stats": {"字符数": len(text), "句子数": len(_split_sentences(text)),
                  "关键词": "、".join(kws) if kws else "（无）"},
        "sections": [{"title": "AI 分析结果", "content": content}],
        "suggestions": [],
    }


# ============================================================
# 对外统一入口
# ============================================================

def analyze(text: str, mode: str, api_key: str = "") -> Dict[str, Any]:
    text = (text or "").strip()
    if not text:
        return {"error": "请先输入要分析的内容。"}
    if len(text) > 8000:
        return {"error": "内容过长（上限 8000 字），请分段处理。"}

    use_real = bool(api_key) or Config.has_real_ai()
    try:
        if use_real:
            return _real_analyze(text, mode, api_key=api_key)
        return _mock_analyze(text, mode)
    except requests.RequestException as e:
        return {"error": f"调用 AI 接口失败：{e}。请检查 Base URL / Key / 网络。"}
    except Exception as e:  # noqa
        return {"error": f"分析失败：{e}"}
