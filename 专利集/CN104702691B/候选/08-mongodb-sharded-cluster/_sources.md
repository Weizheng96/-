# 证据索引 — 08-mongodb-sharded-cluster

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 现行(2026在线) | 官方文档 | https://www.mongodb.com/docs/manual/sharding/ （本地 sharding.html） | F0：「Each shard must be deployed as a replica set.」shard 必为 replica set |
| 2 | 现行(2026在线) | 官方文档 | https://www.mongodb.com/docs/manual/core/sharding-balancer-administration/ （本地 balancer.html） | F1/F3：balancer 在 config server primary 运行；chunk 从多→少迁移至「even amount of data per shard」；migration threshold 触发；三倍 range size 平衡判据 |
| 3 | 现行(2026在线) | 官方文档 | https://www.mongodb.com/docs/manual/core/replica-set-members/ （本地 replica-set-members.html） | F0：replica set=mongod 组，「The primary receives all write operations.」「Secondaries replicate operations from the primary to maintain an identical data set.」主/备副本二元结构 |
| 4 | 现行(2026在线) | 官方文档 | https://www.mongodb.com/docs/manual/core/replica-set-architectures/ （本地 replica-set-architectures.html） | F2（反亲和意图）：「keep at least one member in an alternate data center」成员跨主机/数据中心分布以容错 |
| 5 | 现行(2026在线) | 官方文档 | https://www.mongodb.com/docs/manual/core/zone-sharding/ （本地 zone-sharding.html） | F2 反向辨析：zone 约束 chunk→shard（主数据放置层），非备副本反亲和 |

## 检索 query 留痕（Phase 1 react 串行）
1. `MongoDB sharded cluster balancer chunk distribution replica set` → balancer / sharding 强信号
2. `MongoDB replica set member distribution different nodes data center awareness secondary placement` → 成员跨主机分布反亲和素材
3. `MongoDB zone sharding chunk balancing placement constraint shard ranges` → zone=chunk→shard 放置约束

## 抓取兜底说明
WebFetch 报 unknown certificate verification error；curl 报 schannel TLS 握手失败；改用 PowerShell Invoke-WebRequest（强制 TLS1.2/1.3）成功下载 5 份 HTML 到本目录，本地 Grep 取 verbatim。

## 时间窗
全部为 MongoDB 官方现行 Manual（持续维护，2026-06 在线），远晚于专利公开日 2017-12-01，满足时间窗。
