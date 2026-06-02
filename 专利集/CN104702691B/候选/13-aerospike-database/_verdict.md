# 13-aerospike-database verdict

## 候选基本信息
- 名称：Aerospike Database（partition + replica + rack-aware rebalance） / 组织：Aerospike Inc / 类型：产品 / 初判F#：F0,F1,F2,F3 / 专利公开日：2017-12-01

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F0 | 命中（字面） | "One node acts as the data master for reads and writes for a partition, while zero or more nodes act as read-only replicas." ；"Each namespace is divided into 4096 logical partitions" ；"Every read and write request is sent to the data master for processing." | https://aerospike.com/docs/server/architecture/data-distribution | 多节点 + 多分区，每分区有 master（对外读写）+ replica（容错），RF≥2 时每主分区≥1备 = 多节点+多主分区+每主≥1备，字面命中 F0 |
| F1 | 命中（字面/等同） | "the last 128 partitions are tweaked to even out the number of leader partitions each node has." ；"distributes partitions across nodes as evenly as possible" ；"each node stores ~1/n of the data" | https://aerospike.com/blog/optimizing-server-resources-using-uniform-balance/ ；https://aerospike.com/docs/server/architecture/data-distribution | uniform-balance（默认 prefer-uniform-balance=true）显式"even out the number of leader/master partitions each node has"=主分区个数在各节点均匀（任意两节点差趋近1）= F1 目标。算法不同（确定性哈希+末128分区微调）但效果等同 |
| F2 | 命中（等同） | "the master copy of a partition and its replica are stored in two separate racks, defined by their rack-id" ；"If the RF is less than or equal to the number of racks, replication factor number of racks are ensured to have one replica for a given partition." ；replicas "distribute across all other nodes" from the master node | https://aerospike.com/docs/server/architecture/rack-aware ；https://aerospike.com/docs/server/architecture/data-distribution | 备副本默认放在 master 之外的其他节点（排除主副本所在节点=第一类节点）；rack-aware 进一步把 replica 放到与 master 不同的 rack（排除主副本所在分组=分组级第一类节点），并在各 rack 间均匀=反亲和 + 备分区均匀 = F2。专利"第二类节点（节点级或分组级排除）"两种形式 Aerospike 均提供，等同命中 |
| F3 | 命中（等同） | "When nodes are added or removed, a new cluster forms and its nodes coordinate to evenly divide partitions between themselves. The cluster automatically rebalances." ；node 加入后"the cluster rebalances to include the new node" ；migration 在拓扑变化后重新均分分区 | https://aerospike.com/docs/server/architecture/data-distribution ；https://aerospike.com/blog/optimizing-server-resources-using-uniform-balance/ | 节点增减触发自动 rebalance/migration，把分区从原持有节点迁移以使各节点分区数重新均匀（多持有→少持有方向迁移）= F3 的"高负载（分区多）→低负载（分区少）迁移"目标。实现机制（确定性 succession list 重排 + 最小化迁移）不同，但达成相同结果，等同命中 |

## 已检查文档清单
- Aerospike Data distribution（4096 partition、master/replica、random hashing 均匀、节点增减自动 rebalance）— https://aerospike.com/docs/server/architecture/data-distribution
- Aerospike Rack awareness（master 与 replica 放不同 rack、RF≤rack 数时每 RF 个 rack 各持一 replica）— https://aerospike.com/docs/server/architecture/rack-aware
- Aerospike Blog: Optimizing Server Resources using Uniform Balance（2023-04-19；"even out the number of leader partitions each node has"、解决节点间分区数差异问题）— https://aerospike.com/blog/optimizing-server-resources-using-uniform-balance/

## 最终判定
**第 2 档：全特征命中，含 ≥1 等同**

判定依据：F0 字面命中（多节点+4096 主分区+每主分区 master 对外服务、replica 容错）；F1 字面/等同（uniform-balance 显式"even out the number of leader partitions each node has"=主分区个数均匀）；F2 等同（备副本默认放 master 之外节点 + rack-aware 放不同 rack=节点级/分组级反亲和，并在 rack 间均匀）；F3 等同（节点增减自动 rebalance/migration 重新均分分区，方向为多持有→少持有）。F2/F3 实现机制（确定性哈希 succession list + 最小化迁移）与专利"按阈值显式高低负载迁移"在算法上不同，但达成同一技术结果（备分区反亲和均匀 + 拓扑变化后再均衡），构成等同。全程未发现任何反向证据（无"不支持副本反亲和/不做再均衡"之类表述），公开材料均为持续在线文档，时间满足 >2017-12-01。

## 升级路径（第3-4档）
不适用（已落第 2 档）。若要进一步坐实第 1 档（全字面）须证明 Aerospike 的备分区均衡与高低负载迁移是按"分区个数阈值"显式判定并移动——但 Aerospike 用确定性哈希算法实现，难以字面对齐专利的阈值化高低负载迁移措辞，故维持第 2 档（等同）而非第 1 档。

## 总结一句话
Aerospike 以 4096 分区 + master/replica + uniform-balance 主分区均匀 + rack-aware 副本反亲和 + 节点增减自动 rebalance，对应 F0 字面、F1 字面/等同、F2/F3 等同，无反向证据，落第 2 档。
