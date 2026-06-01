# 38-tech-webrtc-fec — 检索与抓取留痕

## Phase 1 — WebSearch 粗筛（react 串行）

| # | Query | 关键信号 |
|---|---|---|
| q1 | `WebRTC FlexFEC ULPFEC adaptive FEC service type scenario detection` | 命中：BlogGeek FlexFEC/ULPFEC 词条、getstream Media Resilience、Pion FEC blog、IETF draft-ietf-rtcweb-fec-10、RFC 8854、Chromium FecController；**未发现** "service type 检测"作为 WebRTC FEC 设计概念出现 |
| q2 | `WebRTC FEC packet scheduling redundancy count algorithm adaptive network state` | 命中：Hairpin NSDI'24、RFC 8854、Altanai blog、getstream；明示 WebRTC FEC 主要按 loss rate 自适应，无 service-type 输入 |
| q3 | `Pion webrtc FEC implementation adaptive scheduling` | 命中：Pion FEC blog、Pion issue #920 / #1418、IEEE "ML-Powered Adaptive FEC"；NLnet "Pion adaptive" 项目；明示 Pion 用 TWCC + 静态 NumMediaPackets/NumFECPackets，非业务类型驱动 |
| q4 | `chromium webrtc source code fec_controller adaptive redundancy` | 命中：`api/fec_controller.h` (lkgr)、receiver_fec.cc、TAROT (arxiv)、getstream、Mozilla audio FEC 实验 — 拿到 fec_controller.h 直链供 Phase 2 抓取 |

Phase 1 结论：**有信号，可进入 Phase 2 深抓**（不剪枝）。

## Phase 2 — WebFetch / curl 深抓（react 串行）

| # | 方式 | URL | 状态 | 落盘 |
|---|---|---|---|---|
| f1 | WebFetch | https://chromium.googlesource.com/external/webrtc/+/refs/heads/lkgr/api/fec_controller.h | 200 — 提取 `UpdateFecRates` 完整签名，确认 5 参数无 service type | — |
| f2 | WebFetch | https://pion.ly/blog/fec-with-pion/ | 200 — 提取 NumMediaPackets/NumFECPackets 手配 + interleave 调度 verbatim | — |
| f3 | WebFetch | https://datatracker.ietf.org/doc/html/rfc8854 | 200 — 确认 RFC silent on service-type / inputs / scheduling | — |
| f4 | WebFetch | https://getstream.io/resources/projects/webrtc/advanced/media-resilience/ | 200 — 概念性介绍 XOR FEC + loss-rate driven | — |
| f5 | WebFetch | https://www.usenix.org/system/files/nsdi24-meng.pdf | **403 Forbidden** → curl 兜底 | `nsdi24-meng-hairpin.pdf` (2.9 MB) ✓ |
| f6 | curl | https://chromium.googlesource.com/external/webrtc/+/refs/heads/lkgr/api/fec_controller.h?format=TEXT | 200 — base64 解码后保存 | `fec_controller.h` (3751 bytes) ✓ |
| f7 | curl | https://pion.ly/blog/fec-with-pion/ | 200 | `pion-fec-blog.html` (28k) ✓ |
| f8 | curl | https://datatracker.ietf.org/doc/html/rfc8854 | 200 | `rfc8854.html` (102k) ✓ |
| f9 | WebFetch | https://chromium.googlesource.com/external/webrtc/+/refs/heads/main/modules/video_coding/fec_controller_default.h | 200 — 二次确认 UpdateFecRates 签名 | — |
| f10 | local grep | `nsdi24-meng-hairpin.pdf` | service type/content type/media type/business type/interleav = **0 hits** | — |

## 关键反向证据 verbatim

1. **Chromium `fec_controller.h`**：
   > `virtual uint32_t UpdateFecRates(uint32_t estimated_bitrate_bps, int actual_framerate, uint8_t fraction_lost, std::vector<bool> loss_mask_vector, int64_t round_trip_time_ms) = 0;`
   — 5 参数全部为网络层指标，无业务类型 / 4 项 data-flow 特征变量

2. **Pion blog**：
   > "By default, for every 5 media packets, 2 FEC packets will be produced…"
   > "Interleaved protection will be used, which means that media packet `X` will be protected by FEC packet `(X mod NumFECPackets)`"
   — 手工常量 + 单一固定 interleave 调度

3. **RFC 8854 §8**：
   > "FEC should only be activated if network conditions warrant it, or upon explicit application request."
   — 仅"网络状态条件" + "应用显式请求"两种激活条件，无业务类型自动检测

4. **getstream.io**：
   > "FEC redundancy rate is dynamically determined by the packet loss in the last a few seconds"
   — 单一 loss-rate 驱动

## 工具受限说明

- NSDI'24 论文 PDF 通过 WebFetch 返回 403，已用 curl 兜底成功（2.9 MB），并通过 pdfplumber 抽文 + grep 关键词补证。
- 未抓取下游商业 RTC 平台（Daily.co / LiveKit / Twilio / Agora 等）的私有 FEC 实现 — 本候选范围限定为"WebRTC 默认 stack + 公开标准 + Pion 主流实现"。下游商业实现在各自候选条目中处理。
