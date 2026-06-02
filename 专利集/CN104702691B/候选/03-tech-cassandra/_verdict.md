# 03-tech-cassandra verdict

## 候选基本信息
- 名称：Apache Cassandra（vnode + NetworkTopologyStrategy） / 组织：DataStax / 类型：技术 / 初判F#：F0,F1,F2,F3 / 专利公开日：2017-12-01

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F0 | 反向（不成立） | "Cassandra also has a masterless architecture – any node in the database can provide the exact same functionality as any other node"；"As every replica can independently accept mutations to every key that it owns"；"All replicas are equally important; there is no primary or master replica." | https://cassandra.apache.org/_/cassandra-basics.html ；https://cassandra.apache.org/doc/4.1/cassandra/architecture/dynamo.html | F0 要求"每个主分区对应于至少一个备分区（主副本对外服务+备副本容错）"的主/备二元结构。Cassandra 为 masterless 全对等多主，所有副本平等、均可独立读写——**无主/备副本之分**，F0 前提架构层级不同。此为产品正向架构事实，非通用反推。 |
| F1 | 命中（等同） | vnode（num_tokens 默认 256 / allocate_tokens_for_keyspace）使 token range 均匀分布；"When a node joins the cluster, it assumes responsibility for an even portion of data from the other nodes" | https://docs.datastax.com/en/cassandra-oss/3.0/cassandra/architecture/archDataDistributeVnodesUsing.html | 数据/token 在节点间近均匀分布，对应 F1"任意两节点分区数差<阈值"目标。但 Cassandra 无"主分区"概念，均匀的是所有副本而非"主副本"。 |
| F2 | 命中（等同） | "NetworkTopologyStrategy also attempts to choose replicas within a datacenter from different racks as specified by the Snitch"；rack 数 ≥ RF 时每副本落不同 rack | https://cassandra.apache.org/doc/4.1/cassandra/architecture/dynamo.html | 跨 rack/DC 放置副本＝反亲和（对应 F2"第二类节点排除主副本所在分组"）。但因无主副本锚点，实为"所有副本互相分散到不同 rack"，并非"备副本排除主副本所在节点/分组"。映射结构性偏弱。 |
| F3 | 命中（等同） | 节点增减后 vnode 增量再均衡 + anti-entropy repair（"sub-range repair and incremental repair" via Merkle tree）；nodetool cleanup/repair；"If a node fails, the load is spread evenly across other nodes" | https://cassandra.apache.org/doc/4.1/cassandra/architecture/dynamo.html ；https://docs.datastax.com/en/cassandra-oss/3.0/cassandra/architecture/archDataDistributeVnodesUsing.html | 拓扑变化后把数据/副本重新均匀分摊，对应 F3 高低负载再均衡的目标层面。但同样作用于所有平等副本，非"备分区从高负载移到低负载"。 |

## 已检查文档清单
- Apache Cassandra Basics（masterless 架构，节点对等，无 master/primary 节点） — https://cassandra.apache.org/_/cassandra-basics.html
- Apache Cassandra Dynamo 架构文档（所有副本平等可独立读写；NetworkTopologyStrategy 跨 rack 放置；vnode 增量再均衡 + repair） — https://cassandra.apache.org/doc/4.1/cassandra/architecture/dynamo.html
- DataStax Data replication 文档（NetworkTopologyStrategy 跨 rack 副本放置） — https://docs.datastax.com/en/cassandra-oss/3.0/cassandra/architecture/archDataDistributeReplication.html
- DataStax Virtual nodes 文档（vnode 均匀 token 分布、节点加入承担均等份额、故障负载均摊） — https://docs.datastax.com/en/cassandra-oss/3.0/cassandra/architecture/archDataDistributeVnodesUsing.html
- AxonOps / CMU QuABase（佐证 masterless、所有副本平等无 primary） — https://axonops.com/docs/data-platforms/cassandra/architecture/distributed-data/ ；https://quabase.sei.cmu.edu/mediawiki/index.php/Cassandra_Data_Replication_Features

## 最终判定

**第 5 档：已排除（架构层级不同 — F0 前提不成立）**

五档：1=全字面；2=全命中含≥1等同；3=≥60%且无反向；4=<60%；5=已排除（仅(a)真反向/(b)证据全<2017-12-01/(c)架构层级不同）。

判定依据：本专利权利要求以"主分区 + 对应备分区（主副本对外服务 + 备副本容错）"的**主/备二元副本结构**为前提（F0）。Apache Cassandra 是 masterless 全对等多主架构，官方文档正向陈述"所有副本平等、无主/备副本之分、每个副本均可独立接受对其拥有 key 的读写"——这是针对该产品的**正向架构事实**，构成对 F0 的真反向（命中第5档硬门槛 (c)）。F1/F2/F3 虽在 vnode 均匀、跨 rack 反亲和、再均衡层面有功能对应，但它们都作用于"所有平等副本"而非"主分区/备分区"；一旦 F0 这一前提性系统结构限定不成立，整条独立权利要求的主题（在"主分区"间均衡、把"备分区"按"第二类节点=排除主副本所在分组"放置并再均衡）即无法读到 Cassandra。故排除。

## 升级路径（第3-4档）
不适用（已落第5档）。理论上若指向某个在 Cassandra 之上人为引入"主副本/写主"语义的衍生方案（如某些读写分离代理、或 DataStax 自有把某副本钉为 primary 的特性），需对该衍生层另立候选并重新核 F0；本候选指向的开源 Cassandra/vnode/NetworkTopologyStrategy 本体不满足 F0。

## 总结一句话
Cassandra 为 masterless 全对等架构、所有副本平等无主/备之分，与本专利"主分区+备分区"二元结构属架构层级不同，落第5档（已排除）。
