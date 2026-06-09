# 09-transwarp-slipstream sources（检索留痕）

## Phase 1 — react 粗筛 WebSearch query 留痕
1. `星环科技 Slipstream 流计算 SQL StreamSQL 执行计划 逻辑计划 物理计划`
   - 命中：官方产品页 / 文档站 / StreamSQL 博客；确认 Slipstream 为星环自研实时流计算引擎，StreamSQL 兼容 ANSI SQL 2003；Slipstream Studio 监控"任务逻辑执行和物理执行计划"。→ 命中 F1/F2/F3 信号，缩小特征词。
2. `星环科技 Slipstream 架构 Spark Driver Executor master worker 调度 StreamSQL source sink 输入 输出`
   - 命中：架构博客 + 文档；确认 Worker/Server 故障恢复、分布式任务调度、source→sink 实时 ETL。→ 命中 F4/F5 信号。

（2 条即定位真实本领域产品并取得各 F# 正向信号，未触发早剪枝，进入 Phase 2 深抓。）

## Phase 2 — 落盘文档（curl 抓取，UTF-8；transwarp.cn 为 NUXT SPA，正文在 __NUXT__ 内嵌 JSON，已本地解析）
- `blog-1098.html`（424KB）— Transwarp Slipstream——分布式实时计算引擎产品页 / 博客。含 productFunction（StreamSQL / ANSI SQL 2003 verbatim）、Slipstream Studio "任务逻辑执行和物理执行计划"、"当 Worker 或者 Server 发生故障时，实现秒级别的任务自动恢复"、"分布式计算引擎，task级自动重试至可用节点"。原始博客发布日 2018-12-24，但 productFunction / 优势 / Studio 段为现行 9.x 商用产品内容（站点 lastCommitDate 2024-2025）。
  - URL: https://www.transwarp.cn/blog/1098
- `slipstream-intro.html`（382KB）— Slipstream 9.3 官方文档"Slipstream简介"。含 **3 级优化器** verbatim（规则优化器→逻辑执行计划；成本优化器→物理执行计划；代码生成器→更高效执行代码 / Java Byte Code）、CREATE STREAM DDL。文档版本 9.3（2024），晚于授权日 2020.05.08。
  - URL: https://www.transwarp.cn/doc/slipstream/9.3/slipstream-introduction
- `blog-190-streamsql.html`（523KB）— 基于流的 SQL 引擎 StreamSQL 基础介绍。含 Input Stream / Derived Stream / StreamJob / receiver / Kafka 数据源 verbatim。原始发布日 2017-03-31（早于授权日，仅作机制背景，不单独计入时间窗证据）。
  - URL: https://www.transwarp.cn/blog/190
- `sql-ddl.html`（377KB）— Slipstream 9.3 SQL 参考 DDL 页 TOC（CREATE/DROP/ALTER 作用于 DATABASE/TABLE/STREAM/APPLICATION/STREAMJOB；含"5.2.3 Stream 操作"与 DML"输入输出"章节；lastCommitDate 2024-08）。各子节正文体为懒加载未随首屏返回。
  - URL: https://www.transwarp.cn/doc/slipstream/9.3/sql-referance--slipstream-ddl
- 本地解析中间产物：`_extract.txt`（各文档关键术语 verbatim 切片）。

## 工具受限明示
- WebFetch 对 transwarp.cn（NUXT SPA）返回壳页，正文在 __NUXT__ JSON / 懒加载 → 改用 curl 落盘 + 本地正则解析 __NUXT__ 内嵌 JSON 提取 verbatim 正文（成功）。
- sql-ddl 各子节正文体懒加载未返回，以 TOC + slipstream-intro 的 CREATE STREAM verbatim 佐证，未伪造子节正文。
- 未对 patents.google.com 检索星环自有同主题专利（列为升级路径，证书拦截风险）。
