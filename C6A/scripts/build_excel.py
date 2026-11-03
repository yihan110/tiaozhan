# -*- coding: utf-8 -*-
"""
build_excel.py
==============
C6A 提交数据仪表盘 - Excel 报表生成脚本（Level 2）

读取 ../data/submissions.json，生成 5 个 Sheet：
    1. 总览       —— 学生 × 挑战矩阵 + 完成率
    2. 按学生     —— 每个学生的提交明细
    3. 按挑战     —— 每个挑战的学生提交情况
    4. 时间线     —— 按提交时间排序
    5. 缺失项     —— 高亮缺失必填项

用法：
    python build_excel.py
    python build_excel.py --data ../data/submissions.json --out ../阮依涵_C6A_report.xlsx
"""

import argparse
import json
import os
from collections import defaultdict

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

# 样式
HEADER_FILL = PatternFill("solid", fgColor="1F4E78")
HEADER_FONT = Font(bold=True, color="FFFFFF", size=11)
GREEN_FILL = PatternFill("solid", fgColor="C6EFCE")
YELLOW_FILL = PatternFill("solid", fgColor="FFEB9C")
RED_FILL = PatternFill("solid", fgColor="FFC7CE")
THIN = Side(border_style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
CENTER = Alignment(horizontal="center", vertical="center")


def style_header(ws, row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = CENTER
        cell.border = BORDER


def auto_width(ws, max_width=40):
    for col in ws.columns:
        length = max((len(str(c.value)) if c.value is not None else 0) for c in col)
        ws.column_dimensions[get_column_letter(col[0].column)].width = min(max_width, length + 2)


def status_fill(status):
    return {"complete": GREEN_FILL, "partial": YELLOW_FILL, "missing": RED_FILL}.get(status)


# ---------------------------------------------------------------------------
def build_overview(wb, data, students, challenges):
    ws = wb.active
    ws.title = "总览"

    # 索引：(学生, 挑战) -> record
    idx = {(r["student"]["name"], r["challenge"]): r for r in data["records"]}

    headers = ["学生"] + [c["id"] for c in challenges] + ["完成率", "完整数", "部分数", "缺失数"]
    ws.append(headers)
    style_header(ws, 1, len(headers))

    for stu in students:
        row = [stu["name"]]
        complete = partial = missing = 0
        for ch in challenges:
            rec = idx.get((stu["name"], ch["id"]))
            if rec is None:
                row.append("—")
                missing += 1
            else:
                row.append({"complete": "✅", "partial": "⚠️", "missing": "❌"}[rec["status"]])
                if rec["status"] == "complete":
                    complete += 1
                elif rec["status"] == "partial":
                    partial += 1
                else:
                    missing += 1
        total = len(challenges)
        rate = round((complete + 0.5 * partial) / total * 100, 1)
        row += [f"{rate}%", complete, partial, missing]
        ws.append(row)

    # 行底色
    for r in range(2, ws.max_row + 1):
        for c in range(1, len(challenges) + 2):
            cell = ws.cell(row=r, column=c)
            v = cell.value
            if v == "✅":
                cell.fill = GREEN_FILL
            elif v == "⚠️":
                cell.fill = YELLOW_FILL
            elif v == "❌":
                cell.fill = RED_FILL
            cell.alignment = CENTER
            cell.border = BORDER

    # 末尾统计行
    ws.append([])
    ws.append(["全班完成率"] + [""] * len(challenges) + ["=AVERAGE(" + get_column_letter(len(challenges)+2) + "2:" + get_column_letter(len(challenges)+2) + str(len(students)+1) + ")"])
    auto_width(ws)


def build_by_student(wb, data):
    ws = wb.create_sheet("按学生")
    headers = ["学生", "挑战编号", "挑战标题", "提交时间", "状态", "完成度", "缺失项", "达到Level", "备注"]
    ws.append(headers)
    style_header(ws, 1, len(headers))
    for r in sorted(data["records"], key=lambda x: (x["student"]["name"], x["challenge"])):
        ws.append([
            r["student"]["name"], r["challenge"], r["challenge_title"],
            r["submitted_at"], r["status"], r["completeness"],
            "|".join(r["missing"]) or "—", r["level_achieved"], r["notes"],
        ])
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=5, max_col=5):
        for cell in row:
            cell.fill = status_fill(cell.value)
            cell.alignment = CENTER
    auto_width(ws)


def build_by_challenge(wb, data, challenges):
    ws = wb.create_sheet("按挑战")
    headers = ["挑战编号", "挑战标题", "提交学生数", "完整数", "部分数", "缺失数", "挑战完成率"]
    ws.append(headers)
    style_header(ws, 1, len(headers))
    by_ch = defaultdict(list)
    for r in data["records"]:
        by_ch[r["challenge"]].append(r)
    for ch in challenges:
        recs = by_ch.get(ch["id"], [])
        complete = sum(1 for r in recs if r["status"] == "complete")
        partial = sum(1 for r in recs if r["status"] == "partial")
        missing = sum(1 for r in recs if r["status"] == "missing")
        total = len(STUDENTS_FROM_DATA)
        rate = round((complete + 0.5 * partial) / total * 100, 1)
        ws.append([ch["id"], ch["title"], len(recs), complete, partial, missing, f"{rate}%"])
    auto_width(ws)


def build_timeline(wb, data):
    ws = wb.create_sheet("时间线")
    headers = ["提交时间", "学生", "挑战编号", "状态", "完成度", "缺失项"]
    ws.append(headers)
    style_header(ws, 1, len(headers))
    recs = sorted(data["records"], key=lambda x: x["submitted_at"])
    for r in recs:
        ws.append([r["submitted_at"], r["student"]["name"], r["challenge"], r["status"],
                   r["completeness"], "|".join(r["missing"]) or "—"])
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=4, max_col=4):
        for cell in row:
            cell.fill = status_fill(cell.value)
            cell.alignment = CENTER
    auto_width(ws)


