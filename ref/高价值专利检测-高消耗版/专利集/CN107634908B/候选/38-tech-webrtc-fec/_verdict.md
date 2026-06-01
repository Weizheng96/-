# 38-tech-webrtc-fec verdict

## 候选基本信息（专利公开日 2021-06-08）
- **类型**：技术（开源标准 + 主流实现）
- **名称**：WebRTC FEC — RFC 5109 (ULPFEC) / RFC 8627 (FlexFEC) / RFC 8854 (WebRTC FEC Requirements) / draft-ietf-rtcweb-fec-10；libwebrtc (Chromium) 参考实现；Pion Go 实现（pion/webrtc v4.1.2 + pion/interceptor v0.1.38, FlexFEC encoding）
- **组织 / 主导方**：IETF / W3C / Google (libwebrtc) / Pion 社区
- **公开度**：高（开源源码 + 公开 RFC + 公开 blog + 公开 issue tracker）
- **时间合规性**：RFC 5109 = 2007；draft-flexfec / RFC 8627 = 2010-2020；RFC 8854 = 2021-01；libwebrtc fec_controller.h 早于本专利公开日 2021-06-08。**所有候选标准与默认实现均为 prior art 或与本专利同期独立演进**。判定核心在于：默认实现 + 已知派生实现里是否实际落入权 1 的 F1+F2+F4 三元组组合，而不是 prior 即排除（标准是 prior 不代表后续公司在专利公开后扩展的实现没有命中）。

## F# 命中表（F1–F5）

