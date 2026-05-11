# 候选：NVIDIA VF-LAG — Topology-B（多 ConnectX/BlueField 跨卡 LAG）

## 候选标识
- candidate_slug: `04-nvidia-vf-lag-topology-b`
- 主体类型：B. SmartNIC / DPU 硬件方（核心技术候选 — R-6 归并下游集成方为应用案例）
- 适用独立权：权 23, 33, 35, 36
- 拓扑变体：**topology-B** = 多 ConnectX/BlueField 跨卡 LAG（N ≥ 2 NIC）—— 真正命中候选

## §A 主流来源摘要

### §A.4 / §A.7（命中 — 显式真反向证据）

| # | 源 | URL | 引文 |
| --- | --- | --- | --- |
| 1 | StackHPC VF-LAG | https://www.stackhpc.com/vflag-kayobe.html | **决定性引文**："VF-LAG only works for two ports on the same physical NIC. **It cannot be used for LAGs created using multiple NICs**" |
| 2 | mlx5 lag.c | https://github.com/Mellanox/bluefield-linux/blob/master/drivers/net/ethernet/mellanox/mlx5/core/lag.c | `MLX5_MAX_PORTS=2` 硬编码限制 |
| 3 | NVIDIA Forum 跨卡 bond 问答 | https://forums.developer.nvidia.com/t/how-to-bond-two-connectx-6-port/279595 | 2024-01-22 — 官方回复"use standard Linux method"——**无 hardware offload** |
| 4 | DPDK multi-host lag probe patch | https://www.mail-archive.com/dev@dpdk.org/msg312437.html | 2025-03-11 — multi-host LAG = 一张 NIC 物理上挂多 host（partial ports per host），**与本专利 F1 拓扑相反** |
| 5 | LWN mlx5 socket direct (Multi-PF) | https://lwn.net/Articles/964644/ | 2024-03 — 同一 NIC 插两个 PCIe 槽做 cross-NUMA；leader-secondary 单路径转发——**与 F4 "同时下发 N 份" 完全不同** |

### §A.2 学术阵地

**0 命中** SIGCOMM / NSDI 论文实现细节披露 NVIDIA 跨卡 LAG hardware offload + sync flow

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整记录 | 最终 verdict |
| --- | --- | --- | --- |
| 权 23 / 33 / 35 / 36 | **已排除（第 5 档）** | F1 真反向 "VF-LAG cannot be used for LAGs created using multiple NICs"；F3/F4 真反向（mlx5 LAG 终结于 HCA 边界）；§5.0 豁免：满足 (a) | **已排除（topology-B — F1/F3 真反向证据，跨卡 LAG hardware offload 在 NVIDIA 公开栈中不存在）** |

### 最终 verdict

**已排除**：NVIDIA 在公开 DOCA / mlx5 驱动栈中**显式排除**跨卡 LAG hardware offload；2024-2025 multi-host LAG / Socket Direct 是不同概念（一张 NIC 跨主机 / 单 NIC 跨 PCIe 槽）。

## 总结一句话

NVIDIA VF-LAG 显式 intra-HCA-only（StackHPC verbatim "cannot be used for LAGs created using multiple NICs"）——topology-B F1/F3 真反向，**落第 5 档已排除**。
