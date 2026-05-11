# 候选：Linux 发行版集合（Debian / Ubuntu / SUSE / 麒麟 / 统信）

## 候选标识
- candidate_slug: `28-linux-distros`
- 主体类型：A. vSwitch 软件方（次级商业发行版）
- 适用独立权：权 36（介质权）

## §A 摘要

各发行版打包 mainline kernel + OVS 上游 + DPDK 上游——能力继承自上游（已排除 — 候选 01 / 02 / 03）。

| 发行版 | 备注 |
| --- | --- |
| Debian / Ubuntu | mainline kernel + OVS 上游；无主动推荐"多 NIC + LACP + sync flow"配置 |
| SUSE | 同上；Harvester 用 mainline + KubeVirt |
| 麒麟（Kylin） | 国产 OS；信创目录；mainline kernel 派生 |
| 统信 UOS | 同上 |
| Canonical Charmed OpenStack | mainline + OVS；用 active-backup 默认 |

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整 | 最终 verdict |
| --- | --- | --- | --- |
| 权 36 | **公开资料不足（第 4 档弱候选）** | 上游已排除（OVS / Linux bonding 都不实现 F3+F4 sync），发行版只是被动 ship；按 R-3 双层激活商业发行版独立评估，但 0 命中"主动推荐"档证据 | **公开资料不足（第 4 档弱候选）** |

## 总结一句话

Linux 发行版（Debian/Ubuntu/SUSE/麒麟/统信）能力继承自已排除的上游，无主动推荐"F1-F4 组合配置" — **落第 4 档公开资料不足弱候选**。
