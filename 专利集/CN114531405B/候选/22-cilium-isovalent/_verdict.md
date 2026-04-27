# 候选 #22 Cilium / Isovalent — 合议判定

**主体类型**：软件 / 固件发布方
**适用独立权**：权 36（计算机存储介质）
**判定**：**已排除**

---

## 子 agent 投票表（F1-F6 × 3 文档）

| 特征 | 子 agent A（bond issue 18706） | 子 agent B（XDP bond issue 30072） | 子 agent C（Cisco Live PDF） | 合议（取并集） |
| --- | --- | --- | --- | --- |
| **F1** vSwitch | 否 | 否 | 否 | **否**（无字面，无等同；Cilium 是 CNI 不是 vSwitch） |
| **F2** N≥2 物理 NIC | 部分（环境含 bond）| 字面（4 张 mellanox NIC + LACP） | 否（未提多 NIC） | 部分字面（仅指 Cilium 运行环境恰好有 bond）|
| **F3** NIC 内部物理端口 LACP 聚合 | 否（LACP 在 Linux kernel bonding driver） | 否（同上：host bond） | 否（无 LACP 描述） | **否，反向证据强**：LACP 在 OS 内核，不在 NIC 内部 |
| **F4** N 个逻辑端口 → 同一目标端口标识 | 否 | 否 | 否 | **否** |
| **F5** 同一精确流表同时下发到 N 张 NIC | 否 | **强反向**（attach XDP 到 bond0 invalid argument，连单一 attach 都做不到） | 否 | **否，强反向证据**：issue #30072 直接证明 Cilium 缺失"同程序下发到多 slave NIC"能力 |
| **F6** NIC 侧硬件 offload 流表 | 否（mlx5 lag map ≠ 硬件流表 offload） | 否（无硬件 offload 描述） | 否（仅顺带提 MacSec 不支持） | **否** |

## 反向证据汇总（强证据）

1. **F3 反向**：3 份文档一致显示 LACP 由 **Linux kernel bonding driver** 完成，并非 NIC 内部聚合。专利 F3 字面要求"每张 NIC 内部多个物理端口基于 LACP 聚合形成的逻辑端口"——Cilium 既不在 NIC 内做 LACP，也不在自身代码中实现 LACP（依赖 kernel 已有实现）。
2. **F5 反向**：Cilium GitHub issue #30072（2024）直接报错 *"attaching XDP program to interface bond0: invalid argument"*——Cilium **无法**把同一 XDP 程序同时下发到 bond 多张 slave NIC，与专利 F5 完全相反。
3. **F1 反向**：Cilium 是 K8s **CNI**（容器网络接口），处理 Pod-to-Pod / Pod-to-Service 的 eBPF 软件转发，**不是 vSwitch**——与专利权利要求开宗明义"应用于虚拟交换机"不符。
4. **F6 反向**：Cisco Live 演讲明确把 Cilium 与传统 Switch/Router/LACP/VXLAN/EVPN 模型**对立呈现**；"硬件加密 offload (MacSec)"是作为 Cilium **不支持**的反例提到——Cilium 不走 NIC 硬件 offload 流表路径。

## 落入专利明确排除的相邻方案

参照 [专利介绍](../../CN114531405B"专利介绍".md) "明显不在保护范围内的相邻方案"清单，Cilium 同时命中其中 2 项：
- 第 3 项：**纯软件 vSwitch（无任何 NIC 卸载）**——Cilium eBPF 在内核数据路径，无 NIC ASIC offload
- 第 5 项：**仅在 NIC 内部做 LACP，但虚拟交换机没有第二级"目标端口标识"映射**——更激进地，Cilium 既不在 NIC 内做 LACP，也无 vSwitch 第二级映射

## 最终结论
**Cilium / Isovalent 在权 36 下已排除**。F1 / F3 / F4 / F5 / F6 五项要件均字面 + 等同不命中，F2 即便环境有 bond 也是主机 OS 层 bond 而非 NIC 内部聚合。Cisco 完成对 Isovalent 的收购（2024）后短期内技术路线无重大转向迹象。

升级前提：如果 Cilium 未来引入"vSwitch 模式 + NIC 内部 LACP + 多 NIC 同表 XDP/TC offload"，需重新评估——但目前没有任何路线图迹象指向此方向。
