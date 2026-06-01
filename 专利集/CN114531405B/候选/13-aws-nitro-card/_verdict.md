# 候选 13 — AWS Nitro Card 网络卸载 _verdict

## 候选基本信息
- 类型：产品
- 名称：AWS Nitro Card 网络卸载（Nitro Card for VPC）
- vendor：AWS
- 命中 F#（初判）：F1, F2, F4, F5
- 公开度：低（AWS 自研硬件，技术细节高度封闭，公开资料多为白皮书 / re:Invent 演讲 / 第三方解读）
- 一句话定位：Nitro 系统中承担 VPC 数据面 / 网络卸载的自研 PCIe 卡，做报文封装解封、安全组、路由、流跟踪卸载。
- 专利公开（授权）日：2023-06-06（时间窗：仅 2023-06-06 之后公开的材料计为侵权候选材料）

## 检索粗筛（Phase 1 留痕）
- query1（WebSearch）：`AWS Nitro Card network offload VPC virtual switch flow table` → 命中 Nitro Card for VPC 做网络卸载 + flow tracking + flow-cache 加速（有信号，进 Phase 2）。
- query2（WebSearch）：`AWS Nitro multiple NIC bonding LACP flow table sync offload virtual switch` → **无 AWS 特异信号**，返回的全是通用 Linux/Windows/Nutanix bonding/LACP 资料，与 Nitro 无指代关系。
- query3（WebSearch）：`AWS Nitro Card for VPC architecture single card per server flow cache acceleration redundancy multiple cards` → 命中关键事实"most instances have a single Nitro Card for VPC；some instance types use more than a single card when additional resources are needed"。

## F# 命中表

| F# | 含义 | 判定 | 证据（verbatim） | URL | 备注 |
|----|------|------|------------------|-----|------|
| F1 | 多虚机 + **多网卡 N≥2** 架构 | **未命中 / 资料不足** | "A modern EC2 server is made up of a main system board and **one or more Nitro Cards**" ；"**most instances have a single Nitro Card for VPC**, some AWS instance types use more than a single card when additional resources are needed" | https://docs.aws.amazon.com/whitepapers/latest/security-design-of-aws-nitro-system/the-components-of-the-nitro-system.html ；https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ena-nitro-perf.html | "多张 Nitro 卡"指为扩资源加卡、且默认单卡；卡间互联是管理用内部网络（"connected through an internal network within a server enclosure... private communication channel"），并非"把 N≥2 块**网络接口卡**聚合成一个逻辑端口"的专利语义 |
| F2 | N 个逻辑端口聚合为"第一端口" | **未命中（公开资料无）** | 白皮书 / mvdirona 均无"将多块 NIC 的逻辑端口映射到一目标端口标识、聚合为第一端口"的描述 | https://perspectives.mvdirona.com/2019/02/aws-nitro-system/ | 反向抓取确认："there is no description of LACP bonding, multi-NIC aggregation, flow tables, or cache miss synchronization" |
| F3 | 每网卡逻辑端口由物理端口基于 **LACP** 聚合 | **未命中（公开资料无）** | 检索到的 LACP / bonding 资料均为通用 Linux/Windows/Nutanix 技术，无任何 AWS Nitro 使用 LACP 跨网卡聚合的公开证据 | https://www.loadbalancer.org/blog/what-is-networking-bonding-and-what-might-you-use-it-for/ | AWS 公开材料零 LACP 锚点（ENA 倾向由 Nitro 屏蔽底层、不向租户暴露 LACP） |
| F4 | 卸载流表 miss 作为触发 | **泛化弱命中（非专利特异）** | "The Nitro system uses the **full network flow for new connections** and for packets that aren't eligible for acceleration. **After a flow is established**, the majority of packets... are eligible for acceleration" ；"The Nitro card uses **flow tracking** to maintain state" | https://aws.amazon.com/ec2/nitro/ ；https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ena-nitro-perf.html | 通用 SDN flow-cache（首包慢路径→建表→后续快路径加速）语义，几乎所有硬件卸载方案都有；不能据此外推为专利的"跨多网卡 miss 触发同步"特异机制 |
| F5 | 精确流表跨**全部 N 个网卡**卸载 | **未命中（公开资料无）** | 无任何材料描述"一次 miss 把同一精确流表同步下发到聚合内所有 N 块网卡" | https://docs.aws.amazon.com/whitepapers/latest/security-design-of-aws-nitro-system/the-components-of-the-nitro-system.html | F5 是专利核心创新点（消除单网卡单点故障的关键），AWS 公开资料完全未触及 |

