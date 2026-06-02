# 01-tech-google-webrtc 检索留痕（_sources.md）

## Phase 1 — react 粗筛（WebSearch）
- query 1: `WebRTC FlexFEC ULPFEC adaptive redundancy 冗余 网络状态`
  → 命中相关。确认 WebRTC 用 FlexFEC/ULPFEC（XOR FEC, RFC 5109/8627），并依网络状态(丢包/带宽/RTT)自适应启停与调整 FEC。getstream / bloggeek / RFC 8854。
- query 2: `WebRTC FEC controller protection factor loss rate bandwidth estimate VCMProtectionMethod media optimization`
  → 命中强相关一手机制描述。FecControllerDefault.UpdateFecRates 输入 = estimated_bitrate_bps + fraction_lost + RTT + actual_framerate；ProtectionFactor 用 kFecRateTable[bitrate, packetLoss] 查表，并按分辨率/帧率/RTT 调整；I/P 帧分别保护。Google 研究论文 research.google.com/pubs/archive/41611.pdf。

（粗筛即命中强信号，进入 Phase 2，未触发早剪枝。）

## Phase 2 — react 深抓（WebFetch / 落盘）
- WebFetch https://research.google.com/pubs/archive/41611.pdf → 302 跳转 static.googleusercontent.com；二次 WebFetch 得二进制 PDF（398KB），已落盘 `google-handling-packet-loss-webrtc.pdf`，用 pdfplumber 提取正文核验。【L1 一手：Google "HANDLING PACKET LOSS IN WEBRTC", Holmer/Shemer/Paniconi, ICIP 2013】
  - 关键句：MO（Media Optimization）"periodically receives network statistics … These network statistics include the available bandwidth, fractions of packets lost and the Round Trip Time (RTT)"；"The MO also receives encoder statistics such as the incoming frame rate and the actual bitrates"；"The main function of MO … is to set the amount of FEC protection"。
  - 多帧 FEC 跨度 λ ~ max(1, min(f·RTT, λo))（f=帧率）；接收端附加播放时延 d_add = min(max(K – RTT/2 – d_jitter,0),RTT)（K=最大可接受端到端时延）。
  - 全文未出现"业务类型/traffic type/media type 由数据流特征(包长度/数目/到达间隔/突发性)自动识别"的机制。
- WebFetch https://blog.csdn.net/qw225967/article/details/136457874 → 命中，核对 FecControllerDefault 源码级输入。【L2 二手代码分析】
  - 输入 = fraction_lost + estimated_bitrate_bps + round_trip_time_ms + actual_framerate + SetEncodingData(width,height)。ProtectionFactor 查表 indexTable=rateIndexTable*kPacketLossMax+packetLoss，并按分辨率/每帧包数调整。
  - 明确"未发现业务类型/media type 自动识别机制"；仅有关键帧/P 帧的编码层区分，非业务层；未涉及"时延要求→冗余传输总时间→冗余包发送调度"的链路。

## 工具受限说明
- https://www.fanyamin.com/webrtc/tutorial/build/html/3.media/webrtc_fec.html → 404，放弃（已有 Google L1 论文 + CSDN 源码分析两源相互印证，足以判定）。

## 证据时间窗
- Google ICIP 论文 2013 年（早于专利公开日 2021-06-08），属机制描述类背景；WebRTC FecControllerDefault 代码持续维护至今（2024 CSDN 分析对应现行代码），机制延续，时间窗不单独构成排除理由。判定主依据为"机制是否落 F#"。
