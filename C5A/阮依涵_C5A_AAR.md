# 阮依涵_C5A_AAR 复盘（After-Action Review）

> 复盘对象：挑战 C5A「GitHub 入门与仓库理解」
> 复盘人：阮依涵 ｜ 日期：2026-11-01

---

## 一、做了什么（What happened）

1. 通读了挑战资料：CHALLENGE.md、rubric.json、challenge.json、README.md、materials/C5A.pdf。
2. 确认本机环境：Python 3.13.16、Git 2.53.0 均已就绪。
3. 尝试 `git clone https://github.com/neolaf2/neoskills.git` —— **失败**：本机直连 GitHub 超时。
4. 改用 jsDelivr 公开 CDN 镜像，真实抓取了：仓库 README 全文、完整文件树（112 个文件）、
   `skills/bank-status/SKILL.md`、`skills/skill-dedup/SKILL.md` 原文。
5. 基于真实材料完成《仓库分析.md》（回答四个问题）、《GitHub 入门操作记录.md》（分步+状态标注）。
6. 产出 AI 日志、拿来说明、AAR、提交说明 README。

## 二、目标 vs 实际（Did we hit it?）

| 目标 | 结果 |
|---|---|
| 读懂 neoskills 并讲清四问 | ✅ 达成，且有真实来源 URL 可复核 |
| 本机完成 clone | ❌ 未达成，卡在网络（直连超时） |
| 用本人账号 fork/注册 | ⬜ 待本人在自己账号+可联网环境完成 |
| 不伪造截图、不编造内容 | ✅ 达成，全程如实标注 |

## 三、做得好的（What went well）

- **没有因为 clone 失败就编一个目录结构交差。** 第一反应是换通道（CDN 镜像）去拿真实材料，
  而不是凭 README 猜目录。
- **证据意识**：每个结论都挂了可复核的 URL，老师/评审可以自己点开核对。
- **诚实分级**：把"AI 已做"和"必须本人账号做"分得清清楚楚，没有越权代办。

## 四、问题与原因（Why did it go off track）

1. **网络直连 GitHub 超时** —— 这是环境问题，不是命令写错。我一开始没先测连通性就直接 clone，
   导致白白等了几轮。教训：**网络类任务先做最小连通性测试，再上重操作。**
2. **第一次 PowerShell 抓 README 用了 20s 超时偏短**，第二次 jsDelivr 拉 SKILL.md 也偶发超时，
   后来加了"重试 3 次"才稳定拿到。教训：**不稳定的外部请求要带重试和更长超时。**
3. **截图缺口**：账号/仓库/fork 类截图必须本人拍，AI 代不了。这部分我用"截图说明 + 待拍清单"
   补位，而不是 P 图。

## 五、下一轮具体改进方案（Action items）

1. **联网环境补全闭环**：回到能上 GitHub 的网络后，30 分钟内完成注册→建仓→fork→clone，
   按《入门操作记录》第 1~4 步跑通，并把 6 张截图按命名放进 `阮依涵_C5A_screenshots/`。
2. **把本机学到的 Git 命令真正用一遍**：不只看文档，亲手做一次 `branch/add/commit/push`，
   体验"改一行→提交→推上去"的完整手感（Level 3）。
3. **做一个自己的小技能练手**：参考 neoskills 的 SKILL.md 写法，把我常做的"试卷照片→结构化文字
   整理"写成一个个人 SKILL.md，放到自己的仓库里——这是把"读懂别人仓库"变成"我也能产出"。
4. **排错能力清单化**：把这次遇到的"clone 超时/直连不通"记进自己的排错手册：
   ① 先 `ping`/小请求测连通；② 换镜像源（jsDelivr / gitee 镜像）；③ 检查代理；④ 再决定是否换网络。

## 六、一句话收获

> C5A 让我明白：GitHub 的门槛不是"会不会点按钮"，而是"我能不能读懂一个陌生仓库、
> 并诚实地说清楚哪些我做到了、哪些还没做"。工程素养，先从诚实和证据开始。
