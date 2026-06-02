# 07-napatech-ovs-offload — 检索留痕 (_sources.md)

专利：CN114531405B 流表处理方法（华为）；授权日 2023-06-06（时间窗起算）
候选：Napatech 全 OVS 卸载 SmartNIC（FPGA），Link-Virtualization 软件

## Phase 1 — 粗筛 WebSearch 留痕（react 串行）

- query 1: `Napatech full OVS offload SmartNIC FPGA LACP multiple NICs flow table`
  → 命中相关。Napatech full OVS offload（数据面卸载，控制面/慢路径仍在 host），~6x 性能；HW megaflow/flow table 移入 SmartNIC；支持 up to 2x100G、link aggregation 列为特性。信号：相关但需确认聚合作用域（卡内 vs 跨卡）。

- query 2: `Napatech Link-Virtualization bonding LACP multiple SmartNIC redundancy failover OVS offload flow rule all NICs`
  → 命中相关。机制为 megaflow caching：「only new and unknown flows are resolved in the host CPU」「The megaflow cache in the SmartNIC hardware is automatically updated when a change is made to the OVS megaflow cache」。**搜索结果明确：未含 bonding 模式(LACP)、多网卡冗余配置、跨卡 failover 的具体细节**。另见 specs.openstack.org Nova-spec（support-napatech-linkvirtualization-smartnic，2023.2）可作升级路径取证点。

（累计 2 条 WebSearch，已有足够信号定档，未走早剪枝——F4 有等同信号，非 0 命中。）

## Phase 2 — 深抓 WebFetch 留痕（react 串行）

- WebFetch: virtual-switch-offload-solution
  → 架构：FPGA SmartNIC/DPU 卸载虚拟交换；明确举例「NT200A02 SmartNIC with dual 25Gbps ports」=单卡多端口。未公开"多块独立 SmartNIC""跨卡 LACP""流表向全部卡下发"。

- WebFetch: light-at-the-end-of-the-tunnel-ovs-offload（blog）
  → **发布日期 2019-02-06 < 2023-06-06 授权日 → 现有技术，不计入侵权证据**，仅作架构背景。SmartNIC PMD 直接接管 VirtQueue，~6x。无 LACP/多卡/冗余描述。

- WebFetch: products/link-virtualization-software（产品页）
  → megaflow cache 自动从 host OVS 同步至 SmartNIC HW cache；Virtio-net 支持 Live Migration。单卡 cache 同步机制。

- WebFetch: data-sheets/link-virtualization-software（数据表，Copyright 2026）
  → 「Link aggregation (active/active and active/standby)」列为特性；「Non-degrading HW Megaflow cache for tracking billions of flows」。**未公开**链路聚合作用域（卡内/跨卡）、N≥2 独立卡、流表向全部卡分发、跨卡 failover/SPOF 消除。

## 工具受限说明
- 无登录墙/付费墙阻碍；以上均公开 vendor 文档可达。
- 未深抓 OpenStack Nova-spec（specs.openstack.org）——已记入升级路径，本轮预算内未展开。

## 结论
F4 等同命中（megaflow miss→host→HW cache）；F1/F2/F3/F5 因公开文档只述单卡形态、megaflow 单卡同步，未触及本专利核心区分点（N≥2 独立网卡 + 跨卡 LACP + 精确流表向全部网卡冗余下发），判公开资料不足。无 vendor 明示"仅单卡"的正向反向证据 → 不构成第5档。**落第 4 档（公开资料不足，弱候选）**。
