# 检索留痕 — 05-marvell-octeon10

候选：Marvell OCTEON 10 DPU OVS 卸载（vendor: Marvell）
公开日时间窗：> 2023-06-06（专利授权公告日）
初判命中 F#：F1, F2, F4, F5

## Phase 1 粗筛（WebSearch 串行）

1. query: `Marvell OCTEON 10 DPU OVS hardware offload flow table`
   - 命中：确认 OCTEON 10 / OCTEON DPU SmartNIC 支持 OVS offload、VTEP、TCP offload、GRE/GTP 隧道、NFV（vSwitch/防火墙/负载均衡）卸载。含 VPP 引擎、集成 1Tbps switch。
   - 信号：OVS 硬件卸载存在（F4 cache-miss-driven offload 为 OVS 卸载通用语义），但无"跨多块独立网卡 + 流表同步全部网卡"描述。
   - 来源：
     - https://www.marvell.com/products/data-processing-units.html
     - https://cloudswit.ch/blogs/marvell-octeon-devices-power-edge-computing/
     - https://cloudswit.ch/product/asterfusion-dpu-based-smartnic-marvell-octeon-tx-cn9670-ovsnfv-offload/

2. query: `Marvell OCTEON OVS offload bonding LAG multiple NIC cross-card redundancy`
   - 命中：业界 OVS offload + LAG/bonding 的标准实现（SR-IOV VF LAG）是**单卡内两个物理口** bond 成一个 bonded PF（如 ConnectX-5 的 enp3s0f0 + enp3s0f1，同一张卡）。未见 OCTEON 跨多块独立网卡 bond。OCTEON TX CN9670 为单卡 2×100G QSFP28。
   - 信号：反向——LAG offload 的标准范式是单卡双口，非"跨 N 张独立网卡"。
   - 来源：
     - https://docs.nvidia.com/networking/display/MLNXOFEDv531001/OVS+Offload+Using+ASAP%C2%B2+Direct
     - https://cloudswit.ch/product/asterfusion-dpu-based-smartnic-marvell-octeon-tx-cn9670-ovsnfv-offload/

3. query: `OVS hardware offload flow table sync across two separate SmartNIC cards single point of failure redundancy`
   - 命中：现有文献聚焦**单 SmartNIC** 部署，host 控制面把流表同步到一块硬件设备。多 SmartNIC 流表同步 / 双卡冗余 / 跨卡消除单点故障**未标准化、未检索到具体实现**。
   - 信号：反向——"流表同步到全部 N 张网卡"这一核心机制在公开文献中不存在。
   - 来源：
     - https://developers.redhat.com/articles/2021/12/10/tracing-hardware-offload-open-vswitch
     - https://hareshkhandelwal.blog/2020/03/11/lets-understand-the-openvswitch-hardware-offload/

4. query: `Marvell OCTEON DPU dual card high availability failover virtual switch redundancy two NIC`
   - 命中：双 OCTEON DPU 整机（如 Asterfusion CX102S-16GT-DPU-M-SWP，含 2 张 CN9130 DPU 卡 + Marvell Prestera MV-DX2556 交换芯片）通过 **MC-LAG** 实现冗余/active-active，并由 BFD/OSPF/BGP 等做 sub-50ms 故障切换。
   - 信号：反向/架构不同——双卡冗余靠**交换芯片层 MC-LAG**，不是"vSwitch 把 N 张网卡聚合为第一端口 + miss 触发把同一精确流表卸载至全部 N 卡"。
   - 来源：
     - https://cloudswit.ch/product/sonic-switch-add-marvell-octeon-tx2-cn9130-dpu/

## Phase 2 深抓（WebFetch 串行）

A. https://cloudswit.ch/product/asterfusion-dpu-based-smartnic-marvell-octeon-tx-cn9670-ovsnfv-offload/
   - 单卡 2×100G QSFP28；支持 OVS offload、SR-IOV、NFV。
   - 未描述：跨多块独立网卡聚合 / LACP 跨卡 / 流表跨卡同步 / 跨卡冗余。
   - 结论：单卡设备，OVS 卸载局限于单卡，无 F1/F5 的"N≥2 独立网卡 + 流表卸载至全部网卡"。

B. https://cloudswit.ch/product/sonic-switch-add-marvell-octeon-tx2-cn9130-dpu/
   - 两张 OCTEON DPU 作为**独立计算实体**（一张 OpenWrt、一张 Ubuntu/Debian），各自独立运行。
   - 冗余表述为通用 MC-LAG（交换芯片 L2/L3 能力），**未描述两 DPU 间流表/转发规则同步**，未描述一卡故障时另一卡接管的 vSwitch 流表机制。
   - 结论：架构不同——MC-LAG（交换 ASIC 层）≠ 权 1 的 vSwitch 跨网卡流表同步卸载。

## 受限说明
- 未检索到 OCTEON 公开资料显示"vSwitch 把 N≥2 张独立网卡基于 LACP 聚合为第一端口、并在 cache miss 时把同一精确流表同步卸载至全部 N 张网卡"。
- 双卡场景下的冗余机制为交换芯片层 MC-LAG，属不同机制（switch fabric redundancy），非权 1 的卸载控制面机制。
