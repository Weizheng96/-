# 08-mongodb-sharded-cluster verdict

## 候选基本信息
- 名称：MongoDB Sharded Cluster（chunk balancer + zone sharding + replica set） / 组织：MongoDB Inc（NASDAQ: MDB） / 类型：产品 / 初判F#：F0,F1,F2,F3 / 专利公开日：2017-12-01

## 检索粗筛（Phase 1 react 留痕）
- 起步：`MongoDB sharded cluster balancer chunk distribution replica set` → 命中官方 Manual（balancer、sharding），强信号，材料持续维护（2026 仍在线），无早剪枝触发。
- 缩 1：`MongoDB replica set member distribution different nodes data center awareness secondary placement` → 命中 Replica Set Deployment Architectures，得到"成员跨主机/数据中心分布"反亲和素材。
- 缩 2：`MongoDB zone sharding chunk balancing placement constraint shard ranges` → 命中 Zones 文档，确认 zone 是"chunk→shard"放置约束（主数据放置层），非备副本反亲和。
- 早剪枝判定：未触发（材料非 0 命中、主题相关、均为持续维护的现行官方文档，远晚于 2017-12-01）。

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F0 | 字面命中 | "Each shard must be deployed as a replica set."；"A replica set in MongoDB is a group of mongod processes that provide redundancy and high availability."；"The primary receives all write operations."；"Secondaries replicate operations from the primary to maintain an identical data set." | https://www.mongodb.com/docs/manual/sharding/ ; https://www.mongodb.com/docs/manual/core/replica-set-members/ | 多节点集群；数据切 chunk（主分区数据），每 shard=Replica Set，primary 对外写服务+secondary 容错=主/备副本二元结构。primary 选举产生 vs 专利静态主副本→主备语义对应，记等同（依协议"主备语义对应记等同"） |
| F1 | 等同命中 | "the balancer migrates chunks from shards with more chunks to shards with a fewer number of chunks, until there is an even distribution of chunks for the collection across the shards."；"attempts to automatically migrate data between shards and reach an even amount of data per shard" | https://www.mongodb.com/docs/manual/core/sharding-balancer-administration/ | Balancer 把 chunk（主分区数据）在 shard 间均衡到"每 shard 数据量相等"=主分区在节点间均匀分布。判据是 chunk 数/数据量差而非整数阈值1，属"差<阈值"目标的等同实现（中间变量/阈值取值开放枚举，记等同） |
| F2 | 部分命中（架构层级部分对应：反亲和意图等同，"按主分区分组计数均衡"机制不对应） | （反亲和意图）"To protect your data in case of a data center failure, keep at least one member in an alternate data center."；（成员分布）"Distributing replica set members across geographically distinct data centers adds redundancy"；（zone=放置约束）"If the chunk range falls into a zone, the balancer migrates the chunk into a shard inside that zone." | https://www.mongodb.com/docs/manual/core/replica-set-architectures/ ; https://www.mongodb.com/docs/manual/core/zone-sharding/ | 见下"F2 架构层级分析"。备副本不与主同主机/数据中心=反亲和意图对应；但 MongoDB 备副本是 Replica Set 成员（持有整 shard 全量数据，非按主分区为单位的 per-partition 备分区放置），且成员落主机的分布是运维静态部署决定、非"在第二类节点间按个数自动均衡"的算法。zone sharding 约束的是 chunk→shard（主数据放置层），非备副本反亲和。机制不对应 |
| F3 | 等同命中（限于主分区/chunk 层；备副本层无独立 F3 机制） | "the balancer migrates chunks from shards with more chunks to shards with a fewer number of chunks"；"the difference in the number of chunks between the shards reaches the migration thresholds ... and triggers migration"；"A collection is considered balanced if the difference in data between shards ... is less than three times the configured range size" | https://www.mongodb.com/docs/manual/core/sharding-balancer-administration/ | 高 chunk 数 shard→低 chunk 数 shard 迁移、用 migration threshold 界定高/低负载（按 chunk 个数判定，与专利 F3"按分区个数判高低负载"一致）=F3 等同。但此迁移作用于 chunk（=主分区数据），专利 F3 是"在第二类节点范围内迁移备分区做二次均衡"；MongoDB 备副本不单独再均衡（secondary 全量跟随 primary），故 F3 仅在主/chunk 层对应，备副本层无对应机制 |

