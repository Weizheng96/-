# Verdict — 06 ByteDance VolcRTC

> 候选：T1-04 字节跳动 火山引擎 VolcRTC + 抖音内部栈 + 飞书音视频
> 适用独立权：权 1
> 主体类型：T1 RTC SDK；Priority P0

## F# 命中表

| F# | 字面 | 等同 | 综合 |
| --- | --- | --- | --- |
| F1 | VolcRTC 区分音视频 + 业务 SDK | — | **字面命中** |
| F2 | 火山引擎 veRoCE 含 loss recovery；FEC 字面文档薄 | — | **公开资料不足** |
| F3 | 抖音 / 飞书会议 deadline 隐含 | 等同 | **等同命中** |
| F4 | 抖音多次 SIGCOMM 投稿 | 等同 | **等同命中** |
| F5 | VolcRTC + 抖音直播 + 飞书全栈 | — | **字面命中** |

字面 2/5 + 等同 2/5 + 资料不足 1/5。

## 状态机三栏

| 权 | 原始 | 后置 | 最终 |
| --- | --- | --- | --- |
| 权 1 | **第 3 档 公开资料不足（强）** | 1. 等同三步法 F3/F4 4 行成立；2. 反向脑补禁令 F2；3-7 同 01；字节未上市无 SEC 披露 | **第 3 档 公开资料不足（强）** |

## 关键证据 URL

- [developer.volcengine.com/resource/7584346532149723178](https://developer.volcengine.com/resource/7584346532149723178) — 字节 veRoCE 传输协议
- [www.volcengine.com](https://www.volcengine.com/) — 火山引擎主站
- [developer.volcengine.com](https://developer.volcengine.com/) — 开发者社区
- [www.volcengine.com/docs](https://www.volcengine.com/docs)
- 抖音 SIGCOMM / NSDI 投稿（未单独命中具体 FEC 论文）

## 总结一句话

字节跳动 VolcRTC + veRoCE 公开技术博客提及 loss recovery；FEC 字面证据薄；落第 3 档（公开资料不足强）；建议法务通过字节 IPO 招股书 / IETF / 3GPP contribution / SIGCOMM 论文 author 归因检索升级。
