# 证据索引 — 05-cockroachlabs-cockroachdb

## Phase 1 react WebSearch（串行，3 条，均强信号，不剪枝）
1. `CockroachDB replica placement locality constraints rebalancing` → Replication Layer 文档 / tech-notes/rebalancing.md / RFC 20170602 / Configure Replication Zones / issue #85652。
2. `CockroachDB replication zone diversity anti-affinity replica placement same locality` → Replication Layer / Node Locality in K8s 博客 / Multi-Region under-the-hood。确认 "high locality diversity"、"one replica per AZ"=反亲和。
3. `CockroachDB rebalance replicas from overloaded store to underutilized store load balancing` → tech-notes/rebalancing.md / store_rebalancer.go / automated-rebalance-and-repair 博客。确认 StoreRebalancer 把 lease/replica 从 overloaded store 迁到低负载 store。

## 证据索引（Phase 2 WebFetch，串行）
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 现行 stable（>2017-12-01） | 官方文档 | https://www.cockroachlabs.com/docs/stable/architecture/replication-layer | leaseholder=唯一服务读/提议写=主；副本随节点变化再均衡；按 replica count+CPU/QPS 自动 rebalance；placement constraint/locality survivability 约束 → F0/F1/F2/F3 |
| 2 | master（>2017-12-01） | 源码内 tech-note | https://github.com/cockroachdb/cockroach/blob/master/docs/tech-notes/rebalancing.md | range count 均衡(F1)；diversity-of-localities 反亲和、从不降低 diversity(F2)；StoreRebalancer 处理 overloaded store(F3)；leaseholder=主(F0) |
| 3 | master（StoreRebalancer 自 v2.1/2018） | 源码注释 | https://github.com/cockroachdb/cockroach/blob/master/pkg/kv/kvserver/store_rebalancer.go | infinite loop 检测 store 在 range count/QPS/disk 维度是否 overloaded，超阈值则迁 leases/replicas → F3（range count 维度为字面） |

## 时间合规
CockroachDB 持续开源发布；StoreRebalancer 自 v2.1（2018）引入；引用 stable/master 文档为现行版本，均晚于专利公开日 2017-12-01。证据时间合规。

## 反向证据排查
未发现 "不支持/仅限/explicitly excludes" 形式真反向证据。所见限定（如 "load-based goals do not override placement constraints/survivability"）属机制约束说明，非排除特征。
