# 10-zego-rtc _sources

## Phase 1 WebSearch

1. q1 = `即构 ZEGO FEC 自适应 抗丢包 业务类型`
   - https://blog.csdn.net/zego_0616/article/details/78803258  （zego_0616：实时语音视频 SDK 使用 FEC 和 ARQ 实现超低延迟，2017-12）
   - https://www.cnblogs.com/zegoinfo/p/17773031.html  （ZEGO 音视频服务高可用架构）
   - https://brands.cnblogs.com/zego  （ZEGO 即构博客园专区入口）

2. q2 = `ZEGO Express SDK scene profile setRoomScenario 业务场景 参数`
   - https://www.zegocloud.com/docs/video-call/scene-based-video-config?platform=android&language=java  （Android 场景化音视频配置）
   - https://www.zegocloud.com/blog/upgrade-your-live-streaming-for-diverse-scenarios-with-scene-specific-settings  （Scene-Specific Settings 博文）
   - https://docs.zegocloud.com/article/3557  （Express-Video SDK API Reference）

3. q3 = `zego_0616 实时语音视频SDK FEC ARQ 超低延迟 CSDN 数据流`
   - https://blog.csdn.net/zego_0616/article/details/78803258
   - https://blog.csdn.net/zego_0616/article/details/134878167  （WebRTC 概述｜QOS 技术）

4. q4 = `ZEGO AVERTP 媒体协议 业务特性 传输层 优化 FEC 重传 自适应`
   - https://segmentfault.com/a/1190000041496387  （ZEGO 支撑 100 亿场高质量直播的秘笈）
   - https://www.cnblogs.com/zegoinfo/p/13903026.html  （2020 系统架构师大会：ZEGO 实时音视频服务架构实践）

## Phase 2 WebFetch

| # | URL | 目的 | 结果 |
|---|-----|------|------|
| 1 | https://blog.csdn.net/zego_0616/article/details/78803258 | 抓 zego_0616 FEC+ARQ 老博客的实现细节（F1-F5） | 仅讨论 FEC 冗余度按 PLR 设置 + RS(n,k) + ARQ deadline；**未涉及业务类型输入 / 调度方法枚举 / 自动识别业务类型** |
| 2 | https://www.cnblogs.com/zegoinfo/p/17773031.html | 抓高可用架构文 看是否含包级 FEC 调度 | 全文聚焦机房 / 链路冗余与智能路由，**未提包级 FEC/ARQ 冗余策略** |
| 3 | https://www.zegocloud.com/blog/upgrade-your-live-streaming-for-diverse-scenarios-with-scene-specific-settings | 抓 scene-specific 博文 确认 scenario 来源 | scenario 枚举（Broadcast / StandardVideoCall / HighQualityVideoCall / Karaoke 等）；**"developer explicitly configures it", "no automatic detection mentioned"** |
| 4 | https://www.zegocloud.com/docs/video-call/scene-based-video-config?platform=android&language=java | 抓 Android setRoomScenario 文档 | WebFetch 拿到的是 overview 页非完整 API 页；未含 setRoomScenario 自动识别相关描述 |
| 5 | https://blog.csdn.net/zego_0616/article/details/134878167 | 抓 ZEGO WebRTC QOS 博文 看 FEC 输入变量 | 仅提 ULPFEC/FLEXFEC 概念；**未涉及业务类型 / 包到达间隔 / 数据突发性 / 缓存数目 等本专利 F1 关键变量** |

## 工具受限明示

- 仅做 5 次 WebFetch（Phase 2 限 6 次），未对 segmentfault / cnblogs/13903026 / Express-Video SDK API Reference 详细抓取。
- 未做 curl 兜底，因 WebFetch 均成功返回 markdown。
- 未直接读 ZEGO 商业 SDK 源码（闭源），技术细节限公开博客 / 文档可达部分。
