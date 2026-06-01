# 39-nvidia-geforce-now verdict

## 候选基本信息（专利公开日 2021-06-08）
- 候选 NN: 39
- 类型: 产品
- 名称: NVIDIA GeForce NOW
- 组织: NVIDIA
- 公开度: 中
- 初判命中 F#: F2, F3, F4, F5
- 时间窗判定基准: 专利 2021-06-08 授权；GeForce NOW 商业化早于专利公开日，但 L4S 等新机制 2024 年才上线，落在专利公开日之后——**时间窗合规**。

## 检索粗筛
- q1 `NVIDIA GeForce NOW adaptive FEC packet loss streaming` → 6 命中，无 NVIDIA 官方 FEC 描述
- q2 `GeForce NOW streaming protocol network resilience redundancy` → 8 命中（核心：arXiv 2012.06774 + NVIDIA L4S 帮助页）
- q3 `site:research.nvidia.com cloud gaming FEC` → 0
- q4 `"GeForce NOW" FEC OR "forward error correction" OR "redundant packets" video stream` → 1 个第三方营销博客（TESmart）孤证宣称用 FEC，无一手来源；其余命中均为 FEC 通用知识或社区帖
- q5 `"GeForce NOW" L4S ECN congestion control bitrate adaptation no FEC` → 5 命中，全部聚焦 L4S 是**congestion control / rate adaptation**，无 FEC 描述

**Phase 1 结论**：未出现 GeForce NOW 与"主动 FEC / 冗余包"绑定的高权重证据；反向出现"L4S 是 ECN 拥塞控制 + 码率自适应"主线。粗筛通过（用于继续 Phase 2 深抓而非直接早剪枝）。

## F# 命中表（F1-F5）

| F# | 专利特征 verbatim 摘要 | GeForce NOW 实测 / 文档描述 | 命中判定 |
| --- | --- | --- | --- |
| **F1** | 发送端根据数据流特征变量（缓存包长/数、在网包长/数、到达间隔、突发性）**自动识别业务类型** | 无任何公开来源描述 GFN 在传输层自动从流量统计识别业务类型。GFN 用**端口分流**区分视频/音频/命令（arXiv §4.3 视频 49005、音频 49003、命令独立 UDP）——这是**应用层静态端口分配**，不是"由发送端从流量特征统计推断业务类型"。这种形态对应权 1 从属权 4 的"应用静态制定业务类型"语义，**不命中权 1 F1**（CLAUDE.md/Step 2 已明示）。 | **未命中** |
| **F2** | 根据"网络状态 + 传输成功率 + **业务类型**"三元组联合计算冗余包数量 | GFN 公开机制是 **L4S/ECN 拥塞控制**——根据 CE 标记比例**调整码率**（"adapts the media rate downwards in proportion to the fraction of marked packets"）。这是**码率压缩**而非"计算 n 个冗余副本"；arXiv 实测**未观察到 FEC / 冗余包**。**冗余包数量整数 ≥ 1 限定不成立**（n=0 退化情形）。 | **未命中（反向证据）** |
| **F3** | 根据时延要求获取冗余包**传输总时间** | 无公开来源描述 GFN 把"时延要求"映射到"冗余包发送窗口长度"。L4S 反馈环路是亚 RTT 级码率调节，不涉及冗余包窗口。 | **未命中** |
| **F4** | 根据网络状态 + 传输总时间 + 冗余包数量获取**调度方法**（随机/最短/最长/均匀） | 文档显示 GFN 服务端"paces the packets over time to prevent congestion caused by an overflowed burst" —— **基础流量整形（pacing）**，应用于业务数据本身而非冗余副本；与权 1 限定的"冗余包调度方法"无对应。 | **未命中** |
| **F5** | 按调度方法**发送冗余数据包** | arXiv 实测 §4.1/4.4 **"we do not observe the presence of the RTCP protocol"**、未观察到 retransmission / FEC stream；GFN 抗丢包靠码率降级（≤5% 丢包不降分辨率）+ L4S 主动避免拥塞，**不发送冗余副本**。这是 reactive rate adaptation，非 proactive packet-level redundancy。 | **未命中（反向证据）** |

**命中汇总**：5 项 F1-F5 中 0 项命中；F2 / F5 出现**反向证据**（用码率自适应 / L4S 替代主动冗余，与权 1 "主动冗余 vs 重传/ARQ"区别段的"反方向技术路线"一致）。

## 已检查文档清单
1. arXiv 2012.06774 "A Network Analysis on Cloud Gaming: Stadia, GeForce Now and PSNow"（Di Domenico et al. 2020）—— §4.1 协议 / §4.3 多媒体端口分流 / §4.4 网络韧性
2. NVIDIA support a_id/5522（L4S 设置说明）—— WebSearch 摘要可读，curl/WebFetch 被 Akamai 拒
3. NVIDIA support a_id/4504（reduce-lag 帮助页）—— 同上拒绝；WebSearch 摘要无 FEC 内容
4. l4steam.github.io GeforceNow L4S Compliance PDF（NVIDIA 自己提交）—— 整篇仅讨论 ECN/L4S，无 FEC/冗余包
5. TESmart 第三方营销博客 —— 孤证宣称"用 FEC"，无引用、无技术细节、与 arXiv 实测冲突；**不予采信**

## 最终判定 **第 5 档：已排除**

理由：
- arXiv 学术实测论文（最权威一手网络分析）明确：GeForce NOW **未观察到 FEC、未观察到 RTCP retransmission**；
- NVIDIA 一手公开的抗丢包 / 网络韧性机制**全部是 reactive**（L4S/ECN 拥塞控制 + 码率自适应 + 端口分流），属于权 1 "主动冗余 vs 重传 / ARQ" 区别段中明示的反方向技术路线；
- F2 / F5 出现**真反向证据**（不是"0 命中 ≠ 已排除"的空集），符合 SKILL Step 6 "已排除"档硬条件；
- F1 的"业务类型识别"在 GFN 中是**静态端口分配**，对应权 1 从属权 4 形态，已被权 2 第 2 节"关键限定词与隐含约束"明确排除出权 1。

## 升级路径
不适用（已落第 5 档）。若未来 NVIDIA 公开 GeForce NOW 加入 packet-level FEC 模块（例如发布技术博客披露 RaptorQ/Reed-Solomon 冗余包模块且按业务类型 / 时延要求自适应调整冗余度），可重新评估并按 R-* 升级流程纳入。当前公开技术栈无此特征。

## 总结一句话
NVIDIA GeForce NOW 抗丢包路线为 L4S/ECN 拥塞控制 + 码率自适应 + 端口分流，arXiv 实测未观察到 FEC / RTCP retransmission，与权 1 "业务类型自适应主动冗余"路线方向相反，**落第 5 档：已排除**。

---
*本报告为技术档位评估，非法律意见。专利侵权认定需经法院程序。*
