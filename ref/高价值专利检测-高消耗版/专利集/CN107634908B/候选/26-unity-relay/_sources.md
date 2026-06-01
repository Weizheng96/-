# 证据索引 — 26-unity-relay

## Phase 1 WebSearch（react 串行）

### q1: `Unity Transport UTP FEC redundancy reliability forward error correction`
- 0 FEC-on-UTP 命中。结果均为通用 FEC 概念页或第三方非 UTP 库（UniUDP）。
- 反向信号 URL: https://medium.com/my-games-company/unity-realtime-multiplayer-part-3-reliable-udp-protocol-94fbffe8c72c

### q2: `Unity Netcode GameObjects adaptive packet loss redundancy business type`
- 0 命中（无"业务类型自适应冗余"描述）。
- 结果均为 Netcode 通用介绍 / Lag-and-packet-loss 概念文档（讨论 PacketLoss 度量，不是主动冗余）。
- URL: https://docs-multiplayer.unity3d.com/netcode/current/learn/lagandpacketloss/

### q3: `site:github.com Unity-Technologies com.unity.transport FEC redundancy`
- 0 FEC 命中。返回 UTP 仓库 README / 文档 / Issue，无任何 FEC 模块。
- 仅 UnityRenderStreaming（基于 WebRTC 的渲染流送，独立产品）的 Issue 提到 FEC 配置 — 与 com.unity.transport 无关。

### q4: `Unity Transport ReliableSequencedPipelineStage ARQ retransmission mechanism`
- 强反向证据命中：UTP Reliable 通道是**纯 ARQ**（sequence + ACK + 重传），非 FEC。

### q5: `Unity Relay service mechanism architecture data plane forwarding`
- 明确：Unity Relay 是**代理转发器**（datagram proxy / NAT 穿透），无 FEC / 业务类型冗余描述。

## Phase 2 WebFetch（react 串行）

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| F2-1 | 2026-05-26 | UTP 官方 API 文档 | https://docs.unity3d.com/Packages/com.unity.transport@2.0/api/Unity.Networking.Transport.ReliableSequencedPipelineStage.html | Verbatim："This is done by sending acknowledgements for received packets, and resending packets that have not been acknowledged in a while." + "if a packet is lost, subsequent packets will not be delivered until the lost packet has been resent and delivered." → 纯 ARQ，无 FEC |
| F2-2 | 2026-05-26 | UTP 官方手册 | https://docs.unity3d.com/Packages/com.unity.transport@2.0/manual/pipelines-usage.html | Verbatim："Packets are tagged with a sequence number, and peers will acknowledge the reception of these numbers. If a packet is not acknowledged, it will be resent until it is received." pipeline 全集：Fragmentation / ReliableSequenced / Simulator — **无 FEC 阶段** |
| F2-3 | 2026-05-26 | docs-multiplayer 兜底 | https://docs-multiplayer.unity3d.com/transport/current/pipelines/ | 301 → F2-2，无新信息 |
| F2-4 | 2026-05-26 | UTP 6.6 index | https://docs.unity3d.com/Packages/com.unity.transport@6.6/index.html | 工具受限：WebFetch 仅返回首页框架。未发现新 pipeline 阶段（最新版仍是 Fragmentation/Reliable/Simulator） |
| F2-5 | 2026-05-26 | Unity Relay 官方 introduction | https://docs.unity.com/ugs/en-us/manual/relay/manual/introduction | Verbatim："the Relay service provides connectivity through a universal Relay server acting as a proxy." → 代理/转发器，**不在转发路径上对 payload 做 FEC / 业务类型冗余调度** |
| F2-6 | 2026-05-26 | Unity Relay 消息协议 | https://docs.unity.com/en-us/relay/relay-message-protocol | 协议仅定义 PING/CONNECT/RELAY/DISCONNECT 类消息，无冗余生成 / 业务类型分支 |

## 工具受限明示
- `curl https://raw.githubusercontent.com/needle-mirror/com.unity.transport/master/README.md` → 404；未阻断判定（F2-1/F2-2 已覆盖 pipeline 全集）。
- `WebFetch https://github.com/Unity-Technologies/com.unity.transport` → 404（仓库实际镜像在 needle-mirror，非 Unity-Technologies）；不影响结论。

## 反向证据 vs 限定作用域语 — 区分校验
- 上述全部为**反向证据**（pipeline 全集明确列出且不含 FEC；Reliable 通道明示 ARQ 实现机制） — 不是"future work / 不在范围内"这类限定作用域语。
- ARQ ≠ FEC：UTP 的 Reliable 是**被动重传**（仅在 ACK 缺失后才发第 2 份），不满足专利的"主动冗余 / proactive 多副本"（n≥1 个冗余包在原包发送前/同时调度发出）。
