# -*- coding: utf-8 -*-
"""
build_data.py
=============
C6A 提交数据仪表盘 - 数据生成脚本（Level 1）

作用：
    把"散落的提交记录"整理成结构化 JSON + CSV。
    当前为演示用的【模拟数据】，真实使用时把 generate_mock_records()
    替换成 scan_submission_folder() 即可（见教学说明.md）。

用法：
    python build_data.py                     # 默认输出到 ../data/
    python build_data.py --outdir <DIR>     # 自定义输出目录
    python build_data.py --seed 42          # 固定随机种子（可复现）

输出：
    submissions.json   全量提交记录（含文件清单、状态、缺失项）
    submissions.csv    扁平化表格（一行一条提交）
    challenges.json    挑战元数据（编号、标题、必填文件）
"""

import argparse
import csv
import json
import os
import random
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# 1. 挑战元数据（可复用：新增挑战只改这里）
# ---------------------------------------------------------------------------
CHALLENGES = [
    {"id": "C1A",  "title": "AI 工具上手与 Prompt 基础", "required_files": ["方案设计.md", "AI日志.md", "拿来说明.md"]},
    {"id": "C2A",  "title": "个人方案设计 Proposal",   "required_files": ["proposal.md", "AI日志.md", "拿来说明.md"]},
    {"id": "C3A",  "title": "技能包 Skill 开发",        "required_files": ["skill.md", "验证报告.md", "AI日志.md"]},
    {"id": "C4A",  "title": "C4A 评审技能",            "required_files": ["评审报告.md", "AI日志.md", "拿来说明.md"]},
    {"id": "C4B",  "title": "文章写作与排版",           "required_files": ["article.html", "AI日志.md"]},
    {"id": "C4C",  "title": "作业自动求解与排版",       "required_files": ["skill.md", "output.pdf", "验证报告.md", "AI日志.md"]},
    {"id": "C4D",  "title": "数据可视化作品",           "required_files": ["dashboard.html", "AI日志.md", "拿来说明.md"]},
    {"id": "C5A",  "title": "项目复盘与 AAR",           "required_files": ["AAR.md", "AI日志.md"]},
    {"id": "C6A",  "title": "提交数据仪表盘",           "required_files": ["report.xlsx", "dashboard/", "AI日志.md", "拿来说明.md"]},
]

# ---------------------------------------------------------------------------
# 2. 学生名单（模拟）
# ---------------------------------------------------------------------------
STUDENTS = [
    {"name": "阮依涵", "pinyin": "ruanyihan", "major": "软件工程",   "github": "ruanyihan-sias"},
    {"name": "李思远", "pinyin": "lisiyuan",   "major": "计算机科学", "github": "lsiyuan-2026"},
    {"name": "张雨晴", "pinyin": "zhangyuqing","major": "软件工程",   "github": "yqzhang-ai"},
    {"name": "陈浩然", "pinyin": "chenhaoran", "major": "数据科学",   "github": "hrchen-ds"},
    {"name": "刘思彤", "pinyin": "liusitong",  "major": "软件工程",   "github": "sitonliu"},
    {"name": "杨子墨", "pinyin": "yangzimo",   "major": "人工智能",   "github": "zimo-yang"},
    {"name": "赵欣怡", "pinyin": "zhaoxinyi",  "major": "计算机科学", "github": "xinyi-zhao"},
    {"name": "周泽宇", "pinyin": "zhouzeyu",   "major": "软件工程",   "github": "zeyu-zhou"},
    {"name": "吴佳琪", "pinyin": "wu jiaqi",   "major": "数据科学",   "github": "jqwu-ds"},
    {"name": "郑博文", "pinyin": "zhengbowen", "major": "人工智能",   "github": "bwzheng-ai"},
    {"name": "孙一诺", "pinyin": "sunyinuo",  "major": "软件工程",   "github": "yinuo-sun"},
    {"name": "马晨曦", "pinyin": "machenxi",   "major": "计算机科学", "github": "chenxi-ma"},
]

