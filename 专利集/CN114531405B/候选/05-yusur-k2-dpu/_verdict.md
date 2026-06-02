# 05-yusur-k2-dpu verdict

## 候选基本信息
- 名称：K2/KPU 系列 DPU 敏捷网卡（OVS 卸载 + bonding）
- 组织：中科驭数 Yusur
- 类型：产品
- 初判命中 F#：F1,F2,F3,F4,F5
- 专利公开（授权）日：2023-06-06

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（虚拟交换机 + M VM + N≥2 网卡） | 公开资料不足 | "采用 OVN/OVS 作为网络转发面……网络 I/O 均由 DPU 卸载"（确认 vSwitch + DPU 卸载场景，但未确认"连接 N≥2 块网卡"的跨卡形态；vendor 卸载文档为单卡两端口"select one"） | https://www.yusur.tech/dpu/K2-Pro ; https://kubeovn.github.io/docs/v1.13.x/en/advance/offload-yusur/ | vSwitch+VM+DPU 场景成立；N≥2 跨卡未证 |
| F2（N 逻辑端口聚合为第一端口的端口标识映射） | 公开资料不足 | 未找到 | - | 无公开材料描述"N 个网卡逻辑端口→一目标端口标识映射、聚合为第一端口" |
| F3（每网卡逻辑端口由其物理端口经 LACP 聚合形成） | 公开资料不足 | 未找到（vendor 卸载文档：2200E 两物理端口"select one"，单 PF 配 SR-IOV，无 bonding/LACP 描述） | https://kubeovn.github.io/docs/v1.13.x/en/advance/offload-yusur/ | 跨多块物理网卡 LACP 聚合无公开命中；单卡形态为反向信号但非产品级明示拒绝 |
| F4（目标网卡流表 miss 触发） | 公开资料不足 | "K2-Pro……集成网络卸载、流表卸载……硬件卸载引擎"；"基于 DPU 的网络能力……OVS 做网络转发面……云化流表卸载"（OVS 流表卸载存在，含 first-packet miss→下发 exact flow 的常规语义，但未对该候选逐条明示） | https://www.yusur.tech/dpu/K2-Pro | OVS 卸载通常含 miss→upcall 慢路径，惟未见对本候选的逐条明示 |
| F5（经第一端口将精确流表卸载至全部 N 个网卡） | 公开资料不足 | 未找到"向全部 N 块网卡下发"的描述；vendor 卸载文档为单卡单 PF 形态 | https://kubeovn.github.io/docs/v1.13.x/en/advance/offload-yusur/ | 单卡 OVS 流表卸载有命中，但"向全部 N 网卡下发（冗余防单点）"无公开命中 |

## 已检查文档清单
- 中科驭数 K2-Pro 产品页（流表卸载/RDMA 卸载/P4 可编程，云原生 SDN 用 OVN/OVS 转发面，网络 I/O 由 DPU 卸载）— https://www.yusur.tech/dpu/K2-Pro
- Kube-OVN 官方 "Offload with YUSUR" 配置文档（时间戳 2024-08-13 / 2025-07-21；2200E 两物理端口"select one"，单 PF 配 SR-IOV VF；无 bonding/LACP/多卡/流表跨卡下发）— https://kubeovn.github.io/docs/v1.13.x/en/advance/offload-yusur/

## 最终判定

**第 4 档：公开资料不足（弱候选）**

五档：第1档=确认侵权(高)F1-Fk全字面命中；第2档=确认侵权(中)全命中含≥1等同；第3档=公开资料不足(强候选)≥60%F#命中且剩余无反向；第4档=公开资料不足(弱候选)<60%命中；第5档=已排除（仅当(a)≥1条F#真反向证据，或(b)全部证据<2023-06-06，或(c)架构层级不同）。
**第5档硬门槛**：必须是针对该候选产品的正向事实（正向否定/正向不同机制/自有文档自有专利写明用另一套手段）；行业通用机制反推、"同类一般这样"、"公开资料未提及"一律不算反向，只算公开资料不足。同抽象层但缺某 F# 正向证据又无反向事实→第4档，不得第5档。**0 命中≠已排除**。

判定依据（1-3 句，基于上表 F# 分布）：Yusur K2/K2-Pro 确做 OVS/OVN 流表卸载（F4 及单卡 F5 的卸载机制存在），但本专利的核心区分特征——F2/F3 的"跨多块物理网卡经 LACP 聚合为第一端口"与 F5 的"精确流表向全部 N 块网卡下发（冗余防单点）"——均无公开命中（<60% F# 确认）。Vendor 唯一一份卸载架构文档（Kube-OVN）显示单卡两端口"select one"、单 PF SR-IOV，无 bonding/LACP/多卡，构成"单卡形态"反向信号；但该文为 K8s 卸载配置文档而非产品级对跨卡 LACP 的明示拒绝，整数下界 N≥2 跨卡形态不可外推、亦不足以达第5档硬门槛，故定第4档而非第5档。

## 升级路径（仅落第3-4档时填）
- Google Patents 按申请人"中科驭数 / Yusur"+ 分类 H04L45 检索 2023-06-06 之后申请件，找其自有"跨网卡链路聚合 + 流表卸载"主题专利做机制比对——若写明用另一套手段（如单卡内多端口 bond / 主备而非跨卡聚合）可定第5档；若写明跨卡 LACP + 流表全网卡下发可上调至第2/3档。
- 取 Yusur SDN / 高可用方案白皮书或 FlexFlow-2200T / Conflux-2200E 产品手册，核实是否支持"跨两块 DPU 卡的 LACP bond + 流表向双卡同步下发"（F2/F3/F5 直证）。
- 联系或查阅 K2-Pro 网络高可用/双卡冗余技术规格，确认 N≥2 跨卡拓扑是否为公开支持形态。

## 总结一句话
中科驭数 K2/K2-Pro 确做 OVS/OVN 流表卸载，但跨网卡 LACP 聚合（F2/F3）与流表向全部网卡下发（F5）无公开证据、vendor 卸载文档仅见单卡形态，证据不足且不达明示拒绝门槛，落第 4 档（弱候选）。
