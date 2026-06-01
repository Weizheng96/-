# 10-zego-rtc verdict

## 候选基本信息（专利公开日 2021-06-08）

- 候选名称：ZEGO Express RTC（即构科技实时音视频 SDK）
- 候选类型：产品（商业 RTC SDK，闭源）
- 组织：ZEGO（即构科技）
- 初判命中 F#：F1, F2, F3, F4, F5（高）
- 复核后命中 F#：见下"F# 命中表"
- 公开度：高（官方博客 / CSDN zego_0616 / cnblogs zegoinfo / 官方 docs）
- 时间窗：ZEGO Express SDK 持续运营至今（>2021-06-08），公开文档（setRoomScenario 文档、AVERTP 介绍）当前在线 → 时间窗合规。

## F# 命中表（F1-F5）

| F# | 权 1 限定 | ZEGO 公开材料证据 | 命中？ |
|----|----------|------------------|--------|
| **F1** | 基于数据流特征变量（缓存包长度/数目、在网包长度/数目、到达间隔、数据突发性 ≥1 项）**自动**获取业务类型 | ZEGOCLOUD scene-specific 博文明确："developer explicitly configures it"、"no automatic detection mentioned"。业务类型 = scenario 枚举（Broadcast / StandardVideoCall / HighQualityVideoCall / StandardChatroom / HighQualityChatroom / Karaoke / Default），由应用开发者通过 `ZegoEngineProfile.scenario` / `setRoomScenario()` 静态传入。zego_0616 / cnblogs / WebRTC QOS 博文均未提"按数据包统计自动识别业务类型"。 | **反向证据**（=权 1 从属权 4 的"应用制定业务类型"形态，不命中权 1） |
| **F2** | 冗余包数量 = f(网络状态变量, 传输成功率, 业务类型) 三元组联合 | zego_0616：FEC "根据丢包率（PLR）设置冗余度"；AVERTP 介绍：基于实时流质量计算动态切换。**仅见"网络状态/成功率"两元，未见"业务类型"显式作为冗余包数量计算输入**；scenario 主要影响码率/分辨率/帧率/编码 codec，公开材料未表述其改变 FEC 冗余包数量。 | 部分命中（缺业务类型输入 → 按 SKILL F2 释义"缺业务类型则不命中权 1"） |
| **F3** | 冗余包**传输总时间**由时延要求决定（n 包累计窗口） | zego_0616 仅提"ARQ 重传需在解码 deadline 前完成 / RTT 倍数估算"，是 ARQ 单包 timeout，**不是 n 个冗余包累计发送窗口**；FEC 部分未涉及 deadline-driven 总时间。 | 未确认命中（仅有 ARQ deadline 概念，无 FEC 包累计窗口） |
| **F4** | 调度方法（随机度/最短/最长/均匀 ≥1 种） = f(网络状态, 总时间, 冗余包数量) | AVERTP "基于实时流质量计算动态切换协议（TCP/QUIC/AVERTP）"是协议层切换，**不是冗余包发送时间分布的调度**；公开材料未提随机/最短/最长/均匀任一具体调度模式。 | 未确认命中（无证据 ≠ 反向，但属"未公开" → 不计入命中） |
| **F5** | 按调度方法发送冗余包（n≥1） | ZEGO 公开声明使用 FEC（前向纠错），即"发送前主动生成冗余副本"；AVERTP 在 70%-80% 丢包仍连通主要靠 FEC + 重传组合。 | 命中（FEC 主动冗余存在） |

**命中合计**：F5 命中 1 项；F2 部分；F1 反向证据；F3 / F4 未确认。

## 已检查文档清单

