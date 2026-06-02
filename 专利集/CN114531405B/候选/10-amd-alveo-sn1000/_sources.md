# 证据索引 — 10-amd-alveo-sn1000

专利公开（授权）日：2023-06-06

## Phase 1 — react 粗筛 query

- query 1: `AMD Xilinx Alveo SN1000 SmartNIC OVS offload LACP multiple NICs link aggregation`
  → 命中相关：SN1000 支持 OVS 数据面卸载（MAE/tc-flower/rte_flow）；通用 OVS LACP 描述为**单卡内**动态链路聚合；未见"跨多块独立网卡聚合"。
- query 2: `Alveo SN1000 OVS flow offload upcall exact-match flow table multiple cards redundancy single point failure`
  → 命中：MAE 处理 OVS 收发流水线；OVS 社区有 exact-match offload 特性（运行时开关）。**多卡部署 / 跨卡冗余 / 单点故障 / 跨分布式流表 upcall：搜索结果明确表示未覆盖**。
- query 3（规格确认）: `AMD Alveo SN1000 "two 100" port QSFP28 single card dual port specification`
  → 确认：SN1000 = **单块卡，2×QSFP28（双 100Gb 端口）**，FHHL PCIe，XCU26 FPGA + 16 核 Arm。两个端口在**同一块卡**上。

## Phase 2 — 深抓

- WebFetch `xilinx-alveo-sn1000-technical-brief.pdf` → 返回二进制（PDF 已落盘），改用 pdfplumber 本地解析。
  本地解析结果：全文（Technical Overview）**完全未出现** lacp / aggregation / bond / redundancy / single point / failover 任一关键词。
  正文将 SN1000 描述为单块 composable SmartNIC，OVS 功能由收发流水线的 Match Action Engine (MAE) 处理，面向单卡内 VM/容器流量；P4 可编程流水线。**无任何跨卡链路聚合 / 多卡高可用 / 流表向多卡冗余下发的描述**。
  落盘路径：`...tool-results\webfetch-1780316890546-0o8x27.pdf`

## 工具受限说明
- 无付费墙 / 登录墙阻断；technical brief PDF 经 pdfplumber 成功解析。
- 未检索到 AMD/Xilinx 公开描述"SN1000 跨多块独立网卡 LACP 聚合 + 精确流表向全部网卡冗余下发以消除单点故障"的资料（此为本专利核心区分点）。

## 关键事实小结（用于判定）
- SN1000 是**单块双端口卡**，其 OVS 卸载为单卡 MAE 卸载（含 upcall/exact-match 慢路径语义）——这部分与 F4 同抽象层。
- 本专利 F1/F3/F5 要求 **N≥2 块独立网卡** + **跨卡 LACP 聚合** + **流表向全部 N 块卡冗余下发（消除单网卡单点故障）**。SN1000 公开资料仅描述单卡（N=1）形态，未见跨卡系统级方案。
- 依据"整数下界外推禁令"：vendor 仅描述 N≥2 下界以下（单卡）形态 → 判"公开资料不足"，不外推为字面命中；且 vendor **未明示拒绝**多卡方案 → 不构成反向证据，不得落第5档。