def build_missing(wb, data):
    ws = wb.create_sheet("缺失项")
    headers = ["学生", "挑战编号", "状态", "缺失必填项", "备注"]
    ws.append(headers)
    style_header(ws, 1, len(headers))
    n = 0
    for r in data["records"]:
        if r["missing"]:
            ws.append([r["student"]["name"], r["challenge"], r["status"],
                       "|".join(r["missing"]), r["notes"]])
            n += 1
    # 整行标红
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=5):
        for cell in row:
            cell.fill = RED_FILL
    auto_width(ws)
    return n


# ---------------------------------------------------------------------------
def main():
    global STUDENTS_FROM_DATA
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default=os.path.join(os.path.dirname(__file__), "..", "data", "submissions.json"))
    parser.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "阮依涵_C6A_report.xlsx"))
    args = parser.parse_args()

    with open(args.data, "r", encoding="utf-8") as f:
        data = json.load(f)

    student_names = sorted({r["student"]["name"] for r in data["records"]})
    STUDENTS_FROM_DATA = student_names
    # 取每个学生的完整信息（按名字排序）
    stu_map = {}
    for r in data["records"]:
        stu_map[r["student"]["name"]] = r["student"]
    students = [stu_map[n] for n in student_names]
    challenges = data["challenges"]

    wb = Workbook()
    build_overview(wb, data, students, challenges)
    build_by_student(wb, data)
    build_by_challenge(wb, data, challenges)
    build_timeline(wb, data)
    n_missing = build_missing(wb, data)

    out = os.path.abspath(args.out)
    wb.save(out)

    # 校验：重新读取，打印每个 sheet 的列结构
    from openpyxl import load_workbook
    wb2 = load_workbook(out)
    print("=" * 60)
    print("Excel 报表生成完成")
    print("=" * 60)
    print(f"输出文件: {out}")
    print(f"文件大小: {os.path.getsize(out)} bytes")
    print(f"Sheet 数量: {len(wb2.sheetnames)}")
    for name in wb2.sheetnames:
        ws = wb2[name]
        headers = [c.value for c in ws[1]]
        print(f"  - [{name}] 行数={ws.max_row} 列数={ws.max_column}")
        print(f"      表头: {headers}")
    print(f"缺失项条目数: {n_missing}")
    print("=" * 60)


if __name__ == "__main__":
    main()
