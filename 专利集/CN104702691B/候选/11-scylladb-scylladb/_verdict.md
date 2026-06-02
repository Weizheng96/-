# 11-scylladb-scylladb verdict

## 候选基本信息
- 名称：ScyllaDB（vnode/tablet + 拓扑副本 + 动态均衡） / 组织：ScyllaDB Inc / 类型：产品 / 初判F#：F0,F1,F2,F3 / 专利公开日：2017-12-01

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F0 | 反向 | "All replicas share equal priority; there are no primary or master replicas." / "All nodes are equal: there are no master, slave, or replica sets." | https://www.scylladb.com/glossary/database-replication/ | 决定性。ScyllaDB 为 masterless 全对等架构，所有副本平权，**无主副本/备副本之分**。F0 要求"每主分区对应≥1备分区，主副本对外服务+备副本容错"的主/备二元结构在 ScyllaDB 不存在——架构层级不同（真反向，非未提及）。 |
| F1 | 不适用/功能相似但无主分区语义 | tablet load balancer "balance the global load in the cluster"；副本由 partitioner + RF 均匀分布到节点 | https://docs.scylladb.com/manual/stable/architecture/tablets.html | ScyllaDB 确将数据（tablet/vnode）均匀分布到节点，但其分布对象是"平权副本"而非 F1 的"主分区"。因 F0 反向，F1 的"主分区均匀"语义无承载主体。 |
| F2 | 不适用/反亲和存在但非"主/备"约束 | "Scylla guarantees that the three replicas of each piece of data will be in different racks"（rack-aware，NetworkTopologyStrategy） | https://docs.scylladb.com/manual/stable/cql/ddl.html ; https://university.scylladb.com/courses/scylla-operations/lessons/configuration-and-where-to-run-scylla/topic/configuration-and-where-to-run-scylla-racks-and-setup/ | ScyllaDB 有 rack/DC 反亲和（不同副本不同 rack），功能上类似 F2 的"第二类节点排除"。但 F2 限定为"将**备分区**放到排除**主分区**所在节点/分组的第二类节点"——以主/备区分为前提。ScyllaDB 副本平权，无"主副本所在节点"可排除，反亲和约束对象是 R 个平权副本而非"主+备"。 |
| F3 | 不适用/迁移存在但非"备分区"迁移 | "migrate tablets from nodes with higher to nodes with lower disk utilization, equalizing the load" | https://www.scylladb.com/2024/06/17/how-tablets/ | tablet 动态均衡确从高负载向低负载节点迁移，机制上贴合 F3。但迁移对象是平权 tablet 副本，非 F3 的"第二类节点内的备分区"；且 F3 以"分区个数"超阈值界定高/低负载，ScyllaDB 以磁盘利用率界定。同样因 F0 反向而失去"备分区"承载主体。 |

## 已检查文档清单
- ScyllaDB Database Replication（masterless / all replicas equal / 无 primary 或 master replica）— https://www.scylladb.com/glossary/database-replication/
- ScyllaDB Architecture - Fault Tolerance（peer-to-peer，RF 副本平权）— https://docs.scylladb.com/manual/stable/architecture/architecture-fault-tolerance.html
- NoSQL vs SQL Architecture（masterless，no primary/replica hierarchy）— https://www.scylladb.com/learn/nosql/nosql-vs-sql-architecture/
- Data Definition / CQL DDL（NetworkTopologyStrategy，rack-aware 副本放置）— https://docs.scylladb.com/manual/stable/cql/ddl.html
- Data Distribution with Tablets（tablet load balancer 跨节点均衡、动态迁移）— https://docs.scylladb.com/manual/stable/architecture/tablets.html
- How We Implemented Tablets（高→低利用率节点 tablet 迁移）— https://www.scylladb.com/2024/06/17/how-tablets/
- Deployment Best Practices: Racks（RF 副本分布到不同 rack 保证）— https://university.scylladb.com/courses/scylla-operations/lessons/configuration-and-where-to-run-scylla/topic/configuration-and-where-to-run-scylla-racks-and-setup/

## 最终判定

**第 5 档：已排除（架构层级不同，(c)）**

五档:1=全字面;2=全命中含≥1等同;3=≥60%无反向;4=<60%;5=已排除(仅(a)真反向/(b)全<2017-12-01/(c)架构层级不同)。第5档硬门槛=针对该候选正向事实,"通用反推/未提及"不算。0命中≠已排除。

判定依据：ScyllaDB 官方明确为 masterless 全对等架构——"All replicas share equal priority; there are no primary or master replicas"——这是针对本候选的**正向架构事实**（非"未提及"反推）。本专利 F0 的核心是"主分区+备分区"二元结构（主副本对外服务、备副本容错、备副本反亲和放置），而 F1/F2/F3 全部以主分区/备分区为限定主体。ScyllaDB 副本平权、无主/备语义，整套权利要求赖以成立的结构前提缺失，属架构层级不同（第5档(c)）。其 rack 反亲和（F2 相似）、tablet 高→低负载迁移（F3 相似）虽功能贴近，但作用对象是平权副本而非"备分区"，不构成对以主/备结构为前提的权利要求的落入。

## 升级路径（第3-4档）
本候选因 F0 架构层级反向落第5档，无第3-4档升级空间。除非：ScyllaDB 未来版本引入显式"主副本对外服务+备副本仅容错"的主/备分层语义（届时 F2/F3 的反亲和与负载迁移机制可重新按主/备承载主体比对），否则结构前提不成立。当前所有公开架构文档一致表述为全对等 masterless。

## 总结一句话
ScyllaDB 为 masterless 全对等架构、所有副本平权无主/备之分，与本专利 F0"主分区+备分区"二元结构架构层级不同（rack 反亲和与 tablet 负载迁移仅功能相似、非备分区语义），落第5档（已排除-架构层级不同）。
