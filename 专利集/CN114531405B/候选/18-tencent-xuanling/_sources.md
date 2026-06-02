# 证据索引 — 18-tencent-xuanling

## Phase 1 — 粗筛 query 留痕（react，串行，预算 ≤4 已用满）

- query 1: `腾讯云 玄灵 智能网卡 OVS 流表卸载 多网卡 链路聚合`
  → 命中均为通用 OVS/TC-flower 卸载与 bond/LACP 背景文章（天翼云、知乎、腾讯云开发者社区、阿里云龙蜥），**无一条**触及玄灵网卡"跨多块独立网卡 LACP 聚合 + 流表向全部 N 网卡冗余下发"的区分点。
- query 2: `腾讯 专利 虚拟交换机 多网卡 流表卸载 LACP 逻辑端口 聚合 单点故障`
  → 0 条腾讯专利命中；返回均为 LACP/bond 通用配置与故障排查文章。
- query 3: `Tencent patent smart NIC flow table offload multiple network interface cards LACP logical port aggregation virtual switch`
  → 命中专利为 VMware/Nicira 系（US11606310 "Flow processing offload using virtual port identifiers"、US12192116、US 端口聚合 / NIC aggregation framework 等），**均非腾讯**；无腾讯同主题专利。
- query 4: `腾讯云 玄灵 DPU 智能网卡 架构 白皮书 网络卸载 拓扑 单卡 双网卡`
  → 未检索到玄灵官方白皮书 / 拓扑说明；仅通用 DPU/SmartNIC 综述。无法确认玄灵是单卡还是多卡形态。

## 证据索引表

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | - | 通用科普 | https://cloud.tencent.com/developer/article/1892174 | 智能网卡 OVS/TC-flower 卸载通用机制，无玄灵跨卡聚合区分点 |
| 2 | - | 通用科普 | https://cloud.tencent.com/developer/article/2526271 | DPU/SmartNIC 综述，无玄灵拓扑/流表下发机制 |

## 结论
腾讯为闭源大厂，玄灵网卡公开度低。4 条 query 累计**未检索到任何描述玄灵实现本专利区分机制（跨独立网卡 LACP 聚合 + 流表向全部网卡冗余下发以消除单网卡单点故障）的一手公开材料**，亦无腾讯同主题专利。无正向命中、亦无任何针对玄灵的反向事实（未见"玄灵仅单卡 / 玄灵明示用另一套机制"之类正向否定）。→ 判公开资料不足（弱候选），Phase 1 早剪枝，不进 Phase 2。

## 工具受限说明
玄灵为闭源自研芯片，官方未公开架构白皮书；公开渠道仅有通用 DPU 科普文，无产品级拓扑 / 流表下发机制描述。
