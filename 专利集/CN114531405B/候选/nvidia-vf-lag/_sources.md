# 来源索引 — NVIDIA VF-LAG 调查

| # | URL | 类型 | 日期 | 关键引用摘要 |
|---|-----|------|------|------------|
| E1 | https://www.stackhpc.com/vflag-kayobe.html | 第三方技术博客 | 2021-03-30 | "VF-LAG only works for two ports on the same physical NIC. It cannot be used for LAGs created using multiple NICs." |
| E2 | https://www.spinics.net/lists/netdev/msg540007.html | 上游内核 PR | 2018-12-14 | "VF LAG ... different physical ports of the same Connect-X card" |
| E3 | https://github.com/Mellanox/bluefield-linux/blob/master/drivers/net/ethernet/mellanox/mlx5/core/lag.c | 内核源码 | (持续) | `MLX5_MAX_PORTS=2` 硬编码同卡上限 |
| E4 | https://www.spinics.net/lists/netdev/msg882440.html | 上游 netdev | 2023-02-14 | "MultiPort E-Switch ... all the vports and physical ports on the NIC" |
| E5 | https://docs.kernel.org/networking/multi-pf-netdev.html | kernel.org 文档 | (持续) | "combining multiple PFs of the same port ... up to two PFs (sockets)" |
| E6 | https://lwn.net/Articles/964644/ | LWN 文章 | 2024-03-05 | "leader/secondary ... All RX/TX traffic is steered through the primary" |
| E7 | https://lists.openwall.net/netdev/2024/12/18/285 | 上游 netdev | 2024-12-18 | "multi-host NICs provide each host with partial ports" (反向拓扑) |
| E8 | https://www.mail-archive.com/dev@dpdk.org/msg312437.html | DPDK 邮件列表 | 2025-03-11 | "NIC exports total 4 ports, and each host get 2 ports" (反向拓扑) |
| E9 | https://enterprise-support.nvidia.com/s/article/Configuring-VF-LAG-using-TC | NVIDIA 官方 KB | n/a | WebFetch 空响应，仅搜索摘要可用 |
| E10 | https://forums.developer.nvidia.com/t/how-to-bond-two-connectx-6-port/279595 | NVIDIA 官方论坛 | 2024-01-22 | 官方回复跨卡只指向 standard linux bonding |
| E11 | https://forums.developer.nvidia.com/t/vf-lag-offload/225798 | NVIDIA 官方论坛 | 2022-08 | hash 行为说明，语境仍单卡两口 |
| E12 | (SIGCOMM/NSDI 论文检索) | 学术论文 | n/a | **0 hits** — 未检索到对应论文 |
