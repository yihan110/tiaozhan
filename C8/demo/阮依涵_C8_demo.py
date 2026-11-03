# -*- coding: utf-8 -*-
"""
阮依涵_C8_demo.py
C8 Project B（企业本体 Agent 系统）早期验证物：电信运营商数字孪生本体 Agent 原型

本脚本是一个**可离线真实运行**的最小原型，演示：
  1. T-box（术语层）：用 Python 类定义概念、关系、业务约束；
  2. A-box（断言层）：内存中的 property graph（节点 + 带类型的边）；
  3. Agent Workflow：模拟 KSTAR/ReAct 认知循环（Think -> Act -> Observe -> Decide），
     输入一个"客户报障"任务，在本体图上做推理遍历，输出数字孪生处置方案。

设计说明：
  - 仅使用 Python 标准库，不依赖任何外部 API / API Key / 图数据库服务；
    目的是在没有外网和 Key 的环境下也能确定性复现，作为早期验证物。
  - 未来在真实企业环境中，A-box 替换为 Neo4j / PostgreSQL，
    Think 环节替换为 LLM + NL2SQL，本脚本的图遍历与业务规则层保持不变。

运行方式：
  python 阮依涵_C8_demo.py
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


# ============================================================
# 第一部分：T-box（术语层 / Schema）
# ============================================================
# 对应 CHALLENGE.md Project B 的"本体建模：T-box（概念、关系、约束）"。
# 这里用 Python 类 + 枚举式关系名表达，而不是真的写 OWL 文件——
# 这正是"拿来主义"里 removed 的部分（去掉重型 OWL/RDF 序列化）。

CUSTOMER = "Customer"          # 客户
CONTRACT = "Contract"           # 合约
SERVICE = "ServicePlan"         # 业务套餐（宽带/移动/ IPTV）
CELL = "CellSite"               # 基站 / 局端设备
AREA = "CoverageArea"           # 覆盖区域
TICKET = "TroubleTicket"        # 故障工单
TECH = "Technician"             # 运维工程师

# T-box 业务约束（axioms）——原型阶段用注释 + 代码检查表达：
#  A1: 一张工单必须关联且仅关联 1 个 Customer。
#  A2: 工单必须 AFFECTS 至少 1 个 ServicePlan。
#  A3: ServicePlan DEPLOYS_AT 的 CellSite 若 DOWN，则该 Service 下所有客户故障优先按站点故障处置。
#  A4: VIP 客户工单自动升级为 P1 并指派高级工程师。


@dataclass(eq=False)
class Node:
    """property graph 节点：id + 类型 + 属性字典。"""
    nid: str
    ntype: str
    props: dict = field(default_factory=dict)

    def __repr__(self) -> str:  # 便于日志打印
        return f"[{self.ntype}:{self.nid}] {self.props.get('name', '')}"


class Graph:
    """内存版 property graph：adjacency list，边带类型。"""
    def __init__(self):
        self.nodes: dict[str, Node] = {}
        self.edges: list[tuple[str, str, str]] = []  # (src_id, rel, dst_id)

    def add_node(self, node: Node) -> None:
        self.nodes[node.nid] = node

    def add_edge(self, src: str, rel: str, dst: str) -> None:
        self.edges.append((src, rel, dst))

    def out(self, nid: str, rel: Optional[str] = None) -> list[tuple[str, str]]:
        return [(r, d) for (s, r, d) in self.edges if s == nid and (rel is None or r == rel)]

    def in_(self, nid: str, rel: Optional[str] = None) -> list[tuple[str, str]]:
        return [(s, r) for (s, r, d) in self.edges if d == nid and (rel is None or r == rel)]

    def find_by_type(self, ntype: str) -> list[Node]:
        return [n for n in self.nodes.values() if n.ntype == ntype]

    def find_customer_by_name(self, name: str) -> Optional[Node]:
        for n in self.find_by_type(CUSTOMER):
            if name in n.props.get("name", "") or n.props.get("name", "") in name:
                return n
        return None


# ============================================================
# 第二部分：A-box（断言层 / 实例数据）——一个迷你电信数字孪生
# ============================================================

def build_demo_graph() -> Graph:
    g = Graph()

    # --- 客户 ---
    g.add_node(Node("C001", CUSTOMER, {"name": "张女士", "tier": "VIP",
                                       "phone": "138****0001"}))
    g.add_node(Node("C002", CUSTOMER, {"name": "李先生", "tier": "normal",
                                       "phone": "139****0002"}))
    g.add_node(Node("C003", CUSTOMER, {"name": "王同学", "tier": "normal",
                                       "phone": "137****0003"}))

    # --- 合约 ---
    g.add_node(Node("K001", CONTRACT, {"name": "张女士家庭融合合约"}))
    g.add_node(Node("K002", CONTRACT, {"name": "李先生单宽带合约"}))
    g.add_node(Node("K003", CONTRACT, {"name": "王同学校园套餐合约"}))

    # --- 业务套餐 ---
    g.add_node(Node("S001", SERVICE, {"name": "千兆光纤宽带", "status": "normal"}))
    g.add_node(Node("S002", SERVICE, {"name": "5G 移动套餐", "status": "normal"}))
    g.add_node(Node("S003", SERVICE, {"name": "百兆宽带(老)", "status": "normal"}))

    # --- 覆盖区域 ---
    g.add_node(Node("A001", AREA, {"name": "金水区花园路片区"}))
    g.add_node(Node("A002", AREA, {"name": "二七区大学路片区"}))

    # --- 基站 / 局端 ---
    # CS002 当前 DOWN —— 这是触发"站点故障根因"的关键实例
    g.add_node(Node("CS001", CELL, {"name": "花园路汇聚机房", "status": "normal"}))
    g.add_node(Node("CS002", CELL, {"name": "大学路分纤箱3号", "status": "DOWN"}))

    # --- 工程师 ---
    g.add_node(Node("T01", TECH, {"name": "赵工", "level": "senior",
                                  "covers": "二七区大学路片区", "load": 0.3}))
    g.add_node(Node("T02", TECH, {"name": "钱工", "level": "junior",
                                  "covers": "金水区花园路片区", "load": 0.8}))

    # --- 工单 ---
    g.add_node(Node("TK9001", TICKET, {"desc": "李先生:百兆宽带无法上网",
                                       "status": "OPEN", "priority": "P3"}))

    # ===== 边 =====
    # Customer -[HAS_CONTRACT]-> Contract
    g.add_edge("C001", "HAS_CONTRACT", "K001")
    g.add_edge("C002", "HAS_CONTRACT", "K002")
    g.add_edge("C003", "HAS_CONTRACT", "K003")
    # Contract -[SUBSCRIBES]-> Service
    g.add_edge("K001", "SUBSCRIBES", "S001")
    g.add_edge("K001", "SUBSCRIBES", "S002")
    g.add_edge("K002", "SUBSCRIBES", "S003")
    g.add_edge("K003", "SUBSCRIBES", "S002")
    # Service -[DEPLOYS_AT]-> CellSite
    g.add_edge("S001", "DEPLOYS_AT", "CS001")
    g.add_edge("S002", "DEPLOYS_AT", "CS001")
    g.add_edge("S003", "DEPLOYS_AT", "CS002")
    # CellSite -[COVERS]-> Area
    g.add_edge("CS001", "COVERS", "A001")
    g.add_edge("CS002", "COVERS", "A002")
    # Customer -[REPORTED]-> Ticket
    g.add_edge("C002", "REPORTED", "TK9001")
    # Ticket -[AFFECTS]-> Service
    g.add_edge("TK9001", "AFFECTS", "S003")
    return g


# ============================================================
# 第三部分：Agent Workflow（认知循环：Think -> Act -> Observe -> Decide）
# ============================================================
# 这里没有接 LLM：Think 阶段用规则模板，Act 阶段就是图遍历，
# Observe 阶段打印遍历到的节点，Decide 阶段套 T-box 业务约束 A1~A4。

@dataclass
class Trace:
    """记录 Agent 每一步在图上做了什么，作为可验证的执行轨迹。"""
    steps: list[str] = field(default_factory=list)

    def log(self, msg: str) -> None:
        self.steps.append(msg)
        print("  " + msg)


def agent_handle_task(g: Graph, customer_name: str, symptom: str) -> dict:
    """输入一个自然语言任务（客户名 + 症状），输出数字孪生处置方案。"""
    print("=" * 64)
    print(f"[Agent] 收到任务：客户「{customer_name}」报障 -> {symptom}")
    print("-" * 64)
    trace = Trace()

    # ---- Think 1: 定位客户 ----
    trace.log("[Think] 从任务中抽取客户名，在图中定位 Customer 节点")
    customer = g.find_customer_by_name(customer_name)
    if customer is None:
        trace.log("[Decide] 未找到客户，转人工坐席。（这就是一个真实分支）")
        return {"action": "transfer_to_human", "reason": "customer_not_found"}
    trace.log(f"[Act]   命中 {customer}")

    # ---- Act 1: 沿 HAS_CONTRACT -> SUBSCRIBES -> DEPLOYS_AT 遍历 ----
    trace.log("[Act]   沿 HAS_CONTRACT -> SUBSCRIBES -> DEPLOYS_AT 做图遍历")
    affected_services = []
    affected_sites = []
    for _, kid in g.out(customer.nid, "HAS_CONTRACT"):
        for _, sid in g.out(kid, "SUBSCRIBES"):
            svc = g.nodes[sid]
            affected_services.append(svc)
            trace.log(f"        合约 {g.nodes[kid].props['name']} 包含业务 {svc}")
            for _, csid in g.out(sid, "DEPLOYS_AT"):
                site = g.nodes[csid]
                affected_sites.append(site)
                trace.log(f"          业务部署于 {site} (状态={site.props['status']})")

    # ---- Observe: 检查是否存在已 OPEN 工单（A1/A2 约束） ----
    trace.log("[Observe] 检查该客户名下 OPEN 工单是否已存在（约束 A1/A2）")
    open_tickets = [g.nodes[t] for (_, t) in g.out(customer.nid, "REPORTED")
                    if g.nodes[t].props.get("status") == "OPEN"]
    for t in open_tickets:
        trace.log(f"        已有未结工单 {t.nid}: {t.props['desc']} (P{t.props['priority'][-1]})")

    # ---- Decide: 套 T-box 约束 ----
    trace.log("[Decide] 套用 T-box 业务规则判定根因")
    root_cause = "customer_side"   # 默认：客户侧问题
    for site in affected_sites:
        if site.props["status"] == "DOWN":
            root_cause = "site_outage"
            trace.log(f"        规则 A3 命中：{site.props['name']} 状态 DOWN "
                      f"=> 判定为站点/局端故障，非客户侧问题")
            break

    # 匹配工单影响的业务
    if open_tickets:
        for tk in open_tickets:
            for _, sid in g.out(tk.nid, "AFFECTS"):
                trace.log(f"        工单 {tk.nid} 关联业务 {g.nodes[sid].props['name']}")

    # 规则 A4: VIP 升级
    priority = "P3"
    if customer.props["tier"] == "VIP":
        priority = "P1"
        trace.log("        规则 A4 命中：VIP 客户 => 工单升级 P1")

    # 派单：按覆盖区域选工程师
    area_names = {g.nodes[a].props["name"] for cs in affected_sites
                  for (_, a) in g.out(cs.nid, "COVERS")}
    assigned = None
    for tech in g.find_by_type(TECH):
        if tech.props["covers"] in area_names:
            # VIP 必须 senior
            if customer.props["tier"] == "VIP" and tech.props["level"] != "senior":
                continue
            assigned = tech
            break

    plan = {
        "customer": customer.props["name"],
        "tier": customer.props["tier"],
        "symptom": symptom,
        "root_cause": root_cause,
        "priority": priority,
        "affected_services": [s.props["name"] for s in affected_services],
        "affected_sites": [s.props["name"] for s in affected_sites],
        "assigned_technician": assigned.props["name"] if assigned else "待调度",
        "open_tickets": [t.nid for t in open_tickets],
    }
    print("-" * 64)
    print("[数字孪生处置方案]")
    for k, v in plan.items():
        print(f"  - {k}: {v}")
    print("=" * 64)
    print()
    return plan


# ============================================================
# 第四部分：跑 3 个真实测试用例，输出可验证记录
# ============================================================

if __name__ == "__main__":
    print("C8 Project B 早期验证物：电信本体 Agent 原型")
    print("运行时间基准：本机 python", __import__("sys").version.split()[0])
    print()

    g = build_demo_graph()

    # Case 1：李先生——其宽带部署在 DOWN 的分纤箱 => 根因应判为 site_outage
    agent_handle_task(g, "李先生", "百兆宽带突然断网，光猫红灯")

    # Case 2：张女士（VIP）——其业务所在机房正常，但应被 A4 升级为 P1
    agent_handle_task(g, "张女士", "5G 信号时有时无，家里老人急需上网课")

    # Case 3：未注册客户——应走 transfer_to_human 分支
    agent_handle_task(g, "陌生人", "手机号打不通")

    print("[自检] 三个用例均已执行完毕，处置方案见上方输出。")
    print("下一步（入选后）：把内存 Graph 换成 Neo4j，把 Think 换成 LLM+NL2SQL。")
