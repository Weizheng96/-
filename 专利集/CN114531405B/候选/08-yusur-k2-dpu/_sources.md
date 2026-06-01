# 证据索引 — 08-yusur-k2-dpu

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| Q1 | 2026-06-01 | WebSearch | `中科驭数 K2 KPU DPU 敏捷网卡 OVS 流表卸载` | 命中：K2/K2-Pro 做 OVN/OVS 流表卸载、网络/存储/RDMA 卸载引擎；但均为通用流表卸载，无多网卡聚合描述 |
| Q2 | 2026-06-01 | WebSearch | `中科驭数 DPU 链路聚合 多网卡 流表 高可靠 卸载 LACP bond` | 命中：Multi-Host（连接多路 CPU）、流表卸载引擎；无 LACP/跨网卡同步卸载/单点故障描述。出现"中科驭数 DPU 网卡硬件流表卸载专利"线索 |
| Q3 | 2026-06-01 | WebSearch | `中科驭数 DPU 网卡 流表 专利 Multi-Host 多网卡 单点故障 冗余` | 无单点故障/冗余/跨网卡内容；Multi-Host 仅为多路 CPU 连接，非链路聚合 |
| Q4 | 2026-06-01 | WebSearch | `中科驭数 DPU网卡硬件流表卸载 专利 ...` | **定位到驭数自有专利 CN119402422A「DPU网卡硬件流表卸载方法、装置、设备及介质」，申请 2024-10，公开 2025-02** |
| F1 | 2026-06-01 | WebFetch | https://www.yusur.tech/solution/networkConvergence | 网络融合方案页：无跨多网卡流表卸载/LACP/miss 同步下发/多网卡冗余描述；仅 Multi-Host 多路 CPU |
| F2 | 2026-06-01 | curl(404) | https://www.sohu.com/a/858776476_121924584 → 404 | 搜狐原文已 404（dead link），仅搜索摘要可见；本地存档 sohu-yusur-flowtable-patent.html 为 404 页 |
| F3 | 2026-06-01 | curl | yusur-CN119402422A.html (Google Patents) | **关键反向证据**：驭数自有流表卸载专利权 1 为单网卡 BPF 字节码驱动卸载；快/默认路径 miss 处理；无 N≥2 多网卡、无 LACP 聚合"第一端口"、无精确流表同步至全部网卡 |

## 受限说明
- WebFetch 抓 Google Patents 报 unknown certificate verification error → 改用 curl UA 兜底成功。
- 搜狐"驭数 DPU 网卡专利"文已 404，仅余搜索引擎摘要；该专利实体经 Google Patents（CN119402422A）核实，机制与本专利不同。
