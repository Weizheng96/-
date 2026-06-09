# 01-tech-apache-flink verdict

## 候选基本信息
- 名称：Apache Flink（Flink SQL）
- 组织：Apache 基金会 / 主贡献阿里巴巴等
- 类型：技术
- 初判命中 F#：F1,F2,F3,F4,F5
- 专利公开（授权）日：2020.05.08

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（客户端提交 SQL + 输入/输出通道描述） | 确认命中（字面） | "A table registered with the CREATE TABLE statement can be used as both table source and table sink." | https://docs.confluent.io/cloud/current/flink/reference/statements/create-table.html | Flink SQL 用户提交 SQL 作业，CREATE TABLE + WITH(connector=…) 即"输入/输出通道描述信息"，对应 Step 2 描述方式②③ |
| F2（由 SQL + 通道生成"第一流图"=逻辑节点图） | 确认命中（字面） | "Once an SQL statement is executed, it is parsed to obtain an SQLNode tree… an operation directed acyclic graph (DAG) is generated… The operation DAG is transformed into a RelNode (relational expression) DAG." | https://www.alibabacloud.com/blog/deep-insights-into-flink-sql-flink-advanced-tutorials_596628 | SQL → SQLNode 树 → operation DAG → RelNode（逻辑关系表达式）DAG = 第一流图（逻辑节点），正对应 Step 2 描述方式①③ |
| F3（逻辑节点分组+选公共算子→第二流图；一个算子承载多个逻辑节点=算子合并） | 确认命中（等同） | "the output of the optimizer is a Physical Rel DAG. The Physical Rel DAG is transformed into an ExecNode… Finally, the ExecNode is transformed into a Transformation DAG. The Transformation DAG is transformed into a JobGraph." 且 "Flink chains operator subtasks together into tasks… Chaining operators together into tasks is a useful optimization." | https://www.alibabacloud.com/blog/deep-insights-into-flink-sql-flink-advanced-tutorials_596628 ; https://nightlies.apache.org/flink/flink-docs-release-1.11/concepts/flink-architecture.html | 逻辑 RelNode DAG → Physical Rel DAG（选物理算子）= 第二流图；operator chaining 把多个算子合并进一个 task/JobVertex = "一个算子实现一组逻辑节点功能"。两级流图 + 算子合并两关键区分限定均字面命中 |
| F4（按第二流图控制工作节点执行流计算任务） | 确认命中（字面） | "The JobManager has a number of responsibilities related to coordinating the distributed execution… it decides when to schedule the next task… The TaskManagers (also called workers) execute the tasks of a dataflow." 且 "the JobManager deploys the subtask to a slot of the container." | https://nightlies.apache.org/flink/flink-docs-release-1.11/concepts/flink-architecture.html ; https://www.alibabacloud.com/blog/in-depth-analysis-of-flink-job-execution-flink-advanced-tutorials_596633 | JobManager（管理节点/master）按 ExecutionGraph 把 task 调度部署到 TaskManager（工作节点/worker）执行，字面对应 master-worker |
| F5（输入/输出通道：数据生产系统→流图→数据消费系统） | 确认命中（字面） | "A table source provides access to data which is stored in external systems (such as a database, key-value store, message queue, or file system). A table sink emits a table to an external storage system." | https://nightlies.apache.org/flink/flink-docs-release-1.12/dev/table/connectors/ | source connector 从上游数据生产系统读入、sink connector 写到下游数据消费系统，字面对应输入/输出通道定义 |

