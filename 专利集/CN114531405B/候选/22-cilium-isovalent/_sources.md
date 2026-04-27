# 候选 #22 Cilium / Isovalent — 资料索引

**主体类型**：软件 / 固件发布方（CNI + eBPF 数据面）
**适用独立权**：权 36（计算机存储介质）
**取证日期**：2026-04-27

---

## 五类源扫描结果

### 1. 专利
- WebSearch query：`Isovalent OR Cilium 申请 专利 patent assignee 流表 multi-NIC LACP bond OVS 2023 2024 2025`
- **结果**：**0 命中**与本专利同向的 Isovalent / Cilium 专利申请
- WebSearch query：`site:patents.google.com Cilium OR Isovalent multi-NIC LACP bond` (隐式)
- **结果**：仅命中无关的 CN103030102B（MEMS 水听器纤毛绑定，技术领域完全无关）
- **结论**：Cilium / Isovalent 在该方向无公开专利布局

### 2. 学术论文
- WebSearch query：`Cilium Isovalent SIGCOMM OR NSDI OR EuroSys OR APNet paper SmartNIC DPU 2023 2024 2025`
- **结果**：SIGCOMM/NSDI/APNet 2023-2025 列出的 SmartNIC / DPU 论文中**未见任何 Cilium 或 Isovalent 署名**
- 命中的相关论文（其他作者）：Alkali (NSDI 2025)、Lightning (SIGCOMM 2023)、LEED (SIGCOMM 2023)、P4 SmartNIC packet processing (SIGCOMM 2023)、Burstable Cloud Block Storage with DPU (OSDI 2024) — 都不是 Cilium 项目
- **结论**：Cilium 没有相关顶会论文披露多 NIC + LACP + 同表分发实现

### 3. 宣传材料
- 来源：[cilium.io](https://cilium.io/)、[isovalent.com](https://isovalent.com/)
- 关键信息：Cilium = "Cloud Native, eBPF-based Networking, Observability, and Security"，**核心数据面是 eBPF**，不是 OvS
- Cisco 2024-04 完成对 Isovalent 的收购
- **结论**：宣传材料反复强调 eBPF + XDP + TC，没有任何 LACP / NIC 内部聚合 / 多卡同表的描述

### 4. 使用手册 / 技术文档
本地存档：
- `cilium-program-types.html`（外壳 875B，SPA，未抽取到正文；search 结果已含原文摘要："in offloaded XDP mode, the XDP BPF program is directly offloaded into the NIC instead of being executed on the host CPU"）
- `cilium-bond-issue-18706.html`（355 KB，GitHub issue：Host network broken after one of the underlying interfaces of a bond goes down）
- `cilium-xdp-bond-issue-30072.html`（269 KB，GitHub issue：Cilium fails to attach xdp to bonded interface）
- `cisco-live-cilium-intro.pdf`（7 MB，Cisco Live 2025 BRKCLD-2696 Introduction to Cilium）

### 5. 行业标准 / 测试规范
- IEEE 802.3ad LACP：Cilium 不实现该标准；它依赖 Linux 内核 bonding 驱动（bonding driver 已经实现 802.3ad）。这意味着 LACP 行为发生在**主机 OS 层**，不在 Cilium 内部，更不在 NIC 内部
- CNI Specification (containernetworking/cni)：标准的 CNI 接口，与本专利保护范围无重合
- **结论**：Cilium 不实现 LACP；本专利 F3 要求"NIC 内部物理端口基于 LACP 聚合"——Cilium 既不在 NIC 内做 LACP，也不在 vSwitch 层做（因为 Cilium 不是 vSwitch）

---

## 拿不到的资料
- `https://docs.cilium.io/en/stable/bpf/progtypes/`：SPA 重定向页，curl + WebFetch 都拿不到正文（依赖 JS 渲染）。**已通过 WebSearch 摘要拿到关键引用**（XDP offload 描述）
- `https://isovalent.com/labs/cilium-multi-networking/`：同样 SPA 问题

详见 `_inaccessible.md`。

---

## 子 agent 审阅分配
- `cilium-bond-issue-18706.html` → 子 agent A（重点：Cilium 与 LACP bond 的实际交互方式）
- `cilium-xdp-bond-issue-30072.html` → 子 agent B（重点：XDP + bonded interface 的支持模型）
- `cisco-live-cilium-intro.pdf` → 子 agent C（重点：Cilium 整体架构与 NIC 卸载模型）
