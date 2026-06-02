# 证据索引 — 14-nvidia-geforce-now（检索留痕）

## Phase 1 — react 粗筛（WebSearch）
1. `NVIDIA GeForce NOW streaming FEC packet loss adaptive redundancy network`
   - 命中 NVIDIA 官方 L4S 文档（custhelp a_id 5522）+ 论坛丢包帖。L4S = ECN 拥塞标记 → 调整串流码率（rate），非冗余包调度。相关但抽象层为"码率自适应"。
2. `GeForce NOW cloud gaming forward error correction FEC redundant packets network condition adaptive`
   - 证实 GeForce NOW 使用 FEC（TESmart 博客："Both NVIDIA's GeForce NOW and AMD's cloud gaming platforms use FEC"）。通用 Adaptive FEC = 按丢包率/SLA 动态调冗余比（单因子链路条件驱动）。
3. `NVIDIA cloud gaming streaming patent forward error correction redundancy adaptive bitrate latency 2022 2023`
   - 命中 NVIDIA 自有专利 US10230405「System and method of forward error correction for streaming media」——FEC repair rate adjuster 按 unrecovered source packets / unused repair packets 调整。

## Phase 2 — react 深抓（WebFetch + 定向 WebSearch）
4. WebFetch https://patents.google.com/patent/US10230405B2/en
   - assignee = NVIDIA Corporation；优先权/申请日 2015-08-26；授权 2019-03-12。
   - 权 1 verbatim 已抓取。机制 = FEC repair rate 按"未恢复源包数 + 未用修复包数"反馈调整（loss/success 驱动）。
   - 明确**无**业务类型识别（no traffic classification）；**无**时延要求→传输总时间→冗余调度链。
5. WebSearch `NVIDIA patent dynamic forward error correction FEC repair rate adjuster ... assignee:Nvidia`
   - 锁定 US10230405 为 NVIDIA 自有同主题专利；另见 US8091011（按上行 FEC 反馈调速，非 NVIDIA 主线）。
6. WebSearch `NVIDIA patent ... redundant packet scheduling latency requirement traffic type 2022 2023 2024 FEC game`
   - 未检索到 2021-06-08 后 NVIDIA 自有专利新增"业务类型识别"或"时延→传输总时间→冗余调度"链。NVIDIA 云游戏专利族集中在 frame-rate capping / RTVL 拥塞码率自适应 / 包优先级，非本专利三输入冗余量 + 调度时间双自适应。

## 关键来源 URL
| # | 类型 | URL | 命中要点 |
| --- | --- | --- | --- |
| 1 | NVIDIA 官方 | https://nvidia.custhelp.com/app/answers/detail/a_id/5522/ | L4S — 拥塞码率自适应，非冗余调度 |
| 2 | 二手博客 | https://www.tesmart.com/blogs/news/what-is-forward-error-correction-how-does-it-improve-gaming-experience | GeForce NOW 使用 FEC（确认在用 FEC） |
| 3 | NVIDIA 自有专利(primary) | https://patents.google.com/patent/US10230405B2/en | FEC repair rate 按未恢复源包/未用修复包反馈调整；无业务类型识别、无时延→调度链 |
| 4 | 专利族概览 | https://www.patsnap.com/resources/blog/articles/cloud-gaming-sub-100ms-latency-patent-landscape-2026/ | NVIDIA 云游戏专利族 = frame-rate capping / RTVL 码率自适应 |
