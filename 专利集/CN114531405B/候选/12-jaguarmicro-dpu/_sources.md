# 证据索引 — 12-jaguarmicro-dpu

专利公开(授权)日基准：2023-06-06。候选：云豹智能 JaguarMicro DPU SoC / 风驰智能网卡。

## Phase 1 — react 粗筛 query 留痕

- query 1: `云豹智能 JaguarMicro DPU 网络卸载 OVS 流表 智能网卡 架构`
  → 命中相关。确认 JaguarMicro 是做云网络卸载的 DPU 厂商，支持 P4 数据面/控制面编程、SRv6 卸载、层级化可编程 DPU（NP/MP+CPU、FPGA+CPU、单芯片 ASIC）。但无任何"跨多块独立网卡 LACP 聚合 + 流表向全部网卡冗余下发"的描述。来源 https://www.jaguarmicro.com/n4.html , https://news.qq.com/rain/a/20230913A08E2C00

- query 2: `云豹智能 专利 网络接口卡 链路聚合 LACP 流表卸载 单点故障 可靠性`
  → 0 命中（云豹相关）。返回全是 LACP 通用教程（CSDN/华为百科），无云豹自有专利或文档涉及跨卡 LACP 聚合。

- query 3: `JaguarMicro patent flow table offload smart NIC DPU multiple network interface cards LACP reliability`
  → 命中一条疑似 JaguarMicro 流表专利线索 US20250310244A1 "EXTEND HIGH CPS FLOW TABLE MANAGEMENT FROM DPU TO HOST CPU"（Justia 标注，2025-10-02 公开）。经核实（见 Phase 2）其真实受让人为 **Advanced Micro Devices, Inc. (AMD/Pensando)，非 JaguarMicro**——Justia 归属标注有误，机制亦不相关。其余命中为通用 SmartNIC/LACP 专利。

- query 4: `云豹智能 风驰 DPU 智能网卡 双网卡 bond 高可用 链路聚合 多网卡 招股书`
  → 命中云豹 IPO/产品报道，但全是融资/上市进展/产品定位（云霄 400Gbps DPU、风驰 400Gbps 智能网卡、适配裸金属/虚拟机/容器、2024 国内 DPU 市占约 15.3%、落地中国移动/腾讯）。**无招股书正文，无任何跨卡聚合/双网卡冗余/流表冗余下发的技术披露**。来源 https://finance.sina.com.cn/roll/2026-04-08/doc-inhtuqfz6550629.shtml 等

## Phase 2 — 深抓留痕

- WebFetch https://patents.justia.com/patent/20250310244 → HTTP 403。
- curl(浏览器 UA) Google Patents US20250310244A1 → 1103B SPA 壳，无正文。
- curl(浏览器 UA) Justia 同 URL → 5591B Cloudflare "Just a moment" 挑战页，无正文。
- curl Google Patents xhr/query → 1103B SPA 壳。
- PatentsView API → TLS 握手失败 (curl 35)。
- curl(浏览器 UA) FreePatentsOnline https://www.freepatentsonline.com/y2025/0310244.html → 73026B 成功。
  实读结论：受让人 = **Advanced Micro Devices, Inc.**（非 JaguarMicro）。独权 1/10/18 机制为：DPU 把 flow-miss 报文经 DPDK 接口上送 host 的 policy agent → host 选 data processing library → 经 control packet 下发回 DPU 编程 P4 datapath 表，以支撑高 CPS 流表事务。**这是"DPU↔host CPU 流表分层管理"，与本专利"跨多块独立网卡 LACP 聚合 + 流表向全部网卡冗余下发"完全不同层级**；且非云豹专利，仅用于排除误归属，不作为云豹机制证据。

## 工具受限说明
- Justia 全站 Cloudflare 挑战、Google Patents 为 SPA 壳，均无法在本环境直读正文；已用 FreePatentsOnline 兜底成功（但拿到的是 AMD 专利，非云豹）。
- **未检索到云豹智能招股书正文公开来源**，亦未检索到云豹自有的"跨卡 LACP 聚合/流表冗余下发"专利或白皮书。判定基于现有公开资料不足，而非反向证据。
