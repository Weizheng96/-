# 证据索引 — 11-snowflake-dynamic-tables

## Phase 1 — react 粗筛 query 留痕（≤4，串行）
1. `Snowflake Dynamic Tables declarative SQL incremental refresh query plan DAG` → 命中（官方 doc + 官方 blog 确认声明式 SQL 定义 + 自动增量刷新 + 依赖 DAG 管线）
2. `Snowflake architecture cloud services layer virtual warehouse query optimizer logical physical plan compute nodes` → 命中（三层架构：cloud services 层做解析/优化/计划生成/dispatch；virtual warehouse = MPP compute nodes 执行）
3. `Snowflake EXPLAIN query profile logical plan physical plan operator tree compilation` → 命中（明确"逻辑 explain plan"与"physical execution plan = DAG of physical operators"两级转换）
4. （未用满；Phase 1 已获足够正向信号，直接进 Phase 2）

## Phase 2 — react 深抓（WebFetch + curl 落盘）

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 持续更新（≥2023 GA，晚于 2020.05.08） | 官方 doc（HTML 落盘 738KB） | https://docs.snowflake.com/en/user-guide/dynamic-tables-about ／ `dynamic-tables-about.html` | F1/F2/F5：声明式 SELECT 定义、解析 query 识别 base table、推断依赖图、自动 dispatch refresh、virtual warehouse 执行 |
| 2 | 持续更新（晚于 2020.05.08） | 官方 doc（HTML 落盘 792KB） | https://docs.snowflake.com/en/sql-reference/sql/explain ／ `explain.html` | F2/F3：明确"逻辑 explain plan"概念；EXPLAIN 编译 SQL；操作（table scan/join）及其逻辑关系；parentOperators 父子链接结构 |
| 3 | 持续更新（晚于 2020.05.08） | 官方 doc（WebFetch verbatim） | https://docs.snowflake.com/en/user-guide/intro-key-concepts | F4/架构：cloud services 层"coordinate activities…process user requests, from sign-in to query dispatch"+"query parsing and optimization"；virtual warehouse = MPP compute cluster 执行 SQL |
| 4 | 2025（晚于 2020.05.08） | 技术深度文（Snowflake 官方 Medium，WebFetch verbatim） | https://medium.com/snowflake/anatomy-of-a-snowflake-query-a-deep-dive-into-the-execution-engine-ca9061022c47 | F2/F3：Parser→内部表示；Optimizer 把声明式 query 转成 procedural plan；"optimized logical plan is translated into a Physical Execution Plan…DAG composed of physical operators" |

> 说明：Snowflake 渲染型文档站，curl 落盘 HTML 体积正常（含全文 JSON 数据），verbatim 引文以 WebFetch 提取为准。patents.google.com 未单独抓取（证书拦截风险），未检索到 Snowflake 2020.05.08 后同主题自有专利的直接公开引文，明示不伪造。
