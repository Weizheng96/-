# Verdict — Google Cloud Andromeda + Snap user-space network stack

> 主体类型：S2 + S5；适用独立权：权 1 / 权 9；分级：**P1**

## 核心组织

**Google LLC（NASDAQ: GOOGL）** — Google Andromeda SDN 控制器 + Snap microkernel 网络栈

## F1-F5 命中表

| F# | 证据来源 | 命中类型 |
| --- | --- | --- |
| F1 | "Andromeda: Performance, Isolation, and Velocity at Scale in Cloud Network Virtualization"（NSDI 2018）+ "Snap: a Microkernel Approach to Host Networking"（SOSP 2019）— Andromeda 含 vSwitch 角色 | **字面命中** |
| F2 | Snap 论文：Snap engines 是多线程用户态包处理 worker | **字面命中** |
| F3 | Snap 论文：spreader / scheduler 监测 engine load 与 NUMA 位置 | **字面命中** |
| F4 | Snap 论文：spreader 自动重平衡（详见 §6）| **字面命中候选 — 等同命中** |
| F5 | Snap 论文：rebalances flows across engines | **字面命中候选 — 等同命中** |

## 时间线

- Andromeda 部署：2014（pre-grant — 实际上还在 priority 之前；但 NSDI 2018 论文 post-grant）
- Snap GA：2017+（论文 2019）→ post-grant 主导
- Snap 持续运营至 2026 → post-grant 长期 ship

## §A 19 类源穿透

- §A.2 学术论文：NSDI 2018 / SOSP 2019（强字面命中）
- §A.3 宣传：Google Cloud blog、Borg / Andromeda 公开演讲
- §A.18 国际同族：Google 在 SDN / packet processing 主分类有 US 专利墙

## 状态机三栏判定

| 独立权 | 状态机原始 | 后置调整 | 最终 |
| --- | --- | --- | --- |
| 权 1 | **第 2 档：确认侵权（中）** — F1-F5 全部命中（多数字面，部分等同）| 等同三步法对 F4/F5：同手段同功能同效果，本领域常识 — 通过 | **第 2 档：确认侵权（中）** |
| 权 9 | 同上 | 同上 | **第 2 档：确认侵权（中）** |

## 总结一句话

GCP Andromeda + Snap：NSDI 2018 / SOSP 2019 论文公开 spreader/scheduler 自动重平衡 engine 流量分配，F1-F5 全部命中（多数字面、部分等同），落第 2 档（确认侵权-中）。
