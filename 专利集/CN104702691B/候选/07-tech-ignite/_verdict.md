# 07-tech-ignite verdict

## 候选基本信息
- 名称：Apache Ignite（partition + backup + affinity backup filter） / 组织：GridGain Systems / 类型：技术 / 初判F#：F0,F1,F2,F3 / 专利公开日：2017-12-01

## 检索粗筛（Phase 1 react 留痕）
- WebSearch 1：`Apache Ignite primary backup partition affinity function` → 命中官方 Data Partitioning 文档、AffinityFunction 源码、ClusterNodeAttributeColocatedBackupFilter javadoc、DZone Data Distribution。明确 primary/backup partition 概念 + affinity function 控制分区→节点映射。强正向。
- WebSearch 2：`Ignite RendezvousAffinityFunction backup filter rack aware different node` → 命中 AffinityBackupFilter / ClusterNodeAttributeAffinityBackupFilter；确认 backup filter 可"排除同 rack/availability zone 节点作为 backup"，且 excludeNeighbors 排除同 host。强正向（F2）。
- WebSearch 3：`Ignite rebalance partitions node join leave even distribution affinity` → 命中 Data Rebalancing 文档、PME；确认 join/leave 触发 rebalance、affinity function 保证分区均匀分布。强正向（F1/F3）。
- 早剪枝判定：不适用（无 0 命中、材料为持续维护的现行版本、架构层级一致——均为分布式数据/缓存的分区-主备放置层）。进入 Phase 2。

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F0 | 字面命中 | "One of the partitions is called the *primary* partition, and the other two are called *backup* partitions. … The node with backup partitions is called the *backup node*." / "only one primary node (and optionally 1 or more backup nodes) need to be updated" | https://ignite.apache.org/docs/latest/data-modeling/data-partitioning | 多节点+多分区，每分区可配≥1 backup（primary 对外读写、backup 容错），与 F0"多节点+多主分区，每主≥1备"字面对应。 |
| F1 | 等同 | "the affinity function guarantees that when the topology changes, partitions are migrated only to the new node that joined or from the node that left." / "When a new node joins the cluster, some partitions are relocated to the new node so that the data remains distributed equally in the cluster." | https://ignite.apache.org/docs/latest/data-modeling/data-partitioning ; https://ignite.apache.org/docs/latest/data-rebalancing | 目标=主分区在各节点均匀（"distributed equally"）。机制为 rendezvous hashing（允许少量偏差），非专利的整数阈值算法→不同机制达成同目标=等同；F1 不要求字面"阈值"。 |
| F2 | 字面命中 | "Attribute-based affinity backup filter that forces each partition's primary and backup nodes to different hardware … e.g., in AWS, to different 'availability zones'." / "the set of attribute values defines the key of a group into which a node is placed, an[d] the primaries and backups for a partition cannot share nodes in the same group." | https://raw.githubusercontent.com/apache/ignite/master/modules/core/src/main/java/org/apache/ignite/cache/affinity/rendezvous/ClusterNodeAttributeAffinityBackupFilter.java | 直接命中 F2 反亲和核心："backup 不与 primary 同分组（rack/AZ/site）"= 专利"备分区放第二类节点(排除主分区所在节点/所属分组)"。excludeNeighbors 另排除同 host=排除主所在节点本身。 |
| F3 | 等同 | "When a new node joins the cluster, some partitions are relocated to the new node so that the data remains distributed equally in the cluster." / "When backups are configured, one of the backup copies of the lost partitions becomes a primary partition and the rebalancing process is initiated." | https://ignite.apache.org/docs/latest/data-rebalancing | 节点增减触发 rebalance，把分区从负载高处搬到新（低载）节点以"distributed equally"，含 backup 副本重建。与 F3"高负载备分区移到低负载节点"同效；判高低载以"分区数均衡"为目标，机制不同=等同。 |

## 已检查文档清单
- Apache Ignite 官方 Data Partitioning（primary/backup partition、affinity function、PME） — https://ignite.apache.org/docs/latest/data-modeling/data-partitioning
- Apache Ignite 官方 Data Rebalancing（join/leave 触发、distributed equally） — https://ignite.apache.org/docs/latest/data-rebalancing
- ClusterNodeAttributeAffinityBackupFilter.java 源码 javadoc（primary/backup 跨 group/AZ 反亲和） — https://raw.githubusercontent.com/apache/ignite/master/modules/core/src/main/java/org/apache/ignite/cache/affinity/rendezvous/ClusterNodeAttributeAffinityBackupFilter.java
- （检索命中）RendezvousAffinityFunction backup filter / excludeNeighbors、ClusterNodeAttributeColocatedBackupFilter javadoc — backup filter 排除同 rack/host

## 最终判定
**第 2 档：全部命中（含等同）**

判定依据：F0、F2 字面命中（primary/backup partition 概念 + affinity backup filter 强制 backup 与 primary 跨 group/AZ/rack = 反亲和"第二类节点"约束）；F1、F3 命中但实现机制为 rendezvous hashing + 拓扑变化 rebalance（"data remains distributed equally"），与专利"整数阈值差<K"算法不同机制达成同一"分区均匀分布/高低负载再均衡"目标，按"不同机制实现X=等同"判为等同。四特征全覆盖、无任一真反向证据。注意：Ignite/GridGain 为持续维护的现行产品，当前版本文档与源码（远晚于 2017-12-01）描述上述特征，满足"专利公开日后仍在公开提供"时间窗。

## 升级路径（第3-4档）
不适用（已为第 2 档，高于 3-4 档）。若反向需降档：仅当能证明 Ignite 默认配置下 backup 放置不做反亲和（默认无 affinityBackupFilter，backup 仅靠 rendezvous hashing 随机落不同节点而非"排除主所在分组"），则 F2 在默认态可能仅为"不同节点"而非"排除分组"，会从字面降为等同——但 backup filter 为官方提供的标准配置项，机架/AZ-aware 部署普遍启用，仍维持第 2 档。

## 总结一句话
Apache Ignite 的 partition+backup+affinity backup filter 四特征全覆盖（F0/F2 字面、F1/F3 等同），无反向证据，落第 2 档。
