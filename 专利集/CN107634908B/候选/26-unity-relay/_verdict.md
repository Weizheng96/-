# 26-unity-relay verdict

## 候选基本信息（专利公开日 2021-06-08）

- 候选 NN: 26
- 类型: 产品（开源 + 托管服务的组合）
- 名称: Unity Relay / Unity Transport（UTP）/ Netcode for GameObjects（NGO）
- 组织: Unity Technologies
- 初判命中 F#（来自 Step 5）: F2, F3, F4, F5
- 公开度: 高（UTP / NGO 在 GitHub 开源；Unity Relay 文档公开）
- 时间窗: 上述三者在 2021-06-08 之后均有持续公开发布与文档维护，**通过时间窗硬条件**

## F# 命中表（F1-F5）

| F# | 专利要件 | UTP / Relay / NGO 实际机制 | 命中？ |
| --- | --- | --- | --- |
| F1 | 发送端根据数据流特征变量（缓存中数据包长度/数目、在网数据包长度/数目、到达间隔、突发性 任一）**自动**获取业务类型 | UTP 的 pipeline 由开发者在代码中**静态选择**（`CreatePipeline(typeof(ReliableSequencedPipelineStage))` 等），不存在"从流量统计推断业务类型"的机制；Relay 仅按 Allocation ID 转发，不区分业务类型 | 否（反向证据） |
| F2 | 根据"网络状态 + 传输成功率 + 业务类型"三元组计算冗余包数量 n（n≥1） | UTP/NGO/Relay 不计算冗余包数量。Reliable 通道是 ARQ（重发已丢包），不是主动冗余；Window 硬编码 32，可调到 64，无"基于业务类型动态算 n"的逻辑 | 否（反向证据） |
| F3 | 根据时延要求计算冗余包传输总时间 | UTP `SetMinimumResendTime()` / 最大 resend timeout 是**单包重传超时**，不是 n 个冗余包的累计调度窗口；语义和专利"传输总时间"不一致 | 否 |
| F4 | 根据"网络状态 + 总时间 + 冗余包数量"三元组动态选调度方法（随机/最短/最长/均匀 至少 1 种） | UTP 不调度冗余包；Relay 是被动代理转发 | 否（无可调度对象） |
| F5 | 按调度方法**主动**发冗余包 | UTP 仅在收不到 ACK 时**被动**重传同一包（ARQ）；不是 proactive 多副本发送 | 否（反向证据，ARQ ≠ FEC） |

**初判 F2/F3/F4/F5 → 复核全部反向**。初判误把 UTP 的"丢包重传"与专利"主动冗余调度"混同；二者机制不同 — UTP 是 reactive ARQ，专利是 proactive packet-level redundancy。

## 已检查文档清单

1. Unity Transport ReliableSequencedPipelineStage API（2.0）
   - https://docs.unity3d.com/Packages/com.unity.transport@2.0/api/Unity.Networking.Transport.ReliableSequencedPipelineStage.html
2. Unity Transport pipelines-usage 手册（2.0）
   - https://docs.unity3d.com/Packages/com.unity.transport@2.0/manual/pipelines-usage.html
3. Unity Transport 6.6 文档首页
   - https://docs.unity3d.com/Packages/com.unity.transport@6.6/index.html
4. Unity Relay introduction
   - https://docs.unity.com/ugs/en-us/manual/relay/manual/introduction
5. Unity Relay message protocol
   - https://docs.unity.com/en-us/relay/relay-message-protocol
6. Medium "Unity Realtime Multiplayer, Part 3: Reliable UDP Protocol"（佐证 ARQ 性质）
   - https://medium.com/my-games-company/unity-realtime-multiplayer-part-3-reliable-udp-protocol-94fbffe8c72c

## 关键反向证据 Verbatim

- UTP API 文档："This is done by sending acknowledgements for received packets, and resending packets that have not been acknowledged in a while." — 这是 ARQ，不是 FEC。
- UTP 手册："Packets are tagged with a sequence number, and peers will acknowledge the reception of these numbers. If a packet is not acknowledged, it will be resent until it is received." — 同样描述 ARQ 重传。
- UTP 手册 pipeline 全集：`FragmentationPipelineStage / ReliableSequencedPipelineStage / SimulatorPipelineStage` — **不存在任何 FEC / 冗余生成 stage**。
- Unity Relay introduction："the Relay service provides connectivity through a universal Relay server acting as a proxy" — Relay 是 datagram 代理，不在转发路径上做 FEC / 业务类型冗余。

## 最终判定 **第 5 档：已排除**

**判定依据**（满足"反向证据"硬条件，非"0 命中即排除"）：

1. **F1 反向证据**：UTP 业务通道是开发者代码静态选择，**不**从流量统计自动推断业务类型。专利 F1 的"数据流特征变量 → 业务类型"自动判定流程在 UTP / NGO / Relay 中均不存在。
2. **F2/F5 反向证据**：UTP Reliable 通道是 **ARQ（重传已丢包）**，专利 F5 要求 **proactive 主动冗余**（n≥1 个冗余副本在原包未确认丢失前就调度发出）。机制根本不同 — 与 CN107634908B 背景技术段"TCP 超时重传 vs 线性网络编码主动冗余"的对照一致，UTP 落在前者一侧。
3. **F4 反向证据**：UTP 不存在"调度方法"概念；冗余包从未生成，自然也没有可调度对象。Window 大小是硬编码上限，不是"基于网络状态 + 总时间 + 冗余包数量"的动态调度。
4. **Relay 层反向证据**：Unity Relay 是 NAT 穿透代理，按 Allocation ID 转发原包，不在转发路径上修改 / 复制 / 重新调度 UDP payload。

判定档位：**第 5 档（已排除）** —— 有充足的反向证据（不仅是 0 命中），可明确排除该候选不实施权 1。

## 升级路径（保留以便后续巡检）

如未来出现下列任一情况，可重启评估：

- Unity 在 UTP 或 NGO 中新增 **FEC pipeline stage** 或 **packet-level redundancy** 模块；
- Unity Relay 引入"应用类型感知"的差异化转发策略并加入主动冗余复制；
- Unity 官方发布第三方 transport（如 multiplayer-community-contributions 中第三方实现）默认捆绑，且该实现满足 F1+F2+F4+F5；
- Unity 发布"adaptive redundancy / per-traffic-class duplication"特性公告。

巡检触发关键词：`Unity Transport FEC`、`UTP forward error correction`、`Netcode adaptive redundancy`、`com.unity.transport FECPipelineStage`。

## 总结一句话

Unity Relay / UTP / Netcode 的可靠传输仅由 ARQ（序列号 + ACK + 被动重传）实现，pipeline 全集无 FEC 阶段、Relay 仅做代理转发、无业务类型自适应冗余调度，与专利"基于业务类型的主动冗余 + 调度方法"机制存在多处反向证据，**落第 5 档（已排除）**。

---

> 免责声明：本判定为基于公开材料的技术档位评估，不构成法律意见。最终侵权认定须由专业律师结合权利要求解释、产品最新源码、商业部署及司法管辖区规则综合判断。
