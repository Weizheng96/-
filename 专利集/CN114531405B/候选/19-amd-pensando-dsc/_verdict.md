# 候选：AMD-Pensando DSC + HPE Aruba CX 10000

## 候选标识
- candidate_slug: `19-amd-pensando-dsc`
- 主体类型：B. SmartNIC / DPU 硬件方
- 适用独立权：权 35 + 权 23/33

## §A 主流来源摘要

### §A.4（命中 — 反向证据）

| # | 源 | URL | 引文 |
| --- | --- | --- | --- |
| 1 | WWT — Pensando: Beyond a Smart NIC | https://www.wwt.com/article/pensando-beyond-a-smart-nic | "servers can support multiple PCIe devices, however **none of Pensando's customers have a defined use case that requires more than one DSC**" |
| 2 | AMD Pensando DSC2-200 product brief | https://www.amd.com/content/dam/amd/en/documents/pensando-technical-docs/product-briefs/pensando-dsc-200-product-brief.pdf | 2023-06 — 单卡产品定位 |
| 3 | Aruba CX 10000 datasheet | https://www.amd.com/content/dam/amd/en/documents/pensando-technical-docs/data-sheets/aruba-cx-10000-series-datasheet.pdf | DPU **inside the ToR switch**，不是 host-side |
| 4 | HPE Aruba AOS-CX VSX guide | https://arubanetworking.hpe.com/techdocs/AOS-CX/10.15/PDF/vsx.pdf | VSX-LAG = 交换机层 chassis HA，不是 host 多 NIC sync |

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整记录 | 最终 verdict |
| --- | --- | --- | --- |
| 权 23 / 33 / 35 | **已排除（第 5 档 — 架构层级不符）** | F1 真反向 "no customer use case requires more than one DSC"；架构 off-axis（DPU 在 switch 而非 host 内） | **已排除（架构层级不符 — DPU-in-switch vs 本专利 host-side DPU）** |

### F# 投票汇总

- F1：Pensando 自身明示 ≥ 1 DSC per host 的客户 use case 不存在；Aruba CX 10000 是 ToR 交换机内 DPU，与本专利 host 内 vSwitch + 多 NIC 拓扑不同抽象层
- F2-F4：架构 off-axis，不展开

### 最终 verdict

**已排除（架构层级不符 R-7）**：AMD-Pensando 在 host 多卡场景 vendor 自己声明无客户 use case；Aruba CX 10000 是 in-switch DPU 模型——与本专利 host-side vSwitch + 多 NIC sync 完全不在同一抽象层。

## 总结一句话

Pensando 自承 host 多 DSC 无客户 use case + Aruba CX 10000 是 ToR-内 DPU——架构层级不符，**落第 5 档已排除**。
