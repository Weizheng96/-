# 06-confluent-ksqldb — 检索留痕 (_sources.md)

## Phase 1 — react 粗筛 WebSearch query 留痕
1. `ksqlDB SQL query logical plan physical plan topology execution Kafka Streams`
   → 命中：Confluent 官方文档 how-it-works、Confluent blog "ksqlDB Execution Plans"、EXPLAIN 文档。确认 SQL→AST→logical plan→physical plan(Kafka Streams topology) 全链路存在。强信号，缩小特征词。
2. `ksqlDB EXPLAIN statement execution plan topology source sink CREATE STREAM connector`
   → 命中：EXPLAIN 文档（execution plan = DAG of steps；StreamSelect/StreamFilter/StreamGroupBy/StreamAggregate 等）、source/sink connector 注册、CREATE STREAM 物理 topology。

（粗筛 2 条即获强信号 → 直接进 Phase 2，未触发早剪枝。）

## Phase 2 — react 深抓 WebFetch
- WebFetch https://www.confluent.io/blog/building-ksqldb-event-streaming-database/
  → "execution plan ... is a DAG of steps"；"ksqlDB builds the final Kafka Streams topology from the execution plan by building the steps, starting with the root"。**发布日期 May 1, 2020 → 早于专利公开日 2020.05.08，单独不计入证据**（仅作背景佐证）。
- WebFetch https://docs.confluent.io/platform/current/ksqldb/operate-and-deploy/how-it-works.html （current 版文档，持续维护，反映 2020.05.08 之后产品状态）
  → "ksqlDB uses the AST and creates the logical plan for your statement."
  → "From the logical plan, the ksqlDB engine creates the physical plan, which is a Kafka Streams DSL application with a schema."
  → "Each ksqlDB Server instance runs a ksqlDB engine. Under the hood, the engine parses your SQL statements and builds corresponding Kafka Streams topologies."
  → "There's no master node or coordination among them required."（F4 架构相关——反向信号）
  → CREATE STREAM/CREATE TABLE 指定 backing Kafka topic；CREATE TABLE AS SELECT 持久查询 "writes continuously to its output topic"。
- WebFetch https://docs.confluent.io/platform/current/ksqldb/developer-guide/ksqldb-reference/explain.html
  → EXPLAIN 输出 Execution Plan（PROJECT/AGGREGATE/REKEY/SOURCE 步骤）+ Processing Topology（Source/Processor/Sink 节点 DAG），例如 "Source: KSTREAM-SOURCE-0000000000 (topics: [clickstream]) --> KSTREAM-MAP-0000000001"。

## 落盘文件
- ksqldb-how-it-works.html (180KB, 真实正文，已 Grep 校验 "creates the logical plan"/"creates the physical plan"/"no master node"/"parses your SQL" 均 verbatim 命中，非 WebFetch 幻觉)
- ksqldb-explain.html (139KB, 真实正文)

## 时间窗说明
- 专利公开（授权）日 2020.05.08。current 版官方文档为持续维护文档，反映授权日之后的产品状态，计入证据；2020-05-01 的 blog 早于授权日，仅作背景。
