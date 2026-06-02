# 证据索引 — 11-cisco-webex

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | Phase1-q1 | WebSearch | `Cisco Webex FEC forward error correction packet loss adaptive redundancy media` | 命中 Webex 带宽白皮书 + Cisco SD-WAN FEC；确认 Webex 随网络条件用 video RTX 或 FEC（方向相关，未剪枝） |
| 2 | Phase1-q2 | WebSearch | `Webex media adaptive FEC RTX network condition media type redundancy whitepaper` | 命中 Cisco 带宽管理架构 PDF + WebRTC media resilience；RTX/FEC 随网络条件与媒体类型选择 |
| 3 | Phase2-q3 | WebSearch | `assignee Cisco patent adaptive FEC redundancy media type packet loss` | 同主题专利多为单因子自适应 FEC；US10225045 实为 HPE |
| 4 | Phase2 | WebFetch(403) | https://www.cisco.com/c/en/us/products/collateral/conferencing/webex-meetings/white_paper_c11-691351.html | Cisco.com 403 Forbidden；curl Schannel TLS handshake 失败；Invoke-WebRequest 连接被关闭 → 原文无法取 |
| 5 | Phase2 | WebFetch(403) | https://www.cisco.com/c/dam/en/us/td/docs/solutions/CVD/Collaboration/AltDesigns/BWM-Wbx.pdf | PDF 403 Forbidden，无法取逐字 |
| 6 | Phase2 | WebFetch | https://www.gtt.net/us-en/resources/blog/sd-wan-and-forward-error-correction-mitigating-packet-loss/ | SD-WAN 按丢包率动态调冗余比例；非 Webex，无业务类型/时延输入 |
| 7 | Phase2 | WebFetch | https://getstream.io/resources/projects/webrtc/advanced/media-resilience/ | 通用 WebRTC：RTX 适合低 RTT、FEC 适合高延迟；随网络条件自适应；无三输入公式 |
| 8 | Phase2 | WebFetch | https://patents.google.com/patent/US10225045B2/en | 受让人 = Hewlett Packard Enterprise（非 Cisco）；机制为按重传请求时序调 FEC 等级；不命中三输入公式 |

## 工具受限说明
- Cisco.com 全站对自动化访问硬拦截：WebFetch 返回 403；curl 8.15 (Schannel) 在 TLS 握手阶段失败 (curl 35)；PowerShell Invoke-WebRequest 连接被远端关闭。Cisco 官方 Webex 媒体韧性原文未能逐字取证，仅能依赖 WebSearch 摘要。
- USPTO image-ppubs PDF 为扫描件(CCITT Fax)，非文本可检索，改用 Google Patents OCR 文本核验受让人与机制。
