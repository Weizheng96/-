# 11-snowflake-dynamic-tables verdict

## 候选基本信息
- 名称：Snowflake Dynamic Tables / Snowpipe Streaming / 组织：Snowflake（NYSE:SNOW） / 类型：产品 / 初判命中 F#：F1,F2,F5 / 专利公开（授权）日：2020.05.08

## 检索粗筛
Phase 1（react，串行）3 条 query 全部命中正向信号，未触发早剪枝（详见 _sources.md）：
1. 声明式 SQL 定义 Dynamic Table + 自动增量刷新 + 依赖 DAG 管线（官方 doc / blog 确认）
2. 三层架构：cloud services 层做解析/优化/计划生成/dispatch，virtual warehouse = MPP compute nodes 执行（master-worker）
3. EXPLAIN：明确"逻辑 explain plan"与"physical execution plan = DAG of physical operators"两级转换

> 候选为真实本领域产品（Snowflake 旗舰数据平台的声明式管线特性），且全部材料晚于 2020.05.08，(i)(ii)(iii) 早剪枝条件均不成立 → 进 Phase 2 深抓。

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（从客户端获取 SQL + 输入/输出通道描述）| 确认命中（字面/等同） | "A dynamic table materializes the results of a SELECT query and keeps them up to date." / "This CREATE statement defines what the table contains (the SELECT query)…" / "Snowflake parses your query, identifies the base tables it reads from" | https://docs.snowflake.com/en/user-guide/dynamic-tables-about | 用户提交 `CREATE DYNAMIC TABLE … AS SELECT`（SQL 语句 = F1 描述方式②的 DDL+查询 SQL）；base table（source）/dynamic table（输出）≈ 输入/输出通道描述。等同满足 |
| F2（SQL+通道→第一流图=逻辑节点图）| 确认命中（字面/等同） | "The EXPLAIN plan is the 'logical' explain plan. It shows the operations that will be performed, and their logical relationship to each other." / "The Parser converts the query into an internal, structured format known as a Query Block Internal Representation." / "the Optimizer…transforming the user's declarative query into a highly efficient procedural plan." | https://docs.snowflake.com/en/sql-reference/sql/explain ; https://medium.com/snowflake/anatomy-of-a-snowflake-query-a-deep-dive-into-the-execution-engine-ca9061022c47 | SQL 经 parser+optimizer 生成"逻辑 plan"（含操作及其逻辑关系），对应"第一流图=逻辑节点图"。字面/等同满足 |
| F3（逻辑节点分组+预设算子库选算子→第二流图；算子承载多逻辑节点=算子合并）| 确认命中（等同；其中"算子合并"子动作公开资料不足） | "The optimized logical plan is translated into a Physical Execution Plan. This plan is a Directed Acyclic Graph (DAG) composed of physical operators, which are the concrete steps the warehouse will take to execute the query." / "An explain plan shows the operations (for example, table scans and joins)…" | https://medium.com/snowflake/anatomy-of-a-snowflake-query-a-deep-dive-into-the-execution-engine-ca9061022c47 ; https://docs.snowflake.com/en/sql-reference/sql/explain | 明确两级：逻辑 plan → physical execution plan（= 物理算子 DAG），与专利"第一流图→第二流图"两级映射等同。物理算子（TableScan/Filter/Join/Aggregate）即"从预设算子集合选出的公共算子"。**但"逻辑节点分组并使一个算子承载多个逻辑节点功能（operator fusion/chaining）"的精确末句无 verbatim 直接命中** → 该子动作记"公开资料不足"，未读入正向反据；核心两级结构+物理算子图按等同确认命中 |
| F4（按第二流图控制工作节点执行流计算任务）| 确认命中（字面/等同） | cloud services 层 "coordinate activities across Snowflake…process user requests, from sign-in to query dispatch" / "Snowflake monitors your dynamic tables, detects upstream changes, and dispatches refreshes automatically." / "A virtual warehouse is a cluster of compute resources…processes SQL statements"（MPP compute clusters） | https://docs.snowflake.com/en/user-guide/intro-key-concepts ; https://docs.snowflake.com/en/user-guide/dynamic-tables-about | cloud services 层（管理节点）做 query dispatch / 协调 refresh，virtual warehouse 的 MPP compute nodes（工作节点）执行物理算子。master-worker 调度等同满足 |
| F5（输入通道：数据生产系统→流图；输出通道：流图→数据消费系统）| 确认命中（字面/等同） | "Snowflake monitors the base tables for changes and refreshes the dynamic table to stay within the target lag." / "The new results are applied to the dynamic table atomically." / "The virtual warehouse runs each refresh query." | https://docs.snowflake.com/en/user-guide/dynamic-tables-about | base table（含 Snowpipe Streaming 自上游 Kafka/消息源流入）= 输入通道/数据生产系统；dynamic table 物化结果供下游消费 = 输出通道/数据消费系统。等同满足 |

