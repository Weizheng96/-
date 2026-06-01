# 候选 08 合议结论 — 中科驭数 K2/KPU 系列 DPU 敏捷网卡（OVS 卸载）

> 候选 NN: 08 · 类型: 产品 · 名称: K2/KPU 系列 DPU 敏捷网卡（OVS 卸载） · 组织: 中科驭数 Yusur
> 公开度: 中 · 初判命中 F#: F1, F2, F3, F4, F5 · 时间窗: 仅取 2023-06-06（授权日）之后材料

## 候选基本信息
- slug：08-yusur-k2-dpu
- 名称：中科驭数 K2 / K2-Pro / KPU 系列 DPU 敏捷网卡（OVN/OVS 流表卸载）
- vendor：中科驭数（北京）科技有限公司 Yusur
- 定位：纯自研 KPU 架构国产 DPU，做 OVN/OVS 流表卸载，电信/金融/云落地

## 检索粗筛
- Q1 `中科驭数 K2 KPU DPU 敏捷网卡 OVS 流表卸载` → 命中：K2/K2-Pro 做 OVN/OVS 流表卸载（有信号，进 Phase 2）
- Q2 `中科驭数 DPU 链路聚合 多网卡 流表 高可靠 卸载 LACP bond` → 无 LACP/跨网卡同步卸载；Multi-Host=多路 CPU；定位到驭数自有专利线索
- Q3 `中科驭数 DPU 网卡 流表 专利 Multi-Host 多网卡 单点故障 冗余` → 无单点故障/冗余/跨网卡内容
- Q4 `中科驭数 DPU网卡硬件流表卸载 专利` → 定位驭数自有专利 **CN119402422A**（申请 2024-10、公开 2025-02，晚于本专利授权日，时间窗合规）

## F# 命中表

| F# | 特征 | 判定 | 证据（verbatim） | URL/路径 | 备注 |
| --- | --- | --- | --- | --- | --- |
| F1 | 多虚机 + 跨多块独立网卡 N≥2 | **未命中（反向）** | 驭数自有专利权 1：「update the hardware flow table component of **the DPU network card**（单数）... perform path matching... obtain a corresponding target path」——全文围绕单块 DPU 网卡 | yusur-CN119402422A.html | 全篇无 N≥2 多网卡；keyword 扫描 multiple network/two network = False |
| F2 | N 个逻辑端口聚合为"第一端口" | **未命中（反向）** | 自有专利无任何"聚合/aggregate/逻辑端口映射/第一端口"表述；网络融合方案页亦无链路聚合 | yusur-CN119402422A.html；yusur.tech/solution/networkConvergence | keyword first port / aggregat = False |
| F3 | 每网卡逻辑端口基于 LACP 形成 | **未命中（反向）** | 全部检索源（产品页、方案页、自有专利）均无 LACP/链路汇聚控制协议字样 | 同上 | Multi-Host 仅指"连接多路 CPU"，非物理端口 LACP 聚合 |
| F4 | 卸载流表 miss 作为触发 | 部分相关（语义不同） | 「When the flow table rule... is **not found** in the hardware flow table component, the target path is determined to be a **default path**」 | yusur-CN119402422A.html | 有 cache-miss 语义，但 miss 后走"默认（慢）路径"，非"向全部 N 网卡同步卸载精确流表" |
| F5 | 精确流表同步卸载至全部 N 个网卡 | **未命中（反向）** | 自有专利 miss 处理为「target path = default path」（单网卡内快/慢路径切换），无"将精确流表卸载至 N 个网卡" | yusur-CN119402422A.html | 本专利核心创新点（F2+F5），驭数机制完全不涉及 |

## 已检查文档清单
1. WebSearch Q1–Q4（见检索粗筛）
2. WebFetch yusur.tech/solution/networkConvergence — 无 4 项特征
3. Google Patents CN119402422A（curl 本地存档 yusur-CN119402422A.html）— 驭数自有流表卸载专利，机制核实
4. 搜狐 a/858776476（404 dead link，本地存档为 404 页，未采信正文）

## 受限说明
- WebFetch 抓 Google Patents 报 unknown certificate verification error → 改用 curl UA 兜底成功（yusur-CN119402422A.html）。
- 搜狐"驭数 DPU 网卡专利"原文已 404，仅余搜索摘要；该专利实体经 Google Patents CN119402422A 核实，机制与本专利不同。

## 最终判定

**第 5 档：已排除**

依据（1-3 句）：
1. 中科驭数确做 OVN/OVS 硬件流表卸载（F1 中"流表卸载"大类相关），但其**自有流表卸载专利 CN119402422A（申请 2024-10、公开 2025-02，时间窗合规）经核实为单块 DPU 网卡内的 BPF 字节码驱动卸载，miss 时走"默认路径"**——构成对 F1(N≥2)/F2(聚合第一端口)/F3(LACP)/F5(精确流表同步卸载至全部网卡)的**真反向证据**，而非"可配合/future work/out of scope"限定语。
2. 三轮检索 + 方案页 + 自有专利全文，keyword（LACP/aggregat/multiple network/first port/all network/link aggreg/bond）扫描全部 False，无任何公开资料显示其做跨多块独立网卡的 LACP 聚合 + 精确流表向全部网卡同步卸载。
3. 本专利核心创新 F2+F5 在驭数路线上无对应实现，仅"单卡只见单卡"+ 机制不同（BPF 字节码 vs LACP 聚合映射），落"已排除"。

（第 5 档，无升级路径段。）

## 总结一句话
中科驭数 K2/KPU 虽做 OVN/OVS 流表卸载，但自有专利 CN119402422A 实证其为单网卡 BPF 驱动卸载、miss 走默认路径，无 N≥2 多网卡 LACP 聚合与精确流表同步下发全部网卡，构成真反向证据，落第 5 档（已排除）。

---
**免责声明**：本报告基于公开检索线索做技术比对，仅产出排查线索与证据链，不构成"已构成侵权"的法律结论；最终是否落入权利要求保护范围须由专业机构以全部技术细节做侵权比对后认定。
