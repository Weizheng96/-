# 11-scylladb-scylladb sources（检索留痕）

## Phase 1 react 粗筛（WebSearch，串行）

1. query: `ScyllaDB replica placement NetworkTopologyStrategy rack`
   - 命中：NetworkTopologyStrategy 跨 rack 放副本；"a primary replica will be chosen via the partitioner, however copies will be placed... on alternating racks"（注：此处 "primary replica" 实指 partitioner 选出的首个副本节点，非主/备语义层级 —— 见第 2 条澄清）。
   - 关键源：https://docs.scylladb.com/manual/stable/cql/ddl.html ; https://docs.scylladb.com/manual/stable/architecture/tablets.html ; https://university.scylladb.com/courses/scylla-operations/lessons/configuration-and-where-to-run-scylla/topic/configuration-and-where-to-run-scylla-racks-and-setup/

2. query: `ScyllaDB masterless peer-to-peer primary replica concept all replicas equal`（核 F0）
   - 决定性命中（正向架构事实）：
     - "All nodes are equal: there are no master, slave, or replica sets."
     - "All replicas share equal priority; there are no primary or master replicas."
     - "Datacenters in ScyllaDB are configured in a peer-to-peer manner... nor are there 'primary/replica' hierarchical relationships."
   - 源：https://www.scylladb.com/glossary/database-replication/ ; https://docs.scylladb.com/manual/stable/architecture/architecture-fault-tolerance.html ; https://www.scylladb.com/learn/nosql/nosql-vs-sql-architecture/

3. query: `ScyllaDB tablets dynamic load balancing migration rebalance overloaded node`
   - 命中：tablet load balancer 自动从高利用率节点向低利用率节点迁移 tablet（"migrate tablets from nodes with higher to nodes with lower disk utilization, equalizing the load"）。
   - 源：https://www.scylladb.com/2024/06/17/how-tablets/ ; https://docs.scylladb.com/manual/stable/architecture/tablets.html ; https://www.scylladb.com/2024/06/13/why-tablets/

## Phase 2 深抓（WebFetch）

- https://www.scylladb.com/glossary/database-replication/
  - 确认：masterless，all replicas equal，无 primary/master replica；coordinator node 仅为操作角色（与数据 mastery 无关）。"In these databases, data is replicated across multiple nodes, all of which are equal."

## 说明
- 未检索到 ScyllaDB Inc 在 2017-12-01 之后就"主备分区均匀分布"同主题的自有专利（本候选为产品，按产品架构事实定档，无需专利比对）。
