# 05-marvell-octeon10 — 合议结果

## 候选基本信息
- 候选 NN：05 · 类型：产品
- 名称：Marvell OCTEON 10 DPU OVS 卸载
- 组织 / vendor：Marvell（整机集成商如 Asterfusion）
- 公开度：中 · 初判命中 F#（待复核）：F1, F2, F4, F5
- 时间窗：专利授权公告日 2023-06-06；OCTEON 10 / OCTEON DPU OVS 卸载产品在此前后均有公开（OCTEON 10 2023-12 推出新型号），时间不构成排除理由。

## 检索粗筛
见 `_sources.md`。Phase 1 共 4 条 WebSearch + Phase 2 共 2 条 WebFetch，全部留痕。

## F# 命中表

| F# | 限定 | 判定 | 证据 verbatim / 说明 | URL | 备注 |
| --- | --- | --- | --- | --- | --- |
| F1 | 多虚机 + 多网卡架构 N≥2（**N 张独立网卡**） | **不命中** | OCTEON SmartNIC 为单卡设备（"24-core ARM processors with 2 ×100G QSFP28 ports"，同一张卡上的两个物理口）。公开资料未见 vSwitch 把 N≥2 张**独立网卡**纳入同一卸载域。双 DPU 整机中两 DPU 为"separate compute entities"，各自独立 OS，非同一 vSwitch 下的 N 张聚合网卡。 | cloudswit.ch/product/...cn9670-ovsnfv-offload/ ; cloudswit.ch/product/sonic-switch-...cn9130-dpu/ | N≥2 独立网卡不满足 |
| F2 | N 个逻辑端口聚合为"第一端口" | **不命中 / 公开资料不足** | 业界 OVS+LAG offload 标准范式（SR-IOV VF LAG）是**单卡内两口** bond 成一个 bonded PF（如 enp3s0f0+enp3s0f1，同一张卡）。未见 OCTEON 把跨卡的多个逻辑端口聚合为一个第一端口。 | docs.nvidia.com/...OVS+Offload+Using+ASAP²+Direct ; cloudswit.ch/...cn9670... | 仅单卡双口聚合，非跨卡 |
| F3 | 每网卡逻辑端口由其物理端口基于 LACP 聚合 | **未证实** | LAG/bonding 存在，但公开资料未明确"每张独立网卡先各自 LACP 聚合形成逻辑端口、再跨卡聚合为第一端口"的两级结构。 | docs.nvidia.com/...ASAP² | 公开资料不足 |
| F4 | 卸载流表 miss 触发卸载 | **命中（通用语义）** | OVS 硬件卸载即 cache-miss-driven offload：首包上送 host 学习流，后续把流规则下发到硬件 datapath（TC flower）。OCTEON 支持 OVS offload。 | developers.redhat.com/...tracing-hardware-offload-open-vswitch ; marvell.com/products/data-processing-units.html | 此特征为 OVS 卸载行业通用，非专利独占 |
| F5 | 精确流表卸载至**全部 N 个网卡** | **不命中 / 反向** | 现有文献聚焦**单 SmartNIC**，host 控制面把流表同步到**一块**硬件设备；"把同一精确流表同步卸载至 N 张全部网卡以消除单点故障"未标准化、未检索到实现。双 DPU 整机的冗余由**交换芯片层 MC-LAG**（Prestera ASIC）实现，未见两 DPU 间流表同步。 | developers.redhat.com/...tracing-hardware-offload ; hareshkhandelwal.blog/...openvswitch-hardware-offload ; cloudswit.ch/product/sonic-switch-...cn9130-dpu/ | 核心创新点缺失 + 双卡冗余为不同机制 |

## 已检查文档清单
1. Marvell DPU 产品页 — https://www.marvell.com/products/data-processing-units.html
2. Asterfusion OCTEON DPU 平台综述 — https://cloudswit.ch/blogs/marvell-octeon-devices-power-edge-computing/
3. Asterfusion OCTEON TX CN9670 OVS/NFV offload SmartNIC（WebFetch 深抓）— https://cloudswit.ch/product/asterfusion-dpu-based-smartnic-marvell-octeon-tx-cn9670-ovsnfv-offload/
4. 双 OCTEON CN9130 DPU SONiC 整机（WebFetch 深抓）— https://cloudswit.ch/product/sonic-switch-add-marvell-octeon-tx2-cn9130-dpu/
5. NVIDIA OVS Offload ASAP² Direct（VF LAG 单卡双口范式）— https://docs.nvidia.com/networking/display/MLNXOFEDv531001/OVS+Offload+Using+ASAP%C2%B2+Direct
6. Red Hat: Tracing hardware offload in OVS（cache-miss-driven offload 语义）— https://developers.redhat.com/articles/2021/12/10/tracing-hardware-offload-open-vswitch
7. OVS 硬件卸载原理博客 — https://hareshkhandelwal.blog/2020/03/11/lets-understand-the-openvswitch-hardware-offload/

## 最终判定

**第 5 档：已排除**

依据（1-3 句）：
1. 权 1 的核心创新点 F1+F2+F5——"vSwitch 把 **N≥2 张独立网卡**基于 LACP 聚合为一个第一端口、并在 miss 时把**同一精确流表同步卸载至全部 N 张网卡**以消除单卡单点故障"——在 OCTEON OVS 卸载公开资料中**找到真反向证据**：OCTEON SmartNIC 为单卡设备，业界 OVS+LAG offload 标准范式是单卡内两口 bond（非跨独立网卡），且现有文献明确流表卸载面向单 SmartNIC、无"同步到全部 N 卡"机制。
2. 双 OCTEON DPU 整机虽有两张卡，但其冗余由**交换芯片层 MC-LAG（Prestera ASIC）**实现，两 DPU 为独立计算实体、无 vSwitch 跨卡流表同步——属**不同机制（architecture different）**，非权 1 的卸载控制面方案。
3. 唯一命中的 F4（cache-miss-driven offload）是 OVS 硬件卸载的行业通用语义，不构成对本专利独占特征的落入。

> 注：本判定为"已排除"是基于真反向证据（单卡范式 + 文献明确单 SmartNIC 卸载）与架构不同（MC-LAG ≠ vSwitch 跨卡流表同步），而非仅 0 命中。若后续出现 OCTEON 官方文档明确描述"vSwitch 跨 N 张独立网卡 LACP 聚合 + 流表向全部网卡同步卸载"的实现，应重新评估升级至 3/4 档。

## 总结一句话
Marvell OCTEON OVS 卸载是单卡范式、双卡冗余靠交换芯片 MC-LAG（不同机制），缺失权 1 核心的"N≥2 独立网卡 + 流表同步卸载至全部网卡"，且有真反向证据，落第 5 档（已排除）。
