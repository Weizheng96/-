# 证据索引 — 16-tencent-start-cloud-gaming

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2024 | 论文 | https://zilimeng.com/papers/hairpin-nsdi24.pdf (本地 hairpin-nsdi24.pdf / .txt) | Hairpin (NSDI'24)，作者含 Tencent；Eq.2 β(α,B,RTT,t)=k·(RTT/t)·β₀(α,B) 按丢包率 α+码率 B+RTT+剩余时间 t 自适应冗余率；MDP 联合优化重传与冗余，受 deadline 约束；START 云游戏生产部署评测（降带宽 40%、降 deadline miss 32%）|
| 2 | 2024-05-13 | 官方文 | https://ur.tencent.com/article/1481 | 腾讯 START 团队三项成果入选 NSDI 2024；Hairpin 实时监测 RTT+丢包动态调 FEC，初传 vs 重传不同冗余策略；Pudica/AUGUR 已生产大规模部署 |
| 3 | 2025 | 论文 | https://zilimeng.com/papers/tooth-nsdi25.pdf (本地 tooth-nsdi25.pdf / .txt) | Tooth (NSDI'25) "Fine-Grained FEC in Cloud Gaming Streaming"；按 application-layer 帧长(包数)+网络丢包分布 → per-frame 冗余率；厂商匿名 "Company W"（非明示 START，仅同领域佐证）|

## Phase 1 — react 粗筛 query 留痕
- query 1：`腾讯 START 云游戏 先锋 串流 弱网 FEC 冗余 抗丢包` → 命中 NSDI 2024 三项成果（Pudica/AUGUR/Hairpin），强相关。
- query 2：`腾讯 START Hairpin NSDI 2024 云游戏 FEC 冗余 网络状态 自适应 重传` → 命中官方文 + Hairpin 用 MDP 建模、实时调 FEC，强相关。
- query 3：`Hairpin NSDI 2024 cloud gaming FEC redundancy retransmission Markov decision process paper Tencent` → 命中 Hairpin/Tooth 论文 PDF，强相关。
- 未触发早剪枝（时间窗合规 2024 > 2021-06-08）。

## Phase 2 — react 深抓
- WebFetch 两 PDF 被快模型判为二进制无法解码 → curl 落盘 + pdfplumber 提取 .txt（兜底成功）。
- WebFetch ur.tencent.com/article/1481（2024-05-13）核实生产部署。

## 同源声明
- Hairpin 为 START 云游戏团队专项边缘交互式视频流传输栈，**非** GME/TRTC 通用 RTC 栈，与候选 03/06 无直接同源，无需对齐其档位。
