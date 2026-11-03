# 阮依涵_C5A_仓库分析：neolaf2/neoskills

> 分析对象：https://github.com/neolaf2/neoskills
> 分析人：阮依涵（郑州西亚斯学院 数字技术产业学院 软件工程 2025 级）
> 分析日期：2026-11-01
> 调研方式说明：本机网络无法直连 github.com / raw.githubusercontent.com（请求超时），
> `git clone` 三次均因网络/确认通道未能完成。为保证分析真实可核对，本报告改为通过
> jsDelivr 公开 CDN 镜像抓取该仓库 `@main` 分支的 **README.md 全文、完整文件树（flat 结构）、
> 以及 skills/ 下两个 SKILL.md 原文** 进行分析。所有引用均给出可复核的真实 URL。

---

## 一、这个仓库是做什么的？（一句话概括）

**neoskills 是一个「Homebrew 风格、面向 AI 编程 Agent 的技能（skill）包管理器」**：
它用一条命令行工具（Python 编写，可 `pip install neoskills`，要求 Python 3.13+），
把分散在各个 git 仓库里、供不同 AI Agent（Claude Code、OpenCode、OpenClaw）使用的"技能"
统一管理——一键浏览、搜索、安装（软链部署）、创建，并用一套本体（ontology）属性图来
描述技能之间的依赖、组成、版本与生命周期关系。

> 一句话版：**neoskills = AI Agent 世界里的 Homebrew + 一个可查询的"技能关系图"。**

- 许可证：MIT；作者：Richard Tong；已发布到 PyPI（`pip install neoskills`）。
- 项目自述原文：*"Homebrew-style skill manager for AI coding agents. Browse skills in one place,
  sync to GitHub, deploy selectively via symlinks, and discover relationships through a built-in ontology graph."*
- 来源：https://cdn.jsdelivr.net/gh/neolaf2/neoskills@main/README.md （镜像自 github.com/neolaf2/neoskills）

---

## 二、仓库的目录结构是怎样的？

以下为通过 jsDelivr 数据接口 `data.jsdelivr.com/v1/packages/gh/neolaf2/neoskills@main?structure=flat`
拉取的真实文件树（共 112 个文件）整理而成。

### 2.1 仓库根目录

```
neoskills/
├── .github/              # GitHub Actions CI 等工作流
├── .claude-plugin/       # Claude 插件清单
├── agents/               # Agent 相关定义
├── commands/             # 命令（commands 目录）
├── docs/                 # 设计文档（如 ontology-design.md）
├── skills/               # 仓库自带的技能示例（仅 2 个，见第三节）
├── src/neoskills/        # ★ 核心源码（Python 包）
├── tests/                # 测试（README 称 172 个测试，12 个测试模块）
├── .gitignore
├── .python-version
├── CLAUDE.md             # 面向 Claude 的项目说明
├── Dockerfile
├── LICENSE               # MIT
├── main.py               # 入口
├── neoskills_v0_1.md     # 各版本发布说明（v0.1 / v0.2 / v0.3 / v0.21）
├── pyproject.toml        # 打包/依赖配置
├── README.md             # 项目主文档
├── TASKS.md              # 待办任务
└── uv.lock               # uv 锁定文件
```

### 2.2 核心源码包 `src/neoskills/`（这是真正的"产品"）

