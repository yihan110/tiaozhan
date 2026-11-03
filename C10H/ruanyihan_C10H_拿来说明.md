# ruanyihan_C10H 拿来说明

> 作者：阮依涵（ruanyihan）
> 原则：拿来主义——说清"拿了什么、参考了哪个来源、改了哪里"。

---

## 一、我"拿"了什么

整个 **Hermes Agent 平台**（Nous Research 开源，MIT 协议）。它不是我自己造的，我是直接拿这个成熟的 Agent 操作系统来用，并在上面做个人化配置。

---

## 二、参考来源清单（真实 URL + 参考了什么 + 改了哪里）

| # | 来源 URL | 我参考了什么 | 我改了/加了什么 |
|---|---|---|---|
| 1 | https://github.com/NousResearch/hermes-agent | 项目本体、源码、README、安装脚本入口 | 没改源码；只在本机文档层面做 WSL2 中文安装指引 |
| 2 | https://hermes-agent.nousresearch.com/docs/zh-Hans/ | 官方中文文档首页：安装命令、功能列表、架构 | 把英文/官方条目翻成针对"软件工程大一学生"的落地步骤；补充 Windows→WSL2 的完整启用流程 |
| 3 | https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/features/personality | SOUL.md 的作用、路径、该写/不该写、内置 personality | 把默认通用人格，换成贴合我身份的 `~/.hermes/SOUL.md`（见《SOUL定制》），加了"不编造、不替我做系统级决定"的边界 |
| 4 | https://hermes-agent.nousresearch.com/docs/zh-Hans/guides/work-with-skills | SKILL.md frontmatter 格式、目录结构、生效方式、与 memory 区别 | 照其规范手写了 `exam-ocr-cleanup` 技能（见《自定义技能》），把我长期的 OCR 保真规矩固化进去 |
| 5 | 社区/文档关于内置 cron 的说明（hermesbible.com、官方"定时自动化"条目） | gateway daemon 每 60 秒 tick、任务跨重启存活、支持自然语言调度 | 据此写了《cron示例》：主推自然语言一句话 + 附 `分 时 日 月 周` 表达式速查，做四级每日提醒 |
| 6 | https://openrouter.ai | LLM provider 选择（200+ 模型、有免费额度、一个 Key 通用） | 推荐自己用 OpenRouter 起步；写了申请 Key 的步骤（2.4 节） |
| 7 | https://agentskills.io | 技能开放标准（保证我的自定义技能可移植、日后可发布） | 我的 SKILL.md 按该标准写，便于将来发布到 Skills Hub |

---

## 三、哪些是"原版照抄"，哪些是"我的改动"

- **照抄（不创造，直接用）**：一键安装命令 `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`、`hermes setup` / `hermes model` / `hermes tools` 等命令、`~/.hermes/` 目录布局、SOUL.md 与 SKILL.md 的官方格式。
- **我的改动/再创作**：
  1. 把官方"Linux/macOS/WSL2"抽象说明，**展开成 Windows 用户从零启用 WSL2 的分步中文指引**（控制面板功能开关、`wsl --install`、重启、`wsl -l -v` 验证）。
  2. 把**已知坑**（PATH 不生效、国内网络代理、虚拟化未开、401/402 Key 问题）写成排错清单。
  3. SOUL.md 全部内容按我的身份重写。
  4. 自定义技能 `exam-ocr-cleanup` 是我针对自己高频需求写的，官方没有。
  5. cron 用"四级每日词汇+待办摘要"这个具体场景落地，不是泛泛例子。

---

## 四、诚实标注：本机没"拿"起来的部分

- 我**没有**在本机真实 clone 仓库、跑 install.sh、连上真实 LLM——因为本机未装 WSL2、也没有 API Key（见《安装配置指南》第 0、6 节证据）。
- 所以本文档交付的是"**拿来的方法 + 可照做的配置模板**"，真正在你机器上把 Hermes 跑起来那一步，需要你按指南在 WSL2 里完成后补截图。这不是"拿了不用"，而是"拿的姿势和定制先准备好，执行在你的真实环境"。
