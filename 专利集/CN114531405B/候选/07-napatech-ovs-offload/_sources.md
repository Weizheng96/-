# 证据索引 — 07-napatech-ovs-offload

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | — | WebSearch | `Napatech OVS full offload SmartNIC FPGA flow table VXLAN` | 有信号：全 OVS 卸载 / FPGA 数据面 / VXLAN/VLAN / flow cache / hardware flow matcher + learning subsystem |
| 2 | — | WebSearch | `Napatech OVS offload link aggregation bonding LACP multiple NIC redundancy` | 无 Napatech 专属信号（仅通用 OVS bond/LACP 文档：Red Hat/Intel/Nutanix） |
| 3 | — | WebSearch | `Napatech SmartNIC multiple cards bonding failover flow table synchronization across NICs` | 多卡仅限抓包时间同步/数据 merge，非卸载场景跨卡冗余 |
| 4 | 2019-02-06 | WebFetch | https://www.napatech.com/light-at-the-end-of-the-tunnel-ovs-offload/ | 单 SmartNIC 卸载；无 LACP/bonding/跨卡流表复制；"two servers each running OVS"=两台独立服务器经 VXLAN 互联 |
| 5 | — | WebFetch | https://www.napatech.com/support/resources/solution-descriptions/virtual-switch-offload-solution/ | 仅 CPU 减负/ROI/性能；无单卡 vs 多卡、无 LACP 多卡聚合、无跨卡流表同步 |

**受限说明**：公开资料未出现"精确流表同步卸载至 N≥2 块独立网卡 + LACP 聚合为一逻辑端口"的架构；Napatech 卸载一致呈现为单 SmartNIC fast-path。

**结论**：仅 F4 命中（通用 miss 触发卸载机制）；F1/F2/F3/F5 未命中，F1/F5 为架构反向（单卡 vs N≥2 跨卡同步）→ 第 5 档（已排除）。
