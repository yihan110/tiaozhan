# 阮依涵_C10_usage_log.md — 使用日志总表

> 每次 KSTAR 循环都在本表留一行。详细日记见同目录下按日期分的文件。

| 日期 | 场景 | 调用 Skill | 输入 | 输出 | R̂ 预期 | R 实际 | ΔR | 改进 |
|------|------|-----------|------|------|--------|--------|-----|------|
| 2026-09-05 | 无人机社副社长竞选简历 | resume-expander | 流水账素材 | 220 字 STAR 段落 | 一次过审 | 改 1 处措辞 | 小 | 加'禁止编造数据'规则 |
| 2026-09-20 | 华为 ICT 省赛排错 | debug-workflow | 拓扑 + ACL 需求 | 漏配 1 条 ACL | 配置一次过 | 省三 | 中 | 加'网段核对表' |
| 2026-10-08 | 四级出分情绪 | （无 Skill，纯 L1 记录） | 395 分 | 情绪日记 | — | — | — | 触发 weekly-planning 睡眠优先 |
| 2026-10-10 | 四级失利复盘 | aar-generator | 3 套真题错题 | 精听计划 | 新闻题 7/10 | 6/10 | -1 题 | 坚持每日精听 |
| 2026-10-12 | 第 41 周复盘 | aar-generator | 本周 L1 三篇 | notice-hardener 候选 | 30 min | 35 min | +5 min | — |
| 2026-10-19 | 三下乡+学业并行周计划 | weekly-planning | 周三踩点+作业 | 一周日历 | 完成率 80% | 85% | +5% | — |
| 2026-10-20 | 三坟村前期调研 | research-scanner | 三坟村旧址背景 | 3 条事实+3 链接 | 40 min | 30 min | -10 min | — |
| 2026-10-23 | ICT 下次赛题方向 | research-scanner | 2027 方向 | 2 条关键事实 | 3 条 | 2 条 | -1 条 | 下周补 1 个来源 |
| 2026-10-25 | 寝室卫生检查通知 | notice-hardener | 软乎乎原稿 | 150 字硬气通知 | 5 回复零吐槽 | 6 回复零吐槽 | +1 | 沉淀 v2 后果绑定 |
| 2026-10-27 | Python IndexError | debug-workflow | 作业报错 | 8 分钟定位边界 | 5 min | 8 min | +3 min | — |
| 2026-10-28 | 教室友二重积分 | math-visual-tutor | 换序题 | 2 张图+讲懂 | 10 min | 20 min | +10 min | 下次先让学生自己说题 |
| 2026-10-29 | 院长视察通知 | notice-hardener | 社长一句话 | 120 字通知 | 1h 内通知到 | 40 min | -20 min | — |
| 2026-10-30 | 自己复习二阶偏导 | math-visual-tutor | z=x²sin(y) | 曲面草图 | 5 min | 8 min | +3 min | — |
| 2026-11-01 | 体测补测通知 | notice-hardener | 300 字长文 | 120 字短通知 | 压到 150 字 | 120 字 | -30 字 | — |

## 汇总
- 总调用次数：14 次
- 涉及 Skill：6 个（notice-hardener / resume-expander / debug-workflow / research-scanner / weekly-planning / aar-generator / math-visual-tutor）
- 平均 ΔR：小幅偏差为主，说明 Skill 已经稳定；2 次中等偏差（ICT ACL、二重积分用时）触发了 Skill 迭代。