## 已检查文档清单
1. AWS Nitro 官方页 https://aws.amazon.com/ec2/nitro/ （WebSearch 命中，flow-cache 加速语义）
2. Nitro 性能调优文档 https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ena-nitro-perf.html （单卡/多卡说明、flow tracking）
3. Nitro 安全设计白皮书—组件章 https://docs.aws.amazon.com/whitepapers/latest/security-design-of-aws-nitro-system/the-components-of-the-nitro-system.html （WebFetch 全文：多卡=扩资源/管理内网，无 LACP、无跨卡流表同步）
4. mvdirona《AWS Nitro System》 https://perspectives.mvdirona.com/2019/02/aws-nitro-system/ （WebFetch：明确无 LACP bonding / 多网卡聚合 / 跨卡 miss 同步描述）
5. 通用 bonding/LACP 资料（loadbalancer.org / Nutanix 等）— 均与 AWS Nitro 无指代关系，仅说明业界 LACP，不构成 AWS 实现证据

> 受限说明：AWS Nitro 数据面实现高度封闭，公开层面无法取得"卡内 ENA 是否对多物理网络连接做 LACP 链路聚合 + 流表跨卡同步"的正面或硬反向技术细节；未抓取到任何 ≥2023-06-06 的 AWS 官方多卡冗余 / 跨卡流状态同步材料。

## 最终判定

**第 4 档：弱信号 / 公开证据不足（命中 < 60%，但无硬反向证据）**

依据（1-3 句）：5 项核心特征中只有 F4 取得"泛化弱命中"，且属所有硬件卸载方案共有的 flow-cache 语义，不具专利特异性；专利两个创新硬限定 F2（N 逻辑端口聚合第一端口）+ F3（LACP 来源）+ F5（精确流表同步至全部 N 网卡）在 AWS 全部公开材料中**完全无锚点**，F1 的"多卡"指 AWS 为扩资源加卡、默认单卡、卡间互联是管理内网而非 LACP 数据面聚合，与专利"跨多块网卡聚合消除单点故障"语义不一致。因 AWS 技术高度封闭，既无法取得正面命中、也无法取得"明示排斥 / 架构不同"的硬反向证据，故不落第 5 档（已排除），落第 4 档。

## 升级路径（第 4 档专属）
- 抓取 AWS re:Invent 网络深度演讲（"Nitro deep dive"、"VPC data plane" 系列）的 PPT / 转录，确认 Nitro 数据面对多网络连接是做"跨物理网卡链路聚合 + 流表同步"还是仅 SR-IOV 单卡多虚函数。
- 检索 AWS 是否在 EC2 实例上对外暴露 LACP / bond 配置（若坐实"不暴露 LACP、由 Nitro 屏蔽底层"则进一步证否 F3）。
- 若日后 AWS 公开 Nitro 多卡冗余 / 跨卡流状态同步白皮书且时间 ≥2023-06-06，据此重判是否升至 2/3 档。

## 总结（≤120 字）
AWS Nitro Card 仅 F4 取得通用 flow-cache 弱命中，F2/F3/F5 三项专利创新（LACP 聚合第一端口 + 精确流表同步全部 N 网卡）公开资料零锚点，F1"多卡"语义也不符；因技术封闭无正证亦无硬反向证据，落第 4 档。
