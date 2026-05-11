# Verdict — 08 Zoom RTC

> 候选：T1-06 Zoom Video SDK + Zoom Meetings
> 适用独立权：权 1
> 主体类型：T1 RTC SDK；Priority P0

## F# 命中表

| F# | 字面 | 等同 | 综合 |
| --- | --- | --- | --- |
| F1 | Zoom 区分 audio / video / screen-share — adaptive bitrate / codec layers | — | **字面命中** |
| F2 | "Zoom may add recovery data every so many packets; if one packet drops, the app can repair it using the FEC data" + "adaptive bitrate" | — | **字面命中** |
| F3 | 实时音视频通话 deadline 隐含 | 等同 deadline-aware | **等同命中** |
| F4 | "FEC adds recovery data every so many packets" — 周期性发 | 等同 uniform 调度 | **等同命中** |
| F5 | Zoom 全平台部署 | — | **字面命中** |

字面 3/5 + 等同 2/5。

## 状态机三栏

| 权 | 原始 | 后置 | 最终 |
| --- | --- | --- | --- |
| 权 1 | 第 2 档 | 1. 等同三步法 4 行成立；2-7 同 01 | **第 2 档 确认侵权（中）** |

## 关键证据 URL

- [library.zoom.com/admin-corner/architecture-and-design/zoom-architected-for-reliability](https://library.zoom.com/admin-corner/architecture-and-design/zoom-architected-for-reliability) — **FEC 周期性发 + adaptive bitrate**
- [cspages.ucalgary.ca/~cwill/papers/2022/Albert-PAM2022.pdf](https://cspages.ucalgary.ca/~cwill/papers/2022/Albert-PAM2022.pdf) — PAM 2022 学术分析
- [ennanzhai.github.io/pub/xron-sigcomm23.pdf](https://ennanzhai.github.io/pub/xron-sigcomm23.pdf) — SIGCOMM 2023 XRON
- [library.zoom.com/admin-corner/network-management/quality-of-service-and-network-best-practices-explainer/configuring-network-components-for-zoom](https://library.zoom.com/admin-corner/network-management/quality-of-service-and-network-best-practices-explainer/configuring-network-components-for-zoom)
- [sciencedirect.com/.../S1389128623003638](https://www.sciencedirect.com/science/article/abs/pii/S1389128623003638) — Adaptive Frame Delivery

## 总结一句话

Zoom 官方 Tech Library 明示"FEC 周期性发冗余 + adaptive bitrate + codec layers"，完整覆盖 F2-F5；落第 2 档（确认侵权中）。
