# 阮依涵_C6A_教学说明.md

> 怎么安装、怎么运行、怎么更新数据、怎么换成真实数据。

---

## 1. 环境要求

- Windows 10/11（macOS/Linux 同样可跑，路径改一下即可）
- Python 3.10+（本机 3.13.16）
- 依赖：`openpyxl`（已在本机安装；如缺：`pip install openpyxl`）
- 浏览器：Edge / Chrome / 任何现代浏览器（双击 index.html 即可，无需服务器）

## 2. 一键复跑（30 秒）

```powershell
cd 挑战C6A_阮依涵_提交包\scripts

# ① 生成结构化数据
python build_data.py

# ② 生成 Excel 报表
python build_excel.py

# ③ 打开仪表盘（任选其一）
start ..\dashboard\index.html
```

跑完后产物：
- `data\submissions.json` / `submissions.csv` / `challenges.json`
- `阮依涵_C6A_report.xlsx`（5 个 Sheet）
- `dashboard\index.html` + `dashboard\data.js`

## 3. 脚本参数

| 脚本 | 参数 | 默认 | 说明 |
|---|---|---|---|
| build_data.py | `--outdir <DIR>` | `../data` | 输出目录 |
| build_data.py | `--seed <INT>` | `42` | 随机种子，固定可复现 |
| build_excel.py | `--data <JSON>` | `../data/submissions.json` | 输入数据 |
| build_excel.py | `--out <XLSX>` | `../阮依涵_C6A_report.xlsx` | 输出 Excel |

## 4. 仪表盘功能操作

| 操作 | 怎么做 |
|---|---|
| 看总览 | 打开 index.html 默认就是 |
| 看某学生所有提交 | 点击热力图里的学生姓名，或下方表格里的学生链接 |
| 看某挑战所有学生 | 点击表格里的挑战编号 |
| 按状态筛选 | 顶部"状态"下拉选 完整/部分/缺失，点"筛选" |
| 按学生/挑战筛选 | 对应下拉框选择后点"筛选" |
| 导出当前数据 | 右上角"导出 JSON"或"导出 CSV"按钮 |

## 5. 怎么换成真实数据（关键）

当前 `data/submissions.json` 里 `is_mock_data=true`。换成真实数据有两种方式：

### 方式 A：手工整理 JSON（最快）
按 `data/submissions.json` 的结构填真实记录，替换整个文件，然后：
```powershell
python scripts\build_excel.py --data data\submissions.json
python -c "import json; d=json.load(open('data/submissions.json','r',encoding='utf-8')); open('dashboard/data.js','w',encoding='utf-8').write('window.DASHBOARD_DATA = '+json.dumps(d,ensure_ascii=False,indent=2)+';')"
```
刷新浏览器即可。

### 方式 B：自动扫描提交文件夹（推荐，Level 4）
在 `build_data.py` 里新增一个函数：

```python
import glob, os
def scan_submission_folder(root_dir):
    """扫描 root_dir 下所有 *_C*_*.md / *.xlsx / *.html 文件，
    按命名规范拆出学生/挑战/必填项，自动判断 present。"""
    records = []
    for fp in glob.glob(os.path.join(root_dir, "**", "*_C*_*"), recursive=True):
        base = os.path.basename(fp)
        parts = base.split("_")   # e.g. ruanyihan_C6A_AI日志.md
        if len(parts) < 3: continue
        pinyin, ch_id = parts[0], parts[1]
        # ... 查表 STUDENTS 反查 name；查 CHALLENGES 反查必填文件清单
        # ... 累加 files[].present，最后算 status/completeness/missing
    return records
```

把 `main()` 里的 `generate_mock_records()` 换成 `scan_submission_folder(r"D:\提交文件夹")` 即可。

## 6. 新增一个挑战

改 `scripts\build_data.py` 顶部 `CHALLENGES` 列表，加一条：
```python
{"id": "C7A", "title": "新挑战标题", "required_files": ["方案设计.md", "AI日志.md"]},
```
重跑两个脚本，Excel 和 HTML 会自动多出一列/一行，无需改前端。

## 7. 常见问题

| 问题 | 解决 |
|---|---|
| 打开 CSV 中文乱码 | 已经用 utf-8-sig 写，Excel 双击应正常；若仍乱码用"数据→从文本/CSV"导入选 UTF-8 |
| 仪表盘打开空白 | 确认 `dashboard/data.js` 与 `index.html` 在同一目录；不要单独移动 index.html |
| openpyxl 报错 | `pip install --upgrade openpyxl` |
| Edge headless 截图命令 | 见 AI日志.md 轮次 5 |
