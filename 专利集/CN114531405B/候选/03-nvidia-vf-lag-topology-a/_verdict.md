# Verdict — NVIDIA SR-IOV VF-LAG 拓扑 T-A：单 NIC 双 PF（vendor 默认部署）

> 主体类型：S3 + S4；适用独立权：权 1 / 11 / 23 / 33 / 34 / 35 / 36；分级：**P0**

## 1. 核心组织
NVIDIA Corporation（NASDAQ: NVDA）+ Mellanox Technologies 子公司

## 2. F1-F5 命中表（T-A 拓扑：单卡 dual-PF）

| F# | 证据 | 命中 |
|---|---|---|
| F1（M VM + N ≥ 2 NIC）| NVIDIA VF-LAG QSG："A VM can be attached with single VF backed up by LAG implemented on the **NIC level**" + "reflected to all VFs of the **same NIC**" — 描述明确是**同一张 NIC 内部**两 PF 绑定 | **不命中**（N=1 单卡部署不满足专利 N ≥ 2 整数限定）|
| F2 | "supported Bond modes are: Active-Backup, XOR and **LACP**" — LACP 模式可用 | 字面命中（卡内 LACP）|
| F3（N 端口标识 → 第一端口）| 单卡场景下 N=1，"跨卡映射"概念不存在 | **不命中** |
| F4 | OVS 标准 miss-to-upcall | 字面命中（与拓扑无关）|
| F5（同时下发到所有 N 网卡）| 单卡场景下"所有 N 网卡"= 1 卡 | 字面命中但语义打折——专利防 SPoF 动机不满足 |

## 3. 状态机三栏判定

| 独立权 | 原始 | 后置调整 | 最终 |
|---|---|---|---|
| 权 1 / 11 / 23 / 33 / 34 / 35 / 36 | **第 5 档：已排除（架构层级不符 / N=1 不满足 F1）** | 已排除门槛硬条件 (d) 架构层级不符；其他调整未触发 | **第 5 档：已排除（N=1，单 NIC 不在专利两层多卡 HA 保护范围）** |

## 4. §A 穿透
- §A.4 NVIDIA VF-LAG QSG（已抓取）— 明示 single-NIC dual-PF
- §A.10 WebSearch："NVIDIA VF-LAG multi-NIC" — top-10 结果均指向单 NIC，**0 命中**真实多 NIC 拓扑

## 5. 总结一句话
NVIDIA VF-LAG 单 NIC 双 PF 拓扑（vendor 公开文档默认描述）= N=1，不满足专利 F1 整数限定 N ≥ 2；落第 5 档（已排除——架构层级不符）。
