# 03-intel-ipu-ipdk verdict

## 候选基本信息
- 名称：Intel IPU（Mount Evans / E2000）+ IPDK / OVS-DPDK
- 组织：Intel
- 类型：产品
- 初判命中 F#：F1,F2,F3,F4
- 专利公开日：2015-08-12

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（检测 K 个转发线程状态属性） | 字面 | "current measured usage history of PMD core cycles for each Rx queue"；"a thread that runs 1:1 on a dedicated core to continually poll ports for packets" | https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/ | OVS-DPDK 每 PMD 线程 1:1 绑核（=K 线程对应 K CPU，对应权 17）；pmd-rxq-show 持续测量每 PMD 的 core cycles 利用率=检测转发线程状态属性（剩余转发资源额度/占比）。 |
| F2（满足预设调整触发条件） | 字面 | pmd-auto-lb 触发：utilization "is greater than the load threshold every 10 secs for 1 minute"；阈值 `pmd-auto-lb-load-threshold`（默认 95%）+ `pmd-auto-lb-improvement-threshold`（默认 25%） | https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/ ；https://developers.redhat.com/blog/2021/04/29/automatic-load-balancing-for-pmd-threads-in-open-vswitch-with-dpdk | 把测得利用率与预设阈值比较作为再分配判据=权 3/11"负载均衡度低于预设"触发条件，字面对应。 |
| F3（调整≥1 线程所服务的交换端口） | 字面 | "dynamically detects imbalance in how workload is spread across PMDs and can trigger an RxQ-to-PMD reassignment"；手动 `ovs-appctl dpif-netdev/pmd-rxq-rebalance` | https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/ | 运行时把 rxq（交换端口队列）从一个 PMD 线程迁移到另一个=调整转发线程所服务的交换端口；动态再分配 vs 业务前固定绑定，正中本专利发明点。 |
| F4（K 为正整数，多线程多端口，线程↔CPU 一一对应） | 字面 | "a thread that runs 1:1 on a dedicated core"；`pmd-cpu-mask` 指定多核；rxq 在多个 PMD 间均衡 | https://developers.redhat.com/blog/2021/04/29/automatic-load-balancing-for-pmd-threads-in-open-vswitch-with-dpdk | 多 PMD 线程、每线程绑一专用 CPU、服务多个 rxq/端口，与权 17"K 线程与 K 处理器一一对应"字面一致。 |

## 已检查文档清单
- OVS 官方 PMD Threads 文档：PMD 1:1 绑核、pmd-rxq-show 测量、pmd-auto-lb 触发阈值（95%/10s/1min）、rxq 自动/手动再分配（pmd-rxq-rebalance）、pmd-rxq-assign 算法（cycles/group/roundrobin） — https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/
- Red Hat 博客：PMD auto load balance 检测忙碌 PMD + 方差改善判据、三阈值参数、dry-run 后把最大负载 rxq 分到不同 PMD、PMD 1:1 绑核 — https://developers.redhat.com/blog/2021/04/29/automatic-load-balancing-for-pmd-threads-in-open-vswitch-with-dpdk
- IPDK Infrastructure Networking recipe：IPDK 在 IPU 上用 P4-OVS 作基础设施数据面，P4-DPDK 软件 target 基于 DPDK PMD on CPU cores（亦可硬件 offload，运行时选择） — https://ipdk.io/documentation/Recipes/InfrastructureNetworking/

## 最终判定
**第 2 档：全命中含等同（数据面层面字面命中；产品集成层面 1 等同）**

判定依据（1-3句）：本专利发明核心（vSwitch 多核转发中"检测 PMD 线程状态→满足预设阈值→运行时把交换端口/rxq 在线程间动态再分配"，对立于业务前固定绑定）与 OVS-DPDK 的 pmd-auto-lb 特性 F1-F4 全部字面命中，且 OVS-DPDK 正是 Intel IPU/IPDK 基础设施网络（P4-OVS / netdev datapath）的数据面，IPDK 软件转发路径运行 DPDK PMD on CPU cores。唯一未坐实的链节是"IPU 部署里 pmd-auto-lb 这一软件多 PMD 再分配是否被实际启用"——IPDK 同时支持把数据面 offload 到 IPU ASIC 硬件 pipeline，硬件路径下无软件多 PMD 再分配，此处按"软件 PMD 数据面成立、产品默认配置待坐实"记为 1 处等同/待证而非反向（无任何明示排除证据），故落第 2 档而非第 1 档。

## 升级路径（第3-4档填）
- （本候选落第 2 档，可选补强）抓取 IPDK 网络容器实际 ovsdb 默认配置 / Mount Evans 部署文档，确认 `other_config:pmd-auto-lb="true"` 在 IPU 基础设施数据面被默认/可启用，且该路径为软件 PMD（非纯 ASIC offload）——以把数据面字面命中升级为产品级字面命中。

## 总结一句话
Intel IPU/IPDK 基础设施数据面基于 OVS-DPDK，其 pmd-auto-lb 特性对本专利"检测 PMD 负载→超阈值触发→rxq 在多绑核 PMD 间动态再分配"F1-F4 字面命中，仅产品默认是否启用软件 PMD 再分配待坐实，落第 2 档。
