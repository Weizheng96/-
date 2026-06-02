# 01-tech-elasticsearch verdict
## 候选基本信息
- 名称：Elasticsearch（primary/replica shard + allocation awareness）
- 组织：Elastic NV（NYSE: ESTC）
- 类型：技术
- 初判命中 F#：F0,F1,F2,F3
- 专利公开（授权）日：2017-12-01
## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F0 | 字面命中 | "The SameShardAllocationDecider is an allocation decider that prevents multiple instances of the same shard to be allocated on the same node. The primary node will not assign a primary shard to the same node as its replica" | https://artifacts.elastic.co/javadoc/org/elasticsearch/elasticsearch/7.13.3/org/elasticsearch/cluster/routing/allocation/decider/SameShardAllocationDecider.html | ES 数据按 index 切 shard，每个 shard 含 1 primary + N replica（primary 对外服务、replica 容错），完全对应 F0 的"多节点+多主分区+每主分区≥1备分区"二元结构 |
| F1 | 字面命中 | "A cluster is *balanced* when it has an equal number of shards on each node" ; "Defines the weight factor for the total number of shards allocated to each node…Raising this value increases the tendency of Elasticsearch to equalize the total number of shards across nodes" | https://www.elastic.co/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings | ES 自动 rebalance 把分片数均衡到各节点（任意两节点分片数趋同），对应 F1"任意两节点主分区数差<阈值（优选1）"。balance threshold 默认 1.0f |
| F2 | 等同命中 | "Elasticsearch won't put a replica shard on the same node as the primary"（同节点反亲和）；"ensuring (if possible) that no two copies of the same shard are in the same rack"（同分组反亲和）；"specify the attribute values that should exist with the cluster.routing.allocation.awareness.force.* settings"（forced awareness 跨 zone/rack 分散） | https://www.elastic.co/docs/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/shard-allocation-awareness | F2 核心"备副本排除主副本所在节点本身(第一类节点)/或其所属分组(rack/zone)"= ES SameShardAllocationDecider（排除同节点）+ allocation/forced awareness（排除同 rack/zone 分组）。备副本在第二类节点间均匀=ES 全局 equal-shard-count 均衡在 awareness 约束下达成，属机制等同（ES 按节点总分片数均衡而非"逐主分区"显式均衡），故判等同命中 |
| F3 | 字面命中 | "Elasticsearch runs an automatic rebalancing process which moves shards between the nodes" ; "The minimum improvement in weight which triggers a rebalancing shard movement. Defaults to 1.0f" | https://www.elastic.co/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings | ES rebalance 把分片从分片数偏多（高负载）节点搬到分片数偏少（低负载）节点，由 weight-improvement 阈值（默认 1.0f）触发，对应 F3"高负载节点(>第三阈值)→低负载节点(<第四阈值)"的二次均衡迁移。rebalance 遵守 forced awareness 约束（即在第二类节点范围内迁移） |
## 已检查文档清单
- Elastic 官方 Shard allocation awareness 文档（allocation/forced awareness、rack/zone 反亲和、no two copies in same rack）— https://www.elastic.co/docs/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/shard-allocation-awareness
- Elastic 官方 Cluster-level shard allocation and routing settings（balanced=equal shards per node、shard balance weight factor、rebalance threshold 1.0f）— https://www.elastic.co/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings
- Elastic 官方 SameShardAllocationDecider Javadoc（primary 不与其 replica 同节点；两 replica 不同节点）— https://artifacts.elastic.co/javadoc/org/elasticsearch/elasticsearch/7.13.3/org/elasticsearch/cluster/routing/allocation/decider/SameShardAllocationDecider.html
- 搜索佐证：BigData Boutique / Mincong Huang allocation deciders / AWS Open Source Blog — 一致描述 ES primary+replica、forced awareness 反亲和、自动 rebalance 均衡分片
## 最终判定
**第 2 档：确认侵权（中）— 全部 F# 命中，含 ≥1 等同**
五档定义：第1档=确认侵权(高)F全字面命中；第2档=确认侵权(中)全命中含≥1等同；第3档=公开资料不足(强候选)≥60%F命中且剩余无反向；第4档=公开资料不足(弱候选)<60%F命中；第5档=已排除(仅当(a)≥1条F有真反向证据 或(b)全部证据<2017-12-01 或(c)架构层级不同)。
第5档硬门槛——必须是针对该候选产品的正向事实(反向证据/自有文档或自有专利写明用另一套手段)，"行业通用机制反推/同类一般这样/公开资料未提及"一律不算反向(那是公开资料不足)。同抽象层但仅缺某F#正向证据又无针对它的反向事实→第4档，不得第5档。**0命中≠已排除**。
判定依据（1-3句，基于F#命中分布）：ES 官方文档对 F0（primary+replica shard 二元结构）、F1（cluster balanced = 各节点分片数相等，weight factor 均衡总分片数）、F3（自动 rebalance 由 weight 阈值 1.0f 触发把分片从多搬到少）均为字面命中；F2（备副本反亲和——SameShardAllocationDecider 排除同节点 + allocation/forced awareness 排除同 rack/zone 分组）机制完全对应，仅"逐主分区显式均匀"由 ES 全局 equal-shard-count 均衡等价达成，判等同命中。无任何 F# 出现反向证据，全部证据均来自当前持续维护并发行的官方文档（产品在 2017-12-01 后仍在持续开发与广泛使用，时间窗合规）。故全部 4 个 F# 命中且含 1 个等同 → 落第 2 档。
## 升级路径（仅第3-4档填）
- （不适用，第 2 档）
## 总结一句话
Elasticsearch 的 primary/replica 分片 + SameShardAllocationDecider/allocation forced awareness 反亲和 + 自动 rebalance（equal-shard-count、阈值触发）逐条覆盖 F0–F3，仅 F2 逐主分区均匀为机制等同，落第 2 档（确认侵权-中）。
