# 证据索引 — 13-aerospike-database

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| S1 | 在线文档（>2017-12-01） | WebFetch | https://aerospike.com/docs/server/architecture/data-distribution | F0：master(读写)+read-only replica；4096 partition 均匀分布；F1：each node ~1/n；F3："nodes are added or removed ... evenly divide partitions ... automatically rebalances" |
| S2 | 在线文档（>2017-12-01） | WebFetch（docs.→aerospike 301） | https://aerospike.com/docs/server/architecture/rack-aware | F2："master copy of a partition and its replica are stored in two separate racks"；"RF≤rack 数 → RF 个 rack 各持一 replica"（副本反亲和+跨rack均匀） |
| S3 | 2023-04-19 | WebFetch | https://aerospike.com/blog/optimizing-server-resources-using-uniform-balance/ | F1："tweaked to even out the number of leader partitions each node has"；F3 问题陈述："Node A 1 partition, node B 3 partitions ... 3x data volume" |

## Phase 1 react 粗筛（WebSearch，串行）
1. `Aerospike partition master replica distribution rack aware` → master/replica + rack-aware 文档命中，架构层级一致（分区-副本放置/再均衡），非网络流量 LB。→ 继续。
2. `Aerospike uniform balance partition distribution algorithm rebalance node add migration` → uniform-balance 均匀分布 + 节点增减自动 rebalance/migration 文档命中。→ 强相关，进 Phase 2。
（2 条即获足够正向信号，未触发早剪枝。）

## 反向证据核查
未发现"不支持副本反亲和 / 不做再均衡 / 仅单副本无主备"等真反向；仅"算法不保证 replica 完全均衡，但通常均衡"为弱化限定语（非反向）。
