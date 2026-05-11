# Verdict — Linux kernel bonding driver + mlx5 LAG offload（核心技术 CT-2）

> 主体类型：S1 + S5；适用独立权：权 1 / 11 / 23 / 33 / 34 / 35 / 36；分级：**P0**

## 1. 核心组织
- Linux Foundation（Linux kernel 项目）
- Mellanox / NVIDIA（NASDAQ: NVDA）—— mlx5 LAG offload 主要贡献方
- Linus Torvalds & Linux 内核 bonding driver maintainers（Jay Vosburgh 等）

## 2. F1-F5 命中表

| F# | 证据 | 命中 |
|---|---|---|
| F1 | Linux kernel bonding driver 支持任意 N 张 NIC 卡聚合 | **字面命中**（kernel bonding 支持 N ≥ 2）|
| F2 | bonding driver 实现 802.3ad LACP mode 4 + 标准协议交互 | **字面命中**（Documentation/networking/bonding.rst — `bond_mode_802.3ad`）|
| F3 | bond master interface + bond slaves 抽象 — "bond0" 即 vSwitch 视角下的"第一端口"等价物 | **字面命中** |
| F4 | NIC miss → kernel netdev stack → upcall to userspace | **字面命中** |
| F5 | mlx5 LAG offload（`drivers/net/ethernet/mellanox/mlx5/lag/`）— 跨 PF LAG 在硬件 e-switch 同步 offload | **字面命中候选**（mlx5 LAG 在硬件层做 LAG offload；但**单卡 dual-PF 默认拓扑下** mlx5 LAG 工作在 PF 级而非跨独立 NIC 卡）|

## 3. 时间线
- Linux kernel bonding driver：自 Linux 2.0 时代已有（~1996）
- mlx5 LAG offload：~2017+
- **现有技术 caveat**：Linux kernel bonding + mlx5 LAG offload 大量在 2020-10-31 之前已实现 — **可能影响专利新颖性**

## 4. §A 穿透
- §A.1 反向专利墙：Mellanox / NVIDIA 在 H04L 主分类同主题专利墙厚（包括跨 PF LAG 相关 — 强现有技术 caveat 信号）
- §A.7 上游归因：`git log --before=2020-10-31 -- drivers/net/ethernet/mellanox/mlx5/lag/` 是关键现有技术取证目标

## 5. 状态机三栏判定

| 独立权 | 原始 | 后置调整 | 最终 |
|---|---|---|---|
| 权 1 / 11 / 23 / 33 / 34 / 35 / 36 | **第 3 档：公开资料不足（强候选）** — F1-F5 多数字面，但拓扑歧义（mlx5 LAG 主要 PF 级）| 1-3 未触发；**4. 现有技术 caveat：强（Linux kernel bonding + mlx5 LAG 2017+ 已实现，与专利 2020-10-31 申请日有时间冲突 → 法务必查）**；5-6 未触发；7. patent license（OIN / Linux Foundation commitment）待法务核查 | **第 3 档：公开资料不足（强候选）+ 强现有技术 caveat** |

## 6. 总结一句话
Linux kernel bonding + mlx5 LAG offload：F1-F4 字面命中、F5 字面命中候选；落第 3 档强候选；附**强现有技术 caveat**（2017+ mlx5 LAG 早于专利申请日，建议法务深读 mlx5 commit history 评估新颖性影响）。
