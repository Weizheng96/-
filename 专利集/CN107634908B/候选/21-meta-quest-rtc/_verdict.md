# Verdict — 21 Meta Quest Air Link + Messenger Call

> 候选：T1-09；适用权 1 + 权 8（Meta Quest 头显设备 OEM）；T1 + T5；P1

## F# 命中表

| F# | 综合 |
| --- | --- |
| F1 | 等同命中（mvfst QUIC streams 区分业务） |
| F2 | **公开资料不足**（mvfst 文档薄于 FEC） |
| F3 | 等同命中（mvfst loss recovery + flexible congestion control） |
| F4 | 等同命中（QUIC packet pacing） |
| F5 | 字面命中（Quest Air Link / WhatsApp / Messenger 全球部署） |

字面 1/5 + 等同 3/5 + 资料不足 1/5。

## 状态机三栏

| 权 | 原始 | 后置 | 最终 |
| --- | --- | --- | --- |
| 权 1 | **第 4 档** | 1. 等同 4 行成立；2. 反向脑补 F2；3-7 同 01；建议法务通过 mvfst issue tracker 详查 | **第 4 档 公开资料不足（弱）** |
| 权 8 | **第 4 档**（Quest 头显设备 OEM） | 同上 | **第 4 档** |

## 关键证据 URL

- [engineering.fb.com/2020/10/21/networking-traffic/how-facebook-is-bringing-quic-to-billions/](https://engineering.fb.com/2020/10/21/networking-traffic/how-facebook-is-bringing-quic-to-billions/) — **mvfst QUIC + loss recovery**
- [engineering.fb.com/2022/07/06/networking-traffic/watch-metas-engineers-discuss-quic-and-tcp-innovations-for-our-network/](https://engineering.fb.com/2022/07/06/networking-traffic/watch-metas-engineers-discuss-quic-and-tcp-innovations-for-our-network/)
- [engineering.fb.com/2023/01/27/networking-traffic/optimizing-large-scale-networks-meta-engineers/](https://engineering.fb.com/2023/01/27/networking-traffic/optimizing-large-scale-networks-meta-engineers/)
- github.com/facebookincubator/mvfst — mvfst 主仓库

## 总结一句话

Meta mvfst QUIC loss recovery 强但 FEC 字面证据薄；Quest Air Link 闭源；落第 4 档（公开资料不足弱）；建议法务通过 mvfst code search + Meta IPR statement 升级。