## 已检查文档清单
- Dynamic Tables 官方总览（声明式 SELECT 定义、解析识别 base table、推断依赖图、自动 dispatch refresh、warehouse 执行）— https://docs.snowflake.com/en/user-guide/dynamic-tables-about （本地 dynamic-tables-about.html）
- EXPLAIN 官方文档（"逻辑 explain plan" 概念、编译 SQL、操作及逻辑关系、parentOperators 父子链接）— https://docs.snowflake.com/en/sql-reference/sql/explain （本地 explain.html）
- Snowflake 核心概念/三层架构（cloud services 解析+优化+dispatch；virtual warehouse MPP 执行）— https://docs.snowflake.com/en/user-guide/intro-key-concepts
- Anatomy of a Snowflake Query（Snowflake 官方 Medium，2025）：Parser→内部表示，Optimizer 把声明式 query 转 procedural plan，逻辑 plan→Physical Execution Plan（物理算子 DAG）— https://medium.com/snowflake/anatomy-of-a-snowflake-query-a-deep-dive-into-the-execution-engine-ca9061022c47

## 最终判定
**第 2 档：全部确认命中含 ≥1 等同**

判定依据：F1–F5 全部确认命中，其中 F1/F4/F5 字面或近字面命中，F2 字面/等同，F3 以等同方式命中——Snowflake 明确存在"逻辑 plan（逻辑算子及其关系）→physical execution plan（物理算子 DAG）"两级转换，与专利"第一流图（逻辑节点）→第二流图（算子）"两级核心区分限定结构等同；物理算子（TableScan/Filter/Join/Aggregate）对应"从预设算子集合选出的公共算子"；cloud services 层（管理节点）做 query dispatch / 协调，virtual warehouse 的 MPP compute nodes（工作节点）执行，构成 master-worker。全程未发现任何针对本候选的正向反据（无"不支持 SQL 定义""无两级 plan""单机非分布式"等正向拒绝证据）。因含 ≥1 等同（F3 等关键限定靠等同而非字面命中），落第 2 档而非第 1 档。

> 唯一不确定点：F3 末句"逻辑节点分组 + 一个算子承载多个逻辑节点功能（operator fusion/chaining）"无 verbatim 直接命中（"公开资料不足"），但该子动作不影响"两级流图 + 物理算子图"核心限定的等同成立，且无反据，故不降档。
> 法律免责：本判定仅为技术档位与证据线索，非"已构成侵权"的法律结论。SQL 解析→逻辑/物理两级 plan→MPP 执行属业界（含 Calcite 等）通用范式，是否落入权利要求保护范围、是否存在在先技术抗辩或具体实现差异，须由专业侵权比对与 FTO 分析另行认定。

## 升级路径（如需进一步坐实 F3 末句"算子合并"）
- 抓取 Snowflake Query Profile / EXPLAIN 实际输出，核实是否存在多个逻辑操作被融合进单一物理算子节点（operator fusion/pipelining）的明确表述或 query profile 截图。
- 检索 Snowflake 2020.05.08 后自有公开专利（查询编译 / 增量刷新 / 调度），看其权利要求是否自述"逻辑节点分组→物理算子"映射，作为 F3 等同的旁证。

## 总结一句话
Snowflake Dynamic Tables 以声明式 SELECT 定义增量物化管线、经 cloud services 层解析为逻辑 plan→物理算子 DAG 并由 virtual warehouse MPP 工作节点执行，F1–F5 全部命中（F3 靠等同），落第 2 档（全部确认命中含等同）。
