# 20-aws-dynamodb verdict

## 候选基本信息
- 名称：Amazon DynamoDB（partition + replica，多 AZ） / 组织：Amazon (AWS) / 类型：产品 / 初判F#：F0,F1,F2,F3 / 专利公开日：2017-12-01

## 检索粗筛
- WebSearch 1：`Amazon DynamoDB partition replica leader availability zone` → 官方文档 + Amazon Science 博客 + USENIX ATC'22 论文笔记，命中"每 partition 3 副本跨 3 AZ，leader 服务写+强一致读，follower 容错"。
- WebSearch 2：`DynamoDB paper USENIX 2022 partition split rebalance load distribution` → 命中"负载非均匀时自动 split partition、移 partition 到不同 storage node（Global Admission Control / adaptive capacity）"。
- 粗筛结论：4 条 F# 均有正向公开材料且时间 ≥2017-12-01，未触发早剪枝，进入 Phase 2 深抓。

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F0 | 命中（字面） | "DynamoDB stores three copies of each partition, in different availability zones." / "There is a leader for the group that is responsible for replicating all the customer mutations and serving strongly consistent reads." / "The replicas for a partition form a replication group. The replication group uses Multi-Paxos for leader election and consensus." "Only the leader replica can serve write and strongly consistent read requests." | amazon.science 博客 / brooker.co.za | 多节点+多 partition；每 partition=1 leader(主副本，对外写+强一致读)+多 follower(备副本，容错)。结构与 F0 一一对应。 |
| F1 | 部分/等同存疑 | "DynamoDB is optimized for uniform distribution of items across a table's partitions." / "adaptive capacity monitors traffic patterns and repartitions tables so that heavily accessed items reside on different nodes." | AWS 文档 / amazon.science 博客 | DynamoDB 确把 partition 分散到各 storage node 追求均衡，但公开材料用 throughput/流量驱动，未见"任意两节点主分区个数之差<整数阈值(优选1)"的分区计数机制。F1 是整数阈值限定，不可外推 → 仅算"目的相近"，机制级证据不足。 |
| F2 | 命中（含等同） | "DynamoDB stores three copies of each partition, in different availability zones." / "we wouldn't assign a partition and one of its copies to nodes that share a power supply, because a power outage would take both of them offline." | amazon.science 博客 | 副本强制放在不同 AZ / 不同 failure domain（不共享电源）= F2"备副本排除主副本所在节点/分组"的反亲和约束。等同实现（AZ/failure-domain 反亲和 ↔ 专利"第二类节点/分组"）。"第二类节点间均匀"无逐字证据，但跨 3 AZ 隐含分散。 |
| F3 | 部分/等同存疑 | "partitions could be further split to allow the table to scale elastically." / "Global Admission Control … proactively splits partitions or moves partitions to different storage nodes." / "adaptive capacity … repartitions tables so that heavily accessed items reside on different nodes." | brooker.co.za / USENIX 笔记 / amazon.science 博客 | DynamoDB 把高负载 partition 移到其他 node 平衡热点，目的与 F3 一致（等同）。但 F3 限定"以分区个数判高/低负载"且明确针对"备分区"迁移；DynamoDB 公开材料以 throughput/流量为度量且不区分主/备副本迁移 → 度量维度与对象不完全吻合，机制级逐字证据不足。 |

## 已检查文档清单
- Amazon Science《Lessons learned from 10 years of DynamoDB》(2022-10-21)：3 副本跨 AZ、leader 服务写+强一致读、反亲和(不共享电源)、自动 split、repartition 到不同 node — https://www.amazon.science/blog/lessons-learned-from-10-years-of-dynamodb
- AWS 官方文档《Partitions and data distribution in DynamoDB》：partition 自动跨多 AZ 复制；负载/容量增长自动分配额外 partition；后台自动管理 — https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.Partitions.html
- Marc Brooker《The DynamoDB paper》(2022-07-12，USENIX ATC'22 作者)：replication group 用 Multi-Paxos 选 leader；仅 leader 服务写+强一致读 — https://brooker.co.za/blog/2022/07/12/dynamodb.html
- USENIX ATC'22 论文《Amazon DynamoDB: A Scalable, Predictably Performant, and Fully Managed NoSQL Database Service》(2022-07，间接经笔记) — https://www.usenix.org/conference/atc22/presentation/elhemali

## 最终判定
**第 3 档：高度相关（≥60% 命中，无反向证据，但部分特征仅有目的级/等同证据而缺机制级逐字证据）**

五档:1=全字面;2=全命中含≥1等同;3=≥60%无反向;4=<60%;5=已排除(仅(a)真反向/(b)全<2017-12-01/(c)架构层级不同)。第5档硬门槛=针对该候选正向事实,"通用反推/未提及"不算。0命中≠已排除。

判定依据：F0 字面命中、F2 等同命中（AZ/failure-domain 反亲和 ↔ 专利"第二类节点/分组"），均有官方/作者级公开证据；F1、F3 目的一致且方向相符（均衡分布 + 高负载 partition 迁移），但本专利 F1/F3 含"以分区个数为度量的整数阈值"且 F3 明确针对备分区，而 DynamoDB 公开材料以 throughput/流量为度量、不区分主/备副本迁移——属架构层级相同（同为分区+多副本放置+负载再均衡）但机制细节缺逐字佐证。命中比例≥60%（F0/F2 实打实，F1/F3 部分），无任何反向证据，DynamoDB 为闭源黑盒、实现细节仅二手披露，故落第 3 档而非更高/更低。

## 升级路径（第3-4档）：
1. 取 USENIX ATC'22 原始 PDF（非笔记），定位 partition 在 storage node 上的放置算法是否以"分区计数"近均匀（验证 F1 整数阈值），及自动 split / move 是否对 follower（备）副本同样适用且以负载阈值触发（验证 F3 对备分区 + 高/低阈值）。
2. 检索 Amazon 2017-12-01 后自有同主题专利（Google Patents，申请人 Amazon/AWS，主题 partition replica placement / rebalance），若有自有专利则进一步佐证机制等同性并可作交叉引用。
3. 若取得机制级逐字证据使 F1/F3 由"目的级"升为"等同"，则可升至第 2 档。

## 总结一句话：
DynamoDB 同为"分区+多 AZ 副本(leader 主/follower 备)+自动 split 与负载再均衡"架构，F0 字面、F2 等同(AZ 反亲和)命中，F1/F3 方向一致但因闭源黑盒缺机制级逐字证据且度量维度(throughput vs 分区计数)不同，无反向证据，落第3档。
