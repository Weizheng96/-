# 证据索引 — 24-epic-eos

## Phase 1 — WebSearch (react 串行, 4 次)

| # | query | 是否产出可深抓的 EOS 特定 URL | 关键发现 |
| --- | --- | --- | --- |
| q1 | `Epic Online Services EOS networking FEC packet loss reliability` | 是 | 命中 `EOS_EPacketReliability` 枚举页 |
| q2 | `Unreal Engine networking adaptive redundancy` | 否（仅 UE 通用 networking overview / "adaptive net update frequency" — 自适应"更新频率"不是冗余包数量） | UE 公开文档不出现 FEC / 冗余 / 重传字眼 |
| q3 | `EOS P2P packet reliability ReliableOrdered ARQ retransmission` | 否（无 Epic 特定结果） | 学术 ARQ 教材，无关 |
| q4 | `"Epic Online Services" P2P NAT punchthrough redundant packet forward error correction proactive` | 是（NAT P2P help / P2P sample） | Epic 官方页面不提 FEC，只提 NAT 打洞 |

Phase 1 结论：4 次检索均未发现 EOS 实现"主动 FEC + 冗余包数量动态计算 + 业务类型自适应"的任何公开证据；q1 直接指向只暴露 3 档可靠性枚举的 API（典型 ARQ 形态）。**继续 Phase 2 抓取反向证据**。

## Phase 2 — WebFetch / curl 兜底（react 串行, 3 次）

> WebFetch 首次返回空内容（Epic Games SPA 文档站对 Anthropic web tool 渲染拦截），按纪律 curl 兜底一次成功。

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | EOS 现行文档（持续维护，发布时间不在页面元数据中，远晚于 2021-06-08 专利公开日） | EOS 官方 API 枚举 | https://dev.epicgames.com/docs/en-US/api-ref/enums/eos-e-packet-reliability ／ 本地：eos-packet-reliability-enum.html | 列出 3 枚举值，措辞为 "may be sent multiple times" — 条件性 ARQ 而非主动 FEC（**反向证据**） |
| 2 | 同上 | EOS 官方 API 结构体 | https://dev.epicgames.com/docs/en-US/api-ref/structs/eos-p-2-p-send-packet-options ／ 本地：eos-sendpacket-options.html | 发送包参数集中**没有**业务类型 / 时延 / 期望成功率 / 冗余数量 / 调度方法 / 网络状态变量字段（**反向证据**） |
| 3 | 同上 | Unreal Engine 官方文档 | https://dev.epicgames.com/documentation/en-us/unreal-engine/networking-overview-for-unreal-engine ／ 本地：ue-networking-overview.html | 全文 0 处 `FEC` / 0 处 `forward error` / 0 处 `redundan` / 0 处 `retransmit`；reliable channel 仅 ACK 表述 |

### 抽取的关键 verbatim 证据

- `EOS_PR_UnreliableUnordered` — "Packets will only be sent once and may be received out of order"
- `EOS_PR_ReliableUnordered` — "Packets may be sent multiple times and may be received out of order"
- `EOS_PR_ReliableOrdered` — "Packets may be sent multiple times and will be received in order"
- 文档 Remarks：`"Types of packet reliability. Ordered packets will only be ordered relative to other ordered packets. Reliable/unreliable and ordered/unordered communication can be sent on the same Socket ID and Channel."`
- `EOS_P2P_SendPacketOptions` 字段全集：`ApiVersion / LocalUserId / RemoteUserId / SocketId / Channel / DataLengthBytes / Data / bAllowDelayedDelivery / Reliability(=枚举) / bDisableAutoAcceptConnection`

## 反向 vs 限定语判别

- "Packets **may** be sent multiple times"（可靠模式）：明确**条件性** ARQ 措辞——"may"对应"在检测到丢失时"才再发，不是 proactive "每包必发 n 份冗余副本"。**反向证据**。
- UE adaptive net update frequency：调节"哪个 Actor 多久同步一次状态"，不是"发多少冗余副本"——**非 F2/F4**。
- `bAllowDelayedDelivery`：仅决定连接未建立时是丢包还是缓冲，与"冗余包传输总时间"（F3）语义无关——**非 F3**。
- 4 次检索 + 3 次抓取均未发现 Epic 公开文档 / 博客 / 工程师 talk 提及"业务类型自适应冗余"。

## 工具受限明示

- `WebFetch` 对 `dev.epicgames.com` 返回空内容（疑似 SPA 渲染拦截），全部改用 `curl -A "Mozilla/..."` 兜底，HTML 完整落盘后离线抽取。
- 未深入 EOS C/C++ SDK 二进制（不公开），结论基于官方 API 文档对外契约——这是开发者**唯一**可调用的接口面，已足以判断"产品对外是否暴露权 1 五特征"。
