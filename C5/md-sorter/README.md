# md-sorter

> 一句话描述：**输入**一个装满 Markdown 笔记的目录，**输出**一份按主题自动分类的 `INDEX.md` 索引 + `manifest.json` 元数据清单。

[![tests](https://img.shields.io/badge/tests-13%20passed-brightgreen)]()
[![python](https://img.shields.io/badge/python-3.10%2B-blue)]()
[![license](https://img.shields.io/badge/license-MIT-lightgrey)]()

---

## 解决什么问题

作为软件工程专业的学生，我的笔记散落在好几个地方：课程笔记、四级错题、AI 学习心得、三下乡策划、心情随笔……文件名五花八门，时间一长根本想不起来"我那篇讲 Prompt 心得的笔记到底放哪了"。

**没有 md-sorter 之前**：打开文件夹 → 肉眼翻 → 一篇篇点开看标题 → 自己在脑子里归类。20 篇笔记翻完要 10 分钟，还经常漏。

**有了 md-sorter 之后**：一行命令，自动扫描、自动识别一级标题、自动抽取 `#标签`、自动按 7 个主题桶（课程笔记 / 作业与考试 / AI 与工具 / 项目与代码 / 活动与实践 / 生活与心情 / 读书笔记）分类，输出一份可以直接当目录用的 `INDEX.md`。

---

## 快速开始

### 安装

```bash
# 1. clone
git clone https://github.com/yihan110/tiaozhan.git
cd md-sorter

# 2. 本项目零第三方运行依赖，只需要 Python 3.10+
#    跑测试时才需要 pytest（可选）
python --version          # 确认 >= 3.10
pip install pytest        # 仅跑测试时需要
```

> 不需要 `pip install -e .`，直接把 `src/` 加到 `PYTHONPATH` 即可运行（见下）。

### 使用

```bash
# Windows PowerShell
$env:PYTHONPATH="src"
python -m md_sorter 你的笔记目录 -o 输出目录

# macOS / Linux
PYTHONPATH=src python -m md_sorter 你的笔记目录 -o 输出目录
```

最简示例（用仓库自带的 sample_notes 跑一遍）：

```bash
$env:PYTHONPATH="src"
python -m md_sorter examples/sample_notes -o examples/sample_output
```

---

## 示例

**输入**：`examples/sample_notes/` 下 5 篇随手写的 Markdown 笔记（课程 / 考试 / AI / 活动 / 心情各一篇）。

**输出**：`examples/sample_output/INDEX.md`（节选）

```markdown
# Markdown 笔记索引

- 扫描目录: `.../examples/sample_notes`
- 共收录 **5** 篇 Markdown 文件

## 课程笔记（1）
- [高数第二章 极限与连续](01_高数极限.md)  —— #课程 #高数

## AI 与工具（1）
- [用 Claude 写 Prompt 的一点心得](03_AI心得.md)  —— #ai #claude #prompt

## 活动与实践（1）
- [三下乡活动策划初稿](04_三下乡策划.md)  —— #三下乡 #志愿 #活动
...
```

同时输出 `manifest.json`，结构化记录每篇笔记的标题、标签、字节数、行数、所属主题，方便后续做二次处理。

**真实运行截图**（本机 Windows + Python 3.13 实跑）：

![terminal run](examples/terminal_run.png)

---

## 项目结构

```
md-sorter/
├── README.md
├── LICENSE                  MIT
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── AI_LOG.md                AI 使用日志
├── ATTRIBUTION.md           借鉴来源
├── requirements.txt
├── src/
│   └── md_sorter/
│       ├── __init__.py
│       ├── __main__.py       支持 python -m md_sorter
│       ├── cli.py            命令行入口
│       ├── scanner.py        递归扫描 .md 文件
│       ├── parser.py         解析一级标题与 #标签
│       ├── classifier.py     按主题桶分类
│       └── indexer.py       生成 INDEX.md / manifest.json
├── examples/
│   ├── sample_notes/         5 篇真实风格示例笔记
│   ├── sample_output/        真实运行产物
│   ├── run_log.txt           真实终端输出
│   └── terminal_run.png      真实运行截图
├── tests/
│   ├── test_scanner.py
│   ├── test_parser.py
│   ├── test_classifier.py
│   ├── test_cli.py
│   └── run_tests_log.txt     pytest 真实运行记录
└── .github/
    └── ISSUE_TEMPLATE/
        ├── bug_report.md
        └── feature_request.md
```

---

## 技术栈

- 语言：Python 3.10+（实际在 3.13 上验证）
- 标准库：`pathlib` / `argparse` / `re` / `json` / `collections` —— **零第三方运行依赖**
- 测试：`pytest`（仅开发期）
- 不依赖任何 LLM API —— 分类规则是硬编码的关键词表，跑起来不需要联网

---

## AI 生成说明

本项目使用 AI（豆包 / Claude）辅助开发，详细的多轮 prompt、迭代过程、踩坑记录见 [AI_LOG.md](./AI_LOG.md)。

## 借鉴来源

本项目参考了以下来源，逐项说明 adopted / removed / improved，见 [ATTRIBUTION.md](./ATTRIBUTION.md)。

## License

[MIT](./LICENSE)
