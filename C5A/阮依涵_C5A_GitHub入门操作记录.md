# 阮依涵_C5A_GitHub 入门操作记录

> 目标：完成「注册账号 → 创建个人仓库 → Fork neolaf2/neoskills → Clone 到本地 → 理解仓库」的完整闭环。
> 说明：本文每一步都标注了【本机已验证】/【需本人 GitHub 账号完成】/【需可联网环境】，
> 绝不伪造截图或假装已完成本人账号操作。

---

## 0. 前置环境（本机已真实验证）

| 项 | 本机实际情况 | 验证命令 |
|---|---|---|
| 操作系统 | Windows 10/11 | —— |
| Python | **Python 3.13.16**（真实运行 `python --version` 得到） | `python --version` |
| Git | **git version 2.53.0.windows.2**（本机已安装 Git，无需再装） | `git --version` |
| 网络到 GitHub | ⚠️ 本机直连 `github.com` / `raw.githubusercontent.com` **超时不可达** | `Invoke-WebRequest` 20s 超时 |

> 结论：本机 Git 已就绪，缺的只是"本人的 GitHub 账号"和"一个能连上 GitHub 的网络环境"。

---

## 1. 注册 GitHub 账号【需本人本人完成 + 需可联网】

1. 浏览器访问 https://github.com ，右上角点 **Sign up**。
2. 输入常用邮箱 → 设置密码 → 设置用户名（建议可识别，如 `ruanyihan-sias` 或 `wanhan-wang`）。
3. 完成邮箱验证（收验证码邮件）。
4. （可选）回答几个问卷后进入主页。
- **预期结果**：能登录，看到右上角头像。
- **本人需做的事**：这一步必须本人用自己邮箱注册，AI 无法代办。
- **截图建议**：登录后的 GitHub 主页截一张，命名 `01_账号主页.png`。

---

## 2. 创建个人仓库（Level 1）【需本人账号 + 可联网】

1. 登录后点右上角 **+** → **New repository**。
2. Repository name 填 `elite20-portfolio`（或 `ruanyihan-elite20`）。
3. 勾选 **Add a README file**。
4. 可见性选 **Public**（公开，方便老师查看）。
5. 点 **Create repository**。
6. 进入仓库后点开 `README.md` → 铅笔编辑，写入：
   ```
   # 阮依涵
   郑州西亚斯学院 · 数字技术产业学院 · 软件工程 2025 级
   一句话介绍：正在学用 GitHub 管理代码与作品，目标是把课程项目都沉淀到自己的主页。
   ```
   提交（Commit）。
- **预期结果**：https://github.com/yihan110/tiaozhan 可公开访问。
- **截图建议**：`02_个人仓库README.png`。

---

## 3. Fork 目标仓库 neolaf2/neoskills【需本人账号 + 可联网】

1. 浏览器打开 https://github.com/neolaf2/neoskills 。
2. 点右上角 **Fork** 按钮。
3. Owner 选你自己的账号，Repository name 保持 `neoskills`。
4. 点 **Create fork**。
- **预期结果**：你的账号下出现一份副本：`https://github.com/neolaf2/neoskills`，
  页面顶部会显示 `forked from neolaf2/neoskills`。
- **截图建议**：`03_fork成功.png`。

---

## 4. Clone 到本地【本机 Git 已就绪；网络/账号取决于环境】

> 换成你自己的用户名：

```bash
# Windows PowerShell 下进入你想放代码的目录
cd C:\Users\asus\code

# 克隆你 fork 下来的副本（注意是你自己用户名，不是 neolaf2）
git clone https://github.com/neolaf2/neoskills.git

# 进入仓库
cd neoskills

# 查看目录结构（Windows 用 dir / 或 ls）
dir
```

- **本机已验证**：`git --version` 正常（2.53.0），说明上面这些命令本机可执行。
- **本机当前未能完成的部分（诚实记录）**：本次执行环境直连 GitHub 超时，
  `git clone` 三次均未能成功拉取，因此**没有本机 clone 成功的真实截图**。
  作为替代，我通过 jsDelivr 公开镜像真实抓取了该仓库的 README、完整文件树和两个 SKILL.md
  （见《阮依涵_C5A_仓库分析.md》第五节来源表），用于替代本地目录浏览。
- **本人需做的事**：在能连 GitHub 的网络下，用自己账号 fork 后执行上面命令。
- **截图建议**：clone 成功后在 PowerShell 里截一张 `04_clone成功.png`（能看到 neoskills 文件夹和 dir 列出的文件）。

---

## 5. 浏览并阅读仓库（本机可做，不依赖网络）

clone 成功后建议顺序：

```bash
# 看顶层
dir

# 读主文档
notepad README.md

# 看自带的两个技能
notepad skills\bank-status\SKILL.md
notepad skills\skill-dedup\SKILL.md

# 看 Git 提交历史（感受迭代）
git log --oneline
```

我本次虽未 clone 成功，但通过镜像已把上面这份"阅读路线"对应的真实内容读完，结论见仓库分析文档。

---

## 6.（Level 3，加分）贡献一个分支并 push【需本人账号 + 可联网】

```bash
# 基于当前主分支新建并切到自己的分支
git checkout -b my-contribution

# 做一点小修改，例如给 README 补一句中文说明，然后：
git add .
git commit -m "docs: add a short Chinese note to README"

# 推送到你自己的 fork
git push origin my-contribution
```

- 回 GitHub 你的 fork 页面 → 会提示 `Compare & pull request` → 可向原仓库发 PR（可选）。
- **截图建议**：`05_commit历史.png`、`06_分支或PR.png`。

---

## 7. 常用 Git 命令速查（备查）

| 命令 | 作用 |
|---|---|
| `git status` | 看当前改了什么 |
| `git add .` | 暂存全部修改 |
| `git commit -m "说明"` | 提交 |
| `git push` | 推到远程 |
| `git pull` | 拉最新 |
| `git branch` / `git checkout -b 名` | 看分支 / 新建并切分支 |
| `git log --oneline` | 看提交历史 |

---

## 8. 操作完成度对照（自查表）

| 步骤 | 状态 | 谁来完成 |
|---|---|---|
| 本机 Git/Python 环境 | ✅ 已验证 | AI 已做 |
| 仓库真实内容调研（README/树/技能） | ✅ 已完成（经镜像） | AI 已做 |
| 注册账号 | ⬜ 待本人 | 阮依涵本人 |
| 创建个人仓库 + README | ⬜ 待本人 | 阮依涵本人 |
| Fork neoskills | ⬜ 待本人 | 阮依涵本人 |
| 本地 clone | ⬜ 待可联网环境执行 | 本人在能联网时做 |
| 提交 commit/push / PR | ⬜ 加分项，待本人 | 阮依涵本人 |
