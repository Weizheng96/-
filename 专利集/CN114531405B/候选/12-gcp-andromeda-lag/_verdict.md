# 候选：Google Cloud Andromeda + Falcon RDMA + IPU 集成

## 候选标识
- candidate_slug: `12-gcp-andromeda-lag`
- 主体类型：C. CSP
- 适用独立权：权 1, 11, 23, 33, 36

## §A 主流来源摘要

### §A.2 / §A.3

| # | 源 | URL | 引文 |
| --- | --- | --- | --- |
| 1 | Google Cloud Andromeda 2.2 blog | https://cloud.google.com/blog/products/networking/google-cloud-networking-in-depth-how-andromeda-2-2-enables-high-throughput-vms | 2023-10 — 描述 Andromeda 2.2 高吞吐 VM；**未提多 NIC + sync flow** |
| 2 | SIGCOMM '25 Falcon | https://dl.acm.org/doi/10.1145/3718958.3754353 | Falcon transport 在 E2100 IPU 内；**单 IPU 内**机制，非多 IPU sync |
| 3 | NSDI '18 Andromeda baseline | https://www.usenix.org/system/files/conference/nsdi18/nsdi18-dalton.pdf | 时间档：早于专利申请日，仅作 architectural baseline 使用，不构成命中 |

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整记录 | 最终 verdict |
| --- | --- | --- | --- |
| 权 1 / 11 / 23 / 33 / 36 | **公开资料不足（第 4 档弱候选）** | Andromeda 闭源；A3 Mega 配 8×200G NIC 是事实，但是否做"vSwitch 内 N→1 同步卸载" 0 命中；按硬约束 4，0 命中 ≠ 已排除 | **公开资料不足（第 4 档弱候选）** |

### F# 投票汇总

- F1：A3 Mega / A4 GPU 实例配 8 × 200G NIC 是公开事实 → F1 N ≥ 2 候选可能命中
- F2：未公开 LACP 实现细节
- F3：未公开 vSwitch N→1 映射
- F4：未公开 sync flow

### 最终 verdict

**公开资料不足（第 4 档弱候选）**：Google Cloud 多 NIC GPU 实例是事实，但 Andromeda 数据面闭源，**0 命中**多 NIC + LACP + vSwitch sync flow 实现细节。

## 总结一句话

Google Cloud A3 Mega 多 NIC GPU 实例事实存在但 Andromeda 闭源，公开 0 命中 F2/F3/F4 实现——**落第 4 档公开资料不足弱候选**。
