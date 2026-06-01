# 33-aws-global-accel verdict

## 候选基本信息（专利公开日 2021-06-08）
- 候选编号：33
- 名称：AWS Global Accelerator
- 组织：Amazon Web Services (AWS)
- 类型：产品（云网络加速服务，2018-11 GA，文档持续更新至 2024-2026）
- 初判命中 F#：F2, F4, F5
- 公开度：中（官方 FAQ / 开发者指南 / blog 公开度高，但无源码，无内部数据面细节）
- 时间窗：服务在专利公开日（2021-06-08）后仍持续运营 + 文档更新，时间窗成立。

## F# 命中表（F1-F5）

| F# | 专利限定 | AWS Global Accelerator 实际做的事 | 命中？ | 证据 |
|----|---------|----------------------------------|--------|------|
| F1 | 发送端从 4 项数据流特征变量（缓存包长度/数目、在网包长度/数目、到达间隔、突发性）中至少识别 1 项以推导业务类型 | 不识别业务类型，亦不基于数据流统计特征做分类；流量分类只靠 listener 协议（TCP/UDP）+ 端口配置 + traffic dial / endpoint weight（用户静态配置）。"How it works" 文档 0 处提及发送端数据流统计 / 业务类型推导。 | 否（反向证据） | doc1, doc2 |
| F2 | 冗余包数量 = f(网络状态变量, 传输成功率, 业务类型) — 三元组联合 | 不生成冗余包；架构是 anycast 入口 + TCP termination at edge + AWS backbone 转发 + UDP 转发（含分片重组）。无任何 "n 个冗余副本" 或 packet-level FEC 描述。AWS doc 用的 "redundant" 一词指 (a) 双 anycast IP（network zone A/B）(b) AWS backbone 为 redundant 网络，均与"包级冗余副本"无关。 | 否（反向证据） | doc1, doc2, doc3 |
| F3 | 冗余包传输总时间 = f(时延要求) | 服务无 "冗余包发送窗口" 概念。仅有 idle timeout（TCP 340s / UDP 30s），与 F3 语义无关。 | 否（反向证据） | doc2 |
| F4 | 调度方法 = f(网络状态, 总时间, 冗余包数量) — 三元组联合；可选集合：随机度/最短/最长/均匀时间 | 不调度冗余包。路由决策针对"连接"或"包"做 endpoint 选择（geo + health + weight + dial），非"在窗口内按时间分布冗余副本"。 | 否（反向证据） | doc2 |
| F5 | 发送端按上述调度方法发送冗余数据包 | 不发送冗余副本；仅做"按最优路径转发原始包"。 | 否（反向证据） | doc1, doc2 |

**F# 命中数：0/5。0/5 命中且 F2/F4/F5 三项均有明示反向证据（机制本身是 anycast + 路径优化，不是 packet-level proactive redundancy），不再是"0 命中不等于已排除"，而是"硬反向证据"。**

## 已检查文档清单
- doc1：https://aws.amazon.com/global-accelerator/faqs/ — 官方 FAQ；机制描述为 anycast + edge proxy，不涉及 FEC / 冗余副本 / 业务类型自适应。
- doc2：https://docs.aws.amazon.com/global-accelerator/latest/dg/introduction-how-it-works.html — 官方开发者指南 "How it works"；完整描述了机制（anycast IP / edge TCP termination / 健康检查 / traffic dial / endpoint weight / UDP 分片转发），全文 0 处提及 FEC / 冗余副本 / 业务类型自适应。
- doc3：https://aws.amazon.com/global-accelerator/features/ + 多个 AWS blog（measurement / resiliency / well-architecting）— 描述 "redundant AWS global network" 与 "redundant anycast IP"，但语义为"网络路径冗余 + IP 地址冗余"，与"专利权 1 中的冗余数据包"不同义。
- doc4：https://aws.amazon.com/blogs/aws/new-aws-global-accelerator-for-availability-and-performance/ — 服务发布博客；机制描述与 doc1/doc2 一致。
- 检索粗筛 query 留痕：见 _sources.md（4 次 WebSearch，全部聚焦 FEC / packet-level redundancy / UDP duplication 议题，均未在 AWS Global Accelerator 上下文中找到与权 1 限定相符的机制描述）。

## 最终判定 **第 5 档：已排除（反向证据明确）**

**判定依据**：

1. **F1 反向**：Global Accelerator 完全不做"基于发送端数据流特征变量推导业务类型"——它根本不识别业务类型；流量在 listener 层只按协议/端口分桶，按地理 + 健康 + 静态权重选 endpoint，未触及权 1 中"缓存包数目/到达间隔/突发性"这类数据流统计输入。
2. **F2/F4/F5 反向**：服务机制是 **anycast 路由 + edge TCP 终结 + 沿 AWS backbone 转发**，**不在数据面生成 / 调度 / 发送冗余数据包**。文档中所有 "redundant" 出现位置均指 (a) 双 anycast IP / 网络区 A、B；(b) AWS 全球骨干网本身是冗余网络。这两种"冗余"都是路径 / 入口冗余（同一个原始包走不同路径或入口），与权 1 所要求的"主动 FEC / packet-level 冗余副本"完全不同义。
3. **领域适配性反向**：专利 F1-F5 描述的是协议栈层（数据链路 / 传输层）的发送端动作，而 Global Accelerator 是 L3/L4 边缘 PoP 路由服务，定位本质不同——它不是"发送端 SDK / 终端协议栈"，亦不会被用作专利中的"发送端"实体。
4. **不构成"0 命中即排除"的偷懒判定**：本档位的依据是上述 3 条**主动反向证据**（官方文档明示机制 + 机制与权 1 不同义 + 定位与"发送端"主体不符），而非"搜不到信号"。

## 升级路径（3-4 档时）
不适用——本候选已落第 5 档。如未来 AWS 发布 Global Accelerator 衍生服务（如 "Global Accelerator for UDP gaming with adaptive FEC" 类产品），需重新立项一个候选 NN-aws-ga-gaming 独立排查；本次结论仅覆盖现役"标准 / 自定义路由"两种 accelerator 类型。

## 总结一句话
AWS Global Accelerator 机制为 anycast + 边缘 TCP 终结 + AWS backbone 路径优化 + 双静态 IP 冗余，不生成 / 不调度 / 不发送 packet-level 冗余副本，亦不基于发送端流量特征识别业务类型，与 CN107634908B 权 1 的 F1-F5 全部反向，**落第 5 档：已排除**。

## 免责声明
本报告仅为技术线索筛查与档位判定，**不构成"已构成侵权"的法律结论**；最终侵权认定需由权利人结合权利要求字面解释、等同原则与司法审理综合判断。所引 AWS 文档为公开访问内容，由 WebFetch 抓取，引用时间为 2026-05-26。
