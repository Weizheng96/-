# 证据索引 — 20-aws-nitro-card

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | (官方文档) | WebSearch | https://docs.aws.amazon.com/whitepapers/latest/security-design-of-aws-nitro-system/the-components-of-the-nitro-system.html | Nitro Card for VPC 做 VPC 数据面卸载（封装/解封装、Security Group、路由），但未提跨多卡 LACP 聚合 / 流表冗余下发 |
| 2 | 2024-06-28 | WebFetch | https://dev.to/choonho/nitro-card-why-aws-is-best-46ph | **强反向**："no redundancy for Nitro Card failure"；"AWS Nitro Server does not make bonding interface"；"two Nitro Cards, 1x primary and 1x networking"（网络面仅 1 卡） |

## Phase 1 — react 粗筛 query 留痕
- query 1: `AWS Nitro card VPC data plane flow table offload multiple NICs LACP architecture` → 命中 AWS 白皮书/servethehome/mvdirona；确认 VPC 数据面卸载，但未见跨多卡 LACP 聚合或流表向全部卡冗余下发。信号：中（场景相关，机制存疑）。
- query 2: `AWS Amazon patent virtual switch flow table offload multiple network interface cards LACP link aggregation redundancy` → 命中 LACP 专利均为第三方且多为 2014 前现有技术；AWS Outposts 的 LACP 仅是与客户外部交换机间聚合，非主机内跨多卡聚合。无 AWS 自有同主题专利。信号：弱/无关。
- query 3: `AWS Nitro multiple cards per instance ENA redundancy network card failure single point host` → 命中关键反向材料（DEV Community, 2024-06-28）。信号：强反向。

## Phase 2 — WebFetch 深抓
- WebFetch https://dev.to/choonho/nitro-card-why-aws-is-best-46ph （发布日 2024-06-28，晚于授权日 2023-06-06，为有效现时证据）verbatim 反向证据：
  - "no redundancy for Nitro Card failure"
  - "Commodity server usually make bonding interface coupling two physical interfaces to single logical interface. But AWS Nitro Server does not make bonding interface."
  - "There are two Nitro Cards, 1x primary and 1x networking."（网络面仅 1 卡）

## 工具受限说明
- AWS 为闭源大厂，VPC 数据面流表内部拓扑无一手公开实现细节；未检索到 AWS 自有同主题（跨卡 LACP + 流表冗余下发）专利或论文。判定主要依据 vendor 架构的正向反向事实（不做 bonding / 单网络卡 / 卡故障无冗余）。
