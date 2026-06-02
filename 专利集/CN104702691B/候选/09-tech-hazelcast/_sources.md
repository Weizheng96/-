# 证据索引 — 09-tech-hazelcast

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| S1 | 2013（Hazelcast 3.0 文档） | 官方文档 | https://docs.hazelcast.org/docs/3.0/manual/html/ch12s03.html | "By default Hazelcast distributes partitions and their backup copies randomly and equally among cluster nodes"（F0/F1）；"a node can not hold more than one copy of a partition (ownership or backup)"（F2 节点级反亲和）；"backups of these partitions are located in another partition group"（F2 分组级反亲和）。**早于申请日 2015-03-13** → 现有技术 |
| S2 | 当前（5.6，机制溯源至早期） | 官方文档 | https://docs.hazelcast.com/hazelcast/5.6/architecture/data-partitioning | "Hazelcast distributes the partitions' primary and backup replicas equally among cluster members"（F0/F1）；成员加入后 "moves some of the primary and backup partition replicas to the new members one by one, making all members equal and redundant"（再均衡，强调最小迁移，非 F3 高低阈值方式） |
| S3 | 3.6.5 / 3.7（2016） | 官方文档/JavaDoc | https://docs.hazelcast.org/docs/3.7/javadoc/com/hazelcast/config/PartitionGroupConfig.html | ZONE_AWARE 等 partition group 类型在 2016 年文档已存在；HOST_AWARE 自 3.0。**早于公开日 2017-12-01** → 现有技术 |
| S4 | 当前 | 官方文档 | https://docs.hazelcast.com/hazelcast/5.3/clusters/partition-group-configuration | "the backup replicas of the partitions won't be kept in the same partition group that the primary replica lives"（F2）；HOST_AWARE/ZONE_AWARE/PLACEMENT_AWARE/CUSTOM 分组策略 |
| S5 | 4.0.1→4.2.4 间（~2020，晚于 2017-12-01） | JavaDoc 对比 | https://docs.hazelcast.org/docs/4.0.1/javadoc/com/hazelcast/config/PartitionGroupConfig.html | PLACEMENT_AWARE 在 4.0.1 JavaDoc 尚无，4.2.4+ 才出现 → 引入于 2020 后；但为反亲和分组的 finer-granularity 变体（按云 placement 元数据），未引入本专利区别特征 |
| S6 | 当前 | GitHub 设计文档 | https://github.com/hazelcast/hazelcast/blob/master/docs/design/partitioning/07-parallel-migrations.md | migration 由 Master 在成员增减时触发再均衡；`hazelcast.partition.max.parallel.migrations` 并行迁移（基础 migration 机制，长期既有） |

## Phase 1 粗筛 WebSearch（串行，4 条）
1. `Hazelcast partition backup migration rebalance` → 基础 partition+backup+migration 机制（成员增减触发，Master 管理）。
2. `Hazelcast partition group anti-affinity backup placement rack awareness` → F2 反亲和分组 + F0/F1 均匀分布。
3. `Hazelcast PartitionGroupConfig ZONE_AWARE introduced version history 3.x release` → ZONE_AWARE 2016（3.6.5/3.7）已有，HOST_AWARE 自 3.0（2013）。
4. `Hazelcast PLACEMENT_AWARE partition group introduced version 4.0 release notes` → PLACEMENT_AWARE 引入于 4.0.1~4.2.4（~2020，晚于 2017-12-01），但仅 finer-granularity 反亲和变体。

## 时间窗结论
- F0/F1/F2 核心机制在 Hazelcast 3.0（2013）/ 3.6.5–3.7（2016）即成文，**全部早于公开日 2017-12-01 且早于申请日 2015-03-13** → 现有技术。
- 本专利背景技术 verbatim 将 hazelcast 列为现有方案，佐证其既有方法是改进对象，不构成侵权证据。
- 唯一 2017-12-01 后新特性 PLACEMENT_AWARE（~2020）仅为反亲和分组的 finer-granularity 变体，未落入本专利区别特征（F2"第二类节点/分组"特定形式化、F3"分区数高/低阈值"二次迁移）。
- 未检索到 hazelcast 在 2017-12-01 后引入落入本专利区别特征的新实现。
