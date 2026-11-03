# ruanyihan_C10H 提交说明（README）

> 挑战：C10H 安装并驾驭 Hermes Agent
> 提交人：阮依涵（ruanyihan）｜郑州西亚斯学院 软件工程专业 2025 级
> 提交日期：2026-11-01

---

## 一、本包是什么

这是 C10H 挑战的提交包。由于本机为 Windows 原生、WSL2 未安装，本包交付的是：**一套完整、可照做的 Hermes Agent 安装配置文档 + 贴合本人的 SOUL/技能/cron 定制模板 + 真实调研来源 + 多轮 AI 日志 + 诚实复盘**。凡需在真实 WSL2 环境执行的环节，均已逐条标注，未伪造任何"已安装成功"的输出。

---

## 二、包内文件清单（全部 ruanyihan_C10H_ 拼音命名）

| 文件 | 作用 |
|---|---|
| `ruanyihan_C10H_安装配置指南.md` | 主文档：Hermes 是什么/架构/为什么需要、Windows 启用 WSL2 分步、API Key 获取、完整安装命令与预期输出、排错清单、本机真实验证证据 |
| `ruanyihan_C10H_SOUL定制.md` | 为本人定制的完整 `~/.hermes/SOUL.md` 内容 + 生效/验证方法 + 个性化对照表 |
| `ruanyihan_C10H_自定义技能.md` | 一个真实可用的自定义技能 `exam-ocr-cleanup`（SKILL.md 全文，符合 agentskills.io 标准）+ 触发词/示例 |
| `ruanyihan_C10H_cron示例.md` | 每日四级词汇+待办摘要定时任务：自然语言配置法 + cron 表达式速查 + 验证/排错 |
| `ruanyihan_C10H_AI日志.md` | 7 个阶段的多轮 AI 使用记录：每轮 prompt、产出、下一轮怎么改 |
| `ruanyihan_C10H_拿来说明.md` | 参考来源 URL 清单（7 项）、每项参考了什么/改了哪里、哪些照抄哪些再创作 |
| `ruanyihan_C10H_AAR.md` | 诚实复盘：预期 vs 实际、做成的、卡壳失败经验、具体改进方案 |
| `ruanyihan_C10H_提交说明.md` | 本文件：包索引 + 待用户在真实环境补的环节清单 |

---

## 三、需要用户（阮依涵）在真实环境完成的环节（逐条）

1. **启用 WSL2**：管理员 PowerShell 跑 `wsl --install` → 重启 → 设 Ubuntu 用户名密码（指南 2.2 节）。
2. **申请 LLM API Key**：openrouter.ai 注册、建 `sk-or-v1-...` Key（指南 2.4 节）。
3. **真实安装 Hermes**：进 WSL bash 跑 install.sh → `hermes setup` → `hermes model` → 首次 CLI 对话（指南第 3 节）。
4. **补真实证据**：截图/录屏安装过程与对话，补 `ruanyihan_C10H_安装记录.md` 与 demo 截图。
5. **落地定制**：把 SOUL.md、exam-ocr-cleanup 技能、cron 任务真的写进 `~/.hermes/` 并跑一周。
6. **（进阶）** 接 Telegram（Level 2）、配两个模型对比（Level 3）。

---

## 四、本机真实验证了什么（附证据）

- `python --version` → **Python 3.13.16**（满足 ≥3.11）。
- `wsl --status` → 退出码 **50**，提示"未安装用于 Linux 的 Windows 子系统"。
- 以上两条为真实执行结果，原文记录在《安装配置指南》第 6 节。

---

## 五、对照 rubric 的自评

| 维度 | 本包如何覆盖 |
|---|---|
| 驾驭程度(25) | 讲清架构、记忆/SOUL/技能/cron 机制、排错清单、可扩展点 |
| 集成质量(20) | 针对 Windows→WSL2 环境给出可复现步骤，命令与路径明确 |
| 产物完整性(15) | 8 个文件齐全、非空、命名规范、互相引用 |
| AI 使用质量(20) | AI 日志 7 阶段多轮迭代、prompt 优化轨迹清晰 |
| 复盘质量(20) | AAR 含失败经验与具体改进方案 |

> 最大风险项：缺真实"安装运行截图"（受本机环境所限），已在第三节列出补做路径。
