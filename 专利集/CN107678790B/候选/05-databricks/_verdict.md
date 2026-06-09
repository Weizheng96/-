# 05-databricks verdict

## 候选基本信息
- 名称：Databricks（Spark Structured Streaming / Delta Live Tables / Photon） / 组织：Databricks / 类型：产品 / 初判命中 F#：F1,F2,F3,F4,F5 / 专利公开（授权）日：2020.05.08

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（客户端获取 SQL + 输入/输出通道描述）| 确认命中（字面）| "CREATE OR REFRESH STREAMING TABLE firehose_raw AS SELECT value raw_data, offset, timestamp, timestampType FROM STREAM read_kafka(bootstrapServers => 'ips', subscribe => 'topic_name');" 及 "Delta Live Tables and their dependencies can be declared with a standard SQL Create Table As Select (CTAS) statement" | https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-streaming-table ; https://www.databricks.com/blog/2022/08/09/low-latency-streaming-data-pipelines-with-delta-live-tables-and-apache-kafka.html | 用户提交一段流式 SQL（含 STREAM 关键字）；`read_kafka(...)` = 输入通道描述、目标 STREAMING TABLE = 输出通道描述。对应"从客户端获取输入通道描述+SQL+输出通道描述" |
| F2（由 SQL+通道生成第一流图=逻辑节点图）| 确认命中（字面）| "Spark SQL begins with a relation to be computed, either from an abstract syntax tree (AST) returned by a SQL parser ..." ；"In the physical planning phase, Spark SQL takes a logical plan and generates one or more physical plans" | https://www.databricks.com/blog/2015/04/13/deep-dive-into-spark-sqls-catalyst-optimizer.html | Catalyst 把 SQL 解析为 AST→逻辑计划（logical plan = 第一流图/逻辑节点），随后进入物理规划。逻辑计划即"若干逻辑节点构成的第一流图" |
| F3（逻辑节点分组 + 从预设算子库选公共算子→第二流图；一个算子实现一组逻辑节点功能=算子合并）| 确认命中（字面/等同）| "In the physical planning phase, Spark SQL takes a logical plan and generates one or more physical plans, using physical operators that match the Spark execution engine"；"Whole-Stage CodeGen ... fuses multiple physical operators (as a subtree of plans that support code generation) together into a single Java function"；"CollapseCodegenStages physical preparation rule finds the physical query plans that support codegen and collapses them together as a WholeStageCodegen" | https://www.databricks.com/blog/2015/04/13/deep-dive-into-spark-sqls-catalyst-optimizer.html ; https://books.japila.pl/spark-sql-internals/whole-stage-code-generation/ | 三子动作全落：①逻辑节点分组 = CollapseCodegenStages 将可 codegen 的物理算子子树分组为 WholeStageCodegen 阶段；②从预设算子库选公共算子 = "using physical operators that match the Spark execution engine"（物理算子集合即预设算子库）；③一个算子实现多个逻辑节点功能 = "fuses multiple physical operators into a single Java function"（多算子融合进单段生成代码，正对应 F3 末句 operator fusion）。物理计划 = 第二流图 |
| F4（按第二流图控制工作节点执行流计算任务）| 确认命中（字面）| "Once the Physical Plan is generated, the Driver schedules the execution of the tasks ... The task scheduler assigns tasks to executors"；"Spark follows a Master-Slave architecture ... one central coordinator and multiple distributed worker nodes"；"Executors are worker processes that run on worker nodes ... executing the tasks assigned to it by the driver" | https://spark.apache.org/docs/latest/cluster-overview.html | Driver（管理节点/master）按物理计划（第二流图）把 task 调度到 Executor（工作节点/worker）执行 → 管理节点根据第二流图控制工作节点执行流计算任务。master-worker 架构吻合隐含约束 |
| F5（输入/输出通道：数据生产系统→流图→数据消费系统）| 确认命中（字面）| "FROM STREAM read_kafka(bootstrapServers => 'ips', subscribe => 'topic_name')"（输入通道：从 Kafka 数据生产系统读流）；"Stores the data from Kafka in an append-only streaming table"（输出通道：写入 streaming table 数据消费系统）；"Delta Live Tables written in Python can directly ingest data from an event bus like Kafka using Spark Structured Streaming" | https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-streaming-table ; https://www.databricks.com/blog/2022/08/09/low-latency-streaming-data-pipelines-with-delta-live-tables-and-apache-kafka.html | source connector（read_kafka/read_files）从上游数据生产系统读数据流入流图；目标 streaming table / sink 写到下游数据消费系统。逻辑表/逻辑流抽象屏蔽具体 IO |

