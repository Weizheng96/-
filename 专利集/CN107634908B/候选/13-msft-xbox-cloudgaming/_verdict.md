# Verdict — 13 Microsoft Xbox Cloud Gaming (xCloud)

> 候选：T2-03；适用权 1；T2 云游戏；P0（间接 — 同集团 Teams 已证 FEC）

## F# 命中表

| F# | 综合 |
| --- | --- |
| F1 | 等同命中（xCloud 区分 game stream / 控制信令） |
| F2 | **公开资料不足**（xCloud 闭源，但 Azure 内 Teams 已有 FEC 实现 — 间接） |
| F3 | 等同命中（云游戏 deadline） |
| F4 | **公开资料不足** |
| F5 | 字面命中（多端部署） |

字面 1/5 + 等同 2/5 + 资料不足 2/5。

## 状态机三栏

| 权 | 原始 | 后置 | 最终 |
| --- | --- | --- | --- |
| 权 1 | **第 3 档 公开资料不足（强）** | 1. 等同三步法 F1/F3 4 行成立；2. 同集团 Teams FEC 实现作间接证据但不直接传到 xCloud（禁止继承推断）；3-7 同 01 | **第 3 档 公开资料不足（强）** |

## 关键证据 URL

- Xbox Cloud Gaming 产品页
- Azure PlayFab Multiplayer Server docs
- 同集团候选 10 Teams 已证 FEC 动态启用（间接信号）

## 总结一句话

xCloud 网络栈较闭源；同集团 Teams 已确认有动态 FEC（候选 10）— 间接信号；落第 3 档（公开资料不足强）；建议法务通过 Azure 客户合作披露或 MS SEC 10-K 升级。
