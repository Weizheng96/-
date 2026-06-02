# 证据索引 — 03-tech-cassandra

候选：Apache Cassandra（vnode + NetworkTopologyStrategy）/ 组织：DataStax
专利公开日：2017-12-01（本判定核心为架构事实，与时间窗无关）

## Phase 1 — react 粗筛 WebSearch（串行，禁并行）

| # | query | 命中要点 | 关键源 |
| --- | --- | --- | --- |
| 1 | `Cassandra NetworkTopologyStrategy replica placement rack` | NetworkTopologyStrategy 同一 DC 内顺时针走 ring 把副本放不同 rack；rack 数 ≥ RF 时每副本保证落不同 rack → 支持 F2 反亲和/跨机架 | cassandra.apache.org/doc/4.1/.../dynamo.html；docs.datastax.com .../archDataDistributeReplication.html |
| 2 | `Cassandra primary replica concept masterless peer-to-peer all replicas equal` | Cassandra=masterless/peer-to-peer，节点功能完全对等，无 primary/leader/master 节点；"All replicas are equally important; there is no primary or master replica." → 对 F0 构成反向架构事实 | cassandra.apache.org/_/cassandra-basics.html；axonops.com .../distributed-data/；quabase.sei.cmu.edu .../Cassandra_Data_Replication_Features |
| 3 | `Cassandra vnode token distribution balance even data across nodes` | vnode（num_tokens 默认 256 / allocate_tokens_for_keyspace）使 token range 均匀分布；节点加入承担均等数据份额，节点故障负载均匀分摊 → 支持 F1（但 Cassandra 无"主分区"概念，实为所有副本均匀） | docs.datastax.com .../archDataDistributeVnodesUsing.html；instaclustr.com/blog/cassandra-vnodes-how-many-should-i-use/ |

## Phase 2 — 深抓 WebFetch（串行）

| # | URL | verbatim 关键证据 |
| --- | --- | --- |
| 1 | https://cassandra.apache.org/_/cassandra-basics.html | 「Cassandra also has a masterless architecture – any node in the database can provide the exact same functionality as any other node」「Any node can act as the coordinator.」→ 无 primary 副本对外服务 vs 备副本容错 的二元结构 |
| 2 | https://cassandra.apache.org/doc/4.1/cassandra/architecture/dynamo.html | 「As every replica can independently accept mutations to every key that it owns」「Write operations are always sent to all replicas, regardless of consistency level.」；"primary range" 指 token 归属范围（数据所有权），非"主副本"语义；NetworkTopologyStrategy 跨 rack 放置（F2 等同）；节点增减后 vnode 增量再均衡 + anti-entropy repair（sub-range/incremental repair, Merkle tree）（F3 等同） |

## 结论指向
F0 在 Cassandra 上有**正向反向架构事实**（masterless，所有副本平等，无主/备副本之分），属第5档 (c) 架构层级不同。F1/F2/F3 在"所有副本"层面有功能对应，但 F0 前提不成立 → 整条权利要求主题（主分区 + 对应备分区的主备结构）不读到该产品。
