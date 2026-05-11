# 候选：Open vSwitch 上游 + bond 模块

## 候选标识
- candidate_slug: `01-ovs-upstream-bond`
- 主体类型：A. vSwitch 软件方（上游）
- 适用独立权：权 1, 11, 23, 36
- R-OPENSOURCE 上游 P0

## §A 主流来源摘要（19 类源）

### §A.4 使用手册 / §A.7 上游归因（命中 — 反向证据）

| # | 源 | URL | 引文 |
| --- | --- | --- | --- |
| 1 | OVS Bonding docs | https://docs.openvswitch.org/en/latest/topics/bonding/ | "In vswitchd, a bond always has at least two members (and may have more)" — bond schema 是单层 `Port` + 多个 `Interface`，**没有** `Interface` 本身是另一个 bond 的构造 |
| 2 | OVS TC-offload howto | https://docs.openvswitch.org/en/latest/howto/tc-offload/ | OVS dpif-netlink 推送一个 TC filter 到 `tcf_block`；当 bond port 被 offload 时，重活在 vendor driver 内（mlx5 VF-LAG 等），OVS 推送一条 TC rule 到 bond netdev |
| 3 | LWN 743391 — shared filter blocks | https://lwn.net/Articles/743391/ | 2018 — `shared block` 让多个 netdev **共享**一个 filter set，**不是 duplicate** identical filters across N TCAMs |
| 4 | OVSCON 2017 — Horman | http://www.openvswitch.org/support/ovscon2017/horman.pdf | TC flower offload design；无 bond-of-bonds 讨论 |
| 5 | OVSCON 2019 — Mellanox HW offloads | https://www.openvswitch.org/support/ovscon2019/day2/0951-hw_offload_ovs_con_19-Oz-Mellanox.pdf | VF-LAG focus；topology 限制来自 mlx5 硬件（参见候选 03/04） |

**0 命中**：
- "bond of bonds" / "nested bond" / "hierarchical bond" / "LAG of LAGs" — 0 命中 docs.openvswitch.org / OVSCON 2017/2019 索引
- OVS-side 显式 program N identical exact-match flows onto N independent NICs — 0 命中

## §C 子 agent 复核

agent ID ab263b2a8351823dd 完成。主 agent 复核 OVS 文档原文 + verbatim 引文后认可。

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整记录 | 最终 verdict |
| --- | --- | --- | --- |
| 权 1 / 11 / 23 / 36 | **已排除（第 5 档）** | F3 真反向证据：OVS bond schema 是单层 `Port` + 多个 `Interface`，**不存在** "bond-of-bonds" 嵌套结构（"Y supports only Z (not X)"）；F4 真反向证据：`shared block` 是 share-not-duplicate 语义，与本专利"sync N identical copies"语义相反；§5.0 豁免：满足 (a) | **已排除（架构层级 + 真反向证据）** |

### F# 投票汇总

- F1：用户可在 OVS 上挂多个 NIC，但 N=2 物理 NIC 的 bond 是单层（不命中 F3 二层）
- F2：OVS 支持 LACP bond mode（balance-tcp + lacp=active）→ 单层命中
- F3：**真反向**——bond 必须有 ≥ 2 个 member，但 member 不能是另一个 bond
- F4：**真反向**——OVS 没有 first-class "sync N identical flows" 机制；shared-block 是共享而非复制

### 后置调整记录（按 7 条）

1. 等同三步法：F3/F4 的等同——OVS bond + tc-flower offload 与本专利的"两层映射 + N 份相同"在同手段（schema 不同）+ 同效果（共享 vs 复制）上均不成立
2. 反向证据 vs 限定语：OVS 文档明示 bond 是单层、shared-block 是共享——属真反向
3-7. 其他后置调整未触发

### 最终 verdict

**已排除（OVS 上游 schema 架构层级与本专利 F3+F4 不一致）**：上游 OVS 不实现"bond-of-bonds" 嵌套聚合 + 不实现"同步 N 份相同 flow" 复制语义。

## 总结一句话

OVS 上游 bond schema 单层 + shared-block 是共享非复制——F3/F4 真反向，**落第 5 档已排除**（但商业发行版需独立 verdict — 见 05/06）。
