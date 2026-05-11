# Verdict — NVIDIA SR-IOV VF-LAG 拓扑 T-B：多 NIC + 卡内 VF-LAG + OVS 跨卡聚合（推测拓扑）

> 主体类型：S3 + S4；适用独立权：权 1 / 11 / 23 / 33 / 34 / 35 / 36；分级：**P0**

## 1. 核心组织
NVIDIA Corporation（NASDAQ: NVDA）

## 2. F1-F5 命中表（T-B 拓扑：多 NIC HA）

| F# | 证据 | 命中 |
|---|---|---|
| F1（M VM + N ≥ 2 NIC）| **NVIDIA 公开文档未明示**多 NIC 跨卡部署 + 全卡 HW offload 完整拓扑 | **公开资料不足**（按 §D 硬约束 3 反向脑补禁令——不能用单卡文档外推多卡命中）|
| F2 | NVIDIA QSG 明示 LACP bond mode（卡内层级）— 跨卡场景同样适用 LACP | **字面命中**（与 T-A 同：LACP support） |
| F3（N 端口标识 → 第一端口）| OVS bond port 抽象在跨卡场景下可形成"第一端口"——NVIDIA 是否在跨卡场景做硬件 offload 未明示 | **公开资料不足** |
| F4 | OVS 标准 miss handling | 字面命中 |
| F5（同时下发到所有 N 网卡）| NVIDIA 文档**未描述**跨卡 hardware e-switch 同步 offload 路径——是否真做到"所有 N 卡同时 offload"未明示 | **公开资料不足** |

## 3. 时间线
- BlueField-2 GA：2020-08；BlueField-3 GA：2023+；DOCA SDK 1-2.x：post-grant 主导
- **现有技术 caveat 警示**：2017-2020 ConnectX-5 + mlx5 driver 早期版本可能已实现部分 F1-F5——建议法务深读 `git log --before=2020-10-31 -- drivers/net/ethernet/mellanox/mlx5/lag/`

## 4. §A 穿透
- §A.1 反向专利墙：NVIDIA / Mellanox 在 H04L49 / H04L45 主分类专利墙厚——**强现有技术 caveat 信号**
- §A.6 联合案例（R-PARTNER）：NVIDIA × Red Hat × VMware vSphere 8 联合 reference architecture 可能含 T-B 完整拓扑——**未深抓取**
- §A.7 上游归因：mlx5_core driver 贡献者归因（@mellanox.com / @nvidia.com email domain）

## 5. 配置参数双引证（R-CONFIG）

| 参数 | prose 引文 | 对应 F# |
|---|---|---|
| `bond mode = LACP (802.3ad)` | NVIDIA QSG 明示卡内层级支持 LACP | F2 |
| SR-IOV switchdev mode | NVIDIA QSG："both PFs of the NIC must first be configured to SR-IOV switchdev mode" | F1 / F5（前置条件）|
| `bond up-link representors` | NVIDIA QSG："bond the up-link representors" | F3 端口标识聚合 |
| 跨卡部署 config | （NVIDIA 文档未明示完整跨卡配置）| F5 公开资料不足 |

## 6. 状态机三栏判定

| 独立权 | 原始 | 后置调整 | 最终 |
|---|---|---|---|
| 权 1 / 11 / 23 / 33 / 34 / 35 / 36 | **第 3 档：公开资料不足（强候选）** — F2/F4 字面命中；F1/F3/F5 NVIDIA 文档未明示完整跨卡 + 全卡 HW offload 拓扑 | 1.等同未触发；2.反向证据未触发；3.Active 不降级；**4.现有技术 caveat：强（2017-2020 mlx5 LAG commit history 需法务深读）**；5.R-STANDARD 未触发；6.§5.0 未触发；7. patent license（NVIDIA 是否对 OIN 做承诺）待法务核查 | **第 3 档：公开资料不足（强候选）** |

## 7. 升级路径
- (a) IncoPat / 智慧芽深读 NVIDIA / Mellanox 同主分类专利墙（关键——核查现有技术 caveat）
- (b) NVIDIA × Red Hat 联合 reference architecture 深读（找 T-B 完整拓扑描述）
- (c) Linux kernel mlx5 driver `git log --before=2020-10-31` 详细审计
- (d) 反向工程 BlueField 双卡 HA 部署的实际 HW offload 行为
- (e) NVIDIA Inception / 客户合作渠道获取多卡 VF-LAG deployment guide

## 8. 总结一句话
NVIDIA VF-LAG 多 NIC 跨卡 HA 拓扑（推测）：F2/F4 字面命中、F1/F3/F5 NVIDIA 公开文档未明示跨卡 + 全卡 HW offload 路径，落第 3 档（公开资料不足强候选）；附强现有技术 caveat（mlx5 LAG 2017+ 早于专利申请日）。
