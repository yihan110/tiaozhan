# StudyLoop（阮依涵_C9_mvp）—— 大学生间隔重复复习命令行工具

> C9 自驱项目 MVP ｜ 纯 Python 标准库，零第三方依赖 ｜ Windows / macOS / Linux 均可

## 它解决什么问题
平时整理的错题、单词、专业课知识点，"整理完就再也不看"。StudyLoop 用简化版 SM-2 间隔重复算法，每天只把"今天真该复习"的几张推到你终端里，复习完即走。

## 环境要求
- Python 3.8+（本机已验证 Python 3.13）
- **不需要 pip install 任何东西**

## 怎么跑（30 秒上手）
打开终端，`cd` 到本目录（mvp/），然后：

```bash
# 1) 录一张卡片（正面=问题，背面=答案，标签可选）
python 阮依涵_C9_mvp.py add --front "二重积分交换积分次序的条件" --back "积分域有限闭且被积函数连续" --tag 高数

# 2) 看今天该复习哪些
python 阮依涵_C9_mvp.py due

# 3) 复习完给这张卡打分：again(没记住) / hard / good / easy(秒会)
python 阮依涵_C9_mvp.py review 1 good

# 4) 看统计
python 阮依涵_C9_mvp.py stats
```

### 可选：指定"今天"的日期（演示/补卡用）
```bash
python 阮依涵_C9_mvp.py --today 2026-11-05 due
```

## 命令一览
| 命令 | 作用 |
|------|------|
| `add --front Q --back A [--tag 学科]` | 新增一张卡片，默认今日到期 |
| `due` | 列出今天（或 --today 指定日）到期的卡片，逾期单独标记 |
| `review <id> again\|hard\|good\|easy` | 给卡片评分，自动算下次到期日 |
| `stats` | 卡片总数 / 今日到期 / 累计复习 / 标签分布 |
| `list` | 列出全部卡片 |

## 数据存在哪
全部在 `data/cards.json`，一个纯文本 JSON。可以直接打开看、改、备份、拷走。没有云端、没有账号、没有锁定。

## 目录里有什么
- `阮依涵_C9_mvp.py` —— 主程序
- `run_demo.py` —— 一次性演示驱动，跑完生成下面 6 份运行记录
- `data/cards.json` —— 真实录入的 5 张卡片 + 复习历史
- `运行记录/01~06_*.txt` —— 本机真实运行的终端输出留档（带时间戳）

## 复现本次演示
```bash
python run_demo.py
```
会清空 data、重新录入 5 张卡、走完完整流程，并刷新 `运行记录/` 下 6 份日志。
