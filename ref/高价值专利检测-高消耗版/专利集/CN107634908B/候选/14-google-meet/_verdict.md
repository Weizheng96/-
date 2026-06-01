# 14-google-meet verdict

## 候选基本信息（专利公开日 2021-06-08）
- 候选编号：14
- 类型：产品
- 名称：Google Meet（基于 Google libwebrtc / Chromium WebRTC 引擎的视频会议）
- 组织：Google LLC
- 公开度：中（产品本身高公开度；FEC 实现细节由 RFC 8854 + libwebrtc 开源代码间接公开，Meet 内部专有调优未公开）
- 业务领域：电视/电话会议 RTC，对应专利场景 6（"在线视频/电视电话会议"，verbatim 来自 CN107634908B 实施例）
- 时间窗：Google Meet 早于专利公开日 2021-06-08 即已存在（2017 上线、2020 大规模普及）；但**专利保护的是"方法/设备"本身**，时间窗判定看 Meet 在 2021-06-08 之后是否仍持续运行该方法——Meet 至今仍在持续提供服务并持续演进 WebRTC FEC，**时间窗成立**。
- 初判命中：F2, F3, F4, F5
- 复核命中（见下表）：F2 部分命中、F3 部分命中、F4 部分命中、F5 命中；**F1 大概率不命中**

## F# 命中表（F1–F5）

| 特征 | 是否命中 | 证据 / 反向证据 | 来源 |
|------|---------|----------------|------|
| **F1（业务类型识别 — 基于数据流特征变量自动判定）** | **否（关键缺失）** | WebRTC FEC 的"区分"是按 **媒体类型**（audio Opus FEC / video FlexFEC / 屏幕共享）静态走不同 pipeline，**audio/video 是 SDP 协商决定**而非"发送端根据缓存包长度/到达间隔/数据突发性自动判定业务类型"。RFC 8854 与 libwebrtc 均未实现"发送端用流量统计 → 推断业务类型"的环节。Meet 同理。**严格按权 1 F1 限定（4 项流量统计中至少 1 项 + 自动推断业务类型）不命中** | RFC 8854；bloggeek webrtc-media-resilience |
| **F2（冗余包数量 = f(网络状态, 成功率, 业务类型)）** | **部分命中（缺业务类型输入）** | 命中部分："SHOULD only transmit the amount of FEC needed to protect against the observed packet loss"（RFC 8854）+ getstream "WebRTC's redundancy calculation of FEC is dynamic, and will dynamically adjust redundancy based on the result of the packet loss and the network bandwidth estimate (BWE)"——网络状态（BWE）+ 传输成功率（packet loss from RTCP RR）两项命中。**缺业务类型联合输入**——audio/video 各自走静态 pipeline，没有"按业务类型自适应"的联合公式。按 SKILL 严格语义（F2 要求三元组联合，缺业务类型不命中权 1）→ 不命中 | RFC 8854; getstream; Chrome M40 release notes |
| **F3（冗余包传输总时间 — 来自时延要求）** | **部分命中** | 命中部分：RFC 8854 "WebRTC implementations SHOULD prefer using RTX or Flexible FEC retransmissions instead of FEC when the connection RTT is within the application's latency budget"——延迟预算确实参与决策。但这是 **RTX vs FEC 的二元选择**，不是"基于时延要求计算 n 个冗余包的累计发送窗口长度"。**FlexFEC / ULPFEC 规范都没有"按时延要求算总传输时间"这种描述**（bloggeek flexfec 与 RFC 都未提及调度时间窗）。严格语义下不命中 | RFC 8854 |
| **F4（调度方法 = f(网络状态, 总时间, 冗余包数量)）** | **未检索到证据 / 大概率不命中** | FlexFEC 规范定义的是 **XOR 编码矩阵**（哪些 source packet 与哪些 FEC packet 关联），而非"网络状态自适应的发送时序调度"。FEC 包通常紧跟 source packet 排队送给 pacer（congestion-controlled pacer 决定实际发包节奏）——pacer 受网络状态影响但**不知道 FEC 包数量或总时间作为输入维度**。SKILL 限定 F4 三元组联合（网络状态 + 总时间 + 冗余包数量）联合决定调度方法——WebRTC pipeline 没有这种联合形式 | bloggeek flexfec; getstream; RFC 8854 |
| **F5（按调度方法发送冗余包 — 真发主动 FEC）** | **命中** | Meet 实际确实发送 FEC 包：RFC 8854 是 IETF WebRTC FEC 规范，Chromium WebRTC 实现 ULPFEC + FlexFEC，Meet 基于该 stack；getstream 与多个测试 blog 实测 Meet 在 packet loss 下表现优于竞品（"sustaining a high frame rate even under 20% packet loss"）——证明 Meet 启用了主动 FEC（reactive RTX 无法在 20% loss 下维持）。F5 命中 | RFC 8854; testdevlab; getstream |

