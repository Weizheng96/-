# 09-tech-hazelcast verdict

## 候选基本信息
- 名称：Hazelcast（partition + backup + migration；背景技术显式引用→须辨析现有技术 vs 改进） / 组织：Hazelcast Inc / 类型：技术 / 初判F#：F0,F1,F2,F3 / 专利公开日：2017-12-01

## 检索粗筛（react 留痕）
Phase 1 串行 4 条 WebSearch：
1. `Hazelcast partition backup migration rebalance` → 基础 partition+backup+migration 机制（成员增减由 Master 触发再均衡）。
2. `Hazelcast partition group anti-affinity backup placement rack awareness` → backup 放到不同 partition group（反亲和）+ 均匀分布。
3. `Hazelcast PartitionGroupConfig ZONE_AWARE introduced version history 3.x release` → ZONE_AWARE 2016（3.6.5/3.7）已有，HOST_AWARE 自 3.0（2013）。
4. `Hazelcast PLACEMENT_AWARE partition group introduced version 4.0 release notes` → PLACEMENT_AWARE 引入于 4.0.1~4.2.4（~2020，晚于 2017-12-01），仅 finer-granularity 反亲和变体。
Phase 2 WebFetch：Hazelcast 3.0 文档（2013）+ 5.6 data-partitioning 文档。详见 `_sources.md`。

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注(注明证据发布/版本时间) |
| --- | --- | --- | --- | --- |
| F0 | 命中（但为现有技术） | "a node can not hold more than one copy of a partition (ownership or backup)" + 多节点主备分区结构 | https://docs.hazelcast.org/docs/3.0/manual/html/ch12s03.html | **Hazelcast 3.0 ≈2013，早于申请日 2015-03-13** → 现有技术 |
| F1 | 命中（但为现有技术） | "By default Hazelcast distributes partitions and their backup copies randomly and equally among cluster nodes"；"distributes the partitions' primary and backup replicas equally among cluster members" | https://docs.hazelcast.org/docs/3.0/manual/html/ch12s03.html ; https://docs.hazelcast.com/hazelcast/5.6/architecture/data-partitioning | 3.0 ≈2013 即均匀分布 → 现有技术 |
| F2 | 命中（但为现有技术） | "backups of these partitions are located in another partition group"；"the backup replicas of the partitions won't be kept in the same partition group that the primary replica lives" | https://docs.hazelcast.org/docs/3.0/manual/html/ch12s03.html ; https://docs.hazelcast.com/hazelcast/5.3/clusters/partition-group-configuration | 节点级反亲和自 3.0（2013）；分组级 HOST_AWARE/ZONE_AWARE 2013/2016。PLACEMENT_AWARE（~2020）仅 finer-granularity 变体，未改变 placement 算法 → 区别点不在此 |
| F3 | 部分/弱命中（且为现有技术方向） | "moves some of the primary and backup partition replicas to the new members one by one, making all members equal and redundant"；强调 "only the minimum amount of partitions are moved"（consistent hashing） | https://docs.hazelcast.com/hazelcast/5.6/architecture/data-partitioning | 再均衡机制长期既有；但 Hazelcast 以 consistent-hashing 最小迁移描述，**未**见本专利 F3"高负载节点(分区数>第三阈值)→低负载节点(分区数<第四阈值)"的特定阈值二次迁移方式 |

## 已检查文档清单
- Hazelcast 3.0 Partition Group Configuration（≈2013，早于申请日）— https://docs.hazelcast.org/docs/3.0/manual/html/ch12s03.html
- Data Partitioning and Replication（5.6，机制溯源早期）— https://docs.hazelcast.com/hazelcast/5.6/architecture/data-partitioning
- Partition Group Configuration（5.3）— https://docs.hazelcast.com/hazelcast/5.3/clusters/partition-group-configuration
- PartitionGroupConfig JavaDoc 3.7 / 4.0.1（版本对比定位 PLACEMENT_AWARE 引入时间）— https://docs.hazelcast.org/docs/3.7/javadoc/com/hazelcast/config/PartitionGroupConfig.html ; https://docs.hazelcast.org/docs/4.0.1/javadoc/com/hazelcast/config/PartitionGroupConfig.html
- Parallel migrations 设计文档 — https://github.com/hazelcast/hazelcast/blob/master/docs/design/partitioning/07-parallel-migrations.md

## 最终判定
**第 5 档：已排除（证据全部早于公开日 2017-12-01，即现有技术）**

判定依据（含现有技术 vs 新特性区分）：Hazelcast 的多节点主备分区（F0）、主备均匀分布（F1）、backup 反亲和到不同节点/分组（F2）、成员增减再均衡迁移（F3 方向）等被检机制，在 Hazelcast 3.0（≈2013）/ 3.6.5–3.7（2016）官方文档即 verbatim 成文，**全部早于本专利申请日 2015-03-13 与公开日 2017-12-01**——属现有技术（第 5 档硬条件 (b)）。本专利背景技术更 verbatim 把 hazelcast 列为其改进对象，意味着专利相对 hazelcast 的区别点（F2"第二类节点/分组"的特定形式化约束、F3 以"分区个数高/低阈值"驱动的备分区二次迁移）正是 hazelcast 既有方法之外的部分，而非被检命中的基础机制。唯一晚于 2017-12-01 的相关新特性 PLACEMENT_AWARE（~2020）仅是反亲和分组的 finer-granularity 变体（按云 placement 元数据分组），其底层 placement 算法仍是既有的"backup 放到不同 group + 均匀分布"，并未引入落入本专利区别特征的新实现。故无法证明 hazelcast 在 2017-12-01 后存在落入区别特征的侵权实现 → 排除。

## 升级路径（第3-4档）
若后续检索到 hazelcast 在 2017-12-01 之后的某版本 release notes / 设计文档中，明确引入"以分区个数超/低于阈值判定高/低负载节点、并将备副本从高负载迁至低负载"的 **F3 特定阈值二次迁移**，或 F2"第二类节点（排除主分区所在节点或其分组）"的精确等价新算法，则可上调至第 3–4 档（需精确到该特性的发布版本与时间晚于 2017-12-01，且证据为正向事实）。

## 总结一句话
Hazelcast 的 partition+backup+反亲和+再均衡机制在 2013/2016 即成文、早于专利公开日且被专利背景技术列为改进对象，属现有技术，未见 2017-12-01 后落入区别特征的新实现，落第 5 档（已排除）。
