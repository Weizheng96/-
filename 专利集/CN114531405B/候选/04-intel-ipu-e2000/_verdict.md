# 04-intel-ipu-e2000 verdict

## 候选基本信息
- 名称：IPU E2000（Mount Evans）流表硬件卸载
- 组织：Intel
- 类型：产品
- 初判命中 F#：F1,F2,F4,F5
- 专利公开（授权）日：2023-06-06

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 反向证据（架构层级不同） | "two NIC ports and an out-of-band management port"；"Intel Mount Evans IPU Card"（单卡单 ASIC） | https://www.servethehome.com/intel-e2000-is-the-new-intel-mount-evans-dpu-ipu-brand/ | E2000 是**一块 IPU/DPU 卡（单 ASIC）**，对外仅 2 个 NIC 端口在同一设备上；专利 F1 要求虚拟交换机连 **N≥2 块独立网络接口卡**。这是"单卡多端口"形态，正是背景技术明示要改进的对象（"只能实现单一网络接口卡内不同链路的可靠性…单点故障"），架构层级与 F1 的"多块独立网卡"不同 |
| F2 | 公开资料不足 | 未找到 N 个网卡逻辑端口→一目标端口标识映射、聚合为第一端口的描述 | https://medium.com/intel-tech/intel-ipu-e2000-a-collaborative-achievement-with-google-cloud-eb1dda8c0177 | E2000 为单设备，无"跨 N 块网卡端口标识聚合"语义 |
| F3 | 反向证据 | E2000 两个 NIC 端口位于**同一 ASIC / 同一卡**；专利明示"单卡内多端口 bond 不满足跨网卡" | https://www.servethehome.com/intel-e2000-is-the-new-intel-mount-evans-dpu-ipu-brand/ | F3 要求"跨多块物理网卡的物理端口经 LACP 聚合"；E2000 端口同卡，属卡内端口，非跨网卡聚合 |
| F4 | 字面命中（部分） | E2000 "support numerous existing use-cases such as vSwitch offload"，P4 可编程包处理流水线，承担 OVS 类硬件卸载（含 miss→慢路径/upcall 语义） | https://medium.com/intel-tech/intel-ipu-e2000-a-collaborative-achievement-with-google-cloud-eb1dda8c0177 | vSwitch 流表硬件卸载的 miss 触发为通用机制，E2000 具备；但这是**单设备内**的卸载，非"目标网卡 miss 触发向全部 N 网卡下发" |
| F5 | 反向证据（架构层级不同） | 未找到"流表向全部 N 块网卡下发"；E2000 为单卸载设备 | https://www.servethehome.com/intel-e2000-is-the-new-intel-mount-evans-dpu-ipu-brand/ | F5 的核心是把精确流表下发到**所有 N 块网卡做冗余防单点**；E2000 单卡架构下无此"跨卡全网卡下发"语义 |

## 已检查文档清单
- ServeTheHome 现场报道（2022-10-11）：E2000 单卡含 two NIC ports + OOB 口 — https://www.servethehome.com/intel-e2000-is-the-new-intel-mount-evans-dpu-ipu-brand/
- Intel Tech / Google Cloud 合作博文：E2000 200G 单 IPU，承担 vSwitch offload — https://medium.com/intel-tech/intel-ipu-e2000-a-collaborative-achievement-with-google-cloud-eb1dda8c0177
- IEEE/ISSCC "An In-depth Look at the Intel IPU E2000"（订阅墙，未抓取，已在 _sources.md 注明） — https://ieeexplore.ieee.org/document/10067333/

## 最终判定

**第 5 档：已排除**

五档：第1档=确认侵权(高)F1-Fk全字面命中；第2档=确认侵权(中)全命中含≥1等同；第3档=公开资料不足(强候选)≥60%F#命中且剩余无反向；第4档=公开资料不足(弱候选)<60%命中；第5档=已排除（仅当(a)≥1条F#真反向证据，或(b)全部证据<2023-06-06，或(c)架构层级不同）。
**第5档硬门槛**：必须是针对该候选产品的正向事实（正向否定/正向不同机制/自有文档自有专利写明用另一套手段）；行业通用机制反推、"同类一般这样"、"公开资料未提及"一律不算反向，只算公开资料不足。同抽象层但缺某 F# 正向证据又无反向事实→第4档，不得第5档。**0 命中≠已排除**。

判定依据（1-3 句，基于上表 F# 分布）：E2000 是**单 ASIC 单卡 IPU/DPU**，对外仅在同一设备上呈现两个 NIC 端口（一手现场报道 verbatim），这是"单卡多端口"架构——正是本专利背景技术明示要改进、并以 F1/F3/F5 加以区分的对象（专利要求 N≥2 块**独立网络接口卡** + **跨卡 LACP 聚合** + **流表向全部网卡下发以防单点故障**）。F1/F3/F5 落在不同架构层级，属正向架构事实（非"未提及"），命中第5档硬门槛 (c) 架构层级不同；F4（vSwitch 流表 miss 卸载）虽具备，但仅为单设备内通用机制，不足以挽回核心 inventive 特征的架构性缺失。

## 升级路径（仅落第3-4档时填）
- （不适用 — 已落第5档）

## 总结一句话
候选 04-intel-ipu-e2000 落第5档（已排除）：E2000 为单 ASIC 单卡、两端口在同一设备，与专利"N≥2 块独立网卡 + 跨卡 LACP + 流表向全部网卡下发防单点"的架构层级不同，构成正向反向证据。