| Feature | 是否命中 | 直接证据 | 备注 |
|---|---|---|---|
| **F1 业务类型识别（基于 4 项 data-flow 特征变量之一）** | **不命中（反向证据）** | Chromium libwebrtc `api/fec_controller.h` 的 `UpdateFecRates(estimated_bitrate_bps, actual_framerate, fraction_lost, loss_mask_vector, round_trip_time_ms)`（5 参数全部为网络层指标，无任何"业务类型/媒体类型/场景类型"输入；亦无 F1 要求的 4 项 data-flow 特征变量：缓存包长度数目、在途包长度数目、到达间隔、突发性） | RFC 8854 在"分内容类型给建议"层面提到 audio/video，但只是 RFC 设计指南给实现者参考 codec 适配；**不是运行时检测业务类型**，更不是从 4 项 data-flow 特征变量自动推断。这是关键区别——专利 F1 要求"发送端根据数据流特征变量自动获取业务类型"，而 WebRTC 是"应用层 / SDP 协商 / 配置阶段静态指定 codec 与 FEC profile" |
| **F2 冗余包数量 = f(网络状态, 成功率, 业务类型)** | **不命中（缺业务类型输入）** | 同上 fec_controller.h 接口；Pion 文档明示 NumMediaPackets / NumFECPackets 是**手工配置常量**（默认 5:2 → 40% overhead）；getstream.io 资料确认"FEC redundancy rate is dynamically determined by the packet loss in the last a few seconds" | 即使 Chromium 做了"基于丢包率 + bitrate + RTT 自适应"，**也只有 2 元（网络状态 + 成功率），缺业务类型这第 3 元** — 权 1 把"业务类型"硬钉入 F2，缺则不命中权 1 |
| **F3 冗余包传输总时间 = f(时延要求)** | 部分（隐含） | RFC 8854 §8 "FEC should only be activated if network conditions warrant it"，对 deadline 有隐含考量；Hairpin (NSDI'24) 论文指出 WebRTC 在实时场景下按 RTT 与 deadline 残余时间规划冗余传输 | 但 WebRTC 不是按"显式时延要求 → 冗余包总传输时间"的方式来组织 — 是按"实时连续流 + 拥塞控制窗口"组织，并未对应权 1 中"冗余包传输总时间"这一明确派生量 |
| **F4 调度方法 = f(网络状态, 总时间, 冗余包数量)，从 {随机度策略 / 最短时间 / 最长时间 / 均匀时间} 中选** | **不命中（反向证据）** | Pion blog 明示："Interleaved protection will be used, which means that media packet `X` will be protected by FEC packet `(X mod NumFECPackets)`" — **单一固定 interleave 调度，无动态选择**；fec_controller.h 接口无任何"调度方法"输出或回调；RFC 8854 silent on scheduling | WebRTC FEC 的核心思想是 XOR over a group of media packets + 立即随 RTP 流发送，无四种调度方法可选 |
| **F5 按调度方法发送冗余包** | 部分（恒等同退化情形） | WebRTC 确实在主流内发送 FEC 冗余 RTP 包 | 但因调度方法不是从一个动态可选集合里选出来的，F5 的"按某调度方法发送"在权 1 语义下不成立 — 它是固定方法的发送，不是 F4 输出驱动的发送 |

**三元组完整性**：权 1 关键创新 = F1 ⊕ F2 ⊕ F4 同时引入"业务类型"和"动态调度方法选择"。WebRTC 默认 FEC stack 在这两个轴上**均无证据命中**，且有强反向证据（接口签名 / 实现代码 / 官方 blog 三类来源相互独立印证）。

## 已检查文档清单

| # | 来源 | URL | 落盘文件 | 核心摘录 |
|---|---|---|---|---|
| 1 | Chromium WebRTC `api/fec_controller.h` (lkgr branch) | https://chromium.googlesource.com/external/webrtc/+/refs/heads/lkgr/api/fec_controller.h | `fec_controller.h` (3751 bytes) | `virtual uint32_t UpdateFecRates(uint32_t estimated_bitrate_bps, int actual_framerate, uint8_t fraction_lost, std::vector<bool> loss_mask_vector, int64_t round_trip_time_ms) = 0;` — 5 个参数全部为网络层指标 |
| 2 | Pion 官方 blog "FEC with Pion" | https://pion.ly/blog/fec-with-pion/ | `pion-fec-blog.html` (28k) | "By default, for every 5 media packets, 2 FEC packets will be produced…" / "Interleaved protection will be used, which means that media packet X will be protected by FEC packet (X mod NumFECPackets)" — 手工常量 + 单一固定 interleave 调度 |
| 3 | RFC 8854 — WebRTC FEC Requirements (2021-01) | https://datatracker.ietf.org/doc/html/rfc8854 | `rfc8854.html` (102k) | 提供"按 codec 类型给 FEC 推荐"的指南，silent on runtime service-type detection / silent on scheduling method selection / silent on inputs beyond loss rate |
| 4 | Hairpin (NSDI'24) — "Rethinking Packet Loss Recovery in Edge-based Interactive Streaming" | https://www.usenix.org/system/files/nsdi24-meng.pdf | `nsdi24-meng-hairpin.pdf` (2.9 MB) | 全文 grep："service type"=0, "content type"=0, "media type"=0, "business type"=0, "interleav"=0；明示 stock WebRTC 高瞬时丢包时会发 100% 冗余 — 单一 loss-rate 驱动而非业务类型驱动 |
| 5 | getstream.io "Media Resilience in WebRTC" | https://getstream.io/resources/projects/webrtc/advanced/media-resilience/ | （仅检索，未落盘 — 信息已收敛于其他 4 源） | 概念性介绍 XOR FEC / Reed-Solomon；明示 "FEC redundancy rate is dynamically determined by the packet loss in the last a few seconds"——只 loss-rate 驱动 |
| 6 | Chromium `modules/video_coding/fec_controller_default.h` (main branch — 二次确认) | https://chromium.googlesource.com/external/webrtc/+/refs/heads/main/modules/video_coding/fec_controller_default.h | — | 同 #1 的 UpdateFecRates 5 参数签名，主分支与 lkgr 一致，无业务类型输入 |

**注**：本次检查的是 **WebRTC FEC 默认实现 + 公开标准 + Pion 主流派生实现**，目的是判定"WebRTC FEC 标准与默认实现"这个候选条目本身的命中度。**WebRTC 的下游 SaaS / RTC 平台（Daily.co / LiveKit / Twilio Video / Janus / mediasoup / SignalWire / Agora 等）若在 WebRTC 之上加了业务类型感知 + 动态调度方法选择，则需要在那些公司各自候选条目里单独判定** — 本候选不涵盖。

## 最终判定 **第 5 档：已排除**

理由：
1. **F1 不命中且有强反向证据** — Chromium 官方 `fec_controller.h` 接口签名只接受 5 个网络层参数，**不含**业务类型 / 媒体类型 / 场景类型 / 内容类型；亦不含权 1 限定的 4 项 data-flow 特征变量（缓存包长度数目 / 在途包长度数目 / 到达间隔 / 突发性）。三个独立来源（Chromium 头文件、Pion blog、Hairpin 论文）相互印证。
2. **F4 不命中且有强反向证据** — Pion 明示固定 interleave (`X mod NumFECPackets`)；Chromium 接口无调度方法输出。**没有从随机度/最短/最长/均匀 4 种方法中选**的机制。
3. **F2 三元组缺第 3 元（业务类型）** — 即便有 loss/bitrate/RTT 三个网络层输入，但**缺业务类型 = 不构成权 1 的 F2**。
4. 时间合规性确认：RFC 5109 / 8627 是 prior art；RFC 8854 与 libwebrtc 默认 FEC 实现都早于 2021-06-08 公开日，**默认行为不可能"使用"后公布的专利**。
5. **本判定限定在 WebRTC 默认 FEC stack + Pion 默认实现**。不排除某下游商业 RTC 平台在 WebRTC 之上自行实现"业务类型 + 动态调度"扩展 — 那是它们各自候选条目的判定范围。

## 升级路径（若日后取得以下新证据可重新评估）

若任一项被证实，可升至第 3 档（疑似命中）：
- (a) 某主流 WebRTC fork（如 Google 实验分支、Meta WebRTC fork、阿里 / 腾讯 / 字节自研 RTC 引擎）在公开源码 / 论文 / 专利中显示其 FEC 模块同时具备 (i) 从 data-flow 特征变量自动推断业务类型，(ii) 从 ≥2 种调度方法中按网络状态动态选择；
- (b) IETF 后续 draft（rfc8854bis 等）规范化"按业务类型选 FEC profile"的运行时机制；
- (c) Chromium WebRTC 后续版本扩展 `FecController` 接口加入业务类型或 4 项 data-flow 特征变量。

升至第 2 档（确认命中）需在上述基础上进一步确证：调度方法集合至少包含 {随机度策略 / 最短时间 / 最长时间 / 均匀时间} 中 ≥1 种 + 实测代码确实在运行时三元组联合计算。

## 总结一句话

WebRTC FEC（RFC 5109 / 8627 / 8854 + libwebrtc + Pion）的默认实现不感知业务类型、不从 4 项 data-flow 特征变量推断业务类型、不在多种调度方法间动态选择，权 1 的 F1/F2/F4 三元组联合限定均未命中且接口签名给出强反向证据，**落第 5 档：已排除**（仅限 WebRTC 默认 stack，不含下游 RTC 平台的私有扩展）。

---

**免责声明**：本报告仅是技术特征比对的线索性分析，不构成"已构成侵权"的法律结论。是否构成侵权需经过权利要求解释、等同原则、专业鉴定与司法程序后由有权机关认定。
