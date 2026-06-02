# 证据索引 — 10-vmware-nsxt-datapath

## Phase 1 — react 粗筛 WebSearch（串行，4 条）
1. `VMware NSX-T Edge enhanced datapath DPDK PMD rxq core load balancing`
   → 命中 Broadcom/VMware Enhanced Data Path 文档；关键句"cores either assigned statically or **on demand**"、Load Balanced Source teaming（NUMA aware）。判定：相关，继续。
2. `NSX-T enhanced data path rx queue assignment poll mode thread rebalance flow cache LPM`
   → ENS 用 DPDK poll-mode driver；pNIC 配 8 Rx queue；fast path + flow cache 五元组校验转发。判定：相关。
3. `NSX-T enhanced datapath ENS load balanced source teaming dynamic rxq reassignment CPU load fast path thread`
   → NUMA-aware 对齐为主；公开文档止步于"初始配置时选定 NUMA / 逻辑核"，未明示按负载运行时再分配。
4. `VMware patent dynamic reassignment receive queue poll mode thread CPU load datapath rebalance`
   → 命中 VMware 自有专利 US11599395（Dynamic core allocation）、US9571426 / US9843540（Traffic and load aware dynamic queue management）；OVS-DPDK PMD auto load balance 作旁证。

## Phase 2 — react 深抓 WebFetch（串行）

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2018-10-30 | VMware 博客 | https://blogs.vmware.com/networkvirtualization/2018/10/accelerated-data-plane-performance-using-enhanced-data-path-in-numa-architecture.html/ | N-VDS(E) 初始按 NUMA 对齐逻辑核/VM/pNIC；**未见**运行时按负载再分配的检测/阈值/触发 → 仅产品文档不足 |
| 2 | 更新 2026-01-21 | Broadcom 产品文档 | https://techdocs.broadcom.com/us/en/vmware-cis/nsx/vmware-nsx/4-0/installation-guide/transport-zones-and-transport-nodes/enhanced-datapath-1.html | Load Balanced Source teaming + NUMA aware（VMXNET3 + High latency sensitivity）；未明示 CPU 负载触发的动态队列再分配 |
| 3 | 2023-08-31 | NVIDIA 文档 | https://docs.nvidia.com/networking/display/VMwareUMv417711/Enhanced+Network+Stack+(ENS) | "NUMA node and amount of logical cores ... selected during the **initial** N-VDS configuration"——初始静态配置 |
| 4 | 申请 2020-02-19 / 授权 2023-03-07 | VMware 自有专利 | https://patents.google.com/patent/US11599395B2/en | **关键证据**：gateway datapath（DPDK，NSX）多核；收集核利用率数据（F1）→ 判定某组核 underutilized（如 <50% 聚合利用率，F2）→ 重新分配核 + 更新负载均衡把数据消息在与核关联的队列间重分发（F3）→ 多核多线程（F4）。链路完整且晚于专利公开日 |
| 5 | — | 旁证（503 未抓取） | https://patents.google.com/patent/US9571426B2/en | US9571426 "Traffic and load aware dynamic queue management"，搜索摘要：动态调整队列分配、在池内把流量从一个队列动态重分配到另一个队列 |

## 备注
- 公开产品文档（EDP / ENS 配置）止步于"DPDK 加速 + NUMA 亲和性 + 初始核分配（含 on demand）"，未直接公开"按转发线程负载自动触发端口/队列再分配"的完整链路 → 单凭产品文档为公开资料不足。
- VMware 自有专利 US11599395B2 补足实现路径：明确"检测核负载 → 阈值条件 → 运行时重分配核并在队列间重分发"——构成 F1-F4 的等同实现强证据。
- 时间合规：所有运行时再分配实现证据（2018 博客之后、2023 专利）均晚于本专利公开日 2015-08-12。
