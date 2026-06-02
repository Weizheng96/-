# 14-yusi-stargate-dpu 检索留痕（_sources.md）

候选：益思芯 Yusi/Resnics Stargate 系列 DPU（千万级流表、OVS/vSwitch 加速）
专利公开（授权）日：2023-06-06

## Phase 1 — react 模式粗筛 query 留痕

- query 1: `益思芯 Yusi Stargate DPU 流表 OVS 卸载 LACP 多网卡`
  → 命中相关。确认 Stargate-F1000-SN 智能网卡支持基于 P4 动态可编程的 vSwitch（OVS）加速、流表卸载；但无"跨多网卡 LACP 聚合 / 流表向全部网卡冗余下发"信号。
- query 2: `益思芯 Resnics Stargate 智能网卡 双网卡 链路聚合 LACP bond 高可用 冗余`
  → 命中相关。Stargate-F1000-SN = **单卡** 2×100G（可改 2×25G）以太网接口。LACP/bond 命中均为通用资料（Linux bond、华为交换机、DPDK-VPP），非 Yusi 自有文档描述"跨多块独立网卡"。
- query 3: `益思芯 Resnics DPU 流表 卸载 专利 跨网卡 全部网卡 下发 单点故障`
  → 全为公司动态/融资/产品新闻，无任何"跨网卡流表冗余下发 / 消除单网卡单点故障"机制描述。未检索到 Yusi 自有同主题专利。
- query 4: `益思芯 Resnics OVS 流表 卸载 first packet miss upcall 慢路径 精确流表 vSwitch P4`
  → 命中均为 OVS 社区通用 upcall/miss 机制资料（CSDN/ovs-dev/博客园），非 Yusi 自有文档；无法将 F4 miss 触发语义具体绑定到 Stargate。

## Phase 2 — 深抓

- WebFetch `http://www.resnics.com/product/netcard` → 失败（unknown certificate verification error）。
- 兜底 curl（浏览器 UA）成功：`netcard.html`（9605 字节，非 SPA 壳，含完整规格表）。
  - verbatim 规格：网络接口 = **2 x QSFP28 100G以太网接口**（单卡双端口）；主机接口 = PCIE Gen3 x16；网络加速 = 基于 P4 可编程的 vSwitch 加速引擎；虚拟化 = 多 PF/多 VF/多队列。
  - 结论：官方 datasheet 仅描述**单卡形态**（单卡 2 端口），未公开"N≥2 块独立网卡 + 跨卡 LACP 聚合 + 流表向全部网卡冗余下发"拓扑。

## 工具受限说明
- WebFetch 对 resnics.com 证书校验失败，已用 curl -k 兜底成功，证据可用。
- 未检索到益思芯/Resnics 在 2023-06-06 之后申请的同主题（跨网卡流表冗余）公开专利。

## 已下载本地材料
- `netcard.html` — Resnics 智能网卡产品规格页（单卡 2×100G，P4 vSwitch 加速）
