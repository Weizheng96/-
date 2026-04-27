# 候选 #21 AWS Nitro System — 合议判定

**主体类型**：部署方（AWS EC2）+ 芯片厂（自研 Nitro Card）
**适用独立权**：权 1 / 11（部署）+ 权 35（Nitro 芯片）
**判定**：**已排除**

---

## 子 agent 投票表（F1-F6 × 5 文档）

| 特征 | A (Nitro overview) | B (re:Invent NET402) | C (ENA perf) | D (Enhanced Networking) | E (Security Design) | 合议 |
| --- | --- | --- | --- | --- | --- | --- |
| F1 vSwitch | 否 | 部分相关（VPC 数据面）但非标准 vSwitch | 否 | **否，强反向**（SR-IOV 直通） | **否，强反向**（"no networking stack"） | **否** |
| F2 N≥2 物理 NIC | 否 | **否**（单 Nitro Card per instance） | 否（单 ENA） | 否（单 VF） | 否 | **否，强反向**（5/5 文档一致单卡） |
| F3 NIC 内部 LACP | **否，0 命中** | **否，0 命中**（LACP/802.3ad/bonding 0 次） | 否 | 否 | 否 | **否，强反向证据**（5/5 文档 LACP 0 命中） |
| F4 多 NIC → 同一目标端口 | 否 | 否 | 否 | 否 | 否 | **否** |
| F5 同表多卡分发 | 否 | **否，反向**（Shared Nitro = 单卡时分多租户） | **否，反向**（Asymmetric routing 反被警告 reduce performance） | 否 | 否 | **否，强反向证据** |
| F6 NIC 硬件 offload | 部分（语义不同） | 是（背景层面） | 是（弱） | 部分（SR-IOV 虚拟化加速） | 部分（密码 offload） | **是但语义不同**（offload 对象是虚拟化职能 / 加密 / SR-IOV，**不是流表分发**） |

## 强反向证据汇总

1. **F1 反向（E）**：Nitro Security Design 白皮书 p.14 原文 *"Nitro Hypervisor … **no networking stack** … no peripheral device driver support"* —— **AWS 主机侧根本没有 vSwitch**，VM 直接通过 SR-IOV 访问 Nitro Card for VPC 的 ENA VF。
2. **F1 反向（D）**：Enhanced Networking 用户指南原文 *"Enhanced networking uses **single root I/O virtualization (SR-IOV)** to provide high-performance networking"* —— SR-IOV 直通范式与本专利"vSwitch + 多 NIC + LACP + 同表分发"路径**正交**。
3. **F2 反向（B）**：re:Invent 2024 NET402 (8 MB / 223 页) 处理栈图 70+ 次以单 Nitro Card 形式呈现；**0 次出现"two/dual/multiple NICs"**。
4. **F3 反向（5/5 文档）**：5 份本地化文档中 **LACP / 802.3ad / bond / link aggregation 全部 0 命中**——这是非常强的反向证据。
5. **F5 反向（C）**：ENA performance tuning 文档原文 *"Asymmetric routing … can **reduce** the peak performance"* —— ENA / Nitro 的设计**鼓励单流走单 NIC**，与本专利 F5"同一精确流表同时下发到全部 N 张 NIC"取向**完全相反**。
6. **F5 反向（B）**：re:Invent NET402 p.182 "Shared Nitro Resources" = **单卡时分多租户**（一张卡服务多 instance），不是**多卡共享一 instance**。
7. **F2/F4 反向（B）**：大流量优化方案是"在 outer UDP source port 注入熵 → 单卡 RSS 多队列"——用 multi-queue 替代了 multi-NIC，**等效但完全不同**的实现路径。

## 落入专利明确排除的相邻方案

参照专利"明显不在保护范围内的相邻方案"清单：
- **第 1 项 单网卡（N=1）+ LACP** —— Nitro 是单 Nitro Card per instance（更激进：连 LACP 都不用，是 SR-IOV）
- **第 3 项 纯软件 vSwitch（无 NIC offload）的反例** —— Nitro 反过来是"无 vSwitch（'no networking stack'）+ NIC 全卸载"，与该相邻方案在另一个极端
- **第 5/6 项**：Nitro 不在 vSwitch + 多 NIC 二级聚合模型内

更根本的：**AWS Nitro 选择了一条与本专利完全不同的技术路线**——专利是"vSwitch 协调多 NIC + LACP 聚合 + 同表分发"；Nitro 是"消除 host vSwitch + SR-IOV 直通 + 单 NIC 大带宽 + 内部 RSS 多队列"。两者抽象层级、设计目标、实现机制都不同。

## 最终结论
**AWS Nitro System 在权 1 / 11 / 35 三层全部已排除**：
- 权 1 / 11（部署侧）：AWS 不部署 vSwitch + LACP 多 NIC 架构
- 权 35（Nitro Card 芯片侧）：Nitro Card 固件不实现 LACP / 多 NIC 同表分发；ENA driver 不基于 802.3ad

字面侵权与等同侵权门槛均不达标——Nitro 的 SR-IOV 直通 + 私有协议路径与本专利路径**实质不同**，等同三步法（基本相同手段 / 功能 / 效果）也难以成立。

## 升级前提
若 AWS 将来废弃 SR-IOV 直通改用标准 vSwitch + LACP（极不可能），需重新评估。截至 2026-04-27，AWS Nitro 路线图明确进一步加强 SR-IOV/ENA 直通模式（v5、200/400 Gbps），无逆转迹象。
