# 证据索引 — 03-intel-ipu-ipdk

## Phase 1 — 粗筛 WebSearch（串行）
1. `Intel IPU IPDK OVS-DPDK pmd-auto-lb rxq load balancing` → 强信号：OVS-DPDK pmd-auto-lb 动态检测 PMD 负载不均→触发 RxQ-to-PMD 再分配；IPDK 为 IPU 上基础设施 offload 框架（含 OVS-DPDK）。
2. `Intel IPU infrastructure OVS pmd rxq rebalance IPDK networking recipe` → IPDK 用 P4-OVS 作基础设施数据面，基于 DPDK PMD；pmd-rxq-rebalance / 利用率分配自 OVS 2.9.0。
3. `IPDK networking container OVS-DPDK userspace netdev datapath PMD threads Mount Evans IPU host CPU` → IPDK 基础设施网络用 P4 OVS 管理虚拟端口/数据面；userspace OVS datapath=netdev，DPDK PMD 由 pmd-cpu-mask 绑核；IPDK 24.01 基于 Mount Evans E2100 SDK。

## Phase 2 — 深抓 WebFetch（串行）
- OVS PMD Threads 官方文档 — https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/
  - PMD 1:1 绑核；pmd-rxq-show 记录每 rxq 的 PMD core cycles 历史（1 分钟）；pmd-auto-lb 在 PMD core 利用率连续超 pmd-auto-lb-load-threshold（默认 95%）每 10s 持续 1 分钟时触发；自动/手动（pmd-rxq-rebalance）把 rxq 在 PMD 间再分配。
- Red Hat: Automatic load balancing for PMD threads in OVS-DPDK（2021-04-29）— https://developers.redhat.com/blog/2021/04/29/automatic-load-balancing-for-pmd-threads-in-open-vswitch-with-dpdk
  - 检测 PMD 是否很忙 + 再分配后方差是否改善；三阈值 load-threshold(95%)/improvement-threshold(25%)/rebal-interval(1min)；dry-run 估算后把最大负载 rxq 分到不同 PMD；PMD = 1:1 绑专用核，pmd-cpu-mask 指定。
- IPDK Infrastructure Networking recipe — https://ipdk.io/documentation/Recipes/InfrastructureNetworking/
  - P4 OVS 生成 P4 pipeline 实现数据面；P4-DPDK 软件 target（DPDK PMD on CPU cores）与硬件 offload（Mount Evans/Oak Springs Canyon IPU 等）均可，运行时经 Target Abstraction Interface 选择。

## 抓取失败
- Intel OVS-DPDK 调优指南（intel.com）WebFetch=403、curl 同样 Access Denied 阻断页 → 已删除占位文件。
