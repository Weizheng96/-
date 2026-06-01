# 证据索引 — 06-broadcom-stingray

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| q1 | — | WebSearch | "Broadcom Stingray SmartNIC Thor flow table offload OVS data plane" | TruFlow / OVS 卸载 / Stingray SoC SmartNIC，有信号 |
| q2 | — | WebSearch | "Broadcom Stingray TruFlow bonding LAG multiple NIC flow offload synchronize all cards failover" | TruFlow per-adapter，未见跨卡同步 |
| q3 | — | WebSearch | "Broadcom bnxt OVS offload bond LAG single port representor flow not synchronized across separate NICs" | bond=PF/端口；卸载粒度单设备 representor/eSwitch |
| 1 | 2026-04-10 | WebFetch | https://techdocs.broadcom.com/us/en/storage-and-ethernet-connectivity/ethernet-nic-controllers/bcm957xxx/adapters/introducing-truflow.html | TruFlow per-adapter 流分类器卸载；无 bond/LACP/跨卡同步 |
| 2 | 2026-04-10 | WebFetch | https://techdocs.broadcom.com/us/en/storage-and-ethernet-connectivity/ethernet-nic-controllers/bcm957xxx/adapters/ovs-tc-and-dpdk-offload/ovs-flow-offloads.html | VxLAN/NAT/TC flower 示例；无 bond/LAG/跨卡同步 |
| 3 | 2020-03-11 | WebFetch | https://hareshkhandelwal.blog/2020/03/11/lets-understand-the-openvswitch-hardware-offload/ | 流装单设备 eSwitch、不跨 bond 成员复制（关键反向证据 F5） |

## 受限说明
Broadcom 官方 TechDocs WebFetch 未返回 bond/LACP/跨卡流表同步逐字内容；F5 反向依据取自 OVS 硬件卸载通用机制（eSwitch per-device）公开描述，非 Broadcom 官方逐字声明。关键证据均为 HTML 页面，已逐字摘录，未下载 PDF。
