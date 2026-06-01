# 证据索引 — 41-google-stadia

## Phase 1 — WebSearch 留痕（react 串行）

### q1
- Query: `Google Stadia adaptive FEC packet loss streaming protocol`
- 结果：通用 FEC / arxiv 论文，**无 Stadia 专项命中**。
- Top URLs:
  - https://arxiv.org/pdf/2001.07852 （DeepRS：通用 FEC for RTC，非 Stadia）
  - https://arxiv.org/pdf/1909.06709 （通用低时延 FEC，非 Stadia）

### q2
- Query: `Stadia streaming protocol network QoS adaptive redundancy Google Research`
- 结果：**命中 Stadia 专项分析论文**。
- Top URLs:
  - https://arxiv.org/pdf/2009.09786 （Carrascosa & Bellalta — Stadia 抓包）
  - https://ar5iv.labs.arxiv.org/html/2012.06774 （Di Domenico et al. — Stadia/GFN/PSNow 对比）
  - https://spectrum.ieee.org/how-the-youtube-era-made-cloud-gaming-possible
  - https://ieeexplore.ieee.org/abstract/document/9484481/ （Network Turbulence for Stadia）
  - https://www.researchgate.net/publication/353826215_A_First_Look_at_the_Network_Turbulence_for_Google_Stadia_Cloud-based_Game_Streaming

### q3
- Query: `Google Stadia WebRTC FEC redundancy game type aware bitrate`
- 结果：摘要级证据 — "Stadia uses WebRTC with no substantial modifications"、"a single UDP flow carries separate streams for audio, video and video retransmissions"、"frame-by-frame bitrate adaptation"。
- Top URLs:
  - https://www.mdpi.com/2673-8732/1/3/15 （Di Domenico MDPI 版 — 后续 fetch 403）
  - https://www.linkedin.com/pulse/stadia-what-anders-n%C3%A4sman
  - https://inria.hal.science/hal-03421031/file/cloud_gamig_traffic_under_constraints_CR.pdf

### q4
- Query: `"Stadia" "FEC" OR "forward error correction" packet loss redundancy network analysis`
- 结果：**0 篇 Stadia 专项 FEC 文献命中**——返回全部为通用 FEC 教程 / 厂商手册。这本身是一条**间接反向信号**：若 Stadia 有公开 FEC 文档，此 query 应命中。

### q5（追加校验）
- Query: `"Stadia" "FEC" OR "forward error correction" Carrascosa Bellalta game type`
- 结果：Carrascosa & Bellalta 论文确认存在但**未提 FEC**。

## Phase 2 — WebFetch / curl 留痕（react 串行）

### fetch-1
- URL: https://arxiv.org/pdf/2009.09786
- 工具：WebFetch
- 结果：PDF 二进制无法被 WebFetch 文本化；自动缓存到本地但 sub-agent 工具集不含 PDF 解析。**走 ar5iv HTML 镜像兜底。**

### fetch-2
- URL: https://ar5iv.labs.arxiv.org/html/2012.06774
- 工具：WebFetch
- 结果：**成功**。提取到核心反向证据：
  - Stadia：reactive RTX retransmission, not proactive FEC；第三 UDP 流于 packet loss 时才激活。
  - Stadia：bitrate constant per resolution tier → static rather than dynamic redundancy scheduling。
  - Stadia：未实证业务类型 / 数据流特征变量驱动决策。

### fetch-3
- URL: https://www.mdpi.com/2673-8732/1/3/15
- 工具：WebFetch → 403 Forbidden → curl 兜底 → 同 Access Denied（Akamai edge）。
- 结果：被拦截，但 fetch-2 的 ar5iv 镜像已覆盖同一论文的内容，无信息损失。

### fetch-4
- URL: https://inria.hal.science/hal-03421031/file/cloud_gamig_traffic_under_constraints_CR.pdf
- 工具：WebFetch → 失败（被 Anubis bot 拦截）→ curl 兜底 → 同 HTML 拦截页（200 但是 HTML，非 PDF）。
- 结果：未获取；非核心来源，不影响判定（D1 + D2 已足够）。

### fetch-5
- URL: https://ar5iv.labs.arxiv.org/html/2009.09786
- 工具：WebFetch
- 结果：**成功**。提取到：Stadia 用 WebRTC + GCC（delay-based + loss-based），"sender uses the minimum of the two bitrates"；3 类 UDP 流（RTP / RTCP / DTLS / STUN）；**论文全文无 FEC / NACK / RTX 主动冗余讨论**，仅讨论 traffic characterization。

## 工具受限明示

- MDPI 与 inria HAL 均通过 edge 反爬（Akamai / Anubis），WebFetch 与 curl 双双失败。
- arxiv 原始 PDF 通过 WebFetch 拿到的是 base64-encoded 二进制流，sub-agent 工具集没有 PDF 文本提取（pdfplumber 在主仓库可用但 sub-agent 不应该跑 python 脚本）。已通过 ar5iv HTML 镜像（D1/D2 两篇核心论文）完整覆盖证据需求。
- 未做：未抓取 Google AI Blog 原文（同样需 WebFetch，预算已耗，且核心反向证据已闭环）。
