# 01-tencent-trtc verdict

## 候选基本信息
- 名称：TRTC（腾讯实时音视频）
- 组织：腾讯云
- 类型：产品
- 初判命中 F#：F1, F2, F3, F4, F5
- 专利公开（授权）日：2021-06-08

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1 | 反向证据 | "The developer calls the `enterRoom` method with the `TRTCAppScene` parameter to specify the scenario."；"The `VideoCall` mode is optimized for video calls, so when there is only one user in a room, TRTC tends to maintain a low bitrate and frame rate to reduce traffic usage" | https://trtc.io/document/47642 ; https://trtc.io/document/36058 | TRTC 业务场景由开发者通过 `enterRoom(TRTCAppScene)` **应用层显式传入**(VideoCall / LIVE)，非"基于发送端缓存包长度/数目、网络中包长度/数目、到达间隔、突发性等数据流特征变量自动识别"。这正是权 1 F1 限定中明示排除的"应用制定的业务类型"(从属权 4)形态。**真反向证据**(不是限定语) |
| F2 | 公开资料不足 | "TRTC通过FEC技术来优化网络抗性，本来要发10个包，为了防止丢包，发的时候可能发11或12个包"；"利用ARQ和FEC机制的基础，需要有准确的带宽预测" | (q2/q3 搜索引用) | 公开资料确认 FEC 冗余度由 ARS 基于丢包率 + 带宽(网络状态)调整，但未披露"业务类型"是否作为第 3 个输入参与冗余包数量公式。鉴于 F1 已认定业务类型源自应用层 hint 而非数据流特征，即便代入 F2 也只对应权 1 从属权形态、不对应权 1 F2 的"网络状态 + 成功率 + 业务类型"三元组要求 |
| F3 | 公开资料不足 | "TRTC ... can keep the latency as low as 100 ms" | https://trtc.io/document/36058 | 仅公开端到端时延目标(~100ms / ~1s)，未披露冗余包传输**总时间**是否由 per-stream 时延要求(deadline)推导 |
| F4 | 公开资料不足 | "QoS流控系统 ... 内部设置了很多调节算法和调控策略" | https://www.cnblogs.com/ccloud/articles/13927052.html | 公开资料未披露 TRTC 是否在"随机/均匀/最短/最长"等冗余包调度方式间动态选择，亦未披露选择是否基于"网络状态 + 总时间 + 冗余包数量"三元组联合决定 |
| F5 | 字面命中 | "TRTC通过FEC技术来优化网络抗性，本来要发10个包 ... 发的时候可能发11或12个包，多出来的这几个包就是做冗余数据校验的" | (q2 搜索引用 知乎 p/1910993857153331687 等) | TRTC 确实在发送侧主动发送 FEC 冗余包(非纯 ARQ 被动重传)，F5"按调度方法发送冗余包"的发送动作本身字面命中 |

## 已检查文档清单
- TRTC App Scene Parameter 官方文档(https://trtc.io/document/47642) — 确认 `enterRoom(TRTCAppScene)` 为开发者显式设置
- TRTC vs Interactive Live Streaming 官方文档(https://trtc.io/document/36058) — 确认 SDK 行为依据开发者设置的 scene 调整，未涉及数据流特征自动识别
- 腾讯云 RTC 实时音视频技术内幕揭秘(cnblogs/ccloud)(https://www.cnblogs.com/ccloud/articles/13927052.html) — 仅高层 QoS 流控描述，无算法细节
- 实时通信优化探索 吞吐量与延迟的最佳平衡(brands.cnblogs.com/tencentcloud)(https://brands.cnblogs.com/tencentcloud/p/20521) — 仅概览性提及 FEC + 数据包丢失掩蔽
- TRTC_Android GitHub README(https://github.com/Tencent-RTC/TRTC_Android) — README 无 QoS / FEC 算法层信息
- 知乎《日均超 30 亿分钟！腾讯实时音视频技术低延时的秘密》(https://zhuanlan.zhihu.com/p/146643148) — 受 zse-ck JS 防护拦截，WebFetch + curl 浏览器 UA 兜底均失败，正文不可读

## 最终判定

**第 5 档：已排除**

判定依据(基于 F# 命中分布)：

TRTC 在 F1 上有**真反向证据**(非作用域限定语)：业务场景由开发者经 `enterRoom(TRTCAppScene)` 应用层显式传入，明确属于权 1 F1 限定中点名排除的"应用制定的业务类型"形态(对应从属权 4，而非权 1)。权 1 F2 中"业务类型"输入因此同样不命中。F5 虽字面命中(发送 FEC 冗余包)、F3/F4 公开资料不足，但 F1 反向证据已足以触发第 5 档 (a) 条件 "≥1 条 F# 有真反向证据"。

## 升级路径
不适用(第 5 档无需升级)。如要质疑反向证据，需取证：TRTC 内部是否另有一条不暴露给 SDK 用户的、基于数据流特征(缓存包长度/数目、网络中包长度/数目、到达间隔、突发性)自动识别业务类型的隐藏算法链路，并把该自动识别结果作为 FEC 冗余度公式的第 3 个输入。这种证据通常仅通过：(1) 反向工程 TRTC SDK 二进制 + 抓包对比配置 LIVE vs VideoCall 时 FEC 行为对相同数据流的差异；(2) 腾讯内部专利 / 论文披露同等机制；(3) 腾讯工程师公开技术演讲披露内部第二层场景识别 — 等渠道获取。

## 总结一句话

候选 01-tencent-trtc 落第 5 档(已排除)：TRTC 业务场景由开发者经 `enterRoom(TRTCAppScene)` 应用层显式传入，构成对权 1 F1"基于数据流特征变量识别业务类型"限定的真反向证据(对应被权 1 排除的从属权 4 形态)。
