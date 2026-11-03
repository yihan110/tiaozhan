# ruanyihan_C10H 安装配置指南

> 作者：阮依涵（ruanyihan）｜郑州西亚斯学院 数字技术产业学院 软件工程专业 2025 级
> 挑战：C10H 安装并驾驭 Hermes Agent
> 文档性质：**可照做的安装配置记录 + 踩坑清单**
> 编写日期：2026-11-01

---

## 0. 状态标注（先看这里，诚实原则）

本指南在一台 **Windows 原生**电脑上编写。Hermes Agent 的官方安装脚本是 bash 脚本，原生 Windows 不被一级支持（官方文档主路径为 Linux / macOS / WSL2）。

| 环节 | 在本机（当前 Windows）的真实状态 |
|---|---|
| 编写本文档、调研官方文档、核实命令与机制 | ✅ **已真实完成** |
| 检查本机 Python 版本 | ✅ 已真实验证：`Python 3.13.16` |
| 检查本机 WSL 状态 | ✅ 已真实验证：**WSL 未安装**（`wsl --status` 返回退出码 50，提示"未安装用于 Linux 的 Windows 子系统"） |
| 启用 WSL2、安装 Ubuntu、重启电脑 | ⏳ **需要用户本人在真实环境执行**（涉及重启与系统功能开关，不在本机代做） |
| 申请 OpenRouter / Nous Portal 的 LLM API Key | ⏳ **需要用户本人注册并付费/领免费额度** |
| 在 WSL2 里跑 install.sh、`hermes setup`、首次 CLI 对话 | ⏳ **需要用户在 WSL2 真实环境执行** |
| 截图/录屏安装过程、真实跑通对话 | ⏳ **需要用户真实环境执行后补截图** |

> ⚠️ 本文档**不伪造**任何"安装成功"的终端输出。下面的"预期输出"是根据官方文档与脚本行为写出的**期望值**，不是本机真实跑出来的结果。凡是本机真实验证过的，都在第 6 节附了证据。

---

## 1. Hermes Agent 是什么 / 架构 / 为什么需要它

### 1.1 一句话定义

Hermes Agent 是 **Nous Research** 出品的开源（MIT 协议）"自我进化型" AI Agent 平台。它不是聊天机器人，而是一个会**跨会话记忆你、自动把重复任务沉淀成技能、能定时自动干活、能在多个消息平台上替你工作**的数字分身。

- 官方仓库：https://github.com/NousResearch/hermes-agent
- 官方文档（中文）：https://hermes-agent.nousresearch.com/docs/zh-Hans/
- 技能标准：https://agentskills.io （兼容开放标准，技能可移植可分享）

### 1.2 为什么 C10H 要"拿"它来用

从零自己搭一个 Agent，要同时解决：记忆管理、工具调用、多平台接入、技能系统、定时调度——这是一堆基础设施脏活。Nous Research 已经把这些做完了（社区星标高、MIT 协议、有活跃文档）。C10H 的核心是**拿来主义 + 系统驾驭**：先学会用、学会排错、学会定制，而不是重复造轮子。

### 1.3 架构（来自官方文档与 CHALLENGE.md）

```
你（用户）
  │  CLI(TUI) / Telegram / Discord / Slack / WhatsApp / Signal …（20+ 平台）
  ▼
Gateway（统一消息网关，常驻后台，每 60 秒 tick 一次）
  │
  ▼
HERMES AGENT CORE
  ├─ LLM Provider：OpenRouter / Nous Portal / OpenAI / 任意兼容端点（模型无关）
  ├─ Memory 记忆系统：SQLite + FTS5 全文搜索、MEMORY.md、USER.md、LLM 摘要回忆
  ├─ Skills 技能系统：自动沉淀技能 + 手动技能，兼容 agentskills.io
  ├─ Tools 工具集：70+ 内置工具（文件、网络、搜索、代码执行、图像、TTS…）
  ├─ Cron 定时调度：自然语言描述即可，任务跨重启存活，投递到任意平台
  ├─ Terminal Backend：Local / Docker / SSH / Modal / Daytona（可远程/无服务器）
  └─ SOUL.md：人格定义（系统提示词第 1 槽位，决定它是谁、怎么说话）
```

**三个必须记住的机制点（Level 1 必答题答案）：**

1. **记忆存在哪？** 持久记忆落在 `~/.hermes/` 目录下的 SQLite 数据库（带 FTS5 全文索引），外加 `MEMORY.md`（关键事实便签）和 `USER.md`（它对你的用户建模）。会话内容被 LLM 摘要后跨会话召回。
2. **`SOUL.md` 是干什么的？** 它是 Agent 的**主要身份文件**，占据系统提示词的第 1 个槽位。定义它的语气、风格、行为准则。路径是 `~/.hermes/SOUL.md`（自定义主目录则是 `$HERMES_HOME/SOUL.md`）。它**只从 HERMES_HOME 加载**，不会从你启动它的当前目录加载，保证人格稳定。
3. **`hermes tools` 有多少工具？** 官方文档现版本写的是 **70+ 内置工具**（CHALLENGE.md 写作时是 40+）。真实数量以你装好后 `hermes tools` 的输出为准——这也是需要在真实环境补的一个数。

