# 01-tech-apache-flink 检索留痕（_sources.md）

## Phase 1 — react 粗筛 query 留痕
- query 1: `Flink SQL parse to logical plan RelNode then StreamGraph JobGraph operator chaining architecture`
  → 强命中。返回 Alibaba Cloud 技术博客（Deep Insights into Flink SQL / In-depth Analysis of Flink Job Execution / Flink Runtime Architecture）+ Apache Flink 官方架构文档。verbatim 摘要直接覆盖 Calcite RelNode 逻辑计划 → Physical Rel DAG → StreamGraph → JobGraph + operator chaining。
- query 2: `Flink SQL CREATE TABLE connector source sink JobManager TaskManager schedule execution graph`
  → 强命中。Apache Flink 官方文档 + Confluent 文档，证实 CREATE TABLE + connector 定义 source/sink（输入/输出通道），table source 读外部系统、table sink 写外部系统。

候选真实存在且明确处于本专利领域（以 SQL 定义流作业的分布式流计算引擎），不剪枝。

## Phase 2 — 深抓 URL 及发布日期
1. Deep Insights into Flink SQL: Flink Advanced Tutorials — Alibaba Cloud（发布日 2020.09.16，晚于授权日 2020.05.08）
   https://www.alibabacloud.com/blog/deep-insights-into-flink-sql-flink-advanced-tutorials_596628
   → F2/F3 第一半：SQL → SQLNode 树 → operation DAG → RelNode DAG → Physical Rel DAG → ExecNode → Transformation DAG → JobGraph。
2. In-depth Analysis of Flink Job Execution: Flink Advanced Tutorials — Alibaba Cloud（发布日 2020.09.16）
   https://www.alibabacloud.com/blog/in-depth-analysis-of-flink-job-execution-flink-advanced-tutorials_596633
   → F3 末句（operator chaining：多个 node 合并进一个 JobVertex/task）+ StreamGraph→JobGraph + F4（JobManager 把 subtask 部署到 TaskManager slot）。
3. Apache Flink 1.11 Documentation: Flink Architecture — 官方一手文档（Flink 1.11 发布于 2020.07，晚于授权日）
   https://nightlies.apache.org/flink/flink-docs-release-1.11/concepts/flink-architecture.html
   → F3 末句 verbatim（"Flink chains operator subtasks together into tasks"）+ F4 verbatim（JobManager master / TaskManagers workers）。
4. Apache Flink Table & SQL Connectors / CREATE TABLE 官方文档（query 2 命中，摘要已足够，未单独 WebFetch）
   https://nightlies.apache.org/flink/flink-docs-master/docs/dev/table/sql/create/
   https://docs.confluent.io/cloud/current/flink/reference/statements/create-table.html
   → F1/F5：CREATE TABLE + connector 定义 source/sink；table source 读外部系统、table sink 写外部系统。

## 工具受限说明
- 未抓取 patents.google.com（环境对其直连可能证书拦截）。Flink 为开源项目，官方文档 + 一手架构文档已足够形成 verbatim 证据链，无需竞品自有专利佐证。
- F1/F5 的 connector 文档以 query 2 的 WebSearch 摘要 verbatim 引用（官方文档原文）；未额外消耗 WebFetch 预算。
