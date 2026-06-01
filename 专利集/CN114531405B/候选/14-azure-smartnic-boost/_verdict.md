# 候选合议判定 — 14-azure-smartnic-boost

## 一、候选基本信息
- **NN / slug**：14 / 14-azure-smartnic-boost
- **名称**：Azure Accelerated Networking (AccelNet) / Azure Boost SmartNIC
- **vendor / 组织**：Microsoft Azure
- **类型**：产品
- **初判命中 F#**：F1, F2, F4, F5
- **专利公开（授权）日**：2023-06-06；本候选核心材料（NSDI'18 论文、AccelNet 架构）公开于 2018 起，属已公开成熟架构，机制可持续存在于后续产品，**时间窗不构成排除依据**——排除依据落在"架构不同"。

## 二、F# 命中表

| F# | 限定要点 | 判定 | 证据（verbatim） | URL / 来源 | 备注 |
| --- | --- | --- | --- | --- | --- |
| F1 | 多网卡 N≥2（跨多块独立物理网卡） | **不命中** | "transparently bonded to a synthetic hv_netvsc device … enables redundancy **without requiring multiple physical NICs per VM**" | 来源#3/#4（Microsoft Learn） | AccelNet 为单 SmartNIC/单 VF per VM；其"bonding"是 VF↔合成网卡透明绑定，非 N≥2 物理网卡 |
| F2 | N 个逻辑端口聚合为"第一端口" | **不命中** | 全文无多端口聚合为单一逻辑端口的描述；bonding 仅 VF↔synthetic 一对一 | 来源#3 | 无 N→1 端口聚合机制 |
| F3 | 每网卡逻辑端口基于 LACP 聚合形成 | **不命中** | 官方文档与 NSDI'18 全程未出现 LACP；绑定经 hv_netvsc 合成设备，非 LACP | 来源#3 | LACP 限定无任何证据 |
| F4 | 卸载流表 miss 作为卸载触发 | **命中（等同/概念一致，L1）** | "VFP offloads data forwarding logic to the hardware NIC **after processing the first packet of a flow** … loaded into a Generic Flow Table (GFT) on the FPGA … subsequent packets take a fast path" | 来源#1；nsdi18-firestone-AccelNet.pdf | GFT 首包 miss→软件(VFP)学习→卸载，与 F4 的 cache-miss-driven offload 语义一致；但此为通用机制，单卡内完成 |
| F5 | 精确流表卸载至全部 N 个网卡 | **不命中** | 卸载目标为该 VM 的单一 SmartNIC GFT，无"同步至 N 个网卡"；无跨网卡流表同步描述 | 来源#1/#3；NSDI'18 PDF | 单卡卸载，无跨网卡同步——本专利核心创新点缺失 |

**命中统计**：F1–F5 共 5 项，仅 F4 命中（且为通用 cache-miss-offload 模式），核心创新链 F1/F2/F3/F5 全部不命中且有反向证据。

## 三、已检查文档清单
1. WebSearch：Azure Accelerated Networking SmartNIC FPGA flow offload GFT（确认 GFT 首包卸载机制）
2. WebSearch：Azure Boost SmartNIC multiple NIC bonding LACP flow table sync（无多网卡 LACP 同步信号）
3. WebSearch：Azure ... single NIC per VM bonding redundancy dual NIC（确认单卡架构 + 透明绑定）
4. 本地 PDF：nsdi18-firestone-AccelNet.pdf（NSDI'18，AccelNet/GFT 原始论文，L1）
5. WebFetch：Microsoft Learn — Accelerated Networking Overview（2026-02-05 更新，权威反向证据：SR-IOV VF↔synthetic hv_netvsc 透明绑定，无需多物理网卡）

## 四、最终判定

**第 5 档：已排除**

依据：1) AccelNet 为**单 SmartNIC / 单 SR-IOV VF per VM**架构，其"bonding"是 VF 与合成 hv_netvsc 设备的透明绑定（用于 live migration/VF 动态收发的冗余），官方文档明示"**without requiring multiple physical NICs per VM**"——与本专利 F1（N≥2 独立物理网卡）、F2（N 端口聚合为第一端口）、F5（流表同步至全部 N 卡）正相反，属**架构不同**的真反向证据。2) 全程无 LACP（F3）任何痕迹。3) 仅 F4（miss 触发卸载）因 GFT 首包学习机制概念命中，但这是通用 cache-miss-offload 模式、单卡内完成，不构成对本专利多网卡同步创新点的落入。综合：核心创新链 F1/F2/F3/F5 缺失且有真反向证据 → 落第 5 档。

## 五、总结
AccelNet/GFT 与本专利共享"首包 miss 触发流表卸载"思想(F4)，但其单 SmartNIC、VF↔合成设备透明绑定、无 LACP、无跨多物理网卡流表同步的架构与本专利 N≥2 网卡 LACP 聚合+流表同步至全部网卡的核心机制正相反——落第 5 档（已排除）。

---
> 免责声明：本判定仅为基于公开资料的技术线索与证据梳理，不构成"已构成侵权"的法律结论。