## 已检查文档清单
- DLT + Apache Kafka 低延迟流管线博客（2022-08-09，DLT 用 SQL CTAS 声明、Structured Streaming 从 Kafka 摄取）— https://www.databricks.com/blog/2022/08/09/low-latency-streaming-data-pipelines-with-delta-live-tables-and-apache-kafka.html
- CREATE STREAMING TABLE 官方 SQL 文档（STREAM 关键字 + read_kafka/read_files 定义 source）— https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-streaming-table
- Spark SQL Internals — Whole-Stage Code Generation（多物理算子融合进单 Java 函数）— https://books.japila.pl/spark-sql-internals/whole-stage-code-generation/
- Deep Dive into Spark SQL's Catalyst Optimizer（SQL/AST→逻辑计划→物理计划→codegen 四阶段）— https://www.databricks.com/blog/2015/04/13/deep-dive-into-spark-sqls-catalyst-optimizer.html
- Spark Cluster Mode Overview（master-worker、Driver 调度 task 到 Executor）— https://spark.apache.org/docs/latest/cluster-overview.html
- Photon Engine GA 公告（向量化物理引擎，2022.07 GA，时间窗确认）— https://www.databricks.com/blog/2022/08/03/announcing-photon-engine-general-availability-on-the-databricks-lakehouse-platform.html

## 最终判定
**第 2 档：全部确认命中含 ≥1 等同**

判定依据：
- F1/F2/F4/F5 均为字面命中——DLT 以流式 SQL（含 STREAM 关键字的 CREATE STREAMING TABLE / CTAS）定义流作业并显式声明 source（read_kafka）与 sink（streaming table）通道；Catalyst 把 SQL 解析为逻辑计划（第一流图）；Driver（master）按物理计划把 task 调度到 Executor（worker）执行；source/sink connector 对应数据生产/消费系统的输入/输出通道。
- F3 为字面 + 等同命中：物理规划"using physical operators"对应"从预设算子库选公共算子"；whole-stage codegen 把多个物理算子"fuse ... into a single Java function" + CollapseCodegenStages 把算子子树分组为 WholeStageCodegen 阶段，正对应专利 F3"逻辑节点分组 + 一个算子实现多个逻辑节点功能"（算子合并/operator fusion）。专利权 1 描述的是"逻辑节点分组→选算子→一个物理算子承载多个逻辑节点"，Spark 实现路径为"物理规划选物理算子→codegen 把多个物理算子融合进单函数"——两者在"把多个细粒度处理单元合并为单个执行单元以提升性能"的功能-方式-效果上等效，差异仅在融合发生于物理算子层（codegen）而非逻辑节点直接映射，按等同检验落入。
- 时间窗：DLT 声明式 SQL 流管线、Photon 向量化引擎 GA 均为 2022 年公开（晚于 2020.05.08）；Catalyst/whole-stage codegen 内核机制虽早于时间窗，但其在 Databricks 商用平台 + DLT/Photon 上的持续集成与公开使用落在时间窗内。
- 未发现任何针对该候选的正向反据（无"不支持 SQL 定义流""单层计划无逻辑→物理两级""非 master-worker"之类排他陈述）。
- 注：标的"第二流图由对第一流图逻辑节点分组+选算子得到"这一**两级流图严格映射**，在 Spark 中体现为"逻辑计划→物理计划"两级（明确两层），故 F2/F3 两级映射约束满足；唯一保留的不确定性是专利"逻辑节点分组"是否要求在逻辑层先分组——Spark 的分组（CollapseCodegenStages）发生于物理层，故就严格字面而言 F3 第一子动作按等同而非纯字面计，已据此落第 2 档而非第 1 档。

## 升级路径（第3-4档填）
（不适用——已达第 2 档）

## 总结一句话
Databricks DLT/Structured Streaming + Catalyst + whole-stage codegen + Driver/Executor 架构对 F1-F5 全部确认命中（F3 算子合并按等同），无正向反据，时间窗内（DLT/Photon 2022），落第 2 档（全部命中含 ≥1 等同）。

---
> 免责声明：本报告仅为技术特征比对线索与证据链梳理，不构成"已构成侵权"的法律结论。最终侵权认定须由权利人结合完整权利要求解释、被诉产品源码/实现细节及法律程序判定。
