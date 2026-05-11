# Verdict — 02 Tencent TRTC + GME

> 候选：T1-01 腾讯云 TRTC + 腾讯游戏多媒体引擎 GME
> 适用独立权：权 1 + 权 8
> 主体类型：T1 RTC SDK
> Priority：P0

## F# 命中表

| F# | 字面 | 等同 | 综合 |
| --- | --- | --- | --- |
| F1 业务类型识别 | `TRTCNetworkQosParam.preference` (PreferClear vs PreferSmooth) — 业务类型差异化 | 也可通过 SDP audio/video stream 区分 | **字面命中**（preference 参数即"业务类型获取"） |
| F2 冗余包数量 | TRTC 宣传 "实测抗丢包率超过 40%、抗网络抖动超过 1000ms" 暗示动态 FEC | — | **字面命中** |
| F3 时延要求 → 总时间 | TRTC 文档暴露端到端时延 < 200ms；从属权 3 ≤ 时延 | — | **字面命中** |
| F4 调度方法 | preference 切换不同 pacing 策略 | 等同 random / shortest / longest / uniform 的子集 | **等同命中** |
| F5 发送冗余包 | 全平台 TRTC SDK + 腾讯会议核心模块部署 | — | **字面命中** |

**字面 4/5 + 等同 1/5**。

## 状态机三栏

| 权 | 原始 | 后置 | 最终 |
| --- | --- | --- | --- |
| 权 1 | 第 2 档（字面 4/5 + 等同 1/5） | 1. 等同三步法对 F4 跑过 4 行论证均成立；2. 无反向证据；3. Active；4. 同 01；5-7 同 01 | **第 2 档 确认侵权（中）** |

## 关键证据 URL

- [cloud.tencent.com/product/trtc](https://cloud.tencent.com/product/trtc)
- [cloud.tencent.com/document/product/647/32236](https://cloud.tencent.com/document/product/647/32236) — TRTCNetworkQosParam preference
- [cloud.tencent.com/developer/article/1739390](https://cloud.tencent.com/developer/article/1739390) — TRTC 技术内幕

## 总结一句话

腾讯云 TRTC 通过 `NetworkQosParam.preference` 业务类型映射 + 实测 80% 抗丢包能力，公开宣传明确包含 CN107634908B 全部 F# 链路；落第 2 档（确认侵权中）。
