# 证据索引 — 12-couchbase-server

## Phase 1 react 粗筛（WebSearch，串行，禁并行）
1. `Couchbase vBucket active replica distribution rebalance`
   → 命中官方文档 vbuckets / rebalance / server group awareness；明确 active vBucket（主，对外服务）+ replica vBucket（备）、active 与 replica 放不同节点、rebalance 重分布、server group 把 active 与 replica 放不同 group。**强信号，不剪枝。**
2. `Couchbase Server Group Awareness replica placement different group`
   → "active vBuckets located on one group, replicas located on another group"；"all replicas of a given vBucket must reside in separate server groups"。F2 反亲和（排除分组）强命中。
3. `Couchbase rebalance vbucket even distribution across nodes equal number`
   → "The end goal of rebalance is that each server within the cluster ends up with the same number of vBuckets"；"distributes vBuckets evenly"。F1/F3 均匀分布命中。

## Phase 2 深抓（WebFetch，串行）
| # | 类型 | URL | 命中要点 |
| --- | --- | --- | --- |
| 4 | WebFetch | https://docs.couchbase.com/server/current/learn/buckets-memory-and-storage/vbuckets.html | F0：active vBucket（写只写 active，读主要走 active，replica 容错）；F1："distributes vBuckets evenly across ... nodes"；F2："The active vBucket and its replicas are always on different nodes" |
| 5 | WebFetch | https://docs.couchbase.com/server/current/learn/clusters-and-availability/groups.html | F2：active 在一个 group，replica 在另一 group；"all replicas of a given vBucket must reside in separate server groups"（排除主副本所属分组 = rack/zone awareness） |
| 6 | WebFetch | https://docs.couchbase.com/server/current/learn/clusters-and-availability/rebalance.html | F1/F3："On rebalance, vBuckets are redistributed evenly among currently available Data Service nodes."；节点增减/故障触发 redistributes |

## 反向证据检查
- 未检索到任何"Couchbase 不支持 active/replica 分离 / 仅单副本 / replica 与 active 同节点 / explicitly excludes 反亲和"的反向陈述。
- "out of scope / future work" 类限定语：无。
- 结论：无真反向证据。

## 时间窗说明
- Couchbase Server 的 vBucket / replica / rebalance 为长期存在的核心架构；Server Group Awareness 在 Enterprise 版长期可用，current 版本文档（2026 检索时）持续维护。产品在 2017-12-01 之后持续公开发售并维护，时间窗满足（产品延续性证据）。
