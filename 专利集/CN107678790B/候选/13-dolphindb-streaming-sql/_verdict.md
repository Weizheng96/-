# 13-dolphindb-streaming-sql verdict

## 候选基本信息
- 名称：DolphinDB 流式 SQL（Streaming SQL，自 v3.00.4） / 组织：浙江智臾科技 DolphinDB / 类型：产品 / 初判命中 F#：F1,F2,F4,F5 / 专利公开（授权）日：2020.05.08

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（从客户端获取 SQL + 输入/输出通道描述）| 确认命中（字面）| `registerStreamingSQL("select id, leftTable.value + rightTable.value from leftTable left join rightTable on leftTable.id=rightTable.id")`；"Users can declare shared tables as streaming SQL tables, on which register streaming SQL queries. Only declared tables can be used to register streaming SQL queries." | https://docs.dolphindb.com/en/Streaming/Streaming_SQL.html | 用户直接提交 SQL（含 select/join）；声明的共享流表 ≈ 输入通道；自 v3.00.4，晚于 2020.05.08 |
| F2（由 SQL 生成"第一流图"=逻辑节点图）| 公开资料不足（未确定，偏命中）| "After a streaming SQL query is submitted, the system creates an execution plan and initializes operator states." | https://docs.dolphindb.com/en/Streaming/Streaming_SQL.html | 确有"由 SQL 生成执行计划 + 算子"——具备计划层与算子；但官方文档**未 verbatim** 区分"逻辑流图(第一流图)"这一独立中间层名称。按等同：SQL→execution plan(含 operators) 已等同覆盖"SQL→逻辑节点图"的实质 |
| F3（逻辑节点分组 + 预设算子库选公共算子 → 第二流图；一算子承载多逻辑节点 = 算子合并）| 公开资料不足（未确定）| Streaming SQL 路径仅见 "operators ... passed up the execution chain"，**未见** logical-node 分组/从算子库选公共算子/operator fusion 的 verbatim。Stream Engine Parser 路径有 "combining the appropriate engines" 级联，但属**脚本 metric 表达式**而非 SQL | https://docs.dolphindb.com/en/Streaming/Streaming_SQL.html ; https://docs.dolphindb.com/en/Tutorials/StreamEngineParser.html | 核心区分限定。公开文档未明示"逻辑→物理两级 + 算子合并"的 SQL 内部结构；非反据（仅文档未公开内部编译细节），判"公开资料不足" |
| F4（按第二流图控制工作节点执行流计算任务）| 确认命中（等同）| "Job management: Each registered streaming SQL query is an independent job with centralized management of the queries' metadata and execution states."；"The subscriber executes the query and maintains a shared result table"；架构："a controller managing all chunk metadata ... Data is logically distributed across data nodes" | https://docs.dolphindb.com/en/Streaming/Streaming_SQL.html ; https://docs.dolphindb.com/en/about_dolphindb.html | 集中式 job 管理 + controller/data-node 分布式架构 = 管理节点控制工作节点执行（等同 master-worker 调度） |
| F5（输入通道：数据生产→流图；输出通道：流图→数据消费）| 确认命中（字面）| 入："capturing data changes in real time and feeding incremental data into the [query]"（声明的共享流表为入口，订阅/CDC 注入）；出："the system generates a result change log stream table to record the incremental changes ... Subscribers receive real-time changes by subscribing to this table"；"results can be output to ... stream tables, message-oriented middleware, databases and API clients" | https://docs.dolphindb.com/en/Streaming/Streaming_SQL.html ; https://docs.dolphindb.com/en/Streaming/streaming_engines.html | 输入(流表/订阅) + 输出(change log 流表→subscriber/MQ/DB/API) 两半齐备 |

