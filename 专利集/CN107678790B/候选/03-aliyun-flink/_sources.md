# 03-aliyun-flink 检索留痕（_sources.md）

## Phase 1 — react 粗筛 query
1. `阿里云实时计算 Flink SQL 作业 逻辑计划 物理计划 operator chaining 算子链`
   → 命中：算子链(operator chaining)将多算子串联到一个 slot；阿里云 Flink 提供企业级 SQL 算子优化；pipeline.operator-chaining 参数拆链。信号强。
2. `阿里云实时计算Flink CREATE TABLE connector source sink SQL 解析 逻辑计划 StreamGraph JobGraph JobManager TaskManager`
   → 命中：SQL→parse→AST(SqlNode)→逻辑执行计划→优化器→物理执行计划→codegen Transformations→JobGraph；CREATE TABLE ... WITH connector 定义源表/结果表；JobManager/TaskManager 资源。覆盖 F1-F5。
3. （F4 补充）`阿里云实时计算Flink JobManager 管理节点 TaskManager 工作节点 调度 部署 文档`
   → 命中：JobManager=集群 Master 协调者，管理从节点 TaskManager，跟踪分布式任务并调度。

## Phase 2 — react 深抓（WebFetch / curl）
- WebFetch https://www.alibabacloud.com/help/zh/flink/realtime-flink/user-guide/optimize-flink-sql （更新 2025-08-08）— 高性能 SQL 优化，SQL 算子级优化，未给架构 verbatim。
- WebFetch https://www.alibabacloud.com/help/zh/flink/support/faq-about-sql-performance （更新 2025-05-26）— `pipeline.operator-chaining: 'false'` 拆分算子链；"拓扑图"节点；本地/全局两层聚合优化。
- WebFetch https://www.alibabacloud.com/help/zh/flink/realtime-flink/getting-started/getting-started-for-a-flink-sql-deployment （更新 2026-01-23）— CREATE TEMPORARY TABLE ... WITH ('connector'='datagen'/'print') 定义 source/sink；INSERT INTO 写下游；控制台部署运行 SQL 作业。【已 curl 落盘 aliyun-flink-sql-quickstart.html，36KB】
- WebSearch 摘要（developer.aliyun.com / help.aliyun.com 产品概述）— JobManager=Master 协调者管理 TaskManager 从节点并调度分布式任务。

## 落盘文件
- aliyun-flink-sql-quickstart.html （L1，SQL 快速入门页，含 CREATE TABLE source/sink + INSERT INTO）

## 备注
- 阿里云实时计算 Flink 版完全兼容开源 Apache Flink 内核；SQL 解析→逻辑计划→物理计划→operator chaining→JobGraph 链路属 Flink/Blink SQL 标准机制，阿里云文档明确暴露这些概念（拓扑图、算子链、SQL 算子优化）。
- 全部引用文档更新日期均晚于专利公开日 2020.05.08；阿里云实时计算 Flink 版（全托管）商用化亦在 2020 之后规模铺开，时间窗合规。