# ---------------------------------------------------------------------------
# 3. 生成模拟提交记录
# ---------------------------------------------------------------------------
def generate_mock_records(seed=42):
    random.seed(seed)
    base_date = datetime(2026, 9, 1, 9, 0, 0)
    records = []

    for stu in STUDENTS:
        # 每个学生覆盖 6~9 个挑战，故意留 0~3 个未提交
        chosen = random.sample(CHALLENGES, k=random.randint(6, 9))
        for ch in chosen:
            # 提交时间：基础日期 + 随机偏移
            days_offset = random.randint(0, 60)
            hour = random.randint(9, 22)
            minute = random.randint(0, 59)
            submitted_at = (base_date + timedelta(days=days_offset, hours=hour-9, minutes=minute)).isoformat(timespec="seconds") + "+08:00"

            # 决定该条记录的状态：complete / partial / missing
            roll = random.random()
            if roll < 0.55:
                status = "complete"
            elif roll < 0.85:
                status = "partial"
            else:
                status = "missing"

            files = []
            missing = []
            for req in ch["required_files"]:
                # complete 全部 present；partial 缺 1~2 个；missing 全缺
                if status == "complete":
                    present = True
                elif status == "partial":
                    present = random.random() > 0.4  # 约 60% 概率 present
                else:
                    present = False
                files.append({
                    "filename": f"{stu['pinyin']}_{ch['id']}_{req}",
                    "category": req.replace(".md", "").replace(".xlsx", "").replace(".html", "").replace(".pdf", "").replace("/", ""),
                    "required": True,
                    "present": present,
                })
                if not present:
                    missing.append(req)

            present_count = sum(1 for f in files if f["present"])
            completeness = round(present_count / len(files), 2) if files else 0.0

            records.append({
                "student": stu,
                "challenge": ch["id"],
                "challenge_title": ch["title"],
                "submitted_at": submitted_at,
                "files": files,
                "status": status,
                "completeness": completeness,
                "missing": missing,
                "level_achieved": random.choice([1, 2, 2, 3, 3, 3, 4]) if status != "missing" else 0,
                "notes": "；".join([f"缺失：{m}" for m in missing]) if missing else "文件齐全",
            })

    return records


# ---------------------------------------------------------------------------
# 4. 输出
# ---------------------------------------------------------------------------
def write_outputs(records, outdir):
    os.makedirs(outdir, exist_ok=True)

    # JSON
    json_path = os.path.join(outdir, "submissions.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "is_mock_data": True,
            "note": "本数据为模拟数据，脚本与流程可一键复用真实数据（见教学说明.md）",
            "challenges": CHALLENGES,
            "records": records,
        }, f, ensure_ascii=False, indent=2)

    # CSV（扁平化）
    csv_path = os.path.join(outdir, "submissions.csv")
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["学生", "拼音", "专业", "GitHub", "挑战编号", "挑战标题",
                         "提交时间", "状态", "完成度", "缺失项", "达到Level", "备注"])
        for r in records:
            writer.writerow([
                r["student"]["name"], r["student"]["pinyin"], r["student"]["major"], r["student"]["github"],
                r["challenge"], r["challenge_title"], r["submitted_at"],
                r["status"], r["completeness"], "|".join(r["missing"]),
                r["level_achieved"], r["notes"],
            ])

    # challenges.json
    ch_path = os.path.join(outdir, "challenges.json")
    with open(ch_path, "w", encoding="utf-8") as f:
        json.dump(CHALLENGES, f, ensure_ascii=False, indent=2)

    return json_path, csv_path, ch_path


def main():
    parser = argparse.ArgumentParser(description="C6A 提交数据生成脚本")
    parser.add_argument("--outdir", default=os.path.join(os.path.dirname(__file__), "..", "data"),
                        help="输出目录（默认 ../data）")
    parser.add_argument("--seed", type=int, default=42, help="随机种子（可复现）")
    args = parser.parse_args()

    outdir = os.path.abspath(args.outdir)
    records = generate_mock_records(seed=args.seed)
    j, c, ch = write_outputs(records, outdir)

    # 终端输出（用于截图证据）
    print("=" * 60)
    print("C6A 数据生成脚本运行完成")
    print("=" * 60)
    print(f"输出目录      : {outdir}")
    print(f"学生数量      : {len(STUDENTS)}")
    print(f"挑战数量      : {len(CHALLENGES)}")
    print(f"提交记录条数  : {len(records)}")
    complete = sum(1 for r in records if r["status"] == "complete")
    partial = sum(1 for r in records if r["status"] == "partial")
    missing = sum(1 for r in records if r["status"] == "missing")
    print(f"  - 完整提交  : {complete}")
    print(f"  - 部分提交  : {partial}")
    print(f"  - 缺失提交  : {missing}")
    print(f"JSON 文件     : {j}  ({os.path.getsize(j)} bytes)")
    print(f"CSV  文件     : {c}  ({os.path.getsize(c)} bytes)")
    print(f"挑战元数据    : {ch}  ({os.path.getsize(ch)} bytes)")
    print("=" * 60)
    print("注意：当前为模拟数据（is_mock_data=true），替换数据源即可接入真实提交。")


if __name__ == "__main__":
    main()
