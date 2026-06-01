# 证据索引 — 29-nvidia-cloudxr

## Phase 1 粗筛 WebSearch

| # | Query | 命中关键源 |
|---|-------|---------|
| q1 | `NVIDIA CloudXR adaptive FEC packet loss streaming protocol` | 主要返回学术论文（DeepRS、TAROT 等）和 USPTO 专利；未直接命中 CloudXR 官方 FEC 描述 |
| q2 | `CloudXR network resilience low latency redundancy` | https://docs.nvidia.com/cloudxr-sdk/usr_guide/network_setup.html（官方网络配置文档） |
| q3 | `site:developer.nvidia.com CloudXR FEC` | https://forums.developer.nvidia.com/t/possible-to-configure-tune-cloudxr-encoding/208977（开发者论坛 — NVIDIA 员工明确回复 FEC 用作 QoS 的一部分） |
| q4 | `CloudXR QoS FEC adaptive bitrate documentation logs` | https://forums.developer.nvidia.com/t/network-qos-implementation/175926 ；https://docs.nvidia.com/cloudxr-sdk/prog_guide/api_doxygen.html ；https://forums.developer.nvidia.com/t/qos-and-event-trace-logs/177754 |
| q5 | `"CloudXR" "FEC" log forward error correction NVIDIA` | 重复确认 forum 175926；TESmart 文章提到 NVIDIA GeForce NOW 用 FEC（旁证） |
| q6 | `CloudXR SDK "TransportType" OR "streamType" OR "VideoQuality" QoS structure` | 指向官方 overview / release notes / api_doxygen 文档（这些页面是 JS 客户端渲染，curl 拿到的仅是 79 KB 框架） |
| q7 | `CloudXR "Missed packets" "Forward error correction" stream type` | 重复确认 forum 175926（用户提问明确把 "Missed packets - Forward error correction" 列为 CloudXR QoS 的特性之一） |

Phase 1 粗筛 **正向命中** —— 多条 NVIDIA 官方 / 员工材料证实 CloudXR 内置 FEC 与 QoS 自适应机制；进入 Phase 2 深抓。

## Phase 2 深抓 WebFetch / curl

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2022-03 起 | 论坛 / 官方 staff 回复 | https://forums.developer.nvidia.com/t/possible-to-configure-tune-cloudxr-encoding/208977 + 本目录 `encoding_tune_forum.json` | **NVIDIA staff Veronica**："Regarding FEC, this is used part of our QoS."  **NVIDIA staff tegradave**："Yes, FEC is used, you'll actually see it noted in the log when it adjusts." "The QoS tuning is all black box under the hood." "We are looking at what specific network options we can expose, likely starting with high level network profiles, like wifi5 vs wifi6 vs 5G..."  原用户日志显示 `Video stream encryption disabled for stream:0` —— 暗示存在多 stream（按 stream:N 编号） |
| 2 | 长期文档 | 官方文档（仅搜索摘要） | https://docs.nvidia.com/cloudxr-sdk/usr_guide/network_setup.html + 本目录 `network_setup_raw.html` `network_setup_latest.html` | curl 拿到的 79 KB 仅为 JS 渲染框架；WebSearch 摘要："CloudXR does not support network connections with high levels of latency or packet drops. NVIDIA CloudXR SDK has built-in resilience to handle typical networking conditions."（非 verbatim，已在 verdict 中谨慎标注） |
| 3 | 2021-04 起 | 论坛 / 仅用户提问 | https://forums.developer.nvidia.com/t/network-qos-implementation/175926 + 本目录 `qos_impl_forum.html` | 仅有原用户提问，无 NVIDIA staff 回复 |
| 4 | 2022-01 起 | 论坛 | https://forums.developer.nvidia.com/t/understanding-cloudxr-client-qos-log-file/203674 | QoS 日志包含 Latency / Round Trip Delay / Estimated Available Bandwidth / Bandwidth Utilization / Average Video Rate；**未** verbatim 描述 FEC 或 stream-type 差异 |
| 5 | 2021-05 起 | 论坛 | https://forums.developer.nvidia.com/t/qos-and-event-trace-logs/177754 | 无 staff 回复，无 FEC verbatim |
| 6 | 2021-12 (CloudXR 3.2) | NVIDIA 技术博客 | https://developer.nvidia.com/blog/build-scalable-immersive-experiences-with-networking-apis-swift-support-and-more-using-nvidia-cloudxr-3-2/ | "Client application developers can also now specify network interface information that helps CloudXR optimize QoS decisions. These include network topology type (5G, Wi-Fi, LAN) and maximum bitrate." "We've introduced an API that enables you to query the quality of service (QoS) and network information from a remote streaming server." **未** verbatim 描述 FEC 算法或 stream-type 差异 |
| 7 | 2022-09 (CloudXR 4.0) | NVIDIA 技术博客 | https://developer.nvidia.com/blog/dialed-into-5g-cloudxr-4-0-brings-enhanced-flexibility-and-scalability-for-xr-deployment/ | 提到 togglable "Low-latency, low-loss scalable throughput (L4S)"；与 Ericsson / Deutsche Telekom 合作；**未** verbatim 描述 FEC 自适应算法 |
| 8 | 长期文档 | 官方 overview | https://docs.nvidia.com/cloudxr-sdk/latest/overview/overview.html | "GPU-accelerated video encoding"、"Low-latency streaming: Optimized frame timing and network handling"；**无** FEC / 业务类型 verbatim |
| 9 | 长期文档 | 官方 API doxygen | https://docs.nvidia.com/cloudxr-sdk/prog_guide/api_doxygen.html ；`/latest/prog_guide/api_doxygen.html` | WebFetch 两个路径均 404 / JS 渲染。未拿到 verbatim 字段定义（实际字段需要本地解包 SDK 或登录 EA portal） |

## 工具受限明示

- CloudXR SDK 完整源码 / header 文件需要在 [NVIDIA CloudXR Early Access Program](https://developer.nvidia.com/cloudxr-sdk-early-access-program) 注册后下载，本 sub-agent 无凭据访问。
- `docs.nvidia.com/cloudxr-sdk/` 下绝大部分页面采用 JS 客户端渲染，curl / WebFetch 拿到的是空 shell，无法 verbatim 抽取 `cxrQoS` / `cxrStream` 等结构字段的描述。
- 因此本判定主要基于：(a) NVIDIA 员工在公开论坛的官方表述（最强证据，staff 标识为 True）；(b) NVIDIA 技术博客 / 官方文档；(c) WebSearch 引擎摘要（最弱证据，已在 verdict 中明确标注）。未触达 SDK header / 源码层。
