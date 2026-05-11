# Verdict — 03 Agora SD-RTN

> 候选：T1-02 声网 Agora + SD-RTN
> 适用独立权：权 1
> 主体类型：T1 RTC SDK；Priority P0

## F# 命中表

| F# | 字面 | 等同 | 综合 |
| --- | --- | --- | --- |
| F1 | Loss Detection Analyzer ML 分类丢包 (congestion/random/other) | 业务类型 ≈ loss category 等同 | **字面命中**（ML 分类即权 5/12 AI 算法路径） |
| F2 | "Congestion Control and Bandwidth Estimation intelligently calculates transmission parameters" + ALT + FEC | — | **字面命中** |
| F3 | 20% 丢包下保流畅 — 暗示 deadline budget | 等同 deadline-aware | **等同命中** |
| F4 | ALT 路径动态切换 + FEC 速率自适应 | 等同调度方法 | **字面命中** |
| F5 | SD-RTN 边缘节点全球部署 | — | **字面命中** |

字面 4/5 + 等同 1/5。

## 状态机三栏

| 权 | 原始 | 后置 | 最终 |
| --- | --- | --- | --- |
| 权 1 | 第 2 档 | 1. 等同三步法 F3 4 行成立；2-7 同 01 | **第 2 档 确认侵权（中）** |

## 关键证据 URL

- [hello.agora.io/.../SD-RTN-Delivers-RealTime-Internet-Advantages.pdf](https://hello.agora.io/rs/096-LBH-766/images/Agora_WP_SD-RTN-Delivers-RealTime-Internet-Advantages.pdf)
- [agora.io/en/the-agora-platform-advantage/](https://www.agora.io/en/the-agora-platform-advantage/)
- [agora.io/en/blog/optimizing-the-live-video-user-experience/](https://www.agora.io/en/blog/optimizing-the-live-video-user-experience/)
- [hello.agora.io/.../Agora-Network-Performance-Whitepaper.pdf](https://hello.agora.io/rs/096-LBH-766/images/Agora-Network-Performance-Whitepaper.pdf)

## 总结一句话

声网 SD-RTN 通过 Loss Detection Analyzer ML + ALT + FEC 自适应实现 F1-F5 完整链路，公开宣传明确支撑命中；落第 2 档（确认侵权中）。
