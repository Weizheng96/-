# 25-valve-sdr verdict

## 候选基本信息（专利公开日 2021-06-08）

- 候选 NN：25
- 类型：产品
- 名称：Steam Datagram Relay (SDR)
- 组织：Valve Corporation
- 初判命中 F#（_meta.json）：F2, F3, F4, F5
- 公开度：中
- 一句话定位：Valve 自家游戏 UDP 加速路由 + 抗丢包传输服务；部分开源在 ValveSoftware/GameNetworkingSockets 仓库。
- 时间合规：SDR 项目早于专利公开日（2021-06-08）即已存在，但本步只看候选**至今**是否在公开层面体现 F1-F5；故时间窗本身不构成排除理由。

## F# 命中表（F1-F5）

| F# | 权 1 限定 | 候选公开证据 | 判定 | 来源 |
| --- | --- | --- | --- | --- |
| F1（业务类型识别 — 由发送端从数据流特征变量自动推断） | 必须从"缓存包长度/数目、在网包长度/数目、到达间隔、突发性"4 项中 ≥1 项**自动**推断业务类型 | 未检索到公开来源描述 SDR / GNS 做发送端流量统计驱动的"业务类型推断"。GNS README 与 SNP 源码片段描述的是 ack vector + token bucket + 优先级 lane（lane 是 API 调用方手动指定的优先级编号，**非发送端自动从流量统计推断的业务类型**） | **不命中** | W2, W3 |
| F2（冗余包数量 = f(网络状态, 传输成功率, 业务类型) — 三元组联合计算） | 三个输入缺一不可，输出为冗余包整数数量 ≥1 | 未检索到公开来源描述 SDR / GNS 生成主动冗余包；SNP 源码中 FEC 仅出现在**单一注释**里（`"perhaps FEC?"`）作为未来设想，**未在产品代码实装** | **不命中** | W2, q2 |
| F3（冗余包传输总时间 — 由时延要求决定的发送窗口长度） | 总时间需由时延要求得出 | 无公开证据 SDR / GNS 存在"按时延要求决定多包累计发送窗口"的逻辑 | **不命中** | W1-W6 |
| F4（调度方法 = f(网络状态, 传输总时间, 冗余包数量) — 三元组联合选择） | 调度策略需动态联合 3 个输入 | 无公开证据 SDR / GNS 有冗余包调度策略选择逻辑 | **不命中** | W1-W6 |
| F5（按调度方法发送冗余包） | 真正发出主动冗余副本（非 ARQ / 重传） | SDR / GNS 公开机制是 ack/nack + 选择性重传（reactive ARQ 类）。"重传"是 reactive，**不构成 F5 命中**（见专利说明 "纯 ARQ / TCP 超时重传机制不构成 F5 命中"） | **不命中** | W2, W3 |

**反向证据 vs 限定作用域语 严格区分**：

- 真反向证据：GameNetworkingSockets 公开 README / SNP 源码片段明确把自身定位为 "reliable & unreliable messages over UDP" + "ack vector" + "retransmission for reliable messages"，**显式描述的是 reactive ARQ 机制**，不是主动 FEC。这是机制层面的反向证据。
- 限定作用域语（不算反向证据）：源码注释 `"If senders do retransmit unreliable segments (perhaps FEC?) then they need to retransmit the exact same segments."` —— 这是**未实现的未来设想**，按规则属于 "future work / 不在本工作范围" 类的限定作用域语，**不能单独作为反向证据**。但配合上一条机制层反向证据，整体仍指向"FEC 未实装"。

## 已检查文档清单

1. Steamworks 官方 SDR 文档（partner.steamgames.com）—— W1
2. GameNetworkingSockets SNP 实现源码（前 1000 行）—— W2
3. GameNetworkingSockets README.md —— W3
4. GameNetworkingSockets README_P2P.md —— W4
5. rtldg SDR FAQ gist —— W5
6. GameIndustry.eu SDR 介绍 blog —— W6
7. Valve Developer Wiki（被 Anubis 反爬阻断，仅靠 WebSearch snippet）—— W7
8. WebSearch q1-q4 全部命中页面预览片段

## 最终判定 **第 5 档：已排除**

- **依据**：F1-F5 全部不命中。Valve SDR / GameNetworkingSockets 公开层面的传输模型是 **reactive ARQ（ack vector + 选择性重传）+ relay 路由 + DDoS 防护**，**不包含**：(a) 发送端从流量统计自动推断业务类型；(b) 主动 FEC / 冗余包生成；(c) 业务类型 × 网络状态 × 成功率三元组冗余包数量计算；(d) 时延要求驱动的冗余调度。
- **0 命中 ≠ 已排除——本判定不是凭"无证据"得出**：而是凭 (i) 官方 Steamworks doc + repo README + P2P doc + SNP 源码 4 个独立官方来源对 SDR 机制的正向描述均为 "reliable/unreliable + ack vector + retransmission"（机制层反向证据），(ii) FEC 关键词在 SNP 源码中仅以 "perhaps FEC?" 形态出现于注释（self-acknowledged 未实装），共同构成反向证据链。
- **不外推**：不排除 Valve 在 Source 引擎 / Steam Remote Play / Half-Life: Alyx Remote 等闭源模块中可能存在未公开的冗余传输逻辑；但本 skill 只依据**公开**层面判定，公开层面无证据 → 落第 5 档。

## 升级路径（不适用）

本候选落第 5 档，无升级路径。若未来出现以下任一新证据，可重启评估：
- Valve 公开发表 SDR / GameNetworkingSockets 加入 FEC / 主动冗余 / 业务类型自适应的 release note 或博客；
- ValveSoftware/GameNetworkingSockets 仓库提交 production FEC 代码（非 "perhaps FEC?" 注释）；
- 第三方逆向 / 抓包研究证明 Steam 客户端实际发送了主动冗余副本且按业务类型 / 网络状态 / 时延动态调度。

## 总结一句话

Valve SDR / GameNetworkingSockets 公开层面是 reactive ARQ + relay 路由，FEC 仅作未来设想出现在源码注释中，未实装主动冗余 / 业务类型自适应调度逻辑，故落第 5 档：已排除。
