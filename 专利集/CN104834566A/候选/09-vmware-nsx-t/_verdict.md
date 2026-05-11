# Verdict — VMware NSX-T + vSphere DSE

> 主体类型：S1（商业 vSwitch）+ S3（vSphere DSE 整机化）；适用独立权：权 1 / 权 9 / 权 17；分级：**P1**

## 核心组织
**Broadcom Inc.（NASDAQ: AVGO）—— VMware 子公司**：VMware NSX-T、vSphere、DSE

## F1-F5 命中表
| F# | 证据 | 命中 |
| --- | --- | --- |
| F1 | VMware NSX-T 官方文档 — N-VDS / VDS 是 vSwitch | **字面命中** |
| F2 | NSX-T 数据面 fastpath 多核 worker；vSphere DSE 通过 BlueField/Pensando DPU 多线程 | **字面命中** |
| F3-F5 | 闭源；NSX-T 内部 PMD 调度算法不公开 | **公开资料不足** |

## 时间线
- NSX-T GA：2017+ → post-grant；vSphere DSE GA：2022+ → post-grant

## §A 穿透
- §A.6 联合案例：VMware × NVIDIA / AMD/Pensando vSphere 8 DSE 联合白皮书（OK 命中 F1-F2，但 F3-F5 仍不公开）
- §A.18 同族：VMware 在虚拟网络主分类专利墙厚

## 状态机三栏
| 权 | 原始 | 调整 | 最终 |
|---|---|---|---|
| 权 1 / 9 / 17 | **第 3 档：公开资料不足（强候选）** — F1-F2 字面命中；F3-F5 闭源 | 闭源限制；建议反向工程 + 联合白皮书深读 | 第 3 档 |

## 总结一句话
VMware NSX-T + vSphere DSE：F1-F2 字面命中，F3-F5 闭源致公开资料不足；落第 3 档（强候选）；建议 vSphere DSE × DPU 联合白皮书深读升级。
