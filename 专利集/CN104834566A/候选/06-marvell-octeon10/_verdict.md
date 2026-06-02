# 06-marvell-octeon10 verdict

## 候选基本信息
- 名称：Marvell OCTEON 10 DPU 数据面 / 组织：Marvell / 类型：产品 / 初判命中 F#：F1,F2,F3,F4 / 专利公开日：2015-08-12

## 检索粗筛
- react 串行 4 条 WebSearch（见 _sources.md），均有信号：OCTEON 10 DPU SDK 软件栈含 OVS-DPDK / VPP / DPDK PMD；net/cnxk PMD 为 CN9K/CN10K 提供 poll-mode ethdev 驱动并支持多 RxQ + 多 forwarding core；命中 OVS-DPDK "PMD auto load balance" 机制。粗筛通过，进入深抓。

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（检测转发线程状态属性） | 等同 | "A PMD core's CPU utilization percentage is measured." | https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/ | OVS-DPDK 持续测量每个 PMD 线程（绑核）的 CPU 利用率＝权1"检测 K 个转发处理线程的状态属性"。OCTEON 10 跑 OVS-DPDK 时该机制在其 ARM 核上运行。 |
| F2（判断满足预设触发条件） | 等同 | "The PMD is considered above the threshold if that percentage utilization is greater than the load threshold every 10 secs for 1 minute." | https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/ | 用户可配 load threshold＝权1"预设调整触发条件"；超阈即触发，对应从权3"负载均衡度低于预设"分支。 |
| F3（调整≥1线程所服务的交换端口） | 等同 | "If a PMD core is detected to be above the load threshold and the minimum pre-requisites are met, a new Rx queue to PMD assignment will be performed." | https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/ | 运行时 RxQ→PMD 重新分配＝权1"调整转发处理线程所服务的交换端口"（端口队列↔线程映射动态迁移，非运行前固定绑定）。 |
| F4（K 正整数，多线程多核，线程↔CPU 一一对应） | 等同 | "PMD threads on cores where Rx queues are pinned will become isolated by default." + OCTEON 10 "ARM Neoverse N2 8-core" 跑 VPP/OVS-DPDK | https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/ ; https://cloudswit.ch/blogs/vector-packet-processing-marvell-octeon-device/ | PMD 线程绑核（每线程对应一 CPU）＝权17"K 个转发线程与 K 个处理器一一对应"；OCTEON 10 为多核（8-core Neoverse N2）多核形态。 |

## 已检查文档清单
- Marvell OCTEON 10 DPU Platform Product Brief（PDF，2023-10-13）— 纯硬件规格，未涉软件再分配 — https://www.marvell.com/content/dam/marvell/en/public-collateral/embedded-processors/marvell-octeon-10-dpu-platform-product-brief.pdf
- Open vSwitch PMD 文档（PMD auto load balance 机制 verbatim）— https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/
- Asterfusion blog — VPP on Marvell OCTEON（2024-09-29，OCTEON 10 8-core Neoverse N2 跑 VPP 48Gbps）— https://cloudswit.ch/blogs/vector-packet-processing-marvell-octeon-device/
- Marvell Data Processing Units 产品页（"DPDK poll mode and event mode drivers"；"VPP and ODP support on top of DPDK"）— https://www.marvell.com/products/data-processing-units.html
- DPDK cnxk platform/nics guide — 抓取失败（TLS handshake），内容由 DPDK 官方文档检索摘要佐证 net/cnxk PMD + 多 RxQ + 多 forwarding core

## 最终判定
**第 3 档：≥60% F 命中、无反向证据（等同/上游继承）**

判定依据：F1-F4 四项全部以"等同"命中——证据链落在 OCTEON 10 软件数据面所运行的上游 OVS-DPDK "PMD auto load balance" 机制：测 PMD 线程 CPU 利用率（F1）→ load threshold 触发（F2）→ 运行时 RxQ-to-PMD 再分配（F3）→ PMD 绑核、OCTEON 10 八核多核（F4），与权1/权17 发明核心严格对应。但 Marvell 自身公开材料仅证实"支持 OVS-DPDK / VPP / DPDK PMD 在其 ARM 核运行"，未明示在 OCTEON 上启用 pmd-auto-lb 这一线程级动态再分配；命中依赖"运行上游 OVS-DPDK 即继承该特性"的推断，且 OCTEON 另有硬件 rte_flow 卸载这一不同机制并存。无任何反向证据（无"不支持/排除 PMD 再分配"表述），架构层级一致（多核软件 vSwitch 数据面），时间合规（OCTEON 10 资料 2023-2024，晚于 2015-08-12 公开日）。因等同命中但缺 Marvell 侧"启用该机制"的直接文证，落第 3 档而非第 1/2 档。

## 升级路径（第3-4档填）
- 取证 Marvell OCTEON SDK 中 OVS-DPDK 是否默认/可启用 `pmd-auto-lb`（other_config:pmd-auto-lb=true）及 cnxk 平台是否在该路径下运行——查 Marvell OCTEON SDK release notes / GitHub（MarvellEmbeddedProcessors）OVS 移植说明、配置文档。
- 取证 OCTEON 上 OVS-DPDK 是走软件 PMD 数据面还是全硬件 rte_flow 卸载——若为后者（硬件 flow steering），则 F3 机制不同，需重判；区分软件 PMD 线程再分配 vs 硬件 flow 卸载是关键。
- 抓取成功的 DPDK cnxk platform guide（当前 TLS 失败），确认 OCTEON 软件转发是否在 OCTEON 核上以多 PMD 线程承载 RxQ。

## 总结一句话
Marvell OCTEON 10 DPU 软件数据面运行上游 OVS-DPDK，其 PMD auto load balance（测线程负载→阈值触发→RxQ-to-PMD 再分配→绑核）与 CN104834566A 权1/权17 全等同命中，但缺 Marvell 侧"已启用该机制"直接文证、且与硬件 flow 卸载并存，落第 3 档。
