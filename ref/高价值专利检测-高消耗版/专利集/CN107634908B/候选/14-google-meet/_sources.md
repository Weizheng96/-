# 证据索引 — 14-google-meet

## Phase 1 — WebSearch

| q# | query | 主要返回 |
| --- | --- | --- |
| q1 | `Google Meet WebRTC FEC ULPFEC FlexFEC adaptive redundancy` | RFC 8854, bloggeek ULPFEC/FlexFEC, getstream media-resilience, pion FEC, chromium bug 5654 |
| q2 | `Google Meet network resilience streaming packet loss redundancy` | rtcbits 2022 Google Meet WebRTC usage, Google Workspace prepare-network, testdevlab "Why Google Meet Works", ithy packet loss thresholds |
| q3 | `WebRTC FEC business type media type audio video different redundancy policy` | bloggeek webrtc-media-resilience, RFC 8854 PDF, bloggeek RED, Mozilla audio FEC experiments |
| q4 | `Google Meet WebRTC FEC scheduling adaptive bitrate Chromium implementation` | TWCC flussonic, Chrome M40 release notes (FEC NetEq), bloggeek google-roadmap-webrtc, Frugal Testing inside-google-meet |

## Phase 2 — WebFetch

| # | URL | 时间 | 类型 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | https://datatracker.ietf.org/doc/html/rfc8854 | 2021-02 | IETF RFC | "SHOULD only transmit the amount of FEC needed to protect against the observed packet loss"；"SHOULD prefer using RTX or Flexible FEC retransmissions instead of FEC when the connection RTT is within the application's latency budget"；audio → RED/Opus FEC，video → FlexFEC；不规定调度算法 |
| 2 | http://www.rtcbits.com/2022/06/webrtc-google-meet.html | 2022-06 | tech blog (实测) | "the usage of redundancy encoding (red) is also negotiated for the audio channels … But even if it is negotiated it is not really active for sending because it is included in the codecs list after opus" |
| 3 | https://bloggeek.me/webrtc-media-resilience/ | 2024 | 综述 | 通用 FEC/RED/RTX 介绍，无 Meet 细节，无动态调度公式 |
| 4 | https://getstream.io/resources/projects/webrtc/advanced/media-resilience/ | 2024 | 综述 | "WebRTC's redundancy calculation of FEC is dynamic, and will dynamically adjust redundancy based on … packet loss and the network bandwidth estimate (BWE)"；"RTX works best on connections with relatively low round-trip times. For higher latency connections, FEC may be more effective" |
| 5 | https://www.frugaltesting.com/blog/inside-google-meet-how-low-latency-architecture-powers-video-quality | 2024 | 综述 | 仅提 ABR 自适应码率，无 FEC 细节 |
| 6 | https://bloggeek.me/webrtcglossary/flexfec/ | n.d. | glossary | FlexFEC 为 XOR-based，主要用于 H.264；未提自适应/调度 |

## 关键观察（对 F# 判定的支撑）

- **F1 反向证据**：所有源都把 WebRTC FEC 的"分流"描述为按**媒体类型（audio vs video）**而非"业务类型（控制/游戏/视频/电话）"，且没有任何"发送端从流量统计推断业务类型"的描述。
- **F2 部分证据**：getstream 明确说"基于 packet loss + BWE 动态调整"——满足"网络状态 + 成功率"两维，但缺"业务类型"维度。
- **F3 部分证据**：RFC 8854 的"latency budget 决定 RTX vs FEC"是二元选择 not n 个冗余包累计时间窗。
- **F4 反向 / 未检索到**：所有源都不提"网络状态 + 总时间 + 冗余包数量"三元联合调度。
- **F5 命中**：testdevlab "sustaining a high frame rate even under 20% packet loss" 间接证明 Meet 启用主动 FEC（仅 RTX 在 20% loss 下不可能维持）。