1. https://blog.csdn.net/zego_0616/article/details/78803258  — zego_0616《实时语音视频 SDK 使用 FEC 和 ARQ 实现超低延迟》(2017-12)
2. https://www.cnblogs.com/zegoinfo/p/17773031.html  — ZEGO 音视频服务的高可用架构设计与运营
3. https://www.zegocloud.com/blog/upgrade-your-live-streaming-for-diverse-scenarios-with-scene-specific-settings  — Scene-Specific Settings 博文
4. https://www.zegocloud.com/docs/video-call/scene-based-video-config?platform=android&language=java  — Android 场景化音视频配置 overview 页
5. https://blog.csdn.net/zego_0616/article/details/134878167  — WebRTC 概述｜QOS 技术
6. (Phase 1 search 命中) https://segmentfault.com/a/1190000041496387  — ZEGO 支撑 100 亿场高质量直播的秘笈（仅取 search 摘要，未深抓）
7. (Phase 1 search 命中) https://www.cnblogs.com/zegoinfo/p/13903026.html  — 2020 系统架构师大会 ZEGO 实时音视频服务架构实践（仅取 search 摘要，未深抓）

## 最终判定

**第 3 档：弱嫌疑 / 需补证**

判定依据：
- ZEGO 在 FEC + 自适应抗丢包这个大方向上确实在做事，F5 显式命中（FEC 主动冗余包发送），AVERTP 也确有按网络状态动态调整码率与协议的能力。
- 但权 1 的核心限定 F1（**业务类型由发送端自动从数据流特征变量获取**）出现**反向证据** —— ZEGO 业务场景由应用层 setRoomScenario 静态枚举传入，对应权 1 从属权 4 的"应用制定业务类型"形态，不直接命中权 1。
- F2/F3/F4 在公开材料中均缺少"业务类型 / 时延要求 / 调度方式"作为冗余决策输入的明确表述，三元组联合无法核实。
- 因 SDK 闭源、公开博客深度不足，无法排除 ZEGO 内部 RTP 栈隐含按包统计做更细粒度业务分流的可能性 → 保留为"需补证"而非直接"已排除"。

**0 命中 ≠ 已排除：本候选并非 0 命中（F5 有命中、F2 部分），且存在确实的反向证据（F1 反证），落第 3 档而非第 5 档（已排除）。**

## 升级路径（3-4 档时）

可上调至**第 2 档（强嫌疑）**所需补证：
1. 取得 ZEGO Express SDK 二进制反汇编 / 符号信息，证明 SDK 内部除了 scenario 枚举外，**还**基于数据包到达间隔 / 突发性 / 缓存数目自动调整 FEC 冗余度。
2. 找到 ZEGO 技术博客或专利明确披露："冗余包数量 = f(丢包率, 业务类型, ...)"或"FEC 包发送时间窗 = f(端到端时延要求, n)"。
3. 找到 ZEGO 实际产品在不同 scenario 下抓包对比，证明同等网络条件下不同 scenario 的 FEC 冗余密度 / 调度时间分布显著不同（实证 F4 业务类型确实参与了冗余决策而不仅是码率决策）。
4. 找到 ZEGO 公开/泄露文档明确提到随机/最短/最长/均匀任一调度策略具体实现。

可下调至**第 4 档（已排除前的待澄清）**所需反证：
1. ZEGO 官方文档明确写：scenario 仅影响 codec/带宽/帧率，**不**影响 FEC 冗余包数量与调度方式（直接反证 F1+F2+F4 联合）。
2. ZEGO 公开声明其 FEC 实现仅按 PLR / 带宽自适应，不区分上层业务类型。

## 总结一句话

ZEGO Express RTC 公开使用 FEC + ARQ + AVERTP 自适应抗丢包（命中 F5），但业务场景由开发者通过 setRoomScenario 静态枚举传入（与权 1 F1"自动从数据流特征变量识别业务类型"形成反向证据），三元组联合 F2/F4 与时延总时间 F3 在公开材料中未确认，**落第 3 档：弱嫌疑 / 需补证**。

## 免责声明

本判定仅基于公开可访问材料的技术维度初步分析，不构成针对 ZEGO 及其客户的法律侵权结论。最终侵权认定需由权利人结合权利要求解释、SDK 反向工程证据、商业授权关系与司法程序综合判断。
