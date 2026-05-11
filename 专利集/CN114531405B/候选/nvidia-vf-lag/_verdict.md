# NVIDIA VF-LAG / Multi-Host LAG / Multi-PF — 与 CN114531405B 比对报告

**Patent**: CN114531405B (Huawei) — 授权日 2023-06-06
**调查目标**: NVIDIA / Mellanox 的 VF-LAG、Multi-Host LAG、Multi-PF (Socket Direct) 等"多端口/多卡聚合 + 卸载"特性
**调查日期**: 2026-05-11

---

## 1. 专利核心特征 (复述)

- **F1**: 多 VM × 多 NIC 拓扑（M ≥ 2 VM + N ≥ 2 NIC，皆挂在同一 vSwitch）
- **F2**: 每张 NIC 内部多物理口经 LACP/802.1AX 聚合成一个逻辑口
- **F3**: vSwitch 中通过 N→1 端口 ID 映射，把 N 张 NIC 的 N 个逻辑口聚成单一"first port"
- **F4**: 当目标 NIC 缺少匹配 offload 流表时，vSwitch 通过该"first port"**同步**把精确匹配流表下发到**全部 N 张 NIC**（N 份完全相同）

关键判定点：F1 / F3 / F4 都要求**多张物理 NIC**（N ≥ 2），且 vSwitch 把流表**同步复制**到所有 NIC 的硬件 FDB。

---

## 2. 收集到的证据 (URL + 关键引用)

### E1 — StackHPC 技术博客（独立第三方综述）
- **URL**: https://www.stackhpc.com/vflag-kayobe.html
- **日期**: 2021-03-30（**早于** F1 grant date）
- **关键引用**:
  > "VF-LAG only works for two ports on the same physical NIC. It cannot be used for LAGs created using multiple NICs."
- **判定意义**: 直接、明确的反向证据，证明 VF-LAG 仅支持单卡 2 端口，不支持跨卡。

### E2 — Mellanox/NVIDIA netdev pull request (2018-12-14)
- **URL**: https://www.spinics.net/lists/netdev/msg540007.html
- **作者**: Saeed Mahameed (saeedm@mellanox.com)
- **关键引用**（commit message）:
  > "VF LAG, which provides load-balancing and high-availability capabilities for VFs associated with different physical ports of the **same Connect-X card**."
- **判定意义**: 上游内核 VF-LAG 设计原意即为"同卡两口"，devcom 机制只在 same-card 范围内做 PF↔PF 通信。

### E3 — mlx5 内核源码 lag.c（Mellanox/bluefield-linux master）
- **URL**: https://github.com/Mellanox/bluefield-linux/blob/master/drivers/net/ethernet/mellanox/mlx5/core/lag.c
- **关键发现**:
  - `MLX5_MAX_PORTS = 2` 硬编码上限
  - `mlx5_lag_check_prereq()` 只校验 `ldev->pf[0].dev` / `ldev->pf[1].dev`（同卡两个 PF）
  - 端口号通过 `PCI_FUNC(dev->pdev->devfn)` 取 function-number，**没有任何跨 PCI device 的父桥比对**
- **判定意义**: 内核实现层面不存在"跨独立 PCIe NIC 卡"的代码路径。

### E4 — Mellanox Multi-Port E-Switch single FDB (2023-02-14)
- **URL**: https://www.spinics.net/lists/netdev/msg882440.html
- **作者**: Roi Dayan
- **关键引用**:
  > "MultiPort E-Switch builds on newer hardware's capabilities and introduces a mode where a single E-Switch is used and all the vports and physical ports **on the NIC** are connected to it."
- **判定意义**: 2023-02 引入的"single FDB"仍仅作用于**同一张 NIC** 内部的 vport / physical port，不是跨卡。

### E5 — kernel.org Multi-PF Netdev (Socket Direct) 文档
- **URL**: https://docs.kernel.org/networking/multi-pf-netdev.html
- **关键引用**:
  > "The feature adds support for combining multiple PFs of the **same port** in a Multi-PF environment under one netdev instance."
  > "Currently, we limit the support to PFs only, and up to two PFs (sockets)."
- **判定意义**: Socket Direct / Multi-PF 是**同一张 NIC 物理插到两个 PCIe 槽位**（跨 NUMA 加速），不是两张独立 NIC。

