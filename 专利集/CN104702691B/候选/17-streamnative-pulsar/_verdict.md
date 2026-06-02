# 17-streamnative-pulsar verdict

## 候选基本信息
- 名称：Apache Pulsar（bundle/broker LB + BookKeeper ensemble 放置） / 组织：StreamNative / 类型：产品 / 初判F#：F0,F1,F3 / 专利公开日：2017-12-01

## 检索粗筛（react 留痕）
- WebSearch: `Apache Pulsar topic bundle broker load balancing` → bundle=分配单元，topic 按 bundle 哈希分到 broker，broker 间按 CPU/内存/网络/吞吐均衡，高负载 broker 卸载 bundle（broker 无状态、无副本）
- WebSearch: `Pulsar BookKeeper ensemble rack-aware placement replica primary backup` → 存储层 BookKeeper 用 EnsembleSize/WriteQuorum/AckQuorum，rack-aware 把副本放不同机架
- WebSearch: `BookKeeper write quorum ack quorum no primary replica ledger striping equal copies` → "does not maintain a primary replica in the traditional sense"，复制/共识逻辑在 client，副本对称
- WebSearch: `StreamNative patent distributed messaging load balancing replica placement` → 未见 StreamNative 自有同主题专利（命中的均为 IBM/Amazon 等他方专利）

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F0 | 不成立（架构层级不同） | "Pulsar brokers have no persistent state that cannot be lost. They are separated from the storage layer."；BookKeeper "does not maintain a primary replica in the traditional sense. Instead, the replication and consensus logic lives in the client." | https://jack-vanlightly.com/blog/2018/10/2/understanding-how-apache-pulsar-works ; https://medium.com/splunk-maas/apache-bookkeeper-insights-part-1-external-consensus-and-dynamic-membership-c259f388da21 | 本专利 F0 要求"主分区+每主≥1备分区，主对外服务/备容错"的主备二元结构。Pulsar 计算层（broker-bundle）完全无副本；存储层（BookKeeper）用 E/Qw/Qa 仲裁副本，各副本对称平等、无主/备之分。两层都不存在专利所述主/备结构 → 架构层级不同 |
| F1 | 不适用 | "topics are assigned to brokers at the bundle level rather than the topic level… distribute these bundles across brokers to achieve load balancing" | https://pulsar.apache.org/docs/next/concepts-broker-load-balancing-concepts/ | bundle 在 broker 间均衡＝把"无副本的服务单元"均衡，形态近似"主分区均匀"，但因 F0 主/备结构不成立，均衡对象与专利"主分区（有对应备分区）"语义不同，不构成 F1 字面/等同命中 |
| F2 | 不适用 | "Rack-aware placement policy enforces different data replicas to be placed in different racks"；"BookKeeper client … pick bookies from different racks" | https://pulsar.apache.org/docs/next/administration-isolation-bookie/ ; https://streamnative.io/blog/deep-dive-into-data-placement-policies | BookKeeper rack-aware ensemble placement 确有"副本跨机架反亲和"语义（近似 F2 的第一类/第二类节点分组约束），但作用于无主/备的对称 quorum 副本，而非专利"某主分区对应的备分区放第二类节点"——缺主备结构则 F2 的"备分区"主语不存在 |
| F3 | 不适用 | "the leader asks the overloaded brokers to unload some high loaded bundles of topics"（broker 层）；存储层 ensemble 一旦写定不做高低负载迁移 | https://pulsar.apache.org/docs/next/concepts-broker-load-balancing-concepts/ ; https://bookkeeper.apache.org/docs/4.6.2/development/protocol/ | broker 层有"高负载卸载 bundle 到低负载 broker"的高→低迁移形态（近似 F3），但迁移对象是无副本的 bundle；F3 限定"将（某主分区的）备分区从高负载移到低负载第二类节点"——无备分区主语，不适用 |

## 已检查文档清单
- Apache Pulsar — Broker load balancing concepts（bundle=assignment unit，topic 按 bundle 分配到 broker，自动卸载高负载 bundle） — https://pulsar.apache.org/docs/next/concepts-broker-load-balancing-concepts/
- Jack Vanlightly — Understanding How Apache Pulsar Works（broker 无持久状态、与存储层分离；BookKeeper E/Qw/Qa 副本对称） — https://jack-vanlightly.com/blog/2018/10/2/understanding-how-apache-pulsar-works
- Splunk-MaaS / Jack Vanlightly — BookKeeper Insights Part 1（SWMR 模型，"does not maintain a primary replica in the traditional sense"，复制/共识逻辑在 client） — https://medium.com/splunk-maas/apache-bookkeeper-insights-part-1-external-consensus-and-dynamic-membership-c259f388da21
- Apache Pulsar — Isolate bookies / rack-aware placement（不同副本放不同机架的反亲和） — https://pulsar.apache.org/docs/next/administration-isolation-bookie/
- StreamNative — Deep Dive into Data Placement Policies（rack-aware / region-aware ensemble placement） — https://streamnative.io/blog/deep-dive-into-data-placement-policies
- Apache BookKeeper — The BookKeeper protocol（writeset/striping，ack quorum 任意子集，无主副本回填） — https://bookkeeper.apache.org/docs/4.6.2/development/protocol/

## 最终判定
**第 5 档：已排除（架构层级不同）**

判定依据：本专利核心前提 F0 是"主分区 + 每主分区≥1 备分区，主副本对外服务、备副本容错"的主/备二元副本结构。Apache Pulsar 计算层（broker-bundle 负载均衡）完全无副本概念，只是把无状态服务单元在 broker 间均衡；存储层（BookKeeper）虽有多副本，但采用 E/Qw/Qa 仲裁协议，各副本对称平等、明确"无传统意义上的主副本"，不存在主/备之分。F0 在两层都不成立属架构层级不同（第 5 档 c），其上的 F1/F2/F3 均无"主分区/备分区"主语可对应——即便 broker 层 bundle 均衡近似 F1/F3、BookKeeper rack-aware 近似 F2 的反亲和，也是落在不同架构层级的不同机制，非专利所述主备分区均衡方法的等同实现。检索亦未发现 StreamNative 2017-12-01 后自有同主题（主备分区放置/再均衡）专利。

## 升级路径（第3-4档）：若后续出现公开材料证明 Pulsar/StreamNative 在同一层引入"分区主副本对外服务 + 备副本容错且每主≥1 备"的主备二元结构，并在该结构上做主分区均匀（F1）、备副本反亲和放置（F2）、备副本高低负载迁移（F3），可重新评估升至第 3-4 档。当前公开架构不满足 F0 前提，无升级依据。

## 总结一句话：Apache Pulsar 计算层无副本、存储层 BookKeeper 用对称 quorum 副本无主/备之分，与本专利"主/备分区"二元结构属不同架构层级，F0 不成立连带 F1/F2/F3 无对应主语，落第 5 档（已排除·架构层级不同）。
