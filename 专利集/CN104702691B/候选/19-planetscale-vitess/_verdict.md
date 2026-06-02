# 19-planetscale-vitess verdict

## 候选基本信息
- 名称：Vitess（sharding + MySQL 副本 + resharding） / 组织：PlanetScale / 类型：产品 / 初判F#：F0,F1,F3 / 专利公开日：2017-12-01

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F0 | 命中（字面） | "In a typical Vitess setup, each shard has a single primary being replicated to two other MySQL instances. This replication allows for better high-availability support…"；"A shard typically contains one MySQL primary and potentially many MySQL replicas." | https://vitess.io/docs/15.0/user-guides/configuration-advanced/resharding/ ; https://vitess.io/docs/22.0/concepts/shard/ | 多节点+多 shard（主分区），每 shard 一个 primary tablet（主副本对外服务）+ ≥1 replica/rdonly tablet（备副本容错），直接对应 F0 的主/备二元结构。 |
| F1 | 部分命中（非系统自动按节点均衡） | resharding："the number of shards is changed on a live cluster … splitting one or more shards into smaller pieces, or merging neighboring shards into bigger pieces … the data in the source shards is copied into the destination shards" | https://vitess.io/docs/21.0/reference/features/sharding/ ; https://vitess.io/docs/15.0/user-guides/configuration-advanced/resharding/ | shard（=主分区）确实分布在多个 MySQL 实例/节点上，方向沾边；但 Vitess 本身不内建"按各节点主分区计数做均匀分配并保证任意两节点差<阈值"的算法，shard/tablet 到物理节点的放置依赖部署层（K8s scheduler / 拓扑）。F1 的"系统自动均匀 + 整数阈值"核心限定未命中，记部分命中。 |
| F2 | 部分命中（等同性弱，依赖部署而非系统自动按分区均衡） | "A master and its semi-sync eligible replica can be ensured to be located in different cells to achieve cross-cell durability."；cross_cell durability policy "only allows Primary and Replica type servers from a different cell than the current primary to acknowledge semi sync." | https://github.com/vitessio/vitess/issues/3355 ; https://vitess.io/docs/archive/16.0/user-guides/configuration-basic/durability_policy/ | Vitess 支持 primary 与 replica 跨 cell（=可用区/机架）放置，达到"备副本不与主副本同失败域"的反亲和效果，方向与 F2 一致；但这是 durability policy / 部署拓扑配置（cell 由运维划分），系统并不"以主分区为单位、令第二类节点上备分区个数两两之差<阈值"地自动均衡。F2 的"按主分区均衡 + 整数阈值"核心限定未命中，仅命中"反亲和"方向，记部分命中。 |
| F3 | 未命中（机制/对象不同，非反向证据） | 再均衡=resharding（改变分片数、按 key range 重分数据，见上）；查询负载用 VTGate Tablet Balancer，但"The tablet balancer does not move or migrate tablets between physical nodes. It operates exclusively at the query routing layer."；其目标为"maintain an even distribution of query load to each tablet" | https://vitess.io/docs/15.0/user-guides/configuration-advanced/resharding/ ; https://vitess.io/docs/23.0/reference/features/tablet-balancer/ | F3 要求"在固定节点集合内把备分区从高负载节点（分区数>阈值）迁到低负载节点（分区数<阈值）"。Vitess 两类机制都不对应：(a) resharding 是改变分片数、按 key range 重分**数据**，对象与触发条件均不同；(b) tablet balancer 只做查询流量路由、明确不迁移 tablet。无"按备分区计数在固定节点间迁移备副本"的内建机制。属正向事实不命中（机制/对象不同），不硬凑等同；这是机制差异而非"未提及"。 |

## 已检查文档清单
- Vitess Resharding（shard 结构：每 shard 1 primary + 2 replica；resharding 按 key range 重分数据，读先于写切流） — https://vitess.io/docs/15.0/user-guides/configuration-advanced/resharding/
- Vitess Sharding 参考（resharding 改变 live cluster 上 shard 数，split/merge，复制源 shard 数据到目标 shard） — https://vitess.io/docs/21.0/reference/features/sharding/
- Vitess Shard 概念（"A shard typically contains one MySQL primary and potentially many MySQL replicas"） — https://vitess.io/docs/22.0/concepts/shard/
- VTGate Tablet Balancer（明确：只做查询路由负载均衡，"does not move or migrate tablets between physical nodes"） — https://vitess.io/docs/23.0/reference/features/tablet-balancer/
- Vitess Durability Policy（cross_cell：primary 与 replica 跨 cell 半同步，备副本跨失败域） — https://vitess.io/docs/archive/16.0/user-guides/configuration-basic/durability_policy/
- Vitess Issue #3355（cell/region 拓扑配置，master 与 semi-sync replica 不同 cell） — https://github.com/vitessio/vitess/issues/3355
- PlanetScale 文档/博客（每 shard primary+replica；PlanetScale 自动在 VTGate 间分发负载——查询层 LB，非分区/副本放置） — https://planetscale.com/docs/vitess/sharding

## 最终判定
**第 4 档：部分命中（<60%，核心再均衡机制 F3 未命中）**

五档:1=全字面;2=全命中含≥1等同;3=≥60%无反向;4=<60%;5=已排除(仅(a)真反向/(b)全<2017-12-01/(c)架构层级不同)。第5档硬门槛=针对该候选正向事实,"通用反推/未提及"不算。0命中≠已排除。

判定依据：F0 字面命中（shard = primary tablet + replica/rdonly tablet 的主/备二元结构，每 shard ≥1 备副本）。F1、F2 仅方向沾边、属部分命中——shard 与 replica 确分布在多节点、且支持跨 cell 反亲和，但均依赖部署层（K8s/拓扑/durability policy），Vitess 不内建"按主/备分区计数令任意两节点差<整数阈值"的自动均衡算法。F3——本专利权 1 的核心"减少迁移的两级再均衡"——明确未命中：Vitess 的 resharding 是按 key range 改变分片数重分**数据**（对象/触发都不同），tablet balancer 只做查询路由且明文不迁移 tablet，二者都不是"在固定节点集合内按备分区负载（分区计数阈值）迁移备副本"。4 项中仅 1 项字面命中、2 项弱部分、1 项核心未命中，故落第 4 档（远低于 60% 且核心特征缺失）。

## 升级路径（第3-4档）：
若能找到 (a) Vitess/PlanetScale 控制面（vtctld / VTOrc / PlanetScale 编排层）存在"按各节点 shard 或 replica 计数自动均匀放置并保证差<阈值"的内建调度（命中 F1）、且 (b) 存在"将备 tablet 从高分区计数节点迁到低分区计数节点"的内建负载迁移机制（命中 F3，对象=备副本、触发=分区计数阈值，而非 resharding 改分片数），可升至第 2-3 档。当前公开文档（截至检索）未见此类机制；亦未检索到 PlanetScale/Vitess 在 2017-12-01 后自有同主题专利。

## 总结一句话：
Vitess 的 shard=primary+replica 二元结构字面命中 F0，shard/副本多节点分布与跨 cell 反亲和仅弱沾边 F1/F2 且依赖部署层；其"再均衡"是按 key range 改分片数的 resharding 与纯查询路由的 tablet balancer，均非专利 F3"在固定节点集合内按备分区负载迁移备副本"的机制，故落第 4 档。