```
src/neoskills/
├── cli/                  # Click 命令行（用户敲的 neoskills 指令都在这里注册）
│   ├── main.py           # 入口与命令注册
│   ├── tap_cmd.py        # 加/删/更新 tap（git 仓库源）
│   ├── list_cmd.py / search / info
│   ├── create_cmd.py     # 脚手架新建技能（生成 SKILL.md + ontology.yaml）
│   ├── link_cmd.py       # 软链部署到 Agent
│   ├── ontology_cmd.py   # 17 个 ontology 子命令
│   ├── doctor_cmd.py     # 健康检查
│   ├── enhance_cmd.py / agent_cmd.py / plugin_cmd.py / schedule_cmd.py ...
├── core/                 # 基础能力：config、workspace、tap、linker(软链)、
│                         #   checksum(SHA256)、frontmatter(读 SKILL.md 头部)、
│                         #   manifest、models、resolver、namespace、auth
├── ontology/             # ★ 本体属性图层（v0.4 核心亮点）
│   ├── models.py         # SkillNode / OntologyEdge 等数据类与枚举
│   ├── graph.py         # 内存中的属性图 SkillGraph
│   ├── loader.py / writer.py   # 文件系统 ↔ 图 双向读写
│   ├── engine.py         # 高层 API：OntologyEngine
│   ├── taxonomy.py       # 领域分类（agent-architecture / education / document-processing...）
│   ├── lifecycle.py      # 技能状态机：candidate→validated→operational→refined→deprecated→archived
│   ├── versioning.py    # 语义化版本 major/minor/patch
│   ├── composition.py    # 技能组合/拆分（compose / split）
│   ├── export.py        # 导出 Mermaid / DOT / JSON / ASCII 树
│   └── templates/       # ontology.yaml 模板
├── adapters/            # 多 Agent 适配：claude / opencode / openclaw + factory
├── runtime/claude/       # Claude MCP 插件（暴露 12+ 工具）
├── meta/enhancer.py     # Claude 驱动的技能增强
├── plugin/              # 插件上下文与 schema
└── translators/
```

### 2.3 它是怎么"跑起来"的（从 README 提炼的设计思路）

1. **工作区**：`neoskills init` 生成 `~/.neoskills/`，里面放 `config.yaml`、`taps/`（git 克隆来的技能源）、`cache/`。
2. **部署模型**：技能不是"复制"过去，而是**软链接**到 Agent 的技能目录，例如
   `~/.claude/skills/kstar-loop -> ~/.neoskills/taps/.../skills/kstar-loop`。
   好处：单一数据源、可同时挂给多个 Agent、改一处即时生效、`unlink` 即可秒级回滚。
3. **技能最小单元**：一个文件夹 + 一个 `SKILL.md`（YAML frontmatter：name/description/author/tags/targets + 正文指令），
   可选配 `ontology.yaml` 记录图关系。
4. **本体图**：把所有技能当作"节点"，用 `requires / extends / composes_with / conflicts_with / supersedes / derived_from`
   这几类"有类型的边"连成一张图，支持依赖查询、冲突校验、生命周期管理、Mermaid 可视化。

---

## 三、里面有哪些技能（skills）？各自做什么？

> 注意：这个仓库的**主体是"技能管理器"这个工具本身**（即 src/neoskills/）；
> `skills/` 目录里只随仓库自带了 **2 个示例/内置技能**。下面逐一分析（原文来自各自 SKILL.md）。

### 技能 1：`bank-status`（技能库状态查询）

- **触发场景**：用户问"技能库里现在有哪些技能 / 库存盘点 / 有哪些技能可用"。
- **做什么**：读取 `~/.neoskills/registry.yaml`（技能目录）和 `~/.neoskills/state.yaml`（当前已嵌入的技能），
  统计技能总数、标签、最近更新时间，列出已配置的目标 Agent。
- **输出格式**：一段摘要——**Bank**（总数+更新时间）、**Targets**（各目标 Agent 及技能数）、
  **Embedded**（当前软链进来的技能）、**Recent**（最近导入的 5 个技能及来源）。
- **本质**：一个**只读的"仪表盘"型技能**，不改动任何东西，只做汇报。

### 技能 2：`skill-dedup`（技能去重 / 查重）

- **触发场景**：用户提到"技能重复了、想清理技能库、导入技能时担心和已有重复、想审计冗余技能"。
- **做什么**：扫描 neoskills 技能库、各 Agent 目录（Claude Code `~/.claude/skills`、OpenCode `~/.config/opencode/skills`）、
  插件目录以及指定的 GitHub 仓库，找出重复和近似重复的技能，再用"合并/删除/保留"策略解决。
