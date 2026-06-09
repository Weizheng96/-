# 证据索引 — 07-materialize

候选：Materialize（Materialize Inc.）｜类型：产品｜专利公开（授权）日基准：2020.05.08

## Phase 1 — react 粗筛 WebSearch query 留痕
1. `Materialize streaming SQL database architecture dataflow plan optimization logical physical plan`
   - 命中：SQL → IR program → optimization passes → Differential Dataflow program；Adapter/Compute 三逻辑组件，environmentd/clusterd 两物理组件，clusterd 跑 Timely Dataflow 可扩展到多 process/replica。强信号，缩小到 EXPLAIN/plan 维度。
2. `Materialize EXPLAIN PLAN raw decorrelated optimized physical plan MIR HIR LIR dataflow operators`
   - 命中（决定性）：`SQL ⇒ raw plan ⇒ decorrelated plan ⇒ optimized plan ⇒ physical plan ⇒ dataflow`；HIR/MIR/LIR 三级 IR；physical plan 阶段 "maps plan operators to differential dataflow operators"。
3. `Materialize clusterd environmentd worker timely dataflow scheduling fuse operators single dataflow architecture`
   - 命中：environmentd=control plane（指挥 clusterd），clusterd=data plane（跑 Timely Dataflow）；"operators can execute in a fused fashion"。覆盖 F3 末句 + F4 master-worker。
4. `Materialize CREATE SOURCE CREATE SINK SQL Kafka source sink connector documentation`
   - 命中：`CREATE SOURCE`（从 Kafka/Redpanda 等上游读取）、`CREATE SINK`（写到下游 topic）。覆盖 F1（SQL+source/sink DDL）+ F5（输入/输出通道）。

## Phase 2 — react 深抓
- WebFetch `https://materialize.com/docs/sql/explain-plan/` → ECONNREFUSED，按协议改 curl。
- curl 落盘 `explain-plan.html`（247,904 bytes，正文完整）→ 提取编译流水线 + Fused 算子 verbatim（最直接的 plan 展开输出文档）。
- curl 落盘 `architecture.html`（162,324 bytes）→ SPA，正文在 JS bundle，HTML body 空；架构 verbatim 以 WebSearch 官方 blog 摘要为准（已标注）。
- curl `https://materialize.com/docs/get-started/key-concepts/` → SSL/TLS handshake 失败（exit 35）；F5 改用 WebSearch CREATE SOURCE/SINK 官方文档摘要。

## 已落盘文件
- `explain-plan.html` — Materialize EXPLAIN PLAN 官方文档（L1 主证据，curl 成功，正文完整）
- `architecture.html` — Materialize 架构 blog（SPA，正文需 JS 渲染，仅作存档）

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 现行文档 | 官方文档 | https://materialize.com/docs/sql/explain-plan/ | SQL⇒raw⇒decorrelated⇒optimized⇒physical⇒dataflow；physical 阶段 maps plan operators to differential dataflow operators；Fuses adjacent operations / Fused Map-Filter-Project |
| 2 | 现行 blog | 官方 blog | https://materialize.com/blog/materialize-architecture/ | Adapter 编译 query→IR program；Compute 经 optimization passes→Differential Dataflow program；environmentd(control)/clusterd(data plane, Timely Dataflow, 多 replica) |
| 3 | 现行文档 | 官方文档 | https://materialize.com/docs/sql/create-source/kafka/ | CREATE SOURCE 从 Kafka/Redpanda 上游读取数据流 |
| 4 | 现行文档 | 官方文档 | https://materialize.com/docs/sql/create-sink/kafka/ | CREATE SINK over 物化视图/source/table，写到下游 Kafka topic |
