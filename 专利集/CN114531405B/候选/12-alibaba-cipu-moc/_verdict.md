# 候选 12 合议判定 _verdict.md

## 一、候选基本信息
- 编号 / slug：12 / `12-alibaba-cipu-moc`
- 类型：产品
- 名称：阿里云 神龙 MoC 卡 / CIPU 云网络卸载（Apsara vSwitch 硬件卸载 / Triton 架构）
- vendor：阿里云（Alibaba Cloud）
- 公开度：低（多为架构博客 / 云栖大会 PPT / 学术论文，缺乏网卡级实现细节）
- 初判命中 F#：F1, F2, F4, F5
- 涉案专利：CN114531405B「一种流表处理方法及相关设备」（华为），授权公告日 2023-06-06
- 一句话定位：自研云基础设施处理器 / MoC 卡，承担虚拟交换（vSwitch）流表硬件卸载，大规模商用。

## 二、检索粗筛（Phase 1 留痕）
- WebSearch①：`阿里云 神龙 MoC 卡 CIPU 虚拟交换机 流表卸载 网络` → 命中。确认 CIPU/MoC 卡承担「VPC overlay 网络硬件加速」「网络转发功能硬化」「虚拟交换卸载」。但全为单卡硬件卸载叙事，无多网卡聚合 / 流表跨网卡同步。
- WebSearch②：`阿里云 CIPU 多网卡 链路聚合 LACP 流表 高可靠 卸载` → 命中均为阿里云开发者社区的**通用 LACP 教程**（与 CIPU 无指代关系）+ CIPU 七千字架构 PDF。CIPU 提到「双上联 100GbE 网络」，属上联链路冗余，非「主机内 N 张网卡聚合 + 精确流表同步至全部网卡」。
- WebSearch③：`Alibaba CIPU vSwitch flow table offload multiple NIC dual uplink high availability` → 命中 SIGCOMM '24 Triton 论文（阿里 Apsara vSwitch 硬件卸载，最权威技术来源）、theregister、AVS/SmartNIC 资料。VPC 高可靠描述为「分布式 vSwitch 防单点 / 跨数据中心 failover / 物理链路冗余」，非网卡级流表同步。

## 三、F# 命中表

| F# | 特征 | 判定 | 证据 verbatim | URL | 备注 |
|----|------|------|----------------|-----|------|
| F1 | 多网卡架构 N≥2（虚拟交换机连接 N 个网卡，N≥2） | 未命中（公开资料不足） | 公开资料均描述「MoC 卡 / CIPU 单芯片承担网络虚拟化卸载」，未见「主机内 N≥2 张独立网卡」作为卸载架构前提；CIPU「双上联」指上联链路而非主机侧多网卡聚合 | https://blog.csdn.net/Jmilk/article/details/125518158 ; https://static-aliyun-doc.oss-cn-hangzhou.aliyuncs.com/file-manage-files/zh-CN/20230831/xxzd/七千字详解阿里云CIPU技术架构.pdf | CIPU PDF 为扫描图片，WebFetch 无法抽取正文 |
| F2 | N 个逻辑端口聚合为「第一端口」 | 未命中 | 4 篇深抓来源（含 Triton 论文、InfoQ、CSDN）均无「N 个逻辑端口 → 一个目标端口标识聚合」描述 | https://cs.stanford.edu/~keithw/sigcomm2024/sigcomm24-final113-acmpaginated.pdf ; https://www.infoq.cn/article/kjno59x5hifczzfoahrw | F2 为本专利核心创新点之一，公开资料无对应 |
| F3 | 每个网卡逻辑端口由其物理端口基于 LACP 聚合 | 未命中 | 检索到的 LACP 内容均为阿里云开发者社区通用教程，与 CIPU/MoC 实现无指代关系（同名异义科普词，回上下文不一致） | https://developer.aliyun.com/article/1628349 | 须回上下文确认指代一致 → 不一致，剔除 |
| F4 | 卸载流表 miss 作为触发条件（cache-miss-driven offload） | 部分契合（机制语义） | Triton 论文描述「fast-path 匹配加速 / slow-path 处理」，AVS「快路径卸载至 ASIC、慢路径软件处理」属 cache-miss-driven offload 的通用语义 | https://cs.stanford.edu/~keithw/sigcomm2024/sigcomm24-final113-acmpaginated.pdf | 通用 vSwitch 卸载范式，非本专利专有；且与 F2/F5 的「跨网卡」限定无关 |
| F5 | 精确流表同步卸载至全部 N 个网卡（消除单点故障关键限定） | 未命中（公开资料不足） | 无任何来源描述「一次 miss 触发把同一精确流表同步下发到聚合内所有 N 张网卡」；VPC 高可靠依赖「分布式 vSwitch / 跨 AZ failover / 物理链路冗余」，机制不同 | https://www.alibabacloud.com/help/en/vpc/product-overview/service-architecture | 「不同机制」属等同性反证信号，非命中 |

