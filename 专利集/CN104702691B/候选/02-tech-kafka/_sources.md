# 02-tech-kafka 检索留痕（_sources.md）

## Phase 1 — react 粗筛（WebSearch，串行）
1. `Kafka rack-aware replica assignment leader follower partition`
   - 命中：KIP-36 Rack aware replica assignment、KIP-881、Cloudera rack awareness、AWS MSK rack awareness、KIP-879 multi-level rack awareness。
   - 信号：replicas of same partition spread across racks（反亲和=F2）；"number of leaders per broker will be constant"（F1）。判定：强正向，继续。
2. `Kafka Cruise Control rebalance broker load partition reassignment move replicas`
   - 命中：Strimzi/Red Hat/Cloudera/IBM Cruise Control 文档、linkedin/cruise-control GitHub。
   - 信号："reassigning partitions to other brokers"、"Partition movement: transferring the partition replica and its data to a new location"、"Leadership movement: switching the leader"（F3+F1）。判定：强正向，继续。
3. `Cruise Control ReplicaDistributionGoal LeaderReplicaDistributionGoal evenly distribute replicas leaders brokers`
   - 命中：linkedin/cruise-control Wiki Pluggable-Components、Red Hat AMQ/Streams 文档。
   - 信号：ReplicaDistributionGoal=均匀副本数（F1/F3）、LeaderReplicaDistributionGoal=均匀 leader 数（F1）、RackAwareGoal（F2）。判定：直接命中四特征，停止粗筛。

（仅用 3 条即获得 F0-F3 全部正向信号，未触发早剪枝。）

## Phase 2 — 深抓（WebFetch，串行）
- https://cwiki.apache.org/confluence/display/KAFKA/KIP-36+Rack+aware+replica+assignment
  - 引文："Assign to as many racks as possible. That means if the number of racks are more than or equal to the number of replicas, each rack will have at most one replica."（F2 反亲和：racks≥RF 时每 rack 至多一副本）
  - 引文："if each rack has the same broker count, each broker will have the same leader count and replica count."（F1 主分区均匀）
  - 时间：2016-03-04，targeting Kafka 0.10.0。
- https://docs.cloudera.com/runtime/7.3.1/cctrl-overview/topics/cctrl-how-it-works.html
  - 引文："partitions, replicas and topics are reassigned between the brokers until the requirements set by the goal are met."（F3 迁移机制）
- https://github.com/linkedin/cruise-control/wiki/Pluggable-Components
  - RackAwareGoal："A goal that ensures all the replicas of each partition are assigned in a rack aware manner."（F2）
  - ReplicaDistributionGoal："Attempt to make all the brokers in a cluster to have the similar number of replicas."（F1/F3）
  - LeaderReplicaDistributionGoal："Attempt to make all the brokers in a cluster to have the similar number of leader replicas."（F1）
  - PreferredLeaderElectionGoal："Attempt to make the first replica in replica list leader replica of the partition for all topic partition."（F0/F1 leader=主副本对外服务）
- 补充检索引文（Cruise Control 各发行商文档 / WebSearch 摘要）：
  - "ReplicaDistributionGoal attempts to make all the brokers in a cluster to have the similar number of replicas. This goal ensures that the total number of partition replicas are distributed evenly amongst brokers in a pool."
  - "A partition reassignment command consists of … Partition movement: Involves transferring the partition replica and its data to a new location. … Leadership movement: This involves switching the leader of the partition's replicas."

## 时间窗说明（基准 2017-12-01）
- KIP-36（2016）/ Cruise Control 核心机制虽首次提出早于专利公开日，但 Kafka 与 Cruise Control 的 rack-aware + distribution-goal 机制在 2017-12-01 之后持续分发并被各商业版（Confluent、Red Hat AMQ Streams、Cloudera、IBM Event Streams、AWS MSK、Strimzi）长期使用与文档化（KIP-879/KIP-881 为 2022；Cloudera 7.3.1 / Red Hat Streams 2.x 文档为 2020-2024）。因此存在大量 2017-12-01 之后的公开证据材料，满足时间窗。

## 工具受限说明
- 无。WebSearch/WebFetch 均正常返回，未触发 curl 兜底。
