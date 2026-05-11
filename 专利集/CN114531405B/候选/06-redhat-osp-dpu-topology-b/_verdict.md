# 候选：Red Hat OpenShift on DPU — Topology-B（理论多 DPU 拓扑）

## 候选标识
- candidate_slug: `06-redhat-osp-dpu-topology-b`
- 主体类型：A. vSwitch 软件方 + E. SDN 控制器
- 适用独立权：权 1, 11, 23, 36
- 命中场景：场景 5
- 拓扑变体：**topology-B** = 假设 OpenShift on DPU 在同节点装 ≥ 2 张 DPU（实际无此 reference architecture）

## §A 主流来源摘要

### §A.4 使用手册 / 技术文档（命中 — 反向证据）

| # | 源 | URL | 关键引文 |
| --- | --- | --- | --- |
| 1 | OpenShift 4.19 DPU Operator | https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking_operators/dpu-operator | "labeling all compute nodes assuming **each node has an attached DPU**" — labeling 模型为 1 host node ↔ 1 DPU node 的 1:1 映射 |
| 2 | Red Hat 2025-11-24 — Unifying multivendor DPUs | https://www.redhat.com/en/blog/unifying-multivendor-dpus-red-hat-openshift | "each one is equipped with a DPU from a different hardware vendor" → multivendor 是**跨节点**异构，**不是**同节点多 DPU |
| 3 | Red Hat Developer — Orchestrate offloaded NF on DPUs (2022) | https://developers.redhat.com/articles/2022/04/26/orchestrate-offloaded-network-functions-dpus-red-hat-openshift | "two x86 hosts with **a** BlueField-2 DPU PCIe card installed" — 单 DPU per host |

### §A.6 联合白皮书

NVIDIA RDG / AMD-Pensando RH OpenShift reference / Lenovo / Dell DPU on RH OpenShift —— 全部描述 1 DPU per host

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整记录 | 最终 verdict |
| --- | --- | --- | --- |
| 权 1 / 11 / 23 / 36 | **已排除（第 5 档）** | F1 整数限定 N ≥ 2 的拓扑外推禁令——Red Hat 公开 reference 全部描述 1 DPU per host，**不存在** ≥ 2 DPU per host 的官方架构；按 SKILL.md Step 5b §D 硬约束 3 "整数限定的拓扑外推禁令"——不能用 vendor 单实例文档推 N ≥ 2 多实例命中 | **已排除（架构层级不符 + R-2 拓扑外推禁令）** |

### 最终 verdict

**已排除（架构层级不符）**：Red Hat OpenShift on DPU 的全部公开 reference architecture 均为 1 DPU per host；多 DPU per host 形态在 Red Hat 公开材料中**0 命中**。F1 整数限定 N ≥ 2 不命中。

## 总结一句话

OpenShift on DPU = 1 DPU per host 单一架构（Red Hat 公开 reference 0 命中多 DPU），F1 整数限定不命中——**落第 5 档已排除**。
