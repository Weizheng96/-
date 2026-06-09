# 04-risingwave verdict

## 候选基本信息
- 名称：RisingWave / 组织：RisingWave Labs / 类型：产品（开源 PostgreSQL 兼容 streaming SQL 数据库）
- 初判命中 F#：F1,F2,F3,F4,F5
- 专利公开（授权）日：2020.05.08（材料均晚于此日，时间窗内）

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（从客户端获取 SQL + 输入/输出通道描述信息） | 确认命中（字面） | "A source is a resource that RisingWave can read data from." / "RisingWave uses the SQL `CREATE SOURCE` command to establish connections with external data streams." / 语法 `CREATE SOURCE ... WITH (connector='connector_name', ...)`；CREATE SINK 写下游。三条 SQL（SOURCE→MV→SINK）组成完整管线 | https://docs.risingwave.com/sql/commands/sql-create-source | 用户提交流式 SQL；CREATE SOURCE/SINK 的 WITH(connector=...) 即"输入/输出通道描述信息"，query SQL 即"若干条 SQL 规则" |
| F2（由 SQL+通道信息生成"第一流图"=逻辑节点图） | 确认命中（字面） | "Building a stream plan. Here a stream plan is a logical plan which consists of logical operators encoding the dataflow. This is carried out by the streaming planner at the frontend." | https://risingwavelabs.github.io/risingwave/design/streaming-overview.html | frontend 的 streaming planner 把 SQL 转成 logical stream plan（逻辑算子构成）= 第一流图（逻辑节点图） |
| F3（逻辑节点分组 + 选公共算子 → "第二流图"；一个算子承载多个逻辑节点 = 算子合并） | 确认命中（字面/等同） | "The stream fragmenter at the meta service breaks the generated logical stream plan into stream fragments... a stream fragment holds partial nodes from the stream plan, and each fragment can be parallelized by building multiple actors." / "The fragmenter breaks the execution plan into fragments, which are groups of execution nodes that share the same data distribution." | https://risingwavelabs.github.io/risingwave/design/streaming-overview.html · https://docs.risingwave.com/get-started/architecture | logical plan→fragment graph 两级映射明确；fragment = "groups of execution nodes"（多个逻辑节点合并进一个物理 fragment/actor）对应"一个算子实现一组逻辑节点功能"；fragment 内的 partial nodes 经物理算子实现，按等同（业界 fragment/operator fusion 等价于 F3 末句"算子合并"） |
| F4（按"第二流图"控制工作节点执行流计算任务） | 确认命中（字面） | "The meta service distributes different fragments into different compute nodes and let all compute nodes build their local actors." / "The Meta Node then instantiates the query into actors and assigns them to Compute Nodes." / "The Streaming Node executes streaming queries." | https://risingwavelabs.github.io/risingwave/design/streaming-overview.html · https://docs.risingwave.com/get-started/architecture | meta（管理节点）按 fragment graph 把 actor 调度到 compute node（工作节点）执行——master-worker 架构 |
| F5（输入/输出通道：数据生产系统→流图→数据消费系统） | 确认命中（字面） | source 端："Sources function as the intake mechanism through which RisingWave consumes streaming data from upstream producers"；"reading from external systems like Kafka"。sink 端：CREATE SINK "creates a sink, which is an external target where you can send data processed in RisingWave"（写到 Kafka/Iceberg/JDBC 等下游） | https://docs.risingwave.com/sql/commands/sql-create-source · https://docs.risingwave.com（CREATE SINK） | source connector = 输入通道（来自数据生产系统 Kafka/CDC），sink connector = 输出通道（写至数据消费系统）；与 F5"输入/输出逻辑通道"字面对应 |

## 已检查文档清单
- RisingWave Streaming Engine 设计文档（stream plan=logical plan / stream fragmenter @ meta service / fragment 持 partial nodes / actor 调度到 compute node） — https://risingwavelabs.github.io/risingwave/design/streaming-overview.html （落盘 streaming-overview.html，已 Grep 验证 verbatim）
- RisingWave architecture 官方文档（Meta Node 实例化 actor 分配给 Compute Node / fragmenter 把 execution plan 拆成 groups of execution nodes / Streaming Node 执行 streaming queries） — https://docs.risingwave.com/get-started/architecture （落盘 architecture.html）
- CREATE SOURCE SQL 命令文档（source 经 SQL 定义、从外部上游摄取输入流） — https://docs.risingwave.com/sql/commands/sql-create-source （落盘 create-source.html）

## 最终判定
**第 2 档：全部确认命中（含 ≥1 等同）**

判定依据：
- F1、F2、F4、F5 均有官方文档 verbatim 字面命中：SQL 驱动（CREATE SOURCE/SINK + query），frontend streaming planner 生成 logical stream plan（第一流图），meta service/Meta Node 按 fragment graph 把 actor 调度到 compute node（master-worker 执行），source/sink 即输入/输出逻辑通道（数据生产系统→流图→数据消费系统）。
- F3 为核心区分限定，RisingWave 满足"两级流图"——logical stream plan（逻辑算子）→ stream fragment graph（物理 fragment/actor）；fragment 明确是"groups of execution nodes"，即把 logical plan 的多个 partial nodes 合并进一个物理 fragment（再由 actor 物化），对应专利"将逻辑节点划分为逻辑节点组、一个算子实现一组逻辑节点的功能"。专利用语为"从预设算子库选公共算子做算子合并"，RisingWave 用语为"fragment / actor 物化"，实现路径不同但功能等同（均为逻辑→物理两级映射 + 多逻辑节点合并进一个物理执行单元），故 F3 按**等同**命中。
- 整个流程未见任何"针对本机制的正向拒绝"——无明示排他、无作用域限定否定、无不同架构层声明，故不存在反向证据。
- 全部材料晚于 2020.05.08，时间窗合规。
- 因 F3 依赖等同（而非纯字面 1:1 术语对应），不落第 1 档，落**第 2 档**。

## 升级路径（第3-4档填）
- 不适用（已落第 2 档）。

## 总结一句话
RisingWave 用 SQL（CREATE SOURCE/SINK + query）定义流作业，frontend 生成 logical stream plan，meta service 把其 fragment 化（fragment=groups of execution nodes）后以 actor 调度到 compute node 执行，source/sink 即输入/输出通道——F1/F2/F4/F5 字面命中、F3（逻辑→物理两级+多节点合并）按等同命中，落第 2 档。
