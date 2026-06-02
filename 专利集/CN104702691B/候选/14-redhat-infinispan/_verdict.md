# 14-redhat-infinispan verdict

## 候选基本信息
- 名称：Infinispan / Red Hat Data Grid（segment owner + rebalance） / 组织：Red Hat (IBM) / 类型：产品 / 初判F#：F0,F1,F2,F3 / 专利公开日：2017-12-01

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F0 | 命中（字面） | "Infinispan splits the owners of a key into one primary owner, which coordinates writes to the key, and zero or more backup owners." / "The first node in the list of owners is the primary owner. The other nodes in the list are backup owners." | https://infinispan.org/docs/stable/titles/configuring/configuring.html | 多节点 + 数据按 key 分到 segment（=主分区粒度），每 segment 有 1 个 primary owner（对外协调写=主副本）+ numOwners-1 个 backup owner（容错=备副本）。映射 F0「多节点+多主分区，每主≥1备」。numOwners≥2 即每主≥1备。 |
| F1 | 命中（等同） | "It is important that the key-to-segment mapping evenly distributes the number of segments allocated to each node while minimizing the number of segments that must move when the cluster topology changes." | https://infinispan.org/docs/stable/titles/configuring/configuring.html | 一致性哈希以"各节点 segment 数尽量均匀"为显式目标。专利 F1 用整数阈值（任意两节点主分区数差<K1，优选1）表达"均匀"；Infinispan 用 capacityFactor 加权一致性哈希实现"evenly distributes"，机制不同但目标等同（中间不要求字面"阈值"）。判等同。 |
| F2 | 命中（等同） | "Server hinting increases availability of data in distributed caches by replicating entries across as many servers, racks, and data centers as possible." / "When Infinispan distributes the copies of your data, it follows the order of precedence: site, rack, machine, and node." / backups "stored on different nodes in the topology than the primary owners" | https://infinispan.org/docs/stable/titles/configuring/configuring.html | F2 核心=备副本反亲和到"第二类节点"（排除主副本所在节点本身；或更强排除其所属分组=机架/可用区）。Infinispan：默认一致性哈希即把 numOwners 个 owner 放在**不同节点**（node 级反亲和=排除主副本所在节点本身）；开启 Server Hinting 后按 site>rack>machine>node 优先级把 backup 放到**不同分组**（=排除主副本所属分组）。两层恰好对应 F2 的"第一类节点=所在节点 / 或所在分组"。判等同。 |
| F3 | 命中（等同） | "It is important that the key-to-segment mapping … minimizing the number of segments that must move when the cluster topology changes." / "When the cache topology changes, because a node joins or leaves the cluster, the segment ownership table is broadcast to every node." / （检索）"When a node joins, rebalancing … to give the joiner a fairly equal share … When a node leaves, its segment copies will be redistributed between remaining nodes." | https://infinispan.org/docs/stable/titles/configuring/configuring.html | F3=拓扑变化时把高负载（segment 数多）节点的备 segment 迁到低负载节点以二次均衡。Infinispan rebalance/state-transfer：join 时给新节点 fairly equal share（从负载高的现有节点迁出），leave 时其 segment 在剩余节点重分布，目标"evenly distribute + minimize movement"。以"segment 个数"衡量负载（非 CPU/流量），与 F3 限定一致。机制名 rebalance/state transfer，等同实现。判等同。 |

## 已检查文档清单
- Infinispan 官方 Configuring 文档（v16.1，当前稳定版）：primary/backup owner、Server Hinting 跨 site/rack/machine/node、segment 均匀分配 + 最小化迁移、join/leave 自动 rebalance — https://infinispan.org/docs/stable/titles/configuring/configuring.html
- Red Hat Data Grid 7.0 Server Hinting 章节（CDN 403/curl Access Denied，未取得；以上游 infinispan.org 等价权威源替代） — https://docs.redhat.com/documentation/en-us/red_hat_data_grid/7.0/html/developer_guide/chap-high_availability_using_server_hinting
- Google Patents 检索：未发现 Red Hat 自有同主题专利

## 最终判定
**第 2 档：全部命中，含 ≥1 等同特征**

判定依据：F0 字面命中（primary owner=主副本对外服务，backup owner=备副本容错，每 key 在 segment 内多 owner）。F1（一致性哈希以各节点 segment 数均匀为显式目标）、F2（默认 owner 跨不同节点 + Server Hinting 跨 rack/site 分组反亲和，恰对应 F2 的"排除所在节点 / 排除所属分组"两级）、F3（join/leave rebalance/state transfer 在均匀化目标下迁移 segment、以 segment 数衡量负载）均以"不同机制名 / 加权一致性哈希"实现专利的目标，属等同而非字面。无任何反向证据（未见"explicitly excludes"反亲和、未见"不做 rebalance"等）。四特征全命中且含多处等同 → 第 2 档。

## 升级路径（第3-4档）：不适用（已达第 2 档）。若需把 F1/F3 提升为字面命中，可核查 Infinispan 是否存在"任意两节点 segment 数差≤整数阈值"的显式实现承诺；但专利整数阈值（优选1）属可外推性差的整数限定，加权一致性哈希难以字面满足"差<K1"，故维持等同判定更稳妥，不强行升档。

## 总结一句话：Infinispan / Red Hat Data Grid 的 primary/backup owner + 一致性哈希均匀分布 + Server Hinting 反亲和 + join/leave rebalance 四要素与本专利 F0-F3 完整对应（F0 字面、F1/F2/F3 等同），无反向证据，落第 2 档。
