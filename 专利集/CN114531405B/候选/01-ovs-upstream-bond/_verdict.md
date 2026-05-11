# Verdict — Open vSwitch 上游 bond port + tc-flower offload（核心技术 CT-1）

> 主体类型：S1（上游开源）+ S5（多发行版分发）
> 适用独立权：权 1 / 23 / 36
> 分级：**P0**（依据 R-3 R-OPENSOURCE 双层激活——上游开源项目列入 P0）

## 1. 核心组织
- Linux Foundation Networking（OVS 项目宿主，非营利）
- Red Hat（IBM 子公司，NYSE: IBM）—— 主要 maintainer
- Mellanox / NVIDIA（NASDAQ: NVDA）+ Intel（NASDAQ: INTC）+ Cisco（NASDAQ: CSCO）—— 多 maintainer

## 2. F1-F5 命中表

| F# | 证据原文 | 来源 | 命中 |
|---|---|---|---|
| F1 | OVS 主仓库支持任意数量 NIC 通过 bond port 聚合；上游不限制 N（用户决定）| OVS bonding.rst | **字面命中**（OVS 上游本身支持 N ≥ 2 部署）|
| F2 | "LACP bonding requires the remote switch to implement LACP... after LACP negotiation is complete, there is no need for special handling of received packets" | [OVS bonding.rst](https://github.com/openvswitch/ovs/blob/main/Documentation/topics/bonding.rst) | **字面命中**（LACP 802.3ad mode 是 OVS 上游主线 feature）|
| F3 | `ovs-vsctl add-bond <br> <bond_port> <slave1> <slave2>` — bond port 是"第一端口"等价物 | OVS ovs-vsctl(8) man page | **字面命中**（bond port 抽象 + 端口聚合 API）|
| F4 | OVS dpif-netdev datapath 标准 miss-to-upcall 机制 | OVS pmd.rst（CN104834566A 候选 01 已抓取）| **字面命中**（OVS 标准 miss handling，与 bond 无关）|
| F5 | OVS 把规则通过 tc-flower / OVS-DOCA 推给底层 driver；**OVS 自身不实现跨卡 HW offload 同步**——委托给 driver | OVS Documentation/howto/tc-offload.rst（推断）| **公开资料不足**（OVS 是 enabling layer；F5 的"多卡同时下发硬件流表"实际由 driver 完成）|

## 3. 配置参数双引证（R-CONFIG）

| 参数 | prose 引文 | 对应 F# |
|---|---|---|
| `ovs-vsctl add-bond <br> <bond> <slave1> <slave2>` | OVS man page | F3 bond port 创建 |
| `bond mode = balance-tcp / balance-slb / active-backup` | OVS bonding.rst（LACP 是 balance-tcp + lacp=active 组合）| F2 LACP 启用 |
| `lacp=active` / `lacp=passive` / `lacp=off` | OVS bond attributes | F2 LACP 模式 |
| `other_config:bond-detect-mode` | OVS man page | F2 状态机参数 |

## 4. 时间线交叉验证

- OVS bond port + LACP 支持：OVS 1.x 早期已有（远早于专利申请日 2020-10-31）
- tc-flower hardware offload 集成：OVS 2.8+（2017+）
- 持续 ship 至 OVS 3.7.x（2025+）
- **时间档**：post-grant（所有 OVS bond port 功能在专利授权日 2023-06-06 之后仍持续 ship）

**现有技术 caveat 警示**：OVS bond port + LACP 在 2020-10-31 前已存在，可能影响本专利新颖性判定——但本专利的实质创新点在"卡间映射到第一端口 + 多卡同步 HW offload"的具体编排，OVS 上游本身**不实现** F5 的硬件同步逻辑，因此现有技术风险有限。

## 5. §A 19 类源穿透扫描

| # | 源类别 | 命中要点 |
|---|---|---|
| 1 | 反向专利墙 | OVS 上游不持有专利（基金会项目）；多 maintainer 公司各自有同主分类专利墙——建议法务 IncoPat 补查 |
| 2 | 学术论文 | OVS 设计论文（USENIX NSDI 2015 "The Design and Implementation of Open vSwitch"）+ FB DPDK summit 系列 |
| 3 | 宣传材料 | openvswitch.org 官网 |
| 4 | 使用手册 | OVS 主仓库 Documentation/ 全部 + man pages |
| 5 | 行业标准 | LACP IEEE 802.3ad / 802.1AX |
| 6 | 联合案例（R-PARTNER）| Red Hat × Intel × NVIDIA OVS-DPDK + bond reference patterns |
| 7 | 上游归因（R-OPENSOURCE）| Red Hat / Intel / NVIDIA / Cisco maintainer 邮箱域 git log |
| 8 | 开源 fork | NVIDIA OVS-DOCA fork 单独评估（见候选 04 T-B）|
| 9 | 现有技术 | OVS bond port LACP 主线 feature 早于专利申请日；具体多卡同步 HW offload 在 OVS 主仓库未明示完整实现 |
| 10-19 | 招聘 / 财报 / 案例 / 招标书等 | 略——R-PROCURE 命中三大运营商集采技术应答书 |
| 20 | 反向工程 | 不需要（OVS 主仓库是开源代码）|

## 6. 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整 | 最终 verdict |
|---|---|---|---|
| 权 1 / 23 / 36 | **第 3 档：公开资料不足（强候选）** — F1/F2/F3/F4 字面命中；F5 OVS 上游本身不实现跨卡 HW offload 同步 | 1.等同未触发；2.反向证据未触发；3.Active 不降级；4.现有技术 caveat：OVS bond port + LACP 主线 feature 早于专利申请日，但本专利创新点在 F5 多卡同步编排，OVS 上游不实现 → caveat 风险有限；5.R-STANDARD 未触发；6.§5.0 豁免未触发；7.Patent license：建议法务核查华为是否对 Linux Foundation / OIN 做过 patent commitment | **第 3 档：公开资料不足（强候选）** |

## 7. 升级路径

- 法务核查华为 OIN 成员承诺 / Linux Foundation patent commitment
- 本地 git clone OVS + `git log -- Documentation/topics/bonding.rst` 审查 LACP + tc-flower offload 协作的具体设计
- 深读 NVIDIA OVS-DOCA fork 是否在上游基础上加了"多卡同步下发"路径

## 8. 总结一句话

OVS 上游 bond port + LACP + tc-flower offload 接口：F1-F4 字面命中（bond port 抽象 + LACP 802.3ad mode + miss handling）；F5 OVS 上游本身是 enabling layer（实际 HW offload 由 driver 完成）→ 公开资料不足；落第 3 档强候选 + patent license caveat 待法务核查。
