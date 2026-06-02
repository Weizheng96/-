# 证据索引 — 04-intel-ipu-e2000

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2022-10-11 | 媒体一手现场 | https://www.servethehome.com/intel-e2000-is-the-new-intel-mount-evans-dpu-ipu-brand/ | verbatim "two NIC ports and an out-of-band management port"；单卡 "Intel Mount Evans IPU Card" — 单 ASIC 单卡架构 |
| 2 | 2022 | 厂商/媒体 | https://medium.com/intel-tech/intel-ipu-e2000-a-collaborative-achievement-with-google-cloud-eb1dda8c0177 | E2000 与 Google Cloud 共同设计，承担 vSwitch offload，200G；单 IPU 设备 |
| 3 | 2023 | 学术(订阅) | https://ieeexplore.ieee.org/document/10067333/ | ISSCC "An In-depth Look at the Intel IPU E2000" — 详尽架构来源，需订阅未抓取 |

## Phase 1 — react 粗筛 query 留痕

- query 1: `Intel IPU E2000 Mount Evans flow table offload LACP bond multiple NIC`
  → 命中相关。要点：E2000（Mount Evans）= Intel 首款 ASIC IPU，200G，与 Google Cloud 共同设计，承担 vSwitch offload / firewall / virtual routing；**单设备含 two NIC ports + 一 OOB 管理口**。无跨卡 LACP / 流表全网卡下发描述。
- query 2: `Intel IPU E2000 vSwitch flow offload exact match table miss upcall single device architecture`
  → 命中通用 OVS exact-match / TC flower / hw-offload 资料，无 E2000 专属的 miss→exact-flow 全网卡下发描述。
- query 3: `Intel IPU E2000 two NIC ports bonding LACP link aggregation redundancy single point failure across multiple IPU cards`
  → 命中通用 LACP 资料 + E2000 产品页。确认：E2000 为**单 ASIC 单卡，含 two NIC ports**；PCIe 子系统可对上游最多 4 台 host 各呈现为独立设备（多 host 连接，非卡内/跨卡端口聚合）。无"多块 E2000 卡跨卡 LACP 聚合 + 流表向全部网卡下发"证据。

## Phase 2 — WebFetch

- WebFetch `https://www.servethehome.com/intel-e2000-is-the-new-intel-mount-evans-dpu-ipu-brand/`（发布 2022-10-11）
  → verbatim: "Here we can see two NIC ports and an out-of-band management port"；描述为单卡 "Intel Mount Evans IPU Card"。未提多卡 LACP / 流表跨网卡复制。

## 工具受限说明
- 无付费墙/登录墙阻断主路径；IEEE Xplore 论文（10067333）为最详尽架构来源但需订阅，未抓取。
- 关键架构事实（单 ASIC 单卡 + two NIC ports）已由 ServeTheHome（一手现场报道，2022-10-11）+ 多条搜索一致佐证。
