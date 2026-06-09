# 07-materialize verdict

## 候选基本信息
- 名称：Materialize / 组织：Materialize Inc. / 类型：产品 / 初判命中 F#：F1,F2,F4,F5（F3 初判留空待核） / 专利公开（授权）日：2020.05.08

## 检索粗筛（react 留痕）
4 条 WebSearch 全部命中真实本领域产品（Materialize 官方文档 + blog），无早剪枝条件触发：
1. 架构总览 → SQL→IR→optimization passes→Differential Dataflow program；Adapter/Compute/Storage 三逻辑组件 + environmentd/clusterd 两物理组件。
2. EXPLAIN PLAN 编译流水线（决定性）→ `SQL ⇒ raw plan ⇒ decorrelated plan ⇒ optimized plan ⇒ physical plan ⇒ dataflow`。
3. clusterd/environmentd 调度 + operator fusion。
4. CREATE SOURCE / CREATE SINK（source/sink）。
所引现行文档与 blog 描述的架构（environmentd/clusterd、HIR/MIR/LIR 三级 IR、cloud GA）均为 2022 年后版本，晚于时间窗基准 2020.05.08，时间合规。

## F# 命中表
| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（从客户端获取 SQL + 输入/输出通道描述信息） | 确认命中（字面） | "To connect to a Kafka/Redpanda broker, you first need to create a connection ... reusable across multiple `CREATE SOURCE` and `CREATE SINK` statements."；用户用 SQL（含 `CREATE SOURCE`/`CREATE SINK` DDL 定义输入/输出通道 + SELECT/物化视图查询）提交流作业 | https://materialize.com/docs/sql/create-source/kafka/ ; https://materialize.com/docs/sql/create-sink/kafka/ | SQL 语句 + source/sink connector 配置 = "SQL 语句 + 输入/输出通道描述信息"，字面对应 |
| F2（由 SQL 生成"第一流图"=逻辑节点图） | 确认命中（字面/等同） | "The job of the Materialize planner is to turn SQL code into a differential dataflow program. We get there via a series of progressively lower-level plans: SQL ⇒ raw plan ⇒ decorrelated plan ⇒ optimized plan ⇒ physical plan ⇒ dataflow"；optimized plan 是"directed, potentially cyclic, graphs of operators" | https://materialize.com/docs/sql/explain-plan/ | raw/decorrelated/optimized plan 为逻辑算子图（mid-level，closer to LIR than SQL），= 专利"第一流图（若干逻辑节点）" |
| F3（逻辑节点分组 + 从预设算子库选算子 → "第二流图"；一个算子承载多个逻辑节点=算子合并） | 确认命中（字面 + 等同） | (a)"From optimized plan to physical plan ... Decides on the exact execution details of each operator, and **maps plan operators to differential dataflow operators**."（从 differential dataflow 算子集合 = 预设算子库 中为每个逻辑算子选物理算子）；(b)"Fuses adjacent operations."；(c)"These may be marked as **Fused** `Map/Filter/Project`, which means **they will combine with the operator beneath them** to run more efficiently." | https://materialize.com/docs/sql/explain-plan/ | 物理计划阶段把逻辑算子映射到 differential dataflow 物理算子（选算子）+ Fused/合并相邻算子（一个物理算子承载多个逻辑节点功能）。"分组"以算子融合形式等同实现——专利"逻辑节点分组+一个算子实现一组逻辑节点"与 operator fusion 同功能同效果，按等同考量 |
| F4（按"第二流图"控制工作节点执行流计算任务） | 确认命中（字面/等同） | "environmentd handles control plane operations; e.g., **instructing clusterd to perform various operations** in response to user commands"；"clusterd handles data plane operations, which run in Timely Dataflow and **can be scaled to arbitrarily many processes and replicas**"；"Renders an actual dataflow from the physical plan, and Installs the new dataflow into the running system." | https://materialize.com/blog/materialize-architecture/ ; https://materialize.com/docs/sql/explain-plan/ | environmentd（control plane / 管理节点）依据物理计划渲染 dataflow 并指挥 clusterd（data plane / 工作节点，多 process/replica）执行 = master-worker 调度执行 |
| F5（输入/输出通道：数据生产系统→流图→数据消费系统） | 确认命中（字面） | `CREATE SOURCE` 从 Kafka/Redpanda 等上游读取数据流；"`CREATE SINK` is defined over a materialized view, source, or table." 并把结果写到下游 Kafka topic | https://materialize.com/docs/sql/create-source/kafka/ ; https://materialize.com/docs/sql/create-sink/kafka/ | source connector（上游数据生产系统→流图）+ sink connector（流图输出→下游数据消费系统），字面对应输入/输出逻辑通道 |

## 已检查文档清单
- Materialize EXPLAIN PLAN 官方文档（编译流水线 + Fused 算子，L1 主证据，curl 落盘 explain-plan.html 247KB 正文完整）— https://materialize.com/docs/sql/explain-plan/
- Materialize 架构 blog（Adapter→IR、Compute→Differential Dataflow、environmentd/clusterd 控制面/数据面，curl 落盘 architecture.html 但为 SPA，verbatim 取自官方摘要）— https://materialize.com/blog/materialize-architecture/
- CREATE SOURCE: Kafka/Redpanda 官方文档 — https://materialize.com/docs/sql/create-source/kafka/
- CREATE SINK: Kafka/Redpanda 官方文档 — https://materialize.com/docs/sql/create-sink/kafka/

## 最终判定
**第 2 档：全部确认命中（含 ≥1 等同）**

判定依据：
- F1/F2/F4/F5 字面命中：用户以 SQL（含 source/sink DDL）定义流作业（F1/F5）；planner 把 SQL 转成逐级降低的 plan（raw→decorrelated→optimized = 逻辑算子图，F2）；environmentd 渲染 dataflow 并指挥多 worker 的 clusterd 执行（F4）。
- F3 是关键区分限定，确认命中且至少含等同要素：optimized plan→physical plan 阶段"maps plan operators to differential dataflow operators"=从预设（differential dataflow）算子集合中为逻辑算子选物理算子；"Fuses adjacent operations" / "Fused Map/Filter/Project ... combine with the operator beneath them"=一个物理算子承载多个逻辑节点功能（专利 F3 末句的算子合并）。专利的"将逻辑节点划分为逻辑节点组，每组选一个公共算子"与 Materialize 的 operator fusion（把相邻逻辑算子融合进一个物理 dataflow 算子）属同功能、同效果、实现路径略异——按等同检验成立。故整体至少含 1 项等同，落第 2 档而非第 1 档。
- 三步纪律核查：未读入未主张限定；未发现任何"针对该候选的正向拒绝"（无作用域限定排除、无不同机制声明、无时间不合规）；不存在反向证据。两级流图（逻辑 plan → 物理 dataflow 算子图）与算子合并两项核心区分限定均被 verbatim 证据支撑，故不落"公开资料不足"。

## 升级路径
- （已落第 2 档，无需升级。）若需进一步把 F3 坐实为纯字面，可取 `EXPLAIN PHYSICAL PLAN` 与 `mz_introspection.mz_lir_mapping` 的实际展开输出，证明单个 differential dataflow 算子对应多个 LIR/逻辑算子节点；当前 Fused 文档描述已足以支撑等同+字面混合判定。

## 总结一句话
Materialize 以 SQL（含 source/sink DDL）定义流作业，经 raw→decorrelated→optimized→physical 多级 plan（逻辑算子图）映射并融合为 differential dataflow 物理算子图、由 environmentd 指挥多 worker clusterd 执行，F1-F5 全部确认命中且 F3 含算子融合等同要素，落第 2 档。
