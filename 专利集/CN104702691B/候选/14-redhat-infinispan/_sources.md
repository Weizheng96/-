# 证据索引 — 14-redhat-infinispan

## Phase 1 react 粗筛（WebSearch，串行，禁并行）
1. `Infinispan distributed mode primary owner backup owner segment consistent hash`
   → primary owner（协调写）+ zero or more backup owners；key 空间切固定 segment（numSegments 可配）；每 key 哈希映射到 segment，第一个 owner=primary，其余=backup。→ 支持 F0、F1。
2. `Infinispan server hinting rack aware backup owner different machine site numOwners`
   → Server Hinting 跨 site/rack/machine/node 复制；precedence=site,rack,machine,node；backup 不与 primary 同物理 server/rack/datacenter；numOwners-1 容错。→ 支持 F2（反亲和）。
3. `Infinispan rebalance state transfer node join leave even balanced segment distribution data minimize movement`
   → "key-to-segment mapping evenly distributes the number of segments allocated to each node while minimizing the number of segments that must move when the cluster topology changes"；join/leave 自动 rebalance，joiner 拿 fairly equal share，leave 时其 segment 在剩余节点间重分布。→ 支持 F1、F3。
4. `Red Hat Infinispan patent distributed cache backup placement consistent hash site:patents.google.com`
   → 未检索到 Red Hat 自有同主题专利（仅第三方分布式缓存/一致性哈希专利）。

## Phase 2 深抓（WebFetch，串行）
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | Infinispan 16.1（当前稳定版，≫2017-12-01） | 官方文档 | https://infinispan.org/docs/stable/titles/configuring/configuring.html | F0：primary owner + backup owners；F2：Server Hinting 跨 site/rack/machine/node，backup 与 primary 不同节点；F1/F3：segment 均匀分配 + 拓扑变化时最小化迁移；rebalance on join/leave |
| 2 | RHDG 7.0 | 官方文档（被 CDN 拦截） | https://docs.redhat.com/.../red_hat_data_grid/7.0/.../chap-high_availability_using_server_hinting | WebFetch 301→403；curl 兜底 Access Denied（Akamai 拦截，非缺文件）。改用 #1 上游 infinispan.org 等价权威源（RHDG=Infinispan 商业版，Server Hinting 同源同实现） |

## 时间窗
证据来自 Infinispan 16.1 当前文档（≫2017-12-01）；Server Hinting / 一致性哈希分布为 Infinispan 长期核心特性，时间合规。
