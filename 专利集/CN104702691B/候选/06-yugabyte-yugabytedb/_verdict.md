# 06-yugabyte-yugabytedb verdict

## 候选基本信息
- 名称：YugabyteDB（tablet 副本 + zone-aware rebalance） / 组织：Yugabyte Inc / 类型：产品 / 初判F#：F0,F1,F2,F3 / 专利公开日：2017-12-01

## 检索粗筛（Phase 1 react 留痕）
- WebSearch 1：`YugabyteDB tablet replica placement zone load balancer` → 命中 cluster-balancing docs / auto-balancing blog / rack-aware placement，正向信号充分。
- WebSearch 2：`YugabyteDB cluster balancing tablet leader high low load move underloaded node` → 命中"load measured by tablet count""moves leaders/data to underloaded nodes"。
- WebSearch 3：`YugabyteDB placement policy replica different fault domain rack anti-affinity primary leader follower` → 命中"replica of each tablet in separate regions/racks""followers replicate, leader serves reads/writes"。
- 结论：3 条内即获 F0–F3 全部正向事实，未触发早剪枝（非 0 命中、证据均 ≥2021、架构层级一致：均为分布式数据库 分区-副本-放置-再均衡层）。

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F0 | 命中（等同） | "we designate one of the copies as the leader that facilitates all the writes and the standby copies as followers"；"Dotted boxes around replicas denote followers and solid ones are the leaders"（RF-3 → tablet 含 1 leader + 2 follower） | https://www.yugabyte.com/blog/auto-balancing-data-in-yugabytedb-a-distributed-sql-database/ | 多节点 + 多 tablet（=主分区），每 tablet ≥1 follower（=备）。leader 对外服务、follower 容错，与"主副本对外服务+备副本容错"语义对应。**但 leader 为 Raft 选举式动态产生，非专利静态指定的主副本 → 记等同（封顶第2档）。** |
| F1 | 命中（字面） | "YugabyteDB's cluster balancer balances the shards of a table and replicas of a shard so that they get uniformly distributed across nodes"；"each of the zones has an equal number of tablet leaders"（leader=主分区，均匀=任意两节点差→0，对应阈值优选1） | https://docs.yugabyte.com/stable/architecture/docdb-sharding/cluster-balancing/ ; https://www.yugabyte.com/blog/auto-balancing-data-in-yugabytedb-a-distributed-sql-database/ | 主分区（leader）在节点/zone 间 uniformly/equal 分布，对应 F1"任意两节点主分区差<阈值（优选1）"。 |
| F2 | 命中（字面） | "a typical replication factor of 3 (RF-3) placement might specify that there should be one replica of each tablet in three separate regions"；"YugabyteDB ensures each tablet (shard) has replicas in different racks, so losing an entire availability zone doesn't cause data loss"；"the load balancer respects this placement by not transferring any load to this new node"（datacenter1.rack1 约束已满时） | https://docs.yugabyte.com/stable/architecture/docdb-sharding/cluster-balancing/ ; https://www.yugabyte.com/blog/auto-balancing-data-in-yugabytedb-a-distributed-sql-database/ | 同一 tablet 的副本被强制放到不同 region/rack/zone（fault domain），即排除"主副本所在分组"的节点 = 专利"第二类节点"反亲和约束；且 placement 内 leader 均匀（"equal number of tablet leaders" per zone）= 备/副本按约束均匀。对应 F2 反亲和+按主分组约束均衡。 |
| F3 | 命中（字面） | "Currently, the total number of tablets and its replicas is taken to be a measure of the load on a node"；"The cluster balancer ... moves tablet data and leaders to evenly distribute data and query load"；"Now that node 4 has a tablet leader, it can actively take on load, thereby reducing the load on other nodes" | https://docs.yugabyte.com/stable/architecture/docdb-sharding/cluster-balancing/ ; https://www.yugabyte.com/blog/auto-balancing-data-in-yugabytedb-a-distributed-sql-database/ | 负载度量=节点上 tablet/副本"个数"（与专利 F3"以分区个数判定高/低负载"一致，非 CPU/流量）；自动把 tablet 数据/leader 从高负载节点移到低负载（新加/欠载）节点。对应 F3 高负载→低负载迁移。 |

## 已检查文档清单
- Cluster balancing（YB-Master 中的 cluster balancer：负载度量=tablet 个数；moves data/leaders 均衡；placement policy = 各 tablet 副本放不同 region；tablets_in_wrong_placement 指标） — https://docs.yugabyte.com/stable/architecture/docdb-sharding/cluster-balancing/
- Auto-Balancing Data in YugabyteDB 博客（datePublished 2021-06-29，dateModified 2024-10-16；load=tablet count、uniformly distributed、leader/follower 角色、placement 反亲和、移 tablet/leader 到新节点降载） — https://www.yugabyte.com/blog/auto-balancing-data-in-yugabytedb-a-distributed-sql-database/
- Rack-aware / multi-zone placement、handling rack failures（replica 跨 rack/zone 反亲和；RF-3 容忍一个 fault domain 故障） — https://docs.yugabyte.com/stable/explore/fault-tolerance/handling-rack-failures/

## 最终判定
**第 2 档：全特征命中，含 ≥1 等同（F0 主备语义为 Raft 选举式 leader/follower，对应但非字面静态主副本）**

五档：1=全字面；2=全命中含≥1等同；3=≥60%无反向；4=<60%；5=已排除（仅(a)真反向/(b)全<2017-12-01/(c)架构层级不同）。第5档硬门槛=针对该候选正向事实，"通用反推/未提及"不算。0命中≠已排除。

判定依据：F0–F3 四项均有公开 verbatim 正向证据，时间窗合规（文档/博客均 2021 年及之后，远晚于 2017-12-01）。F1/F2/F3 为字面命中（主分区 leader 均匀分布、副本跨 fault domain 反亲和、以 tablet 个数为负载度量做高→低负载迁移）；唯 F0 因 leader 由 Raft 动态选举（专利为静态指定主副本）记等同。按纪律"Raft 选举式 leader vs 专利静态主副本→主备语义对应即命中但记等同（封顶第2档）"，故落第2档而非第1档。未检索到反向证据（无"不支持/排除主备/排除反亲和"语句）。

## 升级路径（第3-4档）：不适用——本候选证据强于第3-4档，方向是确认而非补强；如需进一步固化第1↔2档边界，可核查 yb-admin `modify_placement_info` + per-block `min replica count` 是否以"任意两节点副本数差"形式做硬均衡（坐实 F2 阈值语义），以及 Raft leader hint 机制是否使 leader 放置等价于静态指定（若是 F0 可向字面靠拢）。

## 总结一句话：YugabyteDB 以 tablet=分区、leader/follower=主/备、placement 跨 fault domain 反亲和、cluster balancer 以"tablet 个数"为负载度量在节点/zone 间均匀分布并把数据/leader 从高负载移到欠载节点，F0–F3 全命中且证据 2021 起合规，仅 F0 因 Raft 选举式 leader 记等同，落第2档。
