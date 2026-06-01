# 证据索引 — 11-zoom-meetings

## Phase 1 检索 query（WebSearch — react 串行 4 个）

| # | Query | 命中性 | 摘要 |
| --- | --- | --- | --- |
| q1 | `Zoom Meetings adaptive FEC packet loss redundancy` | 命中 | Zoom 官方/第三方均确认使用 FEC + 自适应 QoS（监控带宽/丢包/时延/抖动） |
| q2 | `Zoom audio video FEC scenario codec packet recovery business type` | 命中 | Zoom 视频/音频均做 FEC；丢包率到 ~45% 仍可用；音频优先于视频 |
| q3 | `Zoom patent FEC adaptive redundancy packet loss latency` | 部分命中 | Zoom 有专利组合（压缩 / 自适应码率），但未直接列出 FEC 冗余计算专利号 |
| q4 | `site:patents.google.com Zoom Video Communications FEC redundancy adaptive` | 弱命中 | 搜索结果中 "system and method for correcting network loss" 系列实为 **Agora Lab** 专利，非 Zoom；未检索到 Zoom 公司直接的 FEC 自适应冗余专利 |

## Phase 2 深抓（WebFetch — react 串行 6 个）

| # | 时间 | 类型 | URL | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2026-05 | Zoom 官方 | https://library.zoom.com/admin-corner/architecture-and-design/zoom-architected-for-reliability | 监控 bandwidth/packet loss/latency/jitter；自适应码率 + 丢包缓解；音频优先于视频；未提及 FEC 数量 / 调度公式 / 业务类型分类 |
| 2 | 2026-05 | Zoom 官方 | https://library.zoom.com/admin-corner/network-management/quality-of-service-and-network-best-practices-explainer/configuring-network-components-for-zoom | 明确提及 "Forward Error Correction (FEC) may also be available to recover lost media data packets without retransmission"；DSCP marking；未提及自适应冗余机制 / 调度 |
| 3 | 2026-05 | USPTO PDF | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11616986 | PDF 为图片编码无法解析；同号 GP 查证为 Agora 专利 |
| 4 | 2026-05 | USPTO PDF | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11706456 | PDF 为图片编码无法解析；同号 GP 查证为 Agora 专利 |
| 5 | 2026-05 | Google Patents | https://patents.google.com/patent/US11616986B2/en | **assignee: Agora Lab Inc**（非 Zoom）。reference-order AL-FEC，未涉及业务类型/数据流特征三元组 |
| 6 | 2026-05 | 第三方架构文章 | https://www.designgurus.io/blog/design-video-conferencing-system | Zoom 用 FEC "every so many packets"；音频优先于视频；未涉及自适应冗余包数 / 业务类型分类 / 调度公式 |

## 工具受限明示

- USPTO PDF 端点返回的 PDF 为图像编码（CCITT Fax），WebFetch 无法 OCR；改走 patents.google.com HTML 版本完成解析。
- Zoom 多数 marketing/产品页有 302 同步重定向，未对该页继续 fetch。
- 未对 Zoom 闭源客户端二进制做反向（无授权，超出范围）；未抓 Zoom 闭门白皮书 / SDK PDF。
