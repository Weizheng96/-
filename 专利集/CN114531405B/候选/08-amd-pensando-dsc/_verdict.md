# 08-amd-pensando-dsc verdict

## 候选基本信息
- 名称：Pensando DSC DPU 流表卸载
- 组织：AMD
- 类型：产品
- 初判命中 F#：F1,F2,F4,F5
- 专利公开（授权）日：2023-06-06

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（虚拟交换机+M VM+N 网卡，M,N≥2） | 反向证据 | "Network Ports 2 ports QSFP56"；HA 为 "a pair of DSCs installed either within the same appliance or within different appliances can provide high availability to redirected workloads" | https://www.amd.com/content/dam/amd/en/documents/pensando-technical-docs/product-briefs/pensando-dsc-200-product-brief.pdf | DSC 为单卡（双端口）；HA 靠 SDN Appliance"重定向 + 一对 DSC"实现，是不同机制，非"vSwitch 连接 N≥2 块独立网卡"。无公开资料显示 vSwitch 跨 N≥2 块独立 DSC 卡聚合。整数下界 N≥2 跨独立网卡不成立。 |
| F2（N 逻辑端口聚合为第一端口的端口标识映射） | 公开资料不足 | 未找到 | https://www.amd.com/content/dam/amd/en/documents/pensando-technical-docs/product-briefs/pensando-dsc-200-product-brief.pdf | 公开资料无"N 个网卡逻辑端口标识→一目标端口标识映射聚合为第一端口"的描述；因 F1 跨卡前提不成立，F2 跨卡聚合无从落地。 |
| F3（每网卡逻辑端口由其物理端口经 LACP 聚合形成） | 反向证据 | "Network Ports 2 ports QSFP56" / "2x40/100/200G ... Using Breakout cables: 4x10/25/50/100G" | https://www.amd.com/content/dam/amd/en/documents/pensando-technical-docs/product-briefs/pensando-dsc-200-product-brief.pdf | 单卡双端口，任何链路聚合只能是单卡内多端口（intra-card），不满足"跨多块独立物理网卡的物理端口经 LACP 形成各自逻辑端口再聚合"。单卡内多端口 bond ≠ 跨卡聚合（SKILL 明确区分）。 |
| F4（目标网卡流表 miss 触发） | 等同命中（受限） | "Supports cloud-scale networks with 100k+ flow table entries"；"the software data path component able to install flow/session entries"（SSDK） | https://www.amd.com/content/dam/amd/en/documents/pensando-technical-docs/product-briefs/pensando-dsc-200-product-brief.pdf | DPU 做有状态流表/会话卸载，first-packet miss→慢路径下发 exact flow 是 DPU 通用语义，机制等同；但仅单卡内，且 F1/F3/F5 跨卡前提不成立，故仅记等同信号（受限）。 |
| F5（经第一端口将精确流表卸载至全部 N 个网卡） | 反向证据 | "Network Ports 2 ports QSFP56"（单卡）；HA = "redirected workloads"（重定向而非向全部网卡冗余下发流表） | https://www.amd.com/content/dam/amd/en/documents/pensando-technical-docs/product-briefs/pensando-dsc-200-product-brief.pdf | 单卡架构无"经第一端口把精确流表冗余下发到全部 N≥2 块独立网卡"这一动作；HA 通过 appliance 重定向到备用 DSC 实现，是不同手段（不同机制实现高可用，但流表分发对象/路径与 F5 字面要求不符且无跨卡分发事实）。 |

## 已检查文档清单
- AMD Pensando DSC2-200 Distributed Services Card 官方 Product Brief（2023-06）：单卡 2×QSFP56 端口，Elba P4 DPU，100k+ flow table entries，HA 靠"一对 DSC + SDN Appliance 重定向" — https://www.amd.com/content/dam/amd/en/documents/pensando-technical-docs/product-briefs/pensando-dsc-200-product-brief.pdf

## 最终判定

**第 5 档：已排除**

判定依据（基于上表 F# 分布）：官方文档正向写明 DSC 为单卡双端口（2 ports QSFP56），其链路聚合只能是单卡内多端口（intra-card），不满足 F1/F3 要求的"跨多块独立物理网卡（N≥2）经 LACP 聚合"；高可用通过"一对 DSC + SDN Appliance 重定向"这一不同机制实现，而非 F5 的"经第一端口把精确流表冗余下发至全部 N 块网卡"。F1/F3/F5 均有针对该产品的正向架构事实构成反向证据（单卡形态 + 不同 HA 机制），满足第 5 档硬门槛(a)。F4（流表 miss 慢路径下发）虽机制等同，但限于单卡且失去跨卡前提，不足以支撑命中。

## 总结一句话
候选 08-amd-pensando-dsc 落第 5 档（已排除）：官方文档证实 DSC 为单卡双端口、HA 靠一对 DSC + Appliance 重定向，与本专利"vSwitch 跨 N≥2 块独立网卡 LACP 聚合 + 流表向全部网卡冗余下发"的核心区分点构成反向证据，仅 F4 流表卸载机制等同。
