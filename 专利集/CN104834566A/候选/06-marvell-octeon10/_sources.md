# 证据索引 — 06-marvell-octeon10

## Phase 1 — react 粗筛 WebSearch（串行，4 条）
1. `Marvell OCTEON 10 DPU OVS-DPDK OR VPP vSwitch dataplane rxq PMD`
   → 相关。OCTEON 10 DPU SDK 软件栈含 vSwitch / DPDK / VPP；提供 net/cnxk PMD；Asterfusion 基于 OCTEON 跑 VPP。
2. `OCTEON 10 DPU OVS pmd-auto-lb load balancing forwarding core rxq reassignment`
   → 相关。命中 OVS-DPDK "PMD auto load balance" 机制（检测 PMD 负载不均 → 触发 RxQ-to-PMD 再分配）。
3. `Marvell OCTEON 10 OVS-DPDK software vSwitch dataplane PMD core hardware flow offload`
   → 相关。确认 OCTEON SDK 含 OVS-DPDK；同时存在硬件 rte_flow 卸载路径（不同机制，需区分）。
4. `Marvell OCTEON cnxk DPDK ethdev RxQ multiple queues forwarding cores OVS-DPDK net/cnxk PMD`
   → 相关。net/cnxk PMD 为 CN9K/CN10K 内置网卡提供 poll-mode ethdev 驱动；支持多 RxQ + 多 forwarding core。

## Phase 2 — react 深抓 WebFetch（串行）

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2023-10-13（PDF创建） | Marvell 产品简介 | https://www.marvell.com/content/dam/marvell/en/public-collateral/embedded-processors/marvell-octeon-10-dpu-platform-product-brief.pdf | 纯硬件规格；未提 OVS/VPP/PMD/线程再分配 |
| 2 | latest 文档 | OVS 官方文档 | https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/ | PMD auto load balance 机制 verbatim：测 PMD CPU 利用率→阈值触发→RxQ-to-PMD 再分配→PMD 绑核 |
| 3 | 2024-09-29 | 第三方 blog | https://cloudswit.ch/blogs/vector-packet-processing-marvell-octeon-device/ | OCTEON 10 ARM Neoverse N2 8-core 跑 VPP，48Gbps；无线程级再分配细节 |
| 4 | 产品页 | Marvell 产品页 | https://www.marvell.com/products/data-processing-units.html | "Support for DPDK poll mode and event mode drivers"；"VPP and ODP support on top of DPDK" |

## 抓取失败
- DPDK cnxk platform guide（https://doc.dpdk.org/guides-24.03/platform/cnxk.html）
  → WebFetch "unknown certificate verification error"；curl 兜底 schannel SSL/TLS handshake 失败（exit 35）。
  内容已由 Phase 1 query 4 的 DPDK 官方文档摘要佐证（net/cnxk PMD + 多 RxQ + 多 forwarding core）。
