# 06-confluent-ksqldb verdict

## 候选基本信息
- 名称：ksqlDB / 组织：Confluent / 类型：产品 / 初判命中 F#：F1,F2,F3,F4,F5 / 专利公开（授权）日：2020.05.08

## 检索粗筛
- WebSearch ①：`ksqlDB SQL query logical plan physical plan topology execution Kafka Streams` → 命中官方文档/blog/EXPLAIN，确认 SQL→AST→logical plan→physical plan(topology) 全链路。
- WebSearch ②：`ksqlDB EXPLAIN statement execution plan topology source sink CREATE STREAM connector` → 命中 EXPLAIN（execution plan = DAG of steps）、source/sink、CREATE STREAM 物理 topology。
- 强信号，未触发早剪枝。详见 `_sources.md`。

## F# 命中表
| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 确认命中（字面） | "Register a stream or table by using the DDL statements, CREATE STREAM and CREATE TABLE."；DDL 用 WITH(...) 指定 backing Kafka topic（输入/输出通道描述），客户端经 SQL CLI/REST 提交 SQL 语句 | https://docs.confluent.io/platform/current/ksqldb/operate-and-deploy/how-it-works.html | 用户向 ksqlDB Server 提交 SQL；CREATE STREAM/TABLE WITH(...) 即"输入/输出通道描述信息" |
| F2 | 确认命中（字面） | "ksqlDB uses the AST and creates the logical plan for your statement." | https://docs.confluent.io/platform/current/ksqldb/operate-and-deploy/how-it-works.html | SQL→AST→logical plan，对应"第一流图=逻辑节点图" |
| F3 | 确认命中（含等同） | "From the logical plan, the ksqlDB engine creates the physical plan, which is a Kafka Streams DSL application with a schema."；EXPLAIN 输出 execution plan(PROJECT/AGGREGATE/REKEY/SOURCE 步骤) + Processing Topology(KSTREAM-SOURCE/KSTREAM-MAP/KSTREAM-FILTER 等内置处理器 DAG) | https://docs.confluent.io/.../how-it-works.html ; https://docs.confluent.io/.../explain.html | logical plan→physical plan(topology) 两级映射=字面命中；物理算子取自 Kafka Streams 内置处理器集合=预设算子库（字面）；"一个算子承载多个逻辑节点"=Kafka Streams 子拓扑内 processor fusion——按等同，未取得明示 verbatim |
| F4 | 公开资料不足（未确定，含部分正向反据） | "There's no master node or coordination among them required."；但 "Each ksqlDB Server instance runs a ksqlDB engine. Under the hood, the engine parses your SQL statements and builds corresponding Kafka Streams topologies." 且 "distributing the processing load ... across all ksqlDB Server instances" | https://docs.confluent.io/platform/current/ksqldb/operate-and-deploy/how-it-works.html | 严格"管理节点控制工作节点"master-worker 结构：ksqlDB 明示无 master、为对等 server 集群——对**结构限定**构成部分正向反据；但功能上确有"编译出 plan/topology 后在多 server 实例分布执行"，按等同可争。结构层非全异（仍是分布式流引擎），不足以单独触 5 档 |
| F5 | 确认命中（字面） | source：CREATE STREAM/TABLE 指定 backing Kafka topic 从上游读取；sink：CREATE TABLE AS SELECT 的持久查询 "writes continuously to its output topic"；EXPLAIN topology 含 "Source: KSTREAM-SOURCE-0000000000 (topics: [clickstream])" 及 sink 节点 | https://docs.confluent.io/.../how-it-works.html ; https://docs.confluent.io/.../explain.html | 输入通道(source topic/stream，来自数据生产系统 Kafka)+输出通道(output topic，至数据消费系统)，逻辑流/逻辑表抽象屏蔽具体 IO |

## 已检查文档清单
- ksqlDB Architecture / How it works（current 版官方文档，持续维护，反映 2020.05.08 后产品状态；含 AST→logical plan→physical plan、no master node、source/sink topic、ksqlDB engine） — https://docs.confluent.io/platform/current/ksqldb/operate-and-deploy/how-it-works.html （落盘 ksqldb-how-it-works.html 180KB，已 Grep 校验 verbatim 命中）
- EXPLAIN 语句文档（execution plan 步骤 + Kafka Streams Processing Topology DAG） — https://docs.confluent.io/platform/current/ksqldb/developer-guide/ksqldb-reference/explain.html （落盘 ksqldb-explain.html 139KB）
- Confluent blog "ksqlDB Execution Plans: Move Fast But Don't Break Things"（execution plan = DAG of steps；topology built from execution plan）— https://www.confluent.io/blog/building-ksqldb-event-streaming-database/ （发布 2020-05-01，早于授权日，仅作背景，不计入证据）

## 最终判定
**第 3 档：高度疑似（≥60% 确认命中且无整体正向反据）**

判定依据：
- F1/F2/F5 字面命中、F3 含等同命中——即"以 SQL 定义流作业（CREATE STREAM/TABLE + 查询）→ 解析为 logical plan → 转 physical plan(Kafka Streams topology)→ 内置处理器算子 DAG → source topic 输入 / sink topic 输出"这条核心链路与权 1 的 F1/F2/F3/F5 高度吻合，logical→physical 两级流图映射（专利核心区分限定）字面成立。
- 命中比例 4/5（F3 含等同），≥60%。
- 唯一不确定项 F4：ksqlDB 明示"no master node"，与权 1 严格的"管理节点控制工作节点"master-worker 结构存在差异，对结构限定构成**部分**正向反据；但 ksqlDB 仍是"编译出执行计划后在多 server 实例分布执行"的分布式流引擎，整体架构层并非与专利完全不同，不构成 5 档"架构层不同"的整体排除条件；且功能等同（plan→分布式执行）可争。故按纪律落第 3 档而非 2 档（F4 未达确认命中）、亦非 5 档（无整体正向反据）。
- F3 "一个算子承载多个逻辑节点（算子合并/operator fusion）"末句仅取得等同支持、无明示 verbatim，故 F3 计等同而非字面，整体不到第 2 档全字面/全确认。

## 升级路径（第 3 档）
- F3 算子合并：抓取 Kafka Streams 官方文档中 sub-topology / processor fusion 的明示 verbatim（多个逻辑步骤合并进同一 sub-topology/task），或对一段含 filter+project+aggregate 的 KSQL 跑 EXPLAIN 的实际输出，看多个逻辑步骤是否映射进同一 sub-topology，取明示证据把 F3 从"等同"升为"字面"。
- F4：核实 ksqlDB 集群对**同一持久查询**是否按 Kafka 分区把任务分配到不同 server 实例执行（即"编译节点 → 分布式 worker 执行"的功能等价是否成立），以及 headless/interactive 模式下提交节点与执行节点的关系，判定能否以等同方式补强 F4。补强后可升至第 2 档。

## 总结一句话
ksqlDB 以 SQL 定义流作业并经 logical plan→physical plan(Kafka Streams topology) 两级映射、source/sink topic 对应输入输出通道，F1/F2/F3(含等同)/F5 命中、仅 F4 master-worker 结构存差异且无整体反据，落第 3 档（高度疑似）。

---
> 免责声明：本 verdict 仅为技术特征比对线索与证据链，非法律意见，不构成"已侵权"结论。
