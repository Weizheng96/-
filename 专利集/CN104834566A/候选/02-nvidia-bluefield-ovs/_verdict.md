# 02-nvidia-bluefield-ovs verdict

## 候选基本信息
- 名称：NVIDIA BlueField DPU + OVS-DOCA / ASAP² / 组织：NVIDIA / 类型：产品 / 初判命中 F#：F1,F2,F3,F4 / 专利公开日：2015-08-12

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（检测 K 个转发线程状态属性） | 等同 | "The load threshold is the percentage of processing cycles one of the PMD threads must consistently be using for one minute before a reassignment can occur." / 每 PMD 线程 1:1 绑专用核 | https://developers.redhat.com/blog/2021/04/29/automatic-load-balancing-for-pmd-threads-in-open-vswitch-with-dpdk | pmd-auto-lb 持续监测各 PMD（转发处理线程）的 processing cycles（负载），即"检测 K 个转发线程状态属性"。BlueField OVS-DPDK 在 ARM 核继承该机制。 |
| F2（满足预设调整触发条件） | 字面 | "If a PMD core is detected to be above the load threshold and the minimum pre-requisites are met, a dry-run ... is performed." + "If any numa's estimated dry-run variance is improved from the current one by the variance threshold, a new Rx queue to PMD assignment will be performed."（默认 load threshold 95%） | https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/ | load-threshold + improvement(variance) threshold 即"预设调整触发条件"；可由用户配置阈值。对应权 3/11 的"K 线程间负载均衡度低于预设"择一命中。 |
| F3（调整≥1 个线程所服务的交换端口） | 字面 | "The reassignment code will assign the largest loaded Rx queues to different PMD threads." | https://developers.redhat.com/blog/2021/04/29/automatic-load-balancing-for-pmd-threads-in-open-vswitch-with-dpdk | 触发后把最重载的 Rx 队列（交换端口的接收队列）重新分配给不同 PMD 线程 = 运行时动态迁移端口↔线程映射，非业务前固定绑定。 |
| F4（K 为正整数，K 线程↔K CPU 多核形态） | 等同 | PMD threads run "1:1 on a dedicated core to continually poll ports for packets" + pmd-cpu-mask 绑核 | https://developers.redhat.com/blog/2021/04/29/automatic-load-balancing-for-pmd-threads-in-open-vswitch-with-dpdk ; https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/ | 多 PMD 线程各 1:1 绑一个 CPU 核（pmd-cpu-mask），K 个线程↔K 个 CPU，命中权 17 的一一对应限定与 F4 的多核形态。 |

## 已检查文档清单
- NVIDIA Virtual Switch on BlueField — 确认 BlueField ARM 核运行 OVS（OVS-Kernel/OVS-DPDK/OVS-DOCA 三模式），"performing all the operations supported by OVS" — https://docs.nvidia.com/doca/sdk/virtual-switch-on-bluefield/index.html
- Red Hat: Automatic load balancing for PMD threads in OVS-DPDK（2021-04-29）— pmd-auto-lb 检测/触发/再分配机制 verbatim — https://developers.redhat.com/blog/2021/04/29/automatic-load-balancing-for-pmd-threads-in-open-vswitch-with-dpdk
- OVS 上游 PMD Threads 文档 — load-threshold / variance threshold / rxq→PMD 分配 / pmd-cpu-mask 绑核 verbatim — https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/

## 最终判定

**第 2 档：全命中含≥1 等同**

判定依据（1-3句）：F2、F3 在 OVS-DPDK 上游 pmd-auto-lb 机制中字面命中（预设阈值触发条件 + 把最重载 Rx 队列再分配给不同 PMD 线程）；F1（以 processing cycles 作为线程状态属性）、F4（K 个 PMD 线程 1:1 绑 K 个 CPU）为等同命中。NVIDIA 官方文档确认 BlueField ARM 核运行的 OVS 支持"OVS 全部操作"，故 OVS-DPDK 软件 PMD 路径继承该机制——抽象层与本专利"K 个转发线程↔交换端口动态再分配"一致（区别于 ASAP²/eSwitch 的纯硬件 flow 卸载）。

## 升级路径（第3-4档填）
- （不适用，已落第 2 档）若需进一步坐实：抓取 NVIDIA DOCA OVS-DPDK 配置文档中显式出现 `pmd-auto-lb`/`pmd-cpu-mask` 配置示例的页面，将"BlueField 上启用 pmd-auto-lb"由"继承上游能力"提升为"官方文档显式示例"。

## 总结一句话
NVIDIA BlueField OVS-DPDK 软件路径继承上游 OVS pmd-auto-lb（按 PMD 负载阈值触发、把最重载 rxq 再分配给不同 PMD 线程、各线程 1:1 绑核），F1-F4 全命中（F2/F3 字面、F1/F4 等同），落第 2 档。
