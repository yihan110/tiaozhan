# 阮依涵_C6A_拿来说明.md

> 本文件列出 C6A 提交包中**直接复用或参考**的外部来源、技能文档、库与工具。每项写清：来源、参考了什么、改了哪里。

---

## 1. 官方挑战资料（必读）

| 来源 | 参考了什么 | 改了哪里 |
|---|---|---|
| `挑战资料包/.../CHALLENGE.md` §数据模型 Schema | 提交记录 JSON 结构（student/challenge/submitted_at/files/status/completeness/missing） | 完全对齐，未改字段名；额外加了 `notes` 字段用于备注 |
| `CHALLENGE.md` §Level 2 Excel 报表 表格 | 5 个 Sheet 的命名与内容要求（总览/按学生/按挑战/时间线/缺失项） | Sheet 名与要求一致；总览额外加了"完成率/完整数/部分数/缺失数"4 列统计 |
| `CHALLENGE.md` §Level 3 功能表 | 仪表盘功能清单（总览/学生详情/挑战详情/筛选/文件链接/缺失提醒） | 文件链接改为"展示文件名+✅/❌"（因为是模拟数据，没有真实文件可下）；其余功能一一对应 |
| `rubric.json` | 5 个评分维度与权重 | 方案设计.md §6 自评表完全按 rubric 维度打分 |

## 2. 本机技能文档

| 来源路径 | 参考了什么 | 改了哪里 |
|---|---|---|
| `C:\Users\asus\AppData\Local\Doubao\User Data\Profile 1\.doubao\agent_mode\workspace\.skills\sheet\SKILL.md` | openpyxl 多 Sheet 写法、条件填色 PatternFill、表头样式 Font/Border 的标准用法 | 参考了"三色语义填色"思路（绿/黄/红对应 complete/partial/missing）；未直接搬代码，自己按 openpyxl API 重写 |
| `...\.skills\html\SKILL.md` | 静态 HTML 单文件交付、零依赖优先、离线可打开的原则 | 采纳"不引外部 CDN"的建议，砍掉 Chart.js，改用纯 CSS Grid 热力图 |

## 3. 第三方库

| 库 | 版本 | 用途 | 是否修改源码 |
|---|---|---|---|
| Python 标准库 `json` / `csv` / `argparse` / `random` / `datetime` | 3.13.16 | 数据生成、序列化、CLI 参数化 | 否 |
| `openpyxl` | 3.1.5 | 生成 .xlsx 报表 + load_workbook 自检 | 否（`pip install openpyxl` 安装） |

## 4. 工具

| 工具 | 用途 | 证据 |
|---|---|---|
| Microsoft Edge (headless) | 真实打开 index.html 并截图 | screenshots/*.png；命令见 AI日志.md 轮次 5 |
| PowerShell 5.1 | 运行 Python 脚本、Tee 终端日志、打包 zip | logs/01_build_data.log.txt、logs/02_build_excel.log.txt |
| 豆包 / Doubao AI | 6 轮迭代（见 AI日志.md） | AI日志.md 全文 |

## 5. 没有用到、但被讨论过的方案

| 方案 | 为什么没用 |
|---|---|
| Chart.js CDN | 离线环境可能加载失败，砍掉 |
| React / Vue 构建工具 | 评审同学不需要装 Node，单文件 HTML 最简 |
| Streamlit | 需要 `pip install streamlit` 且起本地服务，不如静态 HTML 直接 |
| Flask/FastAPI 后端 | 模拟数据无需后端；Level 3 要求"本地网站"，静态页足够 |

## 6. 数据来源声明

`data/submissions.json` 中 `is_mock_data = true`。所有学生姓名（除阮依涵本人）、GitHub 账号、提交时间均为 `build_data.py` 用 `random.seed(42)` 生成的**模拟数据**，不指向任何真实同学。脚本与流程完全可复用于真实提交数据（见教学说明.md）。
