# 证据索引 — 16-asterfusion-helium

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2023-06-02 | 官网 blog | https://asterfusion.com/blog20230602-smartnic-open-source/ | Helium 单块 DPU 智能网卡（Marvell OCTEON CN9670），OVS/百万级流表卸载；无跨卡聚合/流表冗余 |
| 2 | — | 官网 blog | https://asterfusion.com/blog20230601-dpu-open-source-100-200g/ | 数据中心部署开源 DPU 网卡，单卡形态 |
| 3 | — | GitHub | https://github.com/asterfusion/Helium_DPU/blob/main/README.en.md | 仅单块 SmartNIC 功能；无多网卡/LACP/链路聚合/跨卡流表复制/failover |

## Phase 1 — react 粗筛 query
- query 1: `Asterfusion Helium DPU OVS offload smart NIC flow table` → 命中相关（官网 blog20230602/20230601 + GitHub asterfusion/Helium_DPU + cloudswitch 产品页）。确认 Helium 是基于 Marvell OCTEON CN9670 的单块 DPU 智能网卡，支持 OVS / 百万级流表卸载。
- query 2: `Asterfusion Helium DPU LACP bond multiple SmartNIC cross-card link aggregation flow table redundancy` → 命中同一批材料；明确声明"搜索结果未包含 LACP bond / 跨卡链路聚合 / 流表冗余的具体实现信息"。即专利核心区分点（跨多卡 LACP + 流表向全部网卡冗余下发）无公开资料支撑。

## Phase 2 — WebFetch 深抓
- WebFetch GitHub README.en.md → 仅描述单块 SmartNIC 功能；明确无：多网卡配置 / LACP / 链路聚合 bond / 跨卡流表复制 / 高可用 failover / 单点故障缓解。
- WebFetch blog20230602（发布日 2023-06-02）→ 四项核心特征（跨卡 LACP 聚合 / 流表向全部网卡冗余下发 / vSwitch 连 M VM+N 网卡 / first-packet miss 触发 exact 流表下发）均未提及；仅单卡 OVS 卸载。

## 工具 / 资料限制
- 未检索到任何描述"多块独立 Helium 网卡 + 跨卡 LACP 聚合 + 流表向全部网卡冗余下发"的公开材料。官网 / GitHub / 第三方产品页均为单卡形态叙述。
- 时间窗：核心 blog 发布日 2023-06-01 / 2023-06-02，略早于专利授权日 2023-06-06；但因架构层面缺核心机制证据，时间非本次定档主因。
