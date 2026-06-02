# 11-broadcom-stingray verdict

## 候选基本信息
- 名称：Stingray SmartNIC / Thor 数据面卸载
- 组织：Broadcom
- 类型：产品
- 初判命中 F#：F1,F2,F4,F5
- 专利公开（授权）日：2023-06-06

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（vSwitch + M VM + N 网卡，M,N≥2） | 公开资料不足 | "TruFlow ... fully support generic flow offload"；OVS 卸载基于单设备/VF representor 配置；未见"N≥2 块独立网卡"拓扑 | https://techdocs.broadcom.com/.../ovs-flow-offloads.html | TruFlow/OVS 卸载支持虚拟交换场景，但公开材料只展示单卡形态，N≥2 跨独立网卡未证实 |
| F2（N 逻辑端口聚合为第一端口的端口映射） | 公开资料不足 | bond/LAG 卸载以 "SR-IOV VF LAG"（单卡多端口）描述 | https://doc.dpdk.org/guides/nics/bnxt.html（VF-LAG） | 聚合证据均指向单卡内端口聚合，非"N 块独立网卡逻辑端口→第一端口"映射 |
| F3（每网卡逻辑端口由其物理端口经 LACP 聚合，且跨多卡） | 公开资料不足 | "VF representor port configuration should only be made on the first network port on the card"（VF-LAG = 单卡两端口） | (WebSearch) bnxt VF-LAG | **核心区分点**：公开材料仅为单卡内多端口 LACP/VF-LAG，无跨多块独立网卡 LACP 聚合证据 |
| F4（目标网卡流表 miss 触发） | 字面命中 | "Offload of the flow classifier ... flow-based systems"；OVS 卸载本即 first-packet miss→upcall→下发 datapath flow（megaflow/exact） | https://techdocs.broadcom.com/.../ovs-flow-offloads.html | OVS 硬件卸载通用 miss 语义，单卡层面成立 |
| F5（经第一端口将精确流表卸载至全部 N 个网卡） | 公开资料不足 | techdoc 仅描述单设备/逐端口流表下发；无"流表向全部 N 块网卡冗余下发"论述 | https://techdocs.broadcom.com/.../ovs-flow-offloads.html | 未见跨多卡冗余下发；非反向（文档沉默而非否定） |

## 已检查文档清单
- Broadcom TechDocs «OVS Flow Offloads» — TruFlow/OVS 硬件流表卸载，仅单设备/逐端口配置 — https://techdocs.broadcom.com/us/en/storage-and-ethernet-connectivity/ethernet-nic-controllers/bcm957xxx/adapters/ovs-tc-and-dpdk-offload/ovs-flow-offloads.html
- Broadcom TechDocs «Virtualization Offload»（更新 2026-04-10）— VMQ/tunnel offload，无 LAG/跨卡冗余 — https://techdocs.broadcom.com/us/en/storage-and-ethernet-connectivity/ethernet-nic-controllers/bcm957xxx/adapters/introduction/features/virtualization-offload.html
- DPDK BNXT PMD / VF-LAG 说明 — bond/LAG 卸载为单卡 VF-LAG 形态 — https://doc.dpdk.org/guides/nics/bnxt.html

## 最终判定

**第 4 档：公开资料不足（弱候选）**

判定依据（1-3 句，基于上表 F# 分布）：仅 F4（OVS miss→流表下发的通用语义）可在单卡层面字面命中；F1/F2/F3/F5 均落"公开资料不足"——Broadcom 公开材料只展示 TruFlow/OVS 单卡硬件卸载与 SR-IOV **VF-LAG（单卡内多端口聚合）**，未出现本专利核心区分点"跨多块独立网卡（N≥2）LACP 聚合 + 精确流表向全部 N 块网卡冗余下发以消除单卡单点故障"。命中比例 <60%，且文档对跨卡机制为**沉默**（非明示拒绝），不构成反向证据，故不落第5档。按"整数下界 + 跨实体聚合 + 向全部实体分发三要素同现"规则，仅观察到单实体内子部件聚合（VF-LAG）不得记字面命中，判公开资料不足。

## 升级路径（仅落第3-4档时填）
- 检索 Broadcom 是否有 2023-06-06 之后申请的同主题专利（跨网卡 bond 卸载 / 多卡流表冗余下发）做机制比对（Google Patents 申请人=Broadcom）。
- 查 bnxt_en/bnxt 内核驱动或 TruFlow 内部 SDK 是否支持 "bond across two PFs on separate adapters" 且把 TC/flow rule 镜像下发到两张卡的 e-switch（kernel shared-block 机制是否被 Broadcom 用于跨卡）。
- 寻找 Broadcom 数据中心 SmartNIC 部署白皮书是否提及"双网卡冗余 + 流表卸载防单点故障"实拓扑。

## 总结一句话
Broadcom Stingray/TruFlow 公开材料仅证实单卡 OVS 流表卸载与 VF-LAG（单卡多端口聚合），缺乏本专利核心的"跨多块独立网卡 LACP + 流表向全部网卡冗余下发"证据，且文档沉默非反向，落第 4 档（公开资料不足-弱候选）。
