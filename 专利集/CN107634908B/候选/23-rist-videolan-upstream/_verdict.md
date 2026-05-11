# Verdict — 23 RIST VideoLAN Upstream

> 候选：C3 RIST 协议 + librist (VideoLAN)
> 适用独立权：权 1 + 权 8
> 主体类型：T4 核心技术；R-OPENSOURCE；Priority P1

## F# 命中表

| F# | 综合 |
| --- | --- |
| F1 | **公开资料不足** — RIST 协议层之下无业务感知 |
| F2 | 字面命中（main profile NACK + FEC + recovery buffer adaptive ratecontrol） |
| F3 | 字面命中（`reorder_buffer_ms` + `reorder_timeout` 显式时延约束） |
| F4 | **公开资料不足**（librist FEC 主动适配公开度低）|
| F5 | 字面命中（librist 在多家 RIST 商业实现部署） |

字面 3/5 + 资料不足 2/5。

## 状态机三栏

| 权 | 原始 | 后置 | 最终 |
| --- | --- | --- | --- |
| 权 1 | **第 4 档**（边界 — 接近 3 档） | 1. 反向脑补禁令；3-7 同 01；与 SRT 不同，RIST 文档未明示"FEC purely static"——保留开放评估 | **第 4 档 公开资料不足（弱→强 边界）** |

## 关键证据 URL

- [code.videolan.org/rist/librist](https://code.videolan.org/rist/librist) — librist 主仓库
- [code.videolan.org/rist/librist/-/issues/194](https://code.videolan.org/rist/librist/-/issues/194) — Main Profile UDP 输出问题
- [code.videolan.org/rist/librist/-/releases/v0.2.0](https://code.videolan.org/rist/librist/-/releases/v0.2.0) — Release notes
- [github.com/videolan/vlc/blob/master/modules/access/rist.c](https://github.com/videolan/vlc/blob/master/modules/access/rist.c) — VLC RIST 模块
- [code.videolan.org/rist/librist/-/wikis/6.%20Appendix%20RIST%20Overview](https://code.videolan.org/rist/librist/-/wikis/6.%20Appendix%20RIST%20Overview)

## 总结一句话

librist 实现 NACK + reorder buffer + recovery buffer adaptive ratecontrol；FEC 主动适配公开度低；落第 4 档（公开资料不足弱→强边界）。
