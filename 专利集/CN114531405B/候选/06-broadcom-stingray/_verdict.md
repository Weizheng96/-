# 候选 06 — Broadcom Stingray SmartNIC / Thor 流表卸载 _verdict

## 候选基本信息
- 名称：Stingray SmartNIC / Thor 流表卸载（TruFlow）
- 组织：Broadcom
- 类型：产品
- 初判命中 F#（取自 _meta.json）：F1, F2, F4, F5
- 公开日基准（时间窗）：2023-06-06（专利授权公告日，取自 _meta.json / Step 2）

## 检索粗筛（query 留痕）
- WebSearch q1: "Broadcom Stingray SmartNIC Thor flow table offload OVS data plane" → 有信号（Stingray SoC SmartNIC，TruFlow 流卸载，OVS 卸载）
- WebSearch q2: "Broadcom Stingray TruFlow bonding LAG multiple NIC flow offload synchronize all cards failover" → TruFlow per-adapter 流分类器卸载，未见跨卡同步
- WebSearch q3: "Broadcom bnxt OVS offload bond LAG single port representor flow not synchronized across separate NICs limitation" → bond 的是 PF/端口，卸载粒度为单设备 port representor / eSwitch
- 粗筛结论：有信号且时间晚于专利公开日（产品长期在售），进入 Phase 2 深抓。

## F# 命中表

| F# | 含义 | 判定 | 证据 verbatim | URL | 备注 |
|----|------|------|----------------|-----|------|
| F1（多虚机+多网卡 N≥2 架构） | 跨 N≥2 块**独立网卡** | 部分/不支持 | "you can base guest VMs on VXLAN and VLAN by using either the same set of interfaces attached to a bond, or a different set of NICs"；OVS 卸载以单设备粒度："Each port representor corresponds to a single virtual function of that device" | https://docs.redhat.com/en/documentation/red_hat_openstack_platform/16.1/html/network_functions_virtualization_planning_and_configuration_guide/part-sriov-nfv-configuration ；https://hareshkhandelwal.blog/2020/03/11/lets-understand-the-openvswitch-hardware-offload/ | Broadcom 支持 bond，但 bond 的是 PF/端口，卸载落在报文到达的那块设备的 eSwitch，而非"把同一流表同步到 N 块独立网卡全部" |
| F2（N 个逻辑端口聚合为"第一端口"） | N 个网卡逻辑端口聚合 | 不支持/无证据 | TruFlow 与 OVS 卸载文档均未述及把多块独立网卡逻辑端口聚合为单一"第一端口"映射；TruFlow 为 "hardware offload of a packet flow classifier on the ... adapters"（per-adapter） | https://techdocs.broadcom.com/us/en/storage-and-ethernet-connectivity/ethernet-nic-controllers/bcm957xxx/adapters/introducing-truflow.html | 卸载资源 per-device，无跨卡聚合端口标识映射 |
| F3（每网卡逻辑端口由其物理端口基于 LACP 聚合形成） | LACP 形成逐网卡逻辑端口再聚合 | 不支持/无证据 | Broadcom 公开文档未见"每块网卡内物理端口先 LACP 成逻辑端口、再把 N 块逻辑端口聚合"的两级结构 | https://techdocs.broadcom.com/us/en/storage-and-ethernet-connectivity/ethernet-nic-controllers/bcm957xxx/adapters/introducing-truflow.html | — |
| F4（卸载流表 miss 触发） | cache-miss-driven offload | 命中（通用语义） | "Once all flows pertaining to a particular traffic stream are formed, ovs will use TC flower utility to push and program these flows on NIC hardware" | https://hareshkhandelwal.blog/2020/03/11/lets-understand-the-openvswitch-hardware-offload/ | miss→offload 是 OVS 硬件卸载通用语义，非本专利独有创新点 |
| F5（精确流表跨**全部 N 块独立网卡**同步卸载） | 一次 miss 把同一精确流表同步下发到聚合内所有 N 块网卡 | 反向/不支持 | "offloaded flows reside in individual NIC hardware, not replicated across multiple cards"；"flows are programmed on a particular PCI device's embedded switch"；"the architecture appears to offload flows where packets naturally arrive ... not proactively replicate them across bonded members" | https://hareshkhandelwal.blog/2020/03/11/lets-understand-the-openvswitch-hardware-offload/ | **本专利核心创新点 F5 与 Broadcom 实际架构相反**：流装在报文到达的那一块设备的 eSwitch，不向 bond 内其它卡同步复制 |

