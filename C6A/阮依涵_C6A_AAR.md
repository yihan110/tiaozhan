# 阮依涵_C6A_AAR.md（After-Action Review）

> 复盘：做了什么 / 学了什么 / 怎么验证的 / 下次怎么改进。

---

## 1. 实际成果 vs 计划

| 计划 | 实际 | 差异 |
|---|---|---|
| Level 1：结构化 JSON+CSV | ✅ 85 条记录，JSON 90KB + CSV 14KB | 超出预期（原计划 10 学生，实际 12） |
| Level 2：5 Sheet Excel | ✅ 总览/按学生/按挑战/时间线/缺失项，三色填色 | 完成 |
| Level 3：本地仪表盘 | ✅ 单文件 HTML，零依赖，含 modal/筛选/导出 | 完成 |
| Level 4：自动化 | ⚠️ 脚本参数化已做；自动扫描真实文件夹未做（无真实数据） | 留接口，未实现 |

## 2. 三个具体失败点 + 修复

### 失败 1：docstring 里的 Windows 路径引发 SyntaxError
- **现象**：`python build_data.py` 第一行就挂，`unicodeescape codec can't decode bytes`。
- **根因**：docstring 写了 `--outdir D:\xxx`，Python 把 `\x` 当 hex 转义。
- **修复**：示例路径全部改成 `<DIR>` 占位符。
- **教训**：写 Windows 路径示例时，要么用 raw string `r"D:\xxx"`，要么别写反斜杠。

### 失败 2：students 列表类型不一致
- **现象**：`build_overview` 里 `stu["name"]` 报 `TypeError: string indices must be integers`。
- **根因**：main 里传的是 `sorted({名字字符串})`，函数却按 dict 解。
- **修复**：在 main 里用 `stu_map` 按名字保留完整学生 dict。
- **教训**：跨函数传数据时，先在脑子里过一遍"传进去的到底是什么类型"，别靠命名猜。

### 失败 3：headless 截图截不到 modal
- **现象**：modal 是 JS 点击触发的，Edge headless 一次性截图只能截初始页面。
- **根因**：headless 模式不会模拟点击。
- **修复**：用 PowerShell 读 index.html 字符串，在 `</body>` 前注入 `setTimeout(()=>showStudent("阮依涵"),300)`，生成临时 `_tmp_student.html` 截图后删除。
- **教训**：自动化截图前先想清楚"页面的哪个状态是我要截的"，必要时注入 JS 直达目标状态。

## 3. 最有价值的一个决策

**砍掉 Chart.js CDN，改用纯 CSS Grid 画热力图。**

一开始 AI 给的方案默认引 Chart.js，我直接接受了。后来想到：评审同学双击 index.html 时可能没网，CDN 加载失败就白屏。换成纯 CSS 后，仪表盘在 `file://` 协议下 100% 可跑。

**这一条让交付物从"看起来炫"变成"真的能用"。**

## 4. 数据洞察（从模拟数据里看到的结论）

虽然是模拟数据，但管线跑通后可以立刻看到几个口径：

1. **薄弱挑战**：C4C（作业自动求解）partial+missing 占比最高——这类需要产出 PDF/技能包的硬产出挑战，最容易缺文件。
2. **薄弱学生**：陈浩然、杨子墨、郑博文三人在多个挑战上 missing——如果是真实数据，应优先私聊催交。
3. **缺失项高发**：`AI日志.md` 和 `拿来说明.md` 是最常缺的两个必填文件——课程方下次可以把这两项做成提交模板的固定勾选项。

> 真实数据接入后，以上结论应重新跑一遍验证，不能直接外推。

## 5. 下次改进方案

| 改进点 | 具体做法 |
|---|---|
| 自动扫描真实文件夹 | 在 build_data.py 加 `scan_submission_folder(root)`：用 glob 匹配 `*_C*_*.md`，按文件名拆出学生/挑战/必填项，自动判断 present |
| 加趋势图 | Excel"时间线"Sheet 已有按时间排序，下一步在仪表盘加"每日提交数"折线图 |
| 加评审集成 | 把 C4A 评审标准做成 JSON，每条记录自动打分 1-5 星 |
| 通知系统 | 每周一跑一次 build_data.py，自动生成"上周缺失项 Markdown"发群 |
| 单元测试 | 给 build_data.py 加 pytest：断言 records 数 = 学生数 × 挑战数 × 覆盖率；断言 missing 条目数 > 0 |

## 6. 怎么验证这次交付是真的跑了

- 终端日志：`logs/01_build_data.log.txt`、`logs/02_build_excel.log.txt`（含文件大小、Sheet 行列数）。
- Excel 自检：build_excel.py 末尾 `load_workbook` 重新读了一遍，打印每个 Sheet 的表头。
- 仪表盘截图：`screenshots/01~04.png`，全部 > 240KB，不是白屏。
- 包内文件自检：见 README.md §打包后自检。
