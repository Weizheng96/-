# 候选 #19 NVIDIA DOCA / VF-LAG / BlueField — 合议判定

**主体类型**：芯片厂 + 软件发布方
**适用独立权**：权 35 + 权 36
**判定**：**已排除**

---

## 子 agent 投票表（F1-F6 × 5 文档）

| 特征 | A (VF-LAG QSG) | B (404) | C (BF3 datasheet) | D (OVS-DOCA v2.10.0) | E (ASAP² Direct) | 合议 |
| --- | --- | --- | --- | --- | --- | --- |
| F1 vSwitch | 是 | 无效 | 是（ASAP²） | 是 | 是 | **是**（OvS / ASAP² / DOCA Flow） |
| F2 N≥2 物理 NIC | **否，强反向**（"same NIC"） | 无效 | 否（单芯片多 port） | **是**（D 误读） | **否**（"both PFs of the NIC"） | **否**：4/4 有效文档明示单 NIC，D 误读已证伪 |
| F3 NIC 内部 LACP 聚合 | 是（单 NIC 内） | 无效 | 否 | 是（D） | 部分（单 NIC 内） | **是但仅限单 NIC 内**——不命中专利 F3"每张 NIC 内部"在 N≥2 NIC 语境下的含义 |
| F4 多 NIC → 同一目标端口 | **否** | 无效 | 否 | **是**（D） | **否** | **否**：D 误读已证伪 |
| F5 同表多卡分发 | **否** | 无效 | 否 | **是**（D） | **否**（"flow not split between PFs of same NIC"） | **否**：D 误读已证伪 |
| F6 NIC 硬件 offload | 是 | 无效 | 是 | 是 | 是 | **是** |

## 子 agent D 误读复查

D 在 OVS-DOCA v2.10.0 文档中读到 "Multiport eSwitch Mode"："all uplinks and VFs/SFs representors of all physical ports are managed by the same hardware switch"，并据此判 F2/F4/F5 命中。

**主 agent 复查（grep 原文）**：

实际配置命令（节内紧接的代码块）：
```
devlink dev param set pci/0000:03:00.0 name esw_multiport value 1 cmode runtime
devlink dev param set pci/0000:03:00.1 name esw_multiport value 1 cmode runtime
```

两条命令操作的是 `0000:03:00.0` 和 `0000:03:00.1`——**同一 BDF（PCI bus 03）的 function 0 和 function 1**，即**同一张 ConnectX/BlueField 卡的两个 PF**。文档进一步说："configure multiport eswitch for each PF where **p0 and p1 represent the netdevices for the PFs**"——p0 / p1 是同一卡的两个 PF。

**结论**：D 把"两个 physical port"理解为"两张物理 NIC"，但配置命令的同 BDF 证明这仍然是**单张 NIC 多 PF** 架构，与 VF-LAG 同源，只是允许 port-to-port 直接转发（不走 bond）。**D 的 F2/F4/F5 命中判定错误，本合议否决**。

## 反向证据汇总（强）

1. **VF-LAG QSG（A）原文**："the bond mode is reflected to all VFs of the **same NIC**"（行 1596）；"A single virtual function is backed by **two physical bond ports**"（行 1511）—— 字面"same NIC" + "two ports"。
2. **ASAP² Direct（E）原文**："both physical functions of **the NIC**"（行 2771）、"all VFs of **the two PFs**"（行 2858）—— 同卡双 PF。
3. **OVS-DOCA v2.10.0 Multiport eSwitch（A 复查）**：配置命令同一 BDF（`0000:03:00.0` / `0000:03:00.1`）—— **同卡双 PF**，与 VF-LAG 同源架构。
4. **BlueField-3 datasheet（C）**："1, 2, 4 ports with up to 400 Gb/s connectivity"——单芯片多 port，无跨卡机制。
5. **专利墙（main agent）**：NVIDIA 在 Google Patents 同方向 0 命中。
6. **顶会论文（main agent）**：NVIDIA 未在 SIGCOMM/NSDI/APNet/EuroSys 发表 multi-DPU same-flow 主题论文。

## 落入专利明确排除的相邻方案
参照专利"明显不在保护范围内的相邻方案"清单：
- 第 1 项 **单网卡（N=1）+ LACP 不满足 F2/F4** —— 命中（NVIDIA VF-LAG / ASAP² / Multiport eSwitch 都是单 NIC）

## 最终结论
**NVIDIA DOCA / VF-LAG / BlueField 在权 35 + 权 36 双重已排除**：
- 权 35（BlueField / ConnectX 芯片）：5 份本地化文档中 4 份明确反向证据，1 份 D 的误读已被合议证伪。所有 NVIDIA NIC 内 bond / LAG 机制（VF-LAG / Multiport eSwitch）均限定于**单 NIC 多 PF**，不构成专利 F2 的 "N≥2 张物理 NIC"
- 权 36（DOCA SDK / MLNX_OFED 软件二进制）：基于同样的单 NIC 架构假设，软件层无多 NIC 同表分发代码路径

## 数据完整性说明
- 1 份文档（B：OVS-DPDK Hardware Offloads）NVIDIA Docs 返回 404，URL 已失效。但其他 4 份文档已提供足够强的反向证据
- D 的误读记录在案——这正是 Step 5b "**子 agent 独立审 + 主 agent 合议**"协议的设计意图：单一 agent 误读会被多 agent 投票纠正

## 升级前提
NVIDIA 未来发布"跨 ConnectX/BlueField 多卡 + 同一 eSwitch 域 + 同一精确流表分发"的官方支持，需要重新评估。当前 Multiport eSwitch 仍是单卡内能力。
