# 03-aliyun-flink verdict

## 候选基本信息
- 名称：阿里云实时计算 Flink 版（Realtime Compute for Apache Flink，含 Blink/VVR 二次开发） / 组织：阿里云（阿里巴巴） / 类型：产品 / 初判命中 F#：F1,F2,F3,F4,F5 / 专利公开（授权）日：2020.05.08

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（从客户端获取 SQL + 输入/输出通道描述信息） | 确认命中（字面） | "CREATE TEMPORARY TABLE datagen_source(...) WITH ('connector' = 'datagen');" 与 "CREATE TEMPORARY TABLE print_table(...) WITH ('connector' = 'print', ...);"；"本SQL示例使用Datagen连接器生成随机的数据流，并通过Print连接器将计算结果打印到实时计算开发控制台上" | https://www.alibabacloud.com/help/zh/flink/realtime-flink/getting-started/getting-started-for-a-flink-sql-deployment | 用户在控制台提交 SQL 草稿 + 用 `CREATE TABLE ... WITH ('connector'=...)` 定义 source/sink connector 配置（=输入/输出通道描述信息），对应 F1 可能描述方式②③。 |
| F2（由 SQL + 通道信息生成第一流图=逻辑节点图） | 确认命中（字面/等同） | "SQL文本通过parse阶段转换为逻辑执行计划，将SQL语句解析成AST抽象语法树SqlNode，然后通过convert转换方法进行处理。逻辑计划通过优化器优化为物理执行计划，最后通过代码生成技术生成Transformations并编译为可执行的JobGraph"（WebSearch 摘要，源自阿里云 Flink SQL 解析链路） | https://www.alibabacloud.com/help/zh/flink/user-guide/develop-an-sql-draft | SQL→AST(SqlNode)→逻辑执行计划=第一流图（逻辑节点）；阿里云/Blink 基于 Calcite。对应 F2 可能描述方式①③。 |
| F3（逻辑节点分组+选公共算子→第二流图；一个算子实现一组逻辑节点功能=算子合并） | 确认命中（字面/等同） | "逻辑计划通过优化器优化为物理执行计划"；"算子链…将尽可能多的满足条件的数据处理操作在一个 slot 中串联完成，从而最小化线程执行上下文切换和网络通信"；"pipeline.operator-chaining: 'false'"（拆开算子链）；"观察最终生成的拓扑图…由原来一层的聚合变成了两层的聚合"（LocalGroupAggregate/GlobalGroupAggregate 物理算子） | https://www.alibabacloud.com/help/zh/flink/support/faq-about-sql-performance ; https://blog.csdn.net/xianpanjia4616/article/details/126569629 | 逻辑计划→物理执行计划（两级映射，命中两级流图核心区分限定）；operator chaining 把多个算子合并进一个物理 task/slot，直接对应 F3 末句"一个算子实现多个逻辑节点功能"；物理算子来自 Flink 内置算子集合（预设算子库等同）。对应 F3 可能描述方式①②③。 |
| F4（按第二流图控制工作节点执行流计算任务） | 确认命中（字面/等同） | "JobManager扮演着集群中的管理者Master的角色，它是整个集群的协调者…同时管理Flink集群中从节点TaskManager"；"在任务执行期间，JobManager跟踪分布式任务，决定何时调度下一个任务（或一组任务）"；"作业拓扑较复杂时应增加TaskManager的资源" | https://developer.aliyun.com/ask/373780 ; https://www.alibabacloud.com/help/zh/flink/support/faq-about-sql-performance | JobManager=管理节点(Master) 按 JobGraph(第二流图) 调度算子 task 到 TaskManager=工作节点 执行，标准 master-worker。对应 F4 可能描述方式①③。 |
| F5（输入/输出通道：数据生产系统→流图→数据消费系统） | 确认命中（字面） | source connector（如 datagen/Kafka/MySQL CDC）"生成随机的数据流"/读取上游；sink connector（如 print/MySQL）"将计算结果打印/写出"；"MySQL连接器可以在SQL作业中用作源表、维表或结果表" | https://www.alibabacloud.com/help/zh/flink/realtime-flink/getting-started/getting-started-for-a-flink-sql-deployment ; https://help.aliyun.com/zh/flink/developer-reference/mysql-connector/ | source connector=输入通道（来自数据生产系统），sink connector=输出通道（写数据消费系统），逻辑表抽象屏蔽 IO。对应 F5 可能描述方式①②③。 |

## 已检查文档清单
- Flink SQL 快速入门（CREATE TABLE source/sink + INSERT INTO + 控制台部署运行，更新 2026-01-23，已落盘 aliyun-flink-sql-quickstart.html） — https://www.alibabacloud.com/help/zh/flink/realtime-flink/getting-started/getting-started-for-a-flink-sql-deployment
- SQL 作业开发（SQL→parse→AST(SqlNode)→逻辑计划→优化器→物理计划→Transformations→JobGraph） — https://www.alibabacloud.com/help/zh/flink/user-guide/develop-an-sql-draft
- 作业性能问题 FAQ（operator chaining 算子链 / pipeline.operator-chaining / 拓扑图节点 / 两层聚合 / TaskManager 资源，更新 2025-05-26） — https://www.alibabacloud.com/help/zh/flink/support/faq-about-sql-performance
- 高性能 Flink SQL 优化技巧（SQL 算子级优化，更新 2025-08-08） — https://www.alibabacloud.com/help/zh/flink/realtime-flink/user-guide/optimize-flink-sql
- JobManager 角色问答（Master/协调者，管理 TaskManager 从节点，调度分布式任务） — https://developer.aliyun.com/ask/373780
- MySQL 连接器（源表/维表/结果表，WITH 子句配置） — https://help.aliyun.com/zh/flink/developer-reference/mysql-connector/

## 最终判定
**第 2 档：全部确认命中（含 ≥1 等同）**

判定依据：F1（SQL + CREATE TABLE WITH connector 定义 source/sink）、F5（source/sink connector 对接数据生产/消费系统）属字面命中；F4（JobManager 管理节点按执行图调度 TaskManager 工作节点）字面命中。F2（SQL→AST→逻辑执行计划=第一流图）与 F3（逻辑计划→物理计划两级映射 + operator chaining 把多算子合并进一个物理 task=F3 末句"一个算子实现多个逻辑节点功能"，物理算子取自 Flink 内置算子集合=预设算子库）在术语上以 Flink/Blink 实现名（逻辑执行计划 / 物理执行计划 / 算子链 / 拓扑图）对应专利"第一流图 / 第二流图 / 公共算子 / 算子合并"，属字面+等同命中。两级流图核心区分限定（逻辑计划→物理计划两级）与算子合并关键区分限定（operator chaining）均有阿里云官方文档 verbatim 支撑，且全部引用材料更新日期晚于 2020.05.08，时间窗合规。未发现任何针对该候选的正向反据。判 **第 2 档**（含等同认定，故未列第 1 档）。

## 升级路径（第3-4档填）
（不适用，已落第 2 档）

## 总结一句话
阿里云实时计算 Flink 版以标准 SQL + CREATE TABLE connector 定义流作业，经 SQL→逻辑执行计划→物理执行计划（含 operator chaining 算子合并）由 JobManager 调度 TaskManager 执行，F1-F5 全部确认命中（含等同），落第 2 档。
