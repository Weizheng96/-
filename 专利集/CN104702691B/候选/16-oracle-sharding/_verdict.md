# 16-oracle-sharding verdict

## 候选基本信息
- 名称：Oracle Globally Distributed Database / Oracle Sharding（shard + 复制 + shard director；含 23ai Raft Replication）
- 组织：Oracle
- 类型：产品
- 初判 F#：F0,F1,F2,F3
- 专利公开日：2017-12-01

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F0 | 命中（字面/等同） | "A replication unit (RU) is a set of chunks ... each RU having three replicas placed on different shards ... some of these replicas being leaders and some being followers"（搜索摘要）；"All DMLs ... are executed in the leader first, and then are replicated to its followers" | docs.oracle.com/.../23/shard/enabling-raft-replication.html ；blogs.oracle.com Raft 摘要 | 多 shard（节点）+ 多 chunk-set（≈主分区单元），每单元含 1 leader（主副本对外服务）+ 多 follower（备副本容错）。Raft 模式下结构与 F0 等同；Data Guard 模式为整库 standby（见判定依据）。 |
| F1 | 命中（等同） | "Raft replication ... handle chunk assignment, chunk movement, workload distribution, and balancing"；"maintain an equal distribution of the load and activity across all shards"；默认"each shard ... a leader for two RUs"（leader 在 shard 间均衡） | 19c arch；23 raft-replication.html；blogs.oracle 摘要 | 主副本（leader）/chunk 在各 shard 上均匀分布，对应"任意两节点主分区数差 < 阈值"的均匀目标。机制不同（chunk/RU 计数均衡 vs 节点分区计数均衡）但效果等同。 |
| F2 | 命中（等同） | "each RU having three replicas placed on different shards"；"Each RU is a bundle of table chunks and their replicas, spread across multiple shards"；"Every shard houses one chunk set, and for each chunk set, replicas exist across multiple shards"；"a follower for four other RUs by default"（follower 在 shard 间均衡） | blogs.oracle 摘要；infolob.com（2025-04-10） | 备副本（follower/replica）强制放在**不同 shard**（≠ leader 所在 shard）= 反亲和；且 follower 在各 shard 间均衡分布。patent 的"节点/分组"与 Oracle 的"shard"为同层反亲和单位的等同实现。详见判定依据中的抽象层讨论。 |
| F3 | 命中（等同） | "the unit of data migration between shards is the chunk"；"move chunks from more active servers to less active servers"；"When a shard is added to or removed ... multiple chunks are migrated to maintain a balanced distribution of chunks and workload across shards" | 19c arch；Oracle Sharding lifecycle 文档（搜索摘要） | 扩缩容/负载倾斜时把 chunk（含其副本所属 RU）从高活动 shard 迁到低活动 shard，对应"高负载节点备分区→低负载节点"的二次均衡。Raft 模式下 follower 随 RU 一并再均衡。 |

## 已检查文档清单
- Oracle Sharding Architecture and Concepts（19c，chunk=shard 间迁移单位、Data Guard standby shard 放置）— https://docs.oracle.com/en/database/oracle/oracle-database/19/shard/architecture-and-concepts1.html
- Raft Replication Configuration and Management（23ai，RU 自动分布+chunk 移动+扩缩容均衡）— https://docs.oracle.com/en/database/oracle/oracle-database/23/shard/raft-replication.html
- Enabling Raft Replication（23ai，RU 定义、≥3 shard）— https://docs.oracle.com/en/database/oracle/oracle-database/23/shard/enabling-raft-replication.html
- INFOLOB: Oracle 23ai Raft Replication（第三方，RU 副本跨多 shard、leader/follower 均衡，发布 2025-04-10）— https://www.infolob.com/oracle-23ais-built-in-fault-tolerance-raft-replication-configuration-and-management/
- Sharded Database Lifecycle Management / chunk move 与 resharding（搜索摘要）— https://docs.oracle.com/en/database/oracle/oracle-database/18/shard/sharding-lifecycle-management.html

## 最终判定

**第 2 档：全特征命中（含等同）**

五档：1=全字面；2=全命中含≥1等同；3=≥60%无反向；4=<60%；5=已排除。

判定依据：
1. **抽象层关键问题（F2 是"分区级备副本放置"还是"整库 standby"）**——分两条产品路径：
   - **Data Guard 模式（23ai 之前的默认复制）**：复制单位是**整个 shard 数据库**（standby shard 是整库 standby），不是"按主分区为单位放置备副本"。该模式下 standby 确实放在不同节点/region（存在 shard 级反亲和），但抽象层是"整库"而非"分区级备副本均衡分布"，与 F2 的"每个主分区的备分区放第二类节点且在第二类节点间均匀"**不在同一抽象层**——单看 Data Guard 模式 F2 仅部分对应。
   - **23ai Raft Replication 模式**：复制单位是 **replication unit（RU=一组 chunk≈分区单元）**，每个 RU 的**多个副本（leader+follower）放在不同 shard 上**，且 follower 在各 shard 间均衡（默认每 shard 当 2 个 RU 的 leader、4 个 RU 的 follower）。这与 patent 的 F0/F1/F2/F3 在同一抽象层逐条对应：RU≈主分区单元、follower≈备分区、"放在不同 shard"=反亲和（第二类节点）、leader/follower 计数均衡=F1/F2 的均匀目标、chunk 随扩缩容在 shard 间迁移=F3。
2. 因此**至少存在一个产品配置（Oracle Globally Distributed Database 23ai + Raft Replication）在 F0–F3 上全部命中**，差异仅为机制实现（chunk/RU 计数均衡、Raft 共识 vs Data Guard 物理备库）与命名（shard vs 节点、follower vs 备分区），属"以不同机制实现同一特征"= 等同，非反向。
3. 未检索到任何 Oracle 文档声明"备副本可与主副本同 shard""不要求副本跨 shard"等反向证据；亦无"out of scope/future work"之类限定语影响判定。
4. 时间合规：Raft Replication 为 Oracle Database 23ai（2024）特性，远晚于专利公开日 2017-12-01；Data Guard standby shard 放置自 12.2（2017 前后）即有，但本判定主要锚点 23ai Raft 完全落在时间窗内。
5. 落第 2 档而非第 1 档：F1–F3 均为"等同"而非字面（patent 以"节点分区计数差<整数阈值"限定均匀，Oracle 以 chunk/RU/leader-follower 计数均衡实现；patent"第二类节点=排除主所在节点/分组"，Oracle 为"replica on different shard"）——核心思想一致但表述与计量单位不同，含多处等同，故 2 档。

## 升级路径（第3-4档）
不适用（已判第 2 档）。若需收紧到第 1 档（全字面），需进一步取证：Oracle Raft 是否以"任意两 shard 上 leader/follower 个数之差 < 某整数阈值（优选 1）"的字面整数阈值实现均衡（专利 K1/K2 为整数限定，不可外推）——当前证据仅显示"balanced/even distribution"与"默认 2 leader+4 follower"，未给出严格整数阈值表述，故停在等同层。

## 总结一句话
Oracle Globally Distributed Database（尤其 23ai Raft Replication：replication unit 的多副本跨不同 shard 放置、leader/follower 在 shard 间均衡、chunk 随扩缩容在 shard 间迁移）在多节点+主备副本结构、主副本均匀、备副本反亲和均衡、负载再均衡四个特征上与本专利逐条对应（多处为等同实现），落第 2 档。