---

## 2. 安装前准备

### 2.1 环境要求（官方前置条件）

| 条件 | 要求 | 本机现状 |
|---|---|---|
| 操作系统 | Linux / macOS / **WSL2**（不支持原生 Windows 一级支持） | Windows 原生 → 需要装 WSL2 |
| Python | 3.11+（安装脚本会自动用 uv 装 3.11，一般不用你操心） | 本机 Windows 侧 Python 3.13.16（仅作参考，Hermes 跑在 WSL 里） |
| Node.js | 需要 | 安装脚本自动处理 |
| LLM API Key | 至少一个 | 需自行申请，见 2.4 |
| 网络 | 能访问 GitHub | 国内网络可能需要代理，见 5.2 坑 |

> 📌 **一个诚实的新发现**：我调研时（2026-11）发现官方文档已经新增了**原生 Windows（PowerShell）早期测试版**安装入口：
> `iex (irm https://hermes-agent.nousresearch.com/install.ps1)`
> 但 CHALLENGE.md 明确写"不支持原生 Windows"，且官方标注该 PowerShell 版为**早期测试版**。**稳妥起见，本指南走 WSL2 这条官方一级支持路径**。如果你愿意尝鲜原生 PowerShell 测试版，可作为备选，但排错难度更高、不在本指南保证范围内。

### 2.2 在 Windows 上启用 WSL2（完整分步）

> 这一步需要**管理员权限的 PowerShell**，且最后要**重启电脑**。属于系统级改动，按你的要求我没有代做，下面是给你照做的步骤。

**第 1 步：以管理员身份打开 PowerShell**
- 开始菜单搜 "PowerShell" → 右键 → "以管理员身份运行"。

**第 2 步：一键安装 WSL + 默认 Ubuntu**
```powershell
wsl --install
```
- 这条命令会自动：启用"虚拟机平台"和"适用于 Linux 的 Windows 子系统"两个 Windows 功能 → 下载内核 → 把默认发行版设为 Ubuntu。

**第 3 步：重启电脑**（命令行会提示你重启）。

**第 4 步：重启后**会自动弹出 Ubuntu 窗口，让你设置一个 Linux 用户名和密码（这个密码是 sudo 用的，记牢）。

**第 5 步：验证 WSL2 就绪**（重启后再开一个普通 PowerShell）：
```powershell
wsl --status
wsl -l -v
```
- 预期：`wsl -l -v` 里能看到 `Ubuntu` 且 `STATE` 为 `Running`、`VERSION` 为 `2`。
- 如果你这一步之前的报错就是本文档第 6 节记录的"未安装 WSL"，跑完上面流程后它会变成正常状态。

**手动开关功能的兜底做法**（如果 `wsl --install` 因组策略/公司电脑失败）：
1. 控制面板 → 程序 → 启用或关闭 Windows 功能 → 勾选：
   - ☑ 适用于 Linux 的 Windows 子系统
   - ☑ 虚拟机平台
2. 确定后重启，再执行 `wsl --install -d Ubuntu`。

> 硬件要求：需要 CPU 支持虚拟化（Intel VT-x / AMD-V）。进 BIOS 确认虚拟化已开。若 `wsl --install` 报"虚拟化未启用"，就是这个问题。

### 2.3 进入 WSL 环境

装好后，在 PowerShell 里输入：
```powershell
wsl
```
就进入了 Ubuntu 的 bash 终端（提示符变成 `你的用户名@机器名:~$`）。**下面所有 Hermes 安装命令，都在这个 WSL 的 bash 里跑，不要再在 Windows PowerShell 里跑。**

### 2.4 获取 LLM API Key（推荐 OpenRouter）

1. 打开 https://openrouter.ai → 注册/登录。
2. 右上角 → Keys → Create Key，复制那串 `sk-or-v1-...`。
3. OpenRouter 一个 Key 可调用 200+ 模型，有免费额度模型（如 `:free` 后缀的），学生起步零成本。
4. （备选）Nous Portal：https://portal.nousresearch.com ，Hermes 原生兼容；OpenAI：https://platform.openai.com 。
5. 把 Key 存好（不要提交进 git，不要写进本文档）。

---

## 3. 完整安装配置分步记录

> 以下命令全部在 **WSL2 的 bash** 里执行。"预期输出"为依据官方文档的期望值，非本机真实截图。

### Step 1：一键安装 Hermes
```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```
（等价的 GitHub 原始脚本：`curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash`）

**它会自动做的事**：安装 uv 包管理器 → 装/定位 Python 3.11 → 克隆仓库到本地 → 装依赖 → 不需要 sudo。

**预期**：脚本跑完打印一行"installation complete"之类，并提示把某行 `export PATH=...` 加到 shell 配置。

