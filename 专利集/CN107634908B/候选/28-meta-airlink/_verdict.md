# 28-meta-airlink verdict

## 候选基本信息（专利公开日 2021-06-08）

- 候选 NN: 28 · 类型: 产品 · 名称: Meta Air Link / Quest Air Link
- 组织: Meta (Reality Labs)
- 公开度: 低（公开技术资料以使用指南 / 故障排查 / 第三方延时拆解为主，无官方传输层协议白皮书）
- 初判命中 F#: F2, F3, F4, F5
- 时间窗判定：Air Link 2021-04 首发，**早于专利公开日 2021-06-08**；但 Air Link 持续迭代（AFI 上线、Quest 3 适配等更新均在 2021-06 之后），按"公开后仍持续使用 / 演进"判定仍纳入时间窗考察。

## 检索粗筛

Phase 1 WebSearch 4 次（详 _sources.md）：
- q1 Meta Quest Air Link FEC packet loss streaming
- q2 Oculus Air Link adaptive redundancy VR streaming protocol
- q3 site:patents.google.com Meta Oculus FEC streaming forward error correction
- q4 "Air Link" OR "Quest Link" architecture protocol traffic type business type aware bitrate

粗筛结论：**FEC / 主动冗余 / 业务类型识别 0 命中**；反而出现强反向证据信号——Air Link 的公开机制为 ① 动态码率（reactive） + ② AFI 渲染层运动矢量外推（post-delivery） + ③ Wi-Fi 链路自身 ARQ 重传，**无任何"传输层主动冗余包"路径的描述**。判定：粗筛未通过"0 命中 = 已排除"，但通过"反向证据 → 不命中权 1"路径。Phase 2 深抓后维持该结论。

## F# 命中表（F1-F5）

| F# | 描述 | 命中？ | 证据 |
| --- | --- | --- | --- |
| F1 | 业务类型识别 — 基于发送端缓存 / 在途包 / 到达间隔 / 数据突发性 4 项数据流特征变量 ≥1 项 | **未命中（反向）** | Meta 官方 AFI 博客明示文档"explicitly NOT covered: Traffic classification systems"（f1）。公开资料中 Air Link 仅基于网络状态（带宽 / 信号强度 / 历史抖动）做码率自适应，未见"业务类型"维度的输入，更未见基于"缓存包长 / 数目 / 到达间隔 / 数据突发性"四项之一做业务类型判别。 |
| F2 | 冗余包数量 = f(网络状态, 传输成功率, 业务类型) 三元组 | **未命中** | Air Link 公开机制不发送主动冗余包（见 F5），三元组失去前提；即便存在隐式 FEC，业务类型维度缺失（见 F1）。 |
| F3 | 冗余包传输总时间 ← 时延要求 | **不适用** | F5 未发动 → F3 无对应行为可比对。 |
| F4 | 调度方法 = f(网络状态, 总时间, 冗余包数量) — 随机度 / 最短 / 最长 / 均匀 ≥1 | **不适用** | 同 F3。Air Link 的"调度"层面体现为编码器帧率 / 码率档位切换，不是冗余包时间窗内的调度策略。 |
| F5 | 按调度方法发送冗余包（**主动 FEC**，非 ARQ） | **未命中（反向）** | f2 verbatim：> "the TCP retransmission mechanism inherent in Wi-Fi networking introduces unavoidable frame delays when packet loss occurs"——Air Link 丢包恢复依赖 TCP ARQ 重传（reactive），不是主动冗余包（proactive FEC）。f1 verbatim：文档"explicitly NOT covered: Pre-transmission redundancy or FEC mechanisms"。 |

**初判 F2/F3/F4/F5 命中** → **核查后全部转为未命中 / 不适用 / 反向**。

## 已检查文档清单

1. https://developers.meta.com/horizon/blog/air-link-framerate-insurance-afi/ — Meta 官方 AFI 技术博客（f1，WebFetch 成功）
2. https://pimax.com/blogs/highlights/technical-comparison-displayport-direct-connection-vs-quest-3-streaming-solutions-for-pcvr — Pimax 第三方 Air Link 协议拆解（f2，WebFetch 成功）
3. https://mixed-news.com/en/meta-quest-2-pc-vr-streaming-with-air-link-latency-review/ — Mixed-news 延时拆解（f3，WebFetch 成功，证据空白）
4. WebSearch 4 次结果摘要（详 _sources.md q1-q4）
5. Google Patents Meta/Oculus FEC streaming 命中清单（q3，无对应布局）

## 最终判定 **第 4 档：基本不构成（反向证据明确，公开资料范围内）**

判定理由：
1. **F1（业务类型识别）反向**：Meta 官方明示 Air Link / AFI 文档不涉及 traffic classification；现有码率自适应仅基于网络状态，无"业务类型"输入维度。
2. **F5（主动冗余）反向**：公开技术资料一致显示 Air Link 走"动态码率 + AFI 渲染层外推 + Wi-Fi ARQ 重传"路径——前两者是后置补偿、第三者是反应式重传，均不构成"发送前主动产生 ≥1 个冗余包"的 F5 动作。
3. **F2/F3/F4 失锚**：F5 未发动 → 冗余包数量 / 总时间 / 调度方法三个限定无对应物理动作。
4. **专利布局侧证**：Google Patents 检索未发现 Meta / Oculus 名下与本专利权 1 路径相似的 FEC streaming 专利布局，间接说明 Meta 并未在该技术路径上发力。

> **注（0 命中 ≠ 已排除）**：本判定并非基于"检索 0 命中"，而是基于公开资料中可读到的 Air Link 实际机制（动态码率 + ML 外推 + ARQ）与权 1 路径（业务类型自适应 + 主动 FEC 冗余 + 三元组调度）在**架构维度**互斥这一**反向证据**。

> **协议黑盒残余风险**：未排除 Meta Air Link 内部存在未公开的轻量级 FEC 模块（如视频帧内 RS 码 / 应用层 FEC）。但即便存在，需同时满足"业务类型自动识别（F1） + 三元组冗余包数量计算（F2） + 时延窗内调度（F3-F4）"才能命中权 1；公开资料中无任何线索指向 Meta 在 F1（业务类型识别）维度有相应实现。

## 升级路径（仅作排查参考；当前为 4 档不触发）

若未来获得以下任一新证据，可考虑升至 3 档：
- Meta 公开（论文 / 技术博客 / 专利申请）Air Link 协议层包含基于流统计（缓存包长 / 到达间隔 / 数据突发性）的业务类型识别模块。
- Meta 在 Air Link 中实装基于丢包率 + 业务类型的 packet-level FEC，并按时延窗调度。
- Air Link SDK / 抓包逆向分析显示 RTP-FEC 风格冗余包流（uneven distribution，按业务自适应）。

升至 2 档需更多 F# 同时命中且证据可重现（如官方技术文档明示 + 第三方逆向佐证）。

## 总结一句话

Meta Air Link 公开机制为动态码率 + AFI 渲染外推 + Wi-Fi ARQ 重传，无传输层主动 FEC 冗余包，亦无"业务类型自动识别"维度，与权 1 的"业务类型 + 三元组冗余 + 时延窗调度"路径架构互斥，**落第 4 档：基本不构成**。

> 本判定仅为基于公开资料的技术档位评估，不构成法律意见；任何"已构成侵权"结论应由专利权人通过正式渠道判定。
