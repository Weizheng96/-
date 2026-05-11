# Verdict — Intel IPU E2000 (Mount Evans) + IPDK + OPI Project

> 主体类型：S3 + S4；适用独立权：权 1 / 权 9 / 权 17；分级：**P1**

## 核心组织
**Intel Corporation（NASDAQ: INTC）** — IPU 整机 + IPDK（Infrastructure Programmer Development Kit）+ OPI（Open Programmable Infrastructure，Linux Foundation 项目，Intel 主导）

## F1-F5 命中表
| F# | 证据 | 命中 |
| --- | --- | --- |
| F1 | IPDK 文档明确支持 OVS 卸载到 IPU；Intel Network Builders 联合白皮书系列 | **字面命中** |
| F2 | DPDK 上游 PMD 多线程模型由 Intel 主导维护 | **字面命中** |
| F3 | Intel 文档提及 NUMA-aware 调度 | **字面命中** |
| F4 | Intel 自家文档未单独推荐 auto-LB（参考 NVIDIA 类似情况） | **公开资料不足** |
| F5 | IPDK 支持 P4 / TC flower 重映射，pmd-rxq-affinity 通过 OVS-DPDK 上游可达 | **字面命中** |

## 时间线
- IPU E2000 / Mount Evans GA：2022 → post-grant；IPDK 1.0：2022 → post-grant

## §A 穿透
- §A.2 Intel SIGCOMM / OFC paper 涉及 IPU 数据面
- §A.6 Intel Network Builders × Red Hat / VMware 联合白皮书丰富
- §A.7 Intel 是 OVS / DPDK 上游主要 maintainer（强归因证据）

## 状态机三栏
| 权 | 原始 | 调整 | 最终 |
|---|---|---|---|
| 权 1 / 9 / 17 | **第 3 档：公开资料不足（强候选）** — F1-F3/F5 字面，F4 不足 | 同 NVIDIA 候选——禁止上游继承推断；F4 维持不足 | 第 3 档 |

## 总结一句话
Intel IPU E2000 + IPDK + OPI：F1/F2/F3/F5 字面命中（Intel 自家文档），F4 因 Intel 未主动推荐 auto-LB 标公开资料不足；落第 3 档强候选。
