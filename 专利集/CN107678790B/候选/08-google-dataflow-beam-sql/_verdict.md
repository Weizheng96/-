# 08-google-dataflow-beam-sql verdict

## 候选基本信息
- 名称：Google Cloud Dataflow + Apache Beam SQL / 组织：Google Cloud / 类型：产品 / 初判命中 F#：F1,F2,F3,F4,F5 / 专利公开（授权）日：2020.05.08

## F# 命中表
| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（从客户端获取 SQL + 输入/输出通道描述信息） | 确认命中（字面） | "Your SQL query is translated to a `PTransform`, an encapsulated segment of a Beam pipeline." ；"SqlTransform: the interface for creating `PTransforms` from SQL queries." ；Beam SQL 扩展含 "CREATE EXTERNAL TABLE"（以 SQL DDL 定义外部表，即输入/输出通道描述信息）。 | https://beam.apache.org/documentation/dsls/sql/overview/ | 用户提交 SQL 查询作为作业；CREATE EXTERNAL TABLE 即对应"输入/输出通道描述信息"。字面命中。 |
| F2（由 SQL + 通道信息生成"第一流图"=逻辑节点图） | 确认命中（字面/等同） | Beam SQL "uses Calcite SQL based on Apache Calcite"；planner（BeamQueryPlanner）把 SQL 经 RelNode→BeamRelNode 生成逻辑计划；"Dataflow creates an execution graph from the code that constructs your `Pipeline` object…" | https://beam.apache.org/documentation/dsls/sql/overview/ ; https://docs.cloud.google.com/dataflow/docs/pipeline-lifecycle | Calcite logical plan（RelNode 树）= 第一流图/逻辑节点图，业界标准 SQL→logical plan，字面/等同命中。 |
| F3（逻辑节点分组 + 选公共算子 → 第二流图；一个算子实现一组逻辑节点功能 = 算子合并） | 确认命中（字面/等同） | "When Dataflow runs a job, it converts the _steps_ of the pipeline into _stages_." ；"a stage represents a single unit of work that is performed by Dataflow." ；"To optimize the pipeline, Dataflow might fuse multiple steps into one stage." ；"Optimizations can include fusing multiple steps or transforms in your pipeline's execution graph into single steps." | https://docs.cloud.google.com/dataflow/docs/concepts/execution-details ; https://docs.cloud.google.com/dataflow/docs/pipeline-lifecycle | steps→stages 即逻辑节点→物理执行单元两级映射；fuse 多个 steps 进一个 stage 正对应"一个算子实现一组逻辑节点的功能"（operator fusion）。强命中 F3 末句。 |
| F4（按第二流图控制工作节点执行流计算任务） | 确认命中（字面/等同） | "The Dataflow service automatically parallelizes and distributes the processing logic in your pipeline to the workers you assign to perform your job." | https://docs.cloud.google.com/dataflow/docs/pipeline-lifecycle | Dataflow service（管理/master）按优化后 execution graph 把 stage 分发到 workers（工作节点）执行，master-worker 架构，等同命中。 |
| F5（输入/输出通道：数据生产系统→流图→数据消费系统） | 确认命中（字面/等同） | "During graph construction, Apache Beam locally executes the code… stopping at the calls to a source, sink, or transform step, and turning these calls into nodes of the graph." ；Beam SQL 以 CREATE EXTERNAL TABLE 定义 source/sink（如 Pub/Sub、BigQuery、Kafka connector）。 | https://docs.cloud.google.com/dataflow/docs/pipeline-lifecycle ; https://beam.apache.org/documentation/dsls/sql/overview/ | source connector 从数据生产系统读入、sink connector 写到数据消费系统，逻辑通道抽象，字面/等同命中。 |

## 已检查文档清单
- Beam SQL Overview（SQL→PTransform、SqlTransform、Calcite、CREATE EXTERNAL TABLE） — https://beam.apache.org/documentation/dsls/sql/overview/
- Dataflow Pipeline lifecycle（execution graph、fusing steps/transforms、Dataflow service 分发到 workers） — https://docs.cloud.google.com/dataflow/docs/pipeline-lifecycle
- Dataflow Execution details（steps→stages、stage=单位工作量、fuse multiple steps into one stage） — https://docs.cloud.google.com/dataflow/docs/concepts/execution-details

## 最终判定
**第 2 档：全部确认命中（含 ≥1 等同）**

判定依据：F1–F5 全部确认命中，无任一项出现针对该候选的正向反据。
- F1 字面命中（SQL 查询作为作业输入 + CREATE EXTERNAL TABLE 定义 source/sink 即输入/输出通道描述信息）。
- F2 经 Apache Calcite 把 SQL 解析为逻辑计划（RelNode/BeamRelNode 树），对应"第一流图（逻辑节点）"，字面/等同。
- F3 是核心区分限定——Dataflow 将 steps（逻辑步骤）转为 stages（物理执行单元），并 "fuse multiple steps into one stage"，精确对应"逻辑节点分组 + 一个算子实现一组逻辑节点功能"（operator fusion）；两级图（执行图→融合后 stage 图）成立。
- F4 Dataflow service（master）把工作分发到 workers（master-worker 架构）执行。
- F5 source/sink connector 对应输入/输出逻辑通道（数据生产系统→pipeline→数据消费系统）。
存在等同判定环节（Calcite logical plan↔第一流图、steps→stages fusion↔逻辑节点分组+算子合并、Dataflow service+worker↔管理节点+工作节点），并非每项均为逐字字面对应，故落第 2 档而非第 1 档。注：本判定为技术特征档位，非侵权法律结论。

## 升级路径（第3-4档填）
（不适用：已落第 2 档）

## 总结一句话
Google Cloud Dataflow + Apache Beam SQL 以 SQL（含 CREATE EXTERNAL TABLE 定义 source/sink）定义流作业、经 Calcite 生成逻辑计划、由 Dataflow runner 将 steps 融合（fuse）为 stages 后由 Dataflow service 分发到 workers 执行，F1–F5 全部确认命中（含等同），落第 2 档。
