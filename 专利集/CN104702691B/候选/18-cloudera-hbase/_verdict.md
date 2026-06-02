# 18-cloudera-hbase verdict

## 候选基本信息
- 名称：Apache HBase（Region Balancer + region replica） / 组织：Cloudera / 类型：产品 / 初判F#：F0,F1,F3 / 专利公开日：2017-12-01

## 检索粗筛（react 留痕）
- WebSearch 1: `HBase region balancer distribution RegionServer StochasticLoadBalancer` → 命中 StochasticLoadBalancer/RegionCountSkewCostFunction（F1/F3 信号强）。
- WebSearch 2: `HBase region replica read replica placement different RegionServer primary secondary` → 命中 Cloudera Read Replicas（primary/secondary 主备 + replica 放不同 RegionServer/rack，F0/F2 信号强）。
- WebSearch 3: `HBase StochasticLoadBalancer RegionReplicaHostCostFunction RegionReplicaRackCostFunction RegionCountSkewCostFunction cost functions` → 确认 replica host/rack 代价函数与移出 co-hosted replica 的候选生成器存在。
- 粗筛结论：4 类特征均有正向信号，进入 Phase2 深抓。

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F0 | 命中（条件性：需开启 region replica；等同） | "One RegionServer services the default or primary replica, which is the only replica which can service write requests... Other RegionServers serve the secondary replicas, follow the primary RegionServer and only see committed updates. The secondary replicas are read-only" | https://docs.cloudera.com/runtime/7.2.18/hbase-high-availability/topics/hbase-read-replicas.html | 多 RegionServer（多节点）+ Region（主分区），primary replica 对外服务写、secondary replica 容错只读=主/备二元结构。**辨析**：HBase 默认 REGION_REPLICATION=1（仅主、无 region 级备副本；数据冗余在底层 HDFS 块级——不同抽象层、无分区级主备语义，不落 F0）；F0 仅在显式开启 read replica（REGION_REPLICATION>1）后成立，此时 replica 为 region 级、有主备语义=同抽象层。 |
| F1 | 命中 | "Compute the cost of a potential cluster state from skew in number of regions on a cluster."（RegionCountSkewCostFunction）；"these regions must be distributed across the region servers in such a way that the whole cluster is used optimally" | https://hbase.apache.org/2.0/devapidocs/org/apache/hadoop/hbase/master/balancer/StochasticLoadBalancer.html ; https://docs.cloudera.com/runtime/7.3.1/configuring-hbase/topics/hbase-stochastic-load-balancer.html | StochasticLoadBalancer 以 region 数 skew 为代价函数把 Region（主分区）均匀分布到各 RegionServer=主分区均匀分配（最小化任意两节点 region 数差，对应专利"阈值优选1的近乎完全均匀"目标）。 |
| F2 | 命中（条件性：需开启 region replica；等同） | "Replicas are placed on different RegionServers, and on different racks when possible."；"A cost function for region replicas." (RegionReplicaHostCostFunction)；"A cost function for region replicas for the rack distribution." (RegionReplicaRackCostFunction)；"Generates candidates which moves the replicas out of the region server for co-hosted region replicas." | https://docs.cloudera.com/runtime/7.2.18/hbase-high-availability/topics/hbase-read-replicas.html ; https://hbase.apache.org/2.0/devapidocs/org/apache/hadoop/hbase/master/balancer/StochasticLoadBalancer.html | secondary replica 放到与 primary 不同的 RegionServer/不同 rack=反亲和，正对 F2"第二类节点=排除主分区所在节点本身或其所属分组（rack=分组）"；replica host/rack cost function + 把 co-hosted replica 移出的 candidate generator=以主分区为单位让备副本在第二类节点间均衡。等同实现 F2。仅在开启 read replica 时成立。 |
| F3 | 命中 | "The Balancer creates a random nextAction... swapping two regions, or moving one region to another RegionServer. The action is applied virtually, and then the new cost is calculated. If the new cost is lower than our previous one, the action is stored."；RegionCountSkewCostFunction（"skew in number of regions"） | https://ranganathg.wordpress.com/2024/09/07/understanding-hbase-load-balancer/ ; https://hbase.apache.org/2.0/devapidocs/org/apache/hadoop/hbase/master/balancer/StochasticLoadBalancer.html | Balancer 迭代把 region 从高代价（region 数偏多=高负载）RegionServer 移到低代价节点以降 skew 代价=高负载→低负载迁移再均衡；F3 以"分区个数"判高/低负载，与 RegionCountSkewCostFunction 同口径。开启 replica 时 replica 同受 balancer 迁移并维持反亲和（移出 co-hosted replica 的候选生成器）。 |

