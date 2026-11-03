# tiaozhan — AI4Math 挑战交付物仓库

本仓库是 **阮依涵（2025140020206）** 在 AI4Math 课程挑战中的全部交付物集合。每个挑战一个独立目录，均包含挑战要求的交付物、AI 协作日志与复盘（AAR），可直接按目录单独阅读。

> 说明：仓库为个人学习记录，所有内容均由本人完成，AI 协作过程在各自的 `*AI日志*.md` 中如实记录（含失败与返工），未做美化。

## 目录索引

| 目录 | 挑战 | 核心产出 |
|------|------|---------|
| [`C4B_答案/`](C4B_答案/) | C4B 公众号文章生成技能 | `wechat-publisher-pro` 技能包（Markdown → 公众号 HTML，22 条自检断言）、公众号文章源文件、传播方案、AI 日志、AAR |
| [`C4_algo-solver_答案/`](C4_algo-solver_答案/) | C4 算法解题技能 | 算法求解技能包、题解与验证脚本、AI 日志、AAR |
| [`C4A_答案/`](C4A_答案/) | C4A 技能进阶 | 技能包与配套说明、验证记录、AI 日志、AAR |
| [`C4C_答案/`](C4C_答案/) | C4C 技能工程化 | 技能包、工程化改造记录、AI 日志、AAR |
| [`ruanyihan_C2G_parameter_golf/`](ruanyihan_C2G_parameter_golf/) | C2G Parameter Golf | 参数效率实验代码与结果、AI 日志、AAR |
| [`C5/`](C5/) | C5 挑战 | 交付包与文档 |
| [`C5A/`](C5A/) | C5A 挑战 | 交付包与文档 |
| [`C6/`](C6/) | C6 挑战 | 交付包与文档 |
| [`C6A/`](C6A/) | C6A 挑战 | 交付包与文档 |
| [`C7/`](C7/) | C7 挑战 | 交付包与文档 |
| [`C8/`](C8/) | C8 挑战 | 交付包与文档 |
| [`C9/`](C9/) | C9 挑战 | 交付包与文档 |
| [`C10/`](C10/) | C10 挑战 | 交付包与文档 |
| [`C10H/`](C10H/) | C10H 挑战 | 交付包与文档 |

## 怎么读这个仓库

1. **先看 AAR**：每个目录下的 `*复盘AAR*.md` 是最短的入口，写的是「做了什么、错在哪、怎么修的」。
2. **再看 AI 日志**：`*AI日志*.md` 记录真实对话轮次、失败输出与 prompt 迭代（含原始 prompt → 修改后 prompt → 输出差异对照）。
3. **最后看成品**：技能入口为各目录下的 `SKILL.md`，可执行脚本在 `scripts/` 内。

## 最值得看的一个：C4B `wechat-publisher-pro`

```bash
cd C4B_答案/wechat-publisher-pro
python scripts/convert_to_wechat_pro.py --selftest                 # 22 条断言自检
python scripts/convert_to_wechat_pro.py ../ruanyihan_C4B_文章源文件.md \
       --theme blue --preview --validate ../ruanyihan_C4B_output_body.html
```

- 五段流水线：解析前预处理 → AST 解析 → DOM 后处理 → 中文排版清洗 → 标签白名单校验
- 产物三形态：完整预览页 / 可直接粘贴的正文片段（不含 `<html>/<body>` 外壳）/ 纯文本备份
- 样式与内容解耦：5 套主题均为字典数据，代码中没有按主题名分支的逻辑

## 环境

- Python 3.9+（`markdown`、`beautifulsoup4`、`Pillow`）
- 无需网络、无需任何 API Key；转换全程本地完成
- Windows 控制台需 UTF-8（脚本已内置强制设置，规避 GBK 下的 `UnicodeEncodeError`）

## 许可与使用

仅供课程评审与个人学习参考。如需引用，请注明来源仓库。
