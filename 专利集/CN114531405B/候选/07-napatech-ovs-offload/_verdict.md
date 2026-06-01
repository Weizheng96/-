# 候选 07 — Napatech 全 OVS 卸载 SmartNIC（FPGA）— 合议结果

## 一、候选基本信息
- slug：07-napatech-ovs-offload
- 类型：产品
- 名称：Napatech 全 OVS 卸载 SmartNIC（FPGA）
- vendor / 组织：Napatech（Oslo 上市）
- 一句话定位：FPGA SmartNIC 全 OVS 卸载（含 VXLAN/VLAN），fast path 完全绕过软件 OVS。
- 命中 F#（初判）：F1, F2, F4, F5
- 专利公开（授权）日时间窗：2023-06-06（仅此后公开材料计入侵权窗；本案判定不依赖时间窗——见下）

## 二、检索粗筛留痕（Phase 1）
- WebSearch #1 `Napatech OVS full offload SmartNIC FPGA flow table VXLAN` → **有信号**：确认 Napatech 提供全 OVS 卸载，OVS 数据面跑在 FPGA、控制面在 SoC，支持 VXLAN/VLAN 卸载，~6x 性能；SmartNIC 内实现 flow table / flow cache，硬件 flow matcher + learning subsystem。
- WebSearch #2 `Napatech OVS offload link aggregation bonding LACP multiple NIC redundancy` → **无 Napatech 专属信号**：仅返回通用 OVS bond/LACP 文档（Red Hat / Intel / Nutanix），无 Napatech 跨多卡卸载内容。
- WebSearch #3 `Napatech SmartNIC multiple cards bonding failover flow table synchronization across NICs` → Napatech 多卡能力仅见于"抓包/分析的多卡时间同步与数据 merge"（daisy-chain 时间戳同步、多 SmartNIC 数据合流），**非** OVS 卸载场景下的跨卡 LACP 冗余；"both flow tables" 指卡内学习用双流表，非 N≥2 独立网卡间复制。

## 三、深抓留痕（Phase 2）
- WebFetch `light-at-the-end-of-the-tunnel-ovs-offload`（2019-02-06）→ OVS 卸载在**单块 SmartNIC** 内完成；**无** LACP / bonding / 跨卡流表复制；verbatim："Packets that can be handled by the SmartNIC fast path never end up in OVS for either ingress or egress."；性能测试用"two servers each running OVS"是两台独立服务器经 VXLAN 隧道互联，**非**单机多网卡聚合。
- WebFetch `virtual-switch-offload-solution`（solution description）→ 仅讲 CPU 减负 / ROI / 性能，未提单卡 vs 多卡、未提 LACP 多卡聚合、未提跨卡流表同步消除单点故障。
- 注：受限——Napatech 公开材料未出现"将精确流表同步卸载至 N≥2 块独立网卡 + LACP 聚合为一逻辑端口"的架构描述；其卸载架构一致地呈现为**单 SmartNIC fast-path 卸载**。

## 四、F# 命中表（F1-F5）
| F# | 判定 | 证据（verbatim / 摘要） | URL | 备注 |
|----|------|------------------------|-----|------|
| F1（多虚机+多网卡 N≥2） | **未命中（架构反向）** | Napatech OVS 卸载在单块 SmartNIC 内完成；"the VirtQueues are no longer handled by OVS but by the SmartNIC's Poll Mode Driver (PMD) directly"；多卡能力仅见于抓包时间同步/数据 merge，非卸载冗余 | https://www.napatech.com/light-at-the-end-of-the-tunnel-ovs-offload/ | 权 1 硬限定 N≥2 跨独立网卡；Napatech 为单卡卸载，公开资料无 N≥2 卸载冗余 |
| F2（N 逻辑端口聚合为"第一端口"） | **未命中** | 无 LACP/bonding 将多块网卡聚合为一逻辑端口的描述 | 同上 + virtual-switch-offload-solution | 单卡架构下不存在跨卡逻辑端口聚合 |
| F3（每卡逻辑端口基于 LACP 形成） | **未命中** | Napatech OVS 卸载文档零 LACP；LACP 仅在通用 OVS 文档出现，与 Napatech 卸载无关 | https://www.napatech.com/support/resources/solution-descriptions/virtual-switch-offload-solution/ | — |
| F4（卸载流表 miss 触发） | **命中** | "each new flow is analyzed by the hardware flow matcher … to determine if it matches a record in the flow table … The learning subsystem updates the … flow tables so that subsequent flows … processed on the SmartNIC"——cache-miss-driven offload 语义一致 | WebSearch #1/#3 摘要（Napatech flow cache / learning subsystem） | 仅此特征命中；属硬件卸载通用机制，非专利核心创新点 |
| F5（精确流表跨全部 N 网卡卸载） | **未命中（架构反向）** | 流表驻留单 SmartNIC；"no mention of synchronizing flow tables across independent cards"；无跨 N≥2 网卡同步复制 | https://www.napatech.com/light-at-the-end-of-the-tunnel-ovs-offload/ | 专利核心创新点（多卡同步卸载消除单点故障）在 Napatech 架构中不存在 |

## 五、已检查文档清单
1. WebSearch：`Napatech OVS full offload SmartNIC FPGA flow table VXLAN`（有信号）
2. WebSearch：`Napatech OVS offload link aggregation bonding LACP multiple NIC redundancy`（无专属信号）
3. WebSearch：`Napatech SmartNIC multiple cards bonding failover flow table synchronization across NICs`（多卡仅限抓包时间同步/数据 merge）
4. WebFetch：https://www.napatech.com/light-at-the-end-of-the-tunnel-ovs-offload/ （2019-02-06，单卡卸载）
5. WebFetch：https://www.napatech.com/support/resources/solution-descriptions/virtual-switch-offload-solution/ （无多卡/LACP/跨卡同步）

## 六、最终判定

**第 4 档：公开资料不足（弱候选）**

> 主 agent 复核更正（原 sub-agent 判第 5 档已排除）：本判定的"反向"依据为"公开材料无跨卡同步的描述"（absence of mention），而非 Napatech 官方对该特征的正向否定。按 SKILL 硬约束"0 命中 ≠ 已排除"——absence ≠ 真反向证据，且 Napatech 与本专利同属 SmartNIC OVS 卸载抽象层（非层级不同）。无产品级正向反证时应判**公开资料不足**而非已排除。

判定依据（1-3 句）：权 1 核心创新 F1/F2/F5（N≥2 块独立网卡经 LACP 聚合为"第一端口" + 精确流表 miss 触发后同步卸载至全部网卡）在 Napatech 公开材料中**0 命中**；其公开材料一致呈现为单 SmartNIC fast-path 卸载，但**未见 Napatech 正向声明"不支持/不做"跨卡同步**——仅是公开资料未覆盖。仅 F4（miss 触发卸载）命中通用语义。故按"单卡只见、不可外推、无真反向证据"落第 4 档（公开资料不足）。

## 七、升级路径
- 取 Napatech Link-Capture / OVS 卸载软件栈官方文档或 SDK，确认其是否支持把多块独立 SmartNIC 经 LACP 聚合并同步流表（FPGA 方案理论上可定制）；
- 或实测双 Napatech SmartNIC bond 配置下流表在两卡的实际分布。

## 八、总结一句话
Napatech 全 OVS 卸载公开材料仅见单 SmartNIC fast-path 卸载、F1/F2/F5 零命中，但无 Napatech 正向否定跨卡同步的反证（仅 absence），**落第 4 档（公开资料不足）**。

---
> 免责声明：本文为侵权线索与证据链梳理，非法律结论，不构成"已构成侵权"之认定。
