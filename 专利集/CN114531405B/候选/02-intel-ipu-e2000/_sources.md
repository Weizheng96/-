# 证据索引 — 02-intel-ipu-e2000

## Phase 1 — react 模式粗筛（4 WebSearch，串行）

### query1: `Intel IPU E2000 Mount Evans OVS flow offload virtual switch`
命中：确认 E2000（Mount Evans）是 Intel 首款 ASIC IPU，支持 vSwitch/OVS 流表卸载，与 Google Cloud 合作，C3 机型部署。
- https://medium.com/intel-tech/intel-ipu-e2000-a-collaborative-achievement-with-google-cloud-eb1dda8c0177
- https://www.servethehome.com/intel-e2000-is-the-new-intel-mount-evans-dpu-ipu-brand/
- https://www.networkworld.com/article/971040/intel-details-ipu-roadmap-to-free-up-cpus.html

### query2: `Intel IPU E2000 bonding LAG multiple NIC flow table offload LACP link aggregation`
无 E2000 专属命中：仅返回通用 LACP/bonding 文档，无 E2000 跨多块网卡聚合 + 流表向全部网卡卸载的资料。
- https://www.intel.com/content/www/us/en/developer/articles/technical/link-aggregation-configuration-and-usage-in-open-vswitch-with-dpdk.html

### query3: `Intel IPU E2000 architecture single card uplink ports vSwitch offload multiple network interface cards`
关键命中：E2000 是单卡设备，卡上含 two NIC ports + 一个带外管理口；可 headless（独立交换/卸载）或 multi-host 模式。卸载在单卡内部完成。
- https://www.servethehome.com/intel-e2000-is-the-new-intel-mount-evans-dpu-ipu-brand/
- https://www.intel.com/content/www/us/en/products/details/network-io/ipu.html
- https://ieeexplore.ieee.org/document/10067333/

### query4: `"IPU E2000" OR "Mount Evans" cross-card redundancy single point of failure flow table sync multiple SmartNIC failover`
无 E2000 专属反向/正向命中：未检索到 E2000 把"虚拟交换机连接 N≥2 块独立网卡 + LACP 聚合 + miss 时把精确流表同步卸载至全部 N 块网卡"的公开资料。仅有通用 SmartNIC 流表同步学术文献。
- https://www.servethehome.com/intel-e2000-is-the-new-intel-mount-evans-dpu-ipu-brand/
- https://www.datacenterdynamics.com/en/news/intel-and-google-cloud-jointly-launch-data-center-accelerator-chip/

## 工具受限说明
无。4 条 WebSearch 均正常返回。

## 粗筛结论
架构层级不同（早剪枝条件 iii）：E2000 是"单块 IPU 卡内部承担 vSwitch/流表卸载"，属本专利背景技术明示区分的"单一网络接口卡内"卸载方案；公开资料不支持其作为 vSwitch 管理/聚合 N≥2 块**独立网卡**并把精确流表同步下发到**全部**网卡。F2/F5 核心创新点（跨网卡聚合 + 向全部网卡同步卸载）无证据，F1 的 N≥2 块独立网卡架构限定不满足。早剪枝。
