# 证据索引 — 10-tech-redis-cluster

## Phase 1 粗筛 WebSearch（串行）
1. `Redis Cluster hash slot master replica node distribution`
   → 命中：slot 在 master 间均分(F1)、master 服务+replica 容错+每 master ≥1 replica+自动 failover(F0)。signal 强。
2. `Redis Cluster replica different node anti-affinity rack-aware --cluster-replicas placement`
   → 命中：redis-cli 为 anti-affinity 优化 replica 分配、primary/replica 置于不同节点、rack-zone awareness 跨 zone 分布(F2)。signal 强。
3. `redis-cli cluster rebalance slots move weight balance nodes`
   → 命中：`--cluster rebalance` 把 slot 均匀分到 master、支持 weight、reshard 移指定 slot(F1/F3 思想)。signal 中。
（粗筛 3 条均有正向 signal，不触发早剪枝。）

## Phase 2 深抓证据表
| # | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- |
| 1 | WebFetch | https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/ | F0：master 服务 slot、replica 容错/failover、每 master 终≥1 replica；F1：slot 均匀分到 master |
| 2 | WebFetch | https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/ | F1：16384 slot 均分到 master；reshard 在节点间移 slot |
| 3 | curl 兜底(本地) | severalnines-rebalance.html（源 https://severalnines.com/blog/hash-slot-resharding-and-rebalancing-redis-cluster/ ；WebFetch cert error） | F1/F3：`rebalance` 把 slot 均分，实测每节点 5461/5462 slot；迁移对象为 master slot |
| 4 | WebFetch | https://oneuptime.com/blog/post/2026-01-25-redis-cluster-slot-rebalancing/view | F3：rebalance 非自动、须人工 CLI；不涉及 replica/备副本迁移 |
| 5 | WebSearch摘要 | https://redis.io/docs/latest/operate/rs/clusters/configure/rack-zone-awareness/ | F2：primary/replica 跨 zone 分布（=分组反亲和） |
| 6 | WebSearch摘要 | https://redis.io/docs/latest/operate/kubernetes/reference/yaml/rack-awareness/ | F2：replica 与 master 置于不同节点 |
| 7 | WebFetch | https://github.com/redis/redis/issues/11306 | rack-aware replica 调度为社区提问（非内建确证；未采纳为反向证据） |

## WebFetch 失败兜底记录
- severalnines WebFetch 返回 "unknown certificate verification error"
  → 已用 `curl -ksSL -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"` 下载 severalnines-rebalance.html（134 KB），本地 grep 取证。

## 受限/未决
- 未检索到 Redis Ltd 2017-12-01 之后自有同主题专利（不影响本判定）。
- 未取证到 Redis 内建"按负载在节点间自动迁移备副本"能力（→ F3 仅等同+对象差异，留升级路径）。
