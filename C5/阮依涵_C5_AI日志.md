# AI_LOG —— md-sorter 开发过程中的 AI 使用记录

> 本文件按"阶段 × 轮次"记录我（阮依涵）用 AI 辅助开发 md-sorter 的全过程。
> 每一轮写清楚：**prompt → AI 给了什么 → 我怎么改 → 为什么这么改**。
> 凡是手写而非 AI 生成的代码，单独标注。

---

## 阶段 0：选题与立项

### Round 0.1 —— 我该做什么项目？

**Prompt（豆包）**：
> "我是软件工程大一学生，要交 C5 GitHub 仓库挑战，rubric 看实用性、可复现性、代码质量、文档、AI 使用。我手上有一堆散落在文件夹里的 Markdown 笔记（课程、错题、AI 心得、三下乡策划），自己整理很痛苦。帮我想一个小而真实的 Python 项目方向。"

**AI 回答要点**：给了 3 个方向 —— (a) Markdown 整理器 (b) 英语单词本 CLI (c) 课程表生成器。推荐 (a)，因为"你自己就是用户，痛点真实，且能在 2 小时内做完"。

**我的判断**：选 (a)。理由 —— 我自己真有这个痛点，不是为了交作业硬编一个场景。

### Round 0.2 —— 项目边界

**Prompt**：
> "那我做 (a)。但我不想做太复杂，不要做全文搜索、不要做向量检索。最小可用版本应该有什么、不应该有什么？"

**AI 回答**：
- 必做：递归扫描 `.md`、抽一级标题、抽 `#标签`、按主题分桶、输出 `INDEX.md`。
- 不做（v0.1 砍）：全文搜索、重命名文件、跨目录去重、GUI、Web 界面。

**我采纳了这个边界**。后面全程没有越界。

---

## 阶段 1：项目骨架

### Round 1.1 —— 生成目录结构

**Prompt**：
> "按 Python 标准开源项目结构，给我一个最小骨架：src/ 布局、tests/、examples/、.gitignore、LICENSE(MIT)、requirements.txt。我用 Python 3.13。"

**AI 给的骨架**（adopted，未做大改）：
```
md-sorter/
├── src/md_sorter/
├── tests/
├── examples/
├── README.md
├── LICENSE
├── .gitignore
└── requirements.txt
```

**我自己加的**：
- `CHANGELOG.md`、`CONTRIBUTING.md`（rubric 里 community 维度加分项）
- `.github/ISSUE_TEMPLATE/`（同上）

### Round 1.2 —— .gitignore

AI 给的标准 Python .gitignore 太长（带 PyInstaller、Jupyter 等我用不到的东西）。**我手动删到只剩 12 行**，理由是"一个学生练手项目不需要这么全"。

---

## 阶段 2：核心代码

### Round 2.1 —— scanner.py

**Prompt**：
> "写一个 Python 模块 `scanner.py`：输入一个目录，递归找出所有 `.md` 和 `.markdown` 文件，要跳过 `.git`、`.venv`、`__pycache__`、`node_modules`、以 `.` 开头的隐藏目录。找不到目录要抛 `FileNotFoundError`，不是目录要抛 `NotADirectoryError`。返回值按相对路径排序。"

**AI 给的初版**：用 `glob.glob(recursive=True)`。
**我让它改的原因**：glob 没法在遍历过程中"剪掉"目录树（还是会进 `.venv` 再走出来），性能差。**让它改成 `os.walk` + 原地修改 `dirnames`**，这是 Python 官方文档推荐的剪枝写法。

### Round 2.2 —— parser.py

**Prompt**：
> "写 `parser.py`：读一个 .md 文件，返回 `{path, title, tags, size_bytes, line_count}`。title 取第一个一级标题（行首 `# `），没有就用文件名。tags 用正则抽 `#xxx` 形式的行内标签（支持中文标签）。文件编码坏掉要降级处理，不能崩。"

**AI 给的正则初版**：`r"#(\w+)"`。
**我发现的 bug**：`\w` 在 Python 默认 regex 里不吃中文（虽然 re.UNICODE 在 3.x 默认开，但组合 `[\u4e00-\u9fa5]` 更稳），而且会把 Markdown 一级标题 `# 标题` 误抓成标签。
**手动改的正则**：
```python
_TAG_RE = re.compile(r"(?<!\w)#([\u4e00-\u9fa5A-Za-z][\u4e00-\u9fa5A-Za-z0-9_-]{1,14})")
```
**编码兜底**是我自己加的：`try: read_text(encoding="utf-8") except UnicodeDecodeError`，AI 初版没考虑这个边界。

### Round 2.3 —— classifier.py（**这一段是踩坑重点**）

**Prompt 第一版**：
> "写 `classifier.py`：内置 7 个主题桶，按 (bucket, keywords) 表匹配，命中哪个桶就归哪个。"

