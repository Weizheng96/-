# 13-ms-teams verdict

## 候选基本信息

- **NN / slug**：13 · 13-ms-teams
- **类型**：产品（实时通信媒体栈）
- **名称**：Microsoft Teams Media Stack（含 Skype for Business 共用底层）
- **组织**：Microsoft Corporation
- **关联场景**：场景 6（在线视频 / 电视电话会议） — 专利说明书 verbatim "电视/电话会议"
- **公开度**：中（音频编解码 + FEC 概念有官方博客 + Learn 文档；冗余包数量算法 / 调度方法层面**不公开**）
- **专利公开（授权）日**：2021-06-08（时间窗基准）
- **时间窗判定**：✅ 通过 — Teams + Skype 媒体栈使用动态 FEC 至 2025-06-18 仍在官方文档中（post-grant 持续运行）；Satin 编解码 2021-02 上线后已成为所有 Teams/Skype 两方通话默认编解码

## F# 命中表

| F# | 权 1 verbatim 要素 | Teams 公开证据 | 判定 | 证据强度 |
|----|---|---|---|---|
| **F1** | 发送端根据**数据流特征变量**（缓存中数据包长度/数目、在网数据包长度/数目、到达间隔、突发性 ≥1 项）获取**业务类型** | Teams 在媒体面对 audio / video / sharing 三种媒体类型有差异化处理（不同 UDP 端口 3479/3480/3481、不同 FEC 行为：音频 dynamic-on-loss、视频 always-on），但**业务类型识别基于编码会话已知的媒体类型**（音频会话就是音频），**不是从发送端缓存的数据流统计特征推断**。F1 的关键创新点（用流量统计变量自动推断业务类型）在公开材料中**无证据**。 | **不命中** | 反向倾向（机制不同） |
| **F2** | 冗余包数量 = f(网络状态变量, 传输成功率, 业务类型) | (a) 音频：**"FEC is used dynamically when there's packet loss on the link"** + 带 FEC 带宽表（如 RTAudio Wideband 57→86 Kbps）→ 网络状态 / 成功率参与 ✅；(b) Satin "redundancy algorithms improved for burst loss" → 突发性参与（属于网络状态变量的扩展）✅；(c) 音频 vs 视频 FEC 行为差异 → 媒体类型参与 ≈ 业务类型 △（媒体类型不等同于专利权 4 的细分业务类型如"控制消息/在线游戏/视频"）。三元组联合的"业务类型"输入**部分等价、不强**。 | **部分命中（机制方向匹配，关键输入弱）** | 中 |
| **F3** | 冗余包**传输总时间**来自时延要求 | Teams 公开的时延要求（<60ms RTT optimal）和 jitter buffer 概念存在，但**没有任何公开文档说"用时延要求计算冗余包的传输总时间窗口"**。Satin / SILK 的 in-band 冗余是把冗余字段直接附在每个 RTP 包内（典型 LBRR 是上一帧的低速率版本附在当前包），这是**包级时序**而非"n 个冗余包累计窗口长度"。 | **不命中**（机制不同：in-band per-packet vs accumulated multi-packet window） | 反向倾向 |
| **F4** | 调度方法 = f(网络状态, 传输总时间, 冗余包数量)，可选集合：随机度 / 最短时间 / 最长时间 / 均匀时间 | 公开材料**完全没有**披露 Teams 的冗余包调度策略选择算法；SILK LBRR 是固定 "previous frame in current packet" 这种隐式均匀；Satin 用 "redundancy algorithms"（不公开细节）。"三元组动态选调度方法"**无证据**。 | **不命中 / 证据不足** | 低 |
| **F5** | 发送端按调度方法发送冗余包 | Teams **确实发送了主动冗余包**（不仅是 ARQ 重传）：SILK LBRR / Satin redundancy frames / 视频 FEC bundled in payload。"proactive FEC, not reactive retransmission"**机制方向命中**。但缺 F4 → 缺"按调度方法"的限定。 | **机制命中、限定语证据不足** | 中 |

**命中汇总**：F1 不命中、F2 部分命中、F3 不命中、F4 不命中 / 证据不足、F5 机制方向命中但限定语不全 → 权 1 整体**未达到 verbatim 5/5 全要素命中**。核心缺口是 F1（业务类型来自数据流统计变量）和 F3+F4（冗余包总时间和调度方法的三元组联合选择）。

## 已检查文档清单

