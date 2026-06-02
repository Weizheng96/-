# 证据索引 — 04-redhat-osp-ovsdpdk

## Phase 1 — react 粗筛 query 留痕
1. WebSearch: `Red Hat OpenStack OVS-DPDK pmd-auto-lb automatic load balancing PMD threads`
   - 强相关命中：Red Hat Developer 博客 "Automatic load balancing for PMD threads in Open vSwitch with DPDK"、"Improve multicore scaling in Open vSwitch DPDK"、OVS 官方 PMD 文档、RH Bugzilla #1824458 RFE、RH OSP NFV 文档。
   - 结论：首条 query 即直接命中 pmd-auto-lb 全特征，无需追加 query。

## 证据索引
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2021-04-29 | RH Developer 博客 | https://developers.redhat.com/blog/2021/04/29/automatic-load-balancing-for-pmd-threads-in-open-vswitch-with-dpdk | F1 PMD/RxQ 负载测量；F2 load-threshold 持续 1 分钟 + rebal-interval 时间窗 + variance 改善判断；F3 RxQ 重新分配到不同 PMD；F4 PMD 1:1 绑核轮询多端口多 RxQ |
| 2 | 2021-11-19 | RH Developer 博客 | https://developers.redhat.com/articles/2021/11/19/improve-multicore-scaling-open-vswitch-dpdk | 佐证：阈值满足触发 reassignment、config 变更（增删 RxQ/PMD）触发、group 分配按当前 PMD 负载最佳平衡铺开 workload |
| 3 | — | OVS 官方文档 | https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/ | pmd-auto-lb 配置项（pmd-auto-lb-load-threshold 默认 95%、pmd-auto-lb-rebal-interval 默认 1 分钟、PMD 绑核轮询 RxQ） |
| 4 | — | RH Bugzilla RFE | https://bugzilla.redhat.com/show_bug.cgi?id=1824458 | Red Hat OSP 中 ovs-dpdk auto load balance 启用（[RFE] ovs-dpdk auto load balance enablement）|

## 反向证据
- 未发现任何"不支持/excludes"型真反向证据。
- 时间合规：所有一手资料发布日期均 > 专利公开日 2015-08-12。
