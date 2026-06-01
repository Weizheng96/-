# 28-meta-airlink _sources.md

## Phase 1 WebSearch query 留痕（react 串行）

### q1
- query: `Meta Quest Air Link FEC packet loss streaming`
- 结果摘要：Air Link 丢包讨论多为 Wi-Fi 链路质量 / 路由器兼容性 / 用户故障；未出现"主动 FEC 冗余包"技术描述。
- 主要 URL：
  - https://www.meta.com/help/quest/975178886590868/
  - https://communityforums.atmeta.com/t5/Get-Help/Resolved-Air-Link-Connections-Lag-or-Low-FPS/td-p/970955
  - https://community.tp-link.com/en/home/forum/topic/634366

### q2
- query: `Oculus Air Link adaptive redundancy VR streaming protocol`
- 结果摘要：Meta 官方机制名为 **AFI（Air Link Framerate Insurance）**，使用 ML / ASW 风格运动矢量外推；另一主要机制为 **动态码率（dynamic bitrate）**。两者均非传输层主动 FEC。
- 主要 URL：
  - https://developers.meta.com/horizon/blog/air-link-framerate-insurance-afi/
  - https://www.pcgamesn.com/oculus/quest-2-afi-streaming
  - https://mixed-news.com/en/meta-quest-2-pc-vr-streaming-with-air-link-latency-review/

### q3
- query: `site:patents.google.com Meta Oculus FEC streaming forward error correction`
- 结果摘要：未找到 Meta / Oculus 名下专门针对"VR 串流 + FEC 主动冗余 + 业务类型识别"的专利布局。命中 5 篇均为他人 / 通用 FEC 流媒体专利。
- 主要 URL：
  - https://patents.google.com/patent/US7676735
  - https://patents.google.com/patent/WO2006135877A2/tr
  - https://patents.google.com/patent/US8015474

### q4
- query: `"Air Link" OR "Quest Link" architecture protocol traffic type business type aware bitrate`
- 结果摘要：Air Link 采用 **动态码率自适应** + YUV 4:2:0 子采样；未发现"业务类型自适应"或"数据流特征变量驱动业务分类"机制的公开描述。
- 主要 URL：
  - https://pimax.com/blogs/highlights/technical-comparison-displayport-direct-connection-vs-quest-3-streaming-solutions-for-pcvr
  - https://forums.flightsimulator.com/t/dynamic-bitrates-with-link-and-air-link-a-dynamic-duo/695087

## Phase 2 WebFetch 留痕

### f1 — Meta 官方 AFI 技术博客
- URL: https://developers.meta.com/horizon/blog/air-link-framerate-insurance-afi/
- 提取：AFI = post-transmission frame recovery（ASW 风格运动矢量外推），dynamic bitrate 为反应式码率调节。文档明示 "explicitly NOT covered: Pre-transmission redundancy or FEC mechanisms; Packet-level protocol details; Traffic classification systems"。
- 证据指向：**F1（业务类型识别） 反向证据**；**F5（主动冗余包发送） 反向证据**。

### f2 — Pimax 第三方 Air Link 协议拆解
- URL: https://pimax.com/blogs/highlights/technical-comparison-displayport-direct-connection-vs-quest-3-streaming-solutions-for-pcvr
- 提取 verbatim：
  - > "Air Link's dynamic bitrate scaling algorithm, designed to avoid frame drops, proactively reduces video quality when link conditions degrade"
  - > "the TCP retransmission mechanism inherent in Wi-Fi networking introduces unavoidable frame delays when packet loss occurs"
- 证据指向：Air Link 走 **动态码率 + TCP/ARQ 重传** 路径；与权 1 的"主动 FEC 冗余包 + 业务类型自适应"路径不重叠。**F5 反向证据**。

### f3 — Mixed-news Air Link 延时拆解
- URL: https://mixed-news.com/en/meta-quest-2-pc-vr-streaming-with-air-link-latency-review/
- 提取：延时分量含 Encode/Transfer/Decode ~5.6ms，但未描述任何传输层冗余 / 业务类型 / 冗余调度机制。证据空白（neither hit nor strict counter，倾向 reactive 模式）。

## 工具受限明示
- 无法访问 Meta 内部 Air Link 协议 SDK / 源码 / 内部技术白皮书；以上结论基于公开技术博客 + 第三方拆解 + 专利检索综合判断。
- Air Link 协议黑盒——不排除内部存在未公开的轻量级 FEC 模块，但即便存在，公开资料未显示其与权 1 的"业务类型 + 数据流特征变量 + 冗余包数量 + 调度方法"四元组耦合方式一致。
