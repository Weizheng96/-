# _verdict.md — 03-intel-e810-ovs-offload

## 候选基本信息
- 类型：产品
- 名称：Intel Ethernet 800 系列（E810）OVS 卸载 + bonding
- vendor：Intel
- 命中 F#（初判）：F1, F2, F3, F4, F5
- 公开度：中
- 一句话定位：E810 网卡在 eSwitch switchdev 模式下支持 OVS/TC-Flower 流表硬件卸载，并支持 SR-IOV VF-LAG（bond），但 bond 范围为**同一张卡的两个 PF**。
- 时间窗：专利公开（授权）日 2023-06-06；E810 OVS 卸载 + VF-LAG 早于该日已公开（Rev1.0 TechConfigGuide 2021-08-30）→ 时间**不构成排除理由**，按机制判定。

## 检索粗筛
- Q1 `Intel E810 OVS TC hardware offload bonding LAG flow table` → 命中：E810 switchdev 支持 OVS TC-Flower 硬件卸载 + SR-IOV VF-LAG。
- Q2 `Intel E810 ice driver bond LAG offload two ports same NIC vs across multiple NICs` → 多为 bond 引起 driver hang 的 bug 报告；无"跨多卡同步卸载"正向证据。
- Q3 `E810 switchdev SR-IOV VF LAG bond two PFs hardware offload flows duplicated failover` → 关键：VF-LAG 需先把 NIC 的两个 PF 都置 switchdev，再 bond uplink 表征口；支持 active-backup/LACP/XOR——**单卡两 PF** 语义。
- Q4 `Intel E810 OVS hw offload bond across two separate physical NICs not supported` → 反向：bonded ice 接口 tc/ethtool 卸载"not supported"；"eSwitch per {PF: LAN port} pair"——offload per-PCI-device，无法跨多张独立物理卡。
- 粗筛结论：有信号，进入 Phase 2 深抓。

## F# 比对

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（多虚机 + 多网卡架构，N≥2 **独立网卡**） | **不命中** | "the two network interfaces from the NIC PFs are bounded in the hypervisor"（示例 PCI `61:00.0` + `61:00.1`）；"there is an eSwitch per {PF: LAN port} pair" | NVIDIA VF-LAG QSG；E810 社区/驱动层（Q4） | VF-LAG bond 的是**同一张卡的两个 PF**（单一 PCI device 的两个端口），非 N≥2 块**独立网络接口卡**。专利 F1 硬限定"N 个网络接口卡（N≥2）"指多块独立物理卡 |
| F2（N 个逻辑端口聚合为"第一端口"） | 部分命中（仅单卡两 PF 聚合） | "bond the up-link representors"；"the two network interfaces from the NIC PFs are bounded" | NVIDIA VF-LAG QSG | 确有把两表征口聚合为一个 bond/逻辑端口，但聚合对象是单卡两 PF，不满足"N 个独立网卡逻辑端口聚合" |
| F3（每个逻辑端口由其物理端口基于 LACP 聚合形成） | 部分命中 | "When in XOR or LACP mode, if both PFs are up, traffic from any VF is split between these two PFs" | E810 switchdev VF-LAG（Q3） | 支持 LACP/XOR/active-backup bond 模式，符合 LACP 语义；但仍是单卡两 PF |
| F4（卸载流表 miss 触发） | 命中（通用卸载语义） | "If the flag shows as offloaded:yes, dp:tc, it means flows are on hardware"；TC-Flower exact match 规则按 cache-miss 下发 | Intel E810 switchdev 配置指南（Q1） | E810 OVS 卸载属 cache-miss-driven offload，F4 触发语义命中 |
| F5（精确流表跨**全部 N 个独立网卡**同步卸载） | **不命中 / 近反向** | (a) "Issuing ethtool or tc commands to a bonded ice interface will result in error messages from the ice driver to indicate the operation is not supported"；(b) "eSwitch per {PF: LAN port} pair … hardware offload is per-PCI-device" | E810 社区/驱动层（Q4） | E810 硬件卸载**按 PCI device/eSwitch 隔离**，不存在"把同一精确流表同步下发到 N 块独立物理卡全部网卡"的机制；正是专利背景所称需被克服的"只能实现单一网络接口卡内不同链路的可靠性" |

## 已检查文档清单
1. WebSearch Q1：`Intel E810 OVS TC hardware offload bonding LAG flow table`
2. WebSearch Q2：`Intel E810 ice driver bond LAG offload two ports same NIC vs across multiple NICs`
3. WebSearch Q3：`E810 switchdev SR-IOV VF LAG bond two PFs hardware offload flows duplicated failover`
4. WebSearch Q4：`Intel E810 OVS hardware offload bond across two separate physical NICs not supported limitation`
5. PDF：Intel E810 eSwitch switchdev TechConfigGuide Rev1.0（2021-08-30，本地 `_e810_extract.txt`；未含 VF-LAG 章节）
6. WebFetch：NVIDIA SR-IOV VF-LAG QSG（同属 VF-LAG 机制族，提供"两 PF bond"verbatim）

## 最终判定 **第 5 档：已排除（架构不同 — 单卡两 PF LAG，非跨多块独立网卡同步卸载）**

判定依据：
1. 专利核心创新（F1+F5）要求在 **N≥2 块相互独立的物理网络接口卡** 之间，把同一"精确流表"**同步卸载到全部 N 块网卡**，以消除单网卡单点故障——这正是专利背景明确区分的"现有技术只能实现单一网络接口卡内不同链路的可靠性"之上的改进。
2. E810 OVS 卸载 + bonding 的真实机制是 **SR-IOV VF-LAG**：bond 的是**同一张卡的两个 PF**（同一 PCI device 的两个 LAN 端口，如 `61:00.0`/`61:00.1`），落在专利所称"单一网络接口卡内不同链路"层面；且 E810 硬件卸载**按 per-PCI-device/per-eSwitch 隔离**，对 bonded ice 接口下发 tc/ethtool 卸载被驱动明确报"not supported"——构成对 F5"跨全部独立网卡同步卸载"的近反向证据。
3. F4（miss 触发卸载）与 LACP 模式（F3 语义）虽命中，但 F1、F5 两个核心硬限定不成立且有架构性反向证据，整体不落入权 1 保护范围。

## 总结一句话
E810 OVS 卸载 + bonding 实为单卡两 PF 的 SR-IOV VF-LAG、且硬件卸载 per-PCI-device 隔离，恰是专利要克服的"单网卡内可靠性"现有技术，未实现跨 N 块独立网卡同步卸载——**落第 5 档（已排除，架构不同）**。

---
*免责声明：本报告仅为侵权线索与证据链梳理，不构成"已构成侵权"的法律结论。*
