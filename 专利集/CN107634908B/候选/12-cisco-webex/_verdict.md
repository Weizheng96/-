# 12-cisco-webex verdict

## 候选基本信息（专利公开日 2021-06-08）
- 候选编号：12
- 类型：产品
- 名称：Cisco Webex Media Engine（涵盖 Webex Meetings App / Webex Calling / Webex 视频会议端点 / Webex Room/Desk/Board 系列设备的媒体引擎）
- 组织：Cisco Systems, Inc.
- 一句话定位：Cisco 的企业级实时音视频会议媒体引擎，使用 MARI（Media Adaptation and Resilience Implementation）框架统一调度 FEC + RTX + 视频 pacing + 自适应分辨率降级。
- 时间窗状态：MARI 框架与 Webex 自适应 FEC/RTX 文档（含本判定引用的 Bandwidth Planning 白皮书、Troubleshooting Audio & Video Quality 文档）均在 2021-06-08 之后仍持续更新发布（最新 PA 文档明确标注 2025），覆盖时间窗。Cisco co-authored RFC 8627（FlexFEC）于 2019-07 发布，属专利公开日前的标准基础。
- 主要适用独立权：权 1（方法）或权 8（设备形态，Webex Board/Room/Desk 终端可对应"处理器+存储器"形态）。

## F# 命中表（F1-F5）

| F#  | 内容                                                                 | 命中状态           | 关键证据来源                                                                                                                                                                                                                                                                                       |
| --- | -------------------------------------------------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| F1  | 由数据流特征变量（缓存长/数、在网长/数、到达间隔、突发性 ≥1）识别业务类型 | **部分命中 (不充分)** | Troubleshooting 文档显式提到 MARI 含"video packet pacing which minimizes packet loss due to **burstiness**"——**4 项之一（突发性）有 verbatim 命中**。但 MARI 对 RTX/FEC 的二选一是基于"negotiated bandwidth and delay tolerance for a given **media stream**"——media stream 是应用层声明（audio / main video / content sharing），更接近从属权 4 形态而非权 1 要求的"由发送端从真实流量统计自动识别业务类型"。无公开证据表明 Cisco 用 4 项之一的统计反推业务类型。 |
| F2  | 冗余包数量 = f(网络状态 + 传输成功率 + 业务类型) 三元组                 | **部分命中**       | "Collaboration endpoints **dynamically choose RTX or FEC** depending on **negotiated bandwidth and delay tolerance** for a given media stream"（Troubleshooting 文档 L467-468）。三元组中"网络状态"（bandwidth, packet loss）+"业务类型"（media stream class）有命中；但这是 mechanism-selection（选 RTX 还是 FEC），非冗余包"数量"计算公式，且"传输成功率"未明示。冗余包数量公式属闭源实现，无公开技术细节。 |
| F3  | 冗余包传输总时间 = f(时延要求)                                       | **命中**           | "Audio retransmit capability is **based on currently observed latency where there is still enough time** to attempt packet recovery via packet retransmission"（Bandwidth Planning whitepaper L1738）+ Troubleshooting 文档"depending on negotiated bandwidth and **delay tolerance**"（L467-468）。延迟预算作为算法输入有明确 verbatim 证据。 |
| F4  | 调度方法 = f(网络状态 + 总时间 + 冗余包数量) 三元组                    | **部分命中**       | MARI 含"video packet pacing which minimizes packet loss due to **burstiness**"——存在显式的"调度/pacing"逻辑，且根据 Bandwidth Planning whitepaper L1736"using **network probes and prediction algorithms** to selectively maintain higher resolution capability when subject to a network environment"——pacing 确实参考网络状态。但 F4 要求的"网络状态 + 总时间 + 冗余包数量"三元组联合是否实际被 pacing 算法用作输入，无公开实现细节可证实。 |
| F5  | 按调度方法发送冗余包                                                 | **命中（proactive FEC 部分）** | Troubleshooting 文档 L454-455："The third mechanism is **Forward Error Correction (FEC)**, which works by **sending redundant video data within RTP packets**"——明确发送主动冗余包。Cisco 是 RFC 8627（FlexFEC video/audio repair stream）合著者（M. Zanaty, Cisco），FlexFEC 即 source RTP + 独立 repair RTP stream 的主动冗余模式。注意：RTX 路径不算 F5 命中（reactive 重传），但 FEC 路径满足。 |

**命中结构小结**：F3 + F5 强命中；F1/F2/F4 部分命中，关键缺口在于"冗余包数量的具体计算公式是否包含三元组输入"无公开证据可证；F1 的"数据流特征变量识别业务类型"路径与 Cisco 实际采用的"应用层声明 media stream type"路径不完全一致。

## 已检查文档清单

