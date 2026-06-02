# 证据索引 — 01-tech-nvidia-asap2-vflag

## Phase 1 — react 粗筛 query 留痕

- query 1: `NVIDIA ASAP2 VF-LAG OVS hardware offload bond LACP two NICs flow rules`
  → 命中强相关。要点：VF-LAG 让网卡 PF 把 OVS 试图卸载到 bond netdevice 的规则卸载到硬件 e-switch；支持 Active-Backup / XOR / LACP；"both physical functions of the NIC should first be configured to SR-IOV SwitchDev mode, and only afterwards bond the up-link representors"（单卡双 PF）。
- query 2: `NVIDIA ConnectX bond across two separate NICs multi-device LAG eswitch offload not supported same NIC`
  → 命中。"bonding separate NICs with full eswitch offload support is not a supported configuration. The eswitch offload functionality works within a single NIC's embedded switch."（跨独立网卡 + 全卸载不支持）。

## Phase 2 — WebFetch 深抓

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 早于 2023-06-06（ConnectX-5 onwards，MLNX_EN/OFED 多版本） | NVIDIA 官方文档 | https://docs.nvidia.com/networking/display/TAN10110/OVS+Kernel+-+VF+LAG+Configuration | bond 成员示例 `enp3s0f0`+`enp3s0f1`（同一 PCIe 设备 enp3s0 的 f0/f1 两端口=单卡双端口）；支持 LACP/active-backup |
| 2 | 早于 2023-06-06 | NVIDIA 官方文档 | https://docs.nvidia.com/networking/display/MLNXENv543580/OVS+Offload+Using+ASAP²+Direct | "both physical functions of the NIC ... SR-IOV SwitchDev mode"；"offload ... to the hardware e-switch"（单数）；"if both PFs are up, traffic from any VF will split between these two PFs"（同卡两 PF 分流） |
| 3 | — | 搜索聚合（NVIDIA 文档/论坛） | 见 query 2 | "eswitch offload functionality works within a single NIC's embedded switch"；跨独立网卡全卸载不支持 |

## 工具受限说明
- 无付费墙 / 登录墙阻挡；NVIDIA 公开文档可访问。
- 时间窗：NVIDIA ASAP² / VF-LAG 功能与文档早于本专利公开日 2023-06-06 即已公开（属现有/同期的单卡技术形态）。
