# Verdict — 腾讯云 TGW + F-Stack + 银杉 DPU

> 主体类型：S2 + S5；适用独立权：权 1 / 权 9；分级：**P1**

## 核心组织
**腾讯控股（HKEX: 0700）**：腾讯云、F-Stack 上游开源（GitHub F-Stack/f-stack）

## F1-F5 命中表
| F# | 证据 | 命中 |
| --- | --- | --- |
| F1 | F-Stack 是用户态 TCP/IP stack（非传统 vSwitch），但腾讯云 TGW 网关含 vSwitch 性质的转发；银杉 DPU 卸载 vSwitch | **字面命中候选**（TGW）/ **作用域限定**（F-Stack 不直接是 vSwitch，等同度低） |
| F2 | F-Stack 多线程 worker（开源代码可证） | **字面命中**（在 F-Stack 范围内） |
| F3-F5 | 银杉 DPU 闭源；F-Stack 上游 worker rebalance 机制有限（手动） | **公开资料不足** |

## 时间线
- F-Stack 开源：2017+ → 临时保护期/post-grant；银杉 DPU GA：2023+ → post-grant

## 状态机三栏
| 权 | 原始 | 调整 | 最终 |
|---|---|---|---|
| 权 1 / 9 | **第 4 档：公开资料不足（弱候选）** — F-Stack 不是严格 vSwitch；TGW 闭源 | F1 等同命中存疑；F4-F5 公开资料不足 | 第 4 档 |

## 总结一句话
腾讯 TGW + F-Stack + 银杉 DPU：F-Stack 用户态 stack 不严格落入 vSwitch 范围，F1 等同存疑；TGW + 银杉闭源致 F3-F5 公开资料不足，落第 4 档（公开资料不足弱候选）。
