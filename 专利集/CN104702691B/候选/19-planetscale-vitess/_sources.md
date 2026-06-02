# 证据索引 — 19-planetscale-vitess（query 留痕）

## Phase 1 react 粗筛（WebSearch，串行）
1. `Vitess shard tablet primary replica resharding`
   - 命中：vitess.io Resharding / Sharding / Reparenting；PlanetScale Horizontal Sharding。
   - 关键事实：每 shard = 1 primary + （通常）2 replica；resharding = split/merge shard，按 key range 重分数据，读先于写切流。→ F0 方向命中。
2. `Vitess tablet placement cell durability replica anti-affinity zone`
   - 命中：vitess.io Durability Policy / Scalability；Issue #3355 cell/region 拓扑；Issue #5505 semi-sync。
   - 关键事实：cross_cell durability — primary 与 semi-sync replica 可强制不同 cell（=AZ/机架）= 反亲和，但属 durability policy / 部署拓扑配置。→ F2 仅方向沾边。
3. `Vitess rebalance shards across nodes automatic load tablet distribution`
   - 命中：vitess.io Sharding / Tablet Balancer / Shard 概念。
   - 关键事实：所谓 rebalance shards = resharding（改分片数）；VTGate tablet balancer = 维持查询负载在各 tablet 间均匀，非数据/副本放置。→ F1/F3 核心机制存疑，进入 Phase 2。

## Phase 2 深抓（WebFetch，串行）
4. WebFetch https://vitess.io/docs/23.0/reference/features/tablet-balancer/
   - 结论：tablet balancer "does not move or migrate tablets between physical nodes. It operates exclusively at the query routing layer." → F3 否（查询层 LB，非备副本迁移）。
5. WebFetch https://vitess.io/docs/22.0/concepts/shard/
   - 结论："A shard typically contains one MySQL primary and potentially many MySQL replicas." 确认 F0；文档未述系统自动按节点均匀放置 shard/tablet（F1 依赖部署层）。

## Phase 2 自有专利核查（WebSearch）
6. `PlanetScale Vitess patent shard replica placement load balancing`
   - 命中：PlanetScale Vitess/Sharding 文档、博客。未检索到 PlanetScale/Vitess 在 2017-12-01 后自有同主题专利。

## 证据索引表
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 现行文档(v15) | WebSearch+doc | https://vitess.io/docs/15.0/user-guides/configuration-advanced/resharding/ | 每 shard 1 primary + 2 replica；resharding 按 key range 重分数据 → F0 命中，F1/F3 机制线索 |
| 2 | 现行文档(v21) | doc | https://vitess.io/docs/21.0/reference/features/sharding/ | rebalance shards = resharding（改分片数 split/merge），非按节点均衡放置 → F1 部分 |
| 3 | 现行文档(v22) | WebFetch | https://vitess.io/docs/22.0/concepts/shard/ | "A shard typically contains one MySQL primary and potentially many MySQL replicas" → F0 字面 |
| 4 | 现行文档(v23) | WebFetch | https://vitess.io/docs/23.0/reference/features/tablet-balancer/ | tablet balancer 只做查询路由，"does not move or migrate tablets" → F3 未命中 |
| 5 | 现行文档(v16) | doc | https://vitess.io/docs/archive/16.0/user-guides/configuration-basic/durability_policy/ | cross_cell durability：primary 与 replica 跨 cell → F2 反亲和方向 |
| 6 | issue 2017+ | doc | https://github.com/vitessio/vitess/issues/3355 | cell/region 拓扑，master 与 semi-sync replica 不同 cell → F2 部分 |
| 7 | 现行文档 | doc | https://planetscale.com/docs/vitess/sharding | 每 shard primary+replica；VTGate 间负载分发（查询层 LB） |

## 时间窗
- 专利公开日 2017-12-01。上述均为持续在线的现行产品文档（2017 后仍维护，v15-v23），落在时间窗内。

## 判定
第 4 档：F0 字面命中；F1/F2 部分命中（依赖部署层）；F3 未命中（resharding 改分片数 / tablet balancer 查询路由，均非备副本按负载迁移，机制与对象不同，非反向证据）。
