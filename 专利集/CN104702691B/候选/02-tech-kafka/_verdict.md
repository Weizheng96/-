# 02-tech-kafka verdict

## 候选基本信息
- 名称：Apache Kafka（leader/follower partition + rack-aware replica assignment + Cruise Control / Self-Balancing）/ 组织：Confluent Inc（及 Apache 社区、Red Hat、Cloudera、IBM、AWS MSK、Strimzi 等分发方）/ 类型：技术 / 初判命中F#：F0,F1,F2,F3 / 专利公开日：2017-12-01

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F0 | 字面 | "Leadership movement: This involves switching the leader of the partition's replicas." / RackAwareGoal："A goal that ensures all the replicas of each partition are assigned in a rack aware manner." | https://github.com/linkedin/cruise-control/wiki/Pluggable-Components | Kafka 每个 topic partition 由多 broker 节点上的多副本组成，其中 leader 副本对外读写服务、follower 副本仅同步容错 → 主分区+备分区二元结构，每主分区≥1备副本，命中 F0 前提结构。 |
| F1 | 字面/等同 | "if each rack has the same broker count, each broker will have the same leader count and replica count." / LeaderReplicaDistributionGoal："Attempt to make all the brokers in a cluster to have the similar number of leader replicas." | https://cwiki.apache.org/confluence/display/KAFKA/KIP-36+Rack+aware+replica+assignment ; https://github.com/linkedin/cruise-control/wiki/Pluggable-Components | leader（=主分区，对外服务）在 broker 间数量均衡（"similar number"="任意两节点差<阈值"等同表述）。命中 F1。 |
| F2 | 字面/等同 | "Assign to as many racks as possible. That means if the number of racks are more than or equal to the number of replicas, each rack will have at most one replica." / RackAwareGoal："…all the replicas of each partition are assigned in a rack aware manner." | https://cwiki.apache.org/confluence/display/KAFKA/KIP-36+Rack+aware+replica+assignment ; https://github.com/linkedin/cruise-control/wiki/Pluggable-Components | follower（备副本）放置排除 leader 所在 rack/分组（rack≥RF 时每 rack 至多一副本=反亲和），等价专利"第一类节点=主分区所在节点所属分组、备副本只放第二类节点"；ReplicaDistributionGoal 保证副本在 broker 间均匀。命中 F2。 |
| F3 | 等同 | "partitions, replicas and topics are reassigned between the brokers until the requirements set by the goal are met." / ReplicaDistributionGoal："Attempt to make all the brokers in a cluster to have the similar number of replicas." / "Partition movement: Involves transferring the partition replica and its data to a new location." | https://docs.cloudera.com/runtime/7.3.1/cctrl-overview/topics/cctrl-how-it-works.html ; https://github.com/linkedin/cruise-control/wiki/Pluggable-Components | Cruise Control / Confluent Self-Balancing 通过 partition reassignment 把副本从副本数偏多（高负载）broker 迁到副本数偏少（低负载）broker，使各 broker 副本数趋同——以"goal-driven 收敛到 similar number"机制实现专利"分区数>阈值节点的备分区移到分区数<阈值节点"的目标，属等同（实现手段不同、效果一致）。命中 F3。 |

## 已检查文档清单
- KIP-36 Rack aware replica assignment（2016-03-04, Kafka 0.10.0）— rack 反亲和 + leader/replica 均衡 — https://cwiki.apache.org/confluence/display/KAFKA/KIP-36+Rack+aware+replica+assignment
- linkedin/cruise-control Wiki «Pluggable Components» — RackAwareGoal / ReplicaDistributionGoal / LeaderReplicaDistributionGoal / PreferredLeaderElectionGoal 定义 — https://github.com/linkedin/cruise-control/wiki/Pluggable-Components
- Cloudera «How Cruise Control works»（7.3.1, 2023+）— reassignment 迁移机制 — https://docs.cloudera.com/runtime/7.3.1/cctrl-overview/topics/cctrl-how-it-works.html
- Red Hat / Cloudera Cruise Control 文档（2020-2024）— Partition movement / Leadership movement 描述、ReplicaDistributionGoal 均匀副本数说明
- （检索覆盖）KIP-881 / KIP-879（2022）、AWS MSK rack awareness、Strimzi Cruise Control blog（2020）— 证明机制在 2017-12-01 后持续分发与文档化

## 最终判定
**第 2 档：全命中（含 ≥1 等同）**

判定依据：F0、F1 字面命中（leader/follower 二元结构、leader 在 broker 间均衡）；F2 以 rack-aware 反亲和 + ReplicaDistributionGoal 命中（"第一类节点=主副本所属分组"恰对应 rack 排除，字面/等同）；F3 以 Cruise Control goal-driven partition reassignment 将副本从副本多的 broker 迁到副本少的 broker 实现专利"高负载→低负载迁移"目标，属等同实现。未发现任何 F# 的真反向证据（无"explicitly excludes"/"不支持"类陈述）。时间窗满足：机制虽 2016 首提，但在 2017-12-01 后由 Confluent/Red Hat/Cloudera/IBM/AWS MSK/Strimzi 持续分发并文档化。

## 升级路径（第3-4档填）：不适用（已落第 2 档）。如需升至第 1 档（全字面），需就 F3 找到 Kafka/Cruise Control 文档中"以分区数阈值（count threshold）判定高/低负载并据此迁移"的字面表述（当前为 goal 收敛到 similar number 的等同表述，而非专利的整数阈值字面）；当前 F3 为等同，故停在第 2 档。

## 总结一句话：Apache Kafka（leader/follower 分区 + KIP-36 rack-aware 反亲和 + Cruise Control 副本均衡再分配）对专利 F0-F3 全部命中，其中 F3 高低负载迁移属等同实现，落第 2 档（全命中含等同），无反向证据且时间窗满足。
