# Sources — 04 WebRTC Upstream Google

| # | 类型 | URL | 时间档 | 命中 |
| --- | --- | --- | --- | --- |
| 1 | §A.4 代码 / 文档 | [api/fec_controller.h](https://webrtc.googlesource.com/src/+/master/api/fec_controller.h) | 持续维护 | F2 — FecController 抽象 |
| 2 | §A.4 代码 | [flexfec_sender.cc](https://webrtc.googlesource.com/src/+/1743a19183e65c338db05d2b212afd6a13151721/webrtc/modules/rtp_rtcp/source/flexfec_sender.cc) | 2018+ | F2 — FlexFEC (RFC 8627) |
| 3 | §A.4 文档 | [Pacer index.md](https://webrtc.googlesource.com/src/+/HEAD/modules/pacing/g3doc/index.md) | 持续 | F4 — leaky bucket + priority |
| 4 | §A.4 文档 | [RTP in WebRTC](https://webrtc.googlesource.com/src/+/HEAD/pc/g3doc/rtp.md) | 持续 | F1 — SSRC + payload type |
| 5 | §A.4 文档 | [Video stats](https://webrtc.googlesource.com/src/+/HEAD/video/g3doc/stats.md) | 持续 | F2 — GCC bandwidth estimation |
| 6 | §A.4 文档 | [Video coding](https://webrtc.googlesource.com/src/+/HEAD/modules/video_coding/g3doc/index.md) | 持续 | F2 — FecControllerDefault |
| 7 | §A.4 引擎 | [media/engine/webrtc_video_engine.cc](https://webrtc.googlesource.com/src/+/2efae7786e6632b5a223fd6963df3a860cfff770/media/engine/webrtc_video_engine.cc) | 2017+ | F1/F2 — ULPFEC/RED/FlexFEC 自动配置 |

§A.7 上游开源贡献者归因：webrtc.googlesource.com 主要 maintainer 来自 Google + 第三方贡献（Cisco, Mozilla, Apple, MS）。
§A.18 国际同族专利：本专利在美国 / 欧洲 / 日本 / 韩国是否有同族 — 工具能力下未深抓。
§A.20 反向工程：N/A — 上游开源代码已公开，可直接源代码级审计。
