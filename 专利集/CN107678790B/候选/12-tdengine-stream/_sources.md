# 证据索引 — 12-tdengine-stream

## Phase 1 — react 粗筛 WebSearch 留痕
1. `TDengine stream processing CREATE STREAM AS SELECT SQL documentation` → 官方文档 CREATE STREAM ... INTO ... AS SELECT；"define stream transformations in SQL"。强信号。
2. `TDengine stream processing engine internals logical plan physical plan mnode vnode scheduling architecture` → 内部引擎文档：mnode 把逻辑执行计划转物理执行计划并下发 vnode；meta store 存 DAG；snode/vnode 执行节点。
3. `TDengine 3.0 release date stream processing GA 2022` → TDengine 3.0（含 stream 引擎）2022.08.23 GA → 晚于授权日 2020.05.08，时间窗满足。
4. `TDengine "stream processing" mnode "logical execution plan" "physical execution plan" vnode DAG task source agg sink` → 关键 verbatim（见下）。

## 证据索引表
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 文档(2022.08.23 后) | WebFetch 成功 | https://docs.tdengine.com/reference/taos-sql/stream/ | F1/F5：CREATE STREAM [INTO table] AS subquery；[FROM table_name]（regular/super/sub/virtual table）；INTO 目标表 |
| 2 | 文档 | WebFetch 成功 | https://docs.tdengine.com/cloud/stream/ | F1：CREATE STREAM ... INTO stb_name AS subquery + 示例 select ... from ... interval(5s) |
| 3 | 文档 | WebSearch 抽取(URL 多次一致) | https://docs.tdengine.com/inside-tdengine/stream-processing-engine/ | F2/F3/F4：逻辑执行计划→物理执行计划→DAG；mnode 下发 vnode 调度；source/sink/agg task |
| 4 | 公告 2022.08.23 | WebSearch | https://www.globenewswire.com/news-release/2022/08/23/2502937/0/en/... | TDengine 3.0 发布日期（时间窗证据） |
| L1(curl) | - | curl 落盘 11754B SPA 空壳 | 候选/12-tdengine-stream/stream-processing-engine.html · query-engine.html · architecture.html | 渲染型 SPA，静态正文为空；详见工具受限说明 |

## 工具受限明示
- `inside-tdengine/*` 内部引擎页 WebFetch 返回 HTTP 404（渲染型 SPA 路由）；curl 三页均为同一 11754 字节空壳，正文由 JS 渲染，无法静态抓取。
- 内部引擎页正文以 WebSearch 在 3 次独立检索中返回的一致 verbatim 为准，互相印证，未伪造；如需 100% 字面核验需在浏览器渲染后取证。

## 关键 verbatim（来源 inside-tdengine/stream-processing-engine/，WebSearch 抽取）
- "The mnode uses the vgroups information to convert the logical execution plan into a physical execution plan, and further generates a Directed Acyclic Graph (DAG) for the stream task."
- "The mnode contains four logical modules related to stream processing, including task scheduling that converts logical execution plans into physical execution plans and distributes them to vnodes."
- "On each vnode, at least two stream tasks are deployed: one is the source task ... reading data from the WAL (and from the TSDB when necessary) ... distributing the processed results to downstream tasks; the other is the sink task ... writing the received data into the vnode it resides in."
- "the agg task is prioritarily executed on the snode ... If there is no snode in the cluster, mnode will randomly select a vnode to schedule the execution of the agg task."
- "The mnode plays a crucial role in issuing control commands to stream processing tasks ... pausing, resuming execution, deleting stream tasks, and updating upstream and downstream information."

## CREATE STREAM verbatim 语法/示例（taos-sql + cloud）
- "CREATE STREAM [IF NOT EXISTS] [db_name.]stream_name options [INTO [db_name.]table_name]... AS subquery"；"[FROM [db_name.]table_name]"；"a trigger table can be a regular table, supertable, subtable, or virtual table"。
- `create stream current_stream into power.current_stream_output_stb as select _wstart, _wend, max(current) as max_current from power.meters where voltage <= 220 interval (5s);`
