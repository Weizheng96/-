# 候选：AWS Nitro System (v3-v5) + multi-ENI / multi-Nitro Card

## 候选标识
- candidate_slug: `11-aws-nitro-multi-eni`
- 主体类型：C. 公有云 CSP
- 适用独立权：权 1, 11, 23, 33, 34, 35, 36
- 命中场景：场景 1 / 4

## §A 主流来源摘要

### §A.4 使用手册 / 技术文档

| # | 源 | URL | 引文 |
| --- | --- | --- | --- |
| 1 | AWS Nitro Security Whitepaper | https://docs.aws.amazon.com/whitepapers/latest/security-design-of-aws-nitro-system/the-components-of-the-nitro-system.html | "A modern EC2 server is made up of a main system board and **one or more** Nitro Cards"；Nitro Cards 之间通过私有内部网络互联——但**枚举的功能**是 VPC / EBS / Storage / Controller，**不是 N 张 NIC + sync flow** |
| 2 | AWS Nitro perf tuning | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ena-nitro-perf.html | "When a Nitro card performs the initial evaluation for a new flow, it saves information... 5-tuple flow"——**per-Nitro-card** 流表缓存，**无多卡同步**描述 |
| 3 | AWS network cards | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html | "When you attach a network interface to an instance that supports multiple network cards, you can select the network card... The primary network interface must be assigned to network card index 0" — 每 NetworkCardIndex 是**独立**的 ENI/EFA endpoint，**独立 IP / 独立 subnet** |
| 4 | AWS multi-card EFA | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa-acc-inst-types.html | P5/P5e=32 cards、trn1n/trn2=16 cards — 但每 NCI 是独立 ENI，**无 LACP / 无 LAG / 无 bonding** |

### §A.2 学术阵地

- NSDI '25 / SIGCOMM '24-'25 — **0 命中** AWS-authored Nitro 多卡数据面论文
- James Hamilton blog — 最近 Nitro post 是 2019，**0 命中**post-2023-06-06 更新

### §A.13 技术分享视频

- re:Invent 2024 NET402 PDF（7.7 MB binary，无法 verbatim 提取）；secondary 索引描述涵盖 ENA 演进 + flows after connections established，**无 verbatim 提及多 Nitro vSwitch / LAG**
- re:Invent 2025 CMP316 — 描述 SRD / ENA Express / security，**0 命中** vSwitch / LAG / multi-card flow synchronization

### §A.16 多语言 cross

- 中文圈 zhihu / cnblogs / upcloudx — **0 命中**泄漏的非公开 Nitro 内部细节

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整记录 | 最终 verdict |
| --- | --- | --- | --- |
| 权 1 / 11 / 23 / 33 / 34 / 35 / 36 | **已排除（第 5 档）** | F1 部分反向（multi-card = independent ENI 独立 IP/subnet，不构成"多 NIC 接同一 vSwitch"）；F2 真反向（Nitro 不实现 LACP）；F3 真反向（无 vSwitch 概念，无 N→1 映射）；F4 真反向（per-card flow caching, no sync）；§5.0 豁免：满足 (a) | **已排除（架构层级 + F1-F4 多重反向证据）** |

### F# 投票汇总

- F1：multi-card 是**独立** ENI（不同 IP / subnet），**不构成同一 vSwitch 下的 N 张 NIC**
- F2：AWS Nitro **不实施 LACP**——每 NCI 独立 endpoint
- F3：AWS Nitro **没有 vSwitch 概念**，更没有 N→1 映射
- F4：per-card 5-tuple flow caching，**无 N 份同步副本**

### 最终 verdict

**已排除**：AWS Nitro multi-card 模型是"多个独立 PCIe Nitro Card + 独立 IP/subnet endpoint"——架构层面与本专利 F1-F4 全部不一致。

## 总结一句话

AWS Nitro multi-card = independent ENI（不同 IP/subnet），无 vSwitch/LACP/sync flow——架构层面 F1-F4 全部反向，**落第 5 档已排除**。
