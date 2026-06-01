# _verdict.md — 04-amd-pensando-dsc

## 候选基本信息
- slug：04-amd-pensando-dsc
- 名称：AMD Pensando DSC（DSC2-200）DPU 流表卸载
- vendor / 组织：AMD（Pensando）
- 类型：产品
- 公开度：中
- 关键文档时间：DSC2-200 Product Brief = **2023 年 6 月**（≥ 专利公开日 2023-06-06，时间窗在边界、可参与判定）
- 命中 F#（初判）：F1, F2, F4, F5

## 检索粗筛
- WebSearch #1 `AMD Pensando DSC DPU flow table offload virtual switch P4` → 有信号（P4 流表卸载 + 首包 miss 慢路径装表）
- WebSearch #2 `Pensando DPU bonding LAG multiple NIC flow table sync offload high availability` → 无跨独立网卡聚合/流表同步信号
- WebSearch #3 `AMD Pensando DPU dual card redundancy cross-card flow state failover single point of failure` → 仅单卡 fast-path 内 HA state machine，无跨独立网卡流表同步
- 结论：有外围信号，进入 Phase 2 深抓。

## F# 命中表

| F# | 限定要点 | 判定 | 证据（verbatim） | URL | 备注 |
| --- | --- | --- | --- | --- | --- |
| F1 | 虚拟交换机连接 M 个虚机 + **N 个网络接口卡（N≥2，跨多块独立网卡）** | **不命中 / 公开资料不足** | Pensando DSC 为单卡设备："2 ports QSFP56"；HA 形态为 "a pair of DSCs installed either within the same appliance or within different appliances can provide high availability to **redirected** workloads"——appliance 级 redirect HA，非"一台虚拟交换机聚合 N 块独立网卡" | dsc-200-product-brief.pdf（amd.com） | 单卡多端口 ≠ 专利"跨多块独立网卡"；HA 走流量重定向，不是把 N 块网卡聚合为第一端口 |
| F2 | 将 N 个逻辑端口经映射**聚合为一个"第一端口"** | **不命中** | 公开材料仅描述单卡内 P4 流表与端口；未见"将多块独立网卡的逻辑端口聚合为单一第一端口"的映射机制 | WebSearch #2/#3 | 核心创新点之一，无公开证据 |
| F3 | 每网卡逻辑端口由其物理端口**基于 LACP** 聚合形成 | **不命中** | 未检索到 Pensando 把跨卡流表卸载建立在 LACP 聚合逻辑端口之上的公开来源 | WebSearch #2/#3 | 硬限定，无证据 |
| F4 | 卸载流表 **miss 作为触发**（cache-miss-driven offload） | **命中** | "When the first packet of a session arrives, flow lookup in the P4 data path fails and the packet is sent to an exception path (slow path), where software ... install flow/session entries" | WebSearch #1（amd.com SDN/SSDK 资料转述） | 首包 miss → 慢路径装表，语义与 F4 一致，但属业界 SmartNIC 通用做法 |
| F5 | 通过第一端口将精确流表**卸载至 N 个（全部）网卡** | **不命中 / 不同机制** | 公开 HA 机制为 "a pair of DSCs ... provide high availability to **redirected** workloads"——靠重定向到另一对卡实现可用性，而非把同一精确流表**同步卸载到聚合内全部 N 块独立网卡** | dsc-200-product-brief.pdf | F5 是消除单点故障的核心限定；Pensando 用 redirect-HA 达到类似目标但属 different mechanism，且仍缺"流表同步至全部网卡"要素 |

## 已检查文档清单
1. WebSearch：`AMD Pensando DSC DPU flow table offload virtual switch P4`
2. WebSearch：`Pensando DPU bonding LAG multiple NIC flow table sync offload high availability`
3. WebSearch：`AMD Pensando DPU dual card redundancy cross-card flow state failover single point of failure`
4. 本地 PDF：`dsc-200-product-brief.pdf`（DSC2-200 Product Brief，2023 年 6 月，源 amd.com）— 已 pdfplumber 提取全文核对
5. WebSearch：`Pensando DSC high availability pair active-passive flow state replication redirect mechanism`

## 最终判定：**第 4 档：弱命中 / 命中 <60%**

依据（1–3 句）：
- Pensando DSC 仅在**外围特征**命中——F4（首包 miss 触发慢路径装表）属业界通用 cache-miss-driven offload；F2 的"流表卸载"能力存在但不涉及多网卡聚合。
- 专利的**全部区分性限定**（F1 跨 N≥2 块独立网卡 / F2 聚合为第一端口 / F3 LACP 来源 / F5 精确流表同步卸载至全部 N 块网卡）均无公开证据；Pensando 为单卡架构，其 HA 是"一对 DSC + 流量 redirect"，与"把同一流表同步卸载到 LACP 聚合全部网卡"为不同机制。
- 不满足第 5 档"已排除"硬条件：无明确"不支持/excludes"反向陈述、关键文档时间未全部早于公开日、领域高度相关（虚拟交换机硬件流表卸载正是专利场景 2/3）；0 命中区分特征 ≠ 已排除，故落第 4 档。

## 升级路径（仅 3-4 档）
- 抓取 AMD Pensando SSDK / SDN Policy Offload 参考流水线文档与 Aruba CX / Cisco 集成白皮书，确认是否存在"跨两块独立 DSC + LACP bond + 流表同步卸载"配置；若有可升至 3 档。
- 核查 Pensando HA 是否做**流表/会话状态向第二块卡的同步复制**（state replication）而非纯 redirect；若为同步复制至全部成员卡，则 F5 或构成等同，升至 3 档。
- 核查 OVS-offload / DPDK rte_flow 在 Pensando 上是否支持 bond 成员同步下发规则（F2/F5 等同点）。

## 总结一句话
AMD Pensando DSC 仅命中通用的 miss 触发流表卸载（F4）与流表卸载能力（F2 部分），缺失专利全部区分性限定（N≥2 跨独立网卡 + LACP 聚合第一端口 + 流表同步卸载至全部网卡），其 HA 为单卡/一对卡 redirect 机制而非跨网卡流表同步，落第 4 档。
