# 14-apache-storm-sql verdict

## 候选基本信息
- 名称：Apache Storm SQL（含腾讯云 EMR 等托管分发） / 组织：Apache 软件基金会 / 腾讯云 EMR 等 / 类型：技术 / 初判命中 F#：F1,F2,F3,F4,F5 / 专利公开（授权）日：2020.05.08 / 专利申请日：2016.07.29

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注（含证据发布日期/版本） |
| --- | --- | --- | --- | --- |
| F1（从客户端获取 SQL + 输入/输出通道描述）| 确认命中（字面）| "StormSQL parses the SQL statements" + "In StormSQL data is represented by external tables" + `CREATE EXTERNAL TABLE FOO (...) LOCATION 'kafka://test?bootstrap-servers=localhost:9092'`（用 LOCATION 声明输入通道、另一张 EXTERNAL TABLE 声明输出通道）| storm-sql-internal.html / storm-sql.html | 用户提交 SQL 语句 + 用 CREATE EXTERNAL TABLE 定义 source/sink 通道描述，字面对应 F1。文档版本 1.2.3（机制自 1.1.0/2017 起） |
| F2（SQL+通道→第一流图=逻辑节点图）| 确认命中（字面）| "StormSQL parses the SQL statements and translates them to a Calcite logical plan. A logical plan consists of a sequence of SQL logical operators that describe how the query should be executed irrespective to the underlying execution engines. Some examples of logical operators include `TableScan`, `Filter`, `Projection` and `GroupBy`." | storm-sql-internal.html | Calcite 逻辑计划 = 逻辑算子序列 ≙"第一流图含若干逻辑节点"。字面命中 |
| F3（逻辑节点分组+选公共算子→第二流图；一个算子承载多个逻辑节点=算子合并）| 确认命中（字面 + 等同）| "The next step is to compile the logical execution plan down to a physical execution plan. A physical plan consists of physical operators... Physical operators such as `Filter`, `Projection`, and `GroupBy` are directly mapped to operations in Trident topologies. StormSQL also compiles expressions in the SQL statements into Java code blocks and plugs them into the Trident functions which will be compiled once and executed in runtime." | storm-sql-internal.html | 逻辑计划→物理计划两级映射字面命中"第一流图→第二流图"。"一个算子承载多个逻辑节点"按等同：StormSQL 把 SQL 中的（多个）表达式编译进同一个 Trident function 一次编译运行时执行（多逻辑节点功能合入一个物理执行单元 = operator/expression fusion 等同）。逐算子级"分组数量"等整数限定未外推 |
| F4（按第二流图控制工作节点执行）| 确认命中（字面）| 物理计划"directly mapped to operations in Trident topologies"，提交到集群：Nimbus 为 master node，"responsible for analyzing topology and distributing tasks on different supervisors"；"Supervisors are worker node managers that execute tasks assigned by Nimbus... manages one or more worker processes that... execute the actual tasks of a topology" | storm-sql-internal.html / dzone Apache Storm Architecture | 第二流图（Trident topology）由 Nimbus(主) 调度到 Supervisor-Worker(从) 执行，master-worker 字面命中 F4 |
| F5（输入/输出通道：数据生产系统→流图→数据消费系统）| 确认命中（字面）| `CREATE EXTERNAL TABLE ... LOCATION 'kafka://...'`（输入表/输出表分别绑定 Kafka 上游/下游）；"The TBLPROPERTIES clause specifies the configuration of KafkaProducer and is required for a Kafka sink table"；"the output table represents the output stream" | storm-sql.html / storm-sql-example.html | source EXTERNAL TABLE 从数据生产系统（Kafka）读入、sink EXTERNAL TABLE 写出至数据消费系统，逻辑表抽象屏蔽 IO，字面命中 F5 |

