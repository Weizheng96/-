# 证据索引 — 14-azure-smartnic-boost

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2018 | WebSearch | Azure Accelerated Networking SmartNIC FPGA flow offload GFT | 确认 AccelNet/VFP 首包送软件、后续流卸载到 FPGA SmartNIC 的 GFT（Generic Flow Table）→ 对应 F4（miss 触发卸载）语义 |
| 2 | 2018 | PDF（本地） | nsdi18-firestone-AccelNet.pdf（https://www.usenix.org/system/files/conference/nsdi18/nsdi18-firestone.pdf） | NSDI'18 论文，AccelNet/GFT 机制原始出处，L1 证据；已落盘 754KB |
| 3 | 2026-02-05（更新） | WebFetch | https://learn.microsoft.com/en-us/azure/virtual-network/accelerated-networking-overview | **关键反向证据**：AccelNet 的"bonding"是 SR-IOV VF **transparently bonded to a synthetic hv_netvsc device**（VF↔合成设备透明绑定，用于 live migration/VF 动态收发），**非 N≥2 独立物理网卡 LACP 聚合**；全文无 LACP、无多物理网卡聚合、无跨网卡流表同步 |
| 4 | — | WebSearch | Azure ... single NIC per VM bonding redundancy | 二手确认"transparent bonding ... enables redundancy **without requiring multiple physical NICs per VM**"——与本专利 F1（N≥2 网卡）正相反 |

> 受限说明：WebFetch 对 NSDI'18 PDF 的正文文本抽取不完整（PDF 编码段未解析），但 GFT 机制由 WebSearch#1 与官方 Learn 文档交叉佐证；多网卡聚合/LACP/跨网卡同步的反向结论以官方 Learn 文档（来源#3）为准，证据充分。
