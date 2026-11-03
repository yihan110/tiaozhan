# -*- coding: utf-8 -*-
"""一次性演示驱动脚本：清空 data -> 跑完整 MVP 流程 -> 把每步真实 stdout 写入 运行记录/*.txt"""
import os, shutil, subprocess, sys, datetime

MVP = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(MVP, "data")
LOGDIR = os.path.join(MVP, "运行记录")
os.makedirs(LOGDIR, exist_ok=True)

# 用 python 内部删除，不触发 PowerShell 确认弹窗
shutil.rmtree(DATA, ignore_errors=True)

PY = sys.executable
SCRIPT = os.path.join(MVP, "阮依涵_C9_mvp.py")
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")

def run(args):
    """运行 MVP 命令，返回 (命令串, stdout 文本)"""
    cmd = [PY, SCRIPT] + args
    r = subprocess.run(cmd, cwd=MVP, capture_output=True, text=True, encoding="utf-8", env=ENV)
    return "$ python 阮依涵_C9_mvp.py " + " ".join(args), (r.stdout or "") + (r.stderr or "")

def write_log(fname, title, blocks):
    path = os.path.join(LOGDIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n")
        f.write(f"# 本机真实运行时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# 解释器：{sys.executable}\n")
        f.write("=" * 60 + "\n\n")
        for cmd, out in blocks:
            f.write(cmd + "\n")
            f.write("-" * 60 + "\n")
            f.write(out.strip() + "\n\n")
    print("written:", path)

# ---------- 01 初始化与添加卡片 ----------
b1 = []
b1.append(run(["add", "--front", "二重积分交换积分次序的前提条件",
               "--back", "积分区域须为有限闭区域且被积函数连续可积；先画积分域再定限", "--tag", "高数"]))
b1.append(run(["add", "--front", "计算 xy 在 D 上的二重积分，D 由 y=x 与 y=x^2 围成",
               "--back", "交点(0,0)(1,1)；X型 x∈[0,1] y∈[x^2,x]；结果 1/24", "--tag", "高数"]))
b1.append(run(["add", "--front", "四级作文中表达“认为”的高分替换词",
               "--back", "maintain / hold the view that / reckon / argue that，避免通篇 think", "--tag", "四级"]))
b1.append(run(["add", "--front", "abundant 的中文含义与搭配",
               "--back", "adj.丰富的；be abundant in = 富于；四级高频词", "--tag", "四级"]))
b1.append(run(["add", "--front", "栈和队列的区别（一句话面试版）",
               "--back", "栈 LIFO 后进先出，队列 FIFO 先进先出；栈用于递归/括号匹配，队列用于 BFS/任务排队", "--tag", "数据结构"]))
write_log("01_初始化与添加卡片.txt", "Step 1 初始化数据库并添加 5 张卡片", b1)

# ---------- 02 今日待复习 ----------
b2 = [run(["due"])]
write_log("02_今日待复习.txt", "Step 2 列出今天到期的卡片（新卡全部今日到期）", b2)

# ---------- 03 执行复习评分 ----------
b3 = []
b3.append(run(["review", "1", "good"]))
b3.append(run(["review", "2", "again"]))   # 这张高数错题没掌握 -> 明天重来
b3.append(run(["review", "3", "good"]))
b3.append(run(["review", "4", "easy"]))
b3.append(run(["review", "5", "good"]))
write_log("03_复习操作与评分.txt", "Step 3 逐张复习并按 SM-2 评分", b3)

# ---------- 04 复习后今日列表（应只剩 again 那张？不，again=明天，所以今日清空） ----------
b4 = [run(["due"])]
write_log("04_复习后今日列表.txt", "Step 4 复习完后再查今日待复习", b4)

# ---------- 05 用 --today 模拟未来日期，验证间隔重复生效 ----------
b5 = []
b5.append(run(["--today", "2026-11-02", "due"]))   # again 那张( #2 )明天到期
b5.append(run(["--today", "2026-11-05", "due"]))   # 11-01 good 的(1,3,5) interval=1 -> 11-02到期；4号easy interval=4 ->11-05
write_log("05_模拟未来日期验证间隔重复.txt", "Step 5 指定 --today 模拟未来日期，验证 SM-2 排期生效", b5)

# ---------- 06 统计与全量列表 ----------
b6 = [run(["stats"]), run(["list"])]
write_log("06_统计与全量列表.txt", "Step 6 统计与全量卡片列表", b6)

print("DEMO DONE")
