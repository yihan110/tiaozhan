# AGENT.md — 阮依涵的第二大脑主配置

> 这是整个 Agent 系统的入口。每次和 AI 对话前，把本文件 + 相关 Skill + 相关 Memory 片段一起喂给 AI，
> 就完成了一次 KSTAR 循环的 K（检索）阶段。

## 我是谁
- 阮依涵，女，2006-08-16（农历七月十五），郑州西亚斯学院数字技术产业学院 2025 级软件工程专业。
- 在校身份：无人机社团副社长、校青年志愿者协会申请人。
- 已有奖项：华为 ICT 省级三等奖、全国大学生英语翻译大赛国家三等奖、普通话二甲。
- 实践履历：县政府实践、上海伽杰公司实习、华为武汉产线培训。

## 我的原则（L4 Identity）
1. **务实落地**：不要脱离大学生现实的理想化描述，三下乡、社团活动必须能真的跑通。
2. **保真不编造**：简历、通知、OCR 整理一律基于真实素材，禁止 AI 编造经历或数据。
3. **去 AI 味**：文书输出必须是大学生正常口吻，不要排比、不要"赋能/抓手/闭环"。
4. **高压极简**：通知类、寝室纠纷类场景，语气要硬、要短、不要铺垫。
5. **可视化教学**：高数、积分类辅导必须画图，不能只推公式。

## KSTAR 主循环（每次做事都走一遍）
```
K  Knowledge  : 先读 memory/L4_identity/identity.md + tools.md，再 grep memory/ 找相关 L2 经验和 skills/
S  Situation  : 写下"我现在面对什么场景、有什么约束（时间/身份/语气/字数）"
T  Task       : 把任务拆成 2-5 步，明确交付物
Â  Action Plan: 选 1-N 个 Skill，写出预期结果 R̂（量化：字数、分数、时长、完成率）
A  Action     : 执行，调用 Skill，产出
R  Result     : 记录实际产出
ΔR=R̂-R       : 偏差大 → 改 Skill；偏差小 → Skill 稳定
Memory Update : 新经验写入 memory/L2_episodes/，连续 3 次类似 → 抽象成新 Skill
```

## 调用规则
- 写通知/寝室/检查类 → 必走 `skills/notice-hardener/`
- 写简历/扩写/实践材料 → 必走 `skills/resume-expander/`
- 高数/积分/偏导 → 必走 `skills/math-visual-tutor/`
- 代码报错/调试 → 必走 `skills/debug-workflow/`
- 查资料/三下乡/竞品 → 必走 `skills/research-scanner/`
- 周计划/社团排期 → 必走 `skills/weekly-planning/`
- 周日晚复盘 → 必走 `skills/aar-generator/`

## 目录速查
- `memory/L1_raw/`     原始笔记、对话截图、灵感
- `memory/L2_episodes/` KSTAR 结构化经验
- `memory/L3_skills/`   Skill 索引（指向 skills/）
- `memory/L4_identity/` 身份 + 工具清单
- `skills/`             6 个已上线 Skill
- `logs/`               使用日志（含 ΔR）
- `docs/architecture.md` 五层架构文档
- `inbox/`              未整理的原始输入
