# 27-riot-direct verdict

## 候选基本信息（专利公开日 2021-06-08）
- 类型：产品（自建专网 / backbone network）
- 名称：Riot Direct backbone
- 组织：Riot Games（拳头游戏，腾讯系）
- 初判命中 F#（Step 5 假设）：F2、F3、F4、F5（本次 Step 6 核实后该假设不成立）
- 公开度：低（官方技术博客仅有架构层介绍，无协议细节、无源码）
- 公开材料覆盖窗口：Part I/II/III 系列约 2014–2016；Valorant netcode 2020；均早于专利公开日 2021-06-08，之后未见任何"加入 FEC / 冗余包"的更新公告。

## 检索粗筛（Phase 1）
4 次 WebSearch 全部完成（详见 _sources.md）。命中点全部指向 Riot 官方 tech blog 三部曲 + Valorant netcode 博客；二手来源（玩家排错、esports.net）均围绕"如何在玩家端缓解丢包"主题，与本专利发送端冗余机制无关。**Phase 1 通过**（有充分公开材料可深抓核实），进入 Phase 2 深抓。

## F# 命中表（F1-F5）

| F# | 专利限定 | Riot Direct 公开证据 | 命中？ |
|----|----------|---------------------|--------|
| F1 | 发送端根据"缓存包长/数、在传包长/数、到达间隔、突发性"自动识别业务类型 | 无任何公开材料显示 Riot Direct 做包级业务类型识别——Riot Direct 是 L3 backbone / BGP 引流层面，对 Riot 自家流量 vs 其他互联网流量的区分在 BGP / Anycast 路由层完成，与 F1 限定的"基于数据流统计变量识别业务类型"语义不同 | **不命中** |
| F2 | 冗余包数量 = f(网络状态, 传输成功率, 业务类型) 三元组联合 | Riot 官方明确不发冗余包：Part II 的核心叙述是减少跳数物理降丢包；Valorant 用 client prediction + server reconciliation；**全链路未发包级冗余副本** | **不命中** |
| F3 | 冗余包传输总时间 = f(时延要求) | 无冗余包 → 无"冗余包总时间"概念 | **不命中** |
| F4 | 冗余包调度方法 = f(网络状态, 总时间, 冗余包数量)，可选随机/最短/最长/均匀时间 | 无冗余包 → 无调度方法 | **不命中** |
| F5 | 发送端按调度方法发送冗余包 | Riot Direct **不发送冗余包**；Valorant 客户端通过 server reconciliation 处理丢失输入，是 reactive 预测/纠正，**非 proactive FEC**，按 SKILL.md 显式约束"纯预测/重传 ≠ F5" | **不命中** |

## 已检查文档清单

1. https://www.riotgames.com/en/news/fixing-internet-real-time-applications-part-i — Riot Direct 系列 Part I（问题陈述）
2. https://www.riotgames.com/en/news/fixing-internet-real-time-applications-part-ii — Riot Direct 系列 Part II（技术核心：BGP + peering + 暗光纤）
3. https://www.riotgames.com/en/news/fixing-internet-real-time-applications-part-iii — Riot Direct 系列 Part III（Anycast + 自定义路由 + 监测指标）
4. https://www.riotgames.com/en/news/peeking-valorants-netcode — Valorant netcode（client prediction + server reconciliation）
5. 检索期间标题命中但未独立 fetch（已确认主题与上述结论一致，未涉及包级冗余）：
   - "Leveling Up Networking For A Multi-game Future"
   - "Engineering Esports: The Tech That Powers Worlds"
   - "Improving Performance by Streamlining League's Server Selection"

## 反向证据（关键引文）

- **Riot Direct 设计哲学**（Part II，来自 WebFetch 摘要）：> "creating a network ... with many fewer routers (and other devices) that drop packets and degrade the player experience"——这是**减少丢包发生的物理概率**（fewer hops），与本专利 F2/F4 的"基于实测丢包率自适应调冗余副本"是完全相反的设计哲学。
- **Riot Direct 路由治理手段**（Part II）：> "had to work with the ISP to fix this by having them mark their traffic using BGP Communities or MED preferences"——表明问题修复发生在 BGP 控制面，而非数据面包级冗余。
- **Valorant 丢包应对**（Peeking into Netcode）：> "your client is always locally predicting the results of your inputs and showing you the likely outcome"；缺包时服务端 > "guess that they continued to hold down whatever keys were being held in the last received update"——明确是 reactive 预测/纠错，非 proactive 冗余传输；归属于 SKILL.md 中"纯 ARQ / 预测 ≠ F5 命中"的反向情形。
- **业务类型语义错位**：Riot 在 BGP / Anycast 层区分"Riot 流量 vs 非 Riot 流量"，与 F1 限定的"由发送端基于缓存包长 / 到达间隔 / 突发性自动识别上层业务类型（控制消息 vs 视频 vs 游戏 vs ...）"完全不同。

> 反向证据 vs 限定作用域语严格区分（SKILL.md 硬约束）：本节引用的均为 Riot 自家对其架构的**实证描述**（"we built X / we use Y"），属于真反向证据；不是"future work"、"out of scope"等限定语。

## 时间窗判定
- Riot Direct 系列博客发布时间：约 2014–2016（早于本专利 2021-06-08 公开日）；
- Valorant netcode 博客：2020 年（早于专利公开日）；
- 即便假设存在命中点，时间合规性也需重新评估；但本案核心是**反向证据**（设计哲学不同），时间窗仅作辅助判断。

## 最终判定 **第 5 档：已排除**

判定依据（三选一硬条件）：
- ☑ **真反向证据**：Riot Direct 多份官方文档明确技术路径为 "fewer routers / less hops / BGP & peering optimization"，**显式不采用包级冗余**；Valorant netcode 明确用 client prediction + server reconciliation 应对丢包，**显式不采用 FEC / 冗余包**。这与权 1 F2-F5 的"主动发送 ≥1 个冗余包并按调度方法调度"形成直接构造性冲突。
- ☐ 时间不合规（不构成排除主因）
- ☐ 领域无关（部分相关：Riot Direct 服务于"在线游戏低延时"场景，与本专利场景 2 主题词重叠；但**实现机制完全不同**——构造性冲突优先于场景重叠）

注：本判定不构成法律意见，仅为基于公开材料的技术档位评估。

## 升级路径
不适用（第 5 档无升级路径）。若未来出现以下证据则需重新评估：
- Riot 公开宣布在 Riot Direct 上叠加 packet-level FEC / 冗余传输模块；
- Valorant / LoL 客户端协议被独立逆向工程证实发送 redundant copies 并按丢包率/业务类型自适应调度；
- Riot 发布的网络专利或论文显示 F1-F5 等价机制。

## 总结一句话
Riot Direct 用"少跳数 backbone + BGP/Anycast 引流 + 暗光纤"从物理上降低丢包概率，Valorant 用 client prediction + server reconciliation 应对剩余丢包，**均不采用 F2-F5 描述的"主动发送基于业务类型/丢包率自适应的冗余副本"机制**，落第 5 档：已排除。
