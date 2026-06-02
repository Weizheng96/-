# 证据索引 — 16-oracle-sharding（检索留痕）

## Phase 1 react 粗筛（WebSearch，串行，禁并行）

1. `Oracle Sharding chunk distribution replication primary standby`
   - 命中：chunk = shard 间数据迁移单位；shard 用 Data Guard 复制为 standby shard（同 region=HA / 跨 region=DR）；GoldenGate 可按 chunk 级复制（21c 起 deprecated）。→ 有强信号，继续。
2. `Oracle Sharding rebalance move chunks across shards balance distribution`
   - 命中："unit of data migration between shards is the chunk"；"maintain an equal distribution of the load and activity across all shards"；"move chunks from more active servers to less active servers"；添加/移除 shard 时自动 resharding 迁移多个 chunk 维持均衡。→ F1/F3 直接对应。
3. `Oracle Globally Distributed Database 23ai Raft replication unit replica placement different shards`
   - 命中（关键 F2）：replication unit (RU)=一组 chunk，**3 个副本放在不同 shard 上**；每 shard 含多个 RU 的副本（部分 leader、部分 follower）；Raft 维持 leader/follower 在 shard 间均衡（默认每 shard 当 2 个 RU 的 leader、4 个 RU 的 follower）；"no primary or standby shards"（active/active）。
4. `Oracle patent sharded database chunk replica placement balancing distributed database 2019 2020`
   - 命中：同主题 USPTO 专利存在（US10977276 "Balanced partition placement in distributed databases"；US11848987 "Sharded database leader replica distributor"）。注：为 US 专利、权属未逐一核实、且非 Oracle Sharding 产品本身——仅作背景，不作判定依据。

## Phase 2 深抓（WebFetch 因 cert error 全部走 curl 兜底）

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 19c 文档 | Oracle 官方 | https://docs.oracle.com/en/database/oracle/oracle-database/19/shard/architecture-and-concepts1.html（本地 arch_concepts.html 105KB） | "a chunk ... is the unit of data migration between shards"；"Shards are replicated for high availability and disaster recovery with Oracle Data Guard. ... Data Guard standby shards can be placed in the same region where the primary shards are placed. ... standby shards can be located in another region." |
| 2 | 23ai 文档 | Oracle 官方 | https://docs.oracle.com/en/database/oracle/oracle-database/23/shard/raft-replication.html（本地 85c0ea9f.html 12KB） | "Raft replication ... creates smaller replication units and distributes them automatically to handle chunk assignment, chunk movement, workload distribution, and balancing upon scaling (addition or removal of shards) ..." |
| 3 | 23ai 文档 | Oracle 官方 | https://docs.oracle.com/en/database/oracle/oracle-database/23/shard/enabling-raft-replication.html（本地 raft_doc.html 11KB） | "A replication unit (RU) ..."；"You must have at least 3 shards in your distributed database to use Raft replication." |
| 4 | 2025-04-10 | 第三方博客 | https://www.infolob.com/oracle-23ais-built-in-fault-tolerance-raft-replication-configuration-and-management/ | "Each RU is a bundle of table chunks and their replicas, spread across multiple shards."；"If a shard leads one replication unit, it plays follower in others, creating a balanced, interconnected system."；"Every shard houses one chunk set, and for each chunk set, replicas exist across multiple shards." |

## 兜底下载文件（候选目录内）
- arch_concepts.html（19c 架构，105KB，有效）
- 85c0ea9f.html（23 Raft Config 概览，12KB，有效）
- raft_doc.html（23 Enabling Raft，11KB，有效）
- using_raft.html（404 page-not-found，无效，忽略）
