# 证据索引 — 04-tech-tikv

## Phase 1 react 粗筛（WebSearch）
1. `TiKV PD scheduler region replica placement label`
   - 命中：Schedule Replicas by Topology Labels（location-labels / isolation-level）、TiKV Scheduling、TiDB Scheduling、PD Config、PD Control。强信号：F2 反亲和（label/zone 散布副本）。
2. `TiDB PD balance-region balance-leader scheduler hot region`
   - 命中：Best Practices for PD Scheduling、tikv/pd Wiki Balance/Scheduling Introduction、pd-ctl。强信号：三默认调度器 balance-region(F1/F3) / balance-leader(F1) / balance-hot-region(F3)。
   - 结论：2 条 WebSearch 即全特征命中，无早剪枝条件，进入 Phase 2。

## Phase 2 深抓（WebFetch）+ 证据索引

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | stable（公开日后持续维护） | 官方文档 | https://docs.pingcap.com/tidb/stable/tidb-scheduling/ | F0：Region 多副本，leader 读写/follower 复制；F1："All Region leaders are distributed evenly on stores"；F2："Replicas of a Region must not be in one unit"；F3：hot spot 检测与分布 |
| 2 | stable | 官方文档 | https://docs.pingcap.com/tidb/stable/schedule-replicas-by-topology-labels/ | F2：location-labels / isolation-level，"different replicas of the same data are scattered as much as possible"，zone/rack 隔离 |
| 3 | stable | 官方文档 | https://docs.pingcap.com/tidb/stable/pd-scheduling-best-practices/ | F1/F3：balance-region / balance-leader / balance-hot-region 三默认调度器，按 region count 评分均衡 |
| 4 | wiki | tikv/pd Wiki | https://github.com/tikv/pd/wiki/Balance-Scheduling | F3：balance-region 选 high score 的 source store 迁移到 lower score 的 target store（高→低迁移机制确认） |
| 5 | master | pingcap/docs 源 | https://github.com/pingcap/docs/blob/master/tidb-scheduling.md | F2：调度需求 "Replicas of a Region must not be in one unit" / "distributed on different machines according to different topologies"；F1/F3 优化项 |

## 时间窗说明
专利公开日 2017-12-01。证据均来自 PingCAP 官方文档 stable 版本（PD 调度自 TiDB GA 起持续维护、2017-12-01 后长期公开），满足"公开日之后仍公开"的时间窗要求。
