# 13-ms-teams 检索留痕

候选：Microsoft Teams Media Stack（Microsoft）
专利公开日基准：2021-06-08

## Phase 1 WebSearch（粗筛）

| # | Query | 命中数（相关） | 关键命中 |
|---|---|---|---|
| q1 | `Microsoft Teams adaptive FEC packet loss media stack` | 0 直接 Teams 命中（多为通用学术 / 通用专利） | DeepRS arXiv、US9577682B2 通用 adaptive FEC 专利 |
| q2 | `Microsoft Teams network resilience Skype FEC redundancy real-time` | 1 强命中 | MS Learn Skype-for-Business plan-network-requirements 页面（含 "FEC is used dynamically when there's packet loss"） |
| q3 | `site:patents.google.com Microsoft Teams Skype forward error correction redundancy adaptive` | 6 通用 adaptive FEC 专利但无 Teams/Skype 专属 | US8015474B2 / US6772388B2 / US9577682B2 — MS 有自家 adaptive FEC 专利组合（非本专利权人） |
| q4 | `"Microsoft Teams" OR "Skype" media stack FEC "business type" OR "traffic type" proactive redundancy` | 部分相关 | call-flows 页（区分 audio/video/sharing 流量类型）、media-quality 页（QoS 标记差异化） |
| q5 | `Microsoft Teams "media stack" Skype audio FEC inband redundancy SIGCOMM paper` | 1 强命中 | Satin 博客（techcommunity）— 明确说 Satin 用 "redundancy and forward error correction" 主动恢复丢包 |
| q6 | `"Microsoft Teams" OR "Skype" media quality "RED" OR "redundancy" "audio" "video" different FEC scheme separate` | 1 间接相关 | webrtcHacks RED 文章提到 Skype 使用 SILK LBRR 冗余格式 |

## Phase 2 WebFetch / curl（深抓）

| # | URL | 工具 | 状态 | 关键 verbatim |
|---|---|---|---|---|
| f1 | https://learn.microsoft.com/en-us/previous-versions/skypeforbusiness/optimizing-your-network/media-quality-and-network-connectivity-performance | WebFetch | 200 / 全文 | 仅 QoS / ExpressRoute / 网络阈值表（<5% 包丢失、<60ms RTT）；无 FEC 算法层面披露 |
| f2 | https://learn.microsoft.com/en-us/microsoftteams/microsoft-teams-online-call-flows | WebFetch | 200 / 全文 | 区分 audio (UDP 3479) / video (UDP 3480) / sharing/VBSS (UDP 3481) 流量类型 + SRTP；无 FEC 算法细节 |
| f3 | https://learn.microsoft.com/en-us/skypeforbusiness/plan-your-deployment/network-requirements/network-requirements | WebFetch | 200 / 全文 | **核心证据**：(1) "Forward Error Correction (FEC) is used dynamically when there's packet loss on the link to help maintain the quality of the audio stream." (2) "Video FEC is always included in the video payload bit rate when it's used" (3) "Maximum bandwidth with FEC … the bandwidth when the stream is at 100% activity and there's packet loss triggering the use of FEC" — 音频 / 视频 FEC 行为差异化 + 由 packet loss 动态触发；文档 ms.date 2018-03，updated_at 2025-06-18（**post-grant** 重审通过） |
| f4 | https://techcommunity.microsoft.com/t5/microsoft-teams-blog/satin-microsoft-s-latest-ai-powered-audio-codec-for-real-time/ba-p/2141382 | WebFetch 失败 → curl 兜底 | HTTP 200 / 385KB / 本地 satin_blog.html | **核心证据**：(1) "Satin's ability to deliver great audio at a low rate of 6 kbps provides the flexibility to use some of the available bitrate to add redundancy and forward error correction to quickly recover from these situations." (2) "We have recently improved our redundancy algorithms to provide better protection under burst loss." (3) "Satin is already being used for all Teams and Skype two-party calls"；博客日期 2021-02-17（**grant 前 4 个月**，但机制持续运行至 grant 后） |

## 反向证据 / 限定语监测

- f3 中 "Video FEC is always included in the video payload bit rate" —— **永远开启** ≠ "by packet loss adaptive"。可解读为视频 FEC 是固定冗余（非自适应），可能弱化 F2 中"网络状态 / 成功率参与冗余包数量计算"的命中力度。这是**限定作用域语**而非反向证据：音频 FEC 仍然是 dynamic by packet loss。
- f1 / f2 中关于 QoS 标记和 DSCP 的描述 —— 仅是网络优先级，**与冗余包数量 / 调度无关**，不构成 F2-F4 命中证据。
- q3 中 MS 自家 adaptive FEC 专利组合（US8015474B2 2008 申请等）—— 表明 MS 在本专利之前就有独立 adaptive FEC 专利路径，**降低了"必须使用本专利"的归属概率**（不是法律免责证据，但是非侵权抗辩素材）。

## 工具受限明示

- WebFetch 对 techcommunity.microsoft.com 的 Satin blog 报错 "no content provided"（应是 Cloudflare 渲染或 JS-required 页面），已按 SKILL 规则 curl 兜底成功（385KB HTML 保存到本地 `satin_blog.html`），用 Python regex 抽取了 FEC/redundancy 邻域文本。
- 未访问 MS 内部技术白皮书 / Build 大会 deep-dive session（YouTube `BRK4016 Understanding Media Flows in Microsoft Teams` 仅是 URL 引用，未做 WebFetch 视频转录）。
