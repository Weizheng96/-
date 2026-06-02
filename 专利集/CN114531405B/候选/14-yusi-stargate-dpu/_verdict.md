# 14-yusi-stargate-dpu verdict

## 候选基本信息
- 名称：Stargate 系列 DPU（千万级流表、OVS 加速）
- 组织：益思芯 Yusi（Resnics）
- 类型：产品
- 初判命中 F#：F1,F2,F4,F5
- 专利公开（授权）日：2023-06-06

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（虚拟交换机 + M VM + N≥2 网卡） | 公开资料不足 | 网络接口："2 x QSFP28 100G以太网接口"；主机接口："PCIE Gen3 x 16"——官方规格仅描述**单卡双端口**，未公开 N≥2 块独立网卡 | http://www.resnics.com/product/netcard | 仅满足"单卡内多端口"，不满足 F1 要求的"≥2 块独立网卡"。属下界以下形态，按整数限定外推禁令→不记字面命中；无明示拒绝→非反向 |
| F2（N 逻辑端口聚合为第一端口的端口标识映射） | 公开资料不足 | 未找到 | http://www.resnics.com/product/netcard | 单卡形态下无"跨 N 块网卡的逻辑端口→单一目标端口标识"公开描述 |
| F3（每网卡逻辑端口由其物理端口经 LACP 聚合形成） | 公开资料不足 | 未找到（仅检索到通用 LACP/bond 资料，非 Yusi 自有文档） | http://www.resnics.com/product/netcard | 单卡 2 端口虽可做 LACP，但不满足"跨多块物理网卡"聚合；无 Yusi 自有文档佐证 |
| F4（目标网卡流表 miss 触发） | 公开资料不足 | "基于P4可编程的vSwitch加速引擎"（产品做 OVS/vSwitch 加速，miss/upcall 为 OVS 通用机制，但无 Yusi 自有 verbatim 绑定） | http://www.resnics.com/product/netcard | OVS first-packet miss→upcall 为生态通用语义；无法具体绑定到 Stargate 自有实现，记公开资料不足 |
| F5（经第一端口将精确流表卸载至全部 N 个网卡） | 公开资料不足 | 未找到 | http://www.resnics.com/product/netcard | 官方资料未公开"流表向全部 N 块网卡冗余下发以消除单网卡单点故障"的拓扑 |

## 已检查文档清单
- Resnics 智能网卡产品规格页（Stargate-F1000-SN：单卡 2×100G QSFP28、PCIe Gen3 x16、P4 可编程 vSwitch 加速、多 PF/VF/队列、热迁移） — http://www.resnics.com/product/netcard
- 益思芯交付国内首款商用云原生智能网卡新闻（确认 P4 vSwitch/OVS 加速、流表卸载定位，单卡形态） — http://www.resnics.com/news/yi-si-xin-ke-ji-jiao-fu-guo-nei-di-yi-kuan-zi-zhu-yan-fa-de-shang-yong-yun-yuan-sheng-zhi-nen-wang-ka
- （检索留痕见 _sources.md：4 条 Phase 1 query + curl 兜底抓取 netcard.html）

## 最终判定

**第 4 档：公开资料不足（弱候选）**

五档：第1档=确认侵权(高)F1-Fk全字面命中；第2档=确认侵权(中)全命中含≥1等同；第3档=公开资料不足(强候选)≥60%F#命中且剩余无反向；第4档=公开资料不足(弱候选)<60%命中；第5档=已排除（仅当(a)≥1条F#真反向证据，或(b)全部证据<2023-06-06，或(c)架构层级不同）。
**第5档硬门槛**：必须是针对该候选产品的正向事实（正向否定/正向不同机制/自有文档自有专利写明用另一套手段）；行业通用机制反推、"同类一般这样"、"公开资料未提及"一律不算反向，只算公开资料不足。同抽象层但缺某 F# 正向证据又无反向事实→第4档，不得第5档。**0 命中≠已排除**。

判定依据（1-3 句，基于上表 F# 分布）：候选确属同一抽象层（数据中心服务器虚拟化网络 + 智能网卡/DPU 上的 OVS/vSwitch 流表卸载），与 F# 概念层级一致；但官方公开资料仅披露**单卡双端口（2×100G）**形态，对本专利的核心区分点——F1 的 N≥2 块**独立网卡**、F3 的**跨卡** LACP 聚合、F5 的**流表向全部网卡冗余下发以消除单网卡单点故障**——均无任何正向公开证据，5 项 F# 全部为"公开资料不足"（命中率 0%，<60%）。同时益思芯从未明示拒绝多网卡方案，不构成反向证据，故不入第 5 档。

## 升级路径（仅落第3-4档时填）
- 取 Stargate 在真实部署中是否支持"一服务器插多块 Stargate 卡并跨卡 LACP 聚合 + 流表冗余下发"的工程文档 / SDK 手册 / 用户案例（官网 datasheet 不足，需技术白皮书或部署指南）。
- 检索益思芯/Resnics 在 2023-06-06 之后申请的同主题（跨网卡流表冗余 / 多 DPU 高可用）公开专利做机制比对（本轮 Google Patents 未检索到）。
- 抓取《中国移动 DPU 技术白皮书》中益思芯撰写章节，核实其是否描述跨卡流表卸载冗余架构。

## 总结一句话
候选 14-yusi-stargate-dpu 落第 4 档（公开资料不足-弱候选）：产品确做智能网卡 OVS/vSwitch 流表卸载且层级吻合，但官方资料仅披露单卡双端口形态，对 N≥2 独立网卡跨卡 LACP 聚合 + 流表全网卡冗余下发的核心区分点无任何正向证据，又无反向事实。
