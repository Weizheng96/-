# 04-tencent-start verdict

## 候选基本信息（含专利公开日 2021-06-08）

- **候选类型**：产品（云游戏服务）
- **候选名称**：腾讯 START 云游戏（Tencent START Cloud Gaming）
- **组织**：腾讯（Tencent Inc.）
- **专利公开（授权）日**：2021-06-08
- **核心证据时间线**：
  - 2021-09：Hairpin 在 Tencent START 生产环境进行 A/B 测试 17k 会话，A/B 之后**持续集成**到 START UDP 连接（原文："Hairpin has been integrated into the UDP-based connections of our cloud gaming service since then"）—— **2021-09 > 2021-06-08，符合时间窗**。
  - 2024-04：Hairpin 论文发表于 NSDI 2024（公开化）。
  - Pudica 同样在 Tencent START 大规模部署，"serving millions of players"。
- **公开度**：高（3 篇 NSDI 顶会论文 + 中文媒体报道 + 团队官方公告）。
- **沟通定位**：START 是腾讯云游戏 PaaS 业务，需要在不可靠 WAN 上低延时下发视频流并回传控制流；Hairpin 是其 packet loss recovery 层（FEC + 重传联合优化），属于本专利"在线游戏 / 低延时控制流"应用场景（场景 2）的直接对应产品。

## F# 命中表（F1–F5）

