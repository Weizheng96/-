# Verdict — 25 YouTube Live + Twitch + Meta Live Family

> 候选：T3-05；适用权 1；T3 直播；P2

## F# 命中表

| F# | 综合 |
| --- | --- |
| F1 | **公开资料不足** |
| F2 | **公开资料不足**（RTMP/HLS ingest 主流，FEC 不普及）|
| F3 | 等同命中（HLS-LL deadline） |
| F4 | **公开资料不足** |
| F5 | 字面命中（YouTube / Twitch / Meta Live 全球部署） |

字面 1/5 + 等同 1/5 + 资料不足 3/5。

## 状态机三栏

| 权 | 原始 | 后置 | 最终 |
| --- | --- | --- | --- |
| 权 1 | **第 4 档** | RTMP ingest 主流不含发送端 FEC；HLS-LL 命中度低；3-7 同 01 | **第 4 档 公开资料不足（弱）** |

## 关键证据 URL

- YouTube Live RTMP ingest docs
- Twitch IVS Amazon docs
- Facebook Live / Instagram Live RTMP ingest

## 总结一句话

海外 UGC 直播头部主流是 RTMP / HLS ingest，FEC 不普及；落第 4 档（公开资料不足弱）。
