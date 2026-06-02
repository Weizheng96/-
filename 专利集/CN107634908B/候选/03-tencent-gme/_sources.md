# 证据索引 — 03-tencent-gme

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| Q1 | 2026-06 检索 | WebSearch | query:`腾讯 GME 游戏多媒体引擎 弱网 FEC 抗丢包 冗余` | 命中 GME 网络编解码系列文章；确认 FEC+PLC / ARQ+PLC 分场景策略 |
| Q2 | 2026-06 检索 | WebSearch | query:`腾讯 GME 业务类型 语音 游戏 网络策略 FEC 冗余 自适应 网络状态 切换` | 确认对战开黑(FEC 4+4) / 社交语音(ARQ) / 直播(UDT) 分场景 |
| 1 | ~2019 (付费墙) | HTML | https://blog.csdn.net/Tencentgme/article/details/103857430 | 腾讯官方 GME 博客；2.1 节后付费墙，仅取概述 |
| 2 | ~2019 | HTML(本地) | segmentfault-gme-network-codec-21501763.html / https://segmentfault.com/a/1190000021501763 | **核心证据**：分场景策略、FEC 4+4 上限抗 30%、丢包率驱动"快响应慢恢复"动态冗余、Jitter/RTT 时延约束 |
| 3 | ~2019 | HTML | https://segmentfault.com/a/1190000021282923 | FEC 信道编码原理 X+Y 包；**房间类型由开发者显式选择**（非引擎自动识别业务类型） |
| 4 | ~2019 | HTML | https://segmentfault.com/a/1190000021233052 | "抗丢包，主要是自适应重传策略，或者冗余编码"；"信道编码，包括包头和FEC编码" |

注：GME 网络编解码公开文章成文于约 2019 年（早于专利授权日 2021-06-08），但 GME 为持续运营的在线产品，授权日后仍在售/在用，故按持续性材料纳入；机制级证据来自这批公开技术文章。
