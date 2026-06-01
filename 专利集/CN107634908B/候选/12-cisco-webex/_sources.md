# 12-cisco-webex 检索留痕

## Phase 1 WebSearch queries（react 串行）

1. `Cisco Webex adaptive FEC packet loss media stack`
   - 命中：Bandwidth Planning whitepaper, 5 smart ways media-enhancement-ebook (PDF 被 403), SDWAN FEC docs, TalkingPointz
   - 信号：Webex 50% packet loss resilience；FEC vs RTX 选择基于 network conditions；audio/video 流独立 resilient。
2. `Cisco Webex media engine network optimization business type adaptive redundancy decision`
   - 命中：Bandwidth Planning whitepaper（再次）, Webex Calling PA, Webex Edge Connect, BRKCOL-2055。
   - 信号："Cisco will always prioritize audio over content sharing and main video"——明确按 media class 区分调度。
3. `Cisco IETF RFC FEC redundancy RTP video traffic class`
   - 命中：RFC 8627 (FlexFEC), RFC 6015, RFC 8854 (WebRTC FEC requirements)。
   - 信号：Cisco co-author M. Zanaty 参与 RFC 8627 制定，FlexFEC 是 Cisco 系标准基础。
4. `site:patents.google.com Cisco adaptive FEC video conferencing redundancy traffic type`
   - 命中：US9577682B2 (Adaptive FEC system), US8495474B2, CN107534520A (Bundling FEC for multi-streams)。
   - 信号：Cisco 在 adaptive FEC 领域有自有专利组合（后续可深查 US9577682B2 claim 文本以判断是否覆盖三元组算法）。
5. `"Webex" "FEC" packet loss percentage threshold algorithm audio voice priority`
   - 命中：Unified CM call quality grades, Troubleshooting AV Quality PDF, Bandwidth Planning whitepaper, USF-AFEC paper study, Voice Quality MOS in Control Hub。
   - 信号：进一步确认 Webex 按 loss <2.5% / latency <200ms / jitter <75ms 阈值监控，但具体 FEC 阈值公式未公开。
6. `"Webex" "MARI" media adaptation resilience implementation video pacing burstiness`
   - 命中：Troubleshooting AV Quality PDF, Webex blog (smart adaptive media resilience), Bandwidth Planning whitepaper, 2 USPTO patents on adaptive pacing (9654525, 9237467)。
   - 信号：MARI 名词与"video packet pacing which minimizes packet loss due to burstiness"确认；burstiness 是 MARI 显式输入。

## Phase 2 WebFetch / curl 留痕（react 串行）

1. WebFetch `https://www.cisco.com/c/dam/en/us/products/collateral/conferencing/webex-meetings/webex-meetings-media-enhancement-ebook.pdf` → **HTTP 403 Forbidden**
2. WebFetch `https://www.cisco.com/c/en/us/products/collateral/conferencing/webex-meetings/white_paper_c11-691351.html` → **HTTP 403 Forbidden**
3. curl 兜底 #1：`webex-meetings-media-enhancement-ebook.pdf` → 仍被 block（返回 523 byte 假 PDF / HTML 错误页，已删除）
4. curl 兜底 #2：`white_paper_c11-691351.html` → **成功**（166 KB HTML），已落盘为 `webex-bandwidth-whitepaper.html`，关键内容在 L1713-1744（Audio/Video RTX + 50% loss resilience）。
5. curl `https://www.cisco.com/c/dam/en/us/td/docs/solutions/CVD/Collaboration/hybrid/AltDesigns/PA-WbxCall.pdf` → **成功**（7.9 MB PDF），落盘 `PA-WbxCall.pdf`，pdfplumber 提取后 `PA-WbxCall.txt`（206 KB），主要含 Webex Calling 部署架构，无媒体引擎 FEC 细节。
6. curl `https://www.cisco.com/c/dam/td-xml/en_us/collaboration/cloud_cmr/pcia_2_0/reports/Troubleshooting_Audio_and_Video_Quality_Using_Webex_Control_Hub.pdf` → **成功**（2.8 MB），落盘 `Troubleshooting_AV_Quality.pdf` + 提取 `Troubleshooting_AV_Quality.txt`（59 KB）。**关键证据所在**：L454-473 含 MARI 定义 + RTX-vs-FEC 动态选择规则 + delay tolerance 输入 + per-media-stream class 分流。
7. WebFetch `https://datatracker.ietf.org/doc/html/rfc8627` → 成功；确认 Cisco co-author M. Zanaty；RFC 仅定义 FEC 格式与 payload type，**不规定** redundancy 数量算法（留给 implementation）。
8. curl `https://www.cisco.com/c/dam/en/us/td/docs/solutions/CVD/Collaboration/AltDesigns/BWM-Wbx.pdf` → **被 block**（483 byte 假 PDF，已删除）。
9. WebFetch `https://blog.webex.com/collaboration/video-conferencing/turning-good-videoconferencing-into-a-great-meetings-with-smart-adaptive-media-resilience-in-webex-meetings/` → 成功但仅含 marketing 表述，无算法细节。

## 工具受限说明
- Cisco 部分 PDF endpoint（webex-meetings-media-enhancement-ebook.pdf, BWM-Wbx.pdf）对 WebFetch 与 curl 均返回 403，无法获取。这些 PDF 的高层信息已通过 WebSearch 摘要捕获（Bandwidth Planning whitepaper HTML 版本已完整获取，覆盖了相同主题）。
- Cisco Webex 媒体引擎为闭源商业产品，公开技术文档止步于 mechanism-level 描述（"用 FEC + RTX"、"根据延迟与带宽选择"），不披露具体的冗余数量计算公式与调度算法。这是本判定卡在第 3 档而非升至第 2 档的核心原因。

## 候选可保留的最终落盘文件
- `webex-bandwidth-whitepaper.html`（166 KB）
- `PA-WbxCall.pdf`（7.9 MB）+ `PA-WbxCall.txt`（206 KB）
- `Troubleshooting_AV_Quality.pdf`（2.8 MB）+ `Troubleshooting_AV_Quality.txt`（59 KB）
- `_verdict.md`、`_sources.md`、`_meta.json`
