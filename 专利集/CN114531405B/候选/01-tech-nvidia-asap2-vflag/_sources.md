# 证据索引 — 01-tech-nvidia-asap2-vflag

## Phase 1 — WebSearch query 留痕（react 串行）
- query 1: `NVIDIA ASAP2 VF-LAG OVS hardware offload bond`
  → 命中相关。要点：ASAP² 把 OVS 数据面卸载到 ConnectX-5+ 网卡 eSwitch；VF-LAG "creates a single bonded PF port"，"both physical functions of the NIC" 配置为 switchdev 后 bond uplink representors。即单卡双 PF 端口聚合。
- query 2: `NVIDIA VF-LAG offload LAG both physical ports of NIC e-switch single bonded PF port`
  → 再次确认 "single bonded PF port"、"both physical functions of the NIC"、LACP(mode=4) 支持。

## Phase 2 — WebFetch 深抓（串行）
- WebFetch: https://docs.nvidia.com/networking/display/MLNXENv495100/OVS+Offload+Using+ASAP2+Direct
  → verbatim："To enable SR-IOV LAG, both physical functions of the NIC should first be configured to SR-IOV switchdev mode"
  → "Bond modes supported are: Active-Backup, Active-Active, LACP"
  → "SR-IOV VF LAG allows the NIC's physical functions to get the rules that the OVS will try to offload to the bond net-device, and to offload them to the hardware e-switch."
- WebFetch: https://docs.nvidia.com/networking/display/public/SOL/QSG+for+High+Availability+with+NVIDIA+Enhanced+SR-IOV+with+Bonding+Support+(VF-LAG)
  → verbatim："The two network interfaces from the NIC PFs are bounded in the hypervisor."
  → "A single virtual function is backed by two physical bond ports."
  → "BONDING_OPTS=\"mode=4 miimon=100 lacp_rate=1\""（mode=4 = LACP）；"Supported modes are 1, 2, 4."
  → 页面日期：Created 2020-04-16；Last updated 2023-09-12。
  → 无任何"多块独立网卡聚合 / 防网卡卡级故障"描述。

## 关键证据（F1/F5 分歧点）
NVIDIA VF-LAG = 单块网卡(one NIC)的两个物理端口(two physical ports / two PFs) 做 LAG，
对外呈现 "single bonded PF port"。这与本专利 F1/F5 要求的 "N≥2 块独立网卡(NIC card) 聚合
并把精确流表同步卸载到全部 N 块网卡以消除单网卡单点故障" 在架构层级上不同——
VF-LAG 若该单卡故障整 bond 即失效，正是本专利背景技术明确批评的单网卡单点故障。
依据"整数限定外推禁令"（N≥2 块网卡，vendor 仅单卡双端口 N=1 → 不得判字面命中）。

## 工具限制
无付费墙/登录墙；NVIDIA 官方 docs 公开可取，WebFetch 一次成功，未触发 curl 兜底。
