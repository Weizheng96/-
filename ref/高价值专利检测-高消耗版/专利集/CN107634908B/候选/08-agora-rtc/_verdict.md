# 08-agora-rtc verdict

## 候选基本信息（专利公开日 2021-06-08）
- **组织**：Agora（声网，NYSE: API；NASDAQ 上市；招股书 S-1 已公开）
- **产品**：Agora RTC SDK（音视频通话/直播 SDK）+ SD-RTN™ 软件定义实时网络
- **类型**：产品（云端 + SDK 双面）
- **业务相关性**：高 — 命中专利场景 2（在线游戏 / 低时延通信）、场景 5（VR / 体感）、场景 6（在线视频 / 视频会议）
- **时间窗合规**：✓ Agora RTC SDK 及 SD-RTN 持续在 2021-06-08 之后销售运营（无需进一步举证持续期）
- **初判 F# 集**（来自 Step 5 候选表）：F1, F2, F3, F4, F5
- **本轮检索目的**：核实 Agora SDK / SD-RTN 公开材料中是否真有 F1（业务类型识别 — 基于数据流特征变量）与 F2（业务类型作为冗余包数量计算的输入之一）的命中证据

## F# 命中表（F1-F5）

| F# | 限定核心 | 公开证据 | 命中评估 |
| --- | --- | --- | --- |
| F1 | 发送端**自动**从（缓存包长度/数目、在网包长度/数目、到达间隔、突发性）≥1 项**统计**得到业务类型；不是上层应用静态配置 | **反向证据**：Agora 暴露给开发者的"业务类型"是 `setChannelProfile`（COMMUNICATION / LIVE_BROADCASTING）+ `setAudioProfile`/`AUDIO_SCENARIO_*`，均由开发者**调用 API 静态传入**（[docs.agora.io 助力解答 — profile_difference](https://docs.agora.io/en/help/integration-issues/profile_difference) "use this method to set the channel profile as either CHANNEL_PROFILE_COMMUNICATION or CHANNEL_PROFILE_LIVE_BROADCASTING"；[set audio profile 文档](https://docs.agora.io/en/3.x/interactive-live-streaming/basic-features/audio-profiles) "call setAudioProfile to set the audio profile and scenario before joining a channel"）。这恰好是权 1 的负面限定情形（≈ 从属权 4 "应用制定的业务类型"，不落入权 1 主权项）。<br/>另一条相关表述："improved FEC algorithm enables adaptive switches according to the frame rate and number of video frame packets"（[Agora 4K release-notes search 命中](https://docs.agora.io/en/3.x/interactive-live-streaming/introduction/release-notes)）—— FEC 自适应输入是 **frame rate + 单视频帧包数**（编码层参数），不是"对在网传输数据包做流量统计后识别业务类型"。 | **未命中**（有反向证据 — 业务类型来自应用层 API，不是发送端从流量统计自动识别） |
| F2 | 冗余包数量 = f(网络状态, 传输成功率, 业务类型)；**三元组联合**且业务类型不可缺 | SegmentFault 演进文（[SD-RTN 演进 v2 思否](https://segmentfault.com/a/1190000040725941/en)）verbatim："SD-RTN uses FEC or multi-channel redundancy technologies at the bottom layer **based on the network link assessment status and the required qos level**"。inputs = 网络评估 + QoS 等级（应用层 API 设定的"业务类别"），**未提及"业务类型"作为独立第三输入参与冗余包数量计算**；并且这里的 "qos level" 仍是上层 API 设定，**不构成 F1 意义下的"流量统计驱动业务类型"**。 | **部分命中（弱）**：网络状态 ✓；传输成功率 ✓（"network link assessment"）；业务类型作为应用层静态 hint 间接参与 ✓ — 但与 F1 同源的"业务类型必须从流量自动识别"限定不满足，因此**F2 在权 1 意义下不命中** |
| F3 | 冗余包传输**总时间** = f(时延要求)；是 n 个冗余包累计窗口而非单包 timeout | Whitepaper p10-12 verbatim："latency of less than 200ms is considered ideal"、"median latency less than 76ms globally"。Agora 全网围绕"端到端 sub-second 时延"做编排，但**公开材料未披露"冗余包发送总时间由时延要求换算得到"这种 explicit 算法形态**。SDK 文档亦未暴露 FEC 总时间窗参数。 | **不可证实**（既无正向 verbatim 也无反向证据） |
| F4 | 调度方法 = f(网络状态, 总时间, 冗余包数量)；调度方法应在随机度/最短时间/最长时间/均匀时间集合中至少 1 种 | Whitepaper p13 verbatim："In order to minimize data packet loss, Agora's SD-RTN sends redundant data through the three most optimized network paths possible by default"。Agora 公开侧重 **多路径冗余（route diversity）** 而非"权 4 / 权 9 中的时间维度调度方法选择"——这是**网络层路径冗余**，与权 1 中"冗余包发送时机调度方法"是不同抽象层。 | **不命中**（公开证据指向多路径冗余，与权 1 时间调度集合无对应） |
| F5 | 按调度方法发送冗余包（前提是 F1-F4 成立） | 仅"发冗余"层面成立（多路径冗余 + FEC），但因为 F1 / F4 不命中，权 1 整体不闭合 | **从属于上层失败**（不构成权 1 命中） |

## 已检查文档清单
1. `agora_sd-rtn_whitepaper.pdf`（本地落盘，7.3MB，pdfplumber 提取到 `_whitepaper_text.txt` 共 326 行）
   - 关键段：p3-5 SD-RTN 哲学与 QoS；p6 "Packet Loss UDP-based"；p13 "SD-RTN sends redundant data through the three most optimized network paths possible by default"；p10-12 时延描述
2. https://segmentfault.com/a/1190000040725941/en — Agora SD-RTN 演进文（中英双语稿）
3. https://docs.agora.io/en/help/integration-issues/profile_difference — 频道 profile 文档
4. https://docs.agora.io/en/3.x/interactive-live-streaming/basic-features/audio-profiles — 音频 profile / scenario 文档
5. https://docs.agora.io/en/3.x/interactive-live-streaming/introduction/release-notes — 3.x ILS release notes（仅 1 处 "optimizing the FEC codec" 提及）
6. https://docs.agora.io/en/video-calling/overview/release-notes — 4.x video-calling release notes（全文未提 FEC）

## 最终判定

**第 4 档：弱信号 — 仅部分技术词命中、缺核心三元组业务类型输入**

**判定依据**：
- ✓ Agora SDK / SD-RTN 在做 FEC + 多路径冗余 + 网络状态自适应 — 与本专利同一技术领域
- ✗ Agora 公开材料中**业务类型来自应用层 API**（`setChannelProfile` / `setAudioProfile`），不是发送端从流量统计自动识别 — 与 F1 限定相反
- ✗ 公开材料中冗余包数量计算仅披露 "network link assessment + qos level" 两输入，未披露权 1 要求的"业务类型"作为联合输入 — F2 不闭合
- ✗ Agora 公开的"冗余"主要是**多路径路由层冗余**（route diversity）+ FEC 编码层冗余 — 与权 1 时间维度调度集合（随机度 / 最短时间 / 最长时间 / 均匀时间）抽象层不同 — F4 不闭合
- 注：以上为"公开材料"层面的判定；Agora 闭源 SDK 内部具体冗余算法实现未公开，可能存在更接近权 1 的内部细节，但无公开证据可证实

**不上 5 档原因**：F1 已有明确反向证据（业务类型来自应用层 API），权 1 的整数三元组"业务类型"参数缺失，与权 1 主权项的核心创新点对立；如要落 5 档需要 Agora 公开 SDK 内部 FEC 算法源码或同行评审论文明确说明"从流量统计识别业务类型 → 三元组联合决定冗余包数量"。

**不下 3 档原因**：领域强相关、技术词高度同源（FEC、冗余包、网络状态自适应、QoS 都有）、产品规模大且活跃（NYSE: API 上市公司，2021 年后持续运营），需要承认存在中等信号；并非"已排除"。

## 升级路径（4 档 → 3 档）

要把本候选升至 3 档（"高度疑似 — 需法律评估"），需补充以下任一类证据：
1. **Agora 招股书 S-1 / 10-K 技术附录** 中如明确表述 "FEC redundancy count is jointly determined by network state, transmission success rate, **and inferred traffic type from flow statistics**"
2. **Agora 同行评审论文**（SIGCOMM / NSDI / MM / IMC / IEEE TON 等）若披露 SD-RTN 内部 FEC 算法用流量统计变量（包长度 / 在网包数目 / 到达间隔 / 突发性）做业务类型推断
3. **Agora 招股书 / 法律声明** 中如承认实施过华为 CN107634908B 或其同族专利
4. **Agora 开源组件 / SDK 反编译** 中如出现 `inferTrafficTypeFromFlowStats` / `redundancyCount(loss, successRate, trafficClass)` 等代码

要降至 5 档（"确认侵权"），需以上至少 2 条交叉证据 + F# 全闭合（F1-F5 5 项全部有 verbatim 引文）。

## 总结一句话

Agora SD-RTN 与本专利同一技术领域且 FEC + 多路径冗余 + QoS 自适应公开充分，但权 1 核心限定（业务类型必须由发送端从流量统计自动识别、并作为冗余包数量的三元组联合输入之一）在 Agora 公开材料中存在反向证据（业务类型来自 `setChannelProfile`/`setAudioProfile` 应用层 API），**落第 4 档：弱信号、缺核心三元组业务类型输入**。

---

> **免责声明**：本判定仅基于公开技术资料对权 1 的逐特征比对，不构成法律意见；是否构成侵权需由专业法律评估，并以具体涉案产品版本、闭源 SDK 实施细节、地域适用法及权利要求解释为准。
