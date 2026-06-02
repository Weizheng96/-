# 04-tech-tikv verdict

## 候选基本信息
- 名称：TiKV / TiDB（Region 多副本 + PD 调度）
- 组织：PingCAP
- 类型：技术
- 初判F#：F0,F1,F2,F3
- 专利公开日：2017-12-01

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F0 | 命中（等同） | "In TiKV, data is organized as Regions, which are replicated on several stores. In all replicas, a leader is responsible for reading and writing, and followers are responsible for replicating Raft logs from the leader." | https://docs.pingcap.com/tidb/stable/tidb-scheduling/ | Region=分区，每 Region 多副本；leader=主副本对外读写，follower=备副本容错。等同点：Raft 多副本对等、leader 由选举产生（非静态指定主），但运行期"leader 读写 / follower 备份"语义与"主副本对外服务 + 备副本容错"完全对应。 |
| F1 | 命中 | "All Region leaders are distributed evenly on stores."；balance-leader "calculating a score based on the region count and using operators to distribute leaders as evenly as possible across stores" | https://docs.pingcap.com/tidb/stable/tidb-scheduling/ ; https://docs.pingcap.com/tidb/stable/pd-scheduling-best-practices/ | 主分区（leader）在各 store 间均匀=balance-leader；F1 的"任意两节点主分区数差<阈值"对应"distribute leaders as evenly as possible"。 |
| F2 | 命中 | "PD schedules replicas according to the label layer to make sure that different replicas of the same data are scattered as much as possible.… ['zone','rack'] means that replicas should be placed to different zones first, then to different racks"；"Replicas of a Region must not be in one unit"；isolation-level=zone 时 "PD will always guarantee that replicas of the same Region are distributed across different zones" | https://docs.pingcap.com/tidb/stable/schedule-replicas-by-topology-labels/ ; https://github.com/pingcap/docs/blob/master/tidb-scheduling.md | 直接对应 F2 反亲和：备副本排除主副本所在节点 / 分组（host/rack/zone）。location-labels = "第一类节点所属分组"约束；同一 Region 副本散布到不同 unit 即"备分区放第二类节点"。 |
| F3 | 命中 | balance-region "selects a 'source store' with high region scores … and migrates regions to target stores with lower scores"；"PD can detect hot spots from store heartbeats and Region heartbeats, so that PD can distribute hot spots"；balance-hot-region "redistribute hot spots across stores as much as possible … redistribute both region peers and leaders" | https://github.com/tikv/pd/wiki/Balance-Scheduling ; https://docs.pingcap.com/tidb/stable/tidb-scheduling/ ; https://docs.pingcap.com/tidb/stable/pd-scheduling-best-practices/ | 高负载 store（高分/热点）→ 低负载 store（低分）迁移 region peer/副本，对应 F3"高负载节点备分区移到低负载节点"。判据用 region score/count 而非 CPU/流量，与 F3"以分区个数界定高低负载"一致。 |

## 已检查文档清单
- TiDB Scheduling（官方文档：Region 多副本、leader/follower 语义、调度需求与优化项）— https://docs.pingcap.com/tidb/stable/tidb-scheduling/
- Schedule Replicas by Topology Labels（location-labels / isolation-level / 副本反亲和散布）— https://docs.pingcap.com/tidb/stable/schedule-replicas-by-topology-labels/
- Best Practices for PD Scheduling（balance-region / balance-leader / balance-hot-region 三调度器）— https://docs.pingcap.com/tidb/stable/pd-scheduling-best-practices/
- tikv/pd Wiki: Balance Scheduling（source store 高分 → target store 低分迁移）— https://github.com/tikv/pd/wiki/Balance-Scheduling
- pingcap/docs tidb-scheduling.md（"Replicas of a Region must not be in one unit" 反亲和需求）— https://github.com/pingcap/docs/blob/master/tidb-scheduling.md

## 最终判定
**第 2 档：全部命中（含 ≥1 等同特征）**

五档：1=全字面；2=全命中含≥1等同；3=≥60%无反向；4=<60%；5=已排除（仅(a)真反向/(b)全<2017-12-01/(c)架构层级不同）。第5档硬门槛=针对该候选正向事实，"通用反推/未提及"不算。0命中≠已排除。

判定依据：F0/F1/F2/F3 四特征均有 PingCAP 官方文档 verbatim 正向证据。Region=主备分区、PD 按 label/zone 反亲和放副本（F2 字面命中）、balance-leader 主副本均匀（F1）、balance-region/hot-region 高分 store→低分 store 迁移副本（F3）。F0 计为等同：TiKV 用 Raft 多副本（leader 由选举产生、副本对等），与专利"静态指定主副本"实现机制不同，但运行期"leader 对外读写 + follower 容错"与"主副本对外服务 + 备副本容错"语义等同，故落第 2 档而非第 1 档。F2/F3 调度持续演进且 TiDB GA 在 2017-12-01 之后仍长期维护，时间窗满足（材料均为公开日后持续公开版本）。

## 升级路径（第3-4档）
不适用（已落第 2 档）。若需进一步坐实第 1 档（全字面），可抓取 PD 源码 schedulers（balance_region.go / balance_leader.go）确认"source = max region/leader count store，target = min count store"的整数计数比较逻辑，以及 placement-rules 中按 location-labels 的硬隔离实现，验证是否存在与专利"任意两节点之差 < 阈值（优选 1）"完全字面对应的计数阈值判定。

## 总结一句话
TiKV/TiDB 的 PD 调度（Region 主备副本 + location-labels 反亲和 + balance-region/leader/hot-region 高低 store 迁移）F0–F3 全命中，因 Raft 选举式主副本属等同而非字面，落第 2 档。
