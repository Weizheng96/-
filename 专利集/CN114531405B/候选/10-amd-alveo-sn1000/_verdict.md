# 10-amd-alveo-sn1000 verdict

## 候选基本信息
- 名称：Alveo SN1000 SmartNIC（OVS 卸载）
- 组织：AMD（Xilinx）
- 类型：产品
- 初判命中 F#：F1,F2,F4,F5
- 专利公开（授权）日：2023-06-06

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 公开资料不足 | "The Alveo SN1000 comes with two 100 Gb SmartNIC ports in FHHL PCIe form factor with 2X QSFP28" + "Open vSwitch (OVS) functions are handled to manage traffic for virtual machines and containers running on the host"（即单块卡服务多 VM，但无 N≥2 独立网卡的系统级描述） | https://www.xilinx.com/publications/technology-briefs/xilinx-alveo-sn1000-technical-brief.pdf | F1 要求虚拟交换机连 N≥2 块独立网卡；SN1000 公开资料仅描述单块卡（双端口在同一卡），未见跨多卡系统拓扑。整数下界 N≥2 仅描述下界以下形态→公开资料不足，不外推为命中 |
| F2 | 公开资料不足 | "未找到"（未检索到"N 个网卡逻辑端口→一目标端口标识映射、聚合为第一端口"的跨卡聚合描述） | — | 仅单卡 OVS 卸载，无跨卡端口标识映射/聚合证据 |
| F3 | 公开资料不足 | "未找到"（technical brief 全文未出现 LACP/aggregation/bond 任一词；通用 OVS LACP 仅为单卡内动态聚合） | https://www.xilinx.com/publications/technology-briefs/xilinx-alveo-sn1000-technical-brief.pdf | F3 要求"每网卡物理端口经 LACP 形成逻辑端口"的跨多卡聚合；单卡内多端口 bond 不满足跨卡。无明示拒绝→非反向，仅资料不足 |
| F4 | 等同命中（受限） | "the Match Action Engine (MAE) ... where ... Open vSwitch (OVS) functions are handled" + OVS "exact-match-offload" 特性（first-packet miss → 下发 exact flow 的 upcall/慢路径语义） | https://www.xilinx.com/publications/technology-briefs/xilinx-alveo-sn1000-technical-brief.pdf ; https://www.mail-archive.com/ovs-dev@openvswitch.org/msg88766.html | SN1000 单卡 OVS 卸载具备 miss→upcall→exact flow 下发的同抽象层语义；但本特征仅落"单卡内"，未达 F4 要求的"目标网卡（N 卡之一）"多卡语境 |
| F5 | 公开资料不足 | "未找到"（technical brief 全文无 redundancy/single point/failover；无"精确流表向全部 N 个网卡冗余下发"描述） | https://www.xilinx.com/publications/technology-briefs/xilinx-alveo-sn1000-technical-brief.pdf | F5（向全部 N 卡冗余下发消除单点故障）为本专利核心区分点；SN1000 单卡形态下不存在"全部 N 卡"，无正向证据 |

## 已检查文档清单
- AMD/Xilinx Alveo SN1000 产品/技术页 + Technical Overview PDF（pdfplumber 全文解析）：描述单块双端口 composable SmartNIC，OVS 由收发流水线 MAE 卸载；全文无 LACP/聚合/冗余/单点故障字样 — https://www.xilinx.com/publications/technology-briefs/xilinx-alveo-sn1000-technical-brief.pdf
- SN1000 规格（2×QSFP28 双 100Gb，单块 FHHL PCIe 卡，XCU26 FPGA + 16 核 Arm）— https://www.xilinx.com/products/boards-and-kits/alveo/sn1000.html
- OVS exact-match HW offload RFC（社区特性，非 SN1000 专属，说明 upcall/exact-match 语义存在）— https://www.mail-archive.com/ovs-dev@openvswitch.org/msg88766.html

## 最终判定

**第 4 档：公开资料不足（弱候选）**

五档：第1档=确认侵权(高)F1-Fk全字面命中；第2档=确认侵权(中)全命中含≥1等同；第3档=公开资料不足(强候选)≥60%F#命中且剩余无反向；第4档=公开资料不足(弱候选)<60%命中；第5档=已排除（仅当(a)≥1条F#真反向证据，或(b)全部证据<2023-06-06，或(c)架构层级不同）。
**第5档硬门槛**：必须是针对该候选产品的正向事实（正向否定/正向不同机制/自有文档自有专利写明用另一套手段）；行业通用机制反推、"同类一般这样"、"公开资料未提及"一律不算反向，只算公开资料不足。同抽象层但缺某 F# 正向证据又无反向事实→第4档，不得第5档。**0 命中≠已排除**。

判定依据（1-3 句，基于上表 F# 分布）：5 个 F# 中仅 F4 达"等同命中（受限）"（SN1000 单卡 OVS 卸载具 miss→upcall→exact-flow 下发的同抽象层语义），F1/F2/F3/F5 均为公开资料不足——SN1000 公开资料只描述单块双端口卡，缺本专利核心区分点（N≥2 独立网卡 + 跨卡 LACP 聚合 + 流表向全部 N 卡冗余下发以消除单点故障）的任何正向证据。正向命中率 < 60% 且不构成任何 F# 反向证据（vendor 未明示拒绝多卡方案，依"整数下界外推禁令"只判资料不足而非反向），故落第 4 档而非第 3/5 档。

## 升级路径（仅落第3-4档时填）
- 检索 AMD/Xilinx 是否有"双 SN1000 卡 + 跨卡 LACP bond + OVS 流表向两卡冗余下发"的参考架构 / 部署白皮书 / 客户案例（如电信 NFV 高可用部署）。
- 查 AMD/Xilinx 在 2023-06-06 之后申请的"多 SmartNIC 跨卡链路聚合 + 流表冗余"同主题专利做机制比对。
- 抓 SN1000 driver/onload 或 OVS-DOCA 类文档，确认是否支持跨两块物理卡的 LAG + exact flow 同步下发到两卡（而非单卡内双端口 bond）。

## 总结一句话
AMD Alveo SN1000 仅公开单块双端口 SmartNIC 的单卡 OVS 卸载（F4 等同/受限），缺 N≥2 独立网卡跨卡 LACP 聚合与流表向全部网卡冗余下发的核心区分证据，正向命中 <60% 且无反向证据，落第 4 档（公开资料不足-弱候选）。
