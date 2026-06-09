# 证据索引 — 05-databricks

## 检索粗筛 query 留痕（react 串行，每次 1 条）
1. WebSearch: `Databricks Delta Live Tables define streaming pipeline with SQL CREATE STREAMING TABLE source sink` → 命中 DLT 声明式 SQL 流管线（F1/F5 信号）
2. WebSearch: `Spark Catalyst SQL parse logical plan physical plan whole-stage codegen fuse multiple operators single function` → 命中 Catalyst 四阶段 + whole-stage codegen 算子融合（F2/F3 信号）
3. WebSearch: `Spark Driver schedules tasks Executor worker nodes physical plan stages master architecture` → 命中 master-worker、Driver 按物理计划调度 Executor（F4 信号）
4. WebSearch: `Databricks Photon vectorized engine generally available release date 2022 physical execution operators` → Photon GA 2022.07（时间窗确认 + 物理算子）

## 深抓证据表

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2022-08-09 | 厂商博客 | https://www.databricks.com/blog/2022/08/09/low-latency-streaming-data-pipelines-with-delta-live-tables-and-apache-kafka.html | DLT 用标准 SQL CTAS 声明流管线；Structured Streaming 从 Kafka source 摄取（F1/F5）|
| 2 | 现行文档 | 官方 SQL 文档 | https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-streaming-table | `CREATE OR REFRESH STREAMING TABLE ... AS SELECT ... FROM STREAM read_kafka(...)` —— SQL 定义流作业 + source/sink（F1/F5）|
| 3 | 长青(Spark内核) | 第三方内核文档 | https://books.japila.pl/spark-sql-internals/whole-stage-code-generation/ | whole-stage codegen "fuses multiple physical operators ... into a single Java function"；CollapseCodegenStages 折叠（F3 算子合并）|
| 4 | 2015-04-13(机制长青) | 厂商博客 | https://www.databricks.com/blog/2015/04/13/deep-dive-into-spark-sqls-catalyst-optimizer.html | Catalyst：SQL/AST→逻辑计划→优化→物理计划→codegen（F2/F3）|
| 5 | 文档(架构长青) | 官方文档 | https://spark.apache.org/docs/latest/cluster-overview.html | master-worker：Driver 调度 task 到 Executor worker（F4）|
| 6 | 2022-07(GA) | 厂商博客 | https://www.databricks.com/blog/2022/08/03/announcing-photon-engine-general-availability-on-the-databricks-lakehouse-platform.html | Photon 向量化物理引擎 GA 2022.07（时间窗确认）|

> 时间窗说明：DLT/Photon 作为商用产品的关键能力（声明式 SQL 流管线、Photon GA）均在 2020.05.08 之后公开（2022 年）。Catalyst/whole-stage codegen 的内核机制虽早于时间窗，但其在 Databricks 商用平台上的持续运行与 DLT/Photon 集成属时间窗内的持续公开使用。
