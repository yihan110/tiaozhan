# ruanyihan_C10H AI 日志

> 作者：阮依涵（ruanyihan）
> 说明：本日志记录我在完成 C10H 过程中，如何用 AI（本助手）分阶段、多轮迭代地调研与撰写。每条包含：阶段、我给的 prompt、AI 给的关键产出、我下一轮怎么改。**这不是一句话指令直接提交**，而是多轮打磨。

---

## 阶段 0：读懂任务，定边界

- **我给的 prompt**："先别动手，把挑战资料包里的 CHALLENGE.md、rubric.json、challenge.json、README.md、C10H.pdf 全部读完，告诉我：到底要交哪几个文件、满分标准卡哪几条红线、本机 Windows 能不能直接装 Hermes。"
- **AI 产出**：列出 8 个必交文件（安装配置指南/SOUL定制/自定义技能/cron示例/AI日志/拿来说明/AAR/提交说明），点出 rubric 五条维度（驾驭25/集成20/完整性15/AI使用20/复盘20），以及三条红 flag（缺产物、无AI日志、一句话AI）。并指出 Hermes 官方要求 Linux/macOS/WSL2，本机 Windows 原生不能直接装。
- **我下一轮怎么改**：决定不伪造"已安装成功"，而是把"文档+调研做到满分，真实安装环节如实标注需要用户在 WSL2 补"。

## 阶段 1：环境真实验证

- **我给的 prompt**："在本机真实跑一下 python --version 和 wsl --status，把结果原文给我，别猜。"
- **AI 产出**：`Python 3.13.16`；`wsl --status` 退出码 50，提示"未安装用于 Linux 的 Windows 子系统"。
- **我下一轮怎么改**：把这两个真结果写进安装指南第 6 节作为证据，并据此把"启用 WSL2+重启"列为需用户本人执行的环节，而不是我代做。

## 阶段 2：调研 Hermes 是什么（第一轮 prompt）

- **我给的 prompt**："去网上查 Hermes Agent：官方仓库、官方文档、它到底是什么、支持哪些平台、记忆和技能机制。要真实 URL，不要编。"
- **AI 产出**：仓库 github.com/NousResearch/hermes-agent；中文文档 hermes-agent.nousresearch.com/docs/zh-Hans；MIT；核心是自我进化 Agent，记忆=SQLite+FTS5，技能兼容 agentskills.io，内置 cron。
- **我下一轮怎么改**：第一轮只拿到概览，不够写"可照做"的指南，于是要求抓具体安装命令和 Windows 说明。

## 阶段 3：调研安装方式（第二轮，发现关键新事实）

- **我给的 prompt**："把官方中文文档首页抓下来，重点看安装命令、Windows 到底支不支持、一键脚本具体装了什么。"
- **AI 产出**：Linux/macOS/WSL2 用 `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`；**新发现**官方已加原生 Windows PowerShell 早期测试版 `iex (irm https://hermes-agent.nousresearch.com/install.ps1)`；脚本自动装 uv+Python3.11、clone 仓库、无需 sudo。
- **我下一轮怎么改**：这里有个判断——CHALLENGE.md 说"不支持原生 Windows"，但文档新增了早期测试版。我决定：**主路径仍走 WSL2（官方一级支持、与挑战一致），但把 PowerShell 早期测试版作为诚实备注写进指南**，不瞒着用户。

## 阶段 4：调研 SOUL.md 机制

- **我给的 prompt**："抓官方 SOUL.md 文档，告诉我它放在哪、系统提示词里排第几、该写什么不该写什么、有哪些内置 personality。"
- **AI 产出**：路径 `~/.hermes/SOUL.md`；占系统提示词第 1 槽位（身份）；只从 HERMES_HOME 加载；写语气/风格，不写项目路径（那是 AGENTS.md）；内置 helpful/concise/technical/teacher/kawaii 等 14 种；可用 `/personality` 会话级切换。
- **我下一轮怎么改**：拿到"该写/不该写"清单后，我把 SOUL 定制从"通用助手"改成贴合我身份的"软件工程学生的学习+社团+竞赛搭档"，并加了"不编造事实、不替我做系统级/付费决定"的边界。

## 阶段 5：调研技能系统，定技能格式

- **我给的 prompt**："抓官方 skills 文档，给我 SKILL.md 的精确 frontmatter 格式、目录结构、怎么让它生效、和 memory 的区别。"
- **AI 产出**：目录 `~/.hermes/skills/<分类>/<技能名>/SKILL.md`；frontmatter 含 name/description/version/metadata.hermes.tags/category；放进去即生效、变斜杠命令；按需 `skill_view` 加载省 token。
- **我下一轮怎么改**：最初我想写个"万能学习助手"技能，但官方 best practice 说"技能要聚焦，别太宽"。于是改成只做我高频的一件事——"试卷 OCR 题目保真整理"，并把我长期的硬规矩（不改原文、存疑标注、题型分开）写进 Core Rules。

## 阶段 6：调研 cron 机制

- **我给的 prompt**："Hermes 的定时任务怎么配？是不是要手写 cron 表达式？任务重启后还在吗？"
- **AI 产出**：内置 cron，gateway daemon 每 60 秒 tick；任务跨重启存活；**支持自然语言调度**，你说"每天早 8 点提醒我"它自己转成表达式；投递到任意平台。
- **我下一轮怎么改**：据此把 cron 示例写成"主推自然语言一句话 + 附等价 cron 表达式讲解"两条路，而不是只丢一个 `0 8 * * *` 让用户懵。

## 阶段 7：组装文档 + 自检

- **我给的 prompt**："按拼音命名 ruanyihan_C10H_xxx，把 8 个文件写进提交文件夹，然后打包 zip，再用 python zipfile 列出包内容核对每个文件都在且非空。"
- **AI 产出**：建文件夹、写 8 个 md、压缩、自检清单。
- **我下一轮怎么改**：自检若发现有空文件或命名不符（必须 ruanyihan 拼音开头），就补写/改名，再压一次。

---

## 迭代小结

| 阶段 | 轮次 | 关键改进 |
|---|---|---|
| 定边界 | 1 | 从"照做安装"改为"文档满分+真实环境环节如实标注" |
| 环境 | 1 | 真跑命令，不猜 |
| 调研 | 3 轮 | 概览 → 抓安装细节 → 发现 Windows 早期测试版并诚实备注 |
| SOUL | 2 轮 | 通用 → 贴合身份+加安全边界 |
| 技能 | 2 轮 | 宽泛"学习助手" → 聚焦"OCR 保真整理" |
| cron | 2 轮 | 只给表达式 → 自然语言+表达式双路径 |
