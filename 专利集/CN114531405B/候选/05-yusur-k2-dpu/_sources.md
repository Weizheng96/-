# 证据索引 — 05-yusur-k2-dpu

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | - | 搜索 | query: `中科驭数 Yusur K2 DPU OVS 流表卸载 bonding LACP 网卡` | 确认 K2/K2-Pro 提供 OVS/OVN 流表卸载（云原生 SDN）；未见跨网卡 LACP / 流表向全部网卡下发 |
| 2 | - | 搜索 | query: `中科驭数 DPU 双网卡 跨网卡 LACP 链路聚合 流表卸载 单点故障 冗余` | SWIFT-2200N 为"双端口"单卡；未找到跨多块物理网卡 LACP 聚合 + 单点故障冗余流表卸载 |
| 3 | - | 搜索 | query: `中科驭数 专利 流表卸载 网卡 链路聚合 patent Yusur flow table offload NIC` | 命中 Kube-OVN "Offload with YUSUR" 文档；未检索到 Yusur 自有同主题专利 |
| 4 | - | 搜索 | query: `中科驭数 K2-Pro DPU bonding 网卡 主备 双卡 流表 全部网卡下发 高可用` | K2-Pro 发布稿（流表/RDMA 卸载、P4 可编程）；无 bonding/主备/双卡/流表全网卡下发细节 |
| 5 | 2024-08-13 / 2025-07-21 | WebFetch | https://kubeovn.github.io/docs/v1.13.x/en/advance/offload-yusur/ | 仅描述**单卡**卸载：2200E 两物理端口"select one"，单 PF 配 SR-IOV VF；**无** bonding/LACP/多卡/流表跨卡下发 → 单卡形态反向信号（K8s 卸载配置文档，非产品级明示拒绝） |

## 工具受限说明
- 未访问 CNIPA / Google Patents 上 Yusur 自有专利全文（query 3 未直接命中其同主题专利）。升级取证路径：Google Patents 按申请人"中科驭数/Yusur"+ H04L45 检索 2023-06-06 后申请件。
- F2/F3（跨网卡 LACP→第一端口）与 F5（流表向全部 N 网卡下发）均无公开命中；F4/F5 的单卡 OVS 流表卸载机制有命中。整数下界 N≥2 跨卡形态无公开材料，不外推为字面命中。
