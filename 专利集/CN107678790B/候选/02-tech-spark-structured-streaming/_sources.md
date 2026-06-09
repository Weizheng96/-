# 证据索引 — 02-tech-spark-structured-streaming

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| WebSearch-1 | 2026.06 检索 | query | `Spark Structured Streaming SQL query Catalyst logical plan physical plan whole-stage codegen` | 命中逻辑计划→物理计划→codegen，强信号 |
| WebSearch-2 | 2026.06 检索 | query | `Spark Structured Streaming spark.sql readStream writeStream source sink connector Driver Executor scheduling` | source/sink、driver/executor 协调，强信号 |
| WebSearch-3 | 2026.06 检索 | query | `Databricks Delta Live Tables CREATE STREAMING TABLE SQL define streaming pipeline source sink` | 纯 SQL 定义流作业（F1/F2 关键限定），强信号 |
| L1 | 文档 latest（Spark 4.1.2，机制自 2.x 持续公开） | 官方文档 | https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-streaming-table ｜本地 create_streaming_table_databricks.html | F1/F2/F5：纯 SQL `CREATE STREAMING TABLE … AS SELECT … FROM STREAM read_kafka(...)` |
| L1 | 发布 2022-07-11 | 技术深析 | https://dataninjago.com/2022/07/11/spark-structured-streaming-deep-dive-5-incrementalexecution/ ｜本地 incrementalexecution_dataninjago.html | F2/F3：逻辑计划→物理计划（SparkPlan）转换 |
| L2 | 文档 latest（Spark 4.1.2） | 官方文档 | https://spark.apache.org/docs/latest/streaming/getting-started.html | F1/F5：readStream/writeStream、source/sink |
| L2 | 文档 latest | 技术参考 | https://jaceklaskowski.gitbooks.io/mastering-spark-sql/content/spark-sql-SparkPlan-WholeStageCodegenExec.html | F3 末句：多算子合并进单个 WholeStageCodegenExec（算子融合） |
| L1 | 文档 latest（Spark 4.1.2） | 官方文档 | https://spark.apache.org/docs/latest/cluster-overview.html | F4：driver/SparkContext 向 worker 节点上的 executor 发送 task（master-worker） |
| - | 2021-04-27 | vendor 博客 | https://www.databricks.com/blog/2021/04/27/whats-new-in-apache-spark-3-1-release-for-structured-streaming.html | 仅功能公告，未取到 driver→executor 调度 verbatim（未采信） |

## Phase 1 react 留痕（串行，每条看完再发下一条；3 条即强信号，未触发早剪枝）
1 → 2 → 3，均强信号。

## 落盘文件
- create_streaming_table_databricks.html （F1/F2/F5 一手，官方 vendor 文档）
- incrementalexecution_dataninjago.html （F2/F3 一手）

## 工具受限说明
- patents.google.com 直抓可能被证书拦；本候选为公开开源技术，官方 + vendor 文档已足够定位，未触发该兜底。
- 官方文档取 "latest"（Spark 4.1.2，2026 现行）；其逻辑计划→物理计划、whole-stage codegen 算子融合、driver-executor 调度机制自 Spark 2.x 起稳定且持续公开，时间窗（>2020.05.08）满足。