| 特征 | 专利限定 | Hairpin / START 实现 | 命中等级 |
|------|----------|----------------------|----------|
| **F1**（业务类型识别 — 基于数据流特征变量；至少含"包长度/数目"、"在传包长度/数目"、"到达间隔"、"突发性"之一） | 发送端**自动**从数据流特征变量获取业务类型 | Hairpin 输入包含 **frame size（每帧 packet 数）**与 **loss rate**——frame size 等价于"发送端缓存中待传输数据包的数目"。但 Hairpin **没有从该变量推断"业务类型"标签**，而是直接把 frame size 喂进 MDP；它对所有 START 流默认是 "low-latency interactive video" 单一业务类型。**F1 限定的"业务类型识别"抽象步骤缺失**。 | **部分命中（等同存疑）** |
| **F2**（冗余包数量 = f(网络状态, 传输成功率, 业务类型)） | 三元组联合 | Hairpin 公式 β(α,B,RTT,t) = f(loss rate α, bitrate B, RTT, remaining time t)；并通过 MDP 求 βopt(d,l)。**输入含网络状态（RTT, loss rate）+ 传输成功率（MDP 节点转移概率即成功率推导）**，但**不显式输入"业务类型"轴**。 | **三选二命中**（缺业务类型轴；权 1 严格读法要求 3 项齐全） |
| **F3**（冗余包传输总时间 = f(时延要求）） | deadline → 调度窗口 | Hairpin 公式 L = (T − d/Θ) / RTT，**T 即 application deadline（50–200ms）**；显式以时延要求 T 反推 remaining transmission chance L（= 冗余包传输总时间窗口长度）。 | **字面命中** |
| **F4**（调度方法 = f(网络状态, 总时间, 冗余包数量)） | 三元组联合调度 | Hairpin 用 2-D Markov chain（维度：transmission chance × packets to transmit）联合优化"block size + 每轮 redundancy rate + 何时重传"；输入 = {loss rate（网络状态）+ remaining time（总时间）+ frame size（冗余包数量基础）}。Step 3 还在"立即重传 vs 等下一个 FEC block"之间动态决策，对应权 2 / 权 9 列举的"最短时间 / 均匀时间"调度族。 | **字面命中** |
| **F5**（按调度方法发送冗余包） | proactive FEC + 按调度发包 | Hairpin 采用 Reed-Solomon FEC（<100% 冗余）+ 自定义 codec（≥100% 冗余），由 FEC Encoder 模块在 Packet Sender 之前插入冗余包，按 MDP 输出的 (β, d) 参数主动多发；非纯 ARQ。 | **字面命中** |

## 已检查文档清单

1. `专利集/CN107634908B/候选/04-tencent-start/nsdi24-hairpin.pdf` — Meng et al., "Hairpin: Rethinking Packet Loss Recovery in Edge-based Interactive Video Streaming", NSDI 2024（2.8 MB，21 页，已落盘 `nsdi24-hairpin.txt`）。
2. `专利集/CN107634908B/候选/04-tencent-start/nsdi24-pudica.pdf` — Wang et al., "Pudica: Toward Near-Zero Queuing Delay in Congestion Control for Cloud Gaming", NSDI 2024（已抽取前 2 页 → 确认是 CCA 而非 FEC，定位为部署证据非 F# 证据）。
3. `专利集/CN107634908B/候选/04-tencent-start/nsdi25-tooth.pdf` — An et al., "Tooth: Fine-Grained FEC in Cloud Gaming Streaming", NSDI 2025（确认 Tooth 部署在 "Well-Link Times Inc." 而非 Tencent START，**不属于本候选证据**——但提示 F1 类"按 frame length 区分"策略在云游戏生态已普及）。
4. WebSearch：`腾讯 START 云游戏 弱网 FEC 抗丢包`、`Tencent START Hairpin NSDI 2024`、`Pudica Tencent START`、`AUGUR Tencent NSDI 2024`、`Tencent START "control packets" vs "video packets"`、`"cloud gaming" FEC frame type adaptive Tencent`（全部留痕 `_sources.md`）。
5. WebFetch：`https://ur.tencent.com/article/1481`（腾讯高校合作官方公告页 —— 三篇 NSDI 2024 入选论文官方说明，确认 Hairpin / Pudica / AUGUR 均部署在 START）。

## 关键原文摘录（Hairpin）

- 部署时间："*The A/B test runs for one week in September 2021, covering 17k sessions in total… Hairpin has been integrated into the UDP-based connections of our cloud gaming service since then.*"（§4.7）
- 输入变量："*Step 1: Calculating remaining transmission chance. Given current network RTT, the remaining time towards deadline T, the bottleneck bandwidth Θ, and a certain block size d, the remaining transmission chance L could be calculated as: L = (T − d/Θ) / RTT*"（§3.3）
- 联合优化："*Hairpin … jointly optimize packet retransmission and redundancy for edge-based interactive streaming … MDP, which is known for efficiently optimizing the temporal dependency.*"（§1）
- 业务类型限定："*one frame from the stream … We focus on the interaction lag*" —— 全文未做"业务类型分类"，单一业务流（interactive video streaming）。

## 最终判定

**第 3 档：强候选-资料不足**

### 判定依据（1–3 句）

Hairpin 在 Tencent START 生产环境的部署时间（2021-09）严格落在专利授权日（2021-06-08）之后；F3/F4/F5 字面命中明确（deadline 反推调度窗口、MDP 联合优化网络状态 + 时间 + 冗余包数、Reed-Solomon FEC 主动发包），F2 在网络状态 + 传输成功率两维上命中，但**缺少"业务类型"这一显式输入轴**；F1 用到了权 1 限定 4 项中"待传输包长度和数目"（frame size），但没有用它做"业务类型识别"的中间抽象。因此整体落 3/5 字面命中 + 2/5 部分命中（等同候选）—— 资料层面不足以下"全字面"或"含等同"判定，需要进一步取证补充。

## 升级路径（仅 3-4 档适用）

如下任一证据出现，可升至 **第 2 档（含等同命中）**：

1. **代码 / 配置直接证据**：START 客户端 SDK / 服务端二进制 / 反编译产物中出现"按业务类型（control vs video / 帧类型 / DSCP / RTP payload type）选择不同 FEC β"的代码路径。
2. **公开文档证据**：Tencent 技术博客 / 腾讯云开发者社区 / KaiwuDB 披露 START（或 RTC Engine）对"控制流（玩家输入）"与"视频流（屏幕推流）"采用不同冗余策略 / 不同 FEC 参数表。
3. **续作论文证据**：Hairpin 的后续工作（如 Tooth 改造版 / Pudica + FEC 联合论文）显式引入"frame type / business type → β" 的映射步骤。
4. **专利文献证据**：腾讯 START 团队在 2021-09 之后申请的中国 / PCT 专利中描述"按业务类型自适应冗余"。

如下证据出现，可降至 **第 5 档（已排除）**：

1. **明确反向证据**：Hairpin / START 团队论文或公开文档显式声明 "we do not differentiate flow types"——目前 §3.4 "Hairpin does not rely on the assumption of underlying loss patterns" 只是限定作用域语，不是 F1 反向证据。
2. **时间反向**：（已确认不适用——2021-09 严格晚于 2021-06-08）。

## 总结一句话

腾讯 START 云游戏的 Hairpin 模块 2021-09 起在生产环境联合优化 FEC 冗余 + 重传调度（F2/F3/F4/F5 命中明确，F1 缺"业务类型识别"抽象步骤）—— **落第 3 档：强候选-资料不足**，等待业务类型分流维度证据补强即可升至含等同档。

---

**免责声明**：本判定仅为基于公开技术资料的技术档位归类，不构成对腾讯 START 已构成专利侵权的法律结论。是否构成侵权需经权利要求逐项映射的司法 / 鉴定程序认定。
