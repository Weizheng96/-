# 证据索引 — 06-yugabyte-yugabytedb

## 检索 query 留痕（Phase 1，react 串行）
1. `YugabyteDB tablet replica placement zone load balancer`
2. `YugabyteDB cluster balancing tablet leader high low load move underloaded node`
3. `YugabyteDB placement policy replica different fault domain rack anti-affinity primary leader follower`

## 证据表
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 文档当前版（2026 抓取） | 官方文档 | https://docs.yugabyte.com/stable/architecture/docdb-sharding/cluster-balancing/ （本地：候选/06-yugabyte-yugabytedb/cluster-balancing.html） | F1/F3 负载度量与均衡："moves tablet data and leaders to evenly distribute data and query load"；F2 placement："one replica of each tablet in three separate regions" |
| 2 | datePublished 2021-06-29 / dateModified 2024-10-16 | 官方博客 | https://www.yugabyte.com/blog/auto-balancing-data-in-yugabytedb-a-distributed-sql-database/ （本地：候选/06-yugabyte-yugabytedb/auto-balancing-blog.html） | F3："total number of tablets and its replicas is taken to be a measure of the load on a node"；F0："leader ... and the standby copies as followers"；F1："uniformly distributed across nodes"；F2："load balancer respects this placement by not transferring any load" |
| 3 | 文档当前版 | 官方文档 | https://docs.yugabyte.com/stable/explore/fault-tolerance/handling-rack-failures/ | F2 反亲和："replicas in different racks"，RF-3 容忍一个 fault domain 故障 |

## 备注
- WebFetch 被网络策略拦截（docs.yugabyte.com 安全校验失败 / yugabyte.com 证书校验失败），改用强制兜底 `curl -ksSL --tlsv1.2`，两个 HTML 均成功落地（cluster-balancing.html 124KB / auto-balancing-blog.html 376KB），verbatim 经本地 Grep 核验。
- 时间窗：全部证据 ≥2021，远晚于专利公开日 2017-12-01，时间合规。
