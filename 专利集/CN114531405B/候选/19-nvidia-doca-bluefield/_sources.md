# 候选 #19 NVIDIA DOCA / VF-LAG / BlueField — 资料索引

**主体类型**：芯片厂（BlueField DPU / ConnectX）+ 软件发布方（DOCA SDK / MLNX_OFED / OVS-DOCA）
**适用独立权**：权 35（芯片系统）+ 权 36（计算机存储介质）
**取证日期**：2026-04-27

---

## 五类源扫描结果

### 1. 专利
- WebSearch query：`NVIDIA Mellanox patent assignee 流表 multi-NIC LACP bond OVS offload site:patents.google.com 2023 2024 2025`
- **结果**：0 命中本方向。返回的 NVIDIA 专利集中在 GPU 渲染 / 多 GPU 同步 / 网络包加速等通用方向，无"多 NIC + LACP + 同表分发"
- **结论**：NVIDIA 在该方向无公开专利布局指向

### 2. 学术论文
- WebSearch query：`NVIDIA BlueField DPU SIGCOMM OR NSDI OR APNet OR EuroSys paper multi-DPU bond LACP same-flow distribution 2024 2025`
- **结果**：0 命中。返回的全是 NVIDIA 产品页 / 营销材料
- **结论**：NVIDIA 未在顶会发表过 multi-DPU 同表分发论文

### 3. 宣传材料 + 4. 使用手册（合并归档，5 份）
本地存档：
- `ovs-dpdk-hw-offloads-doca.html`（91 KB）— DOCA SDK 文档：OVS-DPDK Hardware Offloads
- `vf-lag-qsg.html`（164 KB）— Networking 文档：VF-LAG QSG（关键反向证据"single NIC"）
- `bluefield3-datasheet.pdf`（586 KB）— BlueField-3 DPU datasheet
- `ovs-doca-acceleration.html`（512 KB）— DOCA SDK 文档：OVS-DOCA Hardware Acceleration（v2.10.0）
- `asap2-direct-ovs-offload.html`（554 KB）— MLNX_OFED 文档：OVS Offload Using ASAP² Direct
- 来源：[docs.nvidia.com/doca](https://docs.nvidia.com/doca/)、[docs.nvidia.com/networking](https://docs.nvidia.com/networking/)、[NVIDIA BlueField-3 datasheet](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/documents/datasheet-nvidia-bluefield-3-dpu.pdf)

### 5. 行业标准
- IEEE 802.3ad LACP：BlueField DPU 在硬件层面通过 ASAP² eSwitch 支持，但**仅在单 NIC 双 port 范围内**（VF-LAG 限定）
- DOCA / IPDK 不引入新的多 NIC 二级聚合标准
- **结论**：NVIDIA 仅实现单 NIC 内 LACP，没有跨 NIC 的二级聚合标准

---

## 子 agent 审阅分配
- `vf-lag-qsg.html` → 子 agent A（**关键文档**：VF-LAG 的"single NIC" 限制）
- `ovs-dpdk-hw-offloads-doca.html` → 子 agent B（OVS-DPDK 卸载架构）
- `bluefield3-datasheet.pdf` → 子 agent C（BlueField-3 硬件能力）
- `ovs-doca-acceleration.html` → 子 agent D（OVS-DOCA v2.10.0 硬件加速）
- `asap2-direct-ovs-offload.html` → 子 agent E（ASAP² Direct 卸载）
