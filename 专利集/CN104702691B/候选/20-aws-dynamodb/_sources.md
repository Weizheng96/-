# 证据索引 — 20-aws-dynamodb

## Phase 1 react 粗筛（WebSearch，串行）
1. `Amazon DynamoDB partition replica leader availability zone`
   - 命中：AWS 官方文档、Amazon Science 10 周年博客、多篇 USENIX ATC'22 论文笔记。
   - 信号：每 partition 3 副本跨 3 AZ；每 partition 有 leader 副本负责写 + 强一致读，follower 容错；写需 2/3 quorum。→ F0/F2 强信号。
2. `DynamoDB paper USENIX 2022 partition split rebalance load distribution`
   - 命中：USENIX ATC'22 论文及多篇笔记。
   - 信号：负载非均匀时自动 split partition、把 partition 移到不同 storage node（Global Admission Control / adaptive capacity）。→ F1/F3 信号。

## Phase 2 深抓（WebFetch，串行）
- AWS 官方文档 partition 页：partition 自动跨多 AZ 复制；负载/容量增长时自动分配额外 partition；后台自动管理。
- Amazon Science 博客（2022-10-21）：3 副本跨不同 AZ；leader 负责复制变更 + 强一致读；副本不放在共享电源的节点（反亲和/不同 failure domain）；表增长或负载增加时 partition 进一步 split；adaptive capacity 监控流量并 repartition，使热点 item 落到不同 node。
- Marc Brooker 博客（2022-07-12，USENIX ATC'22 作者）：replication group 用 Multi-Paxos 选 leader 与共识；仅 leader 副本能服务写与强一致读。

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2022-10-21 | 官方博客 | https://www.amazon.science/blog/lessons-learned-from-10-years-of-dynamodb | 3 副本跨 AZ、leader 服务写+强一致读、反亲和(不共享电源)、自动 split、repartition 到不同 node |
| 2 | (常更新文档) | 官方文档 | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.Partitions.html | partition 自动跨多 AZ 复制；负载/容量增长自动分配额外 partition |
| 3 | 2022-07-12 | 作者博客 | https://brooker.co.za/blog/2022/07/12/dynamodb.html | replication group 用 Multi-Paxos 选 leader；仅 leader 服务写+强一致读 |
| 4 | 2022-07 | 论文 | https://www.usenix.org/conference/atc22/presentation/elhemali | USENIX ATC'22 DynamoDB 原论文（间接，经笔记） |

## 时间窗
所有引用材料发布日期均 ≥ 2017-12-01（2022 年），满足时间门槛。
