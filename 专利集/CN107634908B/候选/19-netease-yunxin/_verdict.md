# Verdict — 19 NetEase Yunxin NeRTC

> 候选：T1-05 网易云信 NeRTC
> 适用独立权：权 1
> 主体类型：T1 RTC SDK；Priority P0

## F# 命中表

| F# | 字面 | 等同 | 综合 |
| --- | --- | --- | --- |
| F1 | NeRTC 区分音视频流；自研 NEVC 编码业务化 | — | **字面命中** |
| F2 | "80% 丢包仍支持正常通话" 暗示动态 FEC | — | **字面命中** |
| F3 | < 200ms 端到端 deadline + 1000ms 抖动抗 | 等同 deadline-aware | **等同命中** |
| F4 | NeRTC 2.0 整体架构升级 — 调度细节公开较少 | 等同 | **等同命中** |
| F5 | NeRTC 服务器 + SDK 全平台部署 | — | **字面命中** |

字面 3/5 + 等同 2/5。

## 状态机三栏

| 权 | 原始 | 后置 | 最终 |
| --- | --- | --- | --- |
| 权 1 | 第 2 档 | 1. 等同三步法 F3/F4 4 行成立；2-7 同 01；net ease 与华为无 patent grant 关系 | **第 2 档 确认侵权（中）** |

## 关键证据 URL

- [doc.yunxin.163.com/nertc/concept/zY0MjQ5NjE](https://doc.yunxin.163.com/nertc/concept/zY0MjQ5NjE?platform=client) — 产品介绍 + 性能指标
- [doc.yunxin.163.com/nertc/outdated_articles/DIyNDc1NzM](https://doc.yunxin.163.com/nertc/outdated_articles/DIyNDc1NzM?platform=client) — 性能指标
- [doc.yunxin.163.com/nertc/getting-started](https://doc.yunxin.163.com/nertc/getting-started) — 开发者中心
- [doc.yunxin.163.com/nertc/concept/zU5NzI3NTM](https://doc.yunxin.163.com/nertc/concept/zU5NzI3NTM?platform=client) — 更新日志
- [github.com/netease-im](https://github.com/netease-im) — 网易云信开源代码

## 总结一句话

网易云信 NeRTC 公开宣传 80% 抗丢包 + 1000ms 抖动适应 + 自研 NEVC，技术指标与 CN107634908B 全链路要求高度吻合；落第 2 档（确认侵权中）。
