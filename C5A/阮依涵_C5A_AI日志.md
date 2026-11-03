# 阮依涵_C5A_AI 日志（AI 使用全过程）

> 说明：本日志按真实工作顺序记录"每一轮让 AI 做了什么、我给的 prompt、AI 产出了什么、我如何判断/迭代"。
> 目的是证明这不是"一句话指令直接交差"，而是多轮、带判断、带排错的协作过程。

---

## 第 0 轮：理解任务边界
- **我给的指令（大意）**："这是 Elite20 挑战 C5A，学生阮依涵要满分提交包，最终打成一个 zip。
  你只负责 C5A，先通读挑战资料，按 CHALLENGE.md 交付表和 rubric 满分标准来。"
- **AI 产出**：列出需要先读的文件清单（CHALLENGE.md / rubric.json / challenge.json / README.md / C5A.pdf），
  并明确本任务不碰其他挑战文件夹。
- **我的判断**：方向对，先读资料再动手，避免凭空写。

## 第 1 轮：读资料 + 探环境
- **指令**："读完 CHALLENGE.md、rubric.json、challenge.json、README.md、C5A.pdf；
  顺便确认 python 和 git 是否可用。"
- **AI 产出**：
  - 提炼出交付清单：仓库分析.md（必答四问）、GitHub 入门操作记录、截图、AAR、AI 日志。
  - 跑 `python --version` → Python 3.13.16；`git --version` → git 2.53.0.windows.2。
- **我的判断**：环境 OK，可以真做，不用假设环境。

## 第 2 轮：尝试真实 clone（第一次排错）
- **指令**："用 git clone 把 https://github.com/neolaf2/neoskills.git 克隆到临时目录，做真实目录分析。"
- **AI 产出**：clone 命令挂起/等待确认，未成功。
- **我的判断**：这一步不能装作成功。需要先确认是网络问题还是权限问题。

## 第 3 轮：测连通性（关键排错）
- **指令**："先别急着重 clone，先测一下本机能不能连 GitHub：
  用 Invoke-WebRequest 抓 raw.githubusercontent.com 的 README，20 秒超时。"
- **AI 产出**：`The request was canceled due to ... HttpClient.Timeout of 20 seconds elapsing.`
- **我的判断**：确诊——**本机直连 GitHub 超时，是网络问题，不是命令写错。**
  这一步改变了策略：不能再死磕 clone，要换可达通道拿真实材料。

## 第 4 轮：换通道拿 README（策略调整）
- **指令**："raw 直连不通，改用 jsDelivr CDN 镜像试抓 README：
  https://cdn.jsdelivr.net/gh/neolaf2/neoskills@main/README.md ，抓不到再试 @master。"
- **AI 产出**：**200 成功，拿到 12906 字符完整 README**。
  我据此第一次搞清：neoskills 是"Homebrew 风格的 AI Agent 技能管理器"，Python 包、MIT、作者 Richard Tong。
- **我的判断**：通道通了！这是最强替代证据。下一步要拿"真实目录树"，不能只看 README 自述。

## 第 5 轮：拉真实文件树
- **指令**："用 jsDelivr 数据接口拿完整文件树：
  https://data.jsdelivr.com/v1/packages/gh/neolaf2/neoskills@main?structure=flat ，
  重点看 skills/ 下到底有几个技能。"
- **AI 产出**：共 112 个文件；根目录有 skills/、src/neoskills/、docs/ 等；
  `skills/` 下实际只有两个技能：`bank-status` 和 `skill-dedup`。
- **我的判断（关键纠正）**：我原以为 neoskills 仓库"自带一大堆技能"，实际**它本体是工具，只附带 2 个示例技能**。
  这个纠正是靠真实文件树才发现的——如果只看 README 会写错。

## 第 6 轮：抓两个 SKILL.md（带重试）
- **指令**："分别抓 skills/bank-status/SKILL.md 和 skills/skill-dedup/SKILL.md。"
- **第一次产出**：第二个请求又 30 秒超时了。
- **迭代指令**："加个最多重试 3 次的循环再抓 skill-dedup。"
- **最终产出**：拿到两个技能全文。
  - bank-status：只读的"技能库状态仪表盘"。
  - skill-dedup：带 scripts/dedup_scan.py，按 SHA256/相似度做三类去重、可 dry-run、可备份。
- **我的判断**：够写"哪个技能最有意思"了——选 skill-dedup，因为它带真脚本、解决真痛点、贯彻软链哲学。

## 第 7 轮：起草核心交付物
- **指令**："基于以上真实材料写《仓库分析.md》，必须回答四问，每个结论附来源 URL，
  并在开头诚实写明'本机未能 clone、改用镜像抓取'。"
- **AI 产出**：仓库分析初稿。
- **我的判断/迭代**：要求它把"skills/ 只有 2 个技能、其余是 src/ 源码"这个容易写错的点讲清楚，避免评审误以为仓库自带大量技能。

## 第 8 轮：补齐其余交付物
- **指令**："再写：GitHub 入门操作记录（每步标注【本机已验证】/【需本人账号】）、
  AAR、拿来说明、README 提交说明；截图目录只放一份'截图说明'，绝不伪造图片。"
- **AI 产出**：上述文档全部生成。
- **我的判断**：守住红线——不伪造截图、不编造本人账号信息。

## 第 9 轮：打包与自检
- **指令**："把文件放进提交文件夹，打成 zip，再用 python zipfile 列出内容核对必备文件都在且非空。"
- **AI 产出**：见最终打包自检结果。

---

## 本轮 AI 使用复盘（自评）

- **是否多轮迭代**：是，至少 9 轮，中间因网络问题改了 2 次策略（死磕 clone → 测连通 → 换镜像 → 加重试）。
- **是否有 prompt 优化**：是，从"直接 clone"迭代到"先测连通、再换镜像、再加重试"。
- **是否有判断/纠偏**：是，纠正了"仓库自带大量技能"的错误预设。
- **是否诚实记录失败**：是，clone 失败、超时都如实写进 AAR 和日志。
- **一句话**：AI 是干活的手，但"先测连通、换通道、不伪造"这些判断是我（学生侧）提出来的。
