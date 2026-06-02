# 证据索引 — 11-broadcom-stingray

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2026(更新) | techdoc | https://techdocs.broadcom.com/us/en/storage-and-ethernet-connectivity/ethernet-nic-controllers/bcm957xxx/adapters/ovs-tc-and-dpdk-offload/ovs-flow-offloads.html | TruFlow/OVS 硬件流表卸载存在；仅单设备/逐端口配置，无跨多卡 bond、无流表向全部网卡下发、无单卡单点故障论述 |
| 2 | 2026-04-10 | techdoc | https://techdocs.broadcom.com/us/en/storage-and-ethernet-connectivity/ethernet-nic-controllers/bcm957xxx/adapters/introduction/features/virtualization-offload.html | 虚拟化卸载特性（VMQ/tunnel）；无 LAG/跨卡冗余 |
| 3 | n/a | 检索 | (WebSearch) SR-IOV VF LAG | bond/LAG 硬件卸载以 VF-LAG（**单卡多端口**）描述："VF representor port configuration should only be made on the first network port on the card" |

## Phase 1 — react 粗筛 query 留痕
- query 1: `Broadcom Stingray SmartNIC flow table offload OVS multiple NIC LACP`
  → 命中相关：Broadcom TruFlow / OVS 硬件流表卸载存在；命中的 LAG 材料均为内核通用 "distribute filters to all lower devices" 机制（非 Broadcom 专属，非跨独立网卡聚合证据）。
- query 2: `Broadcom TruFlow OVS offload bond LAG two NICs flow table all ports redundancy`
  → 命中相关：TruFlow 支持 generic flow offload；bond/LAG 卸载以 **SR-IOV VF LAG**（单卡多端口）描述，未见跨多块独立网卡。
- query 3: `Broadcom NetXtreme bond LAG hardware offload across two separate adapters bnxt active-backup limitation`
  → 无跨多卡 LAG 硬件卸载的正向材料；命中 "Use of VF-LAG halfs the offloaded port capacity of the card ... VF representor port configuration should only be made on the first network port on the card"（VF-LAG = 单卡两端口形态）。

## Phase 2 — WebFetch
- WebFetch techdocs OVS Flow Offloads → 仅描述单设备/逐端口配置（Normal/Secure 模式、VxLAN、NAT、TC rule），无跨多卡 bond、无流表向全部网卡下发、无单卡单点故障消除论述。
- WebFetch techdocs Virtualization Offload（Last Updated 2026-04-10）→ 仅 multiqueue/VMQ/tunnel offload，无 LAG/跨卡冗余论述。

## 工具受限说明
- 无付费墙/登录墙阻碍；Broadcom techdocs 公开可访问。
- 候选实际是否在内部支持"跨多块独立网卡 LACP 聚合 + 流表向全部 N 网卡下发"无公开材料证实或证伪——属公开资料不足，非反向证据。
