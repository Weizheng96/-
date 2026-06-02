# 17-alibaba-cipu-moc verdict

## 候选基本信息
- 名称：神龙 MoC 卡 / CIPU 云网络卸载
- 组织：阿里云
- 类型：产品
- 初判命中 F#：F1,F2,F4,F5
- 专利公开（授权）日：2023-06-06

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 公开资料不足 | "Triton ... is implemented on our internally developed SmartNIC"；"If the physical server supports multiple SmartNICs, the bandwidth can be further increased." | https://yangye-huaizhou.github.io/files/Triton.pdf | vSwitch(AVS) 连多 VM（M≥2 成立），但卸载目标描述为**单块 SmartNIC**；多 SmartNIC 仅作"带宽横向扩展"可选项，非 N≥2 独立网卡的架构前提。整数下界 N≥2 的"跨多块独立网卡"形态未见正向描述 → 公开资料不足，不外推为字面命中。 |
| F2 | 公开资料不足（未找到） | "未找到"（全文 grep `logical port / target port / 端口标识` 0 命中） | https://yangye-huaizhou.github.io/files/Triton.pdf | 无"建立 N 个逻辑端口标识→一目标端口标识映射、聚合为第一端口"的任何描述。 |
| F3 | 公开资料不足（未找到，含弱反向信号） | "Through the horizontal expansion of multiple SmartNICs, Triton is sufficient to support ~Tbps level bandwidth"（全文无 LACP/link aggregation/bond） | https://yangye-huaizhou.github.io/files/Triton.pdf | 全文 0 处 LACP / 链路聚合；多 SmartNIC 定位为带宽横向扩展而非"每网卡物理端口经 LACP 聚合成逻辑端口再跨卡聚合"。非明示拒绝，故记公开资料不足（带弱反向信号）。 |
| F4 | 等同命中 | "FPGA Miss, upcall Action"；"If the packet fails to find the flow entry on the Fast Path, it will undergo [Slow Path]"；图示 "Slow Path / Miss Update / Fast Path" | https://yangye-huaizhou.github.io/files/Triton.pdf | first-packet 在硬件 Fast Path 查不到流表项（miss）→ upcall 至 SlowPath → Miss Update 下发流表。与 F4"目标网卡查不到对应卸载流表时触发"同手段/同功能（标准 OVS 式 fast/slow path 慢路径 upcall）。 |
| F5 | 公开资料不足（未找到） | "未找到"（仅描述 miss 后向硬件 Fast Path 下发流表，无"向全部 N 个网卡冗余下发"） | https://yangye-huaizhou.github.io/files/Triton.pdf | 流表下发到（单块）SmartNIC 硬件快路径；无"经第一端口将精确流表卸载至全部 N 个网卡以消除单网卡单点故障"的描述。专利所解决的跨网卡单点故障问题未被 Triton 公开材料涉及。 |

## 已检查文档清单
- Triton: A Flexible Hardware Offloading Architecture for Accelerating Apsara vSwitch in Alibaba Cloud（SIGCOMM 2024，阿里云一手论文）—— 架构为单块自研 SmartNIC（SoC+FPGA）上的 AVS 硬件卸载；fast/slow path + miss upcall 下发流表；多 SmartNIC 仅作带宽横扩；全文无 LACP / 跨卡端口聚合 / 流表向全部网卡冗余下发 — https://yangye-huaizhou.github.io/files/Triton.pdf
- 阿里云 X-Dragon/CIPU/神龙 MoC 卡架构科普（The Register / Alibaba Cloud Community / 阿里云开发者社区）—— vSwitch 卸载到 MoC 卡（单数），FPGA 加速 — https://www.theregister.com/2022/06/14/alibaba_dpu_cloud/

## 最终判定

**第 4 档：公开资料不足（弱候选）**

五档：第1档=确认侵权(高)F1-Fk全字面命中；第2档=确认侵权(中)全命中含≥1等同；第3档=公开资料不足(强候选)≥60%F#命中且剩余无反向；第4档=公开资料不足(弱候选)<60%命中；第5档=已排除（仅当(a)≥1条F#真反向证据，或(b)全部证据<2023-06-06，或(c)架构层级不同）。
**第5档硬门槛**：必须是针对该候选产品的正向事实（正向否定/正向不同机制/自有文档自有专利写明用另一套手段）；行业通用机制反推、"同类一般这样"、"公开资料未提及"一律不算反向，只算公开资料不足。同抽象层但缺某 F# 正向证据又无反向事实→第4档，不得第5档。**0 命中≠已排除**。

判定依据（1-3 句，基于上表 F# 分布）：5 项 F# 中仅 F4 等同命中、F1 部分（M≥2 成立但 N≥2 跨卡形态未证实），F2/F3/F5 在阿里一手论文中均未找到，命中率 < 60%；但论文并未明示拒绝多网卡 LACP 冗余（多 SmartNIC 甚至被提及，只是用于带宽扩展），不构成 F# 真反向证据，故不入第5档。专利的核心区分点（跨多块独立网卡 LACP 聚合 + 流表向全部网卡冗余下发以消除单卡单点故障）在阿里公开材料中无正向证据，落弱候选。

## 升级路径（仅落第3-4档时填）
- 取证阿里云 ECS 裸金属/CIPU 的**多 MoC 卡部署拓扑**官方文档，确认单服务器是否标配 ≥2 块独立 MoC 卡并对其做跨卡链路聚合（而非单卡内多端口）。
- 检索阿里巴巴（申请人）2023-06-06 之后申请的同主题专利（关键词：流表 / 网卡 / 链路聚合 / 冗余 / 卸载），做机制比对，常一步定档。
- 抓 Apsara/Achelous 网络虚拟化平台、神龙 4.0/CIPU 2.0 后续技术披露，核对是否引入"流表向全部网卡冗余下发"的高可用机制。

## 总结一句话
候选 17-alibaba-cipu-moc 落第 4 档：阿里一手论文(Triton)证实 vSwitch 卸载 + miss upcall 下发流表(F4 等同)，但跨卡 LACP 聚合(F3)、N 逻辑端口聚合(F2)、流表向全部网卡冗余下发(F5)均无公开证据且 N≥2 跨卡形态未证实，命中<60% 又无真反向，属公开资料不足(弱候选)。