## 四、已检查文档清单
1. CSDN「看阿里云 CIPU 的 10 大能力」（2022-06-29）——网络卸载为单卡机制，无多网卡/LACP/流表同步。
2. InfoQ「三问阿里云：CIPU 究竟是什么」（2022-06-15）——仅 200G/4000 万 PPS 等单芯片加速指标，无多网卡聚合/流表冗余。
3. SIGCOMM '24 Triton: Apsara vSwitch 硬件卸载架构论文（2024-06-29）——最权威技术来源，无 LACP/多网卡聚合/跨网卡流表同步。
4. 阿里云 CIPU 七千字技术架构 PDF（2023-08-31）——扫描图片型 PDF，WebFetch 无法抽取正文（受限，见下）。
5. 阿里云 VPC service-architecture 文档——高可靠为分布式 vSwitch + 跨 AZ failover + 链路冗余，非网卡级流表同步。

## 五、检索受限声明
- 阿里云 CIPU 七千字架构 PDF（static-aliyun-doc OSS）为图片/扫描型，WebFetch 与正文抽取均失败，未能验证其内是否含「双上联」之外的多网卡聚合细节。该处存在抽取盲区，但其余 4 篇文本来源已形成一致负向信号。
- 云厂商网卡级实现细节公开度低（架构博客/PPT 为主），未能获得 MoC/CIPU 内部流表下发拓扑的权威实现文档。

## 六、最终判定

**第 4 档：公开证据不足以支撑核心特征命中（<60%）**

依据（1–3 句）：
1. 阿里云 CIPU/MoC 确实大规模商用地承担 vSwitch 流表硬件卸载，命中场景 2「硬件卸载交换」的大方向，且 F4（cache-miss-driven offload）语义部分契合——但这是行业通用 SmartNIC 卸载范式，非本专利专有。
2. 本专利的核心创新点 F2（N 逻辑端口聚合为「第一端口」）+ F3（LACP 形成逻辑端口）+ F5（精确流表同步卸载至**全部 N 张网卡**消除单点故障）在 4 篇文本来源（含最权威的 SIGCOMM '24 Triton 论文）中**均无对应描述**；阿里 VPC 的高可靠走「分布式 vSwitch + 跨 AZ failover + 链路冗余」路线，与「主机内多网卡 + 流表同步」机制不同。
3. 命中均为「公开资料不足」而非「确凿反向证据」，且来源时间不全在 2023-06-06 之前（Triton 论文为 2024），故**不落第 5 档（已排除）**；核心特征 F1/F2/F3/F5 公开证据缺失 → 落第 4 档。

## 七、升级路径（第 4 档专属）
- 抓取并 OCR 阿里云 CIPU 七千字架构 PDF（OSS 图片型），检索「双上联」「bond」「多网卡」「流表同步」是否在网卡级展开。
- 查阅阿里云神龙/CIPU 相关**专利与论文**（如 SIGCOMM/NSDI/OSDI 阿里署名网络卸载论文、CN 申请号），定位是否有「精确流表跨多网卡同步」的实现。
- 检索神龙第三/四代 MoC 卡白皮书或云栖大会深度技术 session 是否披露主机内 N≥2 网卡 bond + 流表卸载拓扑。
- 若获实现证据证明「N 张网卡 LACP 聚合 + miss 触发同步全部网卡」→ 可上调至第 3 档（≥60% 无反向）；若获明确「单网卡卸载 / 不做跨网卡同步」反向文档 → 下调至第 5 档。

## 八、总结一句话
阿里云 CIPU/MoC 确做 vSwitch 流表硬件卸载（命中卸载大方向 + F4 语义），但本专利核心的「N≥2 网卡 LACP 聚合为第一端口 + 精确流表同步卸载至全部网卡」在含 Triton 论文在内的公开来源中均无对应、亦无确凿反证，证据不足，落第 4 档。

---
> 免责声明：本文档仅为侵权线索与证据链梳理，不构成「已构成侵权」的法律结论。最终判定以权利要求逐一比对及法律程序为准。
