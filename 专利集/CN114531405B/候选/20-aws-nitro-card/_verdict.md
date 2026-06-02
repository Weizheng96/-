# 20-aws-nitro-card verdict

## 候选基本信息
- 名称：Nitro Card 网络卸载
- 组织：AWS
- 类型：产品
- 初判命中 F#：F1,F2,F4,F5
- 专利公开（授权）日：2023-06-06

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（虚拟交换机 + M VM + N≥2 网卡） | 反向证据 | "There are two Nitro Cards, 1x primary and 1x networking."（网络面仅 1 块 networking 卡，N=1 网络卡，不满足 N≥2 独立网卡） | https://dev.to/choonho/nitro-card-why-aws-is-best-46ph | Nitro 实例网络面仅 1 块 networking 卡；另一块为 primary/storage，非第二块网络卡。不构成"虚拟交换机连接 N≥2 网卡" |
| F2（N 逻辑端口聚合为第一端口的端口标识映射） | 反向证据 | "AWS Nitro Server does not make bonding interface."（不做 bond/聚合，故无"将 N 个逻辑端口聚合为第一端口"） | https://dev.to/choonho/nitro-card-why-aws-is-best-46ph | 无跨卡端口聚合，故无 N→1 端口标识映射 |
| F3（每网卡逻辑端口由其物理端口经 LACP 聚合形成） | 反向证据 | "Commodity server usually make bonding interface coupling two physical interfaces to single logical interface. But AWS Nitro Server does not make bonding interface." | https://dev.to/choonho/nitro-card-why-aws-is-best-46ph | vendor 明示拒绝 bonding/链路聚合，与 F3 的 LACP 聚合形成逻辑端口正相反 |
| F4（目标网卡流表 miss 触发卸载） | 公开资料不足 | Nitro Card for VPC 做流表/数据面卸载（封装、Security Group、路由），但未见 first-packet miss → exact flow 下发的公开机制描述 | https://docs.aws.amazon.com/whitepapers/latest/security-design-of-aws-nitro-system/the-components-of-the-nitro-system.html | 闭源，无一手实现细节；不影响总判（F1/F3/F5 已反向） |
| F5（经第一端口将精确流表卸载至全部 N 个网卡） | 反向证据 | "no redundancy for Nitro Card failure"（Nitro 卡故障无冗余，即不向多卡冗余下发以消除单点故障） | https://dev.to/choonho/nitro-card-why-aws-is-best-46ph | F5 核心是"流表向全部 N 卡冗余下发以消除单网卡单点故障"；AWS 明示 Nitro 卡故障无冗余、不做 bonding，正相反 |

## 已检查文档清单
- AWS 官方白皮书《The components of the Nitro System》—— Nitro Card for VPC 承担 VPC 数据面卸载（封装/解封装、Security Group、路由），未提跨卡 LACP 聚合或流表冗余下发 — https://docs.aws.amazon.com/whitepapers/latest/security-design-of-aws-nitro-system/the-components-of-the-nitro-system.html
- DEV Community《Nitro Card, Why AWS is best!》(choonho, 2024-06-28) —— 明确：Nitro 卡故障无冗余、不做 bonding 接口、网络面仅 1 块 networking 卡（关键反向证据）— https://dev.to/choonho/nitro-card-why-aws-is-best-46ph

## 最终判定

**第 5 档：已排除**

五档：第1档=确认侵权(高)F1-Fk全字面命中；第2档=确认侵权(中)全命中含≥1等同；第3档=公开资料不足(强候选)≥60%F#命中且剩余无反向；第4档=公开资料不足(弱候选)<60%命中；第5档=已排除（仅当(a)≥1条F#真反向证据，或(b)全部证据<2023-06-06，或(c)架构层级不同）。
**第5档硬门槛**：必须是针对该候选产品的正向事实（正向否定/正向不同机制/自有文档自有专利写明用另一套手段）；行业通用机制反推、"同类一般这样"、"公开资料未提及"一律不算反向，只算公开资料不足。同抽象层但缺某 F# 正向证据又无反向事实→第4档，不得第5档。**0 命中≠已排除**。

判定依据（1-3 句，基于上表 F# 分布）：针对 AWS Nitro 的公开材料给出**多条正向反向事实**——"AWS Nitro Server does not make bonding interface"（明示拒绝链路聚合，反 F2/F3）、"no redundancy for Nitro Card failure"（卡故障无冗余，反 F5 的跨卡冗余下发本意）、网络面仅 1 块 networking 卡（反 F1 的 N≥2 独立网卡）。本专利核心区分点（跨 N≥2 独立网卡 LACP 聚合 + 流表向全部卡冗余下发以消除单点故障）被 AWS 架构正向否定，满足第5档硬门槛 (a)。

## 升级路径（仅落第3-4档时填）
（不适用 — 已落第5档，存在针对候选产品的正向反向事实）

## 总结一句话
候选 20-aws-nitro-card 落第 5 档（已排除）：AWS Nitro 公开材料正向写明"不做 bonding/聚合""卡故障无冗余""网络面仅 1 块网卡"，与本专利"跨 N≥2 网卡 LACP 聚合 + 流表向全部卡冗余下发"核心区分点正相反，构成真反向证据。
