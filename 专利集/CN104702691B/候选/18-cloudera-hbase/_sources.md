# 证据索引 — 18-cloudera-hbase

## WebSearch（Phase1 粗筛，串行）
1. `HBase region balancer distribution RegionServer StochasticLoadBalancer` → StochasticLoadBalancer / RegionCountSkewCostFunction（F1/F3 信号强）。
2. `HBase region replica read replica placement different RegionServer primary secondary` → Cloudera HBase Read Replicas（primary/secondary 主备、replica 放不同 RegionServer/rack；F0/F2 信号强）。
3. `HBase StochasticLoadBalancer RegionReplicaHostCostFunction RegionReplicaRackCostFunction RegionCountSkewCostFunction cost functions` → 确认 replica host/rack 代价函数 + 移出 co-hosted replica 候选生成器存在。

## 证据明细

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | CDP 7.2.18（>2017-12) | WebFetch + curl 兜底 | https://docs.cloudera.com/runtime/7.2.18/hbase-high-availability/topics/hbase-read-replicas.html | F0/F2：primary 唯一可写、secondary 只读容错；"Replicas are placed on different RegionServers, and on different racks when possible."（反亲和）。curl 取正文 5577B、grep 确认 verbatim 后删除临时文件。 |
| 2 | HBase 2.0 API | WebFetch | https://hbase.apache.org/2.0/devapidocs/org/apache/hadoop/hbase/master/balancer/StochasticLoadBalancer.html | F1/F3：RegionCountSkewCostFunction "skew in number of regions"；F2 等同：RegionReplicaHostCostFunction / RegionReplicaRackCostFunction + "Generates candidates which moves the replicas out of the region server for co-hosted region replicas." |
| 3 | CDP 7.3.1（>2017-12) | WebFetch | https://docs.cloudera.com/runtime/7.3.1/configuring-hbase/topics/hbase-stochastic-load-balancer.html | StochasticLoadBalancer 概述（代价函数细节在子页，信息有限）。 |
| 4 | 2024-09（>2017-12) | WebFetch | https://ranganathg.wordpress.com/2024/09/07/understanding-hbase-load-balancer/ | F1/F3：balancer 迭代把 region 从高代价节点移到低代价节点降 skew=均匀分布+高低负载迁移机制说明。 |

## 时间合规
所有来源为 CDP 7.x / HBase 2.x 当前维护版本文档，晚于专利公开日 2017-12-01。

## 反向证据
无。唯一限定为"region replica 默认关闭（REGION_REPLICATION=1）"——属作用域条件而非反向证据；F1/F3 在默认形态即成立。

## Cloudera 自有同主题专利核查
未做 Google Patents 逐项比对（候选已稳定落第2档；如需自有专利抗辩另行单查）。
