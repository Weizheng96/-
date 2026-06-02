# 证据索引 — 17-streamnative-pulsar

## Phase 1 react 粗筛 query（串行）
1. WebSearch `Apache Pulsar topic bundle broker load balancing` → bundle=分配单元；topic 按 bundle 哈希分到 broker；broker 间按 CPU/内存/网络IO/吞吐均衡；leader 让高负载 broker 卸载高负载 bundle。broker 无状态、无副本。
2. WebSearch `Pulsar BookKeeper ensemble rack-aware placement replica primary backup` → 存储层 BookKeeper EnsembleSize/WriteQuorum/AckQuorum；RackAwareEnsemblePlacementPolicy 把不同副本放不同机架。
3. WebSearch `BookKeeper write quorum ack quorum no primary replica ledger striping equal copies` → "does not maintain a primary replica in the traditional sense"；SWMR；复制/共识逻辑在 client；ack quorum 为 write quorum 任意子集；副本对称。
4. WebSearch `StreamNative patent distributed messaging load balancing replica placement` → 未发现 StreamNative 自有同主题专利；命中均为他方（IBM/Amazon 等）。

## Phase 2 深抓 WebFetch（串行）
1. WebFetch https://jack-vanlightly.com/blog/2018/10/2/understanding-how-apache-pulsar-works
   - verbatim："Pulsar brokers have no persistent state that cannot be lost. They are separated from the storage layer."
   - "Each topic is owned by a single Pulsar broker."（单 broker 服务该 topic，但 broker 不持有数据副本）
   - BookKeeper E/Qw/Qa；副本对称、无层级。

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | — | docs | https://pulsar.apache.org/docs/next/concepts-broker-load-balancing-concepts/ | bundle=分配单元，broker 间均衡，高负载 bundle 卸载（无副本） |
| 2 | 2018-10 | blog | https://jack-vanlightly.com/blog/2018/10/2/understanding-how-apache-pulsar-works | broker 无持久状态、与存储层分离；BookKeeper E/Qw/Qa 副本对称 |
| 3 | — | blog | https://medium.com/splunk-maas/apache-bookkeeper-insights-part-1-external-consensus-and-dynamic-membership-c259f388da21 | "does not maintain a primary replica in the traditional sense"，复制/共识在 client |
| 4 | — | docs | https://pulsar.apache.org/docs/next/administration-isolation-bookie/ | rack-aware：不同副本放不同机架（反亲和） |
| 5 | — | blog | https://streamnative.io/blog/deep-dive-into-data-placement-policies | rack-aware / region-aware ensemble placement |
| 6 | — | docs | https://bookkeeper.apache.org/docs/4.6.2/development/protocol/ | writeset/striping，ack quorum 任意子集，无主副本回填 |

## 核心辨析结论
- 计算层（broker-bundle LB）：无副本，纯无状态服务单元均衡。
- 存储层（BookKeeper ensemble）：有多副本但 quorum 对称、无主/备之分。
- 两层均不满足专利 F0 的"主/备分区二元结构" → 架构层级不同（第 5 档 c）。F1/F2/F3 形态虽各有近似机制，但因 F0 主语缺失而不适用。