**F# 综合：F1 否；F2/F3/F4 部分命中（但 SKILL 严格语义下都缺关键限定项）；F5 命中。**

## 已检查文档清单
- RFC 8854 — WebRTC FEC Requirements（Google 共同主导的 IETF 规范） https://datatracker.ietf.org/doc/html/rfc8854
- rtcbits 2022 — "New look at WebRTC usage in Google Meet"（实测 Meet 的 SDP 协商） http://www.rtcbits.com/2022/06/webrtc-google-meet.html
- BlogGeek media resilience https://bloggeek.me/webrtc-media-resilience/
- BlogGeek FlexFEC https://bloggeek.me/webrtcglossary/flexfec/
- getstream WebRTC media resilience https://getstream.io/resources/projects/webrtc/advanced/media-resilience/
- Frugal Testing — Inside Google Meet https://www.frugaltesting.com/blog/inside-google-meet-how-low-latency-architecture-powers-video-quality

## 最终判定 **第 4 档：技术关联强但权 1 关键限定缺失（疑似不构成）**

**判定理由**：
1. Meet 确实做主动 FEC（F5 命中），并且 FEC 数量是按 packet loss + BWE 动态调整（F2 网络维度命中），延迟预算参与 RTX/FEC 二元决策（F3 部分命中）；
2. 但权 1 的核心创新点在于"**业务类型**作为自变量参与 F2 冗余数量计算 与 F4 调度方法选择"——专利 verbatim 把"业务类型"硬钉入权 1，且 F1 要求"业务类型"由发送端**从流量统计变量自动推断**（包长度/到达间隔/数据突发性等）；
3. WebRTC / Meet 的实际实现是"按媒体类型（audio Opus FEC vs video FlexFEC）静态走不同 pipeline"——**媒体类型 ≠ 专利所述的"业务类型"**：媒体类型是 SDP 协商出来的静态属性，专利的"业务类型"是发送端**实时从数据流量特征推断**出的语义标签（控制消息 / 在线游戏 / 在线视频 / 电话会议）。这是显著不同的两套机制；
4. F4 在 WebRTC 中实际由 congestion-controlled pacer 决定发包节奏，**未见"网络状态 + 总时间 + 冗余包数量"三元联合的调度选择逻辑**；
5. 无直接反向证据排除（getstream 等明确证明 Meet 用 FEC 且动态调整），故不入第 5 档；但 F1 + F4 关键限定缺失，且 F2 三元组的"业务类型"维度缺失，故不能入第 1/2/3 档。

落第 4 档（技术关联强、权 1 关键限定缺失，疑似不构成侵权）。

## 升级路径（可能升至第 3 档的条件）
- **若**能取得 libwebrtc / Google 内部 Meet stack 源码或专利交叉引证，证明 Meet 在 audio/video pipeline 之外还有"按业务子类型（如 control 消息 vs voice 流 vs 屏幕共享）从流量统计自动分流到不同 FEC 配置"的代码路径——可命中 F1，整体升至第 3 档；
- **若**能找到 Meet 把"业务类型" hint（如 DSCP / RTP header extension / application-level signal）作为 FEC 决策输入的公开代码或论文——但注意 SKILL 已注明：仅由应用层 hint / DSCP 指明 ≠ "发送端自动从流量统计推断"（属从属权 4 形态，仍不命中权 1）；
- **若**能取得 Google 内部论文或 Meet 工程 blog 描述"按业务类型联合优化 FEC 时序窗口"，可升至第 3 档；
- **若**能取得 Meet 在中国大陆境内主动提供服务的证据 + 上述实现细节确认——可考虑升至第 2/3 档（但 Meet 在中国大陆未直接提供服务，地域风险本身就较低）。

## 总结一句话
Google Meet 在 WebRTC pipeline 上确实做主动 FEC 且按网络状态动态调整冗余量（F2/F5 部分命中），但其按"媒体类型"静态分流 ≠ 专利权 1 要求的"发送端从流量统计自动推断业务类型"（F1 缺失），且 F4 调度未见三元联合公式，**落第 4 档（技术关联强但权 1 关键限定缺失，疑似不构成侵权）**。

---
*免责声明：本判定为基于公开资料的技术档位评估，不构成法律意见，不下"已构成侵权"结论；权 1 是否真命中需由权利人结合 libwebrtc 源码 / Meet 内部实现做权利要求逐项比对（claim chart）方可定性。*
