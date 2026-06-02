# 12-couchbase-server verdict

## 候选基本信息
- 名称：Couchbase Server（vBucket + replica + server group awareness）
- 组织：Couchbase Inc（NASDAQ: BASE）
- 类型：产品
- 初判 F#：F0,F1,F2,F3
- 专利公开日：2017-12-01

## 检索粗筛
Phase 1 react 串行 WebSearch（详见 _sources.md）：
1. `Couchbase vBucket active replica distribution rebalance` → 命中官方 vbuckets / rebalance / groups 文档，强信号。
2. `Couchbase Server Group Awareness replica placement different group` → F2 反亲和（排除分组）命中。
3. `Couchbase rebalance vbucket even distribution across nodes equal number` → F1/F3 均匀分布命中。
判定：强信号，不触发早剪枝。进入 Phase 2 深抓（3 篇官方文档 WebFetch）。

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F0 | 命中（字面） | "active vBuckets"；"Data write operations write only to active vBuckets"；"the system can read items from replica vBuckets when needed" | https://docs.couchbase.com/server/current/learn/buckets-memory-and-storage/vbuckets.html | 多节点 + 1024 个 vBucket（数据分区），每 vBucket 有 active（主，对外写/读服务）+ replica（备，容错），可配置 ≥1 replica。主备二元结构字面命中 F0。 |
| F1 | 命中（字面/近字面） | "The system distributes vBuckets evenly across the memory and storage resources of nodes"；"On rebalance, vBuckets are redistributed evenly among currently available Data Service nodes"；（搜索摘要）"the end goal of rebalance is that each server within the cluster ends up with the same number of vBuckets" | vbuckets.html / rebalance.html | active vBucket（=主分区）在各节点间均匀分布，目标"每节点相同数量"即任意两节点之差 ≈0 < 第一阈值（优选 1）。F1 字面命中。 |
| F2 | 命中（字面 + 等同） | "The active vBucket and its replicas are always on different nodes in the cluster"；"active vBuckets ... located on one group, while the corresponding replicas are located on another group"；"all replicas of a given vBucket must reside in separate server groups" | vbuckets.html / groups.html | 排除主副本所在节点（different nodes）= 第二类节点的节点级反亲和；Server Group Awareness 排除主副本所属分组（separate server groups = rack/zone awareness）= F2 "第一类节点所属分组"约束。replica vBucket 经 rebalance 在合规节点间均匀分布。两层反亲和均字面命中。 |
| F3 | 命中（等同） | "On rebalance, vBuckets are redistributed evenly among currently available Data Service nodes"；节点增减/故障触发 "rebalance redistributes data ... among available nodes" | rebalance.html | rebalance 把 vBucket（含 replica）从分布不均的状态搬到均匀，使每节点趋同。专利 F3 以"分区个数 > 第三阈值的高负载节点 → < 第四阈值的低负载节点"描述同一目的；Couchbase 以"达到每节点相同数量"的等价目标实现高→低迁移，属不同表述、相同机制的等同。整数阈值具体取值未字面出现，按等同认定（机制相符，非整数外推）。 |

## 已检查文档清单
- Couchbase 官方 vBuckets 文档（active/replica 定义、均匀分布、不同节点放置）— https://docs.couchbase.com/server/current/learn/buckets-memory-and-storage/vbuckets.html
- Couchbase 官方 Server Group Awareness 文档（active 与 replica 分属不同 group、replica 必须在不同 server group）— https://docs.couchbase.com/server/current/learn/clusters-and-availability/groups.html
- Couchbase 官方 Rebalance 文档（节点增减/故障触发均匀重分布）— https://docs.couchbase.com/server/current/learn/clusters-and-availability/rebalance.html

## 最终判定
**第 2 档：全特征命中，含 ≥1 等同**

判定依据：F0/F1/F2 由 Couchbase 官方文档 verbatim 字面命中（active/replica vBucket 二元结构、vBucket 均匀分布、replica 与 active 跨节点 + 跨 server group 反亲和）；F3（高负载→低负载备分区迁移）以 rebalance "redistribute evenly / 每节点相同数量" 的等价机制认定为等同（专利用整数阈值描述高/低负载，Couchbase 用目标均匀态描述，机制相符）。无任何真反向证据；产品在 2017-12-01 后持续公开维护，时间窗满足。因含 1 项等同（F3），不落第 1 档（全字面），落第 2 档。

## 升级路径（第3-4档）
不适用（本候选为第 2 档）。若需把 F3 升至字面命中，可深抓 Couchbase rebalance 内部算法/源码（如 ns_server vbucket map 生成逻辑或 rebalance planner）核实是否以"分区计数超/欠阈值"显式触发迁移；若证实，则 F3 由等同升为字面，整体可升至第 1 档。

## 总结一句话
Couchbase Server 的 active/replica vBucket 二元结构、rebalance 均匀分布、跨节点 + Server Group Awareness 跨分组反亲和，与本专利 F0–F3 高度对应（F3 为等同），无反向证据，落第 2 档。