### E6 — LWN Article on mlx5 socket direct (Multi-PF) (2024-03-05)
- **URL**: https://lwn.net/Articles/964644/
- **关键引用**:
  > "combining multiple devices (PFs) of the same port under one netdev instance"
  > "One device is picked to be a primary (leader)... others (secondaries) are disconnected from the network in the chip level (set to silent mode). All RX/TX traffic is steered through the primary."
- **判定意义**: Socket Direct 机制是 leader-secondary 单路径转发，不是 vSwitch 把流表"复制 N 份"下发；与 F4 的"N copies are identical"语义完全不同。

### E7 — netdev 2024-12-18 mlx5 misc patch (multi-host LAG)
- **URL**: https://lists.openwall.net/netdev/2024/12/18/285
- **作者**: Tariq Toukan (tariqt@nvidia.com), Rongwei Liu
- **关键引用**:
  > "The first two patches by Rongwei add support for multi-host LAG. The new multi-host NICs provide each host with **partial ports**, allowing each host to maintain its **unique LAG configuration**."
- **判定意义**: 这里的 "multi-host LAG" 是指"**一张 NIC 物理共享给多个 host，每个 host 看到部分端口**"——拓扑方向与本专利相反（F1 是"一个 host 上多张 NIC"）。

### E8 — DPDK multi-host lag probe patch (2025-03-11)
- **URL**: https://www.mail-archive.com/dev@dpdk.org/msg312437.html
- **作者**: Rongwei Liu
- **关键引用**:
  > "Under multi-host environments, the NIC exports total 4 ports, and each host get 2 ports. The 2 ports' identifier is uncontinous now."
- **判定意义**: 再次确认"multi-host" = 一张 NIC 拆给多 host，每 host 拿一部分端口。仍然不是 F1 拓扑。

### E9 — NVIDIA enterprise support (Configuring VF LAG using TC)
- **URL**: https://enterprise-support.nvidia.com/s/article/Configuring-VF-LAG-using-TC
- **状态**: WebFetch 返回空内容（页面可能要求登录或被反爬）；记为部分检索失败
- **来自二级搜索摘要的引用**:
  > "both physical functions of the NIC must first be configured to SR-IOV switchdev mode, and only afterwards bond the up-link representors"
  > "Three bonding modes can be offloaded; Active-Backup, Balance-Xor, and 802.3ad."
- **判定意义**: 官方 KB 描述的也是"NIC 的两个 PF"——同卡两口。

### E10 — NVIDIA Developer Forum: "How to Bond two ConnectX-6 port"
- **URL**: https://forums.developer.nvidia.com/t/how-to-bond-two-connectx-6-port/279595
- **日期**: NVIDIA 工程师 Jonathan 答复 2024-01-22
- **关键引用**:
  > "In order to bond two ports together, you can use the standard linux method for interface bonding."
- **判定意义**: 当用户问到跨多张 ConnectX-6 卡聚合时，官方回复仍只指向标准 Linux bonding——**没有硬件 offload 的跨卡 LAG 方案**。

### E11 — NVIDIA Developer Forum: "VF-LAG offload" (2022-08)
- **URL**: https://forums.developer.nvidia.com/t/vf-lag-offload/225798
- **关键引用**:
  > NVIDIA 工程师 xiaofengl: "one MAC address can only be mapped to one port at a time"
- **判定意义**: 偏侧证据——官方解释 hash/分流行为时的语境仍是单卡两口。

### E12 — SIGCOMM / NSDI / netdev 学术会议论文检索
- **检索 query**: `SIGCOMM NSDI mlx5 ASAP2 SR-IOV VF-LAG paper Mellanox NVIDIA`
- **结果**: **0 篇** 直接对应的 NVIDIA / Mellanox 工程师署名 VF-LAG 实现论文
- **判定意义**: 未检索到可作为 F4 流表同步机制证据的学术文献。

---

## 3. 逐 F# 判定

