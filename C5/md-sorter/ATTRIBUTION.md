# ATTRIBUTION —— 借鉴来源说明

> 本项目遵循"拿来主义"：站在巨人的肩膀上，但每一处借鉴都标注清楚 —— **参考了什么、用了多少、改了哪里**。
> 格式：`adopted` = 直接采用；`removed` = 看了但没用；`improved` = 参考后按自己需求改造。

---

## 1. Python 官方文档

| 来源 | 参考了什么 | 处理 |
|------|-----------|------|
| [os.walk 文档](https://docs.python.org/3/library/os.html#os.walk) | "想剪枝就原地修改 `dirnames`" 这个标准做法 | **adopted**：`scanner.py` 里 `dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]` |
| [pathlib 文档](https://docs.python.org/3/library/pathlib.html) | `Path.glob` / `Path.relative_to` / `Path.read_text(encoding=...)` 的 API 形态 | **adopted**：全程用 pathlib 不用 os.path |
| [re 文档](https://docs.python.org/3/library/re.html) | 正则 `(?<!...)` 负向后顾、Unicode 字符类 | **improved**：AI 初版给的 `r"#(\w+)"` 太粗，我参考文档改成 `(?<!\w)#([\u4e00-\u9fa5A-Za-z]...)` 避免误抓一级标题 |
| [argparse 文档](https://docs.python.org/3/library/argparse.html) | `add_argument` / `--version` 动作 | **adopted**：cli.py 直接照文档模板写 |

## 2. 社区惯例

| 来源 | 参考了什么 | 处理 |
|------|-----------|------|
| [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) | CHANGELOG 的小节结构（Added / Changed / Fixed） | **adopted**：CHANGELOG.md 直接用 |
| [MIT License 全文](https://opensource.org/license/mit) | LICENSE 标准文本 | **adopted**：只改了版权行（`Copyright (c) 2026 Wang Wanhuan`） |
| GitHub 官方 `python.gitignore` 模板 | 该忽略什么 | **improved**：AI 给了一份很长的完整版（含 PyInstaller、Jupyter、mypy 配置），**removed** 掉我用不到的项，精简到 12 行 |
| GitHub 官方 Issue 模板（`bug_report.md` / `feature_request.md`） | 字段结构 | **improved**：把英文模板翻译成中文，加了"贴目录 tree"这种针对本项目的提示 |

## 3. AI 工具

| 来源 | 参考了什么 | 处理 |
|------|-----------|------|
| 豆包 / Claude 在 Round 2.1~2.4 给出的代码初稿 | 模块划分、函数签名、注释语气 | **improved**：scanner 的剪枝方式、parser 的正则、classifier 的两轮判定，都是 AI 初稿 + 我改 bug 后的产物。**没有一行代码是没经过我审校直接 commit 的** |
| CHALLENGE.md 里给的 README 模板 | README 章节顺序 | **adopted**：严格按模板章节写，但**removed** 了 AI 初稿里夸张的表情和虚构数据 |
| CHALLENGE.md 里的 `wechat-doc-mapper` 示例 | "扫描目录 → 映射 → 输出索引" 这个产品形态 | **improved**：示例是扫微信文件夹映射到挑战；我改成扫笔记目录映射到主题桶，思路借鉴但场景完全换了 |

## 4. 未借鉴的部分（反向举证）

- **classifier 的 7 个主题桶关键词表**：完全是我自己对着"我和我同学平时怎么给笔记分类"列出来的，没有抄任何现成的标签体系。
- **INDEX.md 的输出格式**：自己设计的"标题（N）→ 列表 → 标签尾巴"，没抄任何别的工具。
- **README 里"解决什么问题"那两段**：写的是我自己整理笔记的真实痛点（四级错题、三下乡策划、心情随笔），不是 AI 编的。

---

## 一句话

> 工具和文档是站在别人肩膀上的，**产品形态和痛点是我自己的**。
> 这就是拿来主义 —— 不是抄，是把别人成熟的轮子装到自己真实的车上。
