# Verdict — 07 ZegoCloud RTC

> 候选：T1-03 即构 ZegoCloud + ZEGO Express SDK + ZEGO Live SDK
> 适用独立权：权 1
> 主体类型：T1 RTC SDK；Priority P1

## F# 命中表

| F# | 字面 | 等同 | 综合 |
| --- | --- | --- | --- |
| F1 | ZegoCloud SDK 区分场景化业务 | — | **字面命中** |
| F2 | 70% 丢包流畅 + 79ms 延迟 — 暗示动态 FEC | — | **字面命中** |
| F3 | 79ms 延迟 deadline | 等同 | **等同命中** |
| F4 | 高可用架构博客提及动态集群调度 | 等同 | **等同命中** |
| F5 | 全球 500+ 边缘节点部署 | — | **字面命中** |

字面 3/5 + 等同 2/5。

## 状态机三栏

| 权 | 原始 | 后置 | 最终 |
| --- | --- | --- | --- |
| 权 1 | **第 3 档 公开资料不足（强）** | 1. 等同三步法 F3/F4 4 行成立；2. 反向脑补禁令；3-7 同 01；ZegoCloud 未上市无 SEC 披露 | **第 3 档 公开资料不足（强）** |

## 关键证据 URL

- [zego.im](https://www.zego.im/) — 79ms 延迟 / 70% 丢包流畅
- [cnblogs.com/zegoinfo/p/17773031.html](https://www.cnblogs.com/zegoinfo/p/17773031.html) — 高可用架构博客
- [ext.dcloud.net.cn/plugin?id=3617](https://ext.dcloud.net.cn/plugin?id=3617)
- [toolify.ai/zh/tool/zegocloud](https://www.toolify.ai/zh/tool/zegocloud)

## 总结一句话

即构 ZegoCloud 公开 70% 抗丢包 + 79ms 延迟 + 动态调度，技术指标与 CN107634908B 高度吻合但 FEC 字面披露薄；落第 3 档（公开资料不足强）。
