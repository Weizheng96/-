# 04-redhat-osp-ovsdpdk verdict

## 候选基本信息
- 名称：Red Hat OpenStack Platform OVS-DPDK（NFV fast-datapath）
- 组织：Red Hat (IBM)
- 类型：产品
- 初判命中 F#：F1,F2,F3,F4
- 专利公开日：2015-08-12

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（检测转发线程状态属性） | 字面 | "A PMD thread, or poll mode driver thread, is a thread that runs 1:1 on a dedicated core to continually poll ports for packets." + "The percentage usage shown for each Rx queue here is tightly measured around processing packets for individual Rx queues." + "a PMD core's CPU utilization percentage is measured" | https://developers.redhat.com/blog/2021/04/29/automatic-load-balancing-for-pmd-threads-in-open-vswitch-with-dpdk | PMD 线程=转发处理线程；测量每 PMD 核 CPU 利用率 / 每 RxQ 负载即"检测 K 个转发线程的状态属性"（对应从权"剩余转发资源额度/负载"状态属性）。 |
| F2（判断是否满足预设调整触发条件） | 字面 | "The load threshold is the percentage of processing cycles one of the PMD threads must consistently be using for one minute before a reassignment can occur." + "The interval threshold is the minimum time in minutes between which two reassignments can be triggered." + 触发前判断"the variance between the PMD thread loads is likely to improve after a reassignment." | https://developers.redhat.com/blog/2021/04/29/automatic-load-balancing-for-pmd-threads-in-open-vswitch-with-dpdk | load-threshold（默认 95%，持续 1 分钟）+ rebal-interval（默认 1 分钟时间窗）+ 负载方差可改善判断 = 权 1"满足预设调整触发条件"，且命中从权"K 线程间负载均衡度低于预设"。 |
| F3（调整至少 1 个线程所服务的交换端口） | 字面 | "The reassignment code will assign the largest loaded Rx queues to different PMD threads. It will also try to ensure that all PMD threads have the same number of assigned Rx queues." | https://developers.redhat.com/blog/2021/04/29/automatic-load-balancing-for-pmd-threads-in-open-vswitch-with-dpdk | RxQ（交换端口的接收队列）运行时从一个 PMD 迁移到另一 PMD = 调整转发线程所服务的交换端口（运行时动态再分配，非业务前固定绑定）。 |
| F4（K 为正整数，多线程多端口） | 字面 | "A PMD thread … runs 1:1 on a dedicated core" + "Each PMD thread is assigned a group of Rx queues from the various ports attached to the OVS-DPDK bridges to poll." + 预置条件 "two or more non-isolated PMDs present, and at least one non-isolated PMD is polling more than one Rx queue." | https://developers.redhat.com/blog/2021/04/29/automatic-load-balancing-for-pmd-threads-in-open-vswitch-with-dpdk | PMD 1:1 绑核（K 线程↔K CPU 一一对应，正中权 17 限定），每线程轮询多端口多 RxQ，K≥2 多核形态。 |

## 已检查文档清单
- "Automatic load balancing for PMD threads in Open vSwitch with DPDK"（2021-04-29，Red Hat Developer）— 一手主证据，F1-F4 全 verbatim — https://developers.redhat.com/blog/2021/04/29/automatic-load-balancing-for-pmd-threads-in-open-vswitch-with-dpdk
- "Improve multicore scaling in Open vSwitch DPDK"（2021-11-19，Red Hat Developer）— 佐证阈值/config 变更触发 reassignment、group 按负载最佳平衡分配 — https://developers.redhat.com/articles/2021/11/19/improve-multicore-scaling-open-vswitch-dpdk
- OVS 官方 PMD 文档 — pmd-auto-lb 配置项默认值 — https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/
- RH Bugzilla #1824458 [RFE] ovs-dpdk auto load balance enablement — 证明该特性在 Red Hat OSP 商用产品中启用 — https://bugzilla.redhat.com/show_bug.cgi?id=1824458

## 最终判定
**第 1 档：全字面命中**

判定依据（1-3句）：Red Hat OSP OVS-DPDK 的 pmd-auto-lb（PMD 自动负载均衡）特性逐项字面对应权 1 的 F1-F4——检测各 PMD 线程/RxQ 负载（F1）、按 load-threshold 持续 1 分钟 + rebal-interval 时间窗 + 负载方差可改善判断触发（F2）、将高负载 RxQ 重新分配到不同 PMD 线程（F3）、PMD 线程 1:1 绑核且每线程轮询多端口多 RxQ（F4，并正中权 17 的 K 线程↔K CPU 一一对应限定）。证据均出自 Red Hat 官方一手资料、时间（2021）远晚于专利公开日（2015-08-12），无任何反向证据。NFV/数据中心 vSwitch 多核转发场景与专利背景技术高度吻合。

## 升级路径（第3-4档填）
（不适用 — 已落第 1 档，证据充分。如需诉讼级取证，可进一步抓取 OVS 源码 lib/dpif-netdev.c 中 pmd_rebalance_dry_run / sched_numa_list_variance 实现 verbatim 以坐实算法等同。）

## 总结一句话
Red Hat OSP OVS-DPDK 的 pmd-auto-lb 特性逐项字面对应 F1-F4（含权 17 的 PMD 绑核一一对应），一手官方资料且时间合规、无反向证据，落第 1 档（全字面命中）。
