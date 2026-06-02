# 证据索引 — 07-tech-ignite

## Phase 1 WebSearch（react 串行）
1. `Apache Ignite primary backup partition affinity function`
   - https://ignite.apache.org/docs/latest/data-modeling/data-partitioning
   - https://github.com/apache/ignite/blob/master/modules/core/src/main/java/org/apache/ignite/cache/affinity/AffinityFunction.java
   - https://ignite.apache.org/releases/latest/javadoc/org/apache/ignite/cache/affinity/rendezvous/ClusterNodeAttributeColocatedBackupFilter.html
   - https://dzone.com/articles/data-distribution-in-apache-ignite
2. `Ignite RendezvousAffinityFunction backup filter rack aware different node`
   - https://ignite.apache.org/releases/latest/javadoc/org/apache/ignite/cache/affinity/rendezvous/ClusterNodeAttributeAffinityBackupFilter.html
   - https://apacheignite.readme.io/docs/affinity-collocation
3. `Ignite rebalance partitions node join leave even distribution affinity`
   - https://ignite.apache.org/docs/latest/data-rebalancing
   - https://cwiki.apache.org/confluence/display/IGNITE/(Partition+Map)+Exchange+-+under+the+hood

## Phase 2 深抓（curl 兜底，WebFetch 证书/403 失败）
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 现行版本 | 官方文档 | data-partitioning.html — https://ignite.apache.org/docs/latest/data-modeling/data-partitioning | F0（primary/backup partition）、F1（affinity 均匀分布）verbatim |
| 2 | 现行版本 | 官方文档 | data-rebalancing.html — https://ignite.apache.org/docs/latest/data-rebalancing | F1/F3（join/leave 触发 rebalance、distributed equally、backup→primary）verbatim |
| 3 | master 源码 | 源码 javadoc | backupfilter-src.java — https://raw.githubusercontent.com/apache/ignite/master/modules/core/src/main/java/org/apache/ignite/cache/affinity/rendezvous/ClusterNodeAttributeAffinityBackupFilter.java | F2 反亲和：primary/backup 不同 group/AZ/site verbatim |

失败来源：ClusterNodeAttributeAffinityBackupFilter.html javadoc（HTTP 403）、affinity-collocation（readme.io SPA，curl 35）、configuring-backups.html（curl 35）——核心证据已由上述三份成功取证覆盖。

## 时间窗说明
专利公开日 2017-12-01。Ignite 为持续维护现行产品，当前版本文档/源码（远晚于 2017-12-01）仍描述上述特征，满足"公开日后仍在公开提供"。
