# 候选：NVIDIA VF-LAG — Topology-A（单 ConnectX/BlueField 多端口）

## 候选标识
- candidate_slug: `03-nvidia-vf-lag-topology-a`
- 主体类型：B. SmartNIC / DPU 硬件方
- 适用独立权：权 35（芯片）+ 权 23/36（驱动 / DOCA）
- 拓扑变体：**topology-A** = 单 BlueField/ConnectX 卡的多端口 LAG（N=1 NIC）

## §A 主流来源摘要

### §A.4 / §A.7（命中 — 反向证据）

| # | 源 | URL | 引文 |
| --- | --- | --- | --- |
| 1 | StackHPC VF-LAG | https://www.stackhpc.com/vflag-kayobe.html | "VF-LAG only works for two ports on the same physical NIC" |
| 2 | mlx5 VF-LAG netdev PR | https://www.spinics.net/lists/netdev/msg540007.html | 2018-12-14 — "VFs associated with different physical ports of the same Connect-X card" |
| 3 | mlx5 lag.c | https://github.com/Mellanox/bluefield-linux/blob/master/drivers/net/ethernet/mellanox/mlx5/core/lag.c | 源码：`MLX5_MAX_PORTS=2` 硬编码；only same-card PF pair checks |
| 4 | NVIDIA Forum | https://forums.developer.nvidia.com/t/how-to-bond-two-connectx-6-port/279595 | 2024-01-22 — 跨两张 ConnectX 卡 bond 的官方答复："use standard Linux method"——**无 hardware offload** |
| 5 | NVIDIA Configuring VF LAG using TC | https://enterprise-support.nvidia.com/s/article/Configuring-VF-LAG-using-TC | VF LAG 配置全部基于单 HCA 的双口 |

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整记录 | 最终 verdict |
| --- | --- | --- | --- |
| 权 23 / 35 / 36 | **已排除（第 5 档）** | F1 真反向（topology-A 是 N=1 NIC 单卡）；R-2 拓扑外推禁令——不能从单卡推 N ≥ 2 多卡命中 | **已排除（topology-A — F1 不满足整数限定 N ≥ 2）** |

### F# 投票汇总

- F1：单卡多端口 → N=1 NIC，**字面不命中** F1
- F2：LACP 支持（mlx5 802.3ad）→ 字面命中（在单卡内）
- F3：单卡内 LAG 是单层，**不构成 N→1 二层映射**
- F4：单卡 hardware mirror flow 在卡内端口间，与"跨 N 张 NIC sync"语义不同

### 最终 verdict

**已排除（topology-A）**：单卡多端口 LAG 是 N=1 NIC，F1 整数限定 N ≥ 2 不命中；按 R-2 拓扑外推禁令不允许推到 topology-B。

## 总结一句话

NVIDIA VF-LAG topology-A 是单卡多端口（N=1 NIC），F1 整数限定不命中——**落第 5 档已排除**。
