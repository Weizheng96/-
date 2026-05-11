# Verdict — 16 Kuaishou Live

> 候选：T3-02；适用权 1；T3 直播；P1

## F# 命中表

| F# | 综合 |
| --- | --- |
| F1 | 等同命中（快手直播区分主视频 / 弹幕 / 互动） |
| F2 | **公开资料不足**（A2BR/LingXi 是播放端 ABR，不是发送端 FEC） |
| F3 | 等同命中（直播 deadline） |
| F4 | **公开资料不足** |
| F5 | 字面命中（快手 / Kwai 全球部署） |

字面 1/5 + 等同 2/5 + 资料不足 2/5。

## 状态机三栏

| 权 | 原始 | 后置 | 最终 |
| --- | --- | --- | --- |
| 权 1 | **第 3 档 公开资料不足（强）** | 等同 F1/F3 4 行成立；反向脑补禁令；3-7 同 01；建议法务深读快手 Klink 内部技术博客 | **第 3 档 公开资料不足（强）** |

## 关键证据 URL

- [godka.github.io/a2br-jsac23.pdf](https://godka.github.io/a2br-jsac23.pdf) — A2BR JSAC 2023（播放端 ABR）
- [dl.acm.org/doi/10.1145/3718958.3750526](https://dl.acm.org/doi/10.1145/3718958.3750526) — LingXi SIGCOMM 2025（播放端 ABR）
- [arxiv.org/html/2508.16454](https://arxiv.org/html/2508.16454) — LingXi arXiv
- [liveopen.kuaishou.com](https://liveopen.kuaishou.com/) — 快手直播开放平台

## 总结一句话

快手 SIGCOMM 2025 LingXi + A2BR JSAC 2023 主要为播放端 ABR；推流端 FEC 公开度低；落第 3 档（公开资料不足强）。
