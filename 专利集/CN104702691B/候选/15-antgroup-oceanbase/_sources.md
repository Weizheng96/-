# 证据索引 — 15-antgroup-oceanbase

## Phase 1 react 粗筛（WebSearch，串行）
1. `OceanBase 分区 副本 Paxos leader follower 负载均衡`
   - 命中：三副本/分区、leader 主副本对外读写、follower 备副本投票+弱一致读、Paxos 多数派、未设 primary zone 时按负载均衡自动选主、主副本在 server 间均匀分布。→ F0/F1 强信号。
2. `OceanBase Zone 副本分布 主备 RootService 均衡`
   - 命中：Locality=各 Zone 副本分布、Primary Zone 按优先级把 leader 打散到不同机器、RootService 每 Zone 部署一个、RootService 管理资源单元负载均衡（CPU/磁盘/内存/IOPS）。→ F1/F2/F3 信号。
3. `OceanBase 分区副本 迁移 负载均衡 unit 数据均衡 反亲和 不同Zone`
   - 命中：分区转移技术以分区为单位跨节点搬迁、Unit 迁移实现 Zone 内节点间负载均衡、同一分区副本分布在多个 Zone、扩缩容触发副本迁移。→ F2/F3 信号。
4. `蚂蚁 OceanBase 专利 分区 副本 负载均衡 迁移 主副本 节点`
   - 命中（文档/介绍为主）：每台 OB Server 均有主副本和从副本、自动迁移部分分区到新节点做负载均衡、副本由系统按策略分散到多 Server、按负载均衡策略在多个全功能副本中选 leader。

粗筛结论：四条全部正向命中，无早剪枝，进入 Phase 2。

## Phase 2 深抓（WebFetch，串行）

| # | 时间/版本 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | OB v3.1.1 教程 | 官方文档 | https://www.bookstack.cn/read/OceanBase-3.1.1-zh/c0c7037ce0b5914c.md | 主均衡=primary_zone 资源单元上主数量均衡(F1)；RootService 按 CPU/磁盘/内存/IOPS 均衡(F3)；分区组先个数均衡再交换负载最高/最低资源单元上的分区(F3) |
| 2 | OB v1.4 教程 | 官方文档 | https://www.bookstack.cn/read/oceanbase-1.4-zh/1522fe8ff850a576.md | leader 对外提供服务、follower 可非一致读(F0)；每分区物理多副本(F0)；副本按策略分散到多 Server、Locality=各 Zone 副本分布(F2) |
| 3 | OB v2.2.77 教程 | 官方文档 | https://www.bookstack.cn/read/OceanBase-2.2.77-zh/d1e167e910d90924.md | 交换负载最高/最低资源单元上的分区、负载动态变化持续触发迁移使硬盘持续均衡(F3) |
| 4 | — | （取数失败） | http://www.oceanbase.wiki/concept/.../overview-of-partitions-and-replicas/ | WebFetch 证书错误 + curl Empty reply，未取到；F2 证据已由 #2 覆盖 |

## 备注
- OceanBase 为蚂蚁集团自研、已开源分布式关系数据库；上述官方教程为真实实现描述，版本（v2.2.77/v3.1.1 为 2019 年后；v1.4 副本机制持续沿用）均晚于专利公开日 2017-12-01。
- 未检索到可直接抓取权利要求的蚂蚁自有同主题中国专利原文（WebSearch 仅返回文档/科普），故以官方技术文档作为实现证据。
