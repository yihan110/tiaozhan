# 阮依涵_C6A_方案设计.md

> 挑战：C6A 提交数据仪表盘 ｜ 作者：阮依涵（郑州西亚斯学院 软件工程 2025 级）
> 完成级别：Level 3（本地网站仪表盘）+ Level 4 自动化要素（脚本参数化、可一键复跑）

---

## 1. 目标

把"散落在群文件、聊天记录、个人文件夹"的 Elite 20 课程提交物，整理成一条**可复跑的数据管线**：

```
提交文件夹 / 群文件
      ↓  ① build_data.py（结构化）
submissions.json + submissions.csv + challenges.json
      ↓  ② build_excel.py（openpyxl）
阮依涵_C6A_report.xlsx（5 个 Sheet）
      ↓  ③ dashboard/index.html（静态 HTML+JS）
本地浏览器仪表盘（总览 / 学生详情 / 挑战详情 / 筛选 / 导出）
```

## 2. 技术选型

| 环节 | 选型 | 理由 |
|---|---|---|
| 数据结构化 | Python 3.13 + 标准库 json/csv | 零额外依赖，参数化输入输出 |
| Excel 报表 | openpyxl 3.1.5 | 支持多 Sheet、条件填色、表头样式；CHALLENGE.md 官方推荐 |
| 仪表盘 | 纯静态 HTML + 原生 JS + 内嵌 CSS | 零构建、零依赖、双击 index.html 即可打开；评审同学不需要装 Node |
| 图表 | 自绘热力图（CSS Grid）+ KPI 卡片 | 不引 Chart.js CDN，离线可跑；学生×挑战矩阵用热力图比饼图信息密度更高 |
| 截图证据 | Edge headless `--screenshot` | 本机无 Chrome，用系统自带 Edge headless 模式真实截图 |

## 3. 数据模型

### 3.1 提交记录 Schema（与 CHALLENGE.md §数据模型 对齐）

```json
{
  "student": {"name": "阮依涵", "pinyin": "ruanyihan", "major": "软件工程", "github": "ruanyihan-sias"},
  "challenge": "C6A",
  "submitted_at": "2026-09-25T10:22:00+08:00",
  "files": [
    {"filename": "ruanyihan_C6A_report.xlsx", "category": "报表", "required": true, "present": true},
    {"filename": "ruanyihan_C6A_dashboard/", "category": "仪表盘", "required": true, "present": false}
  ],
  "status": "partial",           // complete / partial / missing
  "completeness": 0.75,
  "missing": ["dashboard/"],
  "level_achieved": 3,
  "notes": "缺失：dashboard/"
}
```

### 3.2 覆盖范围

- **学生**：12 名（含本人阮依涵）
- **挑战**：9 个（C1A / C2A / C3A / C4A / C4B / C4C / C4D / C5A / C6A）
- **提交记录**：85 条（完整 40 / 部分 25 / 缺失 20）
- **缺失项分析**：40 条记录含至少 1 个缺失必填项（Excel"缺失项"Sheet 全部标红）

> ⚠️ **数据为模拟数据**：当前 `data/submissions.json` 中 `is_mock_data=true`。脚本与流程不依赖具体学生姓名——替换数据源即可接入真实提交（见教学说明.md §"如何换成真实数据"）。

## 4. 仪表盘功能清单（对照 CHALLENGE.md Level 3）

| 功能 | 实现位置 | 截图证据 |
|---|---|---|
| 总览页（KPI + 热力图） | index.html 顶部 | screenshots/01_overview.png |
| 学生详情（文件清单 ✅/❌） | 点击学生名/热力格 | screenshots/02_student_detail.png |
| 挑战详情（必填文件 + 全学生状态） | 点击挑战编号 | screenshots/03_challenge_detail.png |
| 按学生/挑战/状态/关键字筛选 | 筛选栏 | screenshots/04_filter_partial.png |
| 缺失提醒（红色 badge + 红字缺失项） | 全局样式 | 全部截图可见 |
| 导出 JSON / 导出 CSV | 顶部按钮 | 教学说明.md §导出演示 |

## 5. 可复用性设计

1. **脚本参数化**：`build_data.py --outdir <DIR> --seed <N>`；`build_excel.py --data <json> --out <xlsx>`。
2. **新增挑战**：只改 `build_data.py` 顶部 `CHALLENGES` 列表，HTML/Excel 自动适配（按 challenges 数组动态渲染）。
3. **新增学生**：改 `STUDENTS` 列表即可，无需改前端。
4. **接入真实数据**：把 `generate_mock_records()` 替换为 `scan_submission_folder(root_dir)`（伪代码已在教学说明中给出）。

## 6. 自评分（对照 rubric.json）

| 维度 | 满分 | 自评 | 依据 |
|---|---|---|---|
| 数据洞察 | 25 | 23 | 85 条记录、40 条缺失项可分析；热力图直接定位薄弱学生/薄弱挑战 |
| 可视化 | 20 | 18 | KPI + 热力图 + 表格，三色状态语义清晰；未引外部图表库 |
| 产物完整性 | 15 | 14 | 数据/脚本/Excel/仪表盘/截图/文档齐全，README 可独立跑通 |
| AI 使用质量 | 20 | 18 | AI日志.md 记录 6 轮迭代，含踩坑与 prompt 演化 |
| 复盘质量 | 20 | 18 | AAR.md 含 3 个具体失败点 + 改进方案 |