| 序号 | 文件 / URL                                                                                                                                                                                  | 类型             | 用途                                                                  |
| ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | --------------------------------------------------------------------- |
| 1    | `webex-bandwidth-whitepaper.html` (Cisco Webex Meetings Bandwidth Planning White Paper, c11-691351, 截至 WBS 40.10)                                                                          | Cisco 官方白皮书 | 取证 Audio RTX / Video RTX 延迟预算驱动、playout buffer 决策、stream 优先级 |
| 2    | `Troubleshooting_AV_Quality.pdf` (Troubleshooting Audio and Video Quality Using Webex Control Hub)                                                                                           | Cisco 官方白皮书 | 取证 MARI 框架定义、RTX-vs-FEC 动态选择规则、pacing + FEC 用途分工        |
| 3    | `PA-WbxCall.pdf` (Cisco Preferred Architecture for Webex Calling, 2025-08)                                                                                                                   | Cisco 官方架构文档 | 验证范围 / 部署形态；未发现媒体引擎 FEC 算法细节                            |
| 4    | RFC 8627（Flexible FEC, 2019-07）— Cisco co-author M. Zanaty                                                                                                                                  | IETF 标准        | 确认 Cisco 在 FlexFEC 标准制定中的核心地位；标准本身**未规定**冗余数量公式，留给实现 |
| 5    | https://blog.webex.com/collaboration/video-conferencing/turning-good-videoconferencing-into-a-great-meetings-with-smart-adaptive-media-resilience-in-webex-meetings/                          | Cisco blog       | 仅泛述 "smart adaptive" 媒体韧性，无算法细节                              |

## 反向证据 / 限定作用域语审查

- **不构成反向证据**：
  - Cisco 文档明示 "Depending on the specific network conditions encountered, video **RTX or FEC** will be used"——这说明 FEC 路径在 Cisco 实现中**存在且 active**，不是仅作为对比项被列出。FEC 路径独立成立时即可触发权 1 命中判定。
  - "RTX is preferred over FEC where bandwidth saving matters"——只是优先级，不是 FEC 被废弃。
- **真正的证据缺口（不是反向证据，但是"未知"）**：
  - 冗余包"数量"如何计算（是否参考成功率 + 业务类型 + 网络状态的三元组）：闭源，无公开细节。
  - 业务类型识别是否真由发送端 4 项特征变量统计推算：公开材料显示是应用层声明（media stream type 由 SDP/codec negotiation 决定），与权 1 隐含约束不完全一致。
  - F4 的 pacing 算法是否真用"网络状态 + 总时间 + 冗余包数量"作三元输入：无公开实现细节。

## 最终判定 **第 3 档：技术路线高度相关但实证不足，无法确认完整命中权 1**

判定依据：
- F3 + F5 有强公开证据命中；F1/F2/F4 在抽象层面与专利方案路径高度相似（自适应 FEC + 延迟驱动 + media 分类 + pacing 调度），但权 1 的关键限定（"数据流特征变量识别业务类型"、"三元组联合计算冗余数量"、"三元组联合选择调度方法"）依赖于**闭源媒体引擎实现细节**，公开文档止步于 mechanism-level 描述，不足以判定完整命中权 1 的全部要素。
- 不是"已排除"档：有真实主动 FEC 发送行为 + 延迟驱动 + 媒体类型分流，技术路径与本专利非显著背离。
- 不是"第 1/2 档（确认/疑似侵权）"：缺少 verbatim 命中权 1 三元组的算法描述；缺少 reverse-engineering 报告 / 源代码 / 协议 trace 可佐证完整 F1-F5 链。

## 升级路径（如何上升到第 1-2 档）

要把本候选从第 3 档升到 1-2 档，需要任一以下证据之一：
1. **Cisco 内部技术 blog / Cisco Live 演讲 PPT / 工程博客**披露 MARI 中冗余包数量的实际计算公式，明确包含"loss rate + media type + delay budget"三元组（或等价输入）。
2. **抓包逆向证据**：从 Webex Meetings App 抓取 FlexFEC repair stream，统计不同网络条件 / 不同媒体类型下 repair packet 数量与 source packet 数量之比，证明该比例随业务类型 + 损失率 + 延迟预算独立变化（不仅随损失率单变量）。
3. **Cisco 在 USPTO / Google Patents 的同族专利**披露其 MARI/Webex 媒体引擎的 FEC 调度算法（可搜索 Cisco 系 FEC patents post-2020，例如 US9577682B2 "Adaptive FEC system and method" 已检索到，可作为后续跟进切入点深查 claim 文本）。
4. **第三方学术研究**（IEEE / ACM）针对 Webex / Cisco MARI 做的黑盒测量论文，验证其 redundancy 调度模型。

## 总结一句话
**Cisco Webex 媒体引擎（MARI 框架）实现了主动 FEC + RTX + 延迟驱动 + 媒体类型分流，技术路径与本专利权 1 高度相关，但权 1 三元组（网络状态 + 成功率 + 业务类型 → 冗余数量；网络状态 + 总时间 + 冗余数量 → 调度方法）的具体算法因闭源不可证，仅 F3/F5 有 verbatim 命中，落第 3 档：技术可能命中但实证不足。**

---
*免责声明：本判定仅为基于公开文档的技术档位评估，不构成法律意见，亦未替专利权人做出"已构成侵权"的法律结论。是否侵权需经源代码审查、协议抓包或诉讼程序由法院依法认定。*
