# 证据索引 — 03-intel-e810-ovs-offload

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| Q1 | 2026-06 | WebSearch | `Intel E810 OVS TC hardware offload bonding LAG flow table` | E810 switchdev 支持 OVS TC-Flower 硬件卸载 + SR-IOV VF LAG；命中 F2/F4 语义（流表卸载、bond） |
| Q2 | 2026-06 | WebSearch | `Intel E810 ice driver bond LAG offload two ports same NIC vs across multiple NICs` | 多为 bond 引起 driver hang 的 bug 报告；未直接给"跨多卡同步卸载"证据 |
| Q3 | 2026-06 | WebSearch | `E810 switchdev SR-IOV VF LAG bond two PFs hardware offload flows duplicated failover` | 关键：VF LAG 需"先把 NIC 的两个 PF 都置 switchdev，再 bond uplink 表征口"；active-backup/LACP/XOR；流量在两端口间分发——**单卡两 PF** 语义 |
| F1 | 2021-08-30 | PDF(curl+pdfplumber) | E810_eSwitch_switchdev_TechConfigGuide.pdf (Rev1.0) | 本 Rev1.0 未覆盖 VF-LAG/bond 细节（仅 UL_PR/VF_PR 表征口机制）；提取文本存 `_e810_extract.txt` |
| F2 | 2026-06 | WebFetch | NVIDIA VF-LAG QSG (docs.nvidia.com) | verbatim "the two network interfaces from the NIC PFs are bounded"；示例 PCI `61:00.0` + `61:00.1`——**同一张卡的两个 PF**；offload 在两端口分发 |
| Q4 | 2026-06 | WebSearch | `Intel E810 OVS hw offload bond across two separate physical NICs not supported` | 关键反向：(a) "Issuing ethtool or tc commands to a bonded ice interface ... not supported"；(b) "eSwitch per {PF: LAN port} pair"——**offload 是 per-PCI-device/per-eSwitch，无法跨多张独立物理卡** |

> 受限说明：Intel 官方 Rev1.0 PDF 未含 VF-LAG 章节；架构判定依据 NVIDIA VF-LAG 文档（同属 SR-IOV VF-LAG 机制族）+ Intel 社区/驱动层"per-PCI-device eSwitch"与"bonded ice interface tc/ethtool not supported"陈述。未检索到 E810 在 N≥2 独立物理网卡间把同一精确流表同步卸载到全部网卡的公开来源。
