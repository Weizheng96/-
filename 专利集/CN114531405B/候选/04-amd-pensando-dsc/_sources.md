# 证据索引 — 04-amd-pensando-dsc

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2026-06 检索 | WebSearch | `AMD Pensando DSC DPU flow table offload virtual switch P4` | Pensando DPU 用 P4 做有状态流表卸载，首包 miss 走 exception/slow path 装流表 → 命中 F2/F4 语义 |
| 2 | 2026-06 检索 | WebSearch | `Pensando DPU bonding LAG multiple NIC flow table sync offload HA` | 未见跨多块独立网卡的 LACP 聚合 / 流表同步卸载；通用 offload 能力描述 |
| 3 | 2026-06 检索 | WebSearch | `AMD Pensando DPU dual card redundancy cross-card flow state failover` | 仅见单卡 fast path 内 Active-Active/Active-Passive HA state machine，非跨独立网卡流表同步 |
| 4 | June 2023 | PDF(本地) | `dsc-200-product-brief.pdf`（源 amd.com /pensando-dsc-200-product-brief.pdf） | 单卡 2 端口 QSFP56；HA = "a pair of DSCs ... can provide high availability to redirected workloads"（appliance 级 redirect HA，非 LACP 聚合 + 流表同步卸载至全部网卡） |
| 5 | 2026-06 检索 | WebSearch | `Pensando DSC high availability pair active-passive flow state replication redirect` | 无 Pensando 专属 HA flow-state 同步细节；HA 走 redirect/appliance 配对 |
