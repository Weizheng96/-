# 证据索引 — 08-google-dataflow-beam-sql

## Phase 1 — react 粗筛（WebSearch）
1. `Apache Beam SQL pipeline PTransform logical plan Calcite`
   - 命中：Beam SQL → PTransform；Beam SQL 用 Apache Calcite；BeamQueryPlanner / RelNode→BeamRelNode（logical plan）。对应 F1/F2。
2. `Google Cloud Dataflow fusion optimization fused stages pipeline runner`
   - 命中：Dataflow 把 steps 转 stages；fuse 多个 steps 进一个 stage；execution graph；Dataflow service 分发到 workers。对应 F3/F4/F5。

（2 条即获足够信号，未用满 4 条；未触发早剪枝。）

## Phase 2 — react 深抓（WebFetch）
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 持续维护（开源文档，当前 Beam 2.69/2.70 在线版，>2020.05.08） | HTML | https://beam.apache.org/documentation/dsls/sql/overview/ | "Your SQL query is translated to a PTransform"；"SqlTransform: the interface for creating PTransforms from SQL queries"；Calcite；CREATE EXTERNAL TABLE（SQL DDL 定义表）→ F1/F2 |
| 2 | 持续维护（>2020.05.08） | HTML | https://docs.cloud.google.com/dataflow/docs/pipeline-lifecycle | "Dataflow creates an execution graph from the code…"；"Optimizations can include fusing multiple steps or transforms in your pipeline's execution graph into single steps"；"The Dataflow service automatically parallelizes and distributes the processing logic… to the workers" → F2/F3/F4 |
| 3 | 持续维护（>2020.05.08） | HTML | https://docs.cloud.google.com/dataflow/docs/concepts/execution-details | "When Dataflow runs a job, it converts the steps of the pipeline into stages"；"a stage represents a single unit of work that is performed by Dataflow"；"Dataflow might fuse multiple steps into one stage" → F3 |

## 工具限制说明
- cloud.google.com 301 跳转到 docs.cloud.google.com，已按重定向 URL 重新抓取，成功取得 verbatim。
- 未抓 Google 自有同主题专利；主特征已由官方文档充分佐证，不影响档位判定。
- 上述官方文档为持续维护的在线版本，内容晚于 2020.05.08 时间窗（fusion / steps→stages 机制为 Dataflow 长期既有特性，2020 前后均成立）。