## 已检查文档清单
- TruFlow 介绍页（techdocs.broadcom.com，页面标注 2026-04-10）— 仅述 per-adapter 流分类器卸载，无跨卡/LACP 聚合/流表同步
- OVS Flow Offloads 页（techdocs.broadcom.com，标注 2026-04-10）— 仅述 VxLAN/NAT/TC flower 示例，无 bond/LAG/跨卡同步
- OVS 硬件卸载机制博客（hareshkhandelwal.blog，2020-03-11）— 明示流装在单设备 eSwitch、不跨 bond 成员复制
- Red Hat OSP 16.1 NFV 文档 — bond/不同 NIC 集合可用于 OVS HW offload，但 representor 对应单设备 VF

> 受限说明：Broadcom 官方 TechDocs（TruFlow / OVS Flow Offloads）WebFetch 返回未涉及 bond/LACP/跨卡同步细节；跨卡流表放置行为依据 OVS 硬件卸载通用架构（eSwitch per-device）与 bnxt/representor 单设备语义推定，未在官方页找到与 F5 相反或相符的逐字官方原文，故 F5 反向依据来自 OVS 卸载机制公开描述而非 Broadcom 官方逐字声明。

## 最终判定

**第 4 档：公开资料不足（弱候选）**

> 主 agent 复核更正（原 sub-agent 判第 5 档已排除）：本候选的 F5"反向证据"实为推定而非 Broadcom 官方逐字声明——本文件"受限说明"已自承"F5 反向依据来自 OVS 卸载机制公开描述而非 Broadcom 官方逐字声明"。且 Broadcom **正向支持跨独立网卡 bond**（Red Hat 文档 verbatim："either the same set of interfaces attached to a bond, or a different set of NICs"），即它能把 N≥2 块独立网卡 bond 起来；只是"是否把同一精确流表同步到全部成员卡"无公开资料披露。按 SKILL 硬约束"0 命中 ≠ 已排除（须真反向证据/时间不合规/层级不同其一）"，此处既无产品级正向反证、又与专利同抽象层（SmartNIC OVS 卸载），应判**公开资料不足**而非已排除。

依据：
1. F4（cache-miss-driven offload）命中通用语义；F1 概念沾边（Broadcom 支持跨独立网卡 bond）。
2. F2/F3/F5 在 Broadcom 公开资料中无正向证据，**亦无产品级真反向证据**（仅基于 OVS 通用 eSwitch per-device 机制的推定）——属公开资料不足。
3. 时间合规（产品长期在售，跨越 2023-06-06 授权日）。

## 升级路径
- 取 Broadcom TruFlow / bnxt 驱动在 bond-over-separate-NICs 场景下的官方文档或源码，确认 OVS 卸载是否把同一流表同步到 bond 内全部独立网卡成员；
- 或通过 NDA/实测在双 Broadcom 网卡 bond 配置下抓取 TC flower 卸载规则在两卡 eSwitch 的实际分布，验证 F5 是命中（同步全部）还是反向（仅落到达卡）。

## 总结
Broadcom Stingray/Thor TruFlow 为标准 SmartNIC per-device eSwitch 卸载且支持跨独立网卡 bond，但"是否把同一精确流表同步到 bond 内全部网卡"无公开资料、亦无产品级真反向证据，落第 4 档（公开资料不足）。

---
> 免责声明：本文件为证据线索与机制比对，不构成"已构成侵权"的法律结论。
