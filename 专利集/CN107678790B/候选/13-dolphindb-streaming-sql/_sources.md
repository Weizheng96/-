# 证据索引 — 13-dolphindb-streaming-sql

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 自 v3.00.4（2025） | 官方文档 | https://docs.dolphindb.com/en/Streaming/Streaming_SQL.html （已 curl 落盘 StreamingSQL.html, 40KB） | registerStreamingSQL("select ... left join ...") = SQL 驱动；"creates an execution plan and initializes operator states"；"passed up the execution chain"；Job management 独立 job 集中管理；结果 change log stream table + subscribe 输出 |
| 2 | 2025-11-17 | 官方 Medium | https://medium.com/@DolphinDB_Inc/dolphindb-streaming-sql-real-time-at-the-speed-of-thought-24b5fcea92b7 | 偏用例/特性；未述 logical/physical plan、未述算子合并 |
| 3 | — | 官方文档 | https://docs.dolphindb.com/en/about_dolphindb.html | controller 管 chunk 元数据 + data node 存数据 = 分布式 master-worker 类架构 |
| 4 | 公布 2020-08-13 | USPTO 专利（**非本候选**） | https://patents.google.com/patent/US20200257689A1 | "Structured cluster execution for data streams" 受让人 = **Databricks Inc**；含 logical→physical query plan 强表述但**不可归于 DolphinDB** |
| 5 | — | 官方文档 | https://docs.dolphindb.com/en/Streaming/streaming_engines.html | 列出 10+ 流计算引擎（时序/响应式状态/横截面/会话窗/异常检测/规则等）；输出可到 stream table/MQ/DB/API client |
| 6 | — | 官方文档 | https://docs.dolphindb.com/en/Tutorials/StreamEngineParser.html | Stream Engine Parser 把**脚本 metric 表达式**（非 SQL）解析成多引擎级联 pipeline；"combining the appropriate engines" |

## 检索 query 留痕
### Phase 1 — WebSearch（串行 4 条）
1. `DolphinDB streaming SQL stream computing engine documentation architecture` → 命中官方 Streaming SQL/Engines/Parser/pub-sub/HA，强信号。
2. `DolphinDB streaming SQL parser logical plan physical plan operator execution chain` → 命中 Medium + USPTO 专利（注意 logical→physical 表述属 Databricks 专利）。
3. `"Structured cluster execution for data streams" patent assignee DolphinDB OR Zhejiang` → 确认 US20200257689A1 = Databricks，排除误归。
4. `DolphinDB 流计算 专利 流式SQL 执行计划 浙江智臾` → 厂商浙江智臾；DolphinDB 有集群/流数据中国专利（CN117573656B 等），与本专利两级流图主题不直接对应。

### Phase 2 — WebFetch/curl（串行）
- WebFetch 上述 URL 1/2/3/4/5/6；curl 落盘 StreamingSQL.html 并 Grep 取 verbatim。

## 关键澄清
- DolphinDB 有两条流处理路径：(a) **Streaming SQL**（自 v3.00.4，真 SQL 驱动，有 execution plan + operator execution chain + job 管理）；(b) **流计算引擎 + Stream Engine Parser**（脚本 metric 表达式驱动的引擎级联，非 SQL）。本判定以 (a) Streaming SQL 路径为准。
- 含"logical plan→physical plan"强表述的专利属 **Databricks**（US20200257689A1），不可归于本候选——已剔除误归。
