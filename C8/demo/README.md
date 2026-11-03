# demo/ — C8 Project B 早期验证物：电信本体 Agent 原型

## 这是什么

一个**纯 Python 标准库、可离线真实运行**的最小原型，验证我对 Project B
（企业本体 Agent 系统 / 电信运营商数字孪生）的理解已经落到代码上，而不只是纸面 Proposal。

它演示了 CHALLENGE.md 里 Project B 的四件事：

| CHALLENGE.md 要求 | 本原型对应实现 |
|---|---|
| 本体建模：T-box（概念/关系/约束） | `Node` 类 + 6 类概念常量 + 注释里的 A1~A4 业务约束 |
| A-box（实例数据） | `build_demo_graph()` 里 13 个节点、15 条带类型边的迷你电信图 |
| 知识图谱 property graph | `Graph` 类：adjacency list，边带类型（HAS_CONTRACT / SUBSCRIBES / DEPLOYS_AT / COVERS / REPORTED / AFFECTS） |
| Agent Workflow（基于本体的推理执行） | `agent_handle_task()`：Think → Act（图遍历）→ Observe → Decide（套 T-box 约束） |

## 运行方式

```powershell
# 无需 pip install 任何东西（只用标准库）
python 阮依涵_C8_demo.py
```

本机 Python 3.13.16 实测通过，运行输出已保存到 `run_output.txt`（真实运行记录，非伪造）。

## 三个测试用例验证了什么

1. **李先生报障** → 图遍历发现其宽带部署在状态为 `DOWN` 的分纤箱 → 规则 A3 命中 →
   根因判定为 `site_outage`（站点故障），派单覆盖该区域的赵工。
2. **张女士（VIP）报障** → 机房状态正常 → 根因 `customer_side`；但规则 A4 命中 →
   工单升级 `P1`；因没有 senior 工程师覆盖该片区 → 派单结果 `待调度`（暴露真实资源缺口，不是"一切顺利"）。
3. **陌生人报障** → 图中无此 Customer 节点 → 走 `transfer_to_human` 分支。

## 与真实企业环境的差距（诚实说明）

| 维度 | 本原型 | 真实 Project B 环境 |
|---|---|---|
| 存储 | 内存 dict | Neo4j / Apache AGE + PostgreSQL |
| Think 阶段 | 规则模板 | LLM + NL2SQL pipeline |
| 数据量 | 13 节点玩具数据 | 千万级真实业务数据 |
| 向量召回 | 无 | pgvector 语义检索 |

这正是"早期验证物"该有的样子——**架构骨架对、业务规则对、可跑通端到端链路**，
但不冒充已完成品。入选后按 KSTAR 方案逐步替换。
