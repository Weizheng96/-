# 证据索引 — 04-risingwave

候选：RisingWave / RisingWave Labs / 产品（开源 streaming SQL 数据库）
专利公开（授权）日基准：2020.05.08

## Phase 1 — react 粗筛 WebSearch query 留痕（串行）
1. `RisingWave SQL streaming query logical plan physical plan fragment actor architecture`
   → 命中：SQL→parse→logical plan→physical graph→fragment（stream fragmenter @ meta service）→actor；meta node 实例化为 actor 分配给 compute node。强信号，无早剪枝。
2. `RisingWave meta node compute node architecture CREATE SOURCE CREATE SINK connector streaming SQL`
   → 命中：四类节点（含 Meta Node / Compute/Streaming Node）；CREATE SOURCE / CREATE SINK 纯 SQL 定义 source/sink connector（Kafka/CDC/Iceberg 等）；materialized view 为核心抽象。
3. `RisingWave CREATE SOURCE Kafka CREATE SINK SQL documentation source ingest sink deliver`
   → 命中：CREATE SOURCE = 从外部上游（Kafka 等）摄取输入流；CREATE SINK = 把结果写到外部下游目标；三条 SQL（SOURCE→MV→SINK）组成完整管线。

## Phase 2 — react 深抓 WebFetch（逐个串行）+ curl 落盘

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | RisingWave 现行设计文档 | 设计文档 | https://risingwavelabs.github.io/risingwave/design/streaming-overview.html · streaming-overview.html | F2/F3/F4：stream plan=logical plan；stream fragmenter @ meta service 把 logical stream plan 拆成 fragment（每 fragment 持有 stream plan 的 partial nodes）；meta service 把 fragment 分发到 compute node，actor 为最小调度单元 |
| 2 | RisingWave 官方架构文档 | 官方文档 | https://docs.risingwave.com/get-started/architecture · architecture.html | F3/F4：fragmenter 把 execution plan 拆成 fragments（"groups of execution nodes that share the same data distribution"）；Meta Node 把 query 实例化为 actors 并分配到 Compute Nodes；Streaming/Compute Node 执行 streaming queries |
| 3 | RisingWave SQL 命令文档 | 官方文档 | https://docs.risingwave.com/sql/commands/sql-create-source · create-source.html | F1/F5：CREATE SOURCE（SQL + WITH connector）从外部上游（Kafka 等）读取输入流；配合 CREATE SINK 写到外部下游 |

落盘验证：streaming-overview.html 为 32KB 静态页，已 Grep 验证 fragmenter/actor/compute node verbatim 存在；architecture.html / create-source.html 为 SPA 大文件（已落盘）。

## 时间窗说明
RisingWave 公司成立 2021、v1.0 GA 2023、v2.0 2024——全部晚于 2020.05.08，材料均在时间窗内。
