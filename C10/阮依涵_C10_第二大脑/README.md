# 阮依涵_C10_第二大脑 — 使用说明

## 这是什么
一套完全用 Markdown 写的个人 Agent 系统（第二大脑），按 KSTAR 五层架构组织。
不依赖任何特定 App，用记事本/VSCode/Obsidian/飞书文档都能打开。

## 目录结构
```
阮依涵_C10_第二大脑/
├── AGENT.md                 ← 主配置（每次对话先读它）
├── README.md                ← 本文件
├── docs/
│   └── architecture.md     ← 五层架构详细说明
├── memory/
│   ├── L1_raw/              ← 原始笔记（3 篇示例）
│   ├── L2_episodes/         ← KSTAR 经验（4 篇示例）
│   ├── L3_skills/           ← Skill 索引
│   └── L4_identity/         ← 我是谁 + 我能调什么工具
├── skills/                  ← 7 个已上线 Skill
│   ├── notice-hardener/
│   ├── resume-expander/
│   ├── math-visual-tutor/
│   ├── debug-workflow/
│   ├── research-scanner/
│   ├── weekly-planning/
│   └── aar-generator/
├── logs/                    ← 使用日志（含 ΔR）
└── inbox/                   ← 待整理输入
```

## 怎么用（3 步）
1. **遇到事**：先把原始想法扔进 `inbox/` 或 `memory/L1_raw/`。
2. **做事前**：打开 AI 对话，把 `AGENT.md` + 对应 `skills/<名字>/SKILL.md` 一起贴进去，让它按步骤执行。
3. **做完后**：在 `logs/usage_log.md` 加一行（日期/场景/Skill/R̂/R/ΔR），周日晚用 `aar-generator` 把本周 L1 升级成 L2。

## 怎么维护
- **每月 1 号**：整个文件夹 push 到 GitHub 私有仓备份一次。
- **每周日晚**：30 分钟做周 AAR。
- **每学期末**：检查有没有 Skill 连续 2 个月没被调用，有就标记 deprecated。
- **新 Skill 触发条件**：同一类事件在 L2 中出现 ≥3 次。

## 怎么判断它还活着
- Elite20 结束三个月后（2027 年 2 月），如果 logs/ 里还有新的记录，就算成功。