## 时间窗专项结论
- Storm SQL（Calcite 逻辑计划→Trident 物理计划）机制首次公开版本/日期：**Apache Storm 1.1.0，STORM-1446 解决于 2017-01-23**（亦含于 2.0.0）。
- 相对申请日 2016.07.29：机制公开（2017-01）**晚于**专利申请日 → 该机制本身**不构成对本专利申请日的现有技术**（不影响专利新颖性的此条路径）。
- 相对授权日 2020.05.08：开源机制（2017）早于授权日；但**被诉商用分发（腾讯云 EMR）在授权日之后仍持续提供**：Storm 1.2.3 见于 EMR-V 2.6.0（2021.07）与 EMR-V 2.7.0（2022.07），**均晚于 2020.05.08 授权日** → 存在授权日后的持续提供 + 新发布版本证据，**不属于第 5 档(ii)"全部证据 < 授权日"**。
- 腾讯云 EMR 当前是否含 Storm 组件：**已不含**。Storm 在 Hadoop 2.x 标准版 EMR-V 2.6.0（2021.07）/2.7.0（2022.07）为 1.2.3；EMR-V 2.8.0（2024.03）Storm 标"—"（移除）；Hadoop 3.x 全程无 Storm，现主推 Flink（1.12.1–1.18.1）。依据：腾讯云 EMR 组件版本概览文档。
- 授权日后是否仍有持续提供/新版本证据：**有**——EMR-V 2.6.0（2021.07）、2.7.0（2022.07）两个授权日后版本均打包 Storm 1.2.3（即含 Storm SQL）；提供窗口约 2021.07–2024.03。

## 已检查文档清单
- storm-sql-internal.html（Storm 1.2.3 文档；机制自 1.1.0/2017）— SQL→Calcite 逻辑计划→物理计划→Trident 映射、表达式编译进 Trident function、EXTERNAL TABLE — https://storm.apache.org/releases/1.2.3/storm-sql-internal.html
- STORM-1446（Resolved/Fixed，Fix 1.1.0 & 2.0.0，2017-01-23）— Calcite 逻辑计划→Storm Trident 编译机制首次落地 — https://issues.apache.org/jira/browse/STORM-1446
- 腾讯云 EMR 组件版本概览（截 2024.03）— Storm 1.2.3 见于 EMR-V 2.6.0(2021.07)/2.7.0(2022.07)，2.8.0(2024.03)移除 — https://cloud.tencent.com/document/product/589/66338
- cs101 blog "How Storm SQL is executed"（2017-01-25）— SqlNode→RelNode→TridentRel 代码追踪（算子融合细节作者标 TODO）— https://cs101.blog/2017/01/25/how-storm-sql-is-executed/

## 最终判定
**第 2 档：全部确认命中（含 ≥1 等同）**

判定依据：F1–F5 五项全部确认命中，其中 F1/F2/F4/F5 为字面命中（SQL 提交 + EXTERNAL TABLE source/sink；Calcite 逻辑计划=逻辑节点序列；Nimbus 主/Supervisor-Worker 从调度执行；source/sink 通道对应数据生产/消费系统），F3 的"一个算子承载多个逻辑节点功能（算子合并）"子限定按**等同**命中（StormSQL 将 SQL 中多个表达式编译进同一 Trident function 一次编译运行时执行，与"一个物理算子实现一组逻辑节点功能"为同一发明构思的等效实现）。

**时间窗对档位的影响（关键）**：技术机制层面 Storm SQL 与权 1 高度同构，但需严格区分"机制公开时间"与"被诉侵权行为时间"——(a) 机制随 Storm 1.1.0（2017）公开，晚于专利申请日（2016.07.29），故不是申请日现有技术；(b) 更重要的是被诉商用分发"腾讯云 EMR"在**授权日 2020.05.08 之后**（2021.07、2022.07 两个版本）仍持续打包提供 Storm 1.2.3，构成授权日后的持续提供证据，使本候选**不落入第 5 档(ii) 现有技术排除**，证据计入。综合 F1–F5 全命中且无任何正向反据，判**第 2 档**。

注：本判定为技术档位，非法律侵权结论；专利有效性（机制本身 2017 即开源、可能影响 2020 授权权项的稳定性）属另一独立维度，不在本档位范畴。

## 升级路径（第3-4档填）
（不适用——本候选为第 2 档）

## 总结一句话
Apache Storm SQL（SQL→Calcite 逻辑计划→Trident 物理计划→Nimbus/Supervisor 执行）F1–F5 全命中（F3 算子合并按等同），且腾讯云 EMR 在授权日后 2021.07/2022.07 仍打包 Storm 1.2.3 → 证据计入、不属现有技术排除，**落第 2 档**。
