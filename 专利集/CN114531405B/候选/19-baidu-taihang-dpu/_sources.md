# 证据索引 — 19-baidu-taihang-dpu

候选：百度智能云 太行 DPU 2.0 / 软硬一体可编程网关 ｜ 公开度：低（闭源商用，无开源仓库 / 无公开架构白皮书细节）

## Phase 1 — react 粗筛 query 留痕（串行，4 条）

- query 1: `百度 太行 DPU 流表卸载 多网卡 LACP 链路聚合` → 命中泛化资料（LACP 科普 + 太行 DPU 综述），无"跨多块独立网卡 LACP 聚合 + 流表向全部网卡冗余下发"具体描述。
- query 2: `百度 太行 DPU 专利 流表 网络接口卡 卸载 冗余 单点故障` → 命中太行 DPU 2.0 综述（虚拟化全卸载、200Gbps、5000 万 PPS）+ DPU 科普；未检索到百度自有同主题专利或冗余/单点故障架构细节。
- query 3: `Baidu patent flow table offload multiple network interface cards LACP virtual switch DPU` → Google Patents 命中均为他方（Microsoft/Intel 等），**非百度**；US10419239（LACP teaming）、US11606310（flow processing offload）与百度无关，不可作百度命中证据。
- query 4: `百度 太行 DPU 智能网卡 OVS 流表卸载 跨网卡 高可用 弹性裸金属 技术架构` → 命中 OVS 卸载科普（netdev_offload_dpdk/tc）+ 太行 DPU 综述（虚拟化/网络/存储全卸载、BBC 弹性裸金属），仍无跨网卡 LACP 聚合 + 流表向全部网卡下发的拓扑级描述。

## Phase 2 — 深抓（2 条 WebFetch）

| # | 时间 | 类型 | URL | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2024-10-23（授权日后） | 官方综述 | https://cloud.baidu.com/article/3358950 | 仅"虚拟化软件全部卸载到 DPU""存储/网络 I/O 卸载硬件加速"+带宽/性能指标；**无**多网卡 LACP 跨卡聚合、无流表向全部网卡冗余下发、无单点故障防护架构描述 |
| 2 | 2022-12-28 / 转载 2023-02-09 | 第三方详解 | https://cloud.tencent.com.cn/developer/article/2214380 | 列六大自研引擎（vQPE/BTHv/BOE/BDMA/RDMA/BHQoS）+计算/存储/网络/虚拟化能力，但**无**网卡数量、LACP 聚合、OVS 流表卸载、网络高可用颗粒级细节 |

## 工具受限说明
- 百度太行 DPU 为闭源商用产品，无开源仓库 / 无公开架构白皮书；公开渠道仅营销级综述，缺拓扑级实现细节。
- Google Patents 未检索到百度（百度在线/百度智能云）在 2023-06-06 后申请的同主题（跨网卡 LACP 流表冗余下发）专利可供机制比对。
- 无付费墙/登录墙阻挡；为"公开信息客观不足"，非工具失败。
