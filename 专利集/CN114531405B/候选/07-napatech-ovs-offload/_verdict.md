# 07-napatech-ovs-offload verdict

## 候选基本信息
- 名称：全 OVS 卸载 SmartNIC（FPGA）
- 组织：Napatech
- 类型：产品
- 初判命中 F#：F1,F2,F4,F5
- 专利公开（授权）日：2023-06-06

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（虚拟交换机+M VM+N≥2 独立网卡） | 公开资料不足 | "NT200A02 SmartNIC with dual 25Gbps ports"；产品均为单卡（NT200A02 / NT50B01），公开文档仅描述单 SmartNIC 形态，未见"一主机内 N≥2 块独立网卡"拓扑 | https://www.napatech.com/support/resources/solution-descriptions/virtual-switch-offload-solution/ | 单卡多端口≠跨多块独立网卡；整数下界 N≥2 仅描述下界以下形态→判公开资料不足，禁外推为字面命中 |
| F2（N 逻辑端口聚合为第一端口的端口标识映射） | 公开资料不足 | "Link aggregation (active/active and active/standby)" 仅列为特性，未公开"跨网卡 N 逻辑端口→一目标端口标识映射"机制 | https://www.napatech.com/support/resources/data-sheets/link-virtualization-software-for-napatech/ | 链路聚合特性存在但作用域（卡内/跨卡）未公开 |
| F3（每网卡逻辑端口由其物理端口经 LACP 聚合形成） | 公开资料不足 | "Link aggregation (active/active and active/standby)"；公开文档仅及单卡 dual-port，未明示"跨多块物理网卡物理端口经 LACP 聚合" | https://www.napatech.com/support/resources/data-sheets/link-virtualization-software-for-napatech/ | 单卡内端口 bond 不满足"跨网卡 LACP"；未见跨卡正向描述 |
| F4（目标网卡流表 miss 触发） | 等同命中（受限） | "ensuring that only new and unknown flows are resolved in the host CPU"；"The megaflow cache in the SmartNIC hardware is automatically updated when a change is made to the OVS megaflow cache" | https://www.napatech.com/products/link-virtualization-software/ | first-packet miss→host 解析→HW cache 更新，与 miss 触发上送语义同功能；但为 megaflow（非 exact-match）且单卡 cache 同步 |
| F5（经第一端口将精确流表卸载至全部 N 个网卡） | 公开资料不足 | "Non-degrading HW Megaflow cache"；megaflow cache 自动从 host OVS 同步至 SmartNIC，未公开"经聚合第一端口将精确流表冗余下发至全部 N 块网卡" | https://www.napatech.com/support/resources/data-sheets/link-virtualization-software-for-napatech/ | 单卡 cache 同步≠向 N 块网卡冗余下发；F5 跨卡冗余维度无正向证据 |

## 已检查文档清单
- Virtual switch offload solution（架构描述：单 SmartNIC，NT200A02 dual-25G） — https://www.napatech.com/support/resources/solution-descriptions/virtual-switch-offload-solution/
- Light at the end of the tunnel: OVS offload 6x（**发布 2019-02-06，早于授权日，现有技术，仅作架构背景**） — https://www.napatech.com/light-at-the-end-of-the-tunnel-ovs-offload/
- Link-Virtualization Software 产品页（megaflow cache 自动同步机制） — https://www.napatech.com/products/link-virtualization-software/
- Link-Virtualization Software 数据表（Link aggregation active/active+active/standby；HW Megaflow cache；Copyright 2026） — https://www.napatech.com/support/resources/data-sheets/link-virtualization-software-for-napatech/

## 最终判定

**第 4 档：公开资料不足（弱候选）**

五档：第1档=确认侵权(高)F1-Fk全字面命中；第2档=确认侵权(中)全命中含≥1等同；第3档=公开资料不足(强候选)≥60%F#命中且剩余无反向；第4档=公开资料不足(弱候选)<60%命中；第5档=已排除（仅当(a)≥1条F#真反向证据，或(b)全部证据<2023-06-06，或(c)架构层级不同）。
**第5档硬门槛**：必须是针对该候选产品的正向事实（正向否定/正向不同机制/自有文档自有专利写明用另一套手段）；行业通用机制反推、"同类一般这样"、"公开资料未提及"一律不算反向，只算公开资料不足。同抽象层但缺某 F# 正向证据又无反向事实→第4档，不得第5档。**0 命中≠已排除**。

判定依据（1-3 句，基于上表 F# 分布）：5 个 F# 中仅 F4 达等同命中（megaflow miss→host 解析→HW cache 更新，同功能但非 exact-match、单卡），F1/F2/F3/F5 因公开文档只描述"单 SmartNIC 单卡多端口 + megaflow cache 单卡同步"形态、未公开本专利核心区分点（N≥2 块独立网卡 + 跨卡 LACP 聚合 + 精确流表向全部网卡冗余下发以消除单卡 SPOF），均判公开资料不足。字面/等同命中 <60%，且核心跨卡维度无任何正向证据，落弱候选。注意：未见 Napatech "明示拒绝/正向声明仅单卡"，故不构成第5档反向，仅资料不足。

## 升级路径（仅落第3-4档时填）
- 取 Napatech Link-Virtualization 部署/集成手册或 OpenStack Nova-spec（specs.openstack.org 已见同主题 spec），核查是否支持一主机内 N≥2 块独立 SmartNIC 做跨卡 LACP bond 且流表向全部卡下发。
- 检索 Napatech 在 2023-06-06 之后申请的同主题专利（Google Patents，关键词 cross-NIC LACP / redundant flow offload），做机制比对。
- 找 vendor 配置文档确认 "Link aggregation active/standby" 是否可跨两块物理 SmartNIC 形成单逻辑端口 + 流表冗余——若是→升第3档；若文档明示仅卡内端口聚合→转第5档反向。

## 总结一句话
候选 07-napatech-ovs-offload 落第 4 档：公开文档仅及单卡 OVS 全卸载 + megaflow cache 单卡同步（F4 等同命中），未公开 N≥2 独立网卡跨卡 LACP 聚合 + 精确流表向全部网卡冗余下发这一核心区分点，跨卡维度无正向也无反向证据，公开资料不足。
