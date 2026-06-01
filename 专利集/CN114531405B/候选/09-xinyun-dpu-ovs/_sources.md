# 证据索引 — 09-xinyun-dpu-ovs

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| Q1 | 2026-06 | WebSearch | query=`星云智联 DPU OVS 硬件流表全卸载 VTEP 网卡` | 确认星云智联是真实 DPU/SmartNIC 厂商，主打 OVS 全卸载（控制面+转发面全卸载）；无跨多卡聚合信号 |
| Q2 | 2026-06 | WebSearch | query=`星云智联 DPU 链路聚合 LACP 多网卡 流表 卸载 可靠` | 全部为通用 LACP/bond 教程，无星云智联跨网卡流表同步信号 |
| Q3 | 2026-06 | WebSearch | query=`星云智联 NebulaMatrix DPU 产品 高可靠 跨网卡 冗余 bond 流表同步` | 定位官网产品页（DPU / S1000 / S1400 / S2000 / N1025XS）；摘要无跨网卡冗余/流表同步具体描述 |
| Q4 | 2026-06 | WebSearch | query=`星云智联 DPU 智能网卡 双网卡 高可用 单点故障 OVS bond 主备` | 仅返回通用 OVS bond（active-backup/balance）与双网卡绑定教程，非星云智联专有机制 |
| S1 | 2026-06 | curl→本地 | s1000-body.js（官网 S1000 渲染内容，来自 img.wanwang.xin CDN） | 含 OVS / 流表 / 卸载 / 全卸载 / VXLAN / 转发 / 拥塞控制 / 存储卸载 / 安全；**grep 0 命中：LACP/链路聚合/bond/冗余/单点/多网卡/跨网卡/聚合为** —— 单卡 OVS 全卸载，无跨卡机制 |
| S2 | 2026-06 | curl→本地 | s1400-body.js（官网 S1400 渲染内容） | 仅 1 处命中：以太网标准清单中列 "IEEE 802.3ad LACP"（单卡标准端口聚合，与 RS-FEC 并列）；仍无 跨网卡/多网卡/冗余/单点/流表同步至全部网卡 表述 |
| S3 | 2026-06 | curl→本地 | dpu-body.js（官网 DPU 落地页） | 主要为页面导航/产品系列名（S1000/S1400/S2000），无详细机制规格 |

说明：星云智联官网为 JS 渲染 SPA，WebFetch 无法读取正文（多次返回"仅标题"）；改用 curl 抓取 CDN 的 `*.Body.js` 渲染内容后用 grep 核验。