## F2 架构层级分析（核心争点）
专利 F2 = "每个主分区的备分区放在第二类节点（排除主副本所在节点/分组=反亲和），且这些备分区在第二类节点间按个数均匀"。这是**按主分区为单位、对备分区做反亲和放置 + 计数均衡**的算法。

MongoDB 是**两层**结构：
- chunk 层（shard 间）：Balancer 把 chunk 均衡到各 shard（=F1/F3，主数据层）；zone sharding 约束 chunk→哪个 shard（仍是主数据放置约束，非备副本反亲和）。
- 副本层（Replica Set 内）：每个 shard 的 secondary 持有该 shard **全量数据的副本**（不是"某个主分区对应的备分区"），成员落到不同主机/数据中心是**运维静态部署**推荐做法，不是产品自动执行的"按第二类节点计数均衡"算法。

因此：F2 的"反亲和意图"在 MongoDB 中以"成员跨主机/数据中心部署"等同体现；但"按主分区为单位放备分区 + 在第二类节点间自动计数均衡"这一**具体算法机制在 MongoDB 中没有对应物**——副本是 Replica Set 成员级全量复制，由运维决定主机分布，非系统按分区粒度的自动反亲和均衡。属架构层级部分对应，记 F2 部分命中。

## 已检查文档清单
- Sharding（sharded cluster 组成：shard 必为 replica set、config server、mongos） — https://www.mongodb.com/docs/manual/sharding/
- Sharded Cluster Balancer（balancer 在 config server primary 运行；chunk 从多→少迁移达均衡；migration threshold；三倍 range size 平衡判据） — https://www.mongodb.com/docs/manual/core/sharding-balancer-administration/
- Replica Set Members（replica set 定义；primary 收所有写；secondary 复制保持相同数据集） — https://www.mongodb.com/docs/manual/core/replica-set-members/
- Replica Set Deployment Architectures（成员跨主机/数据中心分布以容错；丢失一个数据中心仍可多数派/留有副本） — https://www.mongodb.com/docs/manual/core/replica-set-architectures/
- Zones / Zone Sharding（zone 把 chunk 约束到关联 shard；chunk 落 zone 则 balancer 迁入该 zone 内 shard） — https://www.mongodb.com/docs/manual/core/zone-sharding/

## 最终判定
**第 2 档：全部 F# 命中（含等同）**

五档:1=全字面;2=全命中含≥1等同;3=≥60%无反向;4=<60%;5=已排除(仅(a)真反向/(b)全<2017-12-01/(c)架构层级不同)。第5档硬门槛=针对该候选正向事实,"通用反推/未提及"不算。0命中≠已排除。

判定依据：F0 字面命中（shard=replica set，主/备副本二元结构）；F1/F3 等同命中（Balancer 把 chunk 在 shard 间从多到少均衡、用 migration threshold 界定高/低负载并迁移）；F2 部分命中——反亲和意图等同（成员跨主机/数据中心部署），但"按主分区为单位的备分区反亲和+计数均衡"算法在 MongoDB 中无对应物。全部 4 个 F# 均有正向命中、无任何反向证据，但 F2/F3 在备副本层非字面对应，故落第 2 档而非第 1 档。

## 升级路径（第3-4档）
不适用（已在第 2 档，高于 3-4 档）。若反向收紧到第 1 档需找到 MongoDB **自动按分区粒度对备副本反亲和放置 + 在排除主节点的节点集合间按个数均衡**的机制证据（现文档显示副本为 Replica Set 成员级全量复制 + 运维静态主机分布，不满足，无法升至第 1 档）。

## 总结一句话
MongoDB Sharded Cluster：shard=Replica Set（主/备副本，F0 字面），Balancer 把 chunk 在 shard 间从多到少均衡迁移（F1/F3 等同），备副本反亲和仅以"成员跨主机部署"意图等同体现而无按分区计数均衡的对应算法（F2 部分），落第 2 档。

---
*免责声明：本报告仅为侵权线索与证据链梳理，不构成"已构成侵权"的法律结论。最终判定需由专业法律/技术鉴定机构结合权利要求逐项比对完成。*
