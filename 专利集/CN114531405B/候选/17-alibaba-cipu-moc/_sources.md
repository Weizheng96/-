# 证据索引 — 17-alibaba-cipu-moc

## Phase 1 — WebSearch（react，串行）
- query 1: `Alibaba CIPU X-Dragon MoC card virtual switch flow table offload SmartNIC architecture`
  → 相关。命中 X-Dragon/CIPU 架构：MoC NIC 承载网络虚拟化软件，vSwitch 卸载到 **单块** MoC 卡（FPGA 加速）。强一手论文线索：Triton SIGCOMM 2024。
- query 2: `Alibaba Triton SIGCOMM 2024 hardware offloading flow table multiple NIC LACP redundancy single point failure`
  → 相关。锁定 Triton 论文（Apsara vSwitch AVS 硬件卸载）。摘要未提 NIC 数量/LACP/冗余细节，需读全文。
- query 3: `阿里云 神龙 MoC 卡 双网卡 链路聚合 LACP 流表 冗余 单点故障 卸载`
  → 相关性偏弱。神龙 1.0/2.0/3.0 均描述为"卸载到 MoC 卡"（单数）；LACP/冗余命中的均为行业通用机制文章，非阿里实际架构。

## Phase 2 — 一手 PDF
- Triton: A Flexible Hardware Offloading Architecture for Accelerating Apsara vSwitch in Alibaba Cloud（SIGCOMM 2024，阿里云）
  - URL: https://yangye-huaizhou.github.io/files/Triton.pdf （= https://dl.acm.org/doi/10.1145/3651890.3672224）
  - WebFetch 解析失败（PDF 编码流不可读）→ 已落地 `triton-sigcomm2024.pdf`，pdfplumber 提取全文 `_triton_text.txt`（76k 字符，14 页）。
  - curl 兜底直链 schannel TLS 握手失败（exit 35）；改用 WebFetch 已缓存的二进制副本 cp 进候选目录。
  - 关键 verbatim：
    - "is implemented on our internally developed SmartNIC. The SmartNIC splits into software (SoC) and hardware (FPGA) components" — 架构单元为**单块自研 SmartNIC**。
    - "If the physical server supports multiple SmartNICs, the bandwidth can be further increased." / "Through the horizontal expansion of multiple SmartNICs, Triton is sufficient to support ~Tbps level bandwidth" — 多 SmartNIC 仅作**带宽横向扩展**，非跨卡 LACP 聚合/流表冗余下发。
    - Fig: "Slow Path / Miss Update / Fast Path"；"FPGA Miss, upcall Action"；"If the packet fails to find the flow entry on the Fast Path, it will undergo [Slow Path]" — first-packet miss → upcall → 下发流表（F4 等同命中）。
    - 比较表 "Link failover: Multi-path"（vs baseline Unsupported）——支持多路径链路 failover，但无 LACP/跨卡端口聚合/流表向全部网卡下发的描述。
  - 全文 grep `LACP|link aggregat|bond|端口标识|logical port|target port` 无命中。

## 工具受限说明
- curl 直接抓取目标域名 TLS 握手失败（schannel exit 35）；最终用 WebFetch 缓存副本落地，PDF 完整可读，不影响判定。