- **自带可执行脚本**：`scripts/dedup_scan.py`（这是两个技能里唯一带真代码的）。
- **把重复分成三类**：
  1. **完全重复（Exact）**：内容 SHA256 完全一致 → 安全合并，以库内副本为准，目标副本换成软链。
  2. **已分叉副本（Diverged）**：同一个技能 ID 存在多处但内容不同 → 脚本挑出"更丰富"的一份，建议导入库内。
  3. **名字相近组（Name-Similar）**：不同技能 ID 但名字/描述相似 → 需要人工判断。
- **能力亮点**：支持 `--resolve exact|diverged|all` 自动处理、`--dry-run` 先预览不动手、
  `--threshold 0.80` 相似度阈值、`--json` 机器可读输出，且自动备份为 `.<skill>.dedup-backup`。
- **本质**：一个**带脚本、可自动执行、可回滚**的"运维型技能"。

---

## 四、我觉得哪个技能最有意思？为什么？

**我觉得最有意思的是 `skill-dedup`。** 理由有四点：

1. **它真的"动手"，而不只是"动嘴"。**
   `bank-status` 只是把文件读出来念一遍；而 `skill-dedup` 自带 `scripts/dedup_scan.py`，
   是两个技能里唯一附带可执行代码的。这让我第一次直观理解了"SKILL.md 里的正文，
   其实是在指挥 Agent 去跑一段真实脚本"——技能 = 说明书 + 可执行资产。

2. **它解决了一个会真实发生的痛点。**
   当你同时在 Claude Code、OpenCode、各种插件里都装技能时，重复安装、版本分叉几乎是必然的。
   它用 **SHA256 判全等 + 相似度阈值判近似** 这种很"工程"的办法，把模糊的"好像重复了"
   拆成 Exact / Diverged / Name-Similar 三类，处理策略也分层（能自动的自动、要人工的标人工），
   这种"机器先做 80%、人来做最后判断"的分工设计很聪明。

3. **它贯彻了整个仓库的设计哲学——软链与零复制。**
   去重时它不是删文件，而是"把目标副本换成指向库内正本的软链"，并且先 `--dry-run` 预览、
   再留 `.dedup-backup` 备份。这种"可逆、可审计、不破坏"的操作方式，和我在 README 里读到的
   `link/unlink 秒级回滚` 完全一致，让我看到了一个工程理念是怎么在不同模块里一致落地的。

4. **它让我想到自己以后能写什么技能。**
   作为软件工程专业的学生，我意识到"技能"门槛并不高：写一个 SKILL.md 说清"什么时候触发、
   按什么步骤做、输出长什么样"，再配一个小脚本就行。我完全可以以后为自己常用的
   OCR 整理作业、试卷录入这类重复劳动写一个专属技能——这正是这个仓库给我的最大启发。

---

## 五、参考来源（均可复核）

| 用途 | 来源 |
|---|---|
| 项目定位、架构、CLI、本体图设计 | README.md 全文：https://cdn.jsdelivr.net/gh/neolaf2/neoskills@main/README.md （镜像自 github.com/neolaf2/neoskills） |
| 完整目录树（112 个文件） | jsDelivr 数据接口：https://data.jsdelivr.com/v1/packages/gh/neolaf2/neoskills@main?structure=flat |
| 技能 bank-status 原文 | https://cdn.jsdelivr.net/gh/neolaf2/neoskills@main/skills/bank-status/SKILL.md |
| 技能 skill-dedup 原文 | https://cdn.jsdelivr.net/gh/neolaf2/neoskills@main/skills/skill-dedup/SKILL.md |
| 官方仓库主页（fork 目标） | https://github.com/neolaf2/neoskills |

> 诚实声明：本机因网络原因未能完成 `git clone` 到本地，故本报告基于上述公开镜像抓取的真实
> README / 文件树 / SKILL.md 内容撰写，未编造任何目录或技能细节。待本人在可联网环境用自己的
> GitHub 账号 fork 并 clone 后，可与本报告逐项对照验证。
