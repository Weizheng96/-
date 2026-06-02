# 证据索引 — 15-cloudvein-metafusion

候选：云脉芯联 metaFusion-200 100G DPU（OVS 卸载 + RDMA）
专利公开（授权）日：2023-06-06（时间窗起算）

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2023-01-05 | 新闻 | https://www.jiemian.com/article/8691691.html | metaFusion-200=2口100G RDMA 智能网卡(DPU)；集成 OvS 虚拟化网络卸载+RDMA；**单卡双口**，未提多卡/跨卡 LACP/冗余下发 |

## Phase 1 — react 粗筛 WebSearch 留痕

- query 1: `云脉芯联 metaFusion-200 DPU OVS 卸载 多网卡 流表`
  → 命中相关。确认 metaFusion-200 = 国内首款 FPGA 平台集成 OVS 虚拟化网络卸载 + RDMA 的 100G DPU；OVS 控制面放 SoC 片上 CPU，硬卸载。未见"跨多块独立网卡聚合 / 流表向全部网卡下发"描述。
- query 2: `云脉芯联 metaFusion DPU OVS 卸载 LACP 链路聚合 bond 多块网卡 流表下发`
  → 0 命中 vendor 专属信息；仅返回通用 OVS bonding / LACP / DPU 卸载科普（Red Hat / SDNLAB / 知乎等），与候选实际架构无关。
- query 3: `云脉芯联 专利 智能网卡 流表 卸载 链路聚合 虚拟交换机`
  → 命中公司概况（YSA-100 芯片、metaScale/metaConnect 系列），未检索到云脉芯联在本主题（跨多卡流表卸载）的公开专利申请。
- query 4: `云脉芯联 metaFusion-200 OvS 虚拟化网络卸载 RDMA 100G DPU 产品 架构 单卡 双口`
  → 多源一致确认：产品为**单块 FPGA DPU 卡，支持 2×100G（双口）**；同系列 metaConnect-200 亦为 2×100G 单卡。无"多块独立网卡 / 跨卡冗余 / 流表向全部网卡下发"描述。

## Phase 2 — WebFetch 留痕

- WebFetch https://www.jiemian.com/article/8691691.html （2023-01-05 发布，早于授权日，仅作架构定性参考）
  → verbatim：「支持 2 口 100G RDMA 智能网卡」「集成 OvS 虚拟化网络卸载功能和 RDMA 存储网络功能于一体」。未提及多网卡链路聚合(LACP)、跨网卡冗余、流表下发至多块网卡。确认产品为单卡双口形态。

## 工具受限 / 局限说明

- 云脉芯联官网 (yunsilicon.com) 产品详情多为发布通告 / SPA 壳，未检索到公开 datasheet / 白皮书 PDF 直链，无法获得 vendor 一手详细拓扑文档。
- 未检索到云脉芯联在"跨多块独立网卡流表卸载 + LACP 聚合 + 冗余下发"主题下的公开专利申请。
- 结论性架构判定基于多源新闻一致描述（单卡双口），而非 vendor 一手技术规格书；属"公开资料不足"性质，非正向反向证据。