## 已检查文档清单
- HBase StochasticLoadBalancer 配置与代价函数概述（Cloudera Runtime 7.3.1） — https://docs.cloudera.com/runtime/7.3.1/configuring-hbase/topics/hbase-stochastic-load-balancer.html
- StochasticLoadBalancer Javadoc（代价函数：RegionCountSkewCostFunction / RegionReplicaHostCostFunction / RegionReplicaRackCostFunction / 移出 co-hosted replica 的 candidate generator） — https://hbase.apache.org/2.0/devapidocs/org/apache/hadoop/hbase/master/balancer/StochasticLoadBalancer.html
- HBase Read Replicas（CDP Public Cloud 7.2.18）：primary 唯一可写、secondary 只读容错、replica 放不同 RegionServer/不同 rack（curl 兜底取正文确认 verbatim） — https://docs.cloudera.com/runtime/7.2.18/hbase-high-availability/topics/hbase-read-replicas.html
- Understanding HBase Load Balancer（balancer 迭代移动 region 降代价的机制说明） — https://ranganathg.wordpress.com/2024/09/07/understanding-hbase-load-balancer/

## 最终判定
**第 2 档：全特征命中（含等同）**

五档:1=全字面;2=全命中含≥1等同;3=≥60%无反向;4=<60%;5=已排除(仅(a)真反向/(b)全<2017-12-01/(c)架构层级不同)。第5档硬门槛=针对该候选正向事实,"通用反推/未提及"不算。0命中≠已排除。

判定依据：F1/F3（RegionCountSkewCostFunction 驱动的 region 均匀分布 + balancer 高低负载迁移）为 HBase 默认形态即字面命中；F0/F2（primary/secondary 主备二元 + replica 放不同 RegionServer/rack 反亲和 + replica host/rack cost function 均衡）在显式开启 region replica（REGION_REPLICATION>1）后成立，属功能等同（HBase 以代价函数+候选生成器近似实现"备副本反亲和均匀放置"，非字面的整数阈值差比较）。关键辨析已落实并区分两个抽象层：HBase 默认仅 HDFS 块级冗余（块级、无主备语义、不落 F0/F2）；region replica 一旦开启即 region 级主备 + 反亲和，与专利同抽象层。证据均公开版本（CDP 7.x / HBase 2.x，2017-12-01 后维护发布），时间合规。无任何反向证据。

## 升级路径（第3-4档）：本档已为第2档。若审阅认为 region replica 属可选特性、不计入"默认产品形态"，可将 F0/F2 视为条件成立而把候选降至第3档（F1/F3 默认命中 ≥60% 无反向）。要升至第1档需 HBase 文档/源码出现"任意两 RegionServer 上 region/replica 数之差 < 整数阈值（优选1）"的字面阈值差表述——当前为代价函数近似，达不到字面，故定第2档（含等同）。

## 总结一句话：Apache HBase（Cloudera）StochasticLoadBalancer 以 region 数 skew 代价均匀分布并迁移 Region（F1/F3 字面命中），开启 region replica 后 primary/secondary 主备 + replica 放不同 RegionServer/rack 反亲和均衡（F0/F2 等同，与专利同抽象层），落第2档。
