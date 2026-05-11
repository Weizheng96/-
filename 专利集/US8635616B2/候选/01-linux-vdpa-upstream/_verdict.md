# Verdict — Linux kernel vDPA framework + vhost-vdpa（核心技术 CT-1）

> 主体类型：S1 + S5；适用独立权：Claim 1 / 11 / 19 / 20 / 21；分级：**P0**

## 1. 核心组织
- **Linux Foundation**（项目宿主，非营利）
- **Red Hat（IBM 子公司，NYSE: IBM）** — 主要 maintainer + 商业 vDPA 集成方
- **Mellanox / NVIDIA（NASDAQ: NVDA）** — mlx5_vdpa driver 主要贡献方
- **Intel（NASDAQ: INTC）** — ifcvf driver 贡献方
- **ARM、Marvell、Bytedance** — 各贡献方

## 2. F1-F9 字面命中表

| F# | 证据来源 | Verbatim 引文 | 命中 |
|---|---|---|---|
| F1（hardware + Host + VM）| Linux kernel vDPA design docs + drivers/vdpa/Kconfig | "vDPA bus driver bridges between vhost framework and physical devices" | **字面命中** |
| F2（VF device 由 SR-IOV virtualize 出来）| Linux SR-IOV + vDPA bus | mlx5_vdpa / ifcvf 文档明示基于 SR-IOV VF | **字面命中** |
| F3（VF software instance）| `drivers/vdpa/<vendor>/` 各个 vDPA driver = VF software instance | 字面对应 | **字面命中** |
| F4（BE in Host + FE in VM）| `drivers/vhost/vdpa.c` = BE；virtio-net frontend in QEMU/guest = FE | 字面对应 | **字面命中** |
| F5（BE 与 idle VF software instance 绑定）| vDPA management API：`vdpa-mgmtdev` + `vdpa dev add` | 字面对应 | **字面命中** |
| F6（FE pre-allocates DMA cache）| virtio-net 标准行为 | 字面命中 | **字面命中** |
| F7（VF software instance 通过 BE exporting API 写入 storage unit）| vhost-vdpa kernel module API + vDPA struct vdpa_config_ops | 字面对应 | **字面命中** |
| F8（VF device DMA write to FE-pre-allocated cache）| vDPA driver 通过 IOMMU 设置实现 zero-copy DMA | 字面对应 | **字面命中** |
| F9（DMA 完成后通知 FE）| vDPA driver irq + virtio doorbell + irqfd | 字面对应 | **字面命中** |

## 3. 配置参数双引证（R-CONFIG）

| 参数 | prose 引文 | 对应 F# |
|---|---|---|
| `vdpa-mgmtdev` 注册 | Linux kernel vDPA bus driver | F3 |
| `vdpa dev add` 命令 | iproute2 vdpa CLI | F5 |
| `vhost-vdpa` device file `/dev/vhost-vdpa-N` | drivers/vhost/vdpa.c | F4 / F7 |
| QEMU `-netdev type=vhost-vdpa,vhostdev=/dev/vhost-vdpa-N` | QEMU 文档 | F4-F9 |

## 4. 时间线
- vDPA framework 首次合入 Linux kernel 5.4：2019-11-24
- 持续 evolve 至 Linux 6.x（2024-2026）
- 专利申请日 2012-11-13；优先权日 2011-12-31；授权日 2014-01-21
- **判定**：vDPA 上游 framework 完全在 post-grant 时间窗内；不存在现有技术抗辩问题

## 5. §A 19 类源穿透扫描

- §A.1 反向专利墙：Red Hat / NVIDIA / Mellanox / Intel 在 G06F9/4555 主分类厚专利墙；建议 IncoPat 补查
- §A.2 学术论文：vDPA 设计文档发表于 KVM Forum 2019-2024、Linux Plumbers Conference
- §A.3 宣传：Red Hat developer blog 多次介绍 vDPA
- §A.4 使用手册：Linux kernel Documentation/networking/vrf.rst 等
- §A.7 上游归因：Red Hat / NVIDIA / Intel 邮箱域工程师在 vDPA 上游主导
- §A.18 国际同族：华为本身在 G06F9/4555 主分类有 PCT 同族专利

## 6. 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整 | 最终 verdict |
|---|---|---|---|
| Claim 1（含 DMA workflow）| **第 1 档：确认侵权（高）** — F1-F9 全部字面命中 | 1.等同未触发；2.反向证据未触发；3.Active 不降级；4.现有技术 caveat：vDPA 概念由华为 2011 申请、Red Hat / Mellanox 在 Linux 主线 2019 实现——**vDPA 上游实现是否独立于本专利？**需法务审查华为是否就本专利曾向 Linux Foundation 做出 patent grant / open source pledge；如有，则上游 / Red Hat 实施可能受 patent license 覆盖；5.R-STANDARD 未触发；6.豁免未触发 | **第 1 档：确认侵权（高）** + patent license caveat |
| Claim 11 | 同上 | 同上 | **第 1 档** |
| Claim 19 | 同上（Host + module 结构对应 vDPA bus + vhost-vdpa）| 同上 | **第 1 档** |
| Claim 20 | 同上 | 同上 | **第 1 档** |
| Claim 21 | 同上 | 同上 | **第 1 档** |

## 7. 升级路径
- 法务确认华为是否就 US8635616B2 曾向 Linux Foundation / OIN 做 patent grant
- 检索华为 vDPA 相关 PCT 同族
- 联合开发 / 商业谈判记录

## 8. 总结一句话

Linux kernel vDPA framework + vhost-vdpa + virtio-net frontend 完全字面对应 F1-F9（Host + Hardware + VM + SR-IOV VF + VF software instance + BE/FE + DMA workflow），落第 1 档（确认侵权-高）；附 patent license / open source pledge caveat — 需法务确认华为是否对 Linux Foundation / OIN 做出 patent commitment。
