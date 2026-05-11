# 候选：Intel IPU E2000 (Mount Evans) / E2100 + Google Cloud Andromeda + IPDK

## 候选标识
- candidate_slug: `20-intel-ipu-e2000`
- 主体类型：B. 芯片厂 + C. CSP（Google）+ A. 上游软件（IPDK）
- 适用独立权：权 35 + 权 1/11/23/36

## §A 主流来源摘要

### §A.2 / §A.4

| # | 源 | URL | 引文 |
| --- | --- | --- | --- |
| 1 | IPDK Infrastructure Networking | https://ipdk.io/documentation/Recipes/InfrastructureNetworking/ | "IPDK includes support for **LAG LACP (802.3ad) mode** in Linux Networking capable of active-active LACP" |
| 2 | IPDK Mount Evans target | https://ipdk.io/documentation/Targets/MountEvansIPU/ | E2000 IPU 目标平台 |
| 3 | Google Cloud Andromeda 2.2 blog | https://cloud.google.com/blog/products/networking/google-cloud-networking-in-depth-how-andromeda-2-2-enables-high-throughput-vms | 2023-10 后 — encryption offload + DMA engines；**0 多 IPU sync 描述** |
| 4 | Intel/Google IPU E2000 collab | https://medium.com/intel-tech/intel-ipu-e2000-a-collaborative-achievement-with-google-cloud-eb1dda8c0177 | E2000 与 Google 联合开发 |
| 5 | SIGCOMM 2025 Falcon | https://dl.acm.org/doi/10.1145/3718958.3754353 | E2100 200Gbps IPU 内 reliable transport，**单 IPU 内**，非多 IPU sync |

### §A.4 / §A.13

- IPDK 公开支持 LACP 802.3ad，但 **0 命中** "multi-IPU per host" 文档
- Google Andromeda 闭源，**0 公开**多 IPU per host bond + sync flow

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整记录 | 最终 verdict |
| --- | --- | --- | --- |
| 权 1 / 11 / 23 / 35 / 36 | **公开资料不足（第 4 档弱候选）** | F2 IPDK 字面命中 LACP；F1/F3/F4 公开资料 0 命中（无多 IPU per host 文档）；按硬约束 4，0 命中 ≠ 已排除；按硬约束 3，整数限定 N ≥ 2 拓扑外推禁令——不能从单 IPU 文档推多 IPU 命中 | **公开资料不足（第 4 档弱候选）— 闭源 Andromeda 需取证升级** |

### F# 投票汇总

- F1：IPDK + 单 IPU 是公开 baseline；多 IPU per host 公开资料 0 命中
- F2：IPDK 字面 LACP 命中（单 IPU 内）
- F3：单 IPU LAG → 单层
- F4：无多 IPU sync 描述

### 最终 verdict

**公开资料不足（第 4 档弱候选）**：IPDK + Intel IPU 是 6 路候选中"最有可能" 的——具备 LACP + OVS hw-offload building blocks——但 Google Andromeda 是闭源数据面，**未公开多 IPU per host + sync flow 实现**。需法务取证 / 客户合作披露 / NDA 渠道 / Google 内部技术博客作者询证升级。

## 总结一句话

Intel IPU + IPDK 具备 LACP / OVS offload building blocks（最强候选块）但 Google Andromeda 闭源不公开多 IPU sync flow——**落第 4 档公开资料不足弱候选**，需取证升级。
