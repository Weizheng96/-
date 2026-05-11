# 候选：阿里云 CIPU + 神龙 4.0 / 倚天 ECS

## 候选标识
- candidate_slug: `13-aliyun-xdragon-cipu`
- 主体类型：C. 公有云 CSP + B. 自研 SmartNIC
- 适用独立权：权 1, 11, 23, 33, 34, 35, 36

## §A 主流来源摘要

### §A.2 学术阵地（深度命中）

| # | 论文 | URL | 引文 |
| --- | --- | --- | --- |
| 1 | **Triton (SIGCOMM 2024)** | https://dl.acm.org/doi/10.1145/3651890.3672224 ; PDF https://cs.stanford.edu/~keithw/sigcomm2024/sigcomm24-final113-acmpaginated.pdf | "Apsara vSwitch (AVS) is a **per-host** deployed forwarding component"；"our internally developed SmartNIC (also referred to as **CIPU**)"；**全文 0 处 LACP / 0 处 802.1AX / 0 处 bond / 0 处 multi-NIC** |
| 2 | **Nezha (SIGCOMM 2025)** | https://dl.acm.org/doi/10.1145/3718958.3750466 ; PDF https://ng-95.github.io/files/Nezha_SIGCOMM25.pdf | "Nezha reuses the existing idle SmartNICs **on other servers** to handle the excess load from the local SmartNIC" — vNIC 前后端**远程**分离，**与 F4 "本地多 NIC 同步" 思路相反** |
| 3 | **HPN (SIGCOMM 2024)** | https://dl.acm.org/doi/10.1145/3651890.3672265 ; PDF https://ennanzhai.github.io/pub/sigcomm24-hpn.pdf | **17 处 LACP + 6 处 bond**：每 host 9 张 NIC，每张 NIC 双端口 LACP 接两台非堆叠 ToR；但**仅用于 LLM 训练 RDMA backend 网络**；论文明示"rather than hardware-offloaded RDMA"，**绕过 vSwitch** |
| 4 | Sirius (NSDI '24) / Alkali (NSDI '25) 摘要 | https://www.usenix.org/conference/nsdi24/technical-sessions ; https://www.usenix.org/conference/nsdi25/technical-sessions | Sirius "shared pool of high-performance cards"；Alkali 编译器框架；**均无"本地多 NIC + LACP + 同步流表"** |

### §A.4 文档

- ebmgn7ex 规格："2 张物理网卡 160 (80×2) Gbit/s"——**未提 LACP / bonding 语义**
- ECS 多网卡方案：每容器/实例独占 ENI 弹性网卡（**软件视图**）— 非 N→1 物理 NIC 聚合
- CIPU 10 大能力（CSDN Jmilk）：**单节点单 MoC/CIPU 卡** + 该卡支持挂多达 32 张 ENI

### §A.10 / 11 / 14 / 19

- 招聘 JD（boss / 拉勾 site 限定）：未返回 CIPU 多 NIC LACP 相关岗位描述
- @alibaba-inc.com 邮箱域 query：仅返回通用论文署名页
- 0 命中

## §C 子 agent 复核

agent ID a324869b0cf22132e 完成深度调研，重点抓取 Triton / Nezha / HPN PDF verbatim。主 agent 复核 claim 1 + 11 + 23 后认可：HPN 中 LACP 是**RDMA backend bypass vSwitch**——不构成 F2 字面命中（属"同名异境 cross-context false positive"）。

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整记录 | 最终 verdict |
| --- | --- | --- | --- |
| 权 1 / 11 / 23 / 33 / 34 / 35 / 36 | **已排除（第 5 档）** | F1 部分反向（Triton 单 CIPU per host）+ F4 部分反向（Nezha local↔remote 分离 vs F4 本地多 NIC 同步思路相反）；HPN 字面 LACP 命中但属"同名异境" — 不能作为 F2 命中证据；§5.0 豁免：满足 (a) | **已排除（架构反向证据 + LACP 出现于不同上下文）** |

### F# 投票汇总

- F1：Triton 明确"per-host AVS + 单 CIPU"——多 NIC 不在同一 vSwitch 下
- F2：HPN 字面 LACP 出现 17 次但属 RDMA backend，**与 vSwitch 流表卸载不在同一技术上下文** → 同名异境，不计入 F2 命中
- F3：无 N→1 vSwitch 端口映射描述
- F4：Triton "upcall to software 再下发**单条**到 CIPU"；Nezha 本地↔远端分离——**与 F4 "本地多 NIC 同步" 思路相反**

### 最终 verdict

**已排除**：阿里云 CIPU 走"per-host AVS + 单 CIPU"+"远端 idle SmartNIC 池"的范式（Triton + Nezha SIGCOMM 论文公开声明），与本专利 F1+F3+F4 在架构层面对立。HPN 的 LACP 字面出现属于 RDMA backend 上下文，与 vSwitch 流表卸载不同技术栈。

## 总结一句话

阿里 CIPU 走 per-host 单卡 + 远端共享范式（Triton / Nezha 反向证据），HPN LACP 仅用于 RDMA backend bypass vSwitch——**落第 5 档已排除**。