**AI 初版逻辑**：外层遍历桶，内层遍历关键词，命中即返回。

**第一次跑测试，挂了**：`test_classify_tag_overrides_title` 失败 —— 一篇标题写着"操作系统课笔记"、标签打了 `#ai` 的笔记，被归到了"课程笔记"而不是"AI 与工具"。

**为什么挂**：外层按桶顺序走，"课程笔记"在桶表里排第一，标题里有"操作系统"就先命中返回了，根本轮不到看标签。

**我让 AI 改的 prompt（Round 2.3.2）**：
> "分类逻辑有 bug：tags 命中应该优先于 title 命中，但现在是按桶顺序混着判断。请改成两轮扫描：第一轮把所有 tags 在所有桶里扫一遍，命中即返回；第二轮再把 title 在所有桶里扫一遍。"

**AI 给的新版**：两轮 for 循环。**采纳**。重跑 13/13 全过。

> 这段是我在 AI_LOG 里必须写清楚的"失败经验"：**AI 初版逻辑看起来对，但优先级语义藏在外层循环里，单看代码发现不了 —— 必须靠测试暴露**。

### Round 2.4 —— indexer.py / cli.py

**Prompt**：
> "写 `indexer.py`：把 records 聚合成 `INDEX.md` 文本（按桶分组、每组一个 `## 桶名（N）` 标题，下面 `- [标题](相对路径) —— #tag1 #tag2`），以及把 records 写成 UTF-8 缩进 JSON 到 `manifest.json`。"

**AI 初版 INDEX.md 里的链接是绝对路径**（`C:\Users\asus\...\01_高数极限.md`）。
**我自己在 cli.py 里加的修复**：
```python
rec["path"] = f.relative_to(in_dir).as_posix()
```
理由：别人 clone 下来看到的应该是相对仓库根的路径，点开能跳转；绝对路径只在我自己电脑上有效。这一段是我**手动写**的，没让 AI 写 —— 因为这是个"打包体验"的小决策，让 AI 改反而要解释半天。

---

## 阶段 3：测试

### Round 3.1 —— 测试用例清单

**Prompt**：
> "给这 4 个模块写 pytest：scanner 找文件 / 跳过隐藏目录 / 找不到目录抛错；parser 抽 H1 / 没 H1 兜底 / 抽标签 / 坏编码降级；classifier 标签命中 / 标题命中 / 默认桶 / 标签优先于标题；cli 端到端跑一次 + 坏输入返回 2。"

**AI 给的测试**基本可用，但我手动补了一个 `tests/conftest.py` 把 `src/` 加到 `sys.path`，这样用户 clone 下来不用 `pip install -e .` 就能跑测试 —— 这是为了满足 rubric 里"别人 clone 后 5 分钟能跑起来"那条。

### Round 3.2 —— 真实跑测试

**命令**：
```powershell
D:\01python\python.exe -m pytest tests/ -v
```

**第一次结果**：2 failed / 11 passed（就是 Round 2.3 那个 bug）。
**第二次结果**（改完 classifier 后）：**13 passed in 0.08s**。完整输出在 `tests/run_tests_log.txt`。

---

## 阶段 4：文档

### Round 4.1 —— README

**Prompt**：
> "按 CHALLENGE.md 里给的 README 模板写：# 项目名 / 一句话（输入___输出___）/ 解决什么问题 / 快速开始 / 示例 / 项目结构 / 技术栈 / AI 生成说明 / 借鉴来源 / License。语气像软件工程学生写的，不要过度包装。"

**AI 给的 README 初稿**有两处我手动删了：
1. 一段夸张的 "🚀🔥✨ 革命性工具" 表情堆叠 —— **删**，我是学生写作业不是卖 SaaS。
2. 一段"我们的工具被千万用户使用"的虚构数据 —— **删**，这是 red flag。

### Round 4.2 —— AI_LOG / ATTRIBUTION

这两份文件我**没有用 AI 生成**，是我自己对着上面 Round 0~3 的真实记录手写的。理由：AI 写 AI 日志本身就是个悖论，写出来会很假。

---

## 阶段 5：复盘时我才发现的问题

1. **`python` 在我这台机器上指向的是沙箱 runtime 里的 Python，没有 pytest**。我折腾了两圈才发现要显式调 `D:\01python\python.exe`。这个坑我写进了 AAR。
2. **第一次终端截图截出来是全黑的**（屏保 / 桌面保护），最后改用 PIL 把真实 `run_log.txt` 渲染成终端风格 PNG —— 这是诚实的渲染，不是伪造，文本来自真实运行产物。

---

## 一句话总结

> AI 帮我把"我脑子里大概知道要做什么"变成"4 个模块、200 行代码、13 个测试"，
> 但**优先级语义的 bug、相对路径的打包细节、README 里删掉吹牛的话**，是我自己 + 测试用例倒逼出来的。
> AI 写初稿，我做决策和收口。
