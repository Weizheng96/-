# Verdict — 04 WebRTC Upstream (Google)

> 候选：C1 WebRTC 上游（webrtc.googlesource.com）
> 适用独立权：权 1 + 权 8（内嵌 WebRTC 的浏览器 / 终端 OS）
> 主体类型：T4 上游开源协议（R-OPENSOURCE 双层 P0 上游侧）
> Priority：P0

## F# 命中表（仅看 WebRTC 上游自身代码 + 文档）

| F# | 字面 | 等同 | 综合 |
| --- | --- | --- | --- |
| F1 业务类型 | RtpPacketPacer 优先级排序 (audio > retransmissions > video/FEC > padding) — 按 SSRC + payload type 区分业务 | 等同 service-type | **字面命中**（priority 字段即业务类型差异化）|
| F2 冗余包数量 | `FecController` / `FecControllerDefault` + `ProtectionBitrateCalculator` + FlexFEC speed = f(GCC, loss, RTT) | — | **字面命中** |
| F3 时延要求 | RTP timestamp + 实时优先级隐含 | 等同 deadline (jitter buffer + audio deadline 实时性) | **等同命中** |
| F4 调度方法 | Pacer "leaky bucket algorithm" + GCC SetPacingRates | 等同 uniform 调度方法 | **等同命中** |
| F5 发送 | PacedSender 经 UDP socket 实际发送 | — | **字面命中** |

字面 3/5 + 等同 2/5。

## 状态机三栏

| 权 | 原始 | 后置 | 最终 |
| --- | --- | --- | --- |
| 权 1 | 第 2 档 | 1. 等同三步法对 F3/F4 跑过 4 行成立；2. 上游继承推断禁止规则：本候选证据 100% 来自 WebRTC 上游自家文件，非从下游推断 ✅；3. Active；4. §A.9 未发现专利申请日前覆盖度 ≥60%；5-7 同 01；patent pledge：Google 是 WebRTC 维护方但**华为非 WebRTC patent grant 方**，工具能力下未发现华为做 royalty-free 承诺 | **第 2 档 确认侵权（中）** |
| 权 8 | 第 2 档（Chromium / Edge / Firefox / Safari / 内嵌 WebRTC 的 OS 出厂时设备权候选） | 同上 | **第 2 档 确认侵权（中）** |

## 关键证据 URL

- [webrtc.googlesource.com/src/+/master/api/fec_controller.h](https://webrtc.googlesource.com/src/+/master/api/fec_controller.h) — FecController 抽象
- [webrtc.googlesource.com/.../flexfec_sender.cc](https://webrtc.googlesource.com/src/+/1743a19183e65c338db05d2b212afd6a13151721/webrtc/modules/rtp_rtcp/source/flexfec_sender.cc) — FlexFEC sender (RFC 8627)
- [webrtc.googlesource.com/src/+/HEAD/modules/pacing/g3doc/index.md](https://webrtc.googlesource.com/src/+/HEAD/modules/pacing/g3doc/index.md) — Pacer leaky bucket + priority
- [webrtc.googlesource.com/src/+/HEAD/pc/g3doc/rtp.md](https://webrtc.googlesource.com/src/+/HEAD/pc/g3doc/rtp.md) — RTP / SSRC / payload type
- [webrtc.googlesource.com/src/+/HEAD/video/g3doc/stats.md](https://webrtc.googlesource.com/src/+/HEAD/video/g3doc/stats.md) — video stats / GCC
- [webrtc.googlesource.com/src/+/HEAD/modules/video_coding/g3doc/index.md](https://webrtc.googlesource.com/src/+/HEAD/modules/video_coding/g3doc/index.md) — FecControllerDefault

## 总结一句话

WebRTC 上游 (Google 维护) 通过 FecController + FlexFEC + Pacer + GCC 形成 F1-F5 完整链路（含 2 个等同命中）；落第 2 档（确认侵权中）作为 R-OPENSOURCE 双层 P0 上游侧；下游商业 fork 派生独立评估（候选 02 / 03 / 06 / 09 / 26 等）。
