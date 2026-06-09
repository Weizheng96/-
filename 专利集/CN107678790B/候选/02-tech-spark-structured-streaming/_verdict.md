# 02-tech-spark-structured-streaming verdict

## 候选基本信息
- 名称：Apache Spark Structured Streaming（Spark SQL，含 Databricks DLT / CREATE STREAMING TABLE 路径）
- 组织：Apache 软件基金会 / 主贡献 Databricks 等
- 类型：技术
- 初判命中 F#：F1,F2,F3,F4,F5
- 专利公开（授权）日：2020.05.08

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 确认命中（字面） | `CREATE OR REFRESH STREAMING TABLE firehose_raw AS SELECT value raw_data, offset, timestamp, timestampType FROM STREAM read_kafka(bootstrapServers => 'ips', subscribe => 'topic_name');`；"This query must be a **streaming** query." | https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-streaming-table | 纯 SQL 定义流作业，SQL 内同时声明输入通道（`STREAM read_kafka(...)`）与输出（流式表），对应"从客户端获取 SQL + 输入/输出通道描述信息"。满足 F1/F2 的"必须由 SQL 驱动"关键限定。 |
| F2 | 确认命中（字面） | "The logical plan of the streaming query is created, analysed and initialised before the streaming query starts to run."；Catalyst "analysis, logical optimization, physical planning, and code generation"，"Spark Structured Streaming reuses the Spark SQL execution engine, including the analyser, optimiser, planner" | https://dataninjago.com/2022/07/11/spark-structured-streaming-deep-dive-5-incrementalexecution/ | SQL → Catalyst 逻辑计划（LogicalPlan，由若干逻辑算子节点构成）= 第一流图（逻辑节点图）。 |
| F3 | 确认命中（等同） | "The optimised logical plan is then converted into one or more candidate physical plan based a set of predefined Spark query planning strategies."；"Those planning strategies transform platform-independent LogicalPlans to SparkPlan"；WholeStageCodegenExec "when executed triggers code generation for the entire child physical plan subtree"，多算子（如 Filter + Range）"collapsed under a single WholeStageCodegenExec instance that generates one continuous Java function" | https://dataninjago.com/2022/07/11/spark-structured-streaming-deep-dive-5-incrementalexecution/ ; https://jaceklaskowski.gitbooks.io/mastering-spark-sql/content/spark-sql-SparkPlan-WholeStageCodegenExec.html | 逻辑计划→物理计划（SparkPlan）= 第一流图→第二流图；物理算子取自"predefined query planning strategies"内置物理算子集合（≈预设算子库，字面措辞不同按等同）；whole-stage codegen 把多个物理算子融合进单个 WholeStageCodegenExec/单段生成函数，字面对应 F3 末句"一个算子实现多个逻辑节点的功能"（operator fusion 强命中）。 |
| F4 | 确认命中（字面） | "Spark applications run as independent sets of processes on a cluster, coordinated by the `SparkContext` object in your main program (called the _driver program_)."；"Spark acquires _executors_ on nodes in the cluster"；"Finally, SparkContext sends _tasks_ to the executors to run." | https://spark.apache.org/docs/latest/cluster-overview.html | Driver（管理节点，承载 Catalyst 规划）按物理计划把 task 调度到 worker 节点上的 executor 执行 = master-worker，对应"管理节点根据第二流图控制工作节点执行流计算任务"。 |
| F5 | 确认命中（字面） | readStream `.format("socket")...load()` 创建 streaming DataFrame（输入源）；writeStream `.format(...).start()`；"The 'Output' is defined as what gets written out to the external storage."；SQL 侧 `FROM STREAM read_kafka(...)`（上游数据生产系统）→ 写入流式表（下游消费） | https://spark.apache.org/docs/latest/streaming/getting-started.html ; https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-streaming-table | source connector 从数据生产系统（Kafka/文件等）读入流图，sink 把结果写到数据消费系统（存储/表）= 输入/输出逻辑通道。 |

## 已检查文档清单
- Databricks CREATE STREAMING TABLE SQL 参考（纯 SQL 定义流作业 + STREAM read_kafka source + 流式表 sink）— https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-streaming-table （本地 create_streaming_table_databricks.html）
- Spark Structured Streaming IncrementalExecution 深度解析（逻辑计划→物理计划，复用 Spark SQL 引擎，发布 2022-07-11）— https://dataninjago.com/2022/07/11/spark-structured-streaming-deep-dive-5-incrementalexecution/ （本地 incrementalexecution_dataninjago.html）
- Spark 官方 Structured Streaming 入门指南（Spark 4.1.2；readStream/writeStream、source/sink）— https://spark.apache.org/docs/latest/streaming/getting-started.html
- Spark SQL Internals — WholeStageCodegenExec（算子融合）— https://jaceklaskowski.gitbooks.io/mastering-spark-sql/content/spark-sql-SparkPlan-WholeStageCodegenExec.html
- Spark 官方 Cluster Mode Overview（Spark 4.1.2；driver→executor 发 task，master-worker）— https://spark.apache.org/docs/latest/cluster-overview.html

## 最终判定
**第 2 档：确认侵权（中）— 全部确认命中，含 ≥1 等同**

> 主 agent 复核（Step 6.2）调档说明：本 verdict 原文已自陈 F3 的"预设算子库选公共算子"与 Spark "predefined query planning strategies/物理算子集合"措辞略异、按等同命中。按五档规则"含 ≥1 等同 → 第 2 档"，且与同引擎候选 05（Databricks，亦 Spark）一致，由第 1 档下调至第 2 档。仍属"确认侵权"档。

判定依据：F1（纯 SQL `CREATE STREAMING TABLE … AS SELECT … FROM STREAM read_kafka(...)` 在 SQL 内同时声明输入/输出通道）、F2（Catalyst 把 SQL 解析为逻辑计划 = 第一流图）、F3（逻辑计划→物理计划 SparkPlan，且 whole-stage codegen 把多算子融合进单个算子/单段生成函数，字面对应"一个算子实现多个逻辑节点"）、F4（driver/SparkContext 把 task 发到 worker 节点 executor 执行，master-worker）、F5（source 从生产系统读、sink 写到消费系统）均有 verbatim 一手证据，且全部材料晚于 2020.05.08，无任何针对本候选的正向反据。F3 的"预设算子库选公共算子"字面措辞与 Spark "predefined query planning strategies/物理算子集合"措辞略异，按最宽合理含义/等同仍命中，故整体置于第 1 档（如对该措辞从严要求字面一致，可降至第 2 档；不影响"高命中"结论）。

## 升级路径（第3-4档填）
（不适用——本候选已落第 1 档。如需进一步固化证据，可补抓 Spark 官方 `df.explain()` / `EXPLAIN` 输出样例，展示同一查询的 Parsed/Analyzed Logical Plan → Optimized Logical Plan → Physical Plan 两级映射与 `*(1)` whole-stage codegen 标记，作为 F2/F3 两级流图 + 算子合并的最直接一手 verbatim。）

## 总结一句话
Spark Structured Streaming（尤其 Databricks 纯 SQL 的 CREATE STREAMING TABLE 路径）以 SQL 定义流作业、经 Catalyst 逻辑计划→物理计划、whole-stage codegen 多算子融合、driver→executor master-worker 调度、source/sink 对接上下游，F1–F5 均有授权日后一手 verbatim 证据（F3"预设算子库选公共算子"措辞按等同），落第 2 档。
