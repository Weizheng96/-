# 证据索引 — 08-amd-pensando-dsc

## 检索粗筛留痕（Phase 1，react 串行）
- query 1: `AMD Pensando DSC DPU flow table offload LACP multiple NICs failover` → 命中官方 DSC/SSDK 文档；确认 P4 可编程 DPU + 流表卸载（100k+ flow entries），但无"跨多块独立网卡 LACP 聚合 + 流表向全部网卡下发"信号。
- query 2: `AMD Pensando DSC dual port LACP bond link aggregation redundancy single card` → 命中官方 DSC2-200 product brief（2023-06）；指向单卡双端口形态。
- query 3: `Pensando DSC host mode two cards bond LACP across cards uplink redundancy host failover` → 未检索到任何"vSwitch 跨 N≥2 块独立 DSC 卡 LACP 聚合"的官方资料；HA 仅以"a pair of DSCs"在 SDN Appliance 重定向模式下实现。

## 深抓证据（Phase 2）
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2023-06 | 官方 product brief PDF | 本地 dsc-200-product-brief.pdf / https://www.amd.com/content/dam/amd/en/documents/pensando-technical-docs/product-briefs/pensando-dsc-200-product-brief.pdf | 单卡 = "2 ports QSFP56"（单卡双端口）；HA = "a pair of DSCs installed either within the same appliance or within different appliances can provide high availability to redirected workloads"（SDN Appliance 重定向模式，非 vSwitch 跨卡聚合）；"100k+ flow table entries"流表卸载，但单卡。WebFetch 超时→curl 浏览器 UA 兜底成功，pdfplumber 提取。 |

## 工具受限说明
- WebFetch 对该 PDF 超时（>60s），已按兜底规则 curl -A 浏览器 UA 下载本地后用 pdfplumber 解析，无付费/登录墙。
