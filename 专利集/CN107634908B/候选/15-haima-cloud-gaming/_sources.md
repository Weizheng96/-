# 证据索引 — 15-haima-cloud-gaming

## Phase 1 — react 粗筛 query（4 条，串行）
1. `海马云 云游戏 串流 弱网 FEC 冗余 抗丢包 自适应`
   - 命中信号：海马云自研 hmRTC 实时流媒体系统，传输优化含「FEC 纠错算法改进 + 特殊包冗余保护 + 指令流 QoS + 拥塞控制 + 带宽估计」；宣称 30%+ 丢包仍稳定。→ 相关，不剪枝。
2. `海马云 hmRTC 串流传输 FEC 冗余 网络状态 自适应 拥塞控制 专利`
   - 多为通用 CSDN/知乎 FEC 文章；海马侧仅「动态自适应丢包恢复 / 动态纠错 / 实时监控网络状况」营销级表述，无 F1-F5 颗粒度。
3. `海马云 蔚领时代 专利 冗余 数据传输 FEC 丢包 业务类型 调度 assignee`
   - WebSearch 未直接命中海马/蔚领自有专利，转 Google Patents assignee 检索。
4. `海马云 hmRTC 技术博客 自适应纠错 冗余包 网络状况 视频流 串流 抗丢包 实现`
   - 仍为营销页（8ms 延迟 / 0 丢包 / 30% 丢包稳定），无机制级披露。

## Phase 2 — 深抓（WebFetch + curl 兜底）
- WebFetch haimacloud.com 行业资讯页（2025-02-12）：仅营销指标，无 FEC/冗余/调度机制描述。
- 知乎 p/578937003 → HTTP 403；curl UA 兜底未取得可用正文（跳过）。
- Google Patents assignee SPA 页无服务端数据 → 改用 XHR API：
  - `https://patents.google.com/xhr/query?url=assignee=蔚领时代&country=CN` → gpatents-weiling.json
  - `https://patents.google.com/xhr/query?url=assignee=海马云&country=CN` → gpatents-haima.json
- 命中自有同主题专利并逐个 WebFetch：
  - CN117135148A（蔚领时代，2023-11-28）基于 WebRTC 音视频传输 — 含「选择一定比例数据作为 FEC 包」固定比例 FEC。
  - CN116137560A（海马云，2023-05-19）重传请求处理 / 数据发送端 — ARQ 条件冗余重传。
  - CN116112128A（海马云，2023-05-12）重传请求发送 / 数据接收端 — 接收端按 RTT 调重传间隔。

## 证据索引表

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2025-02-12 | 营销页 | https://www.haimacloud.com/zixun/hangye/1889615878090178561.html | hmRTC 30% 丢包稳定，无机制披露 |
| 2 | — | assignee 检索 | gpatents-weiling.json / gpatents-haima.json | Google Patents XHR 自有专利清单 |
| 3 | 2023-11-28 | 专利 | https://patents.google.com/patent/CN117135148A/zh | 蔚领时代 WebRTC 传输，固定比例 FEC |
| 4 | 2023-05-19 | 专利 | https://patents.google.com/patent/CN116137560A/zh | 海马云 发送端 ARQ 条件冗余重传 |
| 5 | 2023-05-12 | 专利 | https://patents.google.com/patent/CN116112128A/zh | 海马云 接收端按 RTT 调重传间隔 |
