# 证据索引 — 09-marvell-octeon10

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2023-10/11 | WebFetch PDF | https://www.marvell.com/content/dam/marvell/en/public-collateral/embedded-processors/marvell-octeon-10-dpu-platform-product-brief.pdf | OCTEON 10 DPU 通用定位；无单卡vs多卡部署、无跨卡LACP、无流表向多卡冗余下发描述 |
| 2 | 2025-07（页修改日） | WebFetch | https://cloudswit.ch/product/asterfusion-dpu-based-smartnic-marvell-octeon-tx-cn9670-ovsnfv-offload/ | 「Dual 100GE QSFP28 ports」「2x100G」=单卡双端口架构；OVS offload罗列；无多卡集群/跨独立网卡LACP/分布式流表冗余 |
| 3 | — | WebSearch | （query 1）OCTEON 10 DPU OVS offload + LACP cross-card redundancy | 确认有 OVS offload 能力；无跨多块独立网卡聚合/流表全卡下发描述；架构=单DPU卡per host全卸载 |
| 4 | — | WebSearch | （query 2）Asterfusion Helium OVS offload dual NIC bond LACP redundancy | Helium=单卡(2x100G/4x25G)做OVS offload；出现「LACP should not be used with OVS-based bonds」通用建议 |
| 5 | — | WebSearch | （query 3）OCTEON DPU HA redundancy two cards failover | OCTEON的HA=交换机/网关层 MC-LAG + BFD sub-50ms failover；双DPU经10G以太背板集成充当gateway/router；非host vSwitch跨N≥2独立网卡+流表全卡冗余下发 |

## 检索小结
- Phase 1 三条 WebSearch（串行）+ Phase 2 两条 WebFetch（串行）。
- 关键发现：OCTEON / Asterfusion 公开资料中，OVS offload 一致呈现为「**单卡** OVS 全卸载」（一块 DPU per host，单卡多端口）；HA 由「**交换机层 MC-LAG**」承担。两者均与本专利「host vSwitch 跨 **N≥2 块独立网卡** LACP 聚合 + 精确流表向**全部 N 块网卡**冗余下发」不在同一架构层级。
- F3/F5 的核心区分点（跨多块独立网卡 LACP + 流表全卡冗余下发）在所有公开资料中均未出现，亦无候选自有专利/文档明示采用另一套手段实现同目标 → 属「单实体内子部件聚合 + 公开资料不足」，非字面命中、亦无正向反向证据。

## 工具受限说明
- 无付费墙 / 登录墙阻断；上述均为公开页面。
