# 证据索引 — 06-xinyun-dpu-ovs

## Phase 1 — react WebSearch (4 条)
- query 1: `星云智联 DPU OVS 硬件流表全卸载 网卡 架构`
  → 命中 vendor 官网 nebula-matrix.com + 多篇 DPU OVS 全卸载科普；信号：星云 DPU 确做 "OVS 硬件流表全卸载、数据面硬件流表操作"。但科普描述的是**通用单网卡 OVS 全卸载**（netdev_offload_dpdk / netdev_offload_tc），未涉及跨多卡 LACP + 流表向全部网卡冗余下发。
- query 2: `星云智联 DPU 跨网卡 LACP 链路聚合 流表 冗余 双网卡 可靠性`
  → 0 个 vendor 命中；全部为通用 LACP 协议科普（华为/思科/阿里云）。无星云"跨网卡聚合+流表冗余"信号。
- query 3: `星云智联 Nebula Matrix DPU 专利 流表 多网卡 网卡故障 单点`
  → 命中 vendor 公司页 / 36氪 / 产品页（NebulaX D1055AS、S1000 系列）；信息仅"数据面硬件实现流表操作、队列隔离、带宽隔离"，**无多网卡冗余 / 单点故障 / 跨卡 LACP** 细节。
- query 4: `珠海星云智联 patent 流表 网络接口卡 LACP 卸载 site:patents.google.com`
  → 0 个星云专利命中；返回的均为他方 LACP 链路聚合专利。未找到星云自有"跨卡流表卸载"专利做机制比对。

## Phase 2 — WebFetch / curl
- WebFetch https://www.nebula-matrix.com/smartnic → HTTP 404。
- WebFetch https://www.nebula-matrix.com/dpu → 仅返回标题头（SPA 壳），无正文。
- curl (浏览器 UA) https://www.nebula-matrix.com/dpu → HTML 仅 662 字节（JS 渲染 SPA 空壳），无技术正文。
- WebFetch https://www.nebula-matrix.com/newsinfo/3184277.html → 仅返回页面标题（招聘页），无技术正文。

## 工具受限说明
- 星云智联官网为 JS 渲染 SPA，所有页面经 WebFetch / curl 均只得标题头（<1KB），产品技术正文不可静态抓取（无登录墙/付费墙，纯前端渲染）。产品级 OVS 全卸载结论来自第三方科普与公司概览页，**未取得 vendor 一手拓扑文档**确认跨卡 LACP + 流表向全部网卡下发。
