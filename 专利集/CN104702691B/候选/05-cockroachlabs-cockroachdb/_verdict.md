# 05-cockroachlabs-cockroachdb verdict

## 候选基本信息
- 名称：CockroachDB（range 副本 + locality rebalancing） / 组织：Cockroach Labs / 类型：产品 / 初判F#：F0,F1,F2,F3 / 专利公开日：2017-12-01

## 检索粗筛
Phase 1 react（串行 WebSearch ×3，均强信号，无早剪枝）：
1. `CockroachDB replica placement locality constraints rebalancing` → 命中 Replication Layer 文档、tech-notes/rebalancing.md、store_rebalancer.go、RFC 等；确认 range 多副本 + locality 约束 + 自动 rebalance。
2. `CockroachDB replication zone diversity anti-affinity replica placement same locality` → 确认副本按 locality diversity 分散（"one replica per AZ"），属反亲和。
3. `CockroachDB rebalance replicas from overloaded store to underutilized store load balancing` → 确认 StoreRebalancer 把 lease/replica 从 overloaded store 迁到低负载 store。

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F0 | 命中（等同） | "Cockroach maintains multiple replicas of each range of data for fault tolerance. It also maintains a single leaseholder for each range to optimize the performance of reads"；"A single node in the Raft group acts as the leaseholder, which is the only node that can serve reads or propose writes" | https://github.com/cockroachdb/cockroach/blob/master/docs/tech-notes/rebalancing.md ; https://www.cockroachlabs.com/docs/stable/architecture/replication-layer | range=分区；多副本/range；leaseholder=唯一对外服务读写=主副本，其余副本=备副本（容错）。主/备二元结构成立（等同：术语不同、语义相同） |
| F1 | 命中（等同） | "Number of ranges on each store" 为放置决策考量；"We then only have to do range count comparisons within these 'comparable' classes of stores."；副本 "rebalanced automatically across the cluster based on a combination of: 1. Replica count." | https://github.com/cockroachdb/cockroach/blob/master/docs/tech-notes/rebalancing.md ; https://www.cockroachlabs.com/docs/stable/architecture/replication-layer | 以 range（含 leaseholder=主）数在各 store 间均衡=主分区按节点均匀；阈值化均衡≈"差<第一阈值"（等同；未给整数=1 的字面值） |
| F2 | 命中（等同） | "Diversity of localities. If we put all of the replicas for a range in just one or two localities, then a single locality (datacenter, rack, region, etc) failure will cause data unavailability / loss. We should try to spread replicas as widely as possible"；"replacing s3 or s4 with s2 would hurt the range's diversity, which we never choose to do" | https://github.com/cockroachdb/cockroach/blob/master/docs/tech-notes/rebalancing.md | locality diversity = 同一 range 的副本尽量分散到不同 locality（datacenter/rack/region=分组），从不放置在会降低 diversity（即与已有副本同 locality）的 store ⇒ 备副本反亲和（排除主副本所在节点/分组），与 F2"第二类节点"语义高度等同 |
| F3 | 命中（部分字面+等同） | "Start runs an infinite loop ... which regularly checks whether the store is overloaded along any important dimension (e.g. range count, QPS, disk usage), and if so attempts to correct that by moving leases or replicas elsewhere."；"This store exceeds the max threshold, we should attempt to find rebalance targets."；"We only bother rebalancing stores that are fielding more than the cluster-level overfull threshold of load." | https://github.com/cockroachdb/cockroach/blob/master/pkg/kv/kvserver/store_rebalancer.go ; https://github.com/cockroachdb/cockroach/blob/master/docs/tech-notes/rebalancing.md | 高负载 store（超 overfull 阈值）的副本迁到低负载 store。当 overload 维度取 "range count" 时即"分区数>阈值→移到分区数<阈值节点"=字面命中；取 QPS/CPU 时为等同实现 |

## 已检查文档清单
- CockroachDB Replication Layer（leaseholder 服务读写 / 副本随节点变化再均衡 / 按 replica count+负载自动 rebalance / 受 placement constraint 与 locality survivability 约束） — https://www.cockroachlabs.com/docs/stable/architecture/replication-layer
- cockroach tech-notes/rebalancing.md（range count 均衡 / diversity-of-localities 反亲和 / StoreRebalancer 处理 overloaded store / leaseholder=主） — https://github.com/cockroachdb/cockroach/blob/master/docs/tech-notes/rebalancing.md
- store_rebalancer.go 源码注释（infinite loop 检测 store 是否在 range count/QPS/disk 维度 overloaded，超阈值则把 leases/replicas 迁走） — https://github.com/cockroachdb/cockroach/blob/master/pkg/kv/kvserver/store_rebalancer.go

## 最终判定
**第 2 档：全部命中（含等同）**

五档：1=全字面；2=全命中含≥1等同；3=≥60%无反向；4=<60%；5=已排除（仅(a)真反向/(b)全<2017-12-01/(c)架构层级不同）。第5档硬门槛=针对该候选正向事实，"通用反推/未提及"不算。0命中≠已排除。
判定依据：F0–F3 四特征均有 post-2017-12-01 公开材料支撑（StoreRebalancer 始于 v2.1/2018；stable+master 文档为现行版本），无任一反向证据。F0（leaseholder=主、余=备）、F2（locality diversity=备副本排除同 locality/分组的反亲和）、F1（按 range count 均衡）为术语不同语义相同的等同；F3 在 "range count" 维度字面命中、QPS/CPU 维度等同。因含多处等同（非全字面），落第 2 档而非第 1 档。

## 升级路径（第3-4档）：不适用（已达第 2 档）。若欲向第 1 档（全字面）逼近，需找到 CockroachDB 官方以"分区/副本个数差<整数阈值（如 1）"明文表述 F1/F3、且 F2 排除集明文等价于"主副本所在节点或其分组"的整数化表达；但其用 diversity score+负载阈值实现，预计仍属等同层面。

## 总结一句话：CockroachDB 的 range 多副本（leaseholder=主、余为备）+ locality diversity 反亲和 + StoreRebalancer 高负载→低负载副本迁移，四特征均以等同（F3 含字面）命中且无反向证据，落第 2 档。
