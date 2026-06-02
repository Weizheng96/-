# 10-tech-redis-cluster verdict
## 候选基本信息
- 名称：Redis Cluster（hash slot + replica + reshard） / 组织：Redis Ltd / 类型：技术 / 初判F#：F0,F1,F2,F3 / 专利公开日：2017-12-01
## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F0 | 命中(字面) | "a single hash slot will be served by a single node (however the serving node can have one or more replicas that will replace it in the case of net splits or failures…)" + "Eventually every master will be backed by at least one replica." + "A replica is promoted to the role of master when needed in order to continue to operate when a failure occurs." | https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/ | 多节点+多主分区(slot),master对外服务,replica容错,每master最终≥1 replica。对应"主副本对外服务+备副本容错,每主≥1备"。 |
| F1 | 命中(字面) | "Each master node in a cluster handles a subset of the 16384 hash slots." + "Automatic rebalancing distributes slots evenly across all master nodes" + "The hash slots are now balanced out evenly across the … active Redis nodes"（实测每节点5461/5462 slot,差≤1） | https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/ ; https://severalnines.com/blog/hash-slot-resharding-and-rebalancing-redis-cluster/ | slot(主分区)在master间均匀,实测差值≤1,对应"任意两节点主分区差<第一阈值(优选1)"。 |
| F2 | 命中(等同) | "Redis CLI will propose a configuration and try to optimize replicas allocation for anti-affinity." + "the cluster still ensures that primary and replica shards are placed on distinct nodes" + 启用rack-zone awareness时"distributes primary and replica shards across zones" | https://redis.io/docs/latest/operate/rs/clusters/configure/rack-zone-awareness/ ; https://redis.io/docs/latest/operate/kubernetes/reference/yaml/rack-awareness/ | replica置于与master不同节点(=排除第一类节点),rack-zone awareness按分组(rack/zone)排除(=第一类节点所属分组)。反亲和+不同节点核心特征命中。等同:Redis按"每master配replica"组织反亲和,非按"主分区分组单位对备副本做均衡迁移(差<阈值)"的字面表述,目标一致。 |
| F3 | 部分命中(等同,对象差异) | "Rebalance the cluster so that a given set of hash slots are moved between nodes." + "redis-cli --cluster rebalance … --weight"(按权重把slot从多者移到少者) — 但迁移对象为master的slot,非备分区 | https://severalnines.com/blog/hash-slot-resharding-and-rebalancing-redis-cluster/ ; https://oneuptime.com/blog/post/2026-01-25-redis-cluster-slot-rebalancing/view | rebalance把slot从高占用节点搬到低占用节点(对应"高负载>阈值→低负载<阈值"迁移思想),但Redis搬的是**主分区(master slot)**,而专利F3明确搬的是**备分区在第二类节点间二次均衡**。Redis中replica与master 1:1绑定,无"按负载在节点间自动迁移备副本"的内建行为,且rebalance须人工运行CLI(非自动)。落"等同+对象差异",非字面。 |
## 已检查文档清单
- Redis cluster specification（master服务slot/replica容错/failover/每master≥1 replica/slot均匀） — https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/
- Scale with Redis Cluster（16384 slot在master均分,reshard移slot） — https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/
- Hash Slot Resharding and Rebalancing（rebalance实测每节点5461/5462,均匀,迁移对象为slot） — https://severalnines.com/blog/hash-slot-resharding-and-rebalancing-redis-cluster/
- How to Rebalance Redis Cluster Slots（rebalance非自动须人工CLI;无备副本迁移） — https://oneuptime.com/blog/post/2026-01-25-redis-cluster-slot-rebalancing/view
- Rack-zone awareness in Redis Software（primary/replica跨zone分布=分组反亲和） — https://redis.io/docs/latest/operate/rs/clusters/configure/rack-zone-awareness/
- Control node selection / rack-awareness（replica与master置于不同节点） — https://redis.io/docs/latest/operate/kubernetes/reference/yaml/rack-awareness/
## 最终判定
**第 3 档：高度相关，多数特征命中（含等同），无反向证据，F3 存对象差异**

五档:1=全字面;2=全命中含≥1等同;3=≥60%无反向;4=<60%;5=已排除(仅(a)真反向/(b)全<2017-12-01/(c)架构层级不同)。第5档硬门槛=针对该候选正向事实,"通用反推/未提及"不算。0命中≠已排除。

判定依据：F0、F1 字面命中（master/replica 主备结构、slot 在 master 间均匀，实测差≤1）。F2 以"redis-cli anti-affinity 优化 + rack-zone awareness 跨分组分布"等同命中专利"备副本排除主所在节点/分组"。F3 仅部分等同：Redis rebalance 把高占用节点 slot 搬到低占用节点（迁移思想一致），但迁移对象是主分区 slot 而非专利所限定的"备分区在第二类节点间二次均衡"，且 replica 与 master 1:1 绑定、无按负载自动迁移备副本的内建机制。3/4 特征命中（含 ≥1 等同）、无任何反向证据，落第 3 档。
## 升级路径（第3-4档）：核证 Redis 是否存在"按负载在节点间迁移 replica/备分区"的内建或官方工具能力（若有→F3 字面化→可升第2档）；核证 redis-cli create 的 anti-affinity 实现是否含"按主分区分组单位对备副本做均匀(差<阈值)"语义（若是→F2 更接近字面）；抓 Redis Enterprise / Valkey 文档看 replica 放置是否含"任意两节点备副本数差<阈值"的均衡约束。
## 总结一句话：Redis Cluster 在主备结构(F0)、主分区slot均匀(F1)、副本反亲和+跨分组放置(F2)上命中本专利，F3仅以"高低占用迁移"思想等同（迁移对象为主slot非备分区、且须人工CLI），无反向证据，落第3档。
