#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
StudyLoop —— 大学生错题 / 知识点间隔重复复习命令行工具（C9 MVP）
作者：阮依涵（郑州西亚斯学院 软件工程）

设计目标：
  把"整理完就再也不看"的高数错题、四级单词、专业课知识点，
  用简化版 SM-2 间隔重复算法，每天只推送到期的卡片，复习完即走。

零第三方依赖，仅用 Python 标准库。数据存为同目录下 data/cards.json。

用法（在 mvp 目录下）：
  python 阮依涵_C9_mvp.py add --front "二重积分交换积分次序的条件" --back "积分区域可拆成 X/Y 型..." --tag 高数
  python 阮依涵_C9_mvp.py due                 # 列出今天到期的卡片
  python 阮依涵_C9_mvp.py review <id> <grade> # grade: again|hard|good|easy
  python 阮依涵_C9_mvp.py stats               # 统计
  python 阮依涵_C9_mvp.py list                # 列出全部卡片

可选：--today YYYY-MM-DD  指定"今天"的日期（用于演示/补卡，默认真实今天）
"""

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "cards.json")

# 评分等级 -> (含义, 间隔天数系数/规则, 易度系数调整)
GRADES = ["again", "hard", "good", "easy"]


def load_db():
    if not os.path.exists(DATA_FILE):
        return {"next_id": 1, "cards": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_db(db):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def parse_today(s):
    if s:
        return datetime.strptime(s, "%Y-%m-%d").date()
    return date.today()


def d2s(d):
    return d.isoformat()


def s2d(s):
    return datetime.strptime(s, "%Y-%m-%d").date()


# ---------- 简化 SM-2 ----------
def schedule(card, grade, today):
    """根据本次评分，更新卡片的间隔 / 易度 / 下次到期日。直接改 card 字典。"""
    ef = card.get("ease", 2.5)
    rep = card.get("reps", 0)          # 连续答对次数
    ivl = card.get("interval", 0)      # 当前间隔（天）

    if grade == "again":
        rep = 0
        ivl = 0                         # 明天再战
        ef = max(1.3, ef - 0.2)
        due = today + timedelta(days=1)
    elif grade == "hard":
        ivl = max(1, round(ivl * 1.2)) if rep > 0 else 1
        ef = max(1.3, ef - 0.15)
        due = today + timedelta(days=ivl)
    elif grade == "easy":
        rep += 1
        ivl = 1 if rep == 1 else (round(ivl * ef * 1.3) if ivl > 0 else 4)
        ef = ef + 0.15
        due = today + timedelta(days=ivl)
    else:  # good
        rep += 1
        if rep == 1:
            ivl = 1
        elif rep == 2:
            ivl = 3
        else:
            ivl = round(ivl * ef)
        due = today + timedelta(days=ivl)

    card["reps"] = rep
    card["interval"] = ivl
    card["ease"] = round(ef, 2)
    card["due"] = d2s(due)
    card["last_review"] = d2s(today)
    card["history"] = card.get("history", [])
    card["history"].append({"date": d2s(today), "grade": grade, "interval": ivl})


# ---------- 命令 ----------
def cmd_add(args):
    db = load_db()
    card = {
        "id": db["next_id"],
        "front": args.front,
        "back": args.back,
        "tag": args.tag or "未分类",
        "created": d2s(parse_today(args.today)),
        "due": d2s(parse_today(args.today)),   # 新卡今天就该看
        "interval": 0,
        "reps": 0,
        "ease": 2.5,
        "history": [],
    }
    db["cards"].append(card)
    db["next_id"] += 1
    save_db(db)
    print(f"[添加成功] 卡片 #{card['id']} 已入库，标签=「{card['tag']}」，今日即可复习。")
    print(f"  正面：{card['front']}")


def cmd_due(args):
    db = load_db()
    today = parse_today(args.today)
    pending = [c for c in db["cards"] if s2d(c["due"]) <= today]
    overdue = [c for c in db["cards"] if s2d(c["due"]) < today]
    print(f"=== 今日待复习（{d2s(today)}）===")
    if not pending:
        print("没有到期卡片。要么今天休息，要么先 add 几张新卡。")
        return
    print(f"共 {len(pending)} 张到期（其中逾期 {len(overdue)} 张）：\n")
    for c in pending:
        flag = "（逾期）" if c in overdue else ""
        print(f"  #{c['id']} [{c['tag']}]  已复习{c['reps']}次  下次间隔{c['interval']}天{flag}")
        print(f"      问：{c['front']}")
    print("\n复习后执行： python 阮依涵_C9_mvp.py review <id> again|hard|good|easy")


def cmd_review(args):
    db = load_db()
    today = parse_today(args.today)
    card = next((c for c in db["cards"] if c["id"] == args.id), None)
    if not card:
        print(f"[错误] 找不到 id={args.id} 的卡片。用 list 查看全部。")
        sys.exit(1)
    if args.grade not in GRADES:
        print(f"[错误] grade 必须是 {GRADES} 之一。")
        sys.exit(1)
    print(f"=== 复习卡片 #{card['id']} ===")
    print(f"问：{card['front']}")
    print(f"答：{card['back']}")
    print(f"你的评分：{args.grade}")
    schedule(card, args.grade, today)
    save_db(db)
    print(f"-> 已记录。下次到期日：{card['due']}（间隔 {card['interval']} 天，连续答对 {card['reps']} 次，易度 {card['ease']}）")


def cmd_stats(args):
    db = load_db()
    today = parse_today(args.today)
    cards = db["cards"]
    if not cards:
        print("还没有卡片。先 add 几张。")
        return
    due_now = [c for c in cards if s2d(c["due"]) <= today]
    tags = {}
    for c in cards:
        tags[c["tag"]] = tags.get(c["tag"], 0) + 1
    total_reviews = sum(len(c.get("history", [])) for c in cards)
    print("=== StudyLoop 统计 ===")
    print(f"卡片总数：{len(cards)}")
    print(f"今日到期：{len(due_now)}")
    print(f"累计复习次数：{total_reviews}")
    print("标签分布：")
    for t, n in tags.items():
        print(f"  - {t}: {n} 张")


def cmd_list(args):
    db = load_db()
    print(f"=== 全部卡片（{len(db['cards'])} 张）===")
    for c in db["cards"]:
        print(f"  #{c['id']} [{c['tag']}] due={c['due']} reps={c['reps']} | {c['front']}")


def main():
    parser = argparse.ArgumentParser(description="StudyLoop 间隔重复复习工具")
    parser.add_argument("--today", help="指定今天日期 YYYY-MM-DD（演示用，默认真实今天）")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="添加一张新卡片")
    p_add.add_argument("--front", required=True, help="问题 / 题干")
    p_add.add_argument("--back", required=True, help="答案 / 解析")
    p_add.add_argument("--tag", help="标签，如 高数 / 四级 / 数据结构")

    p_due = sub.add_parser("due", help="列出今天到期的卡片")
    p_rev = sub.add_parser("review", help="复习一张卡片并评分")
    p_rev.add_argument("id", type=int)
    p_rev.add_argument("grade", choices=GRADES)
    sub.add_parser("stats", help="统计")
    sub.add_parser("list", help="列出全部卡片")

    args = parser.parse_args()
    {"add": cmd_add, "due": cmd_due, "review": cmd_review,
     "stats": cmd_stats, "list": cmd_list}[args.cmd](args)


if __name__ == "__main__":
    main()
