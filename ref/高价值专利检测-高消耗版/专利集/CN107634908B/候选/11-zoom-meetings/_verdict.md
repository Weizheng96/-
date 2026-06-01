# 11-zoom-meetings verdict

## 候选基本信息（专利公开日 2021-06-08）

- 候选 NN: 11 · 类型: 产品
- 名称: Zoom Meetings
- 组织: Zoom Video Communications, Inc.（US 公司；产品在全球及中国大陆有客户）
- 初判命中 F#: F2, F3, F4, F5
- 公开度: 中（marketing/admin 文档多，传输层算法细节闭源）
- 时间窗：Zoom Meetings 2012 年起上线，远早于 2021-06-08 — 但 **时间窗的判断对象是"实施本专利方法的具体版本/特性"，而非产品发布日**；2021-06-08 之后 Zoom 仍持续迭代媒体引擎，时间上不构成排除。

## F# 命中表（F1–F5）

| F# | 专利限定 | 已公开证据 | 命中性 |
| --- | --- | --- | --- |
| F1 | 由发送端自动从数据流特征变量（队列长度/数目、在网包长度数目、到达间隔、突发性 中**至少 1 项**）推得业务类型 | Zoom 官方 / 第三方均**未**披露其内部如何由流量统计推得 "业务类型"。仅有 DSCP 标记（由 admin 配置，属于权 4 的"应用层指定业务类型"形态，**不命中权 1 的 F1**） | **未见公开证据** |
| F2 | 冗余包数量 = f(网络状态变量, 传输成功率, **业务类型**) — 三元组联合 | Zoom 官方文档明示监控 bandwidth/packet loss/latency/jitter（覆盖网络状态 + 传输成功率两项），但**未公开**业务类型是否参与冗余包数量计算 | **部分命中**（缺业务类型输入证据） |
| F3 | 冗余包传输总时间 = f(时延要求) | Zoom 官方页面强调 real-time / low latency 设计，但**未公开**冗余包总时间是否由显式时延预算导出 | **未见公开证据** |
| F4 | 调度方法 = f(网络状态, 传输总时间, 冗余包数量) — 三元组联合 | Zoom 客户端 sender 调度逻辑闭源，**无公开证据** | **未见公开证据** |
| F5 | 按调度方法发送冗余包（主动 FEC，非 ARQ） | Zoom 官方 KB 明确 "Forward Error Correction (FEC) may also be available to recover lost media data packets without retransmission" — **主动 FEC 命中**，区别于 ARQ | **命中**（仅 FEC 存在性，未涉及调度细节） |

**总体**：F5 有官方公开证据；F2 仅部分要素（网络状态 + 成功率）有证据，关键的"业务类型作为输入"要素无证据；F1/F3/F4 均无公开证据可比对。

## 已检查文档清单

1. Zoom 官方 — Architected for Reliability — https://library.zoom.com/admin-corner/architecture-and-design/zoom-architected-for-reliability
2. Zoom 官方 — Configuring Network Components — https://library.zoom.com/admin-corner/network-management/quality-of-service-and-network-best-practices-explainer/configuring-network-components-for-zoom
3. patents.google.com — US11616986B2（确认 assignee 为 Agora，非 Zoom，**已排除为误指**）
4. patents.google.com — US11706456B2（确认 assignee 为 Agora，非 Zoom，**已排除为误指**）
5. designgurus.io — Zoom Architecture 第三方解析 — https://www.designgurus.io/blog/design-video-conferencing-system
6. patentpc.com — Zoom 专利组合综述（business 层叙事，无 FEC 技术细节）

## 最终判定

**第 4 档：公开资料不足，无法判定**

理由：
- F5（主动 FEC 存在性）有 Zoom 官方文档明确背书；
- F2 的核心鉴别要素"**业务类型作为冗余包数量计算的输入**"在所有可公开访问的 Zoom 文档 / Zoom 专利 / 第三方架构文章中**均未提及**；
- F1（由流量统计自动推业务类型）、F3（时延要求驱动冗余总时间）、F4（三元组联合选调度）均无公开证据可比对，且无反向证据；
- "0 命中 ≠ 已排除"：未公开 ≠ 未使用。Zoom 媒体引擎闭源，仅凭 marketing 文档既不能证伪 F1–F4，也不能等同命中本专利的全部限定。
- 注意：US11616986B2 / US11706456B2 看似相关，但确认为 **Agora Lab** 专利非 Zoom 自有，不应作为 Zoom 实施证据。

## 升级路径（→ 第 3 档：明确命中迹象）

满足以下任一类公开证据可升级：
1. Zoom 公司自有专利（assignee 字段确为 "Zoom Video Communications" 而非 Agora 等供应商）的独立权利要求中出现：① 由流量统计推得"业务类型/流类型"；② "业务类型"作为冗余包数量计算的输入；③ 时延预算驱动冗余总时间；④ 调度方法由三元组联合选定。
2. Zoom 工程团队的会议论文 / 技术博客（如 SIGCOMM/NSDI/SOSP/USENIX ATC/IMC 出现的 Zoom-authored 论文）明示 sender 端按 "audio / video / screen share / control" 业务类型分别使用不同冗余强度 + 调度。
3. Zoom SDK 源码或反向工程报告（GitHub / Zoom-SDK-iOS 等）出现 traffic-class → redundancy-count → schedule 的代码路径。

## 升级路径（→ 第 2/1 档：高度疑似 / 确认侵权）

- 需取得权 1 全部 F1–F5 的完整证据链，且 verbatim 引文对应到 Zoom 公开材料；
- 鉴于 Zoom 是 **US 公司、产品主要在美国销售**，CN107634908B 是 **中国专利**，专利地域问题（在境内销售/部署的 Zoom 服务才落入中国专利地域范围；Zoom 已于 2022 年起退出中国大陆直销，仅经销代理）建议留法律团队定性。本档位仅评估"技术特征对应度"，**不作地域适用判断**。

## 总结一句话

Zoom Meetings 在 Zoom 官方文档中可确证使用主动 FEC（F5 命中），但"业务类型作为冗余包数量输入"等本专利核心鉴别要素无任何公开证据，与之并存的 Zoom-related 误指专利（US11616986/US11706456 实为 Agora）已排除，**落第 4 档：公开资料不足，无法判定**（地域适用问题留法律团队评估）。

---

> 免责声明：本判定仅基于截至 2026-05-26 可公开访问的 Zoom 文档与第三方资料，不构成法律意见；"已构成侵权"的认定须由专业律师及司法机关基于完整证据链作出。