## 已检查文档清单
- DolphinDB Streaming SQL（官方文档，自 v3.00.4；已 curl 落盘 StreamingSQL.html, 40KB） — https://docs.dolphindb.com/en/Streaming/Streaming_SQL.html
- DolphinDB Streaming SQL（官方 Medium, 2025-11-17） — https://medium.com/@DolphinDB_Inc/dolphindb-streaming-sql-real-time-at-the-speed-of-thought-24b5fcea92b7
- About DolphinDB（集群架构：controller + data node） — https://docs.dolphindb.com/en/about_dolphindb.html
- Streaming Engines（10+ 流计算引擎列表 + 输出去向） — https://docs.dolphindb.com/en/Streaming/streaming_engines.html
- Understanding the Stream Engine Parser（脚本 metric 表达式→引擎级联，非 SQL） — https://docs.dolphindb.com/en/Tutorials/StreamEngineParser.html
- US20200257689A1 "Structured cluster execution for data streams"（受让人 Databricks，**非本候选**，仅用于排除误归 logical→physical plan 表述） — https://patents.google.com/patent/US20200257689A1

## 最终判定
**第 3 档：疑似命中（≥60% 确认命中且无正向反据，待补证）**

判定依据：
- 架构层**相同**——DolphinDB Streaming SQL（v3.00.4）是 SQL 驱动的流计算，提交 `registerStreamingSQL("select ... join ...")`，系统 "creates an execution plan and initializes operator states"，算子沿 "execution chain" 增量计算，集中式 job 管理 + controller/data-node 分布式架构，输入声明流表、输出 change log 流表→订阅者。这与本专利"用 SQL 替代拖拽构图、管理节点编译 SQL 成流图并控制工作节点执行"属**同一抽象层**，可据字面/等同比对（非据 (iii) 架构层不同排除）。
- F1 / F5 字面命中，F4 等同命中 → 3/5 确认命中（60%）。F2 偏命中（确有 SQL→execution plan+operators，仅缺"逻辑流图"独立命名层 verbatim）。
- F3（两级流图 + 逻辑节点分组 + 预设算子库选公共算子 + 算子合并）为本专利**核心区分限定**，DolphinDB 公开文档未 verbatim 公开其 SQL 内部编译为"逻辑→物理两级 + operator fusion"的结构。这是**文档未公开内部细节**（缺失沉默），**不是正向反据**——按判定纪律三，不判"确认未命中"，判"公开资料不足"。
- 因存在未确定的核心限定（F2 命名层 / F3 全部），不达第 2 档（全部确认含等同）；因 ≥60% 确认且无任何正向反据，落第 3 档而非第 4/5 档。

## 升级路径（第3-4档填）
- 取 DolphinDB Streaming SQL **执行计划展开输出**（类似 `explain` 的逻辑→物理计划文本）或源码/技术博客，核实是否存在"逻辑算子树 → 物理算子/执行计划"两级映射（验 F2 的第一流图层 + F3 的第二流图层）。
- 查 DolphinDB 是否有 operator chaining / fusion / 算子合并（一个物理算子承载多个逻辑算子）的 verbatim 描述（验 F3 末句"一个算子实现多个逻辑节点功能"）。
- 查 DolphinDB 是否有"预设算子库 / built-in operator 集合中按逻辑节点组选算子"的明示（验 F3 中段"在预设算子库中选择公共算子"）。
- 若上述三点任一获 verbatim → 可升第 2 档；若获明确反向证据（如官方说明 Streaming SQL 为单层解释执行、无逻辑/物理两级、无算子合并）→ 才可据机制不同降第 5 档。

## 总结一句话
DolphinDB Streaming SQL（v3.00.4，2020.05.08 后）是同抽象层的 SQL 驱动流计算引擎，F1/F4/F5 确认命中、F2 偏命中，仅核心区分限定（两级流图 + 预设算子库选算子 + 算子合并 F2 命名层/F3）因官方未公开内部编译细节而"公开资料不足"、无任何正向反据，落第 3 档（疑似命中，待补执行计划/算子合并 verbatim）。