## 已检查文档清单
- Deep Insights into Flink SQL: Flink Advanced Tutorials（Alibaba Cloud，2020.09.16）— SQL→SQLNode→operation DAG→RelNode DAG→Physical Rel DAG→ExecNode→Transformation DAG→JobGraph — https://www.alibabacloud.com/blog/deep-insights-into-flink-sql-flink-advanced-tutorials_596628
- In-depth Analysis of Flink Job Execution: Flink Advanced Tutorials（Alibaba Cloud，2020.09.16）— operator chaining 合并多 node 进一 JobVertex；JobManager 部署 subtask 到 TaskManager slot — https://www.alibabacloud.com/blog/in-depth-analysis-of-flink-job-execution-flink-advanced-tutorials_596633
- Apache Flink 1.11 Documentation: Flink Architecture（官方一手，2020.07+）— operator chaining + JobManager/TaskManager master-worker verbatim — https://nightlies.apache.org/flink/flink-docs-release-1.11/concepts/flink-architecture.html
- Apache Flink 1.12 Table & SQL Connectors（官方）— table source/sink 读写外部系统 — https://nightlies.apache.org/flink/flink-docs-release-1.12/dev/table/connectors/
- Confluent Cloud / Apache Flink CREATE TABLE 文档 — CREATE TABLE 同时充当 source 与 sink — https://docs.confluent.io/cloud/current/flink/reference/statements/create-table.html

## 最终判定

**第 2 档：确认侵权（中）**

> 主 agent 复核（Step 6.2）调档说明：F1/F2/F4/F5 字面命中证据充分；F3 的"两级流图 + operator chaining 算子合并"字面成立，但专利 F3 中段"在**预设算子库**中选择每个**逻辑节点组**对应的**公共算子**"这一专利特有措辞，Flink 以"planner 从内置物理算子集合选 ExecNode/Transformation"按**等同**对应（术语非逐字一致）。按五档规则"含 ≥1 等同 → 第 2 档"，且与同引擎候选 03（阿里云 Flink 版）、05（Databricks/Spark）保持跨候选一致，故由第 1 档下调至第 2 档。仍属"确认侵权"档。

五档定义（"命中"=三态中的"确认命中"，含字面/等同）：
  - 第 1 档：确认侵权（高）— F1-Fk 全部"确认命中·字面"
  - 第 2 档：确认侵权（中）— F1-Fk 全部确认命中，含 ≥1 等同
  - 第 3 档：公开资料不足（强候选）— "确认命中" ≥60%，其余为"公开资料不足"且无"确认未命中（有正向反据）"
  - 第 4 档：公开资料不足（弱候选）— "确认命中" <60%，且无足以触发第5档的正向反据
  - 第 5 档：已排除 — 仅当：(a) ≥1 条 F# 为"确认未命中（有正向反据）"，或 (b) 全部证据 < 2020.05.08，或 (c) 架构层级不同
**0 命中 ≠ 已排除**：无正向反据（含"未提及/通用机制反推/非互斥手段"）→"公开资料不足（未确定）"（第 3 或 4 档），不是第 5 档。

判定依据（1-3 句，基于上表）：
F1–F5 全部以官方/一手文档 verbatim 字面命中：Flink SQL 经 Calcite 把 SQL 解析为 RelNode 逻辑 DAG（第一流图，F2），优化为 Physical Rel DAG / ExecNode / Transformation DAG（第二流图，选物理算子，F3 前半），再经 operator chaining 把多个算子合并进一个 task/JobVertex（F3 末句"一个算子承载多个逻辑节点"），由 JobManager 调度到 TaskManager 执行（F4 master-worker），CREATE TABLE + connector 定义 source/sink 输入/输出通道（F1/F5）。两级流图 + 算子合并两个关键区分限定均字面落入，且所有证据发布日期均晚于授权日 2020.05.08。

## 升级路径（仅当落第 3-4 档时填）
- 不适用（已落第 1 档）。

## 总结一句话
候选 01-tech-apache-flink（Apache Flink / Flink SQL）落第 2 档：SQL→RelNode 逻辑图→Physical/Transformation 物理图（含 operator chaining 算子合并）→JobManager 调度 TaskManager 执行，F1–F5 全部确认命中（F3"预设算子库选公共算子"措辞按等同），证据均晚于 2020.05.08。
