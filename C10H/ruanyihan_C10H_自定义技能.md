# ruanyihan_C10H 自定义技能

> 作者：阮依涵（ruanyihan）
> 依据官方技能系统文档：https://hermes-agent.nousresearch.com/docs/zh-Hans/guides/work-with-skills
> 技能兼容 agentskills.io 开放标准

---

## 1. 技能系统怎么回事（拿来前先懂机制）

- Skills 是**按需加载的 Markdown 知识文档**，教会 Hermes 怎么干某类特定活。
- 存放位置：`~/.hermes/skills/<分类>/<技能名>/SKILL.md`。放进去即生效，**无需注册**，新会话自动出现，并变成一个斜杠命令 `/<技能名>`。
- 文件本质：带 **YAML frontmatter 的 Markdown**。
- 加载方式：会话开始只加载紧凑列表（`skills_list`，约 3k tokens），用到时才 `skill_view` 读全文——不用不耗 token。
- 命令：`/skills` 看列表、`/skills search <词>` 搜索、`hermes skills list`、`hermes skills install <源>` 从 Hub/URL 安装。
- 它和 Memory 的区别：Skills = 程序性知识（怎么做某事，可几百行，按需加载）；Memory = 事实性便签（你是谁、你偏好啥，每会话自动注入）。

---

## 2. 我为自己写的真实技能：试卷 OCR 题目保真整理

**为什么是这个**：她高频用 AI 把题目照片整理成结构化文档（试卷整理/作业录入），而且**严格要求零篡改、选择/判断分类分开**。这是个重复发生、规则明确的真实需求，非常适合沉淀成技能。

### 2.1 安装目录

```bash
mkdir -p ~/.hermes/skills/study/exam-ocr-cleanup
```

### 2.2 把下面内容写入 `~/.hermes/skills/study/exam-ocr-cleanup/SKILL.md`

```markdown
---
name: exam-ocr-cleanup
description: 把 OCR/拍照识别出的试卷或作业文本，整理成结构化文档——严格保真不改原文，选择题与判断题分开归类，标注存疑处。
version: 1.0.0
metadata:
  hermes:
    tags: [study, ocr, exam, cleanup, fidelity]
    category: study
---

# 试卷 OCR 题目保真整理

## When to Use（什么时候触发）
当用户发来一段 OCR/拍照识别出来的试卷、作业、题库文本，要求"整理成文档""按题型分类""录入题目"时使用本技能。
典型触发说法："帮我整理这张卷子""把这些题目分分类""OCR 出来的排版乱了帮我理顺"。

## Core Rules（铁律，优先级最高）
1. **严格保真**：用户给的题干、选项、答案文字，一字不改、不补写、不润色、不"帮你优化表达"。只调整排版与归类，不改动内容本身。
2. **存疑标注**：OCR 可能认错字。凡是看不清/可疑的字、数字、符号，用 `【存疑：xxx】` 标在该处，不要擅自猜定。
3. **题型分开**：按"选择题 / 填空题 / 判断题 / 简答题"分大类，各类之间用二级标题隔开。
4. **答案隔离**：答案与题号对齐放在题目下方或单独"参考答案"区，不要混进题干里改变原文。
5. **不确定就问**：如果整段逻辑断裂到无法判断是哪题，把那段原样保留并注明"这一段未能识别归属"，不要瞎拼。

## Procedure（标准流程）
1. 通读全文，先判断这是哪几种题型。
2. 按题型分组；每组内按原顺序保留题号（原卷没题号就顺延编号）。
3. 选择题保留 A./B./C./D. 选项原样；判断题统一写成"（ ）题干……"形式。
4. 把所有 `【存疑：xxx】` 汇总到文末"待人工核对清单"。
5. 输出前自查一遍：有没有哪个字被我偷偷改过？有就改回原文。

## Output Template（输出模板）
## 一、选择题
1. 题干原文……（存疑字处标【存疑：xx】）
   A. ……  B. ……  C. ……  D. ……
   答案：X
## 二、判断题
1. （ ）题干原文……
   答案：对/错
## 待人工核对清单
- 第 3 题选项 B：【存疑：xxx】

## Pitfalls（常见坑）
- 坑：手滑把"which"改成"what"，或把数字"31"顺成"37"。修法：输出前逐题对照原文复核。
- 坑：擅自把口语化题干改通顺。修法：题干保持 OCR 原貌，只动排版。
- 坑：把答案解析塞进题干。修法：答案单独成行/单独分区。

## Verification（自检）
整理完后，对用户说一句："已按题型分类完成，所有存疑点都列在文末，请对照原图核对。"
```

### 2.3 验证技能生效

```bash
# 新开会话后查看
hermes skills list | grep exam-ocr-cleanup
# 或在聊天里
/skills search ocr
# 直接试用（会变成斜杠命令）
/exam-ocr-cleanup （然后贴一段 OCR 乱文本让它整理）
```

---

## 3. 触发词 / 指令 / 示例（对照任务要求）

| 项 | 内容 |
|---|---|
| 触发词 | "整理这张卷子""OCR 文本分类""把题目按选择/判断分开录入" |
| 斜杠指令 | `/exam-ocr-cleanup` |
| 示例输入 | 一段 OCR 出来的、题型混排、有识别错字的试卷文本 |
| 示例预期输出 | 按选择/判断/填空分好类、存疑点用【存疑：】标出、末尾有待核对清单，原文一字未改 |

---

## 4. 为什么这个技能算"驾驭"而不是照抄

- 它不是 Hermes 自带技能，是我**针对自己真实高频痛点**（试卷 OCR 保真整理）手动写的。
- 把我在长期使用中形成的硬规矩（保真不改字、存疑标注、题型分开）固化进了 SKILL.md 的 Core Rules，下次任何会话加载都遵守，不用每次重复交代。
- 结构完全遵循官方 SKILL.md 规范（frontmatter + When to Use + Procedure + Pitfalls + Verification），符合 agentskills.io 标准，日后可发到 Skills Hub。

> 说明：本技能文件已按官方格式写好，**尚未在真实 Hermes 实例加载**（本机无 WSL2）。装好后放到 `~/.hermes/skills/study/exam-ocr-cleanup/` 即可，无需注册自动生效。
