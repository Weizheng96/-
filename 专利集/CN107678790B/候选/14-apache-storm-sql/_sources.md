# 证据索引 — 14-apache-storm-sql

## Phase 1 — react 粗筛 WebSearch（串行，3 条即足够转 Phase 2）
1. `Apache Storm SQL internal Calcite logical plan Trident physical plan` → 命中 storm-sql-internal 官方文档 + STORM-1446 JIRA + cs101 blog。确认 Storm SQL = SQL → Calcite 逻辑计划 → 物理计划（物理算子 Filter/Projection/GroupBy）→ Trident topology。强命中 F2/F3 方向。
2. `Apache Storm SQL CREATE TABLE source sink Kafka Nimbus Supervisor worker` → 命中 storm-sql 官方文档（CREATE EXTERNAL TABLE + LOCATION kafka://… 定义 source/sink）+ DZone/Packt 架构文（Nimbus=主、Supervisor-Worker=从）。命中 F1/F4/F5 方向。
3. `腾讯云 EMR 组件 Apache Storm 版本 支持组件列表` → 命中腾讯云 EMR 组件版本概览（589/66338），转 Phase 2 核实时间窗。

## Phase 2 — react 深抓 WebFetch（串行）

| # | 时间/版本 | 类型 | URL | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 1.2.3 文档 | 官方 storm-sql-internal | https://storm.apache.org/releases/1.2.3/storm-sql-internal.html | verbatim：SQL→Calcite 逻辑计划（TableScan/Filter/Projection/GroupBy）→物理计划（物理算子）→直接映射 Trident topologies；表达式编译为 Java code block 塞进 Trident functions；CREATE EXTERNAL TABLE+LOCATION 定义 source/sink |
| 2 | Fix 1.1.0 & 2.0.0；解决 2017-01-23 | JIRA | https://issues.apache.org/jira/browse/STORM-1446 | "Compile the Calcite logical plan to Storm Trident logical plan"，Resolved/Fixed。该机制首次随 Storm 1.1.0（2017）公开 |
| 3 | EMR 文档（截 2024.03） | 腾讯云官方 | https://cloud.tencent.com/document/product/589/66338 | Storm 1.2.3 出现在 EMR-V 2.6.0（2021.07）与 EMR-V 2.7.0（2022.07）；EMR-V 2.8.0（2024.03）Storm 标"—"已移除；Hadoop 3.x 全程无 Storm；主推 Flink 1.12.1–1.18.1 |
| 4 | 2017-01-25 | 第三方 blog | https://cs101.blog/2017/01/25/how-storm-sql-is-executed/ | 代码追踪 SqlNode→RelNode→TridentRel（STORM_REL_CONVERSION_RULES+TridentLogicalConvention），EvaluationFilter/Janino；算子融合细节作者标 TODO 未展开 |

## 工具受限说明
- patents.google.com 未访问（本候选为开源系统 + 腾讯云官方文档已充分，无需）。
- 各 URL 均 WebFetch 成功，未触发 curl 兜底。
