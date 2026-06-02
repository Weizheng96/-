# 证据索引 — 13-dayu-paratus-dpu

## Phase 1 — react 粗筛（4 条 WebSearch，串行）
- query 1: `大禹智芯 Paratus DPU 流表卸载 OVS 多网卡 LACP` → 命中相关：确认 Paratus 2.0 做 OVS 全卸载（ARM SoC+FPGA），但无多网卡/LACP/HA 细节。
- query 2: `大禹智芯 DPU 双网卡 跨网卡 链路聚合 LACP bond 单点故障 流表 高可用` → 仅返回通用 Linux/DPDK bond LACP 教程，**无 vendor 专属的跨网卡聚合/流表 HA 信号**。
- query 3: `大禹智芯 专利 流表 网卡 卸载 patents.google.com Dayu DPU flow table offload` → 检出 Dayu 专利 CN116521596A（PCIe Switch 模拟器，主题不同）；未检出跨网卡 LACP 流表 HA 同主题专利。
- query 4: `大禹智芯 Paratus OVS 卸载 网络高可用 主备 冗余 智能网卡 白皮书 架构` → 仅返回通用智能网卡 OVS 卸载/网络冗余文章，无 vendor 专属白皮书定位本机制。

## Phase 2 — react 深抓（3 条 WebFetch，串行）
- WebFetch https://cloud.tencent.com/developer/news/937365 （Paratus 2.0 发布稿）→ verbatim 仅"OVS全卸载/存储客户端全卸载/NVMe模拟"；网卡数量/LACP/HA/流表多卡下发 **均未提及**。
- WebFetch https://mp.ofweek.com/cloud/a256714210447 （3 周年文）→ 仅"无感知端到端网络数据加密……保证数据网络传输可靠性"；OVS 卸载/多网卡/LACP/流表多卡下发 **均未提及**。
- WebFetch https://patents.google.com/?assignee=大禹智芯&country=CN → **SPA 空壳**（仅返回 "Google Patents" header，无专利数据）。转 WebSearch 替代。
  - 替代 WebSearch: `北京大禹智芯科技 发明专利 流表 网卡 链路聚合 高可用 site:patents.google.com` → 返回的链路聚合专利（CN104488238A / CN1571354A / CN103618678A 等）**均非 Dayu 申请人**，与本候选无关。

## 证据索引表

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2022-10 | 媒体发布稿 | https://cloud.tencent.com/developer/news/937365 | Paratus 2.0：OVS 全卸载/存储客户端全卸载/NVMe 模拟；无多网卡/LACP/HA 细节 |
| 2 | 2023 | 媒体文章 | https://mp.ofweek.com/cloud/a256714210447 | 3 周年 DPU 云网络底座；仅端到端加密"传输可靠性"；无 vSwitch/多网卡/LACP/流表多卡 |
| 3 | — | 官网 | https://www.dayudpu.com/ | 公司定位 DPU 云网络卸载（FPGA→ASIC）；公开度低 |
| 4 | 2023 | 专利 | https://patentimages.storage.googleapis.com/15/00/6a/b2f8eef5dcede5/CN116521596A.pdf | Dayu 专利 CN116521596A：PCIe Switch 模拟器（主题不同，非本机制） |

## 工具受限说明
- Google Patents assignee 检索页为 SPA，WebFetch 取不到专利列表（仅 header）。已用 WebSearch 兜底，未发现 Dayu 申请人的跨网卡 LACP 流表 HA 同主题专利。
- 大禹智芯公开度低（无在线技术白皮书/datasheet 全文直链），核心区分 F# 无法从公开材料核实。

## 结论
未检索到任何针对 Paratus DPU 的反向证据，也未检索到证明其满足"N≥2 独立网卡跨卡 LACP 聚合 + 流表向全部网卡冗余下发"的正向证据。落第 4 档（公开资料不足-弱候选）。
