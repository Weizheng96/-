# 候选 #20 VMware vSphere 8 U3 / NSX / DSE — 合议判定

**主体类型**：软件发布方
**适用独立权**：权 36（计算机存储介质）
**判定**：**已排除**

---

## 子 agent 投票表（F1-F6 × 5 文档）

| 特征 | A (DSE TechDocs) | B (8U3 公告) | C (8U3 详细 blog) | D (LACP TechDocs) | E (NVIDIA-VMware 白皮书) | 合议 |
| --- | --- | --- | --- | --- | --- | --- |
| F1 vSwitch | 是 | 间接 | 是 | 是 | 是 | **是** |
| F2 N≥2 物理 NIC | 否 | 弱命中 | 命中（4 vmnic 同 vDS）| 是（vDS 跨多 NIC）| **否，强反向**（"only one DPU per host"）| **否** |
| F3 NIC 内部 LACP 聚合 | 否 | 否 | 否 | **否，强反向**（LACP 在 ESXi kernel host proxy switch，非 NIC 内部） | 否 | **否，强反向证据** |
| F4 多 NIC → 同一目标端口 | 否 | **否，反向**（"full isolation"） | 部分 / 未明 | 部分（vDS LAG 抽象，不是单主机内 NIC 聚合） | 否 | **否** |
| F5 同表多卡分发 | 否 | **否，反向**（HA = active/standby）| **否，反向**（"no failover" / active/standby）| 部分（LACP hashing，非"同表多卡"） | 否 | **否，多份反向证据** |
| F6 NIC 硬件 offload | 是 | 是 | 是 | 否（仅讲 LACP 软件层） | **强命中** | **是** |

## 强反向证据汇总

1. **NVIDIA-VMware 联合白皮书（E）原文 p14**：*"In the vSphere 8 versions studied in this paper, **only one DPU is supported per ESXi Host**"*（2023-08 发布）—— **直接否定 F2**。
2. **vSphere 8 U3 公告（B）原文 L458**：*"**dual independent DPUs offer full isolation** and double the offload capacity per host"*；以及 *"Active/Standby HA"* —— 两种 dual-DPU 配置都对应专利明确排除的相邻方案。
3. **vSphere 8 U3 详细 blog（C）原文 L628**：*"DPU-1 is attached to vmnic0 and vmnic1 ... DPU-2 is attached to vmnic2 and vmnic3"*，且 *"no failover"* in independent 模式 / active-standby in HA 模式。**两种模式都不是 F5 的"同时下发到多 DPU"**。
4. **vSphere LACP TechDocs（D）**：*"a LAG object is also created on the **proxy switch of every host**"* —— LACP 在 ESXi kernel 软件层（host proxy switch）实现，**不在 NIC / DPU 内部**，**直接否定 F3** "NIC 内部物理端口基于 LACP 聚合"。
5. **DSE TechDocs（A）**：通篇用单数"DPU"，未提双卡协同语义，进一步弱化跨 NIC 同表分发可能。

## 落入专利明确排除的相邻方案
参照专利"明显不在保护范围内的相邻方案"清单：
- **第 2 项 active/standby 主备方案** —— 命中（vSphere 8 U3 dual-DPU HA 模式恰好是这个）
- **第 6 项 多 NIC 各自独立维护流表** —— 命中（vSphere 8 U3 independent 模式 = "full isolation"）

VMware 双 DPU 方案**同时落入两条相邻排除方案**——这是非常清晰的反向证据。

## 最终结论
**VMware vSphere 8 U3 / NSX / DSE 在权 36 已排除**：
- F2 反向（NVIDIA-VMware 白皮书明文单 DPU per host；vSphere 8 U3 dual-DPU 也是各自独立 vDS）
- F3 反向（vDS LACP 在 ESXi kernel，不在 NIC 内部）
- F4 / F5 反向（active/standby HA 或 full isolation independent，**都属于专利明确排除的相邻方案**）

ESXi/NSX 软件二进制层**不含"多 DPU 同表分发"代码路径**，权 36 字面 + 等同均不命中。

## 升级前提
若 vSphere 9.0 或 8 U4+ 引入 active/active dual-DPU 同表分发模式，需重新评估。截至 2026-04-27 检索日，VMware/Broadcom 路线图无该方向公开声明。
