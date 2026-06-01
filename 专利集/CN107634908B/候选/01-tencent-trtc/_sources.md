# 01-tencent-trtc sources

## Phase 1 — WebSearch
- q1: `Tencent TRTC adaptive FEC packet loss redundancy ARS` → 命中 TRTC 多篇博客，确认 TRTC 使用 FEC + ARQ + 自适应抖动缓冲，可抗 ≤80% 丢包；未披露具体算法
- q2: `腾讯 TRTC ARS 自适应抗丢包 业务场景 冗余 算法` → 命中知乎/CSDN 中文技术博客，确认 TRTC 提供"多人实时互动(会议)"与"超低延时直播"两类业务场景方案，FEC 加冗余包(10→11/12)；冗余度算法细节未公开
- q3: `腾讯 TRTC FEC 冗余度 计算 网络状态 业务类型 场景` → 命中腾讯云官方文档与博客，确认 ARQ/FEC 依赖带宽预测，"以带宽换延时"；冗余度具体计算公式未披露
- q4: `TRTC setAppScene VideoCall LIVE scene FEC strategy difference` → **关键命中**：TRTC SDK 通过 `enterRoom(TRTCAppScene)` 由开发者**显式**指定 VideoCall / LIVE 场景，SDK 据此调整内部编码器 + 网络协议预设

## Phase 2 — WebFetch / curl
- https://trtc.io/document/47642 (WebFetch): 确认 `TRTCAppScene` 是 `enterRoom` 的显式参数；`setNetworkQosParam` 仅提供 smoothness vs quality 偏好开关；FEC/冗余策略细节未公开
- https://zhuanlan.zhihu.com/p/146643148 (WebFetch 403 → curl 兜底): 知乎 bot 防护(694 字节 JS stub)，落盘 `zhihu_146643148.html` 仅 stub，无可用内容
- https://www.cnblogs.com/ccloud/articles/13927052.html (WebFetch): 仅高层"QoS 流控系统调节算法"描述，未披露 FEC 冗余度 / 时间窗 / 调度策略算法细节
- https://brands.cnblogs.com/tencentcloud/p/20521 (WebFetch): 仅概览性提及 "实施前向纠错（FEC）和数据包丢失掩蔽"，无算法实现层细节
- https://trtc.io/document/36058 (WebFetch): **关键确认** —— "The `VideoCall` mode is optimized for video calls" 等表述表明 SDK 根据**开发者设置**的 `TRTCAppScene` 调整策略；无任何基于数据流特征自动识别业务类型的描述
- https://github.com/Tencent-RTC/TRTC_Android (WebFetch): README 仅高层目录与样例分类，无 FEC/调度/QoS 公式细节

## 工具受限说明
- 知乎 `p/146643148` 受 zse-ck JS 防护拦截，WebFetch 与 curl(浏览器 UA) 均仅返回 JS stub，无法读取正文 — 已在候选目录保留 `zhihu_146643148.html` stub 作为留痕
