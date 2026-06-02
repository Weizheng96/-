# 01-tech-ovs-dpdk-pmd-autolb verdict

## 候选基本信息
- 名称：Open vSwitch OVS-DPDK `pmd-auto-lb`（RxQ-to-PMD 动态再分配）
- 组织：Open vSwitch 社区 / Linux Foundation
- 类型：技术
- 初判命中 F#：F1,F2,F3,F4
- 专利公开（授权）日：2015-08-12

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（检测转发线程状态属性） | 字面命中 | "When PMD Auto Load Balance is enabled, a PMD core's CPU utilization percentage is measured." | https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/ | PMD 线程=转发处理线程；周期性测量各 PMD 的 CPU 利用率，即检测 K 个转发线程的状态属性（对应权 2 "剩余转发资源额度/占比"类属性） |
| F2（满足预设调整触发条件） | 字面命中 | "The PMD is considered above the threshold if that percentage utilization is greater than the load threshold every 10 secs for 1 minute." / "If any numa's estimated dry-run variance is improved from the current one by the variance improvement threshold, a new Rx queue to PMD assignment will be performed."（默认 25%） | https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/ | load threshold + variance improvement threshold(25%) + rebal-interval(1 min) 即"预设调整触发条件"；对应权 3 "K 线程间负载均衡度低于预设" |
| F3（调整至少 1 个线程所服务的交换端口） | 字面命中 | "a new Rx queue to PMD assignment will be performed" / "The reassignment code will assign the largest loaded Rx queues to different PMD threads." | https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/ ; https://developers.redhat.com/blog/2021/04/29/automatic-load-balancing-for-pmd-threads-in-open-vswitch-with-dpdk | RxQ(交换端口队列)运行时重新分配到不同 PMD 线程=调整转发线程所服务的交换端口；运行时动态再分配，与专利批判的"运行前固定绑定"对立 |
| F4（K 为正整数，多线程多端口） | 字面命中 | "a _PMD thread_ ... runs 1:1 on a dedicated core to continually poll ports" / "Each PMD thread is assigned a group of Rx queues" / 前置条件："two or more non-isolated PMDs present and at least one non-isolated PMD is polling more than one Rx queue" | https://developers.redhat.com/blog/2021/04/29/automatic-load-balancing-for-pmd-threads-in-open-vswitch-with-dpdk ; https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/ | PMD 1:1 绑核（线程↔CPU 一一对应，命中权 17）；特性前置条件即 ≥2 个 PMD、≥1 个轮询多 RxQ → K≥2 多核多端口形态被文档明示，非外推 |

## 已检查文档清单
- Open vSwitch 官方文档 PMD Threads 章节：verbatim 给出 utilization 测量、load threshold（10s×6=1min）、variance improvement threshold（默认 25%）、dry-run、RxQ→PMD 重分配、PMD 绑核 isolated 机制 — https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/
- Red Hat Developer 官方技术博客（主维护者 Red Hat，发布 2021-04-29，更新 2024-02-05）："runs periodically"、prerequisites（PMD busy + variance 可改善）、reassignment 把最重负载 RxQ 分到不同 PMD — https://developers.redhat.com/blog/2021/04/29/automatic-load-balancing-for-pmd-threads-in-open-vswitch-with-dpdk

## 最终判定
**第 1 档：确认侵权（高）— F1-F4 全字面命中**
五档定义：第1档=确认侵权(高)F全字面命中；第2档=确认侵权(中)全命中含≥1等同；第3档=公开资料不足(强候选)≥60%F命中且无反向；第4档=公开资料不足(弱候选)<60%；第5档=已排除(仅当有真反向证据/全部证据早于公开日/架构层级不同)。
**0命中≠已排除**；无正向也无反向证据→第3或4档，不是第5档。
判定依据（1-3句）：OVS-DPDK 的 `pmd-auto-lb` 特性在同一抽象层（宿主机虚拟交换机数据面多核转发）上逐字实现了 F1（周期性测量各 PMD 线程 CPU 利用率=检测 K 个转发处理线程的状态属性）、F2（load threshold + variance improvement threshold 25% + dry-run + rebal-interval=预设调整触发条件）、F3（运行时把 RxQ 重新分配到不同 PMD 线程=调整转发线程所服务的交换端口）、F4（PMD 1:1 绑核、前置条件 ≥2 个 PMD 且 ≥1 个轮询多 RxQ=K≥2 多核多端口，含权 17 线程↔CPU 一一对应）。四特征均有一手官方文档 verbatim 支撑，无任何反向证据，材料发布日（2021/2024）远晚于专利公开日 2015-08-12。

## 升级路径（仅落第3-4档时填）
- （不适用，已落第 1 档）

## 总结一句话
OVS-DPDK `pmd-auto-lb` 由官方文档与主维护者博客 verbatim 证实 F1-F4 全字面命中、时间窗合规、无反向证据，落第 1 档（确认侵权-高），但本结论仅为技术档位，不构成法律侵权认定。
