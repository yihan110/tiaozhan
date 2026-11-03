# 挑战 C6A 提交数据仪表盘 — 阮依涵 提交包

> 郑州西亚斯学院 软件工程 2025 级 ｜ 阮依涵
> 完成级别：Level 3（本地网站仪表盘）+ Level 4 自动化要素（脚本参数化、可一键复跑）

## ⚠️ 数据声明

本包 `data/submissions.json` 中 `is_mock_data = true`。**所有学生（除阮依涵本人）、GitHub 账号、提交时间均为模拟数据**，由 `scripts/build_data.py` 用 `random.seed(42)` 生成。脚本与流程不绑定具体数据——替换数据源即可接入真实提交（见 `阮依涵_C6A_教学说明.md` §5）。

## 包内文件清单

```
挑战C6A_阮依涵_提交包/
├── README.md                       ← 本文件
├── 阮依涵_C6A_方案设计.md           ← 架构、技术选型、数据模型、自评分
├── 阮依涵_C6A_AI日志.md            ← 6 轮 AI 迭代全过程（必备）
├── 阮依涵_C6A_拿来说明.md           ← 参考了哪些库/技能/来源
├── 阮依涵_C6A_AAR.md               ← 复盘：3 个失败点 + 改进方案
├── 阮依涵_C6A_教学说明.md           ← 怎么跑、怎么换真实数据
├── 阮依涵_C6A_report.xlsx          ← Excel 报表（5 Sheet）
│
├── data/                           ← Level 1 结构化数据
│   ├── submissions.json            （90 KB，85 条记录）
│   ├── submissions.csv             （utf-8-sig，Excel 直接打开）
│   └── challenges.json            （9 个挑战元数据）
│
├── scripts/                        ← 可复跑脚本
│   ├── build_data.py               （生成 JSON/CSV）
│   └── build_excel.py              （openpyxl 生成 5 Sheet）
│
├── dashboard/                      ← Level 3 本地网站
│   ├── index.html                  （单文件，零依赖，双击即开）
│   └── data.js                     （从 submissions.json 生成）
│
├── screenshots/                    ← 真实运行截图（Edge headless）
│   ├── 01_overview.png             （总览页：KPI + 热力图 + 表格）
│   ├── 02_student_detail.png       （学生详情 modal：阮依涵）
│   ├── 03_challenge_detail.png     （挑战详情 modal：C6A）
│   └── 04_filter_partial.png       （筛选 status=partial）
│
└── logs/                           ← 终端运行证据
    ├── 01_build_data.log.txt       （85 条记录生成日志）
    └── 02_build_excel.log.txt      （5 Sheet 自检日志）
```

## 30 秒跑通

```powershell
cd 挑战C6A_阮依涵_提交包\scripts
python build_data.py
python build_excel.py
start ..\dashboard\index.html
```

## 对照 CHALLENGE.md §"需要提交什么"

| 要求 | 本包文件 |
|---|---|
| 姓名_C6A_方案设计.md | ✅ 阮依涵_C6A_方案设计.md |
| 姓名_C6A_data/ | ✅ data/ |
| 姓名_C6A_dashboard/ | ✅ dashboard/ |
| 姓名_C6A_report.xlsx | ✅ 阮依涵_C6A_report.xlsx |
| 姓名_C6A_screenshots/ | ✅ screenshots/ |
| 姓名_C6A_教学说明.md | ✅ 阮依涵_C6A_教学说明.md |
| 姓名_C6A_AAR.md | ✅ 阮依涵_C6A_AAR.md |
| 姓名_C6A_AI日志.md（必须） | ✅ 阮依涵_C6A_AI日志.md |
| 姓名_C6A_拿来说明.md | ✅ 阮依涵_C6A_拿来说明.md |

## 打包后自检

用 Python 列包内文件，确认必备项存在且非空：

```python
import zipfile
z = zipfile.ZipFile("挑战C6A_阮依涵_提交包.zip")
for i in z.infolist():
    print(f"{i.file_size:>8}  {i.filename}")
```
