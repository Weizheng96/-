# 候选：Linux Kernel — bonding driver + mlx5 / ice / bnxt / nfp tc-flower offload

## 候选标识
- candidate_slug: `02-linux-kernel-bonding-mlx5-lag`
- 主体类型：A. vSwitch 软件方（上游） + B. NIC driver
- 适用独立权：权 1, 11, 23, 36
- R-OPENSOURCE 上游 P0

## §A 主流来源摘要

### §A.4 使用手册 / §A.7 上游归因（命中 — 真反向证据）

| # | 源 | URL | 引文 |
| --- | --- | --- | --- |
| 1 | Linux kernel bonding HOWTO | https://docs.kernel.org/networking/bonding.html | bonding.rst **0 命中** "tc-flower" / "hw-offload" / "hardware offload" / "nested bond" |
| 2 | StackHPC — VF-LAG | https://www.stackhpc.com/vflag-kayobe.html | 2024 — 决定性引文："VF-LAG only works for two ports on the same physical NIC. **It cannot be used for LAGs created using multiple NICs**" |
| 3 | Linux ice driver docs | https://docs.kernel.org/networking/device_drivers/ethernet/intel/ice.html | "**You cannot use SR-IOV when link aggregation (LAG)/bonding is active, and vice versa.** To enforce this, the driver checks for this mutual exclusion" |
| 4 | bnxt_tc.c (mainline) | https://github.com/torvalds/linux/blob/master/drivers/net/ethernet/broadcom/bnxt/bnxt_tc.c | tc-flower offload via VF representors in switchdev mode；无多卡同步流表 primitive |
| 5 | NVIDIA MLNX_EN docs v23.07 | https://docs.nvidia.com/nvidia-mlnx-en-documentation-v23-07.pdf | "Only LAGs with all HCA ports are supported" — VF-LAG bound to a single HCA |
| 6 | Red Hat KB 24528 | https://access.redhat.com/solutions/24528 | "Is it possible to configure bonding over bonded interface" — paywalled，但其作为反复 KB 问题的存在表明 mainline 不支持 nested bonding 拓扑 |

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整记录 | 最终 verdict |
| --- | --- | --- | --- |
| 权 1 / 11 / 23 / 36 | **已排除（第 5 档）** | mlx5 真反向 "VF-LAG cannot be used for LAGs created using multiple NICs"；ice 真反向 "SR-IOV mutually exclusive with LAG"；F3 不可达；F4 无原生 sync-N-flows primitive | **已排除（多 driver 真反向证据 + 架构层级不符）** |

### F# 投票汇总

- F1：单 mlx5 HCA 上 N=2 端口（不算多 NIC）；多 HCA bond 不支持 hw-offload → F1 不命中
- F2：bonding driver mode=802.3ad LACP 支持，但仅在软件层；hw-offload 路径不支持 LACP across cards → F2 部分命中
- F3：mlx5 VF-LAG 终结在 HCA 边界，无第二层映射 → 不命中
- F4：bonding 无原生 sync-N-flows primitive；shared-block ≠ duplicate → 不命中

### 最终 verdict

**已排除**：Linux kernel mainline 不实现"跨多 NIC 二层映射 + 同步 N 份相同流表"。mlx5 / ice / bnxt 主流 vendor driver 在 hw-offload 路径下显式排除多卡 LAG。

## 总结一句话

Linux kernel mainline 不实现 F3+F4；mlx5 VF-LAG 字面"intra-HCA only"、ice "SR-IOV ⊥ LAG"——多重真反向，**落第 5 档已排除**。
