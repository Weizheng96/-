# 证据索引 — 02-nvidia-bluefield-ovs

## Phase 1 — react 粗筛（WebSearch）
1. `NVIDIA BlueField DPU OVS-DOCA PMD rxq load balancing` → 命中相关：BlueField 加速 OVS（NFV/SDN），DOCA 含 OVS（OVS-Kernel/OVS-DPDK/OVS-DOCA）。
2. `BlueField OVS-DPDK pmd-auto-lb OR pmd-rxq-assign ARM cores rxq rebalance` → 命中 OVS 上游 pmd-auto-lb / pmd-rxq-assign 机制（rxq→PMD 再分配、rebalance）。
3. `site:docs.nvidia.com BlueField OVS-DPDK hardware offload ASAP2 PMD ARM cores DOCA` → 确认 BlueField 三种 OVS 模式，OVS-DPDK 在 ARM 核上做软件转发；ASAP² 卸载 datapath 到内嵌交换避免每包过 ARM 核。

## Phase 2 — react 深抓（WebFetch）

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 文档(滚动更新) | NVIDIA 官方文档 | https://docs.nvidia.com/doca/sdk/virtual-switch-on-bluefield/index.html | "The virtual switch running on the Arm cores allows us to pass all the traffic ... while performing all the operations supported by OVS." 三模式 OVS-Kernel/OVS-DPDK/OVS-DOCA；`dpdk-init=true` |
| 2 | 2021-04-29 | Red Hat 技术博客 | https://developers.redhat.com/blog/2021/04/29/automatic-load-balancing-for-pmd-threads-in-open-vswitch-with-dpdk | pmd-auto-lb：检测忙 PMD 线程(load threshold 1 分钟持续占用%)；improvement threshold（dry-run 估算方差改善才触发）；"The reassignment code will assign the largest loaded Rx queues to different PMD threads."；每 PMD 线程 1:1 绑定专用核 |
| 3 | 文档(滚动更新) | OVS 上游官方文档 | https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/ | "If a PMD core is detected to be above the load threshold and the minimum pre-requisites are met, a dry-run ... is performed." 默认 load threshold 95%；方差阈值改善后执行新 rxq→PMD 分配；pmd-cpu-mask 绑核 |

## 时间窗
- 专利公开（授权）日 2015-08-12。BlueField DPU + OVS-DOCA/ASAP² 及 OVS pmd-auto-lb（2021）均晚于公开日 → 时间合规。

## 备注：抽象层核验
- BlueField 同时提供硬件 eSwitch 卸载（ASAP²，硬件 flow 卸载，非本专利的多 PMD 线程级再分配）与 OVS-DPDK 软件转发路径（ARM 核上跑 PMD 线程）。
- 本专利 F1-F4 对应的"K 个转发线程↔端口动态再分配"落在 **OVS-DPDK 软件 PMD 路径**（pmd-auto-lb），该路径在 BlueField ARM 核上原生支持（继承上游 OVS 全部操作），抽象层一致。
