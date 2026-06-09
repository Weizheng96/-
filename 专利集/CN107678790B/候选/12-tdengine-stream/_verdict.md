# 12-tdengine-stream verdict

## 候选基本信息
- 名称：TDengine 流计算引擎（Stream Processing） / 组织：涛思数据 TDengine / 类型：产品 / 初判命中 F#：F1,F2,F4,F5 / 专利公开（授权）日：2020.05.08
- 时间窗核对：TDengine 3.0（首次正式引入 stream 引擎）于 **2022.08.23** GA，晚于授权日 → 时间窗满足。

## 检索粗筛
- WebSearch 4 条全部有信号（query 留痕见 _sources.md）：定位为真实本领域产品（时序数据库内置 SQL 流计算引擎，开源 + 官方文档公开）。
- 未早剪枝：架构层一致（管理节点 mnode + 工作节点 vnode/snode 的 master-worker 分布式），材料晚于时间窗。

## F# 命中表
| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（客户端提交 SQL + 输入/输出通道描述） | 确认命中（字面） | "CREATE STREAM [IF NOT EXISTS] [db_name.]stream_name options [INTO [db_name.]table_name]... AS subquery"；源 "[FROM [db_name.]table_name]"（regular/super/sub/virtual table）；示例 "create stream current_stream into power.current_stream_output_stb as select ... from power.meters where voltage <= 220 interval (5s)" | https://docs.tdengine.com/reference/taos-sql/stream/ · https://docs.tdengine.com/cloud/stream/ | 用户提交一段 SQL（含 FROM 源表=输入通道、INTO 目标表=输出通道）定义流作业，完全对应"SQL 语句 + 输入/输出通道描述信息"。 |
| F2（SQL+通道→第一流图=逻辑节点图） | 确认命中（字面/等同） | "The mnode uses the vgroups information to convert the logical execution plan into a physical execution plan..." —— 即存在"逻辑执行计划"（logical execution plan）作为第一级图；meta store "stores ... DAG information" | https://docs.tdengine.com/inside-tdengine/stream-processing-engine/ | SQL 经管理节点 mnode 生成逻辑执行计划（=第一流图/逻辑节点），与 F2 等同。 |
| F3（逻辑节点分组 + 选公共算子→第二流图；一个算子承载多个逻辑节点=算子合并） | 确认命中（等同，末句"算子合并"公开资料不足） | "The mnode uses the vgroups information to convert the logical execution plan into a physical execution plan, and further generates a Directed Acyclic Graph (DAG) for the stream task." | https://docs.tdengine.com/inside-tdengine/stream-processing-engine/ | 逻辑计划→物理计划→DAG 两级转换字面命中"第一流图→第二流图"。物理 DAG 节点（source/agg/sink task）按 vgroup 划分 = 逻辑节点分组+选物理算子（等同）。但"一个算子合并/承载多个逻辑节点功能（operator fusion/chaining）"无直接 verbatim → 该子动作为公开资料不足，不构成正向反据。 |
| F4（按第二流图控制工作节点执行） | 确认命中（字面） | "...task scheduling that converts logical execution plans into physical execution plans and distributes them to vnodes."；"mnode will randomly select a vnode to schedule the execution of the agg task."；"The mnode plays a crucial role in issuing control commands to stream processing tasks..." | https://docs.tdengine.com/inside-tdengine/stream-processing-engine/ | 管理节点 mnode 依据物理 DAG 把任务下发并调度到工作节点 vnode/snode 执行，字面对应 F4。 |
| F5（输入通道：数据生产系统→流图；输出通道：流图→数据消费系统） | 确认命中（字面/等同） | source task "responsible for reading data from the WAL (and from the TSDB when necessary) ... and distributing the processed results to downstream tasks"；sink task "responsible for writing the received data into the vnode it resides in"；SQL 层 "[FROM table]" / "[INTO table]" | https://docs.tdengine.com/inside-tdengine/stream-processing-engine/ · https://docs.tdengine.com/reference/taos-sql/stream/ | FROM 源表（WAL/TSDB=数据生产系统）经流图、INTO 目标表（=数据消费系统）；source/sink task 分别实现输入/输出逻辑通道，命中 F5 两半。 |

## 已检查文档清单
- Stream Processing SQL Reference（CREATE STREAM ... FROM ... INTO ... AS subquery 语法） — https://docs.tdengine.com/reference/taos-sql/stream/
- Stream Processing 概览 + 示例（CREATE STREAM ... INTO stb AS select ... interval） — https://docs.tdengine.com/cloud/stream/
- Stream Processing Engine 内部原理（逻辑→物理执行计划→DAG、mnode 调度、source/agg/sink task、vnode/snode） — https://docs.tdengine.com/inside-tdengine/stream-processing-engine/（WebFetch 404/curl SPA 空壳，正文以 WebSearch 多次一致 verbatim 为准，见 _sources.md 工具受限明示）
- TDengine 3.0 发布公告（2022.08.23，时间窗证据） — https://www.globenewswire.com/news-release/2022/08/23/2502937/0/en/TDengine-3-0-Introduces-Cloud-Native-Architecture-to-Simplify-Large-scale-Time-Series-Data-Operations-in-IoT.html

## 最终判定
**第 2 档：全部确认命中（含 ≥1 等同）**

判定依据：
- F1 字面命中（SQL CREATE STREAM 含 FROM 输入表 / INTO 输出表）；F4 字面命中（mnode 转物理计划并调度下发 vnode/snode 执行）；F5 字面/等同命中（source task 从 WAL/TSDB 读、sink task 写出，FROM/INTO 即输入/输出逻辑通道）。
- F2 命中（mnode 生成 logical execution plan = 第一流图/逻辑节点，等同）。
- F3 命中（"logical execution plan → physical execution plan → DAG" 两级转换 + 按 vgroups 划分 = 逻辑节点分组+选物理算子，按等同检验落入；DAG 拆为 source/agg/sink task 即第二流图算子节点）。F3 末句"一个算子承载多个逻辑节点功能（operator fusion/chaining）"无直接 verbatim，属"公开资料不足"而非正向反据，故不阻断命中、仅使 F3 落"等同含不足"档。
- 无任何"针对该候选的正向拒绝"证据（架构一致、SQL 驱动、master-worker、时间窗合规）。因至少 F3（及 F2）依赖等同/物理 DAG 推定而非逐字"第一流图/第二流图/逻辑节点组"术语对应，故定第 2 档而非第 1 档。

## 升级路径（第 3-4 档填）
（本候选定第 2 档，不需升级；以下为加固 F3 末句的可选补证）
- 直接渲染 docs.tdengine.com/inside-tdengine/stream-processing-engine/ 取"逻辑节点分组 / 选算子 / 算子合并(operator chaining/fusion)"逐字 verbatim；
- 抓 GitHub taosdata/TDengine 源码（stream / planner / scheduler 模块）核 logical plan→physical plan→DAG 的算子分组与合并代码，确证 F3 末句字面对应。

## 总结一句话
TDengine 流计算引擎以 SQL（CREATE STREAM...FROM...INTO...AS SELECT）定义流作业，由管理节点 mnode 生成逻辑执行计划→转物理执行计划→DAG 并调度到工作节点 vnode/snode 执行，source/sink task 对应输入/输出通道，F1-F5 全部命中（F2/F3 含等同、F3 末句算子合并公开资料不足），落第 2 档。