### Step 2：让 hermes 命令生效
```bash
# 按脚本提示，把 hermes 加入 PATH（一般是下面这条，按脚本实际提示为准）
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Step 3：验证安装
```bash
hermes --version
```
**预期**：打印版本号。打不出版本号 = PATH 没配对（见 5.1）。

### Step 4：初始配置向导
```bash
hermes setup
```
向导会问你：选 LLM provider、填 API Key、选 Terminal Backend（学生起步选 **Local**）、是否接入消息平台（可先跳过，后面 `hermes gateway setup` 再配）。

### Step 5：配置 LLM
```bash
hermes model
```
- 选 OpenRouter → 粘贴 Step 2.4 的 `sk-or-v1-...` → 选一个起步模型（如某个 `:free` 模型或便宜的中档模型）。

### Step 6：看一眼装了多少工具
```bash
hermes tools
```
**预期**：列出 70+ 工具。把这个列表截图，就是 Level 1 必答题第 3 问的答案。

### Step 7：第一次 CLI 对话
```bash
hermes
```
进入交互界面后，别只说 hello，给它一个真任务，例如：
```
帮我把这学期软件工程专业课的待办列成一个清单，并设一个每天晚上 9 点的复习提醒。
```
常用斜杠命令：
- `/new` 开新对话
- `/model` 切模型
- `/skills` 看已装技能
- `/personality` 切人格
- `/usage` 看用量

**Level 1 验收**：能和 Hermes 完成一段有实质内容的对话 = Bronze 到手。截图留存。

---

## 4. 验证是否装好（验收清单）

跑下面几条，全部有正常输出才算装好：

```bash
hermes --version        # 有版本号
hermes tools            # 列出工具列表
hermes                  # 能进交互界面，问它一个问题能正常回答
```

补三个 Level 1 必答题的答案：
1. 记忆存哪：`~/.hermes/` 下 SQLite(+FTS5) 数据库 + MEMORY.md + USER.md。
2. SOUL.md 作用：Agent 身份/人格文件，系统提示词第 1 槽位，路径 `~/.hermes/SOUL.md`。
3. 工具数量：以 `hermes tools` 真实输出为准（文档现为 70+）。

---

## 5. 常见报错与解决办法（踩坑清单）

### 5.1 `hermes: command not found`
- 原因：安装脚本加的 PATH 没生效。
- 解决：确认 `~/.bashrc` 里有 `export PATH="$HOME/.local/bin:$PATH"`，然后 `source ~/.bashrc`；或直接用全路径 `~/.local/bin/hermes --version` 验证。

### 5.2 国内网络：curl 下载 GitHub 超时 / clone 失败
- 原因：GitHub raw、clone 在国内直连不稳。
- 解决（任选）：
  - 给终端挂代理：`export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890`（端口按你本机代理改），再重跑安装脚本。
  - 或用 GitHub 镜像 / 手动 clone 后在本地跑脚本。
- 注意：WSL2 里的网络默认和 Windows 宿主机分离，Windows 上开的代理要在 WSL 里用宿主机 IP 才通。

### 5.3 `wsl --install` 报"虚拟化未启用"
- 进 BIOS 打开 CPU 虚拟化（Intel VT-x / AMD-V）。
- 或在 Windows 功能里确认"虚拟机平台"已勾选并重启。

### 5.4 WSL 里 sudo / apt 慢
- 换 Ubuntu 国内镜像源（清华/阿里），这是常规 Linux 操作，与 Hermes 无关。

### 5.5 API Key 填了但模型报 401/402
- 401 = Key 错或没复制全（OpenRouter Key 以 `sk-or-v1-` 开头）。
- 402 = 余额不足，换 `:free` 后缀的免费模型先跑通。

### 5.6 想接 Telegram 但连不上 bot
- Telegram 国内需代理；`hermes gateway setup` 里填 BotFather 给的 token，网关要保持运行（gateway daemon）。

---

## 6. 本机真实验证记录（证据，非伪造）

以下命令是**在当前这台 Windows 上真实执行**的结果：

**6.1 Python 版本**
```powershell
PS> python --version
Python 3.13.16
```
结论：本机 Windows 侧 Python 为 3.13.16（满足 ≥3.11）。但注意 Hermes 实际跑在 WSL2 里，这个版本号只作环境参考。

**6.2 WSL 状态**
```powershell
PS> wsl --status
```
返回退出码 **50**，输出（转写）："未安装用于 Linux 的 Windows 子系统，可通过运行 wsl.exe --install 进行安装……详细信息见 https://aka.ms/wslinstall"。

结论：**本机当前未安装 WSL2**。这正是为什么第 2.2 节把"启用 WSL2 + 重启"列为需要用户本人执行的环节。

---

## 7. 接下来需要你（阮依涵）在真实环境补的东西

1. 按 2.2 装好 WSL2 + Ubuntu，重启。
2. 按 2.4 申请 OpenRouter Key。
3. 按第 3 节跑通 Step 1–7，**截图/录屏**（这是 CHALLENGE.md 要求的"安装记录 + demo"）。
4. 把真实 `hermes tools` 数量、真实对话截图补进本目录，命名 `ruanyihan_C10H_安装记录.md` / demo 截图。
5. 再去配 SOUL.md（见《SOUL定制》）、自定义技能（见《自定义技能》）、cron（见《cron示例》）。
