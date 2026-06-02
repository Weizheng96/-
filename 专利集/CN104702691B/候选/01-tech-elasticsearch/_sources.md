# 证据索引 — 01-tech-elasticsearch

## Phase 1 — react 模式粗筛（WebSearch）
1. `Elasticsearch shard allocation awareness primary replica rebalance`
   - 结果：命中 Elastic 官方 shard allocation awareness / cluster-level shard allocation 文档、SameShardAllocationDecider、AWS/BigDataBoutique 等。强信号覆盖 F0/F1/F2/F3 → 不剪枝，继续缩窄。
2. `Elasticsearch forced awareness replica different zone rack balance shards evenly threshold`
   - 结果：forced awareness 跨 zone/rack 分散 replica、"no two copies of same shard in same rack"、cluster balanced = equal shards per node。F2/F1 信号确认。
3. `Elasticsearch SameShardAllocationDecider replica not on same node as primary copy`
   - 结果：SameShardAllocationDecider "prevents multiple instances of the same shard to be allocated on the same node"；"won't put a replica shard on the same node as the primary"。F2 同节点反亲和 + F0 主备结构确认。

（共 3 条 WebSearch，预算 ≤4，未触发早剪枝——首条即全 F# 强信号。）

## Phase 2 — react 模式深抓（WebFetch）
1. WebFetch https://www.elastic.co/docs/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/shard-allocation-awareness
   - 取得 F2 verbatim：rack/zone 反亲和、"no two copies of the same shard are in the same rack"、forced awareness `cluster.routing.allocation.awareness.force.*`。
2. WebFetch https://www.elastic.co/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings
   - 取得 F1/F3 verbatim：「A cluster is balanced when it has an equal number of shards on each node」「weight factor … equalize the total number of shards across nodes」「minimum improvement in weight which triggers a rebalancing shard movement. Defaults to 1.0f」。

（共 2 条 WebFetch，预算 ≤6。F0 的 SameShardAllocationDecider verbatim 来自 Phase 1 搜索摘要 + Javadoc URL。）

## 证据索引表
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 当前持续维护版 | 官方文档(HTML) | https://www.elastic.co/docs/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/shard-allocation-awareness | F2：allocation/forced awareness、rack/zone 反亲和、no two copies in same rack |
| 2 | 当前持续维护版 | 官方文档(HTML) | https://www.elastic.co/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings | F1/F3：balanced=equal shards per node、weight factor、rebalance threshold 1.0f |
| 3 | v7.13.3 API | 官方 Javadoc | https://artifacts.elastic.co/javadoc/org/elasticsearch/elasticsearch/7.13.3/org/elasticsearch/cluster/routing/allocation/decider/SameShardAllocationDecider.html | F0/F2：primary 不与其 replica 同节点；同 shard 多副本不同节点 |
| 4 | 佐证 | 第三方文章 | BigData Boutique / Mincong Huang(18 allocation deciders) / AWS Open Source Blog | 一致描述 ES primary+replica、forced awareness 反亲和、自动 rebalance |

## 时间窗说明
- 专利公开（授权）日 2017-12-01。ES allocation awareness / forced awareness / 自动 rebalance 机制虽早于此存在，但所引官方文档为当前持续维护版本，产品在 2017-12-01 后仍持续开发并广泛部署使用 → 作为持续侵权材料，时间窗合规。

## 工具受限说明
- 无付费/登录墙阻碍；官方文档均公开可取。WebFetch 均成功，未触发 curl 兜底。