| # | 来源 | 链接 / 路径 | 类型 |
|---|---|---|---|
| 1 | MS Learn — Skype for Business Plan network requirements | https://learn.microsoft.com/en-us/skypeforbusiness/plan-your-deployment/network-requirements/network-requirements | 官方技术文档（updated 2025-06-18） |
| 2 | MS Learn — Microsoft Teams call flows | https://learn.microsoft.com/en-us/microsoftteams/microsoft-teams-online-call-flows | 官方技术文档（updated 2026-03-31） |
| 3 | MS Learn — Skype for Business Online (retired) media quality | https://learn.microsoft.com/en-us/previous-versions/skypeforbusiness/optimizing-your-network/media-quality-and-network-connectivity-performance | 官方文档（归档版） |
| 4 | Microsoft Teams Blog — Satin AI-powered audio codec | https://techcommunity.microsoft.com/t5/microsoft-teams-blog/satin-microsoft-s-latest-ai-powered-audio-codec-for-real-time/ba-p/2141382 （本地 satin_blog.html）| 官方 Teams 团队博客（2021-02-17） |
| 5 | webrtcHacks — RED: Improving Audio Quality with Redundancy | https://webrtchacks.com/red-improving-audio-quality-with-redundancy/ | 第三方技术博客（旁证 Skype 用 SILK LBRR） |
| 6 | Google Patents — MS 自家 adaptive FEC 专利组合 | US8015474B2 / US6772388B2 / US9577682B2 | MS 自家 prior-art 专利（非本专利权人，独立路径证据） |

## 最终判定

### **第 3 档：技术方向匹配但关键限定语缺证据 / 中间环节不公开**

**判定理由**：

1. **技术方向高度匹配**：Teams/Skype 媒体栈**确实**实现了"丢包率自适应主动 FEC 冗余"，且对音频/视频流量类型有差异化处理，与本专利的**核心创新方向**（业务类型 + 网络状态联合自适应主动冗余）属于**同一技术家族**。
2. **但关键 verbatim 要素证据不足**：
   - F1 的"数据流特征变量推断业务类型" — Teams 的业务类型直接来自媒体会话签约（不是从流量统计推断），**机制不同**；
   - F3 的"冗余包传输总时间 = f(时延要求)" — Teams 用 in-band per-packet 冗余（LBRR / Satin 冗余帧），**不是 n 包累计时间窗口**；
   - F4 的"三元组动态选调度方法" — 公开材料完全无披露，且 SILK LBRR 的"固定附前一帧"机制接近**单一调度策略**，不像"在 4 种调度方法中动态选"。
3. **存在 MS 自家独立专利路径**：US8015474B2（2008 申请）等 MS 自家 adaptive FEC 专利早于本专利，**降低了"必须使用本专利"的归属推定**；MS 完全有能力独立实现而无须借鉴 CN107634908B。
4. **不能下"已构成侵权"结论**：核心证据缺口 + 独立技术路径存在 + 具体冗余算法代码不公开 → 仅停留在"技术方向有重合"。

### 升级路径（3 → 2/1 档）

若以下任一**新证据**出现，可上调档位：

- **升至第 2 档（强机制重合 + 个别要素命中）的触发条件**：
  - 找到 MS 官方代码 / 论文 / 专利申请明确披露"基于发送端缓存队列长度 / 包到达间隔 / 突发性统计自动推断流量类型"（命中 F1）；
  - 或找到 Teams 媒体栈技术 deep-dive（如 Build 大会 BRK4016 转录、SIGCOMM 论文）明确说"按时延要求计算冗余包发送窗口"（命中 F3）；
  - 或找到调度方法在 {随机 / 均匀 / 最短 / 最长时间} 中动态选择的实现细节（命中 F4）。
- **升至第 1 档（核心要素全命中）的触发条件**：F1+F3+F4 三个缺口同时被强证据补齐 + 时间窗 post-2021-06-08 持续运行确认。

### 降级路径（3 → 4/5 档）

- **降至第 4 档（弱方向相似）的触发条件**：MS 公开声明 Teams FEC 走 "purely codec-level in-band redundancy + simple FEC matrix"，明确不做发送端流量统计 / 总时间窗口计算 / 多调度策略选择 — 则本专利特有的"四步三元组联合"机制与 Teams 实现属于**不同技术家族**，仅都属于"adaptive FEC" 大类。
- **降至第 5 档（已排除）的触发条件**：需有 MS 官方"反向证据"明确否定主动冗余机制（极不可能，已有正向证据）；当前材料不支持已排除。

## 总结一句话

Microsoft Teams Media Stack 确实实现"丢包自适应主动 FEC 冗余 + 音视频差异化"，技术方向与 CN107634908B 权 1 核心创新一致，但 F1（发送端流量特征推断业务类型）/ F3（按时延要求算冗余总时间）/ F4（多调度方法动态选）三个 verbatim 限定语在公开材料中**缺证据**，且 MS 有独立 adaptive FEC 专利路径，**落第 3 档**。

---

**免责声明**：本判定为基于公开材料的**技术档位评估**，非法律侵权结论。最终侵权认定须由具备资质的专利律师 / 法院依据完整证据链作出。
