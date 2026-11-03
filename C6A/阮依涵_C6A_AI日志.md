# 阮依涵_C6A_AI日志.md

> 本日志如实记录 C6A 全过程中与 AI（豆包 / Doubao）的多轮交互。每轮包含：目标、prompt 摘要、AI 产出、我的判断、下一轮迭代方向。

---

## 轮次 1：需求拆解与数据模型设计

**目标**：刚读完 CHALLENGE.md，不知道从哪下手。

**Prompt 摘要**：
> "我在做 Elite20 的 C6A 提交数据仪表盘。CHALLENGE.md 要求 Level1 数据结构化、Level2 Excel 报表、Level3 本地网站。我现在没有真实提交数据。请帮我：(1) 设计一个能覆盖 12 名学生 × 9 个挑战的模拟数据 schema；(2) 列出三步管线的最小可跑通版本；(3) 告诉我哪些字段必须有，否则'缺失项'分析没意义。"

**AI 产出**：
- 给出了与 CHALLENGE.md §数据模型 对齐的 record schema（student / challenge / submitted_at / files[] / status / completeness / missing）。
- 强调：`files[].present` 必须是布尔数组，而不是只存一个 status——否则"缺了哪个具体文件"无法回答。
- 建议：模拟数据要故意制造 3 类条目——complete / partial / missing，比例约 5:3:2，否则热力图一片绿看不出问题。

**我的判断**：采纳。把比例定为 55% / 30% / 15%（实际跑出来是 40/25/20）。

---

## 轮次 2：脚本第一版（build_data.py）

**Prompt 摘要**：
> "请写一个 Python 脚本，按上面的 schema 生成模拟数据，输出 submissions.json 和 submissions.csv。要求：随机种子固定可复现；学生 12 个、挑战 9 个；CSV 用 utf-8-sig 让 Excel 中文不乱码。"

**AI 产出**：完整脚本。

**踩坑 1**：docstring 里写了 `--outdir D:\xxx`，Python 把 `\x` 当成 unicode 转义，运行直接 SyntaxError。
**修复**：把示例路径改成 `<DIR>` 占位符，避免反斜杠。

**终端证据**：logs/01_build_data.log.txt
```
提交记录条数  : 85
  - 完整提交  : 40
  - 部分提交  : 25
  - 缺失提交  : 20
JSON 文件     : submissions.json  (90180 bytes)
CSV  文件     : submissions.csv  (13957 bytes)
```

---

## 轮次 3：Excel 报表第一版（build_excel.py）

**Prompt 摘要**：
> "用 openpyxl 读 submissions.json，生成 5 个 Sheet：总览（学生×挑战矩阵）、按学生、按挑战、时间线、缺失项。要求：状态用绿/黄/红三色填色；缺失项整行标红；生成后用 load_workbook 重新读一遍打印每个 sheet 的表头和行数做自检。"

**AI 产出**：脚本写完第一次跑挂了。

**踩坑 2**：`build_overview` 里我把 `students` 当成 dict 列表（`stu["name"]`），但 main 里传进去的是 `sorted({r["student"]["name"] ...})` 字符串列表。`TypeError: string indices must be integers`。
**修复**：在 main 里用 `stu_map = {}` 按名字保留学生完整 dict，再传回。

**踩坑 3**：总览 Sheet 末尾想加"全班完成率"，AI 给的 Excel 公式列号算错了。我直接放弃公式，改为在终端输出里打印完成率统计，避免 Excel 公式引用错误。

**终端证据**：logs/02_build_excel.log.txt
```
Sheet 数量: 5
  - [总览] 行数=15 列数=14
  - [按学生] 行数=86 列数=9
  - [按挑战] 行数=10 列数=7
  - [时间线] 行数=86 列数=6
  - [缺失项] 行数=41 列数=5
缺失项条目数: 40
```

---

## 轮次 4：HTML 仪表盘第一版

**Prompt 摘要**：
> "基于 submissions.json 做一个单文件 index.html 仪表盘。要求：(1) 顶部 4 个 KPI 卡片；(2) 学生×挑战热力图，点击格子弹出学生详情 modal；(3) 筛选栏：学生下拉、挑战下拉、状态下拉、关键字；(4) 导出 JSON/CSV 按钮；(5) 不要引外部 CDN，离线能跑。"

**AI 产出**：完整 HTML+JS。

**我的修改**：
- 把 Chart.js CDN 方案砍掉，改用纯 CSS Grid 画热力图——因为评审同学可能没网，CDN 加载失败会白屏。
- 状态 badge 用三色语义（绿=complete、黄=partial、红=missing），与 Excel 完全一致。

---

## 轮次 5：截图方案踩坑

**Prompt 摘要**：
> "我需要给仪表盘截图当证据。本机没有 Chrome，只有 Edge。怎么用命令行截图？"

**AI 产出**：`msedge --headless --disable-gpu --window-size=1400,1800 --screenshot=out.png file:///path/to/index.html`

**踩坑 4**：modal（学生详情/挑战详情）是 JS 点击触发的，headless 截图不会自动点开。
**修复**：用 PowerShell 读取 index.html 字符串，在 `</body>` 前注入一段 `setTimeout(()=>showStudent("阮依涵"),300)`，生成临时 `_tmp_student.html`，截图完删掉临时文件。最终截图：
- screenshots/01_overview.png（总览）
- screenshots/02_student_detail.png（学生阮依涵详情 modal）
- screenshots/03_challenge_detail.png（C6A 挑战详情 modal）
- screenshots/04_filter_partial.png（筛选 status=partial）

---

## 轮次 6：文档与打包

**Prompt 摘要**：
> "我现在有数据/脚本/Excel/HTML/截图。请帮我列一份交付清单，对照 CHALLENGE.md §'需要提交什么'检查缺什么，并告诉我打包前要自检什么。"

**AI 产出**：
- 对照清单：方案设计.md ✅、data/ ✅、dashboard/ ✅、report.xlsx ✅、screenshots/ ✅、教学说明.md ✅、AAR.md ✅、AI日志.md ✅、拿来说明.md ✅。
- 自检建议：用 python zipfile 列包内文件，确认必备文件非空；确认 Excel 能用 openpyxl 打开；确认截图 PNG 大小 > 50KB（防止白屏截图）。

---

## 迭代总结

| 轮次 | 产出 | 关键决策 |
|---|---|---|
| 1 | 数据模型 | files[].present 必须布尔数组 |
| 2 | build_data.py | utf-8-sig CSV；固定随机种子 |
| 3 | build_excel.py | 三色填色；load_workbook 自检 |
| 4 | index.html | 砍 Chart.js CDN，离线优先 |
| 5 | 4 张截图 | 临时注入 JS 触发 modal |
| 6 | 文档+打包 | 对照 CHALLENGE.md 清单逐项核对 |

**最有价值的一次 prompt 修正**：轮次 4 砍掉 CDN。一开始 AI 给的方案默认引 Chart.js，我没多想就接受了；后来想到"评审同学打开本地 HTML 不一定有网"，才改成纯 CSS。这一次改动让仪表盘从"看起来炫"变成"真的能跑"。