| 特征 | Topology-A (单 ConnectX 多端口) | Topology-B (多 ConnectX 跨卡) |
|------|-------------------------------|------------------------------|
| **F1** 多 VM × 多 NIC (N ≥ 2) | **明确反向**（N=1 单卡） | **未检索到**任何 NVIDIA 官方/上游内核实现支持 N ≥ 2 卡的 VF-LAG offload |
| **F2** LACP 802.1AX 聚合 | **字面命中**（E2/E9: 802.3ad/Active-Backup/Balance-Xor 均支持） | 同左（如果硬要做也是 Linux 软 bond，无硬件 offload） |
| **F3** vSwitch N→1 端口聚合 | 概念近似（同卡两个 PF rep → 一个 bond rep），但 N=1 不构成多卡聚合 | **明确反向**：E3 源码 `MLX5_MAX_PORTS=2` 同卡限制；E4/E5/E6 的 single-FDB 与 Socket Direct 也均限同卡 |
| **F4** vSwitch 同步下发流表到全部 N NIC | 硬件 LAG 内部由 firmware 处理，但作用域为同卡两 PF；非"vSwitch 主动下发 N 份完全相同流表" | **明确反向 + 未检索到**：跨独立 PCIe NIC 同步下发流表的机制在 NVIDIA 公开文档/上游内核中**未检索到** |

---

## 4. Topology-A vs Topology-B 总体判定

### Topology-A（N=1 单 ConnectX/BlueField 多端口 LAG）
- **F1 不命中**（N=1 ≠ N≥2），**整体不构成侵权**。
- 与本专利无重叠。

### Topology-B（多 ConnectX/BlueField 跨卡 LAG）
- 经多源交叉验证（独立博客 E1、上游 commit E2、源码 E3、官方文档 E4/E5/E6、最新 multi-host 系列 E7/E8、官方 KB E9、官方论坛 E10）：
  - **NVIDIA 没有为"同 host 多张独立 ConnectX 卡跨卡聚合"提供硬件 offload 路径**；
  - 即便用户硬要做（如 Linux software bond on top of two separate NICs），就**只能走软件路径，无 vSwitch 同步下发到 N 张 NIC 硬件 FDB 的能力**——F3/F4 失配。
  - 2024-12 ~ 2025-03 的 "multi-host LAG" 是**反向拓扑**（一卡多 host），非 F1。
- **整体判定**：不构成 CN114531405B 任一独立权 / 关键从属权的字面 / 等同侵权。

---

## 5. 时间线要点

- VF-LAG 上游引入: 2018-12（早于专利）
- MultiPort E-Switch single FDB: 2023-02（早于 grant 2023-06，仍同卡）
- Multi-PF Socket Direct 文档化: 2024-03（晚于 grant，但仍同卡两 socket）
- "Multi-host LAG" 系列: 2024-12 / 2025-03（晚于 grant，但拓扑相反）
- **没有任何时间点出现 NVIDIA 实现"一 host 多张 NIC 的跨卡 LAG + vSwitch 同步流表下发"**的公开证据。

---

## 6. 证据缺口与诚实声明

- **0 hits**: SIGCOMM / NSDI / netdev conference 上未检索到 NVIDIA 工程师署名的 VF-LAG 实现论文。
- **部分检索失败**: NVIDIA enterprise-support KB 页面 (E9) WebFetch 返回空，仅依赖搜索摘要快照引用。
- **未做**: lore.kernel.org 全文 grep（受 Anubis 反爬阻断），仅通过 spinics.net 镜像 / mail-archive 替代。

---

## 7. 最终结论

**NVIDIA VF-LAG / Multi-Host LAG / Multi-PF (Socket Direct) 任一公开形态都不命中 CN114531405B 的 F1 + F3 + F4 组合。**

- Topology-A：F1 即不满足，无需后续判定。
- Topology-B：经多源公开证据交叉验证，NVIDIA 公开技术栈中**未实现**"同 host 多张独立 ConnectX 卡 LAG + vSwitch 同步下发硬件流表"的机制；上游内核 + 官方文档 + 论坛回复均一致指向"VF-LAG 仅适用于同卡两端口"。
- **建议**：将 NVIDIA VF-LAG 标记为 **已排除** 候选；保留本报告作为未来若 NVIDIA 推出真正跨卡 LAG offload 时可重新评估的基线。

---

**免责声明**: 本报告仅基于公开技术资料整理证据链，不构成法律意见。所有"侵权判定"性质的最终结论须由具资质的专利律师结合权利要求逐项比对后给出。
